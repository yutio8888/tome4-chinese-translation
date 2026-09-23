# 翻译审核当前交接

更新时间：2026-09-23（修复窗口8已完成；待宿主发布收尾，随后审核255）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前授权与实测状态

用户于2026-09-23指示先做工具维护，然后持续推进审核，无需手动确认；有争议条目列入 pending
集中审阅，不修、不阻塞。当前清单见[待用户集中审阅的争议条目](evidence/quality/pending-user-review.md)。
审核模型仍为 **surface `codex/gpt-6-sol`（medium，auto-review）**、**contextual
`claude/claude-opus-5-5`（medium，auto）**；live profile 缺失时按用户指示直接选择并保留快照。

工具维护已提交为 `b626eaf1c30ed389dff0b0a633e393225ea46843`：原生 parser 已支持 Codex 0.156.0
与 Claude Code 2.1.280（含归档末尾 `cost-state` 记录），并以 10 份真实会话验证。原“工具版本偏差”
已经解决，详见[原生 parser 版本维护](evidence/quality/native-parser-versions-20260923/summary.md)。

已核实：活动批次从 batch start 到 finalize 期间不能插入任何提交；
`production_review_v2_lite_batch.py:1084` 会检查 base commit drift，`:1909` 会检查 finalize parent。
修复窗口中 preflight 后插入提交会使 preflight 失效，必须重跑；每次提交后都需 queue rebuild。
因此工具维护只能放在批次或修复窗口之间。

修复窗口8已完成，译文提交为 `9b71efd8714678d10419f9522a93a25c92f3e841`。六条目标为无尽狩猎
描述、`ALL_DREAMS`、Yeek 换行、Thalore 诗句（含紫杉及鸫鸟/猫头鹰行）、麻痹毒素伤害方向和
《龙族传说》四处语义。`REVIEW/full`（`codex/gpt-6-sol`）原始结果为 2 OK / 4 ISSUE：诗句
确认后追加一轮有界修复，其余三条转 pending；`FINAL_REVIEW/full`（`claude/claude-opus-5-5`）
为 6 OK / 0 ISSUE。完整门禁 `run.2f4mryxp` 17/17 通过并含严格构建，任务 `DONE_VERIFIED`；
四个实施/复审 child 均已归档，本 publication child 待宿主归档。完整结果见
[窗口8出版证据](evidence/quality/repair-window-8-20260923/PUBLICATION.md)。

新 catalog 为 `8580c7207ae19005bb206138eabe0daf3fb00a7eb0513c113b64c922adbc5cf2`，migration 为
`518ce6ed86c6d746184ff38b10a45cd9755ff56c2c57a0af650d7aa03252552f`；6 条 revision changed、
29,822 条 unchanged、0 ambiguous/unmapped，6 个 successor 待重新审核，不继承 done。

下一步由宿主执行本证据提交、第二次 queue rebuild 和 push，随后继续审核255（默认80条）。
这些后续步骤尚未完成，不得提前宣称完成。

### 窗口7闭合时的暂停记录（历史）

用户于2026-09-22明确要求“这轮修复完成后暂停并撰写handoff文档”；该暂停已由2026-09-23指示解除。

审核253（`batch-ba766c90924912867b02`）已完全闭合，结果为 **72 done / 8 repair_required**。
证据提交`3927ca05a43daee81bb2a2fadaf77d2b3b881d0b`、收尾提交
`e103379a5e809923401aa0099cfbdc9f104725ca`，收尾后的queue、push、远端HEAD与SQLite evidence
head核验均已完成。详见[253宿主证据](evidence/quality/production-batches/batch-ba766c90924912867b02-host-evidence/summary.md)、
[finalize收据](evidence/quality/production-batches/batch-ba766c90924912867b02-host-evidence/FINALIZE-RECEIPT.json)
及[收尾核验](evidence/quality/repair-window-7-20260922/publication/review253-push-verification.json)。

修复窗口7的八个target已完成并提交为`312dcd6844f80fff34911999bffab7a8f954e34f`。四成员复审各轮
原始结果依次为R0 6 OK / 2 ISSUE、R1 6 OK / 2 ISSUE、R2 6 OK / 2 ISSUE、R3 7 OK / 1 ISSUE；
这些历史finding均保留。R0经宿主源码确认并有界修复疾病传播全部疾病和盾牌跃击动作；R1只接受
Mind Storm总量量词修复，spinneret兄弟项保持范围外advisory。第二轮后SENIOR scope audit对挽歌
触发条件为`keep`、对spinneret兄弟项为`narrow`，宿主仅接受一个触发句修复，默认cycle 3上限
没有扩大。R3的Vault选择坐标/落点观察裁决为非阻断advisory。最终full review为 **8 OK / 0 ISSUE**，
不倒改历轮原始结果。

最终完整门禁`run.4d0v0980`为17/17通过并含strict build；任务与452项、2,317,751 bytes的
immutable快照均`DONE_VERIFIED`。实施/复审22个child及publication child共23个均已确认归档；最终状态检查通过。
完整结果见[窗口7出版证据](evidence/quality/repair-window-7-20260922/PUBLICATION.md)。

一次catalog build和migration-chain已完成，不得重跑。当前catalog为
`0fece77f6c05306c2706b263729cc1a3b5fcdf1dc29f58bd41af380204595696`，migration为
`677e6622a2146f9f9686ee91c9d1bc3f02990c8d08547df721786877dd287325`；8 revision changed、
29,820 unchanged、0 ambiguous/unmapped，8个successor已入队且须重新审核，不继承旧done。

### 已完成的收尾与暂停边界

证据/catalog/migration提交为`bfa1a096da0b6d790167de0f600c7aff41dfcb59`，提交后的第二次queue rebuild、push与远端核验
均已于`2026-09-22T16:14:31.628477+00:00`完成；本地HEAD、origin/develop与SQLite evidence head一致。
队列实测 **22254 done / 1 repair_required / 24 blocked / 7549 queued**；本轮8个新revision逐条确认queued，须重新审核。
详见[收尾核验](evidence/quality/repair-window-7-20260922/closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-CLOSURE.json)。

原452项immutable快照保持原字节；收尾增量共27项，包含publication生命周期、
提交/队列/push证明，与基础快照合并后独立重放为`DONE_VERIFIED`。
见[增量重放结果](evidence/quality/repair-window-7-20260922/closure/replay-verification.json)。
本交接和收尾证明随最终文档提交保存，提交后仅同步queue并push，不再产生译文或新批次。
（当时为STOP；已于2026-09-23由用户新授权解除，审核254已完成。）

旧Archmage、旧回忆录pending、`RW1-SIB-01/02`、旧blocked及范围外兄弟条目保持原状态。
`.ai/consult/`、recipe和15个旧source-workset继续保留。

### 已闭合的修复窗口6

窗口6两条修复（日记省略号前后空行、古战场成就惊扰行为）已完整闭合：译文提交
`38e666aaae9e5738819e3b6525398b9bfc9872eb`，证据/catalog/migration提交
`1351d3f4fb0f8efe4d017039ad236848a13290df`。第二次queue、push与远端/本地/SQLite三方核验
于14:06:43完成，4个child全部确认归档，最终STATE再次DONE_VERIFIED。
原97文件、765623 bytes的immutable包保持不变；发布收尾与生命周期证据已附在本批253
快照中独立重放。原生审计调用汇总12已纠正为11；冻结证据5处历史空白有逐字节例外记录，
没有清洗或改写冻结输入。17/17门禁及严格构建通过。

窗口6闭合时catalog为`6f08ccf5394d2f0431a066c1315ba5abcdeaed1928e4781a0b1cb65e37e68405`，
窗口6migration为`92da0238e3a17f7b5d3b4e46156ef0b9d5bacfd653bb2e00618d6f0ede25a83d`。
两条successor曾重新入队，本次253均通过审核；不得重复catalog build/migration。
窗口6闭合时队列实测22182 done / 1 repair_required / 24 blocked / 7621 queued；后续以本批
收尾rebuild与实际SQLite结果为准。

审核252及Git索引测试夹具维护已闭合并于13:27推送`805b67263c3359441a4e6e12f3ebd0d2bdc5a0da`。
夹具已改为长度无关的非法索引构造；生产解析器未改，默认131模块测试及7/8/12/40位负例通过。
252原失败日志和有界诊断均保留；后续门禁恢复默认Git环境。

### 已闭合的修复窗口5

窗口5执行时用户授权连续审核和每批 push；现以顶部暂停指令为准。审核 250、251 均已完成；窗口 5 因高影响机制问题在
251 安全边界提前进入修复，没有等待第三批。18 条修复由两次真实 repair preflight 的 16 条
（250 十条、251 六条）和 251 宿主独立补充 2 条组成；补充条目没有被伪称为生产
`repair_required`。

译文提交为 `f0560f5d888a9c5a84f21c1216e43eb1645437d3`，只修改 `mod-tome.lua`
的 18 个 target；source、source_tag、args_order 等保持不变，只有原授权 `e56b636891…`
恢复源码 1 LF / 2 TAB 布局。没有术语库变更。三轮上限后的最终复审发现 source 188 的
`hum` 被译成“呼吸”，任务真实暂停 `WAIT_USER`；用户“同意”额外一轮，SENIOR 范围校准
`keep`，仅改成“嗡嗡作响”。本次 `max_cycles=4` 是单次明确授权，不是后续默认规则。

最新最终全量原始结果为 16 `OK` 加 2 `ISSUE`，不是 18 `OK`。宿主裁决范围内无
accepted/deferred 后 completed：回忆录 source 358 清醒时喂水及 source 380 前往 Elvala
的未编辑子句保留 pending；Corruptor 职业 birth descriptor existing 条目不强制映射叙事 `_t`，
保留 advisory。其他历轮范围外回忆录和称谓建议保持原记录，不新增修复。身份或读取边界不合格的
复审尝试及 fresh retries 均原样保留，未把无效结果用作审核依据。

最终完整门禁 `run.rlohbmvk` 为 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。738 文件、
8,798,915 bytes 的冻结包已独立 snapshot 重放通过；归档 STATE 使用 immutable checkpoint。
五个 candidate catalog 文件、migration 与 12 份 publication 原始附件均已逐字安装并复核。
窗口5闭合时 catalog 为 `c267a00eaf39f49b99266912241cfed79dfcbda440903763975ea2e4334a239d`，
migration 为 `198b6812cf2fc2865016eb39153f90a70f244d3984a6ca81009bde8c2e897b6a`。
单次 catalog build 与 migration-chain 已完成，禁止重做；18 条 revision changed、29,810 条
unchanged，0 ambiguous/unmapped，18 个 successor 已入队且须重新审核，不继承旧 revision 完成态。
完整边界、哈希与计时见[窗口5出版证据](evidence/quality/repair-window-5-20260922/PUBLICATION.md)。

窗口5证据提交`901fce3886d5b565bc55b205e5ab27086621aa8f`、提交后的第二次queue rebuild、
push及远端复核均已于12:28完成，18个successor当时逐条验证入队；不再重做。
旧Archmage、范围外pending、旧blocked及`RW1-SIB-01/02`不扩大；`.ai/consult/`、`recipe` 和 15 个旧 source-workset 保留，不纳入
本次提交或清理。

## 审核251：修复窗口5第二批，提前修复边界

`batch-c8180aa79c1822c18e7c`，80条固定tome来源，**74 done / 6 repair_required**。
12条正式上下文复核；16项观察裁决为9 confirmed、3 refuted、4 advisory。另2条独立补充复核
确认击退碰撞日志和可用于治疗的精神暴击日志，保持原生产状态不变，单独纳入修复。
9个真实child全部归档，其中6份有效结果、3份拒收结果；两次revision标识错误及一次读取越界
均保留原始证据，未修补输出或冒充正式结果。最终Opus复审有效，5个有效Sol结果来自surface及补充任务。
三个任务及206文件、1,522,597 bytes的独立快照均DONE_VERIFIED，17项完整门禁与严格构建通过。
证据提交 `e0148fc67c09c8b1f6da0fab77b30aeface0e7f5` 已finalize，运行时contextual字节与提交逐一核验归档。
详情见[251宿主证据](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/summary.md)和
[finalize收据](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/FINALIZE-RECEIPT.json)。

正式修复范围：暴击失衡值方向、闪避适用范围、盾牌抵御/时期/时间修饰语、受伤触发描述、战术边框用途、
伐木工说话状态及恐怖描述。兽族忍耐命名、人物音译、轮/回合只记建议；击退、潜行及按物品分项的聚焦效果误报撤销。
提前修复依据见[窗口决定](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/orchestration/.ai/task/batch-c8180aa79c1822c18e7c/WINDOW5-EARLY-REPAIR-DECISION.json)。
补充两条为 `e68cd1e92d…`、`e6976768f9…`，来源见[补充裁决](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/orchestration/.ai/task/batch251-host-contextual-20260922/HOST-ADJUDICATION.json)。

## 审核250：修复窗口5第一批

`batch-990137011625a41fa36b`，80条固定tome来源，**70 done / 10 repair_required**。
12条上下文复核；22项观察为19 confirmed、1 refuted、2 advisory，按revision合并为10条待修复。
五位真实reviewer均已核验原始结果、读取边界及归档；两个任务及其独立快照重放均DONE_VERIFIED。
17项完整门禁和严格addon构建通过，证据提交 `16c82d316f07007ac7bcbb48ce1bcb2f202414d6` 已finalize。
详情见[250宿主证据](evidence/quality/production-batches/batch-990137011625a41fa36b-host-evidence/summary.md)及
[finalize收据](evidence/quality/production-batches/batch-990137011625a41fa36b-host-evidence/FINALIZE-RECEIPT.json)。
运行时contextual输入及输出与该提交逐字节一致，已保留归档并腾出下一批运行路径。

本批保留了三项宿主准备偏差的真实记录：首次未创建child的profile准备被拒、行政元数据晚补、
producer envelope提前导出后经preflight才重新冻结正式任务输入；所有contextual child均在后者之后派发。
251须在surface派发前完成SPEC/PLAN/SCOPE，并在contextual export前完成准确draft的preflight。
待修复包括幽灵人形、啃噬疫病后续死亡限定、触手追踪上限与换行、生命之泉分类、肢解含义、
自然精灵领地、法师初始知识和两条回忆录局部问题。
Ritch名称误报撤销；See Threads命名及其他非阻断建议不自动扩大修复范围。

## 审核249：修复窗口4第三批

`batch-1da0a9afd2d1888c2099`，80条固定tome来源，**72 done / 8 repair_required**。
13条上下文复核；22项观察裁决为14 confirmed、3 refuted、5 advisory，按revision去重为8条待修复。
5位真实reviewer均通过strict、原生来源与读取边界核验并确认归档；两个任务DONE_VERIFIED，
127文件宿主快照独立重放通过，17项完整门禁和严格addon构建通过。
详情见[249宿主证据](evidence/quality/production-batches/batch-1da0a9afd2d1888c2099-host-evidence/summary.md)。

待修复为`e454e243b1…`换行、`e4871be69c…`腰带修饰关系、`e4afe73e4f…`大罪字幕、
`e4c192463a…`兽人历史、`e4c5fea288…`自然精灵亚种、`e4c8e60909…`治疗反转敌方限定、
`e50eb91c9e…`诗句可能情态、`e542306f47…`潜行动作及句界。
基础伤害与颠茄毒素有源码支持；神器名称、传送门激活措辞、诗歌偏见意译与刃缘形状精细化仅为非阻断建议。
临时准备脚本的旧契约节号说明已更正，实际派发prompt始终允许完整契约；未改冻结输入或既有审核记录。
运行时contextual输入在finalize后已与提交原文逐字节核验并保留归档。

## 审核248：修复窗口4第二批

`batch-d83278160a384bef39ff`，80条固定tome来源，**73 done / 6 repair_required / 1 blocked**。
10条正式上下文复核；18项观察裁决为11 confirmed、1 refuted、6 advisory，confirmed按revision去重为6条。
另有一条长篇回忆录独立补充复核，作为窗口4的补充修复候选，不改写原surface OK或生产状态。
六位真实reviewer均通过strict、原生来源与读取边界核验并确认归档；三个任务DONE_VERIFIED，
157文件归档快照独立重放通过，17项完整门禁与严格addon构建通过。
详情见[248宿主证据](evidence/quality/production-batches/batch-d83278160a384bef39ff-host-evidence/summary.md)。

正式待修复项为峰顶限定`e318607df2…`、Fireflash爆炸半径`e359df96b1…`、建筑内外方位`e3aebb4595…`、
噩梦新增清醒限制`e3b3e027a2…`、毒素集合`e3ed20c85b…`、组装物品关系`e407b46fe5…`。
独立补充`e433115e63…`只修复已确认的裸体/兴奋场景、向东出发及气氛转折、条件性恨意和水晶塔比喻；
依据见[补充裁决](evidence/quality/production-batches/batch-d83278160a384bef39ff-host-evidence/orchestration/.ai/task/batch248-host-contextual-20260922/HOST-ADJUDICATION.json)。

`e3eec8e65c…`旧任务完成提示键与固定源码的空格不同；实际消费者在PlayerQuestPopup.lua。
已按正式host-block记录阻断，[完整来源归因](evidence/quality/production-batches/batch-d83278160a384bef39ff-source-attribution.json)包含全固定源码精确检索和调用位置。
不把表面OK算作done，不在此任务迁移source key。岩石藤蔓有源码支持，标题措辞、传送门简称/空格和
技能树简述只记建议；不扩大距离单位“码”的跨批策略。运行时contextual输入已在finalize后与已提交原文逐字节核验并归档。

## 审核 247：修复窗口 4 第一批

`batch-fe19bbe5e5898a0c3547`，80 条固定 tome 来源，**78 done / 2 repair_required**。
11 条进入上下文复核；13 条观察裁决为 4 confirmed、7 refuted、2 advisory，confirmed
按 revision 去重为 2 条。5 个真实 reviewer 均完成 strict、读取边界及来源核验并确认归档；
初筛和上下文两个任务均 DONE_VERIFIED，134 文件宿主快照独立重放通过。17 项完整门禁
及严格 addon 构建通过。详情见 [247 宿主证据](evidence/quality/production-batches/batch-fe19bbe5e5898a0c3547-host-evidence/summary.md)。

待修复项为 `e22d6fff0c…` 自定义贴图捐赠条件与段落换行、`e2be3d8377…` 腐化者自身腐化之血。
随机选敌、Dismissal 生命上限调整、失眠累积、锥形战吼、Feed Power 和死亡阈值均经固定源码
核验；不能因英文说明陈旧而回改当前译文。Fear 措辞、中文冒号空格及 Wanderer 省略仅为非阻断建议。

首次 surface prepared 配置与 profile 不符，在任何 child 创建前拒绝，保留原 prepared 记录；
实际使用 attempt 2 完整四 lane。首次 contextual export 因246旧运行时槽位占用失败，
对照已提交246原文逐字节核验后保留备份再重试；本批 preflight 在首次 freeze 之前实际通过。
不修改冻结候选，不更改工具防护。后续批次在 finalize 后按既有路径和哈希保留归档其运行时输入，
避免将旧槽位误认为新批次候选；不得据目录残留自行扩展当前 checkpoint 的 refs。

## 审核 246 与流程维护

- 审核 246（`batch-a5489a23ea457e1c6fde`）固定来源 tome，共 80 条，生产结果
  **74 done / 6 repair_required**。8 条正式语境复审、15 条观察裁决、17 项完整门禁和
  严格 addon 构建通过；证据提交
  `7b32ba676f6445970b1547f01b701ed79df8739c` 已 finalize。详情见
  [246 宿主证据](evidence/quality/production-batches/batch-a5489a23ea457e1c6fde-host-evidence/summary.md)。
- 另有 GRAPPLING、Battle Cry 两条宿主独立补充候选；没有改写原 surface 结果或伪造
  原生产 `repair_required`。相关 task 均 `DONE_VERIFIED`，child 已归档，冻结快照回放通过。
- 流程维护 `review-input-policy-20260922` 已 `DONE_VERIFIED`：13 文件统一角色、契约、
  三行 prompt 和实际消费者；249 项定向测试、完整 ci-gates、两轮独立双模型复审通过。
  维护提交已包含在远端基线 `9fb5ec1…`。详情见
  [流程修订验收](evidence/quality/review-input-policy-20260922/summary.md)。

## 修复窗口 3

244—246 的 14 条已确认 target 已在提交 `254ad2b…` 修正，其中 11 条来自原生产裁决，
Rosebloom、擒抱和战吼 3 条为宿主独立补充。候选及当前 `mod-tome.lua` SHA-256 为
`dd793e3d0f4336c881f30e7cb4e62bdccfc90dbaa263182ce4b57a18ad4c76c8`。

- 三批 repair preflight、固定源码核验、两轮合并修复、三轮四 lane v2 复审和最终全量复审完成。
  有效轮次是 r0a3、r1a3、r2a1，最终为 cycle 2 attempt 2 / `f2a1`，14 条全部 `OK`。
  r0a1/r0a2/r1a1/r1a2 为已记录的失效尝试，不计入有效复审；最终 terminal 坐标更正没有
  改写 envelope/raw/prompt/native 结果，也不是新增复审运行。
- 17 项完整门禁、严格 addon 构建和 `DONE_VERIFIED` 已完成。本次出版又从 464 文件、
  3,764,919 bytes 的受跟踪归档快照独立回放，RC 0；冻结包中 STATE 表示出版 child 之前
  全部译文/审核 child 已归档的验证边界，不是出版 child 的实时 STATE。
- 第一次 queue rebuild RC 0；catalog 只构建一次；migration-chain 只运行一次且 plan/check/apply
  均 RC 0。旧 catalog
  `2a8b6f4ac30dba6abff9e96dc37295d5e0f20acb5e4b97067160261b346e358d`
  迁移到 `75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`；
  migration 为 `5dccee54c4aed46e7b80f17a523eb61d9058add7926f7e292ba5eb45350ad0bf`。
  结果为 14 changed / 29,814 unchanged，0 ambiguous/unmapped，14 个 successor 已入队且必须重新审核。
- catalog/schema/policy、migration、464 文件归档及 publication 输入均按来源逐字节安装并复核。
  证据提交 `081d3a03…`、第二次队列同步和远端核验均已完成；完整边界、哈希与真实计时见
  [窗口 3 出版证据](evidence/quality/repair-window-3-20260922/summary.md)。

本窗口只修正获准 target，没有术语库修改、全局改名或跨批策略变更。固定 tome/engine 源码为
`624a67329fe2ad440c5b344785a9c73fcf22ae63`，244—246 无 DLC。距离单位“码”的跨批统一、
“不死亡灵”、generic spellcrit 空格及其他 advisory 均未借机扩大范围。

## 修复预检兼容维护

窗口4首次repair preflight中247通过，248的host_blocks_sha256被修复消费者旧字段集合拒绝，249未运行。
已将前置解析统一为现有封闭schema解析器，保留全部hash、来源、winner和preimage验证。
新增混合repair/blocked回归在修改前复现、修改后通过，3项定向测试和16项完整工具检查通过；
实际三个来源批次重新preflight全部成功（2/6/8条）。原失败尝试及产物保留，正式新workset使用attempt02路径。
此代码维护不改变addon输出，按矩阵跳过构建；后续17条正式译文修复仍需完整构建。
详情见[兼容维护证据](evidence/quality/repair-preflight-host-blocks-20260922/summary.md)。
当时须先提交本维护、同步队列并推送，再以新HEAD启动IMPLEMENT；这些步骤现已作为历史闭合，
已验证的catalog和17条preimage没有变化。

## 保留边界与历史

- Archmage `8b977dd836…`仍为范围外 pending；`RW1-SIB-01`、`RW1-SIB-02` 永久排除，
  不计可执行阈值，不改译或清状态。
- 244 证据提交 `79e81d1ac08123c626fedb9e299c033498e26f97`，78 done / 2 repair_required。
  245 证据提交 `023dcd03addcd342125f1c8908302250ec4af012`，77 done / 3 repair_required；
  244 补充更正和 245 收尾提交 `39cbeefcc36edae80da024cc84931c187381ba62`。旧证据保持不变。
- 修复窗口 2 译文 `14c755659d18a5f0989ec75d67f0245de3f0cc13`、证据
  `e117983a360b8dcb360ab35f0b5414148d534605` 已推送，不重做。
- REVIEWER 仍只使用冻结 envelope 内授权译文/术语正文；正式派发使用统一 builder 和三行 prompt，
  JSON 有效性、读取范围与 child 生命周期分别核验。更早细节见
  [历史交接](docs/handoff-history-through-20260919.md)，当前会话授权优先。
