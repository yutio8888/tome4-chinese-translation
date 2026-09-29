独立裁决结果：**7条 ISSUE、33条 OK，归并为8个确认缺陷；无剩余 PENDING。** 已检查全部40条，包括没有观察或观察被否决的条目，未追加新的确认缺陷。

以下源码版本均为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。表中 `dialogs/`、`class/`、`data/` 分别相对于 `game/modules/tome/`；`engine/` 相对于 `game/engines/default/`。

| entry-ID | 判定 | canonical D或简短依据 |
|---|---|---|
| entry-03212 | OK | 属性收益标题；`LevelupDialog.lua:879`，语义对应。 |
| entry-03213 | OK | 物理豁免名称准确；`:883,907`，冒号后省略空格不影响显示。 |
| entry-03214 | OK | 精神豁免名称准确；`:899,910`。 |
| entry-03215 | OK | 法术豁免名称准确；`:900`。 |
| entry-03216 | ISSUE | D01；“熟练度”等措辞差异仅建议。 |
| entry-03217 | OK | “X键”指物理按键，不要求输入大写字符；`:111–115,1019`。 |
| entry-03218 | OK | 同上；进阶显示方向正确，`:1052`。 |
| entry-03219 | ISSUE | D02。 |
| entry-03220 | OK | 新任务状态、颜色标记准确；词间空格仅排版建议。 |
| entry-03221 | OK | 点击调用 `ShowQuests`；`QuestPopup.lua:88–91`，“任务面板”符合用途。 |
| entry-03222 | OK | 键盘、鼠标分段已消除设备歧义；仅措辞建议。 |
| entry-03223 | OK | 四个参数依次为分类、材料、数量、描述；`ShowIngredients.lua:75`。 |
| entry-03224 | ISSUE | D03。 |
| entry-03225 | OK | 商店付款上限、玩家金币参数顺序正确；`ShowStore.lua:173`。 |
| entry-03226 | OK | 已选中原瞬发陷阱，表示替换其触发准备方式；`TrapsSelect.lua:102–105`。 |
| entry-03227 | OK | 列表中表示瞬发准备状态；“即爆”仅保留措辞建议。 |
| entry-03228 | OK | 当前选中且原已准备，符合“准备完毕”；`:110–113`。 |
| entry-03229 | OK | 新选中、尚待确认，符合“准备中”；`:114–116`。 |
| entry-03230 | OK | 已准备陷阱被取消选择；“分解中”未必指地图拆除，仅措辞建议。 |
| entry-03231 | ISSUE | D04。 |
| entry-03232 | OK | `%s` 消费实际不可学习原因；`:140–141,168–170`。 |
| entry-03233 | OK | 同一阶数检查确实要求提高技能等级；`:142–143`。 |
| entry-03234 | ISSUE | D05、D06，分别为完成时序与取消方向错误。 |
| entry-03235 | OK | 确认时检查数量上限，参数为 `max_traps`；`:159–164`。 |
| entry-03236 | OK | 已补查注册入口及54个 `uberTalent` 定义，50属性要求成立；25、42级点数亦成立。 |
| entry-03237 | OK | 解锁名称用于标题；`UnlockDialog.lua:29–36`。 |
| entry-03238 | OK | 仅遍历已装备且可附加的物品，空列表触发提示；`UseItemDialog.lua:102–121`。 |
| entry-03239 | ISSUE | D07。 |
| entry-03240 | OK | 角色目标等级输入；`debug/AdvanceActor.lua:61–69,319–322`。 |
| entry-03241 | OK | 参数分别为备份角色名和版本序号；`:73–89`。 |
| entry-03242 | OK | 设置六项基础属性，区别于额外属性；`:325–330`。 |
| entry-03243 | OK | 设置总属性与基础属性之差；`:368–373`。 |
| entry-03244 | ISSUE | D08。 |
| entry-03245 | OK | 输入参数日志含义准确；`:263–270`，措辞仅建议。 |
| entry-03246 | OK | 修改指定阵营的关系状态；`debug/AlterFaction.lua:66–70`。 |
| entry-03247 | OK | 文件路径、加载错误参数对应；`debug/CreateItem.lua:48–54`。 |
| entry-03248 | OK | 勾选生成样品，右键清除缓存并重新生成；`:116–124,175–180,198–219`。 |
| entry-03249 | OK | 物品名称及生成／鉴定过程错误信息对应；`:203–216`。 |
| entry-03250 | OK | 错误详情参数与换行保留；`:216`。 |
| entry-03251 | OK | `actor.player` 条件添加玩家标记；`:257,263`。 |

“翻译新增”以下均指**相对于英文产生的偏差**，不表示本次最近修改才引入。

| D-ID | entry-ID | 内容、归因及固定源码证据 |
|---|---|---|
| D01 | entry-03216 | **沿袭上游的奖励范围遗漏。** 类别点发放说明只列10、20、34级，遗漏适用角色超过50级后的64、94……级。`class/Actor.lua:3949–3962`：正常发点分支还执行 `level > 50 and (level - 4) % 30 == 0`。`dialogs/LevelupDialog.lua:964` 的通用类别提示没有说明该范围限制。此结论仅涉及可继续升至这些等级的情况。 |
| D02 | entry-03219 | **沿袭上游的失败原因误报。** 清醒但背包无空间的接收者也会得到“睡眠中”日志。`dialogs/PartySendItem.lua:53–55` 将无空间与睡眠并入同一失败分支；`:74–78` 仍把无空间成员加入可选列表，只附加 `NO ROOM` 标记。 |
| D03 | entry-03224 | **翻译新增的字段关系错误。** `Found as` 译成“发现于”，把手札名称表达成发现地点／时间。`dialogs/ShowLore.lua:83–85` 保存 `name=l.name`；`:102` 的第二个参数为 `item.name`，不是发现位置。 |
| D04 | entry-03231 | **翻译新增的条件维度错误。** “需要更多技能”指向技能数量，实际不足的是精通技能原始等级。`dialogs/TrapsSelect.lua:41` 设置 `mastery_level=getTalentLevelRaw(dialog_talent)`；`:122–124` 比较 `item.tier > mastery_level`；`:142–143` 同条件输出技能等级不足提示。 |
| D05 | entry-03234 | **翻译新增的完成时序错误。** `Preparing` 译成“准备了”，将待确认的准备说成已完成。`dialogs/TrapsSelect.lua:145–151` 此时只更新临时选择；`:159–162` 才返回确认结果。`data/talents/cunning/traps.lua:603–621` 收到结果后才学习陷阱并清除原瞬发状态。退出路径 `TrapsSelect.lua:79–81` 不提交选择；`engine/interface/ActorTalents.lua:1248–1278` 支持这一返回逻辑。 |
| D06 | entry-03234 | **沿袭上游的操作方向错误。** 再次点击取消常规准备时仍报告正在／已经准备。`dialogs/TrapsSelect.lua:145–148` 只检查是否原瞬发陷阱，先打印日志，再无条件翻转选择；`:102–108` 可核对取消后恢复显示瞬发状态。因此与D05独立。 |
| D07 | entry-03239 | **翻译新增的选项范围偏移。** “现在你将选择随机模式”把选择生成方式写成选择具体的“随机模式”。`dialogs/WandererSeed.lua:46–50,68–78` 提供随机与种子两种互斥方式，`:154–165` 实际消费输入种子；`context.lua` 中两项标签分别为“随机模式”“种子模式”。 |
| D08 | entry-03244 | **翻译新增的范围限定遗漏，限调试界面。** `all available talents` 译成“所有的技能”，遗漏可用范围。`dialogs/debug/AdvanceActor.lua:341–355` 只遍历角色现有 `talents_types`，排除物品使用、刻印和觉醒技，通常还检查学习需求；`:210–215,334–339` 另有独立的全部技能树解锁选项。 |

| O-ID | 状态 | 命中D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | advisory | — | `LevelupDialog.lua:448–457` 支持解锁或增加0.2精通度；术语子集没有强制指定这两个译法。仅一致性建议，不覆盖D01。 |
| O002 | confirmed | D01 | `Actor.lua:3959–3962` 确认64、94……级的额外类别点；限定为可超过50级的角色。 |
| O003 | advisory | — | `LevelupDialog.lua:111–115` 匹配小写 `x`；中文“X键”并不要求大写输入。 |
| O004 | advisory | — | 同O003；`:1052` 确认切换到进阶显示。 |
| O005 | confirmed | D02 | `PartySendItem.lua:53–55,74–78` 同时证明错误分支和可选择性。 |
| O006 | confirmed | D02 | 无空间条件独立成立即可输出睡眠日志；不是翻译新增。 |
| O007 | confirmed | D02 | 列表能标注无空间，执行时却仍统一打印睡眠原因。 |
| O008 | mixed | D02 | **confirmed：** 两种失败原因共用睡眠日志。**refuted：** “单改一条译文无法兼容两个分支”的绝对断言；现有证据只能证明无法准确区分原因，不能证明不存在共同适用的表述。 |
| O009 | advisory | — | `QuestPopup.lua:30,70` 保留新任务语义及颜色层次；空格无损。 |
| O010 | advisory | — | `SentientWeapon.lua:53–56` 明确分设备；`:75,187–188` 操作方向对应。`:80–89` 未装入说明控件。 |
| O011 | mixed | — | **advisory：** 方向键名称可更明确。**refuted：** 将其描述成当前界面顶部的实际显示；`:88` 的控件布局已注释，不能仅凭旧 `drawDialog` 定义确定可见。 |
| O012 | mixed | — | **refuted：** 完整“键盘／鼠标”分段并无左右键直接矛盾，也未丢失方向信息。**advisory：** 措辞清晰度。可达性附注的谨慎态度合理，但不能据此确立文字缺陷或可见误导。 |
| O013 | confirmed | D03 | `ShowLore.lua:85,102` 第二参数确为手札名称。 |
| O014 | confirmed | D03 | “发现于”改变字段和值之间的关系。 |
| O015 | confirmed | D03 | 与O013、O014同义归并，不另建缺陷。 |
| O016 | advisory | — | `ShowStore.lua:40–41,173` 提供商店标题语境，付款上限与玩家金币参数正确。未据此扩张到其他交易规则。 |
| O017 | advisory | — | 非爆炸陷阱确实支持瞬发：`traps.lua:952,964–980` 的捕兽夹直接触发伤害和束缚。但该列表后缀标示触发方式，并未声明“仅爆炸陷阱适用”或改变伤害类型；“即爆”的用词建议不升级为排他机制错误。 |
| O018 | refuted | — | `TrapsSelect.lua:119–121` 位于准备列表；`traps.lua:607–610` 撤销已准备陷阱。英文与中文都可用拆解表述撤销准备，没有“地图上陷阱”这一对象断言。不能仅凭 `unlearnTalentFull` 判定叙事动作错误。 |
| O019 | advisory | — | “分解中”与准备列表语境相容，未承诺获得材料或拆除地图实体；仅措辞建议。 |
| O020 | confirmed | D04 | `TrapsSelect.lua:41,122–124` 明确比较原始等级与阶数，非技能数量。确认不依赖“永远只有1–5级”的额外假设。 |
| O021 | confirmed | D04 | 同一条件在`:142–143` 的失败日志进一步支持等级解释。 |
| O022 | confirmed | D04 | 原始等级与技能数量的维度偏差成立。 |
| O023 | confirmed | D04 | 同O020–O022；相邻译文用于语境佐证，最终依据仍为条件表达式。 |
| O024 | confirmed | D05 | 临时选择、确认返回和实际学习三阶段已沿调用链核实。 |
| O025 | confirmed | D06 | `TrapsSelect.lua:145–148` 未区分选中与取消方向。 |
| O026 | confirmed | D06 | 取消也打印准备日志，与D05分别归并。 |
| O027 | confirmed | D05 | EXIT不提交；`traps.lua:606` 无返回选择时不应用准备变化。 |
| O028 | confirmed | D06 | 取消后`:106–108` 显示原瞬发状态，日志却仍称常规准备。 |
| O029 | refuted | — | **本轮解除未决，未认定原观察误报。** `uber/uber.lua:38–108` 六个包装函数统一写入对应属性50；六个加载文件共54个 `uberTalent` 定义，包含已核对的进阶技。`ActorTalents.lua:750–754` 实际检查这些属性。 |
| O030 | confirmed | D07 | 两种互斥方式及种子实际消费均已核验，译文与一个具体选项同名。 |
| O031 | confirmed | D07 | 与O030归并为选择范围／引导语偏移；不把 `can→将` 单独重复计缺陷。 |
| O032 | confirmed | D08 | `AdvanceActor.lua:341–355` 的类别范围、排除项与需求检查支持 `available` 的实质限定。 |
| O033 | confirmed | D08 | 全部技能树解锁是独立选项；“所有的技能”遗漏当前操作限制。 |
| O034 | confirmed | D08 | 同O032、O033；明确影响调试界面。 |
| O035 | advisory | — | `AdvanceActor.lua:263–270` 打印输入键值；生硬空格未改变日志含义。 |
| O036 | advisory | — | `CreateItem.lua:175–180,198–219` 支持右键刷新和生成示例；“样品”未错误承诺立即放入背包。 |

主要分歧按以下边界处理：

- **键盘左右键、即爆、分解中**均结合完整界面语境判断，不把单个词自动解释成排他的设备、伤害机制或地图对象断言。这不是因为玩家“猜得出”，而是现有语境本身已限定其作用。
- **“准备了”与取消日志**分别改变完成时序和操作方向，故保留D05、D06两个缺陷。
- **觉醒技要求**已查到实际注册与消费链。Lich、High Thaumaturgist 的额外意志25要求，以及两项太阳骑士进阶的额外魔力25要求，均不替代包装函数加入的核心属性50要求。没有剩余P-ID。
- **SentientWeapon显示范围**：已确认 `c_tut` 未进入当前 `loadUI`，固定版本 `engine/ui/Dialog.lua` 没有 `drawDialog` 引用；未进行运行时界面测试，也不宣称证明所有外部调用均不可达。文字本身的操作矛盾断言已能独立否决，因此没有遗留译文缺陷待确认。

实际读取范围如下。令 `B` 为[本次冻结输入目录](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923)：

```text
B/ADJUDICATION-INPUT.md
B/INPUT.md
B/entries.json
B/context.lua
B/source-access.json

B/sources/game/modules/tome/dialogs/LevelupDialog.lua
B/sources/game/modules/tome/dialogs/PartySendItem.lua
B/sources/game/modules/tome/dialogs/QuestPopup.lua
B/sources/game/modules/tome/dialogs/SentientWeapon.lua
B/sources/game/modules/tome/dialogs/ShowIngredients.lua
B/sources/game/modules/tome/dialogs/ShowLore.lua
B/sources/game/modules/tome/dialogs/ShowStore.lua
B/sources/game/modules/tome/dialogs/TrapsSelect.lua
B/sources/game/modules/tome/dialogs/UberTalent.lua
B/sources/game/modules/tome/dialogs/UnlockDialog.lua
B/sources/game/modules/tome/dialogs/UseItemDialog.lua
B/sources/game/modules/tome/dialogs/WandererSeed.lua
B/sources/game/modules/tome/dialogs/debug/AdvanceActor.lua
B/sources/game/modules/tome/dialogs/debug/AlterFaction.lua
B/sources/game/modules/tome/dialogs/debug/CreateItem.lua
```

15份冻结源码的SHA-256全部匹配清单。额外源码均通过指定仓库的固定提交单文件 `git show` 获取：

- `game/modules/tome/class/Actor.lua`：由升级点数及 `actor:canLearnTalent` 调用引入。
- `game/engines/default/engine/interface/ActorTalents.lua`：由 `TrapsSelect` 的显式require、Actor继承及 `talentDialogReturn` 引入。
- `game/engines/default/engine/ui/Dialog.lua`：由 `SentientWeapon` 显式require及显示可达性争议引入。
- `game/modules/tome/data/talents/cunning/traps.lua`：追踪 `trap_mastery_tids`、`trap_primed` 的定义及准备对话框调用者。
- `game/modules/tome/data/talents.lua`：追踪 `talents_def` 的模块注册入口。
- `game/modules/tome/data/talents/uber/uber.lua`：由 `talents.lua:311` 的显式load引入。
- `game/modules/tome/data/talents/uber/str.lua`
- `game/modules/tome/data/talents/uber/dex.lua`
- `game/modules/tome/data/talents/uber/const.lua`
- `game/modules/tome/data/talents/uber/mag.lua`
- `game/modules/tome/data/talents/uber/wil.lua`
- `game/modules/tome/data/talents/uber/cun.lua`

最后六份分别来自 `uber/uber.lua:48,60,72,84,96,108` 的显式load。另曾尝试相关单文件路径 `game/modules/tome/data/talents/uber.lua`，该提交不存在此路径，未读取到内容。

临时源码保存在自行创建的 [/tmp/abc40-b096-adjudication-n4brndhv](/tmp/abc40-b096-adjudication-n4brndhv)。仓库未写入；未读取映射、原报告、STATE或其他实验，未创建子agent，未扫描源码目录。
