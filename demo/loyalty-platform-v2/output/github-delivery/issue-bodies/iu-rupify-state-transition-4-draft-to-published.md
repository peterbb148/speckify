## Summary

Transition the system lifecycle from Draft to Published.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-4` (state_transition: `state-transition-4`)

## Scope

- Transition the system lifecycle from Draft to Published.

## Acceptance Criteria

- System can move from Draft to Published.

## Verification Shape

- Intent: Confirm the lifecycle transition from Draft to Published is allowed and produces the expected target state.
- Observable: System can move from Draft to Published.
- Setup requirement: The system starts in the Draft state.
- Expected outcome: The system reaches the Published state after the transition is applied.
- Failure condition: The system cannot leave Draft for Published when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Published.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-transition-4.
