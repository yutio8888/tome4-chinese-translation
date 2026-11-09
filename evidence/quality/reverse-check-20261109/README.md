# 公开插件 0.3.9 反向检查（2026-11-09）

- 对象：发布仓库 5cdbc31 的 data/locales/zh_hans.lua，13,671 条（不含 develop 上 0449–0452 的神器修改）。
- 方法：按约 2.5 万汉字切 32 段，Opus 5.5 子代理先只读中文以玩家视角标出问题，再查英文/源码核实（prompt.md）。32 段全部 read=全量；Claude 周额度 80%→83%。
- 结果：99 条（all-findings.json）。主代理核实（decisions.json）：93 apply、1 反向 apply（cross-tier 库内 20 处「越层」，改唯一「跨层」）、5 skip（2 已于 0449 修复；泰鲁戈洛斯为官方名、非之家为名称，按官方译名原则不改；Jinx 厄运/不幸混用待术语裁决）。
- 严重项：#78 Embers「最大生命值的 5%」误为「5 倍」。
- 执行：Opus 执行者，exec-report.json（93 applied）；lint strict 0 错误，source 全部一致。复审见 lite batch 0454。
