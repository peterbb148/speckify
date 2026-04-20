# Review Fixtures

This directory contains a compact, review-oriented subset of generated planning artifacts.

Purpose:

- make it easier to review planning quality without reading the full demo output tree
- capture representative examples of current decomposition, dependency derivation,
  verification shaping, and rendered artifact quality
- provide a stable comparison surface for future quality changes

Current source:

- `demo/it-systems-inventory-v2/output/`

Current review set:

- `planning-bundle-summary.json`: compact summary of the generated planning bundle
- `rendered-issues/constraint-web-ui.md`: representative constraint issue
- `rendered-issues/workflow-approval-states.md`: representative split workflow issue with
  dependency information
- `rendered-issues/state-transition-active-to-retiring.md`: representative lifecycle
  transition issue with sequencing and verification details
- `quality-review-notes.md`: current review checklist and expected qualities
- `quality-review.json`: machine-readable warning report for current planning-quality gaps
- `quality-review.md`: Markdown projection of the current warning report
- `loyalty-platform-v2-summary.json`: compact review summary for the second real-world demo,
  showing the richer non-CMDB V2 bundle case
