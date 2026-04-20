"""Validation helpers for Speckify planning bundles."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bundle_generation import generate_planning_bundle_file
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


@dataclass
class ValidationIssue:
    """One validation issue found in a planning bundle."""

    path: str
    message: str


class BundleValidationError(Exception):
    """Raised when a planning bundle is invalid."""

    def __init__(self, issues: list[ValidationIssue]) -> None:
        """Initialize the error with collected issues.

        Args:
            issues: Validation issues found in the bundle.
        """
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


def _schema_registry(schema_dir: str | Path) -> Registry:
    """Build a referencing registry for local schema files.

    Args:
        schema_dir: Directory containing schema files.

    Returns:
        Registry containing all local schemas keyed by their `$id`.
    """
    registry = Registry()
    for schema_path in Path(schema_dir).glob("*.json"):
        schema = load_json(schema_path)
        schema_id = schema.get("$id")
        if not schema_id:
            continue
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def _collect_schema_issues(bundle: dict[str, Any], schema_dir: str | Path) -> list[ValidationIssue]:
    """Collect JSON Schema validation issues for a bundle.

    Args:
        bundle: Planning bundle document.
        schema_dir: Directory containing planning bundle schemas.

    Returns:
        Schema validation issues.
    """
    planning_bundle_schema = load_json(Path(schema_dir) / "planning-bundle.schema.json")
    validator = Draft202012Validator(
        planning_bundle_schema,
        registry=_schema_registry(schema_dir),
    )

    issues: list[ValidationIssue] = []
    for error in sorted(validator.iter_errors(bundle), key=lambda item: list(item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        issues.append(ValidationIssue(path=path, message=error.message))
    return issues


def _missing_references(
    source_ids: list[str],
    known_ids: set[str],
    path: str,
    label: str,
) -> list[ValidationIssue]:
    """Collect missing reference issues.

    Args:
        source_ids: Referenced identifiers.
        known_ids: Known identifiers for the target collection.
        path: Field path for issue reporting.
        label: Human-readable reference label.

    Returns:
        Missing reference issues.
    """
    issues: list[ValidationIssue] = []
    for ref_id in source_ids:
        if ref_id not in known_ids:
            issues.append(ValidationIssue(path=path, message=f"Unknown {label} reference: {ref_id}"))
    return issues


def _collect_reference_issues(bundle: dict[str, Any]) -> list[ValidationIssue]:
    """Collect broken cross-record reference issues.

    Args:
        bundle: Planning bundle document.

    Returns:
        Cross-record reference issues.
    """
    issues: list[ValidationIssue] = []

    source_anchor_ids = {item["id"] for item in bundle.get("source_anchors", [])}
    spec_unit_ids = {item["id"] for item in bundle.get("spec_units", [])}
    implementation_unit_ids = {item["id"] for item in bundle.get("implementation_units", [])}
    verification_unit_ids = {item["id"] for item in bundle.get("verification_units", [])}
    trace_bundle_ids = {item["id"] for item in bundle.get("trace_bundles", [])}
    ambiguity_ids = {item["ambiguity_id"] for item in bundle.get("unresolved_ambiguities", [])}

    for index, item in enumerate(bundle.get("spec_units", [])):
        issues.extend(
            _missing_references(
                item.get("source_anchor_ids", []),
                source_anchor_ids,
                f"spec_units[{index}].source_anchor_ids",
                "source_anchor",
            )
        )

    for index, item in enumerate(bundle.get("implementation_units", [])):
        issues.extend(
            _missing_references(
                item.get("derived_from_spec_unit_ids", []),
                spec_unit_ids,
                f"implementation_units[{index}].derived_from_spec_unit_ids",
                "spec_unit",
            )
        )
        issues.extend(
            _missing_references(
                item.get("source_anchor_ids", []),
                source_anchor_ids,
                f"implementation_units[{index}].source_anchor_ids",
                "source_anchor",
            )
        )
        issues.extend(
            _missing_references(
                item.get("dependencies", []),
                implementation_unit_ids,
                f"implementation_units[{index}].dependencies",
                "implementation_unit",
            )
        )
        issues.extend(
            _missing_references(
                item.get("verification_unit_ids", []),
                verification_unit_ids,
                f"implementation_units[{index}].verification_unit_ids",
                "verification_unit",
            )
        )

    for index, item in enumerate(bundle.get("verification_units", [])):
        issues.extend(
            _missing_references(
                [item.get("implementation_unit_id", "")],
                implementation_unit_ids,
                f"verification_units[{index}].implementation_unit_id",
                "implementation_unit",
            )
        )
        issues.extend(
            _missing_references(
                item.get("source_anchor_ids", []),
                source_anchor_ids,
                f"verification_units[{index}].source_anchor_ids",
                "source_anchor",
            )
        )

    for index, item in enumerate(bundle.get("trace_bundles", [])):
        issues.extend(
            _missing_references(
                item.get("source_anchor_ids", []),
                source_anchor_ids,
                f"trace_bundles[{index}].source_anchor_ids",
                "source_anchor",
            )
        )
        issues.extend(
            _missing_references(
                item.get("spec_unit_ids", []),
                spec_unit_ids,
                f"trace_bundles[{index}].spec_unit_ids",
                "spec_unit",
            )
        )
        issues.extend(
            _missing_references(
                item.get("implementation_unit_ids", []),
                implementation_unit_ids,
                f"trace_bundles[{index}].implementation_unit_ids",
                "implementation_unit",
            )
        )
        issues.extend(
            _missing_references(
                item.get("verification_unit_ids", []),
                verification_unit_ids,
                f"trace_bundles[{index}].verification_unit_ids",
                "verification_unit",
            )
        )

    for index, item in enumerate(bundle.get("dependency_edges", [])):
        issues.extend(
            _missing_references(
                [item.get("from_implementation_unit_id", "")],
                implementation_unit_ids,
                f"dependency_edges[{index}].from_implementation_unit_id",
                "implementation_unit",
            )
        )
        issues.extend(
            _missing_references(
                [item.get("to_implementation_unit_id", "")],
                implementation_unit_ids,
                f"dependency_edges[{index}].to_implementation_unit_id",
                "implementation_unit",
            )
        )

    for index, item in enumerate(bundle.get("assembly_rules", [])):
        issues.extend(
            _missing_references(
                item.get("source_anchor_ids", []),
                source_anchor_ids,
                f"assembly_rules[{index}].source_anchor_ids",
                "source_anchor",
            )
        )
        issues.extend(
            _missing_references(
                item.get("member_spec_unit_ids", []),
                spec_unit_ids,
                f"assembly_rules[{index}].member_spec_unit_ids",
                "spec_unit",
            )
        )

    for index, item in enumerate(bundle.get("unresolved_ambiguities", [])):
        ambiguity_id = item.get("ambiguity_id", "")
        if ambiguity_id and ambiguity_id not in ambiguity_ids:
            issues.append(
                ValidationIssue(
                    path=f"unresolved_ambiguities[{index}].ambiguity_id",
                    message=f"Unknown ambiguity reference: {ambiguity_id}",
                )
            )
        issues.extend(
            _missing_references(
                item.get("affects_implementation_unit_ids", []),
                implementation_unit_ids,
                f"unresolved_ambiguities[{index}].affects_implementation_unit_ids",
                "implementation_unit",
            )
        )

    for index, item in enumerate(bundle.get("rendered_issues", [])):
        issues.extend(
            _missing_references(
                [item.get("implementation_unit_id", "")],
                implementation_unit_ids,
                f"rendered_issues[{index}].implementation_unit_id",
                "implementation_unit",
            )
        )

    if not trace_bundle_ids and bundle.get("implementation_units"):
        issues.append(
            ValidationIssue(path="trace_bundles", message="At least one trace bundle is required.")
        )

    return issues


def validate_bundle(bundle: dict[str, Any], schema_dir: str | Path) -> None:
    """Validate a planning bundle against schemas and reference integrity rules.

    Args:
        bundle: Planning bundle document.
        schema_dir: Directory containing JSON Schema files.

    Raises:
        BundleValidationError: If validation fails.
    """
    issues = _collect_schema_issues(bundle, schema_dir)
    if not issues:
        issues.extend(_collect_reference_issues(bundle))

    if issues:
        raise BundleValidationError(issues)


def validate_bundle_file(bundle_path: str | Path, schema_dir: str | Path) -> None:
    """Load and validate a planning bundle from disk.

    Args:
        bundle_path: Path to the bundle JSON file.
        schema_dir: Directory containing JSON Schema files.

    Raises:
        BundleValidationError: If validation fails.
    """
    validate_bundle(load_json(bundle_path), schema_dir)


def validate_generated_bundle_file(
    source_export_path: str | Path,
    schema_dir: str | Path,
) -> dict[str, Any]:
    """Generate and validate a planning bundle from a Rupify export.

    Args:
        source_export_path: Path to the Rupify planning export JSON file.
        schema_dir: Directory containing JSON Schema files.

    Returns:
        The generated and validated planning bundle.

    Raises:
        BundleValidationError: If the generated bundle fails validation.
    """
    bundle = generate_planning_bundle_file(source_export_path)
    validate_bundle(bundle, schema_dir)
    return bundle
