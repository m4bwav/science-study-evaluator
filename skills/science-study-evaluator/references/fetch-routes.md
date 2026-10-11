# Fetch routes: getting the paper, not the press release

Read by [SKILL.md](../SKILL.md) at Step 1 when the script can't run or a fetch fails. Each route here was tried on real appraisals; the dates and evidence are in [LEARNINGS.md](../LEARNINGS.md). Sites change their bot rules, so a route that fails twice in a row is a new lesson, not a reason to retry a third time.

## Order of attempts

1. **`scripts/paper_meta.py <DOI>`** wherever the agent can run Python with open internet (a terminal agent on the user's machine). One call gives the citation check, open-access copies, the PubMed record and similar articles. With `--fulltext DIR` it also saves the whole article from Europe PMC when an open PMC copy exists, as XML and as plain text with headings, tables and the competing-interests note. Grep the `.txt` for what you need (n per arm, the primary outcome, "limitation", "competing") rather than reading 9,000 words into context. (L-009)
2. **Europe PMC full text** when the paper has a PMC ID: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC<id>/fullTextXML` returns the whole article in one request, even for publishers that bot-wall their own sites. It rate-limits (HTTP 429) on rapid repeats: one paper at a time, a few seconds apart. (L-002)
3. **The PDF or page itself** for working papers, institutional repositories and preprint servers: a plain web fetch usually works. Give it one numbered extraction prompt (sample size, design, outcome, effect sizes with CIs, controls, causal language, funding, COI) instead of several fetches. (L-002)
4. **A real browser** (a browser-automation tool or the user's own browser) for commercial publisher domains, which block scripted fetchers. (L-001, L-002)
5. **Abstract level** when the paper stays closed: say so in the verdict, grade on the Crossref or PubMed abstract plus what the outlet article reports, and name the one number the reader should look for if they get the PDF. (L-001)

## Without the script

Hosted chat apps and sandboxes often block outbound requests, and some proxies reject the scholarly APIs while the agent's own web-fetch tool reaches them. Then:

- Citation check: web-fetch `https://api.crossref.org/works/<DOI>`. The record carries authors, affiliations, received and accepted dates, the abstract when deposited, funders, and retraction and correction notices (Retraction Watch data has been in the Crossref API since January 2025).
- Open copies: web-fetch `https://api.unpaywall.org/v2/<DOI>?email=<a contact address>`; the PMC ID is in `oa_locations`.
- PubMed: the NCBI E-utilities API is disallowed by robots.txt for many fetch tools. The PubMed web page (`https://pubmed.ncbi.nlm.nih.gov/?term=<title words>`) in a browser gives the structured abstract, the COI statement and the similar-articles list in one read.

## Known blocks (checked 2026-09 to 2026-10)

| Site | What happens | Route instead |
|---|---|---|
| Wiley, SAGE (`onlinelibrary.wiley.com`, `journals.sagepub.com`) | Cloudflare human check; fetch tools get 403 or an empty page, a browser may clear after a minute, then `/doi/full/` often redirects to the paywalled abstract | Crossref plus Europe PMC; for journals outside MEDLINE (most social science), abstract level after one browser try. Never click through a human-verification check for the user. |
| Elsevier journal sites (`10.1016/...`) | 403 to fetch tools and to scripted curl with a browser User-Agent | Europe PMC if older than about two months; otherwise a real browser on the `/fulltext` URL |
| `pmc.ncbi.nlm.nih.gov` | reCAPTCHA interstitial to fetch tools | Europe PMC `fullTextXML` for the same PMC ID |
| `clinicaltrials.gov` (pages and the v2 API) | robots.txt disallows fetch tools | The trial's published protocol paper (search `"<NCT number>" protocol`); it carries the power statement and analysis plan in the authors' words, which is better evidence than the registry. A browser can still load the registry page. |
| `reddit.com` | Blocked to fetch tools | An r/science title is the outlet's headline verbatim (subreddit rule), so search it in quotes and appraise the outlet article; say in Sources that the post itself was not read. |
| `osf.io` (SocArXiv, PsyArXiv) | The page is a JavaScript shell; `api.osf.io` is robots-disallowed to fetch tools | `https://api.osf.io/v2/preprints/<id>/` from a script on the user's machine. Check the title: a hit on "<author> <topic> SocArXiv" is usually the author's other work. |

## Publication status

Crossref and RePEc lag badly in economics and the quantitative social sciences, where one working paper can circulate for years under several series DOIs (ISER, IZA, IFS, NBER, CEPR) with no crosswalk to the journal version. The corresponding author's own homepage or CV is usually the only place that says "accepted at <journal>" or "forthcoming". Check it before calling a paper a preprint, and whenever the article under review is more than a few months old. (L-007)
