# Plan Overview Template

Write this as `README.md` inside `<NNN><optional-letter>_<name>/`. Use the plan ID and descriptive title as the generated document's heading. Keep the overview compact; put substantial task details in files based on [the task template](task-template.md).

## TL;DR

The user-visible or caller-visible outcome, chosen approach, and why it matters, in a few sentences.

## Current State

- What is implemented and verified, what remains, and the immediate blocker if any.
- Source repository/worktree and baseline revision when known. Explicitly define the root for source paths and commands; document links are relative to this plan directory.
- Parent and related plans, linked by title. State exactly what this plan supersedes, if anything.

This is a brief orientation, not a second progress list. The checklist below is authoritative for individual task status and dependencies.

## Global Constraints and Decisions

- The few invariants, public contracts, compatibility requirements, and scope boundaries every implementer must know.
- A concise architecture/organization summary: owning modules, dependency direction, and shared functionality to reuse or consolidate.
- Important settled decisions and their rationale. Link detailed shared contracts in `design.md` only when multiple tasks need them; otherwise keep detail in its owning task.
- For pipelines, summarize critical schema, row-grain, null/cardinality, and rerun/publication guarantees. Put extensive schema tables and examples in the relevant task or shared design section.

## Reading Order

1. Read this overview to understand scope, constraints, status, and dependencies.
2. Select the user-requested task if unblocked, otherwise the next ready task within the authorized scope.
3. Read that task file, the history entries linked beside its checklist item, and its explicit required references/source files. Follow linked corrections where relevant; do not load the entire plan directory or history by default.

Index shared design sections and supporting reports here with a short description of when each is needed. Required knowledge must be in the current plan or explicitly named references, not assumed from earlier conversation.

## Checklist and Task Index

Use one entry per task. Replace each title with a relative Markdown link to its task file; for a README-only plan, link to the inline work section. T01 corresponds to `01_<task-name>.md`. These are illustrative incomplete entries to replace with the actual task graph:

- [ ] **T01: First independently verifiable outcome** — ready; depends on none.
- [ ] **T02: Next outcome** — pending; depends on T01.
- [ ] **T03: Integrated verification** — pending; depends on T01 and T02.

Keep task IDs stable. Order entries for readability, but express all actual blockers explicitly; an independent task need not wait just because it appears later. A pending task becomes ready when prerequisites and consequential decisions are settled. Use blocked with a reason for unresolved decisions or environment constraints, and in progress for active work.

Only checked entries are completed. Attach concise verification evidence or a report link when checking an entry. Code implemented with required verification outstanding stays unchecked with the gap stated. Task documents may contain acceptance criteria and results, but do not maintain a competing progress checklist or status field.

When a task has a meaningful mistake, pitfall, or revision, add `History:` followed by descriptive, comma-separated links beside its checklist item (an indented continuation line is fine). Targets use stable entry anchors such as `history.md#h001`. Use [the history template](history-template.md) for the exact format; create the file and links only when an event occurs. Update corrected instructions in their owning task/design, and link shared events from every affected checklist item rather than duplicating their explanations.

## Whole-Plan Acceptance

- A1: An observable outcome with concrete inputs and expected behavior.
- A2: A relevant compatibility, failure-path, or integration requirement.
- Map each criterion to the task that proves it. Include a final integrated check for multi-task work rather than assuming individual task completion proves the combined result.

## Open Questions and Assumptions

Separate unresolved decisions from reversible assumptions, identify affected task IDs, and state the smallest action needed to resolve each blocker. Ready implementation tasks must not depend on unanswered consequential questions.

## Resume Here

Name the next task, why it is unblocked, and the exact starting file or command. If work is interrupted, state the next unfinished action and point to its evidence/handoff. If everything is blocked, identify the next decision or investigation instead.

## Small-Plan Adaptation

For a small plan, keep one inline work section with the outcome, relevant source, short implementation steps, and concrete verification. Point the checklist to that section and omit task files and `design.md`. Retain the TL;DR, applicable constraints, acceptance, and next action.
