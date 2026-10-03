#!/usr/bin/env python3
"""Check canonical skill metadata, inline file links, and source layout.

Metadata checks cover this repository's single-line frontmatter and JSON-quoted
Codex interface fields, not the complete YAML or runtime configuration schemas.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LINK_PATTERN = re.compile(r"\[[^\]\n]*\]\(([^\s)]+)\)")


def check_metadata(skill: Path) -> list[str]:
    errors: list[str] = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return [f"{entry}: missing skill entry point"]
    lines = entry.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return [f"{entry}: missing frontmatter delimiters"]
    header: dict[str, str] = {}
    for line in lines[1 : lines.index("---", 1)]:
        key, separator, value = line.partition(":")
        if not separator or not value.strip() or key in header:
            errors.append(f"{entry}: invalid or duplicate single-line field: {key}")
        header[key] = value.strip()
    name = header.get("name", "")
    if name != skill.name or len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append(f"{entry}: name must match the lowercase hyphenated folder name")
    description = header.get("description", "")
    if not description or len(description) > 1024:
        errors.append(f"{entry}: description must contain 1-1024 characters")

    metadata = skill / "agents" / "openai.yaml"
    if not metadata.is_file():
        return errors + [f"{metadata}: missing Codex interface metadata"]
    content = metadata.read_text(encoding="utf-8")
    if not content.startswith("interface:\n"):
        errors.append(f"{metadata}: missing interface mapping")
    for key in ("display_name", "short_description", "default_prompt"):
        matches = re.findall(rf"^  {key}: (.+)$", content, flags=re.MULTILINE)
        try:
            value = json.loads(matches[0]) if len(matches) == 1 else None
        except json.JSONDecodeError:
            value = None
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{metadata}: {key} must be one nonempty JSON-quoted string")
        elif key == "default_prompt" and f"${skill.name}" not in value:
            errors.append(f"{metadata}: default_prompt must name ${skill.name}")
    return errors


def check_skills(root: Path) -> list[str]:
    errors: list[str] = []
    legacy = root / "codex" / "skills"
    if any(path.is_file() for path in legacy.rglob("*")):
        errors.append(f"{legacy}: separate skill sources are obsolete; use skills/ only")
    directory = root / "skills"
    if not directory.is_dir():
        return errors + [f"{directory}: missing skills directory"]
    skills = sorted(
        path for path in directory.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    if not skills:
        errors.append(f"{directory}: no skills found")
    for skill in skills:
        errors.extend(check_metadata(skill))
        for document in skill.rglob("*.md"):
            content = document.read_text(encoding="utf-8")
            for link in LINK_PATTERN.findall(content):
                if link.startswith(("#", "//")) or re.match(r"^[a-zA-Z][\w+.-]*:", link):
                    continue
                target = link.split("#", 1)[0]
                if not (document.parent / target).exists():
                    errors.append(f"{document}: broken local link {link}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    errors = check_skills(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: canonical skill metadata, local file links, and single-source layout")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
