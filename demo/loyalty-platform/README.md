# Loyalty Platform Demo

This directory is the second real Rupify-to-Speckify end-to-end demo in this repo.

Source example:

- `/Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform`

## Purpose

This demo validates the current pipeline against a second real Rupify example that differs
materially from the IT systems inventory V2 fixture.

What it demonstrates:

1. the Rupify planning export can be generated and imported cleanly from a second real
   example
2. Speckify can run the full import, validation, bundle generation, delivery export, and
   round-trip feedback pipeline on that export
3. the current pipeline remains deterministic even when the upstream export contains no
   ready normative elements

## Current Result

The loyalty-platform planning export is structurally clean, but it currently yields zero
planning units because Rupify marks no elements as ready normative in this example.

That makes this a useful contrast fixture:

- `it-systems-inventory-v2`: rich ready-normative bundle with decomposed outputs
- `loyalty-platform`: clean but empty bundle that exercises the no-ready-elements path

## Layout

- `input/loyalty-speckify-planning-export.json`: generated Rupify planning export used for
  this demo
- `output/import-report.json`: structured import analysis
- `output/import-report.md`: human-readable import analysis
- `output/planning-bundle.json`: generated Speckify planning bundle
- `output/github-delivery/`: GitHub delivery export surface
- `output/rupify-feedback/`: round-trip feedback surface
- `output/speckified-specification.md`: consolidated specification view

## Regenerate

```bash
cd /Volumes/Data/GitHub/Peterbb148/rupify
uv run python -m rupify_tools.planning_export_cli \
  --model examples/loyalty-platform/specops-model.json \
  --output /tmp/loyalty-speckify-planning-export.json

cd /Volumes/Data/GitHub/Peterbb148/speckify
uv run speckify-demo-rupify-handoff \
  /tmp/loyalty-speckify-planning-export.json \
  demo/loyalty-platform
```
