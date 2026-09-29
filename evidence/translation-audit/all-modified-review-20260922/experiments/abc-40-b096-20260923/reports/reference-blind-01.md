| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03212 | 未发现问题 | 属性效果分组标题，语义符合上下文 |
| entry-03213 | 未发现问题 | 豁免术语正确，数值拼接有效 |
| entry-03214 | 未发现问题 | 豁免术语正确，数值拼接有效 |
| entry-03215 | 未发现问题 | 豁免术语正确，数值拼接有效 |
| entry-03216 | 未发现问题 | 所列获取等级及两项用途与实现一致 |
| entry-03217 | 未发现问题 | X 为键名表述，显示切换方向正确 |
| entry-03218 | 未发现问题 | X 为键名表述，显示切换方向正确 |
| entry-03219 | 存在问题 | C01：背包无空间也会显示睡眠原因 |
| entry-03220 | 未发现问题 | 新任务状态与颜色标记对应 |
| entry-03221 | 未发现问题 | 点击实际打开任务列表 |
| entry-03222 | 仅建议 | C02：键盘段“左键／右键”的清晰度偏好 |
| entry-03223 | 未发现问题 | 四项参数依次对应分类、材料、数量、描述 |
| entry-03224 | 存在问题 | C03：手札名称被标作发现地点 |
| entry-03225 | 未发现问题 | 商店付款上限与玩家金币参数对应 |
| entry-03226 | 未发现问题 | 对应将即刻触发配置替换为常规配置 |
| entry-03227 | 未发现问题 | “即爆”符合放置时立即触发的实现 |
| entry-03228 | 未发现问题 | 对应原已准备且仍保留的陷阱 |
| entry-03229 | 未发现问题 | 对应本次新选、尚待确认的陷阱 |
| entry-03230 | 未发现问题 | 对应取消原有准备，确认后遗忘该陷阱 |
| entry-03231 | 存在问题 | C04：技能等级不足被译成技能数量不足 |
| entry-03232 | 未发现问题 | 无法学习的具体原因填入 `%s` |
| entry-03233 | 未发现问题 | 准确说明技能等级不足 |
| entry-03234 | 存在问题 | C05：完成时序提前；C06：取消选择也打印准备提示 |
| entry-03235 | 未发现问题 | 数量上限与确认时检查一致 |
| entry-03236 | 未发现问题 | 属性门槛、点数参数及25／42级获点与实现一致 |
| entry-03237 | 未发现问题 | 解锁选项名称参数正确 |
| entry-03238 | 未发现问题 | 检查已装备且允许附加的物品 |
| entry-03239 | 存在问题 | C07：选择生成方式被写成选择随机模式 |
| entry-03240 | 未发现问题 | 输入值作为目标升级等级 |
| entry-03241 | 未发现问题 | 名称及备份版本参数正确 |
| entry-03242 | 未发现问题 | 对应设置六项基础属性 |
| entry-03243 | 未发现问题 | 对应设置六项属性的额外加值 |
| entry-03244 | 存在问题 | C08：遗漏“available”的技能范围限制 |
| entry-03245 | 未发现问题 | 标识角色升级工具及其输入内容 |
| entry-03246 | 未发现问题 | 阵营名称作为操作对象填入 |
| entry-03247 | 未发现问题 | 文件路径及加载错误参数对应 |
| entry-03248 | 未发现问题 | 右键清除样品缓存并重新生成 |
| entry-03249 | 未发现问题 | 生成／鉴定处理失败，名称及错误参数对应 |
| entry-03250 | 未发现问题 | 错误详情及换行保留 |
| entry-03251 | 未发现问题 | 玩家标识的条件和颜色标记保留 |

### C01 | entry-03219 | 存在问题

原文：`cannot receive items while asleep!`  
译文：“不能在睡眠中接收物品！”

**状态：confirmed；沿袭上游误述。** 提示也会在接收者背包没有空间时出现，将拒收原因错误归为睡眠。

证据：`game/modules/tome/dialogs/PartySendItem.lua:53–55`，`use()` 将 `not item.actor:canAddToInven(...)` 与睡眠条件并列，任何一个成立均打印本条。该文件 `generateList():75–78` 仍将背包无空间的队员加入列表，并另标 `NO ROOM`，没有排除这一操作情形。此问题不是译文新增。

### C02 | entry-03222 | 仅建议

原文：`Keyboard: ... right key ... left key`  
译文：“键盘：……右键……左键……”

**状态：advisory。** “右键／左键”单独阅读容易联想到鼠标，但段首“键盘”已限定设备，下一段也明确标为“鼠标”；未丢失增减方向信息。因此只记录措辞清晰度偏好，不计为操作错误。

证据：`game/modules/tome/dialogs/SentientWeapon.lua:53–56` 保留键盘、鼠标两段结构；`74–79` 的鼠标消费逻辑为左键增加、其他点击减少，与译文鼠标段一致。此外，`80–89` 的当前布局并未加入该说明控件，不能据此声称已经造成可见界面操作误导。

### C03 | entry-03224 | 存在问题

原文：`Found as: %s`  
译文：“发现于：%s”

**状态：confirmed；翻译新增。** “发现于”将后面的内容表达为发现地点，实际填入的是手札名称，改变了字段的语义关系。

证据：`game/modules/tome/dialogs/ShowLore.lua:83–85` 从手札定义取得 `l.name`，保存为 `item.name`；`select():102` 依次传入 `item.cat, item.name, item.desc`。第二个参数不是地点字段。

### C04 | entry-03231 | 存在问题

原文：`need more skill`  
译文：“需要更多技能”

**状态：confirmed；翻译新增。** 此处要求提高掌握程度，译文却表达为需要更多项技能，误述了不足的条件。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:41` 用 `actor:getTalentLevelRaw(dialog_talent)` 设置 `mastery_level`；`formatItem():122–124` 仅在 `item.tier > self.mastery_level` 时显示本条。`use():142–143` 对同一条件给出相邻条目“你的技能等级不足”，也明确了语境。

### C05 | entry-03234 | 存在问题

原文：`Preparing trap with normal trigger.`  
译文：“准备了常规触发的陷阱。”

**状态：confirmed；翻译新增。** “准备了”把尚待确认的选择写成已经完成的准备，提前了生效时序。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:145–151` 打印提示后，只切换对话框中的 `traps_selected` 并刷新列表；`159–162` 才在确认时返回选择结果。实际修改发生在 `game/modules/tome/data/talents/cunning/traps.lua:603–621`：等待对话框返回后学习所选陷阱，并清除对应的 `trap_primed`。退出对话框的路径 `TrapsSelect.lua:79–81` 不执行这项确认。

### C06 | entry-03234 | 存在问题

原文：`Preparing trap with normal trigger.`  
译文：“准备了常规触发的陷阱。”

**状态：confirmed；沿袭上游误述。** 再次点击、取消该陷阱的常规准备选择时，仍会打印正在准备的提示，操作方向与信息不符。这与 C05 的完成时序问题独立。

证据：`game/modules/tome/dialogs/TrapsSelect.lua:145–148` 仅凭 `tid == self.actor.trap_primed` 打印本条，随后无条件取反 `self.traps_selected[tid]`。因此从已选切回未选时，同样打印该提示。英文原文已有此问题。

### C07 | entry-03239 | 存在问题

原文：`You can now choose how this set is selected:`  
译文：“现在你将选择随机模式：”

**状态：confirmed；翻译新增。** 原文让玩家选择技能树组合的生成方式，译文将其写成选择“随机模式”，缩窄了选项范围，并与本界面一个具体选项同名。

证据：`game/modules/tome/dialogs/WandererSeed.lua:46–50` 提供 `Random` 与 `Seed` 两个互斥选项；`swapMode():68–78` 分别处理两种模式；`154–165` 在种子模式下使用玩家输入的种子。冻结 `context.lua` 又明确将两个选项分别译作“随机模式”和“种子模式”，因此这里不是无损概括。

### C08 | entry-03244 | 存在问题

原文：`Unlock & Learn all available talents to level:`  
译文：“解锁并学习所有的技能到等级：”

**状态：confirmed；翻译新增。** 译文遗漏 `available`，将有范围限制的学习操作表述为学习所有技能。

证据：`game/modules/tome/dialogs/debug/AdvanceActor.lua:341–355` 只遍历角色已有的 `talents_types`，排除物品使用技能、刻印及觉醒技，并在未勾选忽略需求时调用 `canLearnTalent()`。`210–215` 另设解锁全部技能树选项，`334–339` 仅在该选项启用时扩展技能树集合。本条不能无条件承诺覆盖所有技能。

本次共判定：**存在问题 6 条、待确认 0 条、仅建议 1 条、未发现问题 33 条**。问题条目包含 7 个 confirmed claim。40 条占位符及颜色／样式标记序列均匹配；没有把合法空白、换行或段落调整计为缺陷。

实际读取范围与版本如下。令 `B` 为用户指定目录：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923`

冻结输入读取了 `B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。身份以 `entries.json` 为准，术语仅使用 INPUT 内快照。

以下十五份冻结源码均位于 `B/sources/` 下，完整字节哈希均与 `source-access.json` 相符；版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`：

- `game/modules/tome/dialogs/LevelupDialog.lua`
- `game/modules/tome/dialogs/PartySendItem.lua`
- `game/modules/tome/dialogs/QuestPopup.lua`
- `game/modules/tome/dialogs/SentientWeapon.lua`
- `game/modules/tome/dialogs/ShowIngredients.lua`
- `game/modules/tome/dialogs/ShowLore.lua`
- `game/modules/tome/dialogs/ShowStore.lua`
- `game/modules/tome/dialogs/TrapsSelect.lua`
- `game/modules/tome/dialogs/UberTalent.lua`
- `game/modules/tome/dialogs/UnlockDialog.lua`
- `game/modules/tome/dialogs/UseItemDialog.lua`
- `game/modules/tome/dialogs/WandererSeed.lua`
- `game/modules/tome/dialogs/debug/AdvanceActor.lua`
- `game/modules/tome/dialogs/debug/AlterFaction.lua`
- `game/modules/tome/dialogs/debug/CreateItem.lua`

额外源码均通过 `git -C /workspace/t-engine4 show` 读取同一固定 commit 的单文件：

| 路径 | 调用链／符号来源 |
|---|---|
| `game/modules/tome/class/Actor.lua` | `AdvanceActor.lua:321` 的 `who:forceLevelup()`，追踪角色升级及点数分配 |
| `game/engines/default/engine/interface/ActorLevel.lua` | `Actor.lua:28` 的显式 require；`forceLevelup()` 调用 `self:levelup()` |
| `game/engines/default/engine/interface/ActorTalents.lua` | `TrapsSelect.lua:25` 的显式 require |
| `game/modules/tome/data/talents/cunning/traps.lua` | `TrapsSelect.lua` 使用的 `trap_mastery_tids`、`trap_primed` 符号及准备结果消费 |
| `game/modules/tome/data/talents/uber/mag.lua` | `UberTalent.lua` 的 `uber/magic` 类型，追踪具体觉醒技需求 |
| `game/modules/tome/data/talents.lua` | `mag.lua` 调用的 `uberTalent` 定义追踪入口 |
| `game/modules/tome/data/talents/uber/uber.lua` | `data/talents.lua:311` 的显式 load；共同包装器写入各核心属性50点要求 |

定位期间还尝试读取同一 commit 下的 `game/modules/tome/data/talents/uber/magic.lua`、`game/modules/tome/data/talents/uber.lua`，两者均不存在，未取得内容；随后通过上述实际文件完成核验，没有据失败路径作出结论。

未留下待确认 claim；未越界读取其他报告、当前译文或当前源码工作树，未创建子 agent，未修改仓库，未创建临时文件。本输出仅为独立审核观察，不构成生产完成状态。
