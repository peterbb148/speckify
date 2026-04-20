# Speckified Specification

Source export: `/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json`

## Import Status

- The Rupify hand-off bundle did not import cleanly as-is. This specification is derived from the importable subset only.
- No manual edits were applied to the upstream export; blocked areas are reported separately.

## Importable Normative Core

### Acceptance Constraints

- `acceptance-constraint-requirement-1` Acceptance Constraint 1: UI must be web based
- `acceptance-constraint-requirement-2` Acceptance Constraint 2: SSO
- `acceptance-constraint-requirement-3` Acceptance Constraint 3: role-based access
- `acceptance-constraint-requirement-4` Acceptance Constraint 4: audit trail
- `acceptance-constraint-requirement-5` Acceptance Constraint 5: search
- `acceptance-constraint-requirement-6` Acceptance Constraint 6: filtering
- `acceptance-constraint-requirement-7` Acceptance Constraint 7: performance (regular >1s for web page rendering)
- `acceptance-constraint-requirement-8` Acceptance Constraint 8: availability >=99%
- `acceptance-constraint-success-1` Success Criterion 1: Better planning of IT systems purchasing and life cycle

### Domain Invariants

- `domain-invariant-1` Rule 1: A System must have a business owner before it becomes Active.
- `domain-invariant-2` Rule 2: A System lifecycle state change requires approval for deprecation.
- `domain-invariant-3` Rule 3: A System must record vendor and contract dates.

### Non Functional Requirements

- `non_functional-requirement-2` non_functional-requirement-2: role-based access
- `non_functional-requirement-3` non_functional-requirement-3: audit trail
- `non_functional-requirement-4` non_functional-requirement-4: search
- `non_functional-requirement-5` non_functional-requirement-5: filtering
- `non_functional-requirement-6` non_functional-requirement-6: performance (regular >1s for web page rendering)
- `non_functional-requirement-7` non_functional-requirement-7: availability >=99%

### State Invariants

- `state-invariant-1` Rule 1: A System must have a business owner before it becomes Active.
- `state-invariant-2` Rule 2: A System lifecycle state change requires approval for deprecation.
- `state-invariant-3` Rule 3: A System must record vendor and contract dates.

### State Transitions

- `state-transition-1` state-transition-1: System: Proposed -> Active -> Retiring -> Retired
- `state-transition-2` state-transition-2: System: Proposed -> Active -> Retiring -> Retired
- `state-transition-3` state-transition-3: System: Proposed -> Active -> Retiring -> Retired
- `state-transition-4` state-transition-4: System: Active -> Deprecated

## Import Blockers

- Duplicate element id: functional-requirement-1
- Duplicate element id: non_functional-requirement-1
- Unresolved trace references detected: 10

## Notes

- This document is a first Speckified specification artifact produced from the real Rupify hand-off export.
- It intentionally excludes ambiguous or structurally blocked areas rather than patching upstream data.
