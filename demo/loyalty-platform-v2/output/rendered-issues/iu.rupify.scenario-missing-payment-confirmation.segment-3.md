## Summary

Deliver the source-defined behavior for missing payment confirmation segment 3: System blocks fulfillment until confirmation arrives.

## Source Lineage

- `anchor.rupify.scenarios.scenario-missing-payment-confirmation` (requirement: `scenario-missing-payment-confirmation`)

## Scope

- System blocks fulfillment until confirmation arrives.

## Acceptance Criteria

- System blocks fulfillment until confirmation arrives.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for missing payment confirmation segment 3.
- Observable: System blocks fulfillment until confirmation arrives.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System blocks fulfillment until confirmation arrives.
- Failure condition: The scenario handling is missing or incorrect: System blocks fulfillment until confirmation arrives.

## Dependencies

- `iu.rupify.scenario-missing-payment-confirmation.segment-2`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-missing-payment-confirmation.
