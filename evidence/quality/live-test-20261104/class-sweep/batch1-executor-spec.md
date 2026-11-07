# 全职业巡检 第一批修复（执行者规格，2026-11-07）

你是 ToME4 简体中文汉化仓库 `/workspace/tome4-chinese-translation` 的执行者，是本任务唯一的写入者。只修改译文文件 `mod-tome.lua`、`tome-orcs.lua`、`tome-cults.lua`、`tome-ashes-urhrok.lua`（必要时 `engine.lua`），以及下文点名的 `terminology/*.tsv` 行。**不要 git add / commit / push，不要动 evidence/、tools/、tests/。**

输入：`/tmp/clsfix/findings-batch1.jsonl`（68 条实机测试发现，字段 id/shown/english/locale/issue/suggestion）。下面是主代理的逐条裁决。你要对每条：用固定源码核实（`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/...`；DLC 源码在 `/workspace/tome4-dlcs/{orcs,cults,ashes-urhrok}/`），确认问题成立后按裁决修改；核实不成立就不改并说明理由。suggestion 只是参考，最终译文由你按源码写准确、通顺的中文。

## 硬性规则
1. 只改 `t("source", "target", "tag")` 的 target；source 与 tag 一个字节都不能变。改完运行 `python3 /tmp/srccheck.py mod-tome.lua tome-orcs.lua tome-cults.lua tome-ashes-urhrok.lua` 必须全部 `sources identical`。
2. 占位符（%d %s %0.2f %% #Source# @Target# #COLOR# 等）数量与种类不变；**target 的换行数必须等于 source 的换行数**（多行 `[[...]]` 字符串尤其注意，续行的行首 TAB 保持原样）。
3. 升级预览空格规则：技能说明（tformat）中数值占位符所在 token 若连着汉字，须在其与汉字之间插一个 ASCII 空格（如「%d 点」「抗性， %d」）。最终以 `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict` 0 错误为准，lint 报 `talent-placeholder-spacing` 就按它给的 offsets 补空格。
4. 同一 source 在多个组件文件里都有条目时（如 mod-tome.lua 与 tome-orcs.lua 都有），要同步修改。
5. 改名类：除了改名称条目本身，还要 grep 全部译文文件里引用旧名的说明/日志并同步（只改确实指该技能/技能树的地方）。
6. 「统一」类：先 grep 统计，按库内多数译法和下面的裁决统一，只改确实同义的条目。
7. 修改前先查同类问题（同一错误的其他实例），一并修复并在报告里列出。
8. 用 Edit 工具或 Python 精确替换；不要用 shell heredoc 插值写中文；不要整文件重写。

## 裁决
### 改名（用户已授权纯名称交 Gemini 4 Argon 定名，双向检索无冲突）
- cls02-04：Duck and Dodge「闪避」→「俯身闪躲」。
- cls07b-01：技能树 Temporal Guardian「时空守卫」→「时空守护」（职业名 Temporal Warden 仍为「时空守卫」）。
- cls07b-08：技能树 Dream Smith「梦境锻造」→「梦境铁匠」；Dream Forge「梦之熔炉」→「梦境熔炉」。
- cls09-03：矮人种族技能 Stoneskin「石化皮肤」→「坚石肌肤」（法术 Stone Skin 保持「石化皮肤」；注意 Stoneskin 有 talent name 与 _t 两个条目，状态/日志里指矮人技能的同步）。
- cls09-04：技能树 earthen vines「岩石藤蔓」→「大地藤蔓」；技能 Stone Vines 保持「岩石藤蔓」。
- cls09-01：技能树 eldritch shield「魔力盾牌」→「奥术之盾」；eldritch stone「魔法岩石」→「奥术岩石」（技能 Eldritch Stone「奥术岩盾」不变）。
- cls07b-05：Dimensional Anchor「时空锚」→「空间之锚」；Spatial Tether「时空系绳」→「空间系绳」（含 _t 条目、状态名、说明中的引用）。
- 上述 7 项在 `terminology/talents.tsv` 中若已有对应行，改其 target 并在 notes 末尾加「2026-11-07 全职业巡检改名（Gemini 4 Argon）」；没有就不新增行。

### 对齐（以技能/界面现有名称为准）
- cls02-06：去掉 3 个技能名里的「关节技：」前缀（锁钳、抱摔、飓风投），同步引用。
- cls02-08：状态名「小不点的好运」→「小不点的幸运」，同条说明里幸运/好运统一为「幸运」。
- cls04-04：状态名「矮人坚韧」→「钢筋铁骨」（与技能 Resilience of the Dwarves 一致）。
- cls07b-06：开局职业介绍里的「时空行者」→「时空守卫」。
- cls04-08：「转移护盾」→「偏转护盾」；cls04-12：「荒芜大地」→「荒芜之地」（并补译 rapidly）；cls04-14：引用写成技能实际名「游魂行走 - 返回」。
- cls01-01：Crit Reduction 统一（面板标签与提示标题一致，按多数）。

### 统一用词（按库内多数，逐条确认语义相同）
- cls02-03：魔法豁免→法术豁免（magical/spell save）。
- cls02-09 / cls03-04 / cls06-03：melee 的「近程」→「近战」。
- cls04-05：「维持技能」→「持续技能」（sustain）。
- cls04-07：cold damage「冰冷伤害」→「寒冷伤害」（含穿透）。
- cls04-15：die_at「生命底线」→「死亡底线」。
- cls06-05：「所有抵抗」「全体抗性」→「所有抗性」（all resistances）。
- cls07b-02：preferred Paradox「预设值」/「偏好值」统一（按多数）。
- cls07b-04：detection power「侦查强度」/「侦测强度」统一（按多数），同句标点一并整理。
- cls11b-01：「非瞬间」→「非瞬发」。
- cls11-02 / cls11-03：「半径 %d 内」→「半径 %d 格内」，tome-orcs.lua 同类全部检查。
- cls02-07：rough leather 系列统一「粗制皮…」（手套、投石索）。
- cls09-05：降低物理属性的说法统一为「使其一项物理属性（力量、体质或敏捷）降低 %d 点」类句式。
- cls02-01 / cls09-02：职业说明「他们最重要的属性是：…。」全部统一为有冒号、顿号列举、句末句号。

### 错译与语病（核实源码后改）
cls01-02、cls01-03（换行数）、cls01-04（techniques 指所有 technique/* 类，游戏内类别名请查库内 technique 的译法）、cls01-05、cls02-02/cls03-02/cls04-03（`usable during Aether Avatar` 改为名词性短语，如「以太之体下可用」，使「类型：法术和以太之体下可用」通顺）、cls02-05、cls02-10/cls03-03/cls04-10（护盾符文「最多吸收 %d 点伤害，持续 %d 回合」，保持参数顺序）、cls03-01、cls03-05（保持换行数）、cls04-01、cls04-02、cls04-06、cls04-09、cls04-11、cls04-13、cls06-01（%s 两侧加半角空格使体型词成为独立预览 token）、cls06-02、cls06-04（「%d 分之一」写法）、cls06-06、cls07-01、cls07b-03（Foresight 是几率无视暴击）、cls09-06、cls09-07、cls10-01（半径以源码为准）、cls10-02（回合数以源码为准）、cls12-01（DLC 种族说明 #GOLD# 内外的多余空格，同类 3 行）、cls12-02（数值以源码为准）、cls12-03、cls12-04（` class`/` generic` 键：先确认只被该模板使用再去前导空格，否则不改并说明）。

### 不改（插件代码，已延后）
cls07b-07（引擎折行拆数字）、cls11b-02（main/off 武器组名由引擎传入）、cls11-01（上游 %%%% 转义）。

## 完成标准与报告
- lint strict 0 错误；srccheck 全部 identical；`git diff --check` 无输出。
- 写 `/tmp/clsfix/report.json`：数组，每条 `{"id": "...", "status": "applied|rejected|deferred", "files": ["mod-tome.lua:行号", ...], "old": "...", "new": "...", "note": "源码依据或不改理由"}`；同类扩展修改另列 `{"id": "<原id>+similar", ...}`。
- 最终回复只写一行：`EXECUTOR clsfix DONE applied=<n> rejected=<n> deferred=<n>`。
