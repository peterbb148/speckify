"""Constitution enforcement checks for Speckify transform code."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


TRANSFORM_ROOT = Path("src/speckify_tools")

SUSPICIOUS_LINE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"""\bif\s+["'][^"']+["']\s+in\s+(text|lowered)\b"""),
        "Phrase-specific membership check against source text is constitutionally forbidden.",
    ),
    (
        re.compile(r"""\bif\s+(text|lowered)\s*==\s*["'][^"']+["']"""),
        "Exact source-phrase comparison in transform code is constitutionally forbidden.",
    ),
    (
        re.compile(r"""\bif\s+(text|lowered)\.(startswith|endswith)\(\s*["'][^"']+["']\s*\)"""),
        "Prefix/suffix matching on source text in transform code is constitutionally forbidden.",
    ),
)


@dataclass(frozen=True)
class ConstitutionViolation:
    """One constitutional violation detected in source or staged diff."""

    path: str
    line_number: int
    line_text: str
    reason: str


def _is_transform_python_path(path: str) -> bool:
    """Return whether a path should be checked by the constitution guard."""
    pure = Path(path)
    return (
        pure.suffix == ".py"
        and pure.parts[:2] == TRANSFORM_ROOT.parts
        and pure.name != "__init__.py"
    )


def find_violations_in_text(source: str, path: str) -> list[ConstitutionViolation]:
    """Scan full file contents for constitution-breaking phrase-shaped logic."""
    violations: list[ConstitutionViolation] = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for pattern, reason in SUSPICIOUS_LINE_PATTERNS:
            if pattern.search(line):
                violations.append(
                    ConstitutionViolation(
                        path=path,
                        line_number=line_number,
                        line_text=stripped,
                        reason=reason,
                    )
                )
                break
    return violations


def _staged_python_paths() -> list[str]:
    """Return staged transform python files for pre-commit enforcement."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [path for path in result.stdout.splitlines() if _is_transform_python_path(path)]


def _load_staged_file(path: str) -> str:
    """Read the staged version of one file from the index."""
    result = subprocess.run(
        ["git", "show", f":{path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def staged_violations() -> list[ConstitutionViolation]:
    """Scan staged transform files for newly introduced violations."""
    violations: list[ConstitutionViolation] = []
    for path in _staged_python_paths():
        violations.extend(find_violations_in_text(_load_staged_file(path), path))
    return violations


def repo_violations() -> list[ConstitutionViolation]:
    """Scan transform code in the working tree for all current violations."""
    violations: list[ConstitutionViolation] = []
    for path in sorted(TRANSFORM_ROOT.glob("*.py")):
        if path.name == "__init__.py":
            continue
        violations.extend(find_violations_in_text(path.read_text(), str(path)))
    return violations


def _render_violations(violations: list[ConstitutionViolation]) -> str:
    """Render violations as a human-readable report."""
    lines = [
        "Constitution check failed.",
        "The GitHub SpecKit Constitution forbids phrase-specific transform logic.",
        "",
    ]
    for violation in violations:
        lines.append(f"{violation.path}:{violation.line_number}")
        lines.append(f"  {violation.reason}")
        lines.append(f"  {violation.line_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    """Run constitution enforcement from the command line."""
    args = argv if argv is not None else sys.argv[1:]
    mode = "--staged" if "--all-files" not in args else "--all-files"

    violations = staged_violations() if mode == "--staged" else repo_violations()
    if violations:
        sys.stderr.write(_render_violations(violations))
        return 1

    print("Constitution check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
