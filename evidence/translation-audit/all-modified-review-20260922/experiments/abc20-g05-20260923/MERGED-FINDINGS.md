# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的53项观察及独立盲审的21项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03333 | 未提出此缺陷 | C01（原问题） | 未提出此缺陷 | **翻译新增遗漏**：`upload your addon` 只剩“上传”，没有明确上传的是用户的插件；前句的显式对象反而是 MD5。依据冻结原译文及 `context.lua:43–47`；addon-dev 源码不可用，仅确认文本偏差。 |
| D02 | entry-03345 | 未提出此缺陷 | 未提出此缺陷 | C04（原问题） | **翻译新增遗漏**：`rages and torments` 的折磨行为未保留，“咆哮”仅表达愤怒表现。`S/data/birth/doomelf.lua:29`。 |
| D03 | entry-03345 | 未提出此缺陷 | 未提出此缺陷 | C04（原问题） | **翻译新增时长**：原文没有永久持续限定，译文增加“永远咆哮”。与 D02 的行为遗漏分开。`S/data/birth/doomelf.lua:29`。 |
| D04 | entry-03345 | C02（原问题） | C03（原问题） | C04（原问题） | **翻译新增关系变化**：`the cultists she taught` 变为“召集邪徒”，教导关系丢失。`S/data/birth/doomelf.lua:30`。 |
| D05 | entry-03345 | C02（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增遗漏**：原文明示 `she`，译文没有保留该人物为女性的辨认线索。`S/data/birth/doomelf.lua:30`。 |
| D06 | entry-03345 | C01（原问题） | C05（原问题） | 未提出此缺陷 | **翻译新增目的变化**：`maintain your deception` 是维持欺瞒，译为“隐藏你的踪影”改为掩藏行踪。前文告密语境见 `S/data/birth/doomelf.lua:27–31`。 |
| D07 | entry-03345 | 未提出此缺陷 | C06（原问题） | 未提出此缺陷 | **翻译新增语义变化**：`then you may witness` 的后续见证机会改为“终将诞生”的必然预告，见证者关系也消失。`S/data/birth/doomelf.lua:31–32`。不把 `conception` 强行判作生理受孕阶段。 |
| D08 | entry-03353 | C03（原问题） | C07（原问题） | C07（原问题） | **翻译新增遗漏**：`over time` 的时间过程未表达。`S/data/general/objects/world-artifacts.lua:315`；`:322–427` 的 `act` 根据当前效果反复小额转移免疫值，支持该时间信息有实际意义。 |
| D09 | entry-03358 | C04（原问题） | C08（原问题） | C08（原问题） | **翻译新增范围遗漏**：原文明示所有伤害类型，译文未说明穿透范围。`S/data/general/objects/world-artifacts.lua:679–681` 写入 `resists_pen.all`；同物品 `:673–675` 另有暗影单系穿透，不能把范围视为无意义赘词。 |
| D10 | entry-03361 | C05（原问题） | C09（原问题） | C09（原问题） | **翻译新增句意变化**：周围／包围自身的残骸与内部是否尚存的对照，变成“自身若残损，何物能存”的条件判断。`S/data/general/objects/world-artifacts.lua:737–743`，黑之铠描述。 |
| D11 | entry-03365 | C09（原问题） | 未提出此缺陷 | C10（原问题） | **翻译新增实体身份遗漏**：具体种类 `wretchling` 变为泛称“猥琐小怪”。直接证据 `S/data/lore/demon.lua:60`；种类及酸液特征见 `:116–118、291–295`；允许语境 `context.lua:203、574–575`。不是单纯强制统一旧译名。 |
| D12 | entry-03366 | C11（原问题） | C12（原问题） | 未提出此缺陷 | **翻译新增范围限制**：`standard-issue alteration` 被限定为“思维修改”。`S/data/lore/demon.lua:135` 将改造与忠诚强化、意识连接分别列举；`:191` 的标准改造还涉及传送及内脏。 |
| D13 | entry-03366 | C12（原问题） | 未提出此缺陷 | C11（原问题） | **翻译新增操作变化**：`step on the plate here` 变为“站在那里别动”，踏上板面的动作及对象丢失。`S/data/lore/demon.lua:135`。 |
| D14 | entry-03366 | C12（原问题） | C13（原问题） | C11（原问题） | **翻译新增对象遗漏**：`get the bindings in place` 变为“把它放好”，束缚装置及安装束缚物的信息丢失。`S/data/lore/demon.lua:135`。 |
| D15 | entry-03366 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **独立补查；翻译新增时间遗漏**：`for the first time since you arrived here` 未译，丢失自抵达以来首次摆脱监视的时间关系。`S/data/lore/demon.lua:137`。 |
| D16 | entry-03371 | C14（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增目标及空间关系遗漏**：`isolating` 与体育场建在目标 `around` 的隔离安排，变为泛称“措施”和“为……建造”。`S/data/lore/demon.lua:226`；普通版本的遏制目标语境见 `:210`。 |
| D17 | entry-03371 | C15（原问题） | C14（原问题） | 未提出此缺陷 | **翻译新增命令变化**：`Blow all connectors` 变为“关闭所有链接传送门”，爆破连接设施改成关闭传送门。紧接的平台分离语境见 `S/data/lore/demon.lua:226`，普通版同句见 `:210`。 |
| D18 | entry-03371 | C16（原问题） | C15（原问题） | 未提出此缺陷 | **翻译新增动作及确定程度变化**：`like the pen was rapidly jerked away` 的猛然扯开推测，变为确定的“笔从手上滑落”。`S/data/lore/demon.lua:228`。 |
| D19 | entry-03371 | C17（原问题） | C16（原问题） | C12（原问题） | **翻译新增特征遗漏**：`double-bladed katana` 只剩“武士刀”，双刃特征消失。`S/data/lore/demon.lua:228`。 |
| D20 | entry-03371 | C17（原问题） | C17（原问题） | C12（原问题） | **翻译新增实体描述遗漏**：`giant construct` 的巨大构装体描述未保留。`S/data/lore/demon.lua:228`。 |
| D21 | entry-03371 | 未提出此缺陷 | C17（原问题） | 未提出此缺陷 | **翻译新增身份**：`Ninja Atamathon` 增加“王”。该句没有王者身份信息。`S/data/lore/demon.lua:228`。 |
| D22 | entry-03371 | C17（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增标注关系遗漏**：涂鸦中的对手 `labelled` 某名称，被改为直接以该名称指称对手，没有保留画面上的文字标注关系。`S/data/lore/demon.lua:228`。 |
| D23 | entry-03371 | C16（原问题） | C18（原问题） | C12（原问题） | **翻译新增事件替换**：打断恶魔书写变为把恶魔“吓尿”，原事件遗漏并新增另一事件。`S/data/lore/demon.lua:228`；普通版同一书写中断结构见 `:212`。 |
| D24 | entry-03371 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **翻译新增对象变化**：体育场舞台布置中的 `spotlights` 译成“闪光灯”，聚光照明变为闪光照明。`S/data/lore/demon.lua:226`，与焰火、音响并列。 |
| D25 | entry-03371 | C18（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增性别限定**：无性别限定的 `target's` 变成固定“他的”。同段使用玩家动态代词，见 `S/data/lore/demon.lua:220–226`；本体固定提交 `game/engines/default/engine/Actor.lua:604–610` 提供代词方法。 |
| D26 | entry-03371 | C19（原建议） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增确定性**：`what appear to be motorcycle tire-tracks` 的外观推测变为确定的摩托车胎痕。`S/data/lore/demon.lua:222`。风味文本仍有可辨认的认知状态信息。 |
| D27 | entry-03372 | 未提出此缺陷 | C20（原问题） | C13（原问题） | **翻译新增主体及所属关系变化**：`our casters` 变为“法术”，己方施法者这一参战主体及其所属关系丢失。`S/data/lore/demon.lua:295`。 |
| D28 | entry-03372 | C20（原建议） | C19（原问题） | 未提出此缺陷 | **翻译新增空间关系遗漏**：`the ground they walk on` 只剩“土地”，敌人脚下地面的关系未保留。`S/data/lore/demon.lua:295` 的扑击敌人与使其无助的连续描述。 |
| D29 | entry-03372 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **翻译新增程度强化**：每位参战者“作出巨大贡献”变为每位都已“奉献了一切”。同段区分愿意牺牲与少数存活，不能据此断言每位均已付出全部。`S/data/lore/demon.lua:295`。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O002 | 独立盲审 C01（原建议） | entry-03335 | advisory | `context.lua:95–106` 明确复制目的地；只是“拷贝去”的自然度问题。 |
| O003 | Gemini C01（原建议） | entry-03335 | advisory | 同上；没有操作、对象或目的地变化。 |
| O004 | Sol C02（原建议） | entry-03335 | advisory | 同上；不把搭配偏好计为缺陷。 |
| O005 | Gemini C02（原建议） | entry-03336 | mixed | “种”更贴近英文可作措辞建议；“成就统计23种”被计数实现否定，目标机制归 P01 pending。见成就 `:37–39`、雕像 `:87–92`。 |
| O006 | 独立盲审 C02（原待确认） | entry-03336 | pending | 调用链支持累计次数而非种类去重；目标 DLC 适用性未固定，归 P01。 |
| O007 | Gemini C03（原建议） | entry-03341 | advisory | `corrupted.lua:57、61` 数值及属性对应正确；术语为 existing，不能据此强制改名。 |
| O008 | Opus C07（原建议） | entry-03341 | advisory | 与 O007 相同；属性列表内没有证实实体或数值混淆。 |
| O011 | Sol C03（原问题） | entry-03345 | mixed | 教导关系遗漏 confirmed；“复活目的无依据” refuted，完整恋人复归语境见 `lore/demon.lua:454–460`。 |
| O013 | Sol C04（原问题） | entry-03345 | refuted | `doomelf.lua:28–31` 本身使用让告密者噤声的隐喻；“静默他们的声音”仍可表达该意，不自动排除杀死他们。 |
| O015 | Gemini C04（原问题） | entry-03345 | mixed | 教导、折磨遗漏及“永远”增译 confirmed；“无尽深海”的修辞扩展仅 advisory，不单列事实缺陷。 |
| O018 | Sol C06（原问题） | entry-03345 | mixed | 见证机会变为必然预告 confirmed；把 conception／诞生机械拆成生理阶段错误 refuted，`:26–34` 是种族解锁和改造语境。 |
| O020 | Gemini C05（原建议） | entry-03347 | advisory | `doomelf.lua:39、43` 数值正确；Magic 术语状态不足以强制改名。 |
| O021 | Opus C08（原建议） | entry-03347 | advisory | 与 O020 相同。 |
| O022 | Gemini C06（原建议） | entry-03352 | advisory | 装备 `:118、135–142` 与本体 `FIRE_DRAIN` 的 `healfactor=0.1` 支持数值及治疗对象；仅措辞生硬。 |
| O030 | 独立盲审 C08（原待确认） | entry-03360 | pending | `ceil(power/2)` 经装备更新回调及本体暴击消费核实；目标适用性归 P02。 |
| O034 | Gemini C09（原问题） | entry-03361 | mixed | 句意变化 confirmed；具体认定“废土场景”及译者如何误解介词，证据不足，不采纳这些扩展归因。 |
| O035 | Sol C10（原问题） | entry-03363 | refuted | `context.lua:295–298` 为个人装备属性说明；“全体伤害”没有明确声称全队受益，不能只凭潜在歧义认定对象改变。 |
| O036 | Opus C06（原建议） | entry-03364 | advisory | `All Resists` 条目限定核心面板标签；本句是 DLC 描述，统一措辞仅建议。 |
| O037 | Sol C11（原问题） | entry-03364 | mixed | 队伍受益错误及强制术语适用主张 refuted；“全部抗性”更清晰仅 advisory。见 `context.lua:299–302` 与 INPUT 术语范围。 |
| O039 | Opus C10（原建议） | entry-03365 | advisory | `lore/demon.lua:48、52` 已在相邻影像解释星球含义；显化解释影响含蓄程度，未形成独立事实矛盾。 |
| O041 | Gemini C10（原问题） | entry-03365 | mixed | 具体种类变泛称 confirmed；“全文均如此”未核验，“严肃性”仅风格评价，不用作证据。实际源码位置是 `:60`。 |
| O043 | Gemini C11（原问题） | entry-03366 | mixed | 板面动作及束缚物遗漏 confirmed；“译者误当成水晶”的心理归因无法证明，不采纳。实际源码 `:135`。 |
| O048 | Opus C13（原建议） | entry-03366 | advisory | 被奴役实验对象语境中带引号的“主人”及口语“记住”不足以证实另一项事实改变。 |
| O072 | Opus C20（原建议） | entry-03372 | mixed | 地面关系遗漏 confirmed；开头名词短语的衔接改善仅 advisory，不额外计语法缺陷。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
