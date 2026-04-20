## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward`
- Issue slug: `iu-rupify-redeem-reward`
- Labels: `speckify`, `planning`, `source:rupify`, `use-cases`
- Source anchors: `anchor.rupify.use-cases.redeem-reward`
- Verification units: `vu.rupify.redeem-reward`
- Depends on:
  - `iu.rupify.redeem-reward-extension-1` (Implement Redeem Reward)
  - `iu.rupify.redeem-reward-extension-2` (Implement Redeem Reward)
  - `iu.rupify.redeem-reward-extension-3` (Implement Redeem Reward)
  - `iu.rupify.redeem-reward-step-1` (Implement Redeem Reward)
  - `iu.rupify.redeem-reward-step-2.validate-available-points` (Implement Validate available points)
  - `iu.rupify.redeem-reward-step-2.validate-eligibility` (Implement Validate reward eligibility)
  - `iu.rupify.redeem-reward-step-3.reserve-reward` (Implement Reserve reward)
  - `iu.rupify.redeem-reward-step-3.update-member-balance` (Implement Update member balance)
  - `iu.rupify.redeem-reward-step-4` (Implement Redeem Reward)
  - `iu.rupify.non-functional-requirement-6` (Implement constraint: non_functional-requirement-6)
- Reverse impact hint: Changes here may require upstream review of redeem-reward.

## Summary

Coordinate the Redeem Reward flow across its steps and extension handling.

## Source Lineage

- `anchor.rupify.use-cases.redeem-reward` (requirement: `redeem-reward`)

## Scope

- Coordinate the Redeem Reward flow across its steps and extension handling.

## Acceptance Criteria

- The Redeem Reward flow is supported end to end.

## Verification Shape

- Intent: Confirm the use-case flow is supported end to end for redeem reward.
- Observable: The Redeem Reward flow is supported end to end.
- Setup requirement: The actor can start the use-case flow through its normal entry point.
- Expected outcome: The use-case flow completes as intended: The Redeem Reward flow is supported end to end.
- Failure condition: The use-case flow is incomplete or broken: The Redeem Reward flow is supported end to end.

## Dependencies

- `iu.rupify.redeem-reward-extension-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-extension-2`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-extension-3`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-2.validate-available-points`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-2.validate-eligibility`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-3.reserve-reward`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-3.update-member-balance`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.redeem-reward-step-4`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.non-functional-requirement-6`: Use-case implementation should follow the linked requirement intent.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward.
