# Rupify Downstream Planning Contract

## Purpose

This note defines the concrete contract Speckify needs from Rupify in order to perform
formal decomposition, preserve traceability, and support reversibility without inventing
missing semantics.

It turns the higher-level upstream recommendations into a more explicit planning
contract, with priority levels and a proposed export shape that can later be discussed or
implemented upstream.

This note is the main artifact for issue `#4`.

## Contract Goal

Rupify should remain the source-of-truth specification system. Speckify should consume a
stable, machine-readable downstream planning export rather than mining meaning from
rendered Markdown.

The goal of the contract is:

- stable identity across regeneration
- sufficient traceability for decomposition
- enough semantic structure to define verification intent
- explicit ambiguity and readiness signaling
- a clean boundary between upstream specification and downstream planning

## Boundary Between Repositories

### Rupify Owns

- stakeholder elicitation
- normalization into the canonical project model
- generation of formal specification artifacts
- view-level and element-level traceability in the source model
- readiness and ambiguity reporting for source elements
- export of the machine-readable planning bundle consumed by Speckify

### Speckify Owns

- transformation of source elements into planning-oriented units
- issue-sized slicing
- verification-shape derivation
- downstream trace bundles linking source, planning, and verification records
- feedback proposals when downstream work reveals source-spec clarification or conflict

### Speckify Must Not Own

- direct authorship of the Rupify source model
- reconstruction of missing source semantics through heuristics
- primary interpretation of human-facing Markdown as the source contract

## Contract Priority Levels

The contract surface should be split into three priority tiers.

### Tier 1: Required For First Credible Integration

- stable semantic identifiers
- source element type classification
- minimal cross-view trace links
- structured ambiguity records
- readiness state for downstream-safe planning
- downstream planning export with a stable schema

Without Tier 1, Speckify would be forced into guesswork.

### Tier 2: Strongly Recommended For High-Quality Decomposition

- step-level identifiers for use case and scenario flows
- first-class invariants and constraints
- richer requirement-to-view links
- explicit normative versus informative markings
- element-level readiness

Tier 2 materially improves issue sizing and verification shaping.

### Tier 3: Needed For Strong Reversibility

- model and element version metadata
- semantic hashes or equivalent change identity
- supersession and regeneration lineage
- formal round-trip feedback artifact support

Tier 3 is what moves the system from traceable to genuinely reversible.

## Required Upstream Elements

This section describes the minimum records Speckify should be able to rely on in the
Rupify downstream planning export.

### 1. Stable Semantic IDs

Every meaningful source element should have a durable identifier that remains stable
across regeneration when its semantics are unchanged.

Required surfaces:

- project
- requirement
- actor
- use case
- use case step
- scenario
- scenario step
- domain entity
- relationship
- invariant
- interaction participant
- interaction message
- state
- transition
- component
- interface
- ambiguity

Required fields:

- `id`
- `element_type`

Recommended optional fields:

- `parent_id`
- `display_name`
- `semantic_hash`

### 2. Source Element Classification

Each exportable source element should include a stable classification.

Required fields:

- `element_type`
- `view`

Allowed examples:

- `requirement`
- `use_case`
- `use_case_step`
- `scenario_step`
- `domain_entity`
- `invariant`
- `interaction_message`
- `state_transition`

This gives Speckify enough structure to apply view-aware decomposition later.

### 3. Trace Links

Rupify should emit cross-view trace links directly rather than forcing downstream tools
to infer them.

Required fields:

- `id`
- `from_id`
- `to_id`
- `link_type`
- `basis`

High-value examples:

- requirement -> use case
- requirement -> use case step
- use case step -> scenario step
- use case step -> interaction message
- use case step -> state transition
- domain invariant -> state guard
- requirement -> non-functional constraint -> component

### 4. Ambiguity Records

Rupify should export ambiguity as structured data.

Required fields:

- `id`
- `description`
- `applies_to_element_ids`
- `blocking_for_downstream`
- `resolution_status`

Recommended optional fields:

- `ambiguity_type`
- `source_round`
- `notes`

### 5. Readiness State

Rupify should export readiness explicitly so Speckify can stop honestly when the source
model is not ready for decomposition.

Required fields:

- `target_id`
- `readiness_state`

Allowed values:

- `ready`
- `partial`
- `blocked`

Recommended optional fields:

- `reason`
- `blocking_ambiguity_ids`

### 6. Constraints And Invariants

Rupify should export constraints as first-class records.

Required fields:

- `id`
- `constraint_type`
- `text`

Recommended optional fields:

- `applies_to_element_ids`
- `normative`
- `trace`

High-value constraint types:

- `precondition`
- `postcondition`
- `domain_invariant`
- `state_invariant`
- `guard_condition`
- `non_functional_constraint`

## Proposed Downstream Planning Export

The downstream planning export should be machine-oriented and narrower than the full
canonical Rupify model.

### Root Shape

```yaml
export_metadata:
project:
elements: []
trace_links: []
ambiguities: []
readiness: []
constraints: []
```

### `export_metadata`

Required fields:

- `export_version`
- `source_model_id`
- `source_model_version`
- `generated_at`

Recommended optional fields:

- `source_commit`
- `schema_version`

### `project`

Required fields:

- `id`
- `name`
- `summary`

Recommended optional fields:

- `scope`
- `business_goals`
- `success_criteria`

### `elements`

Each element in the export should follow one normalized shape.

```yaml
id: uc-authenticate.step-capture-credentials
element_type: use_case_step
view: use_case
parent_id: uc-authenticate
display_name: Capture credentials
text: User submits username and password.
normative: true
semantic_hash: abc123
trace:
  source_round: 4
  source_key: use_cases
```

Required fields:

- `id`
- `element_type`
- `view`

Recommended optional fields:

- `parent_id`
- `display_name`
- `text`
- `normative`
- `semantic_hash`
- `trace`

### `trace_links`

```yaml
id: trace-req-auth-step-capture
from_id: req-auth-001
to_id: uc-authenticate.step-capture-credentials
link_type: realizes
basis: requirement realized by use case step
```

### `ambiguities`

```yaml
id: amb-auth-credentials-format
description: Credential format constraints are not yet specified.
applies_to_element_ids:
  - uc-authenticate.step-capture-credentials
blocking_for_downstream: false
resolution_status: open
```

### `readiness`

```yaml
- target_id: uc-authenticate
  readiness_state: ready

- target_id: interaction-authenticate
  readiness_state: partial
  reason: interaction sequence is incomplete
```

### `constraints`

```yaml
- id: pre-auth-001
  constraint_type: precondition
  text: User must provide credentials before verification can begin.
  applies_to_element_ids:
    - uc-authenticate.step-verify-credentials
  normative: true
```

## Minimum Contract For Speckify V1

For a first credible Speckify integration, the export must provide:

- stable IDs for requirements, use cases, and use case steps
- trace links from requirements to use cases or use case steps
- ambiguity records
- readiness state
- first-class constraints where they already exist

If those fields are missing, Speckify should classify the source as `blocked` or
explicitly `partial`.

## Validation Expectations

Speckify should validate the Rupify downstream planning export before decomposition.

Validation failures should include:

- missing `export_metadata`
- missing stable identifiers on required elements
- trace links pointing to unknown element IDs
- readiness entries pointing to unknown elements
- ambiguity records without affected element references

Validation outcomes:

- `valid`
- `partial`
- `blocked`

## Example Contract Fragment

```yaml
export_metadata:
  export_version: 1
  source_model_id: project-speckify-auth
  source_model_version: 3
  generated_at: 2026-04-20T08:00:00Z

project:
  id: project-speckify-auth
  name: Authentication service
  summary: Authenticate registered users.

elements:
  - id: req-auth-001
    element_type: requirement
    view: requirements
    text: The system shall authenticate registered users.
    normative: true

  - id: uc-authenticate
    element_type: use_case
    view: use_case
    display_name: Authenticate user

  - id: uc-authenticate.step-capture-credentials
    element_type: use_case_step
    view: use_case
    parent_id: uc-authenticate
    display_name: Capture credentials
    text: User submits username and password.
    normative: true

trace_links:
  - id: trace-req-auth-use-case
    from_id: req-auth-001
    to_id: uc-authenticate
    link_type: realizes
    basis: requirement realized by use case

ambiguities:
  - id: amb-auth-format
    description: Accepted credential format is not specified.
    applies_to_element_ids:
      - uc-authenticate.step-capture-credentials
    blocking_for_downstream: false
    resolution_status: open

readiness:
  - target_id: uc-authenticate
    readiness_state: ready

constraints:
  - id: pre-auth-001
    constraint_type: precondition
    text: Credentials must be submitted before verification can begin.
    applies_to_element_ids:
      - uc-authenticate.step-capture-credentials
    normative: true
```

## Recommended Upstream Sequence

If Rupify were to implement this contract incrementally, the best sequence is:

1. add stable IDs across all meaningful elements
2. emit a planning-focused export with normalized elements and trace links
3. add structured ambiguity and readiness records
4. lift invariants and constraints into first-class records
5. add semantic hashes and regeneration metadata
6. add formal round-trip feedback support

## Open Questions

- should the planning export be a filtered projection of the canonical model or a distinct
  derived artifact
- should Speckify require `normative` markings from Rupify or apply a temporary default
  when omitted
- how much element text should be copied into the export versus referenced indirectly
- whether `elements` should remain one normalized array or be grouped by view in the
  final export schema
