"""Regression coverage for the IT systems inventory V2 hand-off demo."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from speckify_tools.rupify_handoff_demo import write_demo_outputs


ROOT = Path(__file__).resolve().parents[1]
RUPIFY_EXPORT = ROOT / "demo" / "it-systems-inventory-v2" / "input" / "speckify-planning-export.json"
EXPECTED_DEMO_DIR = ROOT / "demo" / "it-systems-inventory-v2"


def _relative_files(root: Path) -> list[Path]:
    """List relative file paths under a directory."""
    return sorted(
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
    )


def _normalize_report_markdown(text: str) -> str:
    """Normalize source-path lines that legitimately vary by execution location."""
    lines = []
    for line in text.splitlines():
        if line.startswith("Source export: "):
            lines.append("Source export: `<normalized>`")
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


class ITSystemsInventoryV2RegressionTests(unittest.TestCase):
    """Regression behavior for the checked-in demo outputs."""

    def test_demo_outputs_match_checked_in_regression_files(self) -> None:
        """Regenerated demo outputs should match the committed demo directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            actual_demo_dir = Path(temp_dir) / "it-systems-inventory-v2"
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
                    _normalize_report_markdown(actual_path.read_text()),
                    _normalize_report_markdown(expected_path.read_text()),
                    msg=f"Mismatch for {relative_path}",
                )


if __name__ == "__main__":
    unittest.main()
