"""Tests for end-to-end generated bundle validation."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle_file
from speckify_tools.validation import BundleValidationError, validate_bundle, validate_generated_bundle_file


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)


class GeneratedValidationTests(unittest.TestCase):
    """Validation behavior for generated planning bundles."""

    def test_generated_bundle_from_real_export_passes(self) -> None:
        """The real Rupify export should generate a valid bundle end to end."""
        bundle = validate_generated_bundle_file(RUPIFY_EXPORT, SCHEMA_DIR)

        self.assertEqual(bundle["bundle_metadata"]["decomposition_profile"], "rupify-split-v1")
        self.assertEqual(len(bundle["trace_bundles"]), 36)

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
