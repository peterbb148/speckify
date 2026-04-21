## Delivery Metadata

- Implementation unit id: `iu.rupify.browse-rewards-extension-1`
- Issue slug: `iu-rupify-browse-rewards-extension-1`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.browse-rewards-extension-1`
- Verification units: `vu.rupify.browse-rewards-extension-1`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of browse-rewards-extension-1.

## Summary

Deliver the ordered step behavior for browse rewards: Catalog view degrades if an integration is temporarily unavailable.

## Source Lineage

- `anchor.rupify.use-case-steps.browse-rewards-extension-1` (requirement: `browse-rewards-extension-1`)

## Scope

- Catalog view degrades if an integration is temporarily unavailable.

## Acceptance Criteria

- Catalog view degrades if an integration is temporarily unavailable.

## Verification Shape

- Intent: Confirm the use-case step is delivered for browse rewards.
- Observable: Catalog view degrades if an integration is temporarily unavailable.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: Catalog view degrades if an integration is temporarily unavailable.
- Failure condition: The step behavior does not occur as required: Catalog view degrades if an integration is temporarily unavailable.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element browse-rewards-extension-1.
