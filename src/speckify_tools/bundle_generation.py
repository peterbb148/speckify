"""Generate Speckify planning bundles from imported Rupify exports."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
        spec_unit_id = _spec_unit_id(element)
        implementation_unit_id = _implementation_unit_id(element)
        verification_unit_id = _verification_unit_id(element)
        trace_bundle_id = _trace_bundle_id(element)
        view, source_type = _view_and_source_type(element)
        title = _element_title(element)
        summary = _element_summary(element)

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
                "title": f"Implement {title}",
                "summary": f"Implement the planned behavior for {element.id}.",
                "derived_from_spec_unit_ids": [spec_unit_id],
                "source_anchor_ids": [anchor_id],
                "dependencies": [],
                "implementation_scope": [summary],
                "non_goals": [],
                "constraints": [],
                "acceptance_criteria": [summary],
                "verification_unit_ids": [verification_unit_id],
                "drift_checks": [f"Preserve lineage to Rupify element {element.id}."],
                "reverse_impact_hint": f"Changes here may require upstream review of {element.id}.",
                "labels": ["planning", _slug(element.family)],
            }
        )

        verification_units.append(
            {
                "id": verification_unit_id,
                "implementation_unit_id": implementation_unit_id,
                "title": f"Verify {title}",
                "verification_intent": f"Confirm the implementation satisfies {element.id}.",
                "source_anchor_ids": [anchor_id],
                "observables": [summary],
                "setup_requirements": [],
                "expected_outcomes": [summary],
                "failure_conditions": [],
                "invariants_preserved": [],
                "notes": [f"First-pass verification contract derived directly from {element.id}."],
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
                "notes": [f"One-source-to-one-planning-unit derivation for {element.id}."],
            }
        )

    unresolved_ambiguities = [
        {
            "ambiguity_id": ambiguity_id,
            "status": "unresolved",
            "blocking": True,
        }
        for ambiguity_id in export.summary.raw.get("blocking_ambiguity_ids", [])
    ]

    return {
        "bundle_metadata": {
            "bundle_id": f"bundle.{project_id}",
            "schema_version": 1,
            "bundle_version": 1,
            "generated_at": generated_at,
            "source_model_id": source_model_id or project_id,
            "source_model_version": source_model_version,
            "decomposition_profile": "rupify-one-to-one-v1",
        },
        "source_summary": {
            "source_system": "rupify",
            "project_id": project_id,
            "project_name": source_model_id or project_id,
            "export_version": export.raw.get("export_metadata", {}).get("schema_version", 1),
            "notes": [
                "Generated directly from imported Rupify planning export records.",
                "First-pass mapping uses one ready normative source element to one planning unit.",
            ],
        },
        "source_anchors": source_anchors,
        "spec_units": spec_units,
        "implementation_units": implementation_units,
        "verification_units": verification_units,
        "trace_bundles": trace_bundles,
        "dependency_edges": [],
        "assembly_rules": [],
        "unresolved_ambiguities": unresolved_ambiguities,
        "rendered_issues": [],
    }


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
