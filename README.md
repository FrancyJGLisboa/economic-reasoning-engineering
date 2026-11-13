# Economic Reasoning Engineering

[![CI](https://github.com/FrancyJGLisboa/economic-reasoning-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/FrancyJGLisboa/economic-reasoning-engineering/actions/workflows/ci.yml)

Economic Reasoning Engineering is an agent skill for reconstructing economic arguments from authorized source material. It produces traceable opinions, reasoning methods, and portable context packages.

Version 0.3 is the current stable format. It uses Python's standard library and supports Python 3.9 or newer.

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

Restart the agent after installation. Invoke the skill as `$economic-reasoning-engineering` in Codex. Invoke it as `/economic-reasoning-engineering` in Claude Code.

Update an installation with:

```bash
git -C "${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/economic-reasoning-engineering" pull --ff-only
```

## Run an investigation

Create a writable run directory. Keep source material outside the skill installation.

```text
my-investigation/
`-- working/
    `-- corpus/
        `-- authorized-source.txt
```

Ask the agent to use the skill on that corpus. The agent writes extraction artifacts under `working/output/`.

Validate the extraction:

```bash
python3 /path/to/economic-reasoning-engineering/scripts/validate.py \
  --project /path/to/my-investigation/working
```

Build the portable package:

```bash
python3 /path/to/economic-reasoning-engineering/scripts/context_package.py build \
  --project /path/to/my-investigation/working \
  --destination /path/to/my-investigation/output \
  --title "Investigation title"
```

The builder refuses to replace a nonempty destination.

## Navigate a portable package

Start with `CONTEXT.md` in the generated output directory. The bundled tool supports deterministic inspection:

```bash
python3 tools/context_package.py list --package . --collection reasoning_cards
python3 tools/context_package.py query --package . --id GLOBAL_ID --trace
python3 tools/context_package.py validate --package .
python3 tools/context_package.py check-receipt \
  --package . \
  --receipt validation/RECEIPT.json
```

`query --trace` follows a record to its episode and exact source anchors. The query command rejects invalid packages and local-only identifiers.

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
| [`docs/research-status.md`](docs/research-status.md) | Stable and experimental capability boundary |
| [`AGENTS.md`](AGENTS.md) | Maintenance rules for coding agents |

## Test the repository

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
