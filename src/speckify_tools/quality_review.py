"""Quality heuristics for generated planning bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def analyze_bundle_quality(bundle: dict[str, Any]) -> dict[str, Any]:
    """Analyze generated bundle quality and emit review warnings.

    Args:
        bundle: Generated planning bundle.

    Returns:
        Quality review report with warnings only. This does not modify bundle output.
    """
    warnings: list[dict[str, str]] = []

    verification_by_impl = {
        item["implementation_unit_id"]: item
        for item in bundle.get("verification_units", [])
    }

    for implementation_unit in bundle.get("implementation_units", []):
        implementation_id = implementation_unit["id"]
        title = implementation_unit.get("title", "")
        summary = implementation_unit.get("summary", "")
        acceptance = " ".join(implementation_unit.get("acceptance_criteria", []))
        verification = verification_by_impl.get(implementation_id)

        if any(token in title for token in ["functional-requirement-", "non_functional-requirement-"]):
            warnings.append(
                {
                    "kind": "generic_title",
                    "implementation_unit_id": implementation_id,
                    "message": f"Title still exposes a raw requirement identifier: {title}",
                }
            )

        if len(acceptance.strip()) <= 12:
            warnings.append(
                {
                    "kind": "very_short_acceptance",
                    "implementation_unit_id": implementation_id,
                    "message": f"Acceptance criteria may be too short to guide implementation: {acceptance}",
                }
            )

        if "success criterion" in title.lower():
            warnings.append(
                {
                    "kind": "abstract_success_criterion",
                    "implementation_unit_id": implementation_id,
                    "message": "Success-criterion output may still be too abstract for direct implementation planning.",
                }
            )

        if verification:
            observables = " ".join(verification.get("observables", []))
            expected = " ".join(verification.get("expected_outcomes", []))
            if observables.strip() and expected.strip() and observables.strip() == expected.strip():
                warnings.append(
                    {
                        "kind": "weak_verification_distinction",
                        "implementation_unit_id": implementation_id,
                        "message": "Observable and expected outcome are effectively identical.",
                    }
                )

    return {
        "warning_count": len(warnings),
        "warnings": warnings,
    }


def render_quality_report_markdown(report: dict[str, Any]) -> str:
    """Render a Markdown summary for quality warnings."""
    lines = [
        "# Quality Review Report",
        "",
        f"- Warning count: {report['warning_count']}",
        "",
        "## Warnings",
        "",
    ]
    if not report["warnings"]:
        lines.append("- None")
    else:
        for warning in report["warnings"]:
            lines.append(
                f"- `{warning['implementation_unit_id']}` [{warning['kind']}] {warning['message']}"
            )
    return "\n".join(lines) + "\n"


def write_quality_review_artifacts(
    bundle: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write machine-readable and Markdown quality review artifacts.

    Args:
        bundle: Generated planning bundle.
        output_dir: Directory where quality artifacts should be written.

    Returns:
        Quality review report.
    """
    report = analyze_bundle_quality(bundle)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "quality-review.json").write_text(json.dumps(report, indent=2) + "\n")
    (target / "quality-review.md").write_text(render_quality_report_markdown(report))
    return report
