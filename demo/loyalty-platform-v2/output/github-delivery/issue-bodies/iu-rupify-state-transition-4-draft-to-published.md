## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-4.draft-to-published`
- Issue slug: `iu-rupify-state-transition-4-draft-to-published`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-4`
- Verification units: `vu.rupify.state-transition-4.draft-to-published`
- Depends on:
  - `iu.rupify.guard-condition-2.block-publish-without-approval` (Implement guard enforcement: Block publish without approval)
  - `iu.rupify.guard-condition-2.require-validation-approval` (Implement guard enforcement: Require catalog validation approval)
- Reverse impact hint: Changes here may require upstream review of state-transition-4.

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

- `iu.rupify.guard-condition-2.block-publish-without-approval`: Transition implementation depends on the linked guard condition.
- `iu.rupify.guard-condition-2.require-validation-approval`: Transition implementation depends on the linked guard condition.

## Drift Checks

- Preserve lineage to Rupify element state-transition-4.
