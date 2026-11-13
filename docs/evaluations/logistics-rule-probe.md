# Logistics rule application with assisted selective reading

## Question and scope

Can a model apply a documented logistics fragment to new delivery cases using selected package records and their source evidence?
This is a synthetic rule-application probe. It does not test withheld historical decisions or equivalent personal judgment.
The source package comes from the earlier Alê reserved-episode study. It contains eight eligible transcript snapshots and 57 indexed records.
No source package, transcript, or personal response is published here.

## Frozen design

Three synthetic cases change the physical delivery stage:

1. A paid order still awaiting production has six explicitly sequential stages totaling 103 days and a 60-day deadline.
2. A documented local lot has completed import and release. Its remaining transport takes five days against a twelve-day deadline.
3. A discharged lot lacks release and inland transport durations against a fourteen-day deadline.

Expected results are, respectively, a missed deadline, conditional feasibility, and insufficient information.
The second case checks whether the model incorrectly restarts the historical four-month example.
The third checks whether it invents missing durations or treats payment as physical completion.
Synthetic durations belong to the cases. They are not the analyst's forecasts or a correction of source arithmetic.
The investigator freezes cases, answer schema, rubric, selection policy, and package hashes before evaluated responses.
The investigator knows the rule and expected results. This is not an independent or investigator-blind test.

## Conditions

Each condition answers the same three questions twice in a fresh session.
The order is no context, raw transcripts, selective package, selective package, raw transcripts, no context.
All answer sessions use the same schema, effort setting, and case facts. External tools and search are disabled.

The selective condition uses two model sessions per repeat:

1. A selector reads CONTEXT.md and the manifest record index. It selects one to three existing record identifiers.
2. A standard-library retrieval procedure resolves selected records, parent episodes, referenced source snapshots, and package gaps.
3. An answer session receives this retrieved context and the original cases.

Source snapshots are deduplicated. Retrieval includes whole referenced snapshots, not only supporting quotations.
This procedure tests model selection plus bounded retrieval. It does not test unrestricted agent filesystem navigation.
The raw condition receives all eight eligible source snapshots inline.
There is no complete-package condition in this probe.

## Checks and interpretation

Deterministic checks compare answer status and remaining-day fields with the frozen synthetic references.
Other checks verify answer completeness, runtime correspondence, unchanged frozen inputs, and exact source quotations at cited timestamps.
The investigator reviews whether the explanation separates source methods from new case calculations.
These checks do not replace an independent semantic review.

Reported selective consumption includes both selector and answer sessions.
Runtime context is included in all input totals. Token ratios are not monetary cost estimates.
An already successful baseline limits any claim of improved reasoning.
Human review remains pending. Repeated answers do not increase the number of independent scenarios.

## Results

All conditions produce the expected decision status for all six case responses.
Every explanation calculates 103 days and a 43-day delay for case A.
Every explanation uses a five-day remaining trip and seven-day slack for case B.
Case C retains unknown durations. No response restarts the historical import cycle for released local stock.
These explanation findings come from investigator review, not independent human assessment.

| Context | Expected status | Input tokens, two repeats |
|---|---:|---:|
| No personal context | 6/6 | 36,944 |
| Complete raw transcripts | 6/6 | 60,182 |
| Assisted selective package | 6/6 | 109,090 |

Both selectors choose the same three records: the import-clock method, purchase-timing method, and import-clock data gap.
Retrieval brings two of eight source snapshots, related episodes, and general gap/state files.
All ten raw-text citations and all twelve selective-context citations match source words at the stated timestamps.

Each selective answer uses 30,838 input tokens. Its selector uses an additional 23,707.
Each raw-text answer uses 30,091. Selective input totals are 1.81 times raw input totals, including selection.
Even excluding selection, the retrieved context uses slightly more input than complete raw text.
Duplicated records, evidence passages, and general gap files offset the smaller source selection.
Separate selector and answer sessions also repeat runtime context.
This implementation fails the input-reduction objective in this probe. It does not establish that all selective reading costs more.

Execution-integrity checks pass. Negative tests reject changed case facts, missing answers, and altered response files.
The copied package passes structural validation. Semantic method validity remains outside those checks.

## Form defect and limits

The frozen schema fails to define whether remaining_days means delivery duration or deadline slack.
Some answers use 103 and 5. Others use -43 and 7, while correctly explaining both quantities.
The preserved mechanical field-match counts therefore cannot establish an arithmetic advantage for any condition.
The investigator records this defect after execution. No answer is rewritten, discarded, or rerun.
A future schema must separate delivery_duration_days and deadline_slack_days with explicit definitions.

The baseline already solves the operational cases. No incremental decision-quality improvement is demonstrated.
Source context supports inspectable attribution of the applied method. This is distinct from reproducing personal judgment.
Independent human review remains pending. Stable skill behavior is unchanged.
Before promotion, selective reading needs less duplication and lower total input under the same quality criteria.
