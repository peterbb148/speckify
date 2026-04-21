## Delivery Metadata

- Implementation unit id: `iu.rupify.enroll-member-extension-1`
- Issue slug: `iu-rupify-enroll-member-extension-1`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.enroll-member-extension-1`
- Verification units: `vu.rupify.enroll-member-extension-1`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of enroll-member-extension-1.

## Summary

Deliver the ordered step behavior for enroll member: Enrollment is blocked when required consent is missing.

## Source Lineage

- `anchor.rupify.use-case-steps.enroll-member-extension-1` (requirement: `enroll-member-extension-1`)

## Scope

- Enrollment is blocked when required consent is missing.

## Acceptance Criteria

- Enrollment is blocked when required consent is missing.

## Verification Shape

- Intent: Confirm the use-case step is delivered for enroll member.
- Observable: Enrollment is blocked when required consent is missing.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: Enrollment is blocked when required consent is missing.
- Failure condition: The step behavior does not occur as required: Enrollment is blocked when required consent is missing.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element enroll-member-extension-1.
