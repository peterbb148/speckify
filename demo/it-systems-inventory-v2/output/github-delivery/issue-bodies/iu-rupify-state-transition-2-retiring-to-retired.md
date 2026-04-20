## Summary

Transition the system lifecycle from Retiring to Retired.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)

## Scope

- Transition the system lifecycle from Retiring to Retired.

## Acceptance Criteria

- System can move from Retiring to Retired.

## Verification Shape

- Intent: Confirm the lifecycle transition from Retiring to Retired is allowed and produces the expected target state.
- Observable: System can move from Retiring to Retired.
- Setup requirement: The system starts in the Retiring state.
- Expected outcome: The system reaches the Retired state after the transition is applied.
- Failure condition: The system cannot leave Retiring for Retired when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Retired.

## Dependencies

- `iu.rupify.state-transition-2.active-to-retiring`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-2.
