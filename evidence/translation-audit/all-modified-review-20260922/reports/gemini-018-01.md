### batch-018 译文复核报告

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-018.md`
- **冻结文件哈希校验**：`f5afba08194ffaed184af412b5ea3d16b312dd4a5fd3be0b10a5fecf3d64f919`（已核对一致）
- **公开源码基准**：t-engine4 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均属 `mod-tome`）
- **复核范围**：`entry-00681` 至 `entry-00720`（共 40 条，逐条全覆盖）

---

#### entry-00681
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:61`，神器道具名称 `Skull of the Rat Lich`，术语 Lich 对齐“巫妖”，译作“鼠巫妖头骨”准确忠实。

#### entry-00682
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:67`，道具描述文本，译文完整传达头骨残留能量与眼窝微光，标点与分句合理，未见漏译误译。

#### entry-00683
- **状态**：存在疑点
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:79`：
  ```lua
  game.logSeen(who, "%s raises %s %s, and a red light flashes from it's eye sockets!", who:getName():capitalize(), who:his_her(), self:getName({do_color=true, no_add_name=true}))
  ```
  该处为玩家主动使用神器工具 `RATLICH_SKULL`（鼠巫妖头骨）时的日志。三个参数依次为使用者名、物主代词、道具名（头骨），原句意为玩家“举起/托起其鼠巫妖头骨，头骨眼窝中闪过一道红光”。当前译文为“`%s 令 %s %s站了起来，一道红光从它眼中闪过！`”，将动作 `raises`（高举道具）误解为“使……站起来/复活”，在运行时会导致生成诸如“某某 令 他的 鼠巫妖头骨站了起来”的不合理日志。此外“it's eye sockets”译作“它眼中”略欠精准（宜为眼窝）。

#### entry-00684
- **状态**：细微观察
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:94`，占位符 `%s` 对应 `rat.name:capitalize()`，占位符与叹号正确。“dust of decay”（腐朽/衰朽的尘土）译作“灰烬”（通常对应 ashes）在字面上有轻微意译偏差，但作为骷髅鼠召唤日志整体语意通顺，无技术阻断性缺陷。

#### entry-00685
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:101`，生成的事件地下城名称 `Forsaken Crypt`，译作“废弃地宫”准确得当。

#### entry-00686
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:149`，楼梯地形描述 `Stairs seem to lead into some kind of crypt.`，译作“这道楼梯似乎通向某种地宫。”语义忠实。

#### entry-00687
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:166`，进入后原入口变更的名称 `collapsed forsaken crypt`，译作“坍塌的废弃地宫”准确，与 entry-00685 命名一致。

#### entry-00688
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/rat-lich.lua:167`，坍塌楼梯描述 `Stairs lead downwards into rubble.`，译作“向下通往瓦砾之中的楼梯。”结构与语义准确。

#### entry-00689
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/slimey-pool.lua:49`，`("%s (slimey)"):tformat(_t(g.name))`，占位符 `%s` 匹配无误，全角括号符合中文化命名规范。

#### entry-00690
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/spellblaze-scar.lua:36`，地形名称 `spellblaze scar`，术语 spellblaze 对齐“魔法大爆炸”，译作“魔法大爆炸伤痕”准确。

#### entry-00691
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/spellblaze-scar.lua:48`，`("%s (spellblaze aura)"):tformat(_t(g.name))`，占位符保留，全角括号与“魔法大爆炸光环”术语准确。

#### entry-00692
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/sub-vault.lua:116`，阶梯状态名称 `nearly collapsed hidden vault`，地形宝库语境译作“近乎坍塌的隐藏宝库”准确无误。

#### entry-00693
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/tombstones.lua:67`，扰动墓碑战斗日志，术语 undead 对齐实体分类“亡灵”，句意忠实，全角标点规范。

#### entry-00694
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/events/weird-pedestals.lua:83`，占位符 `%s` 对应阵亡敌人名称，两句陈述完整，全角句号规范。

#### entry-00695
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/basic.lua:269`，门检查提示 `door_player_check`，译作“这扇门似乎被封住了，你觉得你可以打开它。”语义准确。

#### entry-00696
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/basic.lua:384`，机关门阻挡提示 `door_player_stop`，译作“这扇门似乎被封住了，你需要设法打开它。”语义准确。

#### entry-00697
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/basic.lua:410`，已开启机关门关闭提示 `door_player_stop`，译作“这扇门似乎被封住了，你需要设法关闭它。”语义准确。

#### entry-00698
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/bone.lua:108`，骨门检查提示 `door_player_check`，译文与 basic.lua 保持完全一致，准确无误。

#### entry-00699
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/bone.lua:141`，骨门阻挡提示 `door_player_stop`，译文一致且准确。

#### entry-00700
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/bone.lua:166`，已开启骨门关闭提示 `door_player_stop`，译文一致且准确。

#### entry-00701
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/fortress.lua:122`，堡垒门检查提示 `door_player_check`，译文一致且准确。

#### entry-00702
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/gothic.lua:256`，哥特门检查提示 `door_player_check`，译文一致且准确。

#### entry-00703
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/gothic.lua:277`，哥特门阻挡提示 `door_player_stop`，译文一致且准确。

#### entry-00704
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/gothic.lua:304`，已开启哥特门关闭提示 `door_player_stop`，译文一致且准确。

#### entry-00705
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/lava.lua:40`，`self:logCombat(who, "#Source# burns #Target#!")`，`#Source#` 与 `#Target#` 战斗标记完整保留，全角感叹号规范。

#### entry-00706
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/sand.lua:47`，流沙挖掘空洞描述，完整翻译 loose sand、filling this void 与 collapse suddenly and completely，行文通顺。

#### entry-00707
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/slimy_walls.lua:256`，黏液门检查提示 `door_player_check`，译文保持跨文件统一，准确无误。

#### entry-00708
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/slimy_walls.lua:277`，黏液门阻挡提示 `door_player_stop`，译文保持跨文件统一，准确无误。

#### entry-00709
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/slimy_walls.lua:304`，黏液门关闭提示 `door_player_stop`，译文保持跨文件统一，准确无误。

#### entry-00710
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/grids/water.lua:125`，`self:logCombat(who, "#Source# poisons #Target#!")`，战斗标记完整保留，译作“#Source#让#Target#中毒！”准确。

#### entry-00711
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/aquatic_critter.lua:60`（龙龟描述），术语 reptile 对齐“爬行动物”，译作“一只巨大、细长且泛着海绿色的爬行动物。”准确。

#### entry-00712
- **状态**：细微观察
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/aquatic_critter.lua:69`（远古龙龟描述，物理抗性 60%）。原句中“it looks old and impenetrable”译作“看上去苍老而结实”。impenetrable 字面侧重“牢不可破/难以穿透/坚不可摧”，译作“结实”语感略显平淡弱化，但整体语义尚可理解。

#### entry-00713
- **状态**：细微观察
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/bear.lua:57`（黑熊描述）。
  1. 标点异常：译文末尾使用了“`哦～。`”，波浪号紧跟全角句号存在冗余标点；
  2. 语气偏差：原句“'Cause this bear wants honey.”为威胁性戏谑（意在暗示玩家若闻起来像蜜就会被吃），译文“这只熊喜欢蜂蜜哦～”语气偏向幼态/萌化。

#### entry-00714
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/bear.lua:88`（灰熊描述），`A huge, beastly bear, more savage than most of its kind.` 译作“一头巨大而凶猛的熊，比同类更加凶残。”准确传神。

#### entry-00715
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/bird.lua:88`（不死鸟涅槃飘字），`game.flyers:add(..., _t"RESURRECT!", ...)` 译作“复活！”准确。

#### entry-00716
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/canine.lua:42`（狼描述），`Lean, mean, and shaggy, it stares at you with hungry eyes.` 译作“它精瘦、凶悍、皮毛蓬松，正用饥饿的眼神盯着你。”自然贴切。

#### entry-00717
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/crystal.lua:29`（水晶 NPC 基础描述），`A shining crystal formation charged with magical energies.` 译作“一簇闪耀的水晶结构，其中充盈着魔法能量。”准确。

#### entry-00718
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/crystal.lua:57`（鬼火实体类型），`type = "elemental"`，source_tag 为 `entity type`，与统一术语“元素生物”完全一致。

#### entry-00719
- **状态**：细微观察
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/crystal.lua:94`（红水晶描述 `A formation of red crystal. It emits bright red, scorching light.`）。原文 formation 本指晶体簇/地质结构形态（如 entry-00717 译作“水晶结构”），译文意译为“由红色水晶构成的生物”。经核对同 section 其它晶体生物译文，译者统一将各类晶体的 formation 意译加词为“……构成的生物”，属于局部统一步调的意译，语义通顺，无阻断性技术问题。

#### entry-00720
- **状态**：未发现问题
- **可核验依据**：固定源码 `game/modules/tome/data/general/npcs/faeros.lua:25`（火妖实体类型），`type = "elemental"`，source_tag 为 `entity type`，符合实体类型统一术语“元素生物”。