"""Generate Speckify planning bundles from imported Rupify exports."""

from __future__ import annotations

import re
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

RAW_SOURCE_IDENTIFIER_RE = re.compile(r"^[a-z]+(?:[_-][a-z0-9]+)*-\d+$")
GENERIC_ORDINAL_TITLE_RE = re.compile(
    r"^(?:Acceptance Constraint|Requirement|Constraint|Scenario|Use Case|Guard Condition|Success Criterion|Rule)\s+\d+$",
    flags=re.IGNORECASE,
)


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


def _humanize_identifier(value: str) -> str:
    """Convert a source-style identifier into readable words."""
    words = value.replace("_", " ").replace("-", " ").split()
    if not words:
        return value
    return words[0].capitalize() + "".join(f" {word}" for word in words[1:])


def _looks_like_raw_source_identifier(value: str) -> bool:
    """Return whether one value still looks like a raw source identifier."""
    return bool(RAW_SOURCE_IDENTIFIER_RE.fullmatch(value.strip()))


def _looks_like_generic_ordinal(value: str) -> bool:
    """Return whether one value still looks like a generic ordinal label."""
    return bool(GENERIC_ORDINAL_TITLE_RE.fullmatch(value.strip()))


def _single_line(text: str) -> str:
    """Flatten text into one trimmed line."""
    return " ".join(text.split()).strip()


def _trim_sentence(text: str, *, max_words: int = 12) -> str:
    """Trim one text fragment to a bounded, sentence-like label."""
    flattened = _single_line(text).rstrip(".")
    words = flattened.split()
    if len(words) <= max_words:
        return flattened
    return " ".join(words[:max_words])


def _best_delivery_label(
    element: RupifyElement,
    title: str,
    summary: str,
    acceptance: str,
) -> str:
    """Resolve a publication-friendly label for one implementation unit."""
    candidates = [title, summary, acceptance]
    for candidate in candidates:
        normalized = _trim_sentence(candidate)
        if not normalized:
            continue
        if _looks_like_raw_source_identifier(normalized):
            continue
        if _looks_like_generic_ordinal(normalized):
            continue
        return normalized
    return _humanize_identifier(element.id)


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


def _normalize_structured_part(part: dict[str, Any]) -> dict[str, str] | None:
    """Normalize one explicit conjunction part into a planning slice."""
    raw_suffix = part.get("suffix") or part.get("id")
    raw_title = part.get("title") or part.get("name") or part.get("label")
    raw_summary = part.get("summary") or part.get("text")
    raw_acceptance = part.get("acceptance") or raw_summary

    if not isinstance(raw_suffix, str) or not raw_suffix:
        return None
    if not isinstance(raw_title, str) or not raw_title:
        return None
    if not isinstance(raw_summary, str) or not raw_summary:
        return None
    if not isinstance(raw_acceptance, str) or not raw_acceptance:
        return None

    return {
        "suffix": _slug(raw_suffix),
        "title": raw_title,
        "summary": raw_summary,
        "acceptance": raw_acceptance,
    }


def _structured_conjunction_parts(element: RupifyElement) -> list[dict[str, Any]]:
    """Return explicit structured conjunction parts from the imported element."""
    candidate_lists = [
        element.obligations,
        element.semantic_parts,
    ]

    sub_obligations = element.attributes.get("sub_obligations")
    if isinstance(sub_obligations, list) and all(isinstance(item, dict) for item in sub_obligations):
        candidate_lists.append(sub_obligations)

    for parts in candidate_lists:
        if parts:
            return parts

    return []


def _split_structured_conjunction(element: RupifyElement) -> list[dict[str, str]]:
    """Split one element using explicit structured conjunction parts only."""
    slices: list[dict[str, str]] = []
    for part in _structured_conjunction_parts(element):
        normalized = _normalize_structured_part(part)
        if normalized is None:
            return []
        slices.append(normalized)

    return slices if len(slices) > 1 else []


def _split_structured_scenario(element: RupifyElement) -> list[dict[str, str]]:
    """Split one scenario using explicit ordered flow segments only."""
    flow_of_events = element.attributes.get("flow_of_events")
    if not isinstance(flow_of_events, list):
        return []
    if not all(isinstance(item, str) and item for item in flow_of_events):
        return []
    if len(flow_of_events) < 2:
        return []

    return [
        {
            "suffix": f"segment-{index}",
            "title": f"{_element_title(element)} segment {index}",
            "summary": event,
            "acceptance": event,
        }
        for index, event in enumerate(flow_of_events, start=1)
    ]


def _decompose_element(element: RupifyElement) -> list[dict[str, str | None]]:
    """Decompose one source element into one or more planning slices."""
    if element.family == "state_transitions":
        slices = _split_state_transition_text(element.text)
        if slices:
            return slices
    if element.family in {"functional_requirements", "domain_invariants", "state_invariants", "use_case_steps"}:
        slices = _split_structured_conjunction(element)
        if slices:
            return slices
    if element.family == "scenarios":
        slices = _split_structured_scenario(element)
        if slices:
            return slices
    if element.family == "guard_conditions":
        slices = _split_structured_conjunction(element)
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


def _implementation_title(
    element: RupifyElement,
    title: str,
    summary: str,
    acceptance: str,
) -> str:
    """Derive a more usable implementation title."""
    label = _best_delivery_label(element, title, summary, acceptance)
    if element.family in {"acceptance_constraints", "non_functional_requirements"}:
        return f"Satisfy constraint: {label}"
    if element.family in {"domain_invariants", "state_invariants"}:
        return f"Enforce invariant: {label}"
    if element.family == "state_transitions":
        return f"Implement lifecycle transition: {label}"
    if element.family == "functional_requirements":
        return f"Implement workflow support: {label}"
    if element.family == "scenarios":
        return f"Implement scenario handling: {label}"
    if element.family == "guard_conditions":
        return f"Implement guard enforcement: {label}"
    if element.family == "use_cases":
        return f"Implement use case: {label}"
    if element.family == "use_case_steps":
        return f"Implement use-case step: {label}"
    return f"Implement {label}"


def _implementation_summary(element: RupifyElement, title: str, summary: str, acceptance: str) -> str:
    """Derive a more usable implementation summary."""
    label = _best_delivery_label(element, title, summary, acceptance)
    if element.family in {"acceptance_constraints", "non_functional_requirements"}:
        return f"Deliver behavior that satisfies the constraint '{acceptance}'."
    if element.family in {"domain_invariants", "state_invariants"}:
        return f"Ensure the invariant '{acceptance}' is enforced in the implemented behavior."
    if element.family == "state_transitions":
        return summary
    if element.family == "functional_requirements":
        return f"Deliver workflow behavior for {label.lower()}: {summary.rstrip('.') }."
    if element.family == "use_cases":
        return f"Deliver the use-case behavior for {label.lower()}: {summary.rstrip('.') }."
    if element.family == "use_case_steps":
        return f"Deliver the ordered step behavior for {label.lower()}: {summary.rstrip('.') }."
    if element.family in {"scenarios", "guard_conditions"}:
        return f"Deliver the source-defined behavior for {label.lower()}: {summary.rstrip('.') }."
    return f"Implement the source-defined behavior for {label.lower()}: {acceptance.rstrip('.') }."


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
    expected_outcomes = [f"The required behavior is delivered: {acceptance}"]
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

    elif element.family == "scenarios":
        verification_intent = f"Confirm the scenario handling behaves correctly for {title.lower()}."
        setup_requirements = ["The system is placed in the exceptional or degraded condition described by the scenario."]
        expected_outcomes = [f"The scenario outcome is handled correctly: {acceptance}"]
        failure_conditions = [f"The scenario handling is missing or incorrect: {acceptance}"]

    elif element.family == "guard_conditions":
        verification_intent = f"Confirm the guard enforcement is applied for {title.lower()}."
        setup_requirements = ["A request reaches the boundary where the guard condition must be checked."]
        expected_outcomes = [f"The guard enforcement is applied correctly: {acceptance}"]
        failure_conditions = [f"The guard condition is not enforced as required: {acceptance}"]

    elif element.family == "use_cases":
        verification_intent = f"Confirm the use-case behavior is delivered for {title.lower()}."
        setup_requirements = ["A representative invocation reaches the start of the use case."]
        expected_outcomes = [f"The end-to-end use-case behavior is completed as specified: {acceptance}"]
        failure_conditions = [f"The use-case behavior is incomplete or incorrect: {acceptance}"]

    elif element.family == "use_case_steps":
        verification_intent = f"Confirm the use-case step is delivered for {title.lower()}."
        setup_requirements = ["The workflow is positioned at the step where this behavior should occur."]
        expected_outcomes = [f"The step completes with the expected behavior: {acceptance}"]
        failure_conditions = [f"The step behavior does not occur as required: {acceptance}"]

    if not setup_requirements:
        setup_requirements = [
            "A representative invocation reaches the source-defined behavior boundary for this unit."
        ]
    if not expected_outcomes:
        expected_outcomes = [f"The required behavior is delivered: {acceptance}"]
    if not failure_conditions:
        failure_conditions = [f"The required behavior is not delivered: {acceptance}"]

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
    export: RupifyPlanningExport,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive dependency edges, assembly rules, and updated implementation units."""
    implementation_index = {item["id"]: item for item in implementation_units}
    dependency_edges: list[dict[str, Any]] = []
    assembly_rules: list[dict[str, Any]] = []

    source_groups: dict[str, list[dict[str, Any]]] = {}
    for item in implementation_units:
        source_anchor_id = item["source_anchor_ids"][0]
        source_groups.setdefault(source_anchor_id, []).append(item)

    for source_anchor_id, members in source_groups.items():
        if source_anchor_id.startswith("anchor.rupify.scenarios.") and len(members) > 1:
            for previous, current in zip(members, members[1:]):
                current["dependencies"].append(previous["id"])
                dependency_edges.append(
                    {
                        "id": f"dep.{current['id'].replace('iu.', '')}.requires-{previous['id'].replace('iu.', '')}",
                        "from_implementation_unit_id": current["id"],
                        "to_implementation_unit_id": previous["id"],
                        "dependency_type": "requires",
                        "reason": "Later scenario flow segments depend on earlier explicit flow segments.",
                    }
                )

            assembly_rules.append(
                {
                    "id": f"assembly.{source_anchor_id.split('.')[-1]}",
                    "source_anchor_ids": [source_anchor_id],
                    "member_spec_unit_ids": [
                        spec_id
                        for item in members
                        for spec_id in item["derived_from_spec_unit_ids"]
                    ],
                    "rule_type": "ordered_sequence",
                    "notes": [
                        "Recombine explicit scenario flow segments into the original scenario.",
                    ],
                }
            )
            continue

        if len(members) > 1 and not source_anchor_id.startswith("anchor.rupify.state-transitions."):
            assembly_rules.append(
                {
                    "id": f"assembly.{source_anchor_id.split('.')[-1]}",
                    "source_anchor_ids": [source_anchor_id],
                    "member_spec_unit_ids": [
                        spec_id
                        for item in members
                        for spec_id in item["derived_from_spec_unit_ids"]
                    ],
                    "rule_type": "conjunctive_set",
                    "notes": [
                        "Recombine explicitly structured sub-obligations into the original source element.",
                    ],
                }
            )
            continue

        if source_anchor_id.startswith("anchor.rupify.state-transitions.") and len(members) > 1:
            ordered_units = members

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

    elements_by_id = {element.id: element for element in export.elements}
    anchor_by_element_id = {element_id: _anchor_id(element) for element_id, element in elements_by_id.items()}

    def add_dependency(
        from_id: str,
        to_id: str,
        dependency_type: str,
        reason: str,
    ) -> None:
        """Add a deterministic dependency edge when both units exist."""
        if from_id not in implementation_index or to_id not in implementation_index:
            return
        if to_id not in implementation_index[from_id]["dependencies"]:
            implementation_index[from_id]["dependencies"].append(to_id)

        edge_id = (
            f"dep.{from_id.replace('iu.', '')}.{dependency_type}-{to_id.replace('iu.', '')}"
        )
        if any(item["id"] == edge_id for item in dependency_edges):
            return
        dependency_edges.append(
            {
                "id": edge_id,
                "from_implementation_unit_id": from_id,
                "to_implementation_unit_id": to_id,
                "dependency_type": dependency_type,
                "reason": reason,
            }
        )

    def implementation_ids_for_element(element_id: str) -> list[str]:
        """Resolve generated implementation ids for one source element."""
        anchor_id = anchor_by_element_id.get(element_id, "")
        if not anchor_id:
            return []
        return [
            item["id"]
            for item in implementation_units
            if item["source_anchor_ids"] == [anchor_id]
        ]

    def ordered_use_case_step_groups() -> list[list[list[str]]]:
        """Collect ordered step groups for each use case."""
        grouped_steps: dict[str, dict[int, list[str]]] = {}
        for element in export.elements:
            if element.family != "use_case_steps" or not element.normative_ready:
                continue
            if "-step-" not in element.id:
                continue
            prefix, step_number = element.id.rsplit("-step-", 1)
            if not step_number.isdigit():
                continue
            step_ids = implementation_ids_for_element(element.id)
            if not step_ids:
                continue
            grouped_steps.setdefault(prefix, {})[int(step_number)] = step_ids

        ordered_groups: list[list[list[str]]] = []
        for prefix in sorted(grouped_steps):
            ordered_groups.append(
                [grouped_steps[prefix][number] for number in sorted(grouped_steps[prefix])]
            )
        return ordered_groups

    for step_groups in ordered_use_case_step_groups():
        for previous_ids, current_ids in zip(step_groups, step_groups[1:]):
            for current_id in current_ids:
                for previous_id in previous_ids:
                    add_dependency(
                        current_id,
                        previous_id,
                        "requires",
                        "Later use-case steps depend on the earlier step in the same ordered flow.",
                    )

    for trace_link in export.trace_links:
        link_type = str(trace_link.raw.get("link_type", ""))

        if link_type == "acceptance_constraint_to_requirement":
            for from_id in implementation_ids_for_element(trace_link.from_id):
                for to_id in implementation_ids_for_element(trace_link.to_id):
                    add_dependency(
                        from_id,
                        to_id,
                        "soft_sequence",
                        "Acceptance-constraint work should follow the linked underlying requirement.",
                    )

        if link_type == "requirement_to_use_case":
            for from_id in implementation_ids_for_element(trace_link.to_id):
                for to_id in implementation_ids_for_element(trace_link.from_id):
                    add_dependency(
                        from_id,
                        to_id,
                        "soft_sequence",
                        "Use-case implementation should follow the linked requirement intent.",
                    )

        if link_type == "guard_to_transition":
            for transition_id in implementation_ids_for_element(trace_link.to_id):
                for guard_id in implementation_ids_for_element(trace_link.from_id):
                    add_dependency(
                        transition_id,
                        guard_id,
                        "requires",
                        "Transition implementation depends on the linked guard condition.",
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
                    "title": _implementation_title(element, title, summary, acceptance),
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
        export,
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
            "decomposition_profile": "rupify-structural-decomposition-v1",
        },
        "source_summary": {
            "source_system": "rupify",
            "project_id": project_id,
            "project_name": source_model_id or project_id,
            "export_version": export.raw.get("export_metadata", {}).get("schema_version", 1),
            "notes": [
                "Generated directly from imported Rupify planning export records.",
                "Deterministic decomposition splits selected ready normative source elements into smaller planning units.",
                "Dependency edges and assembly rules are derived for split workflow, scenario, guard, and transition structures.",
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
