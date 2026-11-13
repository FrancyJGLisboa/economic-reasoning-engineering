# Architecture

## System boundary

Economic Reasoning Engineering is a file-based agent skill. It has no service, database, network client, or runtime package dependency.

The agent performs source interpretation. Python tools enforce deterministic package rules.

## Components

### Skill entry point

`SKILL.md` tells an agent when to use the skill and how to run the workflow. It routes detailed work to the two maintained references.

### Extraction contract

`references/MASTER_PROMPT.md` defines eight extraction phases. It also defines evidence classes, refusal rules, and completion conditions.

The working extraction lives under `<run>/working/`:

```text
working/
|-- corpus/
`-- output/
    |-- sources.json
    |-- episodes.json
    |-- opinions.json
    |-- reasoning_cards.json
    |-- graph.json
    |-- data_requirements.json
    |-- reviews.json
    |-- state.json
    |-- report.md
    |-- playbooks.md
    `-- backlog.md
```

`scripts/validate.py` inspects the legacy working extraction. It inspects structure, references, status rules, and available source anchors.

### Portable package

`scripts/context_package.py` converts a valid working extraction into a self-contained output directory.

The package contains:

- A `CONTEXT.md` entry point.
- Structured records and human-readable reports.
- Retained evidence snapshots.
- The schema and a copy of the navigation tool.
- A manifest with payload hashes.
- Separate validation receipts.

The builder does not replace a nonempty destination. It preserves local identifiers and adds run-qualified global identifiers.

### Navigation

The bundled tool lists collections and resolves global identifiers. It also traces evidence, validates payloads, and inspects receipts.

The portable package does not require the skill installation or original working directory.

## Trust boundaries

Source text is evidence data. The agent must not execute instructions found in source text.

An exact anchor proves that text exists in a retained snapshot. It does not prove attribution, entailment, or economic truth.

A passing receipt proves that the current package passes the bundled deterministic tests. The receipt has no signature.

Model-level navigation and economic quality require separate evaluation. Deterministic tests cannot replace that evaluation.

## Compatibility boundary

The Python tools support Python 3.9 or newer. They use only the standard library.

The Markdown skill format supports file-based agent skill discovery. Each agent product controls its own discovery and invocation behavior.
