## Delivery Metadata

- Implementation unit id: `iu.rupify.domain-invariant-3`
- Issue slug: `iu-rupify-domain-invariant-3`
- Labels: `speckify`, `planning`, `source:rupify`, `domain-invariants`
- Source anchors: `anchor.rupify.domain-invariants.domain-invariant-3`
- Verification units: `vu.rupify.domain-invariant-3`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of domain-invariant-3.

## Summary

Ensure the invariant 'A System must record vendor and contract dates.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.domain-invariants.domain-invariant-3` (domain_invariant: `domain-invariant-3`)

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

- Preserve lineage to Rupify element domain-invariant-3.
