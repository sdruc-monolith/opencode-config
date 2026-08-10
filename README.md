# Agent configuration

Public, generic configuration shared by Codex and OpenCode.

- The repository root is the standard OpenCode config directory.
- `codex/` contains the generic Codex config, agents, and skills.
- Work-specific MCPs, project trust settings, and skills live in a separate
  private overlay.

Run `./install-codex.sh` after cloning to link the generic Codex files into
`~/.codex`. Work sessions use the separately installed `codex-cw` and
`opencode-cw` commands.
