## Summary

Deliver the ordered step behavior for redeem reward: System reserves the reward and updates the member balance.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-3` (requirement: `redeem-reward-step-3`)

## Scope

- System reserves the reward and updates the member balance.

## Acceptance Criteria

- System reserves the reward and updates the member balance.

## Verification Shape

- Intent: Confirm the use-case step is delivered for redeem reward.
- Observable: System reserves the reward and updates the member balance.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: System reserves the reward and updates the member balance.
- Failure condition: The step behavior does not occur as required: System reserves the reward and updates the member balance.

## Dependencies

- `iu.rupify.redeem-reward-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-3.
