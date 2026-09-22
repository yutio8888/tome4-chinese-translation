本批次为 **batch-074**，复核文件哈希已核验一致（SHA-256：`c6db30cd08aae813d95df055275fe6ae9d9aab5a644f65d3fae0da339e364550`）。
本批 40 条译文（entry-02349 至 entry-02388）均位于基础游戏 `mod-tome` 模块；源码核验统一基于 fixed commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

逐条复核报告如下：

---

### entry-02349
- **状态**：未发现问题
- **可核验依据**：源码见 [`duelist.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/duelist.lua) 的 `Tempo` 技能。占位符 `%0.1f`、`%d%%`、`%0.1f` 数量与顺序一致；机制上防御端触发回体与能量、副手暴击回体描述准确。（细微观察：此处 parry 译为“抵挡”，与同树前置技能 `Dual Weapon Mastery` 的“抵挡”一致，但后续条目译为“招架”）。

### entry-02350
- **状态**：未发现问题
- **可核验依据**：源码见 [`duelist.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/duelist.lua) 的 `Feint` 技能。战斗日志占位符 `#Source#` 与 `#Target#` 完整保留，换位阻挡判定语义准确。

### entry-02351
- **状态**：未发现问题
- **可核验依据**：源码见 [`duelist.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/duelist.lua) 的 `Feint` 技能。占位符 `%d`、`%d%%` 数量与类型一致；定身（pin）、眩晕（daze）、换位及招架增益描述与代码机制完全相符。

### entry-02352
- **状态**：细微观察
- **可核验依据**：源码见 [`duelist.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/duelist.lua) 的 `Lunge` 技能 `action` 分支。原文明确写出具体技能名称 `You cannot use Lunge without dual wielding!`，译文泛化译为“你需要双持武器来施展这个技能！”，虽不影响使用提示，但省略了技能具体名称“刺击”。

### entry-02353
- **状态**：未发现问题
- **可核验依据**：源码见 [`duelist.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/duelist.lua) 的 `Lunge` 技能。占位符 `%d%%`、`%d` 顺序与类型一致；译文第二段添加的补充说明“（近战或射击落空、或被招架）”经核验 `Actor.lua` 与 `physical.lua` 中 `do_tempo` 的触发点完全属实，准确阐明了防御触发机制。

### entry-02354
- **状态**：存在疑点
- **可核验依据**：源码见 [`excellence.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/excellence.lua) 的 `Shoot Down` 技能。原文“if you spot a projectile (arrow, shot, spell, ...)”意为“发现/察觉抛射物”，译文误译为“当你**瞄准**抛射物”；对比同类技能 entry-02386 准确译为“如果你发现一个抛射物”。动词词义产生偏差。第二段占位符 `%d` 正常。

### entry-02355
- **状态**：未发现问题
- **可核验依据**：源码见 [`excellence.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/excellence.lua) 的 `Bull Shot` 技能。占位符 `%d%%` 与 `%d` 顺序与类型一致；冲锋接近后射击并击退的机制叙述准确。

### entry-02356
- **状态**：存在疑点
- **可核验依据**：源码见 [`excellence.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/excellence.lua) 的 `Intuitive Shots` 技能。原文分为两段，第二段 `\n\t\tActivating this talent will not interrupt reloading.` 前有明确换行缩进；译文丢失了该换行符，将第二段内容连在第一段末尾。占位符 `%d%%`、`%d%%`、`%d` 数量与顺序无误。

### entry-02357
- **状态**：未发现问题
- **可核验依据**：源码见 [`excellence.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/excellence.lua) 的 `Strangling Shot` 技能。占位符 `%d%%` 与 `%d` 顺序与类型一致；沉默（silence）状态及命中判定说明准确。

### entry-02358
- **状态**：未发现问题
- **可核验依据**：源码见 [`finishing-moves.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/finishing-moves.lua) 的 `Haymaker` 技能。占位符 `@Source@` 完整保留，终结技施放文本表达自然。

### entry-02359
- **状态**：未发现问题
- **可核验依据**：源码见 [`grappling.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/grappling.lua) 的 `Clinch` 技能。5 个占位符 `%d%%`、`%d`、`%d`、`%d%%`、`%d` 顺序与类型完全对应；抓取体型限制、持续时间、每回合物理伤害、伤害转移比例及体力维持消耗均准确对应。

### entry-02360
- **状态**：细微观察
- **可核验依据**：源码见 [`grappling.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/grappling.lua) 的 `Crushing Hold` 技能。占位符 `%d` 与 `%d%%` 数量正确；但等级 5 原文为 `Reduces global action speed by %d%%`，底层修改 `global_speed_add`，术语规范为“全局速度”，译文意译为“目标减速 %d%%”；此外 `#RED#` 后带有一个空格。

### entry-02361
- **状态**：未发现问题
- **可核验依据**：源码见 [`grappling.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/grappling.lua) 的 `Take Down` 技能。行动受限时的玩家日志提示，文本简洁准确。

### entry-02362
- **状态**：未发现问题
- **可核验依据**：源码见 [`grappling.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/grappling.lua) 的 `Take Down` 技能。占位符 `%d%%` 与 `%d` 顺序正确；扑倒攻击与砸地冲击波伤害机制及解除抓取条件说明准确。

### entry-02363
- **状态**：未发现问题
- **可核验依据**：源码见 [`magical-combat.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua)。技能名称 `Arcane Combat` 译为“奥术格斗”，符合标准技能译名。

### entry-02364
- **状态**：未发现问题
- **可核验依据**：源码见 [`magical-combat.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua) 的 `Arcane Combat` 技能 `info`。占位符 `%s` 完整保留，换行格式匹配。

### entry-02365
- **状态**：未发现问题
- **可核验依据**：源码见 [`magical-combat.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua) 的 `Arcane Combat` 技能 `info`。随机法术状态文本翻译准确，空行缩进匹配。

### entry-02366
- **状态**：未发现问题
- **可核验依据**：源码见 [`magical-combat.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua) 的 `Arcane Cunning` 技能。占位符 `%d%%` 与 `%d` 正确对应灵巧百分比加成与当前法术强度增益数值。

### entry-02367
- **状态**：未发现问题
- **可核验依据**：源码见 [`magical-combat.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua) 的 `Arcane Destruction` 技能。占位符 `%d%%`、`%d`、`%d`、`%0.2f` 及字面转义 `50%%`、`50%%` 顺序与类型完全一致，奥术伤害机制表述无误。

### entry-02368
- **状态**：未发现问题
- **可核验依据**：源码见 [`marksmanship.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/marksmanship.lua) 的 `Flare` 技能。4 个占位符 `%d` 依序对应致盲时间、照亮半径、持续时间与闪避/潜行扣减，隐匿（concealment）机制描述准确。

### entry-02369
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `mobility_pre_use` 函数。占位符 `%s` 正确保留，移动受限不可用提示准确。

### entry-02370
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `mobility_pre_use` 函数。占位符 `%s` 正确保留，重甲穿戴限制提示准确。

### entry-02371
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `Evasion` 技能。占位符 `%d%%`、`%d`、`%d` 依序对应躲闪几率、防御（闪避）加成和持续回合，属性缩放说明一致。

### entry-02372
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `Tumble` 技能 `action` 分支。目标格受阻时的提示信息，语义表达准确。

### entry-02373
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `Tumble` 技能。占位符 `%d%%` 与 `%d` 正确对应疲劳增加的体力消耗比例和持续时间，重甲限制说明无误。

### entry-02374
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `Trained Reactions` 技能。颜色代码 `#FIREBRICK#`、`#LAST#` 及占位符 `#Target#`、`%s`、`#Source#` 完整，战斗日志结构合规。

### entry-02375
- **状态**：未发现问题
- **可核验依据**：源码见 [`mobility.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/mobility.lua) 的 `Trained Reactions` 技能。参数顺序经核验代码为 `(trigger, stam, reduce)`，译文中 `%d%%`、`%0.1f`、`%d%%` 严格匹配，减伤与体力触发机制无误。

### entry-02376
- **状态**：未发现问题
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Exotic Munitions` 技能。7 个占位符 `%d%%`、`%d`、`%0.2f`、`%0.2f`、`%d%%`、`%d`、`%d%%` 顺序与类型完全对应，三种弹药特性概览完整。

### entry-02377
- **状态**：未发现问题
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Incendiary Ammunition` 技能。占位符 `%d%%` 与 `%d` 匹配，燃烧弹范围伤害与每回合单次触发限制说明准确。

### entry-02378
- **状态**：未发现问题
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Venomous Ammunition` 技能。占位符 `%0.2f`、`%0.2f`、`%d%%` 顺序匹配，即时与持续自然伤害及削弱伤害比例表述准确。

### entry-02379
- **状态**：未发现问题
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Piercing Ammunition` 技能。占位符 `%d` 与 `%d%%` 匹配，护甲/豁免扣减及物理穿透加成说明无误。

### entry-02380
- **状态**：细微观察
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Explosive Shot` 技能。全部 13 个占位符（包含百分号与浮点数）顺序与类型完全一致；但原文首行末尾带有冒号 `:`（`...loaded ammo:`），译文首行末尾漏译冒号。

### entry-02381
- **状态**：存在疑点
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Enhanced Munitions` 技能。第 3 行原文为 `dealing %0.2f nature damage over 3 turns`，代码结算为 `DamageType.NATURE`，译文误写为“造成 %0.2f **毒素伤害**”；ToME 机制中只有自然伤害类型（同文件其他条目均规范译为自然伤害），伤害类型术语不准确。占位符 `%0.2f`、`%0.2f`、`100%%`、`%d%%` 顺序一致。

### entry-02382
- **状态**：未发现问题
- **可核验依据**：源码见 [`munitions.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/munitions.lua) 的 `Alloyed Munitions` 技能。7 个占位符 `%d`、`%d%%`、`%d%%`、`%d`、`%0.2f`、`%0.2f`、`%d%%` 顺序与类型完全吻合，复合弹药加成机制叙述完整。（行末带西文句号为细微排版痕迹，不影响机制）。

### entry-02383
- **状态**：未发现问题
- **可核验依据**：源码见 [`pugilism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/pugilism.lua) 的 `Striking Stance` 技能。占位符 `%d`、`%d%%`、`%d` 正确对应命中、拳术与终结技伤害加成、以及全伤害固定减免数值。

### entry-02384
- **状态**：未发现问题
- **可核验依据**：源码见 [`pugilism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/pugilism.lua) 的 `Double Strike` 技能。占位符 `%d%%` 匹配，自动替代平碰攻击及 4 级产生 2 点连击点机制叙述准确。

### entry-02385
- **状态**：未发现问题
- **可核验依据**：源码见 [`pugilism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/pugilism.lua) 的 `Flurry of Fists` 技能。占位符 `%d%%` 匹配，快速三拳与 4 级命中按次产生连击点机制说明无误。

### entry-02386
- **状态**：未发现问题
- **可核验依据**：源码见 [`reflexes.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/reflexes.lua) 的 `Shoot Down` 技能。占位符 `%d` 与 `%d%%` 匹配，被动减速敌方抛射物与主动拦截机制描述准确。

### entry-02387
- **状态**：未发现问题
- **可核验依据**：源码见 [`reflexes.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/reflexes.lua) 的 `Intuitive Shots` 技能。占位符 `%d%%` 与 `%d%%` 匹配，受近战攻击时概率防御射击、闪避并反击造成弓箭伤害的机制叙述准确。

### entry-02388
- **状态**：未发现问题
- **可核验依据**：源码见 [`reflexes.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/reflexes.lua) 的 `Sentinel` 技能。占位符 `25%%`、`%d`、`%d` 顺序与类型完全对应，瞬间瞬发必中打断施法并使目标其他技能进入冷却的机制描述准确。

---

### 疑点与观察汇总
1. **存在疑点**：
   - **entry-02354**（`excellence.lua: Shoot Down`）：原文“if you spot a projectile”中的 spot 误译为“瞄准”，应为“发现/察觉”；
   - **entry-02356**（`excellence.lua: Intuitive Shots`）：缺失换行符，第二段关于装填弹药不中断的说明连在第一段末尾；
   - **entry-02381**（`munitions.lua: Enhanced Munitions`）：原文“%0.2f nature damage”误译为“%0.2f 毒素伤害”，伤害类型术语不规范（代码为 DamageType.NATURE）。
2. **细微观察**：
   - **entry-02352**（`duelist.lua: Lunge`）：日志省略具体技能名“Lunge”，泛化为“这个技能”；
   - **entry-02360**（`grappling.lua: Crushing Hold`）：机制属性 `global action speed` 意译为“减速”，偏离规范“全局速度”；
   - **entry-02380**（`munitions.lua: Explosive Shot`）：首行行末英文冒号在译文中漏译。