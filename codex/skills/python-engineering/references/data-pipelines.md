# Data Pipelines

Establish the data contract before choosing an implementation. Inspect representative schemas, producer/consumer code, and existing fixtures; avoid inferring a contract from a few sample rows alone.

## Define the Contract

Record the decisions relevant to the change:

| Concern | Questions to resolve |
| --- | --- |
| Grain | What does one row represent? At which stages does that change? |
| Schema | Required/optional columns, types, nullability, units, decimal precision/scale, timezone interpretation? |
| Keys | Which keys are unique? What do null keys and duplicates mean? |
| Joins | One-to-one, many-to-one, or intentionally many-to-many? What happens to unmatched rows? |
| Ordering | Is order a contract, or are outputs unordered? How are ties resolved when selecting first/latest? |
| Quality | Reject the batch, quarantine records, or apply documented coercion? How are losses accounted for? |
| Output | File/table/dataset format, partition scheme, consumer expectations, and publication boundary? |
| Execution | Expected volume, skew, memory/storage limits, batch or incremental mode? |
| Recovery | Retry identity, partial-output visibility, checkpoint timing, and rerun/backfill behavior? |

Resolve ambiguous business policies rather than silently using engine defaults. Empty inputs must have deliberate behavior, including output schema where an empty dataset is expected.

## Preserve Grain and Cardinality

- Validate uniqueness on the side that must be unique before a join. Use built-in cardinality validation when available, or an explicit grouped-key check with a clear error.
- For a many-to-one left join, output row count should equal input row count when the contract preserves every left row. Verify values as well: row counts alone can hide incorrect matches.
- Do not repair unexpected multiplication with a final `DISTINCT` or arbitrary deduplication. Identify the violated input contract or define the intended aggregation/selection rule.
- A latest-record rule needs a deterministic tie-breaker and a policy for missing timestamps. Selecting whichever record an engine happens to return is not deterministic.
- Treat null-key joins explicitly. For example, pandas can match null keys while SQL equality joins normally do not. Preserve the intended behavior when moving between them.
- Keep row-loss accounting meaningful: input, accepted, rejected, unmatched, and output counts describe different stages and need not all be equal.

## Schema Evolution and Interchange

- Separate input parsing/validation from domain transformation and output publication at useful boundaries.
- Define handling for added, missing, renamed, and retyped columns. Preserve compatible consumers during migrations; distinguish absent columns from present-but-null values.
- Validate timestamp units and timezone interpretation, decimal precision and rounding, null versus NaN, categorical encodings, and integer widths across format/engine boundaries.
- Preserve columnar representations through compatible stages. Account for copies or lossy conversions rather than assuming Arrow interchange is always zero-copy.
- Test round trips through the actual storage format. CSV inference and a Parquet/Arrow schema do not provide equivalent guarantees.
- Use parameterized values in SQL. Validate or quote dynamic identifiers through supported APIs; value parameters do not substitute for table or column names.

## Incremental Processing and Recovery

- Define the unit of idempotency: input batch ID, source offset, object version, partition, or business key. Identify the sink operation that makes repeats safe.
- Advance checkpoints only after the corresponding output is durably published. If sink and checkpoint cannot commit together, design replay/deduplication to cover the crash window.
- Choose event time versus ingestion time deliberately. Specify watermark inclusivity, overlap windows, late-arriving updates, and deterministic conflict resolution when relevant.
- Keep backfill boundaries and partition replacement explicit. Test a repeated batch and an overlapping batch, not just two disjoint successful runs.
- Use transaction or staging-and-publication semantics supported by the actual sink. A local filesystem rename, database transaction, and object-store manifest have different guarantees; multi-object writes are not automatically atomic.
- Readers should observe the intended complete output version. Test interruption before publication and after publication but before checkpoint advancement when those failure windows matter.
- Own and clean up task-created temporary resources. Avoid deleting old partitions or incomplete outputs without a clear ownership and recovery policy.

## Example Implementation Slices

For a pipeline enriching events from a customer dimension:

1. **Enrich and persist a small valid batch:** input fixtures pass through the real transform and output writer; assert the output schema and independently calculated values.
2. **Enforce the input contract:** reject duplicate dimension keys, apply the agreed null/unmatched policy, and verify empty input behavior.
3. **Make publication replay-safe:** rerun the same batch and inject failure around the relevant publication/checkpoint boundary.
4. **Validate the required scale:** exercise representative cardinality and skew, inspect execution, and measure resource use.

Include only slices required by the task. Scale and recovery work need not become new frameworks when an existing system already provides the guarantees.
