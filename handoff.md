# 翻译审核当前交接

更新时间：2026-09-22（修复窗口3已推送；审核247已验收并finalize，下一批248）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前授权与实测状态

用户持续授权连续审核和每批 push；按既定三批审核后汇总修复的窗口推进，不逐批询问。
修复窗口 3 已完成证据提交、第二次队列同步与 push，远端核验为
`081d3a03ccaea62b735c05f0b10f44f4f892cba2`，不得重做。审核 247 已提交并 finalize，
本交接记录的是其出版收尾前快照；宿主随后将提交本交接、同步队列和推送。
恢复时先核对当前 HEAD、远端和 SQLite，不因历史步骤文字重复已完成操作。

- 审核 247 证据提交：`70a0f96223d1596806ebafc37cca645fb06caea0`。
- 当前 catalog：`75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`。
- 审核 247 的 finalize 收据见 [FINALIZE-RECEIPT](evidence/quality/production-batches/batch-fe19bbe5e5898a0c3547-host-evidence/FINALIZE-RECEIPT.json)。
- 当前没有活动审核 child；原有 `.ai/consult/`、`recipe` 和 15 个旧 source-workset
  均保留，严禁将其纳入本任务提交或清理。

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

## 下一步

1. 宿主完成本交接与 finalize 收据的独立提交后，同步队列、push 并核实远端；恢复时以实际状态为准。
2. 无活动 checkpoint 且 HEAD/queue 一致后，继续审核 **248**，默认 80 条，再审核249。
3. 247—249 全部完成后，汇总修复窗口4的已确认候选，按正式修复、复审、门禁、catalog/migration、
   两次队列同步与推送流程执行。不得把 advisory 或范围外 pending 计入修复。

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
