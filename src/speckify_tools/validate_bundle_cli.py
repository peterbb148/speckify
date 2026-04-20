"""CLI entry point for Speckify bundle validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .validation import BundleValidationError, validate_bundle_file


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Validate a Speckify planning bundle.")
    parser.add_argument("bundle", help="Path to the planning bundle JSON file.")
    parser.add_argument(
        "--schema-dir",
        default="schemas",
        help="Directory containing the Speckify JSON Schema files.",
    )
    return parser


def main() -> int:
    """Run the validation CLI.

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_bundle_file(Path(args.bundle), Path(args.schema_dir))
    except BundleValidationError as exc:
        print("Bundle validation failed:", file=sys.stderr)
        for issue in exc.issues:
            print(f"- {issue.path}: {issue.message}", file=sys.stderr)
        return 1

    print("Bundle validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
