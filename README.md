# Agent configuration

Public, generic configuration shared by Codex and OpenCode.

Clone this source repository as `~/repos/opencode-config`. Runtime files are
installed separately under `~/.config/opencode` and `~/.codex`.

- `opencode.base.jsonc` is the generic OpenCode source configuration.
- `codex/` contains the generic Codex config, agents, and skills.
- Work-specific MCPs, project trust settings, and skills live in a separate
  private overlay.

Run `install.sh` from any directory to deep-merge this independent generic
layer into the standard OpenCode and Codex configuration paths. Other
repositories can apply their own layers afterward; later layers win on
conflicting values while non-conflicting nested dictionary entries remain.
