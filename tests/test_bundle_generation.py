"""Tests for Speckify planning bundle generation."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle
from speckify_tools.rupify_import import import_rupify_export_file
from speckify_tools.validation import validate_bundle


RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)
SCHEMA_DIR = Path("/Volumes/Data/GitHub/Peterbb148/speckify/schemas")


class BundleGenerationTests(unittest.TestCase):
    """Behavior of the first-pass planning bundle generator."""

    def test_generate_bundle_from_real_rupify_export(self) -> None:
        """The real Rupify hand-off export should generate a valid planning bundle."""
        export = import_rupify_export_file(RUPIFY_EXPORT)

        bundle = generate_planning_bundle(
            export,
            generated_at="2026-04-20T12:30:00Z",
        )

        self.assertEqual(bundle["bundle_metadata"]["bundle_id"], "bundle.speckify-planning-export")
        self.assertEqual(bundle["bundle_metadata"]["decomposition_profile"], "rupify-one-to-one-v1")
        self.assertEqual(len(bundle["source_anchors"]), 29)
        self.assertEqual(len(bundle["spec_units"]), 29)
        self.assertEqual(len(bundle["implementation_units"]), 29)
        self.assertEqual(len(bundle["verification_units"]), 29)
        self.assertEqual(len(bundle["trace_bundles"]), 29)
        self.assertEqual(len(bundle["rendered_issues"]), 29)
        self.assertEqual(bundle["unresolved_ambiguities"], [])

        validate_bundle(bundle, SCHEMA_DIR)

    def test_generated_bundle_preserves_lineage_for_ready_normative_element(self) -> None:
        """A generated bundle record should point back to its Rupify source id."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        anchor = next(
            item
            for item in bundle["source_anchors"]
            if item["source_id"] == "functional-requirement-1"
        )
        spec_unit = next(
            item
            for item in bundle["spec_units"]
            if item["source_anchor_ids"] == [anchor["id"]]
        )
        implementation_unit = next(
            item
            for item in bundle["implementation_units"]
            if item["derived_from_spec_unit_ids"] == [spec_unit["id"]]
        )
        verification_unit = next(
            item
            for item in bundle["verification_units"]
            if item["implementation_unit_id"] == implementation_unit["id"]
        )

        self.assertEqual(anchor["view"], "requirements")
        self.assertEqual(spec_unit["id"], "su.rupify.functional-requirement-1")
        self.assertEqual(
            implementation_unit["verification_unit_ids"],
            [verification_unit["id"]],
        )


if __name__ == "__main__":
    unittest.main()
