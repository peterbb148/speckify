# Fixtures

This directory contains example fixtures for the Speckify planning pipeline.

## Layout

- `rupify-export/`: example upstream planning exports shaped for Speckify consumption
- `speckify-bundle/`: expected downstream planning bundles derived from the paired export
- `rendered-issues/`: rendered Markdown issue fixtures derived from planning bundles

## Current Scenarios

### `authentication-basic`

Exercises:

- stable source identifiers
- requirement to use-case-step traceability
- a non-blocking ambiguity
- a precondition constraint
- one-to-one planning derivation from a simple authentication flow
- rendered GitHub issue projections for both implementation units
