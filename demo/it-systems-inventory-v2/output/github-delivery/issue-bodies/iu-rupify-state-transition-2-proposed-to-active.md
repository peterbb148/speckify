## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-2.proposed-to-active`
- Issue slug: `iu-rupify-state-transition-2-proposed-to-active`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-2`
- Verification units: `vu.rupify.state-transition-2.proposed-to-active`
- Depends on: none
- Reverse impact hint: Changes here may require upstream review of state-transition-2.

## Summary

Transition the system lifecycle from Proposed to Active.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)

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
