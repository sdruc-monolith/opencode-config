---
name: artifact-management
description: Artifact and file management for generated outputs, reports, logs, screenshots, downloads, datasets, caches, and cleanup. Use when creating, amending, versioning, or organizing saved outputs, planning storage-heavy work, or auditing file and disk growth.
---

# Artifact and File Management

Treat files and disk space as resources with a purpose, an owner, and a lifecycle. Create the smallest useful set of durable outputs, organize them by responsibility, and clean up disposable work as part of the task.

This skill guides file handling within the authorized task. Existing project contracts and explicit retention requirements take precedence. An audit reports findings; it does not authorize reorganizing or deleting files.

## 1. Inspect Before Creating

- Inspect relevant project instructions, the selected worktree, nearby directories, existing outputs, and version-control state. Find the established source, documentation, data, report, build, cache, and temporary locations before choosing paths.
- Search for an existing file, section, output, or reusable capability that already serves the need. Prefer updating its authoritative home or linking to it over creating a competing copy.
- Before adding a file or directory, be able to explain its purpose, intended reader or consumer, owning workflow, and whether it is durable, reproducible, or disposable. Keep this reasoning in the conversation or existing task context; do not create a new inventory or management document merely to justify another file.
- For a small bounded edit, a quick local inspection is enough. Do not turn every file write into a repository-wide audit, storage scan, or approval ceremony.

## 2. Choose a Logical Home

Use the project's existing equivalents of these locations; this table is guidance, not a directory scaffold to create.

| Kind | Home and lifecycle |
| --- | --- |
| Source, tests, fixtures, reusable scripts | The selected worktree's normal source/test/tooling layout; maintained with the code. |
| Durable documentation and plans | The existing documentation or plan location; update the authoritative document and link related material. |
| Generated results and evidence | The owning workflow's output location; retain only what is needed for delivery, reproducibility, comparison, or diagnosis. |
| Build products and caches | Tool-managed locations with existing invalidation and cleanup rules; regenerate rather than copying into reports or source. |
| Downloads and extracted inputs | An established data/cache location, keyed by source identity or version where reuse matters; avoid repeated downloads and extra copies. |
| One-off experiments and intermediates | A task-owned temporary workspace in a permitted location; remove after use unless needed for a specific handoff or failure investigation. |

- Organize by domain or workflow, then by lifecycle where it matters. Keep related inputs, results, and evidence discoverable through their owning task or existing index. Avoid mixing disposable files with source or durable records.
- Add a directory only for a meaningful responsibility, distinct lifecycle, or real group of related files. Do not create empty scaffolding, a folder for each command or session, or parallel `misc`, `new`, `old`, and `archive` dumping grounds. Keep small coherent collections simple; do not force unrelated content into one giant file to reduce file count.
- Use descriptive, predictable names. Avoid `final-v2-fixed`, repeated backup suffixes, and timestamped copies of every edit. Use run IDs or timestamps when distinct runs are genuinely required by consumers, comparison, or reproducibility.
- Respect existing ignore rules and output contracts. Git-ignored does not mean disposable or free of storage cost; do not hide deliverable source in ignored artifact paths.
- Keep a brief result in the conversation or existing task/report unless a saved output is requested or needed by another workflow. Do not create extra summaries, manifests, status files, or cleanup reports by default.
- For durable plans, follow [the planning rules](../plan/SKILL.md#keep-plans-bounded-and-prefer-subplans), including the nine-task limit and linked subplans for substantial new scope. Subplans organize real work, not every attempt or routine correction.

## 3. Bound Storage Before Expensive Work

- Before large downloads, extraction, dataset generation, image builds, trace collection, or work with unknown growth, inspect available space on the actual destination and scratch filesystems. Use scoped measurements such as `df -h <existing-parent>` and `du -sk <owned-output-directory>` or platform equivalents; check quotas or inode availability when relevant. Do not recursively scan the entire machine when a targeted measurement is enough.
- Estimate peak additional storage, not just the final file: include compressed and expanded inputs, staging or atomic-replacement copies, build layers, spill files, logs, parallel workers, and retries. Estimate file count as well as bytes for partitioned or small-file-heavy outputs. State uncertainty rather than presenting guesses as measurements.
- Honor project or user budgets. Choose a bounded sample or pilot when size is unknown, measure it, and scale only when there is enough capacity with working headroom. If capacity is insufficient or cannot be established for a potentially large write, pause that operation and identify the needed space, smaller scope, or suitable destination; continue independent work.
- Prefer selective queries, streaming, batching, column projection, partition pruning, and incremental reuse over full exports and repeated materialization. Bound row counts, partition counts, log sizes, trace duration, retries, and concurrency where they drive growth. Do not change required output semantics merely to save space.
- Reuse valid cached inputs and tool caches rather than downloading or rebuilding copies. Check input identity, configuration, and version before reuse. Use references to existing data when consumers support them; never disguise misplaced deliverable code with symlinks or path overrides.
- Use runtime-approved temporary locations and tool-managed scratch where possible. Moving an output to `/tmp`, another worktree, or an external directory does not remove its storage cost or ownership obligation. Recheck growth at meaningful checkpoints for long-running work and stop the writer before exhausting capacity.

## 4. Reuse Outputs and Define Retention

- Prefer one authoritative current result for reproducible, replaceable outputs. Replace it only when it is task-owned, no consumer requires its old contents, and the replacement is verified; stage safely when an interrupted write could destroy the only usable result.
- Keep published, immutable, or cited evidence stable. Do not overwrite a path that a plan, report, or consumer relies on as evidence of an earlier run. Create a distinct retained version only when required, and link it from the existing owner rather than copying it into multiple folders.
- For task-owned disposable run outputs without another retention requirement, keep the current useful successful result and the evidence needed for unresolved failures. Discard redundant attempts and intermediates after verifying the retained result. Keep historical comparisons only when they answer a concrete question or satisfy a contract.
- Capture the smallest evidence that supports the claim: relevant log windows, representative samples, focused screenshots, and necessary traces. Avoid preserving full dumps or every browser capture when a concise result and selected evidence suffice. Retain larger evidence when diagnosis or reproducibility actually needs it.
- Record important retained output paths, input/revision identity, and regeneration commands in the existing task, report, or index. Add a separate manifest only when a consumer or reproducibility requirement needs one. Use tool-native rotation and retention for continuing output rather than inventing another archive hierarchy.
- Compress only retained material that benefits from it and remains usable by its consumers. Compression and moving files to `archive/` are not substitutes for deciding what to retain; count archives against the storage budget too.

## 5. Make the Latest Version Unambiguous

- When iterating or fulfilling an amendment, identify the existing deliverable first. Update its canonical file in place when it is mutable; for hosted artifacts, use the same artifact ID and stable URL when the platform supports versioned updates. Do not create a sibling deliverable for every requested change.
- Keep one obvious current entry point per deliverable or named variant. If separate retained versions are required, update the existing owning README, report, task, or platform metadata with an explicit `Latest version:` link and revision identifier. Do not make readers infer the latest version from directory order, modification times, filenames, or chat chronology. Reuse an existing index rather than adding a new `LATEST` file or duplicate artifact by default.
- Distinguish recency from readiness. If the newest revision is still a draft, incomplete, or unverified, label it `Latest draft` with its exact path/link and keep the `Current verified` or `Published` version identified separately when one exists. Never imply approval, publication, or verification merely because a revision is newer; use only statuses supported by evidence.
- When a new version supersedes an older one, make that relationship explicit in the owning index or editable metadata, with links to the replacement. Label retained older versions superseded where editing is allowed. Keep immutable or cited evidence unchanged; record its supersession alongside it in the mutable owner rather than rewriting historical evidence.
- Update current-use links and handoffs to the new current version when it is ready, while preserving historical citations that intentionally refer to an older revision. Verify that the entry point resolves to the intended contents and that competing links do not still claim a different version is current. Apply the normal retention rules to redundant task-owned drafts.
- In the amendment completion response, lead with the exact updated artifact path or URL, identify its revision/status when relevant, and briefly state what changed. If a separate artifact was necessary, say which previous artifact it supersedes. A user should be able to open the latest version directly from that response.

## 6. Clean Up Within Known Ownership

- Remove task-created disposable files when they are no longer needed, including failed downloads, extraction intermediates, redundant captures, and temporary experiment scripts. First preserve required evidence and verify the retained result or handoff. During an audit-only workflow, leave findings for the implementer; temporary resources created solely by the audit may follow their established teardown policy.
- For pre-existing files, establish ownership, references, reproducibility, and an applicable cleanup policy before removing or moving them. Age, a large size, an ignored path, or names such as `tmp`, `cache`, and `old` are not sufficient evidence. Ask about the specific unresolved deletion rather than blocking ordinary task-owned cleanup.
- Before deletion, inspect the exact targets and resolve their real locations, including symlinks. Keep operations scoped to confirmed disposable paths. Never use repository-wide resets/cleans, broad recursive globs, global cache purges, or container/volume pruning as a shortcut for this task's cleanup.
- Do not delete source data, checkpoints, user edits, shared caches, container volumes, published outputs, or evidence referenced by other work merely to make space. Use documented tool cleanup only within its confirmed scope and retention rules.
- When authorized to reorganize durable files, update readers, imports, links, configuration, and regeneration commands with the move. Verify references and consumers before removing the old copy. Do not make unrelated historical reorganization a prerequisite for delivering the current task.

## Finish With a Small, Usable Result

- Confirm deliverables are in their intended homes, the latest version and its readiness are explicit, current-use links resolve correctly, and no task-owned disposable copies remain without a concrete reason.
- For storage-heavy work or an explicit cleanup request, compare scoped before/after measurements when available. Distinguish measured reclaimed space from estimated or merely moved bytes; account for retained archives and caches.
- Summarize useful outputs, meaningful cleanup, and anything deliberately retained or blocked in the existing completion response. Do not create another report solely to announce cleanup.

**Done when:** the requested result is usable, the latest version and its readiness are unambiguous, each retained output has a clear home and purpose, temporary work is cleaned up or explicitly needed, and storage claims are supported by measurements at the stated scope.
