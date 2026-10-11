# Setup: science-study-evaluator

What [SKILL.md](SKILL.md) needs outside itself, what each piece is for, how to check it, and how to install it on each environment met so far. Format and rules: the Evergreen Protocol's `SETUP.md` spec. Check here with `evergreen.py setup <this folder>`; it reads the tables below, so keep their shape.

When a step fails for a missing piece, or this environment is not in Environments met: run the check, tell the user what is missing and what it is for, install what you can after saying so, hand the rest to the user with the exact steps, re-check, then record what worked and the environment.

## Needs

| id | kind | check | for | if missing |
|---|---|---|---|---|
| python | command | `python3 --version >= 3.10 \| python --version >= 3.10` | runs scripts/paper_meta.py at Step 1 | optional: fetch the APIs one by one with the agent's web-fetch tool (references/fetch-routes.md) |
| crossref | url | `https://api.crossref.org/works/10.1073/pnas.2528246123` | citation check, retraction and correction notices | optional: abstract and metadata from the publisher or PubMed page |
| eutils | url | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed` | PubMed record, COI statement, similar articles | optional: the PubMed web page in a browser |
| europepmc | url | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=test&format=json` | full text of open PMC papers (--fulltext) | optional: the PDF or a browser |
| email | env | `SSE_EMAIL` | contact address Unpaywall requires; also sent to NCBI and in the User-Agent | optional: no open-access check (pass --email per run instead) |
| ncbi-key | env | `NCBI_API_KEY` | raises the NCBI rate limit from 3 to 10 requests a second | optional: the script waits between calls |
| web-fetch | manual | the agent has a web search and web-fetch tool | finding the article's source and reading open pages | required |
| browser | manual | a browser-automation tool, or the user's own browser | commercial publisher pages that block fetch tools | optional: grade at abstract level and say so |

## Install

### python

- windows: `winget install Python.Python.3.13`
- macos/brew: `brew install python`
- linux/apt: `sudo apt-get install -y python3`
- any: https://www.python.org/downloads/

### email

- any: set `SSE_EMAIL` to an address you read (Unpaywall's terms ask for a real one). Windows: `setx SSE_EMAIL you@example.org`, then restart the agent. macOS and Linux: add `export SSE_EMAIL=you@example.org` to your shell profile.

### ncbi-key

- any: create a free key under Account settings at https://www.ncbi.nlm.nih.gov/account/ and set `NCBI_API_KEY` the same way (manual, secret)

## Attempts

| date | need | env | route | result | took | notes |
|---|---|---|---|---|---|---|

## Environments met

| date | os | harness | missing | notes |
|---|---|---|---|---|
| 2026-10-11 | windows | claude-code | none | Python 3.14; all three APIs reachable; full run in about 4 s |
