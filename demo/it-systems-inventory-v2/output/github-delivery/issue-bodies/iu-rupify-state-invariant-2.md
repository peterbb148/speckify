## Delivery Metadata

- Implementation unit id: `iu.rupify.state-invariant-2`
- Issue slug: `iu-rupify-state-invariant-2`
- Labels: `speckify`, `planning`, `source:rupify`, `state-invariants`
- Source anchors: `anchor.rupify.state-invariants.state-invariant-2`
- Verification units: `vu.rupify.state-invariant-2`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of state-invariant-2.

## Summary

Ensure the invariant 'A System lifecycle state change requires approval for deprecation.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.state-invariants.state-invariant-2` (state_invariant: `state-invariant-2`)

## Scope

- A System lifecycle state change requires approval for deprecation.

## Acceptance Criteria

- A System lifecycle state change requires approval for deprecation.

## Verification Shape

- Intent: Confirm the invariant remains enforced for rule 2.
- Observable: A System lifecycle state change requires approval for deprecation.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: A System lifecycle state change requires approval for deprecation.
- Failure condition: The invariant is breached: A System lifecycle state change requires approval for deprecation.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-invariant-2.
