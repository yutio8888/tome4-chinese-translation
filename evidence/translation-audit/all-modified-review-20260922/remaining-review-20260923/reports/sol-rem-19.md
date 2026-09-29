---

# rem-19 只读交叉核验报告

本报告完成 **GPT 6 Sol 本阶段**的 20 条核查与 C01–C04 四项疑点复核；不代表其他模型复核或正式流程已完成。状态表示本次独立判断，未修改文件。

| 条目 | 本次判定 | 依据 |
|---|---|---|
| entry-04082 | 未发现问题 | 杀兽人及意外对巨人有效，语义相符 |
| entry-04084 | 未发现问题 | 与 04082 同文，译法一致 |
| entry-04085 | 未发现问题 | 喊话、`%s` 和颜色标记完整 |
| entry-04088 | 仅建议 | C01：护符主体不够明确 |
| entry-04090 | 未发现问题 | “A history lesson”语义相符 |
| entry-04091 | 未发现问题 | 职业进阶标题与标记相符 |
| entry-04092 | 存在问题 | C02：遗漏“削弱敌人”这一并列特性 |
| entry-04093 | 未发现问题 | 出生选项标题相符 |
| entry-04094 | 未发现问题 | 法师系选项相符 |
| entry-04095 | 未发现问题 | 盗贼系选项相符 |
| entry-04096 | 未发现问题 | 原版战役选项可表达所指战役 |
| entry-04097 | 未发现问题 | 种族名称及标记相符 |
| entry-04098 | 未发现问题 | 种族名称及标记相符 |
| entry-04099 | 未发现问题 | 职业与类别名称相符 |
| entry-04101 | 存在问题 | C03：“削弱”变成“无处遁形” |
| entry-04104 | 未发现问题 | 数值占位符及颜色标记完整 |
| entry-04105 | 未发现问题 | 源码仅阻止 `T_SHOOT`，译文“普通射击”吻合 |
| entry-04106 | 仅建议 | C04：称号表达生硬 |
| entry-04107 | 未发现问题 | 选项实际指向工匠大师 |
| entry-04108 | 未发现问题 | 制作日志及 `%s` 相符 |

### C01 | entry-04088 | advisory

原译短引：“**神的光辉**充盈着你的全身”。英文明确写 *the light of the Amulet*；物品源码也将其定义为护符，并在佩戴时输出该句。[护符源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/slumbering-caves/objects.lua:35) 第 35–39、52–58 行。最强等价读法是物品名含 *the Light of God*，“神的光辉”可借指这件护符的光；因此不能据此断言译文写成了神亲自降临。建议明确为“护符的光芒”，保留叙事主体。

### C02 | entry-04092 | confirmed

原译短引：“用水和土的力量**毁灭敌人**”。英文并列写 *damage and debilitate your foes*；“毁灭”只笼统表达伤害，未传达削弱敌人的特性。[解锁文本源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-mage_technomancer.lua:31) 第 31 行。最强等价读法是宣传性概括，但该列表逐项介绍职业特性，省去并列作用构成信息缺失。可改为“用水和土的力量伤害并削弱敌人”。

### C03 | entry-04101 | confirmed

原译短引：“让敌人在你的枪法前**无处遁形**”。英文是 *weaken your foes to your gunslinging*，重点为削弱敌人；“无处遁形”转向无法躲藏，不能等价表达。[解锁文本源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-tinker_psyshot.lua:27) 第 27 行；[惊骇天赋源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/dread.lua:49) 第 49–53、69–72 行也展示了削弱效果。最强等价读法是修辞性的“无法抵挡”，仍无法保留 *weaken*。**初审将其具体解释为降低枪击抗性，现有证据不足以支持这一更窄的机制说法**；修正应只承诺“削弱敌人”。

### C04 | entry-04106 | advisory

原译短引：“%s，**实验的工匠**”。英文 *the experimenting tinker* 指进行实验的工匠；同一事件说明她测试新蒸汽科技时迷路。[事件源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/OrcCampaign.lua:389) 第 389–395 行。最强等价读法是“实验的工匠”在称号中仍可理解为做实验的人，故不判错译；“%s，进行实验的工匠”更清楚。

**映射汇总：**C01 → advisory；C02 → confirmed；C03 → confirmed（不采纳初审的“降低枪击抗性”具体解释）；C04 → advisory。新增疑点：无。20 条中存在问题 2 条、仅建议 2 条、未发现问题 16 条、待确认 0 条。

**实际读取与版本限制：**读取了指定入口、`RULES.md`、`batches/rem-19.md`、`reports/gemini-rem-19.md`、`source-access.json`、`terms.json`、本批在 `snapshots/tome-orcs.lua` 的相关同节上下文，以及上引四份 DLC 源码；另读取 `dread.lua`、`OrcCampaign.lua` 和 `PartyTinker.lua` 的相关调用处。所读五份主要源码与来源索引登记的 SHA256 均匹配。本批属于 orcs DLC；冻结文件可确认文本及所示快照行为，**DLC 仓库 commit 和目标游戏版本未固定，不能声称已核验 1.7.4 正式版**。
