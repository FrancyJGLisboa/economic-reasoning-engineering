# Operations profile implementation

## Outcome and scope

Add an operations profile to the existing evidence workflow. Keep economics as the default.
The user still supplies only an invocation and source material. A question remains optional.
Keep package format 0.3, existing identifiers, and legacy package support.
Exclude strategy profiles, selective reading promotion, dependencies, and a new runner.

## Decisions

The master prompt holds shared extraction rules. Two profile references hold domain-specific guidance.
Select the profile from the requested decision and source argument. Do not select from isolated keywords.
Record the profile, selection reason, and scope limits in state and manifest.
Require explicit expected outputs when a run declares a profile. Legacy runs can omit the new metadata.
Structural validation checks these declarations. It cannot establish correct profile selection or method quality.

## Tasks and acceptance

The primary agent owns all tasks. No delegation is required.

1. Update instructions and profile references. Keep invocation sufficient and economic extraction available.
2. Update builder, schema, and tests. Reject unknown profiles, metadata drift, and missing declared-method outputs.
3. Test the fertilizer transcript privately. Inspect process dependencies, arithmetic, delivery limits, and investigator additions.
4. Run repository checks, review the diff, publish source changes, and synchronize installed skill files.

Each task depends on the previous task. Public files must exclude private source material and evaluation paths.
Engineering evidence must include legacy compatibility, profile metadata integrity, and relocated package validation.
Product evidence must include the real transcript trial. Experience evidence must include a readable package entry point.

## Plan challenge

Executability review: existing builder, schema checker, and test fixtures support optional metadata without new infrastructure.
Failure review: a profile label cannot prove analysis quality. Inspect a real source and state evaluation limits separately.
Failure review: fixed durations can double-count parallel work. Operations instructions must distinguish dependencies and current process state.
Failure review: missing metadata must preserve legacy behavior. Unknown or inconsistent declared metadata must fail validation.

## Status

Implementation and local verification are complete. Publish this source revision and synchronize the shared installation.

## Verification evidence

Local verification on 2026-11-13 used Python's standard library.
The suite passes 51 tests, including legacy compatibility and declared-profile failure cases.
Compilation, repository checks, skill validation, and whitespace checks pass.

A private trial adapted the existing fertilizer transcript extraction to the operations profile.
The source argues primarily about import stages and delivery risk. Financial exposure remains secondary.
The trial retained three methods, added expected outputs, and recorded a conditional stage map.
It checked four arithmetic results: 115–116 illustrative days, subtotal 110 rather than 120, 8.57 operating days, and BRL 4480.
The package contains 77 indexed records. Its validator passes without warnings.
A relocated copy resolves the deadline method, exact evidence, investigator additions, and abstention conditions.

This was a same-agent adaptation. It does not establish independent agent behavior, human quality, or improved domain judgment.
No source transcript or private trial artifact is included in this repository.
Selective reading remains experimental. Strategy profiles and empirical method validation remain outside this change.
