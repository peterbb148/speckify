## Delivery Metadata

- Implementation unit id: `iu.rupify.domain-invariant-1`
- Issue slug: `iu-rupify-domain-invariant-1`
- Labels: `speckify`, `planning`, `source:rupify`, `domain-invariants`
- Source anchors: `anchor.rupify.domain-invariants.domain-invariant-1`
- Verification units: `vu.rupify.domain-invariant-1`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of domain-invariant-1.

## Summary

Ensure the invariant 'A System must have a business owner before it becomes Active.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.domain-invariants.domain-invariant-1` (domain_invariant: `domain-invariant-1`)

## Scope

- A System must have a business owner before it becomes Active.

## Acceptance Criteria

- A System must have a business owner before it becomes Active.

## Verification Shape

- Intent: Confirm the invariant remains enforced for rule 1.
- Observable: A System must have a business owner before it becomes Active.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: A System must have a business owner before it becomes Active.
- Failure condition: The invariant is breached: A System must have a business owner before it becomes Active.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element domain-invariant-1.
