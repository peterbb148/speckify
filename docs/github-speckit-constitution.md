# GitHub SpecKit Constitution

## Purpose

This Constitution defines the non-negotiable rules that govern how Speckify transforms
Rupify source structures into planning artifacts for GitHub SpecKit.

Speckify is intended to be a formal, trace-preserving, round-trip-safe transformation
layer. Any transform behavior that cannot be explained in structural, typed, and
provenance-preserving terms violates the purpose of the system.

## Status

This document is constitutional. It overrides convenience, demo fit, output polish, or
short-term implementation expediency.

## Constitutional Principles

### 1. Source Structure Over Source Phrasing

Speckify must derive decomposition from typed source structure, explicit source
relationships, and formally declared operators.

Speckify must not derive decomposition from:

- exact wording in a demo bundle
- phrase-specific matching tied to one source example
- ad hoc pattern recognition that cannot be justified as a stable structural rule

Equivalent source structure must yield equivalent decomposition even when source wording
changes.

### 2. Typed Inputs Only

The golden path must operate on typed, normalized Rupify exports.

Allowed transform inputs include:

- element family and type
- ordered step structure
- state, transition, and guard structure
- scenario, extension, and exception structure
- invariants and constraints
- trace links
- normative and readiness metadata

Rendered Markdown or prose-only views must not be treated as the authoritative input
surface for decomposition.

### 3. Explicit Decomposition Operators

Every decomposition must be explainable by an explicit operator class.

Examples of valid operator classes include:

- sequence decomposition
- conjunction decomposition
- state-transition chain decomposition
- scenario trigger/response decomposition
- guard prerequisite/enforcement decomposition
- constraint overlay decomposition
- orchestration decomposition

If a derived split cannot name its operator class precisely, it must not exist in the
formal transform.

### 4. Provenance Is Mandatory

Every derived record must preserve explicit lineage to its source anchor or anchors.

Each transform must make it possible to answer:

- which source element produced this unit
- which operator produced this unit
- what other units were produced from the same source element
- how the original source semantics can be reassembled

No hidden derivation is allowed.

### 5. Assembly Rules Are Required

Every split transform must have an explicit assembly rule for recomposition.

Assembly rules must define how derived units reconstruct the source obligation, flow, or
constraint. A split without a declared recomposition path is constitutionally invalid.

### 6. Round-Trip Correctness Is First-Class

Speckify exists to support reversibility and round trips. Therefore:

- downstream changes must remain attributable to source structure
- decomposition must remain stable under regeneration
- output units must be classifiable for upstream feedback
- the system must prefer explicit failure over silent approximation when source semantics
  are insufficient for a formal transform

Any behavior that is not stable enough to support round-trip reasoning is out of bounds
for the golden path.

### 7. No Demo-Specific Rules

Demo bundles are validation fixtures, not rule sources.

Speckify must not merge logic that is specific to:

- one named example bundle
- one project’s phrasing conventions
- one observed sequence of source text fragments

Demo fixtures may expose missing generic operators. They must never justify adding a
bundle-specific transform rule.

### 8. No Invented Fallbacks

When formal decomposition is not justified by the available source structure, Speckify
must fail clearly, preserve the broader unit, or emit an explicit review warning.

It must not silently invent:

- plausible subunits
- heuristic substitutes
- example-fitted decomposition paths
- placeholder round-trip semantics

### 9. Determinism

The transformation must be deterministic for a given source bundle and decomposition
profile.

The same input structure and the same operator set must produce the same:

- source anchors
- derived units
- dependency edges
- assembly rules
- delivery artifacts
- round-trip artifacts

### 10. Constitution Before Optimization

Output quality, readability, and delivery convenience matter, but none of them may
override formal correctness.

If there is a conflict between:

- a nicer-looking output
- a demo-specific improvement
- a constitutionally valid transform

the constitutionally valid transform wins.

## Acceptance Standard For Transform Rules

A transform rule is mergeable only if all of the following are true:

1. It operates on typed source structure or declared source relationships.
2. It can be named as a stable operator class.
3. It preserves explicit provenance.
4. It declares or participates in an assembly rule when it splits a source element.
5. It is stable under source rewording that preserves the same structure.
6. It does not rely on one named demo bundle or one source phrase pattern.
7. It is compatible with round-trip classification and upstream feedback generation.

If any of these checks fail, the rule must be rejected, removed, or rewritten.

## Implementation Consequences

This Constitution implies the following corrective work:

- audit the current generator for phrase-shaped or bundle-shaped rules
- classify each rule as keep, refactor, or remove
- move decomposition behavior toward typed operators and source-structure predicates
- treat the current demo bundles only as regression fixtures for valid generic behavior

## Relationship To GitHub SpecKit

GitHub SpecKit is downstream of Speckify. Therefore GitHub SpecKit artifacts must inherit
these same constitutional guarantees:

- trace-preserving units
- explicit provenance
- deterministic generation
- round-trip-safe semantics
- no example-fitted decomposition hidden in delivery outputs

GitHub delivery convenience is subordinate to constitutional correctness.
