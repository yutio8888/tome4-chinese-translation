# ToME4 1.7.6 译文库死键扫描

确认 22 条死键。其中 21 条有当前源码命中的在用副本，1 条是已删除的引擎日志。12 对中文译文不同，其中 2 对仍有旧键修订中已经处理的在用译文问题。另有 26 条上游保留键待确认。

## 数据与方法

- 本体与引擎取 Git commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/` 归档。译文行号取翻译仓库快照 commit `64e5bcb9d060a6a4c7c8125d3abd26a2c926be5a` 中五个文件的 `t(` 首行。
- DLC 以 1.7.6 安装目录的三个 TEAA 为准，源码仓库和源码 commit 未固定。包内三个 `init.lua` 均声明兼容版本 `{1,7,4}`。以下 SHA-256 标识实测输入。两个 Orcs 在用 lore 源文件与 `tome4-dlcs` 公开检出逐字节一致。

| TEAA | addon_version | SHA-256 |
|---|---|---|
| `tome-orcs.teaa` | 1.1.10 | `c9adfa15c94aed31b0e6f3a0c119b6101da9e39313382616039955309abf04ed` |
| `tome-cults.teaa` | 1.0.12 | `9c73c236031409c22aefa780df7a3065940b212ad2b0512cfe459b34609df234` |
| `tome-ashes-urhrok.teaa` | 1.1.4 | `ba9c011a4c32a3ed4687d6a40d0e0b276fedc204c89ec51e10855151e4fb5289` |

- 字节级扫描器跳过单行注释及任意等号层级的长注释，由 LuaJIT 解码短串转义和长串（包括首换行、CRLF 及尾随空白）。扫描 3,383 个 Lua 文件，索引 173,762 次有效字面量出现，合计 50,249 个不同值。33 个 locale Lua 排除出运行源码匹配。第三方 `remdebug/engine.lua:93` 有一处 LuaJIT 拒绝的转义，排除该 token。
- 字面量检索先比字节，再做 Unicode casefold 并移除空白、标点，或按长度允许 1–6 个规范化字符编辑。四条同文件的提示或技能改版通过更宽的相似度及具体定义人工配对。额外读取 2 个 JSON 对话树及 74 个其他文本资源，核对运行时取键、Lua 表键、大小写转换和拼接。文档子串命中只作线索。
- `I18N.lua:41–58,65–69,141–143` 同时写 tag 桶和 `"nil"` 桶，tag 查找失败时回落到 `"nil"`。section 不参与游戏查找。任意字面量的 exact 命中只能证明存在，需结合调用点判断。唯一只在非游戏组件中有 exact 字面量的条目是 `mod-tome.lua:36515` 的 `space`，实际还可由状态的 `subtype` 表键生成。未运行游戏、门禁或 producer。

## 实测计数

| 译文库 | 总条目 | Lua exact | 初筛未 exact | 确认死键 |
|---|---:|---:|---:|---:|
| `mod-tome.lua` | 21,697 | 21,102 | 595 | 19 |
| `engine.lua` | 1,061 | 1,034 | 27 | 1 |
| `tome-orcs.lua` | 3,904 | 3,871 | 33 | 2 |
| `tome-cults.lua` | 2,043 | 2,015 | 28 | 0 |
| `tome-ashes-urhrok.lua` | 849 | 841 | 8 | 0 |
| **合计** | **29,554** | **28,863** | **691** | **22** |

初筛未 exact 中，452 条机械 near、239 条机械 none。按调用或数据来源核对后，这 691 条为 21 条已配对死键、1 条确认删除、614 条运行时生成键、29 条 `.chat` 字段、26 条待确认。

## 在用副本仍有问题的确认修复

- **原始森林文书 `primal-forest-3`**。死键 `tome-orcs.lua:8337`，在用 `tome-orcs.lua:3145`。在用英文第二段末尾的 `potential for abuse.` 后保留两个行尾空格。0236 已识别死键，0456 和 0457 仍以 `0b1457dd6cae` 修订该键。在用稿已表达若干推测和伊格兰斯的实践，但 `regeneration salves` 仍译为「回复药剂」，丢失再生含义和药膏剂型。原文 `a lone megalomaniac destroying much of Eyal` 在用稿也把「独自」弱化为「某个」，把「大片地区」扩大为「大部分地区」。两处在死键修订后均有对应内容。
  [0236 decision](/workspace/tome4-chinese-translation/evidence/lite-review/batches/0236/decision.json) · [0456 decision](/workspace/tome4-chinese-translation/evidence/lite-review/batches/0456/decision.json) · [0457 decision](/workspace/tome4-chinese-translation/evidence/lite-review/batches/0457/decision.json) · [dlc/tome-orcs/data/lore/primal-forest.lua:74](/tmp/t5/deadkey/dlc/tome-orcs/data/lore/primal-forest.lua:74)
- **蒸汽议会纪要 `palace-fumes-5`**。死键 `tome-orcs.lua:8352`，在用 `tome-orcs.lua:2759`。0456 以 `4d8260ebdf43` 修订 DebugMain 死键。在用稿已正确保留辞职前演讲、议程方案和与兽人作战经验等事实。0456 A 点出的「齐腰高的小傻战士们」仍原样出现在用稿，旧键已改为「只有齐腰高……的可笑小个子战士们」。同次修订保留了岩浆为该地热源供能的关系，在用稿仅说「那里的岩浆」，省去了原文 `the magma powering it` 的作用。这条实质差异为本次对照确认，0456 decision 未单列岩浆问题。
  [0456 decision](/workspace/tome4-chinese-translation/evidence/lite-review/batches/0456/decision.json) · [0456 A](/workspace/tome4-chinese-translation/evidence/lite-review/batches/0456/A.json) · [dlc/tome-orcs/data/lore/palace-fumes.lua:88](/tmp/t5/deadkey/dlc/tome-orcs/data/lore/palace-fumes.lua:88)

## 全部配对

提交列按「死键／在用」列出 `git log -L` 对对应译文行范围记录的最近提交。相同提交表示同轮触及译文行。英文原串、逐字符差异和匹配到的 decision 见 [pairs.json](pairs.json)。

| 死键 → 在用 | 当前源码 | 英文差异 | 中文现状 | 最近提交 |
|---|---|---|---|---|
| [mod-tome.lua:1133](/workspace/tome4-chinese-translation/mod-tome.lua:1133) → [mod-tome.lua:1454](/workspace/tome4-chinese-translation/mod-tome.lua:1454) | [src/game/modules/tome/class/interface/PlayerQuestPopup.lua:59](/tmp/t5/deadkey/src/game/modules/tome/class/interface/PlayerQuestPopup.lua:59) | 感叹号后、颜色标记前插入一个空格。 | 译文相同。 | `089e147bf6` / `089e147bf6` |
| [mod-tome.lua:1135](/workspace/tome4-chinese-translation/mod-tome.lua:1135) → [mod-tome.lua:1456](/workspace/tome4-chinese-translation/mod-tome.lua:1456) | [src/game/modules/tome/class/interface/PlayerQuestPopup.lua:66](/tmp/t5/deadkey/src/game/modules/tome/class/interface/PlayerQuestPopup.lua:66) | 感叹号后、颜色标记前插入一个空格。 | 译文相同。 | `089e147bf6` / `089e147bf6` |
| [mod-tome.lua:1137](/workspace/tome4-chinese-translation/mod-tome.lua:1137) → [mod-tome.lua:1458](/workspace/tome4-chinese-translation/mod-tome.lua:1458) | [src/game/modules/tome/class/interface/PlayerQuestPopup.lua:70](/tmp/t5/deadkey/src/game/modules/tome/class/interface/PlayerQuestPopup.lua:70) | 感叹号后、颜色标记前插入一个空格。 | 译文相同。 | `089e147bf6` / `089e147bf6` |
| [mod-tome.lua:1139](/workspace/tome4-chinese-translation/mod-tome.lua:1139) → [mod-tome.lua:1460](/workspace/tome4-chinese-translation/mod-tome.lua:1460) | [src/game/modules/tome/class/interface/PlayerQuestPopup.lua:74](/tmp/t5/deadkey/src/game/modules/tome/class/interface/PlayerQuestPopup.lua:74) | 感叹号后、颜色标记前插入一个空格。 | 译文相同。 | `089e147bf6` / `089e147bf6` |
| [mod-tome.lua:1141](/workspace/tome4-chinese-translation/mod-tome.lua:1141) → [mod-tome.lua:1462](/workspace/tome4-chinese-translation/mod-tome.lua:1462) | [src/game/modules/tome/class/interface/PlayerQuestPopup.lua:78](/tmp/t5/deadkey/src/game/modules/tome/class/interface/PlayerQuestPopup.lua:78) | 感叹号后、颜色标记前插入一个空格。 | 译文相同。 | `089e147bf6` / `089e147bf6` |
| [mod-tome.lua:1569](/workspace/tome4-chinese-translation/mod-tome.lua:1569) → [mod-tome.lua:2251](/workspace/tome4-chinese-translation/mod-tome.lua:2251) | [src/game/modules/tome/class/interface/TooltipsData.lua:98](/tmp/t5/deadkey/src/game/modules/tome/class/interface/TooltipsData.lua:98) | 击杀回活力的意志系数 30% → 50%，乘数从分级的一半改为整个分级。 | 在用译文正确跟随当前数值，0032 的修复落在在用条目。 | `b0890a4815` / `ffaab8ba4c` |
| [mod-tome.lua:1706](/workspace/tome4-chinese-translation/mod-tome.lua:1706) → [mod-tome.lua:2262](/workspace/tome4-chinese-translation/mod-tome.lua:2262) | [src/game/modules/tome/class/interface/TooltipsData.lua:198](/tmp/t5/deadkey/src/game/modules/tome/class/interface/TooltipsData.lua:198) | `performa` → `perform`，句首大写。 | 译文相同。 | `58ef6b9776` / `58ef6b9776` |
| [mod-tome.lua:1823](/workspace/tome4-chinese-translation/mod-tome.lua:1823) → [mod-tome.lua:2271](/workspace/tome4-chinese-translation/mod-tome.lua:2271) | [src/game/modules/tome/class/interface/TooltipsData.lua:268](/tmp/t5/deadkey/src/game/modules/tome/class/interface/TooltipsData.lua:268) | 现行格挡说明明确精神伤害不可格挡，同类型抗性使格挡值获得 50% 加成。 | 在用译文跟随新机制。0031 对旧版仅记 advisory。 | `becf31dce5` / `391facb5ed` |
| [mod-tome.lua:21061](/workspace/tome4-chinese-translation/mod-tome.lua:21061) → [mod-tome.lua:21085](/workspace/tome4-chinese-translation/mod-tome.lua:21085) | [src/game/modules/tome/data/talents/celestial/combat.lua:111](/tmp/t5/deadkey/src/game/modules/tome/data/talents/celestial/combat.lua:111) | 命中提升临时伤害护盾强度时，还把持续时间至少补到 2 回合。 | 在用译文已包含持续时间。0371 的修复落在在用条目。 | `846fa91fb3` / `7c836414d5` |
| [mod-tome.lua:23758](/workspace/tome4-chinese-translation/mod-tome.lua:23758) → [mod-tome.lua:23815](/workspace/tome4-chinese-translation/mod-tome.lua:23815) | [src/game/modules/tome/data/talents/cunning/traps.lua:1759](/tmp/t5/deadkey/src/game/modules/tome/data/talents/cunning/traps.lua:1759) | `damgae` → `damage`。 | 0133 修了旧键的最长持续时间和 1 格触发条件。两点均已出现在用译文，在用译文还明确半径及拉向中心。 | `91a4c9ad4f` / `89744ab570` |
| [mod-tome.lua:25886](/workspace/tome4-chinese-translation/mod-tome.lua:25886) → [mod-tome.lua:25901](/workspace/tome4-chinese-translation/mod-tome.lua:25901) | [src/game/modules/tome/data/talents/misc/horrors.lua:671](/tmp/t5/deadkey/src/game/modules/tome/data/talents/misc/horrors.lua:671) | 活化之剑持续 10 → 15 回合。 | 在用译文为 15 回合。 | `54864a0546` / `54864a0546` |
| [mod-tome.lua:25935](/workspace/tome4-chinese-translation/mod-tome.lua:25935) → [mod-tome.lua:26097](/workspace/tome4-chinese-translation/mod-tome.lua:26097) | [src/game/modules/tome/data/talents/misc/inscriptions.lua:245](/tmp/t5/deadkey/src/game/modules/tome/data/talents/misc/inscriptions.lua:245) | 现行英勇纹身原文加上生命值为 0 或以下时增幅封顶 100%。 | 0379／0380 修在旧键上。两份当前译文都正确写出负生命值、持续时间和上限，未发现相应遗漏。 | `67af381cd3` / `917d03accf` |
| [mod-tome.lua:29072](/workspace/tome4-chinese-translation/mod-tome.lua:29072) → [mod-tome.lua:29110](/workspace/tome4-chinese-translation/mod-tome.lua:29110) | [src/game/modules/tome/data/talents/spells/master-necromancer.lua:50](/tmp/t5/deadkey/src/game/modules/tome/data/talents/spells/master-necromancer.lua:50) | 继承伤害加成明确改为取最高一项。 | 译文相同，均含「最高」。 | `ebc483fe3d` / `301d69ad74` |
| [mod-tome.lua:29185](/workspace/tome4-chinese-translation/mod-tome.lua:29185) → [mod-tome.lua:29236](/workspace/tome4-chinese-translation/mod-tome.lua:29236) | [src/game/modules/tome/data/talents/spells/master-of-flesh.lua:235](/tmp/t5/deadkey/src/game/modules/tome/data/talents/spells/master-of-flesh.lua:235) | `lyring` → `lying`。 | 译文相同。 | `ebc483fe3d` / `ebc483fe3d` |
| [mod-tome.lua:43141](/workspace/tome4-chinese-translation/mod-tome.lua:43141) → [mod-tome.lua:17960](/workspace/tome4-chinese-translation/mod-tome.lua:17960) | [src/game/modules/tome/data/lore/misc.lua:372](/tmp/t5/deadkey/src/game/modules/tome/data/lore/misc.lua:372) | 段落缩进与末尾空白变化。 | 0120 的纹身工匠修复落在在用键，两份现均用「纹身工匠」。 | `ba36e6d53a` / `67b5b0840b` |
| [mod-tome.lua:43162](/workspace/tome4-chinese-translation/mod-tome.lua:43162) → [mod-tome.lua:18120](/workspace/tome4-chinese-translation/mod-tome.lua:18120) | [src/game/modules/tome/data/lore/misc.lua:497](/tmp/t5/deadkey/src/game/modules/tome/data/lore/misc.lua:497) | 段落缩进与末尾空白变化。 | 两份措辞多处不同，未找到已确认修复只落在旧键上的记录。 | `ba36e6d53a` / `3d22241ad4` |
| [mod-tome.lua:43179](/workspace/tome4-chinese-translation/mod-tome.lua:43179) → [mod-tome.lua:18002](/workspace/tome4-chinese-translation/mod-tome.lua:18002) | [src/game/modules/tome/data/lore/misc.lua:403](/tmp/t5/deadkey/src/game/modules/tome/data/lore/misc.lua:403) | 段落缩进与末尾空白变化。 | 0364–0366 的确认记录含同步或分开处理。在用译文已保留以首都为据点经商、禁止外人入城、配合市场调查等要点，「尤以金属加工技艺闻名」保留原句强调。 | `e8309f050d` / `67b5b0840b` |
| [mod-tome.lua:43196](/workspace/tome4-chinese-translation/mod-tome.lua:43196) → [tome-cults.lua:2184](/workspace/tome4-chinese-translation/tome-cults.lua:2184) | [dlc/tome-cults/data/lore/kroshkkur.lua:103](/tmp/t5/deadkey/dlc/tome-cults/data/lore/kroshkkur.lua:103) | 段落缩进与末尾空白变化。 | 当前在用文本在 Cults。两份措辞多处不同，未找到已确认修复只落在旧键上的记录。 | `ba36e6d53a` / `a697847d59` |
| [mod-tome.lua:43205](/workspace/tome4-chinese-translation/mod-tome.lua:43205) → [mod-tome.lua:39441](/workspace/tome4-chinese-translation/mod-tome.lua:39441) | [src/game/modules/tome/data/zones/ruined-dungeon/grids.lua:65](/tmp/t5/deadkey/src/game/modules/tome/data/zones/ruined-dungeon/grids.lua:65) | `deeds`／`deads` 拼写和断句标点不同。 | 译文相同。 | `1f53881094` / `7e97425c72` |
| [tome-orcs.lua:8337](/workspace/tome4-chinese-translation/tome-orcs.lua:8337) → [tome-orcs.lua:3145](/workspace/tome4-chinese-translation/tome-orcs.lua:3145) | [dlc/tome-orcs/data/lore/primal-forest.lua:74](/tmp/t5/deadkey/dlc/tome-orcs/data/lore/primal-forest.lua:74) | 实际源码第二段末句 `potential for abuse.` 后保留两个 ASCII 空格。 | 0456／0457 确认修复只写 DebugMain。见重点清单。 | `1c506ab29d` / `fb4bbecb76` |
| [tome-orcs.lua:8352](/workspace/tome4-chinese-translation/tome-orcs.lua:8352) → [tome-orcs.lua:2759](/workspace/tome4-chinese-translation/tome-orcs.lua:2759) | [dlc/tome-orcs/data/lore/palace-fumes.lua:88](/tmp/t5/deadkey/dlc/tome-orcs/data/lore/palace-fumes.lua:88) | 实际源码首行的 `presiding.` 后保留两个 ASCII 空格。 | 0456 确认修复只写 DebugMain。在用译文仍有其中一处原措辞，且缺少地热能源由岩浆供给的关系。见重点清单。 | `10646bc758` / `d11c96ffb7` |

## 无在用副本的近似候选

确认会出现未汉化英文的无孪生替换 **0 条**。另有 14 条待确认的 `.always_merge` 保留键，源码存在规范化相同的字面量，译文库没有这些候选字面量的 exact 条目。下表原样列出字面量。这些多为 ID、内部数据或变量选项，尚无证据表明它们取代了旧的可见字符串。其余 12 条待确认键及原始近似结果见 [none.json](none.json)。

| 库中旧键 | 当前源码中的近似字面量及位置 |
|---|---|
| [engine.lua:4](/workspace/tome4-chinese-translation/engine.lua:4) `"3-head"` | `"3head"` [src/game/modules/tome/data/talents/gifts/summon-distance.lua:569](/tmp/t5/deadkey/src/game/modules/tome/data/talents/gifts/summon-distance.lua:569) |
| [engine.lua:9](/workspace/tome4-chinese-translation/engine.lua:9) `"Assassin lair"` | `"assassin-lair"` [src/game/modules/tome/data/zones/thieves-tunnels/zone.lua:54](/tmp/t5/deadkey/src/game/modules/tome/data/zones/thieves-tunnels/zone.lua:54) |
| [engine.lua:11](/workspace/tome4-chinese-translation/engine.lua:11) `"Cosmic Fauna"` | `"cosmic-fauna"` [src/game/modules/tome/data/general/npcs/losgoroth.lua:28](/tmp/t5/deadkey/src/game/modules/tome/data/general/npcs/losgoroth.lua:28) |
| [engine.lua:21](/workspace/tome4-chinese-translation/engine.lua:21) `"Keepers of Reality"` | `"keepers-of-reality"` [src/game/modules/tome/data/birth/classes/chronomancer.lua:50](/tmp/t5/deadkey/src/game/modules/tome/data/birth/classes/chronomancer.lua:50) |
| [engine.lua:26](/workspace/tome4-chinese-translation/engine.lua:26) `"Portal Room"` | `"portal_room"` [src/game/modules/tome/data/maps/vaults/auto/greater/portal-vault.lua:169](/tmp/t5/deadkey/src/game/modules/tome/data/maps/vaults/auto/greater/portal-vault.lua:169) |
| [engine.lua:27](/workspace/tome4-chinese-translation/engine.lua:27) `"Rhalore"` | `"rhalore"` [dlc/tome-orcs/data/factions.lua:40](/tmp/t5/deadkey/dlc/tome-orcs/data/factions.lua:40) |
| [engine.lua:28](/workspace/tome4-chinese-translation/engine.lua:28) `"Sandworm Burrowers"` | `"sandworm-burrowers"` [src/game/modules/tome/data/zones/sandworm-lair/npcs.lua:41](/tmp/t5/deadkey/src/game/modules/tome/data/zones/sandworm-lair/npcs.lua:41) |
| [engine.lua:32](/workspace/tome4-chinese-translation/engine.lua:32) `"Slavers"` | `"slavers"` [src/game/modules/tome/data/zones/ring-of-blood/grids.lua:46](/tmp/t5/deadkey/src/game/modules/tome/data/zones/ring-of-blood/grids.lua:46) |
| [engine.lua:33](/workspace/tome4-chinese-translation/engine.lua:33) `"Sorcerers"` | `"sorcerers"` [dlc/tome-cults/data/achievements/all.lua:84](/tmp/t5/deadkey/dlc/tome-cults/data/achievements/all.lua:84) |
| [engine.lua:39](/workspace/tome4-chinese-translation/engine.lua:39) `"The Way"` | `"the-way"` [dlc/tome-orcs/data/factions.lua:37](/tmp/t5/deadkey/dlc/tome-orcs/data/factions.lua:37) |
| [engine.lua:45](/workspace/tome4-chinese-translation/engine.lua:45) `"Vargh Republic"` | `"vargh-republic"` [dlc/tome-orcs/data/factions.lua:42](/tmp/t5/deadkey/dlc/tome-orcs/data/factions.lua:42) |
| [engine.lua:46](/workspace/tome4-chinese-translation/engine.lua:46) `"Victim"` | `"victim"` [src/game/modules/tome/data/zones/crypt-kryl-feijan/npcs.lua:98](/tmp/t5/deadkey/src/game/modules/tome/data/zones/crypt-kryl-feijan/npcs.lua:98) |
| [engine.lua:47](/workspace/tome4-chinese-translation/engine.lua:47) `"Water lair"` | `"water-lair"` [src/game/modules/tome/data/zones/flooded-cave/npcs.lua:29](/tmp/t5/deadkey/src/game/modules/tome/data/zones/flooded-cave/npcs.lua:29) |
| [engine.lua:88](/workspace/tome4-chinese-translation/engine.lua:88) `"portal back"` | `"PORTAL_BACK"` [dlc/tome-cults/data/general/events/tentacle-tree.lua:111](/tmp/t5/deadkey/dlc/tome-cults/data/general/events/tentacle-tree.lua:111)；`"portal-back"` [src/game/modules/tome/data/quests/temple-of-creation.lua:72](/tmp/t5/deadkey/src/game/modules/tome/data/quests/temple-of-creation.lua:72)；`"portal_back"` [src/game/modules/tome/data/chats/slasul.lua:56](/tmp/t5/deadkey/src/game/modules/tome/data/chats/slasul.lua:56) |

已删且无替换串的日志为 [engine.lua:366](/workspace/tome4-chinese-translation/engine.lua:366) 的 `following chain...`。引擎提交 `a4c226dfaa44e3223e29db729549d04bc577e18e` 删除了 `engine/Chat.lua` 的 `game.log` 调用。

## 抽查与核验

- 对全部 21 对回到上表源码行重取原始 token，用 LuaJIT 重新求值。逐项确认源码值严格等于在用英文、严格不同于死键英文。随后用固定提交的 `I18N.lua` 加载五个实际译文文件的 `t()` 定义，在在用 tag 和一个不存在的 tag 下各查一次，42 次均返回同一在用译文。
- 另直接核对了 5 个任务日志调用的感叹号后空格，以及两篇 Orcs lore 的 `_t[[…]]` 调用。对非 Lua 对话抽查 `avatar-distant-sun-unlock.chat:38–40`，三项正文／选项均进入 `Chat.lua:341,355` 的 `_t`。对生成键抽查 `Wanderer seed`、`alchemist amber`、`wet giant venus flytrap`、`barbed`、`space`，均找到对应定义及转换或查询路径。
- 可按已确认的英文运行键同步上述两篇在用译文的差异，并在处理确认死键前保留对应的在用键。上游保留键可继续通过实际查询调用取证。

[pairs.json](pairs.json) · [near-only.json](near-only.json) · [none.json](none.json)
