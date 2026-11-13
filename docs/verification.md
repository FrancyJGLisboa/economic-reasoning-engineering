# Verification

## Local commands

Run all commands from the repository root:

```bash
python3 -m compileall -q scripts
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The unit suite must report a nonzero test count and return exit code 0.

## What the suite checks

The current tests cover:

- Valid and invalid working extractions.
- Faithful fragments, speaker attribution declarations, and step evidence indexes.
- Optional critique authorization declarations, separation, indexing, and relocation.
- Declared profiles, required method outputs, metadata consistency, and legacy compatibility.
- Exact source-anchor checks.
- Missing and mismatched source evidence.
- Cross-record identifier integrity.
- Package relocation without the original corpus.
- Path traversal and escaping symbolic links.
- Nonempty destination refusal.
- Payload tampering and stale receipts.
- Invalid query refusal.
- False model-evaluation claim refusal.

`scripts/check_repository.py` checks required files, metadata, local links, excluded research artifacts, private paths, and common credential forms.

## What the suite does not check

The suite does not establish:

- Economic truth or causal validity.
- Source authenticity or legal authority.
- Complete compatibility with every model or agent product.
- Better task performance from selective reading.
- Human usability or economic judgment quality.

Those claims need separate evidence. Record human evaluation by evaluator, method, sample, and limits.

## Continuous integration

GitHub Actions runs the checks on Python 3.9, 3.11, and 3.13 with Ubuntu 24.04.
The runner image is fixed because Python 3.9 builds are unavailable for Ubuntu 26.04. The workflow uses no project dependency installation step.

The local environment can test another supported Python version. State that version in verification evidence.
