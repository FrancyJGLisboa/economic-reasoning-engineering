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

A reusable reasoning card needs a trigger, named inputs, ordered operations, competing explanations, a discrimination test, and abstention conditions.

The card must identify source evidence and investigator additions. Missing method detail requires abstention.

## Integrity

The manifest hashes each payload file except itself and validation receipts. A receipt binds the manifest bytes and bundled validator code.

Any payload change invalidates an earlier passing receipt. Receipt verification reruns the current checks.

## Compatibility changes

Additive optional fields can remain within v0.3 when older readers ignore them safely.

Changes to required fields, identifier semantics, hashes, or refusal behavior require a format review and migration plan.
