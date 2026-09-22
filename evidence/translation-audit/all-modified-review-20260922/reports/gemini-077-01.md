### 复核前验证

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-077.md`
- **SHA-256 校验**：`11ae1c4a879d4729d7e92765a582b9bead326b252448efa986884df64e16a080`（核对一致）
- **条目范围**：`entry-02470` 至 `entry-02509`（共 40 条）
- **公开源码基准**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`t-engine4`）

---

### 逐条复核报告

#### entry-02470
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:320`（Elemental Surge 寒冷爆发日志）。原文 `%s surges with #1133F3#icy#LAST# power!`，译文 `%s涌起#1133F3#冰霜#LAST#能量的狂潮！`。占位符 `%s` 与颜色标签 `#1133F3#...#LAST#` 均完整保留，语境含义准确。

#### entry-02471
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:325`（Elemental Surge 闪电爆发日志）。原文 `%s surges with #ROYAL_BLUE#lightning#LAST# power!`，译文 `%s涌起#ROYAL_BLUE#闪电#LAST#能量的狂潮！`。占位符 `%s` 与颜色标签 `#ROYAL_BLUE#...#LAST#` 完整保留，语义一致。

#### entry-02472
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:330`（Elemental Surge 光系爆发日志）。原文 `%s surges with #YELLOW#light#LAST# power!`，译文 `%s涌起#YELLOW#光系#LAST#能量的狂潮！`。占位符 `%s` 与颜色标签 `#YELLOW#...#LAST#` 完整保留，术语“光系”与规范一致。

#### entry-02473
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:335`（Elemental Surge 自然爆发日志）。原文 `%s surges with #LIGHT_GREEN#natural#LAST# power!`，译文 `%s涌起#LIGHT_GREEN#自然#LAST#能量的狂潮！`。占位符 `%s` 与颜色标签 `#LIGHT_GREEN#...#LAST#` 完整保留，语义一致。

#### entry-02474
- **状态**：细微观察
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:374`（Elemental Surge 技能描述）。源码 `:tformat(t.getThreshold(self, t), t.getDamage(self, t), self:getTalentRadius(t), t.getFire(self, t), cold.armor, cold.dam, t.getLightning(self, t), str)` 对应 8 个占位符（7 个 `%d`，末尾 1 个 `%s`），双百分号 `%%` 均正确保留。排版格式存在细微瑕疵：`#PURPLE#奥术 :#LAST#` 等冒号前多出空格，寒冷效果句末缺少句号；但不影响程序运行与数值显示。

#### entry-02475
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/cun.lua:517`（Tricks of the Trade 前置需求描述）。源码 `special={desc=_t"Have sided with the Assassin Lord", ...}`，译文“与刺客领主同流合污”贴合该任务选择刺客阵营（evil 路线）的语境，无参数格式问题。

#### entry-02476
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/dex.lua:21`。技能名 `Flexible Combat` 译为“灵活格斗”，与觉醒技能既定标准译名一致。

#### entry-02477
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/dex.lua:148`（Swift Hands 技能描述）。源码无占位符参数；译文准确传达备用 4 件工具以及默认 Q 键切装不消耗时间（`takes no time` -> “不再消耗回合”）的机制。

#### entry-02478
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/dex.lua:184`（Windblade 技能描述）。源码为无参 `:tformat()`，原文百分比 `320%%` 正确转义，4 码半径与缴械 4 回合机制准确对应。

#### entry-02479
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/dex.lua:190`。技能名 `Windtouched Speed` 译为“疾风之速”，与既有觉醒技能译名一致。

#### entry-02480
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/dex.lua:278`（Vital Shot 技能描述）。百分比 `450%%` 与 `50%%` 完整保留；源码 `archery_onhit` 实际赋予目标 `EFF_STUNNED`（震慑）与降低三速的 `EFF_CRIPPLE`（残废），受命中（Accuracy）加成，译文完全贴合实际机制。

#### entry-02481
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:65`（Ethereal Form 技能描述）。源码 `:tformat(math.max(self:getMag(), self:getDex()) * 0.7)` 对应 1 个 `%d` 闪避值；百分比 `25%%`、`5%%`、`70%%` 均保留完整无误。

#### entry-02482
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:96`（Aether Permeation 技能描述）。无参数格式；译文准确表达驱散触发（`dispel effect`）、持续 6 回合免疫驱散并中断维持（`unsustaining this spell`）以及提供 40 点原始法强（`raw spellpower`）的机制。

#### entry-02483
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:124`（Arcane Trickster 技能描述）。包含 1 个占位符 `%s`（追加技能列表描述）；引用的技能“毒素爆发”（Venomous Strike）和“诱饵”（Lure）与游戏内对应技能中文译名完全一致。

#### entry-02484
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:137`。技能名 `Arcane Might` 译为“奥术伟力”，为标准觉醒技能名。

#### entry-02485
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:140`（Arcane Might 技能描述）。源码为无参 `:tformat()`，百分比 `50%%`、`100%%`、`25%%` 完整保留，属性转化（武器魔力加成、基础法强转基础物强、法术暴击转物理暴击）表述准确。

#### entry-02486
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:152`（Temporal Form 解锁需求描述）。源码 `special={desc=_t"Have cast over 1000 spells and visited a zone outside of time", ...}`，译文无参数，语义与判定条件完全吻合。

#### entry-02487
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:164`（Temporal Form 技能描述）。无格式参数，百分比 `30%%`、`50%%`、`20%%` 完整保留；各异常技能名（重排、时空风暴、不完美设计、重力井、虫洞）翻译规范。

#### entry-02488
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:174`（Blighted Summoning 解锁需求描述）。源码 `special={desc=_t"Have summoned at least 100 creatures. More permanent summons may count as more than 1.", ...}`，译文无参数，表述准确。

#### entry-02489
- **状态**：存在疑点
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:262`（Blighted Summoning 技能描述）。
  1. **随从术语不一致**：死灵随从列表中的 `- Dread: Slumber` 译为了 `- 梦魇：沉睡`。查阅死灵法师召唤随从实体及技能定义（`mod-tome/data/talents/spells/dreadmaster.lua:16` -> `mod-tome.lua:28559` `t("Dread", "噩灵", "talent name")`）及本批术语快照（`Dread -> 噩灵`），死灵随从应为“噩灵”，“梦魇”常用于 nightmare 类实体，此处偏离随从术语规范。
  2. **细微格式瑕疵**：`- Bone Giants: Bone Spike and Ruin` 译为 `- 骨巨人：白骨尖刺和 毁伤`，“和”字后多了一个多余空格。
  占位符 `%s` 及其他技能名对应正常。

#### entry-02490
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:352`（Cauterize 技能描述）。源码为无参 `:tformat()`，百分比 `10%%` 保留完整，完全吸收当回合致死伤害并在后续 8 回合承受伤害（无视抗性与伤害亲和）的机制描述准确。

#### entry-02491
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:454`（Lich 觉醒触发日志）。源码 `game.bignews:say(120, "#DARK_ORCHID#You are on your way to Lichdom. #{bold}#Your next death will finish the ritual.#{normal}#")`，标签 `#DARK_ORCHID#`、`#{bold}#`、`#{normal}#` 均完整且位置准确。

#### entry-02492
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:465`（Lich 技能描述）。源码为无参 `:tformat()`，百分比 `20%%`、`60%%` 完整保留；各巫妖种族技能（不死之躯、恐怖存在、永恒毁灭、亡者领袖）及数值属性加成翻译完全准确。

#### entry-02493
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/mag.lua:510`（High Thaumaturgist 技能描述）。格式标签 `#CRIMSON#` 完整保留；涉及的基础法术（火球术、奥术射线、闪电术、粉碎钻击、寒冰箭）与元素法师（Archmage）术语均符合规范。

#### entry-02494
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:76`（Giant Leap 技能描述）。源码无参 `:tformat()`，百分比 `200%%` 完整；起跳解定身/眩晕/震慑、落地造成伤害与眩晕（daze）的机制表述清晰。

#### entry-02495
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:127`。技能名 `Massive Blow` 译为“巨力重击”，符合标准觉醒技能名。

#### entry-02496
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:195`（Irresistible Sun 技能描述）。源码 `:tformat(damDesc(FIRE), damDesc(LIGHT), damDesc(PHYSICAL))` 对应 3 个 `%0.2f` 占位符且顺序一致；百分比 `30%%` 与 `150%%` 完整无误。

#### entry-02497
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:217`（You Shall Be My Weapon 技能描述）。源码为无参 `:tformat()`，疲劳值置 0、负重加 500、力量加 50 及体型增大一档（size category +1）准确对应。

#### entry-02498
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:262`（Legacy of the Naloren 技能描述）。源码 `:tformat(level, level)` 对应 2 个 `%d` 技能等级占位符，NPC 人名萨拉苏尔（Slasul）与乌克勒姆斯维奇（Ukllmswwik）准确。

#### entry-02499
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:273`（Superpower 技能描述）。源码为无参 `:tformat()`，百分比 `60%%` 与 `40%%` 完整保留，准确区分了力量转精神强度（Mindpower）与武器意志（Willpower）加成。

#### entry-02500
- **状态**：细微观察
- **依据**：出处为 `mod-tome/data/talents/uber/str.lua:311`（Avatar of a Distant Sun 技能描述）。格式标签 `#GOLD#...#LAST#`、`#{italic}##GOLD#...#{normal}#` 及百分比 `50%%`、`0%%` 均完整；关联技能（光辉引力、光明之刃、灼热之视、阳光之怒、裁决、无御之日）名称均对齐。细微瑕疵：第一项 `The strength of your bond is so strong` 译为了“你的力量如此强大”（实指与遥远恒星间的契约羁绊），但不影响核心机制“同时装备双手武器和盾牌”的正确理解。

#### entry-02501
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/wil.lua:205`（Lucky Day 前置需求描述）。源码 `special={desc=_t"Be lucky already (at least +5 luck)", ...}`，对应基础属性 luck >= 55，译文无参数，表意清晰。

#### entry-02502
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/wil.lua:239`。技能名 `Spell Feedback` 译为“法术反馈”，为反魔系觉醒技能既定标准名。

#### entry-02503
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/wil.lua:245`（Spell Feedback 战斗日志）。源码 `self:logCombat(target, "#LIGHT_BLUE##Source# punishes #Target# for casting a spell!", ...)`，标签 `#LIGHT_BLUE##Source#...#Target#...` 完整保留，机制准确。

#### entry-02504
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/uber/wil.lua:254`（Spell Feedback 技能描述）。源码 `:tformat(damDesc(self, DamageType.MIND, 20 + self:getWil() * 2))` 包含 1 个 `%0.2f` 精神伤害占位符，百分比 `35%%` 完整保留，惩罚法术失败率机制对应正确。

#### entry-02505
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/undeads/ghoul.lua:127`（Retch 视觉日志）。源码 `game.logSeen(self, "%s #YELLOW_GREEN#VOMITS#LAST# on the ground!", ...)`，占位符 `%s` 与颜色标签 `#YELLOW_GREEN#...#LAST#` 均完整无误。

#### entry-02506
- **状态**：细微观察
- **依据**：出处为 `mod-tome/data/talents/undeads/ghoul.lua:251`（Gnaw 技能描述）。源码 `:tformat(100 * damage, duration, damDesc(...), ghoul_duration)` 包含 4 个占位符（`%d%%`、`%d`、`%0.2f`、`%d`），译文顺序与类型完全对应。观察点：描述中提到的召唤随从技能“Ghoulish Leap”译为“食尸鬼跳跃”，与同文件（`mod-tome.lua:31850`）的天赋名称完全一致，但与本批术语快照登记的“定向跳跃”有差异；建议保持与同文件技能名的一致性，不构成阻断问题。

#### entry-02507
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/undeads/lich.lua:95`（Frightening Presence 技能描述）。源码 `:tformat(radius, saves, dam, speed, immune)` 对应 5 个占位符（`%d`、`%d`、`%d%%`、`%d%%`、`%d`），译文顺序、类型及百分号均严格吻合；精神豁免（mental save）、法术强度、物理强度等术语规范。

#### entry-02508
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/undeads/lich.lua:511`（Commander of the Dead 技能描述）。源码 `:tformat(chance, power)` 对应 `%d%%` 与 `%d` 两个占位符，译文匹配；物理强度、法术强度、精神强度与全豁免增益机制表述准确。

#### entry-02509
- **状态**：未发现问题
- **依据**：出处为 `mod-tome/data/talents/undeads/skeleton.lua:100`（Re-assemble 技能描述）。源码 `:tformat(t.getHeal(self, t))` 对应 1 个 `%d` 治疗量占位符；经查阅 `DeathDialog.lua:318`，该技能达到 5 级时在死亡界面确实赋予一次完全重组复活机制（`resurrectBasic` 原地复活并满血恢复资源），译文“原地满血复活（仅限 1 次）”完全符合代码实际机制。

---

### 复核总结

- 全部 40 条均已完成固定源码比对与逐条核验。
- **存在疑点（1 条）**：
  - `entry-02489`：死灵随从 `Dread` 译作“梦魇”（应为“噩灵”，同文件及术语库标准），且存在 `- 骨巨人：白骨尖刺和 毁伤` 多余空格。
- **细微观察（3 条）**：
  - `entry-02474`：冒号前空格与句末标点微瑕。
  - `entry-02500`：首行“bond”意象偏离为“力量”，但不影响功能。
  - `entry-02506`：技能引用“食尸鬼跳跃”与术语快照“定向跳跃”存在差异，但与本地技能条目一致。
- **其余 36 条**：各项占位符、百分号、颜色控制码及技能机制核对均未发现问题。