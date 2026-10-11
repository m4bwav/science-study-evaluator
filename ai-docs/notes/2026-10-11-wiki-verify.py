"""Verification program for the GitHub wiki of science-study-evaluator.

Clones the released tag into a scratch folder and runs every example the wiki pages show, printing a
terminal transcript per case ($ command, merged output, $ echo $?, exit code). Run it on Linux (the pages
show Linux paths) with the tag to verify:

    python3 ai-docs/notes/2026-10-11-wiki-verify.py v0.1.0 > ai-docs/notes/2026-10-11-wiki-verify.out.txt

The script calls the real public APIs (Crossref, Unpaywall, NCBI E-utilities, Europe PMC), about 30
requests per run; records change over time, so a rerun can differ where a database changed.
"""
import os
import shutil
import subprocess
import sys
import tempfile

TAG = sys.argv[1] if len(sys.argv) > 1 else "v0.1.0"
REPO = "https://github.com/m4bwav/science-study-evaluator.git"

root = tempfile.mkdtemp(prefix="sse-wiki-")
clone = os.path.join(root, "science-study-evaluator")
subprocess.run(["git", "clone", "-q", "--depth", "1", "--branch", TAG, REPO, clone], check=True)
scripts = os.path.join(clone, "skills", "science-study-evaluator", "scripts")


def term(name, *commands, cwd=None):
    """One case: each command through /bin/sh with stderr merged, then its exit code."""
    print(f"== case: {name}")
    for cmd in commands:
        print(f"$ {cmd}")
        r = subprocess.run(["/bin/sh", "-c", cmd + " 2>&1"], cwd=cwd or scripts, capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        print("$ echo $?")
        print(r.returncode)
    print()


def streams(name, cmd):
    """Which stream each line goes to."""
    print(f"== case: {name}")
    r = subprocess.run(["/bin/sh", "-c", cmd], cwd=scripts, capture_output=True, text=True)
    print(f"stdout: {r.stdout.strip() or '(empty)'}")
    print(f"stderr: {r.stderr.strip() or '(empty)'}")
    print(f"exit: {r.returncode}")
    print()


def snippet(name, lang, code):
    """A page's code block, run as the page shows it."""
    print(f"== case: {name}")
    path = os.path.join(scripts, "snippet." + ("py" if lang == "python" else "sh"))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(code)
    exe = [sys.executable, path] if lang == "python" else ["/bin/sh", path]
    r = subprocess.run(exe, cwd=scripts, capture_output=True, text=True)
    sys.stdout.write(r.stdout + r.stderr)
    os.remove(path)
    print()


print(f"installed: {TAG} from {REPO}")
print(f"python: {sys.version.split()[0]}")
print()

term("version", "python3 paper_meta.py --version")
term("help", "python3 paper_meta.py --help")
term("first run", "python3 paper_meta.py 10.1073/pnas.2528246123 --email you@example.org --similar 3")
term("full text",
     "python3 paper_meta.py 10.1073/pnas.2528246123 --similar 0 --fulltext papers | tail -n 3",
     "ls papers",
     'grep -n "^## " papers/PMC13462932.txt',
     'grep -n -i "competing" papers/PMC13462932.txt')
term("closed paper, no email", "python3 paper_meta.py 10.1111/jssr.70101 --similar 0 | grep -v '^Abstract'")
term("retracted paper", "python3 paper_meta.py 10.1057/s41599-025-04787-y --similar 0 --email you@example.org | grep -E '^(Title|!!|== |INTEGRITY|PMID)'")
term("bad input", 'python3 paper_meta.py "not a doi"')
streams("bad input streams", 'python3 paper_meta.py "not a doi"')
term("identifier forms",
     "python3 paper_meta.py https://onlinelibrary.wiley.com/doi/full/10.1111/jssr.70101 --similar 0 --json | python3 -c \"import json,sys; print(json.load(sys.stdin)['doi'])\"",
     "python3 paper_meta.py PMID:42566467 --similar 0 --json | python3 -c \"import json,sys; print(json.load(sys.stdin)['doi'])\"",
     "python3 paper_meta.py PMC13462932 --similar 0 --json | python3 -c \"import json,sys; print(json.load(sys.stdin)['doi'])\"")

snippet("recipe: json fields", "python", """\
import json
import subprocess

out = subprocess.run(
    ["python3", "paper_meta.py", "10.1073/pnas.2528246123", "--similar", "0", "--json"],
    capture_output=True, text=True, check=True,
).stdout
paper = json.loads(out)
print(paper["crossref"]["journal"])
print(paper["crossref"]["milestones"])
print(paper["pubmed"]["coi"])
print(paper["next"][0])
""")

snippet("recipe: several DOIs", "sh", """\
for doi in 10.1073/pnas.2528246123 10.1111/jssr.70101 10.1057/s41599-025-04787-y; do
  python3 paper_meta.py "$doi" --similar 0 | grep -E "^Title:|^!! "
done
""")

term("unit tests", "python3 tests/test_paper_meta.py 2>&1 | tail -n 1", cwd=clone)

shutil.rmtree(root, ignore_errors=True)
