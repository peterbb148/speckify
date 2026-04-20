## Summary

Pause redemption until the dependent payment confirmation arrives.

## Source Lineage

- `anchor.rupify.scenarios.scenario-missing-payment-confirmation` (requirement: `scenario-missing-payment-confirmation`)

## Scope

- Pause redemption until the dependent payment confirmation arrives.

## Acceptance Criteria

- Redemption remains paused until dependent payment confirmation arrives.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for pause redemption.
- Observable: Redemption remains paused until dependent payment confirmation arrives.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Redemption remains paused until dependent payment confirmation arrives.
- Failure condition: The scenario handling is missing or incorrect: Redemption remains paused until dependent payment confirmation arrives.

## Dependencies

- `iu.rupify.scenario-missing-payment-confirmation.await-payment-confirmation`: Scenario resolution depends on first identifying the triggering condition.

## Drift Checks

- Preserve lineage to Rupify element scenario-missing-payment-confirmation.
