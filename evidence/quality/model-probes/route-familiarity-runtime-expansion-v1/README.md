# Route-familiarity Runtime expansion v1

This is a zero-inference, deterministic 77-task / 156-row internal
contextual-review audit pool. `build.mjs` reads the frozen inputs through the
task's relative read-only `production-input` entry, validates terminal
fingerprints, typed envelope schemas, canonical dispatch/candidate identities,
and ordered source/target/context bindings, excludes overlap with the frozen
120- and 439-row pools, and emits an internal binding registry plus a separately
sanitized and filtered 66-task / 145-row future presentation. It makes no model
or network calls.

The frozen envelope mix is 76 modern plus one typed legacy envelope. Fixed
source fields are 70 `fixed_source_identity` plus 7 `fixed_source_commit`;
`terminology_snapshot` is always a string, including one legitimate empty
string, while fixed-source values and rendered briefings are non-empty.

Every retained row has some historical model exposure. The internal neutral
historical-route registry is intentionally imbalanced at 122/15/11/8 rows for
H1/H2/H3/H4; after hygiene exclusion the presentation remains imbalanced at
112/14/11/8. These cells are exposure strata, not scores or evidence of
memorization. Exact model-route provenance is intentionally withheld from child
and outbound artifacts. This is not an isolation set, and no absence of an
exact prior-route match is an isolation claim.

The future presentation contains only the retained neutral ID,
category/profile, source, target, and bounded fixed context. Eleven rows
(`RFR-0019`, `RFR-0021`, `RFR-0076`, `RFR-0077`, `RFR-0078`, `RFR-0113`,
`RFR-0131`, `RFR-0134`, `RFR-0137`, `RFR-0139`, and `RFR-0156`) are
mechanically classified as `CONTEXT_META_PROVENANCE_EXCLUDED` because their
historical contexts contain internal identity or review/adjudication/scope
history markers; their prose is not rewritten. Known main-game and DLC
absolute source paths are deterministically rewritten to stable neutral roots
while retaining useful component/file suffixes, and the 15 fixed-source commit
occurrences are replaced by one stable neutral marker. Unrecognized or residual
absolute paths fail closed. Internal bindings retain only raw and sanitized
context hashes/byte counts, dispositions, and rule IDs, not raw context text.

The frozen sanitation pass covers 31 rows / 52 absolute-path occurrences. Its
model-facing output contains 9 `<MAIN_GAME_ROOT>` and 43 `<DLC_ROOT>` markers.
The main marker absorbs the local `t-engine4` repository segment; the DLC marker
now also absorbs the local `tome4-dlcs` aggregation segment, so the public suffix
starts with the DLC aggregation child (for example `cults/...`) rather than
repeating the local aggregation directory. This intentional 43-occurrence text
change updates sanitized-context and output hashes without changing any row,
task, profile, category, H-cell, exclusion, path, or commit-neutralization count.
The complete presentation hygiene walk scans 1,771 key/value strings recursively
and rejects any independently delimited continuous hex token of 40 or more
characters.

The build report hashes the registry and presentation, and the experiment
record hashes those two artifacts plus the build report. All four final output
hashes are frozen externally in `build.mjs`; no JSON artifact contains or
depends on its own hash.

All later results are exploratory reference scores unless a separately frozen
formal design explicitly states otherwise.

Final generated artifact SHA-256 values are:

- registry: `9cc58a068801a707be0eca32a2597493d8fb2b6d64e37914355ac9cd2552d436`
- presentation: `6e8b2a3b485418fca4bdb9d777f4a7a572f0f872efdb27905e52080a23e11084`
- build report: `a0eeb216c4412f0dbb0ef3fcef1302294c09ea0c757a771cc21e280fff1fda2c`
- experiment record: `429ca530b95896e8e0f88021e88d8f9b33c292a96a5443b2ffb4526eb6e28eca`

Run locally from the repository root:

```bash
node --check evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/build.mjs
node --check evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/test-builder.mjs
node --check evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/verify.mjs
node evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/test-builder.mjs
node evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/build.mjs
node evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/verify.mjs
```
