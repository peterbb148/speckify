# Loyalty Platform V2 Demo

This directory is the second real Rupify-to-Speckify end-to-end demo in this repo.

Source example:

- `/Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform-v2`

## Purpose

This demo validates the current Speckify pipeline against a second real V2 publication
bundle from Rupify.

What it demonstrates:

1. the Rupify loyalty-platform V2 planning export imports cleanly
2. Speckify can generate a substantial planning bundle, rendered issues, GitHub delivery
   export, and round-trip feedback outputs from a second real source
3. the current pipeline now generalizes beyond the IT systems inventory V2 fixture

## Current Result

The loyalty-platform V2 planning export currently yields:

- 108 planning-export elements
- 62 ready normative elements
- 66 generated implementation units
- 66 generated verification units
- 4 dependency edges
- 5 assembly rules

This gives a materially different second real fixture with use cases, use-case steps,
extensions, scenarios, invariants, transitions, and constraints.

## Layout

- `input/speckify-planning-export.json`: checked-in Rupify planning export used for this demo
- `output/import-report.json`: structured import analysis
- `output/import-report.md`: human-readable import analysis
- `output/planning-bundle.json`: generated Speckify planning bundle
- `output/rendered-issues/`: rendered issue artifacts
- `output/github-delivery/`: GitHub delivery export surface
- `output/rupify-feedback/`: round-trip feedback surface
- `output/speckified-specification.md`: consolidated specification view

## Regenerate

```bash
cd /Volumes/Data/GitHub/Peterbb148/speckify
uv run speckify-demo-rupify-handoff \
  /Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform-v2/exports/speckify-planning-export.json \
  demo/loyalty-platform-v2
```
