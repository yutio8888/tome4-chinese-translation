# Batch 338 adjudication chain interrupted

The first bd_close run was killed (host session ended) while the contextual-adjudication-chain was inside
prepare-evidence (CI gates 01–03 had passed, gate 04 was running). contextual-import, generate-adjudication
and adjudicate had all exited 0 (see review338-adjudication-chain.log; review338-chain.log is empty because
the wrapper was killed before it flushed, and no chain timing receipt was written). Nothing was committed.
The host reran only the remaining step, prepare-evidence, through timed_command
(review338-prepare-evidence.log / -timing.json), then continued the normal close steps.
