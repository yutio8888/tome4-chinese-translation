# Prospective context-defect expansion v1

This directory freezes a zero-inference, target-bound candidate package for future context-defect research. It reconstructs the complete 1,396-row v4 source-only base, reapplies the v4 eligibility, exposure, locator, and component/content-deduplication rules, removes the 120 v4 presentations, applies the corrected source-focused case-control overlay, and then scans every JSON string leaf in four hash-pinned actual prior model-facing context inputs.

The case-control overlay reduces the v4 complement from 536 to 535 rows. The prior-context screen then excludes 96 complete-source exposures and retains all 439 remaining rows from 34 tasks. The source-only cells are 425 Narrative/dialogue (233 dialogue and 192 narrative), 6 mechanics, 0 UI, 0 runtime-log, and 8 runtime-unknown. UI and runtime-log availability are machine-readable shortfalls; the builder does not pad or relax the frozen rules.

## Phase boundary

Source eligibility, exclusion, ordering, category/profile assignment, and fixed public-source evidence are frozen before target fields are read. The target join then verifies the canonical membership, production commit contract, and all 58 terminal input fingerprints. No model or network call is made.

The case-control overlay excludes a complete source containing at least 12 Unicode code points when the frozen registry proves a strict-longer structured source leaf, a structured exact pair, a source-only exact alias, or a confirmed tracked-input RAW source record. One row qualifies and two rows retain weak evidence. All applicable short-source signal classes are recorded independently; target-only exact aliases remain weak.

The independent prior-context overlay hash-pins `INPUT-B.json` plus `CONTEXT-QUEUE-1.json` through `CONTEXT-QUEUE-3.json`. It records every exact or strict-longer string-leaf match with a workspace-relative logical path and RFC6901 pointer. The 96 qualifying exclusions cover 29 tasks (83 dialogue, 8 narrative, 3 mechanics, and 2 runtime-log rows); three short-source matches remain as weak familiarity controls. Current targets never participate in source eligibility.

## Artifacts

- `SOURCE-EXCLUSION-REGISTRY.json` freezes the 120 identity/content exclusions, the independent 14-source four-route subset proof, the corrected case-control overlay, and all 96 prior-context exclusions plus three short familiarity controls with complete match provenance.
- `SOURCE-EVIDENCE-POOL.json` stores hash-bound fixed-source packets separately from target and canonical identity data.
- `IDENTITY-TARGET-BINDING-REGISTRY.json` is the internal provenance and exact target-binding registry. It is not model-facing.
- `FUTURE-MODEL-CANDIDATES.json` is the sanitized future model-facing presentation. It uses new neutral item IDs and contains only component/category/profile, source, target, and fixed context.
- `BUILD-REPORT.json` records measured counts, shortfalls, frozen input hashes, generated artifact hashes, and zero-inference gates.
- `EXPERIMENT.json` freezes the experiment identity and phase boundary.

No artifact contains local absolute paths. The sanitized presentation contains no task/revision or canonical IDs, terminal-input paths, provider/model provenance, truth labels, defect atoms, adjudication conclusions, or prior audit IDs.

## Rebuild and verification

Use the three local source roots only at runtime; do not persist them in artifacts:

```bash
node build.mjs --production-repo <production-repo> --engine-repo <engine-repo> --dlc-root <dlc-root>
node test-builder.mjs
node verify.mjs --production-repo <production-repo> --engine-repo <engine-repo> --dlc-root <dlc-root>
```

The verifier rebuilds all generated JSON files byte-for-byte in a temporary directory, rechecks schemas, hashes, uniqueness, exclusion coverage, the 14-within-120 relation, target/source bindings, source artifact hashes and packet limits, sanitized leakage rules, zero call counts, and the frozen executor fixture hash. Independently of the build report, it rereads and hash-checks all four prior context inputs, scans their string leaves, validates all 96 exclusion and three weak provenance records, and proves that no final source of at least 12 Unicode code points has an exact or strict-longer overlap.

## Scope and limitation

This is a prospective candidate package, not a truth set and not a translation adjudication. It does not copy sealed reference or final-adjudication content and makes no claim about deleted, untracked, external, or provider-side historical exposure beyond the hash-bound registries it consumes. Independent normal and senior code review are required before any inference.
