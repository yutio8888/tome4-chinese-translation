### 文件校验与复核概述

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-088.md`
- **文件 SHA-256**：`6ceb26935d81f12f6db99878785d30d9714985e4b2f5ffc77e45a6841b3abbd8`（校验一致）
- **条目范围**：`entry-02892` 至 `entry-02931`，共 40 条
- **固定公开源码**：t-engine4 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均归属于 `mod-tome`）
- **译文基线**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

### 逐条复核意见

#### entry-02892
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/timed_effects/physical.lua:4347`。状态效果 `Brutalized` 的 `on_gain` 回调返回 `_t"#Target# is brutalized!"`。译文保留了引擎宏 `#Target#`，全角感叹号匹配，译名与该文件同处定义的“暴行”（Desc/on_lose）一致。

#### entry-02893
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/abashed-expanse/npcs.lua:37`。实体 `SPACIAL_DISTURBANCE` 描述文本，译文“空间结构上的一个孔洞，它似乎是此地空间不稳定的根源”准确表达了 Abashed Expanse（落魄深渊/落魄空间）的语境，语义与标点无误。

#### entry-02894
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ancient-elven-ruins/npcs.lua:110`。木乃伊生物描述 `desc = _t[[An animated corpse in mummy wrappings.]]`，译文“一具缠绕着裹尸布的活化尸体”准确严谨。

#### entry-02895
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ancient-elven-ruins/npcs.lua:157`。腐烂木乃伊描述 `desc = _t[[A rotting animated corpse in mummy wrappings.]]`，译文“一具缠绕着裹尸布的腐烂活化尸体”忠实对应，无语法硬伤。

#### entry-02896
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ancient-elven-ruins/npcs.lua:180`。完好木乃伊描述中 `both very well preserved` 指代尸体与裹尸布两者，译文“尸身与裹尸布均保存完好”理解准确，表意流畅。

#### entry-02897
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ancient-elven-ruins/objects.lua:69`。永夜之袍（ROBE_ETERNAL_NIGHT）与永夜之冠（CROWN_ETERNAL_NIGHT）的套装提示 `set_desc.eternalnight`。译文“再补齐一件配套的套装部件，将成为你至高无上的荣耀”准确传达了双关意味与套装指引。

#### entry-02898
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/grids.lua:33`。`game.logSeen(src, "#VIOLET#The wormhole absorbs the energy of the spell and teleports %s away!", a.name)`。占位符 `%s` 接收被传送者名称，颜色代码 `#VIOLET#` 完整，标点对应。

#### entry-02899
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/grids.lua:37`。`game.logSeen({x=x,y=y}, "#VIOLET#The wormhole absorbs the energy of the spell and explodes in a burst of nullmagic!")`。法术击中不稳定虫洞触发法力燃烧效果的战报，颜色代码 `#VIOLET#` 与标点完整，语义准确。

#### entry-02900
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/objects.lua:29`。日记碎片 1~3 的描述 `desc = _t[[A page of a diary.]]`，译文“日记的一页。”准确无误。

#### entry-02901
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/objects.lua:36`。便条 4 的描述 `desc = _t[[A scrap of paper.]]`，译文“一张纸片。”准确无误。

#### entry-02902
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/objects.lua:51`。蜘蛛毒素之杖技能描述调用 `tformat(self.use_power.range, engine.interface.ActorTalents.damDesc(...), self.use_power.duration)`。三个占位符 `%d`（射程）、`%0.2f`（自然伤害数值）、`%d`（持续回合）在译文中顺序与类型严格一致，机制机制（dot加定身）描述准确。

#### entry-02903
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/ardhungol/objects.lua:63`。`game.logSeen(who, "%s activates %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。三个 `%s` 依次接收使用者名字、物主代词（“他的/她的/它的”）与物品名；中文拼接为“角色激活了他的蜘蛛毒素之杖！”，顺序与数量完全匹配，语序自然。

#### entry-02904
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:64`。角斗场骷髅巨鼠（SKELERAT）描述，破折号使用规范，风趣语调传达自然，无机制错误。

#### entry-02905
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:79`。流浪斗士（homeless fighter）描述 `desc = _t"Will fight for a meal."`，译文“为一餐温饱而战。”精炼贴切。

#### entry-02906
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:332`。多目怪死亡掉落眼球战报 `game.logSeen(self, "#AQUAMARINE#As %s falls all its eyes fall to the ground!", self:getName())`。颜色代码 `#AQUAMARINE#`、占位符 `%s` 及感叹号保留正确。

#### entry-02907
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:781`。潜行系角斗士描述，译文“善用诡计取胜的潜行斗士。小心，他们会偷走你的生命！”忠实流畅，标点无误。

#### entry-02908
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:1005`。黄昏法师（anorithil）角斗士描述，使用光暗法术设定明确，译文“来自远方的战士。他们使用光暗魔法攻击你！”契合 NPC 机制。

#### entry-02909
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:1034`。太阳骑士（sun paladin）角斗士描述，英文俚语 "a mean sword"（精湛凶狠的剑术）意译为“剑术也十分凶狠”，贴合角色剑盾近战兼光系魔法定位。

#### entry-02910
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/npcs.lua:1065`。星辰十字军（star crusader）角斗士描述，承接前一条目句式，将“Darkness, too.”译为“暗魔法也不在话下。”，句意连贯自然。

#### entry-02911
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/objects.lua:75`。角斗场随机闪现靴主动技能 `("blink to a nearby random location within range %d (based on Magic)"):tformat(self.use_power.range(self, who))`。`%d` 占位符保留，传送机制说明无误。

#### entry-02912
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:315`。头顶飘字 `game.flyers:add(..., _t"RANK UP!!", ...)`。感叹号匹配，译为“阶级提升！！”准确传达游戏术语。

#### entry-02913
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:316`。角斗场晋升日志，颜色代码 `#LIGHT_GREEN#` 与 `#WHITE#` 完整闭合，占位符 `%s` 接收段位名称正确。

#### entry-02914
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:325`。单回合连杀飘字 `("%d kills!"):tformat(k)`。占位符 `%d` 接收单回合击杀数，译为“%d连杀！”机制表达极佳。

#### entry-02915
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:347`。休息波次掉落物倒计时清理日志，颜色代码 `#YELLOW#`、`#WHITE#`、`#LAST#` 齐全，占位符 `%d` 对应回合数。

#### entry-02916
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:358`。Boss 波次提示 `game.log("#VIOLET#Boss round!!!")`。颜色代码 `#VIOLET#` 与三连感叹号匹配。

#### entry-02917
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:361`。精英波次提示 `game.log("#GOLD#Miniboss round!")`。颜色代码 `#GOLD#` 与感叹号匹配。

#### entry-02918
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:365`。最终波次提示 `game.log("#LIGHT_RED#Final round!!!")`。颜色代码 `#LIGHT_RED#` 与感叹号匹配。

#### entry-02919
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:403`。通关经验飘字 `("Round Clear! +%s EXP!"):tformat(expAward)`。占位符 `%s` 接收经验值数值，标点匹配。

#### entry-02920
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:404`。`game.log("%sWave clear!", col)`，其中 `col = "#ROYAL_BLUE#"`。首位 `%s` 正确承接颜色代码，句意完整。

#### entry-02921
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:405`：
  ```lua
  game.log("%sClear bonus: %s%s%s! Score bonus: %s%s%s! Danger bonus: %s%s%s! Rank bonus: %s%s%s!", col, hgh, clearBonus, col, hgh, scoreBonus, col, hgh, dangerBonus, col, hgh, rankBonus, col)
  ```
  共 13 处 `%s`，类型与传参顺序完全一致，数值高亮着色逻辑完好。
  **观察**：译文`%s全清奖励：%s%s%s! 分数奖励：%s%s%s! 危险度奖励：%s%s%s! 级别奖励：%s%s%s！`中，前三处使用了半角感叹号加空格（`! `），末尾一处使用了全角感叹号（`！`），存在标点半角/全角混用现象。

#### entry-02922
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:406`。`game.log("%sYour experience increases by %s%d%s!", col, hgh, expAward, col)`。占位符 `%s`、`%s`、`%d`、`%s` 顺序与类型完全对应，感叹号无误。

#### entry-02923
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/arena/zone.lua:407`。`game.log("%sYou earn %s gold for your victory!", col, game.level.arena.bonusMultiplier)`。两个 `%s` 顺序对应颜色代码与金币数量，标点与语意正确。

#### entry-02924
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/blighted-ruins/npcs.lua:160`。枯萎废墟骨骸实验体描述 `desc = _t"This pile of bones appears to move on its own, but it can't seem to organise itself into something dangerous."`，译文表达自然流畅。

#### entry-02925
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/briagh-lair/npcs.lua:28`。Boss 名称 `Briagh, Great Sand Wyrm`，与全库及同文本前文（如 `mod-tome.lua:6689`“布莱亚，那条巨型沙龙”）专名译法一致。

#### entry-02926
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/charred-scar/grids.lua:28`。远行传送门实体名 `name = "Farportal: the Far East"`，与全库其他传送门（如 `mod-tome.lua:38724`）统一译为“远行传送门：至远东大陆”。

#### entry-02927
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/zones/charred-scar/npcs.lua:107`：
  ```lua
  self:doEmote(("Go %s! We will hold the line!"):tformat(game.player.name), 150)
  ```
  占位符 `%s` 接收玩家名字无误。
  **观察**：译文为`去吧%s!我们会坚守防线！`，第一处使用了半角感叹号且紧贴后续中文（`%s!我们会...`），末尾为全角感叹号（`！`），标点未统一且缺乏标点间距。

#### entry-02928
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/charred-scar/npcs.lua:212`。伊兰达尔发现玩家时的台词 `self:doEmote(_t"Damn you, you only postpone your death! Fyrk!", 60)`。召唤并呼喊的炎魔守卫“Fyrk”在同文件 line 38092 中统一译作“弗莱克”，译文“该死，你只是在拖延你的死亡而已！弗莱克！”专名与语境准确一致。

#### entry-02929
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/zones/conclave-vault/npcs.lua:62`。实体名称 `name = "degenerated ogric mass"`。
  **观察**：该怪物在源码中是一个手持双手重锤（greatmaul）、具有 2 阶精英强度的畸变食人魔生物，其描述为 `This huge mass of deformed flesh was probably once an ogre...`（译文对应“这团由畸变血肉组成的庞大聚合体可能曾经是个食人魔……”）。译文将名称定为“退化的食人魔碎肉”，“碎肉”通常意指散落碎屑或肉末，而该生物实际为庞大的畸变血肉团/聚合体实体。用词虽未造成硬性阻断，但形态传达略显偏离，记录为细微观察。

#### entry-02930
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/conclave-vault/objects.lua:47`。神器阿斯特里德的棍杖（ASTELRID_CLUBSTAFF）描述。译文将治愈工具与外科器械被扭曲为凶残武器的背景刻画得极其传神，“治疗魔法”符合术语规范。

#### entry-02931
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/zones/crypt-kryl-feijan/npcs.lua:30`。大恶魔 Boss `Kryl-Feijan`，与全库任务及背景文本（如 `kryl-feijan-escape.lua`）统一译名“克里尔·费扬”严格一致。
