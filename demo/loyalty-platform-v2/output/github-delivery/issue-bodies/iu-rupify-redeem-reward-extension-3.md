## Delivery Metadata

- Implementation unit id: `iu.rupify.redeem-reward-extension-3`
- Issue slug: `iu-rupify-redeem-reward-extension-3`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.redeem-reward-extension-3`
- Verification units: `vu.rupify.redeem-reward-extension-3`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of redeem-reward-extension-3.

## Summary

Deliver the ordered step behavior for redeem reward: Payment confirmation is missing for a reward that depends on purchase completion.

## Source Lineage

- `anchor.rupify.use-case-steps.redeem-reward-extension-3` (requirement: `redeem-reward-extension-3`)

## Scope

- Payment confirmation is missing for a reward that depends on purchase completion.

## Acceptance Criteria

- Payment confirmation is missing for a reward that depends on purchase completion.

## Verification Shape

- Intent: Confirm the use-case step is delivered for redeem reward.
- Observable: Payment confirmation is missing for a reward that depends on purchase completion.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: Payment confirmation is missing for a reward that depends on purchase completion.
- Failure condition: The step behavior does not occur as required: Payment confirmation is missing for a reward that depends on purchase completion.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element redeem-reward-extension-3.
