#!/usr/bin/env python3
"""paper_meta.py: one-call metadata pull for appraising a scientific paper.

Usage:
  python paper_meta.py <DOI | doi.org URL | article URL | PMID:123 | PMC123> [options]

Options:
  --refs           list the deposited reference list (Crossref)
  --similar N      PubMed similar articles to list (default 8, 0 to skip)
  --fulltext DIR   when an open PMC copy exists, save the whole article from Europe PMC
                   to DIR as PMC<id>.xml and a plain-text PMC<id>.txt (grep the .txt)
  --json           print one JSON object instead of text
  --email ADDR     contact address for Unpaywall and NCBI (or set SSE_EMAIL);
                   without one, Unpaywall is skipped
  --timeout S      seconds per request (default 30)
  --version

One run replaces four to eight separate fetches: the Crossref record (authors,
affiliations, received and accepted dates, abstract, funders, retraction and
correction notices, which include Retraction Watch data), Unpaywall's open-access
copies, the PubMed record (PMID, PMCID, structured abstract, COI statement,
grants, retraction and erratum links) and PubMed's similar-articles list, where
companion and contradicting studies usually turn up. The NEXT section names the
cheapest route to the full text.

Standard library only, Python 3.10 or newer. It reads public APIs and writes
nothing unless --fulltext is given. Exit codes: 0 ok, 1 nothing found, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

VERSION = "0.1.0"
REPO = "https://github.com/m4bwav/science-study-evaluator"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
NCBI_DELAY = 0.35  # NCBI allows 3 requests a second without an API key

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+")
PMC_RE = re.compile(r"\bPMC\d+\b", re.I)


# ---------------------------------------------------------------- fetching

class Fetcher:
    """HTTP GET with a polite User-Agent and backoff. Tests replace `get`."""

    def __init__(self, email: str | None = None, timeout: float = 30, tries: int = 3):
        self.email = email
        self.timeout = timeout
        self.tries = tries
        contact = f"; mailto:{email}" if email else ""
        self.headers = {"User-Agent": f"science-study-evaluator/{VERSION} (+{REPO}{contact})"}

    def get(self, url: str) -> str:
        last = None
        for i in range(self.tries):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    return r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                last = e
                if e.code == 404:
                    break
                if e.code not in (429, 500, 502, 503, 504):
                    break
            except Exception as e:  # timeouts, resets
                last = e
            if i < self.tries - 1:
                time.sleep(2 * (i + 1))
        raise FetchError(f"{url}: {last}")

    def json(self, url: str) -> dict:
        return json.loads(self.get(url))


class FetchError(Exception):
    pass


# ---------------------------------------------------------------- parsing input

def parse_identifier(text: str) -> tuple[str, str]:
    """Return ("doi", "10.x/y"), ("pmid", "123") or ("pmcid", "PMC123")."""
    s = urllib.parse.unquote(text.strip())
    m = re.fullmatch(r"(?:pmid:?\s*)(\d{1,9})", s, re.I) or re.search(
        r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{1,9})", s)
    if m:
        return "pmid", m.group(1)
    if re.fullmatch(r"\d{1,9}", s):
        return "pmid", s
    m = DOI_RE.search(s)
    if m:
        doi = m.group(0)
        # trailing punctuation and URL tails that are never part of a DOI
        doi = re.sub(r"(?:/(?:full|abstract|pdf|epdf|fulltext|html))+/?$", "", doi, flags=re.I)
        while doi and doi[-1] in ".,;:]}>" or (doi.endswith(")") and doi.count(")") > doi.count("(")):
            doi = doi[:-1]
        return "doi", doi
    m = PMC_RE.search(s)
    if m:
        return "pmcid", m.group(0).upper()
    raise ValueError(f"no DOI, PMID or PMCID found in {text!r}")


def strip_tags(s: str | None) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def _date(m: dict, key: str) -> str | None:
    parts = (m.get(key) or {}).get("date-parts") or [[None]]
    p = [x for x in parts[0] if x is not None]
    return "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(p)) or None


# ---------------------------------------------------------------- sources

def crossref(f: Fetcher, doi: str, refs: bool = False) -> dict:
    m = f.json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")["message"]
    out = {
        "doi": m.get("DOI", doi),
        "title": (m.get("title") or [""])[0],
        "journal": (m.get("container-title") or [""])[0],
        "publisher": m.get("publisher"),
        "type": m.get("type"),
        "published": _date(m, "published"),
        "published_online": _date(m, "published-online"),
        "milestones": {a["name"]: a.get("value") for a in m.get("assertion", [])
                       if a.get("name") in ("received", "revised", "accepted", "published")},
        "authors": [{"name": " ".join(filter(None, [a.get("given"), a.get("family")])) or a.get("name", ""),
                     "affiliations": [x.get("name", "") for x in a.get("affiliation", [])],
                     "orcid": a.get("ORCID")} for a in m.get("author", [])],
        "funders": list(dict.fromkeys(x.get("name", "") for x in m.get("funder", []))),
        "updates": [],
        "relations": {k: [x.get("id") for x in v] for k, v in (m.get("relation") or {}).items()},
        "license": (m.get("license") or [{}])[0].get("URL"),
        "abstract": strip_tags(m.get("abstract")),
        "reference_count": len(m.get("reference", [])),
    }
    # update-to: this record is a notice about another; updated-by: notices about this one
    for key, direction in (("update-to", "this record updates"), ("updated-by", "updated by")):
        for u in m.get(key, []) or []:
            out["updates"].append({"direction": direction, "type": u.get("type"),
                                   "doi": u.get("DOI"), "label": u.get("label"),
                                   "source": u.get("source"),
                                   "date": _date(u, "updated")})
    if refs:
        out["references"] = [{"doi": r.get("DOI"), "text": strip_tags(r.get("unstructured"))[:200]}
                             for r in m.get("reference", [])]
    return out


def unpaywall(f: Fetcher, doi: str) -> dict:
    d = f.json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(f.email or '')}")
    locs, pmcid = [], None
    for loc in d.get("oa_locations") or []:
        url = loc.get("url") or ""
        locs.append({"host_type": loc.get("host_type"), "version": loc.get("version"),
                     "url": url, "license": loc.get("license")})
        mm = PMC_RE.search(url)
        pmcid = pmcid or (mm.group(0).upper() if mm else None)
    return {"is_oa": d.get("is_oa"), "oa_status": d.get("oa_status"), "locations": locs, "pmcid": pmcid}


def _eutils(f: Fetcher, tool: str, params: dict) -> str:
    q = dict(params, tool="science-study-evaluator")
    if f.email:
        q["email"] = f.email
    if os.environ.get("NCBI_API_KEY"):
        q["api_key"] = os.environ["NCBI_API_KEY"]
    time.sleep(NCBI_DELAY)
    return f.get(f"{EUTILS}/{tool}.fcgi?{urllib.parse.urlencode(q)}")


def pubmed_find(f: Fetcher, kind: str, value: str) -> str | None:
    if kind == "pmid":
        return value
    term = f"{value}[doi]" if kind == "doi" else f"{value}[pmcid]"
    s = json.loads(_eutils(f, "esearch", {"db": "pubmed", "retmode": "json", "term": term}))
    ids = (s.get("esearchresult") or {}).get("idlist", [])
    return ids[0] if ids else None


def parse_pubmed_xml(x: str) -> dict:
    root = ET.fromstring(x)
    out = {"pmid": root.findtext(".//PMID"), "pub_types": [p.text for p in root.iter("PublicationType")],
           "pmcid": None, "doi": None, "abstract": [], "coi": None, "grants": [], "notices": []}
    for idn in root.iter("ArticleId"):
        if idn.get("IdType") == "pmc":
            out["pmcid"] = idn.text
        elif idn.get("IdType") == "doi" and not out["doi"]:
            out["doi"] = idn.text
    for t in root.iter("AbstractText"):
        out["abstract"].append({"label": t.get("Label"), "text": "".join(t.itertext()).strip()})
    coi = root.find(".//CoiStatement")
    if coi is not None:
        out["coi"] = "".join(coi.itertext()).strip()
    out["grants"] = sorted({g.findtext("Agency") for g in root.iter("Grant") if g.findtext("Agency")})
    for c in root.iter("CommentsCorrections"):
        if c.get("RefType") in ("RetractionIn", "RetractionOf", "ErratumIn", "ExpressionOfConcernIn",
                                "UpdateIn", "RepublishedIn", "CommentIn"):
            out["notices"].append({"type": c.get("RefType"), "source": c.findtext("RefSource"),
                                   "pmid": c.findtext("PMID")})
    return out


def pubmed(f: Fetcher, pmid: str, n_similar: int) -> dict:
    out = parse_pubmed_xml(_eutils(f, "efetch", {"db": "pubmed", "id": pmid, "retmode": "xml"}))
    out["similar"] = []
    if n_similar:
        try:
            link = json.loads(_eutils(f, "elink", {"dbfrom": "pubmed", "db": "pubmed", "id": pmid,
                                                   "linkname": "pubmed_pubmed", "retmode": "json"}))
            ids = [i for i in link["linksets"][0]["linksetdbs"][0]["links"] if i != pmid][:n_similar]
            if ids:
                summ = json.loads(_eutils(f, "esummary", {"db": "pubmed", "id": ",".join(ids),
                                                          "retmode": "json"}))["result"]
                for i in ids:
                    r = summ.get(i, {})
                    out["similar"].append({"pmid": i, "first_author": r.get("sortfirstauthor", ""),
                                           "journal": r.get("source", ""), "date": r.get("pubdate", ""),
                                           "title": r.get("title", "")})
        except (FetchError, KeyError, IndexError, ValueError) as e:
            out["similar_error"] = str(e)
    return out


# ---------------------------------------------------------------- full text

def jats_to_text(xml: str) -> str:
    """Plain text of a JATS article: abstract, sections with headings, tables, notes."""
    root = ET.fromstring(xml)
    lines: list[str] = []

    def text(el) -> str:
        return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

    title = root.find(".//article-title")
    if title is not None:
        lines += [f"# {text(title)}", ""]
    for ab in root.iter("abstract"):
        head = ab.findtext("title") or ab.get("abstract-type") or "Abstract"
        lines += [f"## {head.strip().capitalize()}", ""] + [text(p) for p in ab.iter("p")] + [""]

    containers = {"sec", "fn-group", "fn", "notes", "ack", "app", "app-group", "boxed-text", "glossary"}

    def walk(sec, depth):
        t = sec.find("title")
        if t is not None and text(t):
            lines.extend(["#" * min(depth, 6) + " " + text(t), ""])
        for child in sec:
            if child.tag == "p":
                lines.extend([text(child), ""])
            elif child.tag in containers:
                walk(child, depth + 1 if child.find("title") is not None else depth)
            elif child.tag == "list":
                lines.extend([f"- {text(li)}" for li in child.iter("list-item")] + [""])
            elif child.tag in ("table-wrap", "fig"):
                cap = child.find(".//caption")
                lab = child.findtext("label") or child.tag
                lines.append(f"[{lab}] {text(cap) if cap is not None else ''}".strip())
                for tr in child.iter("tr"):
                    lines.append("\t".join(text(c) for c in tr if c.tag in ("td", "th")))
                lines.append("")

    for part in (root.find(".//body"), root.find(".//back")):
        if part is not None:
            walk(part, 1)
    return "\n".join(lines).strip() + "\n"


def fulltext(f: Fetcher, pmcid: str, outdir: str) -> dict:
    xml = f.get(f"{EPMC}/{pmcid}/fullTextXML")
    os.makedirs(outdir, exist_ok=True)
    xml_path = os.path.join(outdir, f"{pmcid}.xml")
    txt_path = os.path.join(outdir, f"{pmcid}.txt")
    with open(xml_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(xml)
    txt = jats_to_text(xml)
    with open(txt_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    return {"xml": xml_path, "txt": txt_path, "words": len(txt.split())}


# ---------------------------------------------------------------- orchestration

def collect(identifier: str, email: str | None = None, refs: bool = False, n_similar: int = 8,
            fulltext_dir: str | None = None, fetcher: Fetcher | None = None) -> dict:
    f = fetcher or Fetcher(email)
    kind, value = parse_identifier(identifier)
    res: dict = {"input": identifier, "id_kind": kind, "id": value, "errors": {}}
    doi = value if kind == "doi" else None
    pmcid = value if kind == "pmcid" else None

    pmid = None
    try:
        pmid = pubmed_find(f, kind, value) if kind != "doi" else None
    except (FetchError, ValueError) as e:
        res["errors"]["pubmed"] = str(e)
    if pmid:
        try:
            res["pubmed"] = pubmed(f, pmid, n_similar)
            doi = doi or res["pubmed"].get("doi")
        except (FetchError, ET.ParseError) as e:
            res["errors"]["pubmed"] = str(e)

    if doi:
        try:
            res["crossref"] = crossref(f, doi, refs)
        except (FetchError, KeyError, ValueError) as e:
            res["errors"]["crossref"] = str(e)
        if f.email:
            try:
                res["unpaywall"] = unpaywall(f, doi)
            except (FetchError, ValueError) as e:
                res["errors"]["unpaywall"] = str(e)
        else:
            res["errors"]["unpaywall"] = "skipped: no contact email (pass --email or set SSE_EMAIL)"
        if "pubmed" not in res and "pubmed" not in res["errors"]:
            try:
                pmid = pubmed_find(f, "doi", doi)
                if pmid:
                    res["pubmed"] = pubmed(f, pmid, n_similar)
                else:
                    res["errors"]["pubmed"] = "no PMID (too new, or the journal is not indexed in PubMed)"
            except (FetchError, ValueError, ET.ParseError) as e:
                res["errors"]["pubmed"] = str(e)
    res["doi"] = doi

    pmcid = pmcid or (res.get("pubmed") or {}).get("pmcid") or (res.get("unpaywall") or {}).get("pmcid")
    res["pmcid"] = pmcid
    if fulltext_dir and pmcid:
        try:
            res["fulltext"] = fulltext(f, pmcid, fulltext_dir)
        except (FetchError, ET.ParseError, OSError) as e:
            res["errors"]["fulltext"] = str(e)
    res["next"] = next_steps(res)
    return res


def next_steps(res: dict) -> list[str]:
    steps = []
    if res.get("fulltext"):
        steps.append(f"Full text saved: grep {res['fulltext']['txt']} ({res['fulltext']['words']} words) "
                     "instead of reading it whole.")
    elif res.get("pmcid"):
        steps.append(f"Full text: fetch {EPMC}/{res['pmcid']}/fullTextXML (one call, the whole article), "
                     "or rerun with --fulltext DIR.")
    else:
        oa = [l["url"] for l in (res.get("unpaywall") or {}).get("locations", []) if l.get("url")]
        if oa:
            steps.append(f"Full text: open copy at {oa[0]} (fetch the PDF or page directly).")
        elif "unpaywall" not in res and res.get("doi"):
            steps.append("Open-copy check skipped (no email): rerun with --email or SSE_EMAIL, or try the "
                         "publisher page; if it stays closed, grade at abstract level and say so.")
        else:
            steps.append("No open copy found: try the publisher page in a real browser; if it stays closed, "
                         "grade at abstract level and say so.")
    upd = (res.get("crossref") or {}).get("updates") or []
    notices = (res.get("pubmed") or {}).get("notices") or []
    if any(u.get("type") in ("retraction", "expression_of_concern") for u in upd) or \
            any(n["type"] in ("RetractionIn", "ExpressionOfConcernIn") for n in notices):
        steps.insert(0, "INTEGRITY NOTICE on this record: read it before anything else.")
    if res.get("pubmed", {}).get("similar"):
        steps.append("Scan the similar articles for a companion paper from the same sample or a "
                     "contradicting design (sibling comparison, negative control).")
    return steps


# ---------------------------------------------------------------- output

def render_text(res: dict) -> str:
    o: list[str] = []
    cr = res.get("crossref")
    o.append("== CROSSREF")
    if cr:
        o.append(f"Title: {cr['title']}")
        o.append(f"Journal: {cr['journal']} | Publisher: {cr['publisher']} | Type: {cr['type']}")
        o.append(f"DOI: {cr['doi']} | Published: {cr['published']} | Online: {cr['published_online']}")
        for k, v in cr["milestones"].items():
            o.append(f"  {k}: {v}")
        o.append("Authors:")
        for a in cr["authors"]:
            aff = "; ".join(filter(None, a["affiliations"]))
            o.append(f"  - {a['name']}" + (f"  [{aff}]" if aff else ""))
        if cr["funders"]:
            o.append("Funders: " + "; ".join(cr["funders"]))
        for u in cr["updates"]:
            o.append(f"!! {u['direction']}: {u['type']} {u['doi']} ({u.get('source') or ''} {u.get('date') or ''})".rstrip())
        if cr["relations"]:
            o.append(f"Relations: {cr['relations']}")
        if cr["license"]:
            o.append(f"License: {cr['license']}")
        o.append("Abstract (Crossref): " + (cr["abstract"] or "(none deposited)"))
        o.append(f"References deposited: {cr['reference_count']}")
        for r in cr.get("references", []):
            o.append(f"  - {r['doi'] or ''} {r['text']}".rstrip())
    else:
        o.append(res["errors"].get("crossref", "(no DOI to look up)"))

    o.append("== UNPAYWALL")
    up = res.get("unpaywall")
    if up:
        o.append(f"is_oa: {up['is_oa']} | oa_status: {up['oa_status']}")
        for l in up["locations"]:
            o.append(f"  OA: {l['host_type']} {l['version']} {l['url']}")
    else:
        o.append(res["errors"].get("unpaywall", "(not run)"))

    o.append("== PUBMED")
    pm = res.get("pubmed")
    if pm:
        o.append(f"PMID: {pm['pmid']} | PMCID: {pm['pmcid'] or '(none yet)'} | Types: {', '.join(pm['pub_types'])}")
        o.append("Abstract (PubMed):")
        for a in pm["abstract"]:
            o.append(f"  {a['label']}: {a['text']}" if a["label"] else f"  {a['text']}")
        o.append("COI: " + (pm["coi"] or "(not in the PubMed record; check the paper)"))
        if pm["grants"]:
            o.append("Grants: " + "; ".join(pm["grants"]))
        for n in pm["notices"]:
            o.append(f"!! {n['type']}: {n['source']}")
        if pm["similar"]:
            o.append(f"Similar articles (top {len(pm['similar'])}):")
            for s in pm["similar"]:
                o.append(f"  - PMID {s['pmid']} | {s['first_author']} | {s['journal']} {s['date']} | {s['title']}")
        elif pm.get("similar_error"):
            o.append(f"Similar articles: unavailable ({pm['similar_error']})")
    else:
        o.append(res["errors"].get("pubmed", "(not run)"))

    if res["errors"].get("fulltext"):
        o.append(f"== FULLTEXT error: {res['errors']['fulltext']}")
    o.append("== NEXT")
    o.extend(res["next"])
    return "\n".join(o) + "\n"


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # accented author names on a Windows console
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(prog="paper_meta.py", description=__doc__.split("\n\n")[0])
    p.add_argument("identifier", help="DOI, doi.org or article URL, PMID:123 or PMC123")
    p.add_argument("--refs", action="store_true")
    p.add_argument("--similar", type=int, default=8)
    p.add_argument("--fulltext", metavar="DIR")
    p.add_argument("--json", action="store_true")
    p.add_argument("--email", default=os.environ.get("SSE_EMAIL"))
    p.add_argument("--timeout", type=float, default=30)
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    a = p.parse_args(argv)
    try:
        res = collect(a.identifier, a.email, a.refs, max(0, a.similar), a.fulltext,
                      Fetcher(a.email, a.timeout))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(res, indent=2, ensure_ascii=False) + "\n" if a.json else render_text(res))
    return 0 if (res.get("crossref") or res.get("pubmed")) else 1


if __name__ == "__main__":
    sys.exit(main())
