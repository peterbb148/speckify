# Delivery Issue-Ready Gates

Speckify delivery exports can be structurally valid without yet being ready for
downstream GitHub issue publication. This note defines the explicit gate set for that
second bar.

The purpose of these gates is to separate:

- schema-valid planning output
- publication-ready issue payloads

These gates do not authorize new decomposition logic. They only evaluate whether the
current delivery export is strong enough for a separate publication workflow to consume
without manual cleanup.

## Principles

- Gates evaluate generated delivery payloads, not source prose.
- Gates must be concrete enough to automate or review deterministically.
- Gates must preserve the Constitution: no demo-shaped logic, no hidden fallback path,
  no publication by optimism.
- Failing a gate should block publication readiness, not silently downgrade behavior.

## Issue-Level Gates

Each exported issue should pass all of the following:

1. `title_avoids_raw_source_identifiers`
   Titles must not expose raw source-style identifiers such as
   `non_functional-requirement-1`.

2. `title_avoids_generic_ordinals`
   Titles must not rely on generic labels such as `Requirement 1`,
   `Constraint 1`, or `Scenario 2`.

3. `summary_is_substantive`
   The summary must provide enough implementation context to stand on its own.

4. `body_sections_present`
   The delivery body must contain:
   - `Delivery Metadata`
   - `Summary`
   - `Source Lineage`
   - `Scope`
   - `Acceptance Criteria`
   - `Verification Shape`
   - `Drift Checks`

5. `acceptance_criteria_are_present`
   The issue body must contain at least one acceptance criterion bullet.

6. `verification_shape_is_complete`
   Verification guidance must include:
   - intent
   - observable
   - setup requirement
   - expected outcome
   - failure condition

7. `verification_shape_is_distinct`
   Observable and expected outcome must not collapse into the same sentence.

8. `lineage_is_visible`
   Source anchors and verification unit ids must be present in the delivery export.

9. `create_payload_is_complete`
   The create payload must include title, body path, and labels.

10. `dependencies_are_explained`
    Dependency ids and dependency titles must stay aligned, and dependency-bearing
    issues must explain those dependencies in the body.

## Bundle-Level Gate

11. `all_issues_pass`
    A bundle is publication-ready only if every exported issue passes all issue-level
    gates.

## Current Use

These gates are intended to be applied against the checked-in V2 delivery exports:

- [IT systems inventory V2 demo](../demo/it-systems-inventory-v2/README.md)
- [Loyalty platform V2 demo](../demo/loyalty-platform-v2/README.md)

The current reports describe exactly where the remaining issue-publication gaps are, so
the next payload-improvement work can target those failures directly.
