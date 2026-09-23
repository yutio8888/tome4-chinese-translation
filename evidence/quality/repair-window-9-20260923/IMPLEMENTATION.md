# 修复窗口 9 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 5 个 target；source、section、source_tag、args_order、printf 占位符、markup、LF 与 TAB 均未改变。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `e9e627f60c…`：高阶奇术师解锁文本仅将 Flame 的旧译“火球术”改为现行技能名“火焰”；奥术射线、闪电术、粉碎钻击、寒冰箭及其余文本不动。
- `ea047c36a0…`：潜行说明仅补回半径内敌人必须能看见你的限制，并将会打破潜行的非瞬间非移动“技能”改为“行动”。
- `ea2d3aa570…`：将“有 %d 个符文”改为“%d 个符文生效中”，恢复 active 的状态含义。
- `ea36045fba…`：仅将夏之眼灵晶的“温暖的微光”改为“明亮温暖的光”。
- `ea4c9e1c88…`：将物品描述中的“这个法杖”改为“这根魔杖”，“撕裂空间”改为“扭曲空间”，并将能量明确为“原始魔法能量”；物品名“回归之杖”未改。

## 固定源码补查

按任务要求，仅以 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查了高阶奇术师解锁文本、Flame、Ice Shards、潜行检测与说明、Runeskin、夏之眼及回归之杖描述。结果与冻结的 `SOURCE-ANCHORS.json` 和 `SOURCE-CLAIMS.json` 一致，未发现范围冲突。

## 不变量与验证

窗口专用验证脚本通过全记录比较确认恰有 5 个 target 变化，其他记录字段不变；source/tag/args_order、printf 占位符、markup、LF 与 TAB 均保持基线。严格 lint、语义 claim 回归和 `git diff --check` 均通过，真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH255.json` 是 `.ai/task/repair-w9-20260923/PREFLIGHT-BATCH255.json` 的逐字节副本，SHA-256 为 `457c1e4797600b340f525e84a5cb343a21982a95cde9d9d6497964cccae505a5`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w9-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `d3bac39b1e20ef178c6a5e4447252f75bb32ec21823d5868108c5502c8cecacc`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w9-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `cd4b09110b7907f3c75ea162a23ffab7ddcabcaf094a102b924aca4f9b4aae9b`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未更新 handoff。
