## Delivery Metadata

- Implementation unit id: `iu.rupify.review-redemption-analytics-step-2.show-redemption-metrics`
- Issue slug: `iu-rupify-review-redemption-analytics-step-2-show-redemption-metrics`
- Labels: `speckify`, `planning`, `source:rupify`, `use-case-steps`
- Source anchors: `anchor.rupify.use-case-steps.review-redemption-analytics-step-2`
- Verification units: `vu.rupify.review-redemption-analytics-step-2.show-redemption-metrics`
- Depends on:
  - `iu.rupify.review-redemption-analytics-step-1` (Implement Review Redemption Analytics)
- Reverse impact hint: Changes here may require upstream review of review-redemption-analytics-step-2.

## Summary

Implement the behavior described by show redemption metrics.

## Source Lineage

- `anchor.rupify.use-case-steps.review-redemption-analytics-step-2` (requirement: `review-redemption-analytics-step-2`)

## Scope

- Show redemption metrics in the analytics dashboard.

## Acceptance Criteria

- The system shows redemption metrics in the analytics dashboard.

## Verification Shape

- Intent: Confirm the implementation satisfies show redemption metrics.
- Observable: The system shows redemption metrics in the analytics dashboard.
- Expected outcome: The system shows redemption metrics in the analytics dashboard.

## Dependencies

- `iu.rupify.review-redemption-analytics-step-1`: Later use-case steps depend on the earlier step in the same ordered flow.

## Drift Checks

- Preserve lineage to Rupify element review-redemption-analytics-step-2.
