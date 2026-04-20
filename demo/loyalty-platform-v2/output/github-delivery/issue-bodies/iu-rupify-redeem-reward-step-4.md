## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-step-4`
- Issue slug: `iu-rupify-redeem-reward-step-4`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-step-4`
- Verification units: `vu.rupify.redeem-reward-step-4`
- Depends on:
  - `iu.rupify.redeem-reward-step-3.reserve-reward` (Implement Reserve reward)
  - `iu.rupify.redeem-reward-step-3.update-member-balance` (Implement Update member balance)
- Reverse impact hint: Changes here may require upstream review of redeem-reward-step-4.

## Summary

Implement the behavior described by redeem reward.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-4` (requirement: `redeem-reward-step-4`)

## Scope

- System confirms redemption to the customer.

## Acceptance Criteria

- System confirms redemption to the customer.

## Verification Shape

- Intent: Confirm the implementation satisfies redeem reward.
- Observable: System confirms redemption to the customer.
- Expected outcome: System confirms redemption to the customer.

## Dependencies

- `iu.rupify.redeem-reward-step-3.reserve-reward`: Later use-case steps depend on the earlier step in the same ordered flow.
- `iu.rupify.redeem-reward-step-3.update-member-balance`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-4.
