# 修复窗口 53 实施记录

任务 `repair-w53-20260929` 由唯一 EXECUTOR 执行。主游戏证据仅来自 `/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `git show`；Orcs 证据仅来自 `SOURCE-ANCHORS.json` 指定 checkout `/workspace/tome4-dlcs/orcs` 的两条目标路径。Orcs 两个源码文件的 SHA-256 分别为 `66df49a75a14a56ea59ee37babb5a41886e714e508cdb65016238841695e6450` 与 `0f33aa795edeebd717c42cb2ec844eb8e8aebdefbd906c1f79f697a254de33ef`，与冻结锚点一致；其源码仓库与 commit 未固定。

## 术语行

- `terminology/classes.tsv` / `Archmage`：`status` 从 `existing` 改为 `preferred`；`notes` 从空值改为“用户 2026-09-28 裁决：职业名保留元素法师，不改大法师”。其余六列及其他行不变。

## 18 个 target 的逐条改动

- `07c8b41ef059881216cbea46e8cb9665a7b92e22949afb826cc6574010b03002`
  - 前：`你需要装备投石索才能使用这个技能！`
  - 后：`你需要装备弓或投石索才能使用速射姿态！`
- `2d5fd209cb78540ff89b388c36ccfde8a4fb58195ea00512f66046c920c9d62e`
  - 前：后两段分别以 `\n\t\t\t` 开头。
  - 后：后两段分别以 `\n\t\t` 开头；正文不变。
- `2f0162776a30bb35cc3d54d06e6fc4010ef07e6792f46a559259b66f86e58cf3`
  - 前：`\n 这道门似乎通向西方的钢铁王座。`
  - 后：`\n这道门似乎通向西方的钢铁王座。`
- `3977a0fcaaccd9b500bf707632a311f53acea58c0c790677acf45bba67660bb6`
  - 前：`如果还有没有完全溶解的部分，就往瓶子里放几个小火球。`
  - 后：`如果难以溶解，朝瓶子打几发火球就能解决。`
- `3fbeca0974583c843d096fff5ed1ea65bd55949400e471eb30a6a72f5bf70c36`
  - 前：`巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。`
  - 后：`巨魔主要分为两大类——科兹拉克和马提普，也就是俗称的岩石巨魔和森林巨魔。`
  - 前：`他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。`
  - 后：`他们通常超过8英尺高，有着极为发达的肌肉力量，外皮厚实坚硬，看上去就像煤块或花岗岩。`
  - 前：`他们大约身高6英尺，尽管他们的尾巴可能更长。`
  - 后：`他们在陆地上身高约6英尺，而尾巴还要再长出好几英尺。`
  - 前：`但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。`
  - 后：`但是他们会用珠宝装饰自己，并用海底找到的材料打造武器和盔甲，例如用层层厚鲨鱼皮制成的柔软锁甲。`
  - 前：`这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。`
  - 后：`这表明了一种先进的文明，但迄今为止，与他们沟通都被证明是不可能的。`
  - 前：`最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。`
  - 后：`最主要的理论得到了永恒精灵魔导师们一些研究的支持，该理论似乎表明恶魔来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。`
- `48484bd69e8dc02dd5a93458860703c6a93ac9571142f5d3c4bf177e2a4f22c2`
  - 前：`击退半径 %d 内的其他生物，对每个生物造成 %0.2f 到 %0.2f 物理伤害（基于力量）。`
  - 后：`击退半径 %d 内的其他生物，对每个生物造成 %0.2f 到 %0.2f 物理伤害（基于力量）`
- `4b3491d1633ae0f4195e34de775888e1b5d58b1819e11ed51f9e9347bbc86617`
  - 前：target 以 `公正之王托拉克。` 结束，无末尾 LF。
  - 后：target 以 `公正之王托拉克。\n` 结束。
- `53dcd8e2cf1b784f2a0186f7b76f38a99f8bfc3f7f9e629a19b047a2cc725c2b`
  - 前：`温度极高，以至于 最多 %d 个负面物理状态被高温驱散`
  - 后：`温度极高，以至于最多 %d 个负面物理状态被高温驱散`
- `71970bfdd55272a285b994eea42dfc31e60038b40a51aa298966b194e756c5cf`
  - 前：从“我完全不记得我们是如何幸存下来的”至“至少清醒时……”被两处 `\n\n` 拆成三段；其中为“也许这就是为什么它没有……不！也许我不应该再想它了。”
  - 后：删去这两处 `\n\n`，合为源文对应的单段；句子改为“也许这就是为什么它没有……不！我不会再去想它了。”
- `8eb3c7aee54b0b9db469382be3aaff4db854ff8e6abbb9d75e1faaaaf180c320`
  - 前：`不，别指望你能用这个场景的讽刺性来笑话我。`
  - 后：`不，这其中的讽刺意味我不会看不出来。`
- `b1a06260359cbe02c8136660fb883064420942b1c0d7fb4b0e63878d3e4751be`
  - 前：`学习传送，使你能更快地旅行并追踪他人。`
  - 后：`传送是旅行的法术学派，能让你更快地旅行并追踪他人。`
- `d1f59f125406599041cb4535ea0dc66825fe7ad1eb99f2f433ce49a1486103e6`
  - 前：`\n 这道门似乎通向远东。`
  - 后：`\n这道门似乎通向远东。`
- `d64daff63a7c293e7e22fbe23398d214e4fbc88d6bc886c5f88c317f024ed0ee`
  - 前：`这道传送门并没有和其他传送门相连接。它只是用来探索异度空间的，你不知道它将会把你送到哪里。`
  - 后：`这道远行传送门没有和其他传送门相连，它是为探索而建造的，你无法知道它会把你送到哪里。`
  - 前：`它应该会自动建立起返回的传送门，但可能该传送门不在你所传送的位置。`
  - 后：`它应该会自动建立一道返程传送门，但那道门未必在你抵达区域的附近。`
- `e5f4a107fe581017380012132fab64fdc5df999f86499e3bedc46a6c8e4a005e`
  - 前：`瞄准目标头部发射穿透性弹药，造成 %d%% 武器伤害。\n此次攻击额外获得 100 命中，且能越过你与目标之间的其他敌人。\n只能对被标记的单位使用，命中时消耗该标记。`
  - 后：`瞄准目标头部进行一次精准射击，造成 %d%% 武器伤害，此次攻击额外获得 100 命中，且能越过你与目标之间的其他敌人。\n只能对被标记的单位使用，命中时消耗该标记。`
- `eed96b47b1f76cf0034b56d64e6d69553456debae545d8c45da95f056e662bf0`
  - 前：`有的废墟甚至位于海洋中沉没的大陆上`
  - 后：`有的废墟甚至位于近海沉没的陆地上`
- `fb8138dd842e67a5e73c7b48b847eb00a2dfc20e1e2e8259d3949ca3a05ce2de`
  - 前：`持续 8 回合。  触发几率  在每次你受到打击时提高，同时随时间下降。`
  - 后：`持续 8 回合。触发几率在每次你受到打击时提高，同时随时间下降。`
- `fd03e791df3181e1280a1d9753749fe387b7ed5738da08fbf2f2cba653914663`
  - 前：`影响范围受法术强度加成。`
  - 后：`传送距离受法术强度加成。`
- `fe2acd05e60cc5f480d26d7f812f468b6adfd92862b69228fceb4203f9161613`
  - 前：第二段以“持续 5 回合，每回合回复总吸收伤害的 10%%（强化护盾技能会影响该系数）。”结束，第三段缺失。
  - 后：第二段以“持续 5 回合。”结束；新增与源文对齐的 `\n\t\t`，第三段为“时间回复力场存在的每回合，你将回复总吸收伤害的 10%%（强化护盾技能会影响该系数）。”

## 不变量与范围

manifest 配置的 LuaJIT 经 `LocaleLoader` 加载 HEAD 与工作树：`mod-tome.lua` 21688 条中恰 16 个 WORKSET target 改变，`tome-orcs.lua` 3904 条中恰 2 个改变；其余 25574 条记录及全部非 target 字段不变。18 条的占位符与 markup 顺序保持；指定 5 条的 LF/TAB 结构与源文一致，其余 13 条与 preimage 的 LF/TAB 结构一致。`mod-tome/data/zones/shertul-fortress-caldizar/grids.lua` 的同源 farportal target 经 HEAD/工作树比较确认未变。

## 发现但未改

- 范围外 `mod-tome/data/zones/shertul-fortress-caldizar/grids.lua` 仍保留同源 farportal 的旧 target。由于本范围内条目已修正，strict lint 报 1 个 `runtime-collision`；按 SPEC 不得修改，须由宿主同步后重跑 strict lint。
- `3977a0fca…` 的源文包含 `\n\t\n` 空行 TAB，现译未补；其末尾 TAB 也保持不变。SOURCE-CLAIMS 已将两者列为 advisory，本窗口未改。
- 未发现其他新增疑点。

## 执行边界

本执行未 stage、commit、push、创建 agent 或修改 `.ai/task/`。独立复审、范围外同源同步、完整 17 项门禁、构建、`DONE_VERIFIED` 与发布由宿主继续。

## REVIEW cycle 0 第 1 轮修复

仅修复 `ADJUDICATION-R0.json` 中两条 `status=confirmed` finding；其他 16 条 target、术语库与文件其他记录不动。主游戏证据仅由 `/workspace/t-engine4` 在固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 上执行 `git show` 取得。

- `07c8b41ef059881216cbea46e8cb9665a7b92e22949afb826cc6574010b03002`
  - 前：`你需要装备弓或投石索才能使用速射姿态！`
  - 后：`你需要装备投石索才能使用速射姿态！`
  - 依据：`game/modules/tome/data/talents/techniques/agility.lua:249-305`；后一个 `on_pre_use` 要求 `sling`，`info` 写明 `Requires a sling to use.`。
- `eed96b47b1f76cf0034b56d64e6d69553456debae545d8c45da95f056e662bf0`
  - 前：`在学界最流行的说法是他们强大的魔法毁灭了自己，内战使他们消弭在历史中。`
  - 后：`目前在学界最流行的说法是，他们强大的魔法毁了他们自己：在某场大规模内乱中，这些魔法被用来对付本族人。`
  - 依据：`game/modules/tome/data/lore/misc.lua:483-491`。

本轮验证：

- manifest LuaJIT / `LocaleLoader` 加载基线 `7264886e652b9254ea26afc20bac4e3ed64f1e05` 与工作树：`mod-tome.lua` 21688 条中恰 16 条 target 改变，`tome-orcs.lua` 3904 条中恰 2 条改变；总数恰 18，WORKSET 精确匹配，非 target 字段不变。
- `python3 -B tools/i18n lint --strict`：退出码 5，检查 30308 条，1 error / 0 warnings；唯一错误为预期的 `mod-tome/data/zones/shertul-fortress-caldizar/grids.lua` 同源 farportal `runtime-collision`，报告为 `.artifacts/i18n/runs/20260929T042524.537808Z-1177310-lint/lint.json`。
- `git diff --check`：退出码 0，无输出。
- 本轮未 stage、commit、push、创建 agent 或修改 `.ai/task/`。

## FINAL_REVIEW cycle 2 第 3 轮修复

仅修复 `ADJUDICATION-F2.json` 中唯一一条 `status=confirmed` finding；其他 17 条 target、术语库与文件其他记录不动。主游戏证据仅由 `/workspace/t-engine4` 在固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 上执行 `git show` 取得。

- `eed96b47b1f76cf0034b56d64e6d69553456debae545d8c45da95f056e662bf0`
  1. 前：`事实上，相关的文献很多，但有事实根据的很少，所以有关该种族的信息也较少。`
     后：`事实上，相关的文献很多，但确凿的事实很少，因为人们对这个堪称文明熔炉的古老种族所知甚少。`
  2. 前：`最权威的研究是基于知名探险家和考古学家达沃德·欧卡顿的发现，但遗憾的是，截至本文写就之时，他已失踪好几个月了。`
     后：`这一领域最博学、最求实的学者是知名探险家和考古学家达沃德·欧卡顿，但遗憾的是，截至本文写就之时，他已失踪好几个月了。`
  3. 前：`在马基·埃亚尔大陆上，夏·图尔如梦似幻的废墟结构被找出并探索`
     后：`在马基·埃亚尔各地都发现了夏·图尔奇幻建筑的废墟`
  4. 前：`仍远远超出我们能够理解的范围`
     后：`仍远远超出当代最伟大的头脑所能理解的范围`
  5. 前：`至今无人敢碰`
     后：`至今无人触碰`
  6. 前：`但是对夏·图尔文明的深入研究仍有着非常重要的价值和意义。`
     后：`但对他们所留遗物的持续研究与考察，仍在不断带来巨大的价值与启发。`
- 保留项：前两轮已改的“有的废墟甚至位于近海沉没的陆地上”与“目前在学界最流行的说法是……在某场大规模内乱中……”保持不变；target 仍为 5 段、8 个 LF，TAB 布局不变，无 placeholder 或 markup 变化。
- 依据：`game/modules/tome/data/lore/misc.lua:483-491`。

本轮验证：

- manifest LuaJIT / `LocaleLoader` 加载基线 `7264886e652b9254ea26afc20bac4e3ed64f1e05` 与工作树：`mod-tome.lua` 21688 条中恰 16 条 target 改变，`tome-orcs.lua` 3904 条中恰 2 条改变；总数恰 18，WORKSET 精确匹配，非 target 字段不变。
- `python3 -B tools/i18n lint --strict`：退出码 5，检查 30308 条，1 error / 0 warnings；唯一错误为预期的 `mod-tome/data/zones/shertul-fortress-caldizar/grids.lua` 同源 farportal `runtime-collision`，报告为 `.artifacts/i18n/runs/20260929T044437.461115Z-1212125-lint/lint.json`。
- `git diff --check`：退出码 0，无输出。
- 本轮未 stage、commit、push、创建 agent 或修改 `.ai/task/`。

## RE_REVIEW cycle 1 第 2 轮修复

仅修复 `ADJUDICATION-R1.json` 中唯一一条 `status=confirmed` finding；其他 17 条 target、术语库与文件其他记录不动。主游戏证据仅由 `/workspace/t-engine4` 在固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 上执行 `git show` 取得。

- `fb8138dd842e67a5e73c7b48b847eb00a2dfc20e1e2e8259d3949ca3a05ce2de`
  - 前：`#CRIMSON# 强度 3+：%s 折磨：当敌人试图对你造成负面效果时，你的折磨光环会对 10 范围内的一个随机敌人进行报复，造成 %d 精神和 %d 暗影伤害。`
  - 后：`#CRIMSON# 强度 3+：%s 折磨：当敌人试图对你施加负面效果时，你的折磨光环会反击施加者（若来源不是生物，则改为攻击半径 10 内的一个随机敌人），造成 %d 精神和 %d 暗影伤害。`
  - 依据：`game/modules/tome/data/timed_effects/other.lua:1523-1550`；来源为生物（`p.src.__is_actor`）时直接反击来源者，只有来源不是生物时才在半径 10 内收集并随机选择敌人。
  - 不变量：保留行首 `#CRIMSON#`、`强度 3+：%s `、两个 `%d` 的顺序以及该 target 其他各行的 LF/TAB 结构。

本轮验证：

- manifest LuaJIT / `LocaleLoader` 加载基线 `7264886e652b9254ea26afc20bac4e3ed64f1e05` 与工作树：`mod-tome.lua` 21688 条中恰 16 条 target 改变，`tome-orcs.lua` 3904 条中恰 2 条改变；总数恰 18，WORKSET 精确匹配，非 target 字段不变。
- `python3 -B tools/i18n lint --strict`：退出码 5，检查 30308 条，1 error / 0 warnings；唯一错误为预期的 `mod-tome/data/zones/shertul-fortress-caldizar/grids.lua` 同源 farportal `runtime-collision`，报告为 `.artifacts/i18n/runs/20260929T043258.795838Z-1190452-lint/lint.json`。
- `git diff --check`：退出码 0，无输出。
- 本轮未 stage、commit、push、创建 agent 或修改 `.ai/task/`。
