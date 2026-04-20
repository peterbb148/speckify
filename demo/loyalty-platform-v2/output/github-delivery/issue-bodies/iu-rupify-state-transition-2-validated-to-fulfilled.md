## Summary

Transition the system lifecycle from Validated to Fulfilled.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)

## Scope

- Transition the system lifecycle from Validated to Fulfilled.

## Acceptance Criteria

- System can move from Validated to Fulfilled.

## Verification Shape

- Intent: Confirm the lifecycle transition from Validated to Fulfilled is allowed and produces the expected target state.
- Observable: System can move from Validated to Fulfilled.
- Setup requirement: The system starts in the Validated state.
- Expected outcome: The system reaches the Fulfilled state after the transition is applied.
- Failure condition: The system cannot leave Validated for Fulfilled when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Fulfilled.

## Dependencies

- `iu.rupify.state-transition-2.requested-to-validated`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-2.
