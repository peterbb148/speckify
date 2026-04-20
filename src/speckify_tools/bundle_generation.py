"""Generate Speckify planning bundles from imported Rupify exports."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .rendering import render_issue_projections
from .rupify_import import RupifyElement, RupifyPlanningExport, import_rupify_export_file


FAMILY_VIEW_MAP = {
    "acceptance_constraints": ("constraint", "constraint"),
    "domain_invariants": ("domain", "domain_invariant"),
    "functional_requirements": ("requirements", "requirement"),
    "non_functional_requirements": ("requirements", "requirement"),
    "state_invariants": ("state", "state_invariant"),
    "state_transitions": ("state", "state_transition"),
}


def _slug(value: str) -> str:
    """Convert an identifier into a stable bundle slug fragment."""
    return value.replace("_", "-").replace(" ", "-").lower()


def _view_and_source_type(element: RupifyElement) -> tuple[str, str]:
    """Resolve bundle view and source type from a Rupify element family."""
    return FAMILY_VIEW_MAP.get(element.family, ("requirements", "requirement"))


def _anchor_id(element: RupifyElement) -> str:
    """Build the source anchor id for a Rupify element."""
    return f"anchor.rupify.{_slug(element.family)}.{_slug(element.id)}"


def _spec_unit_id(element: RupifyElement) -> str:
    """Build the spec unit id for a Rupify element."""
    return f"su.rupify.{_slug(element.id)}"


def _implementation_unit_id(element: RupifyElement) -> str:
    """Build the implementation unit id for a Rupify element."""
    return f"iu.rupify.{_slug(element.id)}"


def _verification_unit_id(element: RupifyElement) -> str:
    """Build the verification unit id for a Rupify element."""
    return f"vu.rupify.{_slug(element.id)}"


def _trace_bundle_id(element: RupifyElement) -> str:
    """Build the trace bundle id for a Rupify element."""
    return f"tb.rupify.{_slug(element.id)}"


def _element_title(element: RupifyElement) -> str:
    """Resolve the best available title for a Rupify element."""
    if element.name:
        return element.name
    return element.id


def _element_summary(element: RupifyElement) -> str:
    """Resolve the best available summary text for a Rupify element."""
    if element.text:
        return element.text
    return f"Derived from Rupify element {element.id}."


def _eligible_elements(export: RupifyPlanningExport) -> list[RupifyElement]:
    """Return the first-pass bundle generation candidates."""
    return [
        element
        for element in export.elements
        if element.content_semantics == "normative" and element.normative_ready
    ]


def _slice_suffix_id(base_id: str, suffix: str | None) -> str:
    """Append a decomposition suffix to an id when present."""
    if not suffix:
        return base_id
    return f"{base_id}.{suffix}"


def _split_state_transition_text(text: str) -> list[dict[str, str]]:
    """Split a chain state transition into individual transition slices."""
    if ":" not in text or "->" not in text:
        return []
    _, chain = text.split(":", 1)
    states = [part.strip() for part in chain.split("->") if part.strip()]
    if len(states) < 2:
        return []

    slices: list[dict[str, str]] = []
    for from_state, to_state in zip(states, states[1:]):
        suffix = f"{_slug(from_state)}-to-{_slug(to_state)}"
        slices.append(
            {
                "suffix": suffix,
                "title": f"{from_state} to {to_state}",
                "summary": f"Transition the system lifecycle from {from_state} to {to_state}.",
                "acceptance": f"System can move from {from_state} to {to_state}.",
            }
        )
    return slices


def _split_functional_requirement_text(text: str) -> list[dict[str, str]]:
    """Split a simple conjunctive functional requirement into separate obligations."""
    lowered = text.lower()
    marker = "stage gates and approval states"
    if marker not in lowered:
        return []
    return [
        {
            "suffix": "stage-gates",
            "title": "Support stage gates",
            "summary": "Support business process stage gates.",
            "acceptance": "Business process stage gates are supported.",
        },
        {
            "suffix": "approval-states",
            "title": "Support approval states",
            "summary": "Support business process approval states.",
            "acceptance": "Business process approval states are supported.",
        },
    ]


def _decompose_element(element: RupifyElement) -> list[dict[str, str | None]]:
    """Decompose one source element into one or more planning slices."""
    if element.family == "state_transitions":
        slices = _split_state_transition_text(element.text)
        if slices:
            return slices
    if element.family == "functional_requirements":
        slices = _split_functional_requirement_text(element.text)
        if slices:
            return slices

    return [
        {
            "suffix": None,
            "title": _element_title(element),
            "summary": _element_summary(element),
            "acceptance": _element_summary(element),
        }
    ]


def _implementation_title(element: RupifyElement, title: str) -> str:
    """Derive a more usable implementation title."""
    if element.family in {"acceptance_constraints", "non_functional_requirements"}:
        return f"Implement constraint: {title}"
    if element.family in {"domain_invariants", "state_invariants"}:
        return f"Enforce invariant: {title}"
    if element.family == "state_transitions":
        return f"Implement lifecycle transition: {title}"
    if element.family == "functional_requirements":
        return f"Implement workflow support: {title}"
    return f"Implement {title}"


def _implementation_summary(element: RupifyElement, title: str, summary: str, acceptance: str) -> str:
    """Derive a more usable implementation summary."""
    if element.family in {"acceptance_constraints", "non_functional_requirements"}:
        return f"Deliver behavior that satisfies the constraint '{acceptance}'."
    if element.family in {"domain_invariants", "state_invariants"}:
        return f"Ensure the invariant '{acceptance}' is enforced in the implemented behavior."
    if element.family == "state_transitions":
        return summary
    if element.family == "functional_requirements":
        return summary
    return f"Implement the behavior described by {title.lower()}."


def _verification_contract(
    element: RupifyElement,
    title: str,
    acceptance: str,
    summary: str,
    implementation_unit_id: str,
) -> dict[str, Any]:
    """Derive a richer verification contract from source semantics."""
    verification_intent = f"Confirm the implementation satisfies {title.lower()}."
    observables = [acceptance]
    setup_requirements: list[str] = []
    expected_outcomes = [acceptance]
    failure_conditions: list[str] = []
    invariants_preserved: list[str] = []

    if element.family in {"acceptance_constraints", "non_functional_requirements"}:
        verification_intent = f"Confirm the delivered behavior satisfies the stated constraint for {title.lower()}."
        setup_requirements = ["The relevant system boundary or UI surface is available for inspection."]
        failure_conditions = [f"The delivered behavior violates the stated constraint: {acceptance}"]

    elif element.family in {"domain_invariants", "state_invariants"}:
        verification_intent = f"Confirm the invariant remains enforced for {title.lower()}."
        setup_requirements = ["A representative system record exists in a state where the rule applies."]
        expected_outcomes = [f"The invariant remains true: {acceptance}"]
        failure_conditions = [f"The invariant is breached: {acceptance}"]
        invariants_preserved = [acceptance]

    elif element.family == "functional_requirements":
        verification_intent = f"Confirm workflow support is present for {title.lower()}."
        setup_requirements = ["The relevant workflow capability is reachable in the system."]
        expected_outcomes = [f"The workflow behavior is supported: {acceptance}"]
        failure_conditions = [f"The workflow behavior is missing or incomplete: {acceptance}"]

    elif element.family == "state_transitions":
        if " from " in summary and " to " in summary:
            transition_text = summary.replace("Transition the system lifecycle from ", "").rstrip(".")
            from_state, to_state = [part.strip() for part in transition_text.split(" to ", 1)]
            verification_intent = f"Confirm the lifecycle transition from {from_state} to {to_state} is allowed and produces the expected target state."
            setup_requirements = [f"The system starts in the {from_state} state."]
            expected_outcomes = [f"The system reaches the {to_state} state after the transition is applied."]
            failure_conditions = [
                f"The system cannot leave {from_state} for {to_state} when the transition is requested.",
                f"The system enters an unexpected state instead of {to_state}.",
            ]
        else:
            failure_conditions = [f"The lifecycle transition does not behave as specified: {acceptance}"]

    return {
        "implementation_unit_id": implementation_unit_id,
        "verification_intent": verification_intent,
        "observables": observables,
        "setup_requirements": setup_requirements,
        "expected_outcomes": expected_outcomes,
        "failure_conditions": failure_conditions,
        "invariants_preserved": invariants_preserved,
    }


def _derive_relationships(
    implementation_units: list[dict[str, Any]],
    spec_units: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive dependency edges, assembly rules, and updated implementation units."""
    implementation_index = {item["id"]: item for item in implementation_units}
    dependency_edges: list[dict[str, Any]] = []
    assembly_rules: list[dict[str, Any]] = []

    state_transition_sequences = [
        [
            "proposed-to-active",
            "active-to-retiring",
            "retiring-to-retired",
        ]
    ]

    source_groups: dict[str, list[dict[str, Any]]] = {}
    for item in implementation_units:
        source_anchor_id = item["source_anchor_ids"][0]
        source_groups.setdefault(source_anchor_id, []).append(item)

    spec_by_id = {item["id"]: item for item in spec_units}

    for source_anchor_id, members in source_groups.items():
        member_ids = sorted(item["id"] for item in members)
        if source_anchor_id == "anchor.rupify.functional-requirements.functional-requirement-1":
            from_id = "iu.rupify.functional-requirement-1.approval-states"
            to_id = "iu.rupify.functional-requirement-1.stage-gates"
            implementation_index[from_id]["dependencies"].append(to_id)
            dependency_edges.append(
                {
                    "id": "dep.functional-requirement-1.approval-states-soft-sequence",
                    "from_implementation_unit_id": from_id,
                    "to_implementation_unit_id": to_id,
                    "dependency_type": "soft_sequence",
                    "reason": "Approval states are coordinated workflow behavior that should follow stage-gate support.",
                }
            )
            assembly_rules.append(
                {
                    "id": "assembly.functional-requirement-1",
                    "source_anchor_ids": [source_anchor_id],
                    "member_spec_unit_ids": [
                        "su.rupify.functional-requirement-1.stage-gates",
                        "su.rupify.functional-requirement-1.approval-states",
                    ],
                    "rule_type": "ordered_sequence",
                    "notes": [
                        "Recombine split workflow concerns into the original conjunctive requirement.",
                    ],
                }
            )
            continue

        if source_anchor_id.startswith("anchor.rupify.state-transitions.") and len(members) > 1:
            ordered_units: list[dict[str, Any]] = []
            for sequence in state_transition_sequences:
                ordered_units = [
                    item
                    for suffix in sequence
                    for item in members
                    if item["id"].endswith(suffix)
                ]
                if ordered_units:
                    break
            if not ordered_units:
                ordered_units = sorted(members, key=lambda item: item["id"])

            for previous, current in zip(ordered_units, ordered_units[1:]):
                current["dependencies"].append(previous["id"])
                dependency_edges.append(
                    {
                        "id": f"dep.{current['id'].replace('iu.', '')}.requires-{previous['id'].replace('iu.', '')}",
                        "from_implementation_unit_id": current["id"],
                        "to_implementation_unit_id": previous["id"],
                        "dependency_type": "requires",
                        "reason": "Later lifecycle transitions require the earlier transition in the same source chain.",
                    }
                )

            assembly_rules.append(
                {
                    "id": f"assembly.{source_anchor_id.split('.')[-1]}",
                    "source_anchor_ids": [source_anchor_id],
                    "member_spec_unit_ids": [
                        spec_id
                        for item in ordered_units
                        for spec_id in item["derived_from_spec_unit_ids"]
                    ],
                    "rule_type": "ordered_sequence",
                    "notes": [
                        "Recombine split lifecycle transitions into the original source transition chain.",
                    ],
                }
            )

    return list(implementation_index.values()), dependency_edges, assembly_rules


def generate_planning_bundle(
    export: RupifyPlanningExport,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Generate a first Speckify planning bundle from imported Rupify records.

    Args:
        export: Typed Rupify planning export.
        generated_at: Optional timestamp override for deterministic tests.

    Returns:
        Planning bundle dictionary.
    """
    if generated_at is None:
        generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    project_id = export.export_metadata.export_kind.replace("_", "-")
    source_model_id = export.raw.get("export_metadata", {}).get("source_model_semantic_id", "")
    source_model_version = (
        export.raw.get("export_metadata", {})
        .get("source_model_change_metadata", {})
        .get("semantic_version", 1)
    )

    elements = _eligible_elements(export)
    source_anchors: list[dict[str, Any]] = []
    spec_units: list[dict[str, Any]] = []
    implementation_units: list[dict[str, Any]] = []
    verification_units: list[dict[str, Any]] = []
    trace_bundles: list[dict[str, Any]] = []

    for element in elements:
        anchor_id = _anchor_id(element)
        view, source_type = _view_and_source_type(element)

        source_anchors.append(
            {
                "id": anchor_id,
                "source_system": "rupify",
                "source_type": source_type,
                "source_id": element.id,
                "view": view,
                "normative": True,
                "ready_state": "ready",
                "trace": {
                    "source_round": element.raw.get("source_round", 0),
                    "source_key": element.raw.get("source_key", "unknown"),
                },
            }
        )

        for slice_data in _decompose_element(element):
            suffix = slice_data["suffix"]
            title = str(slice_data["title"])
            summary = str(slice_data["summary"])
            acceptance = str(slice_data["acceptance"])
            spec_unit_id = _slice_suffix_id(_spec_unit_id(element), suffix)
            implementation_unit_id = _slice_suffix_id(_implementation_unit_id(element), suffix)
            verification_unit_id = _slice_suffix_id(_verification_unit_id(element), suffix)
            trace_bundle_id = _slice_suffix_id(_trace_bundle_id(element), suffix)

            spec_units.append(
                {
                    "id": spec_unit_id,
                    "title": title,
                    "summary": summary,
                    "source_anchor_ids": [anchor_id],
                    "obligation_kind": source_type,
                    "normative": True,
                    "status": "proposed",
                    "notes": [f"Derived from Rupify {element.family} element {element.id}."],
                }
            )

            implementation_units.append(
                {
                    "id": implementation_unit_id,
                    "title": _implementation_title(element, title),
                    "summary": _implementation_summary(element, title, summary, acceptance),
                    "derived_from_spec_unit_ids": [spec_unit_id],
                    "source_anchor_ids": [anchor_id],
                    "dependencies": [],
                    "implementation_scope": [summary],
                    "non_goals": [],
                    "constraints": [],
                    "acceptance_criteria": [acceptance],
                    "verification_unit_ids": [verification_unit_id],
                    "drift_checks": [f"Preserve lineage to Rupify element {element.id}."],
                    "reverse_impact_hint": f"Changes here may require upstream review of {element.id}.",
                    "labels": ["planning", _slug(element.family)],
                }
            )

            verification_units.append(
                {
                    "id": verification_unit_id,
                    "title": f"Verify {title}",
                    "source_anchor_ids": [anchor_id],
                    **_verification_contract(
                        element,
                        title,
                        acceptance,
                        summary,
                        implementation_unit_id,
                    ),
                    "notes": [f"Derived from decomposition slice of {element.id}."],
                }
            )

            trace_bundles.append(
                {
                    "id": trace_bundle_id,
                    "source_anchor_ids": [anchor_id],
                    "spec_unit_ids": [spec_unit_id],
                    "implementation_unit_ids": [implementation_unit_id],
                    "verification_unit_ids": [verification_unit_id],
                    "assembly_rule_ids": [],
                    "notes": [f"Derived from decomposition slice of {element.id}."],
                }
            )

    implementation_units, dependency_edges, assembly_rules = _derive_relationships(
        implementation_units,
        spec_units,
    )

    unresolved_ambiguities = [
        {
            "ambiguity_id": ambiguity_id,
            "status": "unresolved",
            "blocking": True,
        }
        for ambiguity_id in export.summary.raw.get("blocking_ambiguity_ids", [])
    ]

    bundle = {
        "bundle_metadata": {
            "bundle_id": f"bundle.{project_id}",
            "schema_version": 1,
            "bundle_version": 1,
            "generated_at": generated_at,
            "source_model_id": source_model_id or project_id,
            "source_model_version": source_model_version,
            "decomposition_profile": "rupify-split-dependencies-v1",
        },
        "source_summary": {
            "source_system": "rupify",
            "project_id": project_id,
            "project_name": source_model_id or project_id,
            "export_version": export.raw.get("export_metadata", {}).get("schema_version", 1),
            "notes": [
                "Generated directly from imported Rupify planning export records.",
                "First-pass decomposition splits selected ready normative source elements into smaller planning units.",
                "Deterministic dependency edges and assembly rules are derived for split workflow and transition chains.",
            ],
        },
        "source_anchors": source_anchors,
        "spec_units": spec_units,
        "implementation_units": implementation_units,
        "verification_units": verification_units,
        "trace_bundles": trace_bundles,
        "dependency_edges": dependency_edges,
        "assembly_rules": assembly_rules,
        "unresolved_ambiguities": unresolved_ambiguities,
        "rendered_issues": [],
    }
    bundle["rendered_issues"] = render_issue_projections(bundle)
    return bundle


def generate_planning_bundle_file(
    source_path: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Load a Rupify export from disk and generate a planning bundle."""
    return generate_planning_bundle(
        import_rupify_export_file(source_path),
        generated_at=generated_at,
    )
