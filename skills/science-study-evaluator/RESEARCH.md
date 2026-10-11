# Research: science-study-evaluator

Findings that back [SKILL.md](SKILL.md) and the checklist it loads, [references/methodology.md](references/methodology.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: critical appraisal of scientific studies and science journalism: reporting guidelines (CONSORT, PRISMA, STROBE, COREQ/SRQR), risk-of-bias and certainty tools (RoB 2, ROBINS-I, GRADE), metascience and replication, research-integrity and paper-mill/AI-fabrication detection, predatory-journal patterns, retraction tracking. Tier `moderate`. Last refresh 2026-09-30; next due 2026-10-30. Entries before 2026-10-11 were written while the skill was private and are kept as its research history.

## Current understanding

Settled: the evidence hierarchy (systematic review > RCT > cohort > case-control/cross-sectional > case series > mechanism) and the rule that observational and cross-sectional designs support association only. Effect sizes with CIs beat p-values. COI must be checked against affiliations, not just the disclosure box. A citation that does not resolve to the claimed authors/journal/DOI discredits the article regardless of the paper.

Reporting standards in force (as of 2026-09-30): CONSORT 2025 (30 items; new items on prespecification changes, harms, data sharing, intervention delivery, patient involvement) for RCTs, with its NI/equivalence, Outcomes and Harms extensions still on the 2010-era versions (NI/equivalence: Piaggio, JAMA 2012; 2025 revision under development); SPIRIT 2025 for protocols; PRISMA 2020 for systematic reviews; STROBE for observational studies; COREQ (32 items) and SRQR for qualitative interview/focus-group studies. Risk-of-bias tools: Cochrane RoB 2 for RCTs, ROBINS-I v2 (2025) for non-randomized studies. Certainty: GRADE; the GRADE Book is superseding the GRADE Handbook by end of 2026 and GRADErater automation is in testing.

Moving: research integrity. Paper-mill fraud is industrial in 2025-26; screening tools in use include Papermill Alarm (Clear Skies), the STM Integrity Hub, Pangram (AI-generated text), and Grounded AI (citation context); a 2025 ML screen flagged over 250k suspect cancer papers. AI content farms fabricate author lists while linking real papers. Retractions and corrections of load-bearing citations are common enough that a paper's key cited sources need a Retraction Watch check, not just the paper itself (seen 2026-09-02: a widely cited 2025 ChatGPT-and-learning meta-analysis was retracted; a widely cited 2025 AI-and-critical-thinking survey study was corrected). The Retraction Watch database has been queryable through the Crossref API since Jan 2025 (retractions comprehensive; corrections and expressions of concern not). NIH announced a ~$174M replication initiative in Sep 2026, including a PubMed "Linked Discoveries" retraction-aware view (not yet live).

Contested: how much weight single qualitative studies and small-N neuroimaging or social-psychology studies deserve in replication-crisis fields; the checklist gives them a lower prior and demands independent reproduction before "Solid".

Design note: the checklist itself is `references/methodology.md`, kept separate from `SKILL.md` so a refresh edits the checklist without touching the skill's instructions. Retrieval routes (which sites block which tools) are in `references/fetch-routes.md` and come from use, not from web research; they are logged in LEARNINGS.md.

## Open questions

- CONSORT 2025 extensions: as of 2026-09-30 only CONSORT-C/SPIRIT-C are 2025-aligned; Outcomes, Harms and NI/equivalence (under development since May 2025) are not. Re-check.
- COREQ/SRQR: no update as of 2026-09-30 (a 2026 QHR critique of COREQ, Buus et al., changes nothing). Re-check.
- GRADE Book: has the Handbook formally been retired? Still unannounced 2026-09-30; check usblog.gradeworkinggroup.org, since the main site's newsletter stopped in Dec 2024.
- PubMed Linked Discoveries (NIH, announced Sep 2026): once live, does it show retractions reliably enough to be a retraction-check route?
- Resolved 2026-09-30: Retraction Watch data is in the Crossref API (see R-20260930-1).

## Search plan

Queries (scope each to the period since the last refresh; add the year):

- `CONSORT statement update <year>` and `CONSORT extension published <year>`
- `PRISMA OR STROBE OR SPIRIT reporting guideline revision <year>`
- `COREQ OR SRQR qualitative reporting guideline update <year>`
- `Cochrane RoB 2 OR ROBINS-I update <year>` and `GRADE Book GRADErater <year>`
- `paper mill detection <year>` and `AI-generated papers screening publishers <year>`
- `predatory journal new patterns <year>` and `publisher retraction scandal <year>`
- `metascience replication findings <year>`

Best sources (primary first): EQUATOR Network (reporting guidelines index), consort-statement.org, prisma-statement.org, Cochrane Methods (RoB 2, ROBINS-I), gradeworkinggroup.org, Retraction Watch and its database, Crossref API (`api.crossref.org/works/<DOI>`, includes `update-to` for retractions/corrections), Unpaywall API (open-access location), COPE (publication ethics), STM Integrity Hub announcements, PubPeer. Sources that proved noisy: general news coverage of "AI is destroying science"; SEO listicles about predatory journals; "PRISMA 2026" pages on casrai.org, journalmetrics.org and editverse (no DOI, no journal). Productive: Retraction Watch monthly archives and weekend reads, EQUATOR "under development" pages, Crossref docs, and the query `LLM risk of bias RoB 2 <year>`.

## Findings log

Newest first. One entry per material finding; a quiet refresh gets one entry saying so.

### R-20260930-2 · 2026-09-30 · Checklist gap: equivalence declared from P > 0.05, and sponsored-trial comparator design
- Summary: Appraising SWITCH (Harrold et al., BJN 2026) showed methodology.md had no equivalence/non-inferiority check. The paper defined equivalence as a non-significant P value with no margin; against the implied 1.5 kg margin from its own power calculation, the primary 90% CI (−0.2 to 2.4 kg) and the MI analysis (−0.1 to 1.7) both fail. Also no item on comparator choice in sponsored trials (habitual users randomised to continue vs quit), headline timepoints added by amendment, or "no harm" claims read off a small subsample. Found in use, not on the web.
- Sources: https://doi.org/10.1017/S0007114526108150; Piaggio et al., JAMA 2012 (CONSORT NI/equivalence extension)
- Magnitude: 0.4 (checklist items added; not counted as the scheduled check)
- Applied: C-20260930-1

### R-20260930-1 · 2026-09-30 · Scheduled refresh (m 0.25)
- Summary: (a) Retraction Watch data sits in the Crossref REST API since Jan 2025 (`update-type:retraction`, `update-to`, source field) and as a daily CC BY CSV on GitLab; Crossref calls retractions comprehensive, corrections and expressions of concern not. (b) CONSORT/SPIRIT NI-equivalence extensions registered on EQUATOR as under development (May 2025); only CONSORT-C/SPIRIT-C are 2025-aligned so far; Outcomes, Harms and NI/equivalence remain 2010-era. (c) NIH ~$174M five-year replication initiative (Sep 2026) plus PubMed "Linked Discoveries", an AI-assisted view of related papers and retractions, not yet live. (d) RoB2-Evaluator preprint (LLM on RoB 2, 10 RCTs, κ 0.93, domain 2 unstable): tooling note only. (e) Science of the Total Environment: 165 retractions in 2026, delisted from Web of Science Nov 2025; Retraction Watch DB past 67k; Hijacked Journal Checker 450+ entries. (f) "PRISMA 2026" pages on casrai.org / journalmetrics.org are uncited SEO; PRISMA 2020 stands. No COREQ/SRQR update; GRADE Handbook retirement still unannounced.
- Sources: https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/, https://gitlab.com/crossref/retraction-watch-data, https://www.equator-network.org/library/reporting-guidelines-under-development/, https://www.insidehighered.com/news/government/science-research-policy/2026/09/28/nih-launches-174m-replicability-reproducibility, https://commonfund.nih.gov/replication-initiative, https://www.medrxiv.org/content/10.64898/2026.09.22.26363693v1.full, https://retractionwatch.com/2026/09/22/elsevier-journal-retracts-100-papers-for-authorship-issues-editor-conflicts-of-interest/
- Magnitude: 0.25
- Applied: C-20260930-2

### R-20260902-1 · 2026-09-02 · Checklist gaps exposed by first qualitative-study appraisal
- Summary: Appraising Farhat 2026 (Applied Cognitive Psychology, 45 semi-structured interviews) showed `methodology.md` had no qualitative branch (no COREQ/SRQR items: single-coder risk, reflexivity, saturation, selection on the exposure, self-reported perception vs measured outcome), no check for sample recycling across an author's recent papers (a Dec 2025 teaching case by the same author used 40 interviews from the same demographic), and no check on whether a paper's load-bearing citations have been retracted or corrected (two of this paper's key sources had been). These are checklist additions found in use, not web findings.
- Sources: https://api.crossref.org/works/10.1002/acp.70205, https://api.crossref.org/works/10.1177/20438869251397953, https://www.nature.com/articles/s41599-025-04787-y (retracted meta-analysis), https://doi.org/10.3390/soc15090252 (correction notice)
- Magnitude: 0.4 (checklist items added; not counted as a scheduled check)
- Applied: C-20260902-2

### R-20260831-1 · 2026-08-31 · Initial baseline (migrated from state.json)
- Summary: Methodology v2026-08-31.1 written from web research on the current state of appraisal standards: CONSORT 2025 statement (BMJ/Lancet/Nature Medicine, April 2025); GRADE Book transition and GRADErater; ROBINS-I v2 (2025); Cochrane Methods Report 2025; the 2025-26 paper-mill detection landscape (Clear Skies Papermill Alarm, STM Integrity Hub, Pangram, Grounded AI). First check interval set to 30 days.
- Sources: consort-statement.org (CONSORT 2025), gradeworkinggroup.org, methods.cochrane.org (ROBINS-I v2, Methods Report 2025), clear-skies.com, stm-assoc.org (Integrity Hub)
- Magnitude: n/a (initial)
- Applied: C-20260831-1
