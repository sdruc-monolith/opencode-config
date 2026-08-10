#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
codex_dir=${CODEX_HOME:-"$HOME/.codex"}

mkdir -p "$codex_dir/agents" "$codex_dir/skills"
config_tmp=$(mktemp "$codex_dir/config.toml.XXXXXX")
trap 'rm -f "$config_tmp"' EXIT HUP INT TERM
cp "$repo_dir/codex/config.toml" "$config_tmp"
mv -f "$config_tmp" "$codex_dir/config.toml"
trap - EXIT HUP INT TERM

for source in "$repo_dir"/codex/agents/*; do
  ln -sfn "$source" "$codex_dir/agents/$(basename "$source")"
done

for source in "$repo_dir"/codex/skills/*; do
  cp -R "$source" "$codex_dir/skills/"
done

printf '%s\n' "Installed generic Codex configuration from $repo_dir."
