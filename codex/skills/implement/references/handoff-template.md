# Implementation Handoff

Use when work will continue in another session. Keep it brief and omit empty fields. Return it in the conversation unless saving is requested or part of the authorized workflow; use the project's established artifact location when available.

## Goal and Source

- Request and authoritative plan/specification path or URL. For a plan directory, link its `README.md`, current task ID/file, and exact required shared references in reading order.
- Acceptance criteria being implemented.

## Current State

- Branch/revision if available; relevant staged, unstaged, and untracked changes.
- Link the canonical progress checklist and relevant evidence instead of maintaining a second task-status list in this handoff.
- In-progress slice and incomplete edits that the next session must understand.
- Existing user work that overlaps this task.

## Decisions and Deviations

Link the current task/design decisions and relevant stable history entries from the checklist. Record consequential mistakes, pitfalls, and revisions in the plan's history before handing off when editing is allowed; avoid creating a second history in this handoff. If saving is unavailable, include the proposed entry and affected checklist links, clearly marked unsaved.

## Verification

| Requirement/check | Result | Evidence and scope |
| --- | --- | --- |
| Outcome or command | PASS / FAIL / UNVERIFIED | Command, working directory, result, and the revision/worktree state it covered |

Separate baseline failures from new failures. Note when subsequent edits invalidated earlier evidence. Redact credentials and sensitive payloads.

## Resume Here

- Next unblocked task and exact files/symbols to inspect, consistent with the overview's dependencies and authorized scope. Read overview, task, and required references rather than the entire directory.
- Blocking decisions, failed approaches worth avoiding, and missing environment prerequisites.
- Applicable skills, normally `implement` plus `python-engineering` for Python work.

The next session must revalidate this state against the current worktree before continuing.
