"""Demo import helpers for Rupify hand-off bundles."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON document from disk.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON object.
    """
    return json.loads(Path(path).read_text())


def _required_top_level_issues(export: dict[str, Any]) -> list[str]:
    """Collect missing top-level key issues.

    Args:
        export: Rupify hand-off export.

    Returns:
        Human-readable issue strings.
    """
    issues: list[str] = []
    for key in ("export_metadata", "elements", "trace_links", "summary"):
        if key not in export:
            issues.append(f"Missing top-level key: {key}")
    metadata = export.get("export_metadata", {})
    if metadata.get("export_kind") != "speckify_planning_export":
        issues.append("export_metadata.export_kind must be speckify_planning_export")
    return issues


def analyze_rupify_export(export: dict[str, Any]) -> dict[str, Any]:
    """Analyze a Rupify hand-off export for Speckify import readiness.

    Args:
        export: Rupify hand-off export.

    Returns:
        Structured import analysis report.
    """
    errors = _required_top_level_issues(export)
    warnings: list[str] = []

    elements = export.get("elements", [])
    trace_links = export.get("trace_links", [])
    summary = export.get("summary", {})

    element_ids = [element.get("id", "") for element in elements]
    id_counts = Counter(element_ids)
    duplicate_ids = sorted([item for item, count in id_counts.items() if item and count > 1])
    for duplicate_id in duplicate_ids:
        errors.append(f"Duplicate element id: {duplicate_id}")

    known_ids = {element_id for element_id in element_ids if element_id}
    unresolved_trace_refs: list[dict[str, str]] = []
    for link in trace_links:
        for key in ("from_id", "to_id"):
            ref_id = link.get(key, "")
            if not ref_id or ref_id in known_ids:
                continue
            if key == "to_id" and link.get("to_artifact", ""):
                continue
            if ref_id and ref_id not in known_ids:
                unresolved_trace_refs.append(
                    {
                        "trace_id": link.get("id", ""),
                        "field": key,
                        "ref_id": ref_id,
                    }
                )
    if unresolved_trace_refs:
        errors.append(
            f"Unresolved trace references detected: {len(unresolved_trace_refs)}"
        )

    family_counts = Counter(element.get("family", "") for element in elements)
    readiness_counts = Counter(element.get("readiness_status", "") for element in elements)
    semantic_counts = Counter(element.get("content_semantics", "") for element in elements)

    ready_normative_elements = [
        element
        for element in elements
        if element.get("content_semantics") == "normative" and element.get("normative_ready")
    ]
    blocked_or_partial_normative_elements = [
        element
        for element in elements
        if element.get("content_semantics") == "normative" and not element.get("normative_ready")
    ]

    summary_ready_ids = summary.get("ready_normative_ids", [])
    duplicate_summary_ready_ids = sorted(
        [item for item, count in Counter(summary_ready_ids).items() if item and count > 1]
    )
    for duplicate_id in duplicate_summary_ready_ids:
        warnings.append(f"Duplicate ready_normative_id in summary: {duplicate_id}")

    if summary.get("ready_normative_count") != len(summary_ready_ids):
        warnings.append(
            "summary.ready_normative_count does not match len(summary.ready_normative_ids)"
        )

    importable_ready_normative_elements = [
        element for element in ready_normative_elements if element.get("id", "") not in duplicate_ids
    ]

    grouped_importable = defaultdict(list)
    for element in importable_ready_normative_elements:
        grouped_importable[element.get("family", "unknown")].append(element)

    return {
        "source_export_kind": export.get("export_metadata", {}).get("export_kind", ""),
        "clean_import": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "element_count": len(elements),
            "trace_link_count": len(trace_links),
            "ready_normative_count": len(ready_normative_elements),
            "importable_ready_normative_count": len(importable_ready_normative_elements),
            "blocked_or_partial_normative_count": len(blocked_or_partial_normative_elements),
        },
        "family_counts": dict(sorted(family_counts.items())),
        "readiness_counts": dict(sorted(readiness_counts.items())),
        "semantic_counts": dict(sorted(semantic_counts.items())),
        "duplicate_element_ids": duplicate_ids,
        "unresolved_trace_references": unresolved_trace_refs,
        "summary": {
            "blocking_ambiguity_count": summary.get("blocking_ambiguity_count", 0),
            "ready_normative_count": summary.get("ready_normative_count", 0),
            "trace_link_count": summary.get("trace_link_count", 0),
        },
        "importable_ready_normative_by_family": {
            family: [
                {
                    "id": element.get("id", ""),
                    "name": element.get("name", ""),
                    "text": element.get("text", ""),
                }
                for element in family_elements
            ]
            for family, family_elements in sorted(grouped_importable.items())
        },
    }


def render_import_report_markdown(report: dict[str, Any], source_path: str | Path) -> str:
    """Render a Markdown report for the import analysis.

    Args:
        report: Structured import analysis report.
        source_path: Source export path.

    Returns:
        Markdown report text.
    """
    lines = [
        "# Rupify Hand-off Import Report",
        "",
        f"Source export: `{source_path}`",
        "",
        f"Clean import: `{str(report['clean_import']).lower()}`",
        "",
        "## Summary",
        "",
        f"- Elements: {report['counts']['element_count']}",
        f"- Trace links: {report['counts']['trace_link_count']}",
        f"- Ready normative elements: {report['counts']['ready_normative_count']}",
        f"- Importable ready normative elements: {report['counts']['importable_ready_normative_count']}",
        f"- Blocked or partial normative elements: {report['counts']['blocked_or_partial_normative_count']}",
        "",
        "## Errors",
        "",
    ]
    if report["errors"]:
        lines.extend(f"- {item}" for item in report["errors"])
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        lines.extend(f"- {item}" for item in report["warnings"])
    else:
        lines.append("- None")

    lines.extend(["", "## Duplicate Element IDs", ""])
    if report["duplicate_element_ids"]:
        lines.extend(f"- `{item}`" for item in report["duplicate_element_ids"])
    else:
        lines.append("- None")

    lines.extend(["", "## Unresolved Trace References", ""])
    if report["unresolved_trace_references"]:
        for item in report["unresolved_trace_references"]:
            lines.append(
                f"- `{item['trace_id']}` {item['field']} -> `{item['ref_id']}`"
            )
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def render_speckified_specification_markdown(
    report: dict[str, Any],
    source_path: str | Path,
) -> str:
    """Render a first Speckified specification from the importable subset.

    Args:
        report: Structured import analysis report.
        source_path: Source export path.

    Returns:
        Markdown specification text.
    """
    lines = [
        "# Speckified Specification",
        "",
        f"Source export: `{source_path}`",
        "",
        "## Import Status",
        "",
    ]

    if report["clean_import"]:
        lines.append("- The Rupify hand-off bundle imported cleanly with no additional changes required.")
    else:
        lines.append(
            "- The Rupify hand-off bundle did not import cleanly as-is. This specification is derived from the importable subset only."
        )
        lines.append(
            "- No manual edits were applied to the upstream export; blocked areas are reported separately."
        )

    lines.extend(
        [
            "",
            "## Importable Normative Core",
            "",
        ]
    )

    if not report["importable_ready_normative_by_family"]:
        lines.append("- No importable ready normative elements were found.")
    else:
        for family, items in report["importable_ready_normative_by_family"].items():
            lines.append(f"### {family.replace('_', ' ').title()}")
            lines.append("")
            for item in items:
                label = item["name"] or item["id"]
                text = item["text"] or ""
                if text:
                    lines.append(f"- `{item['id']}` {label}: {text}")
                else:
                    lines.append(f"- `{item['id']}` {label}")
            lines.append("")

    lines.extend(["## Import Blockers", ""])
    if report["errors"]:
        lines.extend(f"- {item}" for item in report["errors"])
    else:
        lines.append("- None")

    lines.extend(["", "## Notes", ""])
    lines.append(
        "- This document is a first Speckified specification artifact produced from the real Rupify hand-off export."
    )
    lines.append(
        "- It intentionally excludes ambiguous or structurally blocked areas rather than patching upstream data."
    )

    return "\n".join(lines) + "\n"


def write_demo_outputs(source_export: str | Path, demo_dir: str | Path) -> dict[str, Any]:
    """Write demo import outputs for a Rupify hand-off export.

    Args:
        source_export: Path to the source Rupify export.
        demo_dir: Destination demo directory.

    Returns:
        Structured import analysis report.
    """
    source_path = Path(source_export)
    demo_root = Path(demo_dir)
    input_dir = demo_root / "input"
    output_dir = demo_root / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_text = source_path.read_text()
    (input_dir / source_path.name).write_text(raw_text)

    export = json.loads(raw_text)
    report = analyze_rupify_export(export)

    (output_dir / "import-report.json").write_text(json.dumps(report, indent=2))
    (output_dir / "import-report.md").write_text(
        render_import_report_markdown(report, source_path)
    )
    (output_dir / "speckified-specification.md").write_text(
        render_speckified_specification_markdown(report, source_path)
    )
    return report
