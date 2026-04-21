## Summary

Deliver the source-defined behavior for invalid catalog change segment 3: System rejects the invalid change.

## Source Lineage

- `anchor.rupify.scenarios.scenario-invalid-catalog-change` (requirement: `scenario-invalid-catalog-change`)

## Scope

- System rejects the invalid change.

## Acceptance Criteria

- System rejects the invalid change.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for invalid catalog change segment 3.
- Observable: System rejects the invalid change.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System rejects the invalid change.
- Failure condition: The scenario handling is missing or incorrect: System rejects the invalid change.

## Dependencies

- `iu.rupify.scenario-invalid-catalog-change.segment-2`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-invalid-catalog-change.
