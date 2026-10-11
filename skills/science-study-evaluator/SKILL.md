---
name: science-study-evaluator
description: "Critically appraise a scientific study and the news coverage around it: verify the citation, read the paper itself, check conflicts of interest, measure how far the headline outruns the findings, and give a verdict (Solid, Real but overhyped, Weak, Junk/predatory, Fabricated/misattributed) with the reasoning explained in plain language. Use whenever the user shares a paper, DOI, PubMed link, preprint, press release or news article about research and asks whether it is legit, real, overhyped, junk or worth believing: 'is this study legit?', 'does this paper actually show that?', 'what's wrong with this research?', 'fact-check this health article', 'should I trust this headline?', 'appraise this RCT', or pastes an r/science link. Also for 'refresh science-study-evaluator' and 'is science-study-evaluator stale'. Not for writing or peer-reviewing the user's own manuscript, running statistics on their data, or searching the literature for papers on a topic."
metadata:
  version: "0.1.0"
---

# Science study evaluator

Appraise a scientific study, or the reporting wrapped around it, against a checklist that keeps itself current. Appraisal standards move (reporting guidelines get revised, new fraud patterns appear, metascience advances), so the checklist lives in [references/methodology.md](references/methodology.md) and is refreshed from primary sources on a schedule instead of being frozen here.

`PM` below means `python "<this folder>/scripts/paper_meta.py"` (`python3` on macOS and Linux). It needs Python 3.10 or newer and nothing else.

**The user's folder.** Appraisals and the verdict log live outside this skill so they survive updates: the folder named by the `SSE_HOME` environment variable, else `~/.science-study-evaluator/`. It holds `evaluations.md` (one line per verdict), `appraisals/` (the full reviews) and, optionally, `reader.md`, a few lines on who reads the reviews (background, field, which analogies land). Create the folder on first use. In a hosted app with no persistent disk, skip the files and deliver the review in the chat.

## Step 0: freshness (every use, one read)

Read [evergreen.json](evergreen.json). If `contradiction` is set or today is on or after `next_due`, tell the user in one line ("the appraisal checklist is N days past its refresh; I'll refresh it after the review"), do the appraisal with the current checklist, then refresh (Maintenance below). If the user only asked for a refresh, refresh and stop. Below the due date, spend nothing more.

## Step 1: find the primary source and verify it

1. **Get from the article to the paper.** Follow the article's link or search its key phrases. A reddit link can't be fetched: an r/science title is the outlet's headline verbatim, so search it in quotes and appraise the outlet article.
2. **Run `PM <DOI or URL>` first** wherever Python can reach the internet; add `--email <address>` (or set `SSE_EMAIL`) for the open-access check and `--fulltext <tmp dir>` to save the article as greppable text. One call returns the Crossref record (authors, affiliations, received and accepted dates, abstract, funders, retraction and correction notices), open copies, the PubMed record (structured abstract, COI statement, grants, errata), similar articles, and a NEXT line naming the cheapest route to the full text. If the script can't run, follow [references/fetch-routes.md](references/fetch-routes.md).
3. **Verify the citation.** Authors, journal, year and DOI must match a real paper. Content farms, AI-written ones especially, invent author lists while linking a real paper; that alone makes the article Fabricated/misattributed.
4. **Check the status now, not as of the article.** An INTEGRITY NOTICE from the script comes first. When the article is more than a few months old, check whether the paper has since been published, retracted or superseded; for economics and social-science working papers the author's homepage is usually the only source (fetch-routes.md). Grade the article on what was knowable when it was written and report the current status separately. Then the mirror check: an outlet calling a 15-month-old paper "new" has manufactured the recency, and a gap that size usually means a companion paper from the same sample that the article ignores. The similar-articles list is where it turns up.

## Step 2: appraise

Read [references/methodology.md](references/methodology.md) and follow it. Whatever version it is at, these are non-negotiable:

1. **Read the paper itself** (full text, or abstract plus key numbers), never the article's description of it. Pull: n per group, effect sizes with CIs, what was actually measured (watch for proxies), the limitations section, COI and funding. For a regression paper, pull the whole specification sequence: how far the estimate shrinks as controls are added is itself the confounding diagnostic. If the full text stays closed, say so and grade at abstract level.
2. **Check interests independently.** Compare affiliations against the COI statement; an undisclosed commercial affiliation is a finding in itself. Check who is promoting the study and what they sell; a press release within days of publication is a tell.
3. **Compute the spin delta.** Quote the paper's own hedged conclusion next to the article's claim. Grade each hop separately (paper abstract, press release, author interview, headline) and name the hop that added any causal claim: an outlet faithfully quoting an overconfident author is not the spinner. Grade omission too: a two-sided result reported one-sided is spin even when every quoted sentence is accurate.
4. **Interrogate the exposure before accepting its name.** For a factor score, index or composite, get the items and loadings and ask whether someone could score high without the behaviour the headline names; quote the items. A 10-word vocabulary quiz is crystallized knowledge, not "intelligence"; a single survey item standing in for a validated scale may measure something else too. Read the controls the same way: "persists after controlling for education" is fair when education is entered as years, "not reducible to education" is not.
5. **On an uncontrolled before/after study, find the hold-out outcome.** Get the published protocol paper (it names the real primary outcome, usually compliance for a pilot, and often says the efficacy measures were not powered). Then find a measure theory says should not respond; if it moved, it is the artifact floor for everything measured beside it. Say separately which results survive a multiplicity correction, and that surviving it is not surviving the missing control arm.
6. **On an observational exposure-outcome claim, look for the designs that attack confounding.** Search for sibling comparisons and negative-control exposures (the same exposure at a time it cannot act). A negative control as strong as the real exposure says the signal comes from who gets exposed. Put those numbers next to the headline even when the article never mentions them. For an umbrella review, check overlap (CCA), the AMSTAR-2 ratings of what was pooled, and whether the quality-restricted estimates are reported with CIs.

## Step 3: write it

Read [references/explaining.md](references/explaining.md) and the user's `reader.md` if there is one. Explain, don't just rule: gloss every appraisal term on first use, use an analogy only when it is exact. If the `everwrite` skill is available, write through it and run its checker on the finished review; fix every strong hit.

Open with the verdict line, then the evidence under short headings, in this order:

1. The verdict: one of *Solid*, *Real but overhyped*, *Weak*, *Junk / predatory* or *Fabricated / misattributed*, with a one-sentence reason. Grade the paper and the article separately when both were asked about.
2. What the study shows next to what the article claims, with real numbers (n, effect size, CI) and the effect translated into a felt unit, labelled as your arithmetic.
3. The red and green flags that matter, three to six of them, not an exhaustive dump.
4. The bottom line. On a health topic, add that mechanism debates don't change which treatments work; trials settle that.
5. Sources: the paper (prefer DOI or PMC), the article, and anything else cited; say which were unreadable.

## Step 4: keep it

Unless the user named another place, save the review as `<user folder>/appraisals/<YYYY-MM-DD>-<topic-slug>.md` and append one line to `<user folder>/evaluations.md`: `date | item | verdict | one-clause reason`. Read the last few lines of `evaluations.md` first: a repeat outlet, author or sample (the same cohort sliced twice) is worth a sentence in the review.

## While working: capture learnings

If the user corrects the appraisal, the same retrieval failure happens twice, or a workaround is found (a paywall route, an API that avoids a bot wall), add or update an entry in [LEARNINGS.md](LEARNINGS.md) now (format in MAINTENANCE.md) and, for a retrieval route, fix fetch-routes.md. A study type the checklist doesn't cover is a methodology edit, not a learning: change methodology.md, bump its version line, and log a `C-` entry in [CHANGELOG.md](CHANGELOG.md). If a learning proves the methodology wrong, fix it and set `contradiction` in `evergreen.json`. In an installed, read-only copy, put the change in the user's folder as `pending-learnings.md` and tell the user it belongs upstream.

## Maintenance

This skill is evergreen (topic: critical appraisal of scientific studies and science journalism; tier `moderate`, about every 30 days). Refresh: follow [MAINTENANCE.md](MAINTENANCE.md), or run `evergreen-refresh` when the evergreen plugin is installed. The search plan and best sources are in [RESEARCH.md](RESEARCH.md) §Search plan. Adopt substantive changes only (a change adds or retires a checklist item or materially alters guidance); edit methodology.md in place, bump its version line, log each edit as a `C-` entry citing the `R-` finding, then update `evergreen.json`. Report in at most three lines; a quiet check is the system working. A failed refresh never blocks an appraisal: log `m: null` in `history`, leave `next_due`, retry next use. Tests: [TESTS.md](TESTS.md) and `evals/evals.json`. Needs: [SETUP.md](SETUP.md).
