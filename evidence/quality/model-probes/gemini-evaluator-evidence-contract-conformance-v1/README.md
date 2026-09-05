# Gemini evaluator evidence-contract conformance v1

This frozen package measures **serialization conformance only**: whether candidate `target_span` and evidence strings are exact substrings of the supplied fields. It is reference-free and non-scored. It contains no correctness reference or adjudication and must not be used to claim translation-review effectiveness, model quality, recall, precision, correctness, or generalization.

## Frozen design

Exactly 16 newly authored synthetic EN→ZH pairs are used in fixed `EC-I001`…`EC-I016` order. Each has an obvious surface mismatch. Author-owned context is explicitly dedicated under CC0 1.0 in `EXPERIMENT.json` and `CONTEXT-SOURCE.json`.

The five registered single-call cells, in mandatory order, are:

1. `baseline-p0-s0-a`
2. `schema-p0-s2-a`
3. `prompt-p1-s0-a`
4. `combined-p1-s2-a`
5. `context-p0-s0-c`

The first four form the complete 2×2 prompt/schema factorial without context. The fifth is the P0/S0 context comparison. Frozen UTF-8 request sizes are 5,841, 6,296, 6,491, 6,958, and 34,794 bytes in that order: the A-shape requests are bounded to 4,096–12,288 bytes and the context request to 25,600–40,960 bytes. Each cell is one descriptive observation. All cells are single unreplicated samples under unpinned decoding. This pilot can show only large or deterministic serialization differences; it cannot establish causality or effectiveness, and it does not authorize replication.

## Zero-call build and checks

```bash
node freezer.mjs
node build-manifest.mjs
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs       # expected before task-owned gates: NO_GO_REQUIRED_GATES, NO_RUN, 0/0
node post-run.mjs        # expected before execution: NO_RUN, 0/0
```

Only the task owner may create the two gates `PACKAGE_REVIEW.json` and `EXECUTION_AUTHORIZATION.json`. Package code only reads them and cannot write task gates. No route qualification is claimed or imported.

## Production execution (not part of build/freeze)

After both task-owned gates exist, invoke exactly one registered cell per process:

```bash
node run.mjs --cell baseline-p0-s0-a
```

Proceed in the registered order. `MAX_ATTEMPTS=1`; five agy processes and five inferences are the absolute ceiling, with no retries or sixth process. Process, envelope, or schema failure stops later cells. Exact-substring membership failure and zero candidates are measured outcomes and do not stop later cells. A zero-candidate rate is null—never pass or failure—and cannot trigger an interpretation. Context comparison uses source/target-only evidence membership. The explanatory-prose proxy is split by membership validity; because valid quotations can contain sentence-final punctuation, its unsplit total is only an upper bound. Every interpretation includes supporting rates/counts and the universal single-call/unpinned-decoding caveat. `node post-run.mjs --write` deterministically writes the descriptive result after execution.

Dynamic `execution/` captures, ledger, RAW files, and `RESULT.json` are excluded from the static manifest. Frozen requests and contracts are included.
