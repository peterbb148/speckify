## Summary

Detect that no reward inventory remains for the redemption.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reward-inventory-exhausted` (requirement: `scenario-reward-inventory-exhausted`)

## Scope

- Detect that no reward inventory remains for the redemption.

## Acceptance Criteria

- The system detects when no reward inventory remains for the requested redemption.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for detect exhausted reward inventory.
- Observable: The system detects when no reward inventory remains for the requested redemption.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: The system detects when no reward inventory remains for the requested redemption.
- Failure condition: The scenario handling is missing or incorrect: The system detects when no reward inventory remains for the requested redemption.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-reward-inventory-exhausted.
