# Gemini context-counterexample REVIEWER V5 execution v2

## Status

This directory is the final P0 contracts-only repair candidate. P0 is written, not implemented. It contains no executable package, child creation, semantic mutation, qualification capture, frozen formal request, RAW, score/result, provider/model/network output, or experimental call. P1–P3 are future zero-call phases. Their only positive terminal is `ZERO_CALL_IMPLEMENTATION_COMPLETE`; real mutation, qualification, discovery, confirmation, and result activity requires separate downstream authorization and gates.

V5 and execution-v1 remain byte-immutable. Execution-v1 candidate `71a15acb0c2d4dcb7b18727dd84cbe28b8068694d8e4258ad069f37dd85fb133` is migration input and failed-review history only.

## Retained design

The future package retains 64 bases (32 dialogue/32 narrative); roles 24 context mutant, 16 surface mutant, 24 clean control; each cohort/profile cell 6/4/6; and 32 request identities. Discovery is A/B/C/D × two runs × two shards (16 cells). Confirmation is A plus the derived B/C/D winner × two runs × two shards (8 cells). Every run requires context gain versus A >=3, surface hits >=A, and clean-with-findings <=A; rank is context gain descending, clean findings ascending, then D/C/B. No winner gives `STOP_NO_WINNER` and creates no confirmation authorization, attempt, or RAW.

`runtime-context-text-v2` remains `BEFORE → SOURCE_CONSTRUCT → AFTER`; SOURCE_CONSTRUCT is complete and never renderer-truncated. Exact-source fallbacks remain `V4-C-D01`, `V4-D-D09`, `V4-D-N04`, `V4-D-N07`, `V4-D-N09`, `V4-D-N10`, `V4-D-N15`. Requests are at most 120000 UTF-8 bytes.

## Closed contract highlights

- ORCHESTRATOR alone writes activation, plans, authorization, child observation/audit, lifecycle, review-attestation, manifest, gate, and pin receipts. Manifests are authoritative task artifacts; STATE is informational and package-unreadable.
- Activation scope hashes canonical exact `{allowed_paths,orchestrator_agent_id,task_id,user_authorization,workspace_id}` bytes. Candidate and repository review identities remain distinct and exclude all pre-review plans.
- Every phase/repair gets an immutable PHASE_PLAN after both candidate identities freeze and before controlling review dispatch. It fixes phase/version/nullable repair, both review slots, candidates, and prospective manifest/gate paths. Controlling records bind its hash; the post-PASS manifest binds those exact records. PHASE_REVIEW only attests completed records and invents no lifecycle.
- Module content hashes canonical ordered `{path,raw sha256}` files plus dependency edges. Integration is composition metadata over exact `integration/COMPOSITION.json` and `route/ROUTE.json`; bin owns executable entry files.
- Formal and qualification orphan audits have fixed write-once status/audit paths and exact schemas. Unknown stays IN_PROGRESS; only a valid exact-child terminal audit with FINISHED absent permits STOP_AMBIGUOUS_STARTED.
- Qualification CAPTURE-GATE is validated before releasing the waiting child. CAPTURE-SUMMARY and adapter_result have exact canonical schemas; completion/archive and pure finalization consume them in fixed order.
- Class S begins with two distinct waiting direct children and fixed `receipts/mutation/PLAN.json` before dispatch. Author is archived before validator release.
- Discovery/confirmation authorization, SCORES/RESULT nesting, and all eleven gate input lists/predicates are closed and fixed-path; P1/P2/P3 carry explicit predecessor gate path/hash chains.

## Files

`SCHEMA-CONTRACTS.md` is the normative exact-schema/path/predicate contract. `ARCHITECTURE.md` states trust and composition. `TRUST-ROOTS.json`, `STATE-MACHINE.json`, and `MIGRATION.json` are canonical machine-readable summaries; `ACCEPTANCE.md` defines P0 verification.

Future production commands remain zero-argument `node bin/freeze.mjs`, `qualify-capture.mjs`, `qualify-finalize.mjs`, `run-discovery.mjs`, `run-confirmation.mjs`, and `post-run.mjs`. They are absent in P0 and expose no injection surface.
