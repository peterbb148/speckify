## Delivery Metadata

- Implementation unit id: `iu.rupify.enroll-member-step-2`
- Issue slug: `iu-rupify-enroll-member-step-2`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.enroll-member-step-2`
- Verification units: `vu.rupify.enroll-member-step-2`
- Depends on:
  - `iu.rupify.enroll-member-step-1` (Implement use-case step: Enroll Member)
- Reverse impact hint: Changes here may require upstream review of enroll-member-step-2.

## Summary

Deliver the ordered step behavior for enroll member: Customer provides the required details and consents.

## Source Lineage

- `anchor.rupify.use-case-steps.enroll-member-step-2` (requirement: `enroll-member-step-2`)

## Scope

- Customer provides the required details and consents.

## Acceptance Criteria

- Customer provides the required details and consents.

## Verification Shape

- Intent: Confirm the use-case step is delivered for enroll member.
- Observable: Customer provides the required details and consents.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: Customer provides the required details and consents.
- Failure condition: The step behavior does not occur as required: Customer provides the required details and consents.

## Dependencies

- `iu.rupify.enroll-member-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element enroll-member-step-2.
