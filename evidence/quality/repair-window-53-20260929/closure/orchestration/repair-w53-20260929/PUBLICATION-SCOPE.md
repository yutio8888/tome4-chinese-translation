# 窗口53证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-53-20260929/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/7ed5bcec6d8c59a381f37e30588935e4f399e2eb8a738651d5a1b0b25c4033da.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w53-20260929/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-53-20260929/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window53-20260929-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window53-20260929-migration.json` 逐字复制到上述 migration 目标。已验证 19 revision_changed（18 workset＋1 runtime-sync `55872e196b`）、29809 unchanged、0 ambiguous/unmapped、19 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`RUNTIME-SYNC.json`、`HOST-NOTE-RUNTIME-SYNC.md`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w53-20260929/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`；复制 `.artifacts/i18n/repair-window/window53-20260929-publish-chain.log`、`window53-20260929-publish-chain-timing.json`、`window53-20260929-migration.json`、`window53-20260929-migration-timing.json`，去掉 `window53-20260929-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：审核队列耗尽后积压 18 条（第364批 4、第365批 5、第367批 3、第368批 6），用户 2026-09-29 选择立即开窗；主游戏 16 条（mod-tome.lua）、Orcs 2 条（tome-orcs.lua）；术语库 classes.tsv 的 Archmage 行升 preferred（用户 2026-09-28 裁决保留“元素法师”）；同键兄弟 1 条 runtime-sync（caldizar `55872e196b` 逐字节同步已复审的 `d64daff63a`）。主游戏按 manifest 固定 engine commit 624a673 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。范围外 8b977dd836（Archmage）仍 pending_repair，不在本窗口。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 18 条与术语 1 行 → REVIEW(0) r0a1（GPT-6 Sol）16 OK／2 确认（速射姿态按实现只需投石索、夏·图尔内乱句）→ execute-02 → RE_REVIEW(1) r1a1 17 OK／1 确认（噩梦诅咒“折磨”按实现反击来源者）→ execute-03 → RE_REVIEW(2) r2a1 18/18 → FINAL(2) f2a2（Opus 5.5）17 OK／1 确认（夏·图尔 lore 首段，宿主整条逐句另补 4 处）→ execute-04 → RE_REVIEW(3) r3a1 18/18 → FINAL(3) f3a2 18/18，cycle 3 收敛（max_cycles 5）→ execute-05 runtime-sync。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `359798c301d07abbccfa503ccd9c2b5657c3e725`；新 catalog `cd2d8f8880856795f5a4650efad202178c9b660a338bcd272c60bd158d073510`；migration `7ed5bcec6d8c59a381f37e30588935e4f399e2eb8a738651d5a1b0b25c4033da`。
   - 后续：19 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-29（修复窗口53已完成、待宿主证据提交与推送；按用户指示暂停，恢复后审核窗口53的 19 个 successor，第369批起）`。
   - 第一节以“- 修复窗口已闭合至 **52**”开头的那一整行改写为：`- 修复窗口已闭合至 **53**：审核364–368 确认的 18 条（mod-tome.lua 16、tome-orcs.lua 2）与 1 条同键 runtime-sync 已修复，classes.tsv 的 Archmage 行升 preferred；译文提交 `359798c301d07abbccfa503ccd9c2b5657c3e725`；migration `7ed5bcec…` 的 19 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第369批（见第五节第 1 项，当前按用户指示暂停）。`
   - 第五节第 1 项（第一行以“1. 继续审核第 **369** 批起（合并”开头）：把该行开头从“1. 继续审核第 **369** 批起（”到“默认 80 条，连续推进）”为止的整段替换为 `1. 按用户 2026-09-29 指示暂停；恢复后审核第 **369** 批起（窗口53的 19 个 successor；默认 80 条，连续推进）`，该行其后的文字保留；并在该项（含下一行）中把 `setup_window52.py`、`.artifacts/i18n/repair-w52-20260928/wd.sh`、`/tmp/w52-*.sh` 分别改为 `setup_window53.py`、`.artifacts/i18n/repair-w53-20260929/wd.sh`、`/tmp/w53-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 52 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w53-20260929/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   窗口 53 积压 **18** 条”开头的一行（其中批次清单有重复，是旧生成器缺陷）整行改为：`   窗口 54 积压 **0** 条（窗口53后重新计数，范围外项不计入）：范围外 `8b977dd836`（Archmage 保留“元素法师”已由用户裁决，仍 pending_repair，待按不改收口）；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第368批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w53-20260929/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-53-20260929/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
