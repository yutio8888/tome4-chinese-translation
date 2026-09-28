# 窗口50证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-50-20260928/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/d98cee5629b82fc69dc51663d72e5a29c14090d6e960e4c113b109a17d70c476.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w50-20260928/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-50-20260928/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window50-20260928-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window50-20260928-migration.json` 逐字复制到上述 migration 目标。已验证 27 revision_changed（均为 workset，无 runtime-sync）、29801 unchanged、0 ambiguous/unmapped、27 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w50-20260928/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`以及 task 目录的 `HOST-NOTE-gate03-term-count.md`、`INVALID-F0A2.json`；复制 `.artifacts/i18n/repair-window/window50-20260928-publish-chain.log`、`window50-20260928-publish-chain-timing.json`、`window50-20260928-migration.json`、`window50-20260928-migration-timing.json`，去掉 `window50-20260928-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：窗口外宿主补充 27 条（队列耗尽、积压 0 时用户 2026-09-28 选择开窗），涉及 mod-tome.lua、tome-ashes-urhrok.lua、tome-cults.lua、tome-orcs.lua 与术语库 3 行（classes.tsv 改 Writhing One＝蠕动者并升 preferred；talents.tsv 新增 Writhing One＝蠕动者、Mind Drones＝精神无人机）。两项名称按用户纯名称授权咨询 Gemini 3.8 Flash 后采用：Writhing One＝蠕动者（职业、购买页、同名技能），Mind Drone(s)＝精神无人机（技能族 5 条）。一致性：stack of herbs 十条“一束草药”、Temporal Feast 技能名“时空盛宴”、Sher'tul 三条“夏·图尔”、entropic backlash 两条“熵能反冲”。忠实度：乌尔罗格 fearsome to behold 两条、禁忌之书描述、铜制护目镜附言。无跨组件同键兄弟（check_siblings 0）。不含：Archmage 8b977dd836（pending_repair）、Sunwall 观星台/瞭望台（待用户审第 37 项）、59339a8b7f（A.P.E. 缩写，漏纳入，留待后续）。主游戏按 manifest 固定 engine commit 624a673 核验；DLC 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 27 条与 3 行术语 → REVIEW(0) r0a1（GPT-6 Sol）27/27 OK → FINAL(0) f0a2（Opus 5.5）输出截断（4/27，末 key 残缺）判 INVALID（publication/INVALID-F0A2.json）→ f0a3 27/27 OK，cycle 0 收敛（max_cycles 5）。
   - advisory：a5ef7ca96f（Ashes 乌尔罗格）末句“他面对你的表情似乎并不惊讶”增译“表情”，不在点名分句内，未改。
   - 门禁：17/17 全过，含严格构建（首跑门禁 03 因新增 2 行术语需把静态审计行数 732→734，宿主已改，见 publication/HOST-NOTE-gate03-term-count.md）；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `a674a4b5d2666da9eb8bc63cc391af56b33d4c7e`；新 catalog `19d3fa4cc1b61cda24d1d9995d74d02a0458d32d7b6d180c18940c42b12e24fa`；migration `d98cee5629b82fc69dc51663d72e5a29c14090d6e960e4c113b109a17d70c476`。
   - 后续：27 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-28（修复窗口50已完成、待宿主证据提交与推送，下一步审核窗口50的 successor，第361批起）`。
   - 第一节以“- 修复窗口已闭合至 **49**”开头的那一整行改写为：`- 修复窗口已闭合至 **50**：窗口外宿主补充 27 条（Writhing One＝蠕动者、Mind Drone＝精神无人机两项名称裁决及一致性、忠实度修复；四个 Lua 文件＋术语库 3 行）已修复；译文提交 `a674a4b5d2666da9eb8bc63cc391af56b33d4c7e`；migration `d98cee56…` 的 27 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第361批（见第五节第 1 项）。`
   - 第五节第 1 项（以“1. 继续审核第 **361** 批”开头）只把其中 `setup_window49.py`、`.artifacts/i18n/repair-w49-20260928/wd.sh`、`/tmp/w49-*.sh` 分别改为 `setup_window50.py`、`.artifacts/i18n/repair-w50-20260928/wd.sh`、`/tmp/w50-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 49 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w50-20260928/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后的“   窗口 50 积压 **0** 条”一行改为：`   窗口 51 积压 **0** 条（窗口50后重新计数，范围外项不计入）：范围外 `8b977dd836`（Archmage 职业名“元素法师”，此前同类指控已驳回，仍 pending_repair，待下个窗口按 revision 核实）；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。`；再下一行以“   第360批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w50-20260928/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-50-20260928/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
