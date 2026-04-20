## Summary

Detect that dependent payment confirmation has not yet arrived.

## Source Lineage

- `anchor.rupify.scenarios.scenario-missing-payment-confirmation` (requirement: `scenario-missing-payment-confirmation`)

## Scope

- Detect that dependent payment confirmation has not yet arrived.

## Acceptance Criteria

- The system recognizes when dependent payment confirmation is still missing.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for await payment confirmation.
- Observable: The system recognizes when dependent payment confirmation is still missing.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: The system recognizes when dependent payment confirmation is still missing.
- Failure condition: The scenario handling is missing or incorrect: The system recognizes when dependent payment confirmation is still missing.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-missing-payment-confirmation.
