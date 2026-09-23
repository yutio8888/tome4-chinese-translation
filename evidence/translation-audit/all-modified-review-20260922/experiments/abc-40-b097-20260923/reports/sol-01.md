40 条已逐项核对，七份冻结源码的哈希也与清单一致。我会在结果中单列上游原文本身的机制误述，并注明没有越界读取、写入仓库或创建临时文件。
---

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03252 | 未发现问题 | 参数与物品位置吻合 |
| entry-03253 | 未发现问题 | 击杀归于玩家 |
| entry-03254 | 未发现问题 | 文件与错误信息吻合 |
| entry-03255 | 存在问题 | C01：把曲线图称为属性表 |
| entry-03256 | 未发现问题 | 技能等级标签可对应 TL |
| entry-03257 | 未发现问题 | 文件与行号吻合 |
| entry-03258 | 存在问题 | C02：遗漏悬停对象 |
| entry-03259 | 未发现问题 | 基础角色状态吻合 |
| entry-03260 | 未发现问题 | 基础角色日志吻合 |
| entry-03261 | 未发现问题 | 清除动作吻合 |
| entry-03262 | 未发现问题 | 基础筛选器标签吻合 |
| entry-03263 | 存在问题 | C03：随机角色回退的确定性丢失 |
| entry-03264 | 未发现问题 | Boss 角色状态吻合 |
| entry-03265 | 未发现问题 | Boss 数据标签吻合 |
| entry-03266 | 未发现问题 | 无效筛选器日志吻合 |
| entry-03267 | 未发现问题 | 生成失败日志吻合 |
| entry-03268 | 未发现问题 | 筛选器与错误参数吻合 |
| entry-03269 | 未发现问题 | 无效 Boss 数据日志吻合 |
| entry-03270 | 存在问题 | C04：沿袭上游的角色对象误述 |
| entry-03271 | 存在问题 | C05：行号误作行数 |
| entry-03272 | 存在问题 | C06：遗漏帮助随当前控件变化 |
| entry-03273 | 未发现问题 | 随机筛选器作用吻合 |
| entry-03274 | 未发现问题 | 随机筛选器标签吻合 |
| entry-03275 | 未发现问题 | 基础筛选器标签吻合 |
| entry-03276 | 未发现问题 | 解析器选择标签吻合 |
| entry-03277 | 未发现问题 | 随机神器数据标签吻合 |
| entry-03278 | 未发现问题 | 工作角色及参数吻合 |
| entry-03279 | 未发现问题 | 玩家标记可正确拼接 |
| entry-03280 | 未发现问题 | 玩家标记吻合 |
| entry-03281 | 未发现问题 | 解析器生成日志吻合 |
| entry-03282 | 仅建议 | C07：动态括注使语序稍拗口 |
| entry-03283 | 未发现问题 | 解析器括注吻合 |
| entry-03284 | 未发现问题 | 随机物品生成失败吻合 |
| entry-03285 | 未发现问题 | 筛选器与错误参数吻合 |
| entry-03286 | 未发现问题 | 基础物品生成失败吻合 |
| entry-03287 | 未发现问题 | 筛选器与错误参数吻合 |
| entry-03288 | 未发现问题 | 随机神器生成失败吻合 |
| entry-03289 | 仅建议 | C08：“接受物品”略显生硬 |
| entry-03290 | 未发现问题 | 角色身份及坐标吻合 |
| entry-03291 | 未发现问题 | 无待放置角色的条件吻合 |

### C01 | entry-03255 | 存在问题

原文“Values plot”指技能数值曲线图，译文“技能数值属性表”将显示形式说成表格。`game/modules/tome/dialogs/debug/PlotTalent.lua:114–139`逐级计算坐标并绘制连线，`:149–159`将图形显示到屏幕。状态：已证实，译文新增误述。

### C02 | entry-03258 | 存在问题

原文“Mouse over controls for an actor preview”指定将鼠标悬停在**控件上**；译文“鼠标移动查看角色预览”遗漏操作目标。`game/modules/tome/dialogs/debug/RandomActor.lua:65–75`是该界面说明，`:279–287`的控件选中逻辑显示角色预览。状态：已证实，译文遗漏操作信息。

### C03 | entry-03263 | 存在问题

原文说必要时“will use a random actor”，译文“也可以用随机角色作为基础”只表达可能性。`game/modules/tome/dialogs/debug/RandomActor.lua:353–358`显示没有基础角色时程序直接随机生成一个，再于`:374`生成 Boss。状态：已证实，译文弱化了自动回退条件。

### C04 | entry-03270 | 存在问题

原文“generate a base actor with data”和译文“生成基础角色”均误指失败对象。`game/modules/tome/dialogs/debug/RandomActor.lua:353–358`先取得基础角色，`:374–383`随后用 Boss 数据生成随机 Boss；此处失败的是后一步。状态：已证实；这是**沿袭上游英文日志**的机制误述，非翻译新增。

### C05 | entry-03271 | 存在问题

原文“line: %s”给出源码**行号**，译文“行数：%s”表示行的总数。`game/modules/tome/dialogs/debug/RandomObject.lua:43–50`将 `DebugConsole:functionHelp` 返回的位置传给该格式串，`:53–55`把它用于函数帮助。状态：已证实，译文新增误述。

### C06 | entry-03272 | 存在问题

原文“F1 :: context sensitive help”说明帮助随当前控件变化，译文仅称“查看帮助”。`game/modules/tome/dialogs/debug/RandomObject.lua:329–349`按焦点设置帮助内容，`:474–491`绑定 F1，`:508–513`显示所选内容。状态：已证实，译文遗漏帮助的适用范围。

### C07 | entry-03282 | 仅建议

译文“新随机%s 物品”在 `%s` 插入解析器括注后语序略拗口。`game/modules/tome/dialogs/debug/RandomObject.lua:598`表明括注与物品名仍各自正确传入；信息和格式均未受损。这只是流畅度偏好。

### C08 | entry-03289 | 仅建议

“接受物品”是对“accepting object”的直译，在此处略显生硬。`game/modules/tome/dialogs/debug/RandomObject.lua:667–692`显示它指用解析器将物品加入游戏；现有日志仍保留了解析器和错误信息，不构成事实或参数错误。

实际读取：冻结包的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/dialogs/debug/` 下的 `CreateItem.lua`、`DebugMain.lua`、`Endgamify.lua`、`PlotTalent.lua`、`RandomActor.lua`、`RandomObject.lua`、`SummonCreature.lua`。七份源码的 SHA-256 均与 `source-access.json` 相符；其标注版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。未读取额外源码路径或其他报告，未创建临时文件，未发现需要越界才能裁定的 claim。本结果仅为审核观察，不宣称生产 `DONE_VERIFIED`。
