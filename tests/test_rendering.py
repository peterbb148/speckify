"""Tests for rendered specification and issue artifacts."""

from __future__ import annotations

import unittest
from pathlib import Path

from speckify_tools.bundle_generation import generate_planning_bundle_file
from speckify_tools.rendering import render_specification_markdown


RUPIFY_EXPORT = Path(
    "/Volumes/Data/GitHub/Peterbb148/rupify/examples/it-systems-inventory-v2/exports/speckify-planning-export.json"
)


class RenderingTests(unittest.TestCase):
    """Rendering behavior for generated planning bundles."""

    def test_rendered_issue_projection_uses_documented_section_order(self) -> None:
        """Rendered issue bodies should follow the documented section order."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T13:30:00Z",
        )
        rendered_issue = bundle["rendered_issues"][0]
        body = rendered_issue["issue_body"]

        expected_sections = [
            "## Summary",
            "## Source Lineage",
            "## Scope",
            "## Acceptance Criteria",
            "## Verification Shape",
            "## Dependencies",
            "## Drift Checks",
        ]
        positions = [body.index(section) for section in expected_sections]
        self.assertEqual(positions, sorted(positions))

    def test_render_specification_markdown_summarizes_generated_bundle(self) -> None:
        """The consolidated specification view should summarize the generated bundle."""
        bundle = generate_planning_bundle_file(
            RUPIFY_EXPORT,
            generated_at="2026-04-20T13:30:00Z",
        )
        specification = render_specification_markdown(bundle)

        self.assertIn("# Speckified Specification", specification)
        self.assertIn("## Overview", specification)
        self.assertIn("## Implementation Units", specification)
        self.assertIn("Implement Acceptance Constraint 1", specification)


if __name__ == "__main__":
    unittest.main()
