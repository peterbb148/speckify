"""Tests for GitHub delivery export artifacts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle_file
from speckify_tools.delivery_export import build_github_delivery_export


ROOT = Path(__file__).resolve().parents[1]
RUPIFY_EXPORT = ROOT / "demo" / "it-systems-inventory-v2" / "input" / "speckify-planning-export.json"
DEMO_OUTPUT = ROOT / "demo" / "it-systems-inventory-v2" / "output"


class DeliveryExportTests(unittest.TestCase):
    """Delivery-export behavior for generated planning bundles."""

    def test_delivery_export_matches_generated_issue_count(self) -> None:
        """Each implementation unit should produce one GitHub delivery issue export."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T14:00:00Z",
        )
        delivery_export = build_github_delivery_export(bundle)

        self.assertEqual(
            len(delivery_export["issues"]),
            len(bundle["implementation_units"]),
        )
        self.assertEqual(
            delivery_export["export_metadata"]["export_kind"],
            "speckify_github_delivery_export",
        )
        self.assertEqual(delivery_export["issues"][0]["sequence_number"], 1)
        self.assertIn("create_payload", delivery_export["issues"][0])

    def test_delivery_export_wraps_rendered_issue_markdown_with_delivery_metadata(self) -> None:
        """Delivery issue bodies should add GitHub-creation metadata above the planning body."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T14:00:00Z",
        )
        delivery_export = build_github_delivery_export(bundle)

        delivery_issue = next(
            item
            for item in delivery_export["issues"]
            if item["implementation_unit_id"] == "iu.rupify.state-transition-1.active-to-retiring"
        )
        rendered_issue = next(
            item
            for item in bundle["rendered_issues"]
            if item["implementation_unit_id"] == delivery_issue["implementation_unit_id"]
        )

        self.assertTrue(delivery_issue["body_markdown"].endswith(rendered_issue["issue_body"]))
        self.assertIn("## Delivery Metadata", delivery_issue["body_markdown"])
        self.assertIn("Implementation unit id", delivery_issue["body_markdown"])
        self.assertIn("state-transitions", delivery_issue["labels"])
        self.assertIn(
            "iu.rupify.state-transition-1.proposed-to-active",
            delivery_issue["dependency_ids"],
        )
        self.assertEqual(
            delivery_issue["create_payload"]["body_path"],
            "issue-bodies/iu-rupify-state-transition-1-active-to-retiring.md",
        )
        self.assertEqual(
            delivery_issue["dependency_titles"],
            [
                {
                    "implementation_unit_id": "iu.rupify.state-transition-1.proposed-to-active",
                    "title": "Implement lifecycle transition: Proposed to Active",
                }
            ],
        )

    def test_demo_delivery_export_matches_current_golden_bundle(self) -> None:
        """Checked-in delivery export artifacts should match the current demo bundle."""
        bundle = json.loads((DEMO_OUTPUT / "planning-bundle.json").read_text())
        delivery_export = build_github_delivery_export(bundle)
        checked_in_export = json.loads(
            (DEMO_OUTPUT / "github-delivery" / "issues.json").read_text()
        )

        self.assertEqual(delivery_export, checked_in_export)

        sample_issue = next(
            item
            for item in delivery_export["issues"]
            if item["implementation_unit_id"] == "iu.rupify.state-transition-1.active-to-retiring"
        )
        self.assertEqual(
            sample_issue["body_markdown"],
            (
                DEMO_OUTPUT
                / "github-delivery"
                / "issue-bodies"
                / f"{sample_issue['issue_slug']}.md"
            ).read_text(),
        )


if __name__ == "__main__":
    unittest.main()
