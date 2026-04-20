## Summary

Fail redemption when no reward inventory remains.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reward-inventory-exhausted` (requirement: `scenario-reward-inventory-exhausted`)

## Scope

- Fail redemption when no reward inventory remains.

## Acceptance Criteria

- Redemption fails when no reward inventory remains.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for fail redemption without inventory.
- Observable: Redemption fails when no reward inventory remains.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Redemption fails when no reward inventory remains.
- Failure condition: The scenario handling is missing or incorrect: Redemption fails when no reward inventory remains.

## Dependencies

- `iu.rupify.scenario-reward-inventory-exhausted.detect-exhausted-inventory`: Scenario resolution depends on first identifying the triggering condition.

## Drift Checks

- Preserve lineage to Rupify element scenario-reward-inventory-exhausted.
