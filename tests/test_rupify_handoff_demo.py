"""Tests for the Rupify hand-off demo importer."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.rupify_handoff_demo import analyze_rupify_export, load_json


RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)


class RupifyHandoffDemoTests(unittest.TestCase):
    """Behavior of the demo import analysis."""

    def test_real_handoff_export_reports_current_blockers(self) -> None:
        """The current hand-off export should surface known structural blockers."""
        report = analyze_rupify_export(load_json(RUPIFY_EXPORT))
        self.assertFalse(report["clean_import"])
        self.assertIn("functional-requirement-1", report["duplicate_element_ids"])
        self.assertIn("non_functional-requirement-1", report["duplicate_element_ids"])
        self.assertTrue(report["unresolved_trace_references"])


if __name__ == "__main__":
    unittest.main()
