# 已应用译文的独立复核报告

- 任务：`human-review-adjudication-20260923`
- 复核路线：`pi/cliproxyapi/gemini-3.8-flash-high`（串行，与 executor 裁决路线并行）
- 复核对象：本轮 executor 已应用的 95 条 target 修改
- 路线状态：`COMPLETE_ALL_ITEMS_REVIEWED`

## 复核结果汇总

| 状态 | 条数 |
| --- | --- |
| ok | 95 |

## 复核批次（串行）

| packet | 条数 | 结论 | raw 输出 SHA-256 |
| --- | --- | --- | --- |
| 1 | 20 | issue 0 / ok 20 / unclear 0 | `574074c737ea076e…` |
| 2 | 20 | issue 0 / ok 20 / unclear 0 | `c481c3ebdc40b386…` |
| 3 | 20 | issue 0 / ok 20 / unclear 0 | `5fa3da3054604f84…` |
| 4 | 20 | issue 0 / ok 20 / unclear 0 | `d28f4c06776e1355…` |
| 5 | 15 | issue 0 / ok 15 / unclear 0 | `7c5ed166bc0804d1…` |

## 复核质量评估

- **reviewer_route**：pi/cliproxyapi/gemini-3.8-flash-high
- **items_reviewed**：95
- **verdicts**
  - `ok`：95
  - `issue`：0
  - `unclear`：0
- **evidence_audit**
  - `source_citations_checked`：89
  - `source_citations_valid`：89
  - `fabricated_evidence_found`：0
  - `note`：所有 game/... 源码引用均在固定 commit 624a6732 下存在，未发现编造路径。
- **coverage_audit**
  - `packets`：5
  - `coverage_exact_in_all_packets`：True
  - `missing_items`：0
  - `extra_items`：0
- **independence**
  - `note`：reviewer 只读冻结 packet，未读取 executor 的 reason/verdict；结论独立形成。
  - `but`：reviewer 未被告知本轮修复动因，对「本次改动是否引入新不一致」这一判据覆盖不足。
- **orchestrator_independent_findings**：1
- **reviewer_miss**
  - `entry_id`：entry-00284
  - `what`：族内第三项 entry-00285（mod-tome.lua:987）仍为半角括号，形成族内不一致，reviewer 判 ok 且 new_issue_introduced=false。
  - `why_missed`：同族成员分属不同批次/单条审阅，packet 逐项给出时未并排呈现同族三项；逐项判据看不到横跨三项的风格分裂。
  - `proposed_fix_for_review_route`：后续 packet 应附「同 section 同族其他成员现值」，或增加专门的族一致性判据段落。
- **overall**：reviewer 路线在「改动本身是否正确」上可靠（95/95 且有真实证据）；在「改动是否引入跨条不一致」上存在系统性盲区，需 ORCHESTRATOR 的族扫描补足。
- **recorded_at**：2026-09-24T01:20:00Z

## ORCHESTRATOR 独立核验发现的遗漏

### entry-00284 — new_inconsistency_introduced

- `found_in_packet`：1
- `file`：mod-tome.lua
- `line`：987
- `class`：new_inconsistency_introduced
- `detail`：批次 01 把 Talent on hit(spell)（entry-00284，L986）与 Talent on hit(mindpower)（entry-00286，L988）的括号改为全角，但同一 section、同一句式族的 Talent on hit(nature)（entry-00285，L987）仍为半角，形成族内不一致。entry-00285 不在人工队列中（从未被审），两个端点被分别修正时无人看到中间项。
- `evidence`：['mod-tome.lua:986-988', 'CHANGE-LEDGER.json entry-00284/00286']
- `reviewer_missed`：True
- `reviewer_note`：reviewer-01（gemini-3.8-flash-high）对 entry-00284/00286 均判 ok 且 new_issue_introduced=false，未发现族内第三项仍是半角。
- `status`：pending_user_decision
- `proposed_action`：把 entry-00285 的半角括号一并改为全角，恢复族内一致；该条不在任何批次冻结集合，属跨批次对齐。
- `cross_file_scan`：全库按「同 section + 去括号归一化 source」扫描族内括号风格：mod-tome.lua 1 处（本项）、engine.lua 1 处（ActorTalents.lua:1244/1245，经 git 核对在 campaign 基线 d39131a8 即已存在，非本次引入）、mod-boot.lua 0 处。
- `pre_existing_sibling`：engine.lua:1244/1245 的（未学习）/(%d) 分裂为既存问题，不由本轮引入。
- `recorded_at`：2026-09-24T01:15:00Z


## 逐条复核明细

| entry | 文件:行 | executor 裁决 | 复核结论 | 是否引入新问题 | 证据 |
| --- | --- | --- | --- | --- | --- |
| entry-00105 | engine.lua:1697 | accepted | ok | 否 | terminology/tech.tsv:3 |
| entry-00110 | engine.lua:1779 | accepted | ok | 否 | terminology/places.tsv:46 |
| entry-00144 | mod-boot.lua:364 | accepted | ok | 否 | terminology/places.tsv:46 |
| entry-00111 | engine.lua:1800 | accepted | ok | 否 | terminology/society.tsv:34；terminology/classes.tsv:46 |
| entry-00145 | mod-boot.lua:385 | accepted | ok | 否 | terminology/society.tsv:34；terminology/classes.tsv:46 |
| entry-00112 | engine.lua:1823 | accepted_policy | ok | 否 | — |
| entry-00146 | mod-boot.lua:408 | accepted | ok | 否 | — |
| entry-00139 | mod-boot.lua:282 | accepted | ok | 否 | terminology/tech.tsv:3 |
| entry-00164 | mod-tome.lua:103 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:838 |
| entry-00165 | mod-tome.lua:104 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:860 |
| entry-00166 | mod-tome.lua:105 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:880 |
| entry-00191 | mod-tome.lua:249 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:4530 |
| entry-00195 | mod-tome.lua:277 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:5857 |
| entry-00198 | mod-tome.lua:353 | accepted | ok | 否 | game/modules/tome/class/Actor.lua:7805 |
| entry-00226 | mod-tome.lua:501 | accepted_policy | ok | 否 | game/modules/tome/class/Game.lua:1756 |
| entry-00231 | mod-tome.lua:510 | accepted | ok | 否 | game/modules/tome/class/Game.lua:2211；game/engines/default/engine/Map.lua:1508 |
| entry-00247 | mod-tome.lua:719 | accepted | ok | 否 | game/modules/tome/class/Object.lua:464 |
| entry-00284 | mod-tome.lua:986 | accepted_policy | ok | 否 | game/modules/tome/class/Object.lua:2127 |
| entry-00286 | mod-tome.lua:988 | accepted_policy | ok | 否 | game/modules/tome/class/Object.lua:2167 |
| entry-00288 | mod-tome.lua:1031 | accepted | ok | 否 | game/modules/tome/class/Object.lua:2305 |
| entry-00298 | mod-tome.lua:1115 | accepted | ok | 否 | game/modules/tome/class/Object.lua:199 |
| entry-00299 | mod-tome.lua:1116 | accepted | ok | 否 | game/modules/tome/class/Object.lua:199 |
| entry-00318 | mod-tome.lua:1223 | accepted | ok | 否 | game/modules/tome/class/Trap.lua:288 |
| entry-00344 | mod-tome.lua:1379 | accepted | ok | 否 | game/modules/tome/class/interface/Combat.lua:466 |
| entry-00354 | mod-tome.lua:1428 | accepted_policy | ok | 否 | game/modules/tome/class/interface/PartyIngredients.lua:89 |
| entry-00368 | mod-tome.lua:1579 | accepted | ok | 否 | game/modules/tome/class/interface/TooltipsData.lua:106；terminology/resources.tsv:Equilibrium=失衡值 |
| entry-00373 | mod-tome.lua:1689 | accepted | ok | 否 | game/modules/tome/class/interface/TooltipsData.lua:185 |
| entry-00374 | mod-tome.lua:1772 | accepted | ok | 否 | terminology/combat.tsv:Magic=魔力；game/modules/tome/class/interface/TooltipsData.lua:196 |
| entry-00395 | mod-tome.lua:2283 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:116 |
| entry-00396 | mod-tome.lua:2284 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:117 |
| entry-00397 | mod-tome.lua:2285 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:118 |
| entry-00398 | mod-tome.lua:2286 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:119 |
| entry-00399 | mod-tome.lua:2287 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:120 |
| entry-00400 | mod-tome.lua:2288 | accepted_policy | ok | 否 | game/modules/tome/class/interface/WorldAchievements.lua:121 |
| entry-00423 | mod-tome.lua:2694 | accepted | ok | 否 | game/modules/tome/data/achievements/kills.lua:268 |
| entry-00429 | mod-tome.lua:2788 | accepted | ok | 否 | terminology/places.tsv:Maj'Eyal=马基·埃亚尔；game/modules/tome/data/achievements/kills.lua:422 |
| entry-00443 | mod-tome.lua:2864 | accepted | ok | 否 | terminology/combat.tsv:cold=寒冷；game/modules/tome/data/achievements/talents.lua:36 |
| entry-00448 | mod-tome.lua:2886 | accepted | ok | 否 | game/modules/tome/data/birth/classes/adventurer.lua:135 |
| entry-00455 | mod-tome.lua:2932 | accepted | ok | 否 | game/modules/tome/data/birth/classes/celestial.lua:64 |
| entry-00458 | mod-tome.lua:2943 | accepted | ok | 否 | game/modules/tome/data/birth/classes/celestial.lua:144 |
| entry-00476 | mod-tome.lua:3046 | accepted | ok | 否 | game/modules/tome/data/birth/classes/psionic.lua:26 |
| entry-00489 | mod-tome.lua:3136 | accepted | ok | 否 | game/modules/tome/data/birth/classes/warrior.lua:264 |
| entry-00527 | mod-tome.lua:3748 | accepted | ok | 否 | game/modules/tome/data/birth/races/undead.lua:186 |
| entry-00553 | mod-tome.lua:4090 | accepted | ok | 否 | game/modules/tome/data/chats/alchemist-hermit.lua:366 |
| entry-00560 | mod-tome.lua:4118 | accepted | ok | 否 | game/modules/tome/data/chats/alchemist-last-hope.lua:153；mod-tome.lua:9510 |
| entry-00570 | mod-tome.lua:4681 | accepted | ok | 否 | game/modules/tome/data/chats/assassin-lord.lua:44 |
| entry-00574 | mod-tome.lua:5070 | accepted | ok | 否 | game/modules/tome/data/chats/gates-of-morning-main.lua:61 |
| entry-00604 | mod-tome.lua:5978 | accepted | ok | 否 | game/modules/tome/data/chats/shertul-fortress-butler.lua:175 |
| entry-00605 | mod-tome.lua:5979 | accepted | ok | 否 | game/modules/tome/data/chats/shertul-fortress-butler.lua:176 |
| entry-00620 | mod-tome.lua:6417 | accepted | ok | 否 | game/modules/tome/data/chats/tutorial-start.lua:48 |
| entry-00621 | mod-tome.lua:6472 | accepted | ok | 否 | game/modules/tome/data/chats/ukllmswwik.lua:59 |
| entry-00623 | mod-tome.lua:6557 | accepted | ok | 否 | game/modules/tome/data/chats/unremarkable-cave-fillarel.lua:32 |
| entry-00650 | mod-tome.lua:7048 | accepted | ok | 否 | game/modules/tome/data/damage_types.lua:3244；terminology/combat.tsv:156 |
| entry-00652 | mod-tome.lua:7054 | accepted | ok | 否 | game/modules/tome/data/damage_types.lua:3315；mod-tome.lua:7071 |
| entry-00657 | mod-tome.lua:7159 | accepted | ok | 否 | game/modules/tome/data/general/encounters/fareast.lua:57；mod-tome.lua:7155 |
| entry-00660 | mod-tome.lua:7191 | accepted | ok | 否 | game/modules/tome/data/general/encounters/maj-eyal.lua:81 |
| entry-00683 | mod-tome.lua:7393 | accepted | ok | 否 | game/modules/tome/data/general/events/rat-lich.lua:73 |
| entry-00684 | mod-tome.lua:7394 | accepted | ok | 否 | game/modules/tome/data/general/events/rat-lich.lua:99 |
| entry-00712 | mod-tome.lua:7985 | accepted | ok | 否 | game/modules/tome/data/general/npcs/aquatic_critter.lua:78 |
| entry-00713 | mod-tome.lua:8009 | accepted | ok | 否 | game/modules/tome/data/general/npcs/bear.lua:64 |
| entry-00722 | mod-tome.lua:8183 | accepted | ok | 否 | game/modules/tome/data/general/npcs/ghost.lua:83 |
| entry-00723 | mod-tome.lua:8187 | accepted | ok | 否 | game/modules/tome/data/general/npcs/ghost.lua:131；terminology/narrative.tsv:12 |
| entry-00728 | mod-tome.lua:8258 | accepted | ok | 否 | terminology/creatures.tsv:42；game/modules/tome/data/general/npcs/horror.lua:109 |
| entry-00731 | mod-tome.lua:8266 | accepted | ok | 否 | terminology/creatures.tsv:24；game/modules/tome/data/general/npcs/horror.lua:263 |
| entry-00733 | mod-tome.lua:8298 | accepted | ok | 否 | game/modules/tome/data/general/npcs/horror.lua:882 |
| entry-00740 | mod-tome.lua:8402 | accepted | ok | 否 | game/modules/tome/data/general/npcs/lich.lua:78 |
| entry-00746 | mod-tome.lua:8418 | accepted | ok | 否 | game/modules/tome/data/general/npcs/losgoroth.lua:75 |
| entry-00752 | mod-tome.lua:8515 | accepted | ok | 否 | game/modules/tome/data/general/npcs/naga.lua:54 |
| entry-00763 | mod-tome.lua:8718 | accepted | ok | 否 | game/modules/tome/data/general/npcs/shivgoroth.lua:59 |
| entry-00768 | mod-tome.lua:8734 | accepted | ok | 否 | game/modules/tome/data/general/npcs/skeleton.lua:104 |
| entry-00781 | mod-tome.lua:8969 | accepted | ok | 否 | game/modules/tome/data/general/npcs/venom-drake.lua:48 |
| entry-00804 | mod-tome.lua:9191 | deferred | ok | 否 | game/modules/tome/data/zones/rak-shor-pride/npcs.lua:121；game/modules/tome/data/general/objects/boss-artifacts-far-east.lua:83 |
| entry-00805 | mod-tome.lua:9194 | accepted | ok | 否 | game/modules/tome/data/general/objects/boss-artifacts-far-east.lua:513 |
| entry-00820 | mod-tome.lua:9332 | accepted | ok | 否 | game/modules/tome/data/general/objects/boss-artifacts-maj-eyal.lua:1445 |
| entry-00840 | mod-tome.lua:9487 | accepted | ok | 否 | game/modules/tome/data/general/objects/brotherhood-artifacts.lua:173 |
| entry-00852 | mod-tome.lua:9627 | accepted | ok | 否 | game/modules/tome/data/general/objects/egos/ammo.lua:513 |
| entry-00866 | mod-tome.lua:9858 | accepted | ok | 否 | game/modules/tome/data/general/objects/egos/boots.lua:205 |
| entry-00873 | mod-tome.lua:9973 | accepted | ok | 否 | game/modules/tome/data/general/objects/egos/cloak.lua:194 |
| entry-00980 | mod-tome.lua:11596 | accepted | ok | 否 | game/modules/tome/data/general/objects/quest-artifacts.lua:38 |
| entry-00984 | mod-tome.lua:11658 | accepted | ok | 否 | game/modules/tome/data/general/objects/quest-artifacts.lua:441 |
| entry-00992 | mod-tome.lua:12145 | accepted | ok | 否 | game/modules/tome/data/general/objects/special-artifacts.lua:70；terminology/combat.tsv:54 |
| entry-00997 | mod-tome.lua:12286 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts-far-east.lua:232 |
| entry-01000 | mod-tome.lua:12326 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts-maj-eyal.lua:73；terminology/combat.tsv:120 |
| entry-01001 | mod-tome.lua:12335 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts-maj-eyal.lua:189；terminology/combat.tsv:120 |
| entry-01002 | mod-tome.lua:12357 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts-maj-eyal.lua:382 |
| entry-01029 | mod-tome.lua:12548 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:662 |
| entry-01032 | mod-tome.lua:12552 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:691；terminology/combat.tsv:74 |
| entry-01038 | mod-tome.lua:12614 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:1197 |
| entry-01068 | mod-tome.lua:12825 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:3251 |
| entry-01074 | mod-tome.lua:12857 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:3642 |
| entry-01081 | mod-tome.lua:12872 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:3778 |
| entry-01085 | mod-tome.lua:12879 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:3876 |
| entry-01096 | mod-tome.lua:12927 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:4406 |
| entry-01116 | mod-tome.lua:13089 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:5962 |
| entry-01120 | mod-tome.lua:13125 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:6210；terminology/combat.tsv:9；terminology/combat.tsv:10；terminology/combat.tsv:120 |

