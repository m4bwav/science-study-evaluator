# Handoff: science-study-evaluator

## State (2026-10-11)

0.1.0 published as the public repo m4bwav/science-study-evaluator: one skill (SKILL.md, references/methodology.md v7, fetch-routes.md, explaining.md), scripts/paper_meta.py (rewritten), offline tests, CI on three OSes plus a weekly live job, eval cases (6/6, TESTS.md T-20261011-1), banner, SECURITY.md.

The skill came from a private unit that still holds the original user's appraisal history. That unit is not modified; it can serve as that user's SSE_HOME.

## Next single action

Watch the first CI run on main and fix anything red.

## Later

- Wiki live for 0.1.0 (10 pages); update it at each release: ai-docs/notes/2026-10-11-github-wiki.md.
- Next release: add argparse help text to paper_meta.py options (wiki note, inaccuracy 1).

- Untested routes: Claude Desktop / claude.ai upload, Copilot, Codex, and the no-Python fallback. Run the trigger cases there when convenient.
- Refresh due 2026-10-30 (evergreen.json).

Related: see also [decisions/2026-10-11-public-skill-holds-the-procedure-each-user-s-folder-holds-th.md](decisions/2026-10-11-public-skill-holds-the-procedure-each-user-s-folder-holds-th.md)

## Open as of 2026-11-04

The private unit has methodology items not yet mirrored here: biological-age clocks as outcomes, and the cell-type change check under them. The 2026-11-04 endpoint update is mirrored, but the public version line carries no v-number because of that gap. No version bump or release was cut for it.
