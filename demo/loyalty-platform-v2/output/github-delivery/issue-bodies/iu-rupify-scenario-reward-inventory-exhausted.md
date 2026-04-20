## Delivery Metadata

- Implementation unit id: `iu.rupify.scenario-reward-inventory-exhausted`
- Issue slug: `iu-rupify-scenario-reward-inventory-exhausted`
- Labels: `speckify`, `planning`, `source:rupify`, `scenarios`
- Source anchors: `anchor.rupify.scenarios.scenario-reward-inventory-exhausted`
- Verification units: `vu.rupify.scenario-reward-inventory-exhausted`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of scenario-reward-inventory-exhausted.

## Summary

Redemption fails because no reward inventory remains.

## Source Lineage

- `anchor.rupify.scenarios.scenario-reward-inventory-exhausted` (requirement: `scenario-reward-inventory-exhausted`)

## Scope

- Redemption fails because no reward inventory remains.

## Acceptance Criteria

- Redemption fails because no reward inventory remains.

## Verification Shape

- Intent: Confirm the scenario handling behaves correctly for reward inventory exhausted.
- Observable: Redemption fails because no reward inventory remains.
- Setup requirement: The system is placed in the exceptional or degraded condition described by the scenario.
- Expected outcome: The scenario outcome is handled correctly: Redemption fails because no reward inventory remains.
- Failure condition: The scenario handling is missing or incorrect: Redemption fails because no reward inventory remains.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element scenario-reward-inventory-exhausted.
