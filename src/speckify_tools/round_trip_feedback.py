"""Generate structured round-trip feedback artifacts for Rupify."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .quality_review import analyze_bundle_quality


UPSTREAM_WARNING_KINDS = {
    "very_short_acceptance",
    "abstract_success_criterion",
    "weak_verification_distinction",
}


def _index_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index records by id."""
    return {item["id"]: item for item in items}


def _trace_bundles_by_implementation_id(bundle: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Index trace bundles by implementation unit membership."""
    by_implementation: dict[str, list[dict[str, Any]]] = {}
    for trace_bundle in bundle.get("trace_bundles", []):
        for implementation_unit_id in trace_bundle.get("implementation_unit_ids", []):
            by_implementation.setdefault(implementation_unit_id, []).append(trace_bundle)
    return by_implementation


def _impact_scope_for_warning(warning_kind: str) -> str:
    """Classify a warning as planning-only or upstream-affecting."""
    if warning_kind in UPSTREAM_WARNING_KINDS:
        return "upstream_affecting"
    return "planning_only"


def _change_class_for_warning(warning_kind: str) -> str:
    """Map a warning kind to a reversibility change class."""
    if warning_kind in UPSTREAM_WARNING_KINDS:
        return "spec_clarification"
    return "verification_refinement"


def _feedback_summary(implementation_unit: dict[str, Any], warning: dict[str, str]) -> str:
    """Build a deterministic summary for one change record."""
    return f"{implementation_unit['title']}: {warning['message']}"


def _recommended_actions_for_warning(warning_kind: str, anchor_ids: list[str]) -> list[str]:
    """Return deterministic recommended actions for one warning kind."""
    anchor_text = ", ".join(anchor_ids)
    if warning_kind == "generic_title":
        return [
            f"Refine downstream rendering and naming for source anchors: {anchor_text}.",
        ]
    if warning_kind == "very_short_acceptance":
        return [
            "Clarify the acceptance constraint upstream with concrete behavioral detail.",
            f"Preserve the trace link to source anchors: {anchor_text}.",
        ]
    if warning_kind == "abstract_success_criterion":
        return [
            "Refine the upstream success criterion into more concrete normative constraints.",
            f"Preserve the trace link to source anchors: {anchor_text}.",
        ]
    return [
        "Clarify the upstream constraint or invariant so verification intent is independently testable.",
        f"Preserve the trace link to source anchors: {anchor_text}.",
    ]


def _feedback_type_for_warning(warning_kind: str) -> str:
    """Map an upstream-affecting warning to a feedback category."""
    if warning_kind == "abstract_success_criterion":
        return "split_element"
    return "clarify_element"


def build_round_trip_feedback(bundle: dict[str, Any]) -> dict[str, Any]:
    """Build round-trip change records and upstream feedback proposals.

    Args:
        bundle: Generated planning bundle.

    Returns:
        Structured round-trip artifact set.
    """
    quality_report = analyze_bundle_quality(bundle)
    implementation_units = _index_by_id(bundle.get("implementation_units", []))
    source_anchors = _index_by_id(bundle.get("source_anchors", []))
    trace_bundles_by_implementation = _trace_bundles_by_implementation_id(bundle)

    change_records: list[dict[str, Any]] = []
    feedback_proposals: list[dict[str, Any]] = []

    for warning in quality_report.get("warnings", []):
        implementation_unit = implementation_units[warning["implementation_unit_id"]]
        implementation_unit_id = implementation_unit["id"]
        trace_bundles = trace_bundles_by_implementation.get(implementation_unit_id, [])
        trace_bundle_ids = [item["id"] for item in trace_bundles]
        spec_unit_ids = sorted(
            {
                spec_unit_id
                for trace_bundle in trace_bundles
                for spec_unit_id in trace_bundle.get("spec_unit_ids", [])
            }
        )
        source_anchor_ids = implementation_unit.get("source_anchor_ids", [])
        target_source_ids = [
            source_anchors[anchor_id]["source_id"]
            for anchor_id in source_anchor_ids
            if anchor_id in source_anchors
        ]
        impact_scope = _impact_scope_for_warning(warning["kind"])
        change_class = _change_class_for_warning(warning["kind"])
        recommended_actions = _recommended_actions_for_warning(
            warning["kind"],
            source_anchor_ids,
        )
        change_record_id = (
            f"change.{implementation_unit_id}.{warning['kind']}".replace("_", "-")
        )

        change_record = {
            "id": change_record_id,
            "impact_scope": impact_scope,
            "change_class": change_class,
            "warning_kind": warning["kind"],
            "summary": _feedback_summary(implementation_unit, warning),
            "affected_implementation_unit_ids": [implementation_unit_id],
            "affected_verification_unit_ids": implementation_unit.get("verification_unit_ids", []),
            "source_anchor_ids": source_anchor_ids,
            "trace_bundle_ids": trace_bundle_ids,
            "evidence": [warning["message"]],
            "recommended_action": recommended_actions,
            "status": "proposed",
        }
        change_records.append(change_record)

        if impact_scope != "upstream_affecting":
            continue

        feedback_proposals.append(
            {
                "id": change_record_id.replace("change.", "feedback.", 1),
                "feedback_type": _feedback_type_for_warning(warning["kind"]),
                "change_record_id": change_record_id,
                "summary": change_record["summary"],
                "target_source_ids": target_source_ids,
                "source_anchor_ids": source_anchor_ids,
                "reason": warning["message"],
                "proposed_upstream_action": recommended_actions,
                "impact": {
                    "affected_spec_unit_ids": spec_unit_ids,
                    "affected_implementation_unit_ids": [implementation_unit_id],
                    "affected_verification_unit_ids": implementation_unit.get(
                        "verification_unit_ids",
                        [],
                    ),
                },
                "status": "proposed",
            }
        )

    round_trip_status = {
        "change_record_count": len(change_records),
        "feedback_proposal_count": len(feedback_proposals),
        "planning_only_findings": sum(
            1 for item in change_records if item["impact_scope"] == "planning_only"
        ),
        "upstream_affecting_findings": sum(
            1 for item in change_records if item["impact_scope"] == "upstream_affecting"
        ),
        "open_spec_clarifications": sum(
            1 for item in change_records if item["change_class"] == "spec_clarification"
        ),
        "open_spec_conflicts": 0,
    }

    return {
        "export_metadata": {
            "export_kind": "speckify_round_trip_feedback",
            "bundle_id": bundle["bundle_metadata"]["bundle_id"],
            "generated_at": bundle["bundle_metadata"]["generated_at"],
            "source_system": bundle["source_summary"]["source_system"],
            "project_id": bundle["source_summary"]["project_id"],
        },
        "change_records": change_records,
        "feedback_proposals": feedback_proposals,
        "round_trip_status": round_trip_status,
    }


def render_round_trip_feedback_markdown(feedback_export: dict[str, Any]) -> str:
    """Render a Markdown summary of round-trip feedback artifacts."""
    status = feedback_export["round_trip_status"]
    lines = [
        "# Round-Trip Feedback Report",
        "",
        f"- Change records: {status['change_record_count']}",
        f"- Feedback proposals: {status['feedback_proposal_count']}",
        f"- Planning-only findings: {status['planning_only_findings']}",
        f"- Upstream-affecting findings: {status['upstream_affecting_findings']}",
        "",
        "## Feedback Proposals",
        "",
    ]
    if not feedback_export["feedback_proposals"]:
        lines.append("- None")
    else:
        for proposal in feedback_export["feedback_proposals"]:
            lines.append(
                f"- `{proposal['id']}` [{proposal['feedback_type']}] {proposal['summary']}"
            )
    return "\n".join(lines) + "\n"


def write_round_trip_feedback_artifacts(bundle: dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    """Write round-trip feedback artifacts for a planning bundle.

    Args:
        bundle: Generated planning bundle.
        output_dir: Target directory for output artifacts.

    Returns:
        Structured round-trip feedback export.
    """
    feedback_export = build_round_trip_feedback(bundle)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "change-records.json").write_text(
        json.dumps(feedback_export["change_records"], indent=2) + "\n"
    )
    (target / "feedback-proposals.json").write_text(
        json.dumps(feedback_export["feedback_proposals"], indent=2) + "\n"
    )
    (target / "round-trip-status.json").write_text(
        json.dumps(feedback_export["round_trip_status"], indent=2) + "\n"
    )
    (target / "README.md").write_text(render_round_trip_feedback_markdown(feedback_export))
    return feedback_export
