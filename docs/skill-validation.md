# Skill Validation

## Structural and Installation Checks

Run `python3 scripts/check_skills.py` from any directory using its absolute path,
or from the repository root as shown. It checks:

- `SKILL.md` entry points, required single-line name/description fields, and names
  matching their directories.
- Codex interface metadata and default prompts naming the corresponding skill.
- Inline local Markdown file links, including references loaded conditionally.
- Byte-for-byte parity for shared content, excluding runtime-specific `agents/`
  metadata. Codex-only skills are permitted.

This is a repository-convention check, not a complete YAML/schema validator or
a behavioral evaluation. Anchor targets and external URLs are not validated.

For an installation smoke test, create a disposable temporary directory and set
all three variables before running `./install.sh`:

- `CODEX_HOME=<temporary>/codex`
- `OPENCODE_CONFIG_DIR=<temporary>/opencode`
- `AGENT_CONFIG_STATE_HOME=<temporary>/state`

Check that each installed skill resolves to the intended source directory,
references and Codex metadata remain readable, and a repeated installation
produces the same asset targets. Keep the state-home override: it prevents a
smoke test from changing the real layer registry.

Check discovery through each runtime's available skill-listing interface in an
isolated configuration. In OpenCode, `opencode debug skill` lists available
skills; isolate other global/project skill sources when attributing results to
this layer. A successful listing verifies discovery, not task execution.

## Behavioral Scenarios

Run these as separate fresh sessions against disposable fixture repositories,
using each runtime's normal skill loading. Record runtime/model/version, prompt,
loaded skills/references, edits, commands and results, and the final response.
Use tool traces and observable results as evidence, not phrase matching against
the skill text. Repeat a scenario when changing its relevant workflow branch.

### 1. Small Python Change

**Setup:** A small CLI with an established test command and a help-text typo.

**Prompt:** “Correct this help text.”

**Expected:** A focused edit and proportionate existing checks. No elaborate
planning artifact, new test framework, mandatory coverage target, or unnecessary
dependency. A short task need not load every workflow skill.
If the CLI is a single cohesive script, the agent keeps it simple rather than
creating empty packages or introducing a framework for the text edit.

### 2. Pipeline Planning

**Setup:** A Python project with event input, customer dimension, output writer,
and documented test commands. Dimension uniqueness and unmatched-customer policy
are not yet specified.

**Prompt:** “Use plan to scope customer enrichment and daily Parquet output.”

**Expected:** Reads actual paths and tests; defines grain, schemas, join
cardinality, null/timezone rules, and output contract; identifies the consequential
policy questions. Proposes a small end-to-end first slice with concrete checks.
Returns a plan without implementation or unsolicited issue publication.

### 3. Duplicate-Key Regression

**Setup:** An enrichment join doubles amounts when a dimension key repeats.
The documented contract requires unique dimension keys and rejecting duplicates.

**Prompt:** “Use implement to fix inflated totals from duplicate dimension keys.”

**Expected:** Reproduces the symptom, adds a behavioral regression check that
fails before the fix, enforces the input contract, and verifies valid inputs.
Does not mask the bug with arbitrary final deduplication or set-only assertions.

### 4. Engine Migration

**Setup:** A pandas pipeline, a proposed DuckDB replacement, and fixtures with
null keys, duplicate rows, offset timestamps, and decimal amounts. Include a
representative benchmark input with relevant size and skew.

**Prompt:** “Plan and implement the DuckDB migration while preserving output.”

**Expected:** Preserves the user's implementation authorization, records semantic
decisions, verifies schema/value equivalence with independent expected cases,
and measures the relevant pipeline including materialization and output costs.
Does not infer scale benefits solely from small correctness fixtures.

### 5. Blocked Integration Check

**Setup:** Unit checks pass, but the integration environment needs unavailable
credentials. A required acceptance criterion depends on that environment.

**Prompt:** “Use verify to check whether this change is complete.”

**Expected:** Runs feasible checks, reports the required integration outcome as
UNVERIFIED with the concrete blocker, and avoids claiming complete verification.
Reports rather than repairing source or substituting a weaker test for the
required evidence.

### 6. Stale Plan and User Work

**Setup:** A plan references a renamed module and marks a slice complete. The
current code only partially implements that slice; unrelated user edits exist.

**Prompt:** “Use implement to resume this plan.”

**Expected:** Inspects current code and version-control state, corrects stale
paths, reclassifies unsupported completion claims, preserves user work, and
starts the next genuinely unblocked slice. Escalates material design changes
rather than treating a stale plan as authority.

### 7. Read-Only Planning

**Setup:** A read-only agent/session and a substantial requested change.

**Prompt:** “Use plan to design this change and save the plan.”

**Expected:** Respects runtime permissions, returns the plan in the conversation
if writing is unavailable, and explains that saving was not performed. It does
not bypass mode restrictions or begin implementation.

### 8. Pipeline Rerun and Publication

**Setup:** A batch writer with a documented replay-safe sink and a checkpoint
updated separately. Inject failures before publication and after publication but
before checkpoint advancement.

**Prompt:** “Use implement to make this pipeline recover correctly on rerun.”

**Expected:** Defines batch identity and the sink's publication guarantees;
verifies repeated/overlapping inputs and the actual failure windows; readers see
the intended complete dataset without duplicated results. Does not assume a
multi-file or object-store write is atomic.

### 9. Growing a Flat Application

**Setup:** A Python application with unrelated modules directly under `src/`,
existing import/CLI consumers, and a feature adding a distinct domain capability.
Repeat with an equivalent flat TypeScript or Go application.

**Prompt:** “Use plan to scope this feature, then implement it.”

**Expected:** Inspects current responsibilities and reuse opportunities, proposes
cohesive domain/capability modules using the language's conventions, and evolves
the affected structure. Records responsibilities and dependency direction;
keeps entry points thin and verifies existing consumers. Does not merely add
another unrelated source file or create a prescribed directory tree with no
meaningful boundaries. Non-Python work does not require the Python skill.

### 10. Consolidating Shared Behavior

**Setup:** Two pipelines implement the same validation contract with differently
written code. A third consumer needs that contract with an explicit configurable
limit. Use Python and a non-Python version of the fixture.

**Prompt:** “Use implement to add this consumer and reuse the existing validation.”

**Expected:** Finds both existing implementations, extracts/generalizes the common
behavior into a descriptively named owning module, represents the limit
explicitly, and migrates the relevant callers. Removes superseded logic and
tests each caller's contract. A helper used only by the new consumer while old
callers retain independent copies is incomplete consolidation.

### 11. Similar Code With Different Policies

**Setup:** Two domains use similar-looking calculations but have distinct,
documented rounding and eligibility rules. Both use the same serialization
format, implemented twice.

**Prompt:** “Use implement to reduce duplication in these workflows.”

**Expected:** Consolidates genuinely shared serialization while preserving the
distinct policies, using focused functions or collaborators where useful.
Does not force the domains through a universal mode-flag helper just to reduce
line count. Verification checks both domain contracts and shared output.

### 12. Package Moves and Incomplete Extraction Audit

**Setup:** A Python change introduces subpackages but leaves package discovery,
a CLI import, and a package-data path stale. The extracted shared validator is
used by one caller while another still duplicates its rule. A non-Python variant
has an equivalent stale export/build path and incomplete caller migration.

**Prompt:** “Use verify to audit this reorganization and shared-code extraction.”

**Expected:** Reports the remaining duplicated behavior and broken package/export
or entry-point boundaries with file/caller evidence. Uses installed-package or
normal build/runtime checks as appropriate, rather than workarounds that hide
the defects. Directory nesting alone is not accepted as proof of modularity;
the audit reports findings without editing source.

### 13. Numbered Plan Directory and Small-Plan Fallback

**Setup:** A plan root containing legacy `013_existing-plan.md`, subplan
`013a_first-followup.md`, and directory `014_another-plan/`. Preserve their
contents while exercising new-plan creation.

**Prompt:** “Use plan to scope and save a plan for this multi-step feature.”

**Expected:** Inspects both files and directories, chooses an unused three-digit
ID, and creates a directory with `README.md` and coherent outcome-oriented task
files. The overview provides a linked checklist, explicit dependencies,
constraints, next task, and integrated acceptance. Required context and concrete
verification are sufficient for an unfamiliar implementer. No task-per-method
fragmentation or automatic migration of legacy plans occurs.

Repeat with a requested subplan of 013: use an available suffix and link the
parent with explicit scope/supersession semantics. Repeat with a small saved
plan: use a directory containing only `README.md` with inline work and checks.
A user-requested ID collision must not overwrite existing work.

### 14. Selective Context and Canonical Progress

**Setup:** A plan directory with a verified prerequisite, a ready implementation
task, an independent later-numbered task, and a dependent integration task.
Tasks name exact required sections of a shared design document. A large
historical report contains superseded instructions and is not required.

**Prompt:** “Use implement to complete the ready task in this plan.”

**Expected:** Reads the overview, selected task, required design sections, and
relevant code. Uses dependency edges rather than assuming all earlier-numbered
tasks are prerequisites. Implements and verifies the requested outcome, records
evidence, then updates the overview's checklist and next action within the
authorized scope. Does not load every document by default, follow historical
instructions, or maintain competing status checklists in task/handoff files.

### 15. Task Readiness and Blocked Verification

**Setup:** One task depends on an unresolved schema policy; another has completed
code but an unavailable required integration environment. A third independent
task is genuinely ready.

**Prompt:** “Use implement to continue this plan.”

**Expected:** Keeps the unresolved implementation blocked rather than inventing
the policy. Keeps implemented-but-unverified work unchecked with its exact gap.
Continues independent ready work within scope. A fresh-session handoff identifies
the overview, task, required context, and next unfinished action without relying
on prior conversation or duplicating the canonical progress list.

### 16. Whole-Plan Audit and Invalidated Evidence

**Setup:** Component tasks are checked off, but the integrated workflow fails.
One checked entry cites evidence predating a contract change. Another task is
missing from the index, and two dependency edges form a cycle.

**Prompt:** “Use verify to audit completion of this plan directory.”

**Expected:** Checks every required outcome and integrated acceptance; identifies
stale evidence, unindexed work, and the dependency cycle. Reports failures or
unverified outcomes instead of declaring success from checkboxes. A task-only
audit limits its claim to that task. The verifier reports findings; the
implementer reopens affected checklist entries and updates the owning contracts
before continuing authorized remediation.

### 17. Task-Linked Mistakes and Revisions

**Setup:** A plan directory has no history file. During T02, the agent discovers
that a planned deduplication step hides incorrect join results. The correction
also affects T03, whose prior verification is now stale. A routine typo occurs
in a separate command but has no lasting implication.

**Prompt:** “Use implement to correct the join behavior and update this plan.”

**Expected:** Corrects the owning task/design instructions, creates `history.md`
with a stable `## H001` entry for the consequential issue, and records the
observation, confirmed cause or labeled hypothesis, resolution, plan revision,
evidence, and actionable pitfall. Links that same entry beside T02 and T03 in
the README checklist and reopens invalidated completion. Later events receive
new IDs and descriptive comma-separated links beside affected tasks. The typo
does not create a noise entry or a second progress checklist.

### 18. Stable History Links and Fresh-Session Recovery

**Setup:** T02's checklist item links H001 and H003. H003 corrects H001's original
hypothesis, with cross-links preserving the evidence trail. Unrelated history
entries are long. In a separate audit variant, one link points to a missing
heading, two entries reuse an ID, and a revision exists only in history while
the task instructions still prescribe the rejected approach.

**Prompt:** “Use implement to resume T02.” Then, in the audit variant: “Use verify
to review this plan's revision record.”

**Expected:** The implementer reads the overview, task, linked entries and relevant
corrections, then follows the corrected current contract without repeating the
failed approach or reading all unrelated history. Existing anchors keep working
as entries are appended; no literal line-number links or renumbering is used.
The verifier reports broken/duplicate anchors and stale current instructions
without editing the plan. An unresolved contradiction blocks affected work
rather than letting the agent silently choose a version.

## Recording Results

For each run, report PASS, FAIL, or UNVERIFIED with evidence and remaining gaps.
Keep structural checks, runtime discovery, and behavioral runs separate in the
report. Documentation review or successful skill discovery does not count as a
completed behavioral scenario.
