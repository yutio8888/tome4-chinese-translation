# execute-02 terminal capture correction

The host first ran `wd_exec_done execute-02` with a wrong `updatedAt` (2026-10-01T07:59:24.104Z, copied from execute-01). It then made a stray call with no arguments. The stray call failed in every step and only wrote two empty-dispatch logs under `.artifacts/`, which the host deleted.

The first call harvested correctly and recorded archive intent. Neither depends on `updatedAt`:

- the report, the provenance and the native tool list come from the Codex rollout log;
- the exact diff was written to `HOST-EXACT-DIFF-POST-FIX1.json`.

No record stores a hash of `execute-02-terminal.json`. The host regenerated it with the observed status values:

- `updatedAt` 2026-10-01T08:07:11.486Z;
- `lastUserMessageAt` 2026-10-01T08:03:49.056Z;
- `attentionTimestamp` 2026-10-01T08:07:11.485Z.
