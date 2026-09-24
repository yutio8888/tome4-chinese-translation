# 已应用译文的独立复核报告

- 任务：`human-review-adjudication-20260923`
- 复核路线：`pi/cliproxyapi/gemini-3.8-flash-high`（串行，与 executor 裁决路线并行）
- 复核对象：本轮 executor 已应用的 386 条 target 修改
- 路线状态：`COMPLETE_ALL_ITEMS_REVIEWED`

## 复核结果汇总

| 状态 | 条数 |
| --- | --- |
| issue | 1 |
| ok | 385 |

## 复核批次（串行）

| packet | 条数 | 结论 | raw 输出 SHA-256 |
| --- | --- | --- | --- |
| 1 | 20 | issue 0 / ok 20 / unclear 0 | `574074c737ea076e…` |
| 2 | 20 | issue 0 / ok 20 / unclear 0 | `c481c3ebdc40b386…` |
| 3 | 20 | issue 0 / ok 20 / unclear 0 | `5fa3da3054604f84…` |
| 4 | 20 | issue 0 / ok 20 / unclear 0 | `d28f4c06776e1355…` |
| 5 | 15 | issue 0 / ok 15 / unclear 0 | `7c5ed166bc0804d1…` |
| 6 | 20 | issue 0 / ok 20 / unclear 0 | `87e958513ef4f229…` |
| 7 | 20 | issue 0 / ok 20 / unclear 0 | `132ad05f8695b935…` |
| 8 | 20 | issue 0 / ok 20 / unclear 0 | `185a18f5c943534c…` |
| 9 | 20 | issue 0 / ok 20 / unclear 0 | `fba2231685488f0e…` |
| 10 | 20 | issue 0 / ok 20 / unclear 0 | `254e062a01eab660…` |
| 11 | 20 | issue 0 / ok 20 / unclear 0 | `51fc4f3dd0b60aa4…` |
| 12 | 20 | issue 1 / ok 19 / unclear 0 | `9205347373f0d93b…` |
| 13 | 20 | issue 0 / ok 20 / unclear 0 | `4e298bdae5efb277…` |
| 14 | 20 | issue 0 / ok 20 / unclear 0 | `fd8787ab93353dfa…` |
| 15 | 20 | ok 20 | `7ee41c7e3b96cb11…` |
| 16 | 20 | ok 20 | `e5c9ea33c0563b59…` |
| 17 | 20 | ok 20 | `1bdb6c0e7232ae2e…` |
| 18 | 20 | ok 20 | `574e5e68faafb917…` |
| 19 | 20 | ok 20 | `eb4e3a928ea0dfd7…` |
| 20 | 11 | ok 11 | `be2eb12b83d93851…` |

## 复核质量评估

- **reviewer_route**：pi/cliproxyapi/gemini-3.8-flash-high
- **items_reviewed**：386
- **verdicts**
  - `ok`：385
  - `issue`：1
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
- **orchestrator_independent_findings**：2
- **reviewer_miss**
  - `entry_id`：entry-00284
  - `what`：族内第三项 entry-00285（mod-tome.lua:987）仍为半角括号，形成族内不一致，reviewer 判 ok 且 new_issue_introduced=false。
  - `why_missed`：同族成员分属不同批次/单条审阅，packet 逐项给出时未并排呈现同族三项；逐项判据看不到横跨三项的风格分裂。
  - `proposed_fix_for_review_route`：后续 packet 应附「同 section 同族其他成员现值」，或增加专门的族一致性判据段落。
- **overall**：reviewer 路线在「改动本身是否正确」上可靠（95/95 且有真实证据）；在「改动是否引入跨条不一致」上存在系统性盲区，需 ORCHESTRATOR 的族扫描补足。
- **recorded_at**：2026-09-24T02:59:37.669537+00:00
- **verdict**：reviewer 路线在「改动本身是否正确」上可靠，并成功捕获 1 项实质术语缺陷；在「改动是否引入跨条不一致」上仍需 ORCHESTRATOR 的族扫描补足（1 项遗漏）。

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

### entry-01891 — reviewer_finding_upheld

- `found_in_packet`：12
- `file`：mod-tome.lua
- `line`：25019
- `class`：reviewer_finding_upheld
- `detail`：reviewer 指出 batch-07（hrq-00291）把 tooltip「用粘液覆盖地面。」改成「用天然粘液覆盖地面。」，而 natural mucus 是 damage type（固定源 game/modules/tome/data/damage_types.lua:3704），本仓固定译名为「自然粘液」（mod-tome.lua:7077）。改动既把 Nature 误作与人工相对的「天然」，又造成同源术语两译。
- `evidence`：['game/modules/tome/data/damage_types.lua:3704', 'mod-tome.lua:7077', 'mod-tome.lua:25019']
- `orchestrator_action`：独立核验确认成立；已将 tooltip 改为「用自然粘液覆盖地面。」与 damage type 对齐，lint --strict 通过。
- `reviewer_missed`：False
- `status`：resolved
- `recorded_at`：2026-09-24T03:05:00Z


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
| entry-01127 | mod-tome.lua:13176 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:6742 |
| entry-01132 | mod-tome.lua:13192 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:6897 |
| entry-01137 | mod-tome.lua:13200 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:6960 |
| entry-01149 | mod-tome.lua:13243 | accepted | ok | 否 | terminology/resources.tsv:5 Vim=活力值 |
| entry-01155 | mod-tome.lua:13277 | accepted | ok | 否 | terminology/narrative.tsv:12 fearscape=恶魔空间 |
| entry-01156 | mod-tome.lua:13278 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:7656 |
| entry-01160 | mod-tome.lua:13294 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:7919 |
| entry-01162 | mod-tome.lua:13310 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:8027 |
| entry-01163 | mod-tome.lua:13314 | accepted | ok | 否 | game/modules/tome/data/general/objects/world-artifacts.lua:8068 |
| entry-01193 | mod-tome.lua:13635 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:138 |
| entry-01194 | mod-tome.lua:13641 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:156 |
| entry-01196 | mod-tome.lua:13650 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:183 |
| entry-01198 | mod-tome.lua:13656 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:201 |
| entry-01201 | mod-tome.lua:13665 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:228 |
| entry-01205 | mod-tome.lua:13677 | accepted | ok | 否 | game/modules/tome/data/ingredients.lua:264 |
| entry-01210 | mod-tome.lua:13785 | accepted | ok | 否 | game/modules/tome/data/lore/age-allure.lua:67 |
| entry-01214 | mod-tome.lua:14196 | accepted | ok | 否 | game/modules/tome/data/lore/angolwen.lua:27 |
| entry-01215 | mod-tome.lua:14230 | accepted | ok | 否 | game/modules/tome/data/lore/angolwen.lua:50 |
| entry-01216 | mod-tome.lua:14450 | accepted | ok | 否 | game/modules/tome/data/lore/daikara.lua:70 |
| entry-01218 | mod-tome.lua:14722 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:82 |
| entry-01220 | mod-tome.lua:14814 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:134 |
| entry-01221 | mod-tome.lua:14988 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:230 |
| entry-01222 | mod-tome.lua:15094 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:292 |
| entry-01223 | mod-tome.lua:15168 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:338 |
| entry-01224 | mod-tome.lua:15300 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:413 |
| entry-01225 | mod-tome.lua:15366 | accepted | ok | 否 | game/modules/tome/data/lore/elvala.lua:455；terminology/creatures.tsv:234 luminous horror=金色恐魔 |
| entry-01228 | mod-tome.lua:15875 | accepted | ok | 否 | game/modules/tome/data/lore/fun.lua:217 |
| entry-01247 | mod-tome.lua:16562 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:17 |
| entry-01256 | mod-tome.lua:16683 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:36 |
| entry-01259 | mod-tome.lua:16826 | accepted | ok | 否 | game/modules/tome/data/lore/last-hope.lua:151 |
| entry-01267 | mod-tome.lua:17570 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:41；mod-tome.lua:17569 |
| entry-01270 | mod-tome.lua:17594 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:65 |
| entry-01271 | mod-tome.lua:17598 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:73 |
| entry-01272 | mod-tome.lua:17618 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:90；terminology/narrative.tsv:76 old forest=古老森林 |
| entry-01273 | mod-tome.lua:17637 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:103 |
| entry-01275 | mod-tome.lua:17677 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:129 |
| entry-01277 | mod-tome.lua:17714 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:154 |
| entry-01278 | mod-tome.lua:17728 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:166 |
| entry-01280 | mod-tome.lua:17737 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:182 |
| entry-01282 | mod-tome.lua:17791 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:218 |
| entry-01283 | mod-tome.lua:17826 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:241 |
| entry-01286 | mod-tome.lua:17921 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:329 |
| entry-01292 | mod-tome.lua:18000 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:388 |
| entry-01294 | mod-tome.lua:18019 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:403 |
| entry-01296 | mod-tome.lua:18037 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:417 |
| entry-01302 | mod-tome.lua:18083 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:455 |
| entry-01306 | mod-tome.lua:18119 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:483 |
| entry-01308 | mod-tome.lua:18137 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:497 |
| entry-01310 | mod-tome.lua:18155 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:511 |
| entry-01312 | mod-tome.lua:18235 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:570 |
| entry-01313 | mod-tome.lua:18334 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:624 |
| entry-01314 | mod-tome.lua:18345 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:636 |
| entry-01315 | mod-tome.lua:18375 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:669 |
| entry-01316 | mod-tome.lua:18410 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:693 |
| entry-01317 | mod-tome.lua:18417 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:702 |
| entry-01318 | mod-tome.lua:18444 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:721 |
| entry-01319 | mod-tome.lua:18474 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:742 |
| entry-01320 | mod-tome.lua:18509 | accepted | ok | 否 | game/modules/tome/data/lore/misc.lua:769 |
| entry-01328 | mod-tome.lua:19211 | accepted | ok | 否 | game/modules/tome/data/lore/sandworm.lua:28 |
| entry-01333 | mod-tome.lua:19365 | accepted | ok | 否 | game/modules/tome/data/lore/shertul.lua:40 |
| entry-01382 | mod-tome.lua:20175 | accepted | ok | 否 | game/modules/tome/data/quests/charred-scar.lua:29；terminology/classes.tsv:8 |
| entry-01384 | mod-tome.lua:20177 | accepted | ok | 否 | game/modules/tome/data/quests/charred-scar.lua:33 |
| entry-01385 | mod-tome.lua:20178 | accepted | ok | 否 | game/modules/tome/data/quests/charred-scar.lua:34 |
| entry-01386 | mod-tome.lua:20179 | accepted | ok | 否 | game/modules/tome/data/quests/charred-scar.lua:37 |
| entry-01389 | mod-tome.lua:20192 | accepted | ok | 否 | game/modules/tome/data/quests/deep-bellow.lua:23 |
| entry-01391 | mod-tome.lua:20194 | accepted | ok | 否 | game/modules/tome/data/quests/deep-bellow.lua:25 |
| entry-01392 | mod-tome.lua:20195 | accepted | ok | 否 | game/modules/tome/data/quests/deep-bellow.lua:26 |
| entry-01400 | mod-tome.lua:20216 | accepted | ok | 否 | game/modules/tome/data/quests/east-portal.lua:45 |
| entry-01408 | mod-tome.lua:20263 | accepted | ok | 否 | game/modules/tome/data/quests/high-peak.lua:27；terminology/society.tsv:2 |
| entry-01410 | mod-tome.lua:20265 | accepted | ok | 否 | game/modules/tome/data/quests/high-peak.lua:29 |
| entry-01424 | mod-tome.lua:20357 | accepted | ok | 否 | game/modules/tome/data/quests/kryl-feijan-escape.lua:29 |
| entry-01432 | mod-tome.lua:20426 | accepted | ok | 否 | game/modules/tome/data/quests/love-melinda.lua:37 |
| entry-01438 | mod-tome.lua:20463 | accepted | ok | 否 | game/modules/tome/data/quests/master-jeweler.lua:23 |
| entry-01462 | mod-tome.lua:20631 | accepted | ok | 否 | game/modules/tome/data/quests/staff-absorption.lua:28 |
| entry-01463 | mod-tome.lua:20634 | accepted | ok | 否 | game/modules/tome/data/quests/staff-absorption.lua:32 |
| entry-01468 | mod-tome.lua:20691 | accepted | ok | 否 | game/modules/tome/data/quests/start-dwarf.lua:26 |
| entry-01474 | mod-tome.lua:20754 | accepted | ok | 否 | game/modules/tome/data/quests/start-undead.lua:24 |
| entry-01479 | mod-tome.lua:20781 | accepted | ok | 否 | game/modules/tome/data/quests/starter-zones.lua:29 |
| entry-01486 | mod-tome.lua:20813 | accepted | ok | 否 | game/modules/tome/data/quests/temple-of-creation.lua:25 |
| entry-01491 | mod-tome.lua:20857 | accepted | ok | 否 | game/modules/tome/data/quests/tutorial.lua:23 |
| entry-01498 | mod-tome.lua:20894 | accepted | ok | 否 | game/modules/tome/data/quests/wild-wild-east.lua:26 |
| entry-01509 | mod-tome.lua:21029 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/chants.lua:386 |
| entry-01514 | mod-tome.lua:21091 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/combat.lua:217 |
| entry-01516 | mod-tome.lua:21110 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/crusader.lua:59 |
| entry-01517 | mod-tome.lua:21116 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/crusader.lua:123 |
| entry-01518 | mod-tome.lua:21122 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/crusader.lua:176；game/modules/tome/data/timed_effects/other.lua:171 |
| entry-01536 | mod-tome.lua:21483 | accepted | ok | 否 | game/modules/tome/data/talents/celestial/radiance.lua:41 |
| entry-01554 | mod-tome.lua:21815 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/bow-threading.lua:120 |
| entry-01557 | mod-tome.lua:21879 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/chronomancer.lua:41 |
| entry-01563 | mod-tome.lua:21913 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/chronomancy.lua:155 |
| entry-01565 | mod-tome.lua:21925 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/chronomancy.lua:206 |
| entry-01586 | mod-tome.lua:22102 | accepted | ok | 否 | terminology/society.tsv:29；game/modules/tome/data/talents/chronomancy/induced-phenomena.lua:281 |
| entry-01588 | mod-tome.lua:22122 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/matter.lua:151 |
| entry-01605 | mod-tome.lua:22286 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/spacetime-folding.lua:201 |
| entry-01617 | mod-tome.lua:22388 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/spellbinding.lua:88 |
| entry-01625 | mod-tome.lua:22512 | accepted | ok | 否 | game/modules/tome/data/talents/chronomancy/temporal-hounds.lua:235 |
| entry-01659 | mod-tome.lua:22839 | accepted | ok | 否 | game/modules/tome/data/talents/corruptions/plague.lua:251 |
| entry-01661 | mod-tome.lua:22895 | accepted | ok | 否 | game/modules/tome/data/talents/corruptions/rot.lua:220；terminology/creatures.tsv:20 |
| entry-01703 | mod-tome.lua:23255 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/artifice.lua:816 |
| entry-01706 | mod-tome.lua:23297 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/called-shots.lua:236 |
| entry-01709 | mod-tome.lua:23310 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/cunning.lua:24 |
| entry-01711 | mod-tome.lua:23313 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/cunning.lua:26 |
| entry-01718 | mod-tome.lua:23329 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/cunning.lua:34 |
| entry-01727 | mod-tome.lua:23437 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/poisons.lua:429 |
| entry-01732 | mod-tome.lua:23449 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/poisons.lua:636 |
| entry-01740 | mod-tome.lua:23519 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/stealth.lua:148 |
| entry-01751 | mod-tome.lua:23647 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/traps.lua:654 |
| entry-01767 | mod-tome.lua:23757 | accepted | ok | 否 | game/modules/tome/data/talents/cunning/traps.lua:1550 |
| entry-01785 | mod-tome.lua:24033 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/cursed.lua:25 |
| entry-01788 | mod-tome.lua:24039 | accepted | ok | 否 | terminology/resources.tsv:Hate；game/modules/tome/data/talents/cursed/cursed.lua:28 |
| entry-01803 | mod-tome.lua:24129 | accepted | ok | 否 | terminology/combat.tsv:darkness；game/modules/tome/data/talents/cursed/darkness.lua:435 |
| entry-01804 | mod-tome.lua:24135 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/darkness.lua:478 |
| entry-01823 | mod-tome.lua:24366 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/primal-magic.lua:116；mod-tome.lua:24365 |
| entry-01835 | mod-tome.lua:24511 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/shadows.lua:468 |
| entry-01838 | mod-tome.lua:24528 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/shadows.lua:651 |
| entry-01839 | mod-tome.lua:24530 | accepted | ok | 否 | game/modules/tome/data/talents/cursed/shadows.lua:669 |
| entry-01851 | mod-tome.lua:24737 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/corrosive-blades.lua:52 |
| entry-01861 | mod-tome.lua:24890 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/eyals-fury.lua:76；game/modules/tome/data/timed_effects/physical.lua:2886 |
| entry-01868 | mod-tome.lua:24956 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/fungus.lua:38 |
| entry-01870 | mod-tome.lua:24969 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/fungus.lua:101 |
| entry-01891 | mod-tome.lua:25019 | accepted | issue | 是 | game/modules/tome/data/talents/gifts/gifts.lua:38；game/modules/tome/data/damage_types.lua:3704；game/modules/tome/data/locales/zh_hans.lua:7099 |
| entry-01895 | mod-tome.lua:25031 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/gifts.lua:53 |
| entry-01899 | mod-tome.lua:25114 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/malleable-body.lua:37；terminology/combat.tsv:Resistances |
| entry-01913 | mod-tome.lua:25288 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/ooze.lua:116 |
| entry-01919 | mod-tome.lua:25331 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/oozing-blades.lua:76 |
| entry-01924 | mod-tome.lua:25467 | accepted | ok | 否 | game/modules/tome/data/talents/gifts/storm-drake.lua:194 |
| entry-01976 | mod-tome.lua:25875 | accepted | ok | 否 | game/modules/tome/data/talents/misc/horrors.lua:173 |
| entry-01980 | mod-tome.lua:25892 | accepted | ok | 否 | game/modules/tome/data/talents/misc/horrors.lua:394 |
| entry-01989 | mod-tome.lua:25981 | accepted | ok | 否 | game/modules/tome/data/talents/misc/inscriptions.lua:252 |
| entry-02015 | mod-tome.lua:26343 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:970 |
| entry-02022 | mod-tome.lua:26417 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:1737 |
| entry-02023 | mod-tome.lua:26441 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:1986；terminology/combat.tsv:cold |
| entry-02024 | mod-tome.lua:26456 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:2134 |
| entry-02025 | mod-tome.lua:26476 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:2331 |
| entry-02027 | mod-tome.lua:26488 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:2364 |
| entry-02028 | mod-tome.lua:26499 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:2438 |
| entry-02032 | mod-tome.lua:26539 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:2757 |
| entry-02043 | mod-tome.lua:26615 | accepted | ok | 否 | game/modules/tome/data/talents/misc/npcs.lua:3312 |
| entry-02069 | mod-tome.lua:26910 | accepted | ok | 否 | game/modules/tome/data/talents/misc/races.lua:765；terminology/creatures.tsv:orc |
| entry-02074 | mod-tome.lua:27062 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/absorption.lua:388 |
| entry-02081 | mod-tome.lua:27179 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/discharge.lua:104 |
| entry-02097 | mod-tome.lua:27318 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/dream-smith.lua:229 |
| entry-02103 | mod-tome.lua:27380 | accepted | ok | 否 | terminology/resources.tsv:2 Stamina=体力值；game/modules/tome/data/talents/psionic/feedback.lua:139 |
| entry-02106 | mod-tome.lua:27408 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/finer-energy-manipulations.lua:178 |
| entry-02107 | mod-tome.lua:27420 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/focus.lua:61 |
| entry-02109 | mod-tome.lua:27517 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/mental-discipline.lua:34 |
| entry-02110 | mod-tome.lua:27521 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/mental-discipline.lua:51 |
| entry-02128 | mod-tome.lua:27692 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/projection.lua:535 |
| entry-02148 | mod-tome.lua:27892 | accepted | ok | 否 | game/modules/tome/data/talents/psionic/slumber.lua:243；game/modules/tome/data/timed_effects/other.lua:2078 |
| entry-02149 | mod-tome.lua:27906 | accepted | ok | 否 | terminology/combat.tsv:133 Global speed=全局速度；game/modules/tome/data/talents/psionic/solipsism.lua:61 |
| entry-02153 | mod-tome.lua:27929 | accepted | ok | 否 | terminology/combat.tsv:143 Mental Save=精神豁免；game/modules/tome/data/talents/psionic/solipsism.lua:193 |
| entry-02187 | mod-tome.lua:28406 | accepted | ok | 否 | game/modules/tome/data/talents/spells/conveyance.lua:163 |
| entry-02189 | mod-tome.lua:28417 | accepted | ok | 否 | game/modules/tome/data/talents/spells/conveyance.lua:281 |
| entry-02191 | mod-tome.lua:28437 | accepted | ok | 否 | game/modules/tome/data/talents/spells/conveyance.lua:349 |
| entry-02192 | mod-tome.lua:28450 | accepted | ok | 否 | game/modules/tome/data/talents/spells/death.lua:66 |
| entry-02210 | mod-tome.lua:28797 | accepted | ok | 否 | game/modules/tome/data/talents/spells/explosives.lua:165 |
| entry-02227 | mod-tome.lua:29143 | accepted | ok | 否 | terminology/combat.tsv:41 daze=眩晕；game/modules/tome/data/talents/spells/master-necromancer.lua:58 |
| entry-02252 | mod-tome.lua:29537 | accepted | ok | 否 | game/modules/tome/data/talents/spells/spells.lua:30 |
| entry-02258 | mod-tome.lua:29549 | accepted | ok | 否 | game/modules/tome/data/talents/spells/spells.lua:36 |
| entry-02267 | mod-tome.lua:29640 | accepted | ok | 否 | game/modules/tome/data/talents/spells/staff-combat.lua:186 |
| entry-02273 | mod-tome.lua:29694 | accepted | ok | 否 | game/modules/tome/data/talents/spells/stone.lua:128 |
| entry-02277 | mod-tome.lua:29743 | accepted | ok | 否 | terminology/talents.tsv:189 Time Shield=时间盾；game/modules/tome/data/talents/spells/temporal.lua:79 |
| entry-02303 | mod-tome.lua:30008 | accepted | ok | 否 | terminology/talents.tsv:129 Tumble=翻筋斗；game/modules/tome/data/talents/techniques/acrobatics.lua:270 |
| entry-02306 | mod-tome.lua:30039 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/agility.lua:263；game/modules/tome/data/talents/techniques/agility.lua:281 |
| entry-02312 | mod-tome.lua:30077 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/archery.lua:485 |
| entry-02326 | mod-tome.lua:30194 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/bloodthirst.lua:87 |
| entry-02327 | mod-tome.lua:30200 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/bloodthirst.lua:122 |
| entry-02337 | mod-tome.lua:30288 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/combat-training.lua:106 |
| entry-02345 | mod-tome.lua:30379 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/dualweapon.lua:205 |
| entry-02354 | mod-tome.lua:30444 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/excellence.lua:64 |
| entry-02360 | mod-tome.lua:30524 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/grappling.lua:144 |
| entry-02380 | mod-tome.lua:30682 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/munitions.lua:388 |
| entry-02381 | mod-tome.lua:30692 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/munitions.lua:412 |
| entry-02392 | mod-tome.lua:30812 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/sniper.lua:93 |
| entry-02393 | mod-tome.lua:30818 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/sniper.lua:146 |
| entry-02394 | mod-tome.lua:30824 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/sniper.lua:194 |
| entry-02422 | mod-tome.lua:30940 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/techniques.lua:44 |
| entry-02425 | mod-tome.lua:30968 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/techniques.lua:86 |
| entry-02426 | mod-tome.lua:30970 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/techniques.lua:87 |
| entry-02427 | mod-tome.lua:30972 | accepted | ok | 否 | game/modules/tome/data/talents/techniques/techniques.lua:88 |
| entry-02428 | mod-tome.lua:30976 | accepted | ok | 否 | — |
| entry-02435 | mod-tome.lua:31034 | accepted | ok | 否 | — |
| entry-02451 | mod-tome.lua:31195 | accepted | ok | 否 | — |
| entry-02466 | mod-tome.lua:31322 | accepted | ok | 否 | — |
| entry-02474 | mod-tome.lua:31333 | accepted | ok | 否 | — |
| entry-02489 | mod-tome.lua:31513 | accepted | ok | 否 | — |
| entry-02500 | mod-tome.lua:31700 | accepted | ok | 否 | — |
| entry-02522 | mod-tome.lua:32371 | accepted | ok | 否 | — |
| entry-02523 | mod-tome.lua:32407 | accepted | ok | 否 | — |
| entry-02538 | mod-tome.lua:33287 | accepted | ok | 否 | — |
| entry-02541 | mod-tome.lua:33605 | accepted | ok | 否 | — |
| entry-02545 | mod-tome.lua:33711 | accepted | ok | 否 | — |
| entry-02552 | mod-tome.lua:33838 | accepted | ok | 否 | — |
| entry-02555 | mod-tome.lua:34022 | accepted | ok | 否 | — |
| entry-02557 | mod-tome.lua:34056 | accepted | ok | 否 | — |
| entry-02565 | mod-tome.lua:34230 | accepted | ok | 否 | — |
| entry-02570 | mod-tome.lua:34330 | accepted | ok | 否 | — |
| entry-02599 | mod-tome.lua:34882 | accepted | ok | 否 | — |
| entry-02601 | mod-tome.lua:34884 | accepted | ok | 否 | — |
| entry-02636 | mod-tome.lua:35331 | accepted | ok | 否 | — |
| entry-02637 | mod-tome.lua:35332 | accepted | ok | 否 | game/modules/tome/data/timed_effects/magical.lua:2442；mod-tome.lua:35328 |
| entry-02638 | mod-tome.lua:35347 | accepted | ok | 否 | game/modules/tome/data/timed_effects/magical.lua:2527 |
| entry-02694 | mod-tome.lua:35928 | accepted | ok | 否 | terminology/combat.tsv:cooldown=冷却；game/modules/tome/data/timed_effects/mental.lua:348 |
| entry-02740 | mod-tome.lua:36441 | accepted | ok | 否 | terminology/talents.tsv:taints=污印；game/modules/tome/data/timed_effects/other.lua:351 |
| entry-02747 | mod-tome.lua:36505 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:799 |
| entry-02759 | mod-tome.lua:36574 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:1392 |
| entry-02763 | mod-tome.lua:36582 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:1477 |
| entry-02764 | mod-tome.lua:36593 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:1532；mod-tome.lua:36582 |
| entry-02765 | mod-tome.lua:36600 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:1699 |
| entry-02775 | mod-tome.lua:36662 | accepted | ok | 否 | terminology/combat.tsv:cold=寒冷；game/modules/tome/data/timed_effects/other.lua:2297 |
| entry-02789 | mod-tome.lua:36707 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:2635；game/modules/tome/data/timed_effects/other.lua:2658 |
| entry-02790 | mod-tome.lua:36739 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:2890 |
| entry-02798 | mod-tome.lua:36788 | accepted | ok | 否 | terminology/combat.tsv:Magic=魔力；game/modules/tome/data/timed_effects/other.lua:3222 |
| entry-02805 | mod-tome.lua:36800 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:3336 |
| entry-02806 | mod-tome.lua:36802 | accepted | ok | 否 | game/modules/tome/data/timed_effects/other.lua:3354 |
| entry-02830 | mod-tome.lua:37192 | accepted | ok | 否 | game/modules/tome/data/timed_effects/physical.lua:1242；mod-tome.lua:37193 |
| entry-02846 | mod-tome.lua:37383 | accepted | ok | 否 | game/modules/tome/data/timed_effects/physical.lua:2112 |
| entry-02849 | mod-tome.lua:37431 | accepted | ok | 否 | game/modules/tome/data/timed_effects/physical.lua:2530；mod-tome.lua:37433 |
| entry-02856 | mod-tome.lua:37514 | accepted | ok | 否 | game/modules/tome/data/timed_effects/physical.lua:2881 |
| entry-02858 | mod-tome.lua:37532 | accepted | ok | 否 | game/modules/tome/data/timed_effects/physical.lua:3045 |
| entry-02866 | mod-tome.lua:37558 | accepted | ok | 否 | — |
| entry-02921 | mod-tome.lua:37978 | accepted | ok | 否 | — |
| entry-02927 | mod-tome.lua:38083 | accepted | ok | 否 | — |
| entry-02929 | mod-tome.lua:38122 | accepted | ok | 否 | — |
| entry-02957 | mod-tome.lua:38422 | accepted | ok | 否 | — |
| entry-02967 | mod-tome.lua:38557 | accepted | ok | 否 | — |
| entry-02973 | mod-tome.lua:38568 | accepted | ok | 否 | — |
| entry-03023 | mod-tome.lua:39312 | accepted | ok | 否 | — |
| entry-03025 | mod-tome.lua:39318 | accepted | ok | 否 | — |
| entry-03027 | mod-tome.lua:39320 | accepted | ok | 否 | — |
| entry-03058 | mod-tome.lua:39725 | accepted | ok | 否 | — |
| entry-03092 | mod-tome.lua:40038 | accepted | ok | 否 | — |
| entry-03167 | mod-tome.lua:41138 | accepted | ok | 否 | — |
| entry-03735 | tome-orcs.lua:350 | accepted | ok | 否 | — |
| entry-03738 | tome-orcs.lua:410 | accepted | ok | 否 | — |
| entry-03741 | tome-orcs.lua:426 | accepted | ok | 否 | — |
| entry-03747 | tome-orcs.lua:467 | accepted | ok | 否 | — |
| entry-03748 | tome-orcs.lua:474 | accepted | ok | 否 | — |
| entry-03799 | tome-orcs.lua:1499 | accepted | ok | 否 | — |
| entry-03801 | tome-orcs.lua:1509 | accepted | ok | 否 | — |
| entry-03811 | tome-orcs.lua:1569 | accepted | ok | 否 | — |
| entry-03815 | tome-orcs.lua:1613 | accepted | ok | 否 | — |
| entry-03823 | tome-orcs.lua:1740 | accepted | ok | 否 | — |
| entry-03849 | tome-orcs.lua:2195 | accepted | ok | 否 | — |
| entry-03851 | tome-orcs.lua:2218 | accepted | ok | 否 | — |
| entry-03852 | tome-orcs.lua:2523 | accepted | ok | 否 | — |
| entry-03853 | tome-orcs.lua:2545 | accepted | ok | 否 | — |
| entry-03854 | tome-orcs.lua:2559 | accepted | ok | 否 | — |
| entry-03856 | tome-orcs.lua:2625 | accepted | ok | 否 | — |
| entry-03860 | tome-orcs.lua:2690 | accepted | ok | 否 | — |
| entry-03864 | tome-orcs.lua:2808 | accepted | ok | 否 | — |
| entry-03865 | tome-orcs.lua:2874 | accepted | ok | 否 | — |
| entry-03875 | tome-orcs.lua:3579 | accepted | ok | 否 | — |
| entry-03890 | tome-orcs.lua:3965 | accepted | ok | 否 | — |
| entry-03892 | tome-orcs.lua:3977 | accepted | ok | 否 | — |
| entry-03912 | tome-orcs.lua:4559 | accepted | ok | 否 | — |
| entry-03913 | tome-orcs.lua:4573 | accepted | ok | 否 | — |
| entry-03918 | tome-orcs.lua:4796 | accepted | ok | 否 | — |
| entry-03921 | tome-orcs.lua:4930 | accepted | ok | 否 | — |
| entry-03924 | tome-orcs.lua:4969 | accepted | ok | 否 | — |
| entry-03925 | tome-orcs.lua:4985 | accepted | ok | 否 | — |
| entry-03926 | tome-orcs.lua:5007 | accepted | ok | 否 | — |
| entry-03931 | tome-orcs.lua:5089 | accepted | ok | 否 | — |
| entry-03933 | tome-orcs.lua:5112 | accepted | ok | 否 | — |
| entry-03939 | tome-orcs.lua:5186 | accepted | ok | 否 | — |
| entry-03940 | tome-orcs.lua:5210 | accepted | ok | 否 | — |
| entry-03946 | tome-orcs.lua:5320 | accepted | ok | 否 | — |
| entry-03950 | tome-orcs.lua:5374 | accepted | ok | 否 | — |
| entry-03953 | tome-orcs.lua:5416 | accepted | ok | 否 | — |
| entry-03960 | tome-orcs.lua:5483 | accepted | ok | 否 | — |
| entry-03967 | tome-orcs.lua:5552 | accepted | ok | 否 | — |
| entry-03970 | tome-orcs.lua:5594 | accepted | ok | 否 | — |
| entry-03971 | tome-orcs.lua:5610 | accepted | ok | 否 | — |
| entry-03972 | tome-orcs.lua:5628 | accepted | ok | 否 | — |
| entry-03973 | tome-orcs.lua:5649 | accepted | ok | 否 | — |
| entry-03977 | tome-orcs.lua:5742 | accepted | ok | 否 | — |
| entry-03984 | tome-orcs.lua:5853 | accepted | ok | 否 | — |
| entry-03990 | tome-orcs.lua:5951 | accepted | ok | 否 | — |
| entry-03996 | tome-orcs.lua:6002 | accepted | ok | 否 | — |
| entry-03997 | tome-orcs.lua:6019 | accepted | ok | 否 | — |
| entry-04000 | tome-orcs.lua:6060 | accepted | ok | 否 | — |
| entry-04008 | tome-orcs.lua:6167 | accepted | ok | 否 | — |
| entry-04015 | tome-orcs.lua:6272 | accepted | ok | 否 | — |
| entry-04018 | tome-orcs.lua:6318 | accepted | ok | 否 | — |
| entry-04019 | tome-orcs.lua:6320 | accepted | ok | 否 | — |
| entry-04035 | tome-orcs.lua:6445 | accepted | ok | 否 | — |
| entry-04092 | tome-orcs.lua:7901 | accepted | ok | 否 | — |
| entry-04101 | tome-orcs.lua:8071 | accepted | ok | 否 | — |
| entry-04116 | tome-possessors.lua:5 | accepted | ok | 否 | — |
| entry-04129 | tome-possessors.lua:119 | accepted | ok | 否 | — |
| entry-04141 | tome-possessors.lua:356 | accepted | ok | 否 | — |

