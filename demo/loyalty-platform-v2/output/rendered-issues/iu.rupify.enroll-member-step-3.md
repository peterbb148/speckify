## Summary

Deliver the ordered step behavior for enroll member: System validates the submission and creates the member account.

## Source Lineage

- `anchor.rupify.use-case-steps.enroll-member-step-3` (requirement: `enroll-member-step-3`)

## Scope

- System validates the submission and creates the member account.

## Acceptance Criteria

- System validates the submission and creates the member account.

## Verification Shape

- Intent: Confirm the use-case step is delivered for enroll member.
- Observable: System validates the submission and creates the member account.
- Setup requirement: The workflow is positioned at the step where this behavior should occur.
- Expected outcome: The step completes with the expected behavior: System validates the submission and creates the member account.
- Failure condition: The step behavior does not occur as required: System validates the submission and creates the member account.

## Dependencies

- `iu.rupify.enroll-member-step-2`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element enroll-member-step-3.
