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
        self.assertEqual(
            bundle["bundle_metadata"]["decomposition_profile"],
            "rupify-split-dependencies-v1",
        )
        self.assertEqual(len(bundle["source_anchors"]), 29)
        self.assertEqual(len(bundle["spec_units"]), 39)
        self.assertEqual(len(bundle["implementation_units"]), 39)
        self.assertEqual(len(bundle["verification_units"]), 39)
        self.assertEqual(len(bundle["trace_bundles"]), 39)
        self.assertEqual(len(bundle["dependency_edges"]), 8)
        self.assertEqual(len(bundle["assembly_rules"]), 7)
        self.assertEqual(len(bundle["rendered_issues"]), 39)
        self.assertEqual(bundle["unresolved_ambiguities"], [])

        validate_bundle(bundle, SCHEMA_DIR)

    def test_generated_bundle_preserves_lineage_for_split_functional_requirement(self) -> None:
        """Split units should still point back to the original Rupify source id."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        anchor = next(
            item
            for item in bundle["source_anchors"]
            if item["source_id"] == "functional-requirement-1"
        )
        spec_units = [
            item
            for item in bundle["spec_units"]
            if item["source_anchor_ids"] == [anchor["id"]]
        ]
        implementation_units = [
            item
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [anchor["id"]]
        ]
        verification_units = [
            item
            for item in bundle["verification_units"]
            if item["source_anchor_ids"] == [anchor["id"]]
        ]

        self.assertEqual(anchor["view"], "requirements")
        self.assertEqual(
            sorted(item["id"] for item in spec_units),
            [
                "su.rupify.functional-requirement-1.approval-states",
                "su.rupify.functional-requirement-1.stage-gates",
            ],
        )
        self.assertEqual(
            sorted(item["id"] for item in implementation_units),
            [
                "iu.rupify.functional-requirement-1.approval-states",
                "iu.rupify.functional-requirement-1.stage-gates",
            ],
        )
        self.assertEqual(
            sorted(item["id"] for item in verification_units),
            [
                "vu.rupify.functional-requirement-1.approval-states",
                "vu.rupify.functional-requirement-1.stage-gates",
            ],
        )
        stage_gates = next(
            item
            for item in implementation_units
            if item["id"] == "iu.rupify.functional-requirement-1.stage-gates"
        )
        self.assertEqual(stage_gates["title"], "Implement workflow support: Support stage gates")
        self.assertEqual(stage_gates["summary"], "Support business process stage gates.")

    def test_generated_bundle_splits_multi_step_state_transition_chain(self) -> None:
        """A chain transition should decompose into separate transition pairs."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        implementation_units = [
            item
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.state-transitions.state-transition-1"
            ]
        ]

        self.assertEqual(
            sorted(item["id"] for item in implementation_units),
            [
                "iu.rupify.state-transition-1.active-to-retiring",
                "iu.rupify.state-transition-1.proposed-to-active",
                "iu.rupify.state-transition-1.retiring-to-retired",
            ],
        )

    def test_generated_bundle_derives_dependencies_and_assembly_rules(self) -> None:
        """Split units should receive deterministic dependency and assembly metadata."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        approval_states = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.functional-requirement-1.approval-states"
        )
        active_to_retiring = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.state-transition-1.active-to-retiring"
        )
        transition_rule = next(
            item
            for item in bundle["assembly_rules"]
            if item["id"] == "assembly.state-transition-1"
        )

        self.assertEqual(
            approval_states["dependencies"],
            ["iu.rupify.functional-requirement-1.stage-gates"],
        )
        self.assertEqual(
            active_to_retiring["dependencies"],
            ["iu.rupify.state-transition-1.proposed-to-active"],
        )
        self.assertEqual(
            transition_rule["member_spec_unit_ids"],
            [
                "su.rupify.state-transition-1.proposed-to-active",
                "su.rupify.state-transition-1.active-to-retiring",
                "su.rupify.state-transition-1.retiring-to-retired",
            ],
        )

        export_reporting = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.functional-requirement-2.export-reporting-data"
        )
        inventory_rule = next(
            item
            for item in bundle["assembly_rules"]
            if item["id"] == "assembly.functional-requirement-2"
        )
        self.assertEqual(
            export_reporting["dependencies"],
            ["iu.rupify.functional-requirement-2.maintain-system-inventory"],
        )
        self.assertEqual(
            inventory_rule["member_spec_unit_ids"],
            [
                "su.rupify.functional-requirement-2.maintain-system-inventory",
                "su.rupify.functional-requirement-2.export-reporting-data",
            ],
        )

    def test_generated_bundle_strengthens_verification_contracts(self) -> None:
        """Verification units should include family-specific setup and failure details."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        domain_invariant = next(
            item
            for item in bundle["verification_units"]
            if item["id"] == "vu.rupify.domain-invariant-1"
        )
        transition = next(
            item
            for item in bundle["verification_units"]
            if item["id"] == "vu.rupify.state-transition-4.active-to-deprecated"
        )
        constraint = next(
            item
            for item in bundle["verification_units"]
            if item["id"] == "vu.rupify.acceptance-constraint-requirement-1"
        )

        self.assertTrue(domain_invariant["setup_requirements"])
        self.assertTrue(domain_invariant["failure_conditions"])
        self.assertEqual(
            domain_invariant["invariants_preserved"],
            ["A System must have a business owner before it becomes Active."],
        )
        self.assertIn("starts in the Active state", transition["setup_requirements"][0])
        self.assertTrue(any("unexpected state" in item for item in transition["failure_conditions"]))
        self.assertTrue(any("violates the stated constraint" in item for item in constraint["failure_conditions"]))

    def test_generated_bundle_expands_broad_requirement_and_invariant_slices(self) -> None:
        """Broader requirement and invariant families should decompose into narrower units."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        functional_requirement_2_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.functional-requirements.functional-requirement-2"
            ]
        )
        domain_invariant_3_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.domain-invariants.domain-invariant-3"
            ]
        )

        self.assertEqual(
            functional_requirement_2_units,
            [
                "iu.rupify.functional-requirement-2.export-reporting-data",
                "iu.rupify.functional-requirement-2.maintain-system-inventory",
            ],
        )
        self.assertEqual(
            domain_invariant_3_units,
            [
                "iu.rupify.domain-invariant-3.record-contract-dates",
                "iu.rupify.domain-invariant-3.record-vendor",
            ],
        )


if __name__ == "__main__":
    unittest.main()
