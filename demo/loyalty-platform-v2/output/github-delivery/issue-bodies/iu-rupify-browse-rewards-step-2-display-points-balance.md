## Delivery Metadata

- Implementation unit id: `iu.rupify.browse-rewards-step-2.display-points-balance`
- Issue slug: `iu-rupify-browse-rewards-step-2-display-points-balance`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.browse-rewards-step-2`
- Verification units: `vu.rupify.browse-rewards-step-2.display-points-balance`
- Depends on:
  - `iu.rupify.browse-rewards-step-1` (Implement Browse Rewards)
- Reverse impact hint: Changes here may require upstream review of browse-rewards-step-2.

## Summary

Implement the behavior described by display points balance.

## Source Lineage

- `anchor.rupify.use-case-steps.browse-rewards-step-2` (requirement: `browse-rewards-step-2`)

## Scope

- Display the member's current points balance.

## Acceptance Criteria

- The system displays the member's points balance.

## Verification Shape

- Intent: Confirm the implementation satisfies display points balance.
- Observable: The system displays the member's points balance.
- Expected outcome: The system displays the member's points balance.

## Dependencies

- `iu.rupify.browse-rewards-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element browse-rewards-step-2.
