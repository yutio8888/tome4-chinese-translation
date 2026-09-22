# 翻译审核当前交接

更新时间：2026-09-22（审核246已finalize；流程/prompt修订已验收，连续审核已恢复）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前授权与状态

用户已明确恢复“请继续推进审核工作”，并要求“请调整流程和prompt后继续”。此前暂停已解除；连续审核和每批推送的授权持续有效，不逐批询问。当前应先完成本轮维护提交后的queue同步和push，再进入修复窗口3；不先开247。

- 审核246（`batch-a5489a23ea457e1c6fde`）80条固定来源tome，生产结果 **74 done / 6 repair_required**。8条正式语境复审、15条观察裁决、17项完整门禁和严格addon构建通过。证据提交 `7b32ba676f6445970b1547f01b701ed79df8739c` 已实际finalize成功，active checkpoint已移除。实际命令耗时与结果见 [FINALIZE-RECEIPT](evidence/quality/production-batches/batch-a5489a23ea457e1c6fde-host-evidence/FINALIZE-RECEIPT.json)。
- 本批另外以独立补充task确认GRAPPLING、Battle Cry两条原surface OK的修复候选；不改写原初筛或伪造生产repair_required。三个审核task均DONE_VERIFIED，所有实际child确认归档，冻结快照独立重放通过。正式及补充语境输入均实际先anchor preflight后冻结。详见 [246宿主证据](evidence/quality/production-batches/batch-a5489a23ea457e1c6fde-host-evidence/summary.md)。
- 流程维护 `review-input-policy-20260922` 已DONE_VERIFIED：13文件统一角色、契约、正式三行prompt及实际消费者，249项定向测试、完整ci-gates（不影响addon故skip-build）、两轮独立双模型复审通过，全部child归档。详见 [修订验收](evidence/quality/review-input-policy-20260922/summary.md)。为保留活动批次基线，该维护在246 finalize之后单独提交。
- 当前交接撰写时，维护提交、其后的queue rebuild和push尚待宿主执行。恢复时以git/远端和SQLite `meta.evidence_head`实测为准：若已一致，不重复rebuild或finalize。不得把本段当作未完成246审核的理由。

## 流程修订与历史边界

- REVIEWER只使用冻结envelope内实际译文/术语正文；file、line、hash仅证明来源，不授权搜索当前译文或术语库。`terminology_snapshot`可能只是摘要；真实术语正文可在`bounded_context`的`source_facts_v1.fact.terminology`中。
- 可完整读取对应审核契约。contextual仍可沿调用链补查固定版本相关公开源码；surface不因此增加源码调查权限。缺少术语依据不自动成为缺陷，只有具体疑点才记现有observation并由宿主补足中性证据。
- 所有新派发使用正式builder，禁止临时手写prompt或硬编码文档行号；三个入口和两个真实消费者已复用同一模板。三行及800字节限制包含实际路径；输入中的所有行分隔符均拒绝。
- JSON有效、实际读取范围合规、child生命周期闭合必须分别核验。246新语境派发全数一次通过；旧未接纳的一段式prompt输出保留并明确弃用。原已发布surface R3使用定制三行变体的宿主偏差照实记录，不伪称其为正式模板。
- 旧补充R2“术语越界”归因过强已更正；原prompt未明确来源路径与精确行授权的区别，不能追溯归咎reviewer。维护任务的CODE_DIFF文件命名遗漏attempt段也已用字节相同副本和绑定记录修正，原派发/报告/输入保留。

## 修复窗口3：14个可执行revision

短键仅作定位，实施时从受跟踪workset读取完整identity、section、source_tag和冻结target。

| revision前缀 | 问题 | 来源 |
| --- | --- | --- |
| `df61b36589` | 念动弓每回合攻击和伤害遗漏；不恢复与随机选敌实现矛盾的“最近” | 244生产裁决 |
| `df8f5280bf` | 阴影持续补召和数量上限遗漏 | 244生产裁决 |
| `dfdfbe6089` | 纯净以太清除负面效果的“最多”遗漏 | 245生产裁决 |
| `e035e585a6` | skewered被误加“烤”制语义 | 245生产裁决 |
| `e0886c07f8` | 漩涡中/靠近及来袭抛射物方向错误 | 245生产裁决 |
| `dff11a9be5` | Rosebloom最低治疗量按流血效果而非敌人 | 245独立补充 |
| `e1177a8f9f` | 城市后方的小型石岛被改成周围浮空岛 | 246生产裁决 |
| `e122dd9c58` | 黑暗帷幕/阴影群两种掩护关系遗漏 | 246生产裁决 |
| `e128c83148` | 溢出治疗不计及总能量储存上限遗漏 | 246生产裁决 |
| `e172753e04` | Dismissal仅成功检定才减伤的条件遗漏 | 246生产裁决 |
| `e1884052fc` | Swap生物目标被缩窄为怪物 | 246生产裁决 |
| `e1cd6fb504` | Rolf书信地点、獠牙比较、传说延续等事实失真 | 246生产裁决 |
| `e1343327ea` | 擒抱消耗自身的体力，不是吸取；转移的是所受伤害 | 246独立补充 |
| `e200845e1a` | 战吼击溃斗志不等于降低Willpower属性 | 246独立补充 |

“不死亡灵”、generic spellcrit空格、10 %%间距只记advisory，不单独触发修复。距离单位“码”的跨批统一不在授权内。补充审稿把擒抱体力误称生命力，宿主已按`incStamina(-eff.drain)`纠正，原raw不改。

## 下一步

1. 无活动checkpoint，完成维护提交后计时queue rebuild并核对HEAD，再push并核验远端。仅当当前HEAD和queue/远端不一致时做所缺步骤。
2. 分别对244、245、246运行真实repair preflight，保存各自原schema workset；可用`run_repair_steps.py preflight`共享一次投影，不能伪装成一个来源批次。三条宿主补充另列来源/授权/源码验收，不改旧生产状态。
3. 建立唯一EXECUTOR的14条实现任务；固定源码核验、值流、不变量、strict proposal/lint、四成员v2复审与FINAL全量复审、完整门禁及构建、DONE_VERIFIED均须完成。
4. 提交译文 → 第一次queue rebuild → 单次候选catalog及migration-chain → 提交必要repair evidence/catalog/migration → 第二次queue rebuild → push。successor仍待重新审核。随后开247，默认80条。

## 已完成基础与排除项

- 244证据提交 `79e81d1ac08123c626fedb9e299c033498e26f97`，78 done / 2 repair_required；原冻结前anchor preflight遗漏已明确记录，并以有效独立补充验证相同三条。第一次补充的越界读取结论已撤销，更正及替代记录见 `evidence/quality/production-batches/batch-f426f5a2d72329efe102-anchor-remediation/`。不重写原244历史。
- 245证据提交 `023dcd03addcd342125f1c8908302250ec4af012`，77 done / 3 repair_required；另有Rosebloom补充1条。均finalize并推送。244补充更正和245收尾提交 `39cbeefcc36edae80da024cc84931c187381ba62`；旧暂停交接为`7c38a53`。
- 修复窗口2译文 `14c755659d18a5f0989ec75d67f0245de3f0cc13`、证据 `e117983a360b8dcb360ab35f0b5414148d534605`已推送。当前catalog `2a8b6f4ac30dba6abff9e96dc37295d5e0f20acb5e4b97067160261b346e358d`，migration `0e4ad828eb000567f49f34b1b7a9e8c823550740697b51a4d616d72cc9dac454`。不重做；详见`evidence/quality/repair-window-2-20260921/summary.md`。
- Archmage `8b977dd836…`仍为范围外pending；`RW1-SIB-01`、`RW1-SIB-02`永久排除。不计可执行阈值，不改译或清状态。
- 固定tome/engine源码commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；244—246无DLC。没有术语库修改、全局改名或跨批策略变更。
- 保留`.ai/consult/`、`recipe`及旧未跟踪workset，不读取、暂存或清理无关文件。历史细节见`docs/handoff-history-through-20260919.md`，当前会话授权优先。
