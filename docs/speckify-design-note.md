# Speckify Design Note

## Purpose

Speckify is the formal planning layer between Rupify and GitHub SpecKit-driven
implementation. Its role is to transform structured specification artifacts into
implementation-ready work units and verification definitions without losing traceability
to the source model.

The intended flow is:

`Rupify canonical model -> Speckify decomposition model -> issue specs + verification specs -> GitHub issues / SpecKit workflows`

Speckify should not re-interpret freeform requirements from scratch, and it should not
act as an implementation engine. It exists to preserve semantic intent while making the
specification operational for controlled, incremental delivery.

## Architectural Position

Rupify remains the source-of-truth specification engine.

Speckify consumes Rupify's structured outputs, performs formal decomposition into atomic
units, shapes verification intent independently from code implementation, and emits
artifacts that can drive issue-based development.

GitHub SpecKit then consumes those artifacts to guide implementation and constitutional
verification in the coding workflow.

## Input Contract

Speckify should consume a normalized machine-readable export from Rupify rather than
rendered Markdown alone.

Required input areas:

- `project`: project summary, scope, business goals, success criteria
- `requirements`: functional and non-functional requirements with stable identifiers
- `actors`: actors with stable identifiers and roles
- `use_cases`: use cases, preconditions, postconditions, and flows
- `scenarios`: scenario-level steps and scenario-to-use-case relationships
- `domain_elements`: entities, relationships, rules, and invariants
- `interaction_elements`: participants, messages, and ordering constraints
- `state_elements`: states, transitions, guards, and triggers
- `design_elements`: components, interfaces, deployment or runtime boundaries
- `traceability`: cross-view lineage already known in Rupify
- `provenance`: source interview rounds, assumptions, open questions, and uncertainty
- `readiness`: completion status for downstream-safe decomposition

Expected contract behavior:

- Speckify should prefer the canonical Rupify model over rendered documents
- Speckify should fail clearly or mark output partial when required source structure is
  absent
- Speckify should carry unresolved ambiguities forward rather than inventing substitutes

## Internal Model

Speckify should introduce its own intermediate representation instead of emitting GitHub
issues directly from Rupify structures.

Core entities:

- `SourceAnchor`: stable pointer to a Rupify model element
- `SpecUnit`: smallest semantically coherent obligation derived from one or more source
  anchors
- `ImplementationUnit`: issue-sized work slice suitable for one branch and one pull
  request
- `VerificationUnit`: independent verification contract for an implementation unit
- `TraceBundle`: lineage from source anchors through decomposition and verification
- `AssemblyRule`: rule for recomposing decomposed units into source-level behavior
- `ChangeImpact`: structured record of how downstream edits affect the source model

Key modeling rule:

Speckify should not assume that one UML element always maps to one implementation unit.
The transform must make one-to-many and many-to-one relationships explicit.

## Decomposition Rules

Decomposition should be rule-based and view-aware.

Use cases:

- split by main success path step
- split by alternate and exception flows
- split by preconditions and postconditions
- split by actor-to-system responsibility boundaries

Scenarios and interactions:

- split by observable interaction contract
- split by message sequencing obligations
- split by integration boundary crossings

Domain model:

- split by entity lifecycle responsibility
- split by invariant or business rule
- split by relationship maintenance obligation

State model:

- split by transition
- split by guard condition
- split by terminal or invalid-state behavior

Requirements and constraints:

- split by independently testable acceptance condition
- isolate cross-cutting concerns as explicit obligations rather than burying them inside
  feature slices

Validation rules for a decomposed unit:

- it must be traceable to source anchors
- it must be independently implementable
- it must be independently verifiable
- it must be semantically narrow enough for one controlled pull request
- it must be re-assemblable into the originating source behavior

## Output Schema

Speckify should emit structured machine-readable artifacts first, with rendered GitHub
issue text as a downstream presentation layer.

### ImplementationUnit fields

- `id`
- `title`
- `summary`
- `source_anchor_ids`
- `derived_from_spec_unit_ids`
- `dependencies`
- `implementation_scope`
- `non_goals`
- `constraints`
- `acceptance_criteria`
- `verification_unit_ids`
- `drift_checks`
- `reverse_impact_hint`

### VerificationUnit fields

- `id`
- `implementation_unit_id`
- `verification_intent`
- `observables`
- `setup_requirements`
- `expected_outcomes`
- `failure_conditions`
- `invariants_preserved`
- `source_anchor_ids`

### Bundle-level outputs

- traceability matrix
- dependency graph
- assembly map back to source spec fragments
- unresolved ambiguity list

## Verification Philosophy

Speckify should define the shape of verification without necessarily generating final test
code itself.

That means Speckify should define:

- what observable behavior must be demonstrated
- what setup or state assumptions are required
- what outcomes or transitions are expected
- what edge conditions must be checked
- what invariants must remain true

This preserves separation between the actor that shapes verification intent and the actor
that implements the code under test.

## Reversibility Model

Reversibility requires Speckify to behave as a loss-aware, lineage-preserving transform.

Rules:

- every derived unit retains explicit source references
- every split records the rule used to produce it
- every downstream change references the affected implementation or verification unit
- changes that alter source semantics are surfaced upstream rather than absorbed silently

Recommended downstream change classes:

- `implementation_conforming`
- `verification_refinement`
- `spec_clarification`
- `spec_conflict`

Only `spec_clarification` and `spec_conflict` should require formal upstream feedback to
Rupify.

## Boundaries

Speckify should not:

- replace Rupify as the source-of-truth model
- parse human-facing Markdown as the primary contract
- implement product code
- silently invent structure where the upstream model is incomplete
- create traceability for the first time inside GitHub issue prose

## Recommended Initial Delivery Phases

Phase 1:

- define input contract from Rupify
- define Speckify intermediate schema
- define decomposition and validation rules
- emit structured issue specs and verification specs

Phase 2:

- add dependency graphing and assembly maps
- add change classification for downstream updates
- emit formal upstream feedback artifacts for Rupify

Phase 3:

- introduce stronger bidirectional synchronization
- add model diffing and regeneration-aware reversibility workflows

## Open Design Questions

- what exact Rupify export should be the canonical Speckify input
- how granular issue-sized slices should be by default
- whether verification units should remain framework-agnostic or include test skeleton
  templates
- what minimum lineage data is required to support credible round-tripping
