"""Issue-ready quality gates for GitHub delivery exports."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


RAW_SOURCE_IDENTIFIER_RE = re.compile(r"\b[a-z]+(?:[_-][a-z0-9]+)*-\d+\b")
GENERIC_ORDINAL_TITLE_RE = re.compile(
    r"\b(?:Requirement|Constraint|Scenario|Use Case|Guard Condition|Success Criterion) \d+\b"
)

REQUIRED_BODY_SECTIONS = (
    "## Delivery Metadata",
    "## Summary",
    "## Source Lineage",
    "## Scope",
    "## Acceptance Criteria",
    "## Verification Shape",
    "## Drift Checks",
)

REQUIRED_VERIFICATION_PREFIXES = (
    "- Intent:",
    "- Observable:",
    "- Setup requirement:",
    "- Expected outcome:",
    "- Failure condition:",
)

GATE_DEFINITIONS = [
    {
        "id": "title_avoids_raw_source_identifiers",
        "kind": "issue",
        "description": "Titles must not expose raw source-style identifiers.",
    },
    {
        "id": "title_avoids_generic_ordinals",
        "kind": "issue",
        "description": "Titles must not rely on generic ordinal labels such as Requirement 1.",
    },
    {
        "id": "summary_is_substantive",
        "kind": "issue",
        "description": "Summaries must provide enough implementation context to stand on their own.",
    },
    {
        "id": "body_sections_present",
        "kind": "issue",
        "description": "Delivery bodies must contain the required planning and lineage sections.",
    },
    {
        "id": "acceptance_criteria_are_present",
        "kind": "issue",
        "description": "Each issue body must include at least one acceptance criterion.",
    },
    {
        "id": "verification_shape_is_complete",
        "kind": "issue",
        "description": "Verification guidance must include intent, observable, setup, expected outcome, and failure condition.",
    },
    {
        "id": "verification_shape_is_distinct",
        "kind": "issue",
        "description": "Observable and expected outcome must not collapse to identical text.",
    },
    {
        "id": "lineage_is_visible",
        "kind": "issue",
        "description": "Source anchors and verification units must be visible in the delivery export.",
    },
    {
        "id": "create_payload_is_complete",
        "kind": "issue",
        "description": "Create payloads must include title, body path, and at least one label.",
    },
    {
        "id": "dependencies_are_explained",
        "kind": "issue",
        "description": "Dependency metadata must stay aligned with the body and include human-readable titles.",
    },
    {
        "id": "all_issues_pass",
        "kind": "bundle",
        "description": "A bundle is publication-ready only if every exported issue passes all issue-level gates.",
    },
]


def _extract_section(body: str, section_heading: str) -> str:
    """Extract one Markdown section body.

    Args:
        body: Full Markdown body.
        section_heading: Heading to extract, including leading hashes.

    Returns:
        Section content, or an empty string when the section is not present.
    """
    pattern = rf"{re.escape(section_heading)}\n\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, body, flags=re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def _extract_verification_lines(body: str) -> dict[str, str]:
    """Index verification lines by label prefix.

    Args:
        body: Full delivery issue body.

    Returns:
        Mapping from verification label to text value.
    """
    verification_body = _extract_section(body, "## Verification Shape")
    values: dict[str, str] = {}
    for prefix in REQUIRED_VERIFICATION_PREFIXES:
        label = prefix.removeprefix("- ").removesuffix(":")
        pattern = rf"^{re.escape(prefix)}\s*(.+)$"
        match = re.search(pattern, verification_body, flags=re.MULTILINE)
        values[label] = match.group(1).strip() if match else ""
    return values


def _append_failure(
    failures: list[dict[str, str]],
    gate_id: str,
    message: str,
) -> None:
    """Append one gate failure.

    Args:
        failures: Mutable failure list.
        gate_id: Gate identifier.
        message: Human-readable failure reason.
    """
    failures.append({"gate_id": gate_id, "message": message})


def assess_delivery_issue_readiness(issue: dict[str, Any]) -> dict[str, Any]:
    """Assess one delivery export issue against the issue-ready gates.

    Args:
        issue: One exported delivery issue.

    Returns:
        Assessment containing pass/fail status and individual gate failures.
    """
    body = issue["body_markdown"]
    title = issue["title"]
    summary = _extract_section(body, "## Summary")
    acceptance_section = _extract_section(body, "## Acceptance Criteria")
    verification_lines = _extract_verification_lines(body)

    failures: list[dict[str, str]] = []

    if RAW_SOURCE_IDENTIFIER_RE.search(title):
        _append_failure(
            failures,
            "title_avoids_raw_source_identifiers",
            f"Title exposes a raw source-style identifier: {title}",
        )

    if GENERIC_ORDINAL_TITLE_RE.search(title):
        _append_failure(
            failures,
            "title_avoids_generic_ordinals",
            f"Title still depends on a generic ordinal label: {title}",
        )

    if len(summary) < 45:
        _append_failure(
            failures,
            "summary_is_substantive",
            f"Summary is too short to stand alone: {summary or '<missing>'}",
        )

    missing_sections = [
        section for section in REQUIRED_BODY_SECTIONS if section not in body
    ]
    if missing_sections:
        _append_failure(
            failures,
            "body_sections_present",
            "Missing required body sections: " + ", ".join(missing_sections),
        )

    acceptance_lines = [
        line.strip()
        for line in acceptance_section.splitlines()
        if line.strip().startswith("- ")
    ]
    if not acceptance_lines:
        _append_failure(
            failures,
            "acceptance_criteria_are_present",
            "Acceptance criteria section does not include any bullet criteria.",
        )

    missing_verification = [
        label
        for label, value in verification_lines.items()
        if not value
    ]
    if missing_verification:
        _append_failure(
            failures,
            "verification_shape_is_complete",
            "Verification shape is missing: " + ", ".join(missing_verification),
        )

    observable = verification_lines.get("Observable", "")
    expected = verification_lines.get("Expected outcome", "")
    if observable and expected and observable == expected:
        _append_failure(
            failures,
            "verification_shape_is_distinct",
            "Observable and expected outcome are identical.",
        )

    if not issue.get("source_anchor_ids") or not issue.get("verification_unit_ids"):
        _append_failure(
            failures,
            "lineage_is_visible",
            "Delivery export is missing source anchors or verification unit ids.",
        )

    create_payload = issue.get("create_payload", {})
    if not create_payload.get("title") or not create_payload.get("body_path") or not create_payload.get("labels"):
        _append_failure(
            failures,
            "create_payload_is_complete",
            "Create payload must include title, body path, and labels.",
        )

    dependency_ids = issue.get("dependency_ids", [])
    dependency_titles = issue.get("dependency_titles", [])
    if len(dependency_ids) != len(dependency_titles):
        _append_failure(
            failures,
            "dependencies_are_explained",
            "Dependency ids and dependency titles are out of sync.",
        )
    for dependency in dependency_titles:
        if not dependency.get("title"):
            _append_failure(
                failures,
                "dependencies_are_explained",
                "A dependency is missing its human-readable title.",
            )
            break
    if dependency_ids and "## Dependencies" not in body:
        _append_failure(
            failures,
            "dependencies_are_explained",
            "Issue has dependencies but no Dependencies section in the body.",
        )

    return {
        "implementation_unit_id": issue["implementation_unit_id"],
        "title": title,
        "ready": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }


def assess_delivery_export_readiness(delivery_export: dict[str, Any]) -> dict[str, Any]:
    """Assess a GitHub delivery export against publication-quality gates.

    Args:
        delivery_export: GitHub delivery export built from a planning bundle.

    Returns:
        Bundle-level issue-ready assessment.
    """
    issues = [
        assess_delivery_issue_readiness(issue)
        for issue in delivery_export.get("issues", [])
    ]
    failed_issues = [issue for issue in issues if not issue["ready"]]
    bundle_failures: list[dict[str, str]] = []
    if failed_issues:
        bundle_failures.append(
            {
                "gate_id": "all_issues_pass",
                "message": (
                    "Bundle is not publication-ready because "
                    f"{len(failed_issues)} issue(s) failed at least one gate."
                ),
            }
        )

    metadata = delivery_export["export_metadata"]
    return {
        "bundle_id": metadata["bundle_id"],
        "project_id": metadata["project_id"],
        "source_system": metadata["source_system"],
        "issue_count": len(issues),
        "ready_issue_count": len(issues) - len(failed_issues),
        "failed_issue_count": len(failed_issues),
        "publication_ready": not bundle_failures,
        "gate_definitions": GATE_DEFINITIONS,
        "bundle_failures": bundle_failures,
        "issues": issues,
    }


def render_delivery_readiness_markdown(report: dict[str, Any]) -> str:
    """Render a Markdown summary of issue-ready gate results.

    Args:
        report: Delivery readiness report.

    Returns:
        Human-readable Markdown report.
    """
    lines = [
        "# Delivery Readiness Report",
        "",
        f"- Bundle id: `{report['bundle_id']}`",
        f"- Project id: `{report['project_id']}`",
        f"- Source system: `{report['source_system']}`",
        f"- Issue count: {report['issue_count']}",
        f"- Ready issue count: {report['ready_issue_count']}",
        f"- Failed issue count: {report['failed_issue_count']}",
        f"- Publication ready: {'yes' if report['publication_ready'] else 'no'}",
        "",
        "## Bundle Failures",
        "",
    ]
    if not report["bundle_failures"]:
        lines.append("- None")
    else:
        for failure in report["bundle_failures"]:
            lines.append(f"- [{failure['gate_id']}] {failure['message']}")

    lines.extend(["", "## Issue Failures", ""])
    failed_issues = [issue for issue in report["issues"] if not issue["ready"]]
    if not failed_issues:
        lines.append("- None")
    else:
        for issue in failed_issues:
            lines.append(f"### `{issue['implementation_unit_id']}`")
            lines.append("")
            lines.append(f"- Title: {issue['title']}")
            lines.append(f"- Failure count: {issue['failure_count']}")
            for failure in issue["failures"]:
                lines.append(f"- [{failure['gate_id']}] {failure['message']}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_delivery_readiness_artifacts(
    delivery_export: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write issue-ready gate results for a delivery export.

    Args:
        delivery_export: GitHub delivery export.
        output_dir: Directory where readiness artifacts should be written.

    Returns:
        Delivery readiness report.
    """
    report = assess_delivery_export_readiness(delivery_export)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "delivery-readiness.json").write_text(json.dumps(report, indent=2) + "\n")
    (target / "delivery-readiness.md").write_text(render_delivery_readiness_markdown(report))
    return report
