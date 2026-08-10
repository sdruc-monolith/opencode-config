#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
codex_dir=${CODEX_HOME:-"$HOME/.codex"}
opencode_dir=${OPENCODE_CONFIG_DIR:-"$HOME/.config/opencode"}
merge_script="$repo_dir/scripts/merge-config.py"

command -v python3 >/dev/null 2>&1 || {
  printf '%s\n' "Python 3 is required to merge configuration layers." >&2
  exit 1
}

mkdir -p "$codex_dir/agents" "$codex_dir/skills" "$opencode_dir/commands" "$opencode_dir/skills"

python3 "$merge_script" json \
  "$opencode_dir/opencode.jsonc" \
  "$repo_dir/opencode.base.jsonc" \
  "$opencode_dir/opencode.jsonc"
python3 "$merge_script" toml \
  "$codex_dir/config.toml" \
  "$repo_dir/codex/config.toml" \
  "$codex_dir/config.toml"

for source in "$repo_dir"/commands/*; do
  ln -sfn "$source" "$opencode_dir/commands/$(basename "$source")"
done

for source in "$repo_dir"/skills/*; do
  ln -sfn "$source" "$opencode_dir/skills/$(basename "$source")"
done

for source in "$repo_dir"/codex/agents/*; do
  ln -sfn "$source" "$codex_dir/agents/$(basename "$source")"
done

for source in "$repo_dir"/codex/skills/*; do
  ln -sfn "$source" "$codex_dir/skills/$(basename "$source")"
done

printf '%s\n' "Applied the public generic layer to the standard codex and opencode configuration."
