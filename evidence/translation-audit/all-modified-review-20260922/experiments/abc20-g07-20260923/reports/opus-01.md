# 冻结 40 条复核报告：entry-03413 至 entry-03452（translation_contextual_v1，自然语言实验旁路）

本报告只是审核观察，不是真值，也不代表生产 DONE_VERIFIED。DLC 源码快照来自 source-access.json，快照哈希已逐文件核对，全部一致；源码仓库和 commit 均未固定。下文源码路径的前缀为 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/`。

| 完整 entry-ID | 判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03413 | 存在问题 | C01、C02（C03 上游误述、C04 建议） |
| entry-03414 | 未发现问题 | 与原文一致；术语行对应 logSeen 标签，本条为 logPlayer，只差句末标点 |
| entry-03415 | 未发现问题 | 与原文一致 |
| entry-03416 | 存在问题 | C05、C06（C07 上游误述） |
| entry-03417 | 未发现问题 | 数值与参数一一对应 |
| entry-03418 | 未发现问题 | 「近战反击」与 on_melee_hit 一致 |
| entry-03419 | 存在问题 | C08 |
| entry-03420 | 仅建议 | C09 |
| entry-03421 | 未发现问题 | 「10 + %d%%」与 armor=10+v*scale 等价 |
| entry-03422 | 未发现问题 | C10（只有上游误述） |
| entry-03423 | 未发现问题 | 与原文一致 |
| entry-03424 | 未发现问题 | C11（偏离英文，但与源码一致） |
| entry-03425 | 未发现问题 | 与机制一致 |
| entry-03426 | 未发现问题 | 「锥形」符合 target type=cone |
| entry-03427 | 未发现问题 | 与 REBIRTH_BY_FIRE 一致 |
| entry-03428 | 未发现问题 | 与原文一致 |
| entry-03429 | 仅建议 | C12 |
| entry-03430 | 存在问题 | C13 |
| entry-03431 | 存在问题 | C14、C15（C16 上游误述） |
| entry-03432 | 未发现问题 | 与 npcs.lua:42 一致 |
| entry-03433 | 存在问题 | C17 |
| entry-03434 | 未发现问题 | 与 FIERY_TORMENT 一致 |
| entry-03435 | 未发现问题 | 与 wrath.lua:80 条件一致 |
| entry-03436 | 仅建议 | C18 |
| entry-03437 | 存在问题 | C19、C20（C21 建议） |
| entry-03438 | 未发现问题 | val/2 暗影球与原文、译文一致 |
| entry-03439 | 未发现问题 | 与原文一致 |
| entry-03440 | 存在问题 | C22 |
| entry-03441 | 仅建议 | C23 |
| entry-03442 | 未发现问题 | 与原文一致 |
| entry-03443 | 未发现问题 | 与邻近「灵魂燃烧」译法一致 |
| entry-03444 | 未发现问题 | 与 DEMON_SEED 的 callbackOnDeath 一致 |
| entry-03445 | 仅建议 | C24 |
| entry-03446 | 未发现问题 | 占位符与标记完整 |
| entry-03447 | 未发现问题 | 显示值为负数；「不低于 %d 时不会死亡」逻辑正确 |
| entry-03448 | 仅建议 | C25 |
| entry-03449 | 未发现问题 | 与 FIRE_HAVEN 一致 |
| entry-03450 | 未发现问题 | 与原文一致 |
| entry-03451 | 未发现问题 | 术语库该行为 existing「伤害吸收」，不构成改名依据；「伤害亲和」对应 damage_affinity |
| entry-03452 | 未发现问题 | 与原文一致 |

**统计：** 存在问题 8 条，仅建议 6 条，待确认 0 条，未发现问题 26 条。

## 各 claim 明细

### C01 | entry-03413 | 存在问题
- **原文与译文：** 原文「Implanting a seed into unique demons … grant a seed of that type」，译文为「成功将种子植入史诗生物（Unique）的体内…必定会获得该恶魔种子」。
- **问题：** 原文的作用对象是 demons（恶魔），译文丢掉了这个限定，范围扩大成任何史诗生物。
- **源码依据：** `talents/corruptions/demonic-pact.lua:364`（createSeed）。只有 `host.type == "demon"` 时，种子类型才取宿主名；非恶魔宿主一律从 `seeds[lvl]` 随机抽取。因此，非恶魔的史诗宿主不会给出同类种子。

### C02 | entry-03413 | 存在问题
- **原文与译文：** 原文「it will instead increase its level if the host was of higher level … and the demon inside will regenerate … and resurrect」，译文为「如果…已有同类种子，且宿主等级高于恶魔的等级，它会提升种子的等级。此外，里面的恶魔会恢复…复活」。
- **问题：** 译文把「宿主等级更高」提成整句的前提，回复与复活于是也像要满足这个等级条件才会发生。另外，「instead」（不再生成新种子）这层信息丢失了。
- **源码依据：** `demonic-pact.lua:536` 在找到同类种子时就调用 updateSeed。其中 `:440` 取 `hlevel = math.max(hlevel, demon.level)`，`:451` 清除死亡状态，`:467` 执行治疗，三者都不依赖等级条件。

### C03 | entry-03413 | 上游误述（不计为译文缺陷）
- **内容：** 原文称恶魔「regenerate %d%% health」，源码 `:467` 实际是 `demon:heal(t:_getHeal(self))`，getHeal 为 10–30 点固定值，不是百分比。
- **结论：** 译文照搬原文，问题来自上游。

### C04 | entry-03413 | 仅建议
- **内容：** 「眩晕 敌人」中间多了一个空格。
- **为何只是建议：** 属于排版问题，不影响参数和信息。

### C05 | entry-03416 | 存在问题
- **原文与译文：** 原文「within a small range of up to %d grids」，译文为「传到 %d 码外的一个位置」。
- **问题：** 「up to」（最多）是距离上限，译文读起来像固定距离。
- **源码依据：** `demonic-pact.lua:862-875`。目标的 range 为 getRange，属于上限；随后在所选点周围 radius 范围内 teleportRandom。

### C06 | entry-03416 | 存在问题
- **原文与译文：** 原文「summon a random demon from your seeds」，译文为「随机召唤一个恶魔」。
- **问题：** 「from your seeds」丢失，召唤来源的限定没了，读者会以为召唤的是任意随机恶魔。
- **源码依据：** `demonic-pact.lua:879` 为 `rng.table(list).demon`，list 来自已穿戴的种子（availableDemonSeed）。

### C07 | entry-03416 | 上游误述（不计为译文缺陷）
- **内容：** 原文「fizzle」被译为「失败」。
- **源码依据：** `demonic-pact.lua:867-871` 显示，不在视线内时有 35%（外加地图属性修正）的几率改为以自身为中心、按全射程随机传送，并不是施法失败。
- **结论：** 误述来自英文原文。

### C08 | entry-03419 | 存在问题
- **原文与译文：** 原文「This effect stacks multiplicatively up to %d times」，译文为「能叠加至最多 %d 层」。
- **问题：** 译文漏掉「乘算叠加」，玩家会按每层 8% 线性累加去理解。
- **源码依据：** `timed_effects.lua:805/817`（DARK_REIGN）的计算是 `p = 1 - 0.92^stacks`。

### C09 | entry-03420 | 仅建议
- **内容：** 本条用「黑暗伤害」，同组 03419、03438 用「暗影伤害」（术语库 darkness 为 existing「暗影」）。另外，「黑暗支配开启」对一个被动天赋的效果来说稍显别扭。
- **为何只是建议：** 语义没有错，只是用词一致性问题。

### C10 | entry-03422 | 上游误述（不计为译文缺陷）
- **内容：** 原文和译文都写「5 回合」，源码 `doom-shield.lua:185` 设置 CURSE_IMPOTENCE 的持续时间为 10。
- **结论：** 译文忠实于原文，误述来自上游。

### C11 | entry-03424 | 未发现问题（偏离英文，但与源码一致）
- **内容：** 原文写「next 3 turns」，译文写「4 回合」。
- **源码依据：** `fearfire.lua:75` 为 `setEffect(EFF_SENSE, 4, …)`。引擎 `ActorTemporaryEffects.lua` 的 timedEffects（第 78–109 行）先检查 `dur<=0` 再递减，所以实际约持续 4 回合。
- **结论：** 译文与实现一致，不算缺陷。

### C12 | entry-03429 | 仅建议
- **内容：** 选择目标的提示用「受害者」，技能描述 03430 和效果描述用「牺牲生物」，同一流程里称呼不一致。
- **为何只是建议：** 不导致错误信息。

### C13 | entry-03430 | 存在问题
- **原文与译文：** 原文「the victim takes %d%% of the damage」，译文为「%d%% 伤害由牺牲生物承受」。
- **问题：** 「由…承受」暗示这部分伤害从源生物转嫁出去，源生物因此少受伤害。
- **源码依据：** `timed_effects.lua:715-722`（LINK_OF_PAIN 的 callbackOnHit）没有修改 cb.value，只是另外对 victim 执行 `takeHit(cb.value*power/100)`。源生物仍承受全额伤害。

### C14 | entry-03431 | 存在问题
- **原文与译文：** 原文「bleed … for 50%% of the damage done as darkness over 5 turns」，译文为「合计受到额外 50%% 黑暗伤害」。
- **问题：** 百分比的基数「of the damage done」（本次命中的伤害）丢失，「额外 50%」可以读成其他基数的加成。
- **源码依据：** `infernal-combat.lua:168`，`dam = dam * 0.5 / 5`，每回合一跳。

### C15 | entry-03431 | 存在问题
- **原文与译文：** 原文「Any time you damage this foe in melee」，译文为「每次你攻击…目标时」。
- **问题：** 「近战」这个条件丢失，远程攻击和法术看起来也能触发回复。
- **源码依据：** `timed_effects.lua:683`，DEMONIC_CUT 只挂在 callbackOnMeleeHit 上，并要求 `dam > 0` 且 `src == eff.src`。

### C16 | entry-03431 | 上游误述（不计为译文缺陷）
- **内容：** 原文和译文都有「每回合至多 1 次」，但 `timed_effects.lua:683-686` 没有 turn_procs 之类的限制。
- **结论：** 误述来自上游。

### C17 | entry-03433 | 存在问题
- **原文与译文：** 原文「Your successful melee hits」，译文为「你的攻击」。
- **问题：** 「命中」和「近战」两个触发条件都丢了。
- **源码依据：** `oppression.lua:72-75`，callbackOnMeleeAttack，且 `if not hitted then return end`。

### C18 | entry-03436 | 仅建议
- **内容：** 「乌鲁洛克之口：角度增加 %d」缺少单位「度」；原文为「by %d degrees」，数值为 `dest*10`，作用于 `fearfire.lua:186` 的 cone_angle。
- **为何只是建议：** 上下文能看出是角度。

### C19 | entry-03437 | 存在问题
- **原文与译文：** 原文「teleporting you to a specific location up to %d spaces away」，译文为「传送半径 %d」。
- **问题：** 「指定的精确落点」这层信息丢失，「传送半径」容易让人理解成在半径内随机落点。
- **源码依据：** `talents/misc/races.lua:68`，`teleportRandom(x, y, 0)`，落点半径为 0，是精确传送。

### C20 | entry-03437 | 存在问题（术语）
- **原文与译文：** 原文「out of phase」，译文为「脱离空间」「停留在相位外」。
- **问题：** 这里描述的是 EFF_OUT_OF_PHASE 状态（`races.lua:73`）。引擎固定 commit 下，`game/modules/tome/data/timed_effects/magical.lua:2583` 的状态名为「Out of Phase」。术语库 preferred 为「脱离现实」，备注写明「统一沿用效果定义」。译文没有沿用这个名字，玩家难以把描述和状态栏里的效果对上。

### C21 | entry-03437 | 仅建议
- **内容：** 「全体抗性」与术语库 preferred「全部抗性」不同。
- **为何只是建议：** 该术语行针对面板标签（_t），语义也不受影响。

### C22 | entry-03440 | 存在问题
- **原文与译文：** 原文「#Target#'s weapon looks less threatening.」，译文为「#Target#的危险度看起来降低了」。
- **问题：** 所属关系错了：原文说的是目标的武器，译文变成了目标本身。
- **源码依据：** `timed_effects.lua` 中 DEMON_BLADE 的 on_lose（约第 52 行），对应武器附魔结束。

### C23 | entry-03441 | 仅建议
- **内容：** 「blazing」被译为「闪耀」，失去了「燃烧」的意味。这条文本由 Revel 与 Devoured 共用（`timed_effects.lua:157/178`）。
- **为何只是建议：** 它与邻近的「武器闪耀着火花」成对出现，并伴随「-Revel」「-Devoured」提示，机制信息没有丢失。

### C24 | entry-03445 | 仅建议
- **内容：** 「获得%d%% 酸性抗性与 %d%%酸性伤害亲和」前后空格不对称。
- **为何只是建议：** 纯排版问题。

### C25 | entry-03448 | 仅建议
- **内容：** 「charges」被译为「叠加次数」，与邻近的「%d charges.」→「%d层充能」译法不一致。
- **为何只是建议：** 源码显示的就是 eff.stacks（`timed_effects.lua:861`），语义没有错。

## 实际读取的路径与越界情况

**冻结输入（仅读）：** INPUT.md、entries.json、context.lua、source-access.json。

**本组 sources 文件（13 个，哈希已核对）：** 路径前缀为 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/`：
- talents/corruptions/ 下的 demonic-pact、demonic-strength、doom-covenant、doom-shield、fearfire、heart-of-fire、infernal-combat、npcs、oppression、torture、wrath（均为 .lua）
- talents/misc/races.lua
- timed_effects.lua

这些都是 DLC 快照，源码仓库和 commit 未固定，结论对目标版本是否适用仍需确认。

**引擎文件（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63，用 `git show` 各读单个文件）：**
- `game/engines/default/engine/interface/ActorTemporaryEffects.lua`：从 `fearfire.lua:75` 的 `self:setEffect(EFF_SENSE, 4)` 追到 timedEffects，用于判断实际持续回合。
- `game/modules/tome/data/timed_effects/magical.lua`：从 `races.lua:73` 的 `EFF_OUT_OF_PHASE` 追过去，只查看该效果的定义。

**其他情况：**
- 没有读取 dlc_additional_sources 中的额外文件。
- 没有读取 SPEC、STATE 或其他实验文件、报告、当前翻译文件或 locales。
- 没有整目录搜索，没有越界，也没有无法核验的组件。
- 临时目录 `/tmp/abc20-g07-20260923-S3A4tF` 创建后没有写入任何文件，已删除。
- 仓库保持只读；`git status` 与开始时相同。
