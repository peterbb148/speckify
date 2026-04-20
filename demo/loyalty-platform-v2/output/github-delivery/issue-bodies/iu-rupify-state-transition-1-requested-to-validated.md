## Summary

Transition the system lifecycle from Requested to Validated.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-1` (state_transition: `state-transition-1`)

## Scope

- Transition the system lifecycle from Requested to Validated.

## Acceptance Criteria

- System can move from Requested to Validated.

## Verification Shape

- Intent: Confirm the lifecycle transition from Requested to Validated is allowed and produces the expected target state.
- Observable: System can move from Requested to Validated.
- Setup requirement: The system starts in the Requested state.
- Expected outcome: The system reaches the Validated state after the transition is applied.
- Failure condition: The system cannot leave Requested for Validated when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Validated.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-transition-1.
