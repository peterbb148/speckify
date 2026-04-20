## Summary

Implement the behavior described by update member balance.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-3` (requirement: `redeem-reward-step-3`)

## Scope

- Update the member balance after the reward reservation.

## Acceptance Criteria

- The system updates the member balance after reservation.

## Verification Shape

- Intent: Confirm the implementation satisfies update member balance.
- Observable: The system updates the member balance after reservation.
- Expected outcome: The system updates the member balance after reservation.

## Dependencies

- `iu.rupify.redeem-reward-step-2.validate-available-points`: Later use-case steps depend on the earlier step in the same ordered flow.
- `iu.rupify.redeem-reward-step-2.validate-eligibility`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-3.
