# 已确认问题模式的全文检索（2026-11-13）

- **任务**：维护者「请对频繁发现的相同翻译问题进行全文搜索」。只做检索、核对和清单。确认的问题按既有授权用 lite 批修复，命名策略单列待维护者决定。本次没有开展游戏测试。
- **基线**：本仓库 `6ef227f9322d`（检索时的 HEAD）；游戏源码固定 commit `624a67329fe2`；DLC 用公开检出 `/workspace/tome4-dlcs`（来源未固定）。术语库 `terminology/*.tsv` 拼接后 sha256 前 16 位为 `743d97070c99ce21`。
- **纳入**：release-required 有效条目共 29,554 个，取自 `i18nlib.full_review.current_units`，与 lite 审核同一口径。
  - mod-tome.lua 21,697
  - engine.lua 1,061
  - tome-ashes-urhrok.lua 849
  - tome-cults.lua 2,043
  - tome-orcs.lua 3,904
  - 行号由 `load2.py` 按源串定位，29,554 条全部定位成功。
- **排除**：
  - possessors / items-vault / addon-dev / example 两个（outside-release）和 mod-boot（boot 继承），不进发布；
  - `*.copy.lua`、`_not_merged.lua`、`_tdef_append.lua`；
  - 注释掉的 untranslated 块；
  - evidence 下的历史快照与旧批次 input；
  - Cults DLC 自带的 zh_hans.lua 只作参照。
- **计数口径**：「原始命中」指正则或字段命中的出现次数；「对象」指去重后的有效条目，或同一游戏对象（技能、显示调用点）；「根因」指同一类成因。正则没有命中，不代表没有同类语义错误。

## 汇总

| 模式 | 原始命中 | 去重对象 | 新 confirmed（已修） | pending | advisory | 回归锚点 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 同一机制叫法 | 英文 detect/detection power 7 条；中文侦测强度 18 行、侦测能力 5 行；潜行/隐形侦测英文 10 条 | 17 条 | 0 | 0 | 1 根因（潜行/隐形侦测叫法多样） | 侦察强度 0、侦测点数 0（0498/0499 已修） |
| 2 不同对象同名 | 名称类条目 6,514，同译组 128 | 技能↔技能 23 组（47 个技能对象） | 0 | 23 组，待命名决定 | ego 前后缀同译 18 组等 | 致命打击只剩 Death Blow（0498） |
| 3 同族格式 | 「： 」92 处；重复字 13 处 | 92 / 13 | 11 条（2 个根因） | 0 | 5 条调试界面标签；1 处「使使用者」 | 心眼/清晰梦境/避免压力陷阱已无尾空格（0496） |
| 4 正文残留英文缩写 | 目标文大写词约 36 种；带点缩写保留 5 种 | 13 条 | 3 条（2 个根因） | 0 | 若干有意保留 | APE 0 处（0496） |
| 5 条件限定的同源句 | 17 条 | 17 条 | 0 | 0 | 0 | 危机感知限定、利牙项环断口均已修（0499/0501） |
| 6 窄列短标签 | CreateTinker 4 列 + 同类窄列 28 处 | 40 余个取值 | 0 | 0 | 1（配件槽位列，上游英文同样超宽） | 状态列已改为「可制作 %s 级」（0503，11 单位，接近上限，未在游戏中复测） |

新确认的 14 条已在 lite 批 **0505** 修复（门禁、提交与 0506 盲审见下文「收口」）。

## 1. 同一机制叫法（以危机感知、解除陷阱为锚）

- **搜索式**：英文 `detect(ion)? ?'?power'?`（大小写不敏感）；中文 `侦察强度|侦测强度|侦测点数|侦测能力|侦察能力|探测强度|侦查强度|察觉强度|侦测力|侦察力`；潜行/隐形侦测：`stealth detection|invisibility detection|detect(ion)? (stealth|invisib)`，以及中文 `潜行侦测|隐形侦测|侦测潜行|侦测隐形|侦察潜行|看破隐形` 等。
- **陷阱侦测强度**（see_traps / detect 'power'）全部统一为「侦测强度」，解除强度统一为「解除强度」：mod-tome.lua:21452/21459/21466/22269/22275/22283/23560/23563/23571/23643/26318/27498 等。
- **advisory（1 个根因）**：潜行/隐形侦测（see_stealth / see_invisible，与陷阱侦测强度不是同一个数值）有多种写法：潜行侦测 6、侦测潜行 8、隐形侦测 7、侦测隐形 11、侦察潜行 1、看破隐形 1，后缀还混用「等级」「能力」「强度」。例如：
  - mod-tome.lua:23543「侦察潜行和隐身的能力增加 %d」；
  - :26567「提升侦测潜行等级 %d」；
  - :22058「隐形侦测能力 +%d」；
  - tome-orcs.lua:5048「潜行侦测、隐形侦测和陷阱侦测能力」。
  - 意思都清楚，也没有像锚点那样在同一句里给同一个数值起两个名字，所以不判 confirmed。是否统一成一个术语属于术语决定。

## 2. 不同对象同名（以 Deadly Strikes / Death Blow 为锚）

- **方法**：名称池为 talent name、entity name、damage type，以及 timed_effects 段内标题式的 `_t`（效果名），共 6,514 条、5,156 个不同译名。按中文分组，英文规范化（只保留小写字母和数字）后有不同来源的为同译组，共 128 组（`p2-name-collision-groups.json`）。
- **排除**：
  - 技能与其自身效果或伤害类型同名（例如「沉默」对应 Silence、Silenced、silence），这是本库正常做法；
  - 上游垃圾英文 3 组（Indiscernible Anatomyblabla、Mutated Hereragegand、Lash Outrthrthrth）；
  - 同一技能的两种拼写 1 组（Shadow Empathy / Shadows Empathy）。
- **pending：技能↔技能 23 组**（`p2-talent-name-pending.json`，含定义文件与行号、玩家/NPC/召唤物/配件身份）：
  - 强候选（不同的玩家技能同名）：
    - 重组：Re-assemble / Realign / Reform / Rethread，共 4 个；
    - 地震：Earthquake / Quake；
    - 无情：Brutality / Pitiless；
    - 奥术充能：Arcane Feed / Eldritch Infusion；
    - 双重射击：Dual Arrows / Double Shots；
    - 肢解：Dismember / Mow Down；
    - 坚定意志：Resolve / Unbreakable Will；
    - 快速射击：Quick Shot / Swift Shot；
    - 迅捷：Celerity / Quickened；
    - 烟雾弹：Smoke Bomb / Smokescreen；
    - 致命恐惧：Mortal Terror / Terrorize。
  - 玩家↔NPC：寒冰箭（Ice Shards / Ice Bolt）、腐蚀酸雾（Corrosive Mist / Corrosive Vapour）、压制（Dominate / Overpower）、减速（Slow / Speed Sap）。
  - 玩家↔召唤物/配件：火焰喷射（Flamespit / Flame Jet）、燃烧弹（Incendiary Ammunition / Incendiary Shell）、闪光弹（Flare / Flare Shell）。
  - 弱（概念相近）：有丝分裂、酸液喷吐、毒性喷吐、自然治愈（NPC 与 NPC）、火箭发射器（玩家与炮塔）。
  - 这些都是纯名称问题，改名会跨多条日志或说明。是否改、改哪些，属于新的命名决定。按维护者要求先交候选，**没有自动改名**；如获授权，可沿用「纯名称交 Gemini、双向查重」的既有机制分组处理。
- **advisory**：ego 前后缀同译 18 组（如 mighty / powerful 都译「强大的」，caustic / corrosive 都译「腐蚀的」）。同名 ego 可能带不同属性，但这是长期既有译法，不在本次范围内改。

## 3. 同族格式

- **全角冒号后的半角空格**，搜索式 `：[ ]`，共 92 处：
  - 72 处是 lint 要求的，保留：62 处在占位符前，8 处在数字前，2 处在技能 tformat 文本前。依据是 `tools/i18nlib/lint.py` 中的 `placeholder_spacing_offsets`，以及上轮 0498 的实测（删掉后 lint 报错）。
  - 13 处在字符串末尾，属于「标签 + 值」拼接（与 0496 同族）：
    - **confirmed 8 条，已修**：
      - engine.lua:743（ShowAchievements.lua:123）；
      - engine.lua:924/927（UserInfo.lua:35/42）；
      - mod-tome.lua:2324（uiset/Classic.lua:422）；
      - mod-tome.lua:9225（boss-artifacts-maj-eyal.lua:46）；
      - mod-tome.lua:41969/41972（LevelupDialog.lua:1000/1030/1039/1046）；
      - tome-ashes-urhrok.lua:1907（DemonologistsDLC.lua:57）。
      - 依据：`docs/review-operations-guide.md` 6.3，冒号标签不保留尾随空格。
    - **advisory 5 条**：调试界面 AdvanceActor ×4（mod-tome.lua:42381/42386/42387/42389）和 PlotTalent ×1（:42561），属于开发工具，不改。
  - 7 处在正文前：
    - **confirmed 3 条，已修**：「区域效果： 」（mod-tome.lua:36697/36705/36707），同族 23 条中其余 20 条都没有空格。
    - 4 处是有意的列对齐，保留：弹药 2 处、属性表头、统计页。
- **重复字**，搜索式 `的的|被被|了了|在在|和和|是是|…`（共 25 种），13 处命中，全部是合法组合：正在在线、实实在在、动不了了、为了了解、议会会议、目的的等。mod-tome.lua:26356「使使用者在耀眼的闪光中爆炸」语法正确但读起来别扭，记 advisory。
- 数值与汉字之间的空格（「%d 点」）是本库惯例，本次不作为问题检索。

## 4. 已翻专名在正文仍用英文缩写（以 APE 为锚）

- **方法**：在含中文的目标文里，屏蔽颜色码和占位符后找连续大写词；再在英文源串里找带点缩写和 3–5 字母的大写词，统计哪些被保留到目标文。
- **APE**：0 处，0496 已修。tome-orcs.lua:6028「便携式自动材料提取仪（A.P.E.）」是全名首次出现时括注缩写，保留。
- **confirmed 3 条，已修**：
  - tome-orcs.lua:2184「这里是 H.C. 帕默」：H.C. 即 Haze Commander，同一任务线 :2130 已译作「阴霾指挥官帕默」，改为「阴霾指挥官帕默」；
  - tome-orcs.lua:2875「准备好GEM」：英文是 G.E.M.，与其余 5 条（:7028/7038/7059–7061）统一为 G.E.M.；
  - tome-orcs.lua:2130「地热探测鼹鼠GEM」：改为「地热探测鼹鼠（G.E.M.）」。
- **保留**：
  - 界面与游戏用语：WASD、DLC、NPC、UI、HUD、FPS、CPU、ESC、TAB、CTRL、PNG、AI、BOSS；
  - 世界内未翻译的古文：AMAKTHEL、SHER'TUL；
  - 版本号 V1/V2、时间线编号 E4-RL/E4-EXPADV、商店名 AAA、占位名 XXX；
  - 物品专名 S.H. Spear（S.H.长矛）、S.M.A.C.K.。
  - AST、RCHID 是屏蔽颜色码时产生的误报。

## 5. 条件/限定遗漏的同源句（以可豁免限定、neck stump 为锚）

- **搜索式**：`can be resisted|resistible|resistable|that can be (saved|resisted)|stump`（大小写不敏感），17 条命中，逐条对照整句：
  - 锚点 2 条已修：mod-tome.lua:23555（0499）、tome-cults.lua:767（0501）；
  - 其余 15 条正确：
    - irresistible / unresistable 分别译作「无视伤害抗性」「无法减免」「无法抵抗」「不可抗拒」：mod-tome.lua:23429/25428、ashes:1190、cults:2843、orcs:6506；
    - 「可以被抵抗，但不能被豁免」：mod-tome.lua:25959/25966；
    - stump-kneed→两腿短粗、stumpfoot→树桩脚：mod-tome.lua:14446/16792；
    - 无御之日（Irresistible Sun）同族一致：mod-tome.lua:31598/31631/35303/35306/35308，以及 34267。
- **说明**：这只是关键词检索，**不能据此断言全库没有同类语义错误**。删限定词（may/chance/attempts/each）这类缺陷需要逐句复审，不在本次正则范围内。

## 6. 窄列短标签（以 CreateTinker「可制作材质等级」为锚）

- **CreateTinker**（Orcs `overload/mod/dialogs/CreateTinker.lua:56-59`）四列宽度为 配件 45%、槽位 15%、学科 20%、状态 20%。
  - o8d 截图中，20% 列约能容纳 12 个显示单位（汉字记 2，ASCII 记 1）。
  - 状态列现为「可制作 %s 级」= 11 单位、「条件不足」= 8 单位，可以放下，但接近上限；0503 修改后没有在游戏中复测。
  - **advisory**：槽位列 15%（约 9 单位）中，「武器 / 蒸汽枪」13 单位、「护甲 / 布料」11 单位会超宽。不过上游英文（weapon / steamgun，16 个字符）同样超宽，属于上游布局问题，不是译文回归，只是静态风险，没有在游戏中复现。
- **同类窄列**：用正则 `{name=_t"…", width=(≤20),` 在核心、引擎和 DLC 对话框中找到 28 处。UseTalents 状态列的取值（激活、%s 回合、不可用、物品、正在持续、持续、被动技能）最长 8 单位，没有风险。物品栏和商店的「类别」列取值是物品类型名，较短。成就页的「时间」「玩家」列取值是日期和名字，没有逐一评估。

## 收口

- 14 条 confirmed 已在 lite 批 0505 修复（`38c407c0b`，`maintenance.json` 列出调用点与依据），完整门禁通过并经过滤镜像推送。
- 0506 盲审 14 单位：A 判 ISSUE 0；B 判 ISSUE 1，指出「第一级技能等级：1」中「第一级」与「等级」重复。LevelupDialog.lua:1027–1030 只在未学习时显示，后接 traw+1=1，因此改为「初始技能等级：」。0506 提交 `f273f9257`；0507 盲审 A、B 均 ISSUE 0，无改动（`8d76c8e18`）。
- 待维护者决定：
  - pattern 2 的 23 组技能同名是否改名、改哪些。建议先处理玩家与玩家撞名的 11 组，沿用纯名称交 Gemini、双向查重的机制；
  - pattern 1 潜行/隐形侦测是否统一为一个术语。
- 本次没有做全局替换，没有大规模风格改写，没有开新的游戏测试，也没有发布新版本。
- 复现：`load.py`、`load2.py` 生成有效条目集（需要先运行 `current_units` 导出 units.json）；`p2.py`、`p3.py`、`ident.py` 是各模式的检索脚本。
