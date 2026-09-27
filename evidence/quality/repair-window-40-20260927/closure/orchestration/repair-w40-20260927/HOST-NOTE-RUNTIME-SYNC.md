# Host note: cross-component runtime sync (window 40)

The first FINAL-GATES run failed gate `06-runtime-collision-scan` with one collision. The runtime key `Sook's Runes and other Harmless Contraptions` (`entity name`) was fixed in Orcs (`50df66a4c3`, 苏克的符文与其他无害小玩意) but still read 苏克符文道具店 in two `mod-tome.lua` records (Gates of Morning and Last Hope store lists).

All three sources name the same store with the same string, so the reviewed Orcs text applies to every copy. See `RUNTIME-SYNC.json` for the source lines.

`SCOPE.allowed_files` was widened to include `mod-tome.lua`. The EXECUTOR dispatch `execute-06` replaces only those two targets with the byte-identical reviewed text. The host verification now expects the 23 workset revisions plus these 2 sync revisions. The migration queues both new revisions for normal re-review.

Lesson (repeat of window 35): at window setup, grep every workset source across all component files and list siblings in `RUNTIME-SYNC.json` from the start.
