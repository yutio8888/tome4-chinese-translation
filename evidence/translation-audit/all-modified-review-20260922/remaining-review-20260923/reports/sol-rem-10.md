---

# rem-10 只读交叉核验报告

本批 19 条已逐条核对。C01、C02、C04 为 **confirmed**；C03 为 **advisory**。另发现 N01，列为 advisory。判定依据是冻结文本及下列已核来源，未以 Flash 报告的结论作证据。

### C01 | entry-04116 | confirmed

原译“**被诅咒的影子**”把 *Doomed Shade* 当作普通描述。固定版本的本体源码确有以 `Doomed Shade of %s` 命名的玩家分身；冻结术语将职业 *Doomed* 记为“末日使者”。最强的等价读法是把 *doomed* 泛指“遭厄运的”，但在已有同名实体的语境中，“被诅咒的”会错指。建议译为“末日使者之影”等。此项确认的是**名称译法**；本体实体定义不能证明 Possessors 成就的触发机制。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:5>)；本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/data/zones/shadow-crypt/npcs.lua:86–104`；[术语快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json:36>)。

### C02 | entry-04129 | confirmed

原译“**对附近一个生物进行一次直线冲锋**”遗漏 *and all those in straight line behind it*，后句又以单数“目标”承接原文复数 *targets*。即使“直线冲锋”暗示沿线移动，也没有表达该生物后方的其他生物同样受招。建议补出“及其后方直线上的所有生物”，并用复数指代承接伤害。此为冻结文本可直接证明的漏译；未核实 DLC 的实际运行行为。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:119>)。

### C03 | entry-04137 | advisory

原译“**射出一道冲击波**”保留了向敌人发出力量的读法，但省去 *ghastly finger* 的阴森形象，以及 *tell it to simply die* 的精神命令意象。后续伤害、上限和吸收条件仍有翻译，因此作为叙事忠实度建议保留，不判为机制错译。可改为“以阴森的手指指向……发出一道命其死去的灵能脉冲”。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:266>)。

### C04 | entry-04141 | confirmed

原译“**将自己的痛苦分享给**”给痛苦增添了玩家所有格；原文仅说向符合条件者 *radiate agony*，随后明确说敌人专注于“他们自己的痛苦”。“分享”可以作传递痛苦的修辞等价读法，却不能支持新增的“自己的”，且会改变痛苦归属。建议改为“向……辐射痛苦”。这是文本语义判定，不宣称已核实 DLC 效果实现。[同段上下文与译文](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:342>)。

### N01 | entry-04123 | advisory

原文说伤害被取消后“**against the source**”反击伤害来源；译文写“**对目标进行反击**”。“目标”可被读作造成该次伤害者，故尚不足以确认错指，但脱离战斗语境时指代不清。建议明确为“向伤害来源反击”。[冻结批次原文与译文](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-10.md>)。

## 完整条目映射

| 条目 | 结论 | 依据 |
| --- | --- | --- |
| entry-04116 | 存在问题 | C01 |
| entry-04117 | 未发现问题 | 双向击杀关系完整 |
| entry-04118 | 未发现问题 | 击杀双方及所用身体对应 |
| entry-04122 | 未发现问题 | 条件、层数及占位符对应 |
| entry-04123 | 仅建议 | N01 |
| entry-04124 | 未发现问题 | 储存数量及样式标记对应 |
| entry-04125 | 未发现问题 | `%s` 与名称对应 |
| entry-04129 | 存在问题 | C02 |
| entry-04130 | 未发现问题 | 状态提示语义对应 |
| entry-04131 | 未发现问题 | 叙事与动态标记对应 |
| entry-04132 | 未发现问题 | 阶级提示及占位符对应 |
| entry-04134 | 未发现问题 | 自身属性保留比例对应 |
| entry-04135 | 未发现问题 | 身体属性比例及技能上限对应 |
| entry-04136 | 未发现问题 | 六个等级条目对应 |
| entry-04137 | 仅建议 | C03 |
| entry-04139 | 未发现问题 | 范围、伤害及延时对应 |
| entry-04140 | 未发现问题 | 80% 条件与每层增益对应 |
| entry-04141 | 存在问题 | C04 |
| entry-04143 | 未发现问题 | 原始精神强度数值对应 |

**读取与限制：**实际读取了任务入口、[RULES.md](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md>)、`batches/rem-10.md`、获准读取的 `reports/gemini-rem-10.md`、`snapshots/tome-possessors.lua`、`terms.json`、[source-access.json](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json:824>)，以及上述固定 commit 的本体 `shadow-crypt/npcs.lua`。登记表注明 **Possessors 公开源码未定位**；因此没有核验其成就触发或技能运行机制，也没有据本体源码声称核实 DLC 或目标 1.7.4 版本。未写文件。
