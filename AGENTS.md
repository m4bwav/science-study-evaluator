# AGENTS.md

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md` imports this file and `.github/copilot-instructions.md` points here.

## What this is

A cross-agent plugin with one skill, `skills/science-study-evaluator/`: SKILL.md (the appraisal procedure), `references/methodology.md` (the living checklist a refresh edits), `references/fetch-routes.md` (how to reach the paper when sites block tools), `references/explaining.md` (glossary and analogies for the write-up), the single-file script `scripts/paper_meta.py`, and the evergreen companions (RESEARCH, CHANGELOG, LEARNINGS, TESTS, MAINTENANCE, SETUP, `evergreen.json`, `evals/evals.json`). Unit tests are in `tests/`; the runnable eval cases are in the root `evals/` folder (`claude plugin eval` format). Handoff notes, decisions and the log are under `ai-docs/` (start with `ai-docs/HANDOFF.md`).

## Rules

- `paper_meta.py` stays one standard-library Python file (3.10 or newer) that runs on Windows, macOS and Linux. It only reads public scholarly APIs (Crossref, Unpaywall, NCBI E-utilities, Europe PMC), never a publisher site, and writes files only under the folder `--fulltext` names. The contact email comes from `--email` or `SSE_EMAIL`, never from the code.
- Every change to the script has a test in `tests/test_paper_meta.py`; run `python tests/test_paper_meta.py` from the repository root before committing. The tests are offline: responses are invented fixtures served by a fake fetcher. `SSE_LIVE=1` adds one live smoke test.
- The skill is an evergreen unit. Before editing it read `skills/science-study-evaluator/evergreen.json`; if `next_due` has passed or `contradiction` is set, say so and refresh after the task (`evergreen-refresh`, or `MAINTENANCE.md`). Every change is logged in `CHANGELOG.md` with its reason. Checklist changes go in `references/methodology.md` with a version bump; retrieval lessons go in LEARNINGS.md and `references/fetch-routes.md` together.
- Research beats recall: a claim about a reporting guideline, risk-of-bias tool or integrity database carries an `R-` entry in RESEARCH.md with the date it was checked.
- Users' appraisals and verdict logs live in their own folder (`SSE_HOME`, default `~/.science-study-evaluator/`), never in this repository.
- A release bumps the version in `.claude-plugin/plugin.json`, `plugin.json`, `VERSION` in `paper_meta.py`, `metadata.version` in SKILL.md and `version` in `evergreen.json` together, then tags `vX.Y.Z` and publishes a GitHub Release with the CHANGELOG entry as notes.
- No top-level `bin/` folder: Cowork refuses to install a plugin that has one.
- Eval graders: JavaScript regex (`flags: i`, never `(?i)`), one literal tool name per `tool_used` grader. The Bash case needs network and runs under WSL2 or Linux, not native Windows.
- Prose people read (README, SKILL.md, references) is checked with the everwrite checker when it is available: `python <everwrite>/scripts/tells.py <files>`, zero strong findings. Quoted paper titles and the methodology's technical terms may raise weak hits; judge them in context.
- This is a public repository. Nothing in it names a person other than the author credit, authors of credited public projects and authors of published papers cited as examples; no machine names, absolute paths on someone's machine, private projects, email addresses or credentials.
- No AI attribution anywhere: no Co-Authored-By trailers, no "generated with" lines in commits, pull requests, releases or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here (solutions with verified commands, decisions with reasons, plans). At the start of a task, scan it and open only the entries whose title or tags match; no line matches: `everlast.py search "<key terms>"` before concluding nothing was recorded. Read `ai-docs/HANDOFF.md` when continuing unfinished work (everlast-resume skill).
- Before acting on an entry marked `(recheck due)`, run `everlast.py recheck <entry>`, re-run its Verified-by command only when that is read-only or safe (a build, a test, a version query), then record `everlast.py verify <entry>` or `verify <entry> --failed "what broke"`; a fix that changed is superseded, never reused blindly.
- Before finishing a task that hit a dead end, verified a non-obvious command, made a design choice, or taught you something about the user, record it (everlast-capture skill, or `everlast.py note` / `handoff`); rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the private sidecar (`--private`), never here. Lessons about the user or this machine go to the user tier (`--user`).
- Rules go in this file; the doc set holds only what could not be re-derived from the code in a minute.
- Link documents together with relative markdown links: every markdown folder is reachable from an index whose lines say when to read each file (`ai-docs/INDEX.md` is generated from frontmatter; give entries a one-line `summary`), and an entry links the entries it relates to on a typed `Related:` line (`supersedes`, `contradicts`, `builds on`, `see also`). No wikilinks in the repo.
