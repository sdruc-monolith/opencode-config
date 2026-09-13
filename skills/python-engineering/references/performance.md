# Python Pipeline Performance

Measure the workload that motivates the change. A faster function on tiny data does not establish a faster pipeline or lower peak memory.

## Establish a Comparable Baseline

- State the symptom and target: elapsed time, throughput, peak resident memory, spill volume, or another operational requirement.
- Record code revision, Python and dependency versions, input identity/size, cardinality and skew, hardware, thread limits, storage, and relevant configuration.
- Keep inputs and environment comparable between baseline and candidate. Measure the same operation, including I/O and conversions when they are part of the claimed improvement.
- Check correctness first: schema, values, key/cardinality invariants, and required ordering. Discard apparent speedups caused by dropping data or changing semantics.
- Separate cold-start, import, and cold-cache costs from warm execution when relevant. Repeat enough to expose noise and report the measurement method and observed variation.

## Find the Cost

- Identify whether the bottleneck is Python CPU, native engine computation, input scans, network, serialization, intermediate materialization, or output writes.
- Use an existing profiler, query plan/explain facility, or focused timing harness. Python profiling may not attribute native engine work in useful detail.
- Inspect scan projections and filters, join order/cardinality, sort operations, repeated scans, callbacks, and collection points in lazy plans.
- Measure memory with a tool that captures the resources in question. `tracemalloc` tracks Python allocations and may miss substantial native engine/array allocations; process/container measurements have different scopes, especially with worker processes.
- Watch for oversubscription when process pools, dataframe engines, and numerical libraries each create threads. Reuse deployment limits rather than tuning only for the development laptop.

## Improve the Execution Path

- Push filters and column projection toward the source when semantics permit.
- Keep compatible operations in SQL or dataframe expressions; minimize Python row callbacks and per-row network/storage calls.
- Avoid repeated conversion between Python objects, pandas, Arrow, and other engines. Include conversion costs in comparisons.
- Stream or batch where the operation supports it. Chunking a global join, sort, or aggregation is not automatically semantically equivalent or memory-bounded.
- Validate operator-specific spill/streaming behavior on the deployed engine version. Account for temporary disk capacity and cleanup, not only configured memory limits.
- Use partition pruning and an appropriate output file size/partition scheme. Excessive small files or high-cardinality partitions can shift cost to metadata and scans.
- Preserve deterministic tie-breaking, null/NaN policies, timestamp interpretation, decimal precision, and duplicate multiplicity while optimizing.

## Validate an Engine Migration

1. Establish the current schema and behavior with representative fixtures and important independent expected results.
2. Exercise the candidate on the same data; compare outputs using the contract's ordering and type semantics.
3. Benchmark representative sizes and distributions, including skew and the intended larger-than-memory path when required.
4. Include scan, conversion, materialization, write, and read-back costs that consumers actually pay.
5. Compare resource usage against deployment constraints and identify dependency, operational, and maintenance costs.

Favor a migration only when the concrete benefit justifies these costs. A local query rewrite or improved existing-engine plan may solve the problem with less disruption.

## Report

Summarize baseline and candidate, workload, methodology, correctness evidence, elapsed time/resource results, and limitations. Avoid brittle timing thresholds in ordinary unit tests; use the repository's benchmark process or a repeatable experiment. If representative data or instrumentation is unavailable, state that the performance claim remains unverified.
