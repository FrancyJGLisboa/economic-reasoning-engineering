# Research status

## Stable scope

Version 0.3 supports complete portable packages and deterministic navigation. The stable code builds, validates, lists, queries, and inspects package receipts.

## Selective reading

Selective package reading remains a research branch. The current stable source does not expose it as a supported mode.

Before promotion, an evaluation must compare selective and complete reading under equal conditions. The evaluation also needs independent human review.

The review should measure:

- Source fidelity.
- Method specificity.
- Missing-data identification.
- Competing-hypothesis coverage.
- Calibrated abstention.
- Input and cost reduction.

Resource savings alone do not establish equal output quality.

## Compatibility claim

The package uses ordinary files, Markdown, JSON, and Python. This design supports inspection by many agents with file access.

The project does not claim compatibility with every LLM. Each target agent needs a separate navigation evaluation.
