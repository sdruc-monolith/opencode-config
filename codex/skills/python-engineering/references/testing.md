# Python Testing

Use the project's test runner, environment, fixtures, and plugins. The examples below describe pytest techniques when pytest is already in use; they do not require converting another test suite.

## Choose Evidence That Can Disagree With the Code

- Assert observable behavior using explicit expected values, a worked example, an independently trusted oracle, or a domain invariant. Do not compute expected output using the implementation's own transformation.
- For bug fixes, establish a failure on the reported symptom before changing behavior where feasible. For uncertain refactors, characterize the relevant existing contract first.
- Prefer one behavioral slice at a time. A test can have several assertions that jointly describe one outcome, such as schema, values, and exit status.
- Use unit tests for focused domain logic and integration tests where engine, storage, serialization, or transaction semantics are what could fail.
- A persisted dataset, emitted message, or command output can be the public interface. Directly inspecting that output is appropriate; there is no need to invent a query API just for testing.

## Fixtures and Isolation

- Use `tmp_path` for real filesystem inputs/outputs and scratch files; close handles and connections so cleanup works reliably.
- Keep fixtures small, deterministic, and readable. Parametrize meaningful cases such as empty input, nullable keys, duplicate keys, unmatched rows, and precision boundaries rather than enumerating every imaginable input.
- Use `monkeypatch` for process environment and narrow unavoidable ambient state. Inject clocks, random sources, and external clients when the code already has a suitable boundary.
- Test through a real local engine or temporary database when its semantics matter. A mock dataframe chain cannot validate join behavior or lazy execution.
- Mock genuinely external boundaries when necessary; verify their adapters separately when possible. Avoid mocks that just restate internal call order. Interaction assertions are useful when the interaction itself is the contract, such as publishing exactly one batch.
- Avoid leaking global state, live network dependencies, persistent data, or fixture state between tests. Reuse the repository's established async runner and resource fixtures for async code.

## Data Assertions

- Assert schema as well as values where schema is contractual: names, types, nullability, precision/scale, and relevant metadata.
- Decide whether ordering is meaningful. For unordered results, compare multisets or canonicalized rows using a stable comparison strategy that retains duplicate multiplicity. A set comparison can hide duplicate-row bugs.
- Use engine-provided dataframe assertions where appropriate, with explicit dtype, ordering, and numerical tolerance choices. Do not disable type checks merely to make a migration pass.
- Treat floating-point tolerance as part of the requirement. Use exact decimal expectations for exact financial quantities; distinguish null, NaN, and infinity deliberately.
- Include timestamp unit/timezone cases and decimal round trips when those types cross a changed boundary.
- For joins, assert the expected records, unmatched behavior, cardinality, and duplicate handling. Totals alone can pass when individual rows are wrong.
- For output writers, read back the actual produced files/table. Assert the promised schema, values, and publication state, including an empty result when relevant.

## Worked Example

Suppose a daily total groups events by customer and UTC date, summing decimal amounts. A small fixture could contain:

| Customer | Timestamp | Amount |
| --- | --- | --- |
| A | 2026-01-01T23:30:00Z | 1.20 |
| A | 2026-01-02T00:30:00+01:00 | 2.30 |
| B | 2026-01-02T00:00:00Z | 4.00 |

The independently worked expected rows are A / 2026-01-01 / 3.50 and B / 2026-01-02 / 4.00. Assert the output uses the agreed date and decimal schema. Reading the stored output also exercises timezone normalization and serialization.

Add a separate case for a rejected null key or accepted null key according to the contract. For an enrichment step, duplicate a supposedly unique dimension key and assert the agreed rejection rather than accepting inflated totals.

## Property and Differential Tests

- Use property-based testing when there is a strong invariant and ordinary examples miss combinations. Reuse Hypothesis if present; justify adding it otherwise.
- Useful conditional properties include partitioned versus whole-input equivalence for an associative transformation, input permutation invariance for unordered aggregation, and repeated-batch idempotency for a replay-safe sink.
- State the preconditions: floating-point summation, order-sensitive rules, and windowed state can invalidate apparently obvious properties.
- During an engine migration, compare old and new outputs on representative fixtures with agreed normalization. Add independent expected results for important semantics so a shared or pre-existing bug does not become the oracle.
- Failure-injection tests should target a real recovery boundary, such as output publication versus checkpoint update, and demonstrate the resulting consumer-visible state.

## Completion Evidence

Run focused tests during implementation, then the required checks for the affected scope. Use existing coverage policy rather than imposing a universal threshold. Report blocked integration or runtime checks separately; passing unit tests does not substitute for unavailable engine or storage evidence.
