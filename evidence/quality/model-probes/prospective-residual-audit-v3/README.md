# Prospective residual audit v3 candidate set

Status: 40 production-resolved task/revision units selected; uniform source audit pending; model inference prohibited.

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

## Current gate

No v3 reviewer-route model call has been made. `SOURCE-AUDIT-PROTOCOL.json` freezes four possible source-audit outcomes: `CONFIRMED`, `REFUTED`, `INDETERMINATE` and `UNREACHABLE`. It also records that Codex subagents may provide mechanical location or preliminary evidence proposals, but the primary experiment lead must independently verify every fixed source and sign the final verdict before any reviewer-route output exists. All 40 items must receive equal-depth source audit, and none may be replaced after selection.

`SOURCE-LOCATOR-CONTRACT.json` and `SOURCE-LOCATORS.json` bind all 40 items to public source without writing verdicts. Thirty-nine use Git blobs from fixed engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; the one Cults item uses an explicit public-file SHA-256 because the DLC repository was not commit-frozen. There are 37 unique normalized matches and 3 short-source multiple matches; every occurrence is retained for adjudication. No item is currently unreachable at the source-location stage.

The later reviewer context remains Arm A, source and target only. `HOLDOUT-DRAFT.json` is deliberately not inference-ready. A sealed reference, exact weighted estimators and missingness bounds, prompt, schema, scorer, model routes and fail-closed preflight still have to be frozen after source audit.

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
```

The verifier creates and removes its own detached temporary worktree, regenerates the canonical inventory, checks the production input digest and all historical terminal-input fingerprints, regenerates every derived JSON, validates selection probabilities and confirms that inference remains disabled.
