# Gemini context-counterexample REVIEWER — V5 execution v3

Experiment: does a checklist prompt and/or bounded source context change the
`gemini-3.7-flash-high` review route's context-hit, surface-hit and clean-false-positive
counts? This directory is the **harness**, not the result.

## Calls made so far

| counter | value |
|---|---|
| `agy` processes spawned | **0** |
| inference calls made | **0** |
| network calls made | **0** |
| mutations authored | **0** |
| `SCORES.json` / `RESULT.json` for real cells | **none** |

`node preflight.mjs` reports `execution_state: NO_RUN` and those zeros from the ledger alone:
`agy_processes_spawned` is the number of START rows in `execution/LEDGER.jsonl` and
`inference_calls_made` is that count minus the non-inference `qualification-models-list` rows.
No process counter anywhere in this package is a constant read out of a document (C15), and the
two qualification processes are journaled in that same ledger, before they are spawned, under
the cell ids `qualification-models-list` and `qualification-synthetic`. Nothing in this package
has ever run `agy`.
The only process-shaped code paths are exercised with a mock `invoke` function in
`tests/test-package.mjs`.

**What is implemented and tested:** manifest identity, predecessor immutability, the
renderer and its 32 frozen request byte streams, the envelope parser, the scorer, the
append-only ledger and its attempt rules (including qualification journaling and the
ledger-derived budget arithmetic), deterministic RAW derivation, the three gate
checks, the two-stage qualification workflow against a mock process, and the CLI argv
contract. **What is not:** any real `agy` invocation, any qualification evidence, any
mutation, any score for a real cell, and any claim about protocol effectiveness.

## The three blocking gates

There are exactly three, in this order, each a **task-owned** file that this package reads
and never writes (`gates.mjs`):

| # | gate | file | meaning |
|---|------|------|---------|
| 1 | `PACKAGE_REVIEW` | `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v3/PACKAGE-REVIEW-GATE.json` | the frozen checklist C01–C14 is `PASS` against this `MANIFEST.json` |
| 2 | `QUALIFICATION` | `…/QUALIFICATION-GATE.json` | archived two-stage route qualification, reported model `gemini-3.7-flash-high` |
| 3 | `EXECUTION_AUTHORIZATION` | `…/EXECUTION-AUTHORIZATION.json` | the exact authorized cell ids, route contract hash, request manifest hash and process budget |

Every gate binds `manifest_sha256`; gates 2 and 3 also bind the byte hash of their direct
predecessor gate, so the order cannot be skipped. Removed relative to execution-v1:
`CANDIDATE-IDENTITY`, `HASH-DAG`, the dual-review predicates, the mutation gate, the freeze
gate, the discovery-completion receipt and the confirmation authorization.

## Pilot authorization (verbatim, SPEC §6)

> - **Authorized calls:** exactly **4** `agy` invocations against `gemini-3.7-flash-high`, via the frozen route contract, on this host:
>   1. qualification: `agy models list --json` (one process, non-inference; `--version` is not run, so the process count stays at 4)
>   2. qualification: one synthetic 16-item request `D-I001..D-I016` (inference, non-scored)
>   3. discovery cell **A / run 1 / shard 1** (16 unmutated items, protocol A)
>   4. discovery cell **C / run 1 / shard 1** (same 16 items, protocol C with bounded context)
> - **Not authorized:** any fifth call, any retry beyond the `[1,2]` attempt rule, any B/D protocol call, any confirmation cell, any call with mutated items, any run 2.
> - **Counting:** every spawned `agy` process is a call regardless of exit status, and call 1 counts. Attempt 2 of a cell counts. A crashed or timed-out attempt counts. The budget is therefore 4 processes, of which at most 3 are inference.
> - **Pilot passes** when: calls 3 and 4 each produce a parseable envelope, RAW derives deterministically, `SCORES.json` is produced with `clean_with_findings` reported per protocol, ledger reconstructs the run, and `postRun` reports `PILOT_COMPLETE` with `agy_processes_spawned=4` and `inference_calls_made=3`.
> - **Pilot result is not experimental evidence.** It is proof the path works. No claim about protocol effectiveness may be made from it.

The `agy_process_budget` and `inference_call_budget` fields of the execution authorization
are enforced in `runner.mjs`; a fifth process raises `STOP_BUDGET` before any spawn.

## Mutations are out of scope

No mutation is authored in this task, so every row of `sealed/REFERENCE.json` is a
`CLEAN_CONTROL` with zero atoms. A pilot call therefore exercises only
`clean_with_findings`. `context_hits` and `surface_hits` are exercised by the hand-written
scorer fixture (`tests/fixtures/scorer-case.json`, checklist C07), never by the pilot.

## Scoring rule (one direction)

A reported candidate hits a reference atom iff its verdict is `FINDING`, its `claim_type` is
listed on the atom, and the **reported** `target_span` **contains** a frozen atom span. The
reverse containment is not a hit. Each `(item, atom)` pair is credited once; byte-identical
duplicate candidates inside an item are collapsed first.

## Every mechanism beyond the §2 complexity budget

The budget is: 3 blocking gates, 1 append-only ledger, 1 scorer, 1 preflight. Everything
below is additional and answers *which conclusion becomes invalid or irreproducible
without it?*

| mechanism | file | which conclusion dies without it |
|---|---|---|
| package manifest + `--check` | `MANIFEST.json`, `build-manifest.mjs` | Without it no reviewer verdict, gate or score can be tied to a specific set of bytes, so "this checklist passed on this package" is unreproducible (C02). |
| predecessor bindings + replay | `frozen/PREDECESSOR-BINDINGS.json`, `build-frozen-base.mjs` | The 64 bases claim to be the terminal V5 clean heads. Without the replay and the three tree hashes, any later edit to V5 / exec-v1 / exec-v2 would silently change what "the frozen sample" means (C01). |
| renderer + freezer | `request-lib.mjs`, `freezer.mjs`, `frozen/REQUEST-MANIFEST.json` | The A-vs-C comparison is only meaningful if the two requests differ in exactly one controlled way. Without deterministic, hash-bound request bytes, a difference in counts cannot be attributed to the protocol (C04). |
| leakage scan | `request-lib.mjs` (`scanRequestBytes`), `preflight.mjs` | If an internal identifier reaches the model, a hit could come from the harness rather than from the text, invalidating every hit count (C05). |
| envelope parser | `parser.mjs` | Scoring a malformed or mis-ordered response would silently misattribute findings to the wrong item, invalidating all three counts (C06). |
| two-stage qualification | `qualification.mjs` | Without evidence that the route really answered as `gemini-3.7-flash-high`, no count can be attributed to that model (C12, SPEC §8 `STOP_ROUTE`). Route identity is the `models list --json` capture naming that model exactly once, plus the argv `--model` binding of the synthetic request. The envelope's top-level `model` field is an optional runtime self-report that real captures do not carry: its **absence is not a mismatch**, and only a present, different value is `STOP_ROUTE`. |
| runner + parameterless CLI | `runner.mjs`, `run.mjs` | Without a fixed argv contract and a fixed authorization path, an operator could widen what runs, so "only the 4 authorized calls were made" would be unverifiable (C11, SPEC §6 counting). |
| deterministic RAW derivation | `runner.mjs` (`deriveRaw`) | Re-invoking to repair a missing RAW would spend an unauthorized call and could change the answer; without pure derivation the run is neither budget-honest nor reproducible (C10). |
| post-run reconstruction | `post-run.mjs` | The pilot pass condition is "the ledger reconstructs the run". Without an independent reconstruction, `PILOT_COMPLETE` would be self-asserted (C08, C13). |
| contract/fixture authoring scripts | `tests/write-contracts.mjs`, `tests/write-scorer-fixture.mjs` | Both are re-runnable generators for bytes that are otherwise hand-maintained; without them the checked-in contract and fixture bytes could not be regenerated and reviewed as derived artifacts. |

No mechanism was added by cycle 1. The repairs live inside mechanisms that already existed:
the two qualification processes are journaled in the **one** append-only ledger (C15), so the
process and inference counters that `preflight.mjs`, `runner.mjs` and `post-run.mjs` use are
derived from its START rows instead of from a constant in `qualification/EVIDENCE.json`;
capture paths are attempt-numbered, so a failed capture is retried under the same `[1]` /
`[1,2]` rule without deleting a file by hand. An exit-0 attempt whose captured stdout yields no
`agy` envelope is classified `FINISHED_RETRYABLE` by the same ledger, so `STOP_PARSE` follows
the attempt rule (SPEC §8) rather than firing after one attempt; the true exit code is still
journaled unchanged. `freezer.mjs` reports a partial freeze, which `preflight.mjs` treats as a
static-integrity failure. The environment allowlist in `ROUTE-CONTRACT.json` now carries
`HOME`, the `XDG_*` config/cache/data homes, `TMPDIR` and the five credential names the local
`agy` binary reads — `spawnSync` replaces the environment wholesale, so an omitted name is an
absent name and call 1 would exit non-zero and spend an authorized process. Credential values
are passed only as environment values, never substituted into argv or into request bytes, and
never recorded in an artifact.

Nothing else is present. `assignment.mjs`, `control-plane.mjs`, `freeze-hashes.mjs`,
`gate-lib.mjs`, `mutation-gate.mjs`, `post-run-validate.mjs`, `CANDIDATE-MANIFEST.json`,
`HASH-DAG.json`, `MUTATION-GATES.json` and `frozen/ASSIGNMENT-PLAN.json` were deleted with
their mechanisms.

## Files

```
MANIFEST.json            path + sha256 for every source file, bytewise order, self-excluded
EXPERIMENT.json          experiment identity, NO_RUN state, call counters, excluded claims
GATES.json               the three gates and their current (unsatisfied) status
DESIGN-CONTRACT.json     protocols A-D, cohort/run/shard axes, scoring and stopping rules
REQUEST-CONTRACT.json    request/parser/ledger contract in declarative form
ROUTE-CONTRACT.json      local agy path, gemini-3.7-flash-high, argv template, env allowlist
lib.mjs                  hashing, canonical/duplicate-safe JSON, tree walk, predecessor consts
build-manifest.mjs       builds MANIFEST.json; --check rebuilds and compares byte-for-byte
build-frozen-base.mjs    replays the terminal V5 frame -> frozen/BASES.json + bindings
freezer.mjs              renders 64 samples, the sealed reference, 32 requests; --check
request-lib.mjs          context renderer, leakage scan, request builder and byte ceiling
parser.mjs               strict agy envelope + inner response parser
scorer.mjs               the single scorer: context_hits, surface_hits, clean_with_findings
ledger.mjs               the single append-only JSONL ledger, all derived run state and both
                         ledger-derived process counters (execution + qualification cells)
gates.mjs                the three blocking gate checks
qualification.mjs        two-stage non-scored route qualification (2 journaled processes)
runner.mjs               one cell, one attempt, capture, ledger, deterministic RAW
run.mjs                  production CLI; accepts only --cell <id>
preflight.mjs            the single preflight: static integrity, gates, call counters
post-run.mjs             ledger reconstruction, scoring, SCORES.json
frozen/BASES.json        the 64 terminally clean V5 heads
frozen/PREDECESSOR-BINDINGS.json  30 round artifacts + 3 byte-immutable predecessor trees
sealed/README.md         scoring partition policy
model-facing/prompts/    GENERIC.md (A, C) and ENHANCED.md (B, D)
model-facing/schemas/    REVIEWER-SCHEMA.json, the bundle schema handed to agy
tests/test-package.mjs   executable verification of C01-C13, C15 and advisory F1/F3/F6/F8
tests/fixtures/          real-shape agy envelope, duplicate-key sample, scorer case
tests/write-contracts.mjs, tests/write-scorer-fixture.mjs   byte generators for the above
```

## Operational sequence

In this order, and no other. Steps 3-5 spend authorized `agy` processes; steps 1-2 do not.

| # | step | command / actor | why it is here |
|---|------|-----------------|----------------|
| 1 | **freeze** the samples, sealed reference and 32 request byte streams | `node freezer.mjs` (write mode; run `--check` first) | Gate 3 binds `frozen/REQUEST-MANIFEST.json`, so the freeze must exist before that gate can be authored. `preflight.mjs` fails static integrity on a *partial* freeze, so this step is all-or-none. |
| 2 | **author the gates** — `PACKAGE-REVIEW-GATE.json`, then later `QUALIFICATION-GATE.json`, then `EXECUTION-AUTHORIZATION.json` | ORCHESTRATOR, by hand, under `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v3/` | Package code never writes a task-owned file (C11/C12). Gate 1 must exist before qualification; gates 2 and 3 bind the byte hash of their predecessor, so they cannot be authored out of order. |
| 3 | **qualification capture** (processes 1-2) | `captureQualification()` → task owner archives the dispatch and writes `QUALIFICATION-CAPTURE-RECEIPT.json` → `finalizeQualification()` | Produces `qualification/EVIDENCE.json`, which gate 2 binds. Both processes are journaled in `execution/LEDGER.jsonl` before they are spawned. |
| 4 | **run one cell** (processes 3-4) | `node run.mjs --cell <id>`, once per authorized cell | The only production entry point. Its only argument is `--cell`; authorization is read from the task-owned file at the fixed path. |
| 5 | **post-run** | `node post-run.mjs --write` | Reconstructs the run from the ledger, re-derives every RAW, scores, and writes `SCORES.json`. Run it without `--write` first to inspect the report. |

`run.mjs` accepts a cell id matching `<cohort>-<protocol>-run-<run>-shard-<shard>` and nothing
else. For the pilot the two accepted ids are:

```
discovery-A-run-1-shard-1
discovery-C-run-1-shard-1
```

Both must additionally appear in `authorized_cells` of the execution authorization. Any other
id is refused, including the two qualification cell ids `qualification-models-list` and
`qualification-synthetic`, which are journaled in the ledger but never run through `run.mjs`.

## Pre-declared pilot decisions

Decided in advance, before any call, so that neither outcome can be re-interpreted afterwards.

- **A RAW that fails only TARGET/EVIDENCE membership is `MODEL_OUTPUT_NONLITERAL`.** If a
  candidate's `target_span` is not a literal substring of the item target, or its `evidence` is
  not a literal substring of the item source / target / rendered context, the parser rejects the
  RAW. When *membership* is the only failure, that is the model producing a non-literal quote:
  it is a **cell failure, not a harness fault**, it is **not retried**, and it spends no further
  process. The cell is reported unscored with that classification.
- **If cell A's attempt 1 times out or exits non-zero, attempt 2 of A is taken and cell C is
  skipped.** Proving that the retry path works on a cell that has already failed is worth more
  than a second protocol on an untested path. The pilot then reports
  `PILOT_INCOMPLETE_BUDGET` and the overall decision is `NO_GO` with that reason. There is no
  attempt 3 and no fifth process under any circumstance.

## Safe commands now

```bash
node --check *.mjs tests/*.mjs
node build-manifest.mjs --check     # expected: no errors
node build-frozen-base.mjs --check  # expected: PASS, 30 round artifacts, 3 trees
node freezer.mjs --check            # expected: 32 requests, exact_source_appended_count 7
node tests/test-package.mjs         # expected: 32 tests, all ok
node preflight.mjs                  # expected: NO_GO_REQUIRED_GATES, NO_RUN, zero calls
node post-run.mjs                   # expected: NO_RUN
```

Do not run `agy`, qualification, or `run.mjs` until all three gates exist. `run.mjs` refuses
anything but `--cell <id>` and refuses any cell not named in the execution authorization.
