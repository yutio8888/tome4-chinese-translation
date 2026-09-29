本批次为 **batch-059**（条目 entry-01746 至 entry-01785，共 40 条）。
文件哈希核对：`evidence/translation-audit/all-modified-review-20260922/batches/batch-059.md` 的 SHA-256 值为 `699f54fd85349f3b99adb4b1a3b712ebcd2536f68cefaafe2c7189aca56e6e21`，核对一致。

源码依据：固定版本提交 `624a67329fe2ad440c5b344785a9c73fcf22ae63`（mod-tome 映射路径 `game/modules/tome/`）。译文上下文基于仓库当前固定 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

逐条复核报告如下：

---

### entry-01746
- **位置**：mod-tome.lua:23626（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`#CADET_BLUE#Your %s has expired.`
- **译文**：`#CADET_BLUE#你的%s消失了。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 263 行，陷阱持续时间归零触发移除并返还体力时记录 `game.logPlayer(self.summoner, "#CADET_BLUE#Your %s has expired.", self:getName())`。颜色码 `#CADET_BLUE#` 与占位符 `%s` 匹配，译为“消失了”符合陷阱从地图移除的实际运行效果，与同文件条目 entry-01764 的表达习惯一致。

---

### entry-01747
- **位置**：mod-tome.lua:23634（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Prepare which traps? (maximum: %d, up to tier %d)%s`
- **译文**：`准备什么陷阱？(最多%d个，最高阶级 %d)%s`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 600 行，Trap Mastery 技能激活对话框标题，格式化参数依次为可选上限数 `nb`（`%d`）、可准备最高阶级 `math.min(5, self:getTalentLevelRaw(t))`（`%d`）以及换行冷却提示（`%s`），占位符顺序与类型均一致。

---

### entry-01748
- **位置**：mod-tome.lua:23644（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：` (normal trigger)`
- **译文**：` （常规触发）`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 621 行，原设为即爆陷阱被改回普通准备时追加在日志中的后缀字串。前导空格保留，括号使用规范。

---

### entry-01749
- **位置**：mod-tome.lua:23645（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`#LIGHT_BLUE#No changes to trap preparation.`
- **译文**：`#LIGHT_BLUE#陷阱准备未作更改。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 629 行，陷阱准备菜单未作任何变动时向玩家输出的日志，颜色码 `#LIGHT_BLUE#` 与语义完全匹配。

---

### entry-01750
- **位置**：mod-tome.lua:23646（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`#GREY#(see trap description)#LAST#`
- **译文**：`#GREY#（见陷阱描述）#LAST#`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 646 行，若陷阱技能无 `short_info` 时显示的默认回退文本，颜色码 `#GREY#` 与闭合码 `#LAST#` 均匹配。

---

### entry-01751
- **位置**：mod-tome.lua:23647（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  %sTier %d: %s#LAST#
  %s
  ```
- **译文**：
  ```text
  %s材质等级 %d：%s#LAST#
  %s
  ```
- **结论**：存在疑点
- **核验依据**：源码 `traps.lua` 第 651 行：
  `("%sTier %d: %s#LAST#\n%s"):tformat(trap.known and "#YELLOW#" or "#YELLOW_GREEN#", trap.tier, trap.name, trap.info)`
  其中 `%d` 对应 `trap.tier = tr.trap_mastery_level`，即该陷阱技能在陷阱精通体系中所要求的技能阶级（1 至 5 阶），而不是装备物品的“材质等级（material level/tier，如铁/钢等）”。译文将 `Tier %d` 译为“材质等级 %d”属于跨语境套用物品术语；同文件 entry-01747 中对应 `tier` 译为“阶级”，此处宜调整为“阶级 %d”或“等级 %d”。

---

### entry-01752
- **位置**：mod-tome.lua:23666（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 699 行，Lure 技能释放时若周围无可用空格生成的玩家日志，感叹号标点与原文一致。

---

### entry-01753
- **位置**：mod-tome.lua:23669（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Deploy a noisy lure that attracts all creatures within radius %d to it for %d turns.
  		It has %d life (based on your Cunning) and is very durable, with %d armor and %d%% resistance to non-physical damage.
  		At level 5, when the lure is destroyed, it will trigger some traps in a radius of 2 around it (check individual trap descriptions to see if they are triggered).
  		Use of this talent will not break stealth.
  ```
- **译文**：
  ```text
  抛出一个诱饵来吸引 %d 码半径内的所有生物，持续 %d 回合。
  		诱饵有 %d 生命（基于灵巧），且非常坚韧，拥有 %d 护甲和 %d%% 非物理伤害抗性。
  		在等级 5 时，当诱饵被摧毁时，它会触发其周围 2 码范围内的部分陷阱（请查看各陷阱自身的说明，以确认其是否会被触发）。
  		此技能不会打断潜行状态。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 748-753 行，Lure 技能的 `info`。参数依次为嘲讽半径（`%d`）、持续回合（`%d`）、诱饵生命（`%d`）、护甲（`%d`）、非物理抗性（`%d%%`），5 处占位符及转义百分号与源码完全对应，属性与技能机制表述准确。

---

### entry-01754
- **位置**：mod-tome.lua:23681（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`#LIGHT_BLUE#Cancelled Trap Priming.`
- **译文**：`#LIGHT_BLUE#取消即爆陷阱。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 800 行，Trap Priming 技能交互未选择新陷阱时的取消日志，颜色码与技能名对应准确。

---

### entry-01755
- **位置**：mod-tome.lua:23683（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`#LIGHT_GREEN#Preparing %s (instant trigger)`
- **译文**：`#LIGHT_GREEN#准备%s中（立刻触发）`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 809 行，设定即爆陷阱时的玩家日志，颜色码 `#LIGHT_GREEN#` 与占位符 `%s` 匹配无误。

---

### entry-01756
- **位置**：mod-tome.lua:23699（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Shrapnel (radius 2) deals %0.2f physical damage, reduces accuracy, armour, and defence by %d.`
- **译文**：`刀片（范围2）%0.2f 物理伤害，减少命中、护甲和闪避 %d。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 947 行，Springrazor Trap 的 `short_info`，参数分别为物理伤害数值（`%0.2f`）与削弱命中/护甲/闪避属性的数值（`%d`），占位符与属性名称翻译正确。

---

### entry-01757
- **位置**：mod-tome.lua:23703（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a pressure triggered trap that explodes into a radius 2 wave of razor sharp wire, doing %0.2f physical damage. Those struck by the wire may be shredded, reducing accuracy, armor and defence by %d.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置压力感应陷阱，触发后爆开半径 2 格的锋利刀片，造成 %0.2f 物理伤害。被击中的目标可能被刀片切割，命中、护甲和闪避下降 %d。
  		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 950-955 行，Springrazor Trap 的完整说明。占位符 `%0.2f`、`%d`、`%s` 顺序一致，末尾 `%s` 对应即爆状态追加提示。

---

### entry-01758
- **位置**：mod-tome.lua:23708（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Deals %0.2f physical damage and pins, slows (30%%), and wounds for an additional %0.2f damage over 5 turns).`
- **译文**：`%0.2f 物理伤害，定身、30%% 减速，5回合额外 %0.2f 流血伤害。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 989 行，Bear Trap 的 `short_info`。占位符 `%0.2f`、`30%%`、`%0.2f` 匹配无误。原文英文末尾存在多余的反括号“turns).”；译文整理为简明的中文短描述。

---

### entry-01759
- **位置**：mod-tome.lua:23713（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Deals %0.2f acid damage, disarms for %d turns.`
- **译文**：`%0.2f 酸性伤害，缴械 %d 回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1045 行，Disarming Trap 的 `short_info`，占位符 `%0.2f` 和 `%d` 均匹配。

---

### entry-01760
- **位置**：mod-tome.lua:23724（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a pressure triggered trap that collapses the ground under the target, dealing %0.2f physical damage while burying them (removing from combat) for 5 turns.
  Victims may resist being buried, in which case they are pinned (ignores 50%% pin immunity) instead.
  ```
- **译文**：
  ```text
  放置一个压力感应陷阱，目标经过时地面将坍塌，造成 %0.2f 物理伤害并将其埋在地下（暂时移出游戏）5 回合。
  如果目标抵抗被埋，那么他将被定身（无视 50%% 定身免疫）。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1170-1175 行，Pitfall Trap 的技能说明。占位符 `%0.2f` 和 `50%%` 匹配，暂时移出战斗（在地底埋藏 5 回合）机制解释准确。

---

### entry-01761
- **位置**：mod-tome.lua:23729（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Explodes (radius 2) for %0.2f physical damage, 50%% blind/daze for %d turns.`
- **译文**：`爆炸（半径2）造成 %0.2f 物理伤害，50%% 致盲/眩晕 %d 回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1247 行，Flash Bang Trap 的 `short_info`，占位符 `%0.2f`、`50%%`、`%d` 匹配正确。

---

### entry-01762
- **位置**：mod-tome.lua:23730（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a trap that explodes in a radius of 2, dealing %0.2f physical damage and blinding and dazing (50%% chance of each) any creature caught inside for %d turns.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置一个闪光陷阱。产生一个 2 码范围的爆炸，造成 %0.2f 物理伤害，致盲和眩晕目标 %d 回合（各 50%% 几率）。
  		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1251-1255 行，Flash Bang Trap 的完整说明。占位符 `%0.2f`、`%d`、`50%%`、`%s` 齐全，语义准确。

---

### entry-01763
- **位置**：mod-tome.lua:23739（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Fires a beam (range 5) at a foe each turn for %0.2f arcane damage.  Lasts %d turns.`
- **译文**：`每回合发射（射程5）的射线，造成 %0.2f 奥术伤害。持续 %d 回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1386 行，Beam Trap 的 `short_info`，占位符 `%0.2f`（伤害）与 `%d`（持续回合）匹配。

---

### entry-01764
- **位置**：mod-tome.lua:23740（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a magical trap that fires a beam of arcane energy at a random foe (within range 5) each turn for %d turns, inflicting %0.2f arcane damage.
  This trap requires 20 Magic to prepare and does not refund stamina when it expires.
  #YELLOW#Activates immediately when placed.#LAST#
  ```
- **译文**：
  ```text
  放置魔法陷阱，每回合朝 5 格内的随机敌人射出奥术射线，持续 %d 回合，造成 %0.2f 奥术伤害。
  该陷阱需要 20 魔法才能准备，消失时不返还体力。
  #YELLOW#放置后立刻激活。#LAST#
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1391-1395 行，格式化参数依次为持续回合 `dur`（`%d`）与伤害 `damDesc`（`%0.2f`），占位符顺序一致；颜色高亮标签 `#YELLOW#...#LAST#` 闭合完整。

---

### entry-01765
- **位置**：mod-tome.lua:23748（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Releases a radius 3 poison gas cloud, poisoning for %0.2f nature damage over 5 turns with a 25%% for enhanced effects.`
- **译文**：`释放范围 3的毒气，5回合内 %0.2f 自然伤害，25%% 几率强化毒素效果。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1461 行，Poison Gas Trap 的 `short_info`。英文原文字面漏写了 `chance`，译文顺畅补齐为“25%% 几率”，占位符 `%0.2f` 和 `25%%` 正确。

---

### entry-01766
- **位置**：mod-tome.lua:23756（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Explodes (radius 2):  Deals %0.2f cold damage and pins for 3 turns.  Area freezes (%0.2f cold damage, 25%% freeze chance) for 5 turns.`
- **译文**：`爆炸（范围 2）：%0.2f 寒冷伤害并定身 3 回合。范围冻结 (%0.2f 寒冷伤害，25%% 冻结几率) 5回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1533 行，Freezing Trap 的 `short_info`，占位符 `%0.2f`、`%0.2f` 与 `25%%` 完全匹配。

---

### entry-01767
- **位置**：mod-tome.lua:23757（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a trap that explodes into a radius 2 cloud of freezing vapour when triggered.  Foes take %0.2f cold damage and are pinned for 3 turns.
  		The freezing vapour persists for 5 turns, dealing %0.2f cold damage each turn to foes with a 25%% chance to freeze.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置一个陷阱，激活后产生半径 2 的冰冻气体，造成 %0.2f 寒冷伤害并定身 3 回合。
  		冰冻气体持续 5 回合，每回合造成 %0.2f 伤害，有 25%% 几率冻结。
  		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
  ```
- **结论**：细微观察
- **核验依据**：源码 `traps.lua` 第 1537-1542 行，Freezing Trap 的完整说明。占位符 `%0.2f`、`%0.2f`、`25%%`、`%s` 均匹配。细微观察：第二句原文 `dealing %0.2f cold damage each turn` 译作“每回合造成 %0.2f 伤害”，第二处遗漏了“寒冷”修饰，但首句已有“冰冻气体”和“寒冷伤害”，不影响理解。

---

### entry-01768
- **位置**：mod-tome.lua:23764（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Explodes (radius 2): stuns and combusts for %0.2f fire damage per turn for 3 turns.  Area deflagrates (%0.2f fire damage) for 5 turns.`
- **译文**：`爆炸（范围 2）：震慑并在3回合内每回合造成 %0.2f 火焰伤害。范围火焰 (%0.2f 火焰伤害) 持续5 回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1637 行，Dragonsfire Trap 的 `short_info`，占位符 `%0.2f` 与 `%0.2f` 均匹配。

---

### entry-01769
- **位置**：mod-tome.lua:23765（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a pressure triggered trap that explodes in a radius 2 cloud of searing flames when triggered, stunning foes with the blast (%0.2f fire damage per turn) for 3 turns.
  		The deflagration persists in the area for 5 turns, burning foes for %0.2f fire damage each turn.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置一个压力感应陷阱，激活后产生半径 2 的火云，震慑敌人 (每回合 %0.2f 火焰伤害) 3 回合。
  		火焰持续 5 回合，每回合燃烧造成 %0.2f 火焰伤害。
  		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1643-1647 行，Dragonsfire Trap 的完整说明，占位符 `%0.2f`、`%0.2f`、`%s` 匹配无误。

---

### entry-01770
- **位置**：mod-tome.lua:23795（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Radius 2 antimagic: Drains up to %d mana, %d vim, %d positive/negative, deals up to %0.2f arcane damage.  Removes %d magical effects and silences for %d turns.`
- **译文**：`半径 2 反魔：吸收至多 %d 法力，%d 活力，%d 正负能量，造成至多 %0.2f 奥术伤害。解除 %d 项魔法效果，沉默 %d 回合。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1941 行，Purging Trap 的 `short_info`，格式化参数依次为 `base`（法力）、`base/2`（活力）、`base/4`（正负能量）、`damDesc`（奥术伤害）、`nb`（解除魔法数）、`dur`（沉默回合），6 处占位符 `%d, %d, %d, %0.2f, %d, %d` 顺序与类型完全对应。

---

### entry-01771
- **位置**：mod-tome.lua:23796（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a trap that releases a burst of antimagic energies (radius 2), draining up to %d mana, %d vim, %d positive and %d negative energies from affected targets, while inflicting up to %0.2f arcane damage based on the resources drained, silencing for %d turns, and removing up to %d beneficial magical effects or sustains.
  		The draining effect scales with your Willpower, and you must have 25 Willpower to prepare this trap.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置一个陷阱，触发后释放半径 2 的反魔能量波，吸取至多 %d 法力 , %d 活力 , %d 正能量和 %d 负能量，并造成至多 %0.2f 奥术伤害（基于吸取能量），沉默 %d 回合，并解除至多 %d 项正面魔法状态或者维持技能。
  		吸取效果受意志加成，你需要 25 点意志来使用该技能。
  		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 1954-1959 行，Purging Trap 完整说明，参数顺序依次为法力（`%d`）、活力（`%d`）、正能量（`%d`）、负能量（`%d`）、奥术伤害（`%0.2f`）、沉默回合（`%d`）、驱散增益数（`%d`）、即爆提示（`%s`），占位符顺序和类型完全对应。

---

### entry-01772
- **位置**：mod-tome.lua:23804（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Explodes (radius 2) for %0.2f fire damage over 3 turns.`
- **译文**：`爆炸（半径 2）：3回合内 %0.2f 火焰伤害。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2024 行，Explosion Trap 的 `short_info`，占位符 `%0.2f` 匹配无误。

---

### entry-01773
- **位置**：mod-tome.lua:23805（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：
  ```text
  Lay a simple yet effective trap that explodes in a radius 2 on contact, setting those affected on fire for %0.2f fire damage over 3 turns.
  		This trap can use a primed trigger and a high level lure can trigger it.%s
  ```
- **译文**：
  ```text
  放置一个简单而有效的陷阱，有目标接触陷阱时，它会在半径 2 范围内爆炸，使受影响的目标着火，并在 3 回合内造成 %0.2f 点火焰伤害。
  		该陷阱可以被设置为直接激活，也可以被高等级的诱饵激活。%s
  ```
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2029-2032 行，Explosion Trap 完整说明，占位符 `%0.2f` 与 `%s` 匹配无误。

---

### entry-01774
- **位置**：mod-tome.lua:23811（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Target knocked back up to %d grids%s and dazed.`
- **译文**：`目标被击退最多 %d 格%s，并眩晕。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2085 行，Catapult Trap 的 `desc`，`%d` 为击退格数 `self.dist`，`%s` 接收罗盘方向字串 ` (%s)`，占位符与语义匹配无误。

---

### entry-01775
- **位置**：mod-tome.lua:23812（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`%s knocks %s back!`
- **译文**：`%s 将 %s 击退！`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2106 行：
  `game.logSeen(who, "%s knocks %s back!", self:getName():capitalize(), who:getName():capitalize())`
  第一个 `%s` 为陷阱实体名，第二个 `%s` 为目标生物名。译文“%s 将 %s 击退！”主谓宾参数顺序与逻辑一致。

---

### entry-01776
- **位置**：mod-tome.lua:23813（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`%s fails to knock %s back!`
- **译文**：`%s 未能将 %s 击退！`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2111 行：
  `game.logSeen(who, "%s fails to knock %s back!", self:getName():capitalize(), who:getName():capitalize())`
  第一个 `%s` 为陷阱实体名，第二个 `%s` 为目标生物名。译文“%s 未能将 %s 击退！”参数顺序与逻辑一致。

---

### entry-01777
- **位置**：mod-tome.lua:23825（`mod-tome/data/talents/cunning/traps.lua`）
- **原文**：`Lay a trap armed with potent venom.  A creature passing over it will be dealt %0.2f nature damage and be stunned and poisoned for %0.2f nature damage per turn for 4 turns.`
- **译文**：`放置一个涂了颠茄毒素的陷阱，经过的生物会受到 %0.2f 自然伤害，并被震慑和中毒 4 回合，中毒每回合造成 %0.2f 自然伤害。`
- **结论**：未发现问题
- **核验依据**：源码 `traps.lua` 第 2223 行，Nightshade Trap 完整说明，参数分别为自然伤害 `dam`（`%0.2f`）与每回合毒素伤害 `dam/10`（`%0.2f`），占位符匹配无误。

---

### entry-01778
- **位置**：mod-tome.lua:23843（`mod-tome/data/talents/cursed/advanced-shadowmancy.lua`）
- **原文**：
  ```text
  Target a nearby shadow, and force it to slam into a nearby enemy, dealing %0.1f Physical damage.
  		Your shadow will then set them as their target, and they will target your shadow.
  		Damage increases with your Mindpower.
  ```
- **译文**：
  ```text
  指定附近的一个阴影，令其攻击附近的一个敌人，造成 %0.1f 物理伤害。
  		你的阴影将把那个敌人设为目标，而敌人也会攻击那个阴影。
  		伤害受精神强度加成。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `advanced-shadowmancy.lua` 第 59-65 行，Stone 技能说明。占位符 `%0.1f` 匹配，阴影位移、造成物理伤害并嘲讽互锁机制表述准确。

---

### entry-01779
- **位置**：mod-tome.lua:23858（`mod-tome/data/talents/cursed/advanced-shadowmancy.lua`）
- **原文**：
  ```text
  Share your hatred with all shadows within sight range, gaining temporary full control. You then fire a blast of pure hatred from all affected shadows, dealing %0.1f Mind damage per blast.
  		You cannot cancel this talent once the first bolt is cast.
  		Damage increases with your Mindpower.
  ```
- **译文**：
  ```text
  和视野内的所有阴影共享你的仇恨，获得临时的完全控制。随后你从所有受影响的阴影中发射一道纯粹的仇恨冲击，每道造成 %0.1f 精神伤害。
  		一旦发射了第一道，便无法取消该技能。
  		伤害受精神强度加成。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `advanced-shadowmancy.lua` 第 187-193 行，Cursed Bolt 技能说明。占位符 `%0.1f` 匹配，伤害类型“精神伤害”与属性加成“精神强度”翻译准确。

---

### entry-01780
- **位置**：mod-tome.lua:23872（`mod-tome/data/talents/cursed/bloodstained.lua`）
- **原文**：
  ```text
  Teleport to an enemy, striking them for 100%% weapon damage, bleeding them for %d%% weapon damage over five turns, and marking them for six turns. You will not teleport if you are already adjacent.

  When the marked enemy dies, the cooldown of this talent will be reduced by two turns for every turn the mark had remaining.

  Each point in Bloodstained talents reduces the amount of damage you take from bleed effects by 2%%
  ```
- **译文**：
  ```text
  传送至一个敌人面前，攻击造成 100%% 武器伤害，使其在5回合里受到相当于 %d%% 武器伤害的流血伤害，并标记它6回合。如果目标已经在你身边，则不会传送。

  被标记的敌人死亡时，标记每剩余一回合此技能的冷却减少2回合。

  每一点血染系技能使你受到的流血伤害减少2%%。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `bloodstained.lua` 第 98-106 行，Blood Rush 技能说明。占位符 `100%%`、`%d%%`、`2%%` 均保持双百分号转义，分段及各项机制表述准确。

---

### entry-01781
- **位置**：mod-tome.lua:23912（`mod-tome/data/talents/cursed/crimson-templar.lua`）
- **原文**：
  ```text
  When you kill an enemy, their death forms a cursed magical pattern on the ground. This creates a circle of radius %d which blinds enemies and deals them %0.2f light damage, while giving you %d positive energy per turn. The circle lasts for %d turns.
  							The damage will increase with your Spellpower.
  							The duration of the circle can be increased by a critical hit.
  							The blind chance increases with your Spellpower.
  							You can activate this talent to draw the pattern in your own blood, creating it underneath you at the cost of %d%% of your maximum life.

  ```
- **译文**：
  ```text
  当你杀死敌人时，死亡会在地面上形成一个魔法咒印。产生一个半径 %d 的法阵，会致盲敌人并造成 %0.2f 光系伤害，同时每回合给予你 %d 正能量。法阵持续 %d 回合。
  							伤害受法术强度加成。
  							持续时间可以暴击。
  							致盲概率受法术强度加成。
  							你可以主动使用这一技能，支付 %d%% 最大生命，用自己的鲜血在脚下绘制咒印。

  ```
- **结论**：未发现问题
- **核验依据**：源码 `crimson-templar.lua` 第 54-61 行。格式化参数依次为半径 `rad`（`%d`）、伤害 `burn`（`%0.2f`）、固定恢复正能量值 2（`%d`）、持续时间 `dur`（`%d`）以及生命消耗百分比 `cost`（`%d%%`）。5 处占位符顺序与类型一致，制表缩进与换行结构完全吻合。

---

### entry-01782
- **位置**：mod-tome.lua:23948（`mod-tome/data/talents/cursed/cursed-aura.lua`）
- **原文**：`The %s lies defiled at your feet. An aura of hatred surrounds you and you now feel truly cursed. You have gained the Cursed Aura talent tree and 1 point in Defiling Touch, but at the cost of 2 Willpower.`
- **译文**：`你的脚下躺着被亵渎的%s。一股仇恨的气息笼罩了你，你感到自己真正被诅咒了。你获得了诅咒光环技能树和等级 1 的诅咒之触，但是需永久消耗 2 点意志。`
- **结论**：未发现问题
- **核验依据**：源码 `cursed-aura.lua` 第 172 行，剧情弹窗。代码中执行 `self:incIncStat(Stats.STAT_WIL, -2)`，永久减少角色基础意志 2 点；译文“需永久消耗 2 点意志”准确阐明了机制，占位符 `%s` 匹配无误。

---

### entry-01783
- **位置**：mod-tome.lua:23980（`mod-tome/data/talents/cursed/cursed-aura.lua`）
- **原文**：
  ```text
  Your curses bring you dark gifts. Unlocks bonus level %d effects on all of your curses, allowing you to gain that effect when the power level of your curse reaches that level. At talent level 5, the luck penalty of cursed effects is reduced to 1.
  		Talent levels above 5 add bonus power levels to your curses, increasing their effects (currently %0.1f).
  ```
- **译文**：
  ```text
  你的诅咒带来黑暗的礼物。解锁所有诅咒第 %d 层效果，并允许你在诅咒达到该等级时获得此效果。
  		在等级 5 时，因诅咒带来的幸运惩罚降到 1。
  		等级 5 以上时为诅咒增加额外能量等级，增强其效果（当前增加 %0.1f）。
  ```
- **结论**：未发现问题
- **核验依据**：源码 `cursed-aura.lua` 第 299-304 行，Dark Gifts 技能说明。占位符 `%d` 与 `%0.1f` 匹配，幸运惩罚降低与超过 5 级附加额外 power levels 机制翻译准确。

---

### entry-01784
- **位置**：mod-tome.lua:24031（`mod-tome/data/talents/cursed/cursed.lua`）
- **原文**：`Your weapon yearns for its next victim.`
- **译文**：`你的武器渴望着下一个牺牲者。`
- **结论**：未发现问题
- **核验依据**：源码 `cursed.lua` 第 19 行，`cursed/slaughter`（杀戮）技能系分类描述，翻译贴合原文语境。

---

### entry-01785
- **位置**：mod-tome.lua:24033（`mod-tome/data/talents/cursed/cursed.lua`）
- **原文**：`Each day, you lift your weary body and begin the unending hunt.`
- **译文**：`你不知疲倦无时无刻狩猎你的下一个目标。`
- **结论**：存在疑点
- **核验依据**：源码 `cursed.lua` 第 20 行：
  `newTalentType{ allow_random=true, type="cursed/endless-hunt", name = _t("endless hunt", "talent type"), description = _t"Each day, you lift your weary body and begin the unending hunt." }`
  本条存在明显语义背离与反义翻译：
  1. 原文 `weary body`（疲惫/劳累的身躯）描写被诅咒者在折磨下每天勉力支起疲惫残躯，译文却写成相反的“你不知疲倦”，出现反义错译，破坏了角色悲惨折磨的基调。
  2. 原文 `Each day`（每一天/每日）被译为“无时无刻”；`begin the unending hunt`（开启无尽的狩猎，呼应技能系名称 endless hunt）被改写为“狩猎你的下一个目标”（疑似受前一条 01784 “next victim” 串文干扰）。建议核对原文语境重新校对。