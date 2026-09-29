# 匿名源码核验与归并：40 条 / 70 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方70项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好70行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03574

### C01 | entry-03574 | 仅建议
- **原文短引**：`When a target becomes afraid it bolsters you to see their anguish, increasing your darkness and blight damage penetration by %d%% for 2 turns.`
- **译文短引**：`同时，敌人的恐惧和痛苦能激励你的意志，在 2 回合内增加你 %d%% 暗影和枯萎伤害抗性穿透。`
- **问题具体内容**：
  1. 措辞偏好：“激励你的意志”中使用了“意志”（在 ToME4 机制中为核心基础属性 Willpower），容易使玩家误以为本技能提升了角色“意志”属性；英文原文为“it bolsters you to see their anguish”，意为看到敌人的痛苦使你精神受到鼓舞/振奋。
  2. 语境关联：原文“When a target becomes afraid”表达的是目标陷入恐惧时带来增益的连带语境，译文作“同时”系将两者并列，虽契合源码中实际施加效果的实现，但句意上若将“意志”调整为普通鼓舞词汇并理顺衔接，体验更佳。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/disfigured-face.lua:190-202`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`affectTarget` 函数对目标施加 `EFF_GLIMPSE_OF_TRUE_HORROR` 并同时对自身施加 `EFF_GLIMPSE_OF_TRUE_HORROR_SELF`（提升暗影与枯萎抗性穿透），并未修改 `wil`（意志属性）。



## O002 | entry-03574

### C01 | entry-03574 | 待确认

原文：“When a target becomes afraid”；译文：“敌人的恐惧和痛苦……增加你……抗性穿透”。

`S/disfigured-face.lua:190–194` 的 `affectTarget` 在调用目标恐惧效果后，直接给施法者添加穿透效果，没有检查目标是否成功获得恐惧。`D/tome-cults/data/timed_effects.lua:579–580` 则直接把穿透加到暗影、枯萎两类。

因此，快照实现并不要求恐惧成功才给予穿透。中英文都将两者建立了因果联系，属于沿袭上游的疑点；目标版本适用性待确认。



## O003 | entry-03575

### C01 | entry-03575 | 仅建议
- 原文 “Weave your chosen prophecy into your speech, dooming your foe twice over.”；译文 “对你的听众施加双重诅咒。”
- 译文把 foe 换成了“听众”，并省略了“把所选预言织入话语”的描写。
- 核实的机制是所选预言附加给主要目标，见 doom.lua:110-113 和 twofold_curse 函数。下一句“施加给主要目标”已经正确交代了作用对象，所以这里只算措辞偏好。



## O004 | entry-03575

### C02 | entry-03575 | 存在问题
- **原文短引**：`Weave your chosen prophecy into your speech, dooming your foe twice over. The chosen prophecy will apply instantly to your primary target whenever you cast any other prophecy at talent level %d.`
- **译文短引**：`对你的听众施加双重诅咒。每当你施加其他预言时，你选择的预言将同时施加给主要目标 (技能等级 %d)。`
- **问题具体内容**：
  1. 作用对象严重误译：原文“dooming your foe twice over”被翻译为“对你的听众施加双重诅咒”。“foe”意为敌人。本技能“双重诅咒（Twofold Curse）”的作用机制是施法时将所选预言附带施加给当前主要敌方单体（primary target），与同系中面向大范围群体敌人的“隆重演说（Grand Oration: speak to the masses）”截然不同；将“foe”译为“听众”直接曲解了该单体技能的作用对象。
  2. 句子结构与语义完全遗漏：原句前半句“Weave your chosen prophecy into your speech”（将你选择的预言编入你的演说之中）在译文中被彻底漏译。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/doom.lua:371-377` 及 `twofold_curse` 回调逻辑（第 89-94, 156-161, 226-230 行）（DLC 源码快照未固定 commit，source_pinning=unpinned）。当玩家激活双重诅咒时，施放其他预言会直接对当前所命中的敌方目标 `target` 触发所选预言的 `twofold_curse`，属于明确的敌方单体作用机制。



## O005 | entry-03576

### C01 | entry-03576 | 存在问题

原文限定为“one of your talents **on cooldown**”，译文只有“你的一个技能的冷却时间将减少 %d”。这漏掉了只能选取当前处于冷却中的技能，容易被理解为降低任意技能的冷却设定。快照中预言效果遍历施法者的 `talents_cd`，再调用 `alterTalentCoolingdown`；见 [doom.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/doom.lua:415) 与 [timed_effects.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/timed_effects.lua:896)。



## O006 | entry-03576

### C02 | entry-03576 | 存在问题

原文：“cooldown reduced by %d turns”；译文：“冷却时间将减少 %d”。

译文遗漏了数值单位“回合”。这不是占位符错误，但玩家实际看到的减少量缺少原文明示的时间单位。`S/doom.lua:415–422` 中，该参数来自 `getMadness`，并非百分比。

状态：**文本遗漏已确认**。



## O007 | entry-03576

### C02 | entry-03576 | 存在问题
- 原文 “…has its cooldown reduced by %d turns.”；译文 “你的一个技能的冷却时间将减少 %d。”
- 问题：丢了单位“回合”。同一技能树的疯狂预言本身是按百分比增加冷却（doom.lua:130），没有单位时，这个数既可以读成回合，也可以读成百分比。
- 源码：timed_effects.lua:896-913（cults）。callbackOnTalentPost 调用 `eff.src:alterTalentCoolingdown(tid, -eff.cd)`，按回合减少。eff.cd 来自 doom.lua:106 的 Revelation getMadness，即 doom.lua:389 的 math.floor(...)。



## O008 | entry-03576

### C03 | entry-03576 | 存在问题
- **原文短引**：`Prophecy of Madness. Each time the target uses a talent one of your talents on cooldown has its cooldown reduced by %d turns.`
- **译文短引**：`疯狂预言：每次目标使用技能时，你的一个技能的冷却时间将减少 %d。`
- **问题具体内容**：
  单位信息缺失：原文明确包含冷却时间减少的量纲单位“turns”（回合）：`has its cooldown reduced by %d turns`，译文仅翻译为“减少 %d”，末尾遗漏了时间单位“回合”，导致机制描述数值信息不完整。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/doom.lua:411-423`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`getMadness` 计算减少的回合数（1–4 回合）并作为第一个参数填入 `%d turns`。



## O009 | entry-03576

### C03 | entry-03576 | 存在问题
- 原文 “one of your talents on cooldown”；译文 “你的一个技能”。
- 问题：丢了“正在冷却中”这个范围限定。实现只从 `eff.src.talents_cd`（正在冷却的技能）里随机挑一个，且排除 fixed_cooldown，见 timed_effects.lua:901-911。
- 去掉限定后，译文可以读成任意技能，甚至读成技能本身的基础冷却时间被减少。



## O010 | entry-03576

### C03 | entry-03576 | 待确认

原文：“Each time the target takes damage you are healed”；译文：“每次目标受到伤害时，你回复……”。

`D/tome-cults/data/timed_effects.lua:941–945` 的 `PROPHECY_OF_RUIN.callbackOnTakeDamage` 要求 `eff.src == src`，随后给该伤害来源调用 `heal`。快照中，其他单位造成的伤害不满足这一治疗条件。

中英文均未表达伤害来源限制，属于上游已有的机制描述疑点。目标版本适用性待确认。



## O011 | entry-03578

### C04 | entry-03578 | 仅建议
- **原文短引**：`a radius 1 rift in spacetime will be opened underneath the target for %d turns, increasing in radius by 1 each turn to a maximum of %d.`
- **译文短引**：`会在目标处产生一个持续 %d 回合的一格小型黑洞，每回合半径增加 1 直到 %d。`
- **问题具体内容**：
  范围表述偏好：原文为“a radius 1 rift in spacetime”（半径为 1 的时空裂隙），译文作“一格小型黑洞”。在 ToME4 坐标系中，半径 1 实际上是以目标为中心的 3x3 范围；“一格”容易让初见玩家误解为仅占 1 个地块。虽然下文接有“每回合半径增加 1”，但若调整为“半径 1 的小型黑洞/时空裂隙”会更加准确严谨。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/entropy.lua:119-131, 216-234`（DLC 源码快照未固定 commit，source_pinning=unpinned）。黑洞初始 `radius = 1`，通过 `core.fov.circle_grids` 获取范围并逐回合向外扩张。



## O012 | entry-03578

### C04 | entry-03578 | 待确认

原文：“All caught within the rift”；译文：“所有范围内的生物”。

`S/entropy.lua:123–140` 的黑洞 `act` 明确设置 `friendlyfire=false`，并排除召唤者对其关系值非负的目标，再对剩余目标拉拽、造成伤害。

快照行为没有覆盖所有生物。译文沿袭英文的范围泛化；尚缺该快照与目标 DLC 版本的对应证据。



## O013 | entry-03579

### C04 | entry-03579 | 仅建议
- 译文 “增加 %d%% 黑暗和时空伤害”。本批其他条目和术语快照（darkness，damage type，existing）都用“暗影”。
- 机制是 inc_damage/resists_pen 的 DARKNESS/TEMPORAL，见 entropy.lua:264-265，语义没有错。该术语是 existing，不是强制译名，所以只记为一致性建议。



## O014 | entry-03579

### C05 | entry-03579 | 仅建议
- **原文短引**：`increasing your darkness and temporal damage by %d%% and resistance penetration by %d%% at the cost of suffering %0.2f entropic backlash for each non-instant spell.`
- **译文短引**：`增加 %d%% 黑暗和时空伤害与 %d%% 抗性穿透。作为代价，每个非瞬间法术会带来 %0.2f 熵能反冲。`
- **问题具体内容**：
  1. 术语一致性：“darkness”伤害类型在游戏核心机制及同文件其他条目（如 entry-03573、entry-03578 等）中普遍规范为“暗影伤害”，此处作“黑暗伤害”略显脱节；鉴于术语快照中该词条标记为 `existing` 而非强制的 `preferred`，按规则不计为阻断缺陷。
  2. 措辞偏好：“non-instant”在技能描述中建议统一优化为更符合游戏行文习惯的“非瞬发法术”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/entropy.lua:246-283`（DLC 源码快照未固定 commit，source_pinning=unpinned）。机制为增加 `DamageType.DARKNESS` 与 `DamageType.TEMPORAL` 的增伤与穿透，触发检查为 `if ab.is_spell and not ab.no_energy ...`（非瞬发法术）。



## O015 | entry-03579

### C05 | entry-03579 | 待确认

原文：“for each non-instant spell”；译文：“每个非瞬间法术会带来……熵能反冲”。

`S/entropy.lua:249–252` 的 `callbackOnTalentPost` 同时要求法术、非瞬发、主动模式及 `self.in_combat`。中英文描述均未保留战斗状态限制。

快照中存在“战斗外施放不触发”的具体差异，属于沿袭上游的疑点；目标版本待确认。



## O016 | entry-03581

### C02 | entry-03581 | 存在问题

原文末句说更改恐魔的“equipment **and talents**”前，要先转交装备，再取得控制权。译文末句仅说“试图改变其装备时”，漏掉更改技能也属于这段操作说明的范围。其可完全控制的设置见 [friend-of-the-worm.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:237)，原说明见同文件第 425–438 行。



## O017 | entry-03581

### C05 | entry-03581 | 存在问题
- 原文 “Using this spell will ressurect your friendly horror if it died…”；译文 “使用该法术将复活已死亡的单位…”。
- 问题：作用对象从“你的友方恐魔（蠕虫合体）”泛化成了任意“已死亡的单位”。
- 源码：friend-of-the-worm.lua:357-374 只处理 `self.demented_wtw`。on_pre_use（:347）在蠕虫还活着时直接拒绝施放。



## O018 | entry-03581

### C06 | entry-03581 | 仅建议
- 原文 “To change your horror's equipment and talents…”；译文 “试图改变其装备时…”，漏了 talents。
- 第二行“你可以完全控制、升级、更换它的装备和技能”已经交代了技能，所以不算信息丢失。



## O019 | entry-03581

### C06 | entry-03581 | 存在问题

原文：“To change your horror's equipment **and talents** … take control of it”；译文：“试图改变其**装备**时……再切换控制”。

操作说明遗漏了调整技能同样需要切换控制。前文虽然说可以更换技能，却没有保留这项操作要求。`S/friend-of-the-worm.lua:437` 的完整说明同时列举装备与技能；该文件 `:239–241` 还明确建立可完全控制的伙伴成员。

状态：**玩家操作信息遗漏已确认**。



## O020 | entry-03581

### C06 | entry-03581 | 存在问题
- **原文短引**：`To change your horror's equipment and talents first transfer the equipment from your inventory then take control of it.`
- **译文短引**：`试图改变其装备时，先将装备交给它，再切换控制。`
- **问题具体内容**：
  关键操作指引遗漏：原文为“To change your horror's equipment and talents”（试图更改其装备与技能时），明确指导玩家若需为蠕虫合体调整装备及技能点，操作步骤都是先转移装备再控制该仆从。译文仅作“试图改变其装备时”，完全漏译了“and talents”（以及技能），导致缺失了如何为其加点或学习技能的操作说明。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:426-439`（DLC 源码快照未固定 commit，source_pinning=unpinned）。蠕虫合体作为全控型随从，玩家需要通过接管控制来进入其升级加点界面。



## O021 | entry-03582

### C03 | entry-03582 | 存在问题

原文“**both** teleport … and **make a melee attack**”指玩家与蠕虫合体各自攻击。译文“你和蠕虫合体同时传送……造成 %d%% 近战伤害”未交代是各作一次攻击，可能被读成合计一次伤害。快照中玩家与伙伴分别调用 `attackTarget`，见 [friend-of-the-worm.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:492) 的第 492–507 行。



## O022 | entry-03582

### C07 | entry-03582 | 仅建议
- **原文短引**：`teleport to an enemy in range %d and make a melee attack for %d%% damage.`
- **译文短引**：`同时传送至 %d 内的目标处，造成 %d%% 近战伤害。`
- **问题具体内容**：
  量词修饰偏好：原文“in range %d”在译文中仅翻译为“%d 内”，缺少了距离单位或量词，略显生硬，建议优化为“范围 %d 内”或“%d 格内的目标处”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:513-516`（DLC 源码快照未固定 commit，source_pinning=unpinned）。此处第一个参数固定传入距离数值 10。



## O023 | entry-03582

### C07 | entry-03582 | 仅建议
- 译文 “传送至 %d 内的目标处”，没有“范围/格”。数值 10 见 friend-of-the-worm.lua:515，意思能看懂，属于措辞完整度问题。



## O024 | entry-03582

### C07 | entry-03582 | 待确认

原文、译文均称 Blindside 冷却减少 `%d`。

`S/friend-of-the-worm.lua:515` 显示的是 `getBlindside`；但 `update_wtw` 在 `:271–272` 写入的是 `1 + getBlindside`。固定本体 `E/game/modules/tome/class/Actor.lua:6885` 将该字段直接从冷却中扣除。

快照中实际写入的减免比显示值多 1，属于上游参数说明疑点，并非中文新增。DLC 目标版本适用性待确认。



## O025 | entry-03583

### C08 | entry-03583 | 仅建议
- **原文短引**：`your Worm that Walks permanently gains an inscription slot every 2 raw talent levels (%d).`
- **译文短引**：`该技能每增加两级原始等级，你的蠕虫合体获得一个纹身位（当前：%d）。`
- **问题具体内容**：
  副词修饰偏好：原文中“permanently gains”带有“permanently”（永久），译文虽已准确表达了技能每 2 级获得 1 个纹身位的机制，但未显式译出“永久”，建议补充“永久获得”以进一步明确该效果非临时增益。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:526, 545-549`（DLC 源码快照未固定 commit，source_pinning=unpinned）。技能定义设置了 `no_unlearn_last = true`，确保纹身槽位一旦解锁即永久固定。



## O026 | entry-03583

### C08 | entry-03583 | 待确认

原文：“an inscription slot”；译文：“一个纹身位”。

`S/friend-of-the-worm.lua:267–268、528` 增加的是通用 `max_inscriptions` 数量，而非文件内定义的某个“纹身专用槽”。但冻结术语子集没有说明“纹身”是否被项目用作 inscription 的统称，已查阅材料也不足以完整确认此伙伴槽位可接受的铭文类别。

因此，存在把总类缩为子类的具体疑点，但目前不能仅凭个人术语习惯判错。缺少槽位消费规则及本语境术语对应证据。



## O027 | entry-03584

### C09 | entry-03584 | 待确认

原文：“within range 3”；译文：“处于蠕虫合体 3 格范围内”。

`S/friend-of-the-worm.lua:565` 的 `on_pre_use` 在距离 `>= 3` 时拒绝使用，因此快照中恰好距离 3 也不能施放。相邻技能的距离条件则在 `:537` 明确使用 `<= 3`。

中英文对边界的表述均与这里的拒绝条件存在疑点，属于沿袭上游；目标版本适用性待确认。



## O028 | entry-03584

### C10 | entry-03584 | 待确认

原文：“for 3 turns”；译文：“在 3 回合里失去……”。

`D/tome-cults/data/timed_effects.lua:262–267` 的共享疯狂效果，对周围敌人施加 `WTW_TERRIBLE_SIGHT` 时传入持续时间 **2**；`:283–285` 才执行法术豁免、闪避削减。

快照施加值与中英文所写的 3 回合不一致。属于上游已有疑点，目标版本适用性待确认。



## O029 | entry-03588

### C04 | entry-03588 | 存在问题

原文限制目标“at once”不能被**多次裂隙爆炸**击中；译文“一次湮灭不能多次伤害同一目标”把跨爆炸的限制说成单次爆炸内部的重复伤害。快照的爆炸投射使用 `RIFT_EXPLOSION`，其投射器以目标的 `turn_procs.rift_explosion` 阻止同一回合再次受此类爆炸伤害；见 [nether.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/nether.lua:128) 和 [damage_types.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/damage_types.lua:39)。



## O030 | entry-03588

### C09 | entry-03588 | 仅建议
- **原文短引**：`After 3 turns the rift detonates, dealing %0.2f temporal damage to adjacent enemies. Targets cannot be struck by more than a single rift explosion at once.`
- **译文短引**：`3 回合后裂缝湮灭并对周围敌人造成 %0.2f 时空伤害。一次湮灭不能多次伤害同一目标。`
- **问题具体内容**：
  动词选词偏好：原文机制为裂隙引爆，英文使用“detonates”和“rift explosion”。译文采用了玄奥风格的“湮灭”，但在物理及游戏语义中，引爆（爆炸）更符合对其周围造成范围伤害的动态描述，且与后文“single rift explosion”对应更贴切。属于译者文风偏好，列为建议。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:138-159`（DLC 源码快照未固定 commit，source_pinning=unpinned）。机制是在第 3 回合对周围 1 格范围播放 `fireflash` 爆炸音效并结算伤害。



## O031 | entry-03588

### C11 | entry-03588 | 待确认

原文：“cannot be struck by more than a single rift explosion at once”；译文：“一次湮灭不能多次伤害同一目标”。

译文把限制落在“一次湮灭”内部，未明确同时发生的多次裂隙爆炸之间是否共享限制。`D/tome-cults/data/damage_types.lua:40–47` 使用目标上的 `turn_procs.rift_explosion`，先检查、再设置该标记；它不是某次爆炸私有的命中集合。

快照支持按目标共享的回合内限制。译文是否造成范围误解及目标版本对应关系，保留待确认。



## O032 | entry-03588

### C12 | entry-03588 | 待确认

原文、译文均直接陈述施法产生熵能反冲。

`S/nether.lua:147–149` 仅在 `self.in_combat` 时添加反冲效果。中英文均未说明这一条件。

这是沿袭上游的战斗状态限制疑点；目标版本适用性待确认。



## O033 | entry-03593

### C08 | entry-03593 | 仅建议
- 译文 “%0.2f 暗影 %0.2f 时空伤害”，两个数值之间缺“和”或顿号。参数顺序正确（nether.lua:292），可读性偏好。



## O034 | entry-03593

### C10 | entry-03593 | 仅建议
- **原文短引**：`Enemies will take %0.2f darkness and %0.2f temporal damage.`
- **译文短引**：`敌人将受到 %0.2f 暗影 %0.2f 时空伤害。`
- **问题具体内容**：
  标点/连词偏好：译文“%0.2f 暗影 %0.2f 时空伤害”中，两种伤害数值之间直接为空格分隔，缺少中文连词或顿号，格式上建议补充为“%0.2f 暗影和 %0.2f 时空伤害”或“%0.2f 暗影、%0.2f 时空伤害”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:286-293`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`damDesc` 分别生成暗影和时空伤害描述并依次填充。



## O035 | entry-03593

### C13 | entry-03593 | 待确认

原文、译文均直接陈述该法术产生熵能反冲。

`S/nether.lua:277–279` 同样以 `self.in_combat` 为添加反冲效果的前提。它与上一条是不同技能中的独立出现，故单独覆盖。

属于上游已有的条件遗漏疑点；目标版本适用性待确认。



## O036 | entry-03594

### C05 | entry-03594 | 存在问题

原文的“your next **Nether** spell”被译为“下一次**虚空**法术”，改变了可触发强化的技能类别。快照将相关技能归在 `demented/nether`，另有独立的 `demented/void` 类别；本包术语子集也将 `nether` 技能类别记为“彼世”。见 [nether.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/nether.lua:22)、[void.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/void.lua:20)。



## O037 | entry-03594

### C09 | entry-03594 | 存在问题
- 原文 “your next Nether spell will consume all sparks”；译文 “你的下一次虚空法术将消耗所有火花”。
- 问题：Nether 指 demented/nether 技能树。源码里真正会消耗火花的是 Netherblast、Rift Cutter、Spatial Distortion 三个技能，都检查 `EFF_HALO_OF_RUIN charges==5`，见 nether.lua:50-58、103-110、196-201。
- 术语快照里 nether 对应“彼世”，void 对应另一棵技能树 demented/void“虚空”。同一条里的“彼世火花”“彼世冲击”都用了彼世。译成“虚空法术”会把适用范围错指到 Void 技能树。



## O038 | entry-03594

### C10 | entry-03594 | 仅建议
- 原文 “your Magic stat”；译文 “魔法属性”，术语快照里 Magic 是“魔力”（existing）。机制是 stats=self:getMag()，见 nether.lua:242，语义正确，属一致性建议。



## O039 | entry-03594

### C11 | entry-03594 | 存在问题
- **原文短引**：`on reaching 5 sparks your next Nether spell will consume all sparks to empower itself:`
- **译文短引**：`当你拥有 5 个火花时，你的下一次虚空法术将消耗所有火花来获得强化效果。`
- **问题具体内容**：
  1. 技能系别严重误译（实质机制错误）：原文“your next Nether spell”被误译为“你的下一次虚空法术”。在 Cults of Entropy DLC 中，“Nether”是独立的“彼世系”（demented/nether），而“虚空系”（demented/void）是另一个完全不同的技能系。源码实现中严格匹配 `if ab.type[1]:find("^demented/nether")`，只有施放“彼世系”法术（如彼世冲击、裂缝切割、空间扭曲）才会消耗 5 层火花并触发强化；施放虚空法术根本无法消耗火花。此误译直接颠倒了技能交互对象，给玩家造成严重误导。
  2. 属性术语偏差（附带观察）：文末“your Magic stat”被译为“魔法属性”，在游戏机制术语中应规范为“魔力”（Magic 属性）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:308-324`（DLC 源码快照未固定 commit，source_pinning=unpinned）。强化触发只响应 `demented/nether` 系法术；术语快照中 `nether` 对应 `彼世`，`void` 对应 `虚空`。



## O040 | entry-03594

### C14 | entry-03594 | 存在问题

原文：“your next **Nether** spell”；译文：“你的下一次**虚空**法术”。

冻结语境中，Nether 对应本条列出的彼世冲击、裂缝切割、空间扭曲；另有独立的 `demented/void` 技能系。译文把强化消费条件指向了另一类别。

`S/nether.lua:35–58、103–109、196–200` 分别在所列三个彼世技能中检查并消耗五层火花；`S/void.lua:21–22` 则明确属于另一技能系。

状态：**类别指代错误已确认**。这不依赖将 existing 术语升级为强制译名，而是两个不同类别被混淆。



## O041 | entry-03594

### C15 | entry-03594 | 待确认

原文：“Each time you cast…”；译文：“每次你施放……一朵彼世火花……”。

`S/nether.lua:308–314` 的回调还检查 `self.in_combat` 和 `self.turn_procs.halo_of_ruin`。因此，快照中既有战斗状态条件，也有同回合重复触发限制，并非每次合格施法都新增火花。

中英文均未表达这些触发限制，属于上游已有的频率／条件疑点；目标版本待确认。



## O042 | entry-03595

### C16 | entry-03595 | 存在问题

原文：“entropic backlash **applied or increased**”；译文：“每当你**受到熵能反冲**时”。

原文明示的是反冲效果被施加或增加的事件，译文丢失了这两个事件限定，容易与持续反冲伤害的每次结算混同。

`D/tome-cults/data/timed_effects.lua:803–806、815–818` 分别在 `activate`、`on_merge` 中调用 `do_nihil`；`:827–840` 的逐回合伤害结算没有该调用。

状态：**触发事件信息损失已确认**；源码支持该区分，但快照对目标版本的适用性仍未固定。



## O043 | entry-03598

### C17 | entry-03598 | 仅建议

原文：“You do not have line of sight”；译文：“你没有视线”。

`S/rift.lua:220–222` 的语境是所选位置不可见或被地形阻挡。“你没有视线”表达生硬，但在目标选择失败提示中仍可理解，未发现足以确认的功能信息损失。

状态：**仅措辞自然度建议，不计缺陷**。



## O044 | entry-03600

### C06 | entry-03600 | 存在问题

原文“global speed”译作“整体速度”。冻结术语子集对 `tformat` 技能说明中的该属性明确要求“全局速度”，并明确排除“整体速度”。快照的时空漩涡应用 30% 的速度降低，见 [rift.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/rift.lua:425)。



## O045 | entry-03600

### C11 | entry-03600 | 存在问题
- 原文 “reduces their global speed by 30%%”；译文 “使其整体速度降低 30%%”。
- 术语快照里 global speed 在 tformat 下是 preferred“全局速度”，备注明确写了“不写作‘整体速度’”。这是明确适用的术语要求。
- 源码：rift.lua 中 temporal_vortex 以 CHRONOSLOW slow=0.3 作用于半径 4（Pierce the Veil 段，约 rift.lua:425-426）。



## O046 | entry-03600

### C12 | entry-03600 | 仅建议
- “你的虚空造物属性随你的等级和魔法属性提高而提高”，Magic 用了“魔法属性”，与 C10 同类。



## O047 | entry-03600

### C12 | entry-03600 | 存在问题
- **原文短引**：`Temporal Vortex: Inflicts %0.2f temporal damage each turn to enemies in radius 4 and reduces their global speed by 30%%.`
- **译文短引**：`时空漩涡：每回合对半径 4 内的敌人造成 %0.2f 时空伤害，并使其整体速度降低 30%%。`
- **问题具体内容**：
  1. 违反明确适用的 preferred 术语规范：原文“global speed”被译为“整体速度”。本批冻结术语快照中包含明确规则：`global speed -> 全局速度`，status 为 `preferred`，并在 notes 中明确要求：“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文直接使用了禁止采用的“整体速度”。
  2. 属性术语偏差（附带观察）：末尾“Magic stat”同样译为了“魔法属性”（规范应为“魔力”）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/rift.lua:558-570`（DLC 源码快照未固定 commit，source_pinning=unpinned）；术语快照中条目：`global speed -> 全局速度 (preferred core, 不写作“整体速度”或“全体速度”)`。



## O048 | entry-03600

### C18 | entry-03600 | 存在问题

原文：“global speed”；译文：“整体速度”。

冻结术语子集中 `global speed / T.GAME.STAT / tformat` 为 preferred，明确适用于技能说明，并明确排除“整体速度”。本条正属该语境。

状态：**明确适用的术语要求违反已确认**。`S/rift.lua:420–426` 的减速参数也对应本段时空漩涡效果。



## O049 | entry-03602

### C07 | entry-03602 | 存在问题

原文“increasing their global speed”再次译作“增加他们 %d%% 的整体速度”，与同一条明确适用的 `tformat` 术语要求不符。快照通过 `global_speed_base` 增加召唤物速度，见 [rift.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/rift.lua:538)。



## O050 | entry-03602

### C13 | entry-03602 | 存在问题
- **原文短引**：`Dimensional Gate: Voidling Skitterers will be frenzied, increasing their global speed by %d%%.`
- **译文短引**：`维度之门 :#LAST# 虚空造物将会变得狂暴，增加他们 %d%% 的整体速度。`
- **问题具体内容**：
  违反明确适用的 preferred 术语规范：原文“global speed”再次被译为“整体速度”。同样违反了术语快照中 `global speed -> 全局速度 (preferred)` 的显式约束要求（“不写作‘整体速度’或‘全体速度’”）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/rift.lua:620-629`（DLC 源码快照未固定 commit，source_pinning=unpinned）；术语快照 `global speed -> 全局速度`。



## O051 | entry-03602

### C13 | entry-03602 | 存在问题
- 原文 “increasing their global speed by %d%%”；译文 “增加他们 %d%% 的整体速度”，同样违反 global speed 的 preferred 术语。
- 源码：rift.lua:539-540 `m.global_speed_base = m.global_speed_base + self.mult`，确实是全局速度。



## O052 | entry-03602

### C19 | entry-03602 | 存在问题

原文：“global speed”；译文：“整体速度”。

与 C18 相同的明确术语要求在本条再次被违反。`S/rift.lua:538–540` 对强化召唤物增加的是 `global_speed_base`。

状态：**术语问题已确认**。

另核查了本条“3 个额外目标”：`:331–337` 先把首目标放入列表，再循环加入最多 3 个其他目标。因此这处中文有快照依据，不列为缺陷。



## O053 | entry-03604

### C08 | entry-03604 | 存在问题

原文只说受害者内在的“something breaks”，继而让施法者侵入其心智；译文明确写成“**内部器官不断破损**”。器官破损是新增的具体生理事实，原文和该技能的窃取逻辑都没有给出这一信息。见 [slow-death.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/slow-death.lua:100)；同文件第 44–63 行处理可窃取技能。



## O054 | entry-03604

### C14 | entry-03604 | 仅建议
- **原文短引**：`When you digest you can steal a random talent from your victim and can use it for yourself at talent level %d.`
- **译文短引**：`你可以窃取并使用它的一个随机技能（技能等级 %d）。`
- **问题具体内容**：
  条件状语省略：原文第二句开头的明确触发动作“When you digest”（当你消化目标时）未在译文中显式译出。虽然第一句已铺垫了“正在被你消化的目标”，但第二句若补充“当你进行消化时”能更明确指出窃取技能的时机是在施放“消化（Digest）”击杀目标时发生。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/slow-death.lua:42-68, 100-107`（DLC 源码快照未固定 commit，source_pinning=unpinned）。被动技能“苦难折磨（Painful Agony）”在主动技能“消化（Digest）”斩杀目标时触发窃取逻辑。



## O055 | entry-03604

### C20 | entry-03604 | 存在问题

原文：“something breaks inside it”；译文：“内部器官不断破损”。

原文没有指定破损的是器官，也没有“不断”发生的过程描述；随后谈的是进入受害者心智。译文把含混的内在崩溃具体化为持续器官损伤，新增了两项叙事事实。

状态：**无依据的语义增添已确认**。证据为本条完整因果语境及 `S/slow-death.lua:100–105`；不需要据此推断额外游戏机制。



## O056 | entry-03605

### C09 | entry-03605 | 存在问题

原文将第一个 `%s` 直接接在“stats”后，供禁用后缀插入；译文却写成“当前属性**为 %s :**”。后缀为空时显示“属性为 ：”，后缀非空时显示“属性为 ，由于副手非空……：”，两种状态下句子都被插值位置破坏。`tformat` 的实参选择及后缀见 [tentacles.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/tentacles.lua:66) 第 66–80 行；entry-03606 是该后缀的冻结译文。



## O057 | entry-03605

### C10 | entry-03605 | 存在问题

原文带引号的“‘civilized people’”指“文明人”这一人群，译文改为“普通人”，改变了伪装效果所描述的人群范围。该措辞位于触手外观的心灵遮掩说明中，见 [tentacles.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/tentacles.lua:72) 第 72–79 行。



## O058 | entry-03605

### C15 | entry-03605 | 仅建议
- **原文短引**：`hit your target and those on the side whenever you hit with a basic attack.` / `Your tentacle hand currently has these stats%s:\n\t\t%s`
- **译文短引**：`副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。` / `你的触手当前属性为 %s :\n\t\t%s`
- **问题具体内容**：
  1. 方位措辞偏好：“those on the side”被译为“目标同侧”，语意容易被理解为“与目标在同一侧”；机制上是指攻击目标周围身侧/两侧的相邻单位，建议优化为“目标身侧/两侧的其他单位”。
  2. 排版小瑕疵：文末“当前属性为 %s :”中，冒号前包含多余的半角空格。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/tentacles.lua:66-82`（DLC 源码快照未固定 commit，source_pinning=unpinned）。



## O059 | entry-03605

### C21 | entry-03605 | 存在问题

原文：“'civilized people'”；译文：“普通人”。

civilized 限定的是文明社会／文明人的身份，并带有引号形成的叙事语气；“普通人”改成了平凡与特殊之分。两者不是同一人群属性，后面的隐藏恐魔形态说明也没有补回这项限定。

状态：**人群限定的语义变化已确认**。此判断来自本条叙事语境，不要求采用任何未冻结的术语。



## O060 | entry-03605

### C22 | entry-03605 | 待确认

原文：“your target and those on the side”；译文：“目标以及目标同侧的其他单位”。

`D/tome-cults/superload/mod/class/interface/Combat.lua:40–49` 根据攻击方向取施法者相邻的左右两个格子，并仅攻击其中的敌对单位。它没有扫描泛指的“目标同侧”区域。

“同侧”是否准确表达这两个侧邻格存在具体疑点。快照内范围可查，但目标版本适用性未固定，因此保留待确认。



## O061 | entry-03605

### C23 | entry-03605 | 待确认

原文：“whenever you hit with a basic attack”；译文：“当使用普通攻击”。

`D/tome-cults/superload/mod/class/interface/Combat.lua:29–37` 在原攻击完成后检查武器、技能、抑制标记及触手可用性，没有检查原攻击的 `hit` 返回值，也没有在此限定为普通攻击。

译文去掉“命中”条件反而更接近这段实现，不能简单判成漏译；但中英文保留的普通攻击限定与该通用入口之间仍有疑点。尚缺目标版本对应及完整调用覆盖证据。



## O062 | entry-03605

### C24 | entry-03605 | 待确认

原文：“Each time you make an attack with your tentacle”；译文：“每次触手攻击时，获得……疯狂值”。

`D/tome-cults/superload/mod/class/interface/Combat.lua:52–54` 检查并设置 `turn_procs.tentacle_insanity_gain`，同一回合后续触发不能再次由此获得疯狂值。`S/tentacles.lua:259–265` 的缠绕攻击路径也没有直接执行这项增益。

因此“每次触手攻击”与快照中的实际发放条件不完全一致，属于上游已有的触发频率疑点；目标版本适用性待确认。



## O063 | entry-03606

### C14 | entry-03606 | 仅建议
- 原文 “…but is currently disabled due to non-empty offhand”，主语是触手手；译文 “该技能暂时被禁用”。
- 本技能（变异之手）就是触手手本身。副手非空时 canTentacleCombat 返回 false，见 tentacles.lua:39-47 和 superload Combat.lua:32。
- 严格说，Diseased Tongue 用 force=true 仍能使用触手，见 disfigured-face.lua:39。英文原句同样有这种笼统，所以只作措辞建议。插入 03605 的 “%s :” 后能正常显示。



## O064 | entry-03609

### C16 | entry-03609 | 仅建议
- **原文短引**：`Not enough space to summon!`
- **译文短引**：`没有足够的空间召唤！`
- **问题具体内容**：
  标点偏好：本条译文末尾使用了感叹号“！”，与英文原文“!”对应；术语快照中存在 preferred 条目 `Not enough space to summon! -> 没有足够的空间召唤。`（域为 logSeen，以句号结尾）。本条在源码中的标签为 logPlayer，标点差异不造成信息损失或运行时故障，但建议依项目偏好统一标点。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/timethief.lua:200`（DLC 源码快照未固定 commit，source_pinning=unpinned）。



## O065 | entry-03610

### C25 | entry-03610 | 待确认

原文：“wearing light armor”；译文：“穿着轻甲”。

`S/void.lua:31` 调用 `hasLightArmor()`。固定本体 `E/game/modules/tome/class/interface/Combat.lua:2672–2678` 接受 `cloth`、`light`、`mummy` 三种子类，未只接受 `light`。

本条“必须穿着轻甲”可能将实际可用装备范围缩窄。英文也使用同样的概括，故不是单纯的中文新增问题；DLC 目标版本与该本体实现的组合适用性待确认。



## O066 | entry-03612

### C11 | entry-03612 | 存在问题

原文说明虚空之星每 `%d` 回合恢复一颗，**最多累积四颗**；译文只保留恢复频率，漏掉上限。快照的恢复逻辑仅在 `p.nb < 4` 时增星，图标也显示 `/4`；见 [void.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/void.lua:32) 第 32–51 行及第 135–141 行。

**读取范围与版本。** 实际读取了指定的 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/INPUT.md)、同目录的 `entries.json`、`context.lua`、`source-access.json`；以及其 `sections` 列明的 12 个 `sources/dlc/cults/tome-cults/data/talents/demented/` 单文件：`disfigured-face.lua`、`doom.lua`、`entropy.lua`、`friend-of-the-worm.lua`、`madness.lua`、`nether.lua`、`oblivion.lua`、`rift.lua`、`slow-death.lua`、`tentacles.lua`、`timethief.lua`、`void.lua`。额外读取的两份单文件是 `source-access.json` 所列 Cults 快照根目录下的 `tome-cults/data/damage_types.lua` 与 `tome-cults/data/timed_effects.lua`：前者由 `nether.lua` 的 `RIFT_EXPLOSION` 调用引入，后者由 `doom.lua` 的 `PROPHECY_OF_MADNESS` 及 `oblivion.lua` 的 `do_nihil`／`ENTROPIC_WASTING` 符号引入。14 份源码文件的 SHA-256 均与清单匹配。未读取其他报告、当前译文文件或其他源码版本；未创建临时文件，未修改仓库，未发现读取越界。本复核是审核观察，不是生产 `DONE_VERIFIED`。


## O067 | entry-03612

### C15 | entry-03612 | 存在问题
- 原文 “You regenerate 1 star every %d turns, stacking up to 4 times.”；译文 “虚空之星每经过 %d 回合自动恢复一颗。”
- 问题：漏了上限 4 颗这个数量限制。
- 源码：void.lua:49 `if p.nb < 4 then p.nb = p.nb + 1`，图标显示也是 “/4”（void.lua:35）。
- 其余内容已核实：40% 反冲是每回合 floor(reduce/20)、共 8 回合（void.lua:78），与译文一致。



## O068 | entry-03612

### C17 | entry-03612 | 存在问题
- **原文短引**：`You regenerate 1 star every %d turns, stacking up to 4 times.`
- **译文短引**：`虚空之星每经过 %d 回合自动恢复一颗。`
- **问题具体内容**：
  关键机制上限数值严重漏译：原文第三行包含核心限制从句“stacking up to 4 times”（最多叠加 4 颗 / 叠加上限 4 颗）。译文仅翻译了“虚空之星每经过 %d 回合自动恢复一颗”，将后半句关于层数上限的描述“stacking up to 4 times”完全漏译。这导致玩家无法从技能描述中获知虚空之星最大只能累积 4 颗这一关键机制限制，属于重要机制信息的遗漏。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/void.lua:38, 135-142`（DLC 源码快照未固定 commit，source_pinning=unpinned）。源码在休息恢复和状态维护时均硬编码限制最大星数 `local nb = 4`。

---



## O069 | entry-03612

### C26 | entry-03612 | 存在问题

原文：“stacking up to 4 times”；译文只保留“每经过 %d 回合自动恢复一颗”。

译文完全遗漏最多储存 4 颗的上限。`S/void.lua:49–50` 仅在 `p.nb < 4` 时补充星数，`:35` 的显示上限也为 4。

状态：**数量上限遗漏已确认**。这是冻结原译文直接可证的缺失，快照另提供机制支持。



## O070 | entry-03612

### C27 | entry-03612 | 待确认

原文：“only function in light armor”；译文：“只有装备轻甲时生效”。

本条重复出现 C25 的装备范围疑点：`S/void.lua:43` 调用的 `hasLightArmor()`，在固定本体 `E/game/modules/tome/class/interface/Combat.lua:2672–2678` 同时接受布甲及 mummy 子类。

它与上限遗漏是独立 claim。装备适用范围仍待目标 DLC 版本证据确认。

实际读取路径与版本如下。

冻结包根目录 `B`：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923`

读取了：

- `B/INPUT.md`
- `B/entries.json`
- `B/context.lua`
- `B/source-access.json`

其中 `entries.json` 的 SHA-256 为 `a1c330dc46cb4f868aac13366156944333cde688e913cfce5bac9a04cea8635f`；条目身份连续覆盖 entry-03573–entry-03612，共 40 条。

源码前缀 `S`：

`B/sources/dlc/cults/tome-cults/data/talents/demented`

读取并逐一核对了以下 12 个文件，SHA-256 全部匹配 `source-access.json`：

- `S/disfigured-face.lua`
- `S/doom.lua`
- `S/entropy.lua`
- `S/friend-of-the-worm.lua`
- `S/madness.lua`
- `S/nether.lua`
- `S/oblivion.lua`
- `S/rift.lua`
- `S/slow-death.lua`
- `S/tentacles.lua`
- `S/timethief.lua`
- `S/void.lua`

额外 DLC 源码前缀 `D`：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults`

读取了以下清单允许、哈希匹配的文件：

- `D/tome-cults/data/timed_effects.lua`：由已读技能的 `EFF_DISOLVED_FACE`、`EFF_GLIMPSE_OF_TRUE_HORROR`、`EFF_PROPHECY_*`、`EFF_WTW_SHARED_INSANITY`、`EFF_DARK_WHISPERS`、`EFF_DIGEST`、`EFF_ENTROPIC_WASTING` 等调用引入。
- `D/tome-cults/data/damage_types.lua`：由 `nether.lua` 的 `DamageType.RIFT`、`RIFT_EXPLOSION`、`VOIDBURN` 等调用引入。
- `D/tome-cults/superload/mod/class/interface/Combat.lua`：由触手技能的 `getTentacleCombat`、`canTentacleCombat`、`attackTargetWith` 消费链引入。

本体源码通过 `git -C /workspace/t-engine4 show` 读取，固定版本为：

`624a67329fe2ad440c5b344785a9c73fcf22ae63`

实际路径为：

- `E/game/modules/tome/class/Actor.lua`：追查伙伴的 `talent_cd_reduction` 消费；亦在此单文件查询铭文消费函数，但未定位到相应定义。
- `E/game/modules/tome/class/interface/Combat.lua`：追查 `hasLightArmor()` 及战斗接口。
- `E/game/modules/tome/data/damage_types.lua`：追查 `VOID` 的暗影／时空拆分，以及 `CHRONOSLOW` 的伤害和减速消费。

未发现占位符类型或既定 `args_order` 错位。未创建临时文件、子 agent，未修改仓库，未读取其他报告或当前译文文件，也未发生材料访问越界。最初默认沙箱读取因挂载隔离错误未启动，后续仅通过获准的只读调用访问上述材料。

本报告是独立审核观察，不是生产完成判定，不宣称 `DONE_VERIFIED`。

