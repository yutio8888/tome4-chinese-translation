# 冻结40条译文：统一复核规则 v3（临时文件许可）

你是只读 REVIEWER。仅审本包 entry-03212–03251 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc40-b096-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 的实际行为为准。英文描述、术语或现有译文不能覆盖实现；若译文忠实复制了英文的机制错误，也应指出面向玩家的误述，并区分“沿袭上游描述”与“翻译新增”。不得仅凭变量名或英文猜机制。
3. 可读本 INPUT、同目录 entries.json、context.lua、source-access.json，以及 source-access.json 明确列出的十五份 sources/ 冻结源码。可搜索这些文件内的文本。
4. 需要追调用链时，只能对明确相关的单个公开源码文件执行 git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>。新增路径必须说明由哪个已读文件的调用/符号/require引入。禁止读取当前源码工作树、其他commit；禁止仓库根/game/等整目录git grep、rg或find搜索；不扫描仓库、其他task或报告定位答案。无法在该边界内找到证据时写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03212 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。

## entry-03212
位置：mod-tome.lua:42034；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Stat gives:
```
译文：
```text
属性提供：
```

## entry-03213
位置：mod-tome.lua:42036；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Physical save: 
```
译文：
```text
物理豁免：
```

## entry-03214
位置：mod-tome.lua:42042；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Mental save: 
```
译文：
```text
精神豁免：
```

## entry-03215
位置：mod-tome.lua:42043；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Spell save: 
```
译文：
```text
法术豁免：
```

## entry-03216
位置：mod-tome.lua:42054；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A talent category contains talents you may learn. You gain a talent category point at level 10, 20 and 34. You may also find trainers or artifacts that allow you to learn more.
A talent category point can be used either to learn a new category or increase the mastery of a known one.
```
译文：
```text
一个技能树包含你可以学习的技能。你会在 10、20 和 34 级时各获得一个技能树点数，也可以找到训练师或神器来学习更多。
每一点技能树点数可以用来学习一个新的技能树，或者提升一个已知技能树的熟练度。
```

## entry-03217
位置：mod-tome.lua:42068；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<Press 'x' to swap to simple display>
```
译文：
```text
<按 X 键切换简单显示>
```

## entry-03218
位置：mod-tome.lua:42071；section：mod-tome/dialogs/LevelupDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<Press 'x' to swap to advanced display>
```
译文：
```text
<按 X 键切换进阶显示>
```

## entry-03219
位置：mod-tome.lua:42133；section：mod-tome/dialogs/PartySendItem.lua；source_tag：log；args_order：None；special：None

原文：
```text
%s cannot receive items while asleep!
```
译文：
```text
%s不能在睡眠中接收物品！
```

## entry-03220
位置：mod-tome.lua:42142；section：mod-tome/dialogs/QuestPopup.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#New#LAST# Quest!
```
译文：
```text
#LIGHT_GREEN#新#LAST# 任务！
```

## entry-03221
位置：mod-tome.lua:42148；section：mod-tome/dialogs/QuestPopup.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#ANTIQUE_WHITE#(See your Journal for further details or click here)
```
译文：
```text
#ANTIQUE_WHITE#（点击此处或者打开任务面板查看详情）
```

## entry-03222
位置：mod-tome.lua:42154；section：mod-tome/dialogs/SentientWeapon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Keyboard: #00FF00#up key/down key#FFFFFF# to select a stat; #00FF00#right key#FFFFFF# to increase stat; #00FF00#left key#FFFFFF# to decrease a stat.
Mouse: #00FF00#Left click#FFFFFF# to increase a stat; #00FF00#right click#FFFFFF# to decrease a stat.

```
译文：
```text
键盘：#00FF00#上/下键#FFFFFF#选择属性，#00FF00#右键#FFFFFF#增加属性，#00FF00#左键#FFFFFF#降低属性。
鼠标：#00FF00#左键点击#FFFFFF#增加属性，#00FF00#右键点击#FFFFFF#降低属性。

```

## entry-03223
位置：mod-tome.lua:42237；section：mod-tome/dialogs/ShowIngredients.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#GOLD#Category:#AQUAMARINE# %s
#GOLD#Ingredient:#0080FF# %s
#GOLD#Quantity:#0080FF# %s
#GOLD#Text:#ANTIQUE_WHITE# %s
```
译文：
```text
#GOLD#分类：#AQUAMARINE# %s
#GOLD#材料：#0080FF# %s
#GOLD#数量：#0080FF# %s
#GOLD#描述：#ANTIQUE_WHITE# %s
```

## entry-03224
位置：mod-tome.lua:42256；section：mod-tome/dialogs/ShowLore.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#GOLD#Category:#AQUAMARINE# %s
#GOLD#Found as:#0080FF# %s
#GOLD#Text:#ANTIQUE_WHITE# %s
```
译文：
```text
#GOLD#分类：#AQUAMARINE# %s
#GOLD#发现于：#0080FF# %s
#GOLD#文本：#ANTIQUE_WHITE# %s
```

## entry-03225
位置：mod-tome.lua:42279；section：mod-tome/dialogs/ShowStore.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 (pays up to %0.2f gold, Your Gold: %0.2f)
```
译文：
```text
 (最多付款 %0.2f 金币，你的金币：%0.2f)
```

## entry-03226
位置：mod-tome.lua:42319；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (replacing instant trigger)
```
译文：
```text
 （替换瞬间启动机关）
```

## entry-03227
位置：mod-tome.lua:42320；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (primed trigger)
```
译文：
```text
 （即爆启动机关）
```

## entry-03228
位置：mod-tome.lua:42321；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (prepared)
```
译文：
```text
 （准备完毕）
```

## entry-03229
位置：mod-tome.lua:42322；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (preparing)
```
译文：
```text
 （准备中）
```

## entry-03230
位置：mod-tome.lua:42323；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (dismantling)
```
译文：
```text
 （分解中）
```

## entry-03231
位置：mod-tome.lua:42324；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (need more skill)
```
译文：
```text
 （需要更多技能）
```

## entry-03232
位置：mod-tome.lua:42326；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#You cannot prepare this trap: %s.
```
译文：
```text
#LIGHT_BLUE#你不能准备这个陷阱：%s。
```

## entry-03233
位置：mod-tome.lua:42327；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#You need more skill to prepare this trap.
```
译文：
```text
#LIGHT_BLUE#你的技能等级不足，无法准备这个陷阱。
```

## entry-03234
位置：mod-tome.lua:42328；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Preparing trap with normal trigger.
```
译文：
```text
#LIGHT_BLUE#准备了常规触发的陷阱。
```

## entry-03235
位置：mod-tome.lua:42330；section：mod-tome/dialogs/TrapsSelect.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#You cannot prepare more than %d traps.
```
译文：
```text
#LIGHT_BLUE#你不能准备多于%d个陷阱。
```

## entry-03236
位置：mod-tome.lua:42344；section：mod-tome/dialogs/UberTalent.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Number available: %d#LAST#
Prodigies are special talents that only the most powerful of characters can attain.%s
All of them require at least 50 in a core stat and many also have more special demands. You can learn a new prodigy at level 25 and 42.
```
译文：
```text
#LIGHT_GREEN#当前可用觉醒技能点：%d#LAST#
觉醒技是角色足够强大时才能获得的特殊技能。%s
所有觉醒技都要求某项核心属性达到 50 点，其中许多还有更特殊的额外要求。
你可以在人物等级达到25级和42级时各获得一个觉醒技能点。
```

## entry-03237
位置：mod-tome.lua:42360；section：mod-tome/dialogs/UnlockDialog.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Option unlocked: %s
```
译文：
```text
选项已解锁：%s
```

## entry-03238
位置：mod-tome.lua:42370；section：mod-tome/dialogs/UseItemDialog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You do not have any equipped items that it can be attached to.
```
译文：
```text
你没有已装备的、可供它附加的物品。
```

## entry-03239
位置：mod-tome.lua:42457；section：mod-tome/dialogs/WandererSeed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome, wandering one! The Wanderer class uses a randomly selected set of talent trees.
You can now choose how this set is selected:
```
译文：
```text
欢迎，流浪者！流浪者职业具有随机的技能树。
现在你将选择随机模式：
```

## entry-03240
位置：mod-tome.lua:42479；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 Advance to Level: 
```
译文：
```text
 升级到等级： 
```

## entry-03241
位置：mod-tome.lua:42480；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Restore: %s (v%d)
```
译文：
```text
恢复：%s (v%d)
```

## entry-03242
位置：mod-tome.lua:42484；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 Force all BASE stats to: 
```
译文：
```text
 设置所有基础属性为： 
```

## entry-03243
位置：mod-tome.lua:42485；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 Force all BONUS stats to: 
```
译文：
```text
 设置所有额外属性为： 
```

## entry-03244
位置：mod-tome.lua:42487；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Unlock & Learn all available talents to level: 
```
译文：
```text
解锁并学习所有的技能到等级： 
```

## entry-03245
位置：mod-tome.lua:42495；section：mod-tome/dialogs/debug/AdvanceActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#AdvanceActor inputs: %s
```
译文：
```text
#LIGHT_BLUE#升级角色 输入：%s
```

## entry-03246
位置：mod-tome.lua:42531；section：mod-tome/dialogs/debug/AlterFaction.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Alter: %s
```
译文：
```text
改变：%s
```

## entry-03247
位置：mod-tome.lua:42549；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：log；args_order：None；special：None

原文：
```text
#ORANGE# Create Object: Unable to load all objects from file %s:#GREY#
 %s
```
译文：
```text
#ORANGE# 创建物品：无法读取文件%s的所有物品：#GREY#
 %s
```

## entry-03248
位置：mod-tome.lua:42552；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Generate examples (right-click refreshes) 
```
译文：
```text
创建样品（右键刷新） 
```

## entry-03249
位置：mod-tome.lua:42554；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Object %s could not be generated or identified. Error:
%s
```
译文：
```text
#LIGHT_BLUE#物品%s无法被创建或鉴定。错误：
%s
```

## entry-03250
位置：mod-tome.lua:42558；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Error:
%s
```
译文：
```text
错误：
%s
```

## entry-03251
位置：mod-tome.lua:42567；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 #LIGHT_GREEN#(player)#LAST#
```
译文：
```text
 #LIGHT_GREEN#（玩家）#LAST#
```

## 相关术语快照
```tsv
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
```
