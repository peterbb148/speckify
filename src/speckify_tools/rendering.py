"""Render human-readable artifacts from Speckify planning bundles."""

from __future__ import annotations

from typing import Any


def _index_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index bundle items by id."""
    return {item["id"]: item for item in items}


def render_issue_body(
    implementation_unit: dict[str, Any],
    verification_units: list[dict[str, Any]],
    source_anchors: dict[str, dict[str, Any]],
    dependency_edges: list[dict[str, Any]],
) -> str:
    """Render a deterministic issue body for one implementation unit."""
    lines = [
        "## Summary",
        "",
        implementation_unit["summary"],
        "",
        "## Source Lineage",
        "",
    ]
    for anchor_id in implementation_unit.get("source_anchor_ids", []):
        lines.append(f"- `{anchor_id}`")

    lines.extend(["", "## Scope", ""])
    for item in implementation_unit.get("implementation_scope", []):
        lines.append(f"- {item}")

    non_goals = implementation_unit.get("non_goals", [])
    if non_goals:
        lines.extend(["", "## Non-goals", ""])
        for item in non_goals:
            lines.append(f"- {item}")

    constraints = implementation_unit.get("constraints", [])
    if constraints:
        lines.extend(["", "## Constraints", ""])
        for item in constraints:
            lines.append(f"- {item}")

    lines.extend(["", "## Acceptance Criteria", ""])
    for item in implementation_unit.get("acceptance_criteria", []):
        lines.append(f"- {item}")

    lines.extend(["", "## Verification Shape", ""])
    linked_units = {
        item["id"]: item
        for item in verification_units
        if item["id"] in implementation_unit.get("verification_unit_ids", [])
    }
    for verification_unit_id in implementation_unit.get("verification_unit_ids", []):
        verification_unit = linked_units[verification_unit_id]
        lines.append(f"- Intent: {verification_unit['verification_intent']}")
        for item in verification_unit.get("observables", []):
            lines.append(f"- Observable: {item}")
        for item in verification_unit.get("setup_requirements", []):
            lines.append(f"- Setup requirement: {item}")
        for item in verification_unit.get("expected_outcomes", []):
            lines.append(f"- Expected outcome: {item}")
        for item in verification_unit.get("failure_conditions", []):
            lines.append(f"- Failure condition: {item}")

    lines.extend(["", "## Dependencies", ""])
    dependencies = implementation_unit.get("dependencies", [])
    if dependencies:
        for dependency in dependencies:
            reason = next(
                (
                    edge.get("reason", "")
                    for edge in dependency_edges
                    if edge.get("from_implementation_unit_id") == implementation_unit["id"]
                    and edge.get("to_implementation_unit_id") == dependency
                ),
                "",
            )
            if reason:
                lines.append(f"- `{dependency}`: {reason}")
            else:
                lines.append(f"- `{dependency}`")
    else:
        lines.append("- None")

    drift_checks = implementation_unit.get("drift_checks", [])
    if drift_checks:
        lines.extend(["", "## Drift Checks", ""])
        for item in drift_checks:
            lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def render_issue_projections(bundle: dict[str, Any]) -> list[dict[str, str]]:
    """Render all issue projections for a planning bundle."""
    source_anchors = _index_by_id(bundle.get("source_anchors", []))
    verification_units = bundle.get("verification_units", [])
    dependency_edges = bundle.get("dependency_edges", [])

    projections: list[dict[str, str]] = []
    for implementation_unit in bundle.get("implementation_units", []):
        projections.append(
            {
                "implementation_unit_id": implementation_unit["id"],
                "issue_title": implementation_unit["title"],
                "issue_body": render_issue_body(
                    implementation_unit,
                    verification_units,
                    source_anchors,
                    dependency_edges,
                ),
            }
        )
    return projections


def render_specification_markdown(bundle: dict[str, Any]) -> str:
    """Render a consolidated specification view from a planning bundle."""
    source_summary = bundle["source_summary"]
    lines = [
        "# Speckified Specification",
        "",
        f"Project: `{source_summary['project_id']}`",
        "",
        "## Overview",
        "",
        f"- Source system: `{source_summary['source_system']}`",
        f"- Generated implementation units: {len(bundle.get('implementation_units', []))}",
        f"- Generated verification units: {len(bundle.get('verification_units', []))}",
        f"- Trace bundles: {len(bundle.get('trace_bundles', []))}",
        "",
        "## Implementation Units",
        "",
    ]

    for implementation_unit in bundle.get("implementation_units", []):
        lines.append(f"### {implementation_unit['title']}")
        lines.append("")
        lines.append(f"- ID: `{implementation_unit['id']}`")
        lines.append(f"- Summary: {implementation_unit['summary']}")
        lines.append("- Source lineage:")
        for anchor_id in implementation_unit.get("source_anchor_ids", []):
            lines.append(f"  - `{anchor_id}`")
        lines.append("- Acceptance criteria:")
        for criterion in implementation_unit.get("acceptance_criteria", []):
            lines.append(f"  - {criterion}")
        lines.append("")

    return "\n".join(lines) + "\n"
