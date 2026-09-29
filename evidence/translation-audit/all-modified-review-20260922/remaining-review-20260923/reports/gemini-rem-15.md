# 翻译审核报告：rem-15 批次（共 20 条）

**审核环境与授权模式**：只读 REVIEWER 自然语言审核旁路；依用户授权与 RULES.md 规定执行。未编写任何文件，未创建任何子代理，未读取其他非指定报告或任务状态文件。

---

## 一、逐条审核结论表

| 序号 | 条目编号 (Entry ID) | 审核结论 | 依据说明 / Claim 编号 |
| :--- | :--- | :--- | :--- |
| 1 | entry-03987 | **未发现问题** | 医疗炮台 NPC 描述准确，术语与结构一致。 |
| 2 | entry-03990 | **仅建议** | **C01**：“你（或任何其他目标）”中的“其他目标”指代施加效果的行动主体（any others），建议优化为“其他来源/其他人”以防与承受受体混淆。 |
| 3 | entry-03991 | **未发现问题** | 觉醒技能前置要求翻译准确简练。 |
| 4 | entry-03992 | **未发现问题** | 专名“拉克·肖的狡诈”与不死族分支名准确规范。 |
| 5 | entry-03993 | **未发现问题** | 专名“拉克·肖的狡诈”与食尸鬼分支名准确规范。 |
| 6 | entry-03996 | **存在问题** | **C02**：遗漏关键主体与触发限制“you deal to it”，译文“其受到的法术伤害”变相扩大为任意来源伤害触发，与源码及英文不符。 |
| 7 | entry-03997 | **存在问题** | **C03**：“Once put in a robe”误译为主客体倒错的“当你装备长袍的时候”；“current steam level”误译为“蒸汽等级”（实为当前蒸汽储量池）。 |
| 8 | entry-03998 | **未发现问题** | 觉醒技能前置成就名称引用准确，对应 600 单击伤害成就。 |
| 9 | entry-04000 | **仅建议** | **C04**：“while active”译为“启动时”易误判为瞬间消耗；该技能为持续型（sustained），建议澄清为“开启期间/激活状态下”。 |
| 10 | entry-04001 | **仅建议** | **C05**：回复速率遗漏“/回合”时间单位（6/turn 与 4/turn 简写为 +6 与 + 4），且存在多余空格。 |
| 11 | entry-04002 | **未发现问题** | 状态效果名与 `terms.json` 优选词“暮光回响”完全一致。 |
| 12 | entry-04003 | **未发现问题** | 减速叠加、刷新与上限机制翻译准确，两处 `%d%%` 占位符顺序与格式正确。 |
| 13 | entry-04004 | **未发现问题** | 状态效果描述准确完整。 |
| 14 | entry-04005 | **未发现问题** | 获得状态日志信息准确，`#Target#` 占位符与标点完好。 |
| 15 | entry-04006 | **未发现问题** | 获得状态日志信息准确，`#Target#` 占位符与标点完好。 |
| 16 | entry-04007 | **未发现问题** | UI 充能叠加描述准确传意，`%d` 占位符完好。 |
| 17 | entry-04008 | **存在问题** | **C06**：核心动作动词错译，“bores into”误译为“飞入”（实为附着并“钻入”目标头骨）。 |
| 18 | entry-04009 | **未发现问题** | 状态获得日志准确，混乱子类型语境契合，占位符完好。 |
| 19 | entry-04010 | **未发现问题** | 诅咒状态提示语准确，占位符完好。 |
| 20 | entry-04011 | **未发现问题** | 诅咒解除提示语准确，占位符完好。 |

---

## 二、疑点逐项详细核验（Claim 详情）

### C01 (entry-03990)
- **条目编号**：`entry-03990`
- **原译短引**：
  - 原文：`Each time you (or any others) would try to apply a cross-tier effect to this creature, you also try to apply the other two.`
  - 译文：`每次你（或任何其他目标）尝试对这个生物施加越层效果时，也将尝试施加其他两个越层效果。`
- **具体意义差异**：原文中的“any others”是指对该受害生物（this creature）施加越层效果的**其他攻击者／其他行动主体**。译文使用“其他目标”，在中文游戏语境中“目标”极易被误解为承受攻击的受体（即被攻击的对象），从而与后面的“这个生物”产生主客体歧义。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Combat.lua:33-46`
  - 机制：当生物带有 `EFF_INCOMING_DISASTERS` 状态时，一旦受到越层效果触发，便会联动触发另外两种越层判定，因此此处为对该生物进行攻击的任意实体。
- **最强等价读法与处理**：中文语法上“你（或任何其他目标）尝试对这个生物施加……”因处于施动主语位置，结合后句可以推断出是施动方，并非严重机制逆转；但措辞有瑕疵。判定为 **advisory（仅建议）**。
- **处理建议**：建议将“你（或任何其他目标）”修改为“你（或任何其他来源）”或“你（或任何其他攻击者）”。
- **状态**：`advisory`

---

### C02 (entry-03996)
- **条目编号**：`entry-03996`
- **原译短引**：
  - 原文：`Any spell damage you deal to it will ripple around in radius 4 as 160% arcane damage.`
  - 译文：`其受到的法术伤害转化为波纹，对半径 4 内的所有目标造成等同于该伤害 160% 的奥术伤害。`
- **具体意义差异**：原文与代码严格限定触发条件为**你对其造成的法术伤害**（`you deal to it`），而译文译为“其受到的法术伤害”，完全丢失了施法主体限定“你对其造成的”，将其泛化为任意受到的法术伤害。这会导致玩家误以为敌方、中立单位或其他友军对其造成的法术伤害也能触发奥术波纹。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:25-30`
  - 源码逻辑：
    ```lua
    callbackOnTakeDamage = function(self, t, src, x, y, type, dam, tmp)
        if dam <= 0 or src ~= self.summoner then return {dam=0} end
        ...
    ```
    明确检查 `src ~= self.summoner`，仅有召唤者（玩家）造成的伤害才触发反弹。译文缺失了该关键条件。
- **最强等价读法与处理**：该条目系机械装置 NPC 的描述，丢失主体直接导致技能效果机制理解偏差，不能视为等价表达。判定为 **confirmed（存在问题）**。
- **处理建议**：修改为“你对其造成的任何法术伤害转化为波纹，对半径 4 内的所有目标造成等同于该伤害 160% 的奥术伤害。”
- **状态**：`confirmed`

---

### C03 (entry-03997)
- **条目编号**：`entry-03997`
- **原译短引**：
  - 原文：`Once put in a robe, the Arcane Dynamo will regenerate Steam each time mana is spent and increase Spellpower based on current steam level.`
  - 译文：`当你装备长袍的时候，奥术发电机会在你消耗法力值的时候自动产生蒸汽，并根据蒸汽等级提升法术强度。`
- **具体意义差异**：
  1. **主客体与安装操作错译**：“Once put in a robe”中的动词主体是 Arcane Dynamo（奥术发电机插件），动作是将插件安装／镶嵌进长袍中（robe 为其唯一合法安装部位）。译文译成“当你装备长袍的时候”，主语变成玩家，动作变成穿上长袍，完全丢失了“必须先将奥术发电机镶嵌进长袍”这一核心机制前提。
  2. **数值概念错译**：“current steam level”指当前的蒸汽储量／蒸汽资源池数值（即当前存量比例），源码中法强加成公式为 `p = self:getSteam() / 100; return p * 80 - 20`。译文译成“蒸汽等级”，严重误导玩家以为是某种科技等级或技能等级（Rank/Tier）。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/electricity.lua:105`（`on_type = "armor", on_subtype = "cloth"`）
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1915-1925`（`getSpellpower = function(self, t) local p = self:getSteam() / 100 ...`）
- **最强等价读法与处理**：主客体错位与资源概念混淆属于客观可证的机制错译。判定为 **confirmed（存在问题）**。
- **处理建议**：修改为“一旦安装到长袍中，奥术发电机会在你每次消耗法力时回复蒸汽，并根据当前蒸汽储量提升法术强度。”
- **状态**：`confirmed`

---

### C04 (entry-04000)
- **条目编号**：`entry-04000`
- **原译短引**：
  - 原文：`The use of this device is very strenuous, increasing fatigue by 20%% while active.`
  - 译文：`使用这个装置非常的费力，启动时会增加 20%% 疲劳。`
- **具体意义差异**：该技能属于持续开启型技能（sustained talent），“while active”表示处于开启维持状态期间持续增加 20% 疲劳惩罚。译文“启动时”容易让玩家理解为仅在按键激活那一瞬间产生一次性惩罚或消耗。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/wil.lua:22-29`
  - 源码逻辑：`mode = "sustained"`，在 `activate` 中添加持续属性 `self:talentTemporaryValue(ret, "fatigue", 20)`，并在持续期间持续生效。
- **最强等价读法与处理**：日常口语中“启动时”有时可宽泛理解为“启动后生效状态下”，未完全颠覆机制，但存在潜在歧义。判定为 **advisory（仅建议）**。
- **处理建议**：建议调整为“开启期间会增加 20%% 疲劳”或“处于激活状态时增加 20%% 疲劳”。
- **状态**：`advisory`

---

### C05 (entry-04001)
- **条目编号**：`entry-04001`
- **原译短引**：
  - 原文：`Increasing steam regeneration by 6/turn, stun immunity by 30% and stamina regeneration by 4/turn.`
  - 译文：`蒸汽回复 +6，震慑免疫 +30%，体力回复 + 4。`
- **具体意义差异**：原文中清晰标明了“6/turn”与“4/turn”的回合频率单位，译文简写为“+6”与“+ 4”，遗漏了“/回合”；另外“+ 4”较前文多了一个不必要的空格。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/floor.lua:44-48`
- **最强等价读法与处理**：在 ToME4 属性面板中，蒸汽与体力回复基础属性默认按回合结算，中文玩家普遍能理解为每回合回复，属于略写风格。判定为 **advisory（仅建议）**。
- **处理建议**：建议规范补全单位并去除空格：“蒸汽回复 +6/回合，震慑免疫 +30%，体力回复 +4/回合。”
- **状态**：`advisory`

---

### C06 (entry-04008)
- **条目编号**：`entry-04008`
- **原译短引**：
  - 原文：`A mind drone bores into #Target#!`
  - 译文：`一个精神雄蜂飞入#Target#！`
- **具体意义差异**：“bore into”在这里是及物/不及物钻孔动词（to drill / bore into a surface），意思是附着并“钻入／钻进”目标的头骨。译文将“bores into”错译为“飞入”。
- **底层机制与源码核验**：
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua:85`
  - 文件：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua:105`
    源码对应技能详细说明明确写道：
    `If they encounter a creature they will latch on it and bore into its skull for 6 turns, disrupting its thoughts.`
    雄蜂在飞行接触生物后，会紧抓目标并“钻进头骨（bore into its skull）”长达 6 回合以干扰思维。此状态获得提示正是对应“钻入头骨”的恐怖动作，“飞入”不仅属于词义翻译错误，也彻底抹杀了该机械灵能惊悚设定的质感。
- **最强等价读法与处理**：“bore into”没有“飞入”之意（飞入应为 fly into）。属于明确的动词语义错译。判定为 **confirmed（存在问题）**。
- **处理建议**：修改为“一只精神雄蜂钻入#Target#！”（量词用“只”或“个”皆可）。
- **状态**：`confirmed`

---

## 三、批次汇总统计

- **总审核条目数**：20 条
- **未发现问题 (clean)**：14 条
- **存在问题 (confirmed)**：3 条（`entry-03996`, `entry-03997`, `entry-04008`）
- **仅建议 (advisory)**：3 条（`entry-03990`, `entry-04000`, `entry-04001`）
- **待确认 (pending)**：0 条

---

## 四、实际读取路径与来源版本限制说明

1. **实际读取文件清单**：
   - 规则与基准配置：
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-15.md`
   - 快照上下文：
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
   - 冻结 DLC 源码文件（SHA256 校验完全一致）：
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/turrets.lua` (`14dbc643...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/cun.lua` (`5ceb8d4c...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua` (`f66debe2...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/str.lua` (`675153b2...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/wil.lua` (`f4d21540...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/floor.lua` (`8f49d4ad...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/magical.lua` (`6b62a43d...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua` (`518309d2...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/electricity.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Combat.lua`
   - 固定 Commit Engine 源码：
     - `/workspace/t-engine4` (`624a67329fe2ad440c5b344785a9c73fcf22ae63`): `game/modules/tome/data/achievements/kills.lua`, `game/modules/tome/class/Actor.lua`
2. **版本限制声明**：
   - 本批次所有条目均属于 DLC《Embers of Rage》（orcs 组件）。
   - 依据 RULES.md 第 5 条：DLC 源码仅进行 SHA256 哈希校验固定（已全量核验通过），其仓库 commit 及具体目标版本在契约中未固定，**不得宣称已核验 1.7.4**。所有机制判定严格以冻结源文件（frozen sources）的实际调用链和实现事实为准。
   - 所有审核遵循只读旁路规范，未产生外部写入。
