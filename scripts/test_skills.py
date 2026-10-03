"""Regression checks for canonical skills and migration of installed assets."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from check_skills import check_skills


ROOT = Path(__file__).resolve().parents[1]


def file_contents(directory: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(directory): path.read_bytes()
        for path in directory.rglob("*") if path.is_file()
    }


class SkillValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="canonical-skills-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "skills" / "example"
        (self.skill / "agents").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: example\ndescription: Use for a fixture.\n---\n"
            "[Reference](reference.md)\n", encoding="utf-8"
        )
        (self.skill / "reference.md").write_text("Reference\n", encoding="utf-8")
        (self.skill / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "Example"\n'
            '  short_description: "Example fixture"\n'
            '  default_prompt: "Use $example."\n', encoding="utf-8"
        )

    def test_single_source_is_valid(self) -> None:
        self.assertEqual(check_skills(self.root), [])

    def test_duplicate_tree_is_rejected(self) -> None:
        shutil.copytree(self.skill, self.root / "codex" / "skills" / "example")
        self.assertTrue(any("separate skill sources" in error for error in check_skills(self.root)))

    def test_missing_metadata_is_rejected(self) -> None:
        (self.skill / "agents" / "openai.yaml").unlink()
        self.assertTrue(any("missing Codex interface" in error for error in check_skills(self.root)))

    def test_broken_reference_is_rejected(self) -> None:
        (self.skill / "reference.md").unlink()
        self.assertTrue(any("broken local link" in error for error in check_skills(self.root)))

    def test_missing_source_is_rejected(self) -> None:
        shutil.rmtree(self.root / "skills")
        self.assertTrue(any("missing skills directory" in error for error in check_skills(self.root)))


class SkillInstallationTests(unittest.TestCase):
    def test_migration_reinstall_and_overlay_precedence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-install-") as temporary:
            base = Path(temporary).resolve()
            source = base / "source"
            source.mkdir()
            for directory in ("skills", "commands", "codex/agents"):
                shutil.copytree(ROOT / directory, source / directory)
            for relative in (
                "install.sh", "opencode.base.jsonc", "codex/config.toml",
                "scripts/apply_layer.py", "scripts/merge_config.py",
            ):
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)

            homes = {runtime: base / runtime for runtime in ("opencode", "codex")}
            state = base / "state"
            state.mkdir()
            environment = {
                **os.environ,
                "CODEX_HOME": str(homes["codex"]),
                "OPENCODE_CONFIG_DIR": str(homes["opencode"]),
                "AGENT_CONFIG_STATE_HOME": str(state),
                "PYTHONDONTWRITEBYTECODE": "1",
            }

            # Simulate an existing split-source registration whose Codex source
            # disappeared in this migration, plus obsolete installed references.
            for home in homes.values():
                installed = home / "skills" / "plan"
                installed.mkdir(parents=True)
                (installed / "obsolete.md").write_text("old content", encoding="utf-8")
            generic = {
                "id": "generic", "root": str(source),
                "opencode_config": str(source / "opencode.base.jsonc"),
                "codex_config": str(source / "codex/config.toml"),
                "opencode_skills": str(source / "skills"),
                "codex_skills": str(source / "codex/skills"),
            }
            overlay = base / "overlay"
            override = overlay / "skills" / "ui-app-testing"
            override.mkdir(parents=True)
            (override / "SKILL.md").write_text("Overlay-owned skill\n", encoding="utf-8")
            (overlay / "opencode.jsonc").write_text("{}\n", encoding="utf-8")
            (overlay / "codex.toml").write_text("", encoding="utf-8")
            work = {
                "id": "work", "root": str(overlay),
                "opencode_config": str(overlay / "opencode.jsonc"),
                "codex_config": str(overlay / "codex.toml"),
                "opencode_skills": str(overlay / "skills"),
                "codex_skills": str(overlay / "skills"),
            }
            registry_path = state / "layers.json"
            registry_path.write_text(json.dumps({"layers": [generic, work]}), encoding="utf-8")

            for iteration in range(2):
                if iteration:
                    # One source edit must reach both runtimes on reinstall.
                    plan = source / "skills" / "plan" / "SKILL.md"
                    plan.write_text(plan.read_text(encoding="utf-8") + "\nUpdated once.\n", encoding="utf-8")
                result = subprocess.run(
                    ["sh", str(source / "install.sh")], cwd=base, env=environment,
                    capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                layers = json.loads(registry_path.read_text(encoding="utf-8"))["layers"]
                self.assertEqual([layer["id"] for layer in layers], ["generic", "work"])
                for key in ("opencode_skills", "codex_skills"):
                    self.assertEqual(layers[0][key], str(source / "skills"))
                expected_names = {skill.name for skill in (source / "skills").iterdir()}
                for home in homes.values():
                    self.assertEqual({path.name for path in (home / "skills").iterdir()}, expected_names)
                    for skill in (source / "skills").iterdir():
                        installed = home / "skills" / skill.name
                        expected = override if skill.name == override.name else skill
                        self.assertFalse(installed.is_symlink())
                        self.assertEqual(file_contents(installed), file_contents(expected))
                    self.assertFalse((home / "skills/plan/obsolete.md").exists())


if __name__ == "__main__":
    unittest.main()
