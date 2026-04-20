## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-5.published-to-retired`
- Issue slug: `iu-rupify-state-transition-5-published-to-retired`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-5`
- Verification units: `vu.rupify.state-transition-5.published-to-retired`
- Depends on:
  - `iu.rupify.state-transition-5.draft-to-published` (Implement lifecycle transition: Draft to Published)
  - `iu.rupify.guard-condition-2` (Implement Guard Condition 2)
- Reverse impact hint: Changes here may require upstream review of state-transition-5.

## Summary

Transition the system lifecycle from Published to Retired.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-5` (state_transition: `state-transition-5`)

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

- `iu.rupify.state-transition-5.draft-to-published`: Later lifecycle transitions require the earlier transition in the same source chain.
- `iu.rupify.guard-condition-2`: Transition implementation depends on the linked guard condition.

## Drift Checks

- Preserve lineage to Rupify element state-transition-5.
