## Summary

System requests payment confirmation.

## Source Lineage

- `anchor.rupify.scenarios.scenario-missing-payment-confirmation` (requirement: `scenario-missing-payment-confirmation`)

## Scope

- System requests payment confirmation.

## Acceptance Criteria

- System requests payment confirmation.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for missing payment confirmation segment 2.
- Observable: System requests payment confirmation.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System requests payment confirmation.
- Failure condition: The scenario handling is missing or incorrect: System requests payment confirmation.

## Dependencies

- `iu.rupify.scenario-missing-payment-confirmation.segment-1`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-missing-payment-confirmation.
