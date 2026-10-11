# Tests: science-study-evaluator

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`; the runnable copies are in the repository's root `evals/` (claude plugin eval format). A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section).

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case, then `led to:`. Newest first. Budget 150 lines.

## Runs

### T-20261011-1 · 2026-10-11 · claude plugin eval (default model), unittest · Windows 11 native for trigger and decoy, WSL2 Ubuntu for the Bash case · 6/6
- Unit tests: `python tests/test_paper_meta.py`, 15 offline tests pass, the live smoke test skipped without `SSE_LIVE`. Live runs by hand on 10.1073/pnas.2528246123 (open, PMC), 10.1111/jssr.70101 (closed, not in PubMed), 10.1057/s41599-025-04787-y (retracted: Crossref `updated-by` from the publisher and from Retraction Watch, INTEGRITY NOTICE printed), PMID input and a bad input (exit 2).
- trigger-1, trigger-2, trigger-3, decoy-1, decoy-2 native: 5/5, $0.89. Every trigger called `Skill(science-study-evaluator)` once; both decoys called nothing.
- action-1 in WSL2 (`--tag bash --allow-tools Bash Write Edit WebFetch WebSearch`): first run 0.67, skill invoked and `paper_meta.py 10.1073/pnas.2528246123` in the trace, the verdict regex missed in the final message (the report does not keep the text, so the cause is unconfirmed; probably a closing message after the review). Rerun with `--keep-temp`: 1.00, $0.62. The trace shows the script with `--fulltext`, the Europe PMC full text fetched, `evaluations.md` and `reader.md` checked, `explaining.md` and the methodology read, and the review saved under `~/.science-study-evaluator/appraisals/`. Verdict "Weak", resting on d′ (no group difference) against the hit-rate headline, the same reasoning as the private appraisal of 2026-09-14.
- untested: Claude Desktop or claude.ai upload, Copilot, Codex; the no-Python fallback route.
- led to: none
