## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-invalid-catalog-change.segment-2`
- Issue slug: `iu-rupify-scenario-invalid-catalog-change-segment-2`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-invalid-catalog-change`
- Verification units: `vu.rupify.scenario-invalid-catalog-change.segment-2`
- Depends on:
  - `iu.rupify.scenario-invalid-catalog-change.segment-1` (Implement scenario handling: Invalid Catalog Change segment 1)
- Reverse impact hint: Changes here may require upstream review of scenario-invalid-catalog-change.

## Summary

System validates the change.

## Source Lineage

- `anchor.rupify.scenarios.scenario-invalid-catalog-change` (requirement: `scenario-invalid-catalog-change`)

## Scope

- System validates the change.

## Acceptance Criteria

- System validates the change.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for invalid catalog change segment 2.
- Observable: System validates the change.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System validates the change.
- Failure condition: The scenario handling is missing or incorrect: System validates the change.

## Dependencies

- `iu.rupify.scenario-invalid-catalog-change.segment-1`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-invalid-catalog-change.
