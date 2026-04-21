## Summary

Deliver the source-defined behavior for reporting delay segment 1: Operations Manager opens the analytics dashboard.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- Operations Manager opens the analytics dashboard.

## Acceptance Criteria

- Operations Manager opens the analytics dashboard.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reporting delay segment 1.
- Observable: Operations Manager opens the analytics dashboard.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Operations Manager opens the analytics dashboard.
- Failure condition: The scenario handling is missing or incorrect: Operations Manager opens the analytics dashboard.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
