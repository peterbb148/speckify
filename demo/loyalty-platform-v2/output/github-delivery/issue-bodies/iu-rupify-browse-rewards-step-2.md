## Delivery Metadata

- Implementation unit id: `iu.rupify.browse-rewards-step-2`
- Issue slug: `iu-rupify-browse-rewards-step-2`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.browse-rewards-step-2`
- Verification units: `vu.rupify.browse-rewards-step-2`
- Depends on:
  - `iu.rupify.browse-rewards-step-1` (Implement use-case step: Browse Rewards)
- Reverse impact hint: Changes here may require upstream review of browse-rewards-step-2.

## Summary

Deliver the ordered step behavior for browse rewards: System displays available rewards and points balance.

## Source Lineage

- `anchor.rupify.use-case-steps.browse-rewards-step-2` (requirement: `browse-rewards-step-2`)

## Scope

- System displays available rewards and points balance.

## Acceptance Criteria

- System displays available rewards and points balance.

## Verification Shape

- Intent: Confirm the use-case step is delivered for browse rewards.
- Observable: System displays available rewards and points balance.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: System displays available rewards and points balance.
- Failure condition: The step behavior does not occur as required: System displays available rewards and points balance.

## Dependencies

- `iu.rupify.browse-rewards-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element browse-rewards-step-2.
