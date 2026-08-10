#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
codex_dir=${CODEX_HOME:-"$HOME/.codex"}
opencode_dir=${OPENCODE_CONFIG_DIR:-"$HOME/.config/opencode"}
state_dir=${AGENT_CONFIG_STATE_HOME:-"$HOME/.local/share/agent-config"}

command -v python3 >/dev/null 2>&1 || {
  printf '%s\n' "Python 3 is required to rebuild configuration layers." >&2
  exit 1
}

python3 "$repo_dir/scripts/apply_layer.py" \
  --id generic \
  --root "$repo_dir" \
  --opencode-config opencode.base.jsonc \
  --codex-config codex/config.toml \
  --opencode-commands commands \
  --opencode-skills skills \
  --codex-agents codex/agents \
  --codex-skills codex/skills \
  --codex-home "$codex_dir" \
  --opencode-home "$opencode_dir" \
  --state-home "$state_dir"
