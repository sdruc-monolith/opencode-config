---
name: verify
description: Verify engineering work against requirements and current evidence. Use for completion audits, explicit verification requests, or after meaningful implementation to check behavior, regressions, and required project checks.
---

# Verify

Support completion claims with current evidence. Check both whether the implementation delivers the requested behavior and whether the change introduces concrete engineering problems.

This skill audits and reports. It may run permitted checks that generate build/test artifacts, but does not manually edit source, repair failures, or accept new test baselines. An implementation workflow can act on findings and invoke verification again.

## 1. Establish Scope

- Read the request/specification, applicable instructions, acceptance criteria, and relevant implementation. When no formal specification exists, derive concise criteria from the user's request and existing public contracts.
- For a plan directory, begin with `README.md`, then read the task(s) being audited and their required references. A whole-plan audit must cover every acceptance criterion and integrated behavior, loading task evidence as needed. A task-only audit must not claim the entire plan is verified.
- Identify the comparison appropriate to the request. For working changes, inspect staged and unstaged diffs and relevant untracked files; for a branch/PR, establish its intended base and include additional working changes only when in scope.
- Distinguish this task's changes from pre-existing user work. Include callers, fixtures, migrations, and configuration affected by changed contracts.
- Load `python-engineering` for Python-specific review and relevant data/testing/performance references. For browser and visual validation, consult the validation steps of `ui-app-testing` when applicable; during this audit, report defects to the implementer rather than applying its remediation steps.

**Done when:** the requirements and change scope are explicit, including any missing evidence needed to determine them.

## 2. Select and Run Checks

- Discover canonical commands from project instructions, task runners, CI, and tool configuration. Use the project's environment and supported versions.
- Select relevant formatting checks, linting, type checks, tests, builds, and runtime checks. Use non-fixing modes when available; if a command would rewrite source, find an audit alternative or report the constraint.
- Start with focused checks. Run required repository gates and broaden to the affected subsystem or full suite when shared behavior, migration risk, or project policy warrants it.
- Reuse earlier checks only when their scope and results are known and subsequent edits have not invalidated them. Repeat verification when new edits, failures, or unresolved concerns justify it.
- Capture commands, working directories, outcomes, and relevant failure output. Preserve exit status; do not let output filtering or a pipeline turn failure into apparent success.
- Report missing tools, inaccessible services, unavailable credentials, and timeouts as blockers. Complete independent checks that remain feasible.

**Done when:** applicable checks have results or concrete blockers; no required check is silently omitted.

## 3. Inspect Behavioral Evidence and the Diff

- Match each acceptance criterion to code and the strongest relevant evidence. Compilation and static inspection alone do not establish runtime behavior.
- Audit plan completion claims against the canonical overview checklist and task evidence. Flag checked entries with missing/stale evidence, unresolved prerequisites, or blocked verification. Check that task links and dependency IDs resolve, dependencies are acyclic, and all required work is indexed. Report inconsistent progress copies or missing shared contracts rather than treating a complete-looking index as proof.
- Read the history entries linked beside the audited tasks. Check that links resolve to unique stable headings, shared events are linked from affected checklist items, and relevant corrections are traceable. Verify that revisions reached current task/design instructions and invalidated completion claims were reopened; history must not be the sole definition of current behavior. Report findings without editing the plan or history during the audit.
- Check public compatibility, error paths, dependency/lockfile changes, resource cleanup, and meaningful regression coverage. Review security-sensitive boundaries when the change touches them.
- In every language, check that affected source is organized into cohesive domain/capability modules with clear ownership and dependency direction. Identify unrelated files accumulating in flat directories, catch-all utility modules, circular dependencies, and entry points containing reusable business logic. Judge meaningful responsibilities rather than directory depth or arbitrary file-count limits.
- Look for semantic duplication as well as copied code. Verify that shared rules/operations reuse one authoritative implementation, relevant existing callers were migrated, and superseded copies were removed. Check that abstractions simplify their consumers while preserving genuine caller-specific policy.
- For extractions and module moves, verify public imports/exports, build/package inclusion, entry points, and affected caller contracts. Report structural or reuse findings with concrete files, callers, and maintenance/behavioral impact; avoid demanding a repository-wide rewrite for a local issue.
- Prioritize concrete defects and unmet requirements over stylistic preferences. Give file/line references, impact, and practical remediation for findings; identify uncertainty where evidence is incomplete.
- Check for scope drift, debug artifacts, and accidental unrelated edits. Report those findings rather than removing unfamiliar work.
- For data pipelines, inspect schema and value assertions, row grain, key uniqueness, join cardinality, null/timezone/decimal semantics, and persisted output where relevant. A dataset can itself be the public interface.
- Verify rerun and partial-failure behavior when part of the contract. Require representative before/after timing and memory evidence for performance claims; a tiny correctness fixture does not establish scalability.

**Done when:** requested outcomes and relevant regressions are accounted for, including behavior not exercised by automated checks.

## 4. Report

Lead with concrete findings, ordered by impact. If there are none, say so without treating absence of findings as proof of untested behavior.

For each acceptance criterion or required check, use:

| Result | Meaning |
| --- | --- |
| PASS | Current, relevant evidence supports the criterion at the stated scope. |
| FAIL | Observed behavior or a completed check contradicts the criterion. |
| UNVERIFIED | Evidence is insufficient, stale, or blocked; state why and how to unblock it. |

Include a compact requirement/evidence table for substantial work. For small changes, a concise result list is sufficient. Record baseline failures separately; a known baseline failure is still a failed check, not a pass.

End with verification performed, remaining gaps, and the next action. Do not declare the whole task verified while a required outcome is failed or unverified. Return findings to `implement` or the user; this workflow requires no delegation or automatic Git/tracker actions.
