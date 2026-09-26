# 窗口36证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-36-20260926/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、如候选含有则 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/990fc0dd6fb331b5744ae5ccba7d972b033c93042199e6d8d009365e3c9c6bcc.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w36-20260926/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-36-20260926/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window36-20260926-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `window36-20260926-migration.json` 逐字复制到上述 migration 目标。已验证 21 revision_changed、29807 unchanged、0 ambiguous/unmapped、21 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`、全部 `HOST-NOTE-*.md`、`HOST-EXECUTOR-AUDIT-execute-01.json`、`INVALID-R4A1.json`；复制 `.artifacts/i18n/repair-window/window36-20260926-publish-chain.log`、`window36-20260926-publish-chain-timing.json`、`window36-20260926-migration.json`、`window36-20260926-migration-timing.json`，去掉 `window36-20260926-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 306、307、308、309 共 21 条确认问题已修（全在 tome-cults.lua；全仓库同 source 检查无跨组件同键）。Cults 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前两个只读助手逐段比对 4 条最长的菲·维莉欧斯条目（ea6c288d、e6802878、f4db7369、df6ed2f1），宿主逐字核验引文 29/29 后并入修复（ADJUDICATION-HOST-PRECHECK-C0）。
   - 首次 EXECUTOR：execute-01 的 Codex 会话发生上下文压缩（原生日志含 compacted 记录），lifecycle 原生 parser 拒收；按窗口27先例 output_valid=null，task_complete 末条消息逐字留存，成果由宿主精确 diff（恰 21 条 target）独立核验（HOST-EXECUTOR-AUDIT-execute-01）。
   - 复审路径：
     - REVIEW(0) r0a1 确认 2 条：禁忌之书状态“身处书中”；岩谷手记“会是个错误／我们所有人深感痛心”；宿主另补背叛预言重复的持续时间。
     - execute-02 → RE_REVIEW(1) r1a1 确认 1 条：crag 译“岩谷”而非“岩壁”；Void Skitterer 名与熵反冲范围 refuted（本库名；贴合实现）。
     - execute-03 → RE_REVIEW(2) r2a1 确认 2 条：市场骚乱警卫到场顺序；幼龙“皮肤之下”裹着怪物肉团。
     - execute-04 → RE_REVIEW(3) r3a1 确认 1 条：熵教徒解锁文本 entropic backlash 统一为“熵能反冲”。
     - execute-05 → RE_REVIEW(4) r4a1 因 identity 回显少一字符被契约拒收（INVALID-R4A1），重派 r4a2 仅重复已 refuted 的 Void Skitterer 主张，收敛 → FINAL(4) f4a3 21/21 OK。
   - 边界：r4a2 reviewer 通过 Paseo 终端执行只读命令，宿主逐条核对 18 次按键均为只读并在收取后关闭遗留终端。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `a2c6c9797cfaec6ddd116935bae921a85448599d`；新 catalog `f0fbe9c67db4794be2c0d6dc6c63bd8e8fee48db4555eafec7a6b677c3c9ce06`；migration `990fc0dd6fb331b5744ae5ccba7d972b033c93042199e6d8d009365e3c9c6bcc`。
   - 后续：21 个 successor 必须重新审核，不继承旧 done。窗口外宿主补充项留给下一窗口：f6030742 导师文物 Sher'Tul“夏图尔”→“夏·图尔”（基线既有；本窗口 SPEC 专名表误写，见 HOST-NOTE-SPEC-ERRATUM）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10` misery→“困难”；`a5a712dc` Writhing One 技能名。原“第1557行马基埃亚尔”已随 ea6c288d 修复。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-26（修复窗口36已完成、待宿主证据提交与推送，下一步审核第310批）`。
   - 第一节以“- 修复窗口已闭合至 **35**”开头的那一整行改写为：`- 修复窗口已闭合至 **36**：第 306–309 批共 21 条确认问题已修复；译文提交 `a2c6c9797cfaec6ddd116935bae921a85448599d`；migration `990fc0dd…` 的 21 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 37 积压 0 条，从审核310重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项：只把“修复积压达 20 再开窗口 36（模板 `setup_window35.py`、`.artifacts/i18n/repair-w35-20260926/wd.sh`、`/tmp/w35-*.sh`）。”改为“修复积压达 20 再开窗口 37（模板 `setup_window36.py`、`.artifacts/i18n/repair-w36-20260926/wd.sh`、`/tmp/w36-*.sh`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 35 已完成”开头的那一整行）为：“2. 窗口 36 已完成（REVIEW、RE_REVIEW×4〔cycle 4 首次尝试因 identity 回显错误拒收后重派〕、FINAL×1；17/17）。窗口 37 积压 **0** 条（第310批起）：从审核310起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；Codex executor 会话压缩时按窗口27先例宿主 diff 核验；窗口模板为 `setup_window36.py`、`.artifacts/i18n/repair-w36-20260926/wd.sh` 与 `/tmp/w36-*.sh`。”。紧随其后以“   第309批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w36-20260926/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-36-20260926/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
