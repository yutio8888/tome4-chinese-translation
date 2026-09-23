## 40条译文复核判定总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03413 | 存在问题 | C01（存在问题：漏译恶魔并扩大为史诗生物）、C02（仅建议：成功语气过定与空格） |
| entry-03414 | 未发现问题 | 召唤空间不足日志，标点与句意完整无误 |
| entry-03415 | 未发现问题 | 传送选点提示日志，省略号与原文一致 |
| entry-03416 | 仅建议 | C03（仅建议：上限距离表述为“码外”稍欠精确） |
| entry-03417 | 未发现问题 | 恶魔之血被动数值与属性加成完整准确 |
| entry-03418 | 未发现问题 | 深渊护盾护甲、反击与按活力比例减伤逻辑准确 |
| entry-03419 | 存在问题 | C04（存在问题：遗漏“乘算叠加”关键机制修饰语） |
| entry-03420 | 存在问题 | C05（存在问题：伤害类型暗影误译为黑暗伤害） |
| entry-03421 | 未发现问题 | 硬化之核护甲公式与法强提升对应准确 |
| entry-03422 | 未发现问题 | 枯萎之盾反击诅咒机制准确，沿袭上游描述持续回合 |
| entry-03423 | 未发现问题 | 法术失效日志准确无误 |
| entry-03424 | 待确认 | C06（待确认：持续4回合符合快照源码但脱离英文原文3回合，版本适用性待确认） |
| entry-03425 | 未发现问题 | 灵魂焚净负面清除与灼烧伤害比例、伤害亲和术语准确 |
| entry-03426 | 未发现问题 | 地狱吐息锥形范围、恶魔治疗与法术暴击机制准确 |
| entry-03427 | 未发现问题 | 烈焰重生治疗全额分摊与自身不可减免机制准确 |
| entry-03428 | 未发现问题 | 苦痛链接选择源生物提示准确 |
| entry-03429 | 未发现问题 | 苦痛链接选择受害者提示准确 |
| entry-03430 | 未发现问题 | 苦痛链接伤害传递比例与击杀重置冷却准确 |
| entry-03431 | 存在问题 | C07（存在问题：遗漏近战攻击限制条件）、C08（存在问题：暗影伤害误译为黑暗伤害） |
| entry-03432 | 未发现问题 | 恶魔尸傀格式化后缀与全角括号规范准确 |
| entry-03433 | 存在问题 | C09（存在问题：遗漏“近战攻击命中”关键限制条件） |
| entry-03434 | 未发现问题 | 灼魂之罚武器伤害、抗性削减与延时伤害结算准确 |
| entry-03435 | 未发现问题 | 爆裂冲锋双手武器与移动限制提示准确 |
| entry-03436 | 未发现问题 | 毁灭者变身天赋11个占位符与各技能强化机制对应准确 |
| entry-03437 | 存在问题 | C10（存在问题：遗漏特定目标点并将最远射程误译为半径） |
| entry-03438 | 仅建议 | C11（仅建议：爆炸伤害表述与重置冷却时间润色） |
| entry-03439 | 未发现问题 | 武器恶魔附魔提示准确，占位符完好 |
| entry-03440 | 存在问题 | C12（存在问题：遗漏主语“武器”，主客体混淆） |
| entry-03441 | 未发现问题 | 烈焰状态结束日志完整，标点匹配 |
| entry-03442 | 未发现问题 | 目标受折磨日志准确，占位符完好 |
| entry-03443 | 未发现问题 | 灵魂燃烧打断休息提示准确，句末标点匹配 |
| entry-03444 | 未发现问题 | 恶魔种子感染长描述与成熟概率逻辑准确 |
| entry-03445 | 未发现问题 | 酸浴双抗性与伤害亲和提升描述准确 |
| entry-03446 | 未发现问题 | 苦痛链接分摊延迟日志与高亮标记完整 |
| entry-03447 | 未发现问题 | 黑暗支配伤害亲和与负生命存活机制准确 |
| entry-03448 | 未发现问题 | 黑冰层数提示格式化准确 |
| entry-03449 | 未发现问题 | 火焰庇护伤害亲和与枯萎抗性削减数值准确 |
| entry-03450 | 未发现问题 | 饮血者死亡触发条件长描述准确 |
| entry-03451 | 未发现问题 | 效果子类型 affinity 译为伤害亲和，全篇一致 |
| entry-03452 | 未发现问题 | 痛苦协调全系伤害亲和长描述准确 |

---

## 详细复核 Claim 列表

### C01 | entry-03413 | 存在问题
- **原文短引**：`Implanting a seed into unique demons, if successful, will always try to grant a seed of that type, if available.`
- **译文短引**：`如果成功将种子植入史诗生物（Unique）的体内，且它有对应的恶魔种子的话，你必定会获得该恶魔种子。`
- **问题具体内容**：对象与范围扩大错误。原文明确限定为 `unique demons`（史诗/独特恶魔），译文错译为泛指的“史诗生物（Unique）”，漏掉了“恶魔”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua:364-369`（`createSeed` 函数内）：
  ```lua
  if host.type == "demon" then
      kind = host.name
      if not demon_seeds_effects[kind] then kind = rng.table(seeds[lvl]) end
  else
      kind = rng.table(seeds[lvl])
  end
  ```
  代码明确检查宿主实体类型是否为 `demon`；只有恶魔宿主才会匹配自身名字并给予对应的恶魔种子。非恶魔的史诗生物（如人形怪、亡灵等 Unique）进入 `else` 分支，只能随机获取通用种子池中的种子，绝不会获得对应生物的专属种子。译文遗漏“恶魔”导致机制描述失真，误导玩家对任何史诗生物植入种子。

---

### C02 | entry-03413 | 仅建议
- **原文短引**：`If the attack hits a demonic seed tries to take hold inside your foe...`
- **译文短引**：`如果攻击命中，你会将恶魔种子植入目标体内...`；`造成 %d%% 盾牌伤害并眩晕 敌人 %d 回合。`
- **建议简述**：偏好与轻度润色。原文为“tries to take hold”，植入本身受后续几率（5%–100%）限制，“你会将恶魔种子植入”语气稍显绝对，但下文已明确说明存活几率，未构成不可逆信息断裂；另“眩晕 敌人”之间存在一处多余空格。两者均不属于阻断性事实缺陷，列为建议。
- **状态**：仅建议

---

### C03 | entry-03416 | 仅建议
- **原文短引**：`Teleports you randomly within a small range of up to %d grids with %d precision.`
- **译文短引**：`传到 %d 码外的一个位置，误差 %d。`
- **建议简述**：措辞偏好。原文“within a small range of up to %d grids”指最大射程为 %d 码范围，“传到 %d 码外”易被误读为传送至固定的 %d 码距离。但由于玩家在实际操作中需要选取目标格，且属于 ToME 空间传送类技能的通用表述，未导致参数或机制严重偏离，仅属润色偏好。
- **状态**：仅建议

---

### C04 | entry-03419 | 存在问题
- **原文短引**：`This effect stacks multiplicatively up to %d times.`
- **译文短引**：`这个效果能叠加至最多 %d 层。`
- **问题具体内容**：关键数学/机制修饰语遗漏。原文明确声明“stacks multiplicatively”（以乘算方式叠加），译文完全漏译了“乘算/以乘算方式”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:805, 817`（`DARK_REIGN` 效果）：
  ```lua
  local p = 1 for i = 1, old_eff.stacks do p = p * 0.92 end p = 100 * (1 - p)
  ```
  亲和计算逻辑是经典的乘算法则（每层吸收剩余伤害的 8%，实际亲和为 $100\% \times (1 - 0.92^n)$）：1 层为 8%，2 层为 15.36%（而非加算的 16%），3 层为 22.13%（而非 24%）。缺少“乘算”，玩家会按照线性加算预期效果，丢失了核心数值机制信息。

---

### C05 | entry-03420 | 存在问题
- **原文短引**：`Pay %d%% of your current life and gain 100%% darkness damage conversion for 1 turns.`
- **译文短引**：`支付 %d%% 当前生命值，1 回合内你造成的所有伤害转化为黑暗伤害。`
- **问题具体内容**：伤害类型术语错误。将伤害类型 `darkness damage` 误译为“黑暗伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  按术语表（`INPUT.md:691`）明确规则：`darkness` 在伤害类型语境（`T.GAME.DAMAGE`，combat）下标准译名为“暗影”；`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua:32` 亦为 `DamageType.DARKNESS`。同树前一天赋 entry-03419 均译为“暗影伤害”，同效果 Buff 描述 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:845`（`context.lua:112`）亦为“你的所有伤害转化为暗影伤害”。译为“黑暗伤害”造成系统伤害类型概念混乱。

---

### C06 | entry-03424 | 待确认
- **原文短引**：`...allowing you to see all enemies within %d spaces for the next 3 turns.`
- **译文短引**：`...让你能够在 4 回合内觉察到 %d 码内的所有敌对生物。`
- **问题具体内容**：数值与英文原文不一致（原文 3 turns vs 译文 4 回合）。经核对公开快照源码，代码实际行为与译文一致，但与原文字面冲突；因 DLC 源码未固定 commit，目标版本适用性保留待确认。
- **状态**：待确认
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/fearfire.lua:75`：
  ```lua
  self:setEffect(self.EFF_SENSE, 4, {
      range = rad,
      actor = 1,
  })
  ```
  公开快照源码中实际施加的持续时间确实是硬编码的 4 回合（`EFF_SENSE, 4`），而英文字符串硬编码写着 `3 turns`，属于上游代码与技能文本脱节。译文虽然反映了快照源码行为，但由于 ashes-urhrok DLC 来源未固定 commit（`source-access.json:23` 为 unpinned），无法完全排除目标正式版本是否向上游文本统一为 3，目标版本适用性缺口保留为待确认。

---

### C07 | entry-03431 | 存在问题
- **原文短引**：`Any time you damage this foe in melee while it bleeds you get healed for %d (this can only happen once per turn).`
- **译文短引**：`每次你攻击被恶魔角刺穿的目标时，你回复 %d 生命（每回合至多 1 次）。`
- **问题具体内容**：关键机制与操作条件遗漏。原文严格限定“in melee”（近战）且“damage”（造成伤害），译文简略翻译为“每次你攻击...”，遗漏了“近战”和“造成伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:683-686`（`EFF_DEMONIC_CUT` 效果）：
  ```lua
  callbackOnMeleeHit = function(self, eff, src, dam)
      if not dam or dam <= 0 or src ~= eff.src then return end
      src:heal(eff.heal)
  ...
  ```
  该效果的生命回复回调挂在 `callbackOnMeleeHit` 上，明确要求必须是近战命中且造成有效伤害（`dam > 0`）。若玩家使用远程法术、弓箭或未造成有效伤害的攻击，均无法触发治疗。遗漏“近战”使玩家无法知晓真实的技能触发生效范围。

---

### C08 | entry-03431 | 存在问题
- **原文短引**：`...causing it to bleed black blood for 50%% of the damage done as darkness over 5 turns.`
- **译文短引**：`...流血 5 回合，合计受到额外 50%% 黑暗伤害。`
- **问题具体内容**：伤害类型术语错误。将 `as darkness` 伤害类型错译为“黑暗伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua:153`：
  ```lua
  DamageType:get(DamageType.DARKNESS).projector(self, tgt.x, tgt.y, DamageType.DARKNESS, dam)
  ```
  代码明确使用 `DamageType.DARKNESS`。依据术语表（`INPUT.md:691`），`darkness` 在伤害类型分类（`T.GAME.DAMAGE`）下统一确立为“暗影”，不得译为“黑暗”。

---

### C09 | entry-03433 | 存在问题
- **原文短引**：`Your successful melee hits apply a stacking effect that decreases damage done by %d%%.`
- **译文短引**：`你的攻击能够惊吓目标，降低目标 %d%% 的伤害。`
- **问题具体内容**：触发条件关键限定词遗漏。原文明确为“successful melee hits”（近战攻击命中），译文直接泛化为“你的攻击”，遗漏了“近战”与“命中”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/oppression.lua:72-75`：
  ```lua
  callbackOnMeleeAttack = function(self, t, target, hitted)
      local tt = self:isTalentActive(t.id)
      if not tt then return end
      if not hitted then return end
  ...
  ```
  代码通过 `callbackOnMeleeAttack` 回调监听，并且严格检验 `if not hitted then return end`。该技能树的核心设计即“通过近战贴身并命中敌人提供防御”（见该文件行 22 设计注释），法术与远程攻击均不触发。译文直接写“你的攻击”，丢失了关键的作用方式和门槛。

---

### C10 | entry-03437 | 存在问题
- **原文短引**：`Hasten yourself out of phase, teleporting you to a specific location up to %d spaces away.`
- **译文短引**：`加速自身，以至于脱离空间，传送半径 %d。`
- **问题具体内容**：范围机制与玩家操作信息丢失且失真。原文为“teleporting you to a specific location up to %d spaces away”（将你传送至最远 %d 码内的一个指定位置），译文篡改为“传送半径 %d”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/misc/races.lua:40, 47, 56-68`：
  ```lua
  range = function(self, t) return self:attr("control_haste_doom") and 5 or 4 end,
  ...
  target = function(self, t) return {type="beam", range=self:getTalentRange(t), nolock=true, talent=t} end,
  ...
  self:teleportRandom(x, y, 0)
  ```
  该技能为精准定向位移技能，瞄准类型为 `beam`，目标范围参数是最大施法距离 `range`（4 或 5 码），落点精度为 0（即精确传送至玩家点击的目标空地 `x, y`）。译文写成“传送半径 %d”，完全丢失了“指定位置”的操作属性，且将“最远距离/射程”误导为“以自身为中心的随机传送半径”，严重误导机制理解。

---

### C11 | entry-03438 | 仅建议
- **原文短引**：
  - `...triggers a darkness explosion of radius 1 for half the damage...`
  - `...when you transform the cooldowns of Haste of the Doomed and Pitiless are reset`
- **译文短引**：
  - `...在半径 1 的范围内产生一次暗影爆炸，造成额外 50%% 伤害...`
  - `...变形时重置种族技能“末日加速”与种族技能“无情”`
- **建议简述**：措辞偏好。爆炸伤害在代码中为 `DamageType.DARKNESS, val / 2`，译文表达为“额外 50% 伤害”在数学上等价，但表述为“造成相当于该次伤害 50% 的暗影伤害”在 AoE 语境下更严谨；重置技能处遗漏了“冷却时间”，但在汉语游戏语境中“重置技能”通常理解为重置冷却。两者均属建议。
- **状态**：仅建议

---

### C12 | entry-03440 | 存在问题
- **原文短引**：`#Target#'s weapon looks less threatening.`
- **译文短引**：`#Target#的危险度看起来降低了。`
- **问题具体内容**：实体主语严重遗漏与语义错置。原文主语为 `#Target#'s weapon`（目标的武器），译文漏译了 `weapon`，将受词错置为 `#Target#` 本身。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:51-52`（`DEMON_BLADE` 状态）：
  ```lua
  on_gain = function(self, err) return _t"#Target# imbues its weapon with demonic fire.", _t"+Demon Blade" end,
  on_lose = function(self, err) return _t"#Target#'s weapon looks less threatening.", _t"-Demon Blade" end,
  ```
  该状态为恶魔之刃状态，获得时为“给武器附魔”，结束时自然是“武器看起来不再那么危险”。译文丢弃“武器”，变成描述目标本身的危险度降低，导致游戏状态提示日志主客体严重失真。

---

## 核验路径与环境记录

1. **实际读取的所有路径与版本**：
   - 入口与冻结配置：
     - `.../experiments/abc20-g07-20260923/INPUT.md`
     - `.../experiments/abc20-g07-20260923/entries.json`
     - `.../experiments/abc20-g07-20260923/context.lua`
     - `.../experiments/abc20-g07-20260923/source-access.json`
   - 本组 13 份已授权公开 DLC 源码快照（哈希严格匹配 `source-access.json`，版本标注为公开未固定快照）：
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua` (SHA256: `5fc8f608...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demonic-strength.lua` (SHA256: `cc3daff1...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua` (SHA256: `e7f8cb9d...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/doom-shield.lua` (SHA256: `f1a7dc7a...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/fearfire.lua` (SHA256: `c2faeddb...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/heart-of-fire.lua` (SHA256: `9169ec69...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua` (SHA256: `8de1db04...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/npcs.lua` (SHA256: `881a2757...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/oppression.lua` (SHA256: `4df44bc8...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/torture.lua` (SHA256: `c9845ad5...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/wrath.lua` (SHA256: `f2297854...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/misc/races.lua` (SHA256: `66694c67...`)
     - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua` (SHA256: `eb183d02...`)
2. **额外源码路径的调用链来源**：
   - 本次复核所有涉及技能与状态的调用链路均闭合于上述 13 份预授权 sections 快照源码单文件内部，未读取任何外部额外单文件。
3. **无法核验或越界声明**：
   - 无任何越界读取操作。未读取其他实验材料、未读取其他模型报告或生产记录、未修改工作树任何文件、未创建子 agent。
   - 所有机制分析均基于 `source-access.json` 中哈希匹配的公开快照事实， Ashes of Urh'Rok DLC 来源未固定 commit，涉及差异已在 C06 明确标注为“待确认”保留缺口。本报告为只读独立评审观察，不宣称生产 DONE_VERIFIED。
