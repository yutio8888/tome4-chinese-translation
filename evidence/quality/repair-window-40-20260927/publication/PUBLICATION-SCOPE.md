# 窗口40证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-40-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/5b6b372f3fa4e03b2c7fb46ffacfa62fd1e3a1b98ee4272fa7875084ae5a6d3e.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w40-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-40-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window40-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window40-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 25 revision_changed（23 workset + 2 runtime-sync）、29803 unchanged、0 ambiguous/unmapped、25 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`RUNTIME-SYNC.json`、`HOST-NOTE-RUNTIME-SYNC.md`、全部 `ADJUDICATION-*.json`、`INVALID-R1A1.json`、`INVALID-F4A2.json`；复制 `.artifacts/i18n/repair-window/window40-20260927-publish-chain.log`、`window40-20260927-publish-chain-timing.json`、`window40-20260927-migration.json`、`window40-20260927-migration-timing.json`，去掉 `window40-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 324、325、326、327 共 21 条确认问题加第324批 2 条宿主补充（4e560f2e5a 蒸汽采石场、50df66a4c3 苏克商店全名），合计 23 条 workset 已修（均为 tome-orcs.lua）；另因门禁 06 跨组件同键，把 mod-tome.lua 中同名商店 2 条经 runtime-sync（RUNTIME-SYNC.json、HOST-NOTE-RUNTIME-SYNC.md）同步为已复审文本。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定；主游戏按 t-engine4 624a67329fe2ad440c5b344785a9c73fcf22ae63。Gardanion 物品名需新造音译，未入窗，登记待用户审阅第 36 项。
   - 预检：开窗前宿主逐句预检 6 条长条目（ADJUDICATION-HOST-PRECHECK-C0，10 处追加修复点），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：
     - execute-01 修复 23 条 → REVIEW(0) r0a1 确认 3 条（4e560f2e5a 全局速度、5362d5e743 提出协议条件、619199a9ea 人际相处）。
     - execute-02 → RE_REVIEW(1)（r1a1 revision_key 回显错误拒收，r1a2 确认 5d8d908f72 残暴行径；宿主另据源码确认 52bc32cb74 蒸汽枪掌握／等级）→ execute-03 → RE_REVIEW(2) 收敛 → FINAL(2) f2a2 确认 4e560f2e5a pinaciphobia→清单恐惧症。
     - execute-04 → RE_REVIEW(3) 确认 5bb911ddb9 蜘蛛机器人只判定一次冻结（驳回 58c3e2bf11 弹药措辞）→ execute-05 → RE_REVIEW(4) 收敛（再次驳回 58c3e2bf11）→ FINAL(4)（f4a2 截断拒收，f4a3 23/23 OK）。
     - 门禁首跑 06-runtime-collision-scan 报 Sook 店名跨组件冲突 → execute-06 runtime-sync mod-tome.lua 2 条 → 重跑 17/17。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `acae1e6d74fec03894d7e50ce531625da3b215c9`；新 catalog `a1da5518961a538373c3b21cdca9ee57055372a5da9b5580549e9e85b1e838c5`；migration `5b6b372f3fa4e03b2c7fb46ffacfa62fd1e3a1b98ee4272fa7875084ae5a6d3e`。
   - 后续：25 个 successor 必须重新审核，不继承旧 done。待用户审阅第32–36项不变（第35项 Awesome Toss、第36项 Gardanion 为本轮新增）。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口40已完成、待宿主证据提交与推送，下一步审核第328批）`。
   - 第一节以“- 修复窗口已闭合至 **39**”开头的那一整行改写为：`- 修复窗口已闭合至 **40**：第 324–327 批共 21 条确认问题及 2 条宿主补充已修复（另 runtime-sync mod-tome.lua 2 条 Sook 店名）；译文提交 `acae1e6d74fec03894d7e50ce531625da3b215c9`；migration `5b6b372f…` 的 25 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 41 积压 0 条，从审核328重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 40（模板 `setup_window39.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w39-20260926/wd.sh`、`/tmp/w39-*.sh`）。”改为“修复积压达 20 再开窗口 41（模板 `setup_window40.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w40-20260927/wd.sh`、`/tmp/w40-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 39 已完成”开头的那一整行）为下面一整行（逐字）：
     2. 窗口 40 已完成（REVIEW、RE_REVIEW×4、FINAL×2〔r1a1 revision_key 回显错误拒收；f4a2 输出截断拒收〕；cycle 4 收敛；门禁 06 首跑因 Sook 店名跨组件同键失败，runtime-sync mod-tome.lua 2 条后 17/17）。窗口 41 积压 **0** 条（第328批起）：从审核328起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：“stack of herbs”同族四条“一束植物”→“草药”（advisory，跨条）；Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window40.py`、`.artifacts/i18n/repair-w40-20260927/wd.sh` 与 `/tmp/w40-*.sh`；开窗 setup 后先跑 `.artifacts/i18n/repair-w40-20260927/check_siblings.py <WORKSET>` 列跨组件同键兄弟并写 RUNTIME-SYNC（窗口 35、40 都因漏列在门禁 06 失败）；每轮复审 harvest/归档后须立即跑 `publish.py` 发布 stage 记录（窗口 39 漏跑、事后补发，见 HOST-NOTE-LATE-PUBLICATION.md）。
     紧随其后以“   第327批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   - 第五节第 4 项：只把“（当前 35 项；”改为“（当前 36 项；”，并在该项括号内“第 35 项 Awesome Toss 致命翻转”之后追加“；第 36 项 Gardanion 物品名未译”。
   第五节第 3、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w40-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-40-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
