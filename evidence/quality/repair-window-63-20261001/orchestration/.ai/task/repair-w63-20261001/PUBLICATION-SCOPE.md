# 窗口63证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-63-20261001/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/f0e5ef721375a80abb44981c8cc204332302b26cef449626f81eb8022cddc8ee.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中如已有 `IMPLEMENTATION.md` 与 `VALIDATION.json`，保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w63-20261001/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-63-20261001/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window63-20261001-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window63-20261001-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：1 revision_changed（为 workset 条目）、29827 unchanged、0 ambiguous／0 unmapped、1 successor 新队列。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w63-20261001/` 的 `HOST-SUPPLEMENT-CLAIMS.json` 与 `HOST-EXACT-DIFF.json`；
   - `.artifacts/i18n/repair-window/` 的 `window63-20261001-publish-chain.log`、`window63-20261001-publish-chain-timing.json`、`window63-20261001-migration.json`、`window63-20261001-migration-timing.json`，复制时去掉 `window63-20261001-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：1 条译文（mod-tome.lua），无术语改动。
     - 第381批 `batch-4584eb6ddb5e3110acab` 确认：意志之力（Strength of Purpose）`6bba1ea093` 把 maces 译作“权杖”（sceptre）；按其覆盖的武器掌握同句式改为“狼牙棒”，并按整句对照把第一行改为“当使用剑、斧、狼牙棒、匕首或者弓箭时，增加 %d%% 武器伤害和 30 点物理强度。”。
     - 用户 2026-10-01 在审核队列清空后批准以 1 条积压开窗（未达 20 条阈值）。
     - 主游戏按 manifest 固定 commit 624a673 核验（game/modules/tome/data/talents/chronomancy/guardian.lua:33）。无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）1 OK → FINAL(0) f0a2（Opus 5.5）1/1，cycle 0 收敛（max_cycles 5）。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `7a7d8653fddf9e6d5928d307b96635cef48d6913`；
     - 新 catalog `d33f8ddd7a549757946beed25f832e2b945b12d26868df9b3acbd13a5a207c50`；
     - migration `f0e5ef721375a80abb44981c8cc204332302b26cef449626f81eb8022cddc8ee`。
   - 后续：
     - 1 个 successor 必须重新审核，不继承旧 done。
     - 窗口64积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行：改为 `更新时间：2026-10-01（修复窗口63已完成、待宿主证据提交与推送；下一步审核窗口63 的 successor 并发布 addon 0.3.1）`。
   - 第一节以“- 修复窗口已闭合至 **62**”开头的单行条目：整体替换为一行 `- 修复窗口已闭合至 **63**：窗口62（译文 `1f4395f6`）与窗口63（第381批确认的意志之力 maces“权杖”→“狼牙棒” 1 条，译文 `7a7d8653`，migration `f0e5ef72…`）均已修复；窗口63 的 1 个 successor 须重新审核，不继承旧 revision 的 done 状态（窗口61、62 的 successor 已于第381批审完）。`
   - 第三节第 1 项第一行中，从 `下一步待用户决定：以现有积压开修复窗口63，或暂停。` 起止于该句号的子串：替换为 `用户 2026-10-01 批准以该 1 条开修复窗口63（已完成）；下一步审核窗口63 的 1 个 successor。`；该行其余文字保留。
   - 第三节第 2 项：从以“2. 窗口 62 已完成”开头的行起，到以“   窗口 63 积压 **1** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w63-20261001/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第381批计时（实测”开头的一行必须原样保留。

   第三节第 3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w63-20261001/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-63-20261001/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
