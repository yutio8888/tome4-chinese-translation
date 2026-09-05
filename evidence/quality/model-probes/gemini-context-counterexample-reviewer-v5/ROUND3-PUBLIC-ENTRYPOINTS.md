# ROUND3 public entrypoints

With `rounds/ROUND-0003/` present, the canonical phase-aware commands are:

```bash
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/public-replay.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/public-preflight.mjs
```

They delegate to the dedicated ROUND3 implementation and report `completed_rounds: 2` plus `NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED`.

The legacy `replay.mjs` and `preflight.mjs` are byte-frozen ROUND1/ROUND2 compatibility entrypoints. They are not rewritten because their completed-ROUND2 evidence hashes include those exact bytes; direct use against the live ROUND3 tree fails closed on the frozen-contract mismatch. The wrappers are the public commands for pending ROUND3.
