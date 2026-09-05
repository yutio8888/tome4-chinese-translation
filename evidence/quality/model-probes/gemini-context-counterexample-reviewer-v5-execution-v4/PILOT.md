# V5 execution-v4 pilot terminal report

## Decision

**NO_GO_ROUTE_BINARY_DISAPPEARED** (terminal for this task).

Classification: **HARNESS_INFRASTRUCTURE_ROUTE_FAILURE_NOT_MODEL_FAILURE**.

## Measured facts

V4 used two of the four authorized processes and one of the three authorized inference calls. Both non-scored qualification calls completed with exit `0` under the old, qualified executable bytes:

- `qualification-models-list`: one process, no inference.
- `qualification-synthetic`: one process, one non-scored inference.

The qualified executable SHA-256 was `d492241f19f90ea06cb9f85f7788c371dbce3386206d734ddc2c7ec84fa3ddca`. Before A, the installed path contained different bytes, SHA-256 `f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e`, which were not qualified for v4. A same-byte relocation candidate was prepared at `/home/yun/.local/bin/agy.1788410029995956792.old`, but that exact backup disappeared before closure review. Review-05 found no remaining host copy with the qualified hash and failed blocking items R1/R5.

No A or C process was invoked. The ledger therefore remains at four rows, two processes and one inference call. The unused original process capacity is **2**; it is not transferable to a successor task. No retry was used.

There is no discovery-A RAW, discovery-C RAW, `SCORES.json`, A/C score, or model-effectiveness evidence. The successful synthetic call is qualification evidence only. This terminal decision records a host route/harness infrastructure condition, not a model failure or model quality result.

All existing ledger rows, captures, qualification evidence, reuse contracts, route provenance and gate files were preserved byte-for-byte. Only `PILOT-RESULT.json` and this report were added. The manifest was not rebuilt because both terminal artifacts are explicitly excluded generated artifacts.

## Post-run truth

The generic successful-pilot `post-run.mjs` check returns `INVALID_ARTIFACTS`, as expected for this terminal state. It reports stale manifest bindings for all three gates, route/request bindings in execution authorization, and qualification identity/binding errors. Those gates bind the pre-relocation candidate and do not validate the unclosed relocation candidate. This fail-closed result is not a model failure and does not supersede the terminal classification above.

## Integrity bindings

| Artifact | SHA-256 |
|---|---|
| `MANIFEST.json` | `9f6837efd705459e1df55dc2c2be3603f6474610b778de070ed73ee453539b53` |
| `ROUTE-CONTRACT.json` | `f82ac7fd532e47d670be4839dc5d7301ceee143c5d50861445088e7fe79f3a4d` |
| `ROUTE-RELOCATION-CONTRACT.json` | `854aa9e8b93005b05187613a7cd0b8313a34c55862b3e6d00a50855167e91bde` |
| `execution/LEDGER.jsonl` | `d2dd5f069536c3d394bcbac3abc9320c4ff080bd907b7f532fc3452fac6508ef` |
| `qualification/EVIDENCE.json` | `49394c89810be42e11848754591da23cfec3334fd9a7fe6a79dd6a8ed5b93e2e` |
| `qualification/RAW-SYNTHETIC.json` | `b847fa9451befdb928c78f0f61617e69a8351fd245d34374ea3917e4100c1748` |
| model-list reuse contract | `0c958f3315cded885a4273cf8c57f03ed35c9230a2b7451d4b8e2a3eb18d9e95` |
| synthetic reuse contract | `9e2947bcd12d884ac027704601f59fe1c73c4f63eed88796450543ce1bf9a1e4` |
| model-list stdout capture | `b1cc011310435afa07b1e132a5b7f3e22297aa21427177461c858bcbd6a58794` |
| model-list stderr capture | `53f588bc9a928f4a66908deacaca57dddc7e7ce177a0cc3586b5a501be26e1e8` |
| synthetic stdout capture | `d06ea853a5ed9fafa6a71a859e4afe62a39efdaeb9f622b0e0207024184e11b4` |
| synthetic stderr capture | `3a7f8550106d86abb322e8ed0fb30a0296c0e97c6be03d5a8033b99d16737459` |
| frozen request manifest | `170e24a1eca62dea974e703de9391f5be486401cb41e0e0ce19098dd6f18c3b8` |

The immutable execution-v3 predecessor remains 74 files at tree SHA-256 `83201688dfa55420330766ef8b1c75954058cd4103ed10f4fee418979d5867c6`.

## Recommendation (not a measurement)

Any successor must freshly authorize its own process budget and qualify the current binary from a stable, non-updater path. V4's unused capacity and old-binary qualification do not transfer.
