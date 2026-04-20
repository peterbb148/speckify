## Summary

Block a reward from becoming published when catalog validation approval is missing.

## Source Lineage

- `anchor.rupify.guard-conditions.guard-condition-2` (requirement: `guard-condition-2`)

## Scope

- Block a reward from becoming published when catalog validation approval is missing.

## Acceptance Criteria

- A reward does not become Published without catalog validation approval.

## Verification Shape

- Intent: Confirm the guard enforcement is applied for block publish without approval.
- Observable: A reward does not become Published without catalog validation approval.
- Setup requirement: A request reaches the boundary where the guard condition must be checked.
- Expected outcome: The guard enforcement is applied correctly: A reward does not become Published without catalog validation approval.
- Failure condition: The guard condition is not enforced as required: A reward does not become Published without catalog validation approval.

## Dependencies

- `iu.rupify.guard-condition-2.require-validation-approval`: Guard enforcement depends on recognizing the guard prerequisite first.

## Drift Checks

- Preserve lineage to Rupify element guard-condition-2.
