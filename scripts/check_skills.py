#!/usr/bin/env python3
"""Check local skill metadata, inline file links, and cross-runtime content parity.

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


def check_metadata(skill: Path, codex: bool) -> list[str]:
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

    if codex:
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


def shared_files(skill: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(skill): path.read_bytes()
        for path in skill.rglob("*")
        if path.is_file() and path.relative_to(skill).parts[0] != "agents"
    }


def check_skills(root: Path) -> list[str]:
    errors: list[str] = []
    inventories: list[dict[str, Path]] = []
    for relative in ("skills", "codex/skills"):
        directory = root / relative
        if not directory.is_dir():
            errors.append(f"{directory}: missing skills directory")
            inventories.append({})
            continue
        skills = {
            path.name: path
            for path in directory.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        }
        if not skills:
            errors.append(f"{directory}: no skills found")
        inventories.append(skills)
        for skill in skills.values():
            errors.extend(check_metadata(skill, codex=relative == "codex/skills"))
            for document in skill.rglob("*.md"):
                content = document.read_text(encoding="utf-8")
                for link in LINK_PATTERN.findall(content):
                    if link.startswith(("#", "//")) or re.match(r"^[a-zA-Z][\w+.-]*:", link):
                        continue
                    target = link.split("#", 1)[0]
                    if not (document.parent / target).exists():
                        errors.append(f"{document}: broken local link {link}")

    opencode, codex = inventories
    for name, source in opencode.items():
        if name not in codex:
            errors.append(f"{name}: missing Codex counterpart")
            continue
        source_files, target_files = shared_files(source), shared_files(codex[name])
        for path in sorted(source_files.keys() | target_files.keys()):
            if source_files.get(path) != target_files.get(path):
                errors.append(f"{name}/{path}: OpenCode/Codex content differs or is missing")
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
    print("PASS: skill metadata, local file links, and shared runtime content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
