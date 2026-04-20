# Rupify Upstream Note For Speckify

## Purpose

This note captures the Rupify changes that would most improve Speckify's ability to
perform formal decomposition, preserve traceability, and support reversibility.

The goal is not to move Speckify into Rupify. The goal is to strengthen Rupify's output
contract so a downstream planning layer can operate with minimal ambiguity and minimal
loss of semantics.

## Recommended Enhancements

### 1. Stable Semantic IDs Everywhere

Every meaningful model element should have a durable identifier that remains stable across
regeneration whenever the semantics remain the same.

Priority surfaces:

- requirements
- use cases
- scenario steps
- actors
- domain entities
- relationships
- business rules
- interaction messages
- states
- transitions
- guards and triggers
- design components and interfaces

This is the strongest enabler for reversibility and downstream diffing.

### 2. First-Class Step-Level And Rule-Level Trace

Rupify already carries trace metadata, but Speckify benefits from a more granular and
more explicit lineage model.

Recommended additions:

- use case step identifiers
- alternate-flow identifiers
- exception-flow identifiers
- invariant identifiers
- guard identifiers
- transition-to-requirement links
- scenario-step-to-interaction links
- scenario-step-to-state-transition links

This reduces guesswork during decomposition and downstream verification shaping.

### 3. Explicit Normative Versus Informative Content

Rupify should distinguish between content that is binding for implementation and content
that is explanatory for humans.

Suggested split:

- normative: obligations, constraints, required behavior, invariants
- informative: commentary, rationale, examples, explanatory notes

Speckify should only decompose normative content into implementation obligations.

### 4. Stronger Invariant And Constraint Modeling

Rupify should elevate constraints into first-class structured records rather than leaving
them embedded in prose.

Especially valuable:

- domain invariants
- state invariants
- preconditions
- postconditions
- guard conditions
- forbidden transitions
- invalid states
- non-functional acceptance constraints

These are ideal raw materials for downstream verification units.

### 5. Element-Level Readiness

View-level readiness is useful, but downstream planning needs finer granularity.

Recommended capability:

- this use case is ready
- this scenario step is partial
- this invariant is uncertain
- this transition is blocked by ambiguity

Speckify should be able to decompose only what is defensible.

### 6. Structured Ambiguity Objects

Open questions should be available as structured records rather than prose-only lists.

Suggested fields:

- `id`
- `applies_to_element_ids`
- `ambiguity_type`
- `description`
- `blocking_for_downstream`
- `resolution_status`

This allows downstream tooling to stop honestly where ambiguity is still material.

### 7. Richer Cross-View Consistency Links

Rupify should strengthen explicit links between views.

High-value examples:

- requirement -> use case step
- use case step -> interaction message
- use case step -> state transition
- domain invariant -> guard condition
- requirement -> non-functional constraint -> affected design element

This is the raw material for formal decomposition and reverse assembly.

### 8. Change And Regeneration Metadata

Rupify should emit metadata that improves comparison between model versions.

Suggested fields:

- model version
- element version or semantic hash
- last changed timestamp
- change source
- regenerated-from version
- supersedes links

This would materially improve downstream diffing and upstream reconciliation.

### 9. Dedicated Downstream Planning Export

Rupify should consider a machine-oriented export tailored for downstream planning.

Desired traits:

- complete and ready elements only, or explicit partial markers
- flattened stable identifiers
- normalized trace links
- surfaced invariants and constraints
- surfaced ambiguities and readiness markers
- strict schema for downstream consumption

This would become the clean contract between Rupify and Speckify.

### 10. Formal Round-Trip Feedback Format

Rupify should define a structured feedback artifact that downstream tools can emit when
implementation uncovers a source-model issue.

Suggested feedback categories:

- clarify element
- split element
- merge elements
- revise invariant
- revise transition
- add missing requirement
- contradiction detected downstream

This would make reversibility operational instead of aspirational.

## Suggested Near-Term Priorities

If only a few changes are made first, the highest-value sequence is:

1. stable semantic IDs across all meaningful elements
2. stronger trace links at step, transition, and invariant level
3. explicit invariants, constraints, and ambiguities as structured objects
4. dedicated downstream planning export

## Proposed Contract Between Repositories

Recommended split of responsibilities:

- Rupify owns elicitation, normalization, canonical modeling, artifact rendering, and
  upstream traceability
- Speckify owns decomposition, issue sizing, verification shaping, and downstream trace
  bundles
- Speckify emits structured feedback proposals to Rupify instead of rewriting the Rupify
  model directly in the first iteration

This keeps both systems modular while still supporting a credible path toward
reversibility.
