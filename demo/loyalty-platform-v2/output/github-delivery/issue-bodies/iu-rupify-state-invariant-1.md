## Delivery Metadata

- Implementation unit id: `iu.rupify.state-invariant-1`
- Issue slug: `iu-rupify-state-invariant-1`
- Labels: `speckify`, `planning`, `source:rupify`, `state-invariants`
- Source anchors: `anchor.rupify.state-invariants.state-invariant-1`
- Verification units: `vu.rupify.state-invariant-1`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of state-invariant-1.

## Summary

Ensure the invariant 'A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.state-invariants.state-invariant-1` (state_invariant: `state-invariant-1`)

## Scope

- A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.

## Acceptance Criteria

- A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.

## Verification Shape

- Intent: Confirm the invariant remains enforced for rule 1.
- Observable: A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.
- Failure condition: The invariant is breached: A Redemption must not be fulfilled unless reward eligibility and available points are confirmed.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-invariant-1.
