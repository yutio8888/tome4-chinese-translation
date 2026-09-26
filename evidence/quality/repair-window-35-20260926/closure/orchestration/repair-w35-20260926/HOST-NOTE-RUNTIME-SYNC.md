# Host note: cross-component runtime sync (window 35)

The first FINAL-GATES run failed gate `06-runtime-collision-scan` with one collision. The runtime key `#LIGHT_RED##Target# is out of sight of its master; direct control will break!` (`_t`) was fixed in Cults (`c26a569f`, 即将中断) but still read 中断了 in `mod-tome.lua` and `tome-orcs.lua`.

In all three components the source sends this message from `on_gain`, and control is lost later in `on_timeout`. That makes 即将中断 correct everywhere. See `RUNTIME-SYNC.json` for the source lines.

`SCOPE.allowed_files` was widened to include `mod-tome.lua` and `tome-orcs.lua`. The EXECUTOR dispatch `execute-04` replaces only those two targets with the byte-identical reviewed text. The host verification scripts now expect 23 changed revisions: 21 from the workset plus these 2 sync revisions. The migration queues both new revisions for normal re-review, so they do not inherit the tome sibling's old `done` state.
