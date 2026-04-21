"""Tests for Speckify planning bundle generation."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle
from speckify_tools.rupify_import import import_rupify_export, import_rupify_export_file
from speckify_tools.validation import validate_bundle


RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)
LOYALTY_RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform-v2/exports/speckify-planning-export.json"
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
            "rupify-structural-decomposition-v1",
        )
        self.assertEqual(len(bundle["source_anchors"]), 29)
        self.assertEqual(len(bundle["spec_units"]), 36)
        self.assertEqual(len(bundle["implementation_units"]), 36)
        self.assertEqual(len(bundle["verification_units"]), 36)
        self.assertEqual(len(bundle["trace_bundles"]), 36)
        self.assertEqual(len(bundle["dependency_edges"]), 14)
        self.assertEqual(len(bundle["assembly_rules"]), 4)
        self.assertEqual(len(bundle["rendered_issues"]), 36)
        self.assertEqual(bundle["unresolved_ambiguities"], [])

        validate_bundle(bundle, SCHEMA_DIR)

    def test_generated_bundle_preserves_lineage_for_split_functional_requirement(self) -> None:
        """A requirement with explicit sub-obligations should preserve clean lineage."""
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
                "su.rupify.functional-requirement-1.support-approval-states",
                "su.rupify.functional-requirement-1.support-stage-gates",
            ],
        )
        self.assertEqual(
            sorted(item["id"] for item in implementation_units),
            [
                "iu.rupify.functional-requirement-1.support-approval-states",
                "iu.rupify.functional-requirement-1.support-stage-gates",
            ],
        )
        self.assertEqual(
            sorted(item["id"] for item in verification_units),
            [
                "vu.rupify.functional-requirement-1.support-approval-states",
                "vu.rupify.functional-requirement-1.support-stage-gates",
            ],
        )
        requirement = next(
            item
            for item in implementation_units
            if item["id"] == "iu.rupify.functional-requirement-1.support-stage-gates"
        )
        self.assertEqual(
            requirement["title"],
            "Implement workflow support: Support stage gates",
        )
        self.assertEqual(
            requirement["summary"],
            "Support stage gates.",
        )

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
        """Structural state-transition splits should receive deterministic metadata."""
        export = import_rupify_export_file(RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

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

    def test_generated_bundle_keeps_broad_requirement_and_invariant_slices_intact(self) -> None:
        """Broad records remain intact until a formal decomposition operator exists."""
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
            ["iu.rupify.functional-requirement-2"],
        )
        self.assertEqual(
            domain_invariant_3_units,
            ["iu.rupify.domain-invariant-3"],
        )

    def test_generated_bundle_applies_explicit_conjunction_operator(self) -> None:
        """Explicit structured sub-obligations should decompose into formal conjunction slices."""
        export = import_rupify_export(
            {
                "export_metadata": {"export_kind": "speckify_planning_export"},
                "elements": [
                    {
                        "id": "requirement-1",
                        "family": "functional_requirements",
                        "name": "Requirement 1",
                        "text": "Composite requirement.",
                        "content_semantics": "normative",
                        "readiness_status": "ready",
                        "normative_ready": True,
                        "obligations": [
                            {
                                "id": "capture-credentials",
                                "title": "Capture credentials",
                                "summary": "Capture submitted user credentials.",
                                "acceptance": "System accepts credential input.",
                            },
                            {
                                "id": "validate-credentials",
                                "title": "Validate credentials",
                                "summary": "Validate submitted user credentials.",
                                "acceptance": "System validates credential input.",
                            },
                        ],
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
        )

        bundle = generate_planning_bundle(export, generated_at="2026-04-21T08:00:00Z")

        self.assertEqual(
            sorted(item["id"] for item in bundle["implementation_units"]),
            [
                "iu.rupify.requirement-1.capture-credentials",
                "iu.rupify.requirement-1.validate-credentials",
            ],
        )
        assembly_rule = bundle["assembly_rules"][0]
        self.assertEqual(assembly_rule["rule_type"], "conjunctive_set")
        self.assertEqual(
            assembly_rule["member_spec_unit_ids"],
            [
                "su.rupify.requirement-1.capture-credentials",
                "su.rupify.requirement-1.validate-credentials",
            ],
        )
        validate_bundle(bundle, SCHEMA_DIR)

    def test_generated_bundle_fails_closed_without_explicit_structured_parts(self) -> None:
        """Wording alone must not trigger conjunction decomposition."""
        export = import_rupify_export(
            {
                "export_metadata": {"export_kind": "speckify_planning_export"},
                "elements": [
                    {
                        "id": "requirement-1",
                        "family": "functional_requirements",
                        "name": "Requirement 1",
                        "text": "The system validates reward eligibility and available points.",
                        "content_semantics": "normative",
                        "readiness_status": "ready",
                        "normative_ready": True,
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
        )

        bundle = generate_planning_bundle(export, generated_at="2026-04-21T08:00:00Z")

        self.assertEqual(
            [item["id"] for item in bundle["implementation_units"]],
            ["iu.rupify.requirement-1"],
        )
        self.assertEqual(bundle["assembly_rules"], [])

    def test_generated_bundle_applies_explicit_scenario_flow_operator(self) -> None:
        """Explicit ordered scenario flow should decompose into ordered scenario segments."""
        export = import_rupify_export(
            {
                "export_metadata": {"export_kind": "speckify_planning_export"},
                "elements": [
                    {
                        "id": "scenario-1",
                        "family": "scenarios",
                        "name": "Payment Delay",
                        "text": "Scenario summary.",
                        "content_semantics": "normative",
                        "readiness_status": "ready",
                        "normative_ready": True,
                        "attributes": {
                            "flow_of_events": [
                                "Customer submits redemption.",
                                "System waits for payment confirmation.",
                                "System pauses fulfillment.",
                            ]
                        },
                    }
                ],
                "trace_links": [],
                "summary": {
                    "ready_normative_ids": ["scenario-1"],
                    "ready_normative_count": 1,
                    "blocking_ambiguity_count": 0,
                    "trace_link_count": 0,
                },
            }
        )

        bundle = generate_planning_bundle(export, generated_at="2026-04-21T10:00:00Z")

        self.assertEqual(
            [item["id"] for item in bundle["implementation_units"]],
            [
                "iu.rupify.scenario-1.segment-1",
                "iu.rupify.scenario-1.segment-2",
                "iu.rupify.scenario-1.segment-3",
            ],
        )
        self.assertEqual(
            bundle["implementation_units"][1]["dependencies"],
            ["iu.rupify.scenario-1.segment-1"],
        )
        self.assertEqual(
            bundle["implementation_units"][2]["dependencies"],
            ["iu.rupify.scenario-1.segment-2"],
        )
        self.assertEqual(bundle["assembly_rules"][0]["rule_type"], "ordered_sequence")
        validate_bundle(bundle, SCHEMA_DIR)

    def test_generated_bundle_keeps_loyalty_use_case_steps_intact_without_formal_operator(self) -> None:
        """Loyalty step records should remain intact without a structural split operator."""
        export = import_rupify_export_file(LOYALTY_RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        rewards_display_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.use-case-steps.browse-rewards-step-2"
            ]
        )
        redemption_validation_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.use-case-steps.redeem-reward-step-2"
            ]
        )
        redemption_reservation_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.use-case-steps.redeem-reward-step-3"
            ]
        )

        self.assertEqual(
            rewards_display_units,
            ["iu.rupify.browse-rewards-step-2"],
        )
        self.assertEqual(
            redemption_validation_units,
            ["iu.rupify.redeem-reward-step-2"],
        )
        self.assertEqual(
            redemption_reservation_units,
            ["iu.rupify.redeem-reward-step-3"],
        )

    def test_generated_bundle_keeps_loyalty_catalog_and_analytics_steps_intact(self) -> None:
        """Catalog and analytics steps should remain intact without a formal split operator."""
        export = import_rupify_export_file(LOYALTY_RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        catalog_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.use-case-steps.manage-reward-catalog-step-3"
            ]
        )
        analytics_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.use-case-steps.review-redemption-analytics-step-2"
            ]
        )

        self.assertEqual(
            catalog_units,
            ["iu.rupify.manage-reward-catalog-step-3"],
        )
        self.assertEqual(
            analytics_units,
            ["iu.rupify.review-redemption-analytics-step-2"],
        )

    def test_generated_bundle_derives_loyalty_step_and_trace_dependencies(self) -> None:
        """Loyalty V2 should derive dependencies from step order and explicit trace links."""
        export = import_rupify_export_file(LOYALTY_RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        redeem_reward_step = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.redeem-reward-step-2"
        )
        redeem_reward = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.redeem-reward"
        )
        acceptance_constraint = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.acceptance-constraint-requirement-6"
        )
        transition = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.state-transition-4.draft-to-published"
        )

        self.assertEqual(
            redeem_reward_step["dependencies"],
            ["iu.rupify.redeem-reward-step-1"],
        )
        self.assertEqual(
            redeem_reward["dependencies"],
            ["iu.rupify.non-functional-requirement-6"],
        )
        self.assertEqual(
            acceptance_constraint["dependencies"],
            ["iu.rupify.non-functional-requirement-6"],
        )
        self.assertEqual(
            transition["dependencies"],
            ["iu.rupify.guard-condition-2"],
        )

    def test_generated_bundle_splits_loyalty_scenarios_but_keeps_guards_intact(self) -> None:
        """Scenario flow segments may split from explicit structure while guards stay intact."""
        export = import_rupify_export_file(LOYALTY_RUPIFY_EXPORT)
        bundle = generate_planning_bundle(export, generated_at="2026-04-20T12:30:00Z")

        invalid_catalog_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.scenarios.scenario-invalid-catalog-change"
            ]
        )
        missing_payment_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.scenarios.scenario-missing-payment-confirmation"
            ]
        )
        guard_units = sorted(
            item["id"]
            for item in bundle["implementation_units"]
            if item["source_anchor_ids"] == [
                "anchor.rupify.guard-conditions.guard-condition-2"
            ]
        )

        self.assertEqual(
            invalid_catalog_units,
            [
                "iu.rupify.scenario-invalid-catalog-change.segment-1",
                "iu.rupify.scenario-invalid-catalog-change.segment-2",
                "iu.rupify.scenario-invalid-catalog-change.segment-3",
            ],
        )
        self.assertEqual(
            missing_payment_units,
            [
                "iu.rupify.scenario-missing-payment-confirmation.segment-1",
                "iu.rupify.scenario-missing-payment-confirmation.segment-2",
                "iu.rupify.scenario-missing-payment-confirmation.segment-3",
            ],
        )
        self.assertEqual(
            guard_units,
            ["iu.rupify.guard-condition-2"],
        )

        invalid_segment_2 = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.scenario-invalid-catalog-change.segment-2"
        )
        invalid_segment_3 = next(
            item
            for item in bundle["implementation_units"]
            if item["id"] == "iu.rupify.scenario-invalid-catalog-change.segment-3"
        )
        self.assertEqual(
            invalid_segment_2["dependencies"],
            ["iu.rupify.scenario-invalid-catalog-change.segment-1"],
        )
        self.assertEqual(
            invalid_segment_3["dependencies"],
            ["iu.rupify.scenario-invalid-catalog-change.segment-2"],
        )


if __name__ == "__main__":
    unittest.main()
