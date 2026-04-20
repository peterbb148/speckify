## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-invalid-catalog-change.detect-active-offer-conflict`
- Issue slug: `iu-rupify-scenario-invalid-catalog-change-detect-active-offer-conflict`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-invalid-catalog-change`
- Verification units: `vu.rupify.scenario-invalid-catalog-change.detect-active-offer-conflict`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of scenario-invalid-catalog-change.

## Summary

Detect that the new reward configuration would break an active offer.

## Source Lineage

- `anchor.rupify.scenarios.scenario-invalid-catalog-change` (requirement: `scenario-invalid-catalog-change`)

## Scope

- Detect that the new reward configuration would break an active offer.

## Acceptance Criteria

- The system detects when a new reward configuration would break an active offer.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for detect active offer conflict.
- Observable: The system detects when a new reward configuration would break an active offer.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: The system detects when a new reward configuration would break an active offer.
- Failure condition: The scenario handling is missing or incorrect: The system detects when a new reward configuration would break an active offer.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-invalid-catalog-change.
