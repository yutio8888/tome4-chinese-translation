### C01 | entry-03875 | confirmed

原译“让现实……将他们连根拔起”把 *lift them up* 译成了拔除。最强等价读法是：既然前文说“将钩子扎入现实”，这里的“拔起”也许指拔起钩子；但英文宾语 *them* 指维西一族，并与“现实被他们拖入深渊”构成托起或同坠的选择。建议改为“让现实要么托起他们，要么与他们一道坠入深渊”。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3579)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua:107)。

### C02 | entry-03883 | advisory

原译“召唤雪人来协助你”省去 *trained*。最强等价读法成立：同 section 的任务说明已交代野雪人会受训，使用动作又译作“召唤受训练的雪人来帮助你”，玩家仍可理解召来的对象。道具说明单独出现时补上“受训”会更明确；建议润色，不列确认错译。证据：[同 section 原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3887)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua:45)。

### C03 | entry-03890 | advisory

原译“持续能量仍然算向最大值”生硬，容易让“持续能量”被读作持续恢复的能量。最强等价读法是：读者结合技能语境，仍可把“持续”理解为维持技能占用的能量；源码注释也明确谈及 *sustains* 对可用上限的影响。因此保留表达澄清建议，改作“维持技能占用的能量仍计入上限”，不据此断定数值机制译错。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3965)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/energies.lua:32)。

### C04 | entry-03892 | confirmed

原译“在目标所在地创造一个地块”把 *distortion* 丢失，并把地点 *at the target tile* 误作创造对象。最强等价读法是“地块”仅指效果位置；但“创造一个地块”的句法明确说创造地块，邻近技能另有真正造墙的描述，不能替它补出“扭曲”。建议译为“在目标地块制造一处扭曲，击退投射物，并尽可能使其转向外侧”。证据：[同 section 原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3977)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/reflection.lua:135)。

### 新增观察

**N01 | entry-03875 | advisory**：“宇宙也忘不了我们”省去了 *no matter how it may have wanted to* 所含的“即便宇宙想忘记”意味。同篇已交代宇宙敌视维西一族，读者可由上下文补足，故建议润色为“即便宇宙想忘记，也无法忘记我们”，不另列确认错译。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3583)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua:107)。

| Flash 疑点 | 本次判定 |
| --- | --- |
| C01 → entry-03875 | confirmed |
| C02 → entry-03883 | advisory |
| C03 → entry-03890 | advisory |
| C04 → entry-03892 | confirmed |

读取范围为指定的 `sol-rem-11.md` 入口、同目录 `RULES.md`、`rem-11.md`、Flash 报告、`source-access.json`、`terms.json`、涉及的 `snapshots/tome-orcs.lua` 片段及上引四份公开源码；未读其他报告。四份源码的 SHA256 均与 [来源登记](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json:376)相符。`orcs` 源码仅固定快照哈希，仓库 commit 与目标版本未固定；以上源码行为判断只适用于该快照，不宣称已核实目标发行版本。
