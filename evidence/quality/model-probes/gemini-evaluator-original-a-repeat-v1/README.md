# Gemini original Discovery A request repeat v1

Fresh zero-call package for three ordered, reference-free repetitions of the exact original execution-v5 Discovery A request.

## Frozen identity

- request: `model-facing/requests/original-a.txt`
- request SHA-256: `364900148df5fd7649f9c932a00e2b896c5f503d03f6a2545e3c0116591c04f9` (7,049 UTF-8 bytes)
- prompt SHA-256: `c2eee0bdd41aaaf2f74ef624e9e73198da431319344997d42e9066e8d948b920`
- schema SHA-256: `d9485a07b55238c783989650ad9ec9e886f279c1779ae5697985a3dd860ce0d4`
- order: `original-a-repeat-1`, `original-a-repeat-2`, `original-a-repeat-3`

The package contains no sealed reference, predecessor ledger/capture/RAW artifact, or dynamically generated predecessor output. All three cells use the same request path and schema bytes. The full predecessor is fail-closed bound by the canonical 80-file tree SHA-256 above. Exact, unnormalized substring membership is a descriptive metric and does not invalidate a structurally valid response. Field and evidence lengths use JavaScript UTF-16 `String.length`, matching v5. Zero-candidate runs continue but are uninformative.

## Zero-call checks

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs
node post-run.mjs
```

Before the task-owned gates exist, preflight must be `NO_GO_REQUIRED_GATES`, `NO_RUN`, with `0/0` process/inference counts. This package only reads `PACKAGE_REVIEW.json` and `EXECUTION_AUTHORIZATION.json`; it cannot create or modify task gates.

## Authorized execution (not part of package construction)

Only after both gates validate, run each command once and in this exact order:

```bash
node run.mjs --cell original-a-repeat-1
node run.mjs --cell original-a-repeat-2
node run.mjs --cell original-a-repeat-3
node post-run.mjs --write
```

Do not invoke a later cell after route drift, ledger error, process/network failure, malformed envelope, or schema-invalid output. Do continue after structurally valid membership failure or zero candidates. Every START consumes the cell's sole attempt and one unit of the 3/3 process/inference budget. `RESULT.json` and `execution/` are generated artifacts excluded from the static manifest.

The result is descriptive contract behavior only. Three runs have low power: equal outcomes do not establish determinism or exclude stochastic/sample-dependent behavior. Calls may share provider caching, infrastructure, or hidden state, so statistical independence is not claimed; RESULT records deterministic ledger timing gaps for audit context. Route attestation is local-tier only (pinned executable plus requested argv model), not provider-side served-model proof.

The package owns only package files and generated execution artifacts. Task lifecycle, review-directory cleanup, and gate creation remain orchestrator-owned; package commands never mutate them. No separate network-call count is claimed because START is the authoritative process/inference accounting event. Results must not be presented as correctness, precision, recall, effectiveness, model-quality, or generalization evidence.
