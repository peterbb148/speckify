## Delivery Metadata

- Implementation unit id: `iu.rupify.state-transition-3.requested-to-rejected`
- Issue slug: `iu-rupify-state-transition-3-requested-to-rejected`
- Labels: `speckify`, `planning`, `source:rupify`, `state-transitions`
- Source anchors: `anchor.rupify.state-transitions.state-transition-3`
- Verification units: `vu.rupify.state-transition-3.requested-to-rejected`
- Depends on:
  - `iu.rupify.guard-condition-2` (Implement guard enforcement: Guard Condition 2)
- Reverse impact hint: Changes here may require upstream review of state-transition-3.

## Summary

Transition the system lifecycle from Requested to Rejected.

## Source Lineage

- `anchor.rupify.state-transitions.state-transition-3` (state_transition: `state-transition-3`)

## Scope

- Transition the system lifecycle from Requested to Rejected.

## Acceptance Criteria

- System can move from Requested to Rejected.

## Verification Shape

- Intent: Confirm the lifecycle transition from Requested to Rejected is allowed and produces the expected target state.
- Observable: System can move from Requested to Rejected.
- Setup requirement: The system starts in the Requested state.
- Expected outcome: The system reaches the Rejected state after the transition is applied.
- Failure condition: The system cannot leave Requested for Rejected when the transition is requested.
- Failure condition: The system enters an unexpected state instead of Rejected.

## Dependencies

- `iu.rupify.guard-condition-2`: Transition implementation depends on the linked guard condition.

## Drift Checks

- Preserve lineage to Rupify element state-transition-3.
