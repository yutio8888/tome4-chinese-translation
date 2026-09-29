以下为针对 11 条冻结条目（`spot-01` 至 `spot-11`）的语境与固定源码核验结果：

### spot-01
- **核验结果**：未发现问题
- **说明**：出自 `boss-artifacts-far-east.lua`（Whip of Urh'Rok），恶魔领主名与战无不胜传说描述准确，符合术语规范。

### spot-02
- **核验结果**：未发现问题
- **说明**：出自 `gem.lua`（BASE_GEM 宝石名），`lapis lazuli` 译为“青金石”，术语与词义准确。

### spot-03
- **核验结果**：未发现问题
- **说明**：出自 `world-artifacts.lua`（Gloves of the Firm Hand），神器背景描述、内外侧触感与大地能量固定地面的机制叙述完整准确。

### spot-04
- **核验结果**：未发现问题
- **说明**：出自 `world-artifacts.lua`（Honeywood Chalice），树液木杯的描述与饮用感官叙述准确。

### spot-05
- **核验结果**：未发现问题
- **说明**：出自 `talents/chronomancy/timetravel.lua`（Time Skip），时空伤害、移出时间线回合与法术强度加成描述均准确，格式符 `%0.2f` 与 `%d` 一致。

### spot-06
- **核验结果**：存在实质机制与语义错误
- **问题说明及依据**：
  1. **暴击机制严重曲解（实质语义与机制错误）**：
     - **原文**：`You have a %d%% chance to shrug off all direct critical hits (physical, mental, spell).`
     - **冻结译文**：`你受到的直接暴击（物理、精神、法术）的额外伤害降低 %d%%。`
     - **源码依据**：`talents/gifts/ooze.lua` 中该技能（Indiscernible Anatomy）的被动实现为 `self:talentTemporaryValue(p, "ignore_direct_crits", t.critResist(self, t))`。在 ToME 机制中，`ignore_direct_crits` 是**概率完全无视/抵消直接暴击**（使受到的暴击退化为普通命中，即“shrug off critical hits”），而译文写成了“**额外伤害降低 %d%%**”（暴击伤害/暴击倍率削减，属于 `combat_critical_power` 类削减机制）。该处把“概率完全无视暴击”曲解为“削减暴击额外伤害”，与游戏实际生效机制和英文原文均存在实质背离。
  2. **术语不一致**：
     - 原文第三句 `resistance to disease, poison, wounds and blindness`，译文为 `流血和目盲免疫`；而冻结术语快照中 `wound` 统一定为 `创伤`（`T.GAME.EFFECT wound 创伤`），`blind` 统一定为 `致盲`（`T.GAME.EFFECT blind 致盲`）。

### spot-07
- **核验结果**：未发现问题
- **说明**：出自 `talents/gifts/summon-advanced.lua`（Wild Summon），全部 10 种野性生物额外特异能力叙述准确，前置要求 `Master Summoner` 准确对齐技能译名“召唤精通”（`mod-tome.lua:25489`），格式符与排版无误。

### spot-08
- **核验结果**：未发现问题
- **说明**：出自 `talents/psionic/nightmare.lua`，`source_tag` 为 `talent name`，技能名译为“梦魇降临”，与下文召唤物实体名（“暗夜恐魔”）做了明确区分，符合上下文语境。

### spot-09
- **核验结果**：未发现问题
- **说明**：出自 `talents/techniques/archery.lua`（Shoot 技能说明），“远程投射武器”与同文件、同系列技能上下文保持一致。

### spot-10
- **核验结果**：未发现问题
- **说明**：出自 `talents/techniques/techniques.lua`，作为射击类技能在缺少发射器时的动态插入词（对应 `You require a %s to use this talent.`），译为“远程投射武器”符合句式插值与上下文语境。

### spot-11
- **核验结果**：未发现问题
- **说明**：出自 `init.lua`（Loading tips），纪元名称统一遵循术语表（`Age of Pyre` -> “烈火纪”），阿塔玛森与加库尔的背景史实叙述准确流畅。
