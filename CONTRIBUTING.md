# Contributing

## Scope

Speckify is a formal downstream specification system. Contributions should preserve that
design:

- Rupify exports are the structured upstream contract
- Speckify decomposes only from explicit typed source structure
- delivery artifacts must remain traceable back to source anchors
- round-trip safety matters more than opportunistic convenience
- publication-ready output must not rely on guessed semantics

## Local Setup

```bash
uv sync
```

## Useful Commands

Run the full test suite:

```bash
uv run python -m unittest discover
```

Run the constitutional audit:

```bash
uv run speckify-check-constitution --all-files
```

Validate a generated bundle from a Rupify export:

```bash
uv run speckify-validate-generated-bundle \
  /Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json
```

Replay the end-to-end demo pipeline:

```bash
uv run speckify-demo-rupify-handoff \
  /Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json \
  /tmp/speckify-demo
```

## Contribution Rules

- do not add demo-specific transform logic
- do not infer decomposition from phrasing alone
- do not add invented fallback paths unless explicitly required
- prefer explicit upstream structure over downstream semantic guessing
- keep checked-in demos, review fixtures, and delivery outputs synchronized with the
  current contract
- when changing source-family handling, preserve provenance, stable ids, and assembly
  semantics

## Pull Request Expectations

- keep work tied to a GitHub issue
- keep one issue per branch
- include verification notes in the PR description
- update `tasks.md` when work changes repository state or tracked process
- update docs when workflow shape, contract surface, or public-facing project posture
  changes

## Good First Areas

- documentation and workflow polish
- tests around tracked V2 bundles and delivery outputs
- contract hardening between Rupify and Speckify
- quality and review automation for planning and delivery artifacts
