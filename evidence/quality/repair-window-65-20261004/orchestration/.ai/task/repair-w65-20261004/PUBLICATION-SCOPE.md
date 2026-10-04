# 窗口65证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-65-20261004/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/e437cb51838bcc569d772a905f70dfe23b175537a8b2a4a9f1e1b1c19022685f.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w65-20261004/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-65-20261004/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window65-20261004-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window65-20261004-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：revision_changed 11、unchanged 29817、queued_successors 11、ambiguous 0、unmapped 0。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json`、`NEW-TARGETS.json` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w65-20261004/` 的 `HOST-SUPPLEMENT-CLAIMS.json` 与 `HOST-EXACT-DIFF.json`；
   - `.artifacts/i18n/repair-window/` 的 `window65-20261004-publish-chain.log`、`window65-20261004-publish-chain-timing.json`、`window65-20261004-migration.json`、`window65-20261004-migration-timing.json`，复制时去掉 `window65-20261004-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：11 条译文（tome-orcs.lua 8、mod-tome.lua 1、tome-ashes-urhrok.lua 1、tome-cults.lua 1），无术语改动。
     - 2026-10-03 重新复审轮第392–395批宿主确认 9 条（各批 `HOST-FINAL-DECISIONS.json`）：换行与缩进不变量 3 条（物品教程删 2 个多余换行、雷鸣榴弹与精神碾压的全角空格改回 `\t\t`，精神碾压同时补回末行）；忠实性与机制 6 条（恶魔结合改为通过种子召唤恶魔、克罗格解锁文本补译并把伊格兰斯改回伊格、电子咒式补“或技能”、电力放出的电弧伤害补“闪电”、爆矢枪改为多管弩箭发射器与毒弹、任务“已死之神在等待”的通关描述补克鲁克部落与“高阶”）。
     - 宿主补充 2 条（不计积压，第394批 `HOST-FINAL-DECISIONS.json` 的 `additional_host_observations`）：火箭靴补回 `\t\t` 并改末句、紧急蒸汽排出删多余换行并整句改写。
     - 新译文由宿主按各条“修复：”与整句对照写定（`publication/NEW-TARGETS.json`），EXECUTOR 逐字替换；宿主核验 11 条 after 与 new_target 逐字相等（`publication/HOST-EXACT-DIFF.json`）。
     - 主游戏按 manifest 固定 commit 624a673 核验；三个 DLC 源码来源未固定，按公开源码核验并如实标注。四个 locale 文件中无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）10 OK／1 ISSUE → FINAL(0) f0a2（Opus 5.5）11/11，cycle 0 收敛（max_cycles 5）。r0a1 对 `557285f8a1`（电力放出）的 ISSUE：Orcs 源码最多连到 nb−1 个其他目标，而英文写 “arcs to %d other targets”，译文与英文一致；按用户 2026-10-03 撤回决定，英文与实现矛盾不在译文中改写，宿主判 advisory carry_forward（`publication/ADJUDICATION-R0.json`），FINAL 判该条 OK。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `9079821a2d8f61ff9b84e1e7e111c2af65bd0cc1`；
     - 新 catalog `fa20187008d51eaab572200028302cc7cfdf7bc69a16a4270d1f71013db6bff4`；
     - migration `e437cb51838bcc569d772a905f70dfe23b175537a8b2a4a9f1e1b1c19022685f`。
   - 后续：
     - 11 个 successor 必须重新审核，不继承旧 done。
     - 下一个修复窗口（66）积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`：先核对当前 `handoff.md` 的 SHA-256 等于 `1d238bc1cfd1fe2fc6b29d74983f9aa37ea31fa90d5927789dc6739fb01a812a`，不等则停止并报告；相等则将其整体替换为宿主已存的 `.ai/task/repair-w65-20261004/HANDOFF-NEXT.md`（逐字复制，替换后 SHA-256 应为 `480e189f40d1587b4dbdc93404912b2d265656e5bb75d9b8e6fd4cdd34ec2657`）。不要另作改动。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w65-20261004/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-65-20261004/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
