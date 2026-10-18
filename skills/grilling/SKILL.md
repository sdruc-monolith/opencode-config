---
name: grilling
description: Stress-test a plan, decision, or idea through rounds of recommended questions. Use when the user explicitly requests grilling or opts into it during planning.
license: MIT
---

# Grilling

Interview the user thoroughly until you reach a shared understanding of the agreed scope. Map the discussion as a **design tree**: each decision can unlock further decisions that depend on it. Be direct and constructive. Challenge unclear assumptions without repeatedly questioning settled answers.

## Establish Scope

- Start from the user's request, relevant evidence, and decisions already made. When invoked by `plan`, use its current context and the user's opt-in; do not ask for permission to grill again.
- Identify the outcome and boundaries being discussed. Cover consequential choices about requirements, behavior, design, trade-offs, failure cases, and verification as relevant. Keep incidental implementation details out of the interview unless they affect those choices.
- Maintain a concise distinction between settled decisions, open questions, and facts still being investigated. Do not create a plan directory or other saved artifact solely to track the interview.

## Ask in Dependency-Aware Rounds

The **frontier** is the set of open decisions whose prerequisites are already settled. Ask the whole frontier in one round, then wait for answers before asking the next round. If a question depends on another unanswered question, save it for a later round.

Number each question, explain the choice in simple language, and give a recommended answer with a short reason. Phrase the question so that "yes" accepts the recommendation. Use the runtime's question tool when available, keeping the questions and recommendations together; otherwise use this conversational format:

```markdown
### Q1: <Short question title>

<Question and relevant trade-off.>

Recommended: <Answer and why.>

### Q2: <Short question title>

<Another question whose prerequisites are already settled.>

Recommended: <Answer and why.>
```

After each round:

1. Track the answers and any changed decisions in the conversation. Clarify ambiguous or partial answers rather than treating silence as agreement.
2. Recompute the frontier. New answers may unlock questions, remove branches, or expose a conflict with an earlier decision.
3. Ask the next round of ready questions. Keep numbering unambiguous and avoid reopening settled choices without new evidence or a user-requested change.

## Investigate Facts Yourself

- Look up discoverable facts using the repository, documentation, and available tools. Do not ask the user for facts you can inspect yourself.
- Treat an unfinished investigation as an unsettled prerequisite. Continue with independent questions while dependent questions wait; report inaccessible facts explicitly rather than inventing answers.
- Present consequential decisions to the user with evidence and recommendations. Do not silently choose on their behalf unless they explicitly delegate the choice.
- This interview does not authorize implementation, publishing, or delegation. Research directly by default; use subagents only when separately authorized by the user or applicable instructions.

## Finish and Return to Planning

- Finish when every in-scope branch is resolved or explicitly deferred and no ready question remains. Summarize the agreed outcome, constraints, decisions and reasons, acceptance expectations, and any deferred or blocked work.
- Ask the user to confirm that the summary captures the shared understanding before proceeding beyond the interview. If they correct it, update the affected decisions and ask any newly unblocked questions.
- When called from `plan`, return the confirmed decisions to that workflow and continue its normal planning steps. Do not restart `plan` or repeat the grilling offer. Preserve whether the user authorized planning only or also implementation; interview confirmation alone does not authorize implementation.
- If the user asks to stop grilling, stop immediately, summarize settled decisions and unresolved questions, and return to the requested workflow. Mark affected work as unresolved rather than claiming the interview completed.

## Use the Same Plan Artifacts

Grilling changes how decisions are reached, not the plan's format or file structure. Keep interview rounds, the design tree, and the confirmation summary in the conversation. Do not create a separate grilling report, transcript, decision log, directory, or progress checklist.

- When a saved plan is justified, put the confirmed outcomes directly into the normal `plan` artifacts: scope, global constraints, open questions, and the canonical task/workstream index in `README.md`; detailed decisions, rationale, and acceptance criteria in the owning task files; shared contracts in `design.md` only when the normal planning rules call for it.
- Update an existing plan in place, preserving its IDs and canonical checklist. Use `history.md` only for consequential revisions under the normal history rules, never as an interview transcript or one entry per answer.
- Derive implementation tasks from the agreed outcomes using the same dependency, parallel-workstream, and single-session sizing rules. Question numbers and design-tree branches are not task IDs or a reason to create extra task files.
- For conversational planning or standalone grilling, return the decisions in the conversation. Grilling alone does not justify saving artifacts. The final plan must be understandable without reading the interview transcript.

Adapted from [Matt Pocock's grilling skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md). See [LICENSE](LICENSE).
