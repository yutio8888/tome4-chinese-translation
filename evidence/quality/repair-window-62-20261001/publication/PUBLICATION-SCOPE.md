# 窗口62证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-62-20261001/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/67a73acfc5b796718ea8628dc6cdc6781f7388488e2959930023d868090404ec.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中如已有 `IMPLEMENTATION.md` 与 `VALIDATION.json`，保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w62-20261001/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-62-20261001/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window62-20261001-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window62-20261001-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：53 revision_changed（均为 workset 条目）、29775 unchanged、0 ambiguous／0 unmapped、53 successor 新队列。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w62-20261001/` 的 `HOST-SUPPLEMENT-CLAIMS.json`、`rewrites.json`、`HOST-EXACT-DIFF.json`、`HOST-EXACT-DIFF-POST-FIX1.json` 与 `HOST-EXACT-DIFF-POST-FIX2.json`；
   - `.artifacts/i18n/repair-window/` 的 `window62-20261001-publish-chain.log`、`window62-20261001-publish-chain-timing.json`、`window62-20261001-migration.json`、`window62-20261001-migration-timing.json`，复制时去掉 `window62-20261001-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：53 条译文（mod-tome.lua 44、tome-cults.lua 5、tome-ashes-urhrok.lua 3、tome-orcs.lua 1），无术语改动。
     - 用户 2026-10-01 裁决 pending #50 B：其余 50 条 killer_message 改为以凶手为主语的主动分句（“并将其…”；Wrathroot、Norgos、Tannen 三条按语义写作“并让树人们将其化为养分”“并任由群狼分食其尸”“并使其从此下落不明、杳无音讯”）。
     - 用户 2026-10-01 裁决 pending #51 B：dreadfell dark Master 2 条→“黑暗领主”（`df8aa7a487`、`b662213a98`）。
     - 窗口61 FINAL advisory carry_forward：Ashes 苦痛链接效果说明 `5dc5712a74`→“当目标受伤害时，另一名受害者也会承受 %d%% 的伤害。”
     - 逐条改写与依据见 publication/`rewrites.json` 与 `SOURCE-CLAIMS.json`。Cults `0071abb36c` 同串为死键，未改。
     - 主游戏按 manifest 固定 commit 624a673 核验；Ashes／Cults／Orcs 公开源码来源未固定。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json；REVIEW/RE 用 GPT-6.1 Sol，FINAL 用 Opus 5.5）：
     - execute-01 → REVIEW(0) r0a1 2 ISSUE 均确认：苦痛链接漏译 an other（“另一名受害者”）、Murgol 的 flushed out to sea（“冲进了大海”）；
     - execute-02 → RE_REVIEW(1) r1a1 53 OK → FINAL(1) f1a2 1 确认：Tannen 一条以全角逗号起头，而 PartyDeath.lua:94 以 `" "..src.killer_message` 拼接，渲染为“坦能 ，”；
     - execute-03 → RE_REVIEW(2) r2a1 53 OK → FINAL(2) f2a2 53/53，cycle 2 收敛（max_cycles 5）。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `1f4395f69e5d8bbe0fc328e9cb7db1da2148f022`；
     - 新 catalog `8051f4edc57ac47c811ee73dc5cf1ec51044df25e2ee5db991fbf3e111b12027`；
     - migration `67a73acfc5b796718ea8628dc6cdc6781f7388488e2959930023d868090404ec`。
   - 后续：
     - 53 个 successor 必须重新审核，不继承旧 done；连同窗口61 的 22 个。
     - 窗口63 积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行：改为 `更新时间：2026-10-01（修复窗口62已完成、待宿主证据提交与推送；下一步审核窗口61、62 的 successor）`。
   - 第一节以“- 修复窗口已闭合至 **61**”开头的单行条目：整体替换为一行 `- 修复窗口已闭合至 **62**：窗口61（译文 `276e8b2d`）与窗口62（pending #50 B killer_message 凶手主语 50 条＋#51 B 黑暗领主 2 条＋苦痛链接 1 条，译文 `1f4395f6`，migration `67a73acf…`）均已修复；两窗共 75 个 successor 须重新审核，不继承旧 revision 的 done 状态。`
   - 第一节以“- 2026-10-01：审核队列清空后，用户要求系统性分析死亡信息表”开头的那一行：在行尾追加 `窗口62 已于同日完成并推送。`，其余文字不变。
   - 第三节第 1 项第一行中，从 `下一步开修复窗口62` 起到 `推送后审核窗口61、62 的 successor。` 止的子串：替换为 `下一步审核窗口61、62 的 successor（共 75 个，审核队列重建后可见）。`；该行其余文字与该项续行保留。
   - 第三节第 2 项：从以“2. 窗口 61 已完成”开头的行起，到以“   窗口 62 积压 **约 55** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w62-20261001/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第380批计时（实测”开头的一行必须原样保留。

   第三节第 3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w62-20261001/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-62-20261001/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
