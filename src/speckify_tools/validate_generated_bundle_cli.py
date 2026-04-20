"""CLI entry point for end-to-end generated bundle validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .validation import BundleValidationError, validate_generated_bundle_file


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Generate and validate a Speckify planning bundle from a Rupify export."
    )
    parser.add_argument("source_export", help="Path to the Rupify planning export JSON file.")
    parser.add_argument(
        "--schema-dir",
        default="schemas",
        help="Directory containing the Speckify JSON Schema files.",
    )
    return parser


def main() -> int:
    """Run the generated-bundle validation CLI.

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        bundle = validate_generated_bundle_file(
            Path(args.source_export),
            Path(args.schema_dir),
        )
    except BundleValidationError as exc:
        print("Generated bundle validation failed:", file=sys.stderr)
        for issue in exc.issues:
            print(f"- {issue.path}: {issue.message}", file=sys.stderr)
        return 1

    print(
        "Generated bundle validation passed "
        f"({len(bundle['implementation_units'])} implementation units)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
