# V5 execution-v5 pilot terminal report

## Decision

**NO_GO_A_PARSE_INVALID** (terminal for this task).

Classification: **MODEL_OUTPUT_VALIDATION_FAILURE_PATH_PILOT_NOT_EFFECTIVENESS_RESULT**.

## Measured path facts

Qualification passed as `PASS_NON_SCORED`. The ledger contains three spawned agy processes and two inference calls: the model-list qualification process, the non-scored synthetic qualification inference, and discovery A. No retry was made.

A prior dispatch (`discovery-A-007`) stopped before invocation with `NOT_INVOKED_HARNESS_CWD`; it consumed zero processes, zero inference calls, and no budget. The subsequent actual A dispatch invoked `discovery-A-run-1-shard-1` once. The process exited `0`, its ledger state is `FINISHED_SUCCESS`, and an envelope was extracted. Frozen parser validation nevertheless returned `parse_valid: false` with exactly three errors:

- `CANDIDATE:4:0:EVIDENCE_MEMBERSHIP`
- `CANDIDATE:11:0:EVIDENCE_MEMBERSHIP`
- `CANDIDATE:15:0:EVIDENCE_MEMBERSHIP`

This report intentionally does not reproduce or discuss the response content beyond that parser error metadata.

C is `NOT_INVOKED` because `A_BEFORE_C_PARSE_REQUIRED` was not satisfied. The task permits no retry. No `SCORES.json` was created, the pilot is incomplete, and these observations support no A/C protocol-effectiveness, model-quality, capability, or generalization claim.

## Post-run truth

`node post-run.mjs` was run read-only and returned exit `3` with decision `INVALID_ARTIFACTS`. Its sole error was the expected `RAW_PARSE` for A carrying the same three `EVIDENCE_MEMBERSHIP` entries above. Here, `INVALID_ARTIFACTS` is the fail-closed representation of model-output validation failure; it is not infrastructure corruption and it is not a score or effectiveness result.

## Integrity bindings

| Artifact | SHA-256 |
|---|---|
| `MANIFEST.json` | `6aca47be505c59da9030e73580458fdf11ae979fa13ef85dbe6718f7db732cb2` |
| `ROUTE-CONTRACT.json` | `520b37b21e71b1494d1569cc3552f21a6142327506069a7e0676dfded88e56e3` |
| `frozen/REQUEST-MANIFEST.json` | `eeef0a9ddfc332384c9f97485c11873842bf0b48b5ec008ce94df0b4846788bd` |
| `execution/LEDGER.jsonl` | `24c19cba02389f64a04039e26917479db4348eaf3c973ea7d47596d1eb14aecc` |
| `qualification/EVIDENCE.json` | `019260915d2ce743172daa915baa6a276cd8fc5212576c881130e9aa6ce78682` |
| `qualification/RAW-SYNTHETIC.json` | `245b732cf66a1efc2b664b5866676a774b55340e52ee2299aaed11a49ec919b3` |
| `PACKAGE-REVIEW-GATE.json` | `0723ca18488b9662742cdb23651ebdc182bdd8db855a22e79d886a5c116f7405` |
| `QUALIFICATION-GATE.json` | `4d65ad883d433831a48cff469de62f0d7464cc789652b4f0640523149b779ecc` |
| `EXECUTION-AUTHORIZATION.json` | `907fed1504fbbc711b7df451c550e24c360c0e34b5ed1a646427ca564151ac0a` |
| `QUALIFICATION-CAPTURE-RECEIPT.json` | `901ddffcb037afa9d64c764def3d3585762bc48bd8953b30fa8b5201239fbba1` |
| A RAW | `2ef447bbf1743335bd34fb6c480f29acee68f49a09cd950097e8ee6e3ad5c390` |
| A stdout capture | `d0b3ba402a3d8c8fa695fb8d276b702f225b3a8518edd7120ef04ab30a698c5c` |
| A stderr capture | `3a7f8550106d86abb322e8ed0fb30a0296c0e97c6be03d5a8033b99d16737459` |
| pinned agy binary | `f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e` |

The manifest excludes `PILOT-RESULT.json` and `PILOT.md`, so terminalization does not rebuild it. Terminalization authorized zero agy/model/network calls and performed none.
