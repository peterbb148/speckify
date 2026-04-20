## Delivery Metadata

- Implementation unit id: `iu.rupify.enroll-member-step-3`
- Issue slug: `iu-rupify-enroll-member-step-3`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.enroll-member-step-3`
- Verification units: `vu.rupify.enroll-member-step-3`
- Depends on:
  - `iu.rupify.enroll-member-step-2` (Implement Enroll Member)
- Reverse impact hint: Changes here may require upstream review of enroll-member-step-3.

## Summary

Implement the behavior described by enroll member.

## Source Lineage

- `anchor.rupify.use-case-steps.enroll-member-step-3` (requirement: `enroll-member-step-3`)

## Scope

- System validates the submission and creates the member account.

## Acceptance Criteria

- System validates the submission and creates the member account.

## Verification Shape

- Intent: Confirm the implementation satisfies enroll member.
- Observable: System validates the submission and creates the member account.
- Expected outcome: System validates the submission and creates the member account.

## Dependencies

- `iu.rupify.enroll-member-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element enroll-member-step-3.
