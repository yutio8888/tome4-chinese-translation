# 只读 REVIEWER 审核报告：rem-14（20条）

## 一、审核概述与版本说明

- **审核范围**：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-14.md` 中的 20 个条目（`entry-03965` 至 `entry-03986`）。
- **核验模式**：全量独立初审与交叉比对，逐条核验主客体、条件、时序、范围、数值、术语、占位符及动态标记。
- **DLC 来源与版本限制声明**：
  - 本批次所有条目均属于 `Embers of Rage`（orcs）DLC，组件来源为公开 GPL v3 代码。
  - DLC 源码通过 `source-access.json` 中登记的 SHA256 哈希值进行冻结固定核验，本轮已对涉及的 6 份源码文件逐一核验 SHA256 并完全匹配（见文末读取路径表）。
  - **版本限制**：DLC 仓库源码未固定目标发布版本或 upstream commit，不得宣称已核 1.7.4 目标发布版本；判定依据以登记的冻结基线文件实际行为为准。

---

## 二、逐条审核判定表（按输入顺序）

| 条目编号 (Entry ID) | 位置与组件 | 判定结果 | 依据与关联 Claim |
| :--- | :--- | :---: | :--- |
| **entry-03965** | snapshots/tome-orcs.lua:5521 (other.lua) | **未发现问题** | 占位符 `%s` 匹配，log 动词及主宾结构准确一致。 |
| **entry-03966** | snapshots/tome-orcs.lua:5522 (other.lua) | **未发现问题** | 参数与占位符 `%0.2f`, `%d`, `%d` 对应无误，震慑机制与数值说明忠实。 |
| **entry-03967** | snapshots/tome-orcs.lua:5552 (other.lua) | **存在问题** | C01（shot 误译为“弹片”）；C02（漏译 `as it is the ammo`）；C03（叙事动作泛化）。 |
| **entry-03968** | snapshots/tome-orcs.lua:5573 (other.lua) | **未发现问题** | 击退日志主客体与标点准确一致。 |
| **entry-03969** | snapshots/tome-orcs.lua:5593 (other.lua) | **未发现问题** | 拖动抵抗日志忠实对应。 |
| **entry-03970** | snapshots/tome-orcs.lua:5594 (other.lua) | **存在问题** | C04（两处漏译 `up to` 至多）；C05（漏译 `as it is the ammo`）；C06（漏译 hook 特征修饰语并增译“打击”）。 |
| **entry-03971** | snapshots/tome-orcs.lua:5610 (other.lua) | **存在问题** | C07（`bolt` 误译为“闪电球”）；C08（漏译 `up to` 且“周围 %d 的敌人”语病缺量词）；C09（漏译 `as it is the ammo`）；C10（漏译 voltaic）。 |
| **entry-03972** | snapshots/tome-orcs.lua:5628 (other.lua) | **存在问题** | C11（漏译专名修饰语 `Nourishing`）；C12（漏译 `as it is the ammo`）；C13（语序严重倒装生硬及漏译 botanical）。 |
| **entry-03973** | snapshots/tome-orcs.lua:5649 (other.lua) | **存在问题** | C14（`global speed` 术语违规译为“整体速度”）；C15（`Toxin strength` 机制误译为“枯萎伤害”）；C16（漏译 `as it is the ammo`）；C17（漏译 toxic）。 |
| **entry-03974** | snapshots/tome-orcs.lua:5667 (other.lua) | **未发现问题** | 科技法术机制、法术强度、法力转化蒸汽参数 `%d`、`%d`、`%d%%` 及样式标签准确。 |
| **entry-03975** | snapshots/tome-orcs.lua:5702 (physics.lua) | **未发现问题** | 紧凑蒸汽罐容量增加说明简明准确。 |
| **entry-03977** | snapshots/tome-orcs.lua:5742 (sawmaiming.lua) | **存在问题** | C18（`The power and damage` 简缩漏译流血增幅威力随蒸汽强度提升）；C19（漏译 narrow 狭窄锥形修饰及 slam 弱化）。 |
| **entry-03978** | snapshots/tome-orcs.lua:5815 (steam.lua) | **未发现问题** | 灵晶（mindstar）与蒸汽科技（steamtech）术语及动词灌注/掌握准确。 |
| **entry-03979** | snapshots/tome-orcs.lua:5825 (steam.lua) | **未发现问题** | 重装武器类别描述忠实通顺。 |
| **entry-03980** | snapshots/tome-orcs.lua:5835 (steam.lua) | **未发现问题** | 颜色标签 `#VIOLET#` 完整，EUREKA 意译自然。 |
| **entry-03981** | snapshots/tome-orcs.lua:5836 (steam.lua) | **未发现问题** | 占位符与颜色标签完整，符合 `schematic` -> `配方` preferred 术语规范。 |
| **entry-03983** | snapshots/tome-orcs.lua:5839 (steam.lua) | **未发现问题** | 斜体标签 `#{italic}#...#{normal}#` 与叙事省略号准确。 |
| **entry-03984** | snapshots/tome-orcs.lua:5853 (thoughts-of-iron.lua) | **仅建议** | C20（`bore into its skull` 动作泛化；英文原句双重否定已正确处理）。 |
| **entry-03985** | snapshots/tome-orcs.lua:5890 (turrets.lua) | **仅建议** | C21（标点叹号与 terms.json preferred 全角句号存在微差）。 |
| **entry-03986** | snapshots/tome-orcs.lua:5902 (turrets.lua) | **未发现问题** | 火焰炮台实体描述准确无误。 |

---

## 三、疑点明细 (Claims)

### C01: `entry-03967` shot 误译为“弹片”
- **原译短引**：“当每一个弹片击中它的目标”
- **具体意义差异**：原文为 `When each shot reaches its target, it does normal steamgun damage...`。双持蒸汽枪射击时会发射两枚子弹（shot），命中目标时分别造成正常蒸汽枪伤害并产生范围爆炸。原译将 `shot`（射击/子弹）错译为“弹片”（shrapnel），完全违背机制行为。
- **最强等价读法与处理**：等价读法无法将主射击投射物等同于弹片。应修正为“当每发子弹命中其目标时”。
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1338-1342`
- **缺失证据**：无。源码 `archeryAcquireTargets(..., {one_shot=true, type="steamgun"})` 与 `archeryShoot` 证明该投射物为 steamgun 的 shot（子弹/射击）。

### C02: `entry-03967` 漏译 `as it is the ammo`
- **原译短引**：“这个技能不使用弹药。”
- **具体意义差异**：原文为 `This talent does not use ammo as it is the ammo.`。同组所有特殊弹药技能均具有“弹药技能本身即充当弹药，因此无需额外消耗弹药”的设定说明（参见 Flare Shell 等译作“这个技能本身就是弹药，因此不消耗弹药”）。原译漏译了后半句因果说明。
- **最强等价读法与处理**：虽然玩家能看出不耗弹药，但缺失了技能自备弹药的机制与风味说明。应补全为“此技能本身即为弹药，因此不消耗弹药。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1340`
- **缺失证据**：无。

### C03: `entry-03967` 第一句叙事动作泛化
- **原译短引**：“你使用蒸汽枪在射程内制造一场特殊的爆炸。”
- **具体意义差异**：原文为 `You fire a special explosive shot with your steamgun(s) at a spot within range.`。原文是“发射一发特殊的爆炸弹”，原译泛化为“制造一场特殊的爆炸”，弱化了射击动作，且与同文件其他 Shell 技能句式脱节。
- **最强等价读法与处理**：表达虽在广义上能理解，但动作偏差明显。建议对齐同类技能改为：“你用蒸汽枪向射程内的一处地点发射特殊爆炸弹。”
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1337`
- **缺失证据**：无。

### C04: `entry-03970` 两处漏译 `up to`（至多）
- **原译短引**：“他们被拉向你 %d 码 / 你会被拉向空地 %d 码”
- **具体意义差异**：原文两处均为 `pulled up to %d tiles towards ...`。位移受到距离与地形阻挡限制，并非必定拉扯满额距离。原译遗漏“至多 / 最多”（up to），造成机制承诺过强。
- **最强等价读法与处理**：等价读法不能抹消上限限定词。应修正为：“至多被拉向你 %d 格”与“你至多会被拉向该位置 %d 格”。
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1608-1610`
- **缺失证据**：无。源码 `target:pull(self.x, self.y, t.distance(self, t))` 表明拉扯为上限。

### C05: `entry-03970` 漏译 `as it is the ammo`
- **原译短引**：“这个技能不使用弹药。”
- **具体意义差异**：同 C02，原文 `This talent does not use ammo as it is the ammo.` 漏译因果分句。
- **最强等价读法与处理**：补全为“此技能本身即为弹药，因此不消耗弹药。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1611`
- **缺失证据**：无。

### C06: `entry-03970` 漏译 hook 特征修饰语及增译“打击”
- **原译短引**：“发射特殊弹药打击目标或某处”
- **具体意义差异**：原文为 `You fire a special hook shot with your steamgun(s) at a target creature or location.`。技能名为 Hook Shell（钩链弹），此处 shot 特指钩爪/钩链弹，原译泛化为“特殊弹药”；且 Hook Shell 为纯位移技能，无直接伤害判定，原译增译“打击”易误导玩家以为具有攻击伤害。
- **最强等价读法与处理**：建议修正为：“你用蒸汽枪向目标生物或地点发射一枚特殊钩链弹。”
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1607`
- **缺失证据**：无。

### C07: `entry-03971` `Each bolt` / `Bolt damage` 误译为“闪电球”
- **原译短引**：“每个闪电球造成 %0.2f 的闪电伤害 / 闪电球伤害受蒸汽强度加成。”
- **具体意义差异**：原文承接前句的 `powerful electrical currents`，写道 `Each bolt does %0.2f lightning damage.` 与 `Bolt damage scales with Steampower.`。源码中 `tg = {type="beam", range=5}`，粒子效果为 `lightning` 射线电弧，并非球体（ball/orb）；且译文与技能名 Voltaic Shell（伏特弹）脱节，误导玩家机制为产生散开的球形飞行物。
- **最强等价读法与处理**：无法将电弧射线读作“球”。应修正为“每道电弧/闪电造成 %0.2f 闪电伤害”与“电弧伤害受蒸汽强度加成”。
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1670-1678, 1690-1693`
- **缺失证据**：无。

### C08: `entry-03971` 漏译 `up to` 且“周围 %d 的敌人”缺量词语病
- **原译短引**：“打击周围 %d 的敌人。”
- **具体意义差异**：原文为 `at up to %d nearby enemies`（参数对应技能等级，至多选取 %d 名附近敌人）。原译遗漏“至多”（up to），且“周围 %d 的敌人”缺少量词（名/个），语病明显。
- **最强等价读法与处理**：应修正为“打击附近至多 %d 名敌人”。
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1689`
- **缺失证据**：无。源码循环 `for i = 1, math.floor(self:getTalentLevel(t)) do ... if #tgts <= 0 then return end` 证实有上限且目标不足时提前退出。

### C09: `entry-03971` 漏译 `as it is the ammo`
- **原译短引**：“这个技能不使用弹药”
- **具体意义差异**：同 C02，漏译 `as it is the ammo`。
- **最强等价读法与处理**：补全为“此技能本身即为弹药，因此不消耗弹药。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1692`
- **缺失证据**：无。

### C10: `entry-03971` 漏译 voltaic 特征修饰语
- **原译短引**：“你使用蒸汽枪发射特殊弹药打击目标”
- **具体意义差异**：原文 `special voltaic shot` 特指伏特弹/电气弹，原译泛化为“特殊弹药”。
- **最强等价读法与处理**：建议修正为“你用蒸汽枪向目标发射特殊伏特弹”。
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1688`
- **缺失证据**：无。

### C11: `entry-03972` 漏译专有名词修饰语 `Nourishing`
- **原译短引**：“生长成半径 %d 的苔藓 %d 回合。”
- **具体意义差异**：原文为 `spores which grow into Nourishing Moss in a radius of %d for %d turns.`。源码中地图效果专用类型为 `DamageType.NOURISHING_MOSS`（滋养苔藓），原译漏译 `Nourishing`，只写“苔藓”，丢失专有名词定位。
- **最强等价读法与处理**：不可遗漏专名。应修正为“生长出半径为 %d 的滋养苔藓，持续 %d 回合”。
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1753, 1771`
- **缺失证据**：无。

### C12: `entry-03972` 漏译 `as it is the ammo`
- **原译短引**：“这个技能不使用弹药”
- **具体意义差异**：同 C02，漏译 `as it is the ammo`。
- **最强等价读法与处理**：补全为“此技能本身即为弹药，因此不消耗弹药。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1774`
- **缺失证据**：无。

### C13: `entry-03972` 句式倒装生硬及漏译 botanical
- **原译短引**：“每回合苔藓造成 %0.2f 自然伤害对半径内的每一个敌人。”
- **具体意义差异**：原译生硬直译英文后置状语（“造成...伤害对...”），语序严重倒装；同时第一句 `special botanical shot` 泛化为“特殊弹药”，漏译 botanical（植物弹）。
- **最强等价读法与处理**：建议修正语序为：“每回合苔藓对半径范围内的每个敌人造成 %0.2f 自然伤害。”第一句补全“特殊植物弹”。
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1770, 1772`
- **缺失证据**：无。

### C14: `entry-03973` 术语违规：`global speed` 译为“整体速度”
- **原译短引**：“并且降低整体速度 %d%% %d 回合。”
- **具体意义差异**：原文为 `reducing their global speed by %d%% for %d turns.`。`terms.json` 明确将 `global speed` 裁定为 preferred 术语 `全局速度`，并注明：“装备、技能和叙述中的全局行动速度机制；不写作‘整体速度’”。原译明确违反术语库约束。
- **最强等价读法与处理**：应直接按术语库统一为“全局速度”。
- **状态**：`confirmed`
- **来源路径行号**：`terms.json`（行号见 `terms.json: global speed` 行）；`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1849`
- **缺失证据**：无。

### C15: `entry-03973` 机制误译：`Toxin strength` 译为“枯萎伤害”
- **原译短引**：“枯萎伤害受蒸汽强度加成。”
- **具体意义差异**：原文为 `Toxin strength scales with Steampower.`。源码中 `getPower = function(self, t) return 10 + self:combatTalentSteamDamage(t, 0, 50) end`；而在命中效果中：`target:setEffect(target.EFF_METAL_POISONING, ..., {power=t.getPower(self, t), speed=t.getPower(self, t)-10, ...})`。即 `getPower` 同时决定每回合的枯萎伤害以及降低的全局速度数值！原文 `Toxin strength` 准确指代该重金属毒素的整体效果强度（伤害与减速），原译擅自改译为“枯萎伤害”，掩盖了减速比例也受蒸汽强度加成的机制事实。
- **最强等价读法与处理**：无法等价。应忠实修正为：“毒素强度受蒸汽强度加成。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1829, 1832, 1851`
- **缺失证据**：无。

### C16: `entry-03973` 漏译 `as it is the ammo`
- **原译短引**：“这个技能不使用弹药。”
- **具体意义差异**：同 C02，漏译 `as it is the ammo`。
- **最强等价读法与处理**：补全为“此技能本身即为弹药，因此不消耗弹药。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1850`
- **缺失证据**：无。

### C17: `entry-03973` 漏译 toxic 特征修饰语
- **原译短引**：“你使用蒸汽枪发射特殊弹药打击目标”
- **具体意义差异**：原文 `special toxic shot` 特指毒气弹/剧毒弹，原译泛化为“特殊弹药”。
- **最强等价读法与处理**：建议修正为“你用蒸汽枪向目标发射特殊剧毒弹”。
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1847`
- **缺失证据**：无。

### C18: `entry-03977` 简缩漏译流血加深威力受蒸汽强度提升
- **原译短引**：“伤害受蒸汽强度加成。”
- **具体意义差异**：原文为 `The power and damage improves with your Steampower.`。技能源码中包含两个独立函数：`getDamageInc`（流血伤害加深百分比，即 power，对应第 3 个格式化参数）与 `getDamage`（喷血物理伤害，即 damage，对应第 4 个格式化参数），两者均通过 `combatTalentSteamDamage` 随蒸汽强度成长。原译将 `The power and damage` 简缩为“伤害”，造成玩家误以为仅喷血造成的物理伤害受蒸汽强度加成，而流血增幅威力不受加成。
- **最强等价读法与处理**：等价读法无法涵盖两项机制。应修正为：“流血加深效果与伤害均受蒸汽强度提升。”或“其威力与伤害受蒸汽强度加成。”
- **状态**：`confirmed`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/sawmaiming.lua:64, 66, 102`
- **缺失证据**：无。

### C19: `entry-03977` 漏译 narrow 狭窄锥形修饰及 slam 弱化
- **原译短引**：“你 " 轻柔 " 地将链锯放在目标的伤口上 / 对 4 码锥形范围内所有生物造成”
- **具体意义差异**：
  1. 原文 `slam your saws into...` 配双引号 `"gently"` 为黑色幽默（“‘轻柔’地将链锯猛砸入目标的伤口”），原译作“放在”弱化了暴力反讽色彩；
  2. 原文 `in a narrow cone of radius 4`，源码定义 `cone_angle = 25`（常规锥形通常为 45~60 度，25 度属于明显的狭窄锥形），原译漏译 `narrow`。
- **最强等价读法与处理**：建议修正为“你‘轻柔’地将链锯砸入目标的伤口”与“对半径 4 的狭窄锥形范围内所有生物造成”。
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/sawmaiming.lua:83, 98, 100`
- **缺失证据**：无。

### C20: `entry-03984` bore into its skull 动作泛化说明
- **原译短引**：“将进入其大脑 6 回合，干扰思考能力。”
- **具体意义差异**：原文为 `bore into its skull for 6 turns, disrupting its thoughts`。原译泛化为“进入其大脑”，略微减弱了钻开头骨的具象描写。此外，英文原文中 `suffer a -%d%% reduction to fear and sleep immunity` 存在双重否定笔误，中文翻译将其合理理顺为“恐惧和睡眠免疫减少 %d%%”，完全符合实际代码机制（降低目标抗性），无需变动。
- **最强等价读法与处理**：中文字面“进入其大脑”已传达核心机制与大意。可建议优化为“附着其上并钻入其头骨 6 回合，干扰其心智”，属于修辞风格完善。
- **状态**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua:107-109`；`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua:86-87`
- **缺失证据**：无。

### C21: `entry-03985` 标点叹号与术语库 preferred 微差
- **原译短引**：“没有足够的空间召唤！”
- **具体意义差异**：`terms.json` 登记 preferred 为 `[global][T.RUNTIME.LOG][preferred] Not enough space to summon! -> 没有足够的空间召唤。`（句号结尾）。原译保留了英文的感叹号 `！`。依据审核规则第 6 条，静态标点差异不计为缺陷，仅作为统一术语风格的提示。
- **最强等价读法与处理**：若需完全对齐 terms.json preferred 字符串，可将末尾感叹号改为全角句号。
- **状态**：`advisory`
- **来源路径行号**：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json:840`；`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/turrets.lua:325`
- **缺失证据**：无。

---

## 四、实际读取路径与版本限制说明

### 1. 实际读取的文件路径
1. **审核任务输入**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-14.md`
2. **规则与配置清单**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
3. **汉化快照比对文本**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`（5515–5930行上下文）
4. **公开冻结 DLC 源码文件**（均位于 `.artifacts/i18n/all-modified-review-20260922/sources/orcs/`）：
   - `tome-orcs/data/talents/steam/other.lua` (SHA256: `4a12c05410e5f47e466f2ba9f110c9346964a83a2812bad062dc4650c1992970`)
   - `tome-orcs/data/talents/steam/physics.lua` (SHA256: `a764c59d985d26651b6c3684914112650123a30794532f70a59e99e00bce8d0f`)
   - `tome-orcs/data/talents/steam/sawmaiming.lua` (SHA256: `eb7b701da0502dfd685dff66912bd41839dca9fb9b0b7276c4507b186125f169`)
   - `tome-orcs/data/talents/steam/steam.lua` (SHA256: `ff1c3fd79174b935332f62e063968de7d14d9f46a182abe9417600f05e2d6eff`)
   - `tome-orcs/data/talents/steam/thoughts-of-iron.lua` (SHA256: `84a1bba9651083af029928e78000a3d053ac5fa758824e6518b146897d899468`)
   - `tome-orcs/data/talents/steam/turrets.lua` (SHA256: `14dbc643e66d9916ea2bdf257053c3e0870addf2ebfb3bc58bb593258dcd5e1c`)
   - 关联效果机制验证文件：`tome-orcs/data/timed_effects/mental.lua`

### 2. 约束与操作边界执行声明
- 本次审核为纯只读审核旁路，**未修改或写入任何仓库文件**，**未创建任何子代理**。
- 未读取未授权的历史审核报告、评分结果或任务状态文件（STATE / PLAN / SCOPE 等）。
- 严格遵循 DLC 源码来源未固定声明，所有机制事实均标注对应哈希固定文件与行号。报告全量交付完毕。
