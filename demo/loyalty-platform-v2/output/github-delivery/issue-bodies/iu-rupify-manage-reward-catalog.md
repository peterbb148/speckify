## Delivery Metadata

- Implementation unit id: `iu.rupify.manage-reward-catalog`
- Issue slug: `iu-rupify-manage-reward-catalog`
- Labels: `speckify`, `planning`, `source:rupify`, `use-cases`
- Source anchors: `anchor.rupify.use-cases.manage-reward-catalog`
- Verification units: `vu.rupify.manage-reward-catalog`
- Depends on:
  - `iu.rupify.manage-reward-catalog-extension-1` (Implement Manage Reward Catalog)
  - `iu.rupify.manage-reward-catalog-step-1` (Implement Manage Reward Catalog)
  - `iu.rupify.manage-reward-catalog-step-2` (Implement Manage Reward Catalog)
  - `iu.rupify.manage-reward-catalog-step-3.publish-change` (Implement Publish catalog change)
  - `iu.rupify.manage-reward-catalog-step-3.validate-change` (Implement Validate catalog change)
- Reverse impact hint: Changes here may require upstream review of manage-reward-catalog.

## Summary

Coordinate the Manage Reward Catalog flow across its steps and extension handling.

## Source Lineage

- `anchor.rupify.use-cases.manage-reward-catalog` (requirement: `manage-reward-catalog`)

## Scope

- Coordinate the Manage Reward Catalog flow across its steps and extension handling.

## Acceptance Criteria

- The Manage Reward Catalog flow is supported end to end.

## Verification Shape

- Intent: Confirm the use-case flow is supported end to end for manage reward catalog.
- Observable: The Manage Reward Catalog flow is supported end to end.
- Setup requirement: The actor can start the use-case flow through its normal entry point.
- Expected outcome: The use-case flow completes as intended: The Manage Reward Catalog flow is supported end to end.
- Failure condition: The use-case flow is incomplete or broken: The Manage Reward Catalog flow is supported end to end.

## Dependencies

- `iu.rupify.manage-reward-catalog-extension-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.manage-reward-catalog-step-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.manage-reward-catalog-step-2`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.manage-reward-catalog-step-3.publish-change`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.manage-reward-catalog-step-3.validate-change`: Use-case orchestration depends on the linked step and extension units.

## Drift Checks

- Preserve lineage to Rupify element manage-reward-catalog.
