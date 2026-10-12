# 窗口68证据发布

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
