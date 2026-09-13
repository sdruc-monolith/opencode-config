# Task File Template

Write one `NN_<task-name>.md` per coherent, independently verifiable outcome. Use a heading such as `T02: Implement the bounded selector`. The plan's `README.md` owns status and dependency edges; this file owns the instructions and acceptance for the task.

## Outcome

What observable capability exists when this task is complete, and which whole-plan acceptance criteria it supports. Include the implementation and its tests in the same task.

## Required Context

- Read the plan's `README.md` first, including global constraints and this task's prerequisites in the canonical checklist.
- Read the history entries linked beside this task's checklist item and any relevant corrections. Current task/design instructions define the contract; reconcile any unresolved contradiction instead of implementing superseded advice.
- Link exact shared design sections or prior task outputs required here and explain why each is needed. Briefly restate critical invariants, pointing to their authoritative definition.
- Name repository-relative source files, symbols, relevant callers, and existing tests to inspect. Distinguish existing locations from proposed additions or moves; use the source root declared in the overview.
- Define unfamiliar domain terms. Required facts and decisions must be available in this working set, not hidden in historical logs or prior conversation.

## Preconditions

Describe the concrete results expected from prerequisite tasks, required environment/tooling, and settled decisions. The overview remains authoritative for dependency IDs and status. If a prerequisite is missing or conflicts with current code, report the exact mismatch and affected work rather than inventing a replacement contract.

## Design and Contracts

- Chosen approach and rationale, including important interfaces, invariants, and failure behavior. Reference shared definitions instead of creating competing copies.
- Owning modules, dependency direction, existing functionality to reuse/generalize, and relevant callers to migrate. Preserve genuinely distinct policies.
- Compatibility, input/output schemas, and recovery/idempotency requirements that matter to this task.
- A small independently worked example when semantics are subtle. Specify consequential choices while leaving incidental implementation details flexible.

## Implementation Steps

A short ordered sequence of coherent actions. Include relevant module moves/extractions, implementation, caller migration, tests, and documentation together. Each step explains what to change and why; avoid one task per method or edit.

## Verification and Acceptance

- Observable assertions, fixtures/inputs, and expected results for this outcome, including relevant failure paths and compatibility behavior.
- Exact commands and their working directories, using the project's toolchain. If a command cannot yet be determined, identify the discovery step and whether it blocks readiness.
- How to distinguish success from setup failure or an unrelated baseline failure. For bug fixes, describe the check that should fail before the fix and pass after it.
- For an integration-verification task, cover the combined workflow and cross-task contracts. Individual task results do not replace this check.

## Completion Evidence

Record the checks actually performed, their outcomes, and the revision/worktree scope covered. Link detailed reports or logs where they belong. Summarize meaningful decisions or deviations and update their authoritative definitions when necessary.

Record consequential mistakes, pitfalls, and revisions using [the history template](history-template.md), after correcting current instructions. Add descriptive, comma-separated links to the relevant entries beside this task's README checklist item; reuse the same entry on other affected tasks. Keep the lesson and its explanation in history rather than copying it into separate logs.

Only after this evidence supports the task's acceptance should the implementer check the corresponding entry in `README.md` and update its next task. A blocked required check leaves the task unchecked, even if the code is implemented. Keep progress status in the overview, not in a second checklist here.

## Blockers and Handoff

State the smallest action needed to resolve a blocker, any unfinished edits, and the concrete output the next task consumes. An interrupted task records its next action so another session can resume from the overview and this file.

## Investigation Adaptation

For an investigation, replace implementation steps with the question, bounded method, and decision/evidence to produce. State the exit condition and where the resulting contract must be recorded. Keep dependent implementation blocked until consequential questions are settled. Prototype edits or external actions still require authorization; a research plan is not permission to execute them.
