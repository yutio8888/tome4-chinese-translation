# 翻译审核当前交接

更新时间：2026-09-22（审核 246 与流程维护已完成并推送；修复窗口 3 待出版收尾）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前授权与实测状态

用户已恢复连续审核并授权调整流程/prompt后继续；连续审核和每批 push 的授权持续有效，
不逐批询问。审核 246 与流程维护已经完成、验收并推送。修复窗口 3 的 14 条译文已提交，
第一次 queue rebuild、单次 catalog build 和 migration-chain 已完成；当前只待宿主完成证据提交、
第二次 queue rebuild、push 与远端复核，完成后继续审核 247（默认 80 条）。

- 当前实际 `HEAD`：`254ad2b418e2660a1dd5c967889691c24925e6cb`
  （`fix(i18n): repair fourteen translations from batches 244-246`）。
- 当前实际远端 `origin/develop`：
  `9fb5ec1df3c74e09fd981bb7d16300d6bce25ef9`。窗口 3 尚未 push，不得提前宣称完成。
- SQLite meta 实测 `evidence_head=254ad2b418e2660a1dd5c967889691c24925e6cb`，
  `catalog_id=75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`；
  这是第一次同步和 migration apply 后状态。证据提交推进 HEAD 后必须再 rebuild 一次。
- 当前工作树包含本窗口待提交的受跟踪 evidence/catalog/migration/handoff 改动，也保留
  `.ai/consult/`、`recipe` 和旧 source-workset 等用户无关未跟踪文件；不得清理、暂存或改写这些无关文件。

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
  完整边界、哈希、真实计时和待办见
  [窗口 3 出版证据](evidence/quality/repair-window-3-20260922/summary.md)。

本窗口只修正获准 target，没有术语库修改、全局改名或跨批策略变更。固定 tome/engine 源码为
`624a67329fe2ad440c5b344785a9c73fcf22ae63`，244—246 无 DLC。距离单位“码”的跨批统一、
“不死亡灵”、generic spellcrit 空格及其他 advisory 均未借机扩大范围。

## 下一步

1. 复核待提交 diff 只含本窗口允许路径，提交 evidence/catalog/migration/handoff；不得纳入
   `.ai/consult/`、`recipe` 或旧无关 source-workset。
2. 提交推进 HEAD 后运行第二次 `python3 -B tools/i18n production queue rebuild`，核对
   SQLite `meta.evidence_head` 与新 HEAD、catalog ID 和无活动 checkpoint。
3. push `develop`，再实测远端与本地 HEAD 一致。以上步骤未完成前不得宣称窗口 3 已出版。
4. 开始审核 247，默认 80 条，按完整正式批次流程执行并每批 push，不逐批询问。

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
