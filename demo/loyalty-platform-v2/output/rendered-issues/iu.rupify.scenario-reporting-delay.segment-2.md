## Summary

System detects delayed reporting data.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- System detects delayed reporting data.

## Acceptance Criteria

- System detects delayed reporting data.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reporting delay segment 2.
- Observable: System detects delayed reporting data.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System detects delayed reporting data.
- Failure condition: The scenario handling is missing or incorrect: System detects delayed reporting data.

## Dependencies

- `iu.rupify.scenario-reporting-delay.segment-1`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
