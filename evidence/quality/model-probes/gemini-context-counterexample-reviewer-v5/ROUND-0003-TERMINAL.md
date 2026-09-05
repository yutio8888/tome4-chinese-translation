# ROUND-0003 terminal entrypoints

The current ROUND-0003 state is terminal audit evidence: both active replacement heads passed surface and context review, no rejection/replacement/release was created, and neither ROUND-0004 nor formal experiment inference is authorized. Terminalization implementation remains pending independent normal and senior review until an exact dual-PASS lifecycle and combined gate validate.

Use these current phase-aware commands:

```bash
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/public-terminal-replay.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/public-terminal-preflight.mjs
```

Replay accepts only three lifecycle phases at the seven exact canonical paths: all absent; both dispatch receipts with all completion/review/gate files absent; or both dispatch receipts plus both completion receipts, both PASS reviews, and the combined gate. Any partial phase, malformed or noncanonical file, wrong candidate/manifest hash/agent/role/route/verdict, extra file, non-regular file, or symlink fails closed. In the current no-receipt phase, preflight reports `NO_GO_ROUND_0003_TERMINALIZATION_REVIEW_REQUIRED` without authorizing release or ROUND-0004.

`README.md`, `ROUND3-PUBLIC-ENTRYPOINTS.md`, `public-replay.mjs`, and `public-preflight.mjs` are immutable historical compatibility entrypoints covered by the frozen 169/191-file candidates. They intentionally continue to describe or route older ROUND-0003 surface/context phases and must not be used as current terminal entrypoints.

Coverage output compares `actual_files_in_scanned_roots` with `authorized_existing_files_in_scanned_roots`; both count existing paths under the same task/evidence roots. `authorized_path_universe` additionally includes manifest-listed external files and optional future lifecycle paths, while `optional_lifecycle_absent` reports how many lifecycle paths are currently absent.
