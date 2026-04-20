## Delivery Metadata

- Implementation unit id: `iu.rupify.enroll-member`
- Issue slug: `iu-rupify-enroll-member`
- Labels: `speckify`, `planning`, `source:rupify`, `use-cases`
- Source anchors: `anchor.rupify.use-cases.enroll-member`
- Verification units: `vu.rupify.enroll-member`
- Depends on:
  - `iu.rupify.enroll-member-extension-1` (Implement Enroll Member)
  - `iu.rupify.enroll-member-step-1` (Implement Enroll Member)
  - `iu.rupify.enroll-member-step-2` (Implement Enroll Member)
  - `iu.rupify.enroll-member-step-3` (Implement Enroll Member)
- Reverse impact hint: Changes here may require upstream review of enroll-member.

## Summary

Coordinate the Enroll Member flow across its steps and extension handling.

## Source Lineage

- `anchor.rupify.use-cases.enroll-member` (requirement: `enroll-member`)

## Scope

- Coordinate the Enroll Member flow across its steps and extension handling.

## Acceptance Criteria

- The Enroll Member flow is supported end to end.

## Verification Shape

- Intent: Confirm the use-case flow is supported end to end for enroll member.
- Observable: The Enroll Member flow is supported end to end.
- Setup requirement: The actor can start the use-case flow through its normal entry point.
- Expected outcome: The use-case flow completes as intended: The Enroll Member flow is supported end to end.
- Failure condition: The use-case flow is incomplete or broken: The Enroll Member flow is supported end to end.

## Dependencies

- `iu.rupify.enroll-member-extension-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.enroll-member-step-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.enroll-member-step-2`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.enroll-member-step-3`: Use-case orchestration depends on the linked step and extension units.

## Drift Checks

- Preserve lineage to Rupify element enroll-member.
