# Contributing

Changes should preserve evidence traceability and refusal behavior.

## Before you change code

1. Read `AGENTS.md` and the linked contracts.
2. State the behavior that will change.
3. Add a failing test for a defect or new invariant when practical.
4. Keep experimental work separate from stable v0.3 behavior.

## Source material policy

Use synthetic fixtures in automated tests. Keep fixtures short and clearly labeled.

Do not commit:

- Private or licensed transcripts.
- Generated investigation packages.
- Personal evaluation records.
- Credentials, access tokens, or machine-specific paths.

## Verification

Run all repository checks:

```bash
python3 -m compileall -q scripts
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/check_repository.py
git diff --check
```

The project has no third-party Python dependency. No package audit applies to the current source tree.

## Pull requests

Describe the changed behavior, verification commands, and known limits. Link each contract change to its tests.

Do not describe structural validation as economic validation. Identify any human evaluation by evaluator, method, sample, and limits.

## License status

The repository has no license file. A contribution does not create a project license.
