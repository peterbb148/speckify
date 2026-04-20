## Delivery Metadata

- Implementation unit id: `iu.rupify.state-invariant-3.record-contract-dates`
- Issue slug: `iu-rupify-state-invariant-3-record-contract-dates`
- Labels: `speckify`, `planning`, `source:rupify`, `state-invariants`
- Source anchors: `anchor.rupify.state-invariants.state-invariant-3`
- Verification units: `vu.rupify.state-invariant-3.record-contract-dates`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of state-invariant-3.

## Summary

Ensure the invariant 'The system records contract dates.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.state-invariants.state-invariant-3` (state_invariant: `state-invariant-3`)

## Scope

- Record contract dates for the system.

## Acceptance Criteria

- The system records contract dates.

## Verification Shape

- Intent: Confirm the invariant remains enforced for record contract dates.
- Observable: The system records contract dates.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: The system records contract dates.
- Failure condition: The invariant is breached: The system records contract dates.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-invariant-3.
