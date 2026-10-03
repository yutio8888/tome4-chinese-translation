# r0a1 archive ordering note

The host issued `archive_agent` for r0a1 in the same tool batch as the `wd_rev_ok`
step that records archive-intent, so the two ran concurrently rather than strictly
in sequence. The recorded order still holds: STATE.json with
`archive_attempts_started=1` was written at 18:02:19.234Z, and Paseo reports
`archivedAt` 18:02:19.249Z. Harvest (raw output, native log) had already completed
at 18:02 before either step. archive-confirm then succeeded against the closed
snapshot. Later dispatches run archive_agent only after archive-intent returns.
