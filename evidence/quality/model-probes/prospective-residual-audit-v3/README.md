# Prospective residual audit v3 candidate set

Status: the 40-item public holdout, generic reviewer prompt, exact schema, sealed atom matcher, scorer, four preregistered routes and fail-closed runner are frozen; no v3 reviewer inference has been made. A committed-package preflight must report GO before either executable route is invoked.

This directory supersedes `prospective-residual-audit-v2`. The v2 selection was invalidated before source adjudication or model inference because some historical Paseo `translation_snapshot` entries were intermediate review snippets rather than the complete translation revision present at the frozen production commit. The v2 artifacts remain preserved as an audit trail.

## Canonical membership

Every v3 frame member must pass two mechanical gates:

1. its task/revision pair did not appear in any prior model experiment;
2. its component, English source and Chinese target resolve to exactly one canonical inventory revision at production translation commit `1666481409f4c0d63d66e84659f6b6145d8d25d0`.

For repeated exact pairs, the already-frozen bounded context may supply `section=`, `path=` or fixed-source metadata. These forms are normalized mechanically. A record that still fails to resolve is excluded; it is never assigned by hand. This resolves all repeated exact pairs in the eligible frame. Another 128 terminal records are excluded because they are noncanonical source snippets or their candidate target differs from production.

The frozen eligible frame has 46 tasks and 1,396 unique canonical revisions:

- same-family-only: 30 tasks / 733 revisions; select 24 tasks by systematic PPS;
- known cross- or mixed-family: 14 tasks / 569 revisions; census all 14;
- unknown provenance: 2 tasks / 94 revisions; census both.

One revision is selected by seeded equal-probability SHA-256 rank within each selected task. The result is 40 unique production revisions from 40 distinct tasks. `CANONICAL-MEMBERSHIP.json` records the complete frame membership without copying source or target text. `AUDIT-QUEUE.json` records the selected items and design weights.

## Source-audit result and current gate

No v3 reviewer-route model call has been made. `SOURCE-AUDIT-PROTOCOL.json` froze four possible source-audit outcomes: `CONFIRMED`, `REFUTED`, `INDETERMINATE` and `UNREACHABLE`. It also records that Codex subagents may provide mechanical location or preliminary evidence proposals, but the primary experiment lead must independently verify every fixed source and sign the final verdict before any reviewer-route output exists. All 40 items received equal-depth source audit, and none was replaced after selection.

`SOURCE-LOCATOR-CONTRACT.json` and `SOURCE-LOCATORS.json` bind all 40 items to public source without writing verdicts. Thirty-nine use Git blobs from fixed engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; the one Cults item uses an explicit public-file SHA-256 because the DLC repository was not commit-frozen. There are 37 unique normalized matches and 3 short-source multiple matches; every occurrence is retained for adjudication. No item is currently unreachable at the source-location stage.

`SOURCE-AUDIT-DECISIONS.json` records the primary experiment lead's signed decisions and discloses the preliminary Codex subagent proposals as non-ground-truth assistance. `SOURCE-AUDIT.json` mechanically binds those decisions to every registered source occurrence and hash. The frozen result is 1 `CONFIRMED` item (R033, an objective hard-line-break format defect), 39 `REFUTED`, 0 `INDETERMINATE` and 0 `UNREACHABLE`. A subagent proposed R009 as confirmed, but the primary lead independently overrode it and retained the trace: reflowing one adjacent prose line break did not lose a paragraph boundary, token or Chinese word.

`SEALED-REFERENCE.json` contains only the minimal reviewer-hidden identity, stratum, binary scoring label and exact-weight bindings. It does not copy reasons, findings, evidence classes, source or target. `ESTIMATOR-CONTRACT.json` and `REFERENCE-ESTIMATES.json` freeze exact rational weights, Horvitz-Thompson and Hájek reporting, missing-evidence bounds, the 90% determinate gate, zero-denominator rules and the prohibition on a conventional confidence interval under this one-realization design. The design-weighted estimate is `4/1745` (about 0.229%), while the unweighted `1/40` (2.5%) is sample-only and may not be presented as the finite-frame rate.

Both the 40/40 determinate gate and the 38/40 provenance-classifiable gate pass. The translation-origin pilot budget-priority gate fails because only one confirmed item from one task was found, below the frozen four-items/four-tasks requirement; that pilot is deferred, not scientifically disproved. The later independent reviewer audit may still proceed after its own contract is frozen, but it cannot support a stable model ranking with one positive item.

The later reviewer context remains Arm A, source and target only. `HOLDOUT-DRAFT.json` is deliberately not inference-ready. `PUBLIC-HOLDOUT.json`, `PROMPT.md`, `REVIEWER-SCHEMA.json`, `SEALED-ATOM-MAP.json`, `score-lib.mjs` and `REVIEW-CONTRACT.json` now define the frozen review package. The prompt checklist is mechanically derived from the pre-audit scope in `SOURCE-AUDIT-PROTOCOL.json`, not from the sealed positive finding.

All four historical routes remain registered. Claude Opus 5 medium/no-advisor and Pi Z.ai CN GLM 5.3 Flash high are the primary verified routes. At the user's explicit direction, Codex CLI 0.150.1 and agy 1.1.22 are also run and scored as `REFERENCE_ONLY_UNVERIFIED`: Codex cannot mechanically prove that every file tool is absent and lacks server runtime-model attestation; agy cannot disable all tools and does not report runtime identity. Their scores are auxiliary references and cannot enter the primary ranking. Every attempt gets an exclusive directory with immutable raw stdout/stderr; parsing is a separate step.

## Rebuild and verify

Generate a canonical inventory from a detached worktree at the frozen production commit, then run:

```bash
node evidence/quality/model-probes/prospective-residual-audit-v3/build.mjs \
  --repo /path/to/source-repo \
  --inventory /path/to/frozen/inventory.jsonl
node evidence/quality/model-probes/prospective-residual-audit-v3/verify.mjs \
  --repo /path/to/source-repo
node evidence/quality/model-probes/prospective-residual-audit-v3/verify-source-locators.mjs \
  --engine-repo /path/to/t-engine4 \
  --dlc-root /path/to/tome4-dlcs
node evidence/quality/model-probes/prospective-residual-audit-v3/build-source-audit.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/verify-source-audit.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/build-reference.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/verify-reference.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/test-scorer.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/test-runner.mjs
node evidence/quality/model-probes/prospective-residual-audit-v3/preflight.mjs --route-check --write
```

The verifier creates and removes its own detached temporary worktree, regenerates the canonical inventory, checks the production input digest and all historical terminal-input fingerprints, regenerates every derived JSON, validates selection probabilities and confirms that inference remains disabled.
