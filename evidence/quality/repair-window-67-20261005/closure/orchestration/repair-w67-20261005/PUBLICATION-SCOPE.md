# 窗口67证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-67-20261005/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/a0f4f2206d3ff692ae44f032e55b69e282b42d9240718e6da31d6bfd5b1a3038.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json`（execute-01 所写）保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w67-20261005/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-67-20261005/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window67-20261005-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window67-20261005-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：revision_changed 2、unchanged 29826、queued_successors 2、ambiguous 0、unmapped 0。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json`、`NEW-TARGETS.json` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w67-20261005/` 的 `HOST-SUPPLEMENT-CLAIMS.json`、`rewrites.json`、`HOST-EXACT-DIFF.json` 与 `HOST-EXACT-DIFF-POST-FIX1.json`；
   - `.artifacts/i18n/repair-window/` 的 `window67-20261005-publish-chain.log`、`window67-20261005-publish-chain-timing.json`、`window67-20261005-migration.json`、`window67-20261005-migration-timing.json`，复制时去掉 `window67-20261005-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：2 条译文（mod-tome.lua 1、tome-cults.lua 1），无术语改动。
     - 宿主补充 `9d3fc01bdf`（不计积压）：Cults 奎科加章节（kroshkkur.lua:107，源文 records of Anglowen）“根据安格列文的记载”→“根据安格利文的记载”，按 terminology/places.tsv:20 Angolwen＝安格利文（preferred）；窗口66 REVIEW r0a1 确认诸神前言同名术语时发现。
     - 用户 2026-10-05 授权的 `fc55a88fd6`：mod-tome.lua:422 护送奖励日志“%s 技能 %s (+%d 等级)”→“%s技能 %s（+%d 级）”，与已改的同族选项（mod-tome.lua:425、tome-orcs.lua:582）一致；源码 EscortRewards.lua:537 → escort-quest.lua:36 → escort-duty.lua:64“作为奖励，你%s。”。
     - 新译文由宿主写定（`publication/NEW-TARGETS.json`），EXECUTOR 逐字替换；宿主核验 2 条 after 与 new_target 逐字相等（`publication/HOST-EXACT-DIFF.json`）。窗口内修复后宿主重新逐字核验 2 条：REVIEW r0a1 确认的奎科加章节 librarians 漏译（“记录者”→“图书管理员”）与宿主同条确认的 might be 被写成“其实是”（→“可能来自”），由 execute-02 修复，见 `publication/HOST-EXACT-DIFF-POST-FIX1.json`。`NEW-TARGETS.json` 是 execute-01 的冻结输入，保留该条初稿；终稿以 POST-FIX1 核验为准。
     - 主游戏按 manifest 固定 commit 624a673 核验；Cults 源码来源未固定，按公开源码核验并如实标注。四个 locale 文件中无同键兄弟；主游戏 `mod-tome/load.lua` 段另有该章旧版文本的副本（`e4824491182e`），运行时键不同且为已登记死键（`batch-ac27e658…` 中经 host-block 放行），不同步。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 → REVIEW r0a1（gpt-6.1-sol）1 OK／1 ISSUE，确认忠实性 1 条（奎科加章节 librarians 被译作“记录者”）＋宿主同条确认 1 条（might be 被写成“其实是”），execute-02 → RE_REVIEW r1a1 2/2 OK → FINAL f1a2（Opus 5.5）2/2 OK；第 1 轮收敛（max_cycles 5），无无效尝试。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `0de585f6fa87ef93761e4a85e168a70d06cebb30`；
     - 新 catalog `59f6d8272ff985ec3476131c03ce8ee38505a91bb284abf48813f71f09369913`；
     - migration `a0f4f2206d3ff692ae44f032e55b69e282b42d9240718e6da31d6bfd5b1a3038`。
   - 后续：
     - 2 个 successor 必须重新审核，不继承旧 done。
     - 下一个修复窗口（68）积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`：先核对当前 `handoff.md` 的 SHA-256 等于 `8446b04165a32e582ed3318a8c45e71cbacb1bab3014ddfc3b0e25430abc7255`，不等则停止并报告；相等则将其整体替换为宿主已存的 `.ai/task/repair-w67-20261005/HANDOFF-NEXT.md`（逐字复制，替换后 SHA-256 应为 `8b0dbe58fc70e6cb0ecfe632d54e4892e7ec367c8df886710fce8ba6e229d4d6`）。不要另作改动。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w67-20261005/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-67-20261005/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
