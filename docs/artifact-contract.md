# Artifact contract

This document gives maintainers a short map of the portable contract. `references/PORTABLE_CONTEXT.md` remains the normative contract.

## Record identity

Each source uses `source_id`. Each other record uses `id`.

Local identifiers remain stable within one run and collection. A global identifier has this form:

```text
run_id::collection::local_id
```

Consumers must not merge records from different runs by local identifier alone.

## Evidence reference

A portable evidence reference contains:

- `source_id`
- `source_global_id`
- `filename`
- `locator`
- `anchor`
- An optional verified line number

The referenced file must exist inside the package. The exact anchor must occur in that file.

## Record classes

The package uses these broad classes:

- `source_statement`
- `analyst_inference`
- `investigator_proposal`
- `test_result`
- `mixed`

These classes describe origin. They do not describe truth or validation strength.

## Reasoning method minimum

The base card schema retains trigger, inputs, operations, alternatives, tests, and abstention fields.
Faithful extraction uses explicit NOT_DOCUMENTED values when the source omits these details.

Declared-profile runs also require nonempty `expected_outputs`. Legacy runs can omit that field.

Documented cards identify their speaker and link each step to their source evidence.
Missing method detail creates a documentation gap. It does not require inventing or rejecting a documented fragment.
Speaker abstention rules remain separate from extraction gaps.

## Integrity

The manifest hashes each payload file except itself and validation receipts. A receipt binds the manifest bytes and bundled validator code.

Any payload change invalidates an earlier passing receipt. Receipt verification reruns the current checks.

## Compatibility changes

Additive optional fields can remain within v0.3 when older readers ignore them safely.

Changes to required fields, identifier semantics, hashes, or refusal behavior require a format review and migration plan.

## Fidelity metadata

Declared modes and step evidence follow the normative portable contract.
Critique remains optional, authorized, separately indexed, and outside documented speaker methods.
Legacy packages retain their original provenance and mode absence.
The extension uses optional fields with conditional checks for explicitly declared modes.
Existing package format, identifiers, hashes, and legacy refusal behavior remain unchanged.
New critique collections require the package's bundled reader. Older readers do not support the new collection.
