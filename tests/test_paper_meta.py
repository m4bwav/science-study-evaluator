"""Offline tests for skills/science-study-evaluator/scripts/paper_meta.py.

Run from the repository root: python tests/test_paper_meta.py
Every response is an invented fixture served by a fake fetcher, so the suite needs no network.
Set SSE_LIVE=1 to add one smoke test against the real APIs.
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "science-study-evaluator", "scripts"))
import paper_meta as pm  # noqa: E402

pm.NCBI_DELAY = 0

DOI = "10.1234/example.5678"

CROSSREF = {"message": {
    "DOI": DOI, "title": ["An invented trial of something"], "container-title": ["Journal of Examples"],
    "publisher": "Example Press", "type": "journal-article",
    "published": {"date-parts": [[2026, 3, 9]]}, "published-online": {"date-parts": [[2026, 3, 1]]},
    "assertion": [{"name": "received", "value": "2025-10-01"}, {"name": "accepted", "value": "2026-02-02"},
                  {"name": "other", "value": "x"}],
    "author": [{"given": "Ada", "family": "Example", "affiliation": [{"name": "Uni A"}, {"name": "SupplementCo"}]},
               {"given": "Bo", "family": "Sample", "affiliation": []}],
    "funder": [{"name": "Fund X"}, {"name": "Fund X"}, {"name": "Fund Y"}],
    "updated-by": [{"type": "retraction", "DOI": "10.1234/retraction.1", "source": "retraction-watch",
                    "updated": {"date-parts": [[2026, 9, 1]]}}],
    "abstract": "<jats:p>We <jats:italic>found</jats:italic> things.</jats:p>",
    "reference": [{"DOI": "10.1/a", "unstructured": "Ref A"}, {"unstructured": "Ref B"}],
}}

UNPAYWALL = {"is_oa": True, "oa_status": "green", "oa_locations": [
    {"host_type": "repository", "version": "acceptedVersion", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC999/"}]}

PUBMED_XML = """<?xml version="1.0"?><PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>111</PMID>
<Article><Abstract><AbstractText Label="BACKGROUND">Why.</AbstractText><AbstractText Label="RESULTS">d = 0.2 (95% CI <i>0.1</i> to 0.3).</AbstractText></Abstract>
<GrantList><Grant><Agency>Agency Z</Agency></Grant><Grant><Agency>Agency Z</Agency></Grant></GrantList>
<PublicationTypeList><PublicationType>Journal Article</PublicationType><PublicationType>Randomized Controlled Trial</PublicationType></PublicationTypeList>
</Article><CoiStatement>A.E. consults for SupplementCo.</CoiStatement>
<CommentsCorrectionsList><CommentsCorrections RefType="ErratumIn"><RefSource>J Ex 2026;2:3</RefSource><PMID>222</PMID></CommentsCorrections>
<CommentsCorrections RefType="Cites"><RefSource>ignored</RefSource></CommentsCorrections></CommentsCorrectionsList>
</MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="pubmed">111</ArticleId><ArticleId IdType="doi">10.1234/example.5678</ArticleId>
<ArticleId IdType="pmc">PMC999</ArticleId></ArticleIdList>
<ReferenceList><Reference><Citation>A cited paper.</Citation><ArticleIdList><ArticleId IdType="doi">10.9999/cited</ArticleId>
<ArticleId IdType="pmc">PMC555</ArticleId></ArticleIdList></Reference></ReferenceList></PubmedData></PubmedArticle></PubmedArticleSet>"""

ELINK = {"linksets": [{"linksetdbs": [{"links": ["111", "333", "444"]}]}]}
ESUMMARY = {"result": {"333": {"sortfirstauthor": "Sib A", "source": "Epi J", "pubdate": "2026", "title": "A sibling study"},
                       "444": {"sortfirstauthor": "Neg B", "source": "Epi J", "pubdate": "2025", "title": "A negative control"}}}

JATS = """<article><front><article-meta><title-group><article-title>An invented trial</article-title></title-group>
<abstract abstract-type="teaser"><p>Short version.</p></abstract><abstract><p>Long version.</p></abstract></article-meta></front>
<body><sec><title>Methods</title><p>We randomised 40 people.</p><sec><title>Outcomes</title><p>Primary: compliance.</p>
<list><list-item><p>item one</p></list-item></list></sec>
<table-wrap><label>Table 1</label><caption><p>Results</p></caption><table><tr><th>Arm</th><th>n</th></tr><tr><td>A</td><td>20</td></tr></table></table-wrap></sec></body>
<back><ack><title>Acknowledgements</title><p>Thanks.</p></ack><fn-group><fn><p>Competing interests: none.</p></fn></fn-group></back></article>"""


class FakeFetcher(pm.Fetcher):
    """Serves fixtures by URL substring; records every URL asked for."""

    def __init__(self, routes, email="t@example.org"):
        super().__init__(email)
        self.routes, self.urls = routes, []

    def get(self, url):
        self.urls.append(url)
        for key, val in self.routes.items():
            if key in url:
                if isinstance(val, Exception):
                    raise val
                return val if isinstance(val, str) else json.dumps(val)
        raise pm.FetchError(f"{url}: HTTP Error 404")


def full_routes(**over):
    r = {"api.crossref.org": CROSSREF, "api.unpaywall.org": UNPAYWALL,
         "esearch.fcgi": {"esearchresult": {"idlist": ["111"]}}, "efetch.fcgi": PUBMED_XML,
         "elink.fcgi": ELINK, "esummary.fcgi": ESUMMARY, "fullTextXML": JATS}
    r.update(over)
    return r


class ParseIdentifier(unittest.TestCase):
    def test_forms(self):
        cases = {
            DOI: ("doi", DOI),
            f"https://doi.org/{DOI}": ("doi", DOI),
            f"https://onlinelibrary.wiley.com/doi/full/{DOI}": ("doi", DOI),
            f"https://example.org/doi/{DOI}/full": ("doi", DOI),
            f"see {DOI}.": ("doi", DOI),
            "https://doi.org/10.1000%2Fabc%28x%29": ("doi", "10.1000/abc(x)"),
            "(10.1016/S0140-6736(20)30183-5)": ("doi", "10.1016/S0140-6736(20)30183-5"),
            "PMID: 42566467": ("pmid", "42566467"),
            "42566467": ("pmid", "42566467"),
            "https://pubmed.ncbi.nlm.nih.gov/42566467/": ("pmid", "42566467"),
            "pmc13462932": ("pmcid", "PMC13462932"),
        }
        for text, want in cases.items():
            with self.subTest(text=text):
                self.assertEqual(pm.parse_identifier(text), want)

    def test_rejects(self):
        with self.assertRaises(ValueError):
            pm.parse_identifier("nothing here")


class Sources(unittest.TestCase):
    def test_crossref(self):
        f = FakeFetcher(full_routes())
        c = pm.crossref(f, DOI, refs=True)
        self.assertEqual(c["published"], "2026-03-09")
        self.assertEqual(c["milestones"], {"received": "2025-10-01", "accepted": "2026-02-02"})
        self.assertEqual(c["authors"][0]["affiliations"], ["Uni A", "SupplementCo"])
        self.assertEqual(c["funders"], ["Fund X", "Fund Y"])
        self.assertEqual(c["abstract"], "We found things.")
        self.assertEqual(c["updates"][0]["type"], "retraction")
        self.assertEqual(c["updates"][0]["date"], "2026-09-01")
        self.assertEqual(len(c["references"]), 2)

    def test_unpaywall_pmcid(self):
        u = pm.unpaywall(FakeFetcher(full_routes()), DOI)
        self.assertEqual(u["pmcid"], "PMC999")
        self.assertTrue(u["is_oa"])

    def test_pubmed_xml(self):
        p = pm.parse_pubmed_xml(PUBMED_XML)
        self.assertEqual((p["pmid"], p["pmcid"], p["doi"]), ("111", "PMC999", DOI))
        self.assertEqual(p["abstract"][1], {"label": "RESULTS", "text": "d = 0.2 (95% CI 0.1 to 0.3)."})
        self.assertIn("SupplementCo", p["coi"])
        self.assertEqual(p["grants"], ["Agency Z"])
        self.assertEqual([n["type"] for n in p["notices"]], ["ErratumIn"])

    def test_similar_skips_self(self):
        p = pm.pubmed(FakeFetcher(full_routes()), "111", 5)
        self.assertEqual([s["pmid"] for s in p["similar"]], ["333", "444"])

    def test_ncbi_params(self):
        f = FakeFetcher(full_routes())
        pm.pubmed(f, "111", 0)
        self.assertIn("tool=science-study-evaluator", f.urls[0])
        self.assertIn("email=t%40example.org", f.urls[0])


class Collect(unittest.TestCase):
    def test_doi_full_run(self):
        with tempfile.TemporaryDirectory() as d:
            r = pm.collect(DOI, fulltext_dir=d, fetcher=FakeFetcher(full_routes()))
            self.assertEqual(r["errors"], {})
            self.assertEqual(r["pmcid"], "PMC999")
            self.assertTrue(os.path.exists(r["fulltext"]["txt"]))
            self.assertTrue(r["next"][0].startswith("INTEGRITY NOTICE"))
            self.assertTrue(any("grep" in s for s in r["next"]))

    def test_no_email_skips_unpaywall(self):
        f = FakeFetcher(full_routes(), email=None)
        r = pm.collect(DOI, fetcher=f)
        self.assertNotIn("unpaywall", r)
        self.assertIn("skipped", r["errors"]["unpaywall"])
        self.assertFalse(any("unpaywall" in u for u in f.urls))

    def test_not_in_pubmed(self):
        routes = full_routes(**{"esearch.fcgi": {"esearchresult": {"idlist": []}}, "api.unpaywall.org":
                                {"is_oa": False, "oa_locations": []}})
        r = pm.collect(DOI, fetcher=FakeFetcher(routes))
        self.assertIn("no PMID", r["errors"]["pubmed"])
        self.assertIsNone(r["pmcid"])
        self.assertTrue(any("abstract level" in s for s in r["next"]))

    def test_pmid_input_finds_doi(self):
        r = pm.collect("PMID:111", fetcher=FakeFetcher(full_routes()))
        self.assertEqual(r["doi"], DOI)
        self.assertIn("crossref", r)

    def test_crossref_down_still_reports(self):
        r = pm.collect(DOI, fetcher=FakeFetcher(full_routes(**{"api.crossref.org": pm.FetchError("503")})))
        self.assertIn("crossref", r["errors"])
        self.assertIn("pubmed", r)
        self.assertIn("== CROSSREF\n503", pm.render_text(r))


class FullText(unittest.TestCase):
    def test_jats(self):
        t = pm.jats_to_text(JATS)
        self.assertIn("# An invented trial", t)
        self.assertIn("## Teaser", t)
        self.assertIn("## Methods", t)
        self.assertIn("### Outcomes", t)
        self.assertIn("- item one", t)
        self.assertIn("[Table 1] Results", t)
        self.assertIn("A\t20", t)
        self.assertIn("## Acknowledgements", t)
        self.assertEqual(t.count("Competing interests: none."), 1)


class Cli(unittest.TestCase):
    def test_bad_input_exit_2(self):
        err = io.StringIO()
        with redirect_stdout(io.StringIO()):
            sys.stderr, old = err, sys.stderr
            try:
                self.assertEqual(pm.main(["nothing"]), 2)
            finally:
                sys.stderr = old

    def test_json_output(self):
        orig = pm.Fetcher
        pm.Fetcher = lambda email, timeout: FakeFetcher(full_routes(), email)
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                code = pm.main([DOI, "--json", "--email", "t@example.org"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue())["crossref"]["journal"], "Journal of Examples")
        finally:
            pm.Fetcher = orig


@unittest.skipUnless(os.environ.get("SSE_LIVE"), "set SSE_LIVE=1 for the live smoke test")
class Live(unittest.TestCase):
    def test_real_paper(self):
        r = pm.collect("10.1073/pnas.2528246123", n_similar=0)
        self.assertIn("Protecting episodic memory", r["crossref"]["title"])
        self.assertTrue(r["pmcid"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
