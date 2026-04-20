## Summary

Implement the planned behavior for active to retiring.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-3`

## Scope

- Transition the system lifecycle from Active to Retiring.

## Acceptance Criteria

- System can move from Active to Retiring.

## Verification Shape

- Intent: Confirm the implementation satisfies active to retiring.
- Observable: System can move from Active to Retiring.
- Expected outcome: System can move from Active to Retiring.

## Dependencies

- `iu.rupify.state-transition-3.proposed-to-active`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-3.
