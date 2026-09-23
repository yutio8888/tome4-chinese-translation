已完成全部 40 条独立复核及 74 项匿名观察裁决：**9 条 ISSUE、2 条 PENDING、29 条 OK**，归并为 **29 项确认缺陷、2 项未决问题**。

以下 `S/` 指本包 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/`；`A/` 指清单授权的附加 Ashes 快照根目录。DLC 文件均已核对清单哈希，**源码仓库、commit 和目标版本适用性未固定**。确认缺陷中的“翻译新增”表示相对于英文产生，不表示本次修改才引入。

| entry-ID | 判定 | canonical D／P 编号或简短依据 |
|---|---|---|
| entry-03333 | ISSUE | D01：上传对象遗漏 |
| entry-03334 | OK | 重启、语言切换、确认语气及参数保留 |
| entry-03335 | OK | 复制操作及目的地明确；措辞仅建议 |
| entry-03336 | PENDING | P01：种类要求与快照计数实现不一致 |
| entry-03337 | OK | 三名恶魔、时间背景及击杀要求保留 |
| entry-03338 | OK | 专名及颜色标记保留 |
| entry-03339 | OK | 专名一致 |
| entry-03340 | OK | 属性、数值及标记一致 |
| entry-03341 | OK | 属性数值正确；“魔法／魔力”仅建议 |
| entry-03342 | OK | 每级生命加值正确 |
| entry-03343 | OK | 属性数值正确 |
| entry-03344 | OK | 每级生命加值正确 |
| entry-03345 | ISSUE | D02–D07：行为、时长、人物关系及结尾语义变化 |
| entry-03346 | OK | 属性及正负号正确 |
| entry-03347 | OK | 数值正确；“魔法／魔力”仅建议 |
| entry-03348 | OK | 生命成长数值正确 |
| entry-03349 | OK | 经验惩罚数值正确 |
| entry-03350 | OK | 专名一致 |
| entry-03351 | OK | 快照技能沿 `obliterating_smash_wall → DIG` 实现破墙 |
| entry-03352 | OK | 半径、伤害、治疗比例及对象吻合；表达仅建议 |
| entry-03353 | ISSUE | D08：随时间调整的信息遗漏 |
| entry-03354 | OK | 卸下与重置的许可分别保留 |
| entry-03355 | OK | 两项许可均保留 |
| entry-03356 | OK | 三类豁免均按阴影强度增加 |
| entry-03357 | OK | 法术强度对应关系正确 |
| entry-03358 | ISSUE | D09：全伤害类型范围遗漏 |
| entry-03359 | OK | `power/40` 与每点 2.5% 一致 |
| entry-03360 | PENDING | P02：英文与译文共同未说明向上取整 |
| entry-03361 | ISSUE | D10：周围残骸与内部余存改为自身残损的假设 |
| entry-03362 | OK | 物理强度对应关系正确 |
| entry-03363 | OK | 装备语境中的“全体伤害”不构成队伍受益断言 |
| entry-03364 | OK | “全体抗性”仅措辞建议；未证实受益范围错误 |
| entry-03365 | ISSUE | D11：具体恶魔种类变为泛称；长文及格式已全量复核 |
| entry-03366 | ISSUE | D12–D15：改造范围、操作、束缚物及时间信息变化 |
| entry-03367 | OK | 标题及职业指代正确 |
| entry-03368 | OK | 标题及职业指代正确 |
| entry-03369 | OK | 标题及种族指代正确 |
| entry-03370 | OK | 情报标题正确 |
| entry-03371 | ISSUE | D16–D26：隔离命令、叙事动作、实体描写与指代等偏差 |
| entry-03372 | ISSUE | D27–D29：施法者、地面关系及贡献程度变化 |

| D-ID | entry-ID | 内容、归因及证据 |
|---|---|---|
| D01 | entry-03333 | **翻译新增遗漏**：`upload your addon` 只剩“上传”，没有明确上传的是用户的插件；前句的显式对象反而是 MD5。依据冻结原译文及 `context.lua:43–47`；addon-dev 源码不可用，仅确认文本偏差。 |
| D02 | entry-03345 | **翻译新增遗漏**：`rages and torments` 的折磨行为未保留，“咆哮”仅表达愤怒表现。`S/data/birth/doomelf.lua:29`。 |
| D03 | entry-03345 | **翻译新增时长**：原文没有永久持续限定，译文增加“永远咆哮”。与 D02 的行为遗漏分开。`S/data/birth/doomelf.lua:29`。 |
| D04 | entry-03345 | **翻译新增关系变化**：`the cultists she taught` 变为“召集邪徒”，教导关系丢失。`S/data/birth/doomelf.lua:30`。 |
| D05 | entry-03345 | **翻译新增遗漏**：原文明示 `she`，译文没有保留该人物为女性的辨认线索。`S/data/birth/doomelf.lua:30`。 |
| D06 | entry-03345 | **翻译新增目的变化**：`maintain your deception` 是维持欺瞒，译为“隐藏你的踪影”改为掩藏行踪。前文告密语境见 `S/data/birth/doomelf.lua:27–31`。 |
| D07 | entry-03345 | **翻译新增语义变化**：`then you may witness` 的后续见证机会改为“终将诞生”的必然预告，见证者关系也消失。`S/data/birth/doomelf.lua:31–32`。不把 `conception` 强行判作生理受孕阶段。 |
| D08 | entry-03353 | **翻译新增遗漏**：`over time` 的时间过程未表达。`S/data/general/objects/world-artifacts.lua:315`；`:322–427` 的 `act` 根据当前效果反复小额转移免疫值，支持该时间信息有实际意义。 |
| D09 | entry-03358 | **翻译新增范围遗漏**：原文明示所有伤害类型，译文未说明穿透范围。`S/data/general/objects/world-artifacts.lua:679–681` 写入 `resists_pen.all`；同物品 `:673–675` 另有暗影单系穿透，不能把范围视为无意义赘词。 |
| D10 | entry-03361 | **翻译新增句意变化**：周围／包围自身的残骸与内部是否尚存的对照，变成“自身若残损，何物能存”的条件判断。`S/data/general/objects/world-artifacts.lua:737–743`，黑之铠描述。 |
| D11 | entry-03365 | **翻译新增实体身份遗漏**：具体种类 `wretchling` 变为泛称“猥琐小怪”。直接证据 `S/data/lore/demon.lua:60`；种类及酸液特征见 `:116–118、291–295`；允许语境 `context.lua:203、574–575`。不是单纯强制统一旧译名。 |
| D12 | entry-03366 | **翻译新增范围限制**：`standard-issue alteration` 被限定为“思维修改”。`S/data/lore/demon.lua:135` 将改造与忠诚强化、意识连接分别列举；`:191` 的标准改造还涉及传送及内脏。 |
| D13 | entry-03366 | **翻译新增操作变化**：`step on the plate here` 变为“站在那里别动”，踏上板面的动作及对象丢失。`S/data/lore/demon.lua:135`。 |
| D14 | entry-03366 | **翻译新增对象遗漏**：`get the bindings in place` 变为“把它放好”，束缚装置及安装束缚物的信息丢失。`S/data/lore/demon.lua:135`。 |
| D15 | entry-03366 | **独立补查；翻译新增时间遗漏**：`for the first time since you arrived here` 未译，丢失自抵达以来首次摆脱监视的时间关系。`S/data/lore/demon.lua:137`。 |
| D16 | entry-03371 | **翻译新增目标及空间关系遗漏**：`isolating` 与体育场建在目标 `around` 的隔离安排，变为泛称“措施”和“为……建造”。`S/data/lore/demon.lua:226`；普通版本的遏制目标语境见 `:210`。 |
| D17 | entry-03371 | **翻译新增命令变化**：`Blow all connectors` 变为“关闭所有链接传送门”，爆破连接设施改成关闭传送门。紧接的平台分离语境见 `S/data/lore/demon.lua:226`，普通版同句见 `:210`。 |
| D18 | entry-03371 | **翻译新增动作及确定程度变化**：`like the pen was rapidly jerked away` 的猛然扯开推测，变为确定的“笔从手上滑落”。`S/data/lore/demon.lua:228`。 |
| D19 | entry-03371 | **翻译新增特征遗漏**：`double-bladed katana` 只剩“武士刀”，双刃特征消失。`S/data/lore/demon.lua:228`。 |
| D20 | entry-03371 | **翻译新增实体描述遗漏**：`giant construct` 的巨大构装体描述未保留。`S/data/lore/demon.lua:228`。 |
| D21 | entry-03371 | **翻译新增身份**：`Ninja Atamathon` 增加“王”。该句没有王者身份信息。`S/data/lore/demon.lua:228`。 |
| D22 | entry-03371 | **翻译新增标注关系遗漏**：涂鸦中的对手 `labelled` 某名称，被改为直接以该名称指称对手，没有保留画面上的文字标注关系。`S/data/lore/demon.lua:228`。 |
| D23 | entry-03371 | **翻译新增事件替换**：打断恶魔书写变为把恶魔“吓尿”，原事件遗漏并新增另一事件。`S/data/lore/demon.lua:228`；普通版同一书写中断结构见 `:212`。 |
| D24 | entry-03371 | **翻译新增对象变化**：体育场舞台布置中的 `spotlights` 译成“闪光灯”，聚光照明变为闪光照明。`S/data/lore/demon.lua:226`，与焰火、音响并列。 |
| D25 | entry-03371 | **翻译新增性别限定**：无性别限定的 `target's` 变成固定“他的”。同段使用玩家动态代词，见 `S/data/lore/demon.lua:220–226`；本体固定提交 `game/engines/default/engine/Actor.lua:604–610` 提供代词方法。 |
| D26 | entry-03371 | **翻译新增确定性**：`what appear to be motorcycle tire-tracks` 的外观推测变为确定的摩托车胎痕。`S/data/lore/demon.lua:222`。风味文本仍有可辨认的认知状态信息。 |
| D27 | entry-03372 | **翻译新增主体及所属关系变化**：`our casters` 变为“法术”，己方施法者这一参战主体及其所属关系丢失。`S/data/lore/demon.lua:295`。 |
| D28 | entry-03372 | **翻译新增空间关系遗漏**：`the ground they walk on` 只剩“土地”，敌人脚下地面的关系未保留。`S/data/lore/demon.lua:295` 的扑击敌人与使其无助的连续描述。 |
| D29 | entry-03372 | **翻译新增程度强化**：每位参战者“作出巨大贡献”变为每位都已“奉献了一切”。同段区分愿意牺牲与少数存活，不能据此断言每位均已付出全部。`S/data/lore/demon.lua:295`。 |

| O-ID | 状态 | 命中 D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | confirmed | D01 | 冻结原译文及 `context.lua:43–47`；明确上传对象确实省去，不作源码机制推断。 |
| O002 | advisory | — | `context.lua:95–106` 明确复制目的地；只是“拷贝去”的自然度问题。 |
| O003 | advisory | — | 同上；没有操作、对象或目的地变化。 |
| O004 | advisory | — | 同上；不把搭配偏好计为缺陷。 |
| O005 | mixed | — | “种”更贴近英文可作措辞建议；“成就统计23种”被计数实现否定，目标机制归 P01 pending。见成就 `:37–39`、雕像 `:87–92`。 |
| O006 | pending | — | 调用链支持累计次数而非种类去重；目标 DLC 适用性未固定，归 P01。 |
| O007 | advisory | — | `corrupted.lua:57、61` 数值及属性对应正确；术语为 existing，不能据此强制改名。 |
| O008 | advisory | — | 与 O007 相同；属性列表内没有证实实体或数值混淆。 |
| O009 | confirmed | D06 | `doomelf.lua:27–31` 支持告密与维持欺瞒的关系，不是藏行踪。 |
| O010 | confirmed | D04、D05 | `doomelf.lua:30` 明示女性和教导关系；`lore/demon.lua:456–460` 支持恢复恋人的目的。 |
| O011 | mixed | D04 | 教导关系遗漏 confirmed；“复活目的无依据” refuted，完整恋人复归语境见 `lore/demon.lua:454–460`。 |
| O012 | confirmed | D02、D03 | `doomelf.lua:29` 有折磨行为，无“永远”时长。 |
| O013 | refuted | — | `doomelf.lua:28–31` 本身使用让告密者噤声的隐喻；“静默他们的声音”仍可表达该意，不自动排除杀死他们。 |
| O014 | confirmed | D04 | `doomelf.lua:30` 的教导关系未保留；不另将复归恋人目的判错。 |
| O015 | mixed | D02、D03、D04 | 教导、折磨遗漏及“永远”增译 confirmed；“无尽深海”的修辞扩展仅 advisory，不单列事实缺陷。 |
| O016 | confirmed | D06 | 欺瞒变为藏行踪；`doomelf.lua:31`。 |
| O017 | confirmed | D06 | 前后告密语境进一步支持该判断；`:27–32`。 |
| O018 | mixed | D07 | 见证机会变为必然预告 confirmed；把 conception／诞生机械拆成生理阶段错误 refuted，`:26–34` 是种族解锁和改造语境。 |
| O019 | confirmed | D07 | `then you may witness` 未被完整保留；不将诗行先后本身说成完全消失。 |
| O020 | advisory | — | `doomelf.lua:39、43` 数值正确；Magic 术语状态不足以强制改名。 |
| O021 | advisory | — | 与 O020 相同。 |
| O022 | advisory | — | 装备 `:118、135–142` 与本体 `FIRE_DRAIN` 的 `healfactor=0.1` 支持数值及治疗对象；仅措辞生硬。 |
| O023 | confirmed | D08 | 装备 `:315、322–427` 支持反复调整过程；译文未表达时间信息。 |
| O024 | confirmed | D08 | 文本遗漏可以确认；快照机制支持不等于目标 DLC 已固定。 |
| O025 | confirmed | D08 | 正确区分时间遗漏与“状态免疫”用语；实现确实调整免疫字段。 |
| O026 | confirmed | D08 | `act` 内五次循环小额转移支持时间过程；不把“可能误解成立即全额”当译文明示的第二个错误。 |
| O027 | confirmed | D09 | `resists_pen.all` 与同物品单系穿透并存的语境支持范围信息的重要性。 |
| O028 | confirmed | D09 | 文本范围遗漏成立；目标版本适用性声明保留。 |
| O029 | confirmed | D09 | `world-artifacts.lua:673–681` 为直接证据，不仅依靠相邻译法。 |
| O030 | pending | — | `ceil(power/2)` 经装备更新回调及本体暴击消费核实；目标适用性归 P02。 |
| O031 | confirmed | D10 | 黑之铠描述 `:743` 的外部／内部对照变成自身残损条件句。 |
| O032 | confirmed | D10 | 同上；不要求确定 inside 究竟指内心还是铠甲内部。 |
| O033 | confirmed | D10 | 对意象关系变化的限定判断有文本支持。 |
| O034 | mixed | D10 | 句意变化 confirmed；具体认定“废土场景”及译者如何误解介词，证据不足，不采纳这些扩展归因。 |
| O035 | refuted | — | `context.lua:295–298` 为个人装备属性说明；“全体伤害”没有明确声称全队受益，不能只凭潜在歧义认定对象改变。 |
| O036 | advisory | — | `All Resists` 条目限定核心面板标签；本句是 DLC 描述，统一措辞仅建议。 |
| O037 | mixed | — | 队伍受益错误及强制术语适用主张 refuted；“全部抗性”更清晰仅 advisory。见 `context.lua:299–302` 与 INPUT 术语范围。 |
| O038 | confirmed | D11 | `lore/demon.lua:60、291–295` 证实种类身份；实际核对187个方括号段、34次重复和16段结构一致。 |
| O039 | advisory | — | `lore/demon.lua:48、52` 已在相邻影像解释星球含义；显化解释影响含蓄程度，未形成独立事实矛盾。 |
| O040 | confirmed | D11 | 正常叙述中的种类身份丢失；不属于故意误译的方括号隐喻。 |
| O041 | mixed | D11 | 具体种类变泛称 confirmed；“全文均如此”未核验，“严肃性”仅风格评价，不用作证据。实际源码位置是 `:60`。 |
| O042 | confirmed | D12 | `lore/demon.lua:135` 的并列项目不支持把改造限于思维。 |
| O043 | mixed | D13、D14 | 板面动作及束缚物遗漏 confirmed；“译者误当成水晶”的心理归因无法证明，不采纳。实际源码 `:135`。 |
| O044 | confirmed | D12 | `lore/demon.lua:155、191` 支持标准改造包含身体及能力变化。 |
| O045 | confirmed | D12 | 标准改造影响传送与内脏，`:191` 为直接支持。 |
| O046 | confirmed | D13 | `:135` 是回忆中的踏板指示；不扩展为当前任务操作要求。 |
| O047 | confirmed | D13、D14 | 踏上板面和装上束缚具两项信息均未保留；`:135`。 |
| O048 | advisory | — | 被奴役实验对象语境中带引号的“主人”及口语“记住”不足以证实另一项事实改变。 |
| O049 | confirmed | D14 | 束缚物从具名对象变成不明“它”；`:135`。 |
| O050 | confirmed | D14 | 对象遗漏成立；“可能理解成水晶”只是歧义说明，不另计缺陷。 |
| O051 | confirmed | D19、D20、D23 | 双刃、巨型构装体及书写中断三项均可由 `:228` 直接确认。 |
| O052 | confirmed | D17 | `:210、226` 的爆破与平台分离语境不支持“关闭传送门”。 |
| O053 | confirmed | D16 | `isolating` 的行动目标没有保留；`:226`。 |
| O054 | confirmed | D16 | 隔离与环绕建造属于同一围困安排，合并计一次；`:210、226`。 |
| O055 | confirmed | D18 | 猛然扯开与滑落是不同动作；`:228`。 |
| O056 | confirmed | D17 | 文本足以证明命令对象及动作变化，无须假定地图执行脚本。 |
| O057 | confirmed | D17 | 同一爆破连接设施命令；`:210、226`。 |
| O058 | confirmed | D19 | 双刃特征遗漏；`:228`。 |
| O059 | confirmed | D24 | 舞台照明上下文支持聚光灯，不是闪光灯；`:226`。 |
| O060 | confirmed | D18、D23 | 笔的动作与写作中断结论分别变化；`:212、228`。不额外断言玩家实际闯入的具体过程。 |
| O061 | confirmed | D20、D21 | 实体描述遗漏与“王”增译均成立；`:228`。不依赖跨类别强制套术语。 |
| O062 | confirmed | D19 | 双刃不是普通“武士刀”必然具备的信息；`:228`。 |
| O063 | confirmed | D19、D20、D22 | 武器特征、对手描述、画中文字标注关系分别遗漏；`:228`。 |
| O064 | confirmed | D23 | 书写中断被惊吓失禁事件替换；`:228`。 |
| O065 | confirmed | D20、D21 | 巨型构装体遗漏及王者身份增译成立，不依靠读者背景知识补足。 |
| O066 | confirmed | D25 | 原文 target 不限性别，同段提供动态玩家代词；译文固定男性指代。 |
| O067 | confirmed | D26 | 外观推测变确定断言有可证信息变化；不能仅因风味文本降为建议。 |
| O068 | confirmed | D18 | 动作与推测程度均改变；末尾字母本地化为“字”不另计。 |
| O069 | confirmed | D23 | 幽默语体允许改写措辞，不足以豁免叙述事件被替换。 |
| O070 | confirmed | D27 | 己方施法单位变为法术，主体及所属信息丢失；`:295`。 |
| O071 | confirmed | D28 | 特定脚下地面变为泛称土地；`:295`。 |
| O072 | mixed | D28 | 地面关系遗漏 confirmed；开头名词短语的衔接改善仅 advisory，不额外计语法缺陷。 |
| O073 | confirmed | D27 | 与 O070 同义，合并；其附带的读取自述不作为本次核验事实。 |
| O074 | confirmed | D29 | 巨大贡献与已经奉献全部并不等价；`:295` 的愿意牺牲、少数存活语境支持区分。 |

未决问题及主要分歧处理：

- **P01｜entry-03336**：快照中 `S/data/achievements/all.lua:35–41` 只累计 `nb`；`S/data/general/grids/demon_statues.lua:87–92` 只防止同一实例重复激活，调用不传种类。`A/tome-ashes-urhrok/data/general/events/demon-statue.lua:25–35` 的种类移除限于本次生成。固定本体成就链最终在 `engine/interface/WorldAchievements.lua:131–146` 按成就保存计数并调用 `can_gain`，没有补上种类去重。因此不能确认“改成23种才符合机制”。英文的种类要求存在上游疑点；目标 DLC 来源及实现缺失，保持 pending。
- **P02｜entry-03360**：快照 `world-artifacts.lua:725、730–732` 自带5点阴影强度，更新结果为 `ceil(5/2)=3`。`A/.../Actor.lua:61–67` 将真实强度传入并重新应用装备；固定本体 `Combat.lua:1887–1890、2012–2025` 将其作为暴击百分比消费。这是**沿袭上游的取整遗漏**，目标版本适用性待确认。
- **entry-03364 的取整不另立疑点**：已读八件黑石装备提供的阴影强度均为5或10；这些组合下 `ceil(power*0.4)` 与线性描述一致。没有用不可达的任意数值制造缺陷。
- “静默声音”仍可作为噤声／灭口隐喻；“全体伤害／抗性”也不能脱离个人装备语境自动理解成全队效果。这些否决没有借用同条其他缺陷。
- 40条的格式检查未发现占位符、模板表达式及显示标记序列差异；未据此声称已经完成运行时全量测试。

实际读取范围：

- [冻结包入口](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/ADJUDICATION-INPUT.md)，以及同目录 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。
- `S/` 下六个获准单文件：`data/achievements/all.lua`、`data/birth/corrupted.lua`、`data/birth/doomelf.lua`、`data/general/grids/demon_statues.lua`、`data/general/objects/world-artifacts.lua`、`data/lore/demon.lua`。
- 附加快照根目录 `A` 为清单指定的 `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok`。读取并核对哈希的三个单文件：
  - `tome-ashes-urhrok/superload/mod/class/Actor.lua`：由 `artifact_power_obsidian`／`on_obsidian_power_update` 引入。
  - `tome-ashes-urhrok/data/general/events/demon-statue.lua`：由 `demon_statues_list`、生成及激活回调关系引入。
  - `tome-ashes-urhrok/data/talents/corruptions/wrath.lua`：由装备明确列出的技能树、`T_OBLITERATING_SMASH` 和破墙属性引入。
- 本体仅用 `git show` 读取 `/workspace/t-engine4` 的固定提交 `624a67329fe2ad440c5b344785a9c73fcf22ae63`：
  - `game/modules/tome/data/damage_types.lua`：追踪 `FIRE_DRAIN`、`DIG`。
  - `game/modules/tome/class/interface/Combat.lua`：追踪法术暴击消费。
  - `game/modules/tome/class/World.lua` → `game/modules/tome/class/interface/WorldAchievements.lua` → `game/engines/default/engine/interface/WorldAchievements.lua`：沿成就调用和明确继承追踪。
  - `game/engines/default/engine/Actor.lua`：追踪玩家代词方法。

首次默认沙箱读取因挂载隔离错误失败，随后通过获准的只读执行完成。未修改仓库，未创建临时文件或子 agent，未读取模型身份映射、原始报告、STATE 或其他轮答案；无已知越界。本结果仅为独立 REVIEWER 裁决，不作生产完成状态声明。
