## Delivery Metadata

- Implementation unit id: `iu.rupify.manage-reward-catalog-step-3.validate-change`
- Issue slug: `iu-rupify-manage-reward-catalog-step-3-validate-change`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.manage-reward-catalog-step-3`
- Verification units: `vu.rupify.manage-reward-catalog-step-3.validate-change`
- Depends on:
  - `iu.rupify.manage-reward-catalog-step-2` (Implement Manage Reward Catalog)
- Reverse impact hint: Changes here may require upstream review of manage-reward-catalog-step-3.

## Summary

Implement the behavior described by validate catalog change.

## Source Lineage

- `anchor.rupify.use-case-steps.manage-reward-catalog-step-3` (requirement: `manage-reward-catalog-step-3`)

## Scope

- Validate the proposed catalog configuration change.

## Acceptance Criteria

- The system validates the catalog configuration change.

## Verification Shape

- Intent: Confirm the implementation satisfies validate catalog change.
- Observable: The system validates the catalog configuration change.
- Expected outcome: The system validates the catalog configuration change.

## Dependencies

- `iu.rupify.manage-reward-catalog-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element manage-reward-catalog-step-3.
