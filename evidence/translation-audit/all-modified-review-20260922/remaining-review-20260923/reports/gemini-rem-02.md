# 翻译审查报告：rem-02 批次（40条）

本审查为只读独立 REVIEWER 审查，严格遵循 `RULES.md`、`terms.json` 及公开源码调用链。本批共 40 条冻结译文，均归属于 DLC 兽人战役（`component=orcs`）。

---

## 一、 逐条判定汇总表

| 序号 | 条目 ID | 审核判定 | Claim / 简要依据 |
| :--- | :--- | :--- | :--- |
| 1 | entry-03785 | 未发现问题 | 术语与机制描述准确（削减属性的疾病）。 |
| 2 | entry-03786 | 未发现问题 | 寒冷伤害并减速表达准确。 |
| 3 | entry-03787 | 未发现问题 | 酸性伤害降低护甲表达准确。 |
| 4 | entry-03789 | 未发现问题 | `stralite` 对应术语“斯莱特”一致。 |
| 5 | entry-03790 | 未发现问题 | `#Source#` 战斗日志与动作动词完整。 |
| 6 | entry-03791 | 未发现问题 | 闪电伤害与资源吸取机制准确。 |
| 7 | entry-03792 | 未发现问题 | 拟声词“轰。”简洁忠实。 |
| 8 | entry-03793 | 未发现问题 | `stralite` 对应术语“斯莱特”一致。 |
| 9 | entry-03794 | 未发现问题 | `stralite` 对应术语“斯莱特”一致。 |
| 10 | entry-03795 | 未发现问题 | 占位符 `%d` 与 `%s` 匹配，伤害亲和表达准确。 |
| 11 | entry-03796 | 未发现问题 | 占位符 `%d` 与 `%s` 匹配，伤害亲和表达准确。 |
| 12 | entry-03797 | 未发现问题 | 占位符 `%d` 与 `%s` 匹配，伤害亲和表达准确。 |
| 13 | entry-03798 | 未发现问题 | 冷却回合描述无误。 |
| 14 | entry-03799 | 仅建议 | **C01**（代词“These boots”译为“火箭靴”，与通用组件重名）。 |
| 15 | entry-03800 | 未发现问题 | 三处占位符与颜色标记完整，与子句拼接顺畅。 |
| 16 | entry-03801 | 仅建议 | **C02**（参数重排正确，但中文“被致残毒素”缺失谓语）。 |
| 17 | entry-03802 | 未发现问题 | 击退反冲日志准确。 |
| 18 | entry-03803 | 未发现问题 | 较高项判定与冰冻几率机制准确。 |
| 19 | entry-03804 | 未发现问题 | 枪械背景风味对话口语化翻译贴切。 |
| 20 | entry-03805 | 未发现问题 | 占位符 `%s` 顺序与主宾格结构准确。 |
| 21 | entry-03806 | 未发现问题 | 灵晶近战触发与蒸汽强度加成机制准确。 |
| 22 | entry-03807 | 仅建议 | **C03**（动态剩余冷却提示译为“冷却时间”，易被误判为固定冷却时长）。 |
| 23 | entry-03808 | 未发现问题 | 心灵灼烧、心灵脑叶切除、碾碎心灵三大技能术语统一。 |
| 24 | entry-03809 | 仅建议 | **C04**（`airborne probes` 漏译“空载/空中”修饰）。 |
| 25 | entry-03810 | 未发现问题 | 伤害与不死族加倍机制表达无误。 |
| 26 | entry-03811 | 存在问题 | **C05**（`shrapnel` 错译为“榴弹”，且遗漏锥形起点 `from the target`）。 |
| 27 | entry-03812 | 未发现问题 | 战斗日志占位符匹配。 |
| 28 | entry-03813 | 未发现问题 | 谚语意译传神，符合装备主动防御机制。 |
| 29 | entry-03815 | 存在问题 | **C06**（`every third hit` 遗漏“每”，导致周期触发被误读为单次）。 |
| 30 | entry-03816 | 未发现问题 | 颜色代码与占位符匹配。 |
| 31 | entry-03818 | 未发现问题 | 日志主宾占位符格式化正确。 |
| 32 | entry-03819 | 未发现问题 | 风味文本描述忠实。 |
| 33 | entry-03820 | 未发现问题 | 树人召唤冷却描述无误。 |
| 34 | entry-03821 | 未发现问题 | `Blindside` 精准对应技能术语“闪电突袭”。 |
| 35 | entry-03822 | 未发现问题 | 攻速与紊乱值上限比例机制准确。 |
| 36 | entry-03823 | 存在问题 | **C07**（形近词误读：`spilt` 错认作 `split`，错译为“心血之作分离”）。 |
| 37 | entry-03825 | 未发现问题 | 法袍触发提升抗性日志准确。 |
| 38 | entry-03826 | 未发现问题 | 奥术发电机强化日志准确。 |
| 39 | entry-03827 | 仅建议 | **C08**（漆黑护目镜对“运作原理”的惊叹被偏移为“使用方法”）。 |
| 40 | entry-03828 | 未发现问题 | 基础原料名称与术语一致。 |

---

## 二、 原子疑点详情（Claims）

### C01 | entry-03799 | advisory
- **条目 ID**：`entry-03799`
- **原译短引**：
  - 原文：`These boots have a %d%% chance to fail to operate properly (reduced by Cunning).`
  - 译文：`火箭靴有%d%%几率失败（随灵巧降低）。`
- **具体意义差异**：
  本条目所属物品为世界神器 `Anti-Gravity Boots`（反重力鞋），原文主语使用指示代词短语 `These boots` 指代当前鞋子。译文直译为专有名词“火箭靴”，然而在兽人战役工匠系统中，存在同名的通用脚部插件 `rocket boots`（即快照 1381 行的 `%s rocket boots` -> `%s 火箭靴`）。将本神器的被动代词定名为主观专名“火箭靴”，会导致玩家将神器与通用工匠插件产生混淆。此外，`fail to operate properly` 简省为“失败”虽不致理解障碍，但偏向口语。
- **最强等价读法与处理**：
  译者可能是结合下文风味说明中火箭喷射推力理解为火箭靴，但指代当前神器应保持中立代词以避免重名。
  建议处理：`这双靴子有 %d%% 几率无法正常运作（随灵巧降低）。`
- **状态**：`advisory`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1499`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1499)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:174`
  - 冲突项参考：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/mechanical.lua:36`

---

### C02 | entry-03801 | advisory
- **条目 ID**：`entry-03801`
- **原译短引**：
  - 原文：`fire a poisonous bolt out to range %d that deals %d nature damage and afflicts the target with crippling poison (%d%% fail chance) that deals %d addition nature damage over %d turns (damage based on Cunning)`
  - 译文：`发射一支射程最远为 %d 码的毒箭，造成 %d 点自然伤害，并导致目标被致残毒素（%d%% 行动失败几率），在 %d 回合内造成 %d 点额外自然伤害（伤害受灵巧值加成）`
- **具体意义差异**：
  源码第 280 行通过参数重排 `{1, 2, 3, 5, 4}` 正确调换了第 4 占位符（回合数）与第 5 占位符（额外自然伤害），参数映射无缺陷。但在汉化句式组织上，“并导致目标被致残毒素（...）”出现明显的动词脱落（缺少“感染”或“折磨”），主谓宾结构残缺（“导致目标被[名词]”而无后接谓语）。
- **最强等价读法与处理**：
  可理解为译者意图表达“导致目标被致残毒素感染”但漏敲了动词。建议修正以理顺语法：
  建议处理：`发射一支射程最远为 %d 码的毒箭，造成 %d 点自然伤害，并使目标感染致残毒素（%d%% 行动失败几率），在 %d 回合内造成 %d 点额外自然伤害（伤害受灵巧值加成）`
- **状态**：`advisory`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1509`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1509)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:280`

---

### C03 | entry-03807 | advisory
- **条目 ID**：`entry-03807`
- **原译短引**：
  - 原文：`(cooling down: %d turns)`
  - 译文：`(冷却时间：%d 回合)`
- **具体意义差异**：
  在源码第 581 行中，该描述属于动态条件输出：`self.power < maxp and ("(cooling down: %d turns)"):tformat(maxp - self.power) or _t"Ready to trigger!"`。此处的 `%d` 是 `maxp - self.power`，代表**当前剩余冷却回合数**。译文“冷却时间：%d 回合”在中文惯用表述中会被自然理解为该技能/神器的“总冷却时长”，而不是“冷却中倒计时”，容易导致玩家产生机制误读。
- **最强等价读法与处理**：
  等价读法下“冷却时间：X回合”在部分汉化中被笼统当作冷却状态标签，但不够精准。
  建议处理：`（冷却中：%d 回合）` 或 `（距离冷却完毕还有 %d 回合）`。
- **状态**：`advisory`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1551`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1551)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:581`

---

### C04 | entry-03809 | advisory
- **条目 ID**：`entry-03809`
- **原译短引**：
  - 原文：`Through a combination of magic and airborne probes, these shots incite powerful bolts of lightning to strike your target from above, frying them and those around them!`
  - 译文：`这些弹药通过魔法和探针从天空引导强力的闪电冲击你的目标，灼烧目标及周边的单位！`
- **具体意义差异**：
  原文前置名词短语 `airborne probes` 的修饰限定词 `airborne`（空载的、升空的）在名词翻译中被漏掉（仅译作“探针”）。虽然译者在后文添加了“从天空引导”，保留了空间方位概念，但原设定中弹药附带升空探测器/信标的机械构想被弱化。
- **最强等价读法与处理**：
  可视为将修饰词后置融入后句动作，无实质机制破坏。
  建议处理：`这些弹药通过魔法与空载探针相结合，从高空引来强力的闪电劈向你的目标，灼烧目标及周边的单位！`
- **状态**：`advisory`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1560`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1560)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:646`

---

### C05 | entry-03811 | confirmed
- **条目 ID**：`entry-03811`
- **原译短引**：
  - 原文：`Release a burst of shrapnel, dealing physical damage equal to your steampower in a cone from the target of radius 4.`
  - 译文：`释放榴弹，在半径4锥形范围内造成等于蒸汽强度的物理伤害。`
- **具体意义差异**：
  存在两处实质错漏：
  1. **武器术语错译**：`shrapnel` 是“弹片/破片/霰片”，而非“榴弹”（grenade）。
  2. **关键机制范围起点遗漏**：原文明确为 `in a cone from the target of radius 4`。根据源码第 715–720 行的投影实现（`tg = {type="cone", range=0, radius=4, friendlyfire=false, start_x=target.x, start_y=target.y}`），该锥形爆炸的**起点是被击中的目标（target）**并朝远离攻击者的方向喷射，而不是从玩家自身射出。译文删除了 `from the target`，仅表述为“在半径4锥形范围内”，极易误导玩家误以为是自身射出常规锥形攻击，属于明确的机制说明遗漏与词义错误。
- **最强等价读法与处理**：
  无可等价读法，机制判定起点缺失与弹种错误必须修正。
  建议处理：`释放一阵弹片，以目标为起点在半径 4 的锥形范围内造成等于你蒸汽强度的物理伤害。`
- **状态**：`confirmed`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1569`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1569)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:714-720`

---

### C06 | entry-03815 | confirmed
- **条目 ID**：`entry-03815`
- **原译短引**：
  - 原文：`every third hit always crits.`
  - 译文：`第三下攻击必定暴击。`
- **具体意义差异**：
  原文为世界神器 `Golden Gun` 的命中被动效果。源码第 1081–1090 行充能逻辑证实：
  ```lua
  o.charge = o.charge + 1
  if o.charge == 3 then
      o.combat.physcrit=100
      o.charge = 0
  else
      o.combat.physcrit=0
  end
  ```
  每累计命中 3 次（即第 3、6、9、12……次），该次攻击必定暴击并清零重计。原文 `every third hit` 中的 `every` 表明这是周期性重复触发。原译将其简化为“第三下攻击必定暴击”，在中文语境下被理解为“单次生效的第 3 次攻击必定暴击”（类似前两下不暴击、第三下暴击后即失效），丢失了循环周期量词，导致核心战斗机制严重失真。
- **最强等价读法与处理**：
  无法等价解读，周期量词不可遗漏。
  建议处理：`每第 3 次命中必定暴击。` 或 `每 3 次攻击必定暴击一次。`
- **状态**：`confirmed`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1613`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1613)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:1081-1090`

---

### C07 | entry-03823 | confirmed
- **条目 ID**：`entry-03823`
- **原译短引**：
  - 原文：
    ```text
    There is an attached note.
     
    'I've spilt the heartsblood of my work, feeling it pound, like a heart, in my palms.
    Some people just can't let go until they've bled dry.'
    ```
  - 译文：
    ```text
    上面粘着一页笔记。

    '我将我的心血之作分离，感受它的跳动，像心脏一样跳动，在我的手心里。
    总有些人不到血流尽，不撒手。'
    ```
- **具体意义差异**：
  原文所属物品为神器蒸汽链锯 `Heartrend`（撕心锯/心脏切割）。关键句为：`I've spilt the heartsblood of my work`。
  `spilt` 是动词 `spill`（倾洒、泼出、洒出鲜血）的过去分词形式，与后文的 `heartsblood`（心血）、`pound, like a heart`（如心脏般跳动）以及 `bled dry`（流干鲜血）形成极其强烈的残虐流血意象。
  译文显然发生了形近词误读，将 `spilt` 错误看成了 `split`（分离、分裂），并把 `the heartsblood of my work` 曲解为宾语“我的心血之作”，最终拼接成了毫无血腥关联的“我将我的心血之作分离”。这属于因单词混淆导致的严重叙事变异，完全破坏了神器剧情的风味。
- **最强等价读法与处理**：
  无法等价解读，`spill` 与 `split` 含义截然不同。
  建议处理：
  ```text
  上面附着一张便签。

  “我将我作品的心血洒出，感受着它如心脏般在我的手掌中跳动。
  总有些人不到流尽最后一滴血，便绝不肯放手。”
  ```
- **状态**：`confirmed`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1740`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1740)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:2088-2091`

---

### C08 | entry-03827 | advisory
- **条目 ID**：`entry-03827`
- **原译短引**：
  - 原文：`How do these even work?`
  - 译文：`这玩意到底怎么用？`
- **具体意义差异**：
  该文本为世界神器 `X-Ray Goggles`（X射线护目镜）的描述。该神器的未鉴定名为 `pitch black goggles`（漆黑的护目镜，完全不透光），使用效果却是能看穿一切。因此，原文 `How do these even work?` 是主角对这副全黑眼镜“运作原理/如何起效”的荒谬感叹（work = 运转、发挥作用）。原译“这玩意到底怎么用？”将对“运作机理”的惊叹偏移成了对“使用说明/操作方法”的疑问（How to use）。
- **最强等价读法与处理**：
  口语泛化处理下读者仍能感受一定困惑语境，无机制破坏，列为建议。
  建议处理：`这玩意到底是怎么起作用的？` 或 `这东西究竟是怎么运作的？`
- **状态**：`advisory`
- **来源路径行号**：
  - 快照：[`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:1791`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1791)
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/world-artifacts.lua:2396`

---

## 三、 实际读取路径与限制声明

1. **实际读取文件清单**：
   - 规则与词汇：
     - [`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md)
     - [`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json)
     - [`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json)
   - 批次与快照：
     - [`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-02.md`](file:///home/paseo/.paseo/worktrees/2p1pqs
