# rem-15 只读交叉审核报告

已核完冻结批次的 20 条译文及 C01–C06 六项疑点。结论为：**存在问题 3 条、仅建议 3 条、未发现问题 14 条、待确认 0 条**。另在已有问题条目 `entry-03997` 中发现一处独立偏差 N01；未修改文件。

| 条目 | 结论 | 疑点或依据 |
|---|---|---|
| entry-03987 | 未发现问题 | 医疗炮台描述与原文相符 |
| entry-03990 | 仅建议 | C01 |
| entry-03991 | 未发现问题 | “不是不死族”中的“不死族”为完整名词，否定关系正确 |
| entry-03992 | 未发现问题 | 骷髅分支名称相符 |
| entry-03993 | 未发现问题 | 食尸鬼分支名称相符 |
| entry-03996 | 存在问题 | C02 |
| entry-03997 | 存在问题 | C03、N01 |
| entry-03998 | 未发现问题 | 成就引用相符 |
| entry-04000 | 仅建议 | C04 |
| entry-04001 | 仅建议 | C05 |
| entry-04002 | 未发现问题 | “暮光回响”符合冻结术语记录 |
| entry-04003 | 未发现问题 | 减速、刷新、上限及占位符相符 |
| entry-04004 | 未发现问题 | 星界效果描述相符 |
| entry-04005 | 未发现问题 | 状态日志及 `#Target#` 相符 |
| entry-04006 | 未发现问题 | 状态日志及 `#Target#` 相符 |
| entry-04007 | 未发现问题 | `%d` 对应充能层数 |
| entry-04008 | 存在问题 | C06 |
| entry-04009 | 未发现问题 | 噩梦醒来后的混乱描述相符 |
| entry-04010 | 未发现问题 | 诅咒获得日志相符 |
| entry-04011 | 未发现问题 | 诅咒解除日志相符 |

### C01 | entry-03990 | advisory

原译“你（或任何其他目标）”中，“目标”容易指向承受效果的生物；原文 `any others` 指其他施加方。**等价读法**是该词位于“尝试施加”的主语位置，读者仍可理解为行动方，因此保留为澄清建议。冻结源码在受效果生物身上联动判定，未限定某个施加者：[Combat.lua:29](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Combat.lua:29>)；译文见 [快照:5951](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:5951)。建议用“其他人”或“其他来源”。

### C02 | entry-03996 | confirmed

原译“其受到的法术伤害”遗漏 `you deal to it`，将触发来源扩大。**等价反证**不成立：冻结源码明确要求伤害来源为装置召唤者，且来自法术：[mag.lua:25](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:25>)；原文和译文见 [快照:6002](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6002)。建议补“你对其造成的”。

同一源码的运行计算为 **130%**，而此条英文 NPC 描述及其中文均写 **160%**（[mag.lua:34](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:34>)、[mag.lua:82](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:82>)）。这是英文描述与冻结行为的差异，**不计为中文新增错译**。

### C03 | entry-03997 | confirmed

**C03.1** 原译“当你装备长袍的时候”把“将奥术发电机装入长袍”改成玩家穿上长袍。末段“装备在长袍中”提供部分线索，但不能消除本句的动作和前提偏差。装置限定衣物槽位：[electricity.lua:101](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/electricity.lua:101>)；原译见 [快照:6031](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6031)。

**C03.2** 原译“蒸汽等级”将当前蒸汽量写成等级。**等价反证**不成立：法强公式直接读取 `getSteam()`，不是技能等级：[other.lua:1912](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1912>)。建议分别改为“装入长袍后”“当前蒸汽量”。

### C04 | entry-04000 | advisory

原译“启动时会增加 20%% 疲劳”可能被读成仅在启动瞬间发生；原文 `while active` 指开启期间。**等价读法**是“启动时”也可指从启动起持续生效，故列澄清建议。源码将疲劳作为持续技能的临时属性：[wil.lua:20](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/wil.lua:20>)；译文见 [快照:6060](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6060)。建议写“开启期间”。

### C05 | entry-04001 | advisory

原译“蒸汽回复 +6”“体力回复 + 4”省去原文两处 `/turn`。**等价读法**是“回复”属性本身按回合结算，数值与效果未变；补“每回合”可让单位更清楚。“+ 4”的空格仅属格式。源码属性见 [floor.lua:42](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/floor.lua:42>)；原译见 [快照:6074](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6074)。

### C06 | entry-04008 | confirmed

原译“精神雄蜂飞入”只表达移动，遗漏 `bores into` 的钻入动作。**等价反证**不成立：相关技能说明将“飞向目标”与“附着并钻入头骨”写为先后两个动作：[thoughts-of-iron.lua:103](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua:103>)；状态获得日志见 [mental.lua:85](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua:85>)。建议用“钻入”。

### N01 | entry-03997 | confirmed

首句原译“精通于蒸汽科技”把原文 `dabble in steam technology` 的涉猎、尝试程度提升为精通，是独立的叙事意义偏差。**等价反证**是职业最终可能熟练运用科技，但不能覆盖此句明确的程度用词。原文见 [mag.lua:193](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:193>)，译文见 [快照:6033](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6033)。建议用“涉猎蒸汽科技”。

**读取范围与版本限制：**读取了指定入口、`RULES.md`、本批 `batches/rem-15.md`、指定的 `reports/gemini-rem-15.md`、`terms.json`、`source-access.json`、`snapshots/tome-orcs.lua` 的相关 section，以及登记的 orcs 冻结源码：`turrets.lua`、`uber/{cun,mag,str,wil}.lua`、`timed_effects/{floor,magical,mental}.lua`、`steam/{thoughts-of-iron,other}.lua`、`general/objects/tinkers/electricity.lua`、`superload/mod/class/interface/Combat.lua`；另读取了固定 engine commit 的 `game/modules/tome/data/achievements/kills.lua` 中成就相关行。所读 12 个 orcs 源码文件的 SHA-256 均与 `source-access.json` 登记值一致。orcs **只固定文件哈希，未固定源码仓库 commit 或目标版本**；以上机制结论针对这些冻结文件，不能宣称已核验 1.7.4。
