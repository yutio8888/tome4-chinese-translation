# cycle 1 修复 F01
只修改 tome-orcs.lua C06 的 target，以及 repair-notes.md 的 C06 结论和运行组合例句。其他10条保持已经冻结的target。
主代理已确认：固定core的角色表可以显示任意光标目标；C06 用“你”会使敌人状态说明的主语不清，改为“目标”。%s为空时标点前有多余空格，去掉%s前固定空格。%s现译“并被沉默”无指代，并非reviewer声称的第三人称。详见F01-evidence.json。
建议正文：目标受到飞锯切割，每回合受到 %0.2f 物理伤害%s。持续时间自然结束时，若施加者仍在场，飞锯会爆炸，造成 %0.2f 火焰伤害并飞回施加者，将目标拉回最多 %d 格；免疫击退时不会被拉动。
保持source/tag/args/占位符/换行；新增严格 orcs proposal并lint，验证%s空和非空两种组合、11条范围不变量。根目录原报告与旧证据不改。严格核心构建已对最终mod-tome通过，不重复；DLC构建缺既有baseline/mapping，由宿主记录为已诊断限制。不要stage/commit或写.ai。
