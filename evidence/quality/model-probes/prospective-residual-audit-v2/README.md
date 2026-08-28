# Prospective residual audit v2 candidate set

Status: 40 fresh task/revision units selected; uniform source audit pending; model inference prohibited.

This directory starts Phase 2 after `runtime-source-context-pilot-v1`. Phase 1 found a strong source-context recall signal but failed its registered control gates, so this set explicitly keeps the later reviewer policy at Arm A: source and target only.

## Fresh frame

The frozen provenance snapshot contains 120 completed P2 tasks. The selection applies a stricter exclusion than the earlier roadmap required: if any revision from a task appeared in a prior model experiment or item-level reference, the entire task is excluded. This removes 74 previously exposed tasks. One further task has no terminal translation revision.

The remaining fresh frame has 45 tasks and 1,270 terminal revisions:

- same-family-only: 35 tasks / 847 revisions; select 30 tasks by systematic PPS;
- known cross- or mixed-family: 8 tasks / 329 revisions; census all 8;
- unknown provenance: 2 tasks / 94 revisions; census both.

One revision is selected by seeded equal-probability rank within every selected task. The result is 40 revisions from 40 distinct tasks. The selected set contains 32 base-game text revisions and 8 DLC dialogue revisions; none of their tasks appeared in an earlier model experiment.

`FRAME.json` records every eligible task, size measure, first-order task inclusion probability and selection state. `AUDIT-QUEUE.json` records the 40 selected revisions, conditional item probability, total inclusion probability and design weight. `HOLDOUT-DRAFT.json` deliberately omits provenance but is not an inference-ready holdout.

## Current gate

No model call has been made. Every selected item must now receive the same-depth fixed-source audit before reviewer output is allowed. The audit must classify each item as confirmed, refuted, indeterminate or unreachable and must not replace difficult or contaminated items after selection.

Only after that audit is frozen may a later step define the sealed reference, exact weighted estimators and bounds, prompt, response schema, scorer, routes and fail-closed inference preflight.

## Rebuild and verify

```bash
node evidence/quality/model-probes/prospective-residual-audit-v2/select.mjs --repo /path/to/source-repo
node evidence/quality/model-probes/prospective-residual-audit-v2/verify.mjs --repo /path/to/source-repo
```

The verifier requires every terminal input to match the fingerprint in the frozen provenance snapshot, regenerates all derived JSON in a temporary directory, checks the probability totals and selected-unit uniqueness, and confirms that inference remains disabled.
