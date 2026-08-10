#!/usr/bin/env python3
"""Deep-merge a JSON or TOML configuration layer over an existing file."""

from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Optional


Config = dict[str, Any]


def split_dotted_key(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: Optional[str] = None
    for character in value:
        if character in {'"', "'"}:
            quote = None if quote == character else character if quote is None else quote
            current.append(character)
        elif character == "." and quote is None:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    parts.append("".join(current).strip())
    return [ast.literal_eval(part) if part[:1] in {'"', "'"} else part for part in parts]


def parse_toml_value(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        try:
            return int(value)
        except ValueError:
            return float(value)


def parse_toml(content: str) -> Config:
    config: Config = {}
    table = config
    for line_number, raw_line in enumerate(content.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            table = config
            for part in split_dotted_key(line[1:-1]):
                table = table.setdefault(part, {})
            continue
        if "=" not in line:
            raise ValueError(f"Unsupported TOML syntax on line {line_number}: {raw_line}")
        key, value = line.split("=", 1)
        key = key.strip()
        parsed_key = ast.literal_eval(key) if key[:1] in {'"', "'"} else key
        table[parsed_key] = parse_toml_value(value.strip())
    return config


def deep_merge(base: Config, layer: Config) -> Config:
    merged = dict(base)
    for key, value in layer.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = value
    return merged


def toml_value(value: Any) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    raise TypeError(f"Unsupported TOML value: {type(value).__name__}")


def quoted_key(key: str) -> str:
    return json.dumps(key)


def render_toml(config: Config) -> str:
    lines: list[str] = []

    def render_table(table: Config, path: list[str]) -> None:
        scalar_items = [(key, value) for key, value in table.items() if not isinstance(value, dict)]
        table_items = [(key, value) for key, value in table.items() if isinstance(value, dict)]

        if path:
            if lines and lines[-1] != "":
                lines.append("")
            lines.append("[" + ".".join(quoted_key(part) for part in path) + "]")
        for key, value in scalar_items:
            lines.append(f"{quoted_key(key)} = {toml_value(value)}")
        for key, value in table_items:
            render_table(value, [*path, key])

    render_table(config, [])
    return "\n".join(lines).rstrip() + "\n"


def load_config(config_format: str, config_path: Path) -> Config:
    if not config_path.exists():
        return {}
    with config_path.open("rb") as config_file:
        if config_format == "toml":
            return parse_toml(config_file.read().decode())
        return json.load(config_file)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=("json", "toml"))
    parser.add_argument("base", type=Path)
    parser.add_argument("layer", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    merged = deep_merge(load_config(args.format, args.base), load_config(args.format, args.layer))
    rendered = json.dumps(merged, indent=2) + "\n" if args.format == "json" else render_toml(merged)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=args.output.parent, delete=False) as output_file:
        output_file.write(rendered)
        temporary_path = Path(output_file.name)
    os.replace(temporary_path, args.output)


if __name__ == "__main__":
    main()
