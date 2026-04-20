## Delivery Metadata

- Implementation unit id: `iu.rupify.guard-condition-2.require-validation-approval`
- Issue slug: `iu-rupify-guard-condition-2-require-validation-approval`
- Labels: `speckify`, `planning`, `source:rupify`, `guard-conditions`
- Source anchors: `anchor.rupify.guard-conditions.guard-condition-2`
- Verification units: `vu.rupify.guard-condition-2.require-validation-approval`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of guard-condition-2.

## Summary

Require catalog validation approval before a reward can be published.

## Source Lineage

- `anchor.rupify.guard-conditions.guard-condition-2` (requirement: `guard-condition-2`)

## Scope

- Require catalog validation approval before a reward can be published.

## Acceptance Criteria

- Catalog validation approval is required before a reward becomes Published.

## Verification Shape

- Intent: Confirm the guard enforcement is applied for require catalog validation approval.
- Observable: Catalog validation approval is required before a reward becomes Published.
- Setup requirement: A request reaches the boundary where the guard condition must be checked.
- Expected outcome: The guard enforcement is applied correctly: Catalog validation approval is required before a reward becomes Published.
- Failure condition: The guard condition is not enforced as required: Catalog validation approval is required before a reward becomes Published.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element guard-condition-2.
