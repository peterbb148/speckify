## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-5.draft-to-published`
- Issue slug: `iu-rupify-state-transition-5-draft-to-published`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-5`
- Verification units: `vu.rupify.state-transition-5.draft-to-published`
- Depends on:
  - `iu.rupify.guard-condition-2` (Implement guard enforcement: Guard Condition 2)
- Reverse impact hint: Changes here may require upstream review of state-transition-5.

## Summary

Transition the system lifecycle from Draft to Published.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-5` (state_transition: `state-transition-5`)

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

- `iu.rupify.guard-condition-2`: Transition implementation depends on the linked guard condition.

## Drift Checks

- Preserve lineage to Rupify element state-transition-5.
