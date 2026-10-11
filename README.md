# science-study-evaluator

![A brass magnifying glass resting on an open scientific journal with a bar chart, a pie chart and a scatter plot, on a wooden desk by a sunny window beside a cup of tea and an evergreen sprig](https://raw.githubusercontent.com/m4bwav/science-study-evaluator/main/.github/images/banner.jpg)

A skill for AI agents that answers "is this study legit?" Share a news article, a press release, a DOI or a paper, and the agent finds the primary source, reads the paper itself instead of the coverage, checks the conflicts of interest, measures how far the headline outruns the findings, and gives a verdict with the reasoning explained in plain language.

It works in Claude Code, Claude Desktop and Cowork, GitHub Copilot (VS Code and CLI), Codex, Cursor and any other agent that reads `SKILL.md` skills.

## What it does

- **Checks the citation is real.** Authors, journal, year and DOI must match an actual paper. Content farms, AI-written ones especially, invent author lists while linking a real study.
- **Reads the paper, not the story about it.** Sample sizes per group, effect sizes with confidence intervals, what was actually measured, the limitations section, funding and conflicts.
- **Finds where the spin came in.** It quotes the paper's own conclusion next to the headline and grades each hop: abstract, press release, author interview, outlet. Sometimes the overreach is the author's, and the journalist quoted it faithfully.
- **Runs the checks that usually decide the verdict.** What the exposure really is (a "bully" score that is one item of fourteen), whether an uncontrolled trial has a hold-out outcome that moved anyway, whether sibling comparisons or negative-control exposures make a correlation go away, whether "equivalent" was shown or just assumed from p > 0.05.
- **Explains its terms.** Every appraisal term is defined on first use, with an analogy when one fits exactly, because the point is to understand the reasoning.

Verdicts use five levels: **Solid**, **Real but overhyped**, **Weak**, **Junk / predatory**, **Fabricated / misattributed**.

The checklist behind it is [references/methodology.md](skills/science-study-evaluator/references/methodology.md): evidence hierarchy, CONSORT 2025, RoB 2, ROBINS-I v2, GRADE, COREQ, umbrella-review checks, paper-mill and retraction screening, and branches for qualitative studies, observational regressions, single-arm pilots and equivalence trials.

## The metadata script

`scripts/paper_meta.py` pulls everything an appraisal starts with in one call, so the agent doesn't spend eight web fetches on it: the Crossref record (authors, affiliations, received and accepted dates, abstract, funders, retraction and correction notices including Retraction Watch data), Unpaywall's open copies, the PubMed record (structured abstract, conflict-of-interest statement, grants, errata) and PubMed's similar articles, where companion and contradicting studies turn up. With `--fulltext` it saves an open article from Europe PMC as plain text the agent can grep. Standard library only, Python 3.10 or newer.

```
python skills/science-study-evaluator/scripts/paper_meta.py 10.1073/pnas.2528246123 --email you@example.org
python skills/science-study-evaluator/scripts/paper_meta.py https://pubmed.ncbi.nlm.nih.gov/42566467/ --fulltext /tmp/papers --json
```

Set `SSE_EMAIL` once instead of passing `--email`; Unpaywall requires a contact address and the script skips it without one. `NCBI_API_KEY` raises PubMed's rate limit.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add m4bwav/science-study-evaluator
/plugin install science-study-evaluator@science-study-evaluator
```

Any agent that reads personal skills: clone this repository and link or copy `skills/science-study-evaluator` into the agent's skills folder (`~/.claude/skills/`, `~/.agents/skills/` or `~/.copilot/skills/`). Claude Desktop and claude.ai: zip the `skills/science-study-evaluator` folder and upload it under Settings, Capabilities, Skills. In a hosted app the script may not reach the internet; the skill then falls back to the agent's own web tools ([references/fetch-routes.md](skills/science-study-evaluator/references/fetch-routes.md)).

## Your appraisals

Reviews are saved to your own folder, not to the skill: `SSE_HOME` if set, otherwise `~/.science-study-evaluator/`. It holds `appraisals/` (one Markdown file per review) and `evaluations.md` (one line per verdict, which the agent checks for repeat outlets and recycled samples). Add a `reader.md` with a few lines about who reads the reviews ("software engineer, rusty on statistics" or "nurse, wants the clinical bottom line") and the explanations are pitched to match.

## Evergreen

Appraisal standards move: reporting guidelines get revised, fraud gets more industrial, and sites change which tools they block. This skill follows the [Evergreen Protocol](https://github.com/m4bwav/evergreen-protocol): it re-researches its sources on a schedule (`evergreen.json`), logs each finding (`RESEARCH.md`), each change with its reason (`CHANGELOG.md`) and each lesson from real appraisals (`LEARNINGS.md`), and carries the cases that prove it triggers and acts (`TESTS.md`, `evals/`). Without the evergreen plugin installed the skill still works; `MAINTENANCE.md` says how to refresh it by hand.

## Layout

- [skills/science-study-evaluator/SKILL.md](skills/science-study-evaluator/SKILL.md): the skill.
- [references/](skills/science-study-evaluator/references/): the methodology, fetch routes, and the glossary and analogies used in write-ups.
- [scripts/paper_meta.py](skills/science-study-evaluator/scripts/paper_meta.py): the metadata script; [tests/](tests/) holds its offline tests (`python tests/test_paper_meta.py`).
- [ai-docs/INDEX.md](ai-docs/INDEX.md): notes left by past work sessions on this repository.

## Privacy

The skill collects nothing. When you ask for an appraisal, `paper_meta.py` sends the paper's DOI or PubMed ID to Crossref, Unpaywall, NCBI PubMed and Europe PMC, the public scholarly databases it reads, along with the contact email you set, if any (Unpaywall and NCBI ask for one). Nothing else leaves your machine, and the script writes files only where you point `--fulltext`. Your appraisals stay in your own folder. Whatever your AI app does with the conversation is covered by that app's own privacy policy.

## Not medical advice

An appraisal says how well a study supports its claims. It is not a recommendation about your health; talk to a clinician before changing a treatment.

## License

MIT. See [LICENSE](LICENSE).
