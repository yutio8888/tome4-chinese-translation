# repair-w56-20260929 实现记录

- 角色：Paseo EXECUTOR（任务内容唯一写入者）
- 固定基线：`0c91b35e8d0e7b3a71904a49b017484e064640e5`
- 范围：仅修改 `engine.lua` 1 条、`mod-tome.lua` 25 条、`tome-orcs.lua` 3 条冻结 target，并新增本目录的 `IMPLEMENTATION.md` 与 `VALIDATION.json`。
- 源码边界：主游戏与引擎只通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取；Orcs 只读取 `SOURCE-ANCHORS.json` 指定 checkout `/workspace/tome4-dlcs/orcs` 下的两个条目路径。29 个查询涉及的 17 个源码文件 SHA-256 全部匹配锚点；Orcs 仓库与 commit 未固定。
- 裁决边界：名称条目整条替换；其余长文本只替换被点名的 the Sorcerers 称呼、盾战士技能名或火刑堆措辞。术语库与其他译文均未修改。

## 逐条改动

1. `036741e71b5ff6ae46537e723c4d0147f9eebd14b66b08d2e157505bae990515`：`两个魔法师死在你面前` → `两名巫师死在你面前`；`两名魔法师及其神明` → `两名巫师及其神明`。
2. `3af81c1b820cd09ebd2c9b4ba246016c241b29c62b5c321510088abf2fd734a2`：`那些妄图扭曲这个世界的法师` → `那些妄图扭曲这个世界的巫师`。
3. `4a03387e2676ed5725aa248ad42cbde5f9706eec6040090ea7f54e3b0e722a27`（` of thunder`）：`闪电之` → `雷霆之`。
4. `5a43141ad559cf5c9da26787365769c5335643ffaf3f77da8808302c1a10cf75`：`击败了那些法师` → `击败了那些巫师`。
5. `5edb36c4131bb64e743009b48f2e3137a644fe116c2941d9b274109520b52094`：`那些法师已经离开了` → `那些巫师已经离开了`。
6. `6c3cb88d83c6d6bf288a612ac5581f73ab4365fe3102f692e3b2cf0fa86e56dc`：`法师惨遭失败！` → `巫师们惨遭失败！`。
7. `839c8e5e9deb78ac98da61dccda4be01a3ccfab945e588dd9ef84a7fe3992788`（`Sorcerers`）：`法师` → `巫师`。
8. `942d0dd6bc974f411ae72d744cdb6783ecb5b26b39d244c8cd0e4ff1026c87d1`（`and burned on a pyre`）：`并被绑在火刑柱上烧死` → `并被送上火刑堆焚烧`。
9. `997d130491af0d5c5ce9a74d3577f4390c04243e05067ebd3f0d8aae3368e2d4`：`击败了那些法师` → `击败了那些巫师`。
10. `9b8fe2f7b4dd50444d6036ba904b7eaed7cb0919ae4ab6f6b887747efac70ba8`：`两个魔法师死在你面前` → `两名巫师死在你面前`；`搜索魔法师的遗骸` → `搜索巫师们的遗骸`。
11. `9d36aba0a7eb993bbbe72b784765f6600777597596d8c6b851948ff1a85340e0`：`法师已经死去` → `巫师们已经死去`。
12. `a1d6552e3b4656a10f26197bb7787e7b5094c4da9529eb2134e309d3dffc81d5`：`法师们的圣所` → `巫师们的圣所`。
13. `ad393c549eb1ae82cb154bee91abd3940aee3caad6482fe47ab47e9ca5d5ee84`：`两个魔法师死在你面前` → `两名巫师死在你面前`。
14. `af860be63679a6b66994e10c9a5a31fb79e9e3c7f54ac4bd494a1fffe06c6878`（`Twist the Knife`）：`扭曲刀刃` → `伤口拧刀`。
15. `b01c3be48af2c6428be3f4a6e2fbf36d9258b6a45d97de23cbd6fa7fd2908e72`（`Armour Configuration`）：`护甲掌握` → `护甲改装`。
16. `b05f9ea51bc3f87ad402b79d1028cc96e3b3dda9c62752b897e328d918430d4e`（`Harass Prey`）：`痛苦折磨` → `袭扰猎物`。
17. `b06ed2a53c2a54d4cb985f71e4ac8ca72edf79cb0663797cdd3268c8066b8e4c`（`thunder`）：`闪电` → `雷霆`。
18. `b2d7feea6e2bb6d4009998d9292e2987efd2215bdeb84384ad3c827d92224935`（`Knowledge of the Way`）：`维网的力量` → `维网之识`。
19. `b46f9f28342d3c7d945e9e0055fc9b47d0a53694c4aac069a9354c41a9e8a319`（`Eldritch Pearl`）：`埃尔德里奇珍珠` → `骇异珍珠`。
20. `bab5f2f9540bc880b92b9a19f7f41cf4949ec0ff4af013a1d4200781d6e07783`（`Cursed Bolt`）：`诅咒之球` → `诅咒之箭`。
21. `c18aa57452a1cc906acafdc104a3b428894b00f18ecf364b29b8bbaa13a00c75`：`击败了那些法师` → `击败了那些巫师`。
22. `d9b49ce5bc89333e6dac88af1bef9c71769d12b93e30737eaffdd2e7ad206cbe`：`关闭了法师的远行传送门` → `关闭了巫师们的远行传送门`。
23. `dbb3e0495b68f86f95a092d1dea607294d2ec1d0fe45d71d2ecc925fdb61de69`：仅在长 lore 中将最终首领二人组的 `那两位法师／这两位法师／法师们／两位法师` 分别改为 `那两名巫师／这两名巫师／巫师们／两名巫师`；保留“死灵法师”等其他称呼。
24. `dd1c2b2cbca7a89ee05ce701ad76494c4cf9ac3dafeb6b956ff59eabc70686ab`：`法师们已经离去` → `巫师们已经离去`。
25. `de6b64b002430774092ddb4aecba444ae3be48299a729c1eab3927bc6c34fafc`：`法师被消灭` → `巫师们被消灭`。
26. `e703fc0a27b8c8c9ee9f1a48e09fcd2b01a23388c29947516b76defb69347927`：`两个魔法师站在你面前` → `两名巫师站在你面前`。
27. `ed8d6c4b0b9c41cea7d836924b10ed6aad799b3861f897a525b4e9ad224ef903`：`消灭了那些法师` → `消灭了那些巫师`。
28. `ef9189014fb1a40a2feb4a2965c2063aa1d415ffab58f860428ddfcda9880996`：`两个魔法师死在你面前` → `两名巫师死在你面前`。
29. `f37f2d4a4a19b496294797c55adc7abbed87b1eda90d3b9993897f12f096ec65`（盾战士 info 技能列表）：`护甲掌握` → `重甲训练`。

## 验证摘要

- manifest-compatible LuaJIT 加载固定基线与当前 `engine.lua`、`mod-tome.lua`、`tome-orcs.lua`：当前分别为 1,169／22,989／4,202 条记录，1,061／21,688／3,904 条翻译；恰 29 条 target 改变，29/29 WORKSET 精确匹配，非 target 字段变化为 0，其他记录不变。
- 29/29 条 source、source_tag、args_order、special、printf placeholder、markup、LF 与逐行 TAB 结构不变量通过；未新增行尾空白。
- `python3 -B tools/i18n lint --strict`：通过，检查 30,308 条翻译，0 errors、0 warnings。
- `git diff --check`：通过。

## 边界与未改观察

- `SOURCE-CLAIMS.json` 将火刑堆调用点简写为 `class/interface/PartyDeath.lua:94`；固定对象中的完整路径为 `game/modules/tome/class/interface/PartyDeath.lua`，第 94 行确认 `killer_message` 前置一个空格后拼接。该路径补全不改变裁决。
- 冻结术语快照把 `Scourge from the West` 记为“西方天灾”，而 Orcs 长 lore 现译仍有“西方灾星”；它不属于本窗口点名的 the Sorcerers 片段，因此仅记录、未改。
- Orcs 长 lore 另有既有生硬措辞，但本窗口是定向称呼修复，均未改写。
- 未 stage、commit、push，未创建 agent，未修改 `.ai/task/` 或术语库。

## Cycle 1 confirmed finding 修复（2026-09-29T14:37:19Z）

- `3af81c1b820cd09ebd2c9b4ba246016c241b29c62b5c321510088abf2fd734a2`
  - 修复前：`找到那些妄图扭曲这个世界的巫师并阻止他们。`
  - 修复后：`找到那些巫师，在他们让世界屈从于自己的意志之前阻止他们。`
- `d9b49ce5bc89333e6dac88af1bef9c71769d12b93e30737eaffdd2e7ad206cbe`
  - 第二段修复前：`今天，他所需要的英雄是一位战斗的大师，一位从吞噬者加库尔的时代以来就未曾出现的大师。他会综合考虑各种各样的可能性，面对无数的困难，有些可能允许一部分的错误，但是最终只会选择一个。`
  - 第二段修复后：`今天，它所需要的英雄是一位战斗的大师，一位从吞噬者加库尔的时代以来就未曾出现的大师。它考虑了几个不同的人选，认定其中许多都不合格，有些在原谅几处失误后或许勉强称职，而最终被选中的只有一个。`
  - 第三段分句修复前：`前往无尽地下城寻求无穷无尽的挑战`
  - 第三段分句修复后：`深入无尽地下城，走向必然的毁灭`
- 该条其余 target、`<?...?>` 模板序列、8 个 LF、段落与空行位置均未改变；其他 27 条及术语库未改。
- 验证：manifest-compatible LuaJIT 加载三文件并与固定基线比较，仍恰 29 条 target 变化（`1/25/3`），WORKSET 精确匹配，非 target 字段变化 0，其他记录不变；strict lint 为 30,308 条、0 errors、0 warnings；`git diff --check` 通过。
- 边界：主游戏原文由 `/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/data/quests/high-peak.lua` 通过 `git show` 取得；Orcs 原文只读取 SOURCE-ANCHORS 指定的 `/workspace/tome4-dlcs/orcs/tome-orcs/data/lore/pocket-time.lua`，来源仓库与 commit 未固定。

## Cycle 2 confirmed finding 修复（2026-09-29T14:46:31Z）

- `d9b49ce5bc89333e6dac88af1bef9c71769d12b93e30737eaffdd2e7ad206cbe`
  - 修复前：`也欠传说中的西方灾星这个机会`
  - 修复后：`也欠传说中的西方天灾这个机会`
- `dbb3e0495b68f86f95a092d1dea607294d2ec1d0fe45d71d2ecc925fdb61de69`
  - 两个分支修复前：`艾格尼尔恐怖的骨盾环绕在她的四周`
  - 两个分支修复后：`艾格尼尔恐怖的骨甲环绕在她的四周`
- 本轮仅修改上述两个 target；其他 27 条、其他文字、`<?...?>` 模板序列、LF、段落与空行位置不变，术语库未改。此轮执行了上一版“西方灾星仅记录、未改”观察之后新确认的裁决。
- 验证：manifest-compatible LuaJIT 加载三文件并与固定基线比较，仍恰 29 条 target 变化（`1/25/3`），WORKSET 精确匹配，非 target 字段变化 0，其他记录不变；strict lint 为 30,308 条、0 errors、0 warnings；`git diff --check` 通过。
- 未 stage、commit、push，未创建 agent，未修改 `.ai/task/` 或术语库。

## Cycle 3 confirmed finding 修复（2026-09-29T14:55:22Z）

- 仅修改 `d9b49ce5bc89333e6dac88af1bef9c71769d12b93e30737eaffdd2e7ad206cbe`：
  - 修复前：`我此生欠你这个机会，也欠传说中的西方天灾这个机会`
  - 修复后：`这个机会，我欠现实中的你，也欠传说中的西方天灾`
  - 修复前：`但<?=Lore.pocket_time_winner.heshe?>很快发现自己面对的东西要么毫无意义，要么只会对埃亚尔的世界有害，不会给故事增添任何内容。`
  - 修复后：`但<?=Lore.pocket_time_winner.heshe?>可能找到的对手要么根本不值一战，要么会直接危害埃亚尔的居民，都不会给故事增添任何内容。`
  - 修复前：`艾德隆也可以创造一个强大到足以击败<?=Lore.pocket_time_winner.himher?>的敌人`
  - 修复后：`艾德隆也可以安排一个强大到足以最终消灭<?=Lore.pocket_time_winner.himher?>的敌人`
  - 修复前：`因此，它将<?=Lore.pocket_time_winner.name?>的名字在脑海中记录下来，愿意一直牢记住<?=Lore.pocket_time_winner.himher?>，直到它找到或者创造了一位真正能够和<?=Lore.pocket_time_winner.himher?>势均力敌的对手。`
  - 修复后：`因此，它将<?=Lore.pocket_time_winner.name?>记在心里，承诺每当它找到或创造出配得上<?=Lore.pocket_time_winner.himher?>的威胁时，都会想起<?=Lore.pocket_time_winner.himher?>。`
- `dbb3e0495b68f86f95a092d1dea607294d2ec1d0fe45d71d2ecc925fdb61de69` 的本轮指摘已驳回，未修改；其他 28 条、本条其余文字、段落与空行、术语库均未修改。
- 验证：manifest-compatible LuaJIT 加载三文件并与固定基线比较，仍恰 29 条 target 变化（`1/25/3`），WORKSET 精确匹配，非 target 字段变化 0，其他记录不变；`<?...?>` 模板序列、8 个 LF 及空行位置不变；strict lint 为 30,308 条、0 errors、0 warnings；`git diff --check` 通过。
- 未 stage、commit、push，未创建 agent，未修改 `.ai/task/` 或术语库。
