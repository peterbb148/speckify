# Speckify Input Contract And Initial Schemas

## Purpose

This note defines the first formal contract between Rupify and Speckify and the initial
machine-readable schema surface Speckify should use internally.

This is the first implementation-planning artifact under issue `#2`. It is intended to
turn the high-level design note into a concrete, reviewable contract that can guide later
schema files and transformation logic.

## Scope

This note covers:

- the minimum upstream input contract Speckify expects from Rupify
- the first-pass schema shapes for core Speckify records
- required versus optional fields
- validation expectations and failure behavior
- one worked example showing how a small Rupify fragment maps into Speckify records

This note does not define:

- the full decomposition rule system
- the rendered GitHub issue output model
- bidirectional synchronization or automated round-tripping

## Contract Principles

Speckify should operate on structured, normalized source data rather than freeform text.

The contract should follow these rules:

- prefer canonical Rupify model data over rendered Markdown artifacts
- preserve stable identities and explicit lineage
- carry ambiguity and incompleteness forward honestly
- fail clearly when required source structure is missing
- keep schema boundaries explicit between upstream input, internal decomposition records,
  and downstream output artifacts

## Upstream Input Contract

Speckify should accept a single machine-readable Rupify planning bundle. That bundle can
be JSON or YAML, but the logical shape should be stable regardless of serialization.

### Root Structure

```yaml
project:
requirements: []
actors: []
use_cases: []
scenarios: []
domain_elements:
  entities: []
  relationships: []
  invariants: []
interaction_elements:
  participants: []
  messages: []
state_elements:
  states: []
  transitions: []
design_elements:
  components: []
  interfaces: []
traceability: []
provenance:
  assumptions: []
  open_questions: []
  ambiguities: []
readiness: {}
```

### Required Root Fields

- `project`
- `requirements`
- `use_cases`
- `traceability`
- `provenance`
- `readiness`

These are the minimum fields required for Speckify to make defensible planning decisions.

### Optional Root Fields

- `actors`
- `scenarios`
- `domain_elements`
- `interaction_elements`
- `state_elements`
- `design_elements`

These are optional at the root level because not every source model will contain every
view. When present, they must follow the same stability and traceability rules as the
required fields.

### Root Field Expectations

#### `project`

Required fields:

- `id`
- `name`
- `summary`

Optional fields:

- `scope`
- `business_goals`
- `success_criteria`
- `source_model_version`

#### `requirements`

Each requirement should expose:

- `id` required
- `text` required
- `kind` required
- `priority` optional
- `trace` optional but strongly preferred
- `normative` optional, defaults to `true` if omitted in initial planning

#### `use_cases`

Each use case should expose:

- `id` required
- `name` required
- `actor_ids` required
- `preconditions` optional
- `postconditions` optional
- `main_flow` required
- `alternate_flows` optional
- `exception_flows` optional
- `trace` optional but strongly preferred

Each main-flow step should expose:

- `id` required
- `text` required
- `normative` optional, defaults to `true`
- `trace` optional but strongly preferred

#### `traceability`

Each link should expose:

- `id` required
- `from_id` required
- `to_id` required
- `basis` required

Optional fields:

- `link_type`
- `confidence`

#### `provenance`

Required subfields:

- `assumptions`
- `open_questions`
- `ambiguities`

Structured ambiguity records are preferred over freeform prose.

#### `readiness`

Required behavior:

- must allow Speckify to distinguish ready, partial, and blocked source areas
- may be modeled at view level initially
- should evolve toward element-level readiness

## Failure Behavior

Speckify should not silently fabricate structure if required source fields are absent.

Validation outcomes should be classified as:

- `valid`: the input is sufficient for downstream planning
- `partial`: the input can support some planning output, but limitations must be surfaced
- `blocked`: the input is not sufficient for safe decomposition

Blocking examples:

- requirement without stable identifier
- use case without main flow
- traceability omitted entirely
- known ambiguity marked as blocking for downstream planning

Partial examples:

- no interaction view, but use cases and requirements are sufficiently specified
- no state model for a feature that does not appear state-heavy
- optional trace fields missing on some elements, but cross-view trace links still exist

## Initial Speckify Internal Schemas

The following records define the first-pass internal schema surface.

### SourceAnchor

Stable pointer to one upstream element or sub-element.

```yaml
id: anchor.use_case.uc_authenticate.step.capture_credentials
source_system: rupify
source_type: use_case_step
source_id: uc-authenticate.step-capture-credentials
parent_source_id: uc-authenticate
view: use_case
normative: true
ready_state: ready
trace:
  source_round: 4
  source_key: use_cases
```

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

Smallest semantically coherent obligation derived from one or more source anchors.

```yaml
id: su.authentication.capture_credentials
title: Capture credentials for authentication
summary: The system must accept user credentials as the first step of authentication.
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
obligation_kind: behavioral
normative: true
status: proposed
notes: []
```

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

Issue-sized work slice intended for one branch and one pull request.

```yaml
id: iu.authentication.capture_credentials
title: Add credential capture entrypoint
summary: Implement the entrypoint that accepts authentication credentials.
derived_from_spec_unit_ids:
  - su.authentication.capture_credentials
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
dependencies: []
implementation_scope:
  - accept username and password input
  - expose a callable interface for downstream authentication logic
non_goals:
  - credential validation against a user store
constraints:
  - preserve traceability to upstream use case step
acceptance_criteria:
  - system accepts a credential submission payload
verification_unit_ids:
  - vu.authentication.capture_credentials
```

Required fields:

- `id`
- `title`
- `summary`
- `derived_from_spec_unit_ids`
- `source_anchor_ids`
- `implementation_scope`
- `acceptance_criteria`

Optional fields:

- `dependencies`
- `non_goals`
- `constraints`
- `verification_unit_ids`

### VerificationUnit

Independent verification contract associated with one implementation unit.

```yaml
id: vu.authentication.capture_credentials
implementation_unit_id: iu.authentication.capture_credentials
title: Verify credential capture behavior
verification_intent: Confirm that the system accepts authentication credentials.
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
observables:
  - credential payload is accepted by the entrypoint
setup_requirements:
  - authentication entrypoint is available
expected_outcomes:
  - valid payload reaches the boundary defined by the implementation unit
failure_conditions:
  - payload is rejected before validation logic is invoked
invariants_preserved: []
```

Required fields:

- `id`
- `implementation_unit_id`
- `title`
- `verification_intent`
- `source_anchor_ids`
- `observables`
- `expected_outcomes`

Optional fields:

- `setup_requirements`
- `failure_conditions`
- `invariants_preserved`

### TraceBundle

Lineage record connecting source anchors to the derived planning artifacts.

```yaml
id: tb.authentication.capture_credentials
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
spec_unit_ids:
  - su.authentication.capture_credentials
implementation_unit_ids:
  - iu.authentication.capture_credentials
verification_unit_ids:
  - vu.authentication.capture_credentials
assembly_rule_ids: []
```

Required fields:

- `id`
- `source_anchor_ids`
- `spec_unit_ids`
- `implementation_unit_ids`
- `verification_unit_ids`

Optional fields:

- `assembly_rule_ids`

## Schema Boundaries

The key boundary rules are:

- Rupify input records describe the source specification
- `SourceAnchor` records point into that source specification
- `SpecUnit` records describe decomposed obligations
- `ImplementationUnit` records describe issue-sized work
- `VerificationUnit` records describe independent verification intent
- `TraceBundle` records carry lineage across those layers

Speckify should not skip directly from Rupify input records to rendered GitHub issue text.

## Worked Example

This example shows a small Rupify-style fragment and the corresponding Speckify records.

### Example Source Fragment

```yaml
requirements:
  - id: req-auth-001
    text: The system shall authenticate registered users.
    kind: functional

use_cases:
  - id: uc-authenticate
    name: Authenticate user
    actor_ids:
      - actor-user
    main_flow:
      - id: step-capture-credentials
        text: User submits username and password.
      - id: step-verify-credentials
        text: System verifies the submitted credentials.

traceability:
  - id: trace-req-auth-use-case
    from_id: req-auth-001
    to_id: uc-authenticate
    basis: requirement realized by use case

readiness:
  use_case: ready
  interaction: partial
  state: partial
```

### Derived SourceAnchor Records

```yaml
- id: anchor.requirement.req-auth-001
  source_system: rupify
  source_type: requirement
  source_id: req-auth-001
  view: requirements

- id: anchor.use_case.uc_authenticate.step.capture_credentials
  source_system: rupify
  source_type: use_case_step
  source_id: uc-authenticate.step-capture-credentials
  parent_source_id: uc-authenticate
  view: use_case
```

### Derived Speckify Records

```yaml
spec_units:
  - id: su.authentication.capture_credentials
    title: Capture credentials for authentication
    summary: The system must accept user credentials as part of authentication.
    source_anchor_ids:
      - anchor.requirement.req-auth-001
      - anchor.use_case.uc_authenticate.step.capture_credentials
    obligation_kind: behavioral

implementation_units:
  - id: iu.authentication.capture_credentials
    title: Add credential capture entrypoint
    summary: Implement the credential capture boundary used in authentication.
    derived_from_spec_unit_ids:
      - su.authentication.capture_credentials
    source_anchor_ids:
      - anchor.use_case.uc_authenticate.step.capture_credentials
    implementation_scope:
      - accept username and password input
    acceptance_criteria:
      - a credential submission can be accepted by the authentication boundary

verification_units:
  - id: vu.authentication.capture_credentials
    implementation_unit_id: iu.authentication.capture_credentials
    title: Verify credential capture behavior
    verification_intent: Confirm that credentials can be submitted to the authentication boundary.
    source_anchor_ids:
      - anchor.use_case.uc_authenticate.step.capture_credentials
    observables:
      - credential payload is accepted
    expected_outcomes:
      - credential submission reaches the authentication boundary
```

## Current Open Questions

- should `normative` remain optional in the first contract, or should Rupify be expected
  to mark it explicitly
- should Speckify require element-level readiness before any automated decomposition
- should `TraceBundle` remain a standalone record or be embedded into each derived unit
- how much of the Rupify source model should be copied into the Speckify planning bundle
  versus referenced by stable identifier only
