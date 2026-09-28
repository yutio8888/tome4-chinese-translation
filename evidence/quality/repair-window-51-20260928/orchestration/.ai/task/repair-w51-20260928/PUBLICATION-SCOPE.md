# 窗口51证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-51-20260928/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/687fcef22dcc96338d3b422e84269100c17f5f45ac2c8aa51b4152e18b6b56ab.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w51-20260928/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-51-20260928/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window51-20260928-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window51-20260928-migration.json` 逐字复制到上述 migration 目标。已验证 2 revision_changed（均为 workset，无 runtime-sync）、29826 unchanged、0 ambiguous/unmapped、2 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w51-20260928/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`（本窗口无 HOST-NOTE）；复制 `.artifacts/i18n/repair-window/window51-20260928-publish-chain.log`、`window51-20260928-publish-chain-timing.json`、`window51-20260928-migration.json`、`window51-20260928-migration-timing.json`，去掉 `window51-20260928-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：2 条宿主补充（队列耗尽、积压 1 时用户 2026-09-28 选择开窗）：20fa052d6c（第361批确认，成就 They Came Back For Eyal 漏 your patron、portal to 方向误译，改“开启通往你那疯狂的太阳主上的传送门”），59339a8b7f（窗口50漏纳入，科技法师进阶说明补回“（A.P.E.）”并去多余句号）；涉及 mod-tome.lua、tome-orcs.lua；术语库未改；无跨组件同键兄弟（check_siblings 0）。不含：Archmage 8b977dd836（pending_repair）、Sunwall 译名（待用户第 37 项）。主游戏按 manifest 固定 engine commit 624a673 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 2 条 → REVIEW(0) r0a1（GPT-6 Sol）2/2 OK → FINAL(0) f0a2（Opus 5.5）2/2 OK，cycle 0 收敛（max_cycles 5）。
   - advisory：相邻成就（mod-tome.lua:2775，以艾琳之手阻止 your mad patron sun 焚毁世界）同样漏 your patron，不在本 workset，留待后续窗口。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `c1f7bc5ef439c710db9b3e657f3ab91f14a17bb7`；新 catalog `52f38b69945e3eb37146095d6f30b01e607e91fe53a8f6c75e0cb895fbc6c9fe`；migration `687fcef22dcc96338d3b422e84269100c17f5f45ac2c8aa51b4152e18b6b56ab`。
   - 后续：2 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-28（修复窗口51已完成、待宿主证据提交与推送，下一步审核窗口51的 successor，第362批起）`。
   - 第一节以“- 修复窗口已闭合至 **50**”开头的那一整行改写为：`- 修复窗口已闭合至 **51**：第361批确认的成就 patron sun 与窗口50漏纳入的 A.P.E. 缩写共 2 条（mod-tome.lua、tome-orcs.lua）已修复；译文提交 `c1f7bc5ef439c710db9b3e657f3ab91f14a17bb7`；migration `687fcef2…` 的 2 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第362批（见第五节第 1 项）。`
   - 第五节第 1 项（以“1. 继续审核第 **362** 批”开头）只把其中 `setup_window50.py`、`.artifacts/i18n/repair-w50-20260928/wd.sh`、`/tmp/w50-*.sh` 分别改为 `setup_window51.py`、`.artifacts/i18n/repair-w51-20260928/wd.sh`、`/tmp/w51-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 50 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w51-20260928/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后的“   窗口 51 积压 **1** 条”一行改为：`   窗口 52 积压 **0** 条（窗口51后重新计数，范围外项不计入）：范围外 `8b977dd836`（Archmage 职业名“元素法师”，此前同类指控已驳回，仍 pending_repair，待下个窗口按 revision 核实）；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第361批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w51-20260928/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-51-20260928/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
