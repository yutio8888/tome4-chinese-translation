# 修复窗口 37 发布记录

- 范围：来源批次 310、311、312、313、314 共 25 条确认问题已修（tome-cults.lua 6 条、tome-orcs.lua 19 条；全仓库同 source 检查无跨组件同键）。Cults 与 Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
- 预检：开窗前两个只读助手逐段比对 4 条最长条目（fbe22d02、0b55d129、1094f94c、0b59fe6a），宿主逐字核验引文 44/44 后并入修复（ADJUDICATION-HOST-PRECHECK-C0）；其中 1094f94c 的 [b] 强调当时判为保留，后在 FINAL(1) 被推翻。
- 复审路径：
  - execute-01 修复 25 条，宿主精确 diff 核验。
  - REVIEW(0) r0a1 确认 3 条：克林布尔手记卡巴萨进帐篷后才死去；静电震击“造成伤害”才触发（callbackOnHit）；时间盛宴“每次对目标施加衰亡效果时”（衰亡为被动施加）。“软蹄族”译名记 advisory 并登记待用户审阅第31项。
  - execute-02 → RE_REVIEW(1) r1a1 无一级确认：烟雾覆盖（cancel_damage_chance）与 Cunning=灵巧 refuted，软蹄与拘留营末信 “No.” 记 advisory。
  - FINAL(1) f1a2 输出截断（25 条只回 3 条）被契约拒收（INVALID-F1A2），重派 f1a3 确认 1 条：1094f94c 新增的两对 [b] 与源 markup 不一致。
  - execute-03 → RE_REVIEW(2) r2a1 确认 1 条：Kruk Pride 按术语库对齐“克鲁克部落”（条目内一处）。
  - execute-04 → RE_REVIEW(3) r3a1 25/25 OK → FINAL(3) f3a2 25/25 OK。
- 门禁：首轮 17 项中门禁 11 因宿主追加待审阅第31项时在 pending-user-review.md 末尾多留一空行而失败（结果保留为 prior gate run），去掉空行后重跑 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
- 标识：译文提交 `4061b447db0e5320a86d4d50ee7428b6f3451f26`；新 catalog `00d4950120d06e517727b73e5cd17ce47185a5765a9956a2dfc891cb10baf235`；migration `0d087c7cad2d48953faf2b826bb30182a8a925a8acc5319159caeab2975d551b`。
- 后续：25 个 successor 必须重新审核，不继承旧 done。窗口外宿主补充项留给下一窗口：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致；f6030742 导师文物 Sher'Tul“夏图尔”→“夏·图尔”；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10` misery→“困难”；`a5a712dc` Writhing One 技能名。待用户审阅新增第31项（软蹄族／软蹄者）。
- 本 publication child 待宿主归档。
