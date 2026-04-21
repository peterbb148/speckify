## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-step-1`
- Issue slug: `iu-rupify-redeem-reward-step-1`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-step-1`
- Verification units: `vu.rupify.redeem-reward-step-1`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of redeem-reward-step-1.

## Summary

Deliver the ordered step behavior for redeem reward: Customer selects a reward.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-1` (requirement: `redeem-reward-step-1`)

## Scope

- Customer selects a reward.

## Acceptance Criteria

- Customer selects a reward.

## Verification Shape

- Intent: Confirm the use-case step is delivered for redeem reward.
- Observable: Customer selects a reward.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: Customer selects a reward.
- Failure condition: The step behavior does not occur as required: Customer selects a reward.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-1.
