## Delivery Metadata

- Implementation unit id: `iu.rupify.guard-condition-2.block-publish-without-approval`
- Issue slug: `iu-rupify-guard-condition-2-block-publish-without-approval`
- Labels: `speckify`, `planning`, `source:rupify`, `guard-conditions`
- Source anchors: `anchor.rupify.guard-conditions.guard-condition-2`
- Verification units: `vu.rupify.guard-condition-2.block-publish-without-approval`
- Depends on:
  - `iu.rupify.guard-condition-2.require-validation-approval` (Implement guard enforcement: Require catalog validation approval)
- Reverse impact hint: Changes here may require upstream review of guard-condition-2.

## Summary

Block a reward from becoming published when catalog validation approval is missing.

## Source Lineage

- `anchor.rupify.guard-conditions.guard-condition-2` (requirement: `guard-condition-2`)

## Scope

- Block a reward from becoming published when catalog validation approval is missing.

## Acceptance Criteria

- A reward does not become Published without catalog validation approval.

## Verification Shape

- Intent: Confirm the guard enforcement is applied for block publish without approval.
- Observable: A reward does not become Published without catalog validation approval.
- Setup requirement: A request reaches the boundary where the guard condition must be checked.
- Expected outcome: The guard enforcement is applied correctly: A reward does not become Published without catalog validation approval.
- Failure condition: The guard condition is not enforced as required: A reward does not become Published without catalog validation approval.

## Dependencies

- `iu.rupify.guard-condition-2.require-validation-approval`: Guard enforcement depends on recognizing the guard prerequisite first.

## Drift Checks

- Preserve lineage to Rupify element guard-condition-2.
