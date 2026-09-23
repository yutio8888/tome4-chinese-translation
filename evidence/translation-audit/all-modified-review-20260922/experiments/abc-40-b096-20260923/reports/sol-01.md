40 条已逐条对照；占位符与颜色标记的顺序一致。另沿冻结源码中的 `actor.unused_talents_types` 查到升级奖励分支：50 级后还有类别点奖励，因此相关说明有一处沿袭英文原文的遗漏。我会把已证实问题、未能核定的觉醒技条件和纯措辞建议分开列出。
---

| 完整 entry-ID | 四类判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03212 | 未发现问题 | 属性增益标题与显示内容相符 |
| entry-03213 | 未发现问题 | 术语及数值归属正确 |
| entry-03214 | 未发现问题 | 术语及数值归属正确 |
| entry-03215 | 未发现问题 | 术语及数值归属正确 |
| entry-03216 | 存在问题 | C01：遗漏后续类别点等级 |
| entry-03217 | 未发现问题 | `x` 键切换简单显示 |
| entry-03218 | 未发现问题 | `x` 键切换进阶显示 |
| entry-03219 | 存在问题 | C02：背包满时也误报睡眠 |
| entry-03220 | 未发现问题 | 新任务状态与标记正确 |
| entry-03221 | 未发现问题 | 点击会打开任务面板 |
| entry-03222 | 未发现问题 | 操作含义及标记一致 |
| entry-03223 | 未发现问题 | 四个参数与栏位对应 |
| entry-03224 | 存在问题 | C03：“发现于”误指地点 |
| entry-03225 | 未发现问题 | 两个金额参数对应 |
| entry-03226 | 未发现问题 | 指向替换瞬时触发方式 |
| entry-03227 | 存在问题 | C04：“即爆”误述触发效果 |
| entry-03228 | 未发现问题 | 已准备状态正确 |
| entry-03229 | 未发现问题 | 正在准备状态正确 |
| entry-03230 | 存在问题 | C05：误述为分解陷阱 |
| entry-03231 | 存在问题 | C06：把等级不足说成技能数量不足 |
| entry-03232 | 未发现问题 | 失败原因参数保留 |
| entry-03233 | 未发现问题 | 技能等级不足的含义正确 |
| entry-03234 | 存在问题 | C07：取消选择时也提示正在准备 |
| entry-03235 | 未发现问题 | 数量上限参数正确 |
| entry-03236 | 待确认 | C08：通用的 50 属性门槛缺定义证据 |
| entry-03237 | 未发现问题 | 解锁选项名称参数正确 |
| entry-03238 | 未发现问题 | 仅检查已装备且可附加的物品 |
| entry-03239 | 未发现问题 | 随机与种子选择语境相符 |
| entry-03240 | 未发现问题 | 目标等级输入含义正确 |
| entry-03241 | 未发现问题 | 备份名称和版本参数正确 |
| entry-03242 | 未发现问题 | 基础属性作用对象正确 |
| entry-03243 | 未发现问题 | 额外属性作用对象正确 |
| entry-03244 | 存在问题 | C09：遗漏“可用”范围限定 |
| entry-03245 | 仅建议 | C10：调试日志措辞稍生硬 |
| entry-03246 | 未发现问题 | 阵营名称参数正确 |
| entry-03247 | 未发现问题 | 文件及错误参数对应 |
| entry-03248 | 未发现问题 | 样品预览及右键刷新相符 |
| entry-03249 | 未发现问题 | 生成、鉴定失败及错误参数对应 |
| entry-03250 | 未发现问题 | 错误参数及换行正确 |
| entry-03251 | 未发现问题 | 玩家身份标记正确 |

### C01 | entry-03216 | 存在问题

原文与译文都只列出“10、20 和 34 级”的类别点。固定源码的普通升级分支还在 **50 级后每隔 30 级**发放类别点，条件会在 64、94 级等满足。面向玩家的奖励说明遗漏了这一范围；这是**沿袭上游描述**，并非翻译新增。[Actor.lua](/workspace/t-engine4/game/modules/tome/class/Actor.lua:3959) `levelup()` 第 3959–3962 行；[LevelupDialog.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:433) `learnType()` 消费类别点。

### C02 | entry-03219 | 存在问题

“%s不能在睡眠中接收物品！”在目标队友**背包没有空间**时也会显示。`PartySendItem:use()` 把“不能加入背包”和“睡眠且非清醒梦者”合在同一失败分支，随后统一记录睡眠日志；列表本身则能分别显示 `[NO ROOM]` 与 `[SLEEPING]`。译文忠实沿袭了上游错误日志，玩家会收到错误原因。[PartySendItem.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/PartySendItem.lua:52) 第 52–55、74–78 行。

### C03 | entry-03224 | 存在问题

`Found as: %s` 的第二个参数实际是 `item.name`，即手札名称；“发现于：%s”却把名称表述成发现地点。`generateList()` 将 `l.name` 存入该字段，`select()` 再把它传给第二个 `%s`。[ShowLore.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/ShowLore.lua:82) 第 82–85、100–102 行。这是翻译新增的对象错误。

### C04 | entry-03227 | 存在问题

`primed trigger` 表示陷阱在放置时**立即触发**；“即爆”却限定为爆炸。该方式也适用于非爆炸陷阱。`TrapsSelect` 在 `actor.trap_primed == item.tid` 时显示此状态；陷阱实现明确把它称为 `instant trigger`，并按是否 primed 改变放置与触发行为。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:102) 第 102–109 行；固定提交的 `game/modules/tome/data/talents/cunning/traps.lua` 第 48–52、192–208 行。

### C05 | entry-03230 | 存在问题

“分解中”描述了拆解陷阱或物品，但此状态只是把已准备的陷阱从选择中移除；确认后执行 `unlearnTalentFull(tid)`，没有拆解地图上的陷阱。英文 `dismantling` 已采用这一不准确的动作描述，译文沿袭了它。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:118) 第 118–121 行；固定提交的 `game/modules/tome/data/talents/cunning/traps.lua` 第 605–612 行。

### C06 | entry-03231 | 存在问题

“需要更多技能”指向技能数量；实际条件是陷阱的 `tier` 高于当前陷阱精通技能的**原始等级**。相邻的失败日志也明确是技能等级不足。这是翻译新增的条件维度偏差。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:41) 第 41、122–124、142–144 行。

### C07 | entry-03234 | 存在问题

“准备了常规触发的陷阱。”在点击 primed 陷阱时、**切换选择状态之前**输出；再次点击以取消该准备时仍输出同一句。因此取消操作也会被报告成准备操作。这是上游日志的状态错误，译文沿袭。[TrapsSelect.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua:145) 第 145–151 行。

### C08 | entry-03236 | 待确认

“所有觉醒技都要求某项核心属性达到 50 点”照译了原文。已核实 25、42 级的觉醒点发放，但冻结的 `UberTalent.lua` 只调用 `actor:canLearnTalent(t)`，没有列出所有觉醒技及进阶技各自的属性要求。缺少完整的技能定义证据，无法确认“所有”的范围；本项**未认定为错误**。[UberTalent.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/UberTalent.lua:192) 第 192–199、260–282 行；固定提交的 `game/modules/tome/class/Actor.lua` 第 3963–3966 行。

### C09 | entry-03244 | 存在问题

原文是 `all available talents`，译文“所有的技能”遗漏了**可用**限定。调试代码默认只遍历角色已知技能树，并逐个检查能否学习；“解锁所有技能树”是另一个独立选项。因此无条件的“所有”扩大了该操作所述范围。[AdvanceActor.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/debug/AdvanceActor.lua:167) 第 167、210–215、341–365 行。

### C10 | entry-03245 | 仅建议

“升级角色 输入”能传达 `AdvanceActor inputs` 是调试日志的输入记录，只是空格和措辞稍显生硬；没有改变参数或操作含义。[AdvanceActor.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/debug/AdvanceActor.lua:270) 第 263–270 行。

### 读取范围与边界

读取了指定目录下的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/dialogs/` 下的 `LevelupDialog.lua`、`PartySendItem.lua`、`QuestPopup.lua`、`SentientWeapon.lua`、`ShowIngredients.lua`、`ShowLore.lua`、`ShowStore.lua`、`TrapsSelect.lua`、`UberTalent.lua`、`UnlockDialog.lua`、`UseItemDialog.lua`、`WandererSeed.lua` 和 `debug/AdvanceActor.lua`、`debug/AlterFaction.lua`、`debug/CreateItem.lua`。15 份冻结源码的 SHA-256 均与 `source-access.json` 一致，标注的源码版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

额外只读了该固定提交的 `game/modules/tome/data/talents/cunning/traps.lua`（由 `TrapsSelect.lua` 的 `trap_primed`、`Talents.trap_mastery_tids` 引入）、`game/modules/tome/class/Actor.lua` 与 `game/modules/tome/class/Player.lua`（由两个对话框消费的 actor 类别点、觉醒点字段引入）。曾尝试三个相关但不存在的单文件路径：`engine/interface/ActorTalents.lua`、`game/modules/tome/data/talents/uber/strength.lua`、`game/modules/tome/data/talents/uber.lua`；均未读取到内容。未读取其他报告或实验结果，未创建临时文件，未修改仓库。C08 仍待定义证据核验；没有越界读取。本报告仅为 REVIEWER 观察，不声称生产 `DONE_VERIFIED`。
