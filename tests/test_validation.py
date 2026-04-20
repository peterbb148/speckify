"""Tests for Speckify bundle validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from speckify_tools.validation import BundleValidationError, load_json, validate_bundle_file


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
VALID_BUNDLE = ROOT / "fixtures" / "speckify-bundle" / "authentication-basic.bundle.json"


class ValidationTests(unittest.TestCase):
    """Validation behavior for planning bundles."""

    def test_valid_bundle_passes(self) -> None:
        """Fixture bundle should validate successfully."""
        validate_bundle_file(VALID_BUNDLE, SCHEMA_DIR)

    def test_missing_required_field_fails(self) -> None:
        """Missing required fields should fail clearly."""
        bundle = load_json(VALID_BUNDLE)
        del bundle["bundle_metadata"]["bundle_id"]

        with tempfile.TemporaryDirectory() as temp_dir:
            bundle_path = Path(temp_dir) / "invalid-bundle.json"
            bundle_path.write_text(json.dumps(bundle))

            with self.assertRaises(BundleValidationError) as error:
                validate_bundle_file(bundle_path, SCHEMA_DIR)

        messages = [issue.message for issue in error.exception.issues]
        self.assertTrue(any("bundle_id" in message for message in messages))

    def test_broken_reference_fails(self) -> None:
        """Broken cross-record references should fail clearly."""
        bundle = load_json(VALID_BUNDLE)
        bundle["implementation_units"][0]["verification_unit_ids"] = ["vu.missing"]

        with tempfile.TemporaryDirectory() as temp_dir:
            bundle_path = Path(temp_dir) / "invalid-bundle.json"
            bundle_path.write_text(json.dumps(bundle))

            with self.assertRaises(BundleValidationError) as error:
                validate_bundle_file(bundle_path, SCHEMA_DIR)

        messages = [issue.message for issue in error.exception.issues]
        self.assertTrue(any("Unknown verification_unit reference" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
