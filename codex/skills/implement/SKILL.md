---
name: implement
description: Implement a plan, specification, or substantial agreed change in small verified steps. Use when asked to build from a plan, execute engineering work, or resume an implementation across sessions.
---

# Implement

Build the requested behavior in coherent, verified slices. Treat the plan as a guide grounded in current code, not as evidence that work is already complete.

## 1. Reconcile the Starting Point

- Read the request and relevant project instructions. For a plan directory, start with its `README.md`; if given a task file, read its owning overview as well. Use the canonical checklist and dependency edges to select the requested unblocked task or the next ready task within the authorized scope.
- Load the selected task, the history entries linked beside its checklist item (including relevant corrections), its explicitly required references, and relevant current code/tests. Read other task details or historical reports only when needed. A README-only plan contains its work inline; continue a legacy single-file plan without converting it unless requested.
- Inspect version-control state and account for existing user work before editing. Validate the task's concrete preconditions and settled contracts; report missing required context or unresolved consequential decisions instead of guessing.
- Map acceptance criteria to completed, pending, and blocked work. Verify prior completion claims against current code and evidence.
- Recheck paths, interfaces, dependencies, and commands from older plans. Correct stale mechanical details; surface material changes to scope or public behavior.
- Before adding functionality, inspect existing modules, callers, and dependencies for a suitable implementation to reuse or generalize. Identify the owning domain/capability and any duplicated rules the change should consolidate.
- For a substantial change without an actionable plan, load `plan` to establish one. Retain the user's implementation authorization; planning is not an automatic approval gate. A small, clear task needs only a short checklist.
- For multi-step work, use available task or progress-tracking tools to maintain a concise live checklist. When a plan exists, each item should link or explicitly refer to its owning task file or canonical checklist entry so its details remain easy to find. Keep the live checklist aligned as slices start, complete, or become blocked, and do not use it for trivial actions or as a substitute for durable project artifacts.
- Load `python-engineering` for Python work and its relevant references for pipeline, testing, or performance decisions. Use `ui-app-testing` when the change affects a UI workflow.

**Done when:** the next slice is unblocked, its outcome is understood, and the relevant verification command or approach is known.

## 2. Establish a Useful Feedback Loop

- For a bug, prefer a regression test that fails on the reported symptom before the fix. Confirm it fails for the behavior under investigation, rather than setup, imports, or an unrelated failure.
- For substantial new behavior, prefer one behavioral test followed by the implementation that satisfies it. Use expected results from the specification or independently worked examples.
- Before restructuring uncertain existing behavior, add focused characterization coverage where valuable. Distinguish behavior to preserve from a defect the request explicitly changes.
- For reversible, low-impact changes, use proportionate existing checks instead of adding tests that merely mirror the edit.
- Choose boundaries that expose the contract: a callable, API, command, persisted dataset, or running workflow. Reuse established test seams without requiring routine user approval.
- When reproduction is unavailable, investigate with the evidence you can access and identify uncertainty. Do not claim a regression was reproduced or fixed without supporting evidence.

**Done when:** there is a meaningful way to detect success or regression, or its concrete blocker is recorded.

## 3. Implement One Slice at a Time

Apply these organization and reuse requirements in every language:

- Place behavior in cohesive modules/submodules by domain or capability. As responsibilities grow, introduce meaningful structure instead of extending a flat collection of unrelated source files; keep entry points thin and dependencies directional.
- Reuse or generalize an existing implementation before creating a parallel one. Extract repeated rules and operations into focused functions, composed objects, or small interfaces, using the language's idioms.
- Give shared behavior a descriptive owner at the narrowest boundary common to its consumers. Keep caller-specific policy explicit through meaningful parameters, configuration, or collaborators; avoid a universal helper with unrelated mode flags.
- Migrate the relevant existing callers to the shared implementation and remove superseded duplicate logic. An extraction is incomplete while those callers retain independent copies of the same behavior. Preserve genuinely different policies and unrelated user work.
- For module moves, update imports/exports, entry points, build/package configuration, and tests together. Preserve public compatibility where required and verify each affected caller's contract.

1. Mark the slice in progress and make the smallest coherent change that satisfies its outcome, including necessary extraction and reorganization. Measure scope by behavior and responsibility, not by the number of files edited.
2. Preserve relevant APIs, schemas, error behavior, resource ownership, and repository tooling. Keep dependency changes justified and lockfiles consistent.
3. Run focused tests/checks after a meaningful edit. Actively reduce duplication and improve module cohesion in the affected code, keeping the feedback loop green. Check shared behavior through the relevant callers as well as its own boundary.
4. Resolve failures caused by the change. Record unrelated baseline failures or environment blockers separately.
5. Record verification evidence in the task or linked report, then update the canonical checklist and next action in the plan's `README.md`. Check a task as completed only when its required acceptance is supported; implemented-but-unverified work stays unchecked with its blocker stated. Keep task status/dependency edges in the overview, not duplicated in task files. For legacy plans, update their existing progress section; if editing is unavailable, report the proposed update in the conversation.
6. Continue to the next unblocked slice within the authorized scope, loading its context as needed. Record material decisions in the owning task/shared design, update affected instructions and dependencies, and reopen checklist entries whose evidence was invalidated. Record consequential mistakes, pitfalls, and revisions as described below before handing off or progressing past them.

For plan directories, use [the linked history format](../plan/references/history-template.md). Create `history.md` at the first meaningful event. Correct current task/design instructions first, then record what happened, the cause or hypothesis, resolution, affected plan sections, evidence, and the actionable lesson. Assign a stable `H001`-style heading and add descriptive, comma-separated links such as `history.md#h001` beside every affected README checklist item. Preserve IDs, cross-link later corrections, and keep blockers/status in the canonical checklist. Record useful lessons rather than routine command noise; if plan editing is unavailable, report the proposed entry and links without claiming they were saved.

For data pipelines, exercise real input, transformation, and output together early. Add scale, schema evolution, and recovery behavior as the acceptance criteria require; preserve semantics when changing engines.

Keep execution local to the current authorized workflow. Commit, push, create PRs, publish tickets, or delegate only when explicitly authorized. The skill itself does not authorize those actions.

## 4. Verify the Complete Change

- Load `verify` for the completed task, supplying the acceptance criteria, relevant diff scope, and checks already run.
- For a whole-plan implementation, complete its integrated acceptance task/checks after component tasks. Checked component entries alone do not establish completion of the combined behavior.
- Address concrete findings within the requested scope, then rerun checks affected by those changes. Reuse still-valid evidence instead of repeatedly running an unchanged suite.
- A blocked check remains unverified even when other checks pass. Continue the strongest feasible verification and identify the smallest action that would unblock it.

**Done when:** each acceptance criterion has a PASS, FAIL, or UNVERIFIED result, and any remaining failure or unfinished work is explicit. Report full completion only when required behavior is implemented and supported by the required evidence.

Summarize behavior changed, verification results, material deviations, and blockers. For a session interruption or requested handoff, use [the handoff template](references/handoff-template.md) and reference existing artifacts rather than duplicating them.
