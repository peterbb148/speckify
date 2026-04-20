## Delivery Metadata

- Implementation unit id: `iu.rupify.domain-invariant-3.record-vendor`
- Issue slug: `iu-rupify-domain-invariant-3-record-vendor`
- Labels: `speckify`, `planning`, `source:rupify`, `domain-invariants`
- Source anchors: `anchor.rupify.domain-invariants.domain-invariant-3`
- Verification units: `vu.rupify.domain-invariant-3.record-vendor`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of domain-invariant-3.

## Summary

Ensure the invariant 'The system records vendor information.' is enforced in the implemented behavior.

## Source Lineage

- `anchor.rupify.domain-invariants.domain-invariant-3` (domain_invariant: `domain-invariant-3`)

## Scope

- Record vendor information for the system.

## Acceptance Criteria

- The system records vendor information.

## Verification Shape

- Intent: Confirm the invariant remains enforced for record vendor.
- Observable: The system records vendor information.
- Setup requirement: A representative system record exists in a state where the rule applies.
- Expected outcome: The invariant remains true: The system records vendor information.
- Failure condition: The invariant is breached: The system records vendor information.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element domain-invariant-3.
