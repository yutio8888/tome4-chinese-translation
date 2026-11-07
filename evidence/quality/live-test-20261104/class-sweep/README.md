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

## 第二批（51 条，`findings-batch2.jsonl`，每角色新开 DeepSeek 子代理）
主代理裁决后交 Opus 执行者（`batch2-executor-spec.md`），报告 `batch2-executor-report.json`：31 条修改（含同类扩展）、15 条驳回、5 条延后、2 条第一批已修、1 条 advisory。
- 驳回多为说明与实现不符、现译贴合实现（cls08-c2-05 冰墙、cls10-c1-01 默认 friendlyfire=true、cls10-c2-01 固定点数治疗、cls10-c2-05 无每回合限制、cls12-c1-01 约 31%、cls12-c2-01 只作用于炮台、cls12-c2-02 默认眩晕 3 回合、cls12-c2-03 含首个目标、cls09-c3-01 传送到附近）；其余为升级预览空格规则要求的空格（cls09-c3-04、cls11b-c3-02、cls12-c3-03、cls06-c3-04）、暴击减伤按比例（cls08-c3-01）与已知盾牌逗号（cls12-c3-01）。DLC 源码来源未固定。
- 延后（插件代码）：cls11b-c3-01、cls06-c3-02（引擎折行拆数字）、cls10-c2-02（人偶短名截断）、cls08-c3-03、cls06-c3-05（共享键 all 用于 7 个属性行，「抗性改变：+7% 所有」需代码侧处理）。
- advisory：cls05-c1-04 Combat Veteran 技能树「战斗经验」，需术语裁决。
- 队列事故：17:46–17:52 旧队列脚本把 `paseo wait` 的瞬时返回当作结束，误归档了 7 个刚启动的子代理；改用 `cls-q5.sh`（DONE 行或连续 3 次非运行才判结束）后重跑，均已完成。
