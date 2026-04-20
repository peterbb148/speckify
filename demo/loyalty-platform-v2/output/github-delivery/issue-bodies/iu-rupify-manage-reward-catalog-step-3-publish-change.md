## Delivery Metadata

- Implementation unit id: `iu.rupify.manage-reward-catalog-step-3.publish-change`
- Issue slug: `iu-rupify-manage-reward-catalog-step-3-publish-change`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.manage-reward-catalog-step-3`
- Verification units: `vu.rupify.manage-reward-catalog-step-3.publish-change`
- Depends on:
  - `iu.rupify.manage-reward-catalog-step-2` (Implement Manage Reward Catalog)
- Reverse impact hint: Changes here may require upstream review of manage-reward-catalog-step-3.

## Summary

Implement the behavior described by publish catalog change.

## Source Lineage

- `anchor.rupify.use-case-steps.manage-reward-catalog-step-3` (requirement: `manage-reward-catalog-step-3`)

## Scope

- Publish the catalog configuration change after validation.

## Acceptance Criteria

- The system publishes the catalog configuration change.

## Verification Shape

- Intent: Confirm the implementation satisfies publish catalog change.
- Observable: The system publishes the catalog configuration change.
- Expected outcome: The system publishes the catalog configuration change.

## Dependencies

- `iu.rupify.manage-reward-catalog-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element manage-reward-catalog-step-3.
