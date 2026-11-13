# Publication plan

Status: IN_PROGRESS

## Outcome

Publish the stable v0.3 skill in a public repository that humans and file-based agents can navigate.

## Non-goals

- Do not publish transcripts, generated investigation packages, or personal evaluation artifacts.
- Do not promote selective reading to stable behavior.
- Do not add a license without the owner's choice.
- Do not change the installed local skill during repository preparation.

## Constraints

- Keep the repository root directly installable as a skill.
- Keep runtime code on the Python standard library.
- Preserve stable package behavior and refusal rules.
- Provide installation paths for Codex and Claude Code.

## Acceptance criteria

1. The repository contains the stable skill, references, schema, tools, and tests.
2. Public documentation explains installation, use, architecture, artifacts, and limits.
3. Repository checks reject private paths and common credential forms.
4. Unit tests and skill metadata validation pass.
5. The default branch exists on the named GitHub remote.
6. The remote commit matches the verified local commit.

## Risks and controls

| Risk | Control |
|---|---|
| Private source publication | Exclude transcripts and research artifacts. Run repository checks. |
| Capability overstatement | State deterministic and human-evaluation limits beside claims. |
| Package regression | Run the stable suite, repository tests, and continuous integration. |
| Agent navigation drift | Keep the root installable and maintain an explicit repository map. |
| Unlicensed reuse assumptions | State that no license file exists. |

## Verification

See `evidence.md` for the publication record.
