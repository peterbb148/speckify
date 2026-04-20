"""Tests for compact review fixtures derived from golden demo outputs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_OUTPUT = ROOT / "demo" / "it-systems-inventory-v2" / "output"
REVIEW_ROOT = ROOT / "fixtures" / "review"


class ReviewFixtureTests(unittest.TestCase):
    """Alignment checks for the compact review fixture set."""

    def test_review_bundle_summary_matches_current_golden_bundle(self) -> None:
        """The compact bundle summary should reflect the current golden bundle."""
        bundle = json.loads((DEMO_OUTPUT / "planning-bundle.json").read_text())
        review_summary = json.loads((REVIEW_ROOT / "planning-bundle-summary.json").read_text())

        self.assertEqual(review_summary["bundle_id"], bundle["bundle_metadata"]["bundle_id"])
        self.assertEqual(
            review_summary["decomposition_profile"],
            bundle["bundle_metadata"]["decomposition_profile"],
        )
        self.assertEqual(
            review_summary["counts"]["implementation_units"],
            len(bundle["implementation_units"]),
        )
        self.assertEqual(
            review_summary["counts"]["dependency_edges"],
            len(bundle["dependency_edges"]),
        )

    def test_review_rendered_issue_samples_match_golden_outputs(self) -> None:
        """Sample review fixtures should match the current golden rendered issues."""
        mappings = {
            "constraint-web-ui.md": "iu.rupify.acceptance-constraint-requirement-1.md",
            "workflow-approval-states.md": "iu.rupify.functional-requirement-1.approval-states.md",
            "state-transition-active-to-retiring.md": "iu.rupify.state-transition-1.active-to-retiring.md",
        }

        for review_name, demo_name in mappings.items():
            self.assertEqual(
                (REVIEW_ROOT / "rendered-issues" / review_name).read_text(),
                (DEMO_OUTPUT / "rendered-issues" / demo_name).read_text(),
            )


if __name__ == "__main__":
    unittest.main()
