# 窗口54证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-54-20260929/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/f990cf25e98ce2a0759cf48eb673acb91324a1ecc8597632cb27d2cb0054e7a1.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w54-20260929/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-54-20260929/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window54-20260929-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window54-20260929-migration.json` 逐字复制到上述 migration 目标。已验证 2 revision_changed（均为 workset 条目）、29826 unchanged、0 ambiguous/unmapped、2 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w54-20260929/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`；复制 `.artifacts/i18n/repair-window/window54-20260929-publish-chain.log`、`window54-20260929-publish-chain-timing.json`、`window54-20260929-migration.json`、`window54-20260929-migration-timing.json`，去掉 `window54-20260929-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：审核队列耗尽后剩余 repair_required 2 条，用户 2026-09-29 选择先修工具（Claude Code 2.1.284 原生日志白名单）再开窗口54：第369批确认的 Orcs 远行传送门邮递信件 `5d4b280889`（tome-orcs.lua）与 batch-5e2173dbfb90012ff34d 确认的 `8b977dd836`（mod-tome.lua，元素法师职业说明）。`8b977dd836` 原指控（Archmagi→大法师）已被用户 2026-09-28 裁决驳回，职业名保留“元素法师”；宿主按固定 engine commit 624a673 复核出 “unique spell” 被译作“独特技能”（data/talents/misc/misc.lua 的 TELEPORT_ANGOLWEN 为 is_spell=true），改为“独特法术”。主游戏按 manifest 固定 engine commit 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。不改术语库；无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 2 条（信件第二段整段重译、独特技能→独特法术）→ REVIEW(0) r0a1（GPT-6 Sol）1 OK／1 确认（信件第三段 pack golem 与代词）→ execute-02 → RE_REVIEW(1) r1a1 1 OK／1 确认（信件第一段 undoing 与 let alone still carrying your backpacks）→ execute-03 → RE_REVIEW(2) r2a1 2/2 → FINAL(2) f2a2（Opus 5.5）2/2，cycle 2 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `23b32534d3088ae7625697c049c774a2c07a13e0`；新 catalog `ebe486ffb056ac2cca21fe0ab396d0360fac55fa7ba76bae549cac0f96fa1d57`；migration `f990cf25e98ce2a0759cf48eb673acb91324a1ecc8597632cb27d2cb0054e7a1`。
   - 后续：2 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-29（修复窗口54已完成、待宿主证据提交与推送；下一步审核窗口54的 2 个 successor，第370批）`。
   - 第一节以“- 修复窗口已闭合至 **53**”开头的那一整行改写为：`- 修复窗口已闭合至 **54**：第369批确认的 Orcs 信件 `5d4b280889` 与 `8b977dd836`（Archmage 职业说明，保留“元素法师”，只把“独特技能”改为“独特法术”）已修复；译文提交 `23b32534d3088ae7625697c049c774a2c07a13e0`；migration `f990cf25…` 的 2 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第370批（见第五节第 1 项）。`
   - 第五节第 1 项（第一行以“1. 继续审核第 **370** 批起（窗口53的 19 个 successor”开头）：只把该行中的“窗口53的 19 个 successor”改为“窗口54的 2 个 successor”，该行其余文字保留；并在该项下一行把 `setup_window53.py`、`.artifacts/i18n/repair-w53-20260929/wd.sh`、`/tmp/w53-*.sh` 分别改为 `setup_window54.py`、`.artifacts/i18n/repair-w54-20260929/wd.sh`、`/tmp/w54-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 53 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w54-20260929/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   窗口 54 积压 **1** 条”开头的一行整行改为：`   窗口 55 积压 **0** 条（窗口54后重新计数）：队列中已无 repair_required 条目；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第369批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w54-20260929/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-54-20260929/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
