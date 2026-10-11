---
title: GitHub wiki written and published for 0.1.0
kind: note
date: 2026-10-11
verified: 2026-10-11
stale_after: 2027-04-11
tags: [wiki, docs, 0.1.0, github]
summary: "the wiki's pages, where their git working copy is, how every example was verified against the released v0.1.0 tag, the facts found on the way, the gaps in the shipped docs, and how to update the wiki; read before touching the wiki"
---

# GitHub wiki for 0.1.0

## Summary

The maintainer asked for the wiki after saving its first page. Ten pages were written with the wikiwright skill from the repository at v0.1.0, its tests, TESTS.md and the eval traces. Every output on the pages comes from `2026-10-11-wiki-verify.py` (beside this note) run against a fresh clone of the tag on Linux (WSL2 Ubuntu, Python 3.14.4). Wiki commit 4f57569. `live`: 10 pages, 0 failures; everwrite checker 0 strong.

Pages: Home, Getting-Started, How-An-Appraisal-Works, Commands, Configuration, Errors-and-Edge-Cases, Recipes, FAQ, Versions-and-Upgrading, Development, plus _Sidebar and _Footer.

## Where the pages are

`../science-study-evaluator.wiki` (a sibling of this clone), branch `master`, remote `https://github.com/m4bwav/science-study-evaluator.wiki.git`. Plain markdown links, LF.

## How it was published

Preflight: `placeholder` (the maintainer's first page). Pages committed on top and pushed with a plain `git push` (fast-forward). `wikiwright.py live`: 10 pages, 0 failures, sidebar and footer render, 10 anchors fine.

## Updating the wiki later

1. `git -C ../science-study-evaluator.wiki pull --ff-only`.
2. Run `python3 ai-docs/notes/2026-10-11-wiki-verify.py vX.Y.Z > new.out.txt` on Linux (it clones the tag itself), then `wikiwright.py diffout ai-docs/notes/2026-10-11-wiki-verify.out.txt new.out.txt`. Differences come from code changes and from the live databases changing their records (a PMC copy appearing, a retraction notice, an abstract added); both are page fixes.
3. Pages were written from `{{CASE:name}}` placeholders filled from the output (the session scratchpad held the sources); after an update, edit the pages directly and run `wikiwright.py outputs <wiki> <new output> --address ''`, `snippets <wiki> <program>`, `check <wiki> --version X` and the everwrite checker.
4. Commit, push, `wikiwright.py live m4bwav/science-study-evaluator <wiki>`. Pages that name the version: _Footer, Home (the "produced on ... by version 0.1.0" sentence), Versions-and-Upgrading, How-An-Appraisal-Works (methodology version), FAQ (next refresh date).

## How the examples were verified

There is no registry: the released tag stands for the published package. The program clones `v0.1.0` from GitHub into a temp folder and runs each case as a `/bin/sh` transcript from the scripts folder. Deviation from wikiwright's fixture rule: `paper_meta.py` exists to read Crossref, Unpaywall, NCBI E-utilities and Europe PMC, which are public APIs meant for this, so the run calls them live (about 30 requests, contact `you@example.org`), and Home says the outputs are dated. Not run: the agent-side flows (install commands, uninstall, Claude Desktop upload) are marked "not tested" or come from TESTS.md T-20261011-1; exit code 1 is stated from the source. `outputs`: 39 checked, 0 missing, 4 skipped (usage synopsis, folder layout, example file, slash commands). `snippets`: 2 checked, 1 command. Unit tests from the tag: `OK (skipped=1)`.

## Facts verified while writing (not in the README)

- `--help` describes no option except `identifier` and `--version`.
- Results go to stdout; a bad identifier prints `error: ...` to stderr and exits 2.
- A publisher URL (`/doi/full/...`), `PMID:`, a bare PMC number all resolve to the DOI; PubMed and PMC inputs find the DOI through PubMed.
- `--fulltext` writes both `.xml` and `.txt`; the text keeps `##` headings, tables as tab rows and the back matter.
- With no email, the UNPAYWALL section prints a "skipped" line and NEXT says so.
- PubMed's similar-articles list can lead with an unrelated entry ("Personality Theories" for the PNAS sleep paper).
- Crossref shows a retraction twice, once from the publisher and once from Retraction Watch.
- The script waits 0.35 s before each NCBI call even with an API key.

## Inaccuracies found in the shipped docs

1. None found in README or SKILL.md. Gap, not an error: `paper_meta.py --help` lacks option descriptions (the docstring has them). Fix in the next release by adding `help=` to each argparse option.

## Gotchas

- The `{{CASE:...}}` placeholder approach kept long author and abstract lines byte-exact; hand-copying them would have failed `outputs`.

Related: builds on [../decisions/2026-10-11-public-skill-holds-the-procedure-each-user-s-folder-holds-th.md](../decisions/2026-10-11-public-skill-holds-the-procedure-each-user-s-folder-holds-th.md)
