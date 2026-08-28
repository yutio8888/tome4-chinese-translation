# Prospective source context audit v4

Status: `NO_INFERENCE/SOURCE_SCREEN_ONLY`.

This directory freezes a prospective source-only screen. It makes no model or network call, reads no scoring or review conclusions, and never binds translation-side content. It is an experimental candidate package, not a translation decision.

## Frozen outputs

- `SCREEN-CONTRACT.json` fixes the permitted Phase-0 fields, seven recomputed source-only flags, two mutually exclusive predicates, source bindings, locator rule, evidence limits, seed, round-robin algorithm and gates.
- `SOURCE-ONLY-BASE-FRAME.json` contains all 1,396 source-only task/revision rows reconstructed directly from v3 canonical membership and the provenance snapshot's fingerprinted terminal contextual inputs. Reconstruction matches only task/revision identity and verifies only `source_sha256`.
- `SOURCE-EXPOSURE-REGISTRY.json` freezes the nine Git-tracked structured model-facing inputs used for prior source exposure. It keys exposure by `sha256(task_id NUL original_revision_key)` and `sha256(normalize_source(source))`; there is deliberately no RAW-output tier.
- `SOURCE-SCREEN-FRAME.json` contains the final 60 Runtime and 60 Narrative source-only items. Model-facing item fields are exactly the eight Phase-0 scalar fields plus `source_only_flags`.
- `SOURCE-EVIDENCE-PACKETS.json` replaces each matched source span with a marker and retains at most 12 lines and 2,000 UTF-8 bytes on each side. It freezes ToME at commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; each DLC artifact is bound by component-relative path, SHA-256 and byte size.
- `BUILD-REPORT.json` records measured attrition and gate outcomes.

The final source-only presentation SHA-256 is `8deda776d84cdcca0794ea2dcec34f2dbb5d5971b2d937d2653b1f60b95886c5`. It covers the ordered frame items and their ordered public-source evidence packets, not metadata outside that presentation.

## Measured build

The source-only base contains 1,396 rows across 46 tasks. All 58 terminal input files are verified against the frozen provenance fingerprints before projection, but their translation-side fields, mixed risk flags, terminology snapshots, pair hashes and canonical identities are not read by the base builder. The byte/profile gate leaves 1,387 rows; the category predicates classify 700. The nine-file source-only exposure registry removes 21 classified rows, leaving 679 eligible rows: 94 Runtime and 585 Narrative. These are exactly four more Runtime and four more Narrative rows than the invalid target/RAW-influenced starting frame.

The source locator accepts 663 rows, records five missing normalized matches and eleven rows with more than two occurrences as ineligible, then component/content deduplication leaves 656.

The final screen has 120 items across 43 tasks:

- Runtime: 60 items across 23 tasks;
- Narrative: 60 items across 38 tasks;
- maximum contribution from one task in one category: 6;
- selected occurrence counts: 119 unique, 1 double;
- bound source artifacts: 83 (77 ToME, 2 Cults, 4 Orcs).

The 16 non-accepted locator rows are recorded only as aggregate build attrition. They are not repaired, replaced by inference, or promoted to a review conclusion.

## Rebuild and verify

Use the production translation checkout containing the 58 fingerprinted terminal inputs, a checkout of `t-engine4` containing the frozen commit, and a DLC root containing the registered `cults/`, `orcs/` and `ashes-urhrok/` subdirectories:

```bash
node build.mjs --production-repo /path/to/production-checkout --engine-repo /path/to/t-engine4 --dlc-root /path/to/tome4-dlcs
node test-builder.mjs
node verify.mjs --production-repo /path/to/production-checkout --engine-repo /path/to/t-engine4 --dlc-root /path/to/tome4-dlcs
python3 -m json.tool EXPERIMENT.json >/dev/null
python3 -m json.tool SCREEN-CONTRACT.json >/dev/null
python3 -m json.tool SOURCE-ONLY-BASE-FRAME.json >/dev/null
python3 -m json.tool SOURCE-EXPOSURE-REGISTRY.json >/dev/null
python3 -m json.tool SOURCE-SCREEN-FRAME.json >/dev/null
python3 -m json.tool SOURCE-EVIDENCE-PACKETS.json >/dev/null
python3 -m json.tool BUILD-REPORT.json >/dev/null
git diff --check
```

`test-builder.mjs` starts at `reconstructSourceOnlyBaseRows` and changes or deletes every translation-side fixture field. It proves that the base frame, attrition counts, seeded selection order and final presentation remain canonical-byte-identical. `verify.mjs` rebuilds all five generated artifacts byte-for-byte, verifies base/presentation/input/source hashes, checks the frozen source artifacts, and enforces all selection and packet gates.

## Boundary

This package is a GO only for preserving the frozen source-only presentation. It remains a NO-GO for inference, reviewer labels, scoring, or translation changes until a separate protocol is frozen. No artifact here overrides repository adjudication.
