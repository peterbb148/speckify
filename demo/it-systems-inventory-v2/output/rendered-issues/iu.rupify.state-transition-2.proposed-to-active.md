## Summary

Implement the planned behavior for proposed to active.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-2`

## Scope

- Transition the system lifecycle from Proposed to Active.

## Acceptance Criteria

- System can move from Proposed to Active.

## Verification Shape

- Intent: Confirm the lifecycle transition from Proposed to Active is allowed and produces the expected target state.
- Observable: System can move from Proposed to Active.
- Setup requirement: The system starts in the Proposed state.
- Expected outcome: The system reaches the Active state after the transition is applied.
- Failure condition: The system cannot leave Proposed for Active when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Active.

## Dependencies

- None

## Drift Checks

- Preserve lineage to Rupify element state-transition-2.
