---

以下是基于本次冻结输入的**暂定参考判定，不是人工金标准**。共 40 条：**7 条 ISSUE、33 条 OK**；确认 13 个原子缺陷，另保留 1 个未决 claim。OK 包含纯措辞建议。

引文简称：`D/`＝`game/modules/tome/dialogs/`，`M/`＝`game/modules/tome/`，`E/`＝`game/engines/default/engine/`。源码版本均为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

| entry-ID | 判定 | canonical 缺陷 ID 或短依据 |
|---|---|---|
| entry-03172 | OK | `D/Birther.lua:93`：随机创建按钮，译义相符。 |
| entry-03173 | OK | `D/Birther.lua:423–424`：教程窗口中的 Basic 入口，“教程”有语境依据。 |
| entry-03174 | ISSUE | D01：泛指解锁说明变成当前选项的类型指认。 |
| entry-03175 | OK | `D/Birther.lua:964–969`：种族职业搭配的背景警示、仍可选择及可能错过任务均保留。 |
| entry-03176 | ISSUE | D02、D03、D04、D05。 |
| entry-03177 | OK | `D/Birther.lua:1388–1391`：进入捐赠窗口的按钮。 |
| entry-03178 | OK | `D/Birther.lua:1729–1732`：非捐赠者触发外观功能提示，译义相符。 |
| entry-03179 | ISSUE | D06：装备所属角色被译成观看者。 |
| entry-03180 | OK | `D/CharacterSheet.lua:89–96`：参数为分组、名称或类型排序；缩减空格无损。 |
| entry-03181 | OK | `D/CharacterSheet.lua:628–631`：显示并复制流浪者随机种子。 |
| entry-03182 | OK | `D/CharacterSheet.lua:643–648`：生命行中显示 `die_at`，“死亡底线”符合此标签语境。 |
| entry-03183 | OK | `D/CharacterSheet.lua:735–744`：显示治疗系数修正后的回复值；“加成”仅有措辞歧义。 |
| entry-03184 | OK | `D/CharacterSheet.lua:896–898`：双手武器标记，与后续武器类别拼接正常。 |
| entry-03185 | OK | `D/CharacterSheet.lua:951–959`：被缴械时追加禁用标签。 |
| entry-03186 | OK | `D/CharacterSheet.lua:1234–1238`：伤害亲和数据分区标题。 |
| entry-03187 | OK | `D/DeathDialog.lua:31–34`：死亡窗口标题及颜色标记相符。 |
| entry-03188 | OK | `D/DeathDialog.lua:224–225、350`：已登录时提供消息／聊天日志入口。 |
| entry-03189 | OK | `D/Donation.lua:44`；`D/DeathDialog.lua:174–185、340–345`：探索模式无限生命说明相符。 |
| entry-03190 | OK | `D/Donation.lua:44`：改变物品外观的功能标签，“幻化”符合此处语境。 |
| entry-03191 | OK | `D/Donation.lua:48–54`：劝捐关系和功能列表保留；句号与搭配问题属建议。 |
| entry-03192 | OK | `D/GameOptions.lua:107–114`及冻结相邻译文：明确限定为移动动画，越低越快。 |
| entry-03193 | OK | `D/GameOptions.lua:119–124`：移动、攻击时的小幅抖动效果。 |
| entry-03194 | OK | `D/GameOptions.lua:165–170`：战斗日志行数；Minimalist 的 `checkGameOption` 排除此项。 |
| entry-03195 | OK | `D/GameOptions.lua:217–227`及 `context.lua:451–456`明确解释开始消失前的停留时间；短标签有改进空间。 |
| entry-03196 | OK | `D/GameOptions.lua:335–365`：四种战术显示模式完整，标题限定列表范围。 |
| entry-03197 | OK | `D/GameOptions.lua:452–459`；`M/class/Game.lua:2573–2605`：前句已限定 WASD 移动键。 |
| entry-03198 | OK | `D/GameOptions.lua:462–469`：锐化值范围及 0 关闭相符。 |
| entry-03199 | ISSUE | D07：沿袭上游“始终居中”的无条件表述。 |
| entry-03200 | OK | `D/GameOptions.lua:495–502`：生命损失警告阈值，100 禁用。 |
| entry-03201 | OK | `D/GameOptions.lua:634–640`：角色实时状态、重启要求及不使用 Discord 时无效均保留。 |
| entry-03202 | OK | `D/GameOptions.lua:643–647`：在线保存角色资料、非完整存档及分享链接均保留。 |
| entry-03203 | ISSUE | D08：版本检查被改成更新操作。 |
| entry-03204 | OK | `D/GameOptions.lua:724–728`：穿斗篷时替换头部装备图像的条件保留。 |
| entry-03205 | OK | `D/GraphicMode.lua:83、88`；`M/class/Game.lua:632`：“纸娃娃”结合括注明确指装备外观显示。 |
| entry-03206 | ISSUE | D09：“wide”的宽度信息丢失；“transitions／渐变”另有未决 P01。 |
| entry-03207 | OK | `D/LevelupDialog.lua:89`：参数依次为角色名、等级。 |
| entry-03208 | OK | `D/LevelupDialog.lua:265–267`：当前等级限制属性继续增加。 |
| entry-03209 | OK | `D/LevelupDialog.lua:625–656`：四类点数区分完整；“解锁点”作为名称未明确断言唯一用途。 |
| entry-03210 | ISSUE | D10、D11、D12、D13。 |
| entry-03211 | OK | `D/LevelupDialog.lua:773、1077`：升级界面属性点计数标签，参数为 `unused_stats`。 |

确认的原子缺陷如下。同一条目的重复观察只对应同一个 D；不同信息遗漏分别编号。

| D-ID | entry | 内容、归因及证据 |
|---|---|---|
| D01 | entry-03174 | **翻译新增：指代及对象范围改变。** 原文泛指被锁定的战役、种族和职业；“解锁**这个**战役，种族，职业”将其绑定到当前选项。`D/Birther.lua:825–838、857–870`将同文追加到锁定的难度、死亡模式项，当前对象不一定属于译文指认的类型。这里确认的是指代错误，不是“一次同时解锁三类”的断言。 |
| D02 | entry-03176 | **翻译新增：评价对象扩大。** `D/Birther.lua:1379–1380`中 `this` 承接反复游玩、从错误及死亡中学习的设计；译文明确改为“**这款游戏**可能不会被所有人接受”，评价范围扩大。无需把该设计进一步等同于某一种具体永久死亡规则。 |
| D03 | entry-03176 | **翻译遗漏：不必重开。** `D/Birther.lua:1381`的 `without restarting` 未译出。“无限多的尝试次数”未明确保留继续原角色的条件。`D/DeathDialog.lua:340–345 → 252–253 → 174–185`走原角色复活流程，并对无限生命跳过扣次数。 |
| D04 | entry-03176 | **翻译遗漏：免费这一事实。** `D/Birther.lua:1384`的 `free game` 只剩“自娱自乐所做的一款游戏”；制作动机不能替代免费属性。 |
| D05 | entry-03176 | **翻译新增：原因与抱怨对象改变。** `D/Birther.lua:1384`表达现实有时艰难，因此作者欢迎游戏收入补贴家用。译文“不会再抱怨现实的诸多压力”改成停止抱怨现实，并通过“再”加入此前抱怨的意味。两者属于同一语义关系偏移。 |
| D06 | entry-03179 | **翻译新增：所属关系改成接收展示。** `D/CharacterSheet.lua:71–74`第二个参数来自 `self.actor:getName()`；`:364–390`切换该角色主／备用装备组的面板引用。“给 %s 看”将装备所属角色变成观看者。“装备未切换”正确保留，但不抵消此错误。 |
| D07 | entry-03199 | **沿袭上游：无条件的始终居中承诺不成立。** `D/GameOptions.lua:483`中英文均如此表述；`M/class/Game.lua:726`传入玩家坐标与滚屏距离，`E/Map.lua:898–917`计算居中位置后，`:929、934–943`仍强制修正地图边界，小地图还会居中整张地图。因此不能保证玩家始终处于中心。 |
| D08 | entry-03203 | **翻译新增：检查与更新混淆。** `D/GameOptions.lua:671–672`区分手动安装与检查插件新版本；译文“无法更新插件的版本”将“不检查”改为“不能更新”。这个缺陷由明确的操作语义即可证实，不依赖推定某个更新器的行为。 |
| D09 | entry-03206 | **翻译遗漏：宽度特征。** `D/GraphicMode.lua:79–89`为自定义贴图集能力选择；原文明确列举 `wide tiles`，译文“大型贴图”只保留笼统尺寸，丢失“宽”的具体属性。这里只确认词义信息损失，不推断实际像素宽度或覆盖格数。 |
| D10 | entry-03210 | **翻译新增：物品的施受关系改变。** `D/LevelupDialog.lua:655–656`说某些种族或物品能够增加该类点数；“某些种族和物品可以获得额外的点数”把物品写成获得点数的主体。“种族”可以借指相应角色，但“物品”这一并列分支的关系没有正确表达，不能仅凭玩家可猜出原意降为润色。 |
| D11 | entry-03210 | **沿袭上游：高级别点数来源遗漏。** `D/LevelupDialog.lua:655`中英文仅列 10、20、34 级。`M/class/Actor.lua:3949–3962`在正常发放升级点数的分支，还对 `level > 50` 且 `(level - 4) % 30 == 0`发放一点，即 64、94 级等。此结论限定于能达到这些等级且走该发放分支的角色，不表示所有战役都可升到这些等级。 |
| D12 | entry-03210 | **沿袭上游，译文进一步明确错误：自动扩槽／扣点。** `M/class/interface/ActorInscriptions.lua:66–85`无空位时打开对话；`M/data/chats/player-inscription.lua:42–49`只有选择购买答案才扣点、扩槽并安装刻印，`:52`允许取消。`D/LevelupDialog.lua:684–690`的另一入口也需要确认。原文自动学习新槽的说法失准，译文“自动消耗点数解锁”进一步明确了错误操作。 |
| D13 | entry-03210 | **沿袭上游：同一类别精通度只能增强一次的限制遗漏。** `D/LevelupDialog.lua:436–438`明确阻止第二次增强，`:452–457`显示允许时增加 0.2 并消耗一点。原文和译文的用途说明均未交代这一限制。确认的是限制遗漏；“每点提升 0.2”本身符合一次合法投入的增量，不单独证明可无限重复投入。 |

52 条匿名观察逐项裁决如下。状态表示本次核验结果，不沿用观察原来的自我评级。

| O-ID | 状态 | 命中的 D | 具体证据与理由 |
|---|---|---|---|
| O001 | mixed | D01 | **confirmed**：泛指复数变成“这个”的指代问题；难度和死亡模式消费位置见 `Birther:838、870`，不能降为纯风格。**advisory**：逗号、口语化等独立措辞部分。 |
| O002 | confirmed | D01 | 当前项还可能是难度或死亡模式，类型指认错误成立。“条件”概括行动不另计缺陷。 |
| O003 | confirmed | D01 | `Birther:826–838、858–870`直接支持作用对象并非总是战役、种族或职业。 |
| O004 | mixed | — | **advisory**：“完成条件”搭配生硬，但以达成条件概括解锁行动可以成立。**refuted**：并列三类内容不等于承诺一次同时解锁三类；源码逐项生成不能证明该数量断言。不给它借用 D01 命中。 |
| O005 | advisory | — | `Birther:964–969`是背景搭配警示；“剧情”不如“背景设定”精确，但警示关系和可能错过任务均保留。 |
| O006 | refuted | — | 探索模式窗口提到另一项捐赠福利，不自动构成机制错误；`Birther:1387`本来就说明自定义贴图也是福利。`:1385、1401`同文只能证明重复，不能证明复制方向，更不能单凭窗口主题确认事实错误。 |
| O007 | mixed | D02 | **confirmed**：`this`被扩大为整款游戏。**refuted**：把其唯一、明确地解释成“高惩罚性永久死亡机制”超出 `Birther:1379–1380`实际表述；原句谈的是反复游玩和从错误、死亡中学习的设计。 |
| O008 | confirmed | D04 | `Birther:1384`明确有 `free`，冻结译文没有相应信息。 |
| O009 | confirmed | D05 | 欢迎收入及其原因，被改成不再抱怨现实，语义关系确有变化。 |
| O010 | confirmed | D03 | `without restarting`没有相应译文；复活原角色的调用链进一步支持该条件的重要区别。 |
| O011 | confirmed | D02 | 指代范围变化由 `Birther:1379–1380`连续语境支持。 |
| O012 | advisory | — | “从错误中学习”仍传达学习成长语境，`if they wish`可由允许式表达承接，“觉得游戏很好”也已译出；可作措辞建议。存续句移行无损。贴图句没有因出现在该窗口而成为已证机制错误；“复制而来”的历史归因未获证明。 |
| O013 | confirmed | D02 | 与 D02 同一指代范围缺陷，合并计数。 |
| O014 | confirmed | D03 | `DeathDialog:340–345、252–253、174–185`支持原角色复活及无限生命不扣次数。 |
| O015 | confirmed | D04 | “自娱自乐”不能替代“免费”，遗漏成立。 |
| O016 | confirmed | D05 | “现实艰难”由原因变成抱怨对象；“再”也加重了该偏移，合并为同一缺陷。 |
| O017 | confirmed | D02 | 同一语境中的评价对象扩大，未另计新缺陷。 |
| O018 | confirmed | D03 | 无需重新开始的条件确实遗漏。 |
| O019 | mixed | D06 | **confirmed**：所属角色变观看者。**advisory**：“套装”可能引起联想，但并不必然声明套装奖励机制。另须纠正其源码解释：`:364–390`是主／备用装备组，每组都可含主手、副手等槽位，并非只在左右手间切换。 |
| O020 | mixed | D06 | **confirmed**：所属关系错误。**advisory**：“套装”可考虑明确化；不另计的依据是此处缺乏确定的额外机制断言，不能仅因相邻旧译也如此就豁免。 |
| O021 | confirmed | D06 | 第二个参数为角色名，第一参数控制面板装备组；“装备未切换”不抵消关系错误。 |
| O022 | confirmed | D06 | `CharacterSheet:62–79、364–390`支持只更新该角色装备组的显示引用。 |
| O023 | advisory | — | 系数低于 1、结果可能降低属实；但“治疗系数加成后”在此完整数值语境可指应用修正，没有明确承诺结果必增。 |
| O024 | advisory | — | 接受其计算事实，不接受据此直接推出已证错译。`CharacterSheet:735–744`同时显示系数及结果；“加成”存在方向性歧义，尚不足以等同“只会增加”。 |
| O025 | advisory | — | 冻结译文“希望得到你的帮助”末尾确少句号，但换行仍保留句子与段落结构。 |
| O026 | mixed | — | **advisory**：“值得投入这些时间”被压缩成快乐体验，劝捐语境仍成立。**refuted**：“第三段末尾缺句号”不符输入，末尾实际为 `%s。`；缺句号处在第二段第一句。`Donation:54`支持列表参数消费正常。 |
| O027 | advisory | — | “我最衷心的希望”等搭配欠自然，`Donation:48–54`的主要语义关系仍完整。 |
| O028 | advisory | — | `GameOptions:107–114`明确数值越高移动越慢；括注与相邻说明已解释数值方向。 |
| O029 | advisory | — | 冻结相邻译文明确限定生物、抛射物移动，“动画速度”没有在完整语境中宣称控制全部动画。 |
| O030 | advisory | — | `LogDisplay:270–274`的 t 秒开始、2t 秒完全透明判断正确。但 `context.lua:451–456`已明确写“开始消失之前的停留秒数”；不能把短标签唯一解释为完全不可见的时刻。属于明确性建议。 |
| O031 | advisory | — | 同上。实际等待时间和 0 的意义已有明确相邻说明；其“会被理解为完成消失”的判断不足以证明固定语境中的错误断言。 |
| O032 | advisory | — | 标题已限定战术信息，四项模式与 `GameOptions:336–360`对应，省略重复“战术”没有丢失列表范围。标记保留。该观察未核实快捷键，也未提出有证据的绑定错误。 |
| O033 | advisory | — | “两个键”由前句 WASD 移动键承接。`Game:2575–2578、2602–2605`确实合成垂直、水平移动方向；没有证据要求将译文读成任意键组合。 |
| O034 | confirmed | D07 | 居中计算之后仍执行边界修正；中英文“始终”均遗漏限制，归为沿袭上游。 |
| O035 | advisory | — | “让朋友看见”未明确排除其他受众；角色实时状态及重启条件仍在。“无效”对应不使用 Discord 时两种设置都不起作用。 |
| O036 | confirmed | D08 | 检查新版本与更新插件不同；`GameOptions:671–672`已明确区分。仅确认这个语义错误，不据此声称穷尽验证了所有手动更新路径。 |
| O037 | confirmed | D08 | “不检查新版本”被改成“无法更新”，纯语义证据充分。 |
| O038 | advisory | — | “新闻”在该游戏内新闻列表项中可成立；空行改变没有合并、隐藏列表或警示层级。 |
| O039 | confirmed | D08 | 同一操作语义错误；手动安装与版本检查的相邻区分支持判定。 |
| O040 | confirmed | D08 | 其限定为译文语义差异是充分且恰当的，不需要先核实所有更新途径。 |
| O041 | pending | — | **P01**：`NicerTiles:684–730`证明该功能选择相邻地形的边缘和角落贴图；但这不能单独证明最终视觉过渡不含渐变，也不能直接将译文解读成特指颜色渐变算法。缺少实际相关视觉效果证据，暂不确认。 |
| O042 | confirmed | D09 | `wide`明确传达宽度；“大型”未保留该属性。确认词义信息损失，不外推像素尺寸机制。 |
| O043 | advisory | — | `LevelupDialog:433–457、678–690`确有增强精通、购买刻印位用途。但“技能树解锁点”在这里是资源名称，未明说“只能解锁”；不足以直接确认为用途排他断言。 |
| O044 | confirmed | D10 | 改判为缺陷。种族可借指相应角色，但将物品写成获得点数的主体，改变了 `LevelupDialog:656`中物品增加角色点数的关系。 |
| O045 | confirmed | D11 | `Actor:3949–3962`支持条件性的 64、94 级等额外来源；须保留正常升级发点与能达到该等级的适用条件。 |
| O046 | confirmed | D12 | 无空位后进入选择对话，购买答案才扣点，取消可用；自动扣点说法不符。默认 3 槽加最多购买 2 槽支持通常上限 5，不外推所有特殊效果。 |
| O047 | mixed | D13 | **confirmed**：它明确指出的“一次上限未写出”成立，且原文、译文均遗漏。**refuted**：“每点”本身必然暗示同一树可反复累加；合法投入确实每点增加 0.2。D13只对应限制遗漏，不将“翻译新增无限重复”的推断算命中。 |
| O048 | advisory | — | 同 O043。完整段落直接列出三种用途，更不足以将名称中的“解锁”解释成只能用于解锁的机制断言。 |
| O049 | confirmed | D12 | `ActorInscriptions:66–85 → player-inscription:42–52`给出购买、扣点及取消的完整证据。 |
| O050 | confirmed | D11 | 高级别增发分支存在，限定于适用情形；10、20、34 三个等级本身没有译错。 |
| O051 | confirmed | D12 | 原先证据缺口已补齐：不仅查看升级界面，还核实使用刻印后的对话购买流程，足以把该疑点升级为 confirmed。 |
| O052 | advisory | — | `LevelupDialog:773、1077`确实填入 `unused_stats`；升级点数界面的简短类别标签可成立，明确程度属建议。 |

尚未解决的是 **P01（entry-03206／O041）**：源码足以确认相邻地形拼接机制，却不足以单凭实现方式排除最终画面的渐变效果。本次没有读取图像资产，也没有进行渲染验证。该条因另有 D09，整体仍为 ISSUE。

其余分歧已作暂定裁决，尤其是：

- “消失时间”结合明确相邻说明，暂按建议；没有把它必然解释成完全透明的时刻。
- “加成”“套装”“技能树解锁点”没有被直接等同于排他的机制断言。
- “每点提升 0.2”与每类别一次的上限分别判断：前者没有独立证实错误，后者确有遗漏。
- 重复的贴图提示不能证明复制方向，也不能仅凭出现于探索模式窗口就确认为机制误述。

实际读取范围如下。冻结文件以本次入口提供的快照为版本；七份冻结源码的 SHA-256 **全部匹配** `source-access.json`。下列 `P` 是完整绝对目录：

```text
P = /home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923
```

| 实际读取文件（相对 P，逐项列全） | 版本／用途 |
|---|---|
| `ADJUDICATION-INPUT.md` | 本次唯一入口、52 条匿名观察及最新临时文件授权 |
| `protocol-v2/INPUT.md` | 冻结规则、40 条原译文及术语子集 |
| `protocol-v2/entries.json` | 冻结条目身份、文本、参数元数据 |
| `protocol-v2/context.lua` | 唯一相邻译文来源 |
| `protocol-v2/source-access.json` | 固定 commit 与七份源码哈希 |
| `protocol-v2/sources/game/modules/tome/dialogs/Birther.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/CharacterSheet.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/DeathDialog.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/Donation.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/GameOptions.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/GraphicMode.lua` | 固定源码，哈希匹配 |
| `protocol-v2/sources/game/modules/tome/dialogs/LevelupDialog.lua` | 固定源码，哈希匹配 |

额外源码均通过 `/workspace/t-engine4` 的单文件 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取，没有读取源码工作树或其他 commit。

| 完整源码对象路径 | 已读材料中的引入依据 |
|---|---|
| `game/modules/tome/class/Game.lua` | `GameOptions:459`的 `game:setupWASD()`、滚屏设置；`GraphicMode:61`的 `game:setupDisplayMode()` |
| `game/modules/tome/class/Actor.lua` | `LevelupDialog`的 `self.actor`、升级点数及刻印槽成员；`CharacterSheet`的 `die_at` |
| `game/modules/tome/class/interface/ActorInscriptions.lua` | `Actor:37、62、295`的 require、继承与初始化 |
| `game/modules/tome/data/chats/player-inscription.lua` | `ActorInscriptions:60、82`的 `Chat.new("player-inscription", …)` |
| `game/modules/tome/class/NicerTiles.lua` | `Game:40`的 require，与 `:633`的高级贴图设置消费 |
| `game/engines/default/engine/Map.lua` | `Game:31`的 require，与 `:726`的 `moveViewSurround()` |
| `game/engines/default/engine/LogDisplay.lua` | `GameOptions:226`的 `logdisplay:enableFading()`；后由 Minimalist 的实例化确认 |
| `game/modules/tome/class/uiset/Minimalist.lua` | `Game:457`的默认 UI require；`:27、478–481`确认 LogDisplay 实例及淡出设置 |

覆盖静态核对确认：40 个 entry-ID、52 个 O-ID 均连续且无重复；40 条的占位符及显式颜色／字体标记顺序一致。未运行 Lua 或渲染测试，未创建子代理，未写仓库或临时文件，未读取 host-only 映射、原始报告、STATE 或模型身份；未发现读取越界。
