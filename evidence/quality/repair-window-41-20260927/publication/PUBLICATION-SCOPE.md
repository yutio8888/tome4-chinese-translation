# 窗口41证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-41-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/db9e58d6af47f261dc6a92abc1745ba7cc563dbfb7d29c7bb82a850215e0f3ef.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w41-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-41-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window41-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window41-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 22 revision_changed（均为 workset，无 runtime-sync）、29806 unchanged、0 ambiguous/unmapped、22 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；复制 `.artifacts/i18n/repair-window/window41-20260927-publish-chain.log`、`window41-20260927-publish-chain-timing.json`、`window41-20260927-migration.json`、`window41-20260927-migration-timing.json`，去掉 `window41-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 328、329、330、331、332 共 22 条确认问题（328 批 2、329 批 3、330 批 7、331 批 5、332 批 5），均为 tome-orcs.lua，已全部修复；无宿主补充，无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Sunwall 全库译名不一登记待用户审阅第 37 项，本窗口不改。
   - 预检：开窗前宿主逐句预检 6 条长条目（ADJUDICATION-HOST-PRECHECK-C0，13 处追加修复点），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：
     - execute-01 修复 22 条 → REVIEW(0) r0a1 确认 2 条（64ff1dc48e 系统过载“大部分”技能、6ce8f3f6ef 科技法师加粗句）。
     - execute-02 → RE_REVIEW(1) r1a1 确认 7b2d6ea173 两处“克鲁克部族”→术语“克鲁克部落”。
     - execute-03 → RE_REVIEW(2) r2a1 22/22 OK → FINAL(2) f2a2 确认 6ce8f3f6ef“装入长袍后”与“当前蒸汽值”（源码 electricity.lua 奥术发电机 on_subtype=cloth、steam/other.lua getSpellpower 用 getSteam()）。
     - execute-04 → RE_REVIEW(3) r3a1 22/22 OK → FINAL(3) f3a2 22/22 OK，cycle 3 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `399a3ae5b406b3e59aa9ff39c39dd1ef203a4369`；新 catalog `c0406a5df9c4132ce21f0e9cf497aa4a4db6c99515cdf9d1241c3ec4d963a186`；migration `db9e58d6af47f261dc6a92abc1745ba7cc563dbfb7d29c7bb82a850215e0f3ef`。
   - 后续：22 个 successor 必须重新审核，不继承旧 done。待用户审阅第32–37项不变。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口41已完成、待宿主证据提交与推送，下一步审核第333批）`。
   - 第一节以“- 修复窗口已闭合至 **40**”开头的那一整行改写为：`- 修复窗口已闭合至 **41**：第 328–332 批共 22 条确认问题已修复（均为 tome-orcs.lua）；译文提交 `399a3ae5b406b3e59aa9ff39c39dd1ef203a4369`；migration `db9e58d6…` 的 22 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 42 积压 0 条，从审核333重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 41（模板 `setup_window40.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w40-20260927/wd.sh`、`/tmp/w40-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开窗口 42（模板 `setup_window41.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w41-20260927/wd.sh`、`/tmp/w41-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 40 已完成”开头的那一整行）为下面一整行（逐字）：
     2. 窗口 41 已完成（REVIEW、RE_REVIEW×3、FINAL×2；FINAL(2) 确认科技法师进阶句失真后 cycle 3 收敛；门禁 17/17）。窗口 42 积压 **0** 条（第333批起）：从审核333起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：“stack of herbs”同族四条“一束植物”→“草药”（advisory，跨条）；Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window41.py`、`.artifacts/i18n/repair-w41-20260927/wd.sh` 与 `/tmp/w41-*.sh`；开窗 setup 后先跑 `.artifacts/i18n/repair-w41-20260927/check_siblings.py <WORKSET>` 列跨组件同键兄弟并写 RUNTIME-SYNC（窗口 35、40 都因漏列在门禁 06 失败）；每轮复审 harvest/归档后须立即跑 `publish.py` 发布 stage 记录（窗口 39 漏跑、事后补发，见 HOST-NOTE-LATE-PUBLICATION.md）。
     紧随其后以“   第332批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   - 第五节第 4 项：只把“（当前 36 项；”改为“（当前 37 项；”，并在该项括号内“第 36 项 Gardanion 物品名未译”之后追加“；第 37 项 Sunwall 全库译名不一”。
   第五节第 3、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w41-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-41-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
