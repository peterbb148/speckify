"""Tests for issue-ready delivery quality gates."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from speckify_tools.delivery_quality import (
    assess_delivery_export_readiness,
    assess_delivery_issue_readiness,
    render_delivery_readiness_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
IT_DELIVERY_EXPORT = json.loads(
    (ROOT / "demo" / "it-systems-inventory-v2" / "output" / "github-delivery" / "issues.json").read_text()
)
LOYALTY_DELIVERY_EXPORT = json.loads(
    (ROOT / "demo" / "loyalty-platform-v2" / "output" / "github-delivery" / "issues.json").read_text()
)
REVIEW_ROOT = ROOT / "fixtures" / "review"


class DeliveryQualityTests(unittest.TestCase):
    """Quality-gate behavior for delivery exports."""

    def test_current_it_delivery_export_is_publication_ready(self) -> None:
        """Current IT delivery export should now satisfy the issue-ready gates."""
        report = assess_delivery_export_readiness(IT_DELIVERY_EXPORT)

        self.assertTrue(report["publication_ready"])
        self.assertEqual(report["failed_issue_count"], 0)

    def test_current_loyalty_delivery_export_is_publication_ready(self) -> None:
        """Current loyalty delivery export should now satisfy the issue-ready gates."""
        report = assess_delivery_export_readiness(LOYALTY_DELIVERY_EXPORT)

        self.assertTrue(report["publication_ready"])
        self.assertEqual(report["failed_issue_count"], 0)

    def test_complete_issue_passes_when_all_required_fields_are_present(self) -> None:
        """A strong issue payload should pass every issue-ready gate."""
        issue = {
            "implementation_unit_id": "iu.example.record-vendor",
            "title": "Record vendor details before contract activation",
            "dependency_ids": ["iu.example.validate-contract"],
            "dependency_titles": [
                {
                    "implementation_unit_id": "iu.example.validate-contract",
                    "title": "Validate contract dates before activation",
                }
            ],
            "source_anchor_ids": ["anchor.example.requirement-1"],
            "verification_unit_ids": ["vu.example.record-vendor"],
            "create_payload": {
                "title": "Record vendor details before contract activation",
                "body_path": "issue-bodies/iu-example-record-vendor.md",
                "labels": ["speckify", "planning"],
            },
            "body_markdown": """## Delivery Metadata

- Implementation unit id: `iu.example.record-vendor`
- Issue slug: `iu-example-record-vendor`
- Labels: `speckify`, `planning`
- Source anchors: `anchor.example.requirement-1`
- Verification units: `vu.example.record-vendor`
- Depends on:
  - `iu.example.validate-contract` (Validate contract dates before activation)

## Summary

Persist vendor details before contract activation so downstream contract handling has complete supplier context.

## Source Lineage

- `anchor.example.requirement-1`

## Scope

- Capture supplier identity data before activation begins.

## Acceptance Criteria

- Vendor identity fields are stored before contract activation is allowed.

## Verification Shape

- Intent: Confirm vendor data must exist before activation can proceed.
- Observable: Activation requests include vendor identity values.
- Setup requirement: A contract activation request is prepared with supplier data.
- Expected outcome: Activation is permitted only when vendor identity values are stored.
- Failure condition: Activation proceeds without vendor identity values being stored.

## Dependencies

- `iu.example.validate-contract`: Validate contract dates before activation.

## Drift Checks

- Preserve lineage to anchor.example.requirement-1.
""",
        }

        assessment = assess_delivery_issue_readiness(issue)

        self.assertTrue(assessment["ready"])
        self.assertEqual(assessment["failure_count"], 0)

    def test_review_fixtures_match_current_delivery_quality_reports(self) -> None:
        """Checked-in readiness reports should match the current generated review."""
        it_report = assess_delivery_export_readiness(IT_DELIVERY_EXPORT)
        loyalty_report = assess_delivery_export_readiness(LOYALTY_DELIVERY_EXPORT)

        self.assertEqual(
            it_report,
            json.loads((REVIEW_ROOT / "it-systems-inventory-v2-delivery-readiness.json").read_text()),
        )
        self.assertEqual(
            render_delivery_readiness_markdown(it_report),
            (REVIEW_ROOT / "it-systems-inventory-v2-delivery-readiness.md").read_text(),
        )
        self.assertEqual(
            loyalty_report,
            json.loads((REVIEW_ROOT / "loyalty-platform-v2-delivery-readiness.json").read_text()),
        )
        self.assertEqual(
            render_delivery_readiness_markdown(loyalty_report),
            (REVIEW_ROOT / "loyalty-platform-v2-delivery-readiness.md").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
