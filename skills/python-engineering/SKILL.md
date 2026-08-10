---
name: python-engineering
description: Python engineering for .py files, pyproject.toml, application architecture, refactoring, code review, and data processing. Use when writing or changing Python code, especially when choosing between object-oriented design, built-ins, pandas, Polars, NumPy, PyArrow, or DuckDB.
---

# Python Engineering

Build maintainable Python systems with pragmatic object-oriented design and workload-appropriate libraries. Inspect the repository before choosing an architecture, dependency, or tool. Treat the existing codebase as a compatibility constraint, not automatically as an architectural authority.

Preserve public APIs, behavior, data contracts, naming vocabulary, and operational tooling. Follow existing patterns when deviation would create local inconsistency, incompatible abstractions, or disproportionate migration cost. Apply this skill to new or substantially changed boundaries where it provides a clear benefit. Refactor existing code only when needed for correctness, maintainability, performance, or testability, and keep the scope proportional to the requested change.

## Extending Existing Code

- Add characterization tests before restructuring unfamiliar or weakly tested behavior.
- Avoid creating competing architectural patterns within one cohesive subsystem.
- Introduce SOLID boundaries at natural seams such as persistence, HTTP, filesystems, queues, clocks, and external services.
- Prefer adapters around legacy code over broad rewrites when compatibility must be preserved.
- Improve touched code when the improvement is low-risk and supports the requested change; avoid unrelated cleanup.
- Introduce DuckDB, pandas, Polars, or another dependency only when its workload benefit exceeds dependency, conversion, and migration costs.
- Preserve the project's package manager, formatter, linter, test runner, supported Python versions, and deployment constraints.
- Explain intentional deviations from established patterns and identify any follow-up migration that remains.

## Architecture

Prefer objects when behavior belongs to state, a lifecycle, or a domain concept:

- Model domain entities and value objects with focused classes.
- Use services for stateful workflows, external resources, or coordinated operations.
- Use `@dataclass` for typed records with light behavior and Pydantic when runtime validation, serialization, or schema generation is required.
- Define explicit interfaces with `Protocol` or abstract base classes when multiple implementations exist or a boundary needs isolation.
- Inject collaborators rather than constructing databases, clients, and repositories deep inside business logic.
- Keep resource ownership explicit with context managers and clear lifecycle methods.
- Prefer composition over inheritance. Use inheritance only for a genuine substitutable relationship.
- Keep classes cohesive and avoid god objects, static-method containers, speculative base classes, and Java-style ceremony.

Small stateless transformations, predicates, adapters, and module-level entry points may remain functions. Do not wrap logic in a class solely to satisfy an object-oriented style preference.

When procedural code mixes state, policy, I/O, and transformation in one function, separate those responsibilities into cohesive domain objects and collaborators. Keep orchestration readable and move behavior close to the data or resource it governs.

## SOLID Principles

Apply SOLID pragmatically at architectural boundaries:

- **Single Responsibility:** Give each class one coherent reason to change. Separate domain policy, persistence, transport, parsing, and presentation when they evolve independently.
- **Open/Closed:** Add behavior through composition, strategies, registries, or interchangeable collaborators when variation is real. Do not build extension frameworks for hypothetical requirements.
- **Liskov Substitution:** Ensure implementations preserve the interface's behavior, accepted inputs, outputs, error semantics, and invariants. Do not use inheritance when subclasses need special-case checks or weaken guarantees.
- **Interface Segregation:** Prefer small, consumer-focused `Protocol` definitions over broad base classes. Define an interface where it is consumed and avoid requiring clients to depend on methods they do not use.
- **Dependency Inversion:** Keep domain logic dependent on abstractions and inject infrastructure such as databases, filesystems, HTTP clients, clocks, and queues. Concrete composition belongs at application entry points.

Use Python's structural typing and first-class callables where they provide the narrowest clear abstraction. Not every collaborator needs an interface, and not every function needs a class. Introduce abstractions when there are multiple implementations, a meaningful test boundary, independent change, or external I/O.

## Data Tool Selection

Do not default to Python loops and nested dictionaries for substantial tabular, analytical, or numerical work. Select tools according to the workload:

| Workload | Preferred tool |
| --- | --- |
| SQL-style joins, filtering, aggregation, window functions, CSV/JSON/Parquet scans, or larger-than-memory analytics | DuckDB |
| General in-memory tabular manipulation and broad ecosystem interoperability | pandas |
| Performance-sensitive dataframe pipelines, parallel execution, or lazy query plans | Polars |
| Dense numerical arrays, linear algebra, and vectorized numerical operations | NumPy |
| Arrow-native interchange, columnar schemas, and Parquet datasets | PyArrow |
| Small collections, simple control flow, or standard protocol implementation | Python built-ins |

Prefer SQL, vectorized expressions, dataframe operations, and bulk APIs over row-by-row Python loops. Push projections and filters into scans or queries, avoid unnecessary materialization, and preserve columnar formats between compatible tools.

Do not load a large dataset into pandas merely because pandas is familiar. Consider DuckDB or Polars when data size, joins, aggregation, memory use, or repeated scans matter. Conversely, do not add a dataframe engine for a tiny one-pass collection operation that is clearer with built-ins.

## Dependency Decisions

Before adding a package:

1. Inspect `pyproject.toml`, lockfiles, imports, supported Python versions, and the project's package manager.
2. Reuse an established dependency when it is suitable.
3. Confirm the package solves a concrete correctness, performance, interoperability, or maintainability need.
4. Add the smallest appropriate runtime or development dependency with the existing package manager.
5. Update the lockfile when the project tracks one.
6. Avoid introducing overlapping dataframe or validation libraries without a clear benefit.

Packages may be added without asking when the benefit is concrete and the change follows project conventions. State the reason in the final summary. Do not claim a package is faster without evidence appropriate to the workload; benchmark representative data when performance drives the decision.

## Implementation Standards

- Use modern type hints and make public boundaries explicit.
- Represent structured data with typed models instead of loosely shaped dictionaries passed across layers.
- Keep domain logic separate from CLI, HTTP, persistence, and dataframe formatting concerns.
- Prefer iterators or streaming APIs when full materialization is unnecessary.
- Avoid repeated dataframe copies, `iterrows()`, `apply(axis=1)`, and Python callbacks in hot paths when vectorized or SQL alternatives exist.
- Use parameterized SQL and keep query construction safe.
- Preserve null, timezone, decimal, categorical, and schema semantics during conversions.
- Handle errors at meaningful boundaries; do not broadly catch exceptions and silently continue.
- Use logging rather than `print` for application diagnostics.
- Keep APIs narrow and names domain-specific.
- Optimize after identifying the relevant workload, but avoid obviously inefficient algorithms and data movement from the outset.

## Verification

- Test behavior through public interfaces rather than private implementation details.
- Include unit tests for domain objects and integration tests for database, file-format, and dataframe boundaries.
- Use realistic fixtures for nulls, duplicate keys, type coercion, empty inputs, and large-enough data to exercise the selected execution path.
- Run the project's formatter, linter, type checker, and tests using its existing commands.
- For performance changes, compare representative before-and-after timing and memory use when feasible.

## Review Checklist

When reviewing Python code, check:

- Whether domain behavior and state have clear object ownership.
- Whether functions have become procedural collections of unrelated responsibilities.
- Whether classes are cohesive rather than decorative wrappers.
- Whether SOLID boundaries reduce coupling without creating speculative abstractions or excessive indirection.
- Whether built-in loops duplicate operations better expressed by DuckDB, pandas, Polars, NumPy, PyArrow, or another established package already in the project.
- Whether conversions and materialization create avoidable CPU or memory costs.
- Whether a new dependency is justified and correctly declared.
- Whether typing, tests, resource lifecycles, and failure behavior cover the changed boundary.
