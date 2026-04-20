## Delivery Metadata

- Implementation unit id: `iu.rupify.browse-rewards-step-3`
- Issue slug: `iu-rupify-browse-rewards-step-3`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.browse-rewards-step-3`
- Verification units: `vu.rupify.browse-rewards-step-3`
- Depends on:
  - `iu.rupify.browse-rewards-step-2.display-points-balance` (Implement Display points balance)
  - `iu.rupify.browse-rewards-step-2.display-rewards` (Implement Display available rewards)
- Reverse impact hint: Changes here may require upstream review of browse-rewards-step-3.

## Summary

Implement the behavior described by browse rewards.

## Source Lineage

- `anchor.rupify.use-case-steps.browse-rewards-step-3` (requirement: `browse-rewards-step-3`)

## Scope

- Customer filters or sorts the catalog.

## Acceptance Criteria

- Customer filters or sorts the catalog.

## Verification Shape

- Intent: Confirm the implementation satisfies browse rewards.
- Observable: Customer filters or sorts the catalog.
- Expected outcome: Customer filters or sorts the catalog.

## Dependencies

- `iu.rupify.browse-rewards-step-2.display-points-balance`: Later use-case steps depend on the earlier step in the same ordered flow.
- `iu.rupify.browse-rewards-step-2.display-rewards`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element browse-rewards-step-3.
