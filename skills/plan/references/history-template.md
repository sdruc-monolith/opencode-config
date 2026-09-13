# Linked Plan History

Create `history.md` beside the plan's `README.md` only when there is a consequential mistake, reusable pitfall, failed approach worth avoiding, or material plan revision to record. A small plan can add history without splitting its inline tasks into separate files. Keep routine command output and transient editing errors out of this record.

## Entry Identity and Linking

- Use unique, increasing IDs within the plan: `H001`, `H002`, and so on. Check existing entries before assigning the next ID. Keep each heading to its ID alone (for example, `## H001`), with its descriptive title and date on the following line; that example's heading anchor is `#h001`.
- Never renumber, reuse, or rename an entry ID. When later evidence corrects an entry, append a follow-up with a new ID and cross-link the correction; preserve the original observation and label its superseded conclusion.
- Add a `History:` suffix with descriptive, comma-separated links on the affected README checklist item or an indented continuation line. Use the same entry link on multiple affected tasks instead of copying its contents. Link a follow-up alongside the original when it changes the lesson.
- Keep task status and dependencies solely in the README checklist. A history entry is not a second task-status record and is not itself proof of task completion.

Example checklist syntax, using Markdown reference links that render beside the item. Inline Markdown links to the same targets work equally well:

```markdown
- [ ] **T02: Implement selector** — in progress; depends on T01.
  History: [duplicate-key pitfall][h001], [revised schema][h002]

[h001]: history.md#h001
[h002]: history.md#h002
```

Create links only for entries that actually exist. Keep unresolved blockers explicit on the checklist so an agent can identify blocked work before opening history.

## Entry Template

Use the following structure in the generated `history.md`, replacing the example ID and placeholders. Keep entries concise and link detailed evidence rather than pasting transcripts.

```markdown
## H001

**T02 — Short descriptive title — YYYY-MM-DD**

- Observation: What failed, proved incorrect, or changed.
- Cause or rationale: Confirmed explanation, or a clearly labeled hypothesis.
- Resolution: What corrected the issue, or what remains unresolved.
- Plan revision: Exact task/design sections changed and affected task IDs.
- Evidence: Relevant test, command/result, revision, or report link; state when unverified.
- Pitfall: The concrete check or action a future implementer should take.
```

For a deliberate revision with no mistake, explain the old/new decision and why it changed. Omit inapplicable fields rather than inventing a cause or test result. For a shared contract change, update the canonical design, affected task instructions, dependency edges, and any invalidated completion claims; link the history entry from every affected checklist item.

## Recording and Resuming

1. Correct current instructions in the owning task/design (or inline README work section); leave unresolved decisions visibly blocked.
2. Record the event and supporting evidence here, preserving uncertainty and prior observations.
3. Attach the entry links beside affected checklist items and update their status/next action when needed.
4. Before resuming a task, read its checklist-linked entries and relevant corrections. Use current task/design instructions as the implementation contract. If history exposes an unresolved contradiction, reconcile it before proceeding rather than silently choosing a version.

Keep current instructions sufficient to implement the task. History explains the lessons behind them; it should not become the only place that defines required behavior.
