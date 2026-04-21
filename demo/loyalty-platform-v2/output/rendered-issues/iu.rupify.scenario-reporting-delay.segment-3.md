## Summary

Deliver the source-defined behavior for reporting delay segment 3: System shows a partial-data warning.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- System shows a partial-data warning.

## Acceptance Criteria

- System shows a partial-data warning.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reporting delay segment 3.
- Observable: System shows a partial-data warning.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System shows a partial-data warning.
- Failure condition: The scenario handling is missing or incorrect: System shows a partial-data warning.

## Dependencies

- `iu.rupify.scenario-reporting-delay.segment-2`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
