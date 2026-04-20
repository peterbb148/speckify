## Summary

Detect that a reporting source is delayed for the analytics view.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- Detect that a reporting source is delayed for the analytics view.

## Acceptance Criteria

- The system detects when a reporting source is delayed.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for detect reporting source delay.
- Observable: The system detects when a reporting source is delayed.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: The system detects when a reporting source is delayed.
- Failure condition: The scenario handling is missing or incorrect: The system detects when a reporting source is delayed.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
