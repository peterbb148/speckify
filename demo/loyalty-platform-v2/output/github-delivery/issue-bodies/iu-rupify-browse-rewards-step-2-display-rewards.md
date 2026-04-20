## Delivery Metadata

- Implementation unit id: `iu.rupify.browse-rewards-step-2.display-rewards`
- Issue slug: `iu-rupify-browse-rewards-step-2-display-rewards`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.browse-rewards-step-2`
- Verification units: `vu.rupify.browse-rewards-step-2.display-rewards`
- Depends on:
  - `iu.rupify.browse-rewards-step-1` (Implement Browse Rewards)
- Reverse impact hint: Changes here may require upstream review of browse-rewards-step-2.

## Summary

Implement the behavior described by display available rewards.

## Source Lineage

- `anchor.rupify.use-case-steps.browse-rewards-step-2` (requirement: `browse-rewards-step-2`)

## Scope

- Display the rewards that are available to the member.

## Acceptance Criteria

- The system displays available rewards to the member.

## Verification Shape

- Intent: Confirm the implementation satisfies display available rewards.
- Observable: The system displays available rewards to the member.
- Expected outcome: The system displays available rewards to the member.

## Dependencies

- `iu.rupify.browse-rewards-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element browse-rewards-step-2.
