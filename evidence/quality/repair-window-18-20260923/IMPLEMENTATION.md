# Repair window 18 — implementation

- Executor scope: four frozen `mod-tome.lua` targets from batch 264; no other translation, terminology, rule, tool, handoff, catalog, migration, or `.ai` file was changed.
- `f36a77c67030a4ae4a985497a95f1efd368e8e9b5215ff60a484473f5c279299`: changed the ongoing effect message to `#Target#正被碾压。`.
- `f3756e2f2d7f9cf289f5d069c1921b1c338a6f919c993b75ae50ed92f8b46de7`: changed the companion behavior menu label `Standby` to `待命`.
- `f3bf7c41d4567349f7f4e239a7d8a6af82f2c66ffa2bcd12f5b5db4e73fa1ecf`: restored the surprise and offhand-replacement meaning in the first sentence; put the mainhand/unarmed damage sentence and the unarmed-hit result on the same second line; preserved the four `%d` arguments and their order. The target now has the source's two LF and two line-leading TAB pairs.
- `f431fee2ffd961fecdeb4c05a240d52dc59c1201ea6d081aa237d22dcb21c418`: corrected `trivial and in possession of my master`, restored `Ruby of Eldoral` as `艾德瑞尔红宝石`, used `他` consistently in the final sentence, and rendered the corrupted-name utterance as `他只能挤出自己名字走了样的读音：兹基克茨`. During the required sentence-by-sentence comparison, also corrected the plainly omitted `open and unattended`, `acquire a new phylactery`, and dragon-bone/mold relationships without rewriting the remaining faithful sentences.
- Proper names and talent names were checked in `mod-tome.lua`: `Z'quikzshl` uses `兹基克茨`, `Eldoral` uses `艾德瑞尔`, and `Offhand Jab` is the existing talent `副手猛击`.
- Source behavior and wording were checked read-only at fixed commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` with `git -C /workspace/t-engine4 show`.
- Source strings, source tags, argument order, printf placeholders, literal `%%`, markup, and all required LF/TAB positions remain unchanged from the frozen baseline.
- No advisory, pending item, or other repair was included. No staging, commit, push, or agent creation was performed; unrelated untracked files were preserved.

This is the unique EXECUTOR implementation record only. Full gates, independent REVIEW/FINAL_REVIEW, build, DONE_VERIFIED, publication, and lifecycle closure remain the host's responsibility.

## Cycle 1 bounded repair

- Applied confirmed finding `R0-ZQUIK-RITES-READINESS` only, within revision `f431fee2ffd961fecdeb4c05a240d52dc59c1201ea6d081aa237d22dcb21c418`.
- Replaced the exact target substring `我愚蠢的主人说我没有做巫妖的条件，我会引来不必要的关注` with `我愚蠢的主人说我还没准备好接受巫妖仪式，说我会引来不必要的关注`.
- No other text in the Z'quikzshl diary target or any other translation entry was changed in this repair. No rule, tool, terminology, handoff, catalog, migration, or `.ai` file was changed; no staging, commit, push, or agent creation was performed; unrelated untracked files were preserved.
