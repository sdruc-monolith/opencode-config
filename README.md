# Agent configuration

Public, generic configuration shared by Codex and OpenCode.

- `opencode.base.jsonc` is the generic OpenCode source configuration.
- `codex/` contains the generic Codex config, agents, and skills.
- Work-specific MCPs, project trust settings, and skills live in a separate
  private overlay.

Run `install-codex.sh` from any directory to install a generic-only Codex
configuration. On work machines, run the private repository's `install.sh`
instead. It merges this repository with the private overlay into the standard
OpenCode and Codex config paths, so the normal `opencode` and `codex` commands
are the single entry point.
