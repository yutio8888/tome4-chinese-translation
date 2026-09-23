# REVIEWER 复核报告：entry-03212–03251（40 条，translation_contextual_v1 自然语言实验旁路）

## 判定表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03212 | 未发现问题 | LevelupDialog.lua:879，小标题，下列各行是属性变化带来的数值 |
| entry-03213 | 未发现问题 | :883/:907，术语 preferred「物理豁免」一致 |
| entry-03214 | 未发现问题 | :899/:910，术语 preferred「精神豁免」一致 |
| entry-03215 | 未发现问题 | :900/:916，术语 preferred「法术豁免」一致 |
| entry-03216 | 仅建议 | C01 |
| entry-03217 | 仅建议 | C02 |
| entry-03218 | 仅建议 | C03 |
| entry-03219 | 存在问题 | C04（沿袭上游） |
| entry-03220 | 仅建议 | C05 |
| entry-03221 | 未发现问题 | QuestPopup.lua:86-90，点击后打开 ShowQuests，译「任务面板」准确 |
| entry-03222 | 存在问题 | C06 |
| entry-03223 | 未发现问题 | ShowIngredients.lua:75，四个参数和颜色标记都保留 |
| entry-03224 | 存在问题 | C07 |
| entry-03225 | 仅建议 | C08 |
| entry-03226 | 未发现问题 | TrapsSelect.lua:102-105 |
| entry-03227 | 未发现问题 | TrapsSelect.lua:106-108 |
| entry-03228 | 未发现问题 | TrapsSelect.lua:112-114 |
| entry-03229 | 未发现问题 | TrapsSelect.lua:115-117 |
| entry-03230 | 仅建议 | C09 |
| entry-03231 | 存在问题 | C10 |
| entry-03232 | 未发现问题 | TrapsSelect.lua:140-141，%s 是 unlearnable 原因 |
| entry-03233 | 未发现问题 | TrapsSelect.lua:142-143，条件是 tier > 陷阱掌握技能的原始等级 |
| entry-03234 | 存在问题 | C11（翻译新增）、C12（沿袭上游） |
| entry-03235 | 未发现问题 | TrapsSelect.lua:160-164，num_sel <= max_traps |
| entry-03236 | 未发现问题 | UberTalent.lua:192-198，%d/%s 顺序和 evotext 插入位置正确 |
| entry-03237 | 未发现问题 | UnlockDialog.lua:36 |
| entry-03238 | 未发现问题 | UseItemDialog.lua:121 |
| entry-03239 | 存在问题 | C13 |
| entry-03240 | 未发现问题 | AdvanceActor.lua:61 |
| entry-03241 | 未发现问题 | AdvanceActor.lua:76，%s/%d 顺序正确 |
| entry-03242 | 未发现问题 | AdvanceActor.lua:119，基础属性 |
| entry-03243 | 未发现问题 | AdvanceActor.lua:144，额外属性（incIncStat） |
| entry-03244 | 存在问题 | C14 |
| entry-03245 | 未发现问题 | AdvanceActor.lua:270，调试日志 |
| entry-03246 | 未发现问题 | AlterFaction.lua:66，%s 是阵营名 |
| entry-03247 | 未发现问题 | CreateItem.lua:53，两个参数、#GREY# 和换行都保留 |
| entry-03248 | 仅建议 | C15 |
| entry-03249 | 未发现问题 | CreateItem.lua:215 |
| entry-03250 | 未发现问题 | CreateItem.lua:216 |
| entry-03251 | 未发现问题 | CreateItem.lua:257/263 |

合计：存在问题 8 条，仅建议 8 条，未发现问题 24 条，待确认 0 条。

---

### C01 | entry-03216 | 仅建议
- 原文 "increase the mastery of a known one"，译为「提升一个已知技能树的熟练度」；"talent category point" 译为「技能树点数」。
- 机制：LevelupDialog.lua:440-457 `learnType`。知道该技能树时，精通度 +0.2 并扣 1 点 `unused_talents_types`。译文语义正确，换行 `\n` 也保留了。
- 仅属偏好的理由：同一对话框的邻近译文（context.lua）把 mastery 译成「精通度」「技能类别掌握度」，把这种点数译成「技能树解锁点」。这里用「熟练度」「技能树点数」措辞不统一，但不造成误解。本包术语子集没有这两个词条。

### C02 | entry-03217 | 仅建议
- 原文 "<Press 'x' to …>"，译为「<按 X 键切换简单显示>」。
- 源码：LevelupDialog.lua:110-115 `__TEXTINPUT` 只匹配小写 `c == 'x'`。
- 仅属偏好的理由：「X 键」按惯例指键盘上的物理按键，直接按下产生的就是小写 x。只有开着大写锁定或按住 Shift 才会失效，英文原文同样有这个限制。「切换简单显示」少了「到/为」，属语感问题。

### C03 | entry-03218 | 仅建议
- 与 C02 相同，源码见 LevelupDialog.lua:1052 和 :110-115。

### C04 | entry-03219 | 存在问题（沿袭上游）
- 原文 "%s cannot receive items while asleep!"，译文「%s不能在睡眠中接收物品！」。
- 源码：PartySendItem.lua:52-56。条件是 `not item.actor:canAddToInven(...) or (sleep and not lucid_dreamer)`，所以接收方物品栏满了也会走这一条。generateList（:74-77）会把物品栏已满的成员标上 [NO ROOM]，但仍可选择。
- 面向玩家的误述：物品栏已满、而对方醒着时，日志也会说对方在睡眠中。这是上游复用同一条消息造成的，译文忠实于英文，不是翻译新增。单改这一条译文无法让两个分支都正确。

### C05 | entry-03220 | 仅建议
- 译文「#LIGHT_GREEN#新#LAST# 任务！」里「新」和「任务」之间照搬了英文的词间空格。
- 源码：QuestPopup.lua:30、:70，外层加 `#cc9f33#` 前缀，#LAST# 回到该颜色，标记都正确。
- 仅属偏好的理由：中文词间多一个空格只是排版问题，不丢信息。

### C06 | entry-03222 | 存在问题（翻译新增）
- 原文 "Keyboard: … #00FF00#right key#FFFFFF# to increase stat; #00FF00#left key#FFFFFF# to decrease a stat. Mouse: Left click … increase; right click … decrease"。
- 译文键盘一行写「右键增加属性，左键降低属性」，鼠标一行写「左键点击增加属性，右键点击降低属性」。
- 问题：在中文里，「右键/左键」约定俗成指鼠标右键/左键。原文说的是方向键：SentientWeapon.lua:187-188 绑定的是 `MOVE_LEFT`/`MOVE_RIGHT`，:75 的鼠标左键 +1、其余按键 -1。
- 结果：同一段帮助里，「右键增加属性」和「右键点击降低属性」对玩家构成直接矛盾，「方向键」这一操作信息丢失。标记和结尾换行都保留，没有格式问题。
- 显示可达性（附注）：固定 commit 下这段文字可能根本不显示。`c_tut` 在 :53 创建，但 :87-88 已被注释，没有放进 loadUI。旧式 `drawDialog`（:192）也会用这段文字，但 engine/ui/Dialog.lua 在固定 commit 下没有调用 drawDialog 的代码（grep 无结果）。因此玩家实际能否看到这段文字待确认；文字本身的缺陷成立。

### C07 | entry-03224 | 存在问题（翻译新增）
- 原文 "#GOLD#Found as:#0080FF# %s"，译文「#GOLD#发现于：#0080FF# %s」。
- 源码：ShowLore.lua:102 调用 `tformat(item.cat, item.name, item.desc)`，第二个参数 `item.name` 来自 :85 的 `name=l.name`，是这篇手札本身的名称/标题。
- 问题：「发现于」的意思是「在某地/某时发现」，会让玩家把后面的手札名当成发现地点。原文 "Found as" 表示「以……形式/名目被发现」。字段与值的关系被译错。

### C08 | entry-03225 | 仅建议
- 译文「(最多付款 %0.2f 金币，你的金币：%0.2f)」。
- 源码：ShowStore.lua:173，第一个参数是 `store.purse`，第二个是玩家金钱，顺序正确。
- 仅属偏好的理由：付款方省略了，但标题前缀就是商店名，英文同样没有主语。purse 的精确规则在所读文件之外，这里不作机制判断。

### C09 | entry-03230 | 仅建议
- 原文 " (dismantling)"，译文「（分解中）」。
- 源码：TrapsSelect.lua:119-121，指原本已准备、这次取消选择、将被拆除的陷阱。
- 仅属偏好的理由：「拆除中」更贴近原意；「分解」容易联想到拆解物品取材料，但在列表语境下不致误解。

### C10 | entry-03231 | 存在问题（翻译新增）
- 原文 " (need more skill)"，译文「（需要更多技能）」。
- 源码：TrapsSelect.lua:122-124 的条件是 `item.tier > self.mastery_level`，而 :41 `mastery_level = actor:getTalentLevelRaw(dialog_talent)`，即当前陷阱掌握技能的原始等级不够。
- 问题：本译本里「技能」是 talent 的对应词，「需要更多技能」读起来像「需要学会更多技能」（数量），而不是「技能等级不足」。条件的对象被偏移了。同文件 entry-03233 对同一条件译成「你的技能等级不足」，是准确的。

### C11 | entry-03234 | 存在问题（翻译新增）
- 原文 "#LIGHT_BLUE#Preparing trap with normal trigger."，译文「…准备了常规触发的陷阱。」
- 源码：TrapsSelect.lua:145-148。这条日志在对话框里切换选择时就会发出，真正的准备要等 "Accept" 之后通过 `talentDialogReturn` 生效（:161）。按 EXIT（:79）关闭对话框，选择会被丢弃。
- 问题：「准备了」把尚未提交的选择说成已完成，时序信息有误。原文用进行时 "Preparing"。

### C12 | entry-03234 | 存在问题（沿袭上游）
- 源码：TrapsSelect.lua:145-148。只要 `tid == trap_primed` 就先写日志、再翻转选择状态。如果该陷阱当时已被选中（显示 "replacing instant trigger"），这次点击其实是取消选择，退回瞬发状态（:106-108 "primed trigger"），日志却仍说「以常规触发准备」。
- 性质：上游描述与实现分支不符，译文照搬了这一点，不是翻译新增。

### C13 | entry-03239 | 存在问题（翻译新增）
- 原文 "You can now choose how this set is selected:"，译文「现在你将选择随机模式：」。
- 源码：WandererSeed.lua:46/49，下面两个选项分别是「随机模式」和「种子模式」（邻近译文）。
- 问题：原文要玩家在两种选取方式中挑一种。译文「选择随机模式」和第一个选项的标签字面相同，容易读成「接下来就是选随机模式」。「二选一」这一信息丢失，"can" 也被改成了「将」。

### C14 | entry-03244 | 存在问题（翻译新增，调试界面）
- 原文 "Unlock & Learn all available talents to level:"，译文「解锁并学习所有的技能到等级：」。
- 源码：AdvanceActor.lua:341-363。只遍历角色已有的技能树 `who.talents_types`，排除 `is_object_use`、`is_inscription`、`uber` 类技能，并且除非勾选「无视技能需求」，每一级都要通过 `canLearnTalent`。
- 问题：删掉 "available" 把作用范围夸大成「所有技能」，属于范围限定词缺失。只影响调试界面。

### C15 | entry-03248 | 仅建议
- 原文 "Generate examples (right-click refreshes) "，译文「创建样品（右键刷新） 」。
- 源码：CreateItem.lua:116-124 是一个复选框，勾选后在 list_select（:193 起）用 finishEntity 生成示例并显示在 tooltip，不放进物品栏；:178 右键会清掉缓存并重新生成。
- 仅属偏好的理由：「生成示例」更贴切，但同一对话框一直用「样品」，调试界面上不致误用。

---

## 读取路径与边界说明

- 冻结输入（只读）：同目录下的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。
- 冻结源码（`sources/…`，15 份，sha256 已逐一核对，与 `source-access.json` 全部一致）：LevelupDialog、PartySendItem、QuestPopup、SentientWeapon、ShowIngredients、ShowLore、ShowStore、TrapsSelect、UberTalent、UnlockDialog、UseItemDialog、WandererSeed，以及 debug/AdvanceActor、debug/AlterFaction、debug/CreateItem。
- 额外源码 1 份：`git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:game/engines/default/engine/ui/Dialog.lua`，只 grep 了 drawDialog、display、toScreen。
  - 引入依据：SentientWeapon.lua:22 `require "engine.ui.Dialog"`，用来判断 :192 的 `drawDialog` 是否会被调用（对应 C06 的附注）。
- 未读取：SPEC.md、PLAN.md、STATE.json、SCOPE.json、FREEZE.json、BASELINE.json、dispatches/、raw/、reports/、其他报告和当前翻译文件；没有做整目录搜索。
  - `entries.json` 里的 `baseline_target`、`gemini_status` 等字段是随包自带的，只用来确认身份，没有作为判断依据。
- 未能在边界内核验的内容：
  - 技能树点在 10/20/34 级、觉醒点在 25/42 级获得，以及 store.purse 的精确规则，都在 Actor/Store 类中，所读文件没有 require 链引入它们，所以未核验。对应译文与英文一致，也没有具体疑点，因此不列为待确认。
  - C06 的显示可达性只查了 engine/ui/Dialog.lua 的 grep，所以记为附注性待确认。
- 临时文件：没有创建。没有越界，没有写入仓库，没有创建子 agent。
- 以上是审核观察，不是真值，不宣称 DONE_VERIFIED。
