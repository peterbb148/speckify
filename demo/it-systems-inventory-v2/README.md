# IT Systems Inventory V2 Demo

This directory is the Speckify-side demo and test location for the Rupify hand-off bundle
from:

- `/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2`

## Purpose

This demo verifies two things:

1. whether the Rupify hand-off export can be imported cleanly with no additional changes
   required
2. whether Speckify can produce a first specification artifact from that real hand-off
   bundle

The current demo output is a single consolidated Speckified specification document. That
is a first demo artifact, not the full long-term Speckify output model. The broader design
still targets structured planning bundles, issue-ready artifacts, and verification
definitions.

## Layout

- `input/`: unchanged copy of the upstream Rupify hand-off export used for this demo
- `output/import-report.json`: structured import analysis
- `output/import-report.md`: human-readable import analysis
- `output/speckified-specification.md`: first consolidated Speckified specification
  artifact derived from the imported bundle

## Run

```bash
uv run speckify-demo-rupify-handoff \
  /Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json \
  demo/it-systems-inventory-v2
```
