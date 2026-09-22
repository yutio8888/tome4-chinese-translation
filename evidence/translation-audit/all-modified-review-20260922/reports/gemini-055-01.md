### batch-055 译文复核报告

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-055.md`
- **文件哈希校验**：`adde84acbdaa87951b9820acb1802aeefc2cd26fb667962908214024dd7cb442`（核验一致）
- **固定公开源码**：commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均归属于 `game/modules/tome/` 路径）
- **译文终点基准**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`
- **条目范围**：`entry-01585` 至 `entry-01624`，共 40 条，逐条复核如下。

---

#### entry-01585
- **位置**：`mod-tome.lua:22091`（`mod-tome/data/talents/chronomancy/induced-phenomena.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Polarity Shift` 的 `info` 函数传入 `damDesc(self, DamageType.TEMPORAL, damage)`, `duration`, `braid`。占位符 `%0.2f`、`%d`、`%d%%` 的类型、数量及语序完全匹配；机制名 `Cosmic Cycle` 依术语快照准确译为「宇宙圈」，`Spellpower` 译为「法术强度」，生命线编织与伤害分摊机制描述准确。

#### entry-01586
- **位置**：`mod-tome.lua:22102`（`mod-tome/data/talents/chronomancy/induced-phenomena.lua`）
- **判定**：存在疑点
- **核验依据**：术语快照明确记录：`Epoch -> 亚伯契`（`T.PN.PERSON`，附注：“时空位面具名实体专名；同名天赋及神器 Epoch's Curve 均沿用音译，不按普通名词‘纪元’处理”）。在固定 commit 的 `zh_hans.lua` 中亦固定为 `t("Epoch", "亚伯契", "talent name")`（同名 NPC `Epoch` 掉落神器 `Epoch's Curve` / `亚伯契的弧线`）。当前译文译为「纪元」，与专名音译及术语规范冲突。

#### entry-01587
- **位置**：`mod-tome.lua:22116`（`mod-tome/data/talents/chronomancy/matter.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Dust to Dust` 的 `info` 函数格式化参数为时空伤害 `%0.2f`、物理伤害 `%0.2f` 和自身范围 `%d`。占位符顺序与类型一致；扭曲伤害类型（DamageType.WARP 拆分为时空与物理各半）标注正确，`Spellpower` 准确对应「法术强度」。

#### entry-01588
- **位置**：`mod-tome.lua:22122`（`mod-tome/data/talents/chronomancy/matter.lua`）
- **判定**：细微观察
- **核验依据**：
  1. 原文首句“Weave matter into your flesh, becoming incredibly resilient to damage.”意译为“你的血肉被改变，对伤害的抗性提高”，省略了“编织物质”（Weave matter）与技能名称 `Matter Weaving` 的具象动作呼应。
  2. 末句“scale with your Magic”译为“受魔力值加成”（术语表基础属性名为“魔力”）。
  3. 底层代码 `activate` 挂载 `stun_immune`、`cut_immune` 与 `combat_armor`，译文中的「%d 护甲，%d%% 震慑免疫，%d%% 流血免疫」与底层机制属性完全吻合，占位符 `%d`、`%d%%`、`%d%%` 无误。

#### entry-01589
- **位置**：`mod-tome.lua:22128`（`mod-tome/data/talents/chronomancy/matter.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Materialize Barrier` 的 `info` 函数传入 `length`, `duration`, `radius`, `damDesc(..., damage)`。占位符 `%d`（长度）、`%d`（回合）、`%d`（半径）、`%0.2f`（物理伤害）顺序与数值类型完全吻合；挖掘触发流血伤害机制叙述准确。

#### entry-01590
- **位置**：`mod-tome.lua:22170`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Spacetime Mastery` 的 `info` 传入常规时空技能冷却减免 `%d`、虫洞冷却减免 `%d` 以及法术强度/克服失稳概率加成 `%d%%`。对应天赋名称（放逐、空间跳跃、时空交换、时空尾迹、虫洞穿梭）及机制术语（连续体失稳、法术强度）均规范准确，占位符匹配。

#### entry-01591
- **位置**：`mod-tome.lua:22183`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Gather the Threads` 的 `info` 函数格式化参数为首回合加成 `%0.2f`、每回合递增 `%0.2f` 及紊乱值降低 `%d`。占位符类型与顺序一致；英文原文拼写错误“Eacn turn”在译文中被正确理解为“每回合”，`Paradox` 对应「紊乱值」，`Spacetime Tuning` 对应「时空调谐」。

#### entry-01592
- **位置**：`mod-tome.lua:22195`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Fade From Time` 的 `info` 传入全抗 `%d%%` 与负面效果缩减 `%d%%`，字面值 `20%%` 正确保留；法术衰减与法术强度加成描述准确。

#### entry-01593
- **位置**：`mod-tome.lua:22203`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Paradox Clone` 在查找落点失败时调用 `game.logPlayer(self, "Not enough space to summon!")`。译文保留感叹号，语义准确。

#### entry-01594
- **位置**：`mod-tome.lua:22205`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码克隆体描述 `m.desc = ([[The real %s... or so %s says.]]):tformat(self:getName(), self:he_she())`。两处 `%s` 顺序一致，省略号转化为全角省略号，语义完整。

#### entry-01595
- **位置**：`mod-tome.lua:22211`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Displace Damage` 调用 `game:delayedLogMessage(..., "#PINK##Source# displaces some damage onto #Target#!")`。颜色标记 `#PINK#`、实体标记 `#Source#` 和 `#Target#` 及末尾叹号均完整无损。

#### entry-01596
- **位置**：`mod-tome.lua:22216`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Repulsion Field` 的 `info` 传入半径 `%d`、物理伤害 `%0.2f`、持续时间 `%d`。字面量 `50%%` 保留，定身（pinned）、击退（knockback）、法术强度（Spellpower）术语均符合规范。

#### entry-01597
- **位置**：`mod-tome.lua:22230`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Damage Smearing` 传入转化百分比 `%d%%` 与分摊回合 `%d`。后句“bypass resistance and affinity”在战斗伤害机制中指无视抗性与伤害亲和（吸收治疗），译文处理符合战斗机制上下文。

#### entry-01598
- **位置**：`mod-tome.lua:22236`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码传送失败时日志 `The spell fizzles!`，标准战斗日志译为「法术失败了！」，无占位符，准确无误。

#### entry-01599
- **位置**：`mod-tome.lua:22238`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Swap` 的 `info` 格式化参数为施法距离 `%d`、混乱强度 `%d%%`、混乱持续时间 `%d`。占位符顺序一致；法术命中率与法术强度加成关系说明准确。

#### entry-01600
- **位置**：`mod-tome.lua:22242`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Temporal Wake` 视线检查失败日志 `You do not have line of sight.`，标准提示译为「你没有视线。」，准确无误。

#### entry-01601
- **位置**：`mod-tome.lua:22255`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：天赋名称 `Destabilize` 对应造成 `EFF_TEMPORAL_DESTABILIZATION` 状态，译文「时空失稳」与同系技能互引一致。

#### entry-01602
- **位置**：`mod-tome.lua:22256`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Destabilize` 的 `info` 传入周期时空伤害 `%0.2f`、爆炸时空伤害 `%0.2f`、爆炸物理伤害 `%0.2f`。三处 `%0.2f` 顺序与类型完全对应；死亡触发与连续体失稳判定叙述准确。

#### entry-01603
- **位置**：`mod-tome.lua:22264`（`mod-tome/data/talents/chronomancy/other.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Quantum Spike` 的 `info` 传入时空伤害 `%0.2f` 与物理伤害 `%0.2f`。字面量 `<20%%` 与 `50%%` 转义正确；受时空失稳/连续体失稳增伤机制表述准确。

#### entry-01604
- **位置**：`mod-tome.lua:22278`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `makeWarpMine` / `Spatial Tether` 传送被免疫时触发 `game.logSeen(who, "%s resists the teleport!", ...)`。占位符 `%s` 及惊叹号无误。

#### entry-01605
- **位置**：`mod-tome.lua:22286`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：存在疑点
- **核验依据**：
  1. 原文为“inflict %0.2f physical and %0.2f temporal (warp) damage.”，译文为“造成 %0.2f 物理和 %0.2f 时空伤害。”，遗漏了 `(warp)` 即「（扭曲）」的伤害类型说明。对比同文件 `entry-01606`（“造成 %0.2f 物理和 %0.2f 时空（扭曲）伤害”）与 `entry-01610`（“受到 %0.2f 物理和 %0.2f 时空（扭曲）伤害”），此处存在明显漏译。
  2. 末句“The damage caused by your Warp Mines will improve with your Spellpower.”被简略为“伤害受法术强度加成”，省略了主语“时空地雷的”。

#### entry-01606
- **位置**：`mod-tome.lua:22292`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Warp Mines` 的 `info` 依次传入物理伤害 `%0.2f`、时空伤害 `%0.2f`、侦查强度 `%d`、拆除强度 `%d`、持续时间 `%d`、时空折叠范围 `%d`。6 个占位符类型与顺序完全匹配；技能说明完整准确。

#### entry-01607
- **位置**：`mod-tome.lua:22311`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Banish` 施法落点失败日志 `The spell fizzles on %s!`。占位符 `%s` 匹配，语义准确。

#### entry-01608
- **位置**：`mod-tome.lua:22312`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码放逐成功战斗日志 `#CRIMSON#%s has been banished!`。颜色标签 `#CRIMSON#` 与占位符 `%s` 完好，语义准确。

#### entry-01609
- **位置**：`mod-tome.lua:22314`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Banish` 的 `info` 传入传送最小距离 `%d`、最大距离 `%d` 及随机负面持续回合 `%d`。占位符一致；震慑、致盲、混乱、定身四种负面状态翻译规范。

#### entry-01610
- **位置**：`mod-tome.lua:22319`（`mod-tome/data/talents/chronomancy/spacetime-folding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Dimensional Anchor` 的 `info` 传入力场持续时间 `%d`、物理伤害 `%0.2f`、时空伤害 `%0.2f`。英文“daze all enemies”依术语快照准确译为「眩晕」（与 stun 震慑明确区分），锚定传送触发扭曲伤害说明完整。

#### entry-01611
- **位置**：`mod-tome.lua:22329`（`mod-tome/data/talents/chronomancy/spacetime-weaving.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Dimensional Step` 视线检查失败日志 `You do not have line of sight.`。标准提示译为「你没有视线。」，准确无误。

#### entry-01612
- **位置**：`mod-tome.lua:22330`（`mod-tome/data/talents/chronomancy/spacetime-weaving.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `self:logCombat(target, "#Source# folds space with with #target#!")`。实体占位标签 `#Source#` 与 `#target#` 大小写完全保留，英文原文双写“with with”语病在译文中自然修正。

#### entry-01613
- **位置**：`mod-tome.lua:22332`（`mod-tome/data/talents/chronomancy/spacetime-weaving.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `target:logCombat(self, "#Source# resists #target#'s space-time folding!")`。实体标签 `#Source#`（抵抗者）与 `#target#`（施法者）位置匹配，抵抗战斗日志准确。

#### entry-01614
- **位置**：`mod-tome.lua:22350`（`mod-tome/data/talents/chronomancy/spacetime-weaving.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Wormhole` 的 `info` 传入距离 `%d`、精度半径 `%d`、持续时间 `%d`。3 个 `%d` 占位符顺序与数值类型匹配；虫洞放置距离与法术强度加成机制叙述完整。

#### entry-01615
- **位置**：`mod-tome.lua:22372`（`mod-tome/data/talents/chronomancy/speed-control.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Time Stop` 激活日志 `#STEEL_BLUE#%s has stopped time!#LAST#`。颜色标记 `#STEEL_BLUE#` 与闭合标记 `#LAST#`、占位符 `%s` 均完整匹配。

#### entry-01616
- **位置**：`mod-tome.lua:22380`（`mod-tome/data/talents/chronomancy/spellbinding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Empower` 的 `info` 传入法术强度增幅 `%d%%` 与当前绑定技能名 `%s`。占位符类型与数量匹配；单一时空绑定排他性说明准确。

#### entry-01617
- **位置**：`mod-tome.lua:22388`（`mod-tome/data/talents/chronomancy/spellbinding.lua`）
- **判定**：细微观察
- **核验依据**：
  1. 占位符 `%d%%` 与 `%s` 匹配无误。
  2. 原文第二行“Each spell can only be spellbound in one way at a time.”在同系其他 3 个技能（entry-01616、01618、01619）中均统一译为“每个法术同时只能附加一种时空绑定效果”，本条目译为“每个法术同时只能通过一种方式获得时空增效”，存在同系内部表述不一致。

#### entry-01618
- **位置**：`mod-tome.lua:22396`（`mod-tome/data/talents/chronomancy/spellbinding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Matrix` 的 `info` 传入冷却时间减免 `%d%%` 与当前绑定技能名 `%s`。占位符与机制说明准确无误。

#### entry-01619
- **位置**：`mod-tome.lua:22404`（`mod-tome/data/talents/chronomancy/spellbinding.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Quicken` 底层通过 `Actor:getTalentSpeed` 减少技能消耗的能量系数（`speed - getPower`），使施法消耗时间缩短。英文原文虽字面为“Reduces the casting speed”，译文处理为「减少指定时空系法术 %d%% 的施法时间」精准体现了游戏机制实际效用；占位符 `%d%%` 与 `%s` 准确。

#### entry-01620
- **位置**：`mod-tome.lua:22442`（`mod-tome/data/talents/chronomancy/temporal-archery.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Phase Shot` 的 `info` 传入武器伤害百分比 `%d%%`。破甲（APR 1000）与时空武器伤害机制描述准确，占位符一致。

#### entry-01621
- **位置**：`mod-tome.lua:22446`（`mod-tome/data/talents/chronomancy/temporal-archery.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Perfect Aim` 的 `info` 传入暴击伤害倍率 `%d%%` 与物理/法术暴击几率 `%d%%`。两个 `%d%%` 占位符顺序无误，法术强度加成表述正确。

#### entry-01622
- **位置**：`mod-tome.lua:22470`（`mod-tome/data/talents/chronomancy/temporal-combat.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Fold Gravity` 的 `info` 原始传参顺序为 `chance` (%d), `damDesc(..., damage)` (%0.2f), `radius` (%d), `slow` (%d), `duration` (%d)。本条目声明了重排规则 `args_order: [1, 3, 2, 4, 5]`，译文中依次为几率 `%d%%`、半径 `%d`、重力伤害 `%0.2f`、全局速度降低 `%d%%`、持续时间 `%d` 回合，与重排参数严格吻合；术语「全局速度」符合规范。

#### entry-01623
- **位置**：`mod-tome.lua:22486`（`mod-tome/data/talents/chronomancy/temporal-combat.lua`）
- **判定**：未发现问题
- **核验依据**：源码 `Weapon Manifold` 的 `info` 传入 13 个参数。本条目声明了复杂重排规则 `args_order: [1, 3, 2, 4, 5, 8, 6, 7, 9, 11, 10, 12, 13]`。逐项核对译文占位符：
  - 触发几率：%d%%（对应原参 1）；
  - 命运折叠：半径 %d（原参 3）、时空伤害 %0.2f（原参 2）、抗性降低 %d%%（原参 4）、持续 %d 回合（原参 5）；
  - 扭曲折叠：半径 %d（原参 8）、物理伤害 %0.2f（原参 6）、时空伤害 %0.2f（原参 7）、持续 %d 回合（原参 9）；
  - 重力折叠：半径 %d（原参 11）、物理伤害 %0.2f（原参 10）、减速 %d%%（原参 12）、持续 %d 回合（原参 13）。
  全部 13 个占位符类型与语序在映射后完美对应，状态（震慑、致盲、混乱、定身）翻译完备。

#### entry-01624
- **位置**：`mod-tome.lua:22509`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **判定**：未发现问题
- **核验依据**：源码时空猎犬 NPC 描述 `desc=_t[[A trained hound that appears to be all at once a little puppy and a toothless old dog.]]`。风味文本表达贴切，无占位符，翻译准确。

---

### 复核疑点与观察汇总

1. **存在疑点**：
   - **entry-01586**（`Epoch`）：译为「纪元」，违背了术语快照中关于具名实体与同名天赋音译为「亚伯契」的明确规定，且与固定版本源码中的 `zh_hans.lua` 译名冲突。
   - **entry-01605**（`Warp Mine Away`）：技能描述中遗漏了 `(warp)` 即「（扭曲）」伤害类型标注（对比同文件 01606 与 01610）；且末句省略了主语「时空地雷的」。
2. **细微观察**：
   - **entry-01588**（`Matter Weaving`）：首句将“Weave matter into your flesh...”意译为“你的血肉被改变...”，略去了技能核心意象“编织物质”；后句“Magic”作“魔力值”。
   - **entry-01617**（`Extension`）：第二句排他性说明“spellbound”译为“获得时空增效”，与同系其余三条统一使用的“附加一种时空绑定效果”存在措辞微差。