# 修复窗口 23 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次唯一 EXECUTOR 仅修改 `mod-tome.lua` 中冻结 WORKSET 的 3 个 target：

- 夺心魔任务说明：将“清除……两大威胁之一”修为“至少清除一个对夺心魔的威胁”，补全 `at least`，且没有删去任务所指的威胁。
- 埃亚尔之怒类别说明：补出“你周围的敌人”，对应 `foes around you`。
- 奥术漩涡效果说明：明确奥术射线从漩涡处射向视野内随机一名敌人，漩涡附着的目标与射线路径上的所有目标均受到 `%0.2f` 奥术伤害；无敌人时附着目标本回合受到的奥术伤害提高 `50%%`；目标死亡时剩余伤害转化为半径 2 的奥术爆炸。

其余已忠实句子未重写，未处理 advisory、pending 或其他 repair。专名和技能名沿用库内既有译法：夺心魔、埃亚尔之怒、奥术漩涡、奥术射线。`source`、`source_tag`、参数顺序、printf 占位符、`%%` 与 markup 均保持基线。专用验证确认夺心魔任务条 source/target 末尾均恰有 1 个换行，另外两条 source/target 均为 0 个换行；三条 TAB 布局均与原文一致。

`PREFLIGHT-BATCH269.json`、`HOST-WORKSET.json` 与 `SOURCE-ANCHORS.json` 分别从 `.ai/task/repair-w23-20260923/PREFLIGHT-BATCH269.json`、`WORKSET.json` 与 `SOURCE-ANCHORS.json` 机械复制，并已用 `cmp` 和 SHA-256 逐字节核验一致。真实检查结果见 `VALIDATION.json`。

本执行未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。完整门禁、独立 REVIEW、FINAL_REVIEW、构建与 `DONE_VERIFIED` 仍由宿主继续。

## 第 1 轮修复（fresh EXECUTOR）

依据 `ADJUDICATION-R0.json` 的 confirmed finding `R0-VORTEX-NOFOE-SINGLE-HIT`，仅将奥术漩涡条目中的“如果没有找到敌人，漩涡附着的目标本回合受到的奥术伤害提高 `50%%`。”改为“如果没有找到敌人，本回合漩涡对其附着的目标造成的奥术伤害提高 `50%%`。”，以明确提高的是漩涡本次造成的伤害，而非目标本回合受到的全部奥术伤害。该条的 `%0.2f`、`%%`、其余句子、`source` 和 `source_tag` 未改；另外两条既有修改未动。本轮验证结果追加于 `VALIDATION.json`。
