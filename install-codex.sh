#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
codex_dir=${CODEX_HOME:-"$HOME/.codex"}

mkdir -p "$codex_dir/agents" "$codex_dir/skills"
ln -sfn "$repo_dir/codex/config.toml" "$codex_dir/config.toml"

for source in "$repo_dir"/codex/agents/*; do
  ln -sfn "$source" "$codex_dir/agents/$(basename "$source")"
done

for source in "$repo_dir"/codex/skills/*; do
  cp -R "$source" "$codex_dir/skills/"
done

printf '%s\n' "Installed generic Codex configuration from $repo_dir."
