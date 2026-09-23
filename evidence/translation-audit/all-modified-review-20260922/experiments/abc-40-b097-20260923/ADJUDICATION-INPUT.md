# 匿名源码核验与归并：40 条 / 34 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方34项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好34行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03255

### C01 | entry-03255 | 存在问题

原文“Values plot”指技能数值曲线图，译文“技能数值属性表”将显示形式说成表格。`game/modules/tome/dialogs/debug/PlotTalent.lua:114–139`逐级计算坐标并绘制连线，`:149–159`将图形显示到屏幕。状态：已证实，译文新增误述。



## O002 | entry-03255

### C01 | entry-03255 | 存在问题

原文短引：`Values plot for`；译文短引：“技能数值属性表”。

**状态：confirmed；翻译新增。** 原文指技能数值随等级变化的绘图，译文将显示形式说成属性表，丢失了曲线图这一具体含义。

证据：`game/modules/tome/dialogs/debug/PlotTalent.lua:32` 将该字符串作为窗口标题；`generatePlot` 第94–100行逐等级计算技能数值，第114–137行计算坐标、连接相邻数值点并绘制标注。实际呈现不是属性列表。`mastery` 参数及其译文未发现问题。



## O003 | entry-03255

### C01 | entry-03255 | 存在问题
- 原文 `Values plot for: %s (mastery %0.1f)`，译文 `技能数值属性表：%s (技能树系数 %0.1f)`。
- 问题：把“plot（曲线图）”译成了“属性表”。
  - 对话框画的是折线图：PlotTalent.lua:46-143 `generatePlot` 用 `vo:addQuad` 连线。
  - 画的量是技能函数值，不是属性：:78-84 只收集 `radius`、`range` 和 `^get[A-Z]` 函数的数值。
  - 译文既把展示形式说错了，又凭空加了“属性”这个对象。
- “技能树系数”没有问题：`getTalentMastery` 取的是技能类别 mastery 再加加成。依据是 engine/interface/ActorTalents.lua:941-944，以及 tome/class/Actor.lua:5091-5097。
- 属翻译新增的问题，影响限于调试界面。



## O004 | entry-03258

### C01 | entry-03258 | 仅建议
- **原文短引**：`The #LIGHT_BLUE#Base Filter#LAST# is used to filter the actor randomly generated.`
- **译文短引**：`#LIGHT_BLUE#基础过滤器#LAST#用于过滤生成的随机角色。`
- **问题具体内容**：在该说明文本前文第 1、2 行中均使用了“筛选器”（`根据给定的筛选器`、`筛选器由game.zone:checkFilter处理`），且同对话框内对应的 UI 控件标题（[entry-03262](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/sources/game/modules/tome/dialogs/debug/RandomActor.lua#L141)）译为“#LIGHT_BLUE#基础筛选器：#LAST#”。末句将“Base Filter”译为“基础过滤器”存在同义词用词不完全一致的情况。
- **状态**：仅建议。
- **依据与消费逻辑**：源码 [sources/game/modules/tome/dialogs/debug/RandomActor.lua:66-74](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/sources/game/modules/tome/dialogs/debug/RandomActor.lua#L66-L74)。“过滤器”与“筛选器”在此处并不引发机制或语义误解，仅属用词偏好与上下文统一性建议。

---



## O005 | entry-03258

### C02 | entry-03258 | 存在问题

原文“Mouse over controls for an actor preview”指定将鼠标悬停在**控件上**；译文“鼠标移动查看角色预览”遗漏操作目标。`game/modules/tome/dialogs/debug/RandomActor.lua:65–75`是该界面说明，`:279–287`的控件选中逻辑显示角色预览。状态：已证实，译文遗漏操作信息。



## O006 | entry-03258

### C02 | entry-03258 | 存在问题

原文短引：`Mouse over controls for an actor preview`；译文短引：“鼠标移动查看角色预览”。

**状态：confirmed；翻译新增遗漏。** 译文没有说明鼠标需要移到控件上，把有明确目标位置的悬停操作变成泛指鼠标移动。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:94` 为基础角色文本控件设置预览回调；第177行为Boss角色控件设置对应回调；`newButton` 第284–286行根据当前按钮的 `_actor_field` 显示对应角色。预览与具体控件关联，不由任意鼠标移动触发。



## O007 | entry-03258

### C02 | entry-03258 | 存在问题
- 原文 `Mouse over controls for an actor preview`，译文 `鼠标移动查看角色预览`。
- 问题：漏掉了“over controls（悬停在控件上）”这个操作对象，读起来像随便移动鼠标都会出现预览。
- 源码依据：预览只在控件获得焦点或被选中时触发。
  - RandomActor.lua:284-287 `newButton.on_select` 调用 `_M.tooltip`。
  - :94、:177 在 Textzone 的 `on_focus` 里触发。
- 这是对玩家操作描述的缺失。同类句子在 entry-03272 里译成了“将鼠标悬停在控件上”，可作对照。



## O008 | entry-03258

### C03 | entry-03258 | 仅建议
- 末句 `#LIGHT_BLUE#基础过滤器#LAST#` 用了“过滤器”，但实际输入框标签是“基础筛选器：”（entry-03262，RandomActor.lua:141），同一段前两行也用“筛选器”。
- 两词同义，颜色标记也一致，玩家仍能对应到控件，没有信息丢失，只算一致性偏好。



## O009 | entry-03263

### C03 | entry-03263 | 存在问题

原文短引：`will use a random actor if needed`；译文短引：“如果需要的话，也可以用随机角色作为基础”。

**状态：confirmed；翻译新增。** 原文说明生成器在需要时会采用随机基础角色，译文仅表达“可以使用”的能力，遗漏了缺少基础角色时自动补建的行为。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:353` 的 `generateBoss` 在第354–358行读取基础角色；若不存在，直接调用 `game.zone:makeEntity(game.level, "actor")`。该步骤无需用户另行选择或先生成基础角色。



## O010 | entry-03263

### C03 | entry-03263 | 存在问题

原文说必要时“will use a random actor”，译文“也可以用随机角色作为基础”只表达可能性。`game/modules/tome/dialogs/debug/RandomActor.lua:353–358`显示没有基础角色时程序直接随机生成一个，再于`:374`生成 Boss。状态：已证实，译文弱化了自动回退条件。



## O011 | entry-03263

### C04 | entry-03263 | 仅建议
- 原文 `(which will use a random actor if needed)`，译文 `（如果需要的话，也可以用随机角色作为基础）`。
- 源码中这是自动回退：没有基础角色时，由 RandomActor.lua:355-358 自动随机生成。
- “也可以”略带“可选”的意味，但“如果需要的话”保留了条件，也没有说错行为，所以只作措辞建议。



## O012 | entry-03263

### C05 | entry-03263 | 仅建议
- `Boss 数据` 带空格、`boss` 小写，与同文件“Boss数据”（entry-03265）写法不统一。属于无损排版问题。



## O013 | entry-03268

### C04 | entry-03268 | 存在问题

原文短引：`with filter [%s]`；译文短引：“生成基础角色[%s]”。

**状态：confirmed；翻译新增。** 方括号参数原本明确属于筛选器，译文把它紧接在“基础角色”之后，形成角色标识的表达。“以下筛选器”也没有与其参数明确连接，改变了诊断信息的所属关系。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:347` 实际传入 `_M._base_filter, m`：第一个参数是筛选器输入，第二个才是异常信息。这里不是占位符数量或顺序错误，而是参数标签归属错误。



## O014 | entry-03268

### C06 | entry-03268 | 仅建议
- 译文 `无法使用以下筛选器生成基础角色[%s]。`：筛选器内容 `[%s]` 紧跟在“基础角色”后面。
- 但前面有“以下筛选器”指向它，归属仍可辨认，只是语序建议。



## O015 | entry-03270

### C02 | entry-03270 | 存在问题
- **原文短引**：`#LIGHT_BLUE#Could not generate a base actor with data: %s`
- **译文短引**：`#LIGHT_BLUE#无法使用以下数据生成基础角色：%s`
- **问题具体内容**：机制描述错误（沿袭上游描述）。当前上下文处于生成随机 Boss 的逻辑中，`createRandomBoss` 失败时未生成的对象是 Boss 角色而非基础角色（基础角色已在前置逻辑中生成或获取）。上游源码此处存在笔误复制，将本应提示的 Boss 误写为了“base actor”，译文忠实直译为“基础角色”，导致面向使用者的提示对象发生错误。
- **状态**：存在问题（属于沿袭上游描述的机制描述缺陷）。
- **源码路径与消费逻辑**：源码 [sources/game/modules/tome/dialogs/debug/RandomActor.lua:374-384](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/sources/game/modules/tome/dialogs/debug/RandomActor.lua#L374-L384)（函数 `_M:generateBoss()`）：
  ```lua
  local m
  ok, m = pcall(game.state.createRandomBoss, game.state, base, data)
  if ok then
      if m then
          ...
      else
          game.log("#LIGHT_BLUE#Could not generate a base actor with data: %s", _M._boss_data)
      end
  ```
  该分支是利用传入的 `base` 和 `data` 生成 Boss；若 `createRandomBoss` 返回 nil，失败的是 Boss 的生成，上游英文将其错写为 base actor，译文忠实复制了该机制错误。

---



## O016 | entry-03270

### C04 | entry-03270 | 存在问题

原文“generate a base actor with data”和译文“生成基础角色”均误指失败对象。`game/modules/tome/dialogs/debug/RandomActor.lua:353–358`先取得基础角色，`:374–383`随后用 Boss 数据生成随机 Boss；此处失败的是后一步。状态：已证实；这是**沿袭上游英文日志**的机制误述，非翻译新增。



## O017 | entry-03270

### C05 | entry-03270 | 存在问题

原文短引：`Could not generate a base actor with data`；译文短引：“无法使用以下数据生成基础角色”。

**状态：confirmed；沿袭上游描述。** 该日志所在分支描述的是已有基础角色之后的Boss转换结果，却将失败对象称为基础角色。

证据：`game/modules/tome/dialogs/debug/RandomActor.lua:360` 已进入 `if base then`；第374行调用 `game.state.createRandomBoss`，第383行在调用成功但没有返回对象时输出本日志，并传入 `_M._boss_data`。因此日志对应Boss转换阶段，不是基础角色生成阶段。

可达性限制：固定版本 `game/modules/tome/class/GameState.lua:2368` 的 `createRandomBoss` 克隆并加工基础角色，在第2536行正常返回 `b, boss_id`。本观察确认的是这条防御性日志的对象误述，**不据此声称常规运行能够触发该日志**。



## O018 | entry-03271

### C03 | entry-03271 | 存在问题
- **原文短引**：`#LIGHT_GREEN#(From %-10.60s, line: %s):#LAST#`
- **译文短引**：`#LIGHT_GREEN#(来自 %-10.60s, 行数：%s):#LAST#`
- **问题具体内容**：语义与事实错误。此处 `line: %s` 消费的参数是函数在定义文件中的起始行号（line number），而非代码文件的总行数或代码行数（line count）。译文将其译为“行数：%s”，使面向调试者的位置定位语义变为数量统计，导致语义信息发生偏差。
- **状态**：存在问题。
- **源码路径与消费逻辑**：源码 [sources/game/modules/tome/dialogs/debug/RandomObject.lua:44-51](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/sources/game/modules/tome/dialogs/debug/RandomObject.lua#L44-L51)：
  ```lua
  local function formatHelp(f_lines, f_name, f_lnum)
      local help = ("#LIGHT_GREEN#(From %-10.60s, line: %s):#LAST#"):tformat(f_name or _t"unknown", f_lnum or _t"unknown")
  ```
  `f_lnum` 来自 `DebugConsole:functionHelp(func)` 返回的起始行号。对照 [entry-03257](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b097-20260923/sources/game/modules/tome/dialogs/debug/RandomActor.lua#L37) 中相同函数 `formatHelp` 的对应译法“第%s行”，“行数”确属事实语义错误。

---



## O019 | entry-03271

### C05 | entry-03271 | 存在问题

原文“line: %s”给出源码**行号**，译文“行数：%s”表示行的总数。`game/modules/tome/dialogs/debug/RandomObject.lua:43–50`将 `DebugConsole:functionHelp` 返回的位置传给该格式串，`:53–55`把它用于函数帮助。状态：已证实，译文新增误述。



## O020 | entry-03271

### C06 | entry-03271 | 存在问题

原文短引：`line: %s`；译文短引：“行数：%s”。

**状态：confirmed；翻译新增。** 参数表示函数定义所在的源码行号，不是文件或函数的行数，译文改变了数值含义。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:44` 的 `formatHelp` 将 `f_lnum` 填入第二个参数；第54–55行从 `DebugConsole:functionHelp` 获取该值。`game/engines/default/engine/DebugConsole.lua:495` 返回的是 `info.linedefined`，即定义位置。



## O021 | entry-03271

### C07 | entry-03271 | 存在问题
- 原文 `line: %s`，译文 `行数：%s`。
- 问题：“行数”的意思是“有多少行”，而参数实际是函数定义所在的行号。
- 源码依据：RandomObject.lua:45 `formatHelp(f_lines, f_name, f_lnum)`，行号 `f_lnum` 来自 :54 起的 `DebugConsole:functionHelp`。
- 同功能的 RandomActor 版本（entry-03257）译为“第%s行”，是正确的。属翻译新增的语义错误。



## O022 | entry-03272

### C06 | entry-03272 | 存在问题

原文“F1 :: context sensitive help”说明帮助随当前控件变化，译文仅称“查看帮助”。`game/modules/tome/dialogs/debug/RandomObject.lua:329–349`按焦点设置帮助内容，`:474–491`绑定 F1，`:508–513`显示所选内容。状态：已证实，译文遗漏帮助的适用范围。



## O023 | entry-03272

### C07 | entry-03272 | 存在问题

原文短引：`F1 :: context sensitive help`；译文短引：“F1 :: 查看帮助”。

**状态：confirmed；翻译新增遗漏。** 译文保留了帮助快捷键，但删除了帮助内容随当前控件或选择变化的信息。这会影响用户取得筛选器、神器数据或具体解析器说明的操作。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:475` 将F1绑定到 `help`；第509–512行根据 `_M.help_display` 选择内容；第339–347行随解析器选择更新帮助目标，第519–520行随文本框焦点更新目标。该差异涉及功能信息，不只是措辞简化。



## O024 | entry-03272

### C08 | entry-03272 | 存在问题
- 原文 `interpreted by ToME and engine entity/object generation functions`，译文 `由ToME游戏引擎的实体/物品处理函数解析`。
- 问题：原文说的是“ToME 与引擎”两个来源的函数，译文合并成了“ToME游戏引擎”，所属关系丢失。
- 源码依据：帮助里同时列出了引擎的 `game.zone.checkFilter`，以及 ToME GameState 的 `entityFilter`、`entityFilterAlter`、`entityFilterPost`（RandomObject.lua:54-61）。
- “generation”译成“处理”也偏宽泛，但不单独计为缺陷。



## O025 | entry-03272

### C09 | entry-03272 | 存在问题
- 原文 `'F1' :: context sensitive help`，译文 `'F1' :: 查看帮助`。
- 问题：丢了“随上下文变化”的信息。F1 显示什么，取决于当前聚焦的控件。
- 源码依据：
  - RandomObject.lua:508-511 `_M:help()` 的注释写明 “Display context sensitive help”，显示 `_M[_M.help_display]`。
  - 各控件在 :531、:520、:340、:345 等处改写 `help_display`。
- 信息缺失，影响轻微。



## O026 | entry-03272

### C10 | entry-03272 | 仅建议
- 第4行把 `working Actor` 译成“使用的角色”，下一行和按钮（entry-03278）都用“工作角色”。
- 所指对象不变，属于术语一致性偏好。



## O027 | entry-03282

### C07 | entry-03282 | 仅建议

译文“新随机%s 物品”在 `%s` 插入解析器括注后语序略拗口。`game/modules/tome/dialogs/debug/RandomObject.lua:598`表明括注与物品名仍各自正确传入；信息和格式均未受损。这只是流畅度偏好。



## O028 | entry-03282

### C11 | entry-03282 | 仅建议
- 译文 `新随机%s 物品：%s`：没有解析器时 %s 为空（RandomObject.lua:598），显示成“新随机 物品”，中间多一个空格。
- 参数和含义都正确，属无损排版。



## O029 | entry-03285

### C08 | entry-03285 | 存在问题

原文短引：`with filter [%s]`；译文短引：“发生错误[%s]”。

**状态：confirmed；翻译新增。** 第一个参数是筛选器文本，译文却将其附在“错误”之后，使之看似错误编号或错误内容；下一行才是真正的异常信息。两类诊断数据的标签关系被混淆。

证据：`game/modules/tome/dialogs/debug/RandomObject.lua:605` 传入 `_M._random_filter, o`，其中 `o` 是受保护调用失败后取得的异常值。占位符顺序保持一致并不能消除这项语义错位。



## O030 | entry-03285

### C12 | entry-03285 | 存在问题
- 原文 `ERROR generating random object with filter [%s].`，译文 `错误：使用该筛选器生成随机物品时发生错误[%s]。`
- 问题：`[%s]` 是筛选器文本（RandomObject.lua:605 的第一个参数 `_M._random_filter`），译文却把它放在“发生错误”后面。“该筛选器”又没有前文可指，读起来像是错误代码或错误内容，而真正的错误在下一行 `错误：%s`（参数 `o`）。
- 属于参数归属错位，翻译新增。



## O031 | entry-03287

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


## O032 | entry-03287

### C13 | entry-03287 | 存在问题
- 与 C12 同类：`…生成基础物品时发生错误 [%s]。`
- `[%s]` 是 `_M._base_filter`（RandomObject.lua:625），却被放在“发生错误”之后，“该筛选器”也没有所指。属于参数归属错位。



## O033 | entry-03289

### C08 | entry-03289 | 仅建议

“接受物品”是对“accepting object”的直译，在此处略显生硬。`game/modules/tome/dialogs/debug/RandomObject.lua:667–692`显示它指用解析器将物品加入游戏；现有日志仍保留了解析器和错误信息，不构成事实或参数错误。

实际读取：冻结包的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/dialogs/debug/` 下的 `CreateItem.lua`、`DebugMain.lua`、`Endgamify.lua`、`PlotTalent.lua`、`RandomActor.lua`、`RandomObject.lua`、`SummonCreature.lua`。七份源码的 SHA-256 均与 `source-access.json` 相符；其标注版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。未读取额外源码路径或其他报告，未创建临时文件，未发现需要越界才能裁定的 claim。本结果仅为审核观察，不宣称生产 `DONE_VERIFIED`。


## O034 | entry-03289

### C14 | entry-03289 | 仅建议
- `accepting object` 直译成“接受物品”。实际含义是按解析器把物品加入游戏（RandomObject.lua:667-687 `acceptObject`，对应按钮“添加物品”）。
- 作为调试错误日志，含义仍可对应，只是措辞建议。


