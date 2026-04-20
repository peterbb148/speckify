## Delivery Metadata

- Implementation unit id: `iu.rupify.state-invariant-3`
- Issue slug: `iu-rupify-state-invariant-3`
- Labels: `speckify`, `planning`, `source:rupify`, `state-invariants`
- Source anchors: `anchor.rupify.state-invariants.state-invariant-3`
- Verification units: `vu.rupify.state-invariant-3`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of state-invariant-3.

## Summary

Ensure the invariant 'A System must record vendor and contract dates.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.state-invariants.state-invariant-3` (state_invariant: `state-invariant-3`)

## Scope

- A System must record vendor and contract dates.

## Acceptance Criteria

- A System must record vendor and contract dates.

## Verification Shape

- Intent: Confirm the invariant remains enforced for rule 3.
- Observable: A System must record vendor and contract dates.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: A System must record vendor and contract dates.
- Failure condition: The invariant is breached: A System must record vendor and contract dates.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-invariant-3.
