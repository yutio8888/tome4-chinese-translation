---

# rem-14 只读交叉审核报告

已核对入口的 **20 个条目、21 项疑点**。下文的 `S`、`O` 等是文末列出的冻结文件路径；行号均指这些文件。对 7 份用到的 DLC 源码文件逐一计算 SHA256，结果均与 `source-access.json` 登记值一致。

| 条目 | 结论 | 疑点 |
|---|---|---|
| entry-03965 | 未发现问题 | 占位符、抵抗事件相符 |
| entry-03966 | 未发现问题 | 伤害、半径、震慑和占位符相符 |
| entry-03967 | 存在问题 | C01、C02、C03 |
| entry-03968 | 未发现问题 | 击退事件相符 |
| entry-03969 | 未发现问题 | 抵抗拉动事件相符；`%s` 后空格属排版差异 |
| entry-03970 | 存在问题 | C04、C05；C06 仅建议 |
| entry-03971 | 存在问题 | C07、C08、C09；C10 仅建议 |
| entry-03972 | 存在问题 | C11、C12、C13 |
| entry-03973 | 存在问题 | C14、C15、C16；C17 仅建议 |
| entry-03974 | 未发现问题 | 参数、蒸汽储备和样式标记相符 |
| entry-03975 | 未发现问题 | 容量增加相符 |
| entry-03977 | 存在问题 | C19.2；C18、C19.1 仅建议 |
| entry-03978 | 未发现问题 | 类别说明相符 |
| entry-03979 | 未发现问题 | 类别说明相符 |
| entry-03980 | 未发现问题 | 颜色标记与含义相符 |
| entry-03981 | 未发现问题 | 配方、占位符与颜色标记相符 |
| entry-03983 | 未发现问题 | 斜体标记与含义相符 |
| entry-03984 | 仅建议 | C20 |
| entry-03985 | 未发现问题 | C21 已反证 |
| entry-03986 | 未发现问题 | 实体描述相符 |

### C01 | entry-03967 | confirmed

原译“每一个弹片”将 `each shot` 变成爆炸后的碎片；源码实际先取得蒸汽枪射击目标并执行 `archeryShoot`，每次射击命中后才触发爆炸。将“弹片”宽泛理解为弹丸仍不符合此处先射击、后爆炸的顺序。证据：`S:5552–5555`、`O:1327–1343`。

### C02 | entry-03967 | confirmed

“这个技能不使用弹药”保留了结果，遗漏 `as it is the ammo` 所说的“技能本身就是弹药”。结果相同不足以覆盖原句的因果及设定。证据：`S:5552–5555`、`O:1341–1343`。

### C03 | entry-03967 | confirmed

“在射程内制造一场特殊的爆炸”可概括最终效果，但遗漏向射程内一处地点**发射爆炸弹**的动作和落点；源码也明确执行射击。这是叙事动作与目标的具体信息缺失。证据：`S:5552–5555`、`O:1332–1343`。

### C04 | entry-03970 | confirmed

两处“被拉向……%d 码”均漏掉 `up to`，读起来承诺移动足额距离；原文只给最大格数。拉动调用使用该数值作为距离参数，不能据此保证实际总能移动满额。证据：`S:5594–5601`、`O:1583–1599,1603–1606`。

### C05 | entry-03970 | confirmed

原译“这个技能不使用弹药”遗漏“技能本身就是弹药”的因果分句；与 C02 同类。证据：`S:5594–5601`、`O:1603–1606`。

### C06 | entry-03970 | advisory

“特殊弹药打击目标或某处”没有写出 `hook shot` 的钩弹特征；“打击”也可能暗示造成伤害，而所见技能动作是拉动。最强等价读法是“打击”仅表示朝目标发射，后文已解释拉动，因此记为澄清建议。证据：`S:5594–5601`、`O:1581–1606`。

### C07 | entry-03971 | confirmed

“闪电球”把 `bolt` 具体化为球体；本技能对附近敌人的续发效果采用 `beam` 投射及闪电粒子。即使把“球”作宽泛的闪电称呼，也会给出错误的形状印象。证据：`S:5610–5616`、`O:1670–1677,1690–1694`。

### C08 | entry-03971 | confirmed

“打击周围 %d 的敌人”漏掉 `up to`，并缺少人数的量词。源码按技能等级设循环上限，附近敌人用尽会提前退出；译为“附近至多 %d 名敌人”才保留限制。证据：`S:5610–5616`、`O:1670–1675,1691–1695`。

### C09 | entry-03971 | confirmed

“这个技能不使用弹药”遗漏 `as it is the ammo`；同 C02。证据：`S:5610–5616`、`O:1690–1694`。

### C10 | entry-03971 | advisory

“特殊弹药”未呈现 `voltaic`，但紧接着已说明闪电武器伤害及电流效果，玩家仍能识别弹药性质。补出“电气／伏特”可使首句更完整。证据：`S:5610–5616`、`O:1690–1694`。

### C11 | entry-03972 | confirmed

“苔藓”遗漏 `Nourishing Moss` 的 `Nourishing`，使具名效果变成泛称；源码使用 `DamageType.NOURISHING_MOSS`。后文的吸血说明不能补回效果名称。证据：`S:5628–5635`、`O:1750–1755,1771–1776`。

### C12 | entry-03972 | confirmed

“这个技能不使用弹药”遗漏“技能本身就是弹药”的因果分句；同 C02。证据：`S:5628–5635`、`O:1771–1776`。

### C13 | entry-03972 | confirmed

“造成 %0.2f 自然伤害对半径内的每一个敌人”是明显不通顺的语序，应写成“对……造成……伤害”。同项所提 `botanical` 被泛化为“特殊弹药”也值得补出，但其植物性质可从孢子、苔藓读出；确认的问题是句法，修饰语遗漏作为建议。证据：`S:5628–5635`、`O:1771–1773`。

### C14 | entry-03973 | confirmed

“整体速度”与本轮 `global speed → 全局速度` 的 global、`tformat`、preferred 术语记录直接冲突，记录还明确排除“整体速度”。证据：`S:5649–5653`、`T:960–968`、`O:1846–1847`。

### C15 | entry-03973 | confirmed

“枯萎伤害受蒸汽强度加成”将 `Toxin strength` 限缩为伤害。命中时，同一个随蒸汽强度变化的 `getPower` 同时传给毒素的 `power` 和减速的 `speed`；“伤害”不能说明后一效果也成长。证据：`S:5649–5653`、`O:1829–1832,1846–1850`。

### C16 | entry-03973 | confirmed

“这个技能不使用弹药”遗漏 `as it is the ammo`；同 C02。证据：`S:5649–5653`、`O:1846–1849`。

### C17 | entry-03973 | advisory

“特殊弹药”未写 `toxic`，但下一句已交代向目标释放重金属并施加毒素相关效果；性质仍可从上下文辨认。首句补“剧毒”更完整。证据：`S:5649–5653`、`O:1846–1849`。

### C18 | entry-03977 | advisory

原译“伤害受蒸汽强度加成”可能概括流血伤害增幅与喷血伤害，不能直接断言玩家只会理解为后者；写明两项更清楚。初审报告称 `getDamageInc` 是实际流血增幅函数，但冻结源码的效果执行处调用的是 `getDamage`，`getDamageInc` 只出现在说明的格式化参数中。因此其“两项独立函数分别驱动两种实际效果”的论证**不成立**；源码与英文说明之间的这一差异应另行记录，不能算中文新增错误。证据：`S:5742–5750`、`M:64–66,79–86,92–98`。

### C19 | entry-03977 | advisory（C19.1）／confirmed（C19.2）

原译“将链锯放在目标的伤口上”弱化 `slam ... into` 的猛烈动作；结合引号中的“轻柔”，建议改写以保留反讽，但主要动作仍可理解，故 **C19.1 advisory**。原译“4 码锥形范围”则遗漏 `narrow`；源码将锥角设为 25，狭窄是实际范围特征，故 **C19.2 confirmed**。证据：`S:5742–5749`、`M:85–86,93–96`。

### C20 | entry-03984 | advisory

“进入其大脑”传达侵入与干扰结果，却省去 `latch on it` 的附着动作及 `bore into its skull` 的钻入头骨画面。补足可改善叙事；核心效果仍可理解。英文 `-%d%% reduction` 的双重负号不可机械照译：效果代码确实降低恐惧、睡眠免疫，现译这一点正确。证据：`S:5853–5857`、`I:103–107`、`E:77–90`。

### C21 | entry-03985 | refuted

原译感叹号与英文相符；静态标点差异按本轮规则不算缺陷。初审所引 preferred 记录的 `source_tag` 为 `logSeen`，本条冻结输入为 `logPlayer`，也不能把该记录当作本条必须逐字匹配的依据。证据：`S:5890`、`T:993–1001`、`R:6`。

## 完整疑点映射

| 状态 | 编号 |
|---|---|
| confirmed | C01、C02、C03、C04、C05、C07、C08、C09、C11、C12、C13、C14、C15、C16、C19.2 |
| advisory | C06、C10、C17、C18、C19.1、C20 |
| refuted | C21 |
| pending | 无 |

**新疑点：**无中文译文新增疑点。`M:64–66,79–83,98` 显示 C18 所涉英文说明／源码参数使用不一致，已在 C18 单列为源码观察，未计作译文错误。

## 读取路径与版本限制

- `R`：[审核规则](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md)；`S`：[冻结译文快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua)；`T`：[冻结术语](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json)。
- `O`：[other.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua)；`M`：[sawmaiming.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/sawmaiming.lua)；`I`：[thoughts-of-iron.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua)；`E`：[mental.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua)。

另读取了指定入口、当前批次、允许读取的 `gemini-rem-14.md`、`source-access.json`，以及登记的 `physics.lua`、`steam.lua`、`turrets.lua`；未读取其他报告或任务状态，未写文件或创建代理。`source-access.json:377,561–578` 将本批 orcs 源码标为 **unpinned**，仅以文件 SHA256 冻结：上述判断适用于这些哈希匹配的公开源码快照，**不能据此宣称已核对 DLC 的 1.7.4 发布源码或某一 upstream commit**。
