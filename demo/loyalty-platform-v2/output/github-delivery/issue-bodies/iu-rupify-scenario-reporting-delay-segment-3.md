## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-reporting-delay.segment-3`
- Issue slug: `iu-rupify-scenario-reporting-delay-segment-3`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-reporting-delay`
- Verification units: `vu.rupify.scenario-reporting-delay.segment-3`
- Depends on:
  - `iu.rupify.scenario-reporting-delay.segment-2` (Implement scenario handling: Reporting Delay segment 2)
- Reverse impact hint: Changes here may require upstream review of scenario-reporting-delay.

## Summary

Deliver the source-defined behavior for reporting delay segment 3: System shows a partial-data warning.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- System shows a partial-data warning.

## Acceptance Criteria

- System shows a partial-data warning.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reporting delay segment 3.
- Observable: System shows a partial-data warning.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: System shows a partial-data warning.
- Failure condition: The scenario handling is missing or incorrect: System shows a partial-data warning.

## Dependencies

- `iu.rupify.scenario-reporting-delay.segment-2`: Later scenario flow segments depend on earlier explicit flow segments.

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
