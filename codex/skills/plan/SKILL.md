---
name: plan
description: Plan features, architecture changes, migrations, and complex refactors. Use when asked to plan or scope engineering work, or when a substantial change needs repository-grounded decisions and verifiable implementation steps.
---

# Plan

Turn the request into a plan another session can execute. Save new plans as numbered directories with a compact overview and outcome-oriented task files. A small plan can contain only the overview; substantial work needs explicit decisions, dependencies, and observable acceptance criteria.

## Plan Directory Contract

- Use the project's established plan location, defaulting to `artifacts/plans/` when none exists. Name each new plan directory `<NNN><optional-letter>_<name>/`, such as `018_model-import/` or `013b_state-driven-selection/`: three decimal digits, an optional lowercase subplan letter, and a descriptive lowercase hyphenated name.
- Honor a user-supplied plan ID. Otherwise inspect existing plan files and directories before assigning the next unused number; for a requested subplan, use the specified parent's number and an unused letter. Preserve existing IDs and names, never overwrite an occupied ID, and resolve ambiguity rather than guessing a parent. Record parent/related-plan links and whether anything is superseded; a letter alone does not imply supersession.
- `README.md` is the entry point: TL;DR, global constraints, current state, canonical checklist/index, dependencies, next task, and whole-plan acceptance. Keep it short enough to read at every restart.
- Use `01_<task-name>.md`, `02_<task-name>.md`, and so on for coherent implementation outcomes. Task IDs and filenames remain stable after work starts; explicit dependencies determine execution order, not numbering alone.
- Create `design.md` only when several tasks need detailed shared contracts, architecture, or decisions. Keep a concise orientation in the overview and link exact required sections from tasks. Keep detailed execution evidence in report locations rather than growing the overview into a transcript.
- Create `history.md` in the plan directory when the first consequential mistake, pitfall, or revision occurs, using [the history template](references/history-template.md). Give entries stable headings such as `## H001`, linking to `history.md#h001` rather than line numbers. Add descriptive, comma-separated history links beside each affected checklist item; one entry can serve several tasks.
- For small work, keep the short steps and verification inline in `README.md`. Add task files only when there are meaningful separate outcomes. Continue existing single-file plans in place unless migration is requested; do not bulk-convert historical plans.

`README.md` owns task status and dependency edges. Task files own detailed implementation instructions and acceptance criteria; shared design documents own cross-task contracts. Maintain one progress checklist, not independent status lists in every file. Brief reminders of critical invariants may appear in tasks with a pointer to their authoritative definition.

History records what went wrong or changed, why, the resolution or remaining uncertainty, and evidence. Correct current task/design instructions first, then record the history and attach its links to the checklist. Preserve entry IDs and keep corrections traceable; history explains current instructions rather than replacing them. Record useful lessons and material revisions, not every typo or routine failed command.

## Organization and Reuse Across Languages

Organize source code into cohesive modules by domain or capability, with clear responsibilities and dependency direction. Actively reuse and generalize common behavior so each shared rule or operation has one authoritative implementation. Evolve the structure as responsibilities grow, using the language's idiomatic modules, packages, and visibility mechanisms.

- Plan meaningful submodules as distinct responsibilities emerge rather than accumulating unrelated files in a flat source directory. Group code that changes together and keep entry points thin.
- Give shared capabilities descriptive homes at the narrowest boundary shared by their consumers. Prefer explicit ownership over catch-all `utils`, `helpers`, or `common` collections.
- Generalize behavior based on shared meaning, including differently written implementations of the same rule. Keep genuinely different business policies distinct and expose real variation explicitly.
- The smallest coherent change includes necessary extraction and reorganization. Minimize unrelated work, not the number of files changed; include relevant existing callers when consolidation requires it.
- Keep genuinely small programs simple. Each new directory or abstraction should represent a real responsibility or reusable capability rather than an empty architectural scaffold.

## 1. Establish the Request and Current State

- Identify the desired outcome and whether the user requested planning only or also authorized implementation.
- Inspect applicable project instructions, relevant code and callers, existing tests, documentation, and version-control state. Identify canonical development and verification commands from project automation.
- Map current module responsibilities and dependencies. Search for existing implementations and reusable dependencies before proposing new functionality; identify both copied code and repeated business rules.
- Record current file paths and symbols as evidence. Clearly label proposed files and interfaces. Revalidate paths when resuming an older plan.
- Distinguish observed behavior, desired behavior, assumptions, and unresolved decisions. Respect existing public contracts and supported environments.
- For Python architecture, dependencies, or data processing, load `python-engineering` using the runtime's skill mechanism, or read its `SKILL.md` when skills are file-based. Read its data-pipeline reference when schemas, joins, storage, or incremental processing are involved.

**Done when:** the objective, affected boundaries, current behavior, and relevant constraints are grounded in inspected evidence.

## 2. Resolve Decisions That Affect the Approach

- Investigate discoverable facts yourself. Ask the user about consequential choices the repository and request do not settle, supplying a recommendation and trade-off.
- State reasonable, reversible assumptions and continue independent planning. Mark a blocking question against only the work that depends on it.
- Compare alternatives when the choice materially affects correctness, compatibility, operational cost, or maintainability. Prefer the smallest design that meets the real requirements.
- When uncertainty needs an experiment, define its question, bounded scope, evidence, and exit condition. A planning-only or read-only session specifies the experiment rather than executing code changes.
- Record the reason for a decision in the owning task or shared design document. Keep current instructions current and label superseded material as history. Use the project's ADR convention only for significant, durable trade-offs.

**Done when:** each implementation-blocking decision is resolved or explicitly attached to a blocked step; assumptions are visible.

## 3. Slice the Work

- Write observable acceptance criteria, then break the change into coherent, independently verifiable outcomes. Keep implementation, its tests, and necessary documentation together; a task can touch multiple modules. Split by meaningful work boundaries, not by document headings, individual functions, or one file per edit.
- For substantial changes, include the proposed module/package layout, responsibility of each affected boundary, public interfaces, and dependency direction. Name implementations to reuse or consolidate and the callers to migrate; explain when superficially similar behavior should remain separate.
- Prefer a narrow end-to-end path that can be exercised independently. For a pipeline, start with representative input flowing through the actual transformation to its output boundary.
- Scope prerequisite refactoring to the change, including behavior-preserving extractions and module moves needed for coherent organization and reuse. For wide migrations, use expand, migrate, contract when that lets intermediate states remain compatible; otherwise identify the required atomic integration boundary.
- For large efforts, separate investigation tasks from implementation tasks. Give investigations a question, bounded method, and decision/evidence output. Mark implementation that depends on unresolved design as blocked, rather than leaving a less capable implementer to invent the answer.
- Size each task so a fresh agent can implement and verify it using the overview, the task file, explicitly named references, and current source. Split tasks that combine independent outcomes or substantially different context; keep tightly coupled edits together when separation would create unusable intermediate states or excessive handoffs.
- Settle consequential design choices before a task becomes ready. Define domain terms, important interfaces, invariants, error behavior, existing abstractions to reuse, and callers to migrate. Give a short worked example when semantics are subtle, and explain what to report if a prerequisite is false.
- Choose test boundaries from observable contracts and existing tests. Use unit, integration, file-output, or runtime checks where they provide useful evidence. Testing effort should match behavior and risk.
- Discover exact check commands where possible; otherwise state what must be discovered and why. Do not assume a package manager, checker, or coverage target.
- Include integrated acceptance after the component work, normally as the final task for a multi-task plan. Passing individual tasks does not by itself prove the combined behavior.

Use [the overview template](references/plan-template.md) for `README.md` and [the task template](references/task-template.md) for each implementation or investigation file. Omit irrelevant sections, but retain the context and verification needed for an unfamiliar implementer.

**Done when:** ready tasks are executable without reconstructing the conversation or inventing consequential decisions, dependencies and module ownership are explicit, and every acceptance criterion has a verification approach. If all work is blocked, name the decision or investigation needed to unblock it.

## 4. Deliver the Plan

- When saving is requested or part of the authorized workflow and editing is permitted, create the plan directory and return its `README.md` path with a concise summary. Otherwise return the overview and task breakdown in the conversation, identifying files that would be created; do not claim an unsaved plan is on disk.
- Check that every task is indexed, links resolve, dependency IDs exist, the dependency graph is acyclic, and each task's required context is explicit. For history links, verify unique entry IDs and matching heading anchors, not just file existence. Document source-path roots and command working directories, especially when the plan and code live in different worktrees.
- Keep the checklist authoritative: use unchecked entries labeled pending, ready, in progress, or blocked; check an entry as completed only with verification evidence. Separate implemented-but-unverified work from completion. Record evidence first, then update the overview and next task; reopen affected entries when changes invalidate earlier evidence.
- Specify the reading sequence: overview, selected task, its checklist-linked history entries, then required references and source. Read linked corrections as needed, without loading unrelated task details or the entire history by default. Whole-plan verification must still cover every required outcome and integrated acceptance.
- Keep one authoritative plan directory and link supporting evidence. Publishing issues or changing tracker state requires user authorization.
- End with the next executable step and any blocking decision. A plan with blockers is usable for its unblocked work, not a claim that every decision is settled.
- Planning-only requests stop here. If implementation was also requested and permissions allow it, load `implement` and continue with the plan.

Skill loading does not change agent mode or permissions. This workflow requires no subagents; use delegation only when explicitly authorized by the user or applicable instructions.
