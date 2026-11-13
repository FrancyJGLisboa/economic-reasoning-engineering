# Publication evidence

Local verification ran on 2026-11-13 at 13:01 BRT.

## Required evidence

| Criterion | Layer | Method | Environment | Result | Artifact | Limits |
|---|---|---|---|---|---|---|
| Python source compiles | Engineering | `python3 -m compileall -q scripts` | macOS, Python 3.14.7 | PASS | Command output | Does not execute behavior. |
| Unit suite passes | Engineering | `python3 -m unittest discover -s scripts -p 'test_*.py' -v` | macOS, Python 3.14.7 | PASS, 41 tests | Test output | Does not establish economic validity. |
| Repository contract passes | Engineering | `python3 scripts/check_repository.py` | macOS, Python 3.14.7 | PASS | Command output | Pattern tests cannot detect every secret. |
| Skill metadata passes | Product | Skill Creator `quick_validate.py` | Local Skill Creator | PASS | `Skill is valid!` | Does not evaluate behavior. |
| Codex and Claude Code links resolve | Product | Validate temporary links in both skill directories | Local filesystem | PASS | Two valid skill results | Does not test product UI discovery. |
| Documentation is navigable | Experience | Link test, structure review, and STE lint | Local repository | PASS | Contract and linter output | Maintainer inspection only. |
| Remote commit matches local | Engineering | Compare local and remote commit IDs | GitHub | PENDING | Remote reference | Proves Git object identity only. |

The source tree has no dependency manifest or third-party Python import. A package dependency audit does not apply to this version.
