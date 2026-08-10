#!/usr/bin/env python3
"""Register one independent config layer and exactly rebuild managed runtime state."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Dict, List

from merge_config import Config, deep_merge, load_config, render_toml


ASSET_TARGETS = {
    "opencode_commands": ("opencode", "commands"),
    "opencode_skills": ("opencode", "skills"),
    "codex_agents": ("codex", "agents"),
    "codex_skills": ("codex", "skills"),
}


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=str(path.parent), delete=False) as output:
        output.write(content)
        temporary = Path(output.name)
    os.replace(str(temporary), str(path))


def load_registry(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text()).get("layers", [])


def asset_map(layers: List[Dict[str, Any]], category: str) -> Dict[str, Path]:
    assets: Dict[str, Path] = {}
    for layer in layers:
        source_value = layer.get(category)
        if not source_value:
            continue
        source_dir = Path(source_value)
        if source_dir.is_dir():
            for source in source_dir.iterdir():
                if not source.name.startswith("."):
                    assets[source.name] = source.resolve()
    return assets


def replace_managed_link(target: Path, source: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.is_dir():
        shutil.rmtree(str(target))
    temporary = target.with_name(target.name + ".new")
    if temporary.is_symlink() or temporary.exists():
        temporary.unlink()
    temporary.symlink_to(source)
    os.replace(str(temporary), str(target))


def reconcile_assets(
    previous_layers: List[Dict[str, Any]],
    layers: List[Dict[str, Any]],
    codex_home: Path,
    opencode_home: Path,
) -> None:
    homes = {"codex": codex_home, "opencode": opencode_home}
    for category, (home_name, relative_dir) in ASSET_TARGETS.items():
        previous = asset_map(previous_layers, category)
        current = asset_map(layers, category)
        target_dir = homes[home_name] / relative_dir
        for removed_name in previous.keys() - current.keys():
            removed = target_dir / removed_name
            if removed.is_symlink():
                removed.unlink()
        for name, source in current.items():
            replace_managed_link(target_dir / name, source)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--opencode-config", required=True)
    parser.add_argument("--codex-config", required=True)
    parser.add_argument("--opencode-commands")
    parser.add_argument("--opencode-skills")
    parser.add_argument("--codex-agents")
    parser.add_argument("--codex-skills")
    parser.add_argument("--codex-home", type=Path, required=True)
    parser.add_argument("--opencode-home", type=Path, required=True)
    parser.add_argument("--state-home", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    layer: Dict[str, Any] = {
        "id": args.id,
        "root": str(root),
        "opencode_config": str((root / args.opencode_config).resolve()),
        "codex_config": str((root / args.codex_config).resolve()),
    }
    for category in ASSET_TARGETS:
        relative = getattr(args, category)
        if relative:
            layer[category] = str((root / relative).resolve())

    for config_key in ("opencode_config", "codex_config"):
        if not Path(layer[config_key]).is_file():
            raise FileNotFoundError(layer[config_key])

    registry_path = args.state_home / "layers.json"
    previous_layers = load_registry(registry_path)
    layers = list(previous_layers)
    for index, existing in enumerate(layers):
        if existing["id"] == args.id:
            layers[index] = layer
            break
    else:
        layers.append(layer)

    opencode_config: Config = {}
    codex_config: Config = {}
    for registered in layers:
        opencode_config = deep_merge(
            opencode_config, load_config("json", Path(registered["opencode_config"]))
        )
        codex_config = deep_merge(
            codex_config, load_config("toml", Path(registered["codex_config"]))
        )

    atomic_text(args.opencode_home / "opencode.jsonc", json.dumps(opencode_config, indent=2) + "\n")
    atomic_text(args.codex_home / "config.toml", render_toml(codex_config))
    reconcile_assets(previous_layers, layers, args.codex_home, args.opencode_home)
    atomic_text(registry_path, json.dumps({"layers": layers}, indent=2) + "\n")
    print("Applied layers in order: " + " -> ".join(item["id"] for item in layers))


if __name__ == "__main__":
    main()
