"""Tests for compact review fixtures derived from golden demo outputs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from speckify_tools.quality_review import analyze_bundle_quality, render_quality_report_markdown


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
            "workflow-requirement.md": "iu.rupify.functional-requirement-1.support-stage-gates.md",
            "state-transition-active-to-retiring.md": "iu.rupify.state-transition-1.active-to-retiring.md",
        }

        for review_name, demo_name in mappings.items():
            self.assertEqual(
                (REVIEW_ROOT / "rendered-issues" / review_name).read_text(),
                (DEMO_OUTPUT / "rendered-issues" / demo_name).read_text(),
            )

    def test_quality_review_artifacts_match_current_golden_bundle(self) -> None:
        """The checked-in quality review artifacts should reflect the current golden bundle."""
        bundle = json.loads((DEMO_OUTPUT / "planning-bundle.json").read_text())
        report = analyze_bundle_quality(bundle)

        self.assertEqual(
            report,
            json.loads((REVIEW_ROOT / "quality-review.json").read_text()),
        )
        self.assertEqual(
            render_quality_report_markdown(report),
            (REVIEW_ROOT / "quality-review.md").read_text(),
        )

    def test_quality_review_flags_known_current_weaknesses(self) -> None:
        """The quality review should warn on the current broad and generic output cases."""
        bundle = json.loads((DEMO_OUTPUT / "planning-bundle.json").read_text())
        report = analyze_bundle_quality(bundle)

        self.assertEqual(report["warning_count"], 0)
        self.assertEqual(report["warnings"], [])

    def test_loyalty_platform_v2_review_summary_matches_demo_bundle(self) -> None:
        """The second real-world review summary should reflect the loyalty V2 demo bundle."""
        loyalty_demo_output = ROOT / "demo" / "loyalty-platform-v2" / "output"
        bundle = json.loads((loyalty_demo_output / "planning-bundle.json").read_text())
        review_summary = json.loads((REVIEW_ROOT / "loyalty-platform-v2-summary.json").read_text())

        self.assertEqual(review_summary["bundle_id"], bundle["bundle_metadata"]["bundle_id"])
        self.assertEqual(
            review_summary["decomposition_profile"],
            bundle["bundle_metadata"]["decomposition_profile"],
        )
        self.assertEqual(review_summary["counts"]["implementation_units"], 74)
        self.assertEqual(review_summary["counts"]["source_anchors"], 60)


if __name__ == "__main__":
    unittest.main()
