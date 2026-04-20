## Summary

Coordinate the Browse Rewards flow across its steps and extension handling.

## Source Lineage

- `anchor.rupify.use-cases.browse-rewards` (requirement: `browse-rewards`)

## Scope

- Coordinate the Browse Rewards flow across its steps and extension handling.

## Acceptance Criteria

- The Browse Rewards flow is supported end to end.

## Verification Shape

- Intent: Confirm the use-case flow is supported end to end for browse rewards.
- Observable: The Browse Rewards flow is supported end to end.
- Setup requirement: The actor can start the use-case flow through its normal entry point.
- Expected outcome: The use-case flow completes as intended: The Browse Rewards flow is supported end to end.
- Failure condition: The use-case flow is incomplete or broken: The Browse Rewards flow is supported end to end.

## Dependencies

- `iu.rupify.browse-rewards-extension-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.browse-rewards-step-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.browse-rewards-step-2.display-points-balance`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.browse-rewards-step-2.display-rewards`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.browse-rewards-step-3`: Use-case orchestration depends on the linked step and extension units.

## Drift Checks

- Preserve lineage to Rupify element browse-rewards.
