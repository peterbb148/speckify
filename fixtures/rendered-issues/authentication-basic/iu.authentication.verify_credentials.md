## Summary

Implement the verification step after credentials have been captured.

## Source Lineage

- `anchor.use_case.uc-authenticate.step.verify-credentials`

## Scope

- Invoke verification logic after credential submission.

## Non-goals

- Define password reset or account recovery flows.

## Constraints

- Credentials must be submitted before verification can begin.

## Acceptance Criteria

- Credential verification occurs only after credential submission.

## Verification Shape

- Intent: Confirm that verification occurs only after credential submission.
- Observable: Verification logic runs after credential capture.
- Expected outcome: Verification cannot begin before credentials are submitted.

## Dependencies

- `iu.authentication.capture_credentials`

## Drift Checks

- Preserve the precondition that capture precedes verification.
