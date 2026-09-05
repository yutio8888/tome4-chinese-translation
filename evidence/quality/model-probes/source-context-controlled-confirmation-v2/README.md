# Source-context controlled confirmation v2

Status: `COMPLETE / ADOPTION_NO_GO`.

## Result

The registered decision is **not** to adopt source context as the default on
this evidence. Context atom detection increased by 10 of 96 route-items in
each run (`6 -> 16` and `4 -> 14`), with no negative context route direction,
but both runs missed the registered +20 minimum. Run 2 also has an ineligible
GLM A shard because the response added an unexpected top-level field; it was
not retried. Aggregate surface-mutant detection did not fall (`+4`, `+2`), but
the run-2 Codex route fell by one hit. There were no B-only clean candidates,
but post-response adjudication confirmed that K014 was not actually clean:
its translation omits the player-caused “letting her grow” achievement
condition. That control contamination independently fails adoption.

These measurements are descriptive for the frozen finite set. They show a
repeatable positive signal, not confirmation of the registered hypothesis.
See `RESULT.json` and `SCORES.json` for the complete route/item accounting.

This experiment studies one operational question: on project-corpus-novel,
source-verified clean ToME dialogue and narrative revisions, does a mechanically
bound public-source context packet stably improve detection of controlled
defects that cannot be decided from the English source and Chinese target
alone, without reducing surface-defect detection or creating new objective
candidates on clean controls?

The experiment is a fresh version. It does not append a run to
`runtime-source-context-pilot-v1`, relax the failed adoption decision in that
experiment, or reuse the historically exposed 439-row expansion pool as the
primary frame.

## Scope

The finite target population will be the final 60 frozen ToME revisions, not
the whole repository:

- 24 controlled context-required mutants;
- 24 independently clean controls drawn from the same mutation-eligible frame;
- 12 surface-visible mutants used as a retention guardrail.

All 60 base revisions were required to be clean before mutation assignment, use distinct
canonical revisions, English sources and context blocks, use at most three items
from one public source file, and be drawn from the `dialogue` or `narrative`
profiles. Conclusions do not extend to mechanics, UI, runtime-log, DLC
components, natural defect prevalence, or model-family rankings.

`project-corpus-novel` means that the revision and normalized English source
do not occur in the hash-pinned tracked model-probe corpus or the registered
historical terminal contextual frame at the time of the source-screen freeze.
It is not a claim about pretraining data, provider-side logs, deleted or
untracked sessions, or human familiarity.

## Phase order

1. Rebuild the canonical 30,308-row inventory at production translation commit
   `1666481409f4c0d63d66e84659f6b6145d8d25d0`.
2. Before permitting any target-field access for selection, exclude every
   tracked prior revision/source exposure, locate each remaining source in
   fixed public ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`,
   and freeze a source-only candidate screen plus mechanical context packets.
3. Bind targets only after the source screen is frozen. Audit all candidate
   bases surface-first and context-second. Only lead-adjudicated clean bases
   enter mutation eligibility.
4. Author single-atom mutations, run the pre-inference manipulation check, and
   assign the final 60 items with the frozen seed and ordered reserves.
5. Freeze routes, CLI versions, exact request bytes, schema, runner, parser,
   scorer, gates, fixtures, reference hashes, and all model-facing inputs.
6. Run the registered waves `A1 -> B1 -> B2 -> A2`; routes may execute in
   parallel inside a wave. No third run is permitted.
7. Reveal the sealed reference only after all eligible RAW responses are
   immutable, then score and publish the registered decision.

During execution, no model call was authorized until the Phase-0 prerequisites
had passed. A failed screen, clean audit, manipulation check, route
qualification, leakage check or preflight was a no-go for inference in this
version and could not be repaired by post-outcome replacement.

## Registered decision policy

For every run separately, with four frozen CLI routes and 24 context mutants:

- context gain must be at least 20 net atom detections out of 96 route-items;
- at least three routes must have strictly positive context gain and no route
  may have negative gain;
- the B arm must not lose any aggregate or per-route surface-mutant atom hit;
- the B arm must not increase aggregate or per-route objective clean-control
  candidates, and no clean item may become a new B-only objective candidate;
- base contamination, control contamination, mutation-integrity failure,
  missing paired cells, reference leakage, route mismatch or frozen-hash drift
  makes adoption fail or invalid as specified by `DESIGN-CONTRACT.json`.

The two runs are repeated measurements, not additional independent items.
Route-item cells are not treated as independent samples, and no naive binomial
confidence interval or significance claim is registered.

## Recorded execution boundary

All four waves were executed once in the registered order, using three fixed
20-item transport shards introduced by `DESIGN-AMENDMENT-007.json` after the
unsharded non-research qualification exposed a structured-output failure. The
change preceded experimental inference and did not alter sample membership,
order, atoms, routes, runs, gates or denominators. There was no experimental
retry and no third run.

`SCREEN-PREFLIGHT-FAILURE-001.json` and `-002.json` record two pre-target,
zero-inference failures of an over-constrained screen-wide file cap. The
resulting design amendments change only source-screen breadth: the 240-row
screen permits up to twelve rows per file, while the final 60-row sample uses
the amended three-per-file cap and unique context blocks.
