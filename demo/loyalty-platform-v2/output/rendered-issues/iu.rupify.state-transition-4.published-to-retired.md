## Summary

Transition the system lifecycle from Published to Retired.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-4` (state_transition: `state-transition-4`)

## Scope

- Transition the system lifecycle from Published to Retired.

## Acceptance Criteria

- System can move from Published to Retired.

## Verification Shape

- Intent: Confirm the lifecycle transition from Published to Retired is allowed and produces the expected target state.
- Observable: System can move from Published to Retired.
- Setup requirement: The system starts in the Published state.
- Expected outcome: The system reaches the Retired state after the transition is applied.
- Failure condition: The system cannot leave Published for Retired when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Retired.

## Dependencies

- `iu.rupify.state-transition-4.draft-to-published`: Later lifecycle transitions require the earlier transition in the same source chain.

## Drift Checks

- Preserve lineage to Rupify element state-transition-4.
