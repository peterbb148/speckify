"""Tests for round-trip feedback exports."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle_file
from speckify_tools.round_trip_feedback import build_round_trip_feedback


ROOT = Path(__file__).resolve().parents[1]
RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)
DEMO_OUTPUT = ROOT / "demo" / "it-systems-inventory-v2" / "output"


class RoundTripFeedbackTests(unittest.TestCase):
    """Round-trip feedback behavior for generated planning bundles."""

    def test_round_trip_feedback_classifies_planning_only_and_upstream_findings(self) -> None:
        """Feedback export should separate planning-only and upstream-affecting findings."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T14:00:00Z",
        )
        feedback_export = build_round_trip_feedback(bundle)

        self.assertEqual(feedback_export["round_trip_status"]["change_record_count"], 36)
        self.assertEqual(feedback_export["round_trip_status"]["feedback_proposal_count"], 26)
        self.assertEqual(feedback_export["round_trip_status"]["planning_only_findings"], 10)
        self.assertEqual(feedback_export["round_trip_status"]["upstream_affecting_findings"], 26)

    def test_round_trip_feedback_emits_upstream_proposal_for_real_gap(self) -> None:
        """An upstream-affecting quality gap should yield a feedback proposal."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T14:00:00Z",
        )
        feedback_export = build_round_trip_feedback(bundle)

        proposal = next(
            item
            for item in feedback_export["feedback_proposals"]
            if item["change_record_id"]
            == "change.iu.rupify.acceptance-constraint-success-1.abstract-success-criterion"
        )

        self.assertEqual(proposal["feedback_type"], "split_element")
        self.assertIn("acceptance-constraint-success-1", proposal["target_source_ids"])
        self.assertIn(
            "Refine the upstream success criterion into more concrete normative constraints.",
            proposal["proposed_upstream_action"],
        )

    def test_demo_round_trip_feedback_matches_checked_in_artifacts(self) -> None:
        """Checked-in round-trip feedback artifacts should match the current demo bundle."""
        bundle = json.loads((DEMO_OUTPUT / "planning-bundle.json").read_text())
        feedback_export = build_round_trip_feedback(bundle)

        self.assertEqual(
            feedback_export["change_records"],
            json.loads((DEMO_OUTPUT / "rupify-feedback" / "change-records.json").read_text()),
        )
        self.assertEqual(
            feedback_export["feedback_proposals"],
            json.loads((DEMO_OUTPUT / "rupify-feedback" / "feedback-proposals.json").read_text()),
        )
        self.assertEqual(
            feedback_export["round_trip_status"],
            json.loads((DEMO_OUTPUT / "rupify-feedback" / "round-trip-status.json").read_text()),
        )


if __name__ == "__main__":
    unittest.main()
