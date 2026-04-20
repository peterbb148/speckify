# Decomposition Rule Catalog

This directory contains the first machine-readable decomposition rule catalog for
Speckify.

## Purpose

The catalog is the bridge between the prose note in
`docs/decomposition-and-validation-rules.md` and future transformation code.

## Current Files

- `decomposition-rules.json`: view-specific rules, mapping patterns, and blocking
  conditions

## Mapping To Prose

The catalog does not replace the prose note. It encodes the same concepts in a structured
form that later tooling can load directly:

- view-specific decomposition guidance
- one-to-one, one-to-many, and many-to-one mapping patterns
- blocking and partial conditions
- implementation-sized slicing heuristics

When the prose note changes materially, update the catalog in the same change.
