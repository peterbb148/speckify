## Delivery Metadata

- Implementation unit id: `iu.rupify.guard-condition-2`
- Issue slug: `iu-rupify-guard-condition-2`
- Labels: `speckify`, `planning`, `source:rupify`, `guard-conditions`
- Source anchors: `anchor.rupify.guard-conditions.guard-condition-2`
- Verification units: `vu.rupify.guard-condition-2`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of guard-condition-2.

## Summary

Deliver the source-defined behavior for catalog validation approval is required before a reward becomes published: Catalog validation approval is required before a reward becomes Published.

## Source Lineage

- `anchor.rupify.guard-conditions.guard-condition-2` (requirement: `guard-condition-2`)

## Scope

- Catalog validation approval is required before a reward becomes Published

## Acceptance Criteria

- Catalog validation approval is required before a reward becomes Published

## Verification Shape

- Intent: Confirm the guard enforcement is applied for guard condition 2.
- Observable: Catalog validation approval is required before a reward becomes Published
- Setup requirement: A request reaches the boundary where the guard condition must be checked.
- Expected outcome: The guard enforcement is applied correctly: Catalog validation approval is required before a reward becomes Published
- Failure condition: The guard condition is not enforced as required: Catalog validation approval is required before a reward becomes Published

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element guard-condition-2.
