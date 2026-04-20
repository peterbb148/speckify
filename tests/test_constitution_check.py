"""Tests for constitutional enforcement checks."""

from __future__ import annotations

import textwrap
import unittest

from speckify_tools.constitution_check import find_violations_in_text


class ConstitutionCheckTests(unittest.TestCase):
    """Behavior of the constitutional checker."""

    def test_detects_exact_source_phrase_match(self) -> None:
        """Exact source-text checks should be rejected."""
        source = textwrap.dedent(
            """
            def bad(text: str) -> None:
                if text == "System validates and publishes the change.":
                    return
            """
        )

        violations = find_violations_in_text(source, "src/speckify_tools/example.py")

        self.assertEqual(len(violations), 1)
        self.assertIn("constitutionally forbidden", violations[0].reason)

    def test_detects_phrase_membership_against_lowered_text(self) -> None:
        """Membership checks against lowered source text should be rejected."""
        source = textwrap.dedent(
            """
            def bad(lowered: str) -> None:
                if "maintain reward catalog entries and campaign rules" in lowered:
                    return
            """
        )

        violations = find_violations_in_text(source, "src/speckify_tools/example.py")

        self.assertEqual(len(violations), 1)
        self.assertIn("membership check", violations[0].reason.lower())

    def test_allows_structural_family_checks(self) -> None:
        """Typed structural checks should remain allowed."""
        source = textwrap.dedent(
            """
            def ok(element) -> None:
                if element.family == "state_transitions":
                    return
            """
        )

        violations = find_violations_in_text(source, "src/speckify_tools/example.py")

        self.assertEqual(violations, [])

    def test_allows_descriptive_output_strings(self) -> None:
        """Output prose should not be mistaken for transform violations."""
        source = textwrap.dedent(
            """
            def ok() -> str:
                return "Implement workflow support: Maintain reward catalog entries"
            """
        )

        violations = find_violations_in_text(source, "src/speckify_tools/example.py")

        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
