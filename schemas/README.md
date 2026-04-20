# Speckify Schemas

This directory contains the first machine-readable schema set for Speckify planning
artifacts.

## Layout

- `source-anchor.schema.json`
- `spec-unit.schema.json`
- `implementation-unit.schema.json`
- `verification-unit.schema.json`
- `trace-bundle.schema.json`
- `planning-bundle.schema.json`

## Versioning

The schema set currently uses `schema_version: 1` at the planning-bundle level.

Until a transformation engine exists, schema changes should remain tightly aligned with
the merged planning notes under `docs/`. When a schema change materially alters the
contract surface, increment the bundle schema version and update the relevant design
notes in the same change.
