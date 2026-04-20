## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-2.validated-to-fulfilled`
- Issue slug: `iu-rupify-state-transition-2-validated-to-fulfilled`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-2`
- Verification units: `vu.rupify.state-transition-2.validated-to-fulfilled`
- Depends on:
  - `iu.rupify.state-transition-2.requested-to-validated` (Implement lifecycle transition: Requested to Validated)
  - `iu.rupify.guard-condition-2` (Implement Guard Condition 2)
- Reverse impact hint: Changes here may require upstream review of state-transition-2.

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
- `iu.rupify.guard-condition-2`: Transition implementation depends on the linked guard condition.

## Drift Checks

- Preserve lineage to Rupify element state-transition-2.
