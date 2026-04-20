"""Typed import helpers for Rupify planning exports."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RupifyExportMetadata:
    """Top-level metadata for a Rupify planning export."""

    export_kind: str


@dataclass(frozen=True)
class RupifyElement:
    """One element record from a Rupify planning export."""

    id: str
    family: str
    name: str
    text: str
    content_semantics: str
    readiness_status: str
    normative_ready: bool
    raw: dict[str, Any]


@dataclass(frozen=True)
class RupifyTraceLink:
    """One trace link record from a Rupify planning export."""

    id: str
    from_id: str
    to_id: str
    to_artifact: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class RupifyExportSummary:
    """Summary block for a Rupify planning export."""

    ready_normative_ids: list[str]
    ready_normative_count: int
    blocking_ambiguity_count: int
    trace_link_count: int
    raw: dict[str, Any]


@dataclass(frozen=True)
class RupifyPlanningExport:
    """Typed Rupify planning export."""

    export_metadata: RupifyExportMetadata
    elements: list[RupifyElement]
    trace_links: list[RupifyTraceLink]
    summary: RupifyExportSummary
    raw: dict[str, Any]


@dataclass(frozen=True)
class ImportIssue:
    """One import issue found while loading a Rupify export."""

    path: str
    message: str


class RupifyImportError(Exception):
    """Raised when a Rupify planning export cannot be imported."""

    def __init__(self, issues: list[ImportIssue]) -> None:
        """Initialize the error with collected import issues."""
        self.issues = issues
        rendered = "\n".join(f"{issue.path}: {issue.message}" for issue in issues)
        super().__init__(rendered)


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON document from disk.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON object.
    """
    return json.loads(Path(path).read_text())


def _require_dict(value: Any, path: str, issues: list[ImportIssue]) -> dict[str, Any]:
    """Require a JSON object and collect an issue otherwise."""
    if isinstance(value, dict):
        return value
    issues.append(ImportIssue(path=path, message="Expected an object"))
    return {}


def _require_list(value: Any, path: str, issues: list[ImportIssue]) -> list[Any]:
    """Require a JSON array and collect an issue otherwise."""
    if isinstance(value, list):
        return value
    issues.append(ImportIssue(path=path, message="Expected an array"))
    return []


def _require_str(value: Any, path: str, issues: list[ImportIssue]) -> str:
    """Require a string and collect an issue otherwise."""
    if isinstance(value, str) and value:
        return value
    issues.append(ImportIssue(path=path, message="Expected a non-empty string"))
    return ""


def _require_string(value: Any, path: str, issues: list[ImportIssue]) -> str:
    """Require a string and collect an issue otherwise."""
    if isinstance(value, str):
        return value
    issues.append(ImportIssue(path=path, message="Expected a string"))
    return ""


def _require_bool(value: Any, path: str, issues: list[ImportIssue]) -> bool:
    """Require a boolean and collect an issue otherwise."""
    if isinstance(value, bool):
        return value
    issues.append(ImportIssue(path=path, message="Expected a boolean"))
    return False


def _require_int(value: Any, path: str, issues: list[ImportIssue]) -> int:
    """Require an integer and collect an issue otherwise."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    issues.append(ImportIssue(path=path, message="Expected an integer"))
    return 0


def import_rupify_export(document: dict[str, Any]) -> RupifyPlanningExport:
    """Import a Rupify planning export into typed records.

    Args:
        document: Parsed Rupify planning export JSON document.

    Returns:
        Typed Rupify planning export.

    Raises:
        RupifyImportError: If the document does not satisfy the required contract.
    """
    issues: list[ImportIssue] = []
    root = _require_dict(document, "$", issues)

    metadata_value = _require_dict(root.get("export_metadata"), "export_metadata", issues)
    export_kind = _require_str(
        metadata_value.get("export_kind"),
        "export_metadata.export_kind",
        issues,
    )
    if export_kind and export_kind != "speckify_planning_export":
        issues.append(
            ImportIssue(
                path="export_metadata.export_kind",
                message="Expected speckify_planning_export",
            )
        )

    element_values = _require_list(root.get("elements"), "elements", issues)
    elements: list[RupifyElement] = []
    for index, value in enumerate(element_values):
        path = f"elements[{index}]"
        element = _require_dict(value, path, issues)
        elements.append(
            RupifyElement(
                id=_require_str(element.get("id"), f"{path}.id", issues),
                family=_require_str(element.get("family"), f"{path}.family", issues),
                name=_require_string(element.get("name"), f"{path}.name", issues),
                text=_require_string(element.get("text"), f"{path}.text", issues),
                content_semantics=_require_string(
                    element.get("content_semantics"),
                    f"{path}.content_semantics",
                    issues,
                ),
                readiness_status=_require_string(
                    element.get("readiness_status"),
                    f"{path}.readiness_status",
                    issues,
                ),
                normative_ready=_require_bool(
                    element.get("normative_ready"),
                    f"{path}.normative_ready",
                    issues,
                ),
                raw=element,
            )
        )

    trace_link_values = _require_list(root.get("trace_links"), "trace_links", issues)
    trace_links: list[RupifyTraceLink] = []
    for index, value in enumerate(trace_link_values):
        path = f"trace_links[{index}]"
        trace_link = _require_dict(value, path, issues)
        to_artifact_value = trace_link.get("to_artifact", "")
        if to_artifact_value is None:
            to_artifact_value = ""
        if not isinstance(to_artifact_value, str):
            issues.append(
                ImportIssue(
                    path=f"{path}.to_artifact",
                    message="Expected a string when present",
                )
            )
            to_artifact_value = ""
        trace_links.append(
            RupifyTraceLink(
                id=_require_str(trace_link.get("id"), f"{path}.id", issues),
                from_id=_require_str(trace_link.get("from_id"), f"{path}.from_id", issues),
                to_id=_require_string(trace_link.get("to_id"), f"{path}.to_id", issues),
                to_artifact=to_artifact_value,
                raw=trace_link,
            )
        )

    summary_value = _require_dict(root.get("summary"), "summary", issues)
    ready_normative_ids_value = _require_list(
        summary_value.get("ready_normative_ids"),
        "summary.ready_normative_ids",
        issues,
    )
    ready_normative_ids: list[str] = []
    for index, value in enumerate(ready_normative_ids_value):
        ready_normative_ids.append(
            _require_str(
                value,
                f"summary.ready_normative_ids[{index}]",
                issues,
            )
        )

    ready_normative_ids = [
        item
        for item in ready_normative_ids
        if item
    ]

    summary = RupifyExportSummary(
        ready_normative_ids=ready_normative_ids,
        ready_normative_count=_require_int(
            summary_value.get("ready_normative_count"),
            "summary.ready_normative_count",
            issues,
        ),
        blocking_ambiguity_count=_require_int(
            summary_value.get("blocking_ambiguity_count"),
            "summary.blocking_ambiguity_count",
            issues,
        ),
        trace_link_count=_require_int(
            summary_value.get("trace_link_count"),
            "summary.trace_link_count",
            issues,
        ),
        raw=summary_value,
    )

    if issues:
        raise RupifyImportError(issues)

    return RupifyPlanningExport(
        export_metadata=RupifyExportMetadata(export_kind=export_kind),
        elements=elements,
        trace_links=trace_links,
        summary=summary,
        raw=root,
    )


def import_rupify_export_file(path: str | Path) -> RupifyPlanningExport:
    """Load and import a Rupify planning export from disk.

    Args:
        path: Path to the export file.

    Returns:
        Typed Rupify planning export.
    """
    return import_rupify_export(load_json(path))
