execute-01 ran across UTC midnight (2026-09-27 -> 09-28). Codex injected a mid-turn
<environment_context> user block (record 326) plus a partial world_state that only changed
current_date. review_lifecycle._parse_native_final counted it as a new user turn and rejected
the harvest. Host added _codex_date_rollover(): skips exactly that pair (single input_text block,
full environment_context shape, next record world_state == {full:false, state:{environments:
{current_date:<same date>}}}). Harvest then succeeded; native audit 50 calls; exact diff 77.
The executor was archived before the successful harvest (archive-confirm recorded); the native
log was read from archived_sessions.
