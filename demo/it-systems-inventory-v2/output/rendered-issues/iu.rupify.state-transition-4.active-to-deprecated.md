## Summary

Transition the system lifecycle from Active to Deprecated.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-4` (state_transition: `state-transition-4`)

## Scope

- Transition the system lifecycle from Active to Deprecated.

## Acceptance Criteria

- System can move from Active to Deprecated.

## Verification Shape

- Intent: Confirm the lifecycle transition from Active to Deprecated is allowed and produces the expected target state.
- Observable: System can move from Active to Deprecated.
- Setup requirement: The system starts in the Active state.
- Expected outcome: The system reaches the Deprecated state after the transition is applied.
- Failure condition: The system cannot leave Active for Deprecated when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Deprecated.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-transition-4.
