# IT Systems Inventory V2 Demo

This directory is the Speckify-side demo and test location for the Rupify hand-off bundle
from:

- `/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2`

## Purpose

This demo verifies two things:

1. whether the Rupify hand-off export can be imported cleanly with no additional changes
   required
2. whether Speckify can run the real import, generation, validation, and rendering path
   against that bundle and produce stable checked-in outputs

## Layout

- `input/`: unchanged copy of the upstream Rupify hand-off export used for this demo
- `output/import-report.json`: structured import analysis
- `output/import-report.md`: human-readable import analysis
- `output/planning-bundle.json`: generated Speckify planning bundle
- `output/github-delivery/`: machine-readable GitHub issue export plus per-issue Markdown bodies
- `output/rupify-feedback/`: structured round-trip change records and upstream feedback proposals
- `output/rendered-issues/`: issue-ready Markdown projections generated from the bundle
- `output/speckified-specification.md`: consolidated specification view generated from the
  bundle

These checked-in files are the end-to-end regression surface for this demo. If the Rupify
hand-off contract or Speckify generation pipeline drifts, the regression test should fail
instead of silently changing behavior.

## Run

```bash
uv run speckify-demo-rupify-handoff \
  /Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json \
  demo/it-systems-inventory-v2
```
