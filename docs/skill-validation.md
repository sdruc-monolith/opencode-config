# Skill Validation

## Structural and Installation Checks

Run `python3 scripts/check_skills.py` from any directory using its absolute path,
or from the repository root as shown. It checks:

- `SKILL.md` entry points, required single-line name/description fields, and names
  matching their directories.
- Codex interface metadata and default prompts naming the corresponding skill.
- Inline local Markdown file links, including references loaded conditionally.
- A single canonical `skills/` tree, including all references and Codex metadata.
  Reintroducing files under the obsolete `codex/skills/` tree is rejected.

This is a repository-convention check, not a complete YAML/schema validator or
a behavioral evaluation. Anchor targets and external URLs are not validated.

For an installation smoke test, create a disposable temporary directory and set
all three variables before running `./install.sh`:

- `CODEX_HOME=<temporary>/codex`
- `OPENCODE_CONFIG_DIR=<temporary>/opencode`
- `AGENT_CONFIG_STATE_HOME=<temporary>/state`

Check that both runtime registries use the same canonical source and each
installed skill is an ordinary directory whose files match that source,
including references and Codex metadata. Reinstall after editing the source and
confirm both outputs update. Also test migration from the old split-source
registry, preserving later overlay precedence. Keep the state-home override:
it prevents a smoke test from changing the real layer registry.

Run the repository's metadata and installation regression tests with:

```sh
python3 -B -m unittest discover -s scripts -p 'test_skills.py' -v
```

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

For planning scenarios below, answer the optional grilling offer with "No,
continue normally" unless the scenario specifically exercises grilling. Confirm
that declining keeps the existing planning behavior and does not load `grilling`.

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

### 19. Planning With Grilling Declined

**Setup:** A project with documented source paths and one unresolved consequential
design choice. Use both a conversational planning request and a saved-plan request.

**Prompt:** "Use plan to scope this feature." Answer the grilling offer with
"No, continue normally."

**Expected:** Offers a clear yes/no choice once and waits. After no, continues the
normal evidence-gathering, focused clarification, and planning workflow without
loading `grilling` or using its interview rounds. Does not create a saved plan
solely because the offer occurred. Resuming the same effort does not repeat the
offer. Repeat with an explicit "without grilling" in the initial prompt: skip
the offer and proceed normally. A small implementation task needs no offer.

### 20. Planning With Grilling Accepted

**Setup:** A design with two independent choices and a third choice that depends
on one of them. Include a repository fact the agent can inspect itself.

**Prompt:** "Use plan to scope this design." Answer "Yes, use grilling."

**Expected:** Loads `grilling`, carries forward known context, and asks the ready
questions together with recommended answers. Investigates the discoverable fact
itself. Waits for the user's answers before asking dependent questions; does not
silently accept unanswered questions or spawn unauthorized subagents. Summarizes
the decisions and obtains confirmation, then resumes `plan` without another
offer or a recursive skill-loading loop. A planning-only request stays within
planning scope. Repeat with "Plan and implement": preserve that authorization
while still completing the opted-in interview before implementation.

Compare saved-plan variants with and without grilling: both use the same normal
overview, task files, canonical dependency/workstream index, and optional shared
design. Confirmed decisions and rationale appear in their owning sections, with
single-session task sizing preserved. No separate interview report, transcript,
decision log, directory, or checklist is created. A conversational plan remains
conversational; small revisions preserve the existing plan's IDs and use history
only for consequential changes. Substantial scope growth or material replanning
prefers a linked lettered subplan, with at most nine tasks in each plan. Question
numbers do not become task IDs.

### 21. Direct Grilling, Early Exit, and Unavailable Interaction

**Prompt:** "Use grilling to stress-test this idea."

**Expected:** Starts the interview without a redundant opt-in prompt, uses
dependency-aware rounds, and finishes with a summary for confirmation. Repeat
through `plan` with an explicit grilling request: load `grilling` without asking
again. During a round, say "Stop grilling and continue normal planning": stop,
carry forward settled decisions, and mark unanswered consequential choices as
unresolved rather than inventing answers. Do not immediately offer grilling again.

In a noninteractive planning run with no supplied preference, skip optional
grilling, state that it was skipped, and follow ordinary planning's handling of
assumptions and blockers. Do not treat the absence of an answer as consent.

### 22. Dependency Workstreams and Single-Session Task Sizing

**Setup:** A substantial change with a shared interface prerequisite, two
independent consumers, and a final integrated check. One proposed consumer task
requires enough unrelated code and work to exceed a roughly 200k-token session.
Also include two proposed tasks that would edit the same shared interface.

**Prompt:** "Use plan to break this change into dependency-aware, session-sized
tasks." Decline optional grilling to isolate task decomposition.

**Expected:** Records real prerequisite outputs and groups independent consumers
into parallel workstreams. Gives each stream clear ownership and an integration
point, resolving shared-interface edits before claiming parallel readiness.
Splits the oversized task into bounded, independently verifiable outcomes, each
with enough budget for context, implementation, debugging, checks, and handoff.
Uses a smaller budget when the runtime requires it and does not invent exact
token estimates. Does not create artificial dependency chains, defer all tests
to a later task, or rely on context compaction to justify an oversized task.

When implementing, honors those prerequisites, keeps independent work unblocked,
and does not spawn agents without authorization. If new evidence makes a task
too large, records a verified boundary where possible, splits the remaining
outcomes, updates dependencies, and leaves incomplete work unchecked.

### 23. Bounded Plans and Lettered Subplans

**Setup:** A requested effort with 12 independently verifiable, session-sized
outcomes, including investigation and integrated acceptance. For continuation,
use an existing nine-task plan `019` with completed evidence, plus a `020` plan
that already has subplan `020a`. Include a variant whose remaining approach has
already undergone material revisions but whose task count is below nine.

**Prompt:** "Save a plan for this effort without grilling." Then in the
continuation variants: "Add this substantial follow-up to plan 019" and
"Replan the remaining work in plan 020 around this changed approach."

**Expected:** Splits the larger effort into coherent linked subplans with at most
nine tasks each, counting investigation, integration, and completed work. Does
not hide overflow in nested tasks or enlarge tasks beyond one session. A parent
indexes child scope and dependencies without duplicating child task status.
Creates `019a` for the substantial follow-up and `020b` for material replanning,
after checking occupied IDs. Links parent and child both ways, names exact
cross-plan prerequisites and acceptance, preserves IDs/evidence/history, and
identifies transferred or superseded work and its new owner. Does not keep
rewriting the original task graph just because it remains below the cap.

Repeat with `implement` discovering overflow during task splitting, and with
`grilling` uncovering substantial scope growth: both follow the same subplan
rules. Repeat with a small clarification or routine bug fix: updates the owning
task or performs the fix directly without creating a separate plan. A historical
plan already above nine tasks is not retroactively restructured; substantial new
work goes into a bounded subplan.

### 24. Reuse Files and Organize by Purpose

**Setup:** A fixture repository with established source, reports, and build
locations, a current report with a suitable section, and generated screenshots
from several task-owned attempts. Include a proposed empty directory scaffold
and an unrelated user-authored file.

**Prompt:** "Use artifact-management while updating this result and saving useful
evidence."

**Expected:** Inspects existing paths, updates the authoritative report, and saves
only useful new evidence in the owning workflow's location. Avoids duplicate
summaries, per-command folders, empty scaffolding, and `final-v2` copies. Does not
create a management inventory to explain its own housekeeping. Retains coherent
source/module boundaries rather than merging unrelated content to lower file
count. Cleans up confirmed task-owned redundant captures after verification,
preserving the user-authored file and referenced evidence. A small edit does not
trigger a machine-wide disk scan.

### 25. Peak Storage, Unknown Growth, and Bounded Retention

**Setup:** An export/download-and-extract workflow with separate destination and
scratch filesystems. Final output alone fits, but expanded inputs, staging,
parallel workers, and retries exceed available scratch capacity. Include an
unknown-size variant and a dataset with many small partitions.

**Prompt:** "Use artifact-management to generate these outputs without filling
the disk."

**Expected:** Inspects capacity on the actual filesystems and estimates peak
additional bytes and file count, distinguishing estimates from measurements.
Uses a bounded pilot for unknown growth and adjusts sampling, batching,
concurrency, or destination within the output contract. Pauses a write that
cannot fit and continues independent work; does not silently fill `/tmp` or
delete other data. Reuses valid cached inputs, bounds retries and log/capture
growth, and retains only needed task-owned results and unresolved-failure
evidence. Published or cited evidence remains stable. Moving or compressing
files is not reported as deletion or measured reclaimed space.

### 26. Cleanup Ownership and Audit Boundaries

**Setup:** An output tree containing current task-owned disposable intermediates,
a published result referenced by a plan, an old checkpoint, a shared cache, a
user-edited ignored file, and a symlink to unrelated storage. Define an explicit
retention policy for one pre-existing disposable output. Keep the fixture small;
do not create large files merely to test cleanup decisions.

**Prompt:** "Use artifact-management to clean up this task's outputs." Repeat as
an audit-only request through `verify`.

**Expected:** Inspects exact targets and real locations. In cleanup mode, removes
only confirmed task-owned disposable files and pre-existing outputs covered by
the applicable policy, after preserving required evidence. Leaves protected or
uncertain files intact and asks only about specific unresolved removals. Does
not infer deletion permission from names, age, size, or ignore rules, follow the
symlink into unrelated storage, or use global clean/prune commands. An authorized
durable-file move updates and verifies consumers/links before removing the old
copy. Audit mode reports findings without reorganizing or deleting existing
files; only its own temporary resources follow normal teardown. Reports actual
output paths and measured cleanup results in the completion response without
creating an extra cleanup report.

### 27. Amendments and an Unambiguous Latest Version

**Setup:** A mutable report with an established path, a hosted artifact that
supports updates at the same ID/URL, and a versioned deliverable whose older
revision is cited as immutable evidence. An existing owning README links the
current version. Include a newer incomplete draft and misleading modification
times that make the old revision appear newest.

**Prompt:** "Amend this artifact with the requested changes and make it clear
which version is latest." Repeat through `verify` as an audit of the amendment.

**Expected:** Updates mutable deliverables at the same path or artifact ID/URL.
When separate versions are required, updates the existing owner's explicit
latest-version link, revision, and supersession relationship. Labels a newer
incomplete revision as latest draft while keeping the current verified or
published version separately identified, without inventing approval. Does not
infer the current revision from timestamps, directory order, or `final-v2`
suffixes. Updates current-use links after the replacement is ready, preserves
intentional historical citations and immutable contents, and verifies that the
entry point opens the intended revision. The completion response links directly
to the amended artifact, gives its status and a brief change summary, and names
the superseded artifact when a separate replacement was needed. No extra
`LATEST` file, copied deliverable, or version index is created when the existing
owner suffices. Audit mode reports stale or competing current links and incorrect
readiness labels without changing the artifacts.

## Recording Results

For each run, report PASS, FAIL, or UNVERIFIED with evidence and remaining gaps.
Keep structural checks, runtime discovery, and behavioral runs separate in the
report. Documentation review or successful skill discovery does not count as a
completed behavioral scenario.
