# Speckify Output Artifacts And Issue Rendering

## Purpose

This note defines the machine-readable output artifacts Speckify should emit and how
those artifacts should render into GitHub issue-ready text and verification-oriented
outputs.

This is the main artifact for issue `#5`.

## Scope

This note covers:

- the output bundle Speckify should emit after decomposition
- required and optional fields for key output records
- bundle-level artifacts such as traceability matrices and dependency graphs
- rendering rules from machine-readable records into issue-ready Markdown
- worked examples for both structured output and rendered issue text

This note does not cover:

- code generation
- GitHub automation implementation
- round-trip feedback artifacts for reversibility

## Output Design Principles

The output model should follow these rules:

- structured artifacts come first
- rendered issue text is a projection of those artifacts
- traceability must remain explicit in both structured and rendered forms
- rendered artifacts should be concise, but never hide source lineage or constraints
- the same underlying data should support human review and later automation

## Output Bundle Shape

Speckify should emit one planning bundle per decomposition run.

### Root Shape

```yaml
bundle_metadata:
source_summary:
source_anchors: []
spec_units: []
implementation_units: []
verification_units: []
trace_bundles: []
dependency_edges: []
assembly_rules: []
unresolved_ambiguities: []
rendered_issues: []
```

## Bundle Metadata

### `bundle_metadata`

Required fields:

- `bundle_id`
- `bundle_version`
- `generated_at`

Recommended optional fields:

- `source_model_id`
- `source_model_version`
- `decomposition_profile`

### `source_summary`

Required fields:

- `source_system`
- `project_id`

Recommended optional fields:

- `project_name`
- `export_version`
- `notes`

## Core Output Records

### SourceAnchor

`SourceAnchor` should be preserved in the output bundle so every downstream record can be
resolved back to the originating Rupify elements.

Required fields:

- `id`
- `source_system`
- `source_type`
- `source_id`
- `view`

Optional fields:

- `parent_source_id`
- `normative`
- `ready_state`
- `trace`

### SpecUnit

`SpecUnit` expresses the decomposed obligation layer.

Required fields:

- `id`
- `title`
- `summary`
- `source_anchor_ids`
- `obligation_kind`

Optional fields:

- `normative`
- `status`
- `notes`

### ImplementationUnit

`ImplementationUnit` is the main planning record for GitHub issue generation.

Required fields:

- `id`
- `title`
- `summary`
- `derived_from_spec_unit_ids`
- `source_anchor_ids`
- `implementation_scope`
- `acceptance_criteria`

Recommended optional fields:

- `dependencies`
- `non_goals`
- `constraints`
- `verification_unit_ids`
- `drift_checks`
- `reverse_impact_hint`
- `labels`

Example:

```yaml
id: iu.authentication.capture_credentials
title: Add credential capture entrypoint
summary: Implement the boundary that accepts authentication credentials.
derived_from_spec_unit_ids:
  - su.authentication.capture_credentials
source_anchor_ids:
  - anchor.requirement.req-auth-001
  - anchor.use_case.uc_authenticate.step.capture_credentials
dependencies: []
implementation_scope:
  - accept username and password input
  - expose a callable boundary for downstream authentication logic
non_goals:
  - verify credentials against a user store
constraints:
  - preserve lineage to the authentication use case step
acceptance_criteria:
  - credential submission payload is accepted at the authentication boundary
verification_unit_ids:
  - vu.authentication.capture_credentials
drift_checks:
  - do not bypass the source use case flow ordering
reverse_impact_hint: Changes here may affect authentication entry semantics upstream.
labels:
  - planning
  - authentication
```

### VerificationUnit

`VerificationUnit` captures proof intent independent from code implementation.

Required fields:

- `id`
- `implementation_unit_id`
- `title`
- `verification_intent`
- `source_anchor_ids`
- `observables`
- `expected_outcomes`

Recommended optional fields:

- `setup_requirements`
- `failure_conditions`
- `invariants_preserved`
- `notes`

Example:

```yaml
id: vu.authentication.capture_credentials
implementation_unit_id: iu.authentication.capture_credentials
title: Verify credential capture behavior
verification_intent: Confirm that authentication credentials can be submitted to the boundary.
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
observables:
  - credential payload is accepted by the authentication boundary
setup_requirements:
  - authentication entrypoint is available
expected_outcomes:
  - valid credential payload reaches the defined system boundary
failure_conditions:
  - payload is rejected before downstream verification logic begins
invariants_preserved: []
```

### TraceBundle

`TraceBundle` groups lineage across the source, decomposition, implementation, and
verification layers.

Required fields:

- `id`
- `source_anchor_ids`
- `spec_unit_ids`
- `implementation_unit_ids`
- `verification_unit_ids`

Recommended optional fields:

- `assembly_rule_ids`
- `notes`

### DependencyEdge

Dependencies should be explicit, machine-readable records rather than only prose in issue
bodies.

Required fields:

- `id`
- `from_implementation_unit_id`
- `to_implementation_unit_id`
- `dependency_type`

Recommended optional fields:

- `reason`

Allowed `dependency_type` examples:

- `blocks`
- `requires`
- `soft_sequence`

### AssemblyRule

`AssemblyRule` describes how multiple units recompose into source-level behavior.

Required fields:

- `id`
- `source_anchor_ids`
- `member_spec_unit_ids`
- `rule_type`

Recommended optional fields:

- `notes`

Allowed `rule_type` examples:

- `ordered_sequence`
- `constraint_overlay`
- `state_guarded_behavior`

## Bundle-Level Outputs

Speckify should emit several bundle-level outputs in addition to the core records.

### 1. Traceability Matrix

Purpose:

- show how source anchors map into `SpecUnit`, `ImplementationUnit`, and
  `VerificationUnit` records

Suggested shape:

```yaml
- source_anchor_id: anchor.use_case.uc_authenticate.step.capture_credentials
  spec_unit_ids:
    - su.authentication.capture_credentials
  implementation_unit_ids:
    - iu.authentication.capture_credentials
  verification_unit_ids:
    - vu.authentication.capture_credentials
```

### 2. Dependency Graph

Purpose:

- show implementation ordering constraints without burying them in prose

Suggested representation:

- machine-readable `dependency_edges`
- optional rendered Mermaid or adjacency list view later

### 3. Unresolved Ambiguity List

Purpose:

- carry forward ambiguities that remain relevant after decomposition

Suggested shape:

```yaml
- ambiguity_id: amb-auth-format
  affects_implementation_unit_ids:
    - iu.authentication.capture_credentials
  status: open
  blocking: false
```

### 4. Rendered Issue Projections

Purpose:

- provide issue-ready text without making GitHub issue prose the source of truth

Suggested shape:

```yaml
- implementation_unit_id: iu.authentication.capture_credentials
  issue_title: Add credential capture entrypoint
  issue_body: |
    ...
```

## Rendering Rules

Rendered issue text should be a deterministic projection of `ImplementationUnit`,
`VerificationUnit`, `TraceBundle`, and dependency data.

### Title Rule

Issue titles should come directly from `ImplementationUnit.title`.

Title properties:

- action-oriented
- implementation-sized
- should not repeat unrelated context or toolchain explanations

### Body Sections

Every rendered issue body should contain the same top-level sections in the same order.

Recommended sections:

1. Summary
2. Source Lineage
3. Scope
4. Non-goals
5. Constraints
6. Acceptance Criteria
7. Verification Shape
8. Dependencies
9. Drift Checks

### Section Mapping Rules

#### Summary

Source:

- `ImplementationUnit.summary`

#### Source Lineage

Source:

- `source_anchor_ids`
- optional human-friendly lookup text from `SourceAnchor`

Requirements:

- always include source anchor identifiers
- optionally include a short readable label if available

#### Scope

Source:

- `implementation_scope`

Requirements:

- render as a flat bullet list

#### Non-goals

Source:

- `non_goals`

Requirements:

- omit section only if empty

#### Constraints

Source:

- `constraints`

Requirements:

- render all explicit constraints
- do not merge constraints into prose summary

#### Acceptance Criteria

Source:

- `acceptance_criteria`

Requirements:

- render each criterion as a flat bullet
- preserve the original planning statements

#### Verification Shape

Source:

- linked `VerificationUnit` records

Requirements:

- summarize verification intent
- include observables, setup requirements when relevant, expected outcomes, and failure
  conditions when present

#### Dependencies

Source:

- `dependencies`
- `dependency_edges`

Requirements:

- list blocking or required dependencies explicitly
- if none exist, say `None`

#### Drift Checks

Source:

- `drift_checks`

Requirements:

- make drift constraints explicit so later implementation does not quietly diverge

## Example Structured Output

```yaml
implementation_units:
  - id: iu.authentication.capture_credentials
    title: Add credential capture entrypoint
    summary: Implement the boundary that accepts authentication credentials.
    derived_from_spec_unit_ids:
      - su.authentication.capture_credentials
    source_anchor_ids:
      - anchor.requirement.req-auth-001
      - anchor.use_case.uc_authenticate.step.capture_credentials
    implementation_scope:
      - accept username and password input
      - expose a callable boundary for downstream authentication logic
    non_goals:
      - verify credentials against a user store
    constraints:
      - preserve lineage to the authentication use case step
    acceptance_criteria:
      - credential submission payload is accepted at the authentication boundary
    verification_unit_ids:
      - vu.authentication.capture_credentials
    drift_checks:
      - do not bypass the source use case flow ordering

verification_units:
  - id: vu.authentication.capture_credentials
    implementation_unit_id: iu.authentication.capture_credentials
    title: Verify credential capture behavior
    verification_intent: Confirm that authentication credentials can be submitted to the boundary.
    source_anchor_ids:
      - anchor.use_case.uc_authenticate.step.capture_credentials
    observables:
      - credential payload is accepted by the authentication boundary
    expected_outcomes:
      - valid credential payload reaches the defined system boundary
```

## Example Rendered Issue

```md
## Summary

Implement the boundary that accepts authentication credentials.

## Source Lineage

- `anchor.requirement.req-auth-001`
- `anchor.use_case.uc_authenticate.step.capture_credentials`

## Scope

- accept username and password input
- expose a callable boundary for downstream authentication logic

## Non-goals

- verify credentials against a user store

## Constraints

- preserve lineage to the authentication use case step

## Acceptance Criteria

- credential submission payload is accepted at the authentication boundary

## Verification Shape

- Intent: Confirm that authentication credentials can be submitted to the boundary.
- Observable: credential payload is accepted by the authentication boundary
- Expected outcome: valid credential payload reaches the defined system boundary

## Dependencies

- None

## Drift Checks

- do not bypass the source use case flow ordering
```

## Validation Rules For Rendered Output

Before rendering an issue projection, Speckify should validate that:

- the `ImplementationUnit` is valid
- every referenced `VerificationUnit` exists
- every referenced `SourceAnchor` exists
- acceptance criteria are non-empty
- issue title and summary are non-empty

Rendered issue output should be blocked if those conditions are not satisfied.

## What Belongs In Structured Artifacts Versus Issue Prose

### Must Stay Structured

- identifiers
- lineage and trace bundle links
- dependencies
- ambiguity status
- decomposition metadata

### May Be Projected Into Issue Prose

- summary
- scope
- non-goals
- constraints
- acceptance criteria
- verification shape
- drift checks

The structured artifact remains authoritative in all cases.

## Recommended Future Extensions

- rendered Markdown files per implementation unit
- optional Mermaid dependency graph exports
- issue label generation from view type or domain tags
- GitHub template generation from the same rendering contract

## Open Questions

- should `rendered_issues` be stored in the planning bundle or generated on demand
- should dependency graphs be exported only as edges or also as a pre-rendered human view
- how much source-anchor text should be included in rendered issues beyond stable IDs
