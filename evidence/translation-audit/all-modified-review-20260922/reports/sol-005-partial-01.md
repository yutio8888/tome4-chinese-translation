已核对冻结说明，SHA-256 与指定值一致。源码依据均为固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/class/Actor.lua`。

### entry-00164

1. **颜色码及占位符顺序正确：confirmed**

   证据：源码第 838 行调用为：

   `game.log("#VIOLET#Following build order %s; increasing %s by 1.", b.name, self.stats_def[stat].name)`

   第一个 `%s` 是加点方案名 `b.name`，第二个是属性名；译文保留 `#VIOLET#` 和两个 `%s` 的次序。相关冻结译文见 [batch-005.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/batches/batch-005.md:47)。

   影响：未发现颜色码、格式化参数或运行时风险。

   人工待决点：无。

2. **中文句中使用了无空格的半角分号：confirmed**

   证据：冻结译文确为 `顺序%s;增加`。

   影响：只是中西文标点混用，可能影响排版一致性；不影响语义和运行。

   人工待决点：是否把中文日志中的半角分号统一视为需要修正的格式问题。

3. **建议改为全角分号或逗号：advisory**

   证据：中文两分句使用 `；` 或 `，` 通常更自然，但现有冻结输入没有给出强制标点规范。

   影响：属于润色和排版统一，不足以认定为确定缺陷。

   人工待决点：若决定修改，需在 `；` 和 `，` 之间选择；两者均不改变机制含义。

### entry-00165

1. **颜色码及占位符顺序正确：confirmed**

   证据：源码第 860 行为：

   `game.log("#VIOLET#Following build order %s; learning talent category %s.", b.name, tt)`

   两个 `%s` 分别对应方案名和 talent type 标识 `tt`，译文顺序一致。冻结译文见 [batch-005.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/batches/batch-005.md:59)。

   影响：未发现格式化或运行时风险。

   人工待决点：无。

2. **把 `talent category` 译为“技能树”可以接受：pending**

   证据：源码第 845–867 行表明这里处理的是 `b.types` 中的 talent type：尚未掌握时调用 `learnTalentType(tt)`，已经掌握时则把该类别的 mastery 增加 `0.2`。这能证明它是技能类别／技能树层级，但受限输入中没有术语规范，无法确认“技能树”是否为本项目的正式统一译法。

   影响：若既有术语采用“技能类别”等其他译法，会产生术语一致性问题；机制大意仍可理解。另外，“学会”对提高既有类别熟练度的分支略显绝对，不过英文原文本身也统一写作 `learning`。

   人工待决点：需结合本项目已授权的术语依据决定保留“技能树”，还是采用“技能类别”等译法。

3. **中文句中使用了无空格的半角分号：confirmed**

   证据：冻结译文确为 `顺序%s;学会`。

   影响：仅为排版一致性问题，不影响格式化和机制含义。

   人工待决点：是否纳入中文标点统一。

4. **建议换成全角中文标点：advisory**

   没有证据表明当前半角分号违反强制规则，因此只能作为润色建议，不能升级为确定错误。

### entry-00166

1. **颜色码及占位符顺序正确：confirmed**

   证据：源码第 880、901 行均为：

   `game.log("#VIOLET#Following build order %s; learning talent %s.", b.name, t.name)`

   两个调用分别处理职业技能点和通用技能点；参数均为方案名 `b.name`、技能名 `t.name`。译文保留颜色码和占位符顺序。冻结译文见 [batch-005.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/batches/batch-005.md:71)。

   影响：未发现占位符或运行时风险。

   人工待决点：无。

2. **中文句中使用了无空格的半角分号：confirmed**

   证据：冻结译文确为 `顺序%s;学会`。

   影响：中西文标点混用，最多构成轻微排版问题，不影响语义或功能。

   人工待决点：是否统一成全角标点。

3. **建议换成全角分号或逗号：advisory**

   该建议符合通常的中文排版习惯，但冻结证据没有规定必须如此，故不应认定为硬性缺陷。

综合结论：Gemini 对三条译文“使用无空格半角分号”的事实判断均得到确认；把它们提升为需要修复的问题则只能算 **advisory**。唯一证据不足的实质判断是 entry-00165 中“`talent category` 译为‘技能树’可接受”，应保留为 **pending**，等待术语依据裁决。