# Gemini context-counterexample reviewer V4

Status: **NO_GO / static integrity only / zero inference**. The independent V4 selection package is frozen; new V4 audits and every downstream experimental artifact remain unreleased. No model, network, qualification, audit, or inference call was made.

V4 uses V3's corrected scope and exact binder unchanged: 927 dialogue rows in 96 files and 309 narrative rows in 51 files. Narrative includes only exact top-level lore-body bindings and top-level non-tutorial `intro-*`/`message-*`; unresolved lore fields, lore labels, `unlock-*`, tutorials, metadata, logs, mechanics, achievements, and arbitrary strings are rejected.

## Frozen row selection

Seed: `gemini-context-counterexample-reviewer-v4/canonical-selection/v1`. IDs: `V4-{D|C}-{D|N}NN`. Rows rank by `sha256(seed + NUL + profile + NUL + revision_id)`. For each profile, only the first three ranked rows per file form the capped universe. Selection alternates discovery and confirmation slots and freezes 16 dialogue plus 16 narrative rows per cohort. Active selection permits file overlap but caps each profile/file at three total and each profile/file/cohort at two.

Exact result:

- eligible: 927 dialogue + 309 narrative = 1,236 rows;
- cap-3 universe: 265 dialogue + 110 narrative = 375 rows;
- selected: 64 rows (32 per profile; 32 per cohort);
- initial ranked reserve after selection: 311 rows, including 78 narrative rows;
- selected distinct files: 23 dialogue and 19 narrative;
- reserve distinct files: 93 dialogue and 46 narrative;
- maximum concentration: 3 rows/file in capped, selected, and reserve sets;
- discovery/confirmation file overlaps: 6 dialogue files and 8 narrative files.

`AVAILABILITY.json` and `SOURCE-FRAME.json` disclose exact top-file concentrations and overlap filenames. Global uniqueness remains mandatory for revision/base identity, normalized source, and normalized bound context.

## Replacement and audits

`V4_REJECTED_BASES_PATH` accepts a later V4 rejection ledger. It is sanitized into the deterministic, frozen `REJECTED-BASES-INPUT.json`; subsequent `--check` runs use that package input by default and reject an external mismatch. A rejected revision is globally banned. Its slot takes the first unused same-profile ranked reserve that preserves row uniqueness and active caps; incompatible rows are recorded, and exhaustion fails closed with exact profile/cohort. `OUT_OF_SCOPE_NON_PROSE` is excluded without translation-defect attribution. Fixtures exercise 1/28/29 narrative rejections, cap preservation, successful same-file acceptance after capacity is freed, base-identity collision, skipped reserves, and exact exhaustion.

Surface audit must precede context audit and remains blocked until an explicitly released, queue-hash-bound audit state exists. V3 verdicts are provenance only and are not imported. Qualification, run, and execution-authorization validation are documented deferred interfaces; this package is always-deny and does not open those gates. There are no audit records, mutations, samples, sealed references, requests, qualification artifacts, raw outputs, scores, or results.

Prior exposure is `ALLOWED_NOT_EVALUATED`; no novelty, contamination-free, unseen, prevalence, source-file independence, or generalization claim is supported. Requested route identity is `REQUESTED_ROUTE_ONLY_UNVERIFIED`.

## Checks

```bash
node select-and-freeze.mjs --check
node test-source-binding.mjs
node test-assignment.mjs
node test-fixtures.mjs
node test-zero-call.mjs
node test-integrity.mjs
node test-schemas.mjs
for f in *.mjs; do node --check "$f"; done
node preflight.mjs          # exit 3; NO_GO with static_integrity PASS
node post-run-validate.mjs  # NO_RUN
# Post-run validation scans every text file, rejects NUL/non-scannable bytes, and recursively decodes
# bounded nested *_base64 JSON fields; preflight also verifies slotwise frame/ledger and queue bindings.
# Rejection replacement is an explicit transition: use --freeze-rejections with an existing canonical
# input and V4_REJECTED_BASES_PATH; normal --check rejects missing or mismatched external input.
```
