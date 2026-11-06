r6-opus (Opus 5.5, halfling Anorithil, 2026-11-05 03:35–07:40 incl. 1 wake; level 8, Kor'Pul cleared, Heart of the Gloom 2)
All 13 confirmed. 03 (args-order residue) fixed by host with explicit {1,2} on the only 3 affected entries (full scan of 68 official non-identity orders). 08 fixed only for the 7 named "%s is knocked back!" entries; the remaining ~63 logSeen "%s " leading-space entries need a user decision for a cross-batch sweep.

r6-opus part 2 (Opus 5.5, agent 71afca35, 2026-11-05 11:25–13:47; same character: Heart of the Gloom 3 boss The Withering Thing killed, Shatur, The Maze 1–2, level 10; level 12 goal not reached)
- r6-opus-14 confirmed, deferred (addon code): ", " separator is hard-coded in Game.lua:1740 table.concat(dams.descs, ", ") @624a67329fe2.
- r6-opus-15 confirmed: mod-tome.lua:26006 「伤害 : %s」 → 「伤害：%s」 (%s keeps its own leading space from inscriptions.lua:798-801). The list separator inside %s and in short_info (inscriptions.lua:806-808) is hard-coded: deferred (addon code).
- r6-opus-16 confirmed: mod-tome.lua:185 「%d 伤害反射」 → 「%d 反射」. Actor.lua:2580 embeds it as a damage description, so it renders as 「造成66 反射伤害」.
- r6-opus-17 confirmed: mod-tome.lua:186 「!」 → 「！」; 6809 space before #Target# removed.
- r6-opus-18 confirmed, deferred (addon code): ", " comes from shields.lua:26 add_name.
Fixed by host (3 small edits); changed units are reviewed blind in lite batch 0352.

r6-opus part 3 (Opus 5.5, agent 33a877c4, 2026-11-05 23:50–11-06 01:50; same character: lumberjack village boss, Last Hope, Old Forest 1–2; character died permanently at level 10, level 12 goal not reached)
- r6-opus-19/20/22/23/24/26/27/28 confirmed; fixed by executor codex/gpt-6.1-sol agent 047b7759 (host-checked): Thaloren forest unified to 自然精灵森林; 一种圣诗; full-width brackets in lumberjack reward popups and six damage modifiers (+点固定减伤); 50 #Target#/#Source# trailing spaces removed (mod-tome 16, orcs 31, ashes 2, possessors 1); glove hint quotes; Shield 最多持续 and stray space; Fountain of Life signed values.
- r6-opus-21 advisory: boss nameplate truncation is a layout limit; the name is correct.
- r6-opus-25/29 confirmed, deferred (addon code): engine Projectile tooltip and death-dialog unlock line are hard-coded English.
Changed units reviewed blind in lite batch 0386.
