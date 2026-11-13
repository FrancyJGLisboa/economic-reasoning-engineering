# Agent maintenance guide

## Scope

This repository is the source for the Economic Reasoning Engineering skill.
The repository root is also the installable skill directory.

## Read first

Read these files before you change behavior:

1. `SKILL.md`
2. `references/MASTER_PROMPT.md`
3. `references/PORTABLE_CONTEXT.md`
4. `docs/architecture.md`
5. `docs/verification.md`

## Stable boundary

Version 0.3 is the stable package format.
Keep experimental selective reading outside the stable path.
Do not claim human review unless a named human completed it.
Do not publish source transcripts or generated investigation packages.
Do not add private paths, tokens, credentials, or personal evaluation artifacts.

## Change rules

Keep source statements, analyst inference, and investigator proposals separate.
Preserve local identifier behavior and global identifier format.
Do not weaken path confinement or overwrite protection.
Keep runtime code compatible with Python 3.9 or newer.
Use the Python standard library unless maintainers approve a dependency.
Update the contract and tests when an artifact shape changes.

## Required checks

Run these commands from the repository root:

```bash
python3 -m compileall -q scripts
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The test command must execute at least one test.
Review `git diff --check` and `git diff` before each commit.
Do not report success when a required check did not run.

## Documentation

Write public documentation in English.
Use short sentences and active voice.
State limits beside capability claims.
Keep commands reproducible from the repository root.
