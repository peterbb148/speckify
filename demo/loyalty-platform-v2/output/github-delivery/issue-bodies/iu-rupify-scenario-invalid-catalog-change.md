## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-invalid-catalog-change`
- Issue slug: `iu-rupify-scenario-invalid-catalog-change`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-invalid-catalog-change`
- Verification units: `vu.rupify.scenario-invalid-catalog-change`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of scenario-invalid-catalog-change.

## Summary

Publication is rejected because the new reward configuration would break an active offer.

## Source Lineage

- `anchor.rupify.scenarios.scenario-invalid-catalog-change` (requirement: `scenario-invalid-catalog-change`)

## Scope

- Publication is rejected because the new reward configuration would break an active offer.

## Acceptance Criteria

- Publication is rejected because the new reward configuration would break an active offer.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for invalid catalog change.
- Observable: Publication is rejected because the new reward configuration would break an active offer.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Publication is rejected because the new reward configuration would break an active offer.
- Failure condition: The scenario handling is missing or incorrect: Publication is rejected because the new reward configuration would break an active offer.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-invalid-catalog-change.
