## rem-12 只读交叉核验报告

已核验入口指定的 20 条译文及 C01–C08 全部疑点。结论为：**C01、C04、C05、C07、C08 confirmed；C02、C03、C06 advisory**。另发现 N01、N02 两项。以下结论依据冻结译文与源码独立判定；未修改文件。

### C01 | entry-03912 | confirmed

原译「造成 %0.2f 物理伤害并沉默敌人，持续 4 回合」漏掉伤害频率。最强等价读法是将“持续 4 回合”同时理解为伤害和沉默的持续时间，但它仍不能说明 **%0.2f 是每回合伤害**。源码的效果每回合施加 `eff.power` 物理伤害。建议补出“每回合造成”。证据：`snapshots/tome-orcs.lua:4559-4563`；冻结源码 `tome-orcs/data/talents/steam/automated-butchery.lua:66-93`、`tome-orcs/data/timed_effects/physical.lua:445-464`。

### C02 | entry-03913 | advisory

原译「直接恢复 %d%% 蒸汽值」省略了英文的“最大值的”。通常可将“恢复百分比蒸汽值”理解为按上限计算，故不足以判为确定错译；明确写成“恢复最大蒸汽值的 %d%%”更清楚。源码按 `getMaxSteam() * eff.regen` 增加蒸汽。证据：`snapshots/tome-orcs.lua:4573-4577`；冻结源码 `tome-orcs/data/talents/steam/automated-butchery.lua:169-179`、`tome-orcs/data/timed_effects/physical.lua:402-413`。

### C03 | entry-03918 | advisory

原译「无尽地痛苦」中的“地”用字不当，也把原文“The pain shall never stop!”的陈述句改成了短语。最强等价读法是将它视作表达“痛苦无尽”的风味短句；核心意思尚可辨认。建议改为“痛苦永不停歇！”证据：`snapshots/tome-orcs.lua:4796-4798`；冻结源码 `tome-orcs/data/talents/steam/butchery.lua:127-130`。

### C04 | entry-03921 | confirmed

原译「被猎杀的危险令你激动不已」把 *the thrill of the hunt* 的狩猎者视角改成被猎杀者视角。周围敌人带来速度加成，可以解释角色为何兴奋，但不能证明原文采用了“被猎杀”的叙事。建议改为“狩猎的快感令你振奋”。证据：`snapshots/tome-orcs.lua:4929-4933`；冻结源码 `tome-orcs/data/talents/steam/elusiveness.lua:67-99`。

### C05 | entry-03925 | confirmed

原译「你的护甲温度极高，能驱散部分能量攻击」漏掉“**熔炉开启时**”这一生效条件。最强等价读法是借相邻的“熔炉”技能说明推知条件，但本条被动说明单独阅读会显得常驻；源码也先检查熔炉是否激活。建议补明条件。证据：`snapshots/tome-orcs.lua:4984-4995`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:56-67,88-97`。

### C06 | entry-03926 | advisory

原译「只是肉体在燃烧！」保留了“只是”的轻描淡写语气，但把 *a flesh burn* 表成整个肉体正在燃烧，失去局部烫伤的笑点。它是风味句，不改变技能机制；建议改为“区区皮肉烫伤罢了！”证据：`snapshots/tome-orcs.lua:5007-5017`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:170-177`。

### C07 | entry-03931 | confirmed

原译「你能移动到相邻的一格」漏掉“被定身或无法移动时除外”；「取决于扫射期间你消耗的弹药」则把**扫射次数**误作**消耗弹药数**。即使把“在移动中射击”视为一般技能概述，这两处仍会误导具体判定。源码的装填公式使用 `turns` 与弹药容量，移动分支另检查移动限制。原文“双持蒸汽枪”在相邻的使用前提示中已明确，建议在本说明补出，但不单列为确定缺陷。证据：`snapshots/tome-orcs.lua:5086-5095`；冻结源码 `tome-orcs/data/talents/steam/gunslinging.lua:28-40,53-89`。

### C08 | entry-03933 | confirmed

原译「子弹命中后将弹射至其他目标」未说明击中**实体或坚固墙壁**均可跳弹，也未说明**未命中即中断**。这些不是“最多弹射 %d 次”能够涵盖的条件；源码分别处理撞墙与未命中。原译「灵敏」可宽泛涵盖灵巧、敏捷，但原文明确列出两项属性，建议补全。另须谨慎：源码先按距**首个目标**的距离排序候选者，不能仅凭英文“next closest foe”宣称它每次都重新寻找距当前撞击点最近的敌人。证据：`snapshots/tome-orcs.lua:5111-5118`；冻结源码 `tome-orcs/data/talents/steam/gunslinging.lua:177-183,192-241,246-254`。

## 新发现

### N01 | entry-03924 | confirmed

原译「成为大师意味着你经历了更多危险，你的计算力也超越凡人」改变了原文“技艺大师有时须冒险，而**你的风险比别人算得更周全**”。“经历了更多危险”和“计算力超越凡人”均非原文所述。后续属性数值译法无此问题。证据：`batches/rem-12.md` 的 `entry-03924`；冻结源码 `tome-orcs/data/talents/steam/engineering.lua:127-130`。

### N02 | entry-03926 | confirmed

原译「%d 个负面物理状态被高温驱散」漏掉 *up to*，把“**最多 %d 个**”写成固定移除 `%d` 个。源码将该数值作为 `removeEffectsFilter` 的移除上限。证据：`snapshots/tome-orcs.lua:5007-5012`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:157-161,170-177`。

## 完整条目映射

| entry-ID | 结果 | 依据／疑点 |
|---|---|---|
| entry-03906 | 未发现问题 | 抗性、豁免及占位符对应 |
| entry-03910 | 未发现问题 | 战斗日志主体、目标标记对应 |
| entry-03912 | 存在问题 | C01：漏掉每回合伤害 |
| entry-03913 | 仅建议 | C02：明确最大蒸汽值比例 |
| entry-03914 | 未发现问题 | 日志参数对应 |
| entry-03916 | 未发现问题 | 属性与数值对应 |
| entry-03918 | 仅建议 | C03：风味句用字、句式 |
| entry-03919 | 未发现问题 | 扇形范围与伤害参数按 `args_order=[2,1,3,4]` 对应 |
| entry-03921 | 存在问题 | C04：狩猎视角反转 |
| entry-03922 | 未发现问题 | 击退、范围减速及后退对应 |
| entry-03924 | 存在问题 | N01：冒险叙事改义 |
| entry-03925 | 存在问题 | C05：漏掉熔炉开启条件 |
| entry-03926 | 存在问题；另有建议 | N02：漏掉移除数量上限；C06：风味句 |
| entry-03927 | 未发现问题 | 装弹、加成及友方穿透对应 |
| entry-03930 | 未发现问题 | 武器伤害、物理强度和装填参数对应 |
| entry-03931 | 存在问题 | C07：移动限制及装填依据 |
| entry-03933 | 存在问题 | C08：跳弹载体与未命中中断条件 |
| entry-03934 | 未发现问题 | 火焰伤害范围、持续时间、必中与无视护甲对应 |
| entry-03937 | 未发现问题 | 抵抗缴械日志对应 |
| entry-03938 | 未发现问题 | 抵抗震慑日志对应 |

## 读取范围与版本限制

读取了指定入口、同目录 `RULES.md`、当前 `batches/rem-12.md`、`reports/gemini-rem-12.md`、`source-access.json`、`terms.json`，以及 `snapshots/tome-orcs.lua` 的相关同 section 上下文；源码只读取 `source-access.json` 登记的本批相关 `orcs` 冻结文件。所涉及的 15 个冻结源码文件均与登记的 SHA-256 相符。未读取其他报告或任务状态。

`orcs` DLC 在 `source-access.json` 中标为 **unpinned**：上述源码证据只适用于这些经哈希核验的冻结文件；其仓库 commit 和目标发行版本未固定，**不能据此声称已核验 1.7.4**。
