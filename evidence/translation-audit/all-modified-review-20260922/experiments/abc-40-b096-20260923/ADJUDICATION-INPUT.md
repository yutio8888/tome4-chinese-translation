# 匿名源码核验与归并：40 条 / 36 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、sources/ 内 source-access列明的15份源码。先阅读INPUT统一判定规则；沿其限定调用链可以git show固定commit单文件。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方36项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好36行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。


## O001 | entry-03216

### C01 | entry-03216 | 仅建议
- 原文 "increase the mastery of a known one"，译为「提升一个已知技能树的熟练度」；"talent category point" 译为「技能树点数」。
- 机制：LevelupDialog.lua:440-457 `learnType`。知道该技能树时，精通度 +0.2 并扣 1 点 `unused_talents_types`。译文语义正确，换行 `\n` 也保留了。
- 仅属偏好的理由：同一对话框的邻近译文（context.lua）把 mastery 译成「精通度」「技能类别掌握度」，把这种点数译成「技能树解锁点」。这里用「熟练度」「技能树点数」措辞不统一，但不造成误解。本包术语子集没有这两个词条。



## O002 | entry-03216

### C01 | entry-03216 | 存在问题

原文与译文都只列出“10、20 和 34 级”的类别点。固定源码的普通升级分支还在 **50 级后每隔 30 级**发放类别点，条件会在 64、94 级等满足。面向玩家的奖励说明遗漏了这一范围；这是**沿袭上游描述**，并非翻译新增。[Actor.lua](/workspace/t-engine4/game/modules/tome/class/Actor.lua:3959) `levelup()` 第 3959–3962 行；[LevelupDialog.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:433) `learnType()` 消费类别点。



## O003 | entry-03217

### C02 | entry-03217 | 仅建议
- 原文 "<Press 'x' to …>"，译为「<按 X 键切换简单显示>」。
- 源码：LevelupDialog.lua:110-115 `__TEXTINPUT` 只匹配小写 `c == 'x'`。
- 仅属偏好的理由：「X 键」按惯例指键盘上的物理按键，直接按下产生的就是小写 x。只有开着大写锁定或按住 Shift 才会失效，英文原文同样有这个限制。「切换简单显示」少了「到/为」，属语感问题。



## O004 | entry-03218

### C03 | entry-03218 | 仅建议
- 与 C02 相同，源码见 LevelupDialog.lua:1052 和 :110-115。



## O005 | entry-03219

### C01 | entry-03219 | 存在问题

原文：`cannot receive items while asleep!`  
译文：“不能在睡眠中接收物品！”

**状态：confirmed；沿袭上游误述。** 提示也会在接收者背包没有空间时出现，将拒收原因错误归为睡眠。

证据：`game/modules/tome/dialogs/PartySendItem.lua:53–55`，`use()` 将 `not item.actor:canAddToInven(...)` 与睡眠条件并列，任何一个成立均打印本条。该文件 `generateList():75–78` 仍将背包无空间的队员加入列表，并另标 `NO ROOM`，没有排除这一操作情形。此问题不是译文新增。



## O006 | entry-03219

### C01 | entry-03219 | 存在问题
- **原文短引**：`%s cannot receive items while asleep!`
- **译文短引**：`%s不能在睡眠中接收物品！`
- **问题具体内容**：面向玩家的机制误述（沿袭上游描述，非翻译新增）。源码中将“目标无物品栏空间”与“目标处于睡眠”在同一个 `if` 逻辑分支中判定并统一输出此条日志。当队友处于清醒状态但背包已满时，玩家尝试转移物品同样会触发此消息，向玩家误报队友“在睡眠中”。译文忠实还原英文原文，无翻译新增错误，但沿袭了上游代码导致的事实/触发条件误导。
- **状态**：存在问题（沿袭上游描述）
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/PartySendItem.lua:53-56`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/PartySendItem.lua#L53-L56) 中的 `_M:use(item)` 函数：
  ```lua
  if not item or not item.actor:canAddToInven(item.actor.INVEN_INVEN) or (item.actor:attr("sleep") and not item.actor:attr("lucid_dreamer")) then
      game.log("%s cannot receive items while asleep!", item.actor:getName():capitalize())
      return
  end
  ```
  消费逻辑为玩家在队友物品转移界面确认交付时，通过 `game.log` 向控制台输出操作失败原因。

---



## O007 | entry-03219

### C02 | entry-03219 | 存在问题

“%s不能在睡眠中接收物品！”在目标队友**背包没有空间**时也会显示。`PartySendItem:use()` 把“不能加入背包”和“睡眠且非清醒梦者”合在同一失败分支，随后统一记录睡眠日志；列表本身则能分别显示 `[NO ROOM]` 与 `[SLEEPING]`。译文忠实沿袭了上游错误日志，玩家会收到错误原因。[PartySendItem.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/PartySendItem.lua:52) 第 52–55、74–78 行。



## O008 | entry-03219

### C04 | entry-03219 | 存在问题（沿袭上游）
- 原文 "%s cannot receive items while asleep!"，译文「%s不能在睡眠中接收物品！」。
- 源码：PartySendItem.lua:52-56。条件是 `not item.actor:canAddToInven(...) or (sleep and not lucid_dreamer)`，所以接收方物品栏满了也会走这一条。generateList（:74-77）会把物品栏已满的成员标上 [NO ROOM]，但仍可选择。
- 面向玩家的误述：物品栏已满、而对方醒着时，日志也会说对方在睡眠中。这是上游复用同一条消息造成的，译文忠实于英文，不是翻译新增。单改这一条译文无法让两个分支都正确。



## O009 | entry-03220

### C05 | entry-03220 | 仅建议
- 译文「#LIGHT_GREEN#新#LAST# 任务！」里「新」和「任务」之间照搬了英文的词间空格。
- 源码：QuestPopup.lua:30、:70，外层加 `#cc9f33#` 前缀，#LAST# 回到该颜色，标记都正确。
- 仅属偏好的理由：中文词间多一个空格只是排版问题，不丢信息。



## O010 | entry-03222

### C02 | entry-03222 | 仅建议

原文：`Keyboard: ... right key ... left key`  
译文：“键盘：……右键……左键……”

**状态：advisory。** “右键／左键”单独阅读容易联想到鼠标，但段首“键盘”已限定设备，下一段也明确标为“鼠标”；未丢失增减方向信息。因此只记录措辞清晰度偏好，不计为操作错误。

证据：`game/modules/tome/dialogs/SentientWeapon.lua:53–56` 保留键盘、鼠标两段结构；`74–79` 的鼠标消费逻辑为左键增加、其他点击减少，与译文鼠标段一致。此外，`80–89` 的当前布局并未加入该说明控件，不能据此声称已经造成可见界面操作误导。



## O011 | entry-03222

### C02 | entry-03222 | 仅建议
- **原文短引**：`Keyboard: ... right key ... left key ...`
- **译文短引**：`键盘：... 右键 ... 左键 ...`
- **问题具体内容**：措辞偏好建议。在键盘操作说明中将 `right key` 和 `left key` 译为“右键”和“左键”，在中文直觉下容易与鼠标“左键/右键”产生表面混淆。若表达为“右方向键”与“左方向键”（或“方向键右/左”），与下一行“鼠标：#00FF00#左键点击...右键点击...”对比时更清晰工整。然而鉴于本句已位于明确的“键盘：”段落内且紧随“上/下键”，玩家实际操作不会产生实质误解，故仅属表达偏好。
- **状态**：仅建议
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/SentientWeapon.lua:53-56, 195-196`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/SentientWeapon.lua#L53-L56) 中的 `_M:init` 与 `_M:drawDialog`。消费逻辑为智能武器属性调整界面顶部说明区域文本。

---



## O012 | entry-03222

### C06 | entry-03222 | 存在问题（翻译新增）
- 原文 "Keyboard: … #00FF00#right key#FFFFFF# to increase stat; #00FF00#left key#FFFFFF# to decrease a stat. Mouse: Left click … increase; right click … decrease"。
- 译文键盘一行写「右键增加属性，左键降低属性」，鼠标一行写「左键点击增加属性，右键点击降低属性」。
- 问题：在中文里，「右键/左键」约定俗成指鼠标右键/左键。原文说的是方向键：SentientWeapon.lua:187-188 绑定的是 `MOVE_LEFT`/`MOVE_RIGHT`，:75 的鼠标左键 +1、其余按键 -1。
- 结果：同一段帮助里，「右键增加属性」和「右键点击降低属性」对玩家构成直接矛盾，「方向键」这一操作信息丢失。标记和结尾换行都保留，没有格式问题。
- 显示可达性（附注）：固定 commit 下这段文字可能根本不显示。`c_tut` 在 :53 创建，但 :87-88 已被注释，没有放进 loadUI。旧式 `drawDialog`（:192）也会用这段文字，但 engine/ui/Dialog.lua 在固定 commit 下没有调用 drawDialog 的代码（grep 无结果）。因此玩家实际能否看到这段文字待确认；文字本身的缺陷成立。



## O013 | entry-03224

### C03 | entry-03224 | 存在问题

`Found as: %s` 的第二个参数实际是 `item.name`，即手札名称；“发现于：%s”却把名称表述成发现地点。`generateList()` 将 `l.name` 存入该字段，`select()` 再把它传给第二个 `%s`。[ShowLore.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/ShowLore.lua:82) 第 82–85、100–102 行。这是翻译新增的对象错误。



## O014 | entry-03224

### C03 | entry-03224 | 存在问题

原文：`Found as: %s`  
译文：“发现于：%s”

**状态：confirmed；翻译新增。** “发现于”将后面的内容表达为发现地点，实际填入的是手札名称，改变了字段的语义关系。

证据：`game/modules/tome/dialogs/ShowLore.lua:83–85` 从手札定义取得 `l.name`，保存为 `item.name`；`select():102` 依次传入 `item.cat, item.name, item.desc`。第二个参数不是地点字段。



## O015 | entry-03224

### C07 | entry-03224 | 存在问题（翻译新增）
- 原文 "#GOLD#Found as:#0080FF# %s"，译文「#GOLD#发现于：#0080FF# %s」。
- 源码：ShowLore.lua:102 调用 `tformat(item.cat, item.name, item.desc)`，第二个参数 `item.name` 来自 :85 的 `name=l.name`，是这篇手札本身的名称/标题。
- 问题：「发现于」的意思是「在某地/某时发现」，会让玩家把后面的手札名当成发现地点。原文 "Found as" 表示「以……形式/名目被发现」。字段与值的关系被译错。



## O016 | entry-03225

### C08 | entry-03225 | 仅建议
- 译文「(最多付款 %0.2f 金币，你的金币：%0.2f)」。
- 源码：ShowStore.lua:173，第一个参数是 `store.purse`，第二个是玩家金钱，顺序正确。
- 仅属偏好的理由：付款方省略了，但标题前缀就是商店名，英文同样没有主语。purse 的精确规则在所读文件之外，这里不作机制判断。



## O017 | entry-03227

### C04 | entry-03227 | 存在问题

`primed trigger` 表示陷阱在放置时**立即触发**；“即爆”却限定为爆炸。该方式也适用于非爆炸陷阱。`TrapsSelect` 在 `actor.trap_primed == item.tid` 时显示此状态；陷阱实现明确把它称为 `instant trigger`，并按是否 primed 改变放置与触发行为。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:102) 第 102–109 行；固定提交的 `game/modules/tome/data/talents/cunning/traps.lua` 第 48–52、192–208 行。



## O018 | entry-03230

### C05 | entry-03230 | 存在问题

“分解中”描述了拆解陷阱或物品，但此状态只是把已准备的陷阱从选择中移除；确认后执行 `unlearnTalentFull(tid)`，没有拆解地图上的陷阱。英文 `dismantling` 已采用这一不准确的动作描述，译文沿袭了它。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:118) 第 118–121 行；固定提交的 `game/modules/tome/data/talents/cunning/traps.lua` 第 605–612 行。



## O019 | entry-03230

### C09 | entry-03230 | 仅建议
- 原文 " (dismantling)"，译文「（分解中）」。
- 源码：TrapsSelect.lua:119-121，指原本已准备、这次取消选择、将被拆除的陷阱。
- 仅属偏好的理由：「拆除中」更贴近原意；「分解」容易联想到拆解物品取材料，但在列表语境下不致误解。



## O020 | entry-03231

### C03 | entry-03231 | 存在问题
- **原文短引**：` (need more skill)`
- **译文短引**：` （需要更多技能）`
- **问题具体内容**：语义与机制条件误译（翻译新增）。源码判断条件为 `item.tier > self.mastery_level`，其中 `self.mastery_level` 为当前玩家“陷阱精通”（Trap Mastery）技能的等级（1–5）。英文中 `skill` 为不可数名词，在此语境指技能熟练度/技能等级（即需要更高的陷阱技能等级）。译文译为“需要更多技能”，使玩家误以为需要去学习更多数量的其他技能。对比同文件同一触发条件的日志条目 entry-03233（[`TrapsSelect.lua:143`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua#L143)），该处已被正确译为“你的技能等级不足，无法准备这个陷阱。”，证明 entry-03231 存在对机制条件的理解与翻译偏差。
- **状态**：存在问题（翻译新增）
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/TrapsSelect.lua:122-124`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua#L122-L124) 中的 `_M:formatItem(item)`：
  ```lua
  elseif item.tier > self.mastery_level then
      item.color = colors_simple.GREY
      add_text = _t" (need more skill)"
  ```
  消费逻辑为在陷阱选择对话框中，当陷阱阶数（tier）超出玩家当前精通等级时，作为置灰后缀字符串拼接到条目名称尾部显示。

---



## O021 | entry-03231

### C04 | entry-03231 | 存在问题

原文：`need more skill`  
译文：“需要更多技能”

**状态：confirmed；翻译新增。** 此处要求提高掌握程度，译文却表达为需要更多项技能，误述了不足的条件。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:41` 用 `actor:getTalentLevelRaw(dialog_talent)` 设置 `mastery_level`；`formatItem():122–124` 仅在 `item.tier > self.mastery_level` 时显示本条。`use():142–143` 对同一条件给出相邻条目“你的技能等级不足”，也明确了语境。



## O022 | entry-03231

### C06 | entry-03231 | 存在问题

“需要更多技能”指向技能数量；实际条件是陷阱的 `tier` 高于当前陷阱精通技能的**原始等级**。相邻的失败日志也明确是技能等级不足。这是翻译新增的条件维度偏差。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:41) 第 41、122–124、142–144 行。



## O023 | entry-03231

### C10 | entry-03231 | 存在问题（翻译新增）
- 原文 " (need more skill)"，译文「（需要更多技能）」。
- 源码：TrapsSelect.lua:122-124 的条件是 `item.tier > self.mastery_level`，而 :41 `mastery_level = actor:getTalentLevelRaw(dialog_talent)`，即当前陷阱掌握技能的原始等级不够。
- 问题：本译本里「技能」是 talent 的对应词，「需要更多技能」读起来像「需要学会更多技能」（数量），而不是「技能等级不足」。条件的对象被偏移了。同文件 entry-03233 对同一条件译成「你的技能等级不足」，是准确的。



## O024 | entry-03234

### C05 | entry-03234 | 存在问题

原文：`Preparing trap with normal trigger.`  
译文：“准备了常规触发的陷阱。”

**状态：confirmed；翻译新增。** “准备了”把尚待确认的选择写成已经完成的准备，提前了生效时序。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:145–151` 打印提示后，只切换对话框中的 `traps_selected` 并刷新列表；`159–162` 才在确认时返回选择结果。实际修改发生在 `game/modules/tome/data/talents/cunning/traps.lua:603–621`：等待对话框返回后学习所选陷阱，并清除对应的 `trap_primed`。退出对话框的路径 `TrapsSelect.lua:79–81` 不执行这项确认。



## O025 | entry-03234

### C06 | entry-03234 | 存在问题

原文：`Preparing trap with normal trigger.`  
译文：“准备了常规触发的陷阱。”

**状态：confirmed；沿袭上游误述。** 再次点击、取消该陷阱的常规准备选择时，仍会打印正在准备的提示，操作方向与信息不符。这与 C05 的完成时序问题独立。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:145–148` 仅凭 `tid == self.actor.trap_primed` 打印本条，随后无条件取反 `self.traps_selected[tid]`。因此从已选切回未选时，同样打印该提示。英文原文已有此问题。



## O026 | entry-03234

### C07 | entry-03234 | 存在问题

“准备了常规触发的陷阱。”在点击 primed 陷阱时、**切换选择状态之前**输出；再次点击以取消该准备时仍输出同一句。因此取消操作也会被报告成准备操作。这是上游日志的状态错误，译文沿袭。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:145) 第 145–151 行。



## O027 | entry-03234

### C11 | entry-03234 | 存在问题（翻译新增）
- 原文 "#LIGHT_BLUE#Preparing trap with normal trigger."，译文「…准备了常规触发的陷阱。」
- 源码：TrapsSelect.lua:145-148。这条日志在对话框里切换选择时就会发出，真正的准备要等 "Accept" 之后通过 `talentDialogReturn` 生效（:161）。按 EXIT（:79）关闭对话框，选择会被丢弃。
- 问题：「准备了」把尚未提交的选择说成已完成，时序信息有误。原文用进行时 "Preparing"。



## O028 | entry-03234

### C12 | entry-03234 | 存在问题（沿袭上游）
- 源码：TrapsSelect.lua:145-148。只要 `tid == trap_primed` 就先写日志、再翻转选择状态。如果该陷阱当时已被选中（显示 "replacing instant trigger"），这次点击其实是取消选择，退回瞬发状态（:106-108 "primed trigger"），日志却仍说「以常规触发准备」。
- 性质：上游描述与实现分支不符，译文照搬了这一点，不是翻译新增。



## O029 | entry-03236

### C08 | entry-03236 | 待确认

“所有觉醒技都要求某项核心属性达到 50 点”照译了原文。已核实 25、42 级的觉醒点发放，但冻结的 `UberTalent.lua` 只调用 `actor:canLearnTalent(t)`，没有列出所有觉醒技及进阶技各自的属性要求。缺少完整的技能定义证据，无法确认“所有”的范围；本项**未认定为错误**。[UberTalent.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/UberTalent.lua:192) 第 192–199、260–282 行；固定提交的 `game/modules/tome/class/Actor.lua` 第 3963–3966 行。



## O030 | entry-03239

### C07 | entry-03239 | 存在问题

原文：`You can now choose how this set is selected:`  
译文：“现在你将选择随机模式：”

**状态：confirmed；翻译新增。** 原文让玩家选择技能树组合的生成方式，译文将其写成选择“随机模式”，缩窄了选项范围，并与本界面一个具体选项同名。

证据：`game/modules/tome/dialogs/WandererSeed.lua:46–50` 提供 `Random` 与 `Seed` 两个互斥选项；`swapMode():68–78` 分别处理两种模式；`154–165` 在种子模式下使用玩家输入的种子。冻结 `context.lua` 又明确将两个选项分别译作“随机模式”和“种子模式”，因此这里不是无损概括。



## O031 | entry-03239

### C13 | entry-03239 | 存在问题（翻译新增）
- 原文 "You can now choose how this set is selected:"，译文「现在你将选择随机模式：」。
- 源码：WandererSeed.lua:46/49，下面两个选项分别是「随机模式」和「种子模式」（邻近译文）。
- 问题：原文要玩家在两种选取方式中挑一种。译文「选择随机模式」和第一个选项的标签字面相同，容易读成「接下来就是选随机模式」。「二选一」这一信息丢失，"can" 也被改成了「将」。



## O032 | entry-03244

### C08 | entry-03244 | 存在问题

原文：`Unlock & Learn all available talents to level:`  
译文：“解锁并学习所有的技能到等级：”

**状态：confirmed；翻译新增。** 译文遗漏 `available`，将有范围限制的学习操作表述为学习所有技能。

证据：`game/modules/tome/dialogs/debug/AdvanceActor.lua:341–355` 只遍历角色已有的 `talents_types`，排除物品使用技能、刻印及觉醒技，并在未勾选忽略需求时调用 `canLearnTalent()`。`210–215` 另设解锁全部技能树选项，`334–339` 仅在该选项启用时扩展技能树集合。本条不能无条件承诺覆盖所有技能。


## O033 | entry-03244

### C09 | entry-03244 | 存在问题

原文是 `all available talents`，译文“所有的技能”遗漏了**可用**限定。调试代码默认只遍历角色已知技能树，并逐个检查能否学习；“解锁所有技能树”是另一个独立选项。因此无条件的“所有”扩大了该操作所述范围。[AdvanceActor.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/debug/AdvanceActor.lua:167) 第 167、210–215、341–365 行。



## O034 | entry-03244

### C14 | entry-03244 | 存在问题（翻译新增，调试界面）
- 原文 "Unlock & Learn all available talents to level:"，译文「解锁并学习所有的技能到等级：」。
- 源码：AdvanceActor.lua:341-363。只遍历角色已有的技能树 `who.talents_types`，排除 `is_object_use`、`is_inscription`、`uber` 类技能，并且除非勾选「无视技能需求」，每一级都要通过 `canLearnTalent`。
- 问题：删掉 "available" 把作用范围夸大成「所有技能」，属于范围限定词缺失。只影响调试界面。



## O035 | entry-03245

### C10 | entry-03245 | 仅建议

“升级角色 输入”能传达 `AdvanceActor inputs` 是调试日志的输入记录，只是空格和措辞稍显生硬；没有改变参数或操作含义。[AdvanceActor.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/debug/AdvanceActor.lua:270) 第 263–270 行。



## O036 | entry-03248

### C15 | entry-03248 | 仅建议
- 原文 "Generate examples (right-click refreshes) "，译文「创建样品（右键刷新） 」。
- 源码：CreateItem.lua:116-124 是一个复选框，勾选后在 list_select（:193 起）用 finishEntity 生成示例并显示在 tooltip，不放进物品栏；:178 右键会清掉缓存并重新生成。
- 仅属偏好的理由：「生成示例」更贴切，但同一对话框一直用「样品」，调试界面上不致误用。

---


