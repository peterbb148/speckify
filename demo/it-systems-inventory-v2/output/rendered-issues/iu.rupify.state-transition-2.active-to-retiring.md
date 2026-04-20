## Summary

Implement the planned behavior for active to retiring.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-2`

## Scope

- Transition the system lifecycle from Active to Retiring.

## Acceptance Criteria

- System can move from Active to Retiring.

## Verification Shape

- Intent: Confirm the lifecycle transition from Active to Retiring is allowed and produces the expected target state.
- Observable: System can move from Active to Retiring.
- Setup requirement: The system starts in the Active state.
- Expected outcome: The system reaches the Retiring state after the transition is applied.
- Failure condition: The system cannot leave Active for Retiring when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Retiring.

## Dependencies

- `iu.rupify.state-transition-2.proposed-to-active`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-2.
