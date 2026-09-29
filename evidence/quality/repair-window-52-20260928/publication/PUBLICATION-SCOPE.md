# 窗口52证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-52-20260928/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/6b75b260078d4a5d606542869f59a04240f16e70cfb732fdb05013734159bb44.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w52-20260928/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-52-20260928/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window52-20260928-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window52-20260928-migration.json` 逐字复制到上述 migration 目标。已验证 4 revision_changed（均为 workset，无 runtime-sync）、29824 unchanged、0 ambiguous/unmapped、4 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w52-20260928/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`（本窗口无 HOST-NOTE）；复制 `.artifacts/i18n/repair-window/window52-20260928-publish-chain.log`、`window52-20260928-publish-chain-timing.json`、`window52-20260928-migration.json`、`window52-20260928-migration-timing.json`，去掉 `window52-20260928-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：4 条宿主补充（队列耗尽、积压 0 时用户 2026-09-28 批准）：b5e754f6ab（Orcs lore 分类 sunwall observatory“太阳堡垒瞭望台”改“太阳堡垒观星台”：唯一文献为天文学家日志，区域名、任务、成就均作观星台）；5d156a408b（艾琳结局成就 Last Instant of Sanity 补回 your patron＝“太阳主上”与 in a searing flash）；同缺陷兄弟 1e5fe478f9（AOADS_BURN 成就 your patron Distant Sun＝“你的主上遥远的太阳”）与 d58b645c3b（夏·图尔结局叙述：succumbed to the fight 改“在这场搏斗中倒下”，补“太阳主上”）；涉及 mod-tome.lua、tome-orcs.lua；术语库 narrative.tsv 的 sunwall observatory 行改为“太阳堡垒观星台”并升 preferred（用户 2026-09-28 裁决）；无跨组件同键兄弟（check_siblings 0）。主游戏按 manifest 固定 engine commit 624a673 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Archmage 按用户同日裁决保留“元素法师”，范围外 8b977dd836 不在本窗口。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 4 条与术语 1 行 → REVIEW(0) r0a1（GPT-6 Sol）4/4 OK → FINAL(0) f0a2（Opus 5.5）4/4 OK，cycle 0 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `9362911053e2ff022f3ed7d7e80cab07459ed930`；新 catalog `538a4d20024882e2bf0908ca25a3185a0de5d60fa78eb92bff1f852aa55f0d13`；migration `6b75b260078d4a5d606542869f59a04240f16e70cfb732fdb05013734159bb44`。
   - 后续：4 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-29（修复窗口52已完成、待宿主证据提交与推送，下一步审核窗口52的 successor，第363批起）`。
   - 第一节以“- 修复窗口已闭合至 **51**”开头的那一整行改写为：`- 修复窗口已闭合至 **52**：Sunwall Observatory lore 分类名改观星台（术语同步升 preferred）与艾琳结局成就及两条同缺陷兄弟补回 your patron＝太阳主上，共 4 条（mod-tome.lua、tome-orcs.lua）已修复；译文提交 `9362911053e2ff022f3ed7d7e80cab07459ed930`；migration `6b75b260…` 的 4 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第363批（见第五节第 1 项）。`
   - 第五节第 1 项（以“1. 审核队列已耗尽”开头）：把该行开头到“若有新 successor 再审第 **363** 批”为止的文字替换为 `1. 继续审核第 **363** 批（窗口52的 4 个 successor`，紧随其后原有的“（默认 80 条，连续推进）”保留——即结果以 `1. 继续审核第 **363** 批（窗口52的 4 个 successor（默认 80 条，连续推进）；` 开头时请改为 `1. 继续审核第 **363** 批（窗口52的 4 个 successor；默认 80 条，连续推进）；`；并把该项中 `setup_window51.py`、`.artifacts/i18n/repair-w51-20260928/wd.sh`、`/tmp/w51-*.sh` 分别改为 `setup_window52.py`、`.artifacts/i18n/repair-w52-20260928/wd.sh`、`/tmp/w52-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 51 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w52-20260928/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后的“   窗口 52 积压 **0** 条”一行改为：`   窗口 53 积压 **0** 条（窗口52后重新计数，范围外项不计入）：范围外 `8b977dd836`（Archmage 保留“元素法师”已由用户裁决，仍 pending_repair，待按不改收口）；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第362批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w52-20260928/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-52-20260928/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
