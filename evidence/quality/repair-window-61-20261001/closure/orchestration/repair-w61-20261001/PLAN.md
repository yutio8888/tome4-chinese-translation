1. 修复 22 条：审核377–379 确认 9 条＋第377批宿主补充 Blindside 1 条＋2026-10-01 死亡信息表分析 12 条（4 个死亡句式改语序并设 args_order，8 条拼接短语修句尾标点、连接与 reknor 的单复数/时态）；冻结 workset、源码锚点与译文基线；setup 后跑 check_siblings.py。
2. 唯一 EXECUTOR 按 SOURCE-CLAIMS 定向修改译文（无术语改动），给出验证。
3. 宿主核验精确 target/args_order diff，冻结 review 输入，独立 REVIEW/full 与 FINAL_REVIEW/full，必要时有界修复。
4. 17项门禁、DONE_VERIFIED、译文提交、queue/catalog/migration、证据发布与推送。
5. successor 进入审核队列，继续连续审核。
