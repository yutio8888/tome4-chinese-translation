# 修复窗口 66：第二轮重新复审确认项（25 条）

Paseo MCP / schema5 translation_contextual_v2 implement。基线 54134089aad99e0dfcb4be249063b86f56e0530d。

## 来源

- 2026-10-05 用户在 C 档润色后要求“再走一轮生产复核”：迁移 87fb6882 排入的 494 个 successor 已于第397–403批全部审完。
- 第397–403批宿主确认 16 条（397：2、398：2、399：1、400：3、401：3、402：4、403：1）；第398–402批宿主补充 9 条换行不变量修复（不计积压，见各批 HOST-FINAL-DECISIONS.json 的 additional_host_observations）。
- 审核队列清空时积压未达 20 条阈值，2026-10-05 用户选择“修完后再发一个插件版本”。

用户已授权修复、提交与推送，以及修复后发布插件新版本；max_cycles=5（用户 2026-09-25 授权）。

## 写入权限

唯一 EXECUTOR 仅可修改以下内容：

- WORKSET.json 列出的 25 个 target（mod-tome.lua 14 条、tome-ashes-urhrok.lua 2 条、tome-cults.lua 5 条、tome-orcs.lua 4 条）；
- `evidence/quality/repair-window-66-20261005/` 下的修复证据。

不得修改：source、source_tag、section、args_order、运行键、其他译文、术语库、规则工具或旧证据。

不得 stage、commit、push，不得创建 agent，不得修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

## 改写要求

按 NEW-TARGETS.json 中每条的 new_target 整条替换现有 target（宿主已按各条“修复：”与整句对照写定全文；old_target 为现值）：

- 11 条换行修复（0eb305a353、520cfc1133、75061b0aa7、a32121c7fd、9be1dc5a72、a6af085c45、d15beb86fb、d7bd95ff10、ea56758108、f901245fba、7eb1dc011b）的 LF 结构须与原文一致；
- 其余 14 条保持现有 LF／`\t` 结构不变；48267a1ec3 第二处“太阳骑士”改用单引号、f01b17c6a1 补回外层左引号“，改后引号须配对；
- 所有 `%d`、`%0.1f`、`%s`、`%%` 等占位符，`#COLOR#`、`#{italic}#` 等标记与 `@name@` 令牌保持不变；source_tag 不变。

## 验证要求

- 用 LuaJIT 加载 mod-tome.lua、tome-ashes-urhrok.lua、tome-cults.lua 与 tome-orcs.lua，证明恰 25 个 target 变动、其他记录不变；
- 执行 strict lint 及 git diff --check。

无需完整门禁，宿主在独立复审后统一运行 17 项。

## 取证范围

- 主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；Ashes、Cults、Orcs 公开源码在 /workspace/tome4-dlcs/{ashes-urhrok,cults,orcs}（仓库与 commit 未固定）。
- 不扫 `/`、`/workspace` 或无关目录。

## 审查安排

- cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）。
- 收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。
- v2 FINAL 有任何 ISSUE 时，先修复并完成 RE_REVIEW，再重新 FINAL。max_cycles=5。
- reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。

## 宿主裁决依据

与已记录用户裁决相冲的指摘，宿主按裁决驳回（如 The Master＝领主）。与本窗口修改无关的既有问题记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 0eb305a353e1d3b60888ab11f9ce72d923ed8ff14d93a2b8f34bf19d6cb607e3 | mod-tome.lua | mod-tome/data/lore/ardhungol.lua | 公开源码 game/modules/tome/data/lore/ardhungol.lua@624a6732 第 66 行起日志第七篇（Journal Entry VII）为单一段落，篇内无换行；现译在“这根本不可能。”与“除此之外”之间插入一个 \n，整条 LF 由源文 10 个变为 11 个，破坏换行不变量（surface 与 contextual 均指出）。修复：删去该 \n，两句直接相接，文字不变。 contextual 同判。
- 1f7428b354dc7e4cc836a6df60bcba60bba40bb00ad757bfc3695e6185eeb07a | tome-cults.lua | tome-cults/data/lore/kroshkkur.lua | Cults 公开源码（来源未固定，/workspace/tome4-dlcs/cults） tome-cults/data/lore/kroshkkur.lua:125 起厄格莫斯：“alter nature itself to stave off civilisation, creating various plants and guardians to prevent sapient races from plundering its forests”意为改变自然来抵御文明，现译“改变自然来避让文明”意思相反，并与后半句“防止智慧种族掠夺森林”矛盾（surface 指出）。修复：“改变自然来避让文明”改为“改变自然本身来抵御文明”。
- 201a4359ecaa658001e80ac1f08f2c0690a0045082ecab98482ebd6f295b0e14 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | Ashes 公开源码（来源未固定，/workspace/tome4-dlcs/ashes-urhrok） tome-ashes-urhrok/data/lore/demon.lua:444 起 S 的留言：①“a whole lot of blathering about his accomplishments as a naturalist, and his mysterious disappearance”的主语是碑文（The text here），现译“只不过是一个博物学者喋喋不休地讲述他的成就和谜一般的失踪”变成博物学者本人讲述自己的失踪，逻辑矛盾；②“your inevitable agonizing fate WILL end in death”的 agonizing 译成“可悲”，丢了极度痛苦，也丢了 WILL 的强调；③surface 指出“a couple of weeks”译“几周”过泛，宿主认为可一并改准（contextual 报①②，surface 报③）。修复：①改为“只不过是在絮叨一个博物学者的成就和他谜一般的失踪”；②改为“你们无法逃避的痛苦命运必将以死亡告终”（以“必将”体现强调，不加标记）；③“最多只要几周的时间”改为“最多不过两周左右”。 contextual 同判。
- 21521189525d61124b4850bc016700e3a1c74437cd0652cda346d92046b10acb | tome-orcs.lua | tome-orcs/data/lore/misc.lua | Orcs 公开源码（来源未固定，/workspace/tome4-dlcs/orcs） tome-orcs/data/lore/misc.lua:24 起天文学家日志（sunwall-observatory-1）第二段：“If the last century is any indication, the rate of disappearances is accelerating”以过去一个世纪的情况为据推断消失在加速；现译“根据这个世纪以来的记录”把时间范围改成本世纪开始以来（surface 指出，contextual 判 OK；宿主按原文核对，时间范围确实不同）。修复：改为“从过去一个世纪的情况来看，星星消失的速度正在加快……”，同时保留原文的推断语气。
- 48267a1ec3569a224cc2cd4814a96d84982dc2b1a34ed24b896b616727f218d6 | mod-tome.lua | mod-tome/data/lore/ardhungol.lua | 公开源码 game/modules/tome/data/lore/ardhungol.lua@624a6732 第 77–78 行纸片：'sun paladin' 两次都用单引号；现译第一处为‘太阳骑士’，第二处写成外层“…”内的“太阳骑士”，形成双引号嵌套且前后不一致；另“next step … should be cleaning”的 should 被删，“移民计划的下一步是清理”把建议说成既定（删限定词，同类先例见 dropped-modal 记录）。surface 与 contextual 均指出。修复：“清理本地的“太阳骑士”巢穴”改为“清理本地的‘太阳骑士’巢穴”，“下一步是清理”改为“下一步应当是清理”。 contextual 同判。
- 520cfc1133e8756497cb19d7d0f707a6e8f9c4a300d46356bb1d6f0bd93a72ec | mod-tome.lua | mod-tome/data/lore/angolwen.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/angolwen.lua@624a6732 第 73–78 行沃利尔大法师手记：原文“From the desk of Archmage Varil,”后只有 1 个 \n，现译“大法师沃利尔书，”后为 \n\n，整条 LF 由 5 个变为 6 个，违反换行不变量。surface lane-000-0 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：删去“大法师沃利尔书，”后多出的一个 \n，文字不变。
- 66551a698767e8280fc10a8a61f738d7e50fd314ddd99c5cf220f33a869281ba | mod-tome.lua | mod-tome/data/lore/angolwen.lua | 公开源码 game/modules/tome/data/lore/angolwen.lua@624a6732 第 50–66 行《魔法究竟是什么？》：“The true archmage is interested in the interactions of the elemental forces of the world”指元素之力彼此间的相互作用，现译“专注于元素之力是如何影响这个世界的”改成元素之力对世界的影响，研究对象与作用关系都变了（surface 与 contextual 均指出）。contextual 另指出同条三处偏差，宿主核对属实，修复时按整条一并处理：“are we not natural creatures that use it?”是反问（我们本就是运用魔法的自然生物），现译“为何不能去尝试运用它？”丢了论证；“Plumes of fire”译“火焰烟柱”，烟柱指烟；“a powerful force that can be used for good or ill”压成“一柄双刃剑”，丢了 powerful force。修复：该句改为“真正的大法师关注的是世间元素之力彼此间的相互作用，并操纵它们为己所用。”；反问改为“我们不也正是运用它的自然生物吗？”；“火焰烟柱”改为“火柱”；末段改为“但你们要谨记，魔法仍是一股强大的力量，既可用于行善，也可用于作恶。作为工具它确实有着极大的价值——明智地使用它。” contextual 同判。
- 75061b0aa752535cbe764bfa8edd6f81b994ffa33b7fe1355e180fcb2e6d3f32 | mod-tome.lua | mod-tome/data/lore/fun.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/fun.lua@624a6732 第 156–160 行半身人之脚：原文首段为单一段落，现译在“他们觉得此事着实惊人。”后插入 \n，整条 LF 由 4 个变为 5 个，违反换行不变量。surface lane-000-2 判 OK、未进 contextual。本批按惯例记 done，作为宿主补充项登记到窗口66：删去该 \n，与“于是一些人认为”直接相接，文字不变。
- 7b6cdae17595f5e6dbdaad0943c74afb7cc6e31e1c5a7f8ecbf8e2aa565d4758 | mod-tome.lua | mod-tome/data/lore/misc.lua | 公开源码 game/modules/tome/data/lore/misc.lua@624a6732 第 702 行起科斯汀·赫菲因随笔：“maybe these promises leave much to be desired”意为这些保证还远不能令人满意，现译“这些保证有些难以置信”改成可信度问题（surface 与 contextual 均指出）。contextual 另指出：“if you wish me to be more concrete”译“如果你想要让我用语言描述的话”丢了“更具体”；“It is vast, more than you can imagine”被并入“神奇而又美好……远远超出了任何人的想象”，丢了 vast 并增“美好”；宿主核对属实。修复：“这些保证有些难以置信”改为“这些保证还远远不够”；“如果你想要让我用语言描述的话”改为“如果你希望我说得更具体些”；“究竟是多么神奇而又美好，远远超出了任何人的想象”改为“究竟有多么奇妙。它辽阔无边，远超你的想象”。 contextual 同判。
- 7eb1dc011b7de7b5529cbc72f95df40f2d9ccf1df5e403c573fe413d392b26f2 | tome-orcs.lua | tome-orcs/data/chats/shertul-priest.lua | Orcs 公开源码（来源未固定，/workspace/tome4-dlcs/orcs） 宿主补充观察：tome-orcs/data/chats/shertul-priest.lua:33 起（welcome）：开头绿色旁白“*Before you stands a tentaculous horror which you recognize for what it truly is. A living Sher'Tul!.*”为一行，与“Who are you...”之间一个 LF（共 1 个）；现译在“你认出了他的真实身份：”后另插一个 \n，把旁白拆成两行（LF 2），违反换行不变量。该换行在 C 档前（16bf1ef6）已存在。surface lane-001-2 判 OK、未进 contextual。按惯例记入窗口66 宿主补充（不计）：删去该 \n，“：”后直接接“一个活着的”。
- 939927d658c9444d9203ed0cffd80977c3145220bf6df483a1d36e661b75fe99 | tome-cults.lua | tome-cults/data/lore/fay-willows.lua | Cults 公开源码（来源未固定，/workspace/tome4-dlcs/cults） tome-cults/data/lore/fay-willows.lua:753 起菲·维莉欧斯第 5 卷：①“I got inspiration for them from the Nargols when they fought against the Conclave in the Allure Wars”只说灵感来源，现译另断言“这是他们在厄流战争中对抗孔克雷夫时使用的武器”，增出原文没有的史实（surface 指出）；②同条“heat beam rune”一处作“热束符文”，其余与全库实体名（mod-tome.lua:12086 heat beam rune＝热能射线符文）一致作“热能射线符文”（contextual 指出）。修复：①改为“我从纳格尔人在厄流战争中对抗孔克雷夫的经历里得到了灵感。”；②“热束符文”改为“热能射线符文”。 contextual 同判。
- 99451be05d9a01ab49e9f21c1cb0081b67e16dbdbc1acccbb630f80a40597bcc | tome-cults.lua | tome-cults/data/lore/fay-willows.lua | Cults 公开源码（来源未固定，/workspace/tome4-dlcs/cults） tome-cults/data/lore/fay-willows.lua:778 起：①“Your moves are too telegraphed”指动作意图明显、易被预判，与下句“attacks are easily countered”相承，现译“你的动作太夸张了”改成幅度夸张（surface 与 contextual 均指出）；②“I activated the heat beam rune”译“热能射线束符文”，与同条后文及全库实体名“热能射线符文”不一（contextual 指出）。修复：①“你的动作太夸张了”改为“你的动作意图太明显”；②“热能射线束符文”改为“热能射线符文”。 contextual 同判。
- 9be1dc5a72da6b86145e5fc521eb94837e8730c2f2f3990f197dd64b94e798a9 | mod-tome.lua | mod-tome/data/lore/tannen.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/tannen.lua@624a6732 第 47 行起坦能日记：原文末尾以 \n 结束（LF 5），现译末尾“……骨巨人。”后缺这个 \n（LF 4），违反换行不变量。surface lane-000-1 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：在末尾补回一个 \n，文字不变。
- a32121c7fdffeb000f4634832a6108cf0e8d695d701d895722ff1208ab3a5a7f | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 公开源码 game/modules/tome/data/lore/orc-prides.lua@624a6732 第 357–377 行兽人军官日志：每个“...”分隔行与下一段之间只隔一个空行（“...\n\nCurses”“...\n\nWe've”），现译前两处“……”后变成三个换行（“……\n\n\n该死！”“……\n\n\n我们循着”），整条 LF 由 20 个变为 22 个，违反换行不变量；第三处“……\n\n统帅部”与原文一致（surface 与 contextual 均指出，宿主预扫同）。修复：两处“……\n\n\n”各删一个 \n，改为“……\n\n”，文字不变。 contextual 同判。
- a4ad61026b7ca1ba10908db3ed7207ad7f4611ca7a09af5c8cc4c7350adf6b3b | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | Ashes 公开源码（来源未固定，/workspace/tome4-dlcs/ashes-urhrok） tome-ashes-urhrok/data/lore/demon.lua:206–213 恶魔紧急便条：“Blow all connectors, break platform off the continent and dispel oxygenation wards befo--”是炸毁连接结构、驱散供氧结界的破坏指令；现译“关闭所有链接传送门……关闭氧气生成设备，并——”把炸毁弱化为关闭、凭空加“传送门”、把魔法结界说成设备（surface 与 contextual 均指出）。修复：改为“炸毁所有连接结构，将平台从大陆上断开，驱散供氧结界，赶在——”。 contextual 同判。
- a6af085c458cfb8b7cd3dfeece7932283265b8b76e51bb625c396c72a8da260d | mod-tome.lua | mod-tome/data/chats/arena-unlock.lua | 宿主补充观察：公开源码 game/modules/tome/data/chats/arena-unlock.lua@624a6732 第 54 行起竞技场邀约：原文有三处句中硬换行（enough\nwealth、when\nyou、fighting\nour men），共 10 个 LF；现译重排为 8 个 LF，违反换行不变量。surface lane-000-2 判 OK、未进 contextual。本批按惯例记 done，作为宿主补充项登记到窗口66：在“作为回报……”与“你能赢得”之间、“我的小小考验……”与“等你的冒险结束后”之间各补一个 \n（恢复到 10 个 LF），文字不变。
- bb15e6ad6ea81fc1611910790096ec25e49a2ed16214d0829b56ffdbf615640f | tome-orcs.lua | tome-orcs/data/chats/metash.lua | Orcs 公开源码（来源未固定，/workspace/tome4-dlcs/orcs） tome-orcs/data/chats/metash.lua:48（nw-thanks）：开头“We of the Krimbul Clan”点明说话者所属氏族，现译“我们氏族”漏掉专名 Krimbul（surface 与 contextual 均指出）。本库该氏族多作“克里布尔部族”（krimbul.lua 传说分类名、标题与演说共 3 处；另 2 处作“克里布尔部落”，不在本条范围）。修复：开头改为“我们克里布尔部族曾无数次直面灭族危机”，句子其余部分已核对，不变。 contextual 同判。
- d15beb86fb20898202b98da109d372921ddd07a7ef3dbacac07ffe06ed7c329c | mod-tome.lua | mod-tome/data/lore/rhaloren.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/rhaloren.lua@624a6732 第 53–62 行审判者宣言：原文“Many of our mages were killed\nmercilessly”有一处句中硬换行（LF 9），现译把该段并为一行（LF 8），违反换行不变量。surface lane-000-0 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：在“我族许多法师遭到无情杀害，”之后补一个 \n，文字不变。
- d2614f771fd185fee71a37ee5ee89f2f4beeaffd6a95f2d3d6ca07cffae8a893 | tome-cults.lua | tome-cults/data/lore/kroshkkur.lua | Cults 公开源码（来源未固定，/workspace/tome4-dlcs/cults） tome-cults/data/lore/kroshkkur.lua:61 起诸神前言第三段：“there is more than enough evidence to suggest that the gods are fallible and motivated by things just as petty as we mere mortals”意为诸神会犯错，驱使它们的动机也和凡人一样琐碎卑微，用来反驳上句“更远大的目标”；现译“诸神就和凡人一样容易冲动并犯下错误”丢了“动机琐碎”这一论点，又增出原文没有的“容易冲动”（surface 与 contextual 均指出）。修复：该分句改为“但也有十足证据表明，诸神同样会犯错，驱使它们的也不过是和我们凡人一样琐碎卑微的东西”。 contextual 同判。
- d7bd95ff106e9c9bc5975e31b91b5b8bec2492294526697be4a1eec3369ef96b | mod-tome.lua | mod-tome/data/lore/iron-throne.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/iron-throne.lua@624a6732 第 75–79 行钢铁王座敕令：原文末段“This is a grave … long may our empire endure.”为一段（LF 4），现译在“带来灾难。”后另起“\n\n任何向外界泄露……”成两段（LF 6），违反换行不变量。surface lane-000-1 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：删去“带来灾难。”后的 \n\n，与“任何向外界泄露”直接相接。
- e02657942ba5df4779dc0c3dd6488b1bcb71211b4b280a4f1e94455c5030baa0 | tome-cults.lua | tome-cults/data/lore/fay-willows.lua | Cults 公开源码（来源未固定，/workspace/tome4-dlcs/cults） tome-cults/data/lore/fay-willows.lua:404 起末段：“I dodged lava, uneven ground, burnt foliage, and the crashing waves of boiling water as I tried to keep up with my group”中 burnt foliage 是已烧焦的草木，现译“燃烧的树叶”变成正在燃烧；同句 crashing waves of boiling water 只剩“滚烫的波浪”，丢了翻涌拍打之意，并列项也用逗号而非顿号（surface 指出焦点，contextual 判 OK；宿主按整句核对）。修复：整句改为“我躲避着熔岩、崎岖的地面、烧焦的草木和翻涌而来的沸水浪涛，努力跟上我的小组。”（“小组”与上文“离海最近的小组”一致）。
- e69406df8f8cf1cb707818eed7ce45b4759b1da39598d6f45bb01547ac37ad64 | mod-tome.lua | mod-tome/data/chats/alchemist-hermit.lua | 公开源码 game/modules/tome/data/chats/alchemist-hermit.lua@624a6732 第 118 行半身人纸条：“while you've been loafing”是责备玩家磨蹭偷懒，与下句“Hurry the hell up next time”构成因果；现译“在你离开的时候”改成中性的不在场，丢了指责（surface 与 contextual 均指出）。修复：“在你离开的时候”改为“趁你磨洋工的工夫”，“下次动作快点”改为“下次给我快点”，占位符顺序不变。 contextual 同判。
- ea567581080129e9fea76f50d9db62fede16b0e4f85f08fe1d965acfd216683a | mod-tome.lua | mod-tome/data/lore/last-hope.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/last-hope.lua@624a6732 第 173–203 行德瑞克史话：原文“…you accept?\"\n\nThe Conclave mages' response”之间只隔一个空行，现译“你们接受吗？”\n\n\n孔克雷夫”多一个 \n（LF 30→31）。surface lane-000-3 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：删去多出的一个 \n。
- f01b17c6a1335e27af2729076228ae4a73e14f5e24a0ada381d4a4baa4a2b7e5 | tome-orcs.lua | tome-orcs/data/lore/gem.lua | Orcs 公开源码（来源未固定，/workspace/tome4-dlcs/orcs） tome-orcs/data/lore/gem.lua:24 起帕默日志：“She sighs.”之后用 " 重新开始帕默的直接引语，先引任务原文 'Find the Loyalist…'，再接 Which is Council-speak…，到 …underground and..." 才闭合。现译“她叹了一口气。”之后直接写‘寻找忠诚者……’，缺外层左引号“，致使“如果不用官腔的话……而且…”读似旁白，其后的”无从配对（surface 与 contextual 均指出）。这是 C 档修复包 16（a1d40dfc）删去“上面写着，”时连带去掉了左引号造成的回归。修复：在‘寻找忠诚者’前补回“，即“她叹了一口气。“‘寻找忠诚者……”，文字不变。 contextual 同判。
- f901245fbaef3549eba82f7b1068a771bacb26a4d7485633b7d88f373ceb5e2a | mod-tome.lua | mod-tome/data/lore/age-allure.lua | 宿主补充观察：公开源码 game/modules/tome/data/lore/age-allure.lua@624a6732 第 29–46 行红帕兰日志 1–3：原文第二、三篇正文各为一行，现译在“很快就会被削减。”后、“某种餐具……”后各插一个 \n（LF 17→19），违反换行不变量。surface lane-000-3 判 OK、未进 contextual。本批按惯例记 done（宿主补充不改 disposition），作为宿主补充项登记到窗口66：删去这两个 \n，使“但我仍心存希望”“算了，反正愚蠢的夺心魔还有很多”分别与前句相接。
