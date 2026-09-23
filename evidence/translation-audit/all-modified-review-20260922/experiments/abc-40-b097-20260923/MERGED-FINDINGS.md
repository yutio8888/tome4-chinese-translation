# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的25项观察及独立盲审的9项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03255 | C01（原问题） | C01（原问题） | 未提出此缺陷 | **翻译新增，显示形式错误。** `Values plot` →“技能数值属性表”。`debug/PlotTalent.lua:78–84、94–100`采集不同等级下的技能函数值，`:114–137`连接数值点并绘制标注，`:149–159`显示图形。确认“图”变“表”；不把“属性”另计一个对象错误。 |
| D02 | entry-03258 | C02（原问题） | C02（原问题） | 未提出此缺陷 | **翻译新增，操作目标遗漏。** `Mouse over controls` →“鼠标移动”。`debug/RandomActor.lua:94、177`将预览绑定至角色文本控件焦点，`:279–287`按按钮的 `_actor_field`显示对应角色。译文未交代应把鼠标移到控件上。 |
| D03 | entry-03263 | C04（原建议） | C03（原问题） | 未提出此缺陷 | **翻译新增，条件行为信息弱化。** `will use a random actor if needed` →“如果需要的话，也可以用随机角色作为基础”。`debug/RandomActor.lua:180–184`的生成按钮直接调用 `generateBoss`；`:353–358`在没有基础角色时直接生成随机基础角色。译文保留了能力和条件，却未保留需要时由生成流程执行回退的确定行为。 |
| D04 | entry-03270 | 未提出此缺陷 | C04（原问题） | C02（原问题） | **沿袭上游，失败阶段／对象误述。** 英文和中文均称“基础角色”。`debug/RandomActor.lua:354–360`已经取得基础角色，`:374–383`检查的是 `createRandomBoss`返回结果，参数为 Boss 数据。`game/modules/tome/class/GameState.lua:2368–2397、2475、2536`克隆基础角色、加工为随机 Boss 并返回。确认日志的对象描述错误；不声称正常实现会触发这一空返回防御分支。 |
| D05 | entry-03271 | C07（原问题） | C05（原问题） | C03（原问题） | **翻译新增，数值含义错误。** `line: %s` →“行数：%s”。`debug/RandomObject.lua:44–55`将 `functionHelp`第三个返回值填入该参数；`game/engines/default/engine/DebugConsole.lua:462–495`返回 `info.linedefined`。这是定义所在行号，不是行的数量。 |
| D06 | entry-03272 | C09（原问题） | C06（原问题） | 未提出此缺陷 | **翻译新增，功能信息遗漏。** `context sensitive help` →“查看帮助”。`debug/RandomObject.lua:339–347、519–531`随控件焦点或解析器选择更新 `help_display`，`:475、509–512`由 F1 显示相应内容。译文遗漏了获得不同帮助内容所依赖的上下文关系。 |
| D07 | entry-03272 | C08（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，函数来源关系丢失。** `ToME and engine` →“ToME游戏引擎”。`debug/RandomObject.lua:54–61`分别收集 `game.zone.checkFilter`和三个 `game.state.entityFilter*`函数的帮助；实现分别见 `game/engines/default/engine/Zone.lua:294–319`及 `game/modules/tome/class/GameState.lua:1357、1460、1583`。原文明确并列模块与引擎两层来源，译文将其合成一个名称。“generation”译为“处理”不另计缺陷。 |
| D08 | entry-03285 | C12（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，诊断字段归属歧义。** `with filter [%s]` →“发生错误[%s]”。`debug/RandomObject.lua:580–605`表明两个参数依次为 `_M._random_filter`和异常值 `o`。译文将筛选器内容直接附于“错误”，下一行再列真实错误；原文明确的筛选器字段关系因此丢失。并非占位符顺序错误。 |
| D09 | entry-03287 | C13（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，诊断字段归属歧义。** `with filter [%s]` →“发生错误 [%s]”。`debug/RandomObject.lua:611–625`传入 `_M._base_filter, o`。与 D08 同类，但属于另一独立条目，分别计数。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O003 | Opus C01（原问题） | entry-03255 | mixed | **confirmed**：“曲线图”被称为“表”。**advisory**：“属性”可泛指技能参数，不能据此另立对象错误。技能树系数有 ActorTalents.lua:941–944、Actor.lua:5091–5097支持。 |
| O004 | Gemini C01（原建议） | entry-03258 | advisory | 同段及基础输入框均可明确对应同一筛选器；同义词不统一未改变功能。 |
| O008 | Opus C03（原建议） | entry-03258 | advisory | RandomActor.lua:74、141及冻结上下文足以对应“基础过滤器／基础筛选器”。 |
| O011 | Opus C04（原建议） | entry-03263 | mixed | **confirmed**：源码存在自动回退、中文带可选意味。**refuted**：“只有措辞差异、没有信息损失”的结论；保留“如果需要”不能替代执行行为。 |
| O012 | Opus C05（原建议） | entry-03263 | advisory | Boss 的大小写及空格未改变所指数据或转换对象。 |
| O013 | 独立盲审 C04（原问题） | entry-03268 | advisory | RandomActor.lua:347确实传入筛选器和异常；但整句“以下筛选器”仍前指随后唯一的括号内容，不能仅凭紧邻“角色”认定参数已成为角色标识。 |
| O014 | Opus C06（原建议） | entry-03268 | advisory | 同 O013；当前文本保有明确的前指词，属于参数摆放不够顺畅。 |
| O026 | Opus C10（原建议） | entry-03272 | advisory | 同一段“使用的角色／工作角色”仍指同一对象，未造成对象切换。 |
| O027 | Sol C07（原建议） | entry-03282 | advisory | RandomObject.lua:598分别传入解析器括注和物品名；主要问题是语序。 |
| O028 | Opus C11（原建议） | entry-03282 | advisory | 无解析器时首参数为空，额外空格不影响信息或参数消费。 |
| O030 | Opus C12（原问题） | entry-03285 | mixed | **confirmed**：筛选器字段与“错误”的附着关系造成歧义。**refuted**：“该筛选器完全没有所指”；RandomObject.lua:240–249提供当前筛选器输入语境，但这未恢复括号字段的明确标签。 |
| O032 | Opus C13（原问题） | entry-03287 | mixed | **confirmed**：同 D09 的字段归属问题。**refuted**：“该筛选器没有所指”；基础筛选器控件在 RandomObject.lua:310–321明确存在。 |
| O033 | Sol C08（原建议） | entry-03289 | advisory | RandomObject.lua:667–692表明这是解析器接收／加入物品阶段；“接受”生硬但未改变阶段或参数。观察所附读取声明不作为证据。 |
| O034 | Opus C14（原建议） | entry-03289 | advisory | 与 O033 合并为同一措辞建议，不计确认缺陷。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
