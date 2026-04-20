"""Export generated planning artifacts into GitHub-delivery-ready outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _index_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index records by id."""
    return {item["id"]: item for item in items}


def _index_rendered_issues(bundle: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Index rendered issues by implementation unit id."""
    return {
        item["implementation_unit_id"]: item
        for item in bundle.get("rendered_issues", [])
    }


def _github_labels(implementation_unit: dict[str, Any], source_summary: dict[str, Any]) -> list[str]:
    """Derive deterministic GitHub labels for one implementation unit."""
    labels = ["speckify", "planning", f"source:{source_summary['source_system']}"]
    labels.extend(label for label in implementation_unit.get("labels", []) if label != "planning")
    return labels


def build_github_delivery_export(bundle: dict[str, Any]) -> dict[str, Any]:
    """Build a GitHub-delivery export from a planning bundle.

    Args:
        bundle: Generated planning bundle.

    Returns:
        Machine-readable export describing issue-ready delivery payloads.
    """
    implementation_units = _index_by_id(bundle.get("implementation_units", []))
    rendered_issues = _index_rendered_issues(bundle)
    source_summary = bundle["source_summary"]

    issues: list[dict[str, Any]] = []
    for implementation_unit_id in sorted(rendered_issues):
        implementation_unit = implementation_units[implementation_unit_id]
        rendered_issue = rendered_issues[implementation_unit_id]
        issues.append(
            {
                "implementation_unit_id": implementation_unit_id,
                "issue_slug": implementation_unit_id.replace(".", "-"),
                "title": rendered_issue["issue_title"],
                "body_markdown": rendered_issue["issue_body"],
                "labels": _github_labels(implementation_unit, source_summary),
                "dependency_ids": implementation_unit.get("dependencies", []),
                "source_anchor_ids": implementation_unit.get("source_anchor_ids", []),
                "verification_unit_ids": implementation_unit.get("verification_unit_ids", []),
                "reverse_impact_hint": implementation_unit.get("reverse_impact_hint", ""),
            }
        )

    return {
        "export_metadata": {
            "export_kind": "speckify_github_delivery_export",
            "bundle_id": bundle["bundle_metadata"]["bundle_id"],
            "generated_at": bundle["bundle_metadata"]["generated_at"],
            "source_system": source_summary["source_system"],
            "project_id": source_summary["project_id"],
        },
        "issues": issues,
    }


def render_github_delivery_readme(delivery_export: dict[str, Any]) -> str:
    """Render a short README for GitHub delivery artifacts."""
    metadata = delivery_export["export_metadata"]
    lines = [
        "# GitHub Delivery Export",
        "",
        f"- Export kind: `{metadata['export_kind']}`",
        f"- Bundle id: `{metadata['bundle_id']}`",
        f"- Source system: `{metadata['source_system']}`",
        f"- Project id: `{metadata['project_id']}`",
        f"- Issue count: {len(delivery_export.get('issues', []))}",
        "",
        "## Files",
        "",
        "- `issues.json`: machine-readable issue export for batch delivery workflows",
        "- `issue-bodies/*.md`: per-issue Markdown bodies aligned to the rendered planning issues",
        "",
    ]
    return "\n".join(lines) + "\n"


def write_github_delivery_artifacts(bundle: dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    """Write GitHub delivery artifacts for a planning bundle.

    Args:
        bundle: Generated planning bundle.
        output_dir: Target directory for delivery export artifacts.

    Returns:
        The machine-readable GitHub delivery export.
    """
    delivery_export = build_github_delivery_export(bundle)
    target = Path(output_dir)
    issue_bodies_dir = target / "issue-bodies"
    issue_bodies_dir.mkdir(parents=True, exist_ok=True)

    for existing_issue in issue_bodies_dir.glob("*.md"):
        existing_issue.unlink()

    (target / "issues.json").write_text(json.dumps(delivery_export, indent=2) + "\n")
    (target / "README.md").write_text(render_github_delivery_readme(delivery_export))

    for issue in delivery_export["issues"]:
        (issue_bodies_dir / f"{issue['issue_slug']}.md").write_text(issue["body_markdown"])

    return delivery_export
