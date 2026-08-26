# P2 核心文本复核交接（2026-08-23）

> 类型：收尾记录，非契约、非门禁。
> 权威路线仍见 [`project-roadmap.md`](project-roadmap.md)；Paseo 编排与语境审核契约见
> [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md)（2.18-draft）与
> [`paseo-translation-context-review-v1-contract.md`](paseo-translation-context-review-v1-contract.md)。

## 交接更新（2026-08-24）

- 提交基线为 `a5c3ac6`（b6–b19）；其后仅有 b20 的 5 条未提交 `mod-tome.lua` 译文改动。
- b20：`last-hope-weapon-store.lua`（10 条）。将「军事训练」润色为「战斗训练」，补足两类训练的「基础使用方法」表述；保留 `Technique/Combat-training=技巧/战斗训练系`、`Shoot=射击天赋`、金额、source 与 source_tag。冻结身份 `660d64018b6cd24732efa26e35bfdf71fb3e263638936e246855ff204d4f2798`；独立语境复审 10/10 `OK`，严格 lint、`git diff --check`、完整 `tools/ci-gates.sh`、契约与 DONE 状态检查均通过。
- b21：`limmir-valley-moon.lua`（2 条）。固定源码核验后无改动；独立语境复审身份 `139f5312c3d97567e2052b00896bad8c5fc089388bb0636461105764592d447d`，2/2 `OK`。任务产物位于忽略的 `.ai/task/p2-tome-texts-b21-001/` 与 `.ai/reviews/...`。
- b20 已单独提交为 `507d2dc`；本交接文档的 b20／b21 记录提交为 `01179b7`。
- b22：`lost-merchant.lua`、`lumberjack-quest-done.lua`、`lumberjack-quest.lua`、`mage-apprentice-quest.lua` 共 33 条，提交 `6bcf55b`，修订 18 条 target。冻结工作集恢复为受跟踪的 `evidence/quality/p2-batches/p2-tome-texts-b22-lost-merchant-lumberjack-mage.json`（b19–b21 曾只留在忽略的 `.ai/`），33/33 英文键按固定 commit `624a673` 逐条字节核验，窗口内无 `args_order`。
- b22 主要修正：安格利文揭示处原译「为你开启了一个传送门」与固定源码不符——`access_angolwen` 放置城镇与入口传送门地形并 `locationRevealAround`，实为在地图上标出而非开启通路；`everybody in my village` 曾被译成「所有村子里的人」；学徒两个分支的「已收集到一些物品」与「祝你学业顺利」的 studies 从句均曾遗漏；本恩临终的结巴与未尽之言被抹平。`Kar'Krul` 批内统一为「卡·克鲁尔」，与同文件另一处及 `unlock-mage.lua` 一致，不做全局替换（`lore/elvala.lua` 仍为「卡库罗尔」）。
- b22 复审：两轮 `translation_contextual_v1` 全量复审同一冻结集，身份 `471b63ef…`（ctx-01，32/33 `OK`）与 `f2b42ddc…`（ctx-02，32/33 `OK`）。两轮就同一条 `b22-24`「The keepers of ar...」给出相互矛盾的意见（ctx-01 要求补回 keeper 关系，ctx-02 反对补回后的动词化形式）；按本文档规则升级维护者裁决，维护者选择保留「他们守护着奥……」，记为 advisory 未改。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）、契约检查与 `DONE_VERIFIED` 均通过。
- b23：`magic-store.lua`、`melinda-beach-end.lua`、`melinda-beach.lua`、`melinda-fortress.lua` 共 40 条，提交 `f8d8504`，修订 19 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b23-magic-store-melinda.json`，40/40 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b23 主要修正：`that tank` 原译「通道」与固定源码不符——`shertul-fortress-butler.lua` 说明梅琳达每天需在 `regeneration tank` 中治疗八小时，应为「再生槽」，旧译并漏掉每晚回来接受治疗；`I want to train at Zigur?` 误用阵营名「伊格兰斯」，`Zigur` 是地点「伊格」（`terminology/places.tsv`），这是全文件唯一偏离（其余 45 处均正确区分）；`Shadow` 原为「堡垒幻影」，全文其余 9 处均作「堡垒之影」；`We will find a cure` 漏掉治愈目标，而同段伊格兰斯分支保留了「治好你」；`still tainted` 曾误作「肯定」且漏译 `foul`，`raving zealots` 曾夸大为「杀人狂魔」，`I had no idea this would happen` 整句遗漏，沙滩叙述凭空添加阳光与「五颜六色」。另统一了中文文本内的半角 `!?,...`。
- b23 保留项：magic store 的欢迎语与范围外 `jewelry-store.lua` 共用英文键且两处译文一致，单改一侧会拆散共享运行时键，故按 `docs/runtime-key-collisions.md` 保留。
- b23 复审：两轮全量复审，`20b80a8d…`（ctx-01，39/40）与 `09224ef4…`（ctx-02，40/40 `OK`）。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- **教训：复用上一批的 envelope builder 时必须改 revision key 前缀。** b23 的 ctx-01 冻结集沿用了 b22 的 `b22-` 前缀，虽不影响正确性（payload／envelope／返回值内部一致，preflight 通过），但会与上一批的 key 命名空间冲突、误标批次来源；已在 ctx-02 重新冻结时改正为 `b23-`。
- 术语待办（未做）：建议新增 `Ziguranth → 伊格兰斯`（`T.PN.FACTION`，`society`），并注明与地点 `Zigur → 伊格` 严格区分。全文一致使用 27 次却不在术语库，正是 b23 该行发生偏离的原因。新增术语行需同步 `test_real_terminology_is_fully_mapped` 的硬编码行数，属独立小任务。
- 术语：`Ziguranth = 伊格兰斯`（`T.PN.FACTION`／`society`）已加入术语库，提交 `1a4a236`，同时把 `Zigur = 伊格` 行补上交叉引用并把 `test_real_terminology_is_fully_mapped` 的行数 710→711。固定源码证据：`anti-antimagic.lua` 同句「The defenders of Zigur were crushed, the Ziguranth scattered and weakened.」区分据点与教团；引擎另有 Zigur zone 与 `Zigur (Town)` grid 实体，`init.lua` 称 Ziguranth 为 an ancient order。地点用「伊格」，教团用「伊格兰斯」。
- 随后 `8fb41dd` 修正 `maj-eyal-npcs.lua` 的实体名 `ziguranth patrol`：伊格巡逻队 → 伊格兰斯巡逻队，与 `ziguranth.lua` 的三个同类实体一致。该实体在固定源码中 `faction = "zigur"`、`hates_arcane = 1`，是教团的游荡队伍而非地点（小写 faction id 是内部键，不是显示文本）。此偏离由「术语改动后用固定 Lua 桥加载 `mod-tome.lua` 复核」发现，lint 与三项术语审计都不会报——两种写法各自合法。
- b24：`message-last-hope.lua`、`myssil.lua`、`norgan-saved.lua`、`orc-breeding-pits.lua`、`paradoxology.lua`、`player-inscription.lua`、`point-zero-zemekkys.lua`、`pre-charred-scar-eruan.lua`、`pre-charred-scar.lua` 共 40 条，提交 `0b25434`，修订 25 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b24-myssil-point-zero.json`，40/40 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b24 主要修正：`Grand Keeper` 原作泛指的「伟大的守护者」，按术语库 `Keeper of Reality` 行及 `intro-chronomancer.lua`／`npcs.lua` 统一为「现实至高守护者」；育种棚拒绝分支原译成「一个人做不到」（能力不足），固定源码是玩家拒绝亲手行凶并交由艾琳处置，下一分支还凭空多出「一个人足以解决它们全部」；泽梅奇斯把「更年轻的我」讲反；临终太阳骑士的陈述凭空多出「一万倍」并漏掉手绘地图、吃力递交与最后恳求的目光；米歇尔的任务说明漏掉 eldritch forces／powerful／responsible／All corrupted，并把 `high in the Daikara mountains` 误作「最高峰」；另有 `then rest` 等整句遗漏与中文内半角标点。
- b24 复审：`ad8bc967…`（ctx-01）首轮即 40/40 `OK`，无修复轮。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- b24 宿主 advisory（未改）：`paradoxology.lua` 的 `What the...` 由「我X！」改为直译「这是什么……」。直译更贴字面，但削弱了被打断的惊愕语气；复审未提出异议，按编辑裁量记录，不作缺陷。
- 待办（超出当批窗口）：`zemekkys-start-chronomancers.lua` 存在同样的 `Grand Keeper` 偏离，留待轮到该 section 的批次处理。
- 流程变更（2026-08-24，提交 `5a57f2f`）：译文复核改为**连续批次模式**，一批 `DONE` 并提交后直接开始下一批，不再逐批等待批准。停下条件与自行处理范围见 `AGENTS.md`「连续批次模式」；连续运行不豁免任何冻结、复审、门禁与生命周期要求。
- 流程变更（2026-08-24，提交 `e21e01e`）：判定 child 挂起或调用 stop／cancel 前必须先做有界终态取证——重查实时状态并读 `attentionReason`／activeTurn，再看工作树（未产出改动的 EXECUTOR 留下空 diff）。EXECUTOR 结束却无工作成果时输出无效：先归档再 fresh retry，不得对已结束 child 发 follow-up。已写入的故障归因被推翻必须同轮更正。见 `docs/lessons-learned.md` 第 11 条。
- b25：`ring-of-blood-master.lua`、`ring-of-blood-orb.lua`、`ring-of-blood-win.lua`、`sage-kitty.lua`、`shadow-crypt-yeek-clone.lua` 共 37 条，提交 `9ab2a60`，修订 20 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b25-ring-of-blood-shadow-crypt.json`，37/37 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b25 主要修正：竞技场规则原译承诺奖品是「一个戒指」——任务代码确认「鲜血呼唤」确为戒指，但该句台词只点名奖品，故删去凭空补充的说明，并修正 `会……了` 时态冲突、补回 our pawns；十轮回合数与玩家经水晶球控制奴隶的机制已按任务源码复核。`slave fodder` 曾被译成「像奴隶一样的炮灰」（改变了所指）；`Normally you would be taken as a slave` 漏掉被掳为奴；`standard fee` 遗漏且凭空多出「每次」；小猫漏译橘色却多出「眼泪汪汪」。
- b25 复审：`0cbb7c58…`（ctx-01）首轮即 37/37 `OK`，无修复轮。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- b25 生命周期：首个 EXECUTOR dispatch 结束却无任何产出（无 diff、无报告），按新规归档为 spent，另建 fresh retry child 完成本批；两者均已确认归档。
- 冻结方法修正（2026-08-24，提交 `683b674`）：`tools/i18n context` 的 `--limit` 默认 50 且静默截断，冻结脚本与 envelope builder 都必须显式传 `--limit 500`，并断言冻结条数等于该 section 的词法 `t()` 调用数；核验英文键时同时接受原文与转义形式（引擎把换行写成 `\n` 两字符转义）。b22–b25 单段最大仅 24 条，已逐段机械复核未受影响。详见 `docs/lessons-learned.md` 第 12 条。
- b26：`shertul-fortress-butler.lua` 单段 53 条，提交 `300e104`，修订 21 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b26-shertul-fortress-butler.json`。
- b26 主要修正：多处机制数值与描述有误——`open_training` 实际恰好消耗 50 点能量（旧译「至少 50」）、训练设施是「尚未通电」而非仅「需要能量」、堡垒概述漏掉永久远古传送门并凭空说黄金副产物会折算成金币；`titanic wars` 误作「泰坦之战」，`hunt down, killing or banishing` 弱化为「击倒、驱散」；异象段同一指称一处作「堡垒之影」另一处作「那个阴影」，且后者紧接「随后你看到了黑暗；」会被读成那团黑暗；`I will, thanks.` 只译出「知悉」，而该选项带 `spawn_transmo_chest()`，选它就是收下转化之盒。
- b26 术语裁决：堡垒问候语的 `a control rod` 一度被改成专名「回归之杖」，复审反对并获维持——源文用不定冠词泛指，同一文件另有 `the rod of recall` 并说明它并非夏·图尔造物，且文件内 `has_rod` helper 定义后从未被调用（死代码）。已恢复泛指译法。
- **b26 首次触发高级范围校准（`senior-audit-01`）**：ctx-02 在 ctx-01 已判 OK 且字节未变的 3 条上提出新 finding。按契约 `cycle >= 2` 的规则先做 `SENIOR_REVIEW` scope_audit，裁定其中 2 条为源码可证的真缺陷、1 条以错误语法前提为由驳回（`是不是` 是正反问，并不预设存在）。**由此确立的常规**：对未改动且此前判 OK 的文本提出的新 finding，默认驳回，除非带有固定源码或引擎行为证据；若后续轮次就同一 revision 推翻本次校准，按 `AGENTS.md` 的重复实质分歧条件交回维护者。
- **验收标准措辞修正**：b26 的 SPEC 验收第 4 条原写作「独立复审对全部 53 条返回 OK」，即要求复审一致同意，而非缺陷已解决。两名独立复审对字节相同的文本给出互不重叠的 finding 集，说明该机制不可靠地达成一致；已在任务内按高级校准改为「confirmed finding 全部解决、驳回项记为 advisory、cycle ≥ 2 的修复经 scope 校准」。后续批次沿用此措辞。
- b27：`shertul-fortress-caldizar.lua`、`command-orb`、`gladium-orb`、`shimmer`、`training-orb` 共 43 条，提交 `7deb1ee`，修订 27 条 target；复审 42/43，唯一 finding 经固定源码裁定驳回，无修复轮。
- b27 rod 裁决（承接 b26）：同一节内四种写法按指代逐条裁定——水晶球自身铭文 `"Insert control rod."` 保留泛指「控制棒」（古代机器对所需部件的称呼）；孔洞描述、`[Insert the rod]` 与插入场景用「回归之杖」，因为该分支只在 `command-orb.lua:21` 的 `ROD_OF_RECALL` 检查通过后出现。两种译名在同一节共存是有意的；原「魔杖」两者都不符。
- b27 其他修正：`the world of Eyal` 被误作马基·埃亚尔大陆而非整个世界；`Lichform` 统一为「巫妖转生」（与 `talents.lua`、`lichform.lua`、`mag.lua` 一致，英文键的 `ceremory` 拼写错误原样保留）；target dummy 原作「傀儡」与既有实体撞名，改为语料已有 9 处的「训练假人」；shimmer 各选项按其独立 `SHIMMER_*` 槽核对。
- b27 驳回记录：复审称「堡垒竞技场」把竞技场与堡垒混同。固定源码显示 gladium 是独立 zone，且该 zone 自身名称即 `Fortress Gladium`（`zones/gladium/zone.lua:21`），故「堡垒」二字来自原作者而非译文；`[Go back to the Fortress]` 与之并不矛盾。按 advisory 记录，未改。
- 待办（超出当批窗口）：`other.lua` 仍把 `Lichform` 译作「巫妖形态」，与语料的「巫妖转生」不一致，留待轮到该 section 的批次处理。
- b28：`slasul.lua` 单段 21 条，提交 `63e7b1d`，修订 13 条 target；两轮复审（18/21 → 21/21 `OK`）。
- b28 主要修正：萨拉苏尔反驳中的 `which of us is truly evil` 原作「谁才是恶魔」，把反问读成了生物名称，丢失「我未伤人、你却杀我朋友」的论证；`refuse to see reason` 原作「不听我解释」，而固定源码 `slasul.lua:43` 显示该句是玩家拒绝分支的攻击台词，位于萨拉苏尔已经申辩之后，玩家是听过后拒绝接受；`spare / offer mercy` 原用「宽恕」（道德赦免），源文是生杀之权，且与紧邻上一条已用的「饶」自相矛盾；`my liege` 原作「我的主人」，而 `slasul.lua:91` 是玩家缔结生命契约时的效忠称呼，属封建主君关系——「主人」在 b26／b27 中已正确用于堡垒之影称呼玩家的 master，此处沿用会把两种关系混为一谈。
- b28 保留项：`[attack]` 与另外四个 section 共用英文键且译文一致（均为「[攻击]」），单改一侧会拆散共享运行时键，故保留；英文源码中的两处上游拼写错误（`Pay for you sins!`、`I will make your pay`）按约束不改英文键。
- b29：`sorcerer-end.lua` + `sorcerer-fight.lua` 共 48 条，提交 `83a313d`，修订 29 条 target；三轮复审加一次高级范围校准。
- b29 主要修正：遥远太阳牺牲日志的 `%s` 位置使姓名读成「被牺牲的对象」；抵抗分支漏掉强调的 NOW 且把粗体标记落在凭空新增的词上；艾琳的诀别把 `a precious ally and a friend` 误作「伟大的盟友和罕见的伙伴」，并漏掉 `last` 与 `selfless`；主上的 `you are my tool and I intend to use it` 被弱化为泛泛「遵循意志」；`sorcerer-fight` 两段近乎相同的 Creator 台词互相矛盾（造物主／造物之主），统一为语料中五处使用的「造物主」；`I *WILL* stop you!` 对两名魔法师用了单数「你」，而同段其余三句玩家台词均用「你们」。
- **b29 第二次触发高级范围校准（`senior-audit-01`）**：ctx-02 在 ctx-01 已判 OK 且字节未变的 2 条上提出新 finding。校准裁定——`found the peak entertaining` 译成「在山巅看得很尽兴」属**确认缺陷**：固定源码该从句没有任何感知动词，且 `high-peak/zone.lua` 定义高峰是十层战斗关卡，玩家是打上去的，无可观看之物，「看」是凭空新增的动作；`have you at my side` 译成「你能协助我」属**驳回**：`aeryn_comes` 将该事件记为 `aeryn-helps`，引擎本身即把艾琳的到来记作「协助玩家」，且同句后半仍保留共同行动。
- **校准要点（重要）**：高级复审明确指出 b26 确立的「对未改动且此前判 OK 的文本默认驳回」**必须保持为「证据默认」，不得硬化为一概不接受**——因为 ctx-01 确实漏掉了上述确认缺陷。证据门在首次实测中判别正确：带固定源码／引擎行为证据的通过，只有措辞偏好的被驳回。
- b29 收尾：高级校准要求「应用 A、驳回 B、结束本批，不再跑第三轮全量复审」。宿主据此未再做整段复审，仅对修复的那一条做了单条有界核验（ctx-03，1/1 `OK`）；该偏离及理由已记入 `senior-audit-01` 的 host_note。
- 当前预期工作树：干净，仅用户本地未跟踪 `.claude/`；不得提交、删除或混入 `.claude/`。`.ai/` 与 `.artifacts/` 是忽略的派生产物。
- b30：`tannen.lua` 单段 39 条，提交 `20cc334`，修订 15 条 target，另加 1 条越界一致性传播；一轮复审（38/39 `OK`）。
- b30 主要修正：泰恩要求 `hold onto the Orb` 原译成「研究一下多元水晶球」，漏掉保管权转移——固定源码 `east-portal.lua:92-97` 的 `give_orb` 会把「多元水晶球」从玩家背包移除，而 `withheld_orb`（:99-101）只改任务状态、不移除；搜寻提示把 `Diamond` 降格成泛指的「宝石」，而 `remove_materials`（:104-115）按原名移除的是「共鸣钻石」与「血符仪式匕首」；文献标题 `Inverted and Reverted Probabilistic Fields` 原译《关于力场翻转与回复的可能性研究》，把 probabilistic 读成「可能性研究」，切断了与两行后「反转还是复原概率场」提问的对应，玩家无法把要找的书与要问的问题对上；`cursory examination` 原作「粗略的试验」（examination 误作 experiment）；`What in the...` 原用带字母审查的「我X…」，源文只是被打断的惊呼。
- b30 范围修正：该标题在窗口外还出现一次（`data/zones/telmur/npcs.lua` 的阴影消散提示，`mod-tome.lua:40069`）。对固定 commit 执行 `git grep -l 'Inverted and Reverted' -- game/modules/tome` 只返回 `data/chats/tannen.lua` 与 `data/zones/telmur/npcs.lua`，且没有任何物品实体使用该名，四处调用即闭合全集。只修窗口内会把原本一致的一对**新拆成不一致**，故经 SPEC 修正案授权把已定译法传播到该行；`SCOPE.json` 锚点仍只含 `tannen.lua`——标题语义已在窗口内复审三次，40069 只是字节传播，为一行冻结整个 section 不成比例。
- b30 复审裁定：唯一 finding 落在背叛台词 `I am ready. You are not.`（`你还没好`）。裁为 **advisory 而非 confirmed**——固定源码 `tannen.lua:177-183` 的 `wait_end` 是 `fake_orb_end`（:170-175）的孪生分支，两者同为背叛前的挑衅且都走向 `tannen_tower`，对照关系确是该句的修辞内容，但中文「好」承前句「准备好了」省略，语义可还原且无机制损失，按 b22–b24 先例属纯形式异议。因传播已需一轮修复，顺带应用以恢复显式对照。注意该句是 executor 未改动的既有译文，但属本窗口首轮复审，故 b26 的「未改动文本默认驳回」不适用。
- b30 保留项：`Sholtar` 在本段作「肖塔尔」（2 处），在 `misc.lua`／`load.lua` 的复合词「肖塔王国」中作「肖塔」（2 处），二比二无优势形式且跨批次边界，按专名分裂规则（只在批内统一、绝不全局改名）保留；`Maj'Eyal` 全语料分裂为带间隔点 71 处、不带 54 处，术语行仅 `existing` 状态，属全局改名议题，需维护者裁决后再动。

- b31：`tarelion.lua`、`tarelion-start-archmage.lua`、`temporal-rift-end.lua`、`temporal-rift-start.lua`、`the-master-resurrect.lua`、`trap-priming.lua`、`tutorial-start.lua` 共 37 条，提交 `b5283ae`，修订 11 条 target；一轮复审（35/37 `OK`）加两轮修复。
- b31 主要修正：泰尔兰的招呼把 `up to all sorts of doo-daddle in the outside world, I imagine` 译成「大不了算是一个……小子」，凭空加入英文没有的「至多」上限，把同位补充变成贬抑判断（固定源码 `tarelion.lua:20-24`，说话人是假扮和善老者为图书馆募捐的泰尔兰）；魔法大爆炸段落原译「分裂成了几个碎片」，而固定源码 `tarelion-start-archmage.lua:37` 只有**一块**被撕走并抛入虚空（即次元浮岛）；`more of us should get out of here once in a while` 原读成频率（「多多出去」），源文是**人数**；`Temporal Warden` 原作「时间守卫」，术语库为「时空守卫」，修复后语料 24:0；`He looks at you more closely` 原译多出「靠近」这一源文没有的动作；`trap-priming.lua` 是 UI 而非对白——`Not Prepared` 原作口语化的「还没准备好」，而固定源码 `trap-priming.lua:44-48` 将其与「即爆机关／无法使用／常规机关」并列填入 `%s[%s: %s]` 标签格式，且 prepare/dismantle 一句原把「即爆机关」当成「准备」的宾语，实际宾语是陷阱；教程结语被解锁的是**种族与职业**，原译泛化成「内容」；领主台词中的半角逗号与分号。
- b31 保留项：陷阱失败提示 `#LIGHT_BLUE#You cannot prepare this trap: %s.` 句末半角句点值得修，但该运行时键同时存在于 `mod-tome.lua:6399`（窗口内）与 `:42350`（`mod-tome/dialogs/TrapsSelect.lua`，窗口外）且译文字节相同，单改一侧会拆散共享键；与 b30 的标题不同，**不动则两侧仍然一致**，故按 b23 共享键规则保留。The Master 在同一条内保留「领主」（实体）与「主人」（占有关系）的区分，按 b27 控制棒裁定逐处判断，不作统一。
- b31 复审裁定：两条 finding 都落在 executor 未改动的行上，且属本窗口首轮复审，故 b26「未改动文本默认驳回」不适用（该规则针对的是**后一轮推翻前一轮**）。`b31-01` 判 confirmed；`b31-20`（`But what is all th...` 中途打断被补成完整问句）判 **advisory**——省略号已传达话未说完，损失的只是断在词中的突兀感，与 b30-39 同型同判。
- b31 宿主自致回归（已更正）：第二轮 briefing 用「`这到底是……`」作示例句式，executor 逐字照抄，结果丢掉了对抗性的「但」与「一切」，还与 `tannen.lua` 中 `What in the...` 的译文完全相同。第三轮改为 `但是这一切到底是……` 修正。**教训：给约束，不要给可照抄的示例译文。**

- b32：`ukllmswwik.lua`、`undead-start-game.lua`、`undead-start-kill.lua`、`unremarkable-cave-bosses.lua`、`unremarkable-cave-fillarel.lua`、`unremarkable-cave-krogar.lua` 共 50 条，提交 `939ecaa`，修订 16 条 target；一轮复审（47/50 `OK`）加一轮修复。
- b32 主要修正：巨龙的 `You seem to be worthy` 原作「有点价值」，把「有资格听这个故事」的评价改成对玩家利用价值的估量，且「有点」进一步削弱语气（改为「够资格」）；`Thanks for the information` 原作「谢谢你的帮忙」，而该选项的 action 直接杀死死灵法师，玩家是套出情报后翻脸，对方从未提供帮助（改为「谢谢你的情报」）；菲拉瑞尔的 `Abandon this fight` 原作「投降吧」，凭空加入向她屈服的关系，源文只是要求兽人罢手，且克罗加尔的回应是嘲讽她体力而非回应投降要求（改为「罢手吧」）；另补回娜迦改造自身以适应水下生活、神庙「可能是夏·图尔遗迹」、`an act of mercy`、召唤法阵**局部**消退才是逃脱条件、晨曦之门是「仅存的自由堡垒」、兽人部落的「……暂时如此」。
- b32 专名对齐：`Krogar` 一个兽人有三种译名。实体名 `mod-tome.lua:40985` 为「克罗加尔」，固定源码 `unremarkable-cave/npcs.lua:103` 只定义一个 `name = "Krogar"`（:85 以 `act.name == "Krogar"` 判定），故窗口内三处「克罗格」全部对齐为「克罗加尔」。窗口外 `strange-new-world.lua:20814` 的「克洛加尔」按 b24 `Grand Keeper` 先例留作后续批次的遗留项。
- b32 保留项：`[attack]` 与另外四个 section 共用英文键，保持「[攻击]」；乌克勒姆斯维奇与萨拉苏尔的说法**故意互相矛盾**，玩家相信谁决定谁死，不得调和。
- b32 宿主自提 finding（复审判 `OK`，由宿主提出）：round 1 把不定指的 `a cloak` 提升为物品专名「欺诈斗篷」。指称本身成立（`blighted-ruins/npcs.lua:55-58` 确实装备 `CLOAK_DECEPTION`，语料 `mod-tome.lua:38066` 名为「欺诈斗篷」），但英文刻意用不定冠词，说话人是与刚苏醒的亡灵讨价还价的陌生人，玩家从未见过该物品，报出专名等于透露他没说出口的名字——即 b26「泛指的 a control rod 不得变成物品名」同型；b27 的逐处细化不适用，因为那里的分支确由 `ROD_OF_RECALL` 把关，而此处没有任何分支以斗篷为条件（玩家杀死他后自行拾取）。判 **advisory** 并改回泛称「斗篷」，保留 round 1 同一字符串内的其他改进（`普通人`→`普通人类`，英文 Human 大写指种族）。

- b33：`ward.lua`、`worldly-knowledge.lua`、`yeek-wayist.lua`、`zemekkys-done.lua` 共 37 条，提交 `ed63878`，修订 11 条 target；一轮复审（34/37 `OK`）加一轮修复。
- b33 UI 判定：`ward.lua` 与 `worldly-knowledge.lua` **是 UI 不是对白**。固定源码 `ward.lua` 的每个选项由 `("Fire [%d]"):tformat(...)` 生成并绑定引擎 `DamageType` 常量（FIRE/LIGHTNING/COLD/ARCANE/LIGHT/DARKNESS/TEMPORAL/PHYSICAL/NATURE/BLIGHT/ACID/MIND），`%d` 是剩余充能数，故 `T.GAME.DAMAGE` 术语行是这些标签的裁定依据。十一个标签本已一致，唯 `Acid` 作「酸液」而术语行为「酸性」，已对齐。注意「酸液」在技能名（`Acid Spray`＝酸液喷吐）中正确，属不同角色。
- b33 主要修正：精神防护日志把 `the Wayist mind` 译成「夺心魔」——源文指的是**维网信徒**这一归属而非**夺心魔**这一种族，说话者两者皆是，正是易混之处（术语：`Wayist`＝维网信徒，`Yeek`＝夺心魔）；`What is the Way, and what are you?` 原译「你是谁」，而下一节点答的是 `I am a Yeek`，问的是种族；大剑是**变换姿态**而非原译的后退位移；生物描述漏掉 `covered in small white fur`；`cover more ground` 被夸大成「探索这个大陆」；`feelings of peace` 用了政治义的「和平」，此处是内心感受（改「平静」），而数行前「维网是启迪、和平和守护」的教义句保留「和平」——**同词两义，只有感受那处是错的**；`We are the Way, always` 是同一性断言，原译「属于维网」降格为从属关系；伊莫克斯处敷衍的 `Whatever.` 原作「还行吧」，变成对传送门的正面评价，抹掉了与「是的，谢谢你」分支的对立。

- b34：`zemekkys.lua`、`zemekkys-start-chronomancers.lua`、`zigur-mindstar-store.lua` 共 44 条，提交 `e0a5dac`，修订 22 条 target（含一条越界共享键统一）；一轮复审（40/44 `OK`）加两轮修复。
- b34 三处专名对齐（均以 `entity name` 行为锚，且**全部残留归零、集合闭合**）：`Briagh` 窗口内 4 行 5 处作「布莱亚弗」，实体名为「巨型沙虫布莱亚」（`zone.lua`／`grids.lua`／`west-portal.lua` 本已一致）；`Grand Keeper` 作「伟大的守护者」，即 b24 标记的遗留项，实体名为「伊莫克斯，现实至高守护者」；`Great Sand Wyrm` 作「巨型土龙」（全语料仅此一处），实体名为「巨型沙虫布莱亚」「巨型沙虫挖掘者」。
- b34 主要修正：血符仪式匕首是用来**刻画**传送门（固定源码 `zemekkys.lua:83` 的 `etch`，下一行重申必须刻在准备好的共鸣大理石上），原译「开启」是完全不同的操作；共鸣钻石的成因是普通钻石卡在鳞片间数世纪、被灌注**生命节律**（`life rhythms`），原译「生命活力」丢掉了「共鸣」之名的由来；`wild eyes` 原作「野蛮的眼睛」，源文指狂乱失控的眼神，而伊莫克斯是会拿「把自己炸得够呛」自嘲的学者型隐士；`unhallowed` 原作「混沌」，实为「不洁／被亵渎」的祝圣属性，且中性的 `inhabitants` 被预先写成「怪物们」——玩家是被派去**寻找源头**的，提前定性等于泄底；补回「太阳堡垒**以南很远**」与岩浆威胁的深度；灵晶商店三档训练的价格与前置条件now明确。
- b34 共享键统一（宿主自致红门禁，已修复）：`b34-41` 所在字符串的运行时键与 `angolwen-staves-store.lua` 共享。第二轮 briefing 一边以「键被共享」为由禁止改该串的半角括号，一边又要求修改同一个共享 target，只改一侧导致键被拆散，`lint --strict` 与 `classify_runtime_keys` 报错。**executor 行为正确**：拒绝擅自扩大范围，如实报出红门禁，而非回退或掩盖。裁定为**统一而非回退**——固定源码 `angolwen-staves-store.lua` 三档结构与英文键完全相同，`我已经学会了` 在两家商店同样低估了前置条件，缺陷本就在两侧；依 `docs/runtime-key-collisions.md` §4.0「同键分歧统一到裁决形式」的先例，SPEC 增补授权 4217 一行，两侧现已逐字节相同。
- b34 教训：**共享运行时键约束的是整个 target，不只是你恰好注意到的那个隐患**；**专名要整体调查，不能只查名字不查头衔**（`Great Sand Wyrm` 就是因此漏掉、由复审补获）；**子串匹配会掩盖专名漂移**（首次统计「布莱亚」得到 8/8 一致，因为「布莱亚弗」包含「布莱亚」，改用否定前瞻才暴露 4:4 分裂）。

- b35：`zigur-trainer.lua`、`zoisla.lua` 共 23 条，提交 `f7f5790`，修订 9 条 target；一轮复审（22/23 `OK`）加一轮修复。**`data/chats/` 全部 100 个 section 至此审校完毕（b6–b35）。**
- b35 主要修正：训练师的婉拒是**硬性等级门槛**——固定源码两个 answer 的 `cond` 分别是 `player.level >= 10` 与 `< 10`，原译「还太年轻」把可执行的条件读成了年龄评语；奥术驱动的已装备物品由 action 函数 `power_source.arcane` → `removeObject` **自动卸下**，原译读作需要玩家自行取下；教团担心的是奥术终将「毁灭**我们**」而非「毁灭这个世界」，且候选者须**证明自身纯洁**，奖励是**基于精神强度**的通用技能树；食人魔那条是用纹身替换不洁符文并解除依赖（`纹身` 义，而非 `充能` 技能类型义）；`zoisla.lua` 的传送门是**正在崩溃**。
- b35 称谓裁定：大写 `Fighter` 指训练师本人，引言作「战士」、竞技场作「斗士」，同一人物两个称谓。**统一为「斗士」而非反向**——竞技场同一条里「战士」已用于小写的 `warriors`（架住玩家扔进场的两人），若把 Fighter 并入「战士」会让训练师与自己的手下混为一谈；英文本就区分 `Fighter` 与 `warriors`，中文须保留这一区分。术语库无 `Fighter` 行，不构成约束。
- b35 共享键：本窗口三个运行时键与范围外 section 共享，均保持统一未改——`...`（全语料 153 处）、`Farewell.`（2 处，本已一致），以及与 `infinite-dungeon/objects.lua` 共享的中魔提示行。**第三个是 executor 自行发现的**：它改动后被 `lint --strict` 捕获，随即回退自己的修改并如实报告，而非改动另一侧或放任红门禁——正是 b34 briefing 失误想要建立的行为，此次无需提示即自发出现。
- **证据锚点缺口（非审校缺口）**：`gates-of-morning-main`、`jewelry-store`、`last-hope-melinda-father`、`last-hope-weapon-store`、`limmir-valley-moon` 五个 section 在 `evidence/quality/p2-batches/` 无受跟踪工作集。五者字母序均在 `sorcerer-fight.lua` 之前，属 b6–b21 已审范围，`limmir-valley-moon.lua` 更明确记为 b21「已核验无改动」。缺的是审计锚点，源于已记录的 b19–b21「工作集只留在被忽略的 `.ai/`」失误。**重建锚点是独立的文档任务，未擅自开展。**

- b36：**`data/lore/` 首批** —— `age-allure.lua`、`age-pyre.lua`、`angolwen.lua`、`ardhungol.lua` 共 43 条，提交 `fb8d717`，修订 30 条 target；一轮复审（36/43 `OK`）加一轮修复。
- b36 关键修正（类别错误，出现两次）：`inscriptions` 被译成「纹身」。术语库裁定明确——`inscriptions`＝**刻印** 是 `T.GAME.TALENT_CATEGORY` 行（`preferred`／global），其**子类**才是 `runes`＝符文 与 `infusions`＝纹身；该段落讲的正是符文亲和与符文需定期维护，用同级子类「纹身」恰好把主题排除在外，且语料 UI 一律作「刻印」。已改回「刻印」；同一批字符串中残留的「纹身」经核验均对应英文 `infusion`，子类与上位类现已各归其位。
- b36 其他主要修正：`Cataclysm` 与 `Spellblaze` 是**两个不同事件**，宝库条目讲的是「大灾变的地壳剧变绕过已毁隧道」，原译写成魔法大爆炸；监督者的命令原译「永久沉睡」，固定源码 `age-allure.lua:241` 是把炼金药瓶放进通风系统「无痛窒息」全体人员——委婉语掩盖了这道屠杀命令，而叙述者随后正是拒绝执行它；长老会「认为攻击倾向利于士气因而把治疗推迟到战后」这一**决定**被写成「战后可以轻松治疗」，既丢了决定也凭空加了「轻松」；敌方斥候的发现与围困是**已完成**的事实，原译写成哨兵正准备动手；`ardhungol` 清理行动的对象是太阳骑士的**巢穴**（说话者的蔑称），原译写成杀灭太阳骑士本人。
- b36 驳回并上呈的两条：`Atamathon, the giant golem` 保留「阿塔玛森·傀儡之王」、`The spellblade` 保留「魔宗利刃」。复审指出「傀儡之王」「魔宗」都添加了英文没有的身份／门派关系，**这一点成立**；但两者均受实体名支配（`t("Atamathon the Giant Golem", "傀儡之王阿塔玛森", "entity name")`、`t("Spellblade", "魔宗利刃", "entity name")`），只改叙述文本会让文本与玩家所见的实体名脱节，而改实体名属术语层裁决。故窗口内驳回、作为术语议题上呈。注意 `Atamathon` 语料本已分裂：成就行用的是忠实的「巨型傀儡阿塔玛森」。
- b36 宿主核查：本批修订率 25/43（58%），显著高于对话批次的 20–40%，故在接受前对三条最高风险论断逐条比对固定源码（Cataclysm、无痛窒息、高阶太阳骑士艾琳），均成立，判定为 lore 长文本的真实漂移而非 SPEC 禁止的流畅度改写。

- b37：`arena.lua`、`blighted-ruins.lua`、`daikara.lua`、`derth.lua`、`dreadfell.lua` 共 47 条，提交 `f3790d9`，修订 36 条 target（含 1 条条件性越界 collateral）；一轮复审（42/47 `OK`）加一轮修复。
- b37 主线：**恐惧王座领主的逐处裁决**。b32 已确立——该角色本身是「领主」（实体名 `t("The Master","领主","entity name")`），而「主人」表达的是支配／占有关系；b27 要求逐处判断。本窗口原为「主人」12 处、「领主」0 处，现改为角色指称 10 处作「领主」（笔记与书信的物品名、三封信的署名、`slain master`、从其僵死双手夺走法杖），支配关系 4 处保留「主人」（他称呼奴仆时的 `your (great) Master`、`served your Master well`、儿童体诗的 `Me like Master`）。石板诗中的九个并列称号按**修辞性同位语**保留为「……之主」，未按实体名处理。以上全部通过复审，无一条被提出异议。
- b37 条件性 collateral：因窗口内三封信的物品名改为「领主写给……的信」，若不动 `mod-tome/data/zones/dreadfell/objects.lua` 的同类物品名「主人的信」，原本一致的一组物品名反而会被拆散，故按 SPEC 的条件授权一并对齐；已核验该 section 只改动了这一行。
- b37 复审 finding（5 条，同一缺陷类，全部 confirmed）：`daikara.lua` 探险队日记的标题格式为「姓名，种族＋职业」，四名成员中 `Sodelost, Dwarf Rogue`＝矮人盗贼、`Xann, Shaloren Wyrmic`＝永恒精灵龙战士**保留了种族**，而瑞丽与高岚的五处标题只剩职务与职业，`Cornac` 被略去。该事实是**承重**的：四人中两人是科纳克人，正是这一点让后续日记里矮人与精灵的「异类感」成立（高岚对矮人的鄙夷、希安对「软皮生物」的疏离）。已按 `creatures.tsv` 的 `Cornac＝科纳克人` 统一补回，复合方式与同侪标题一致（科纳克人战士／科纳克人弓箭手）。宿主对冻结工作集做了机械核验，并确认首条瑞丽日记中出现的种族词属正文提及、不在标题内。
- b37 其他修正：叛乱记述的施事关系颠倒（谁刺穿谁、谁夺剑、谁失踪）；陷阱机制是压力板触发时**按比例混合**药剂而非组装装置，效果分别为龙火与寒冰；`incapacitate` 的非致命制服被泛化为击退，并补回向安格利文发送求救讯息；领主惩戒令中「一千骷髅发配／二百五十处决」与「卡·普尔早已死去」；复数化的矮人数量改回单指波法斯特。
- b37 保留项：一条被弄脏的诗歌键与范围外 objects section 共享，executor 改动后被 `lint --strict` 捕获，**自行回退并如实报告**，未改动另一侧——这是连续第三批 executor 无需提示即出现该行为。

- b38：`elvala.lua`、`fearscape.lua`、`fun.lua`、`high-peak.lua` 共 52 条，修订 22 条 target（10/3/6/3）。四轮有界 FIX 解决了魔法大爆炸回忆录中的人物关系、战术动作、事件时序与因果错误，恶魔空间祭坛措辞，喜剧诗歌／亡灵指南的原意，以及巅峰日志语义。五份有效全量复审均通过 52/52 冻结 evidence 校验；三次畸形 review 输出按 failure-close 归档，未接受其中意见。四次高级范围校准最终关闭全部 finding，未开启第五轮 FIX。五步门禁、464 项工具链单测、完整 `tools/ci-gates.sh` 12/12（含构建）与 `DONE_VERIFIED` 均通过。受跟踪记录为 `p2-tome-texts-b38-lore-elvala-high-peak.json` 与 `p2-tome-texts-b38-adjudication.json`。
- b39：`infinite-dungeon.lua`、`iron-throne.lua` 共 42 条，修订 22 条 target（12/10）。一轮有界 FIX 在猎神神话、钢铁王座财务与远征记录的初审基础上，恢复七处实体“铭文”、奥术与火焰的双重元素指向，并统一“地城废墟”。第二轮全量复审仅余三条 `Deep Bellow` 报告标题意见；高级范围校准将其作为不可拆分的仓库级专名组统一驳回，避免把范围外稳定使用的“无尽深渊”局部拆成同名异译。五步门禁、464 项工具链单测和完整 CI 12/12（含构建）均通过。受跟踪记录为 `p2-tome-texts-b39-lore-infinite-dungeon-iron-throne.json` 与 `p2-tome-texts-b39-adjudication.json`。
- 接手步骤：`data/chats/` 已于 b35 全部完成（100 个 section，b6–b35）。`data/lore/` 共 34 个 section／582 条，b36–b39 已完成 15 个 section／184 条；剩余 19 个 section／398 条。下一批 b40 为 `keepsake.lua`＋`kor-pul.lua` 共 41 条；`misc.lua`（110）与 `last-hope.lua`（71）各自单独成批。

**术语批次已于 `de44127` 完成**（详见下文「已完成」）。原文如下保留作为记录：**下一步不是 b37，而是一个专门的术语批次。** 维护者已于 2026-08-25 裁定两项统一：`Angolwen`＝**安格利文**（10 处／6 个 section），`Maj'Eyal`＝**马基·埃亚尔**（带间隔点，55 处／33 个 section）。后者更棘手：术语行当前持有的恰是被否决的写法（`Maj'Eyal 马基埃亚尔`，`existing`），需改写行的 target 而非仅提升状态；且波及 `init.lua`、`class/Game.lua`、`class/uiset/Minimalist.lua`、成就、出生世界、区域 grids 等非叙事文件。按 `Ziguranth`（`1a4a236`＋`8fb41dd`）的先例作为**独立术语批次**执行，五步门禁后追加三项术语审计，不并入任何叙事切片。完成后再开 b37（`arena`、`blighted-ruins`、`daikara`、`derth`、`dreadfell`），届时 `derth.lua` 已干净。——**均已完成**：术语批次 `de44127`（`安格列文`／`马基埃亚尔` 残留归零，计数 60／126 与基线算术吻合，复审以哨兵替换法证明无附带改动），b37 `f3790d9`。

## 当前进度

**维护者已明确恢复连续批次模式。** b39 已完成；下一批从 b40 开始，无需逐批确认。

`data/lore/` 34 个 section／582 条中，已完成 15 个 section／184 条（b36–b39），**剩余 19 个 section／398 条，约 7 个切片**：`misc.lua`（110）与 `last-hope.lua`（71）各自单独成批，其余 217 条按约 45 条一批约 5 批。下一切片为 `keepsake`、`kor-pul`（41 条）。

**全局覆盖**：`data/chats/` 100 section／1260 条已完成；`data/texts/` 132 section／176 条按受跟踪证据已完成；`data/lore/` 如上；**`data/quests/` 52 section／514 条受跟踪覆盖为零，且从未列入 P2 范围**（路线图只点名 chats 与 lore）。该目录同属叙事内容，是否纳入需维护者裁决——若纳入，另需约 12 个切片。

`Sholtar` 仍待裁决：实际分布为 2 处「肖塔尔」／4 处「肖塔」（此前记为 2:2 系宿主漏计）。宿主建议「肖尔塔」——音节尾 L 依惯例作「尔」，且同句并列的 `Cornacs`＝科纳克、`Mardrop`＝马卓普 均舍弃 r 尾；三者皆无术语行。`Atamathon`／`spellblade` 亦待裁决。**冻结脚本必须断言取回条数等于该 section 的词法 `t()` 调用数**——b31 就靠这条发现粗略 grep 多算了一条（`trap-priming.lua` 实为 8 条）。每批把冻结工作集写入受跟踪的 `evidence/quality/p2-batches/`；复用上一批的 envelope builder 时先改 revision key 前缀并确认已传 `--limit 500`。连续批次模式下不必逐批请示，按 `AGENTS.md` 的停下条件判断何时交回维护者。
- 复审记录格式注意：`.ai/reviews/` 记录必须带 `status`（或 `result`）且取值属于 `completed`／`completed_with_findings`／`PASS`／`CHANGES_REQUIRED`／`FINDINGS`／`OK`，否则 `ai_state_check.py` 的 `candidate_bindings_valid` 会拒绝 DONE。

## 0. 一句话状态

`p2-tome-texts-b<N>` 轨道已完成 15 个译文批次（2026-08-22 至 08-23）：核心 `mod-tome.lua` 的
`data/texts/intro-*`、全部 `unlock-*`、`data/talents/misc/inscriptions.lua` 全段，以及教程／帮助
文本 part A、教程／帮助文本 part B、竞技场、炼金术士、安格利文与阿尔德胡格对话、工艺工具 UI 与刺客领主对话、遥远太阳化身对话、时空与指挥法杖文本，以及 Conclave、腐化者、德斯镇、恐惧王座、东部传送门、艾德隆位面、埃莉萨、护送任务与堕落艾琳对话。共复核 **690 个 `t(...)` 对**，修订 **157 个 section**，语境审核确认并修复
**62 个 finding**；b1–b5 提交均在本地 `develop`，b6–b15 尚未提交；**未 push、未发布**。

## 1. 批次结果

| 批次 | 口径 | 条目 | 修订区块 | confirmed finding | 提交 |
|---|---|---:|---:|---:|---|
| b1 | `data/texts/intro-*.lua`（18 区块） | 18 | 14/18 | 9 | `5efe265` |
| b2 | `unlock-*.lua` 前 22 区块（adventurer…mage_geomancer） | 44 | 20/22 | 9 | `ff25042` |
| b3 | `data/talents/misc/inscriptions.lua` 全段 | 120 | 17 对 | 4（另 2 条撤回） | `1feed76` → 修正 `9097c6f` |
| b4 | `unlock-*.lua` 其余 21 区块（mage_necromancer…yeek） | 42 | 18/21 | 10 | `f3c6bba` |
| b5 | 教程关卡说明、stats1–9、最后的希望来信（21 区块） | 22 | 16/21 | 7 | `888fc54` |
| b6 | 教程／帮助 part B：calc、scale、tier、timed、tactics、talents、terrain（50 区块） | 50 | 23/50 | 4（另 3 条经高级校准撤回） | 未提交 |
| b7 | `data/chats/arena-start.lua`、`arena-unlock.lua`、`arena.lua` | 65 | 3/3 | 3（波次标签） | 未提交 |
| b8 | 炼金术士 Derth、Elvala、傀儡对话全段；Hermit／Last Hope 共享门锁键 | 93 | 5（3 全段 + 2 单键） | 2（门锁提示语义） | 未提交 |
| b9 | Angolwen 领袖／法杖店、反魔结局、Ardhungol 起止对话 | 46 | 5/5 | 0 | 未提交 |
| b10 | 工艺工具 UI、刺客领主及其喽啰对话 | 29 | 5/5 | 3（所有权、准备过程、复数处置关系） | 未提交 |
| b11 | 遥远太阳解锁与化身对话 | 29 | 2/2 | 0 | 未提交 |
| b12 | 时空异常／时间线／指挥法杖；共享取消键同步至 Ward、傀儡与 Cults | 41 | 6（3 全段 + 3 单键） | 4（取消语义、死后延续、法杖形态、问因） | 未提交 |
| b13 | Conclave 守卫、腐化者招募、德斯镇袭击结局、恐惧王座伏击 | 36 | 4/4 | 0 | 未提交 |
| b14 | 东部传送门结局、艾德隆位面、埃莉萨占卜水晶球与商店对话 | 38 | 4/4 | 0 | 未提交 |
| b15 | 护送任务起止、堕落艾琳对话 | 17 | 3/3 | 1（护卫已死事实） | 未提交 |

finding 数只计语境审核（`translation_contextual_v1`）中宿主裁决为 confirmed 的观察；EXECUTOR 在
读-改阶段直接修正的条目（每批 25–75 行）另见各批次 `evidence/quality/p2-batches/*-host-verification.json`
的 `adjudicated_findings` 与 `items`。每批的工作集冻结文件同目录，均记录 `fixed_source_identity`
（`commit:624a673…`）与逐条 `pinned_source_match`。

典型修正：Point Zero「使时空法术得以存在」（原译为「时空行者方能进入」）；竞技场／无尽地下城
「没有出口」被译成「只有一个出口」；转化之盒凭空多出「无法储存能量」；时空守卫「中型与小型武器」
被译成「或」；堕落者「死星之力」被译成重力；纹身 Wild「减少受到的伤害」；Rune of Vision／
Dissipation 的 `args_order` 误判（见 §3）；最后的希望第二封来信整句遗漏「请务必调查」。

## 2. 本轮基础设施变更（已独立提交、交叉复审）

| 提交 | 内容 |
|---|---|
| `7085a98` | `contextual_anchor_preflight.py` 接受 `ordered_titles: []` 的 whole-section window（契约 2.17-draft）。b1 首次消费 2.16 preflight 时发现其只能表达 Fay Willows 式章节标题锚点，对任何无章节标题的 section 都无法构造合法 SCOPE。 |
| `a2e86d4` | preflight 读取 `t()` 第四参数 `args_order`（规范形式 `{i,j,...}`，接受 `;` 与尾随分隔符），并要求 `bounded_context.context` 精确披露 `args_order={...}` 标记，否则 fail closed（契约 2.18-draft；标记入 `paseo_contract_check` 与 toolchain inventory）。 |
| `90acafe` + `d347d52` | 术语表新增 `Keeper of Reality=现实守护者`、`Wayist=维网信徒`；`d347d52` 修复 `90acafe` 未同步 `test_real_terminology_is_fully_mapped` 的 708→710 行数而导致的红 HEAD。 |

## 3. 必须知道的教训

1. **`args_order` 是一等机制。** `t(source, target, tag, {2,1})` 的第四参数在运行时重排格式参数；
   `mod-tome.lua` 中有 51 条。lint 的 `format-mismatch` 已按 `args_order` 校验转换序列。b3 曾把
   两条带 `args_order` 的条目误判为「占位符顺序缺陷」，并在改写文本后遗留 `{2,1}`，引入真实回归
   （`1feed76`），随即由 `9097c6f` 修正、`779a4d3` 撤回证据中的两条 finding。任何重排译文占位符
   都必须同时更新或删除 `args_order`；宿主与 reviewer 检查占位符顺序时必须读取第四参数。
2. **术语行变更后必须重跑完整 toolchain 单测。** `tests/i18n/test_toolchain.py` 硬编码术语行数
   （现为 710）与 orchestrator.md 标记清单；只跑 preflight 或审计脚本会漏掉它。
3. **共享 runtime key 的术语修正会触发跨组件碰撞门禁。** b3 的「相位之门」落在与
   `tome-ashes-urhrok.lua` 共享的 `logPlayer` 键上；按 `docs/runtime-key-collisions.md` §3.3 先例，
   以 SPEC 修订把 DLC 行对齐为相同译文，而不是回退术语。
4. **reviewer 每轮重看整段。** 长段落通常需要 2–3 轮 FIX／复审才能收敛；这是正常成本，不要跳过
   复审。
5. **结果校验要机械化。** 从 Paseo activity 取回完整 JSON，按冻结 envelope 逐条 byte-compare
   evidence、顺序与 identity（b3 起已如此），不要目测。
6. **不要在工作树上用空的 `git stash`/`stash pop` 对。** 本轮一次 smoke test 误弹出了前一会话的
   stash；已折回 `stash@{0}`（README 链接 + `dependencies/` + `docs/container-dependency-inventory.md`），
   `stash@{1}` 为更早的 `infra-contract-008…` WIP，均未并入任何提交，去留由维护者决定。

## 4. 未完成与下一步

- **batch 6–7 已完成、待单独提交：** b6 为 `data/texts/tutorial/stats*/` 其余 50 条单对 section
  （calc0–11、scale1–12、tier0–12、timed0–8、tactics1–2、talents、terrain）。复核重点为公式、
  百分比、算例与运行时 UI 标签；b7 为竞技场的开始、解锁和对局对话，复核重点为人物关系、奖励与
  波次模式。两批的完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 8 已完成、待单独提交：** `alchemist-derth.lua`、`alchemist-elvala.lua`、
  `alchemist-golem.lua` 全段，并为 strict runtime-collision 门禁把 `alchemist-hermit.lua`、
  `alchemist-last-hope.lua` 的同一门锁提示对齐为“门锁着，无人回应你的敲门声”。93 条均经二轮
  `translation_contextual_v1` 冻结复审；完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 9 已完成、待单独提交：** `angolwen-leader.lua`、`angolwen-staves-store.lua`、`antimagic-end.lua`、
  `ardhungol-end.lua`、`ardhungol-start.lua` 共 46 条；语境审核全部 OK，完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 10 已完成、待单独提交：** `artifact-maker.lua`、`artifice-mastery.lua`、`artifice.lua`、
  `assassin-lord-thieves.lua`、`assassin-lord.lua` 共 29 条；三轮语境审核确认并修正了盗贼领主的
  所有权语气、工艺准备过程与“我们该怎么处置你”的复数关系，完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 11 已完成、待单独提交：** `avatar-distant-sun-unlock.chat`、`avatar-distant-sun.chat` 共 29 条；
  语境审核全部 OK，保留遥远太阳由伪善友好转为操控不耐的语气、烈焰展示、化身状态与拒绝后的觉醒点返还；完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 12 已完成、待单独提交：** `chronomancy-bias-weave.lua`、`chronomancy-see-threads.lua`、`command-staff.lua`
  共 40 条，并同步 3 个共享运行时键（Ward、炼金傀儡、Cults 的龙血形态菜单）。41 条均经五轮
  `translation_contextual_v1` 冻结复审；共享 `Never mind` 键统一为“算了。”，跨组件碰撞归零；完整五步门禁、
  `tools/ci-gates.sh` 与状态契约检查均已通过。
- **batch 13 已完成、待单独提交：** `conclave-vault-greeting.lua`、`corruptor-quest.lua`、
  `derth-attack-over.lua`、`dreadfell-ambush.lua` 共 36 条；语境审核全部 OK，修正了 Conclave 守卫的时代错位、
  腐化者对魔法大爆炸裂隙的利用、德斯镇雷暴袭击的主谓关系与乌克鲁克索要法杖的威胁；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 14 已完成、待单独提交：** `east-portal-end.lua`、`eidolon-plane.lua`、
  `elisa-orb-scrying.lua`、`elisa-shop.lua` 共 38 条；语境审核全部 OK，保留东部传送门的部件交接、
  艾德隆位面的死亡／去留分支、维网识别流程及埃莉萨水晶球的远程通话和普通物品自动鉴定机制；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 15 已完成、待单独提交：** `escort-quest-start.lua`、`escort-quest.lua`、
  `fallen-aeryn.lua` 共 17 条；二轮语境审核确认并修正了堕落艾琳控诉中“有人为保护玩家而死”的既成伤亡事实，
  保留反魔护送分支将 NPC 送往伊格、自然之力使传送门失效及艾琳的毁灭轮回问责；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- 下一候选：`data/chats/`、`data/lore/` 的有界切片；按当前持续处理指示继续选择下一批。
- 已知 advisory（未改）：教程 intro「Tales of Maj'Eyal」作 ToME 4；竞技场标题「挑战主宰」；
  Vim 定义句用「活力」；岩石守卫「分身」。`Maj'Eyal` 在文件内 马基·埃亚尔／马基埃亚尔 并存，
  只在批次内统一，不做全局替换。
- P3 事项不变：`develop → master` PR、正式 release、teaa／te4.org／创意工坊发布均需新指示。

## 5. 单批操作清单（b5 实际流程）

1. 冻结工作集到 `evidence/quality/p2-batches/<batch>.json`：逐条用 `git show 624a673:<path>` 核验
   英文键，并记录每个调用的 `args_order`。
2. 写 `.ai/task/<task>/SPEC.md|PLAN.md|STATE.json`（schema 3、`change_class: standard`、
   `review_contracts: ["translation_contextual_v1"]`）。
3. EXECUTOR（Luna，`auto-review`/xhigh）读-改；宿主核验范围、英文键零变更、行结构，归档。
4. `SCOPE.json`（每个 section `ordered_titles: []`）→ 七键 payload（`bounded_context` 对带
   `args_order` 的调用写入 `args_order={...}`）→ `tools/contextual_anchor_preflight.py` →
   紧凑规范 envelope → REVIEWER（Sol）按契约第四节三行 prompt 派发，labels 含
   `candidate_identity`/`dispatch_id`。
5. 取回 activity 原文机械校验；宿主按固定源码裁决；confirmed 进 fresh EXECUTOR FIX，重新冻结
   envelope 复审，直至全部 OK。
6. 五步门禁 + `tools/ci-gates.sh`（含构建）→ 宿主核验记录 → `ai_state_check.py` DONE →
   单独提交译文批次；roadmap/记忆随后单独提交。
