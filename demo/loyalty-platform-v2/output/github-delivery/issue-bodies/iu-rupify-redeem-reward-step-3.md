## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-step-3`
- Issue slug: `iu-rupify-redeem-reward-step-3`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-step-3`
- Verification units: `vu.rupify.redeem-reward-step-3`
- Depends on:
  - `iu.rupify.redeem-reward-step-2` (Implement Redeem Reward)
- Reverse impact hint: Changes here may require upstream review of redeem-reward-step-3.

## Summary

Implement the behavior described by redeem reward.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-3` (requirement: `redeem-reward-step-3`)

## Scope

- System reserves the reward and updates the member balance.

## Acceptance Criteria

- System reserves the reward and updates the member balance.

## Verification Shape

- Intent: Confirm the implementation satisfies redeem reward.
- Observable: System reserves the reward and updates the member balance.
- Expected outcome: System reserves the reward and updates the member balance.

## Dependencies

- `iu.rupify.redeem-reward-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-3.
