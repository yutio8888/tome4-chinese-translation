# batch-067 译文逐条只读复核报告

### 校验基准与环境信息
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-067.md`
- **文件 SHA-256 校验**：`bec3aea4bbd6c2b67921226121a7909f3ebd2308360ae7f476cd88842beb4f10`（经校验完全一致）
- **源码参考**：`/workspace/t-engine4` 固定公开 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（本批全部 40 条条目均属于核心模块 `mod-tome`，已通过 `git show` 对齐固定版本源码与调用链）
- **条目范围**：`entry-02068` 至 `entry-02107`，共 40 条，已全部逐条覆盖。

---

### entry-02068
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:734-739`。原文使用两处 `%0.1f%%`，分别接收 `t.getPower(self, t)` 与 `10 + t.getPower(self, t) * 5`。译文占位符数量、格式及参数顺序完全一致，体质属性（Constitution）翻译准确，未发现格式或语意偏差。

### entry-02069
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:765-772`。占位符 `%d`、`%d`、`%d`（分别对应负面状态数量、冷却回合、物理豁免）与顺序均正确，机制数值准确。细微观察为：首句「Orcs」译为「兽族」（同 section 的下一条 `entry-02070` 中统一译为「兽人」）；且「They have learnt」在译文中转为了第二人称「你们已经学会忍受」（原文为第三人称叙述「They」）。

### entry-02070
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:787-794`。原文包含两处 `%d%%`，分别传入击杀获得的抗性 `t.getResist(self, t)` 与被动伤害穿透 `t.getPen(self, t)`。译文占位符与顺序完全一致，体质（Constitution）与穿透描述与底层代码逻辑吻合。

### entry-02071
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:950`（Yeek 种族天赋 `Quick Move` 触发日志）。颜色标签 `#RED#` 与 `#LAST#` 完整保留，占位符 `%s` 正确保留且语意与触发条件一致。

### entry-02072
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:1120-1125`。占位符 `%d`（法术豁免）与 `%d%%`（刻印属性倍率加成）顺序和格式正确。排版标签 `#{italic}#“较大”#{normal}#` 对齐原文 `#{italic}#big#{normal}#`，经核对 `game/modules/tome/class/Actor.lua` 中 `size_category == 4` 对应的本地化文本即为“较大”。武器附加伤害减少 50%% 亦与底层 `EFF_2H_PENALTY` 效果一致。

### entry-02073
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/misc/races.lua:1172-1174`（食人魔天赋 `Writ Large` 达到 5 级时日志）。颜色标签 `#PURPLE#` 完整保留。原文「One more inscriptions slot available to buy」译为「你可以消耗一个大系点进一步解锁一个刻印位」，经核验天赋描述与升阶机制，该刻印位确实需要消耗大系点（category point）购买，增译解释性说明符合实际游戏机制。

### entry-02074
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/absorption.lua:388-392`。占位符 `%d%%` 与 `%0.1f` 对应减伤比例及每回合灵能消耗率，数值与底层每回合递增消耗逻辑一致。细微观察为：译文第一行句末「减少受到的所有伤害 %d%%」后缺少英文句号对应的中文句号。

### entry-02075
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-mobility.lua:47-52`。占位符 `%d%%` 与 `-%d%%` 分别对应移动速度提升与击退抗性降低，符号与数值完全对齐。

### entry-02076
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-mobility.lua:80-87`。原文依次传入 `boost`（命中）、`0.5*boost`（暴击率）、`percentinc`（全局速度）及 `t.getDuration`（持续回合），对应占位符 `%d`、`%0.1f%%`、`%d%%`、`%d`。译文顺序、类型完全吻合，精神强度（Mindpower）与全局速度术语规范。

### entry-02077
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-mobility.lua:115-121`。占位符 `%d` 对应施法距离 `range`；状态效果「daze」译为「眩晕」，与震慑（stun）严格区分，符合术语规范。

### entry-02078
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-mobility.lua:154-158`。占位符 `%d` 对应跳跃最大距离，译文准确简练，格式无误。

### entry-02079
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-striking.lua:98-105`。占位符 `%d%%`（武器伤害百分比）、`%d`（定身回合数）、`%0.2f`（对冻结目标的额外伤害）与源码传参顺序严格对齐，定身（pin）、冻结（frozen）、精神强度（Mindpower）翻译准确。

### entry-02080
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/augmented-striking.lua:196-203`。占位符 `%d%%`（寒冷武器伤害）、`%0.1f`（额外寒冷爆发伤害）、`%d`（冻结回合数）完全对应，对定身目标触发冰墙环绕机制的翻译与源码逻辑完全一致。

### entry-02081
- **状态**：存在疑点
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/discharge.lua:104-108`（心灵风暴 `Mind Storm`）。占位符 `%d`、`%0.2f`、`%d`、`%d` 顺序和格式正确。疑点在于：原文中的发射物为「bolts」（飞弹/闪电束/能量弹），译文将其翻译成了「灵能值球」（共出现 3 次）。该技能消耗的专属资源为「反馈值」（Feedback），每个消耗 5 点反馈值；而在 ToME4 机制中，「灵能值」是特定指代「Psi」的另一种独立职业资源。译名中带有「灵能值」字样极易引起玩家对技能消耗资源的误解。

### entry-02082
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/discharge.lua:182-188`。占位符 `%d`（射程）与 `%0.2f`（伤害上限）准确无误；伤害取受击获得的反馈值与上限较小值的逻辑（whichever is lower）翻译准确。

### entry-02083
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/discharge.lua:228-235`。占位符 `%d`（持续时间）、`%d%%`（暴击伤害增益）、`%d%%`（精神抗性穿透）顺序及格式正确。经核验源码，底层随精神强度提升的实际为 `getCritBonus`，译文将最后一句明确作「暴击增益效果按比例加成」，准确体现了代码机制。

### entry-02084
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/distortion.lua:34`。技能名 `Distortion Bolt` 译为「扭曲飞弹」，准确符合惯用译名。

### entry-02085
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/distortion.lua:61-69`。占位符 `%0.2f`（基础伤害）、`%d%%`（抗性降低幅度）、`%d`（爆炸半径）传参顺序一致，静态数值 150%% 准确，5 级免伤友军机制叙述正确。

### entry-02086
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/distortion.lua:227`。战斗日志占位标签 `#Source#` 与 `#Target#` 准确保留，拉取动作与叹号标点一致。

### entry-02087
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:62`。日志颜色标签 `#ORANGE#` 与占位符 `%s` 完整无损，语意匹配。

### entry-02088
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:70`。日志颜色标签 `#ORANGE#` 与占位符 `%s` 完整无损，护盾受击强化机制语意匹配。

### entry-02089
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:201-209`。占位符依次为：%0.2f（锥形精神伤害）、%0.2f（锥形燃烧伤害）、%d（锥形半径）、%d（熔炉外壁持续回合）、%0.2f（外壁周围精神伤害）、%0.2f（外壁周围火焰伤害）。译文 6 处占位符位置与类型完全一致；第二行「50 %%几率」为转义后的合法字符串，不影响逻辑。

### entry-02090
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:220-226`。占位符 `%d`（护甲）、`%d`（闪避）、`%0.2f`（受击回复灵能）准确无误，属性名称与效果对应正确。

### entry-02091
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:254`。颜色标签 `#GOLD#` 与 `%s` 准确保留，动作描述与技能积蓄阶段一致。

### entry-02092
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:257`。颜色标签 `#GOLD#` 与 `%s` 准确保留，对应积蓄完成进入破碎梦境阶段日志。

### entry-02093
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-forge.lua:278-288`。7 处占位符顺序完全对齐：`%d`（最大半径）、`%0.2f`（最大精神伤害）、`%0.2f`（最大燃烧伤害）、`%d`（降低精神豁免数值）、`%d%%`（法术失败率）、`%d`（法术失败持续回合）、`%d%%`（思维封锁几率）。思维封锁（brainlock）与精神豁免（Mental Save）术语一致。

### entry-02094
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-smith.lua:173-178`。占位符 `%d%%`（武器伤害）与 `%d`（命中加成）对应无误，飞锤去程及返回判定机制叙述准确。

### entry-02095
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-smith.lua:181`。技能名称 `Dream Crusher` 译为「梦锤碎击」，用词恰当。

### entry-02096
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-smith.lua:204`。抵抗日志 `%s` 完整，核心技能名「震慑打击」（stunning blow）规范一致。

### entry-02097
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-smith.lua:220-226`。占位符依次为 `%d%%`（武器伤害）、`%d`（震慑回合）、`%d`（计算用物理强度增量）、`%d%%`（所有伤害提升百分比），传参与类型均正确。细微观察为：译文第二行末尾「震慑几率受精神强度加成」遗漏了句末句号。

### entry-02098
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dream-smith.lua:280-287`。占位符依次为 `%d%%`（主目标武器伤害）、`%d`（回音伤害半径）、`%0.2f`（附加精神伤害）、`%0.2f`（附加燃烧伤害），格式与传参完全一致。

### entry-02099
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dreaming.lua:182-187`。占位符 `%d` 对应非睡眠目标时的落点偏差半径 `radius`，优先落于睡眠目标身旁的机制表述准确。

### entry-02100
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/dreaming.lua:222-228`。占位符 `%0.2f%%` 准确反映每回合消耗最大灵能百分比；有关移动中断引导（psionic channel）及梦魇/入梦传染效果在持续期间失效的机制说明完整准确。

### entry-02101
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/feedback.lua:30-38`。占位符 `%0.1f`（转化治疗倍率）、`%d%%`（衰减速率占比）、`%0.1f%%`（每回合衰减率上限）、`%0.2f%%`（每回合实际治疗反馈池占比）4 处顺序与格式完全吻合，意志属性加成表述正确。

### entry-02102
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/feedback.lua:56-61`。固定吸收比例 50%% 与最大吸收量占位符 `%d` 准确，精神强度加成及最多维持 10 回合表述无误。

### entry-02103
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/feedback.lua:146-151`。源码按顺序传入 8 项参数：`heal`、`stamina`、`mana`、`-equilibrium`、`vim`、`positive`（正负能量共用）、`psi`、`hate`；译文对应 8 处 `%d`，参数顺序完全对应，失衡值、活力值、灵能值、仇恨值等资源名称准确。细微观察为：stamina 在此译为「耐力」，而术语快照推荐统一译为「体力值」。

### entry-02104
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/finer-energy-manipulations.lua:89-98`。占位符 `%d`（命中与伤害加成）、`%d`（单件胸甲/盾牌增加护甲）、`%d`（单件胸甲/盾牌降低疲劳）顺序正确；灵晶（mindstars）无法改造及精神强度加成机制叙述清晰。

### entry-02105
- **状态**：未发现问题
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/finer-energy-manipulations.lua:125-131`。占位符 `%d` 对应每回合获得的灵能值，消耗宝石提供 5~13 回合回能与晶体共鸣效果叙述准确。

### entry-02106
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/finer-energy-manipulations.lua:151-159`及 `game/modules/tome/data/talents/psionic/other.lua:246-254`。占位符 `%d%%`（意志灵巧代替力敏百分比）、`%d%%`（抓取几率加成）、`%d`（属性加成）顺序正确。经核验底层代码，心灵聚焦装配宝石时提升的是 6 大主要属性，译文增译「全属性」符合代码事实。细微观察为：第一行句末漏句号；第二行句末混用了半角英文句号「.」；第三行原文为「+%d%%」，译文略去了正号写为「%d%%」。

### entry-02107
- **状态**：细微观察
- **可核验依据**：源码见 `game/modules/tome/data/talents/psionic/focus.lua:62-67`。占位符 `%d`（物理伤害）与固定数值 `-15%%` 准确。细微观察为：原文「for 2 turns」在译文中写为「两轮」（ToME4 技能描述中通行为阿拉伯数字加「2 回合」），括号内「-15%% damage penalty」略去了「惩罚」字样译作「-15%% 伤害」。核心数值与机制判定准确。

---

### 复核总结
- **核验条目总数**：40 条（`entry-02068` 至 `entry-02107`，逐条全覆盖，无遗漏）
- **未发现问题**：33 条
- **细微观察**：6 条（`entry-02069`、`entry-02074`、`entry-02097`、`entry-02103`、`entry-02106`、`entry-02107`，主要为标点遗漏、英文句点混用或专有名词/人称细微差异）
- **存在疑点**：1 条（`entry-02081`：将消耗反馈值的飞弹「bolts」翻译为容易与 Psi 资源混淆的「灵能值球」）