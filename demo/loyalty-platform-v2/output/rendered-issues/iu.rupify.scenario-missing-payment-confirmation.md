## Summary

Redemption pauses until dependent payment confirmation arrives.

## Source Lineage

- `anchor.rupify.scenarios.scenario-missing-payment-confirmation` (requirement: `scenario-missing-payment-confirmation`)

## Scope

- Redemption pauses until dependent payment confirmation arrives.

## Acceptance Criteria

- Redemption pauses until dependent payment confirmation arrives.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for missing payment confirmation.
- Observable: Redemption pauses until dependent payment confirmation arrives.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Redemption pauses until dependent payment confirmation arrives.
- Failure condition: The scenario handling is missing or incorrect: Redemption pauses until dependent payment confirmation arrives.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-missing-payment-confirmation.
