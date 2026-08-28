# Source-context exploratory four-route v1

Status: `FROZEN_BEFORE_EXTERNAL_INFERENCE`.

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
