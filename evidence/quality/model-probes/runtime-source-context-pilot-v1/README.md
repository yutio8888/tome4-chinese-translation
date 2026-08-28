# Runtime source-context pilot v1

Status: complete; registered adoption decision failed.

This finite benchmark compares the same 36 ordered review items under two arms. Arm A contains only `source` and `target`; Arm B adds a mechanically extracted, sanitized public Lua block. Four fixed routes each ran twice, for 16 registered model calls.

The pre-inference freeze is commit `57b776f19fc431d525a405d1d89d182e71438f43`. Mechanical harness amendments are recorded in `HARNESS-AMENDMENT.json`; they do not change the prompt, payload, items, reference, scorer or gates.

## Measured outcome

- Run 1 runtime-mutant detections: A `1/48`, B `32/48`, net `+31/48`; all four route deltas positive.
- Run 2 runtime-mutant detections: A `0/48`, B `35/48`, net `+35/48`; all four route deltas positive.
- Runtime-control candidates decreased in aggregate: `10 -> 6` and `11 -> 3`.
- Run 1 failed the per-route guardrail because Codex had two new B-arm objective control candidates, above the maximum of one.
- P005 was confirmed as a contaminated control: code selects any positive-reaction target, while the target says same faction. The zero-contamination gate therefore fails.

Both runs must pass every gate, so `RESULT.json` records `adopt_B_as_default_for_later_phases=false`. The strong recall signal is retained as measured evidence, but it does not override the guardrails. There is no third run and no post-outcome item replacement.

## Primary artifacts

- `EXPERIMENT.json`, `MANIFEST.json`, `FROZEN-HASHES.json`: frozen contract.
- `HOLDOUT-A.json`, `HOLDOUT-B.json`, `REFERENCE.json`: inputs and sealed atoms.
- `RAW-*`, `CANDIDATE-*`, `FAILURE-*`: complete route envelopes and harness failures.
- `SCORES-PRELIM.json`, `ADJUDICATION.json`, `SCORES.json`, `RESULT.json`: measured scores, control rulings and final decision.
- `POST-RUN-VERIFICATION.json`: frozen-hash, fixture, route-version and executor-baseline verification.

To test source context again, create a new version with a fresh freeze and stronger clean-control verification; do not append another run to this experiment.
