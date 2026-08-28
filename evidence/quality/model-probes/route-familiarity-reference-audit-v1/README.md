# Route-familiarity reference audit v1

This directory is a deterministic, zero-inference preparation package for all
145 retained rows in the frozen route-familiarity presentation. It performs no
sampling, labeling, adjudication, model call, or network call. Historical route
cells are local exposure strata only; they are not truth labels, isolation
evidence, generalization evidence, or memorization evidence.

## Artifacts

- `OUTBOUND-AUDIT-QUEUE.json` preserves the source presentation byte values and
  order. Each item has exactly `neutral_id`, `category`, `profile`, `source`,
  `target`, `bounded_fixed_context`, and an unfilled `response: null` slot. It
  contains no local binding or reference truth.
- `LOCAL-BINDING-REGISTRY.json` is local-only. It binds each neutral ID and
  presentation ordinal to the retained source-registry row, local provenance,
  byte-exact content hashes, and neutral historical route cell.
- `REFERENCE-SCHEMA.json` is an unpopulated Draft 2020-12 schema for completed
  reference responses. It binds the exact queue hash and all 145 neutral IDs in
  frozen order. The only labels are `CLEAN`, `SURFACE_VISIBLE_DEFECT`,
  `CONTEXT_DEPENDENT_DEFECT`, and `UNRESOLVED`.
- `BUILD-REPORT.json` records frozen inputs, counts, zero-call state, gates, and
  hashes of the three core artifacts.
- `EXPERIMENT.json` pins the build report and records the later workflow
  boundary. It contains no result or reference label.
- `build.mjs`, `test-builder.mjs`, and `verify.mjs` build, mutation-test, and
  independently check the package.

The outbound queue must never be combined with the local registry before or
during any later model-facing inference. A completed reference file must be
kept sealed from every later inference prompt and model-facing input. Local
joining by `neutral_id` occurs only after the relevant audit or inference is
complete.

## Deterministic rebuild and verification

Reproduction requires Node 22.x and Ajv 8 with `ajv/dist/2020` resolvable by
Node. This package was verified with Node 22.x and the system-resolved Ajv
8.17.1. Ajv is not pinned or recorded in generated JSON; patch-level drift
within major 8 is an accepted reproducibility limitation. Install Ajv 8 in the
execution environment before running the schema-validation tests and gate.

Run from the repository root:

```bash
node evidence/quality/model-probes/route-familiarity-reference-audit-v1/build.mjs
node evidence/quality/model-probes/route-familiarity-reference-audit-v1/test-builder.mjs
node evidence/quality/model-probes/route-familiarity-reference-audit-v1/verify.mjs
```

The verifier rebuilds all generated JSON into a uniquely named temporary
directory, compares every file byte-for-byte, checks frozen input and output
hashes, independently rejoins the source presentation and retained registry,
scans the outbound object recursively for forbidden identity/provenance/truth
material, and verifies the executor fixture baseline.

The schema is intentionally fail closed:

- every response requires a concise evidence statement containing at least one
  non-whitespace character;
- `CLEAN` rejects defect atoms, source-evidence hashes, and limitations;
- `SURFACE_VISIBLE_DEFECT` requires at least one defect atom and rejects
  source-evidence hashes and limitations;
- `CONTEXT_DEPENDENT_DEFECT` requires at least one defect atom and at least one
  source-evidence hash, and rejects limitations;
- `UNRESOLVED` requires a limitations statement containing at least one
  non-whitespace character;
- unknown labels, fields, queue hashes, neutral IDs, row orders, and row counts
  are rejected by the schema.

This package does not itself populate or validate a completed reference. Any
later reference collection, sealing, scoring, or inference is a separate task.
