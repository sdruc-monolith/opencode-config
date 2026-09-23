# Agent configuration

Public, generic configuration shared by Codex and OpenCode.

Clone this source repository as `~/repos/opencode-config`. Runtime files are
installed separately under `~/.config/opencode` and `~/.codex`.

- `opencode.base.jsonc` is the generic OpenCode source configuration.
- `codex/` contains the generic Codex config, agents, and skills.
- Work-specific MCPs, project trust settings, and skills live in a separate
  private overlay.

Run `install.sh` from any directory to deep-merge this independent generic
layer into the standard OpenCode and Codex configuration paths. The installer
registers the layer, then rebuilds managed configuration from an empty base so
removed settings and assets disappear exactly. Other repositories can apply
their own layers afterward; later registered layers win on conflicting values
while non-conflicting nested dictionary entries remain.

Configuration files are generated, while commands, agents, and skills are
copied into their runtime directories. The installer does not create symlinks.

## Engineering skills

Use **plan → implement → verify** for substantial changes. Each skill is also
useful independently; small tasks use a proportionate checklist and checks.

| Skill | When to use it | Result |
| --- | --- | --- |
| [plan](skills/plan/SKILL.md) | Scope a feature, migration, or complex refactor | Repository-grounded decisions, acceptance criteria, and verifiable slices |
| [implement](skills/implement/SKILL.md) | Build an agreed change or resume a plan | Incremental implementation, progress, and verification evidence |
| [verify](skills/verify/SKILL.md) | Audit completed work | Findings and PASS / FAIL / UNVERIFIED results against requirements |
| [python-engineering](skills/python-engineering/SKILL.md) | Plan, build, or review Python systems and data pipelines | Python architecture, data contracts, testing, and performance guidance |
| [ui-app-testing](skills/ui-app-testing/SKILL.md) | Change or diagnose UI behavior and layout | Local runtime, browser, and visual validation |

All five are available in OpenCode and Codex after installation. In OpenCode,
ask, for example, “Use the plan skill to scope this pipeline change.” In Codex,
use `$plan`, `$implement`, `$verify`, or `$python-engineering` in your prompt.
The runtime's current agent mode and permissions still apply.

Planning-only requests produce a plan. A request to plan and implement can
continue into implementation when permissions allow it. Verification audits
and reports; the implementation workflow handles fixes. Testing is pragmatic:
prefer regression repros and test-first behavioral slices where valuable, and
use the repository's own quality gates.

Organization and reuse are language-independent expectations in all three
workflow skills: group source into cohesive domain/capability modules, keep
dependencies directional, and consolidate repeated behavior into shared
implementations used by the relevant callers. The smallest coherent change can
include extraction and reorganization; it is not measured by files changed.
`python-engineering` adds Python package, import, public-export, and packaging
conventions, including an illustrative subpackage layout.

Python references are loaded for the relevant task:

- [Data pipelines](skills/python-engineering/references/data-pipelines.md): schemas,
  row grain, join cardinality, incremental processing, and replay-safe publication.
- [Testing](skills/python-engineering/references/testing.md): behavioral assertions,
  pytest techniques, real output checks, and property/differential testing.
- [Performance](skills/python-engineering/references/performance.md): representative
  measurements, execution plans, memory, and engine migrations.

### Plan directories

New saved plans use `<NNN><optional-letter>_<name>/` in the project's established
plan location, defaulting to `artifacts/plans/`. For example:

```text
013b_state-driven-selection/
    README.md
    design.md
    history.md
    01_contracts-and-controls.md
    02_bounded-selector.md
    03_scheduled-migration.md
    04_integration-verification.md
```

- `README.md` contains the TL;DR, global constraints, current state, canonical
  checklist/index, dependencies, next task, and whole-plan acceptance.
- Each task file describes one coherent, independently verifiable outcome:
  required context, settled design/contracts, implementation steps, verification,
  evidence, and blockers. Keep implementation and its tests together.
- `design.md` is optional, for detailed contracts shared by multiple tasks.
  Small plans can contain just `README.md`; historical single-file plans remain
  usable without conversion.
- `history.md` is created at the first consequential mistake, pitfall, or plan
  revision. Stable headings such as `H001` give links like `history.md#h001`.
  Add descriptive, comma-separated history links beside each affected checklist
  item. Correct current task/design instructions first; history records what
  changed, why, evidence, and the lesson for the next implementer.
- Implementers read the overview, selected task, and explicitly required
  references, including that task's checklist-linked history entries. The
  overview owns progress; completion requires evidence, and
  whole-plan verification includes the integrated result.

Use the [overview template](skills/plan/references/plan-template.md),
[task template](skills/plan/references/task-template.md),
[linked history template](skills/plan/references/history-template.md), and
[implementation handoff](skills/implement/references/handoff-template.md).

### Maintaining and validating skills

Keep shared skill bodies and references identical under `skills/` and
`codex/skills/`. Codex-specific interface metadata lives in each skill's
`agents/openai.yaml`.

```sh
python3 scripts/check_skills.py
```

This dependency-free check validates the repository's single-line metadata
conventions, inline local file links, and cross-runtime content parity. Runtime
loading and model behavior are separate checks; see the
[skill validation scenarios](docs/skill-validation.md).

After adding skills, run `./install.sh` to rebuild installed assets. Quit and
restart OpenCode, and start a new Codex session, to load the updated skills.
