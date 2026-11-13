# Manual workflow reference

These commands are for maintainers and users who want direct control of the generated artifacts.
The normal user workflow is to invoke the skill and provide the source material.
The agent creates directories, validates extraction artifacts, builds the package, and tests navigation.

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
