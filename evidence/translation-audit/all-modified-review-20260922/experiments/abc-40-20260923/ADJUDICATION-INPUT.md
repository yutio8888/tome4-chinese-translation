# 匿名观察逐项核验（独立参考第二阶段）

你是新的只读 REVIEWER。不得读取本实验的原始报告、STATE、host-only映射或任何其他模型身份信息。只读取本文件、protocol-v2/INPUT.md及其明确允许的冻结材料/固定版本源码。沿相同已知单文件/调用链边界核验。D/=game/modules/tome/dialogs/；M/=game/modules/tome/；E/=game/engines/default/engine/。

用户最新授权：可在仓库外任务专属/tmp/abc40-adjudication/保存临时中间文件并清理；不可修改仓库、译文、冻结输入、其他task，不能读别人的临时文件。其余规则沿protocol-v2/INPUT.md。这项明确授权优先于INPUT较早的绝对不写文件条款。

下面观察来自已冻结的独立输出，模型身份已移除，排序只依entry/文字。条数和相同意见重复绝不是正确证据。你需自行核验每个观察，发现范围内漏项也可指出；全40条都要再检查，不能只看有观察的条目。不得猜模型身份或做模型排名。

输出中文自然语言及Markdown表，不强制JSON：
1. 恰好40行最终参考表：entry-ID | OK/ISSUE/PENDING | canonical缺陷ID或短依据。ISSUE须至少有一个证据充分缺陷；尚有证据缺口又无已确认缺陷则PENDING；纯建议/偏好归OK。按INPUT明确的四类合并规则，不以严重度降级客观错误。
2. 每个已确认原子缺陷给唯一D编号、entry、内容及源码/语境证据；同条的重复/同义观察归同一D，不同信息遗漏拆开。不能用“有另一个真问题”让错误观察也算命中。
3. 恰好每个O编号一行：O-ID | confirmed/refuted/pending/advisory/mixed | 命中的D编号或— | 具体证据与理由。复合观察可能混合，请显式拆分，说明哪些部分confirmed对应哪个D、哪些refuted、pending或advisory，宿主不能替你补语义裁决。建议也须核验，可能被错误降级；明确观察到底提出了什么问题。
4. 说明仍有争议/证据不足的项；给完整读取路径与版本。只基于本次冻结数据和固定源码，不依赖历史规范性裁决。没有实际证据的mechanism claim不能confirmed。无需修改方案。

这是暂定的模型参考判定，不是人工金标准。所有观察均应按同一标准；空行等合法排版只在导致信息结构丢失时才判缺陷。不要因为重复提到某观点就接受，也不要为了制造区别把措辞偏好当错译。

## 匿名观察

### O001 · entry-03174

#### claim-03174-1
- **条目**：[entry-03174](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L52-L67)
- **短引**：原文 `...will make locked campaigns, races and classes permanently available.` / 译文 `...可以永久解锁这个战役，种族，职业。`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`Birther.lua:804`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L804)（以及 826、858、890、944 行）。`locktext` 作为统一模板追加在未解锁的战役、难度、死亡模式、种族和职业描述后展示给玩家。
- **说明**：原文为总括性复数表述（locked campaigns, races and classes），译文使用单数指示代词“这个”并以逗号并列，风格偏口语化；但由于附着于具体未解锁项后显示，语义指向清晰，无实质信息缺失或机制误导，仅属文字规范与标点偏好。

### O002 · entry-03174

**C1（entry-03174）｜已证实｜翻译新增**
- 原文说完成某些操作和任务会让**被锁定的**战役、种族和职业永久可用。
- 译文是"本选项被锁定……可以永久解锁**这个**战役，种族，职业"，把泛指说成了当前选项本身，并且把它归成战役、种族或职业。
- 源码：同一个 locktext 还用在 `generateDifficulties`（Birther.lua:826/838）和 `generatePermadeaths`（Birther.lua:858/870）。所以在锁定的难度或死亡模式选项下，玩家会看到"解锁这个战役，种族，职业"。这是作用对象错误。
- "Performing certain actions" 译成"条件"属于意译，不单独计。

### O003 · entry-03174

- **C01｜entry-03174｜已确认，翻译新增。**  
  原文泛指“locked campaigns, races and classes”，译文变成“解锁**这个**战役，种族，职业”，把一般说明收窄成对当前选项的类型指认。`D/Birther.lua:826、838` 的 `generateDifficulties()` 将同一说明附在锁定的难度选项上；`:858、870` 又用于死亡模式。因此当前选项不一定属于译文指认的三种类型。

### O004 · entry-03174

- **C1｜entry-03174，已证实。** 原文是“Performing certain actions and completing certain quests”，译文“完成特定的任务或条件”把行动改成了条件；“解锁这个战役，种族，职业”又使单个锁定选项看起来会同时解锁三类内容。`Birther.lua:803–811、825–838、950–958` 将同一提示用于不同的锁定出生选项，逐项生成说明。

### O005 · entry-03175

entry-03175 的“剧情”与 *lore-wise* 所指的背景设定不完全贴合，但此处仍传达了种族与职业搭配在叙事上不合适的警示；在现有语境下仅属措辞建议。

### O006 · entry-03176

#### claim-03176-1
- **条目**：[entry-03176](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L82-L111)
- **短引**：原文 `You will need an online profile active and connected for the tile selector to enable.` / 译文 `你需要一个已激活并保持连接的在线档案，贴图选择器才能启用。`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`Birther.lua:1385`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L1385)（`_M:selectExplorationNoDonations`）。该弹窗是未捐赠玩家在创角界面尝试选择“探索模式”（Exploration Mode）时弹出的捐赠说明弹窗。
- **问题内容**：源码英文在此处系由第 1401 行自定义贴图弹窗（`_M:selectTileNoDonations`）直接复制而来的上游文本笔误，导致在探索模式弹窗中错误地向玩家说明为“tile selector”（贴图选择器）的激活条件。译文忠实复制了该英文文本，面向玩家构成机制说明上的事实错误。本条确认为**面向玩家的机制误述**，且为**沿袭上游描述**，非翻译新增。

### O007 · entry-03176

#### claim-03176-2
- **条目**：[entry-03176](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L82-L111)
- **短引**：原文 `I realize this can not please everybody and after multiple requests I have decided to grant exploration mode to donators...` / 译文 `我觉得这款游戏可能不会被所有人接受并且在收到多次请求后，我决定开放探索模式给捐赠者...`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`Birther.lua:1380`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L1380)（`_M:selectExplorationNoDonations`）。上下文紧承前句“Tales of Maj'Eyal is meant to be a very replayable game in which you get better by learning from mistakes (and thus from dying too)”。
- **问题内容**：代词“this”明确指向前句阐述的“在死亡与错误中学习”的高惩罚性永久死亡机制（即这种严苛的硬核玩法无法取悦所有人，因而才提供无限命探索模式）。译文译为“我觉得这款游戏可能不会被所有人接受”，误将对局内死亡机制的指代扩大至整款游戏本身，属于**翻译新增**的语义偏差。

### O008 · entry-03176

**C2（entry-03176）｜已证实｜翻译新增**
- 原文 "While this is a **free** game that I am doing for fun"。
- 译文"尽管这只是我自娱自乐所做的一款游戏"丢了"免费"。这句的让步逻辑正是建立在"免费"上，属于事实信息丢失。
- 语境：Birther.lua:1384，在捐赠请求段落里。

### O009 · entry-03176

**C3（entry-03176）｜已证实｜翻译新增**
- 原文 "I certainly will not complain as real life can be harsh sometimes"：不抱怨的对象是"游戏帮忙养家"，"现实艰难"是原因。
- 译文"我就谢天谢地，不会再抱怨现实的诸多压力了"把原因当成了不抱怨的对象，语义关系改变。

### O010 · entry-03176

**C4（entry-03176）｜已证实｜翻译新增**
- 原文 "only that you can try as much as you want **without restarting**"。
- 译文"仅仅意味着你可以有着无限多的尝试次数"丢了"不必重开"。这正是无限生命与普通重开的区别，属于条件信息丢失。

### O011 · entry-03176

**C5（entry-03176）｜已证实｜翻译新增**
- 原文 "I realize this can not please everybody"：从上下文看，"this"指上一句"从死亡中学习"的设计，下半句正是为此开放探索模式。
- 译文"我觉得这款游戏可能不会被所有人接受"把指代换成了整款游戏。

### O012 · entry-03176

**S1（entry-03176）｜仅建议**
- "get better by learning" 的"变强"、"if they wish"、"find this game good"的措辞有轻微弱化，主旨未丢。
- "It will help ensure its survival." 被移到下一行开头，属于合法排版重排。
- 附注：探索模式弹窗里提到"tile selector"，是上游从 Custom tiles 弹窗（Birther.lua:1398-1402）复制来的原文，译文照译。该句陈述本身不构成机制误述，不计入缺陷。

### O013 · entry-03176

- **C02｜entry-03176｜已确认，翻译新增。**  
  “I realize **this** can not please everybody”承接通过犯错、死亡学习的设计，译成“**这款游戏**可能不会被所有人接受”后，评价对象扩大为整个游戏。证据为 `D/Birther.lua:1379–1380` 的连续语境，属于指代和语义范围变化。

### O014 · entry-03176

- **C03｜entry-03176｜已确认，翻译遗漏。**  
  “try as much as you want **without restarting**”只剩“无限多的尝试次数”，遗漏不必重新开始角色的区别。`D/Birther.lua:1381` 明说此条件；`D/DeathDialog.lua:174–185、340–345` 显示探索模式走原角色复活流程，并且不扣生命次数。无限次重新创建角色与无限次原角色复活并不等价。

### O015 · entry-03176

- **C04｜entry-03176｜已确认，翻译遗漏。**  
  “While this is a **free game** that I am doing for fun”译成“尽管这只是我自娱自乐所做的一款游戏”，遗漏免费这一事实陈述。证据为 `D/Birther.lua:1384`；该信息不能由“自娱自乐”替代。

### O016 · entry-03176

- **C05｜entry-03176｜已确认，翻译新增。**  
  “I certainly will not complain as real life can be harsh sometimes”表达作者欢迎游戏收入补贴家用，并解释现实生活有时艰难。译文“不会**再抱怨现实的诸多压力**了”改成收到帮助后停止抱怨现实，并新增过去一直抱怨的意味。证据为 `D/Birther.lua:1384` 的完整条件句；这不是单纯语气润色。

### O017 · entry-03176

- **C2｜entry-03176，已证实。** 原文“I realize this can not please everybody”的 *this* 承接前句反复游玩、从死亡中学习的设计；译文“这款游戏可能不会被所有人接受”改成了整款游戏。语境见 `Birther.lua:1376–1381`。

### O018 · entry-03176

- **C3｜entry-03176，已证实。** 原文“try as much as you want **without restarting**”，译文只说“无限多的尝试次数”，遗漏无需重新开始这一条件。该文字用于探索模式提示，见 `Birther.lua:1376–1387`。

### O019 · entry-03179

#### claim-03179-1
- **条目**：[entry-03179](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L136-L147)
- **短引**：原文 `#RED#Displaying %s set for %s (equipment NOT switched)` / 译文 `#RED#展示 %s 套装给 %s 看（装备未切换）`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`CharacterSheet.lua:74`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/CharacterSheet.lua#L74)（`init` 中 `c_equipment.on_change`）。当玩家在人物面板的装备标签页切换显示主手/副手武器配置时，触发 `game.logPlayer(self.actor, ...)`。`%1$s` 消费 `self.equip_set`（即 `"main"` 或 `"off"`，在界面对应“主手”或“副手”），`%2$s` 消费 `self.actor:getName():capitalize()`（被查看角色的名称）。
- **问题内容**：原文“Displaying %s set for %s”表达的是“正在为角色 %2$s 显示 %1$s 武器配置/槽位”。译文译作“展示 %s 套装给 %s 看”，将作为所属主体的角色 %2$s 扭曲成了接收展示的受众观众（“给...看”），颠倒了作用对象与所属关系；同时武器配置（set）在装备槽语境并非套装装备（item set），译为“套装”容易引起机制概念混淆。

### O020 · entry-03179

**C6（entry-03179）｜已证实｜翻译新增**
- 原文 "Displaying %s set for %s"：第二个 %s 是 `self.actor:getName()`，意思是"正在显示该角色的某组装备"。
- 译文"展示 %s 套装给 %s 看"把所属关系变成了"展示给某人看"。
- 源码：CharacterSheet.lua:69-74。这是切换装备页时只切换显示的日志，第一个参数为 main/off。
- "套装"一词沿用 context 中 "[E]quipment: %s set" 的既有译法，不另计。

### O021 · entry-03179

- **C06｜entry-03179｜已确认，翻译新增。**  
  “Displaying %s set **for %s**”被译成“展示 %s 套装**给 %s 看**”。`D/CharacterSheet.lua:71–74` 先切换面板展示的 `main/off` 装备组，再传入 `self.actor:getName()`；第二个参数是装备所属角色，不是观看者。“装备未切换”保留正确，但不能抵消所属关系错误。

### O022 · entry-03179

- **C4｜entry-03179，已证实。** 原文“Displaying %s set for %s”表示在角色面板显示某角色的装备组；译文“展示 %s 套装给 %s 看”把第二个参数变成观看者。`CharacterSheet.lua:62–79` 表明第二个参数来自 `self.actor:getName()`，操作仅更新面板引用，装备并未切换。

### O023 · entry-03183

**S2（entry-03183）｜仅建议**
- 数值是 `life_regen * bound(healing_factor, 0, 2.5)`（CharacterSheet.lua:743）。系数可能小于 1，"加成后"略偏正向。
- 但"加成"在游戏语境里常泛指修正，不构成数值误述。

### O024 · entry-03183

- **C5｜entry-03183，已证实。** “with heal mod”译作“治疗系数**加成**后”，但系数可以低于 1，计算结果也可能降低。`CharacterSheet.lua:735–744` 对低于 1 的系数使用红色，并以该系数乘生命回复值。

### O025 · entry-03191

#### claim-03191-1
- **条目**：[entry-03191](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L280-L303)
- **短引**：原文 `...so I have come to disturb you here and now to ask for your kindness.` / 译文 `...所以我来这里打扰你，希望得到你的帮助`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`Donation.lua:51`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Donation.lua#L51)（`init` 中 `desc` 文本区域）。
- **说明**：第二段末句“希望得到你的帮助”句末遗漏句号。由于不丢失实质语义，亦不影响格式化参数与换行渲染，仅属标点完整性层面的排版优化建议。

### O026 · entry-03191

**S3（entry-03191）｜仅建议**
- "the (many) hours … were worth it" 意译成"时间充满了快乐"，第三段末尾缺句号。
- 劝捐的语用功能等价；%s 由 `table.concatNice` 填充（Donation.lua:54），格式正确。

### O027 · entry-03191

- **S01｜entry-03191。** “我最衷心的希望”等局部搭配略显生硬。`D/Donation.lua:48–54` 的自我介绍、捐赠请求及附加功能列表关系仍清楚，属于语言流畅度建议。

### O028 · entry-03192

**S4（entry-03192）｜仅建议**
- 该值是 smooth_move 的动画量，描述写明越高越慢（GameOptions.lua:107-111）。
- "动画速度（越低越快）"与英文同样有字面悖论，括注已消歧，属于沿袭上游的表达。

### O029 · entry-03192

- **S02｜entry-03192。** “设置动画速度”单独看较宽泛，但冻结相邻文本明确限定为平滑生物和投射物移动；`D/GameOptions.lua:107–114` 也在这一选项下打开输入框。结合实际界面语境，没有足够依据判定其宣称控制所有动画，故只作明确性建议。

### O030 · entry-03195

- **C07｜entry-03195｜已确认，翻译新增。**  
  “Fade time”译为“消失时间”，混淆开始淡出与完全消失。`D/GameOptions.lua:217–227` 明确这是日志开始淡出前的秒数，并调用 `enableFading(qty)`；`E/LogDisplay.lua:270–274` 在经过设定的 `t` 秒后才开始降低透明度，到 `2t` 秒才完全不可见。例如设置3秒并不是3秒后消失。术语快照中的技能名“Fade”不适用于此处，判定不依赖该术语行。

### O031 · entry-03195

- **C6｜entry-03195，已证实。** 译文“消失时间”会被理解为日志消失所需时间；该设置实际控制日志和聊天行**开始淡出之前**等待的秒数，0 表示永不淡出。见 `GameOptions.lua:217–227`。

### O032 · entry-03196

**S5（entry-03196）｜仅建议**
- "small/big tactical frame" 译成"小框架/大框架"，省去了"战术"。有标题"切换战术信息显示模式"兜底，信息结构未丢。
- 格式标记 #{italic}#、#{normal}#、#WHITE# 已保留。
- 快捷键 shift+T 为照译，未追查按键绑定，不构成疑点。

### O033 · entry-03197

**S6（entry-03197）｜仅建议**
- "pressing two directions" 译成"同时按两个键"，泛化成"两个键"。"两个方向键"更贴切，但原意可推，不构成错误。

### O034 · entry-03199

- **C08｜entry-03199｜已确认，沿袭上游描述。**  
  “always center on the player”与“始终以人物为中心”都没有说明地图边界限制。`M/class/Game.lua:726` 把玩家坐标和滚屏距离传给 `moveViewSurround()`；`E/Map.lua:899、909` 在边距足够大时计算居中坐标，但 `:929` 随后调用 `checkMapViewBounded()`，`:935–943` 会按地图边界修正，较小地图还会直接居中整张地图。因此靠近地图边缘等情况下，不能保证人物始终居中。译文没有新增此错误。

### O035 · entry-03201

**S7（entry-03201）｜仅建议**
- "show … on your currently playing profile" 意译为"让你的朋友在Discord上看见"，受众表述有变化但功能一致。
- "doesn't do anything in either state" 简化成"无效"，等价。

### O036 · entry-03203

#### claim-03203-1
- **条目**：[entry-03203](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L452-L495)
- **短引**：原文 `- Version checks: Addons will not be checked for new versions.` / 译文 `- 插件版本更新：无法更新插件的版本。`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`GameOptions.lua:672`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/GameOptions.lua#L672)（`generateListOnline` 中 `disable_all_connectivity` 选项说明）。该选项为“禁用全部网络连接”，此段为列举受其影响的各项功能。
- **问题内容**：前一项（`Easy addons downloading & installation`）中已明确说明玩家虽无法在游戏内一键下载，但“仍可手动安装”（`You may still do so manually. / 但仍可手动安装`）。本项“Version checks”特指客户端自动向远端发起的插件新版本在线检测机制。译文将其译为“- 插件版本更新：无法更新插件的版本。”，不仅混淆了“自动版本检测”与“更新插件”，更在逻辑上直接推翻了上一条允许手动更新安装的说明，向玩家传递了错误的限制事实。

### O037 · entry-03203

**C7（entry-03203）｜已证实｜翻译新增**
- 原文 "Version checks: Addons will not be checked for new versions."。
- 译文"插件版本更新：无法更新插件的版本。"把"不检查新版本"改成了"无法更新"。同一段已说明插件"仍可手动安装"，所以"无法更新"与原意不符，混淆了检查与更新。纯语义判断。

### O038 · entry-03203

**S8（entry-03203）｜仅建议**
- "info about new updates to the game" 译成"新闻"，稍泛化，但标题"游戏内新闻"一致。
- 列表后少一个空行、结尾警示段前多一个空行，属于排版差异，未造成信息结构丢失。

### O039 · entry-03203

- **C09｜entry-03203｜已确认，翻译新增。**  
  “Version checks: Addons will not be **checked for new versions**”译成“插件版本更新：**无法更新插件的版本**”，把版本检查改成更新操作，并扩大了禁止范围。`D/GameOptions.lua:671–672` 同时保留手动安装途径，又明确这一项说的是新版本检查；这两种操作不能混为一谈。依据是该选项说明内部明确区分的操作语境，不是对网络变量名的推测。

### O040 · entry-03203

- **C7｜entry-03203，已证实的译文语义差异。** 原文“Addons will not be **checked for new versions**”，译文“无法**更新插件的版本**”。检查新版与执行更新是不同操作；此处译文增加了无法更新的断言。该条目作为禁用联网选项的说明显示，见 `GameOptions.lua:664–685`；本次未沿更新器调用链核实其他更新途径。

### O041 · entry-03206

- **C10｜entry-03206｜已确认，翻译新增。**  
  “transitions”译成“渐变”，未准确表达这里的相邻地形过渡拼接。`D/GraphicMode.lua:84–89` 将选项写入 `tiles_custom_adv`；`M/class/Game.lua:633` 将其用于 `Map.tiles.nicer_tiles`。`M/class/NicerTiles.lua:77–80、684–721` 实际检查相邻地形类型，并选择边缘、外角和内角贴图，`:725–730` 用于水、草地和沙地等地形的衔接。这里涉及地形交界的贴图选择，而不是泛指颜色渐变。未另将“大型贴图”计为一个已证实的机制缺陷。

### O042 · entry-03206

- **C8｜entry-03206，已证实。** 原文“wide tiles”指定贴图的**宽度**特性；译文“大型贴图”改成笼统的尺寸大小。`GraphicMode.lua:76–89` 表明这是自定义贴图集的能力勾选项。

### O043 · entry-03209

- **C9｜entry-03209，已证实。** “Category points”译为“技能树解锁点”，会把点数用途限定为解锁技能树。相邻说明及消费逻辑还包括提升已知类别的精通度、购买刻印位，见 `LevelupDialog.lua:625–656、433–457、678–690`。

### O044 · entry-03210

#### claim-03210-1
- **条目**：[entry-03210](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L574-L597)
- **短引**：原文 `Some races or items may increase them as well.` / 译文 `某些种族和物品可以获得额外的点数。`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`LevelupDialog.lua:655`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/LevelupDialog.lua#L655)（`desc_types`，加点界面中技能树解锁点的机制说明）。
- **说明**：原文指部分特定种族特性（如柯纳克族开局奖励）或物品能够额外增加该类点数。译文“某些种族和物品可以获得额外的点数”在施受逻辑上略有瑕疵（字面将种族和物品作为获得点数的主体），但玩家在角色成长界面的语境下能明确理解其实际效果，未造成机制理解偏差，仅属句意流畅度润色建议。

---

#

### O045 · entry-03210

**C10（entry-03210）｜已证实｜沿袭上游描述**
- 原文/译文"在 10、20 和 34 级获得点数"。
- 实际（Actor.lua:3959-3961）：在 10、20、34 级获得，50 级以后每逢 (level-4)%30==0（64、94……）也会获得。
- 译文忠实复制了英文的遗漏，面向玩家的描述不完整，属上游问题。

### O046 · entry-03210

**C8（entry-03210）｜已证实｜沿袭上游描述，且译文加重**
- 原文 "learning it is automatic when using an inscription"；译文"你使用刻印时会自动消耗点数解锁"。
- 实际机制：`setInscription` 在没有空位时只是打开 `player-inscription` 对话（ActorInscriptions.lua:67-83）。对话里出现一个可选项 "Buy a new slot with one talent category point"，前提是 `inscriptions_slots_added < 2`、有未用点数、且不是同名替换（player-inscription.lua:42-46）。
- 升级界面的 Inscriptions 按钮（LevelupDialog.lua:678-692）也需要 yes/no 确认。
- 所以点数不会自动消耗。英文的"automatic"已经不准确，译文明确写出"自动消耗点数"，误述加重。
- 上限 5 与机制相符（`max_inscriptions` 默认 3 加 2，ActorInscriptions.lua:30-31）。

### O047 · entry-03210

**C9（entry-03210）｜已证实｜翻译新增（上游有遗漏）**
- 译文"每点提升 0.2"暗示同一技能树可以反复投点累加。
- 源码：`learnType`（LevelupDialog.lua:436-438）规定已知技能树只能提升一次（"You can only improve a category mastery once!"），每次 +0.2（LevelupDialog.lua:453）。
- 英文没写一次上限，但也没有按点累加的暗示；"每点"措辞会误导玩家。

### O048 · entry-03210

- **C10｜entry-03210，已证实。** 开头同样使用“技能树解锁点”；虽然下文列出其他用途，名称仍缩窄了这一点数的范围。消费逻辑同 C9。

### O049 · entry-03210

- **C11｜entry-03210｜已确认，沿袭上游描述，译文进一步明确了自动扣点。**  
  原文“learning it is automatic when using an inscription”，译文“使用刻印时会**自动消耗点数解锁**”，与实际玩家操作不符。`M/class/interface/ActorInscriptions.lua:66–85` 找不到空位时打开 `player-inscription` 对话；`M/data/chats/player-inscription.lua:42–49` 只有玩家选择购买新槽的答案后才扣点、增加槽位并安装刻印，`:52` 明确允许取消。另有 `D/LevelupDialog.lua:684–690` 的确认购买流程。因此使用刻印不会无条件自动扣点扩槽。

### O050 · entry-03210

- **C12｜entry-03210｜已确认，沿袭上游信息遗漏。**  
  原文和译文都只列出10、20、34级的点数来源。`M/class/Actor.lua:3959–3962` 的实际升级规则还包含 `level > 50` 且 `(level - 4) % 30 == 0` 的情况，即64、94级等继续获得点数。对于允许角色超过50级的情形，这份点数获取说明不完整；10、20、34这三个等级本身没有译错。

### O051 · entry-03210

- **P1｜entry-03210，待确认。** 原文说使用刻印时自动学会新刻印位，译文进一步说“使用刻印时会自动消耗点数解锁”。`LevelupDialog.lua:678–690` 能确认升级窗口另有**手动确认并消耗一点**的购买路径，却不足以排除使用刻印时还存在自动路径。缺少刻印使用流程的固定版本源码证据，因此不把这项疑点计为已证实问题。

### O052 · entry-03211

- **S03｜entry-03211。** `D/LevelupDialog.lua:773、1077` 填入的是 `unused_stats`。原文和译文都使用简短类别标签，在升级点数界面可以成立；对标签明确程度的偏好不足以认定信息错误。
