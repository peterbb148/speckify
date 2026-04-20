"""CLI entry point for the Rupify hand-off demo import."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .rupify_handoff_demo import write_demo_outputs


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Import a Rupify hand-off export and generate Speckify demo outputs."
    )
    parser.add_argument("source_export", help="Path to the Rupify speckify-planning-export.json file.")
    parser.add_argument("demo_dir", help="Destination demo directory in the Speckify repo.")
    return parser


def main() -> int:
    """Run the demo import CLI.

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args()

    report = write_demo_outputs(Path(args.source_export), Path(args.demo_dir))
    if report["clean_import"]:
        print("Rupify hand-off import passed cleanly.")
        return 0

    print("Rupify hand-off import completed with blockers.", file=sys.stderr)
    for issue in report["errors"]:
        print(f"- {issue}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
