# 窗口61证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-61-20261001/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/70e37de35c9f044447a6ca0026a1d85448334de0628553f21910b62610de8598.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中如已有 `IMPLEMENTATION.md` 与 `VALIDATION.json`，保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w61-20261001/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-61-20261001/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window61-20261001-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window61-20261001-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：22 revision_changed（均为 workset 条目）、29806 unchanged、0 ambiguous/unmapped、22 successor 新队列。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w61-20261001/` 的 `HOST-SUPPLEMENT-CLAIMS.json`、`HOST-EXACT-DIFF.json` 与 `HOST-EXACT-DIFF-POST-FIX1.json` 至 `HOST-EXACT-DIFF-POST-FIX4.json`；
   - `.artifacts/i18n/repair-window/` 的 `window61-20261001-publish-chain.log`、`window61-20261001-publish-chain-timing.json`、`window61-20261001-migration.json`、`window61-20261001-migration-timing.json`，复制时去掉 `window61-20261001-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：22 条译文（mod-tome.lua 17、tome-ashes-urhrok.lua 2、tome-cults.lua 3），无术语改动。
     - 第377–379批确认 9 条：`8efa510a7a`、`a2147f96a9`、`b19b6b1d34`、`bc2f66a5e1`、`de48fb09ea`、`56b7b501eb`、`b028c0ed3b`、`074d7c0b7e`、`fc1ebcae01`。
     - 第377批宿主补充 1 条：`9987aef53c` Blindside＝闪电突袭。
     - 2026-10-01 死亡信息表系统性分析 12 条，见 `evidence/quality/pending-user-review.md` 同日一节，用户同意排入本窗口。
       - 死亡公告四个句式 `ab25e27abc`、`abf9674633`、`49f7781bff`、`7cba41f15f`：经 args_order 改为“在{区域}第{N}层…而死，杀死他（她）的是…”，特殊句式改为“在{区域}第{N}层{消息}”。
       - 拼接短语 8 条：`4ddf91a568`、`d798b563aa`、`7f5e27e174`、`ef3eefd58d`、`5fa2c1c3c1`、`17a76d1b3e`、`efaf9b0f43`、`0aba4d5ba2`。
     - 其中 `17a76d1b3e`、`5fa2c1c3c1`、`ef3eefd58d` 按用户 2026-10-01 对 pending #50 的裁决（B：killer_message 以凶手为主语）改为主动句。
     - 主游戏按 manifest 固定 commit 624a673 核验；Ashes／Cults 公开源码来源未固定。无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json；REVIEW/RE 用 GPT-6.1 Sol，FINAL 用 Opus 5.5）：
     - execute-01 → REVIEW(0) r0a1 4 ISSUE：2 条 killer_message 主语颠倒、意志之力“魔法”→“魔力”、末日加速“相位外”→“脱离现实”；宿主另把同族 `5fa2c1c3c1` 并入；
     - execute-02 → RE_REVIEW(1) r1a1 22 OK → FINAL(1) f1a2 1 确认（苦痛链接 victim 与选择提示“受害者”不一致）；
     - execute-03 → RE_REVIEW(2) r2a1 OK → FINAL(2) f2a2 2 确认（异变之手“心灵护盾”→“灵能力场”；The Amalgamation 吸收进自身）；
     - execute-04 → RE_REVIEW(3) r3a1 OK → FINAL(3) f3a2 1 确认（异变之手属性行与副手非空禁用说明拼接）；
     - execute-05 → RE_REVIEW(4) r4a1 OK → FINAL(4) f4a2 22/22，cycle 4 收敛（max_cycles 5）。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `276e8b2df82095585a353d98717d1715f7ef33df`；
     - 新 catalog `b47c0ca115581428911c65baf9c48e7bcdbe4d050a4320c998f88763b931f18a`；
     - migration `70e37de35c9f044447a6ca0026a1d85448334de0628553f21910b62610de8598`。
   - 后续：
     - 22 个 successor 必须重新审核，不继承旧 done。
     - advisory carry_forward：Ashes 苦痛链接效果说明“牺牲生物”→“受害者”，排入窗口62。
     - 窗口62 积压约 55 条（估算）：pending #50 B 的其余 killer_message 与 #51 B 的 dreadfell dark Master。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下六处，其余逐字保留：
   - 第3行“更新时间”行：改为 `更新时间：2026-10-01（修复窗口61已完成、待宿主证据提交与推送；下一步开修复窗口62）`。
   - 第一节以“- 修复窗口已闭合至 **60**”开头的单行条目：整体替换为一行 `- 修复窗口已闭合至 **61**：窗口60（译文 `d62fe6ff`）与窗口61（第377–379批确认 9 条＋Blindside 补充＋死亡信息表分析 12 条，译文 `276e8b2d`，migration `70e37de3…`）均已修复；窗口61 的 22 个 successor 须重新审核，不继承旧 revision 的 done 状态（窗口59/60 的 successor 已于第375–380批审完）。`
   - 第一节以“- 2026-10-01：用户裁定 deeprock 技能树改”开头的那一行之后：插入一行 `- 2026-10-01：审核队列清空后，用户要求系统性分析死亡信息表（`cd2d0d7e`）；同意把 12 条句式与拼接缺陷并入积压，开窗口61；随后裁定 pending #50（killer_message 改凶手主语）与 #51（dark Master→黑暗领主）均采用 B，排入窗口62。`
   - 第一节“待用户集中审阅的争议条目”两行：把其中的 `共 49 项` 改为 `共 51 项`，其余文字（含“**全部已裁决**”“无未决项。”）不变。
   - 第三节第 1 项第一行中，从 `审核队列已清空：` 起到 `开修复窗口61，或暂停。` 止的子串：替换为 `下一步开修复窗口62（用户 2026-10-01 裁决 pending #50 B／#51 B，见第 2 项积压），推送后审核窗口61、62 的 successor。`；该行其余文字（补空格维护一句）与该项续行保留。
   - 第三节第 2 项：从以“2. 窗口 60 已完成”开头的行起，到以“   窗口 61 积压 **9** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w61-20261001/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第380批计时（实测”开头的一行必须原样保留。

   第三节第 3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w61-20261001/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-61-20261001/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
