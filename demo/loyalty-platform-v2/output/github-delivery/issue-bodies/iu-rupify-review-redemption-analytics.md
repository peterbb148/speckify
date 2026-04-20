## Delivery Metadata

- Implementation unit id: `iu.rupify.review-redemption-analytics`
- Issue slug: `iu-rupify-review-redemption-analytics`
- Labels: `speckify`, `planning`, `source:rupify`, `use-cases`
- Source anchors: `anchor.rupify.use-cases.review-redemption-analytics`
- Verification units: `vu.rupify.review-redemption-analytics`
- Depends on:
  - `iu.rupify.review-redemption-analytics-extension-1` (Implement Review Redemption Analytics)
  - `iu.rupify.review-redemption-analytics-step-1` (Implement Review Redemption Analytics)
  - `iu.rupify.review-redemption-analytics-step-2.show-campaign-metrics` (Implement Show campaign metrics)
  - `iu.rupify.review-redemption-analytics-step-2.show-redemption-metrics` (Implement Show redemption metrics)
- Reverse impact hint: Changes here may require upstream review of review-redemption-analytics.

## Summary

Coordinate the Review Redemption Analytics flow across its steps and extension handling.

## Source Lineage

- `anchor.rupify.use-cases.review-redemption-analytics` (requirement: `review-redemption-analytics`)

## Scope

- Coordinate the Review Redemption Analytics flow across its steps and extension handling.

## Acceptance Criteria

- The Review Redemption Analytics flow is supported end to end.

## Verification Shape

- Intent: Confirm the use-case flow is supported end to end for review redemption analytics.
- Observable: The Review Redemption Analytics flow is supported end to end.
- Setup requirement: The actor can start the use-case flow through its normal entry point.
- Expected outcome: The use-case flow completes as intended: The Review Redemption Analytics flow is supported end to end.
- Failure condition: The use-case flow is incomplete or broken: The Review Redemption Analytics flow is supported end to end.

## Dependencies

- `iu.rupify.review-redemption-analytics-extension-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.review-redemption-analytics-step-1`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.review-redemption-analytics-step-2.show-campaign-metrics`: Use-case orchestration depends on the linked step and extension units.
- `iu.rupify.review-redemption-analytics-step-2.show-redemption-metrics`: Use-case orchestration depends on the linked step and extension units.

## Drift Checks

- Preserve lineage to Rupify element review-redemption-analytics.
