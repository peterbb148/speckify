"""Tests for typed Rupify planning export import."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.rupify_handoff_demo import analyze_imported_rupify_export
from speckify_tools.rupify_import import (
    RupifyImportError,
    import_rupify_export,
    import_rupify_export_file,
)


RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)


class RupifyImportTests(unittest.TestCase):
    """Behavior of the typed Rupify import layer."""

    def test_real_handoff_export_imports_into_typed_records(self) -> None:
        """The checked-in Rupify hand-off export should import cleanly."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        self.assertEqual(export.export_metadata.export_kind, "speckify_planning_export")
        self.assertEqual(len(export.elements), 82)
        self.assertEqual(len(export.trace_links), 127)
        self.assertEqual(export.summary.ready_normative_count, 29)

    def test_real_handoff_export_analyzes_cleanly_after_import(self) -> None:
        """The current hand-off export should analyze as a clean import."""
        report = analyze_imported_rupify_export(import_rupify_export_file(RUPIFY_EXPORT))
        self.assertTrue(report["clean_import"])
        self.assertEqual(report["duplicate_element_ids"], [])
        self.assertEqual(report["unresolved_trace_references"], [])

    def test_import_rejects_missing_required_root_sections(self) -> None:
        """Missing top-level sections should fail the typed import."""
        with self.assertRaises(RupifyImportError) as error:
            import_rupify_export({"export_metadata": {"export_kind": "speckify_planning_export"}})

        self.assertIn("elements", str(error.exception))
        self.assertIn("trace_links", str(error.exception))
        self.assertIn("summary", str(error.exception))

    def test_import_rejects_wrong_field_types(self) -> None:
        """Required fields must keep their declared types."""
        document = {
            "export_metadata": {"export_kind": "speckify_planning_export"},
            "elements": [
                {
                    "id": "requirement-1",
                    "family": "functional_requirement",
                    "name": "Requirement 1",
                    "text": "Do the thing",
                    "content_semantics": "normative",
                    "readiness_status": "ready",
                    "normative_ready": "yes",
                }
            ],
            "trace_links": [],
            "summary": {
                "ready_normative_ids": ["requirement-1"],
                "ready_normative_count": 1,
                "blocking_ambiguity_count": 0,
                "trace_link_count": 0,
            },
        }

        with self.assertRaises(RupifyImportError) as error:
            import_rupify_export(document)

        self.assertIn("elements[0].normative_ready", str(error.exception))


if __name__ == "__main__":
    unittest.main()
