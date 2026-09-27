# 窗口45证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-45-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/2866e76c1a7ebda59d6e5cfeab63713726a5a90aa25f6a6041d4f30c8409ab17.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w45-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-45-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window45-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window45-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 27 revision_changed（均为 workset，无 runtime-sync）、29801 unchanged、0 ambiguous/unmapped、27 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`HOST-NOTES.md`、`HOST-SUPPLEMENT-CLAIMS.json`（源在 `.artifacts/i18n/repair-w45-20260927/`）、全部 `ADJUDICATION-*.json`；复制 `.artifacts/i18n/repair-window/window45-20260927-publish-chain.log`、`window45-20260927-publish-chain-timing.json`、`window45-20260927-migration.json`、`window45-20260927-migration-timing.json`，去掉 `window45-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 349、350、351、352 共 24 条确认问题（349 批 2、350 批 9、351 批 7、352 批 6），加宿主补充 3 条（用户 2026-09-27 裁决的灵能蠕虫 tformat 裸 %；窗口 44 advisory 的毁灭号 beaded panel 两条），合计 27 条，均为 tome-orcs.lua，已全部修复；无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前宿主预检 6 个结构/运行时要点（ADJUDICATION-HOST-PRECHECK-C0：制表符、换行与灵能蠕虫 tformat 裸 %），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修复 27 条 → REVIEW(0) r0a1（GPT-6 Sol）2 条确认（Electricity 频率：第350批宿主 claim 误判“每隔一级”，按 craft_levelup 实为逐级；沉睡洞穴日志单数“我”）＋宿主自查 1 条（成就 Boss 名）→ execute-02（漏改 Boss 名）→ execute-03 补做 → RE_REVIEW(1) r1a1 1 条 advisory（Ureslak 音译，待审第 40 项）→ FINAL(1) f1a2 3 条确认（灵能蠕虫传播对象/豁免、毁灭号启动句、成就句内统一“乌瑞斯拉克”）→ execute-04 → RE_REVIEW(2) r2a1 1 条确认（a handful→几名）＋1 条 advisory（tinker）→ execute-05 → RE_REVIEW(3) r3a1 PASS → FINAL(3) f3a2 1 条（tinker，宿主判 advisory）→ RE_REVIEW(4) r4a1 同一条第三次被指出，宿主改判确认 → execute-06（“电子蒸汽工具”）→ RE_REVIEW(5) r5a1 PASS → FINAL(5) f5a2 27/27 OK，cycle 5 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `41dbeade832bbf97b88ad43dc8b3d9b6440bfd14`；新 catalog `d78ae4f3870aa9ce25dc60a1165755d58d7419c617b6859ad2a3018ca3ad4649`；migration `2866e76c1a7ebda59d6e5cfeab63713726a5a90aa25f6a6041d4f30c8409ab17`。
   - 后续：27 个 successor 必须重新审核，不继承旧 done。新增待审第 40 项（Ureslak 音译）与第 41 项（tinker 道具/蒸汽工具，同族另五条排入窗口 46 宿主补充）。strict lint 漏检非法 % 的修复在本窗口译文之后由宿主另行提交。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口45已完成、待宿主证据提交与推送，下一步宿主提交 lint 修复后审核第353批）`。
   - 第一节以“- 修复窗口已闭合至 **44**”开头的那一整行改写为：`- 修复窗口已闭合至 **45**：第 349–352 批 24 条确认问题与宿主补充 3 条已修复（均为 tome-orcs.lua）；译文提交 `41dbeade832bbf97b88ad43dc8b3d9b6440bfd14`；migration `2866e76c…` 的 27 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 46 积压 0 条，从审核353重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 45（模板 `setup_window44.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w44-20260927/wd.sh`、`/tmp/w44-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开窗口 46（模板 `setup_window45.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w45-20260927/wd.sh`、`/tmp/w45-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 44 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w45-20260927/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第352批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w45-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-45-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
