#!/usr/bin/env python3
"""Validate the local Abandon Skill package without third-party modules."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_PATHS = (
    "SKILL.md",
    "README.md",
    "references/MODES.md",
    "references/SCORING.md",
    "references/EXAMPLES.md",
    "assets/REQUEST_TEMPLATE.md",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).is_file():
            errors.append(f"missing required package file: {relative_path}")

    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return errors

    try:
        metadata = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
        return errors

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if not NAME_PATTERN.fullmatch(name):
        errors.append("name must contain lowercase letters, digits, and single hyphens only")
    if name != root.name:
        errors.append(f"name '{name}' must match parent directory '{root.name}'")
    if not 1 <= len(description) <= 1024:
        errors.append("description must contain 1-1024 characters")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: valid Abandon Skill package at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
