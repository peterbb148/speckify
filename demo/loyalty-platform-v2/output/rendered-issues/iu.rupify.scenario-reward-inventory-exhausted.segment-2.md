## Summary

System checks reward availability.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reward-inventory-exhausted` (requirement: `scenario-reward-inventory-exhausted`)

## Scope

- System checks reward availability.

## Acceptance Criteria

- System checks reward availability.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reward inventory exhausted segment 2.
- Observable: System checks reward availability.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System checks reward availability.
- Failure condition: The scenario handling is missing or incorrect: System checks reward availability.

## Dependencies

- `iu.rupify.scenario-reward-inventory-exhausted.segment-1`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-reward-inventory-exhausted.
