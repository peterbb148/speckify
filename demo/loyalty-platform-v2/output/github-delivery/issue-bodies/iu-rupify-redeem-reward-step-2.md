## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-step-2`
- Issue slug: `iu-rupify-redeem-reward-step-2`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-step-2`
- Verification units: `vu.rupify.redeem-reward-step-2`
- Depends on:
  - `iu.rupify.redeem-reward-step-1` (Implement use-case step: Redeem Reward)
- Reverse impact hint: Changes here may require upstream review of redeem-reward-step-2.

## Summary

Deliver the ordered step behavior for redeem reward: System validates reward eligibility and available points.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-step-2` (requirement: `redeem-reward-step-2`)

## Scope

- System validates reward eligibility and available points.

## Acceptance Criteria

- System validates reward eligibility and available points.

## Verification Shape

- Intent: Confirm the use-case step is delivered for redeem reward.
- Observable: System validates reward eligibility and available points.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: System validates reward eligibility and available points.
- Failure condition: The step behavior does not occur as required: System validates reward eligibility and available points.

## Dependencies

- `iu.rupify.redeem-reward-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-step-2.
