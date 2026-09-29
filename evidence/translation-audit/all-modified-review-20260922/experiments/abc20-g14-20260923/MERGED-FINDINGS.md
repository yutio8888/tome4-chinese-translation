# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的57项观察及独立盲审的25项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03693 | C01（原建议） | C01（原问题） | C01（原建议） | 翻译新增遗漏：`promptly` 的迅速、立即意味未在“吃下了”中表达。CultsDLC:350–354，寄生兽替换选项；不据此推断游戏耗时。 |
| D02 | entry-03694 | C02（原建议） | C02（原问题） | C02（原建议） | 同类遗漏，独立覆盖艾琳条目。CultsDLC:355–359。 |
| D03 | entry-03697 | C03（原问题） | C03（原问题） | C03（原问题） | 翻译新增遗漏：`Myssil of Zigur` 丢失所属关系。Game:59；标题及废墟位置没有表达写信者的所属。 |
| D04 | entry-03697 | C04（原建议） | C04（原问题） | 未提出此缺陷 | 翻译新增强化：`From what the scouts can tell` 变成“侦察员看见”，增加亲眼目击的证据性质。Game:63；“可能”只修饰实验目的。 |
| D05 | entry-03697 | C05（原建议） | 未提出此缺陷 | 未提出此缺陷 | 翻译新增语义变化：`grave news` 说明消息严重，“令人震惊”改为接收者的惊讶反应，两者不等价。Game:61–63。 |
| D06 | entry-03697 | C05（原建议） | 未提出此缺陷 | C04（原问题） | 翻译新增遗漏：对死灵法师的贬称 `filth` 消失。Game:66；前文“肮脏的奥术势力”修饰不同对象，未补回此处侮称。 |
| D07 | entry-03714 | 未提出此缺陷 | 未提出此缺陷 | C06（原建议） | 翻译新增遗漏：`all their damage` 只剩“伤害”，失去明确的全范围限定；不据此声称译文限定为物理伤害。orc:115、125；本体 talents/misc/races:731 → timed_effects/mental:2007 的 `inc_damage={all=eff.power}`。 |
| D08 | entry-03729 | C09（原问题） | C07（原问题） | C09（原问题） | 翻译新增缩窄：`lumps of metal` 变成“铁块”。aaf:47；APE:28–29 同样泛称金属及矿块。无需依赖具体各级材料名称即可确认。 |
| D09 | entry-03729 | C13（原建议） | C08（原问题） | C09（原问题） | 翻译新增泛化：材料语境的 `herbs` 变成“植物”，丢失草药类别。aaf:47；Actor:304–308 为辅助快照证据。 |
| D10 | entry-03729 | C10（原问题） | C09（原问题） | C07（原问题） | 翻译新增遗漏：`which are used to craft tinkers` 无对应译文。aaf:47；APE:29、PartyTinker:81–83、114–117 辅助说明制造材料的用途与消费。 |
| D11 | entry-03729 | C11（原问题） | 未提出此缺陷 | C08（原问题） | 翻译新增遗漏：未说明在 `when you destroy items` 的操作中选择处理工具。aaf:49 的加粗说明；前句介绍分解用途不等于保留这一操作适用条件。 |
| D12 | entry-03730 | C15（原建议） | C11（原问题） | C12（原问题） | 翻译新增遗漏：刻字位于一串钥匙中的 `one` 把这一所属限定消失。destructicus-lead:21。译文并未明确断言每把都有字。 |
| D13 | entry-03730 | C15（原建议） | 未提出此缺陷 | C12（原问题） | 翻译新增细节遗漏：`etched` 的刻制方式未保留于“写着”。destructicus-lead:21；不反向断言译文一定指用笔书写。 |
| D14 | entry-03730 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | 翻译新增遗漏：`just south` 的近处定位只剩“南边”。destructicus-lead:22。 |
| D15 | entry-03731 | C17（原建议） | 未提出此缺陷 | C13（原问题） | 翻译新增误译：`whirrs to life` 是伴随嗡鸣启动，译为“启动了它的生命”，同时丢失声音信息。destructicus:30、37，明确为机械装置。 |
| D16 | entry-03731 | C17（原建议） | C13（原问题） | C13（原问题） | 翻译新增遗漏：`slightly rotating underneath you` 的旋转、幅度与空间关系，被笼统“开始运转”替代。destructicus:37。 |
| D17 | entry-03731 | C17（原建议） | 未提出此缺陷 | C14（原问题） | 翻译新增具体化：`beaded panel` 被译作“珍珠板”，把珠状构造具体化为珍珠。destructicus:37 的显示针说明不支持该材质判断。 |
| D18 | entry-03731 | C16（原问题） | C14（原问题） | C14（原问题） | 翻译新增动作变化：面板滑至玩家面前，译成“从你前方滑过”。destructicus:37、44–53；后续继续观看并切换该面板目标。 |
| D19 | entry-03731 | C17（原建议） | C15（原问题） | C15（原问题） | 翻译新增遗漏：显示针 `pushing out and pulling back` 只剩伸出，丢失回缩动作。destructicus:37。 |
| D20 | entry-03732 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | 翻译新增具体化：再次把同一 `beaded panel` 译成“珍珠面板”。destructicus:37、46。 |
| D21 | entry-03732 | C19（原问题） | C16（原问题） | 未提出此缺陷 | 翻译新增遗漏：`Steam Giant families` 变成无家庭关系限定的“蒸汽巨人们”。destructicus:46、48 的撤离叙事。 |
| D22 | entry-03732 | C19（原问题） | 未提出此缺陷 | 未提出此缺陷 | 翻译新增动作泛化：`huddle` 的聚拢、挤成团动作变成“拥挤”状态；哭泣保留。destructicus:46。 |
| D23 | entry-03732 | C21（原建议） | 未提出此缺陷 | 未提出此缺陷 | 翻译新增动作变化：`pans around the cabin` 是在舱内扫视，译成切换到船舱。destructicus:46，此前已经显示飞船内部。 |
| D24 | entry-03732 | C20（原问题） | C17（原问题） | C17（原问题） | 翻译新增身份遗漏：`crew members` 只剩“成员”。destructicus:46 在家庭、守卫之后另述船员，不能把船上所有成员视为船员。 |
| D25 | entry-03732 | C20（原问题） | 未提出此缺陷 | C17（原问题） | 翻译新增路径变化：`hurrying between` 两个舱室变成“走过”两处。destructicus:46；不额外要求原文必然表示多次往返。 |
| D26 | entry-03732 | C18（原问题） | C18（原问题） | C16（原问题） | 翻译新增替换：`near nothing of importance` 的周围无重要事物，变成“无害地飞舞”的行为评价。destructicus:50；52–53 给出两个射击对象。 |
| D27 | entry-03732 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | 翻译新增语义变化：`would have little effect` 的影响有限变成“没什么意义”的价值判断。destructicus:50；后面的炫耀威力和低伤害描述没有完整保留前一命题。 |
| D28 | entry-03732 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | 独立补充遗漏：`pausing to take worried glances` 包含奔忙中停下来张望，译文“偶尔忧虑地瞥向”只表达频率，未保留停下动作。destructicus:46。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O016 | Gemini C04（原问题） | entry-03697 | mixed | confirmed：`filth` 贬称消失；advisory：`True Wrath` 的强调可由整句愤怒表达承载，不独立计 D。 |
| O017 | Opus C05（原建议） | entry-03697 | mixed | confirmed：严重消息变为震惊消息、侮称遗漏；advisory：`True` 的修辞强调。 |
| O018 | Sol C05（原问题） | entry-03698 | refuted | context:130–146 已交代玩家通过仓库存放服务器物品；“需要你存储”不足以证明注册绑定之外新增独立手动操作。主体表达可更精确，但所述误导未证实。 |
| O019 | 独立盲审 C05（原待确认） | entry-03699 | pending | P01；context:162、167、170 有在线／离线语境，缺字符串实际调用分支。 |
| O020 | Sol C06（原待确认） | entry-03699 | pending | P01；不能仅因同文件含离线日志便断定此提示用于离线。 |
| O021 | Opus C06（原待确认） | entry-03699 | pending | P01；items-vault 源码明确不可用。 |
| O022 | Gemini C05（原建议） | entry-03704 | advisory | special:136–159 与邻近成就名支持文化引用讨论；直译本身成立，不把具体电影归属当缺陷证据。 |
| O025 | Opus C07（原建议） | entry-03719 | advisory | whitehooves:118；末尾句号不改变列表内容。获准天赋文件能确认三个英文名称，未发现具体译名冲突证据。 |
| O026 | Opus C08（原建议） | entry-03728 | advisory | aaf:25–28、35；两类技能、两项天赋及 `npc.name` 对应，逗号属排版。 |
| O036 | Gemini C09（原问题） | entry-03729 | mixed | confirmed：金属缩成铁、草药泛化；pending：具体钢／矮人钢／沃瑞钽及注射药剂用途旁证未核实，见 P03。 |
| O038 | Sol C10（原问题） | entry-03729 | pending | P02；APE:45–62 确有背包标记与地面两步检查，目标版本适用性缺证。 |
| O040 | Gemini C10（原问题） | entry-03729 | mixed | refuted：“APE 不能称内部存物”的前提被 APE:28、41、76 的界面用语反证；pending：地面及确认分支适用性见 P02。背包有物品也不等于有 `__transmo` 物品。 |
| O041 | 独立盲审 C11（原问题） | entry-03729 | advisory | aaf:49 保留了通过使用来设默认的操作目的；译文没有明确写“自动、无需确认”。APE:55–57 的弹窗可支持更精确说明，不能仅据“则”认定排除了确认。 |
| O042 | Opus C11（原问题） | entry-03729 | mixed | confirmed：销毁物品的操作情境遗漏；advisory：在明确二选一语境下，“需要／可以”的措辞差异不另计缺陷。运行前提适用性仍见 P02。 |
| O043 | Opus C12（原问题） | entry-03729 | pending | P02；快照的地面检查属实，但不能直接提升为目标版本已确认机制错误。 |
| O044 | 独立盲审 C12（原待确认） | entry-03729 | pending | P02；版本缺口判断正确，多工具前提也是英文未详述的内容。 |
| O045 | Opus C13（原建议） | entry-03729 | mixed | confirmed：草药类别泛化不能降为偏好；refuted：`infusions` 译“纹身”构成问题的可能性，没有支持。其局部 C 编号不用于跨观察归并。 |
| O046 | Sol C11（原问题） | entry-03730 | mixed | confirmed：“其中一把”限定遗漏；refuted：“上面”必然断言整串每把都有刻字，译文未作该排他断言。 |
| O047 | Gemini C11（原问题） | entry-03730 | advisory | destructicus-lead:23；漏句末感叹号未破坏句法或标记闭合，不足以证明错误显示。 |
| O048 | Sol C12（原问题） | entry-03730 | advisory | destructicus-lead:21 的急切等待语境下，“焦急”可表达迫切等待；未充分证明新增独立忧虑事实。 |
| O049 | Gemini C12（原问题） | entry-03730 | mixed | confirmed：特定钥匙限定及刻制细节丢失；advisory：eagerly／焦急的情绪措辞。 |
| O051 | Opus C14（原建议） | entry-03730 | advisory | 观察已承认“焦急等待”的急切用法；可作语气优化。 |
| O053 | Opus C15（原建议） | entry-03730 | mixed | confirmed：刻字所属和方式遗漏；advisory：“应该”已保留建议语气，不要求逐译 probably；感叹号属排版。 |
| O063 | Opus C17（原建议） | entry-03731 | mixed | confirmed：前四组具体语义偏差；advisory：“磁力／电磁力量”的措辞不据现有语境判错。标记及专名核对通过。 |
| O073 | Gemini C18（原问题） | entry-03732 | advisory | 原译仍有换行，句子和论述顺序完整；少一个空行不足以证明信息结构或渲染损坏。 |
| O077 | Opus C21（原建议） | entry-03732 | mixed | confirmed：舱内扫视变成切换地点；advisory：空行及小鬼“他／它”不构成已证显示或指代错误。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
