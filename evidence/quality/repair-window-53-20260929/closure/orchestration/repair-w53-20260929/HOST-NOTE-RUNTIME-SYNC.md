# Host note: same-file runtime sync (window 53)

Window setup ran `check_siblings.py` and found one sibling: the Exploratory Farportal description of `d64daff63a` (section `shertul-fortress/grids.lua`) also exists as `55872e196b` in section `shertul-fortress-caldizar/grids.lua` of `mod-tome.lua`. Both have the same source and `_t` tag, so they share one runtime key. Until the sibling is synced, strict lint reports exactly one `runtime-collision`.

The fix was reviewed once, in `d64daff63a` (REVIEW r0a1 through FINAL f3a2, all OK). After FINAL passed, the EXECUTOR dispatch `execute-05` copies that reviewed target byte-for-byte into the caldizar record and changes nothing else. `SCOPE.allowed_files` already lists `mod-tome.lua`. Host verification expects the 18 workset revisions plus this 1 sync revision. The migration queues the new caldizar revision for normal re-review.
