"""Tests for end-to-end generated bundle validation."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle_file
from speckify_tools.validation import BundleValidationError, validate_bundle, validate_generated_bundle_file


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
RUPIFY_EXPORT = ROOT / "demo" / "it-systems-inventory-v2" / "input" / "speckify-planning-export.json"
LOYALTY_RUPIFY_EXPORT = (
    ROOT / "demo" / "loyalty-platform-v2" / "input" / "speckify-planning-export.json"
)


class GeneratedValidationTests(unittest.TestCase):
    """Validation behavior for generated planning bundles."""

    def test_generated_bundle_from_real_export_passes(self) -> None:
        """The real Rupify export should generate a valid bundle end to end."""
        bundle = validate_generated_bundle_file(RUPIFY_EXPORT, SCHEMA_DIR)

        self.assertEqual(
            bundle["bundle_metadata"]["decomposition_profile"],
            "rupify-structural-decomposition-v1",
        )
        self.assertEqual(len(bundle["trace_bundles"]), 25)
        self.assertEqual(len(bundle["dependency_edges"]), 9)
        self.assertEqual(len(bundle["assembly_rules"]), 4)

    def test_generated_bundle_from_loyalty_export_passes(self) -> None:
        """The loyalty-platform V2 export should generate a valid bundle end to end."""
        bundle = validate_generated_bundle_file(LOYALTY_RUPIFY_EXPORT, SCHEMA_DIR)

        self.assertEqual(len(bundle["trace_bundles"]), 74)
        self.assertEqual(len(bundle["dependency_edges"]), 39)
        self.assertEqual(len(bundle["assembly_rules"]), 10)

    def test_broken_generated_bundle_fails_reference_validation(self) -> None:
        """Reference drift in a generated bundle should fail explicitly."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T13:00:00Z",
        )
        bundle["trace_bundles"][0]["implementation_unit_ids"] = ["iu.rupify.missing"]

        with self.assertRaises(BundleValidationError) as error:
            validate_bundle(bundle, SCHEMA_DIR)

        messages = [issue.message for issue in error.exception.issues]
        self.assertTrue(any("Unknown implementation_unit reference" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
