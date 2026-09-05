# V5 execution-v3 pilot terminal report

## Decision

**NO_GO_HARNESS_CLI_DRIFT** (terminal for this task).

## Measured facts

The first authorized qualification process ran the frozen argv:

```text
agy models list --json
```

It exited `1` with stderr:

```text
Error: unexpected arguments: [list --json]
```

There was one `agy` process and zero inference calls. The stdout capture was empty. The
qualification therefore did not complete, and no model identity was established by this
attempt.

A corrected model-list retry, followed by the synthetic qualification request and cells A
and C, would require four additional processes. That would exceed the authorized total
budget of four after the one process already spent. No further process is authorized in
this task.

No `EVIDENCE-DRAFT`, synthetic inference response/capture, A response/capture, C
response/capture, `SCORES.json`, or experimental evidence was produced. The checked-in
`qualification/SYNTHETIC-REQUEST.txt` is only a frozen request fixture, not model evidence.

The ledger contains the one qualification process as two rows (START/FINISH), and all
process counters above are derived from it. No source, capture, ledger, gate, README,
experiment, state, predecessor, or other existing file was edited; this report only adds
`PILOT-RESULT.json` and `PILOT.md`.

## Integrity bindings

| Artifact | SHA-256 |
|---|---|
| `MANIFEST.json` | `fd282a90df800677d1c0ccc2932d2f73f8346b587997eff98ef722aa334488a2` |
| `PACKAGE-REVIEW-GATE.json` | `329fb2057e6ebfdaca712d35e61b1505f512aaf846a6fc2d28a34fbfd3d3895d` |
| `execution/LEDGER.jsonl` | `c06c291d94f3da07a4b2195a813f65c665f59a339fe5d0b898f365eef0b7b18b` |
| qualification stdout capture | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| qualification stderr capture | `0e0d8747e5ffe053dd7c5b330c9e67c9ef85a5740de515724f8b04b9e10398b2` |
| `frozen/REQUEST-MANIFEST.json` | `89747774b54d4263873b0419e22caba2840fc79f64b7033689ae26a27b8b30bc` |

## Recommendation (not a measurement)

Create a successor task that first freezes the current CLI-compatible model-list command
using offline installation evidence or a separately authorized qualification probe. Do not
assert the correct replacement command unless it is proved. After that, grant a new
four-process pilot authorization.
