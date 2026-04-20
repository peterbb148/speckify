## Delivery Metadata

- Implementation unit id: `iu.rupify.functional-requirement-1.approval-states`
- Issue slug: `iu-rupify-functional-requirement-1-approval-states`
- Labels: `speckify`, `planning`, `source:rupify`, `functional-requirements`
- Source anchors: `anchor.rupify.functional-requirements.functional-requirement-1`
- Verification units: `vu.rupify.functional-requirement-1.approval-states`
- Depends on:
  - `iu.rupify.functional-requirement-1.stage-gates` (Implement workflow support: Support stage gates)
- Reverse impact hint: Changes here may require upstream review of functional-requirement-1.

## Summary

Support business process approval states.

## Source Lineage

- `anchor.rupify.functional-requirements.functional-requirement-1` (requirement: `functional-requirement-1`)

## Scope

- Support business process approval states.

## Acceptance Criteria

- Business process approval states are supported.

## Verification Shape

- Intent: Confirm workflow support is present for support approval states.
- Observable: Business process approval states are supported.
- Setup requirement: The relevant workflow capability is reachable in the system.
- Expected outcome: The workflow behavior is supported: Business process approval states are supported.
- Failure condition: The workflow behavior is missing or incomplete: Business process approval states are supported.

## Dependencies

- `iu.rupify.functional-requirement-1.stage-gates`: Approval states are coordinated workflow behavior that should follow stage-gate support.

## Drift Checks

- Preserve lineage to Rupify element functional-requirement-1.
