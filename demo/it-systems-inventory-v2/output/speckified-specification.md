# Speckified Specification

Project: `speckify-planning-export`

## Overview

- Source system: `rupify`
- Generated implementation units: 35
- Generated verification units: 35
- Trace bundles: 35
- Dependency edges: 14
- Assembly rules: 3

## Implementation Units

### Acceptance Constraints

#### Implement constraint: Acceptance Constraint 1

- ID: `iu.rupify.acceptance-constraint-requirement-1`
- Summary: Deliver behavior that satisfies the constraint 'UI must be web based'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-1` (constraint: `acceptance-constraint-requirement-1`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-1`
- Acceptance criteria:
  - UI must be web based

#### Implement constraint: Acceptance Constraint 2

- ID: `iu.rupify.acceptance-constraint-requirement-2`
- Summary: Deliver behavior that satisfies the constraint 'SSO'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-2` (constraint: `acceptance-constraint-requirement-2`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-2`
- Acceptance criteria:
  - SSO

#### Implement constraint: Acceptance Constraint 3

- ID: `iu.rupify.acceptance-constraint-requirement-3`
- Summary: Deliver behavior that satisfies the constraint 'role-based access'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-3` (constraint: `acceptance-constraint-requirement-3`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-3`
- Acceptance criteria:
  - role-based access

#### Implement constraint: Acceptance Constraint 4

- ID: `iu.rupify.acceptance-constraint-requirement-4`
- Summary: Deliver behavior that satisfies the constraint 'audit trail'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-4` (constraint: `acceptance-constraint-requirement-4`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-4`
- Acceptance criteria:
  - audit trail

#### Implement constraint: Acceptance Constraint 5

- ID: `iu.rupify.acceptance-constraint-requirement-5`
- Summary: Deliver behavior that satisfies the constraint 'search'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-5` (constraint: `acceptance-constraint-requirement-5`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-5`
- Acceptance criteria:
  - search

#### Implement constraint: Acceptance Constraint 6

- ID: `iu.rupify.acceptance-constraint-requirement-6`
- Summary: Deliver behavior that satisfies the constraint 'filtering'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-6` (constraint: `acceptance-constraint-requirement-6`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-6`
- Acceptance criteria:
  - filtering

#### Implement constraint: Acceptance Constraint 7

- ID: `iu.rupify.acceptance-constraint-requirement-7`
- Summary: Deliver behavior that satisfies the constraint 'performance (regular >1s for web page rendering)'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-7` (constraint: `acceptance-constraint-requirement-7`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-7`
- Acceptance criteria:
  - performance (regular >1s for web page rendering)

#### Implement constraint: Acceptance Constraint 8

- ID: `iu.rupify.acceptance-constraint-requirement-8`
- Summary: Deliver behavior that satisfies the constraint 'availability >=99%'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-requirement-8` (constraint: `acceptance-constraint-requirement-8`)
- Dependencies:
  - `iu.rupify.non-functional-requirement-8`
- Acceptance criteria:
  - availability >=99%

#### Implement constraint: Success Criterion 1

- ID: `iu.rupify.acceptance-constraint-success-1`
- Summary: Deliver behavior that satisfies the constraint 'Better planning of IT systems purchasing and life cycle'.
- Source lineage:
  - `anchor.rupify.acceptance-constraints.acceptance-constraint-success-1` (constraint: `acceptance-constraint-success-1`)
- Acceptance criteria:
  - Better planning of IT systems purchasing and life cycle

### Domain Invariants

#### Enforce invariant: Rule 1

- ID: `iu.rupify.domain-invariant-1`
- Summary: Ensure the invariant 'A System must have a business owner before it becomes Active.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.domain-invariants.domain-invariant-1` (domain_invariant: `domain-invariant-1`)
- Acceptance criteria:
  - A System must have a business owner before it becomes Active.

#### Enforce invariant: Rule 2

- ID: `iu.rupify.domain-invariant-2`
- Summary: Ensure the invariant 'A System lifecycle state change requires approval for deprecation.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.domain-invariants.domain-invariant-2` (domain_invariant: `domain-invariant-2`)
- Acceptance criteria:
  - A System lifecycle state change requires approval for deprecation.

#### Enforce invariant: Rule 3

- ID: `iu.rupify.domain-invariant-3`
- Summary: Ensure the invariant 'A System must record vendor and contract dates.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.domain-invariants.domain-invariant-3` (domain_invariant: `domain-invariant-3`)
- Acceptance criteria:
  - A System must record vendor and contract dates.

### Functional Requirements

#### Implement workflow support: functional-requirement-1

- ID: `iu.rupify.functional-requirement-1`
- Summary: Yes business processes like stage gates and approval states must be supported
- Source lineage:
  - `anchor.rupify.functional-requirements.functional-requirement-1` (requirement: `functional-requirement-1`)
- Acceptance criteria:
  - Yes business processes like stage gates and approval states must be supported

#### Implement workflow support: functional-requirement-2

- ID: `iu.rupify.functional-requirement-2`
- Summary: I think this will be the CMDB for IT Applications/systems - we need to be able to export data to various system for reporting.
- Source lineage:
  - `anchor.rupify.functional-requirements.functional-requirement-2` (requirement: `functional-requirement-2`)
- Acceptance criteria:
  - I think this will be the CMDB for IT Applications/systems - we need to be able to export data to various system for reporting.

### Non Functional Requirements

#### Implement constraint: non_functional-requirement-1

- ID: `iu.rupify.non-functional-requirement-1`
- Summary: Deliver behavior that satisfies the constraint 'UI must be web based'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-1` (requirement: `non_functional-requirement-1`)
- Acceptance criteria:
  - UI must be web based

#### Implement constraint: non_functional-requirement-2

- ID: `iu.rupify.non-functional-requirement-2`
- Summary: Deliver behavior that satisfies the constraint 'SSO'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-2` (requirement: `non_functional-requirement-2`)
- Acceptance criteria:
  - SSO

#### Implement constraint: non_functional-requirement-3

- ID: `iu.rupify.non-functional-requirement-3`
- Summary: Deliver behavior that satisfies the constraint 'role-based access'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-3` (requirement: `non_functional-requirement-3`)
- Acceptance criteria:
  - role-based access

#### Implement constraint: non_functional-requirement-4

- ID: `iu.rupify.non-functional-requirement-4`
- Summary: Deliver behavior that satisfies the constraint 'audit trail'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-4` (requirement: `non_functional-requirement-4`)
- Acceptance criteria:
  - audit trail

#### Implement constraint: non_functional-requirement-5

- ID: `iu.rupify.non-functional-requirement-5`
- Summary: Deliver behavior that satisfies the constraint 'search'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-5` (requirement: `non_functional-requirement-5`)
- Acceptance criteria:
  - search

#### Implement constraint: non_functional-requirement-6

- ID: `iu.rupify.non-functional-requirement-6`
- Summary: Deliver behavior that satisfies the constraint 'filtering'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-6` (requirement: `non_functional-requirement-6`)
- Acceptance criteria:
  - filtering

#### Implement constraint: non_functional-requirement-7

- ID: `iu.rupify.non-functional-requirement-7`
- Summary: Deliver behavior that satisfies the constraint 'performance (regular >1s for web page rendering)'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-7` (requirement: `non_functional-requirement-7`)
- Acceptance criteria:
  - performance (regular >1s for web page rendering)

#### Implement constraint: non_functional-requirement-8

- ID: `iu.rupify.non-functional-requirement-8`
- Summary: Deliver behavior that satisfies the constraint 'availability >=99%'.
- Source lineage:
  - `anchor.rupify.non-functional-requirements.non-functional-requirement-8` (requirement: `non_functional-requirement-8`)
- Acceptance criteria:
  - availability >=99%

### State Invariants

#### Enforce invariant: Rule 1

- ID: `iu.rupify.state-invariant-1`
- Summary: Ensure the invariant 'A System must have a business owner before it becomes Active.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.state-invariants.state-invariant-1` (state_invariant: `state-invariant-1`)
- Acceptance criteria:
  - A System must have a business owner before it becomes Active.

#### Enforce invariant: Rule 2

- ID: `iu.rupify.state-invariant-2`
- Summary: Ensure the invariant 'A System lifecycle state change requires approval for deprecation.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.state-invariants.state-invariant-2` (state_invariant: `state-invariant-2`)
- Acceptance criteria:
  - A System lifecycle state change requires approval for deprecation.

#### Enforce invariant: Rule 3

- ID: `iu.rupify.state-invariant-3`
- Summary: Ensure the invariant 'A System must record vendor and contract dates.' is enforced in the implemented behavior.
- Source lineage:
  - `anchor.rupify.state-invariants.state-invariant-3` (state_invariant: `state-invariant-3`)
- Acceptance criteria:
  - A System must record vendor and contract dates.

### State Transitions

#### Implement lifecycle transition: Proposed to Active

- ID: `iu.rupify.state-transition-1.proposed-to-active`
- Summary: Transition the system lifecycle from Proposed to Active.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-1` (state_transition: `state-transition-1`)
- Acceptance criteria:
  - System can move from Proposed to Active.

#### Implement lifecycle transition: Active to Retiring

- ID: `iu.rupify.state-transition-1.active-to-retiring`
- Summary: Transition the system lifecycle from Active to Retiring.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-1` (state_transition: `state-transition-1`)
- Dependencies:
  - `iu.rupify.state-transition-1.proposed-to-active`
- Acceptance criteria:
  - System can move from Active to Retiring.

#### Implement lifecycle transition: Retiring to Retired

- ID: `iu.rupify.state-transition-1.retiring-to-retired`
- Summary: Transition the system lifecycle from Retiring to Retired.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-1` (state_transition: `state-transition-1`)
- Dependencies:
  - `iu.rupify.state-transition-1.active-to-retiring`
- Acceptance criteria:
  - System can move from Retiring to Retired.

#### Implement lifecycle transition: Proposed to Active

- ID: `iu.rupify.state-transition-2.proposed-to-active`
- Summary: Transition the system lifecycle from Proposed to Active.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)
- Acceptance criteria:
  - System can move from Proposed to Active.

#### Implement lifecycle transition: Active to Retiring

- ID: `iu.rupify.state-transition-2.active-to-retiring`
- Summary: Transition the system lifecycle from Active to Retiring.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)
- Dependencies:
  - `iu.rupify.state-transition-2.proposed-to-active`
- Acceptance criteria:
  - System can move from Active to Retiring.

#### Implement lifecycle transition: Retiring to Retired

- ID: `iu.rupify.state-transition-2.retiring-to-retired`
- Summary: Transition the system lifecycle from Retiring to Retired.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-2` (state_transition: `state-transition-2`)
- Dependencies:
  - `iu.rupify.state-transition-2.active-to-retiring`
- Acceptance criteria:
  - System can move from Retiring to Retired.

#### Implement lifecycle transition: Proposed to Active

- ID: `iu.rupify.state-transition-3.proposed-to-active`
- Summary: Transition the system lifecycle from Proposed to Active.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-3` (state_transition: `state-transition-3`)
- Acceptance criteria:
  - System can move from Proposed to Active.

#### Implement lifecycle transition: Active to Retiring

- ID: `iu.rupify.state-transition-3.active-to-retiring`
- Summary: Transition the system lifecycle from Active to Retiring.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-3` (state_transition: `state-transition-3`)
- Dependencies:
  - `iu.rupify.state-transition-3.proposed-to-active`
- Acceptance criteria:
  - System can move from Active to Retiring.

#### Implement lifecycle transition: Retiring to Retired

- ID: `iu.rupify.state-transition-3.retiring-to-retired`
- Summary: Transition the system lifecycle from Retiring to Retired.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-3` (state_transition: `state-transition-3`)
- Dependencies:
  - `iu.rupify.state-transition-3.active-to-retiring`
- Acceptance criteria:
  - System can move from Retiring to Retired.

#### Implement lifecycle transition: Active to Deprecated

- ID: `iu.rupify.state-transition-4.active-to-deprecated`
- Summary: Transition the system lifecycle from Active to Deprecated.
- Source lineage:
  - `anchor.rupify.state-transitions.state-transition-4` (state_transition: `state-transition-4`)
- Acceptance criteria:
  - System can move from Active to Deprecated.

