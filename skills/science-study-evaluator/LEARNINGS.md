# Learnings: science-study-evaluator

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); tests in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (Learnings section). Retired entries go to LEARNINGS-ARCHIVE.md with a reason. The retrieval lessons are condensed into [references/fetch-routes.md](references/fetch-routes.md); keep the two in step.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful. Appraisal-technique gaps are methodology edits, not learnings (SKILL.md, While working).

Entries before 2026-10-11 come from the skill's private use and keep their original numbers; the missing numbers (L-003, L-005, L-006, L-010) were lessons about one machine and one app's tooling that do not apply to other installs.

## Active

### L-001 · 2026-09-02 · Wiley and SAGE sit behind a Cloudflare human check; get the metadata from Crossref instead
- Trigger: appraising 10.1002/acp.70205 (2026-09-02), a fetch tool on the DOI and on onlinelibrary.wiley.com returned empty; a browser landed on a Cloudflare "Verify you are human" page for both Wiley and journals.sagepub.com. The check cleared after about a minute and a reload, then Wiley redirected `/doi/full/` to `/doi/abs/` (paywalled).
- Hypothesis: the large publishers front their sites with bot detection that fetch tools never pass and a fresh browser profile passes only after a delay; most closed Wiley and SAGE papers have no open copy, so the full text is unreachable either way.
- Rule: verify the citation with Crossref and check Unpaywall for an open copy before trying the publisher. Never click a human-verification check on the user's behalf. Say "abstract-level appraisal" in the verdict when the full text stays closed.
- 2026-09-28 update: on 10.1111/dmcn.70512 (5 days old, no PMC copy) the browser stuck on Wiley's check through two loads, and Europe PMC search and PubMed returned 429 after a few calls. What worked: the PubMed web page in a browser (`pubmed.ncbi.nlm.nih.gov/?term=<title words>`) gave the structured abstract in one read, and its "Similar articles" list surfaced the study that decided the review (a sibling-design paper with a negative-control exposure).
- 2026-10-01 update: on 10.1111/jssr.70101 (a social-science journal outside MEDLINE, closed) the publisher returned 403 and the browser sat on the check through two reads; there is no PubMed fallback for such journals. What worked: the Crossref abstract plus one numbered extraction prompt on the outlet article. Grade those papers at abstract level from the start and stop retrying after one browser read.
- Evidence: three appraisals, 2026-09-02, 2026-09-28, 2026-10-01
- Scope: skill
- Status: active · helpful 3 · harmful 0 · last_confirmed 2026-10-01

### L-002 · 2026-09-08 · Full-text order: Europe PMC fullTextXML, then the PDF, then a browser for commercial publishers
- Trigger: 10.1016/j.gastha.2026.101097 (Elsevier, gold open access): a fetch tool got 403 on the journal site, and so did curl with a real Chrome User-Agent; Europe PMC had nothing yet (article about 3 weeks old). A real browser returned the whole letter, results table and disclosures in one read.
- Hypothesis: Elsevier's bot detection keys on more than the User-Agent (TLS fingerprint, headless signals). Very recent papers are not in PMC or Europe PMC yet even when the journal is open access, so open-access status does not imply a reachable mirror.
- Rule: for a `10.1016/...` DOI, skip fetch tools on the publisher domain and use a real browser on the `/fulltext` URL. Call Crossref through the agent's fetch tool or the script; some sandboxes' egress proxies reject `api.crossref.org` and `www.ebi.ac.uk` for curl while the fetch tool reaches them.
- 2026-09-14 update: `pmc.ncbi.nlm.nih.gov` also bot-walls fetch tools (a reCAPTCHA "Checking your browser" page). A browser loaded a PNAS paper from PMC in one read. Browser output over about 50 KB may be saved to a file instead of returned; parse and grep it rather than re-fetching at a larger size.
- 2026-09-15 update: working papers on institutional sites need no browser: a plain fetch on the `.pdf` URL returned the whole paper, and one numbered extraction prompt pulled every number the review needed.
- 2026-09-16 update, now the first thing to try: when the paper has a PMC ID, `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC<id>/fullTextXML` returns the entire article in one call, even for a Wiley journal whose own site is bot-walled (L-001). Unpaywall gives the PMC ID. A second call 30 s later hit HTTP 429: one paper at a time.
- 2026-10-11 update: `paper_meta.py --fulltext DIR` now does this fetch and writes a plain-text copy with headings and tables, which is grepped rather than read whole (C-20261011-1).
- Evidence: appraisals on 2026-09-08, 2026-09-14 (10.1073/pnas.2528246123), 2026-09-15 (ISER WP 2024-01), 2026-09-16 (10.1002/trc2.70101)
- Scope: skill
- Status: active · helpful 4 · harmful 0 · last_confirmed 2026-09-16

### L-004 · 2026-09-14 · Readers want the reasoning, not a grade; define every term
- Trigger: after a review of a PNAS exercise-vs-nap paper, the reader asked for "a longer easier to read explanation, that covers some of the science evaluation terms". The review had used d′, Cohen's d, equivalence testing, the significant-vs-nonsignificant interaction error and "spin delta" as bare terms. Each was correct and none was explained.
- Hypothesis: an instruction to "keep it tight" was read as "short", so the review compressed into expert shorthand. The reader's dislike of filler is not a wish to skip explanation; an undefined term costs more than three extra paragraphs.
- Rule: gloss every appraisal term on first use in each review, then use it freely. Use an analogy from the reader's field when it is exact; for a technical reader the binary-classifier framing of a recognition test (hit rate as recall, d′ as separability, the response criterion as the threshold) made the hit-rate-without-d′ problem clear in one pass. Codified in references/explaining.md.
- Evidence: the 2026-09-14 review and the reader's follow-up
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-14

### L-007 · 2026-09-15 · Economics working papers: the author's own homepage is the only reliable source for publication status
- Trigger: appraising a March 2024 Psychology Today post about ISER WP 2024-01 (Del Bono, Etheridge and Garcia). Crossref returned only a July 2026 IFS working-paper record with a mistyped title; RePEc still listed a working paper. One author's research page listed it under journal publications as "accepted at Journal of Labor Economics", which moved the venue from unrefereed preprint to a top field journal.
- Hypothesis: economics circulates papers for years through several working-paper series with different DOIs and no crosswalk; Crossref indexes each separately and RePEc updates "published in" late or never. Authors update their own CV pages at once, because that is what the job market reads.
- Rule: for any economics or quantitative social-science paper, check the corresponding author's homepage or CV before calling it a preprint (`<author name> research` or `<author name> CV`; look for accepted, forthcoming, R&R). Do the same whenever the article is more than a few months old, in any field. Report the status as of the review and, separately, what was knowable when the article was written.
- Evidence: the 2026-09-15 appraisal
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-15

### L-008 · 2026-09-16 · ClinicalTrials.gov is robots-disallowed to fetch tools; use the published protocol paper
- Trigger: checking a creatine pilot (NCT05383833) for outcome switching, a fetch of `clinicaltrials.gov/api/v2/studies/<NCT>` returned ROBOTS_DISALLOWED, which no retry or URL change fixes.
- Hypothesis: clinicaltrials.gov's robots.txt covers the v2 API as well as the study pages, and fetch tools honour it.
- Rule: do not spend a call on clinicaltrials.gov. Search `"<NCT number>" protocol` or `<acronym> protocol` for the published protocol paper (Pilot and Feasibility Studies, BMJ Open, Trials and similar), which states the power position and analysis plan in the authors' own words, quotable against an efficacy headline. A browser can still load the registry page if no protocol exists.
- Evidence: the 2026-09-16 appraisal; the protocol (10.1186/s40814-024-01469-5) gave the primary outcome, the success threshold, the planned battery and "formal estimates of power are not required" in one fetch
- Scope: environment
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-16

### L-009 · 2026-09-28 · Run paper_meta.py first; it replaces the scattered metadata fetches
- Trigger: an appraisal (10.1111/dmcn.70512) spent about ten calls on metadata: proxy-rejected curl to Crossref and Unpaywall (a repeat of L-002, because LEARNINGS.md was not read first), 429s from Europe PMC search and PubMed, a Wiley check that never cleared. Afterwards `paper_meta.py` on a machine with open internet returned the Crossref record, affiliations, dates, abstract, open copies, PMID, structured abstract, COI and similar articles in one call, and the similar-articles list held the study that decided the review.
- Hypothesis: a user's own machine usually has open egress to Crossref, Unpaywall and NCBI E-utilities, which sandboxes block or rate-limit and which fetch tools cannot use (E-utilities is robots-disallowed). One scripted pass avoids both, and the per-call summarising cost of a fetch tool. Publisher PDFs are different: scripted requests to Wiley's PDF URL still got the Cloudflare 403, so the script does not try publishers.
- Rule: the first call of every appraisal is `paper_meta.py <DOI>` where Python can reach the internet; use its NEXT line for the full-text route. Never curl scholarly APIs from a sandbox whose proxy has refused them once. Fall back to fetch-routes.md when the script can't run.
- Evidence: the 2026-09-28 appraisal
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-28

### L-011 · 2026-10-01 · Reddit and OSF links: route around them instead of fetching
- Trigger: the user shared an r/science URL; the fetch tool returned SITE_BLOCKED for reddit.com. Searching for author preprints then surfaced two SocArXiv links; a fetch of the `osf.io/preprints/...` page returned only the page shell, and `api.osf.io/v2/preprints/<id>/` was robots-disallowed. A script on the user's machine reached the same API and showed both hits were the author's older, unrelated papers.
- Hypothesis: reddit blocks fetch tools outright, and OSF is a JavaScript app whose API is behind robots rules fetch tools honour. Neither block is transient.
- Rule: never fetch a reddit link. The r/science post title is the outlet's headline verbatim (a subreddit rule), so search it in quotes and appraise the outlet article; say in Sources that the post was not read. Check an OSF, SocArXiv or PsyArXiv hit's title through the OSF API from a script before treating it as a preprint of the paper under review.
- Evidence: the 2026-10-01 appraisal
- Scope: environment
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-01
