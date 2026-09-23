40 条的源码对照和格式检查已完成，占位符顺序、颜色标记及换行数量均一致。另已核实一处英文日志把 Boss 转换失败写成“基础角色生成失败”；固定实现正常返回 Boss 对象，我会区分日志文本的错述与该失败分支的可达性。
---

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03252 | 未发现问题 | 物品、持有者、槽位及坐标参数对应正确 |
| entry-03253 | 未发现问题 | 队伍外对象、移除及归于玩家的击杀符合调用 |
| entry-03254 | 未发现问题 | 文件加载失败及异常信息完整 |
| entry-03255 | 存在问题 | C01：曲线图被称为属性表 |
| entry-03256 | 未发现问题 | TL对应生成图表所用技能等级 |
| entry-03257 | 未发现问题 | 文件与定义行号对应正确 |
| entry-03258 | 存在问题 | C02：遗漏预览操作的控件位置条件 |
| entry-03259 | 未发现问题 | 当前基础角色名称对应正确 |
| entry-03260 | 未发现问题 | 基础角色生成后的状态日志正确 |
| entry-03261 | 未发现问题 | 清除基础角色的动作及对象正确 |
| entry-03262 | 未发现问题 | 基础筛选器标签正确 |
| entry-03263 | 存在问题 | C03：自动补建基础角色被弱化为可选能力 |
| entry-03264 | 未发现问题 | 当前Boss角色名称对应正确 |
| entry-03265 | 未发现问题 | Boss数据标签正确 |
| entry-03266 | 未发现问题 | 筛选器解析或类型错误对应正确 |
| entry-03267 | 未发现问题 | 基础角色生成失败及筛选器对应正确 |
| entry-03268 | 存在问题 | C04：筛选器参数被贴到角色名称位置 |
| entry-03269 | 未发现问题 | Boss数据解析或类型错误对应正确 |
| entry-03270 | 存在问题 | C05：沿袭上游的失败对象误述 |
| entry-03271 | 存在问题 | C06：定义行号误称行数 |
| entry-03272 | 存在问题 | C07：遗漏F1帮助随当前控件变化的信息 |
| entry-03273 | 未发现问题 | 随机筛选器的基本用途对应正确 |
| entry-03274 | 未发现问题 | 随机筛选器标签正确 |
| entry-03275 | 未发现问题 | 基础筛选器标签正确 |
| entry-03276 | 未发现问题 | 解析器选择标签正确 |
| entry-03277 | 未发现问题 | 随机神器数据标签正确 |
| entry-03278 | 未发现问题 | 工作角色UID及名称对应正确 |
| entry-03279 | 未发现问题 | UID、名称及玩家附注对应正确 |
| entry-03280 | 未发现问题 | 玩家身份附注正确 |
| entry-03281 | 未发现问题 | 参数为所用解析器名称 |
| entry-03282 | 未发现问题 | 解析器附注与物品名称的拼接关系保留 |
| entry-03283 | 未发现问题 | 解析器附注内容正确 |
| entry-03284 | 未发现问题 | 随机物品生成失败及筛选器对应正确 |
| entry-03285 | 存在问题 | C08：筛选器参数被贴到错误信息位置 |
| entry-03286 | 未发现问题 | 基础物品生成失败及筛选器对应正确 |
| entry-03287 | 存在问题 | C09：筛选器参数被贴到错误信息位置 |
| entry-03288 | 未发现问题 | 随机神器生成失败及输入数据对应正确 |
| entry-03289 | 未发现问题 | 解析器接收物品失败及异常参数对应正确 |
| entry-03290 | 未发现问题 | 工作角色身份、坐标及设置动作正确 |
| entry-03291 | 未发现问题 | 无待放置角色的提前返回提示正确 |

共40条：存在问题9条，未发现问题31条；无单列待确认或仅建议条目。以下均为审核观察。

### C01 | entry-03255 | 存在问题

原文短引：`Values plot for`；译文短引：“技能数值属性表”。

**状态：confirmed；翻译新增。** 原文指技能数值随等级变化的绘图，译文将显示形式说成属性表，丢失了曲线图这一具体含义。

证据：`game/modules/tome/dialogs/debug/PlotTalent.lua:32` 将该字符串作为窗口标题；`generatePlot` 第94–100行逐等级计算技能数值，第114–137行计算坐标、连接相邻数值点并绘制标注。实际呈现不是属性列表。`mastery` 参数及其译文未发现问题。

### C02 | entry-03258 | 存在问题

原文短引：`Mouse over controls for an actor preview`；译文短引：“鼠标移动查看角色预览”。

**状态：confirmed；翻译新增遗漏。** 译文没有说明鼠标需要移到控件上，把有明确目标位置的悬停操作变成泛指鼠标移动。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:94` 为基础角色文本控件设置预览回调；第177行为Boss角色控件设置对应回调；`newButton` 第284–286行根据当前按钮的 `_actor_field` 显示对应角色。预览与具体控件关联，不由任意鼠标移动触发。

### C03 | entry-03263 | 存在问题

原文短引：`will use a random actor if needed`；译文短引：“如果需要的话，也可以用随机角色作为基础”。

**状态：confirmed；翻译新增。** 原文说明生成器在需要时会采用随机基础角色，译文仅表达“可以使用”的能力，遗漏了缺少基础角色时自动补建的行为。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:353` 的 `generateBoss` 在第354–358行读取基础角色；若不存在，直接调用 `game.zone:makeEntity(game.level, "actor")`。该步骤无需用户另行选择或先生成基础角色。

### C04 | entry-03268 | 存在问题

原文短引：`with filter [%s]`；译文短引：“生成基础角色[%s]”。

**状态：confirmed；翻译新增。** 方括号参数原本明确属于筛选器，译文把它紧接在“基础角色”之后，形成角色标识的表达。“以下筛选器”也没有与其参数明确连接，改变了诊断信息的所属关系。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:347` 实际传入 `_M._base_filter, m`：第一个参数是筛选器输入，第二个才是异常信息。这里不是占位符数量或顺序错误，而是参数标签归属错误。

### C05 | entry-03270 | 存在问题

原文短引：`Could not generate a base actor with data`；译文短引：“无法使用以下数据生成基础角色”。

**状态：confirmed；沿袭上游描述。** 该日志所在分支描述的是已有基础角色之后的Boss转换结果，却将失败对象称为基础角色。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:360` 已进入 `if base then`；第374行调用 `game.state.createRandomBoss`，第383行在调用成功但没有返回对象时输出本日志，并传入 `_M._boss_data`。因此日志对应Boss转换阶段，不是基础角色生成阶段。

可达性限制：固定版本 `game/modules/tome/class/GameState.lua:2368` 的 `createRandomBoss` 克隆并加工基础角色，在第2536行正常返回 `b, boss_id`。本观察确认的是这条防御性日志的对象误述，**不据此声称常规运行能够触发该日志**。

### C06 | entry-03271 | 存在问题

原文短引：`line: %s`；译文短引：“行数：%s”。

**状态：confirmed；翻译新增。** 参数表示函数定义所在的源码行号，不是文件或函数的行数，译文改变了数值含义。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:44` 的 `formatHelp` 将 `f_lnum` 填入第二个参数；第54–55行从 `DebugConsole:functionHelp` 获取该值。`game/engines/default/engine/DebugConsole.lua:495` 返回的是 `info.linedefined`，即定义位置。

### C07 | entry-03272 | 存在问题

原文短引：`F1 :: context sensitive help`；译文短引：“F1 :: 查看帮助”。

**状态：confirmed；翻译新增遗漏。** 译文保留了帮助快捷键，但删除了帮助内容随当前控件或选择变化的信息。这会影响用户取得筛选器、神器数据或具体解析器说明的操作。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:475` 将F1绑定到 `help`；第509–512行根据 `_M.help_display` 选择内容；第339–347行随解析器选择更新帮助目标，第519–520行随文本框焦点更新目标。该差异涉及功能信息，不只是措辞简化。

### C08 | entry-03285 | 存在问题

原文短引：`with filter [%s]`；译文短引：“发生错误[%s]”。

**状态：confirmed；翻译新增。** 第一个参数是筛选器文本，译文却将其附在“错误”之后，使之看似错误编号或错误内容；下一行才是真正的异常信息。两类诊断数据的标签关系被混淆。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:605` 传入 `_M._random_filter, o`，其中 `o` 是受保护调用失败后取得的异常值。占位符顺序保持一致并不能消除这项语义错位。

### C09 | entry-03287 | 存在问题

原文短引：`with filter [%s]`；译文短引：“发生错误 [%s]”。

**状态：confirmed；翻译新增。** 与上一条独立发生：基础物品的筛选器输入被放到“错误”之后，失去原文明确的筛选器参数归属。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:625` 传入 `_M._base_filter, o`。第一项是基础筛选器，第二项是异常信息，不是两个错误字段。

实际读取范围与限制：

冻结包根路径为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/`

读取了该根路径下的全部以下文件：

- `INPUT.md`（统一复核规则v3）
- `entries.json`
- `context.lua`
- `source-access.json`
- `sources/game/modules/tome/dialogs/debug/CreateItem.lua`
- `sources/game/modules/tome/dialogs/debug/DebugMain.lua`
- `sources/game/modules/tome/dialogs/debug/Endgamify.lua`
- `sources/game/modules/tome/dialogs/debug/PlotTalent.lua`
- `sources/game/modules/tome/dialogs/debug/RandomActor.lua`
- `sources/game/modules/tome/dialogs/debug/RandomObject.lua`
- `sources/game/modules/tome/dialogs/debug/SummonCreature.lua`

七份冻结源码的SHA-256均与 `source-access.json` 一致，对应固定版本 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

额外仅通过 `/workspace/t-engine4` 的 `git show` 读取同一固定版本的三个单文件：

- `game/engines/default/engine/DebugConsole.lua`：由两份随机生成对话框中的 `require "engine.DebugConsole"` 和 `functionHelp` 调用引入，核验源码行号。
- `game/modules/tome/class/GameState.lua`：由 `RandomActor.lua` 的 `game.state.createRandomBoss` 调用引入，核验Boss转换及返回值。
- `game/modules/tome/class/Actor.lua`：由 `DebugMain.lua` 的角色 `die(game.player, ...)` 调用引入，核验经验结算与物品掉落逻辑。

40条的占位符序列、颜色标记序列及换行数量均一致；上述参数归属问题属于语义问题。未运行游戏进行显示复现，未将日志分支存在等同于实际可触发。

未越界读取，未读取其他报告或当前译文、当前源码工作树；未创建临时文件、子agent或修改仓库。本次交付仅为独立审核观察，不作生产完成认证。
