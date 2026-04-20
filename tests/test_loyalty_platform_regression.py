"""Regression coverage for the loyalty-platform hand-off demo."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from speckify_tools.rupify_handoff_demo import write_demo_outputs


ROOT = Path(__file__).resolve().parents[1]
RUPIFY_MODEL = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/loyalty-platform/specops-model.json"
)
EXPECTED_DEMO_DIR = ROOT / "demo" / "loyalty-platform"
REVIEW_SUMMARY = ROOT / "fixtures" / "review" / "loyalty-platform-summary.json"


def _relative_files(root: Path) -> list[Path]:
    """List relative file paths under a directory."""
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


class LoyaltyPlatformRegressionTests(unittest.TestCase):
    """Regression behavior for the loyalty-platform demo."""

    def test_loyalty_demo_outputs_match_checked_in_regression_files(self) -> None:
        """Regenerated loyalty demo outputs should match the committed demo directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path("/tmp/speckify-planning-export-loyalty.json")
            self._generate_planning_export(export_path)

            actual_demo_dir = Path(temp_dir) / "loyalty-platform"
            write_demo_outputs(export_path, actual_demo_dir)

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

    def test_loyalty_demo_bundle_is_clean_and_empty(self) -> None:
        """The loyalty-platform fixture should currently produce a clean empty bundle."""
        import_report = json.loads((EXPECTED_DEMO_DIR / "output" / "import-report.json").read_text())
        bundle = json.loads((EXPECTED_DEMO_DIR / "output" / "planning-bundle.json").read_text())
        review_summary = json.loads(REVIEW_SUMMARY.read_text())

        self.assertTrue(import_report["clean_import"])
        self.assertEqual(import_report["counts"]["ready_normative_count"], 0)
        self.assertEqual(len(bundle["implementation_units"]), 0)
        self.assertEqual(len(bundle["rendered_issues"]), 0)
        self.assertEqual(review_summary["counts"]["implementation_units"], 0)

    def _generate_planning_export(self, output_path: Path) -> None:
        """Generate a planning export from the loyalty-platform Rupify model."""
        import subprocess

        subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-m",
                "rupify_tools.planning_export_cli",
                "--model",
                str(RUPIFY_MODEL),
                "--output",
                str(output_path),
            ],
            cwd="/Volumes/Data/GitHub/Peterbb148/rupify",
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
