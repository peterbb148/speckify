# Quality Review Notes

These notes describe what the current generated planning output should demonstrate when the
pipeline is working well enough for human review.

## Bundle-Level Qualities

- decomposition is no longer one-source-to-one-unit everywhere
- split units preserve lineage back to the original Rupify source anchor
- dependency edges and assembly rules exist where split units imply sequencing or
  recomposition
- verification units contain setup and failure information, not just paraphrased source text

## Representative Review Checks

### Constraint Example

Fixture:

- `rendered-issues/constraint-web-ui.md`

What to check:

- title and summary are implementation-oriented rather than generic
- lineage includes both the stable anchor id and readable source context
- verification includes a concrete setup requirement and explicit failure condition

### Workflow Example

Fixture:

- `rendered-issues/workflow-approval-states.md`

What to check:

- the workflow concern is split out as its own implementation unit
- dependency information is visible in rendered output
- the dependency reason is understandable to a human reviewer

### Transition Example

Fixture:

- `rendered-issues/state-transition-active-to-retiring.md`

What to check:

- the transition chain has been decomposed into a specific transition pair
- the rendered issue shows lifecycle sequencing
- verification names the starting state, resulting state, and concrete failure modes

## What Should Trigger Review Concern

- implementation summaries that read like placeholders
- verification sections that simply repeat the acceptance sentence
- missing dependencies for obviously sequenced slices
- flat specifications that are hard to scan or group by concern

## Current Warning Surface

The generated warning artifacts (`quality-review.json` and `quality-review.md`) should
currently call out:

- generic titles that still expose raw requirement identifiers
- very short acceptance criteria such as `SSO`, `search`, or `filtering`
- success-criterion outputs that remain too abstract for direct implementation work
- verification units where observables and expected outcomes collapse into the same text
