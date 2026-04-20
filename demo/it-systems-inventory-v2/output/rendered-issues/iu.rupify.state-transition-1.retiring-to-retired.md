## Summary

Implement the planned behavior for retiring to retired.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-1`

## Scope

- Transition the system lifecycle from Retiring to Retired.

## Acceptance Criteria

- System can move from Retiring to Retired.

## Verification Shape

- Intent: Confirm the implementation satisfies retiring to retired.
- Observable: System can move from Retiring to Retired.
- Expected outcome: System can move from Retiring to Retired.

## Dependencies

- `iu.rupify.state-transition-1.active-to-retiring`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-1.
