## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-reporting-delay.show-partial-analytics`
- Issue slug: `iu-rupify-scenario-reporting-delay-show-partial-analytics`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-reporting-delay`
- Verification units: `vu.rupify.scenario-reporting-delay.show-partial-analytics`
- Depends on:
  - `iu.rupify.scenario-reporting-delay.detect-reporting-delay` (Implement scenario handling: Detect reporting source delay)
- Reverse impact hint: Changes here may require upstream review of scenario-reporting-delay.

## Summary

Show a partial analytics view when a reporting source is delayed.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reporting-delay` (requirement: `scenario-reporting-delay`)

## Scope

- Show a partial analytics view when a reporting source is delayed.

## Acceptance Criteria

- The analytics view remains partial while a reporting source is delayed.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for show partial analytics view.
- Observable: The analytics view remains partial while a reporting source is delayed.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: The analytics view remains partial while a reporting source is delayed.
- Failure condition: The scenario handling is missing or incorrect: The analytics view remains partial while a reporting source is delayed.

## Dependencies

- `iu.rupify.scenario-reporting-delay.detect-reporting-delay`: Scenario resolution depends on first identifying the triggering condition.

## Drift Checks

- Preserve lineage to Rupify element scenario-reporting-delay.
