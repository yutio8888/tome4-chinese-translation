# 窗口57证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-57-20260930/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/f312e80bbb644d441ac98b8c7e91a992d92ec7c25f48557d6d79571d7a7a8882.json`。不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w57-20260930/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-57-20260930/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window57-20260930-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window57-20260930-migration.json` 逐字复制到上述 migration 目标。已验证 87 revision_changed（均为 workset 条目）、29741 unchanged、0 ambiguous/unmapped、87 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`、`INVALID-R2A1.json` 与 `HOST-NOTE-FINAL-ATTEMPT-RENUMBER.md`；从 `.artifacts/i18n/repair-w57-20260930/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json` 与 `HOST-EXACT-DIFF.json`；复制 `.artifacts/i18n/repair-window/window57-20260930-publish-chain.log`、`window57-20260930-publish-chain-timing.json`、`window57-20260930-migration.json`、`window57-20260930-migration-timing.json`，去掉 `window57-20260930-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：审核队列耗尽后，用户 2026-09-30 要求用 Gemini 3.8 Flash（`pi/cpa/gemini-3.8-flash-high`）对 2026-09-21 冻结点 `7c38a53b` 以来修改过的 1190 条译文做一轮快速复核，Claude Opus 5.5 逐子项交叉核验、宿主采纳后确认 83 条（证据 `evidence/translation-audit/modified-since-20260921-flash-20260930/`，提交 `c4728694`）；用户随后“请合并修复”。另含积压：Toxic Death→剧毒之死（pending 第47项，Gemini 裁定）及解锁列表引用，两条 Orcs 开场白 西方灾星→西方天灾（terminology/society.tsv:34 preferred）。共 87 条：engine 1、tome 32、ashes-urhrok 6、cults 24、orcs 24。Elvala 回忆录 8 章首行统一为“埃尔瓦拉最高议会领袖艾伦尼恩·加威尔”。主游戏与引擎按 manifest 固定 commit 624a673 核验；DLC 来源仓库与 commit 未固定。不改术语库；无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 87 条 → REVIEW(0) r0a1（GPT-6 Sol）2 确认（palace-fumes 你们→你；部族→部落）、1 驳回（unique demons 依实现）→ execute-02 → RE_REVIEW(1) r1a1 2 驳回 → FINAL(1) f1a1（Opus 5.5，记录 attempt 改为 2，见 HOST-NOTE-FINAL-ATTEMPT-RENUMBER.md）5 确认（Grand Council 大议会→最高议会 3 条、女附魔师→女巫、为了部落→为了兽人、palace-fumes 裁定句）→ execute-03 → RE_REVIEW(2) r2a1（GPT-6.1 Sol）会话含 compacted 记录，原生 harvest 按设计拒收记 INVALID（INVALID-R2A1.json），fresh retry r2a2 1 驳回（doom shield 按裁决保留忠实译法）→ FINAL(2) f2a3 7 确认＋宿主补 1（age-allure 歌词行），1 驳回（tinkers→插件 既有用法）→ execute-04 → RE_REVIEW(3) r3a1 2 确认（叛离法师→不法法师；“他们离我们所处的地方越来越近”→“我们藏身之处上方的土层越来越薄”）→ execute-05 → FINAL(4) f4a1 87/87 OK，cycle 4 收敛（max_cycles 5）。
   - 工具：Codex 0.159.1 原生会话引导消息只剩两段，经用户授权在 `review_lifecycle.py` 按版本校验引导段并加测试（提交 `88e29cf9`），本窗口 execute-01 起按原生路径收取。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `95b566f83cccd57d0102af7908158c07684bb5c8`；新 catalog `9d42642844e5a69a7df762ac7fdf72279aff578704ba268d734b92584fd269f6`；migration `f312e80bbb644d441ac98b8c7e91a992d92ec7c25f48557d6d79571d7a7a8882`。
   - 后续：87 个 successor 必须重新审核（第373批起），不继承旧 done。窗口 58 积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下六处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-30（修复窗口57已完成、待宿主证据提交与推送；下一步审核窗口57的 87 个 successor，第373批）`。
   - 第一节以“- **暂停中**”开头的条目（连同其下一行续行，共两行）整体替换为一行：`- 2026-09-30：用户恢复工作，要求用 Gemini 3.8 Flash 快速复核 09-21 以来修改过的 1190 条译文（证据提交 `c4728694`，确认 83 条），随后“请合并修复”开窗口57。是否连续审核第373批以当前会话指示为准。`
   - 第一节以“- 修复窗口已闭合至 **56**”开头的条目（连同其下一行续行，共两行）整体替换为一行：`- 修复窗口已闭合至 **57**：快速复核确认的 83 条与积压 4 条（Toxic Death→剧毒之死及解锁列表、两条 Orcs 开场白 西方天灾）已修复；译文提交 `95b566f8`；migration `f312e80b…` 的 87 个 successor（引擎 1、主游戏 32、Ashes 6、Cults 24、Orcs 24）须重新审核，不继承旧 revision 的 done 状态。`
   - 第二节以“- 审核模型：”开头的那一行中，把 `codex/gpt-6-sol` 改为 `codex/gpt-6.1-sol`，其余文字（含下一行续行）保留；第二节以“- 2026-09-29：第372批后用户要求暂停”开头的那一行整行改为：`- 2026-09-30：用户指示此后凡用 GPT-6-Sol 处一律改用 `codex/gpt-6.1-sol`（显式 thinking medium）；Codex 0.159.1 原生会话已纳入 harvest 白名单（`88e29cf9`）。`
   - 第三节第 1 项第一行（以“1. 继续审核第 **373** 批”开头）整行改为：`1. 继续审核第 **373** 批起：窗口57的 87 个 successor（引擎 1、主游戏 32、Ashes 6、Cults 24、Orcs 24，混合来源批）。`；该项其余续行保留。
   - 第三节第 2 项：从以“2. 窗口 57 尚未开启”开头的行起，到以“   窗口 57 积压 **3** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w57-20260930/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第372批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第三节第 3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w57-20260930/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-57-20260930/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
