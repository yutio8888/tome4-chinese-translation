## 复核结果：entry-03252–03291（共40条）

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03252 | 未发现问题 | CreateItem.lua:286 `findObject` 日志，8个参数顺序和颜色标记都保持一致 |
| entry-03253 | 未发现问题 | DebugMain.lua:128-148，`e:die(game.player,…)` 由玩家击杀，与“替玩家将其击杀（给予经验…）”一致 |
| entry-03254 | 未发现问题 | Endgamify.lua:179，`file` 和 `ret` 两个参数及换行保留 |
| entry-03255 | 存在问题 | C01 |
| entry-03256 | 未发现问题 | PlotTalent.lua:37，Textbox 标题 |
| entry-03257 | 未发现问题 | RandomActor.lua:37，“第%s行”对应行号 |
| entry-03258 | 存在问题 | C02（存在问题）；C03（仅建议） |
| entry-03259 | 未发现问题 | RandomActor.lua:86 |
| entry-03260 | 未发现问题 | RandomActor.lua:100 |
| entry-03261 | 未发现问题 | RandomActor.lua:129 |
| entry-03262 | 未发现问题 | RandomActor.lua:141，Textbox 标题 |
| entry-03263 | 仅建议 | C04、C05 |
| entry-03264 | 未发现问题 | RandomActor.lua:169 |
| entry-03265 | 未发现问题 | RandomActor.lua:210 |
| entry-03266 | 未发现问题 | RandomActor.lua:330 |
| entry-03267 | 未发现问题 | RandomActor.lua:343 |
| entry-03268 | 仅建议 | C06 |
| entry-03269 | 未发现问题 | RandomActor.lua:369 |
| entry-03270 | 未发现问题 | RandomActor.lua:383 忠实于原文；原文说“base actor”，实际是 boss 生成失败的分支，属上游措辞问题。但 GameState.lua `createRandomBoss` 只有一个 `return b`（`b = base:clone()`），所以这条日志在固定 commit 下不可达，玩家看不到 |
| entry-03271 | 存在问题 | C07 |
| entry-03272 | 存在问题 | C08、C09（存在问题）；C10（仅建议） |
| entry-03273 | 未发现问题 | RandomObject.lua:174 |
| entry-03274 | 未发现问题 | RandomObject.lua:240 |
| entry-03275 | 未发现问题 | RandomObject.lua:310 |
| entry-03276 | 未发现问题 | RandomObject.lua:327 |
| entry-03277 | 未发现问题 | RandomObject.lua:387 |
| entry-03278 | 未发现问题 | RandomObject.lua:422，uid 和 name 的参数顺序保留 |
| entry-03279 | 未发现问题 | RandomObject.lua:426 |
| entry-03280 | 未发现问题 | RandomObject.lua:426 作为 %s 拼接，前导空格保留 |
| entry-03281 | 未发现问题 | RandomObject.lua:587 |
| entry-03282 | 仅建议 | C11 |
| entry-03283 | 未发现问题 | RandomObject.lua:598，内层 tformat 片段 |
| entry-03284 | 未发现问题 | RandomObject.lua:601 |
| entry-03285 | 存在问题 | C12 |
| entry-03286 | 未发现问题 | RandomObject.lua:621 |
| entry-03287 | 存在问题 | C13 |
| entry-03288 | 未发现问题 | RandomObject.lua:645 |
| entry-03289 | 仅建议 | C14 |
| entry-03290 | 未发现问题 | RandomObject.lua:706，%d 用于整数坐标 x、y |
| entry-03291 | 未发现问题 | SummonCreature.lua:104 |

### C01 | entry-03255 | 存在问题
- 原文 `Values plot for: %s (mastery %0.1f)`，译文 `技能数值属性表：%s (技能树系数 %0.1f)`。
- 问题：把“plot（曲线图）”译成了“属性表”。
  - 对话框画的是折线图：PlotTalent.lua:46-143 `generatePlot` 用 `vo:addQuad` 连线。
  - 画的量是技能函数值，不是属性：:78-84 只收集 `radius`、`range` 和 `^get[A-Z]` 函数的数值。
  - 译文既把展示形式说错了，又凭空加了“属性”这个对象。
- “技能树系数”没有问题：`getTalentMastery` 取的是技能类别 mastery 再加加成。依据是 engine/interface/ActorTalents.lua:941-944，以及 tome/class/Actor.lua:5091-5097。
- 属翻译新增的问题，影响限于调试界面。

### C02 | entry-03258 | 存在问题
- 原文 `Mouse over controls for an actor preview`，译文 `鼠标移动查看角色预览`。
- 问题：漏掉了“over controls（悬停在控件上）”这个操作对象，读起来像随便移动鼠标都会出现预览。
- 源码依据：预览只在控件获得焦点或被选中时触发。
  - RandomActor.lua:284-287 `newButton.on_select` 调用 `_M.tooltip`。
  - :94、:177 在 Textzone 的 `on_focus` 里触发。
- 这是对玩家操作描述的缺失。同类句子在 entry-03272 里译成了“将鼠标悬停在控件上”，可作对照。

### C03 | entry-03258 | 仅建议
- 末句 `#LIGHT_BLUE#基础过滤器#LAST#` 用了“过滤器”，但实际输入框标签是“基础筛选器：”（entry-03262，RandomActor.lua:141），同一段前两行也用“筛选器”。
- 两词同义，颜色标记也一致，玩家仍能对应到控件，没有信息丢失，只算一致性偏好。

### C04 | entry-03263 | 仅建议
- 原文 `(which will use a random actor if needed)`，译文 `（如果需要的话，也可以用随机角色作为基础）`。
- 源码中这是自动回退：没有基础角色时，由 RandomActor.lua:355-358 自动随机生成。
- “也可以”略带“可选”的意味，但“如果需要的话”保留了条件，也没有说错行为，所以只作措辞建议。

### C05 | entry-03263 | 仅建议
- `Boss 数据` 带空格、`boss` 小写，与同文件“Boss数据”（entry-03265）写法不统一。属于无损排版问题。

### C06 | entry-03268 | 仅建议
- 译文 `无法使用以下筛选器生成基础角色[%s]。`：筛选器内容 `[%s]` 紧跟在“基础角色”后面。
- 但前面有“以下筛选器”指向它，归属仍可辨认，只是语序建议。

### C07 | entry-03271 | 存在问题
- 原文 `line: %s`，译文 `行数：%s`。
- 问题：“行数”的意思是“有多少行”，而参数实际是函数定义所在的行号。
- 源码依据：RandomObject.lua:45 `formatHelp(f_lines, f_name, f_lnum)`，行号 `f_lnum` 来自 :54 起的 `DebugConsole:functionHelp`。
- 同功能的 RandomActor 版本（entry-03257）译为“第%s行”，是正确的。属翻译新增的语义错误。

### C08 | entry-03272 | 存在问题
- 原文 `interpreted by ToME and engine entity/object generation functions`，译文 `由ToME游戏引擎的实体/物品处理函数解析`。
- 问题：原文说的是“ToME 与引擎”两个来源的函数，译文合并成了“ToME游戏引擎”，所属关系丢失。
- 源码依据：帮助里同时列出了引擎的 `game.zone.checkFilter`，以及 ToME GameState 的 `entityFilter`、`entityFilterAlter`、`entityFilterPost`（RandomObject.lua:54-61）。
- “generation”译成“处理”也偏宽泛，但不单独计为缺陷。

### C09 | entry-03272 | 存在问题
- 原文 `'F1' :: context sensitive help`，译文 `'F1' :: 查看帮助`。
- 问题：丢了“随上下文变化”的信息。F1 显示什么，取决于当前聚焦的控件。
- 源码依据：
  - RandomObject.lua:508-511 `_M:help()` 的注释写明 “Display context sensitive help”，显示 `_M[_M.help_display]`。
  - 各控件在 :531、:520、:340、:345 等处改写 `help_display`。
- 信息缺失，影响轻微。

### C10 | entry-03272 | 仅建议
- 第4行把 `working Actor` 译成“使用的角色”，下一行和按钮（entry-03278）都用“工作角色”。
- 所指对象不变，属于术语一致性偏好。

### C11 | entry-03282 | 仅建议
- 译文 `新随机%s 物品：%s`：没有解析器时 %s 为空（RandomObject.lua:598），显示成“新随机 物品”，中间多一个空格。
- 参数和含义都正确，属无损排版。

### C12 | entry-03285 | 存在问题
- 原文 `ERROR generating random object with filter [%s].`，译文 `错误：使用该筛选器生成随机物品时发生错误[%s]。`
- 问题：`[%s]` 是筛选器文本（RandomObject.lua:605 的第一个参数 `_M._random_filter`），译文却把它放在“发生错误”后面。“该筛选器”又没有前文可指，读起来像是错误代码或错误内容，而真正的错误在下一行 `错误：%s`（参数 `o`）。
- 属于参数归属错位，翻译新增。

### C13 | entry-03287 | 存在问题
- 与 C12 同类：`…生成基础物品时发生错误 [%s]。`
- `[%s]` 是 `_M._base_filter`（RandomObject.lua:625），却被放在“发生错误”之后，“该筛选器”也没有所指。属于参数归属错位。

### C14 | entry-03289 | 仅建议
- `accepting object` 直译成“接受物品”。实际含义是按解析器把物品加入游戏（RandomObject.lua:667-687 `acceptObject`，对应按钮“添加物品”）。
- 作为调试错误日志，含义仍可对应，只是措辞建议。

## 读取范围与边界
- **实验目录（只读）**：
  - 读了 `INPUT.md`、`source-access.json`、`entries.json`（其中含 `baseline_target` 等字段，一并读到，但判定没有依据旧译文）和 `context.lua`。
  - 读了 7 份 `sources/game/modules/tome/dialogs/debug/*.lua`，sha256 与 source-access.json 全部一致。
  - 另外用 `ls` 列过一次目录，看到了 BASELINE、SPEC、STATE、SCORING 等文件名，但都没有打开。
- **额外源码**：都用 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取，只做了局部 grep/sed，路径来源如下：
  - `game/engines/default/engine/interface/ActorTalents.lua`：来自 PlotTalent.lua:32 的 `actor:getTalentMastery`。
  - `game/modules/tome/class/Actor.lua`：ToME Actor 覆盖了 `getTalentMastery` 内部调用的 `getTalentTypeMastery`。
  - `game/modules/tome/class/GameState.lua`：来自 RandomActor.lua:374 的 `game.state.createRandomBoss`。
- **临时文件**：没有创建任何临时目录或文件。
- **未做的事**：没有修改仓库，没有读其他报告或模型输出，没有创建子 agent。
- **越界情况**：无。没有无法核验的 claim。

以上是审核观察，不是真值；不宣称 DONE_VERIFIED。
