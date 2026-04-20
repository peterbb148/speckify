## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-step-2.validate-available-points`
- Issue slug: `iu-rupify-redeem-reward-step-2-validate-available-points`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-step-2`
- Verification units: `vu.rupify.redeem-reward-step-2.validate-available-points`
- Depends on:
  - `iu.rupify.redeem-reward-step-1` (Implement Redeem Reward)
- Reverse impact hint: Changes here may require upstream review of redeem-reward-step-2.

## Summary

Implement the behavior described by validate available points.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-2` (requirement: `redeem-reward-step-2`)

## Scope

- Validate that the member has enough points for the redemption.

## Acceptance Criteria

- The system validates available points for the redemption.

## Verification Shape

- Intent: Confirm the implementation satisfies validate available points.
- Observable: The system validates available points for the redemption.
- Expected outcome: The system validates available points for the redemption.

## Dependencies

- `iu.rupify.redeem-reward-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-2.
