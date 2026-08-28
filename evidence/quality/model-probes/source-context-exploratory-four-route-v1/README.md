# Source-context exploratory four-route v1

Status: `EXPLORATORY_COMPLETE_WITH_RECOVERED_SCHEMA_ALIASES_NOT_FORMAL`.

This is a deliberately exploratory follow-up to `prospective-source-context-truth-audit-v1`, whose formal GLM gate returned `NO_GO_INSUFFICIENT_TRUTH_SET`. It does not relax or replace that result.

Four requested routes review the same 14 sanitized pairs twice per arm. Arm A receives source and target only; Arm B receives the same bytes plus raw fixed public-source excerpts. The set contains one context-dependent defect, five surface-visible defects, four context-exonerated clean disputes and four ordinary clean controls. Because the single context-positive case is repeated, this experiment can show whether context helped on that case, not estimate general context recall.

The four frozen execution waves are A1, B1, B2, A2, with routes parallel inside each wave. Run one is therefore A then B; run two is B then A. `run.mjs` never reads `REFERENCE.json` contents into the prompt, but binds its SHA-256 into every candidate.

Commands:

```bash
node build-inputs.mjs
node run.mjs codex A 1
node run.mjs claude A 1
node run.mjs glm A 1
node run.mjs gemini A 1
```

Use the same command shape for the remaining frozen waves. If acquisition succeeded but parsing failed, fix only the parser and run the same command with `--parse-existing`; this reuses hash-bound RAW and makes no model call. Never expose `REFERENCE.json` or `ATOM-ADJUDICATION.json` to a candidate model.

All 16 planned acquisitions completed. Fourteen candidates satisfy the frozen response schema. GLM A2 and B1 each contain 14 complete ordered review rows under the top-level key `verdicts` rather than `items`; their candidate files remain strict-invalid. `ANALYSIS-AMENDMENT.json` records the post-inference rule that gives those unchanged rows separately labeled recovery-normalized reference scores. `RESULT.json` therefore reports 14 strict-valid runs, two recovery-normalized runs and 16 reference-scored runs.

The main observation is narrow: fixed source context removed the repeated E007 clean false positive in every route, but no route identified the single context-dependent E013 defect. Codex retained some surface-defect detection but declined from 7/10 atom hits without context to 4/10 with context. The other three routes recorded 0/10 surface atom hits in both arms under the sealed atom rule. These are repeated observations of a deliberately enriched 14-case set, not general provider rankings.
