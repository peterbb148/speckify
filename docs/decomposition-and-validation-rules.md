# Speckify Decomposition And Validation Rules

## Purpose

This note defines how Speckify should decompose structured Rupify source data into
planning-oriented records and how it should validate the resulting units before any
downstream issue rendering or implementation workflow begins.

This is the main artifact for issue `#6`.

## Scope

This note covers:

- decomposition rules by source view type
- how one-to-many and many-to-one mappings should be represented
- blocking and partial conditions when source material is incomplete
- validation rules for `SpecUnit`, `ImplementationUnit`, and `VerificationUnit`
- worked examples showing how source fragments become traceable planning units

This note does not cover:

- the final issue rendering model
- the reversibility feedback artifact format
- execution-time transformation code

## Rule System Goals

The decomposition rules should enforce five properties:

- traceability back to source anchors
- semantic coherence of each derived unit
- issue-sized implementation slices
- independent verification intent
- honest handling of ambiguity, incompleteness, and cross-view gaps

Speckify should prefer not to decompose a source fragment rather than silently create a
misleading planning unit from incomplete semantics.

## Constitutional Constraint

Decomposition operators must be defined over explicit source structure, not over source
phrasing.

Rules:

- conjunction decomposition is only valid when the upstream export carries explicit
  structured sub-obligations such as `obligations`, `semantic_parts`, or equivalent
  normalized fields
- wording alone, including conjunction words, punctuation, or sentence shape, is not
  sufficient evidence for a split
- if the source export does not provide explicit sub-obligation structure, Speckify must
  fail closed and keep the source element intact
- every formal split must emit an assembly rule that describes how the derived units
  recompose into the original source element

## Decomposition Pipeline

Speckify should apply decomposition in four ordered stages.

### Stage 1: Source Anchoring

Map the upstream planning export into `SourceAnchor` records.

Rules:

- every decomposable source element must first have a stable anchor
- sub-elements such as use case steps and state transitions should receive their own
  anchors
- readiness and ambiguity should remain attached to the anchored source material

### Stage 2: SpecUnit Derivation

Derive the smallest semantically coherent obligations from the anchored source material.

Rules:

- each `SpecUnit` must express one obligation or one tightly coupled obligation set
- a `SpecUnit` may be sourced from one anchor or multiple anchors
- if a source fragment cannot be stated as a concrete obligation, it should not become a
  `SpecUnit`

### Stage 3: ImplementationUnit Slicing

Split `SpecUnit` records into issue-sized implementation slices.

Rules:

- each `ImplementationUnit` must be small enough for one branch and one pull request
- an `ImplementationUnit` may combine multiple `SpecUnit` records when they are too
  tightly coupled to implement separately
- a `SpecUnit` may split into several `ImplementationUnit` records when its realization
  crosses meaningful boundaries

### Stage 4: VerificationUnit Derivation

Define independent verification intent for each `ImplementationUnit`.

Rules:

- each `ImplementationUnit` should map to at least one `VerificationUnit`
- a `VerificationUnit` should describe observable proof, not implementation detail
- verification should be shaped by source semantics and constraints, not by the
  implementation author's convenience

## Mapping Patterns

Speckify should support three explicit mapping patterns.

### One Source To One Planning Unit

Used when one source element is already atomic and implementation-sized.

Example:

- one use case step maps to one `SpecUnit`, one `ImplementationUnit`, and one
  `VerificationUnit`

### One Source To Many Planning Units

Used when one source element contains several independently implementable obligations.

Example:

- one use case step describes validation, persistence, and notification
- Speckify splits those into multiple `ImplementationUnit` records while preserving a
  shared source anchor

### Many Sources To One Planning Unit

Used when several source elements together describe one inseparable obligation.

Example:

- one requirement, one use case step, and one invariant jointly define a single planning
  obligation that should remain one `ImplementationUnit`

## View-Specific Decomposition Rules

### Requirements View

Requirements should be decomposed by independently testable obligation.

Rules:

- split composite requirements into separate `SpecUnit` records when they contain
  multiple independent behavioral or constraint obligations
- keep cross-cutting non-functional constraints as standalone `SpecUnit` records unless
  they are inseparable from one specific behavior
- do not derive implementation slices from vague or aspirational requirement language

Typical outputs:

- obligation-focused `SpecUnit` records
- trace links to supporting use cases or constraints

### Use Case View

Use cases are one of the most valuable decomposition inputs.

Rules:

- derive a candidate `SpecUnit` from each main-flow step when the step expresses a
  concrete system obligation
- derive separate candidate `SpecUnit` records for alternate flows and exception flows
  when they create independently meaningful behavior
- treat preconditions and postconditions as constraints unless they themselves define an
  implementation slice
- split by actor-to-system responsibility boundary when a step mixes user action and
  system action

Blocking conditions:

- use case has no stable ID
- use case has no main flow
- step text is too vague to express a concrete obligation

### Scenario View

Scenarios should refine use case behavior into more concrete, traceable flow slices.

Rules:

- derive `SpecUnit` records from scenario steps only when the scenario adds operational
  specificity beyond the use case
- do not duplicate a use case step and a scenario step into separate units when the
  scenario merely restates the same obligation
- scenario-level decomposition should enrich or refine, not create parallel drift

High-value use:

- alternative operational paths
- conditional branches
- integration touchpoints

### Domain View

Domain elements should decompose around responsibility and invariants.

Rules:

- derive `SpecUnit` records from entity lifecycle obligations
- derive separate `SpecUnit` records for domain invariants when they constrain behavior
  independently
- derive relationship-maintenance obligations only when they imply implementation
  behavior, not merely documentation structure

Examples:

- maintain uniqueness of an identifier
- preserve relationship integrity when a child object is deleted

### Interaction View

Interaction elements should decompose around externally meaningful coordination behavior.

Rules:

- derive `SpecUnit` records from observable message obligations
- group tightly coupled request/response exchanges into one `SpecUnit` when splitting
  them would destroy the interaction contract
- split at integration boundary crossings when separate implementation slices are likely

Examples:

- submit command to external system
- handle callback response
- publish domain event after state transition

### State View

State models are best decomposed around transitions and guards.

Rules:

- derive `SpecUnit` records from transitions that represent distinct business behavior
- derive separate `SpecUnit` records for guard conditions when they impose independent
  acceptance constraints
- treat invalid transitions and terminal transitions as explicit obligations when they
  affect observable behavior

Examples:

- reject approval from invalid state
- permit transition only when required documents exist

### Constraint And Invariant View

Constraints should remain visible rather than being buried inside feature slices.

Rules:

- derive standalone `SpecUnit` records for constraints that apply across many behaviors
- embed a constraint into an `ImplementationUnit` only when it is local to that unit
- preserve source linkage to the originating invariant, precondition, postcondition, or
  non-functional constraint

## Slicing Rules For ImplementationUnits

Once `SpecUnit` records exist, Speckify should create issue-sized slices using these
rules.

### Split A SpecUnit When

- the source obligation crosses different technical boundaries
- the work cannot be completed credibly in one focused pull request
- different parts of the obligation can be verified independently
- the obligation mixes behavior and infrastructure concerns that should be reviewed
  separately

### Keep A SpecUnit Together When

- splitting would destroy semantic coherence
- the same acceptance proof applies to the whole obligation
- the same invariant or guard governs the full behavior
- separate implementation would create artificial sequencing or trace drift

### Merge Multiple SpecUnits When

- they are inseparable for implementation
- they describe one tightly coupled behavior from multiple views
- separate issues would only create noise without adding independent verification value

## Blocking And Partial Conditions

Decomposition should produce one of three outcomes for each candidate source area.

### `ready`

The source material is concrete enough for defensible decomposition.

### `partial`

Some planning output is possible, but the result must carry explicit limitations.

Examples:

- use case exists, but supporting interaction view is incomplete
- requirement and main flow are clear, but constraints are underspecified
- some trace links are present, but not all desired cross-view links exist

### `blocked`

Decomposition should not proceed for that source area.

Examples:

- no stable source identifier
- no concrete obligation can be stated
- ambiguity is marked as blocking for downstream planning
- readiness is explicitly `blocked`

## Validation Rules

### Valid SpecUnit

A `SpecUnit` is valid only if:

- it has at least one source anchor
- it can be stated as a concrete obligation
- it is semantically coherent
- it does not hide unresolved blocking ambiguity

### Valid ImplementationUnit

An `ImplementationUnit` is valid only if:

- it maps to at least one `SpecUnit`
- it is independently implementable
- it is narrow enough for one controlled pull request
- it has explicit implementation scope
- it has explicit acceptance criteria
- it preserves source traceability

### Valid VerificationUnit

A `VerificationUnit` is valid only if:

- it maps to one `ImplementationUnit`
- it states observable proof of correctness
- it is independent from implementation detail
- it includes expected outcomes
- it preserves source traceability

## Independent Implementability Test

Speckify should treat an `ImplementationUnit` as independently implementable only if the
answer is yes to all of the following:

- can one developer or one coding thread complete it in one focused branch
- can the scope be described without relying on hidden future work
- can reviewers judge completion from its acceptance criteria
- can the unit land without needing a multi-PR orchestration plan

If not, the unit is too broad or incorrectly sliced.

## Independent Verifiability Test

Speckify should treat a unit as independently verifiable only if:

- the expected observable outcome can be stated clearly
- the success condition does not require unrelated units to be complete
- failure can be explained without reference to hidden assumptions
- relevant invariants or constraints are explicit

If not, verification intent is underspecified.

## Worked Example: Use Case Step Split

### Source Fragment

```yaml
use_cases:
  - id: uc-register-user
    name: Register user
    main_flow:
      - id: step-submit-registration
        text: System validates registration data, creates the user record, and sends a welcome email.
```

### Derived SpecUnits

```yaml
- id: su.registration.validate_input
  title: Validate registration data
  source_anchor_ids:
    - anchor.use_case.uc_register_user.step.submit_registration
  obligation_kind: behavioral

- id: su.registration.create_user_record
  title: Create user record
  source_anchor_ids:
    - anchor.use_case.uc_register_user.step.submit_registration
  obligation_kind: behavioral

- id: su.registration.send_welcome_email
  title: Send welcome email after registration
  source_anchor_ids:
    - anchor.use_case.uc_register_user.step.submit_registration
  obligation_kind: behavioral
```

Reason:

- the original step contains three separable obligations
- each obligation can be implemented and verified independently
- shared source lineage is preserved through the common source anchor

## Worked Example: Many Sources To One Unit

### Source Fragment

```yaml
requirements:
  - id: req-order-approval
    text: Orders above the threshold must be approved.

state_elements:
  transitions:
    - id: transition-order-pending-to-approved
      from_state: pending
      to_state: approved

constraints:
  - id: guard-order-threshold
    constraint_type: guard_condition
    text: Approval is required when order amount exceeds threshold.
```

### Derived Planning Units

```yaml
spec_units:
  - id: su.order.approval_threshold
    title: Enforce approval threshold before approval transition
    source_anchor_ids:
      - anchor.requirement.req_order_approval
      - anchor.state.transition_order_pending_to_approved
      - anchor.constraint.guard_order_threshold
    obligation_kind: behavioral

implementation_units:
  - id: iu.order.approval_threshold
    title: Enforce threshold guard on order approval
    derived_from_spec_unit_ids:
      - su.order.approval_threshold
    source_anchor_ids:
      - anchor.requirement.req_order_approval
      - anchor.state.transition_order_pending_to_approved
      - anchor.constraint.guard_order_threshold
    implementation_scope:
      - reject approval transition when threshold rule is not satisfied
    acceptance_criteria:
      - pending orders above threshold cannot transition to approved without approval
```

Reason:

- the requirement, state transition, and guard are one inseparable obligation
- splitting them would create trace noise rather than better planning

## Recommended Future Extension

Once output artifact definitions are finalized, these rules should be tightened into:

- a machine-readable decomposition rule catalog
- validation checks against the Speckify schemas
- example fixtures derived from real Rupify exports

## Open Questions

- should decomposition rules prefer requirement-first slicing or use-case-first slicing
  when both are present
- when should scenario detail override use case abstraction
- how should Speckify represent decomposition decisions explicitly so later reversibility
  work can reuse them
