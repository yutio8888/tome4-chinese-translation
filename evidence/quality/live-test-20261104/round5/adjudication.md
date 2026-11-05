r5-opus (Opus 5.5, 2026-11-04 22:40 – 11-05 02:41, GPU; level 9, beat Prox, Derth shops, Old Forest)
Fixed in 0338: 01 02 03 04 05 07 08 09 10 11 12 13 14 15 16 19 20 21 22 23 (see fix-report.md)
06 pending user: next level/previous level → 前往下一层/前往上一层 is terminology/places.tsv:16-17 preferred; in 这里有%s（…） it renders 这里有一个前往下一层 (ungrammatical). Changing it needs a terminology decision.
17 advisory: upstream :format branch in effect tooltip (Minimalist.lua:1166, ClassicPlayerDisplay.lua:180) needs a code hook.
18 advisory: Actor.lua:6803-6809 _t(speed_type) without tag falls back to the I18N nil table, last registered shield = effect subtype 护盾; changing the fallback would affect other untagged lookups.
14/22/23 held: the fixes need 9 new t() entries; first close of 0338 failed gate 05 (formal current version vector drift observed=(30317,29837,480) expected=(30308,29828,480)). Additions removed from 0338 and listed in pending-additions.txt until the user decides on bumping the frozen vector.
06/14/22/23 applied in 0341 after user approval 2026-11-05 (vector bumped to 30317).
