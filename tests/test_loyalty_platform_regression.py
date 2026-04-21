"""Regression coverage for the loyalty-platform V2 hand-off demo."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from speckify_tools.rupify_handoff_demo import write_demo_outputs


ROOT = Path(__file__).resolve().parents[1]
RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform-v2/exports/speckify-planning-export.json"
)
EXPECTED_DEMO_DIR = ROOT / "demo" / "loyalty-platform-v2"
REVIEW_SUMMARY = ROOT / "fixtures" / "review" / "loyalty-platform-v2-summary.json"


def _relative_files(root: Path) -> list[Path]:
    """List relative file paths under a directory."""
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


class LoyaltyPlatformRegressionTests(unittest.TestCase):
    """Regression behavior for the loyalty-platform V2 demo."""

    def test_loyalty_demo_outputs_match_checked_in_regression_files(self) -> None:
        """Regenerated loyalty V2 demo outputs should match the committed demo directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            actual_demo_dir = Path(temp_dir) / "loyalty-platform-v2"
            write_demo_outputs(RUPIFY_EXPORT, actual_demo_dir)

            expected_files = sorted(
                [Path("input") / path for path in _relative_files(EXPECTED_DEMO_DIR / "input")]
                + [Path("output") / path for path in _relative_files(EXPECTED_DEMO_DIR / "output")]
            )
            actual_files = sorted(
                [Path("input") / path for path in _relative_files(actual_demo_dir / "input")]
                + [Path("output") / path for path in _relative_files(actual_demo_dir / "output")]
            )
            self.assertEqual(actual_files, expected_files)

            for relative_path in actual_files:
                expected_path = EXPECTED_DEMO_DIR / relative_path
                actual_path = actual_demo_dir / relative_path
                self.assertEqual(
                    actual_path.read_text(),
                    expected_path.read_text(),
                    msg=f"Mismatch for {relative_path}",
                )

    def test_loyalty_demo_bundle_is_clean_and_non_empty(self) -> None:
        """The loyalty-platform V2 fixture should produce a clean non-empty bundle."""
        import_report = json.loads((EXPECTED_DEMO_DIR / "output" / "import-report.json").read_text())
        bundle = json.loads((EXPECTED_DEMO_DIR / "output" / "planning-bundle.json").read_text())
        review_summary = json.loads(REVIEW_SUMMARY.read_text())

        self.assertTrue(import_report["clean_import"])
        self.assertEqual(import_report["counts"]["ready_normative_count"], 62)
        self.assertEqual(len(bundle["implementation_units"]), 76)
        self.assertEqual(len(bundle["rendered_issues"]), 76)
        self.assertEqual(review_summary["counts"]["implementation_units"], 76)
        self.assertEqual(review_summary["counts"]["dependency_edges"], 39)


if __name__ == "__main__":
    unittest.main()
