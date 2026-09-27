# 窗口44证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-44-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/50e8f36cb7bd8eba7ee5a8258569e832c972d6f0de3f99e98dd962ea006359a0.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w44-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-44-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window44-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window44-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 24 revision_changed（均为 workset，无 runtime-sync）、29804 unchanged、0 ambiguous/unmapped、24 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`HOST-NOTES.md`、全部 `ADJUDICATION-*.json`；复制 `.artifacts/i18n/repair-window/window44-20260927-publish-chain.log`、`window44-20260927-publish-chain-timing.json`、`window44-20260927-migration.json`、`window44-20260927-migration-timing.json`，去掉 `window44-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 343、344、345、346、347、348 共 24 条确认问题（343 批 2、344 批 7、345 批 3、346 批 1、347 批 6、348 批 5），均为 tome-orcs.lua，已全部修复；无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前宿主预检 12 个结构/运行时要点（ADJUDICATION-HOST-PRECHECK-C0：换行、制表符、markup 与寒冰之怒 tformat 裸 %），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修复 24 条 → REVIEW(0) r0a1（GPT-6 Sol）PASS → FINAL(0) f0a2（Opus 5.5）3 条确认（卡托尔告示商品名、部落史 squeamish、帕默广播 grunts/slashing）→ execute-02 → RE_REVIEW(1) r1a1 1 条 advisory（珍珠面板，与第 37 行同物一并转窗口 45）→ FINAL(1) f1a2 2 条确认（血液灵晶“两倍”被删、选举告示 rarely）＋1 条 advisory（Chief Councilor 保持“议长”）→ execute-03 → RE_REVIEW(2) r2a1 2 条确认（修复者日志“童年”宾语、太阳堡垒书信原谅对象）→ execute-04 → RE_REVIEW(3) r3a1 1 条 advisory（闪电球 bolt/ball，待审第 33 项）→ FINAL(3) f3a2 24/24 OK，cycle 3 收敛（max_cycles 5）。
   - 重启：窗口在 ADJUDICATE cycle 1 因本机重启暂停，暂停前全部 child 已归档确认；恢复后续跑，无 child 跨越重启。
   - 门禁：首轮 04-quality-facts-unit-tests 因环境变化失败（重启后 PATH 新增 /opt/agents/bin 包装器遮蔽真实 pi，详见 publication/HOST-NOTES.md），去掉该目录后完整重跑 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `16eadd082289e2cf1aef22fb8a9a32d3612175e0`；新 catalog `8a407b557a4a3924bc894e92a8a52148bbf2305bcb3c66951e2701b6672fa271`；migration `50e8f36cb7bd8eba7ee5a8258569e832c972d6f0de3f99e98dd962ea006359a0`。
   - 后续：24 个 successor 必须重新审核，不继承旧 done。窗口 45 预定并入 Psy Worm 裸 %、lint 漏检修复与 Destructicus 面板两条。待用户审阅项不变。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口44已完成、待宿主证据提交与推送，下一步审核第349批）`。
   - 第一节以“- 修复窗口已闭合至 **43**”开头的那一整行改写为：`- 修复窗口已闭合至 **44**：第 343–348 批共 24 条确认问题已修复（均为 tome-orcs.lua）；译文提交 `16eadd082289e2cf1aef22fb8a9a32d3612175e0`；migration `50e8f36c…` 的 24 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 45 积压 0 条，从审核349重新累计（另有窗口 45 预定并入项与窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 44（模板 `setup_window43.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w43-20260927/wd.sh`、`/tmp/w43-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开窗口 45（模板 `setup_window44.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w44-20260927/wd.sh`、`/tmp/w44-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 43 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w44-20260927/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第348批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w44-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-44-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
