# Speckify Reversibility And Upstream Feedback Flow

## Purpose

This note defines how Speckify should preserve enough lineage to support reversibility,
how it should classify downstream changes, and how it should emit structured feedback
upstream when downstream work reveals a source-spec clarification or conflict.

This is the main artifact for issue `#7`.

## Scope

This note covers:

- the reversibility model for Speckify planning artifacts
- change classification for downstream work
- the minimum lineage required for credible round-trip traceability
- the structure of upstream feedback artifacts
- the flow from downstream change detection to upstream feedback proposal

This note does not cover:

- automatic modification of Rupify source models
- bidirectional synchronization implementation
- merge or conflict resolution algorithms

## Reversibility Goal

Speckify does not need to make the entire system fully self-healing in the first
iteration. It does need to preserve enough structured lineage that downstream work can be
classified honestly and source-affecting changes can be surfaced upstream in a structured
way.

The practical goal is:

- identify what source semantics a downstream change touches
- determine whether the change conforms to the current source model
- identify whether the change implies a source clarification or source conflict
- emit a structured upstream feedback proposal when required

## Reversibility Principles

The reversibility model should follow these rules:

- every planning artifact must retain explicit source lineage
- every decomposition decision must be attributable
- every downstream change must resolve to one or more planning units
- changes that affect source semantics must not be absorbed silently
- feedback to Rupify should be structured, not prose-only

## Minimum Lineage Required

Speckify should preserve the following lineage across all major artifacts.

### For Every SpecUnit

Required lineage:

- `source_anchor_ids`
- decomposition rationale or rule reference

### For Every ImplementationUnit

Required lineage:

- `derived_from_spec_unit_ids`
- `source_anchor_ids`
- dependency references where relevant

### For Every VerificationUnit

Required lineage:

- `implementation_unit_id`
- `source_anchor_ids`

### For Every Downstream Change Record

Required lineage:

- `affected_implementation_unit_ids`
- `affected_verification_unit_ids` when relevant
- `source_anchor_ids`
- `trace_bundle_ids`

Without that lineage, Speckify cannot make credible claims about reversibility.

## Downstream Change Classes

Speckify should classify downstream changes into four explicit classes.

### 1. `implementation_conforming`

Meaning:

- the downstream change implements the planning unit without changing source semantics

Examples:

- code added to satisfy a defined implementation scope
- tests added that match the planned verification shape
- internal refactors that do not affect source-observable behavior

Upstream effect:

- no source feedback required

### 2. `verification_refinement`

Meaning:

- downstream work strengthens or clarifies the shape of verification without changing the
  underlying source obligation

Examples:

- turning one expected outcome into two more explicit checks
- adding a missing negative test derived from an already stated invariant

Upstream effect:

- usually no source feedback required
- may produce optional documentation feedback if the refinement reveals a useful source
  clarification

### 3. `spec_clarification`

Meaning:

- downstream work uncovers missing or ambiguous source semantics that need upstream
  clarification, but not necessarily contradiction

Examples:

- a required constraint was implied but never stated
- the use case is clear, but the valid input range is underspecified
- a state transition needs an explicit guard that was missing upstream

Upstream effect:

- structured feedback proposal should be emitted to Rupify

### 4. `spec_conflict`

Meaning:

- downstream work reveals that the current source semantics are inconsistent,
  incomplete in a blocking way, or contradicted by another source element

Examples:

- requirement says a transition is allowed while state model forbids it
- use case and invariant cannot both be true as currently written
- implementation cannot satisfy all linked source anchors simultaneously

Upstream effect:

- structured feedback proposal is required
- downstream implementation should not quietly redefine the source semantics

## Change Classification Rules

Speckify should classify a change as `implementation_conforming` only if:

- it fits within the existing `ImplementationUnit` scope
- it satisfies existing acceptance criteria
- it does not introduce new source-affecting constraints
- it does not contradict linked source anchors

Speckify should classify a change as `verification_refinement` only if:

- it changes the verification shape without changing the source obligation
- all added checks can be derived from existing source semantics or planning constraints

Speckify should classify a change as `spec_clarification` when:

- downstream work needs source detail that is currently ambiguous or absent
- the change extends source semantics rather than contradicting them

Speckify should classify a change as `spec_conflict` when:

- the source semantics are contradictory
- implementation cannot proceed without choosing between incompatible source statements
- the downstream change would alter source meaning if accepted

## Change Record Shape

Speckify should represent downstream changes as structured records before any upstream
feedback is generated.

```yaml
id: change.authentication.capture_credentials.001
change_class: spec_clarification
summary: Credential format constraints need explicit upstream definition.
affected_implementation_unit_ids:
  - iu.authentication.capture_credentials
affected_verification_unit_ids:
  - vu.authentication.capture_credentials
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
trace_bundle_ids:
  - tb.authentication.capture_credentials
evidence:
  - verification design requires a valid input boundary that is not stated upstream
recommended_action: clarify input format constraints in Rupify source model
status: proposed
```

Required fields:

- `id`
- `change_class`
- `summary`
- `affected_implementation_unit_ids`
- `source_anchor_ids`
- `trace_bundle_ids`
- `recommended_action`
- `status`

Recommended optional fields:

- `affected_verification_unit_ids`
- `evidence`
- `notes`

## Upstream Feedback Artifact

When a change is classified as `spec_clarification` or `spec_conflict`, Speckify should
emit a structured feedback artifact for Rupify.

### Feedback Categories

Recommended categories:

- `clarify_element`
- `split_element`
- `merge_elements`
- `revise_invariant`
- `revise_transition`
- `add_missing_requirement`
- `resolve_conflict`

### Feedback Record Shape

```yaml
id: feedback.authentication.capture_credentials.001
feedback_type: clarify_element
change_record_id: change.authentication.capture_credentials.001
summary: Define the accepted credential format for authentication input.
target_source_ids:
  - uc-authenticate.step-capture-credentials
source_anchor_ids:
  - anchor.use_case.uc_authenticate.step.capture_credentials
reason: Verification intent requires explicit input constraints that are absent upstream.
proposed_upstream_action:
  - add a constraint record describing accepted credential format
  - link the constraint to the authentication use case step
impact:
  affected_spec_unit_ids:
    - su.authentication.capture_credentials
  affected_implementation_unit_ids:
    - iu.authentication.capture_credentials
  affected_verification_unit_ids:
    - vu.authentication.capture_credentials
status: proposed
```

Required fields:

- `id`
- `feedback_type`
- `change_record_id`
- `summary`
- `target_source_ids`
- `source_anchor_ids`
- `reason`
- `proposed_upstream_action`
- `status`

Recommended optional fields:

- `impact`
- `notes`

## Upstream Feedback Flow

Speckify should follow this flow when downstream work reveals source-affecting issues.

### Step 1: Detect

Identify the downstream change or planning gap.

Inputs:

- implementation notes
- verification design gaps
- contradiction detected between linked source anchors

### Step 2: Resolve Lineage

Map the affected work back to:

- `ImplementationUnit`
- `VerificationUnit`
- `TraceBundle`
- `SourceAnchor`

If lineage cannot be resolved, the change should be marked as insufficiently traceable.

### Step 3: Classify

Assign one of the defined change classes:

- `implementation_conforming`
- `verification_refinement`
- `spec_clarification`
- `spec_conflict`

### Step 4: Generate Change Record

Create a structured change record with evidence and recommended action.

### Step 5: Emit Upstream Feedback

If the change class is `spec_clarification` or `spec_conflict`, generate a structured
feedback artifact targeted at Rupify.

### Step 6: Preserve Status

Track whether the feedback is:

- `proposed`
- `sent_upstream`
- `accepted`
- `rejected`
- `superseded`

## Bundle-Level Reversibility Outputs

Speckify should eventually include these bundle-level outputs in addition to the planning
bundle itself.

### Change Records

List of structured downstream changes discovered during implementation or verification
planning.

### Feedback Proposals

List of structured upstream feedback artifacts derived from source-affecting changes.

### Round-Trip Status Summary

Suggested shape:

```yaml
round_trip_status:
  change_record_count: 3
  feedback_proposal_count: 2
  open_spec_clarifications: 1
  open_spec_conflicts: 1
```

## Worked Example: Clarification

### Situation

- the source use case defines credential submission
- verification planning requires explicit input constraints
- no upstream constraint record exists

### Classification

- `spec_clarification`

### Result

```yaml
change_record:
  id: change.auth.credentials.format
  change_class: spec_clarification
  summary: Accepted credential format is missing upstream.
  affected_implementation_unit_ids:
    - iu.authentication.capture_credentials
  source_anchor_ids:
    - anchor.use_case.uc_authenticate.step.capture_credentials
  trace_bundle_ids:
    - tb.authentication.capture_credentials
  recommended_action: add explicit input constraint upstream
  status: proposed

feedback:
  id: feedback.auth.credentials.format
  feedback_type: clarify_element
  change_record_id: change.auth.credentials.format
  summary: Define accepted credential format for authentication input.
  target_source_ids:
    - uc-authenticate.step-capture-credentials
  source_anchor_ids:
    - anchor.use_case.uc_authenticate.step.capture_credentials
  reason: Verification planning requires explicit constraints.
  proposed_upstream_action:
    - add a constraint for accepted credential format
  status: proposed
```

## Worked Example: Conflict

### Situation

- requirement says orders above threshold must be approved
- state transition path allows direct approval without threshold guard

### Classification

- `spec_conflict`

### Result

```yaml
change_record:
  id: change.order.threshold.conflict
  change_class: spec_conflict
  summary: Requirement and state transition semantics conflict on approval threshold.
  affected_implementation_unit_ids:
    - iu.order.approval_threshold
  source_anchor_ids:
    - anchor.requirement.req_order_approval
    - anchor.state.transition_order_pending_to_approved
  trace_bundle_ids:
    - tb.order.approval_threshold
  recommended_action: resolve contradiction between requirement and state model
  status: proposed

feedback:
  id: feedback.order.threshold.conflict
  feedback_type: resolve_conflict
  change_record_id: change.order.threshold.conflict
  summary: Align requirement and state transition for threshold-based approval.
  target_source_ids:
    - req-order-approval
    - transition-order-pending-to-approved
  source_anchor_ids:
    - anchor.requirement.req_order_approval
    - anchor.state.transition_order_pending_to_approved
  reason: The current source elements cannot both be satisfied.
  proposed_upstream_action:
    - add or revise threshold guard on approval transition
    - validate consistency between requirement and state model
  status: proposed
```

## Validation Rules

Speckify should not emit a feedback proposal unless:

- the originating change record exists
- source lineage is explicit
- at least one target source ID is known
- the feedback reason is concrete
- the proposed action is stated explicitly

If those conditions are not met, the system should keep the change as an unresolved
downstream note rather than pretending it has actionable upstream feedback.

## Recommended Future Extensions

- formal schema files for change records and feedback artifacts
- change-to-commit or change-to-PR linkage
- richer lifecycle states for upstream feedback handling
- diff-aware comparison between source model versions

## Open Questions

- should feedback proposals target canonical model elements only, or also rendered
  artifact sections
- how much of the downstream evidence should be embedded directly in the feedback artifact
- whether change records should live in the same planning bundle or a follow-on
  round-trip bundle
