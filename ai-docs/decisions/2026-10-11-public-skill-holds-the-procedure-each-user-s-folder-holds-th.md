---
title: Public skill holds the procedure; each user's folder holds their appraisals
kind: decision
status: active
date: 2026-10-11
verified: 2026-10-11
stale_after: 2027-04-09
tags: [design, privacy, portability]
summary: read before moving files between the skill and the user's SSE_HOME folder, or adding user-specific behaviour
---

# Public skill holds the procedure; each user's folder holds their appraisals

## Context

The skill ran privately from 2026-08-31 to 2026-10-10 on one machine and one desktop app. Its SKILL.md named absolute paths, one remote-shell tool and one app's skill-save mechanism; its appraisal log and full reviews sat in the same folder as the checklist; `paper_meta.py` hard-coded a contact email. Publishing it meant separating three things that had grown together: the procedure, the knowledge it maintains, and one user's history.

## Decision

- The skill folder holds only what every user shares: SKILL.md, `skills/science-study-evaluator/references/methodology.md` (the checklist a refresh edits), `skills/science-study-evaluator/references/fetch-routes.md` (retrieval lessons as rules), `skills/science-study-evaluator/references/explaining.md` (glossary and analogies), the script, and the evergreen companions.
- Each user's appraisals, verdict log and an optional `reader.md` live in their own folder: `SSE_HOME`, default `~/.science-study-evaluator/`. The reader profile replaces the original's hard-coded "the reader has a CS background", so the computing analogies stay available without being assumed.
- `paper_meta.py` takes the contact email from `--email` or `SSE_EMAIL` and skips Unpaywall without one, rather than shipping anyone's address. It gained `--fulltext` because the fastest full-text route (Europe PMC fullTextXML) returns 9,000-word articles that are cheaper grepped than read.
- Lessons about one machine's remote-shell quoting and one app's skill-save flow stayed in the private unit; their LEARNINGS numbers are left as gaps so the public entries keep their original ids.
- Steps were renamed source, appraise, write, keep, and the non-negotiables cut from seven to six by moving source verification into Step 1.

## Reasons

Installed copies are read-only and replaced on every update, so anything a user accumulates has to live outside them. A public repository cannot carry a person's email, paths or reading history. Keeping retrieval lessons as dated rules in one reference file lets every harness use them, while LEARNINGS.md keeps the evidence.

## Rejected

- Renaming to a "-wright" name to match the author's other plugins: the skill already had users of the name, and the name says what it does.
- Keeping the appraisal log inside the skill folder: installed plugin copies are read-only and get replaced on update.

Related: see also [../HANDOFF.md](../HANDOFF.md)
