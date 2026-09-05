# Gemini context counterexample reviewer V5

Status: **`NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED`** with static integrity PASS. ROUND-0001 and every ROUND-0002 audit input/output remain frozen. User-authorized replacement/release implementation has produced only canonical `PENDING-RELEASE.json`, a deterministic release fixture, code/tests, and a full-coverage candidate; the real `rounds/ROUND-0002/RELEASE.json` and completed-state mutation remain absent pending independent normal Codex and senior Gemini 3.7 Flash review plus a combined gate. No Opus call is permitted.

ROUND-0002 context-call allowance is exactly `1`, with `started=1` and `remaining=0`; no further context call is authorized. The two release decisions are `V4-D-D05` (`NOT_CLEAN`, dialogue reserve rank 6) and `V4-C-D06` (`OUT_OF_SCOPE_NON_PROSE`, replacement-eligible, dialogue reserve rank 7), with no skipped reserves. `ROUND-INDEX.json.completed_rounds` remains `1` until the future atomic materializer passes the dual-review gate.

Expected completed hashes are release `a42e2b8b4e497a26a4936558ffdf5816b45dd49b3b0e31d3eb42f969ddd0fd70`, active frame `e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3`, lineage `03d2c842fba9ddf95905c16c5170e2c23aa182680d520a3c3a16848f37cbb3d6`, reserve state `4fab5ea380b0e20b8e6dc2ba0ffc98125e126791fd7c283e0e5608119c0725e0`, round index `089a8b17dc7a21ba4f6178b77e1247bf89d420c3801ed2d9a8ee9042d6f8a375`, release state `30ad2ecb49626a23bed45d8a96a79664d5569ca1d1f85f6df77d23c7c3b9c334`, and experiment `a46888e5b330190da0a29b156248cc35e2dca73d9603cc8185551298617c5f56`. On a temporary completed fixture, the actual public `checkReplay` and `runPreflight` paths were each invoked twice. Both observed replay results were byte-identical PASS with `completed_rounds=2`; both observed preflight results were exactly `NO_GO_ROUND_0003_AUDIT_NOT_AUTHORIZED`, static integrity PASS, with 64 active rows, 12 lineage edges, 299 reserves (226 dialogue/73 narrative), 12 banned and 12 consumed. These are observed outputs, not helper-declared flags.

The prior `fba2…` candidate review is immutable non-gating history. Normal Codex reviewer `3d463a0b-96c2-47dc-a26f-dc281e9306b1` returned `CHANGES_REQUIRED` with finding `R2-RELEASE-COMPLETED-REPLAY-001`. Senior Gemini 3.7 Flash attempts `2b8cf9e9-77ab-4440-ac8e-c0bada5f9fc4` and `be4d5229-9d26-4296-9e6e-80d1e3f0905b` produced substantive PASS assessments but ended with the recorded lifecycle timeout; both are classified `NON_GATING_LIFECYCLE_ERROR` and cannot satisfy a gate. No combined gate exists.

## Current frozen state

- ROUND-0001 release SHA-256: `bf37e1fc2f1015d6c86e0666154338df591d2f556a489b25ba775ccf7ce66119`
- Current active-frame SHA-256: `c632d77064d1d80cd950de263ab3b3970820bed4102cb120900835ae279d1a85`
- Current lineage SHA-256: `0fc604bc50220f8accd584f63d7aa5e560d88a2c8a23e43ebb94af3328b9ce7d`
- ROUND-0002 surface queue SHA-256: `e8947540ff6b430fc8b69202abcb039dc34bbc996bb1fc241f671e280cd6a866`
- ROUND-0002 surface view SHA-256: `5858861e071b7229cb3ca2ae6f3c6fd0ed972433dab2490c1a848bf4a2788030`
- Queue size: exactly 10 current ROUND-0001 replacement heads, in current active-frame slot order.

The queue binds the predecessor release, current active frame, scoped authorization, neutral IDs, current revision IDs and row identities. The self-contained view was derived from the pinned 30,308-row inventory and fixed source commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`. It exposes source, target and cryptographic revision provenance, but no prior verdict/evidence, rejected revision, reserve/lineage, reviewer/model, reference or adjudication data.

ROUND-0002 context queue, fixed-commit source anchors, and self-contained view contain exactly the ordered nine-item surface-pass subset. `V4-C-D06` is preserved as `OUT_OF_SCOPE_NON_PROSE` and excluded. The queue and anchors retain lineage/reserve hashes as non-payload integrity bindings; the auditor-facing view deliberately omits both fields. Its recursive leakage guard rejects banned keys and metadata tokens for lineage/reserve, verdict/evidence, rejected/rank, reviewer/model, reference and adjudication data.

The view preserves each exact raw source separately and contains the complete runtime `_t` construct, including a level-matched Lua long-bracket closing delimiter (`]]`, `]=]`, and higher levels) and an optional parenthesized `_t(...)` boundary. It also contains three-line neighborhoods and absolute UTF-8 byte/line coordinates for the nine required source files. The two fixed EOF constructs are `V4-C-N01` at lines `20–31`, bytes `[776,1791)`, and `V4-D-N12` at lines `20–27`, bytes `[776,1176)`; their `after` blocks are valid empty file-end windows.

Candidate coverage is self-describing: it recursively hashes all regular files under the exact task and V5 package roots, in bytewise path order, excluding only the recorded mutable state, self-reference, and future normal/senior/gate paths. Each recipe row is `path + NUL + lowercase SHA-256 + LF`; the candidate reference is the SHA-256 of their concatenation. The archived `27a5…` manifest and its normal/senior `CHANGES_REQUIRED` records remain included history, while adding future review/gate records cannot change the repaired candidate identity.

The archived `724863…` candidate additionally preserves its normal `CHANGES_REQUIRED` and senior `PASS` history; no gate exists for that candidate. Construct recognition now requires `_t` to have a strict identifier left boundary: an ASCII or Unicode letter/number, or underscore, immediately to its left makes the occurrence ineligible. Invalid substrings such as `not_t` and `object_t` are skipped while the extractor continues searching for valid occurrences; exact valid-source cardinality remains one.

Live context-review lifecycle is explicit and fail-closed: no reviews is `PENDING_NORMAL_AND_SENIOR`; one canonical PASS is `PENDING_OTHER_REVIEW`; any canonical `CHANGES_REQUIRED` is `NO_GO_REPAIR_REQUIRED`; dual PASS without a gate is `DUAL_PASS_GATE_REQUIRED`; and only dual PASS plus its bound gate produces `GO_ROUND_0002_CONTEXT_AUDITOR_CALL_ONLY`. Unexpected gate/partial combinations or malformed records are invalid, not pending.

## Authorization field semantics

The completed ROUND-0001 `EXPERIMENT.json` and `RELEASE-STATE.json` are immutable historical outputs. Their `round_0002_audit_authorized: false` means that completion of ROUND-0001 did not itself authorize a ROUND-0002 auditor call.

Live preflight uses two distinct fields:

- `round_0002_surface_input_authorized: true` means the user authorized Stage A construction and freezing of the two surface-input files.
- `surface_auditor_call_authorized: false` now means the sole authorized call has been consumed and no additional surface call is permitted.

Live preflight intentionally does not reuse `round_0002_audit_authorized` for Stage A input authorization.

## R2 review history and repair disposition

Candidate `a1b7b4e496d35278e8b1bfdb77a0f141c9d4451926bad48bd2876595752aaeca` received normal PASS from `49850012-7f63-4a83-8db6-985d384ca404` and senior `CHANGES_REQUIRED` from `471fcff8-d683-4509-b77e-f24ad837b67d`. The exact old manifest is archived as `ROUND-0002-SURFACE-INPUT-CANDIDATE-A1B7-MANIFEST.json`; both review records are immutable history and no combined PASS gate exists for that candidate.

R2-A identified seven commands that still assumed the pre-release ROUND-0001 state. Their tested disposition is:

- `context-queue-view.mjs --check` now validates frozen ROUND-0001 context bytes against the exact historical frame, then verifies the live completed-ROUND1 plus two-file pending-ROUND2 state and confirms ROUND2 context absence.
- `test-pending-context-input.mjs`, `test-pending-context-results.mjs`, `test-context-results-gate-transition.mjs`, `test-pending-surface-stage.mjs`, `test-zero-call.mjs`, and `test-round-0001-release-candidate.mjs` are maintained compatibility entry points. Each runs its exact historical implementation against the frozen 89-file pre-release pack in a fresh temporary copy.
- The historical release-candidate test therefore retains regression coverage for the `!hasRound2SurfaceInput` path and the ROUND-0001 materialization review gate, even though that path is no longer reachable in the live pending-ROUND2 tree.

The fixture pack is test evidence only. It cannot mutate the live package and is not a release, auditor result, or model result.

## Current checks

Run from the repository root:

```bash
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/generate-round-0002-surface-input.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/round-0002-surface-results.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/round-0002-context-input.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/round-0002-context-results.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/surface-queue-view.mjs --check ROUND-0002
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/context-queue-view.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-0002-surface-input.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-0002-context-input.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-0002-context-results.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/round-0002-release.mjs check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-0002-release.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-lineage.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-surface-queue-view.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-v2-completed-replay.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/replay.mjs --check
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-pending-context-input.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-pending-context-results.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-context-results-gate-transition.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-pending-surface-stage.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-zero-call.mjs
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/test-round-0001-release-candidate.mjs
```

Preflight is intentionally nonzero at the current gate:

```bash
node evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/preflight.mjs
# expected exit 3 and decision NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED
```

## Threat model and scope

The package uses `NON_ADVERSARIAL_REPOSITORY_WORKFLOW`. It detects accidental drift, harness/parser errors, missing/extra/symlink/noncanonical artifacts, stale or inconsistent state, and unauthorized phase advancement. Malicious whole-package rewriting, reviewer-identity forgery and validator rewriting are out of scope. Review records are workflow consistency evidence, not authenticity proofs.

ROUND-0001 evidence and all previous review histories remain immutable. The ROUND-0002 surface/context queue, view, raw responses, records and aggregates are hash-bound in the release fixture. The candidate excludes mutable `STATE`, itself, the three future review/gate records, and four future dispatch/completion receipts. Review hashes are deliberately not embedded in release or completed-state expected hashes, avoiding circularity and fixture/production provenance mismatch. This transition creates no real release, review record, gate, ROUND-0003, model/network call, or Git mutation.

## Incident: invalid harness-generated ROUND2 release reviews

The former canonical ROUND2 normal review, senior review, and combined gate were written by sole-writer executor `6f8e3a5a-8131-4b18-8654-254bde8c51b5` without independent dispatch or lifecycle receipts. Their exact bytes are quarantined under uniquely named `ROUND-0002-RELEASE-INVALID-HARNESS-GENERATED-*` evidence files and are non-gating. Future canonical reviews require orchestrator dispatch and non-errored completion receipts bound to candidate, manifest, reviewer identity, route, response hash, and verdict.

## ROUND-0002 recovered completion evidence

The exact orchestrator-recovered normal response is persisted in the canonical completion receipt with verdict `CHANGES_REQUIRED` and raw SHA-256 `6130b62d2402edd4c2c6d80275172e2460b9cad7641baccf92ea762464e4c484`. The exact senior response is persisted with verdict `PASS` and raw SHA-256 `871917fba6d19024708ddb5da03ba6ef455540167cbee0bceb84c892f2786d9b`; both bind to their canonical dispatch receipt and the frozen candidate. The accompanying review-history records are non-gating. Receipt validation uses the persisted reviewer roles/routes and verifies response-text hashes; completed ROUND2 validation requires the same dispatch, completion, review, and gate evidence. Malicious sole-writer fabrication or out-of-band authenticity remains outside the declared `NON_ADVERSARIAL_REPOSITORY_WORKFLOW` threat model.
