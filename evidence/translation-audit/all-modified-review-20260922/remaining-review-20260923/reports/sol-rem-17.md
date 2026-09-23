---

# rem-17 独立 Sol 交叉核验报告

本次按只读 REVIEWER 范围核查了全部 20 条冻结译文及 Flash 报告的 C01–C07。**Flash 报告中“已有 Sol 复审”的说法不成立**；下列判定是本次独立核验结果，未把该自述当作其他模型结论。未修改文件或创建代理。

| 顺序 | Entry-ID | 本次判定 | 依据 |
|---:|---|---|---|
| 1 | entry-04034 | 未发现问题 | 状态解除与“不再烧焦”对应 |
| 2 | entry-04035 | 存在问题 | C01 |
| 3 | entry-04037 | 未发现问题 | 标记状态准确 |
| 4 | entry-04038 | 未发现问题 | 发痒状态准确 |
| 5 | entry-04040 | 未发现问题 | 烟雾中隐藏准确 |
| 6 | entry-04041 | 未发现问题 | 隐藏状态解除准确 |
| 7 | entry-04043 | 未发现问题 | “磁化”对应此处状态；术语“磁力”限技能类别 |
| 8 | entry-04044 | 未发现问题 | 血液灵晶状态获得准确 |
| 9 | entry-04045 | 未发现问题 | 血液灵晶状态解除准确 |
| 10 | entry-04046 | 仅建议 | C02 |
| 11 | entry-04047 | 仅建议 | C03 |
| 12 | entry-04048 | 未发现问题 | `%s` 与颜色标记完整 |
| 13 | entry-04049 | 仅建议 | C04 |
| 14 | entry-04050 | 未发现问题 | AED 准备日志准确 |
| 15 | entry-04051 | 未发现问题 | AED 触发日志准确 |
| 16 | entry-04052 | 未发现问题 | 钳制动作及主客体准确 |
| 17 | entry-04053 | 仅建议 | C05 |
| 18 | entry-04054 | 仅建议 | 新发现 N01 |
| 19 | entry-04055 | 仅建议 | C06 |
| 20 | entry-04056 | 仅建议 | C07；记录英文与机制的差异，不判中文错译 |

### C01 | entry-04035 | confirmed

原译“`#Target# 接住了蒸汽枪。`”保留了接住武器这一主干，但省去 *somehow* 的意外感和 *falling* 的下落动作。前一句明确写将蒸汽枪抛向空中；战斗日志虽可简写，仍不足以传达原句的戏谑场面。建议“`#Target# 不知怎么接住了落下的蒸汽枪。`”。证据：[译文快照第 6444–6445 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6444)、[源码第 602–603 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:602)。

### C02 | entry-04046 | advisory

原译“`忍受痛苦，不能集中精力制造伤害`”能表达受苦导致伤害下降。“忍受”略带主动耐受意味，“制造伤害”也较生硬；“遭受痛苦，无法集中精力造成伤害”更自然。相邻解除句“痛苦减轻了”支持这一语感建议，但不足以判定原译错义。证据：[快照第 6499–6501 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6499)、[源码第 875–886 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:875)。

### C03 | entry-04047 | advisory

原译“`被闪电之网覆盖`”没有写出 *crackling* 的声响；“覆盖”也比 *surrounded by* 更偏表面附着。不过闪电之网及全伤害固定减免均已传达，“覆盖”可作护盾意象理解。可润色为“被噼啪作响的闪电之网环绕”。证据：[快照第 6514–6515 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6514)、[源码第 956–977 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:956)。

### C04 | entry-04049 | advisory

原译“`#target#力量强化！`”概括了力量增强，却弱化 *surges with power* 的涌动感。它与解除句“力量消退了”相配，状态提示仍成立；“力量涌动！”是可选润色。证据：[快照第 6525–6527 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6525)、[源码第 1033–1042 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1033)。

### C05 | entry-04053 | advisory

原译“`打击`”省去了 *strikes down at* 的动作力度，但保留了攻击者、目标和颜色标记。源码证明这是钳制期间的尾部武器自动攻击；它未证明攻击必然具有固定的空间方向，因此 Flash 建议的“向下猛击”不宜作为机制事实强制采用。“猛击”可作润色。证据：[快照第 6552–6557 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6552)、[源码第 1312–1323 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1312)。

### C06 | entry-04055 | advisory

原译增写“`每回合第一次被带有武器类型的近战或远程攻击命中时`”。源码在 `callbackOnHit` 中检查攻击来源的 `weapon_type`，并以目标的 `turn_procs.miasma` 阻止再次触发，支持武器条件和单回合一次的说明。它比英文及相邻光环说明详细，但没有据此确认中文新增机制错误。Flash 所称“100% 吻合”过于绝对：本次核验能直接确认上述回调条件，未把所有攻击类型的消费路径逐一穷尽。证据：[快照第 6568、6572 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6568)、[源码第 1465–1499 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1465)。

### C07 | entry-04056 | advisory

原译“`可手动使用火箭弹幕再次发射，使用其他任何技能会立即结束该效果`”与英文“每回合发射”明显不同。冻结源码显示效果赋予 `Rocket Barrage` 技能，使用其他技能后移除效果；技能说明也写明可主动再次发射。故中文是有源码依据的机制澄清，本项只备案英文表述差异，不计中文错译。证据：[快照第 6573–6574 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6573)、[效果源码第 1502–1535 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1502)、[技能源码第 175–182、187–218 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/artillery.lua:175)。

### N01 | entry-04054 | advisory

原译“`被困在其中的敌人`”比英文 *Enemies within* 多出受困意味。源码显示毒云向范围内目标施加瘴气效果，所核对的效果定义没有定身条件；但“被困在毒云中”也可能只是叙事说法，尚不足以确认玩家会理解为无法离开。建议改为“处于其中的敌人”。证据：[快照第 6568 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6568)、[源码第 1405–1409、1438–1444 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1405)。

**来源与版本限制：**实际读取了指定入口、同目录 `RULES.md`、`batches/rem-17.md`、Flash 的 `reports/gemini-rem-17.md`、`source-access.json`、`terms.json`、本批同 section 的 `snapshots/tome-orcs.lua` 上下文，以及登记的 `physical.lua`、`artillery.lua` 冻结源码。两份源码的本地 SHA256 均与[来源登记](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json:376)相符；`orcs` DLC 的仓库 commit 和目标 1.7.4 版本**未固定**。机制结论只适用于这些哈希固定的公开源码快照，不宣称已核验 1.7.4 发行态。未读取其他报告或任务状态。
