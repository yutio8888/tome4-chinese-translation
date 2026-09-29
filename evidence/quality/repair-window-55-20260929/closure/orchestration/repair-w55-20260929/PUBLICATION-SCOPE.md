# 窗口55证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-55-20260929/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/9035e3de23f2851fbbce54f87c03197884b02bbfdb752a7f01043f05244a3935.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w55-20260929/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-55-20260929/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window55-20260929-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window55-20260929-migration.json` 逐字复制到上述 migration 目标。已验证 7 revision_changed（均为 workset 条目）、29821 unchanged、0 ambiguous/unmapped、7 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w55-20260929/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`；复制 `.artifacts/i18n/repair-window/window55-20260929-publish-chain.log`、`window55-20260929-publish-chain-timing.json`、`window55-20260929-migration.json`、`window55-20260929-migration-timing.json`，去掉 `window55-20260929-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：审核队列耗尽后（第370批后 queued=0、repair_required=0），用户 2026-09-29 集中审阅 `evidence/quality/pending-user-review.md` 第45、46项并裁决（记录提交 2928cfc6）：死亡描述词族只修病句 2 条（burnt→被烧焦、cosmeticed→被‘美化’）与错义 3 条（mauled、timewarped→被时间扭曲、psyched→被心灵摧毁），约 14 条诙谐加工保留；高等人类之绽放效果描述（`e923d2b8d0`）与技能 info（`546a6e96d9`）的“能量”改“资源”。全部 7 条在 mod-tome.lua，按 manifest 固定 engine commit 624a673 核验。不改术语库；无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 7 条 → REVIEW(0) r0a1（GPT-6 Sol）6 OK／1 确认（mauled“被撕咬致残”限定咬伤且“致残”与模板“而死”冲突，宿主在裁决范围内改“被撕碎”）→ execute-02 → RE_REVIEW(1) r1a1 6 OK／1 确认（info 行结构与源文 races.lua:155-157 不符，宿主 setup 误按旧译保留；措辞不变按源文重排）→ execute-03 → RE_REVIEW(2) r2a1 7/7 → FINAL(2) f2a2（Opus 5.5）7/7，cycle 2 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `7211f717a1a5090eb731b698880be14891c30c8b`；新 catalog `12eb193599a4221c02a6c9b4a652645600e0e37b3276bda99af6a7534aab3e84`；migration `9035e3de23f2851fbbce54f87c03197884b02bbfdb752a7f01043f05244a3935`。
   - 后续：7 个 successor 必须重新审核，不继承旧 done。同表 `922c0f9665`（cleaved＝被裂颅，诙谐加工按裁决保留）仍为 blocked，工具无不改收口路径。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-29（修复窗口55已完成、待宿主证据提交与推送；下一步审核窗口55的 7 个 successor，第371批）`。
   - 第一节以“- 修复窗口已闭合至 **54**”开头的那一整行改写为：`- 修复窗口已闭合至 **55**：用户 2026-09-29 集中审阅裁决的 7 条（死亡描述病句／错义 5 条、高等人类之绽放“能量”→“资源”2 条）已修复；译文提交 `7211f717a1a5090eb731b698880be14891c30c8b`；migration `9035e3de…` 的 7 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第371批（见第五节第 1 项）。`
   - 第五节第 1 项（第一行以“1. 继续审核第 **371** 批起（窗口54的 2 个 successor”开头）：只把该行中的“窗口54的 2 个 successor”改为“窗口55的 7 个 successor”，该行其余文字保留；并在该项下一行把 `setup_window54.py`、`.artifacts/i18n/repair-w54-20260929/wd.sh`、`/tmp/w54-*.sh` 分别改为 `setup_window55.py`、`.artifacts/i18n/repair-w55-20260929/wd.sh`、`/tmp/w55-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 54 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w55-20260929/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   窗口 55 积压 **0** 条”开头的一行整行改为：`   窗口 56 积压 **0** 条（窗口55后重新计数）：队列中已无 repair_required 条目；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第370批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w55-20260929/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-55-20260929/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
