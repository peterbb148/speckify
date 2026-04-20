## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-invalid-catalog-change.reject-publication`
- Issue slug: `iu-rupify-scenario-invalid-catalog-change-reject-publication`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-invalid-catalog-change`
- Verification units: `vu.rupify.scenario-invalid-catalog-change.reject-publication`
- Depends on:
  - `iu.rupify.scenario-invalid-catalog-change.detect-active-offer-conflict` (Implement scenario handling: Detect active offer conflict)
- Reverse impact hint: Changes here may require upstream review of scenario-invalid-catalog-change.

## Summary

Reject publication when the reward configuration would break an active offer.

## Source Lineage

- `anchor.rupify.scenarios.scenario-invalid-catalog-change` (requirement: `scenario-invalid-catalog-change`)

## Scope

- Reject publication when the reward configuration would break an active offer.

## Acceptance Criteria

- Publication is rejected when the new reward configuration would break an active offer.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reject invalid publication.
- Observable: Publication is rejected when the new reward configuration would break an active offer.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Publication is rejected when the new reward configuration would break an active offer.
- Failure condition: The scenario handling is missing or incorrect: Publication is rejected when the new reward configuration would break an active offer.

## Dependencies

- `iu.rupify.scenario-invalid-catalog-change.detect-active-offer-conflict`: Scenario resolution depends on first identifying the triggering condition.

## Drift Checks

- Preserve lineage to Rupify element scenario-invalid-catalog-change.
