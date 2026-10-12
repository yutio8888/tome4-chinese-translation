# 窗口68证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-68-20261012/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/6b99f6e01debd92e9de588cffe9b86f02a3e3047fd28ddb263c45c3e92858e86.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json`（execute-01～06 所写）保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w68-20261012/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-68-20261012/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window68-20261012-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window68-20261012-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：168 rows revision_changed/target_changed（106 修复＋62 目录同步），queued successors 168，ambiguous 0，unmapped 0，projection_calls 1。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json`、`NEW-TARGETS.json` 与全部 `ADJUDICATION-*.json`、`CATALOG-SYNC.json`、`FIX3-TARGETS.json`、`FIX4-TARGETS.json`；
   - `.artifacts/i18n/repair-w68-20261012/` 的 `HOST-SUPPLEMENT-CLAIMS.json`、`rewrites.json` 与 `HOST-EXACT-DIFF.json`、`HOST-EXACT-DIFF-POST-FIX1.json`～`HOST-EXACT-DIFF-POST-FIX4.json`、`cands.txt`；
   - `.artifacts/i18n/repair-window/` 的 `window68-20261012-publish-chain.log`、`window68-20261012-publish-chain-timing.json`、`window68-20261012-migration.json`、`window68-20261012-migration-timing.json`，复制时去掉 `window68-20261012-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：106 条译文（mod-tome.lua 78、tome-ashes-urhrok.lua 7、tome-cults.lua 11、tome-orcs.lua 10），无术语改动。用户 2026-10-12 授权“先开 Magic 属性名修复窗口”。
     - 依据：主游戏固定 commit 624a673 `game/modules/tome/load.lua:185` 定义属性 Magic（short mag）；本库界面属性名为“魔力”（mod-tome/load.lua 段 stat name／short_name，`terminology/combat.tsv:122`）。source 中 Magic 指属性、现译写作“魔法”的条目统一改为“魔力”：职业／种族初始属性与“最重要的属性”、“基于魔法”的数值说明、属性变化日志与属性说明本身。传说／概念语境、技能名（Born into Magic 等）与已作“魔力”的条目不在范围（盘点见 `publication/cands.txt`）。
     - 新译文由宿主写定（`publication/NEW-TARGETS.json`），EXECUTOR 逐字替换；宿主逐轮核验 106 条 after 与预期逐字相等（`publication/HOST-EXACT-DIFF*.json`）。复审各轮另确认并修复同批条目的 5 处旧错：Cults Nether Spark“虚空法术”→“彼世法术”（r0a1）、Arcane Destruction“物理强度（当前值）”→“基础物理强度（当前加成）”（r0a1）、Orcs 神器“光明伤害”→“光系伤害”（r1a1）、两条换行结构对齐源文（f2a2）、Arcane Destruction 末尾补 LF（f3a2）；`NEW-TARGETS.json` 是 execute-01 的冻结输入，终稿以 POST-FIX4 核验为准。
     - 主游戏按 manifest 固定 commit 624a673 核验；DLC 源码来源未固定，按公开源码快照 SHA 核验并如实标注。同键兄弟 19 处均在 workset 内同步修改。
     - 目录同步：`c7ea0683b`（官方对照审核修订 52 条／62 处）在 WP2-Lite 流程外改过译文，旧 catalog 仍记修订前 target；本窗口的唯一一次 catalog/migration 一并登记这 62 条（`publication/CATALOG-SYNC.json`），EXECUTOR 未改动它们。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：REVIEW r0a1（GPT-6.1 Sol）104 OK／2 确认 → execute-02 → RE_REVIEW r1a1 105 OK／1 确认 → execute-03（模型容量错误，无输出，归档）→ execute-04 → RE_REVIEW r2a1 106/106 OK → FINAL f2a2（Opus 5.5）104 OK／2 确认 → execute-05 → RE_REVIEW r3a1 105 OK／1 advisory（M264）→ FINAL f3a2 105 OK／1 确认 → execute-06 → RE_REVIEW r4a1 106/106 OK → FINAL f4a2 106/106 OK，cycle 4 收敛（max_cycles=5）。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档（execute-03 因模型容量错误未运行，已归档并 fresh retry 为 execute-04；execute-04 在被忽略的宿主派生目录写过一份校验 JSON，记为边界 advisory）。
   - 标识：
     - 译文提交 `19fd9ec059a6ad43675a07b5175f85976ed35dc7`；
     - 新 catalog `6ae69b9abfc43afa8684a6816341c780d80c09e1cffc8cd8f0d767b4e49fb058`；
     - migration `6b99f6e01debd92e9de588cffe9b86f02a3e3047fd28ddb263c45c3e92858e86`。
   - 后续：
     - 168 个 successor（修复 106＋目录同步 62）必须重新审核，不继承旧 done。
     - 下一个修复窗口（69）积压 1 条：`tome-orcs.lua:1411` “光明伤害”→“光系伤害”（同族，不在本窗口 workset）。
     - Cults “咬一口”秒杀几率（上游英文与实现矛盾，官方对照审核 M264）记 advisory，待用户裁决。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`：先核对当前 `handoff.md` 的 SHA-256 等于 `1be6e486ce4de653fdf44c02f483bc59de96309ae6998fe7c1c55cca12a743ea`，不等则停止并报告；相等则将其整体替换为宿主已存的 `.ai/task/repair-w68-20261012/HANDOFF-NEXT.md`（逐字复制，替换后 SHA-256 应为 `f8cbe3d5070be22c6e82f12cc438477dbddb63f4047e0024676869039521f3aa`）。不要另作改动。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w68-20261012/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-68-20261012/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
