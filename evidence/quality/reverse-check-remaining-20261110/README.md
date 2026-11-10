# 未进入公开插件的译文反向检查（2026-11-10）

- 对象：库内未被插件覆盖、沿用官方中文的条目（去重后 11,218 条：mod-tome 10,317、engine 622、items-vault 44、addon-dev 84）；Possessors 194 条因源码未公开跳过。
- 方法同 `../reverse-check-20261109/`：10 段 Opus 5.5 子代理先读中文再核英文（prompt2.md），全部 read=全量；Claude 周额度 85%→86%。
- 结果：98 条（rem-all-findings.json）。主代理裁决（rem-decisions.json）：90 由执行者修改（rem-exec-report.json）；Un'fezan's Cap 由 Gemini 4 Argon 定名「恩费赞之帽」；跳过：light 共用键（已知限制）、quiver 库内多数为「箭袋」、鬼祟的图书馆（官方名，advisory）。
- 用户 2026-11-10 裁决 maim＝断筋：Maim/Maimed 状态、技能名、缠斗与链锯技能描述统一（术语表新增 Maim 行；双手重创与喊话、lore 不变）。
- 复审见 lite batch 0463 起。
