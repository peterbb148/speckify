## Summary

System reports that inventory is exhausted.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reward-inventory-exhausted` (requirement: `scenario-reward-inventory-exhausted`)

## Scope

- System reports that inventory is exhausted.

## Acceptance Criteria

- System reports that inventory is exhausted.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reward inventory exhausted segment 3.
- Observable: System reports that inventory is exhausted.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System reports that inventory is exhausted.
- Failure condition: The scenario handling is missing or incorrect: System reports that inventory is exhausted.

## Dependencies

- `iu.rupify.scenario-reward-inventory-exhausted.segment-2`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-reward-inventory-exhausted.
