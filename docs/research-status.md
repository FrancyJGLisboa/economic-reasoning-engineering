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

## Documented judgment transfer

The [first judgment-transfer pilot](evaluations/judgment-transfer-pilot.md) compared three historical judgments and one attribution control.
Both conditions matched all frozen multiple-choice conclusions and primary criteria.
The package supplied resolvable method references. It did not improve agreement on this sample.
The baseline reached the test ceiling. This does not establish identical judgment or make the package unnecessary.
Human review remains pending. The subsequent open-response audit appears below.

## Open-response personal decision case

The [Sivers open-response audit](evaluations/sivers-open-response.md) found a difference in predicted pricing policy across context conditions.
Both package responses predicted the additional-fee removal described in the reserved account. Both baseline responses predicted charging after launch.
Model-assessed explanatory alignment did not improve overall.
All sessions recognized the public case, so the experiment cannot isolate personal-judgment transfer from prior story knowledge.
The observation remains exploratory. Human review is pending.
