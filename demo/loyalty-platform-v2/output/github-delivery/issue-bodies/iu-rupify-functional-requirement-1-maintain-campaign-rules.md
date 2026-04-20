## Delivery Metadata

- Implementation unit id: `iu.rupify.functional-requirement-1.maintain-campaign-rules`
- Issue slug: `iu-rupify-functional-requirement-1-maintain-campaign-rules`
- Labels: `speckify`, `planning`, `source:rupify`, `functional-requirements`
- Source anchors: `anchor.rupify.functional-requirements.functional-requirement-1`
- Verification units: `vu.rupify.functional-requirement-1.maintain-campaign-rules`
- Depends on:
  - `iu.rupify.functional-requirement-1.maintain-reward-catalog-entries` (Implement workflow support: Maintain reward catalog entries)
- Reverse impact hint: Changes here may require upstream review of functional-requirement-1.

## Summary

Allow operations managers to maintain campaign rules.

## Source Lineage

- `anchor.rupify.functional-requirements.functional-requirement-1` (requirement: `functional-requirement-1`)

## Scope

- Allow operations managers to maintain campaign rules.

## Acceptance Criteria

- Operations managers can maintain campaign rules.

## Verification Shape

- Intent: Confirm workflow support is present for maintain campaign rules.
- Observable: Operations managers can maintain campaign rules.
- Setup requirement: The relevant workflow capability is reachable in the system.
- Expected outcome: The workflow behavior is supported: Operations managers can maintain campaign rules.
- Failure condition: The workflow behavior is missing or incomplete: Operations managers can maintain campaign rules.

## Dependencies

- `iu.rupify.functional-requirement-1.maintain-reward-catalog-entries`: Campaign rule maintenance should build on maintained reward catalog entries.

## Drift Checks

- Preserve lineage to Rupify element functional-requirement-1.
