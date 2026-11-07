# 全职业／种族巡检（2026-11-07）

用户 2026-11-07「开始派发子代理逐一开始每个职业/种族并检查技能、装备描述是否正常」。36 个职业（不含冒险者/流浪者）分 12 组、每组 3 个角色，种族轮换覆盖全部 18 个种族；每个角色读创建界面、升级窗口全部技能树、开局装备与角色面板，不推进剧情。

- cls01–04：Opus 5.5（02:56 Claude 5 小时额度耗尽中断，06:17 唤醒完成）。
- cls07、cls11：Sonnet 5.5，覆盖偏浅；用户 11-07「同意用deepseek补测一轮」，以 cls07b、cls11b（DeepSeek v4.1 Flash）补测。
- cls05–12 其余组：DeepSeek v4.1 Flash；上游频繁 429（prefill_cap_refused/overloaded），长会话唤醒无效，13:38 起改为每角色新开子代理（cls05-c1 等，第二批）。
- 用户 11-07：子代理改用 Sonnet/DeepSeek；每小时 paseo usage 查额度；Claude 周额度保留 5%。

## 第一批（68 条，`findings-batch1.jsonl`）
主代理逐条裁决后交 Opus 执行者落地（`batch1-executor-spec.md`），执行报告 `batch1-executor-report.json`：71 条修改（含同类扩展）、5 条驳回、3 条延后。
- 改名 7 组按用户 2026-09-27「纯名称交 Gemini」定名（`names-cls.md/json`），双向检索无冲突：Duck and Dodge 俯身闪躲、Temporal Guardian 时空守护、Dream Smith 梦境铁匠 / Dream Forge 梦境熔炉、Stoneskin 坚石肌肤、earthen vines 大地藤蔓、eldritch shield 奥术之盾 / eldritch stone 奥术岩石、Dimensional Anchor 空间之锚 / Spatial Tether 空间系绳（terminology/combat.tsv dimensional anchor 行同步）。
- 驳回：cls07b-03（ignore_direct_crits 按比例削减暴击额外伤害，现译与实现一致）、cls07b-06（开局介绍原文为 chronomancer，两职业共用）、cls10-01/cls10-02/cls12-02（DLC 说明数值与实现不符，现译贴合实现，按 2026-11-02 用户裁决保留；DLC 源码来源未固定）。
- 延后（插件代码）：cls07b-07 引擎折行拆数字、cls11b-02 main/off 武器组名、cls11-01 上游 %%%% 转义。
