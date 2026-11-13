# Economic Reasoning Engineering

[![CI](https://github.com/FrancyJGLisboa/economic-reasoning-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/FrancyJGLisboa/economic-reasoning-engineering/actions/workflows/ci.yml)

Economic Reasoning Engineering is an agent skill for reconstructing economic arguments from authorized source material. It produces traceable opinions, reasoning methods, and portable context packages.

Version 0.3 is the current stable format. It uses Python's standard library and supports Python 3.9 or newer.

## Quick start

After the one-time installation, your normal workflow has two steps:

1. Invoke the skill in your agent.
2. Paste the material, attach a readable file, or provide its accessible location.

In Codex:

```text
$economic-reasoning-engineering

Analyze the material below:
[paste your transcript or document]
```

In Claude Code:

```text
/economic-reasoning-engineering

Analyze the material below:
[paste your transcript or document]
```

You can also attach the material or include its path in the same request.
An optional question can focus the analysis. It is not required.

The agent creates the run directory, prepares sources, extracts the reasoning, validates the artifacts, and builds the portable package.
You do not need to create folders, run Python commands, edit configuration, or choose an artifact schema for each analysis.

The result includes an analysis summary, a link to `output/CONTEXT.md`, a validation receipt, and the remaining evidence gaps.
The agent asks for more information only when it cannot access the material or a missing requirement prevents analysis.
If the environment cannot read the material or execute validation, the agent reports that limit. It does not claim a complete package.

## What the skill produces

The skill converts documents, transcripts, and expert discussions into two layers:

- A working extraction with source records, episodes, opinions, reasoning cards, graph data, and reviews.
- A portable output directory with bundled evidence, stable identifiers, schemas, navigation tools, hashes, and validation receipts.

The portable output is a file-based context package. An agent can inspect it without the original conversation or working directory.

The package preserves evidence and judgment boundaries. It does not prove that an economic claim is true.

## Processing model

```text
authorized sources
       |
       v
working/corpus  ->  working/output  ->  package builder  ->  output/
 source text         extraction          integrity            portable context
                                            checks             and navigation
```

The workflow keeps source statements separate from analyst inference and investigator proposals. It records missing evidence instead of inventing values.

## Install for Codex and Claude Code

Use one clone and create a link for each agent:

```bash
skill_store="${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills"
mkdir -p "$skill_store" "$HOME/.codex/skills" "$HOME/.claude/skills"
git clone https://github.com/FrancyJGLisboa/economic-reasoning-engineering.git \
  "$skill_store/economic-reasoning-engineering"
ln -s "$skill_store/economic-reasoning-engineering" \
  "$HOME/.codex/skills/economic-reasoning-engineering"
ln -s "$skill_store/economic-reasoning-engineering" \
  "$HOME/.claude/skills/economic-reasoning-engineering"
```

Stop if either destination already exists. Inspect the existing installation before you replace it.

The installation is a one-time setup. If the skill does not appear, start a new agent session.

Use `$economic-reasoning-engineering` in Codex or `/economic-reasoning-engineering` in Claude Code.

Update an installation with:

```bash
git -C "${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/economic-reasoning-engineering" pull --ff-only
```

## Use the result

Open `CONTEXT.md` in the output directory to inspect the analysis or give the complete directory to another agent.
The agent handles the working directories, validation, package building, and navigation tests during the run.

Direct Python commands are optional. See the [manual workflow reference](docs/manual-workflow.md) for maintenance and artifact inspection.

## Repository map

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Agent entry point and workflow |
| [`references/MASTER_PROMPT.md`](references/MASTER_PROMPT.md) | Extraction phases and evidence rules |
| [`references/PORTABLE_CONTEXT.md`](references/PORTABLE_CONTEXT.md) | Portable package contract |
| [`schemas/package.schema.json`](schemas/package.schema.json) | Structured artifact definitions |
| [`scripts/context_package.py`](scripts/context_package.py) | Package builder, reader, and validator |
| [`scripts/validate.py`](scripts/validate.py) | Legacy working-extraction validator |
| [`docs/architecture.md`](docs/architecture.md) | Components and trust boundaries |
| [`docs/artifact-contract.md`](docs/artifact-contract.md) | Artifact identity and evidence rules |
| [`docs/verification.md`](docs/verification.md) | Test scope and verification commands |
| [`docs/manual-workflow.md`](docs/manual-workflow.md) | Optional commands for maintenance and artifact inspection |
| [`docs/research-status.md`](docs/research-status.md) | Stable and experimental capability boundary |
| [`AGENTS.md`](AGENTS.md) | Maintenance rules for coding agents |

## Development tests

The test suite has no third-party runtime dependency.

```bash
python3 -m compileall -q scripts
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The tests cover package relocation, source anchors, identifier integrity, path confinement, tamper detection, receipt freshness, and refusal conditions.

See [`docs/verification.md`](docs/verification.md) for the exact test boundary.

## Research status

Selective package reading remains experimental. It is not part of the stable v0.3 source or its capability claims.

Human review of economic quality remains necessary. Automated tests do not establish causal validity, source authority, or model-independent usefulness.

See [`docs/research-status.md`](docs/research-status.md) for the promotion criteria.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before you submit a change. Do not commit private transcripts, generated investigation packages, credentials, or local machine paths.

## License

This repository does not contain a license file. Copyright law applies by default. Do not assume reuse rights beyond those provided by law.
