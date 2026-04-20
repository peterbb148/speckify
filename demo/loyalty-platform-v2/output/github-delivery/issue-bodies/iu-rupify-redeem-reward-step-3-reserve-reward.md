## Summary

Implement the behavior described by reserve reward.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-3` (requirement: `redeem-reward-step-3`)

## Scope

- Reserve the selected reward for the member.

## Acceptance Criteria

- The system reserves the selected reward.

## Verification Shape

- Intent: Confirm the implementation satisfies reserve reward.
- Observable: The system reserves the selected reward.
- Expected outcome: The system reserves the selected reward.

## Dependencies

- `iu.rupify.redeem-reward-step-2.validate-available-points`: Later use-case steps depend on the earlier step in the same ordered flow.
- `iu.rupify.redeem-reward-step-2.validate-eligibility`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-3.
