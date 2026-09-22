# 修复窗口 7 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 8 个 target；source、section、source_tag、args_order、special、printf 与 markup 均未改变。除 `e882cc8d4e…` 按任务要求恢复 source 的格式外，其余 target 的 LF/TAB 序列保持基线。

## 实际修复

- `e80304576e…`：删除仅限四种疾病的错误枚举，并按本轮裁决明确为传播目标身上的所有疾病。
- `e82dab7a29…`：补回法杖尖端“粗大”以及时空在其周围扭曲的外观信息。
- `e83a051874…`：将未来时态的“不会发生”改回过去事实“从未发生”。
- `e85e4d8855…`：首句改为“持盾跃向相邻目标”，保留伤害、`Daze=眩晕`、跳板和落点语义；第二行把“盾牌伤害”的范围补全为“盾牌的属性伤害加成”，第三行保持不变。
- `e882cc8d4e…`：将误作资源球的 bolt 恢复为心灵飞弹，并把灵能通道的射程提升与移动中断条件恢复到同一句；target 从基线的 4LF/8TAB 恢复为 source 的 3LF/6TAB。R1 有界修复仅调整第二行数量关系：每超出 `%d` 点反馈值只换算 1 枚额外飞弹的总量，再分配给敌方目标，每个目标至多 1 枚，且每回合额外飞弹总数不超过 `%d` 枚，不按目标数倍增。
- `e8959a83e2…`：恢复 decay/defiance/spite 的局部原义，并补回已有护盾可叠加强度和延长持续时间的语义及适用条件。R2 有界修复仅将第二行触发条件补全为负面状态须由非自身施加、且不属于“其他”类型；其余词句、占位符与格式保持不变。
- `e895fea030…`：只把 `_t` 未鉴定名 `spinneret` 从“丝腺”改为器官名“吐丝器”；`giant spider spinneret` 的兄弟行与术语库均未修改。
- `e8bc936f6d…`：将仅限心脏的“被掏心”改为体现取出内脏的“被掏出内脏”。

冻结的 `SOURCE-ANCHORS.json` 已包含所需固定源码片段，实施期间无需额外 `git show` 补查。

## 不变量与验证

任务验证脚本通过 LuaJIT 全记录比较确认恰有 8 个 target 变化，其余记录字段不变；printf、markup、特殊 token 与适用的 LF/TAB 序列均满足冻结要求。严格 lint、语义 claim 回归和 `git diff --check` 均通过，真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH253.json` 是 `.ai/task/repair-w7-20260922/PREFLIGHT-BATCH253.json` 的逐字节副本，SHA-256 为 `9cbbbf5f0a328749755d40a5420a941c3c866b9680ed653fa0a1778b83bcc28d`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w7-20260922/WORKSET.json` 的逐字节副本，SHA-256 为 `f7916d0adb742a9f69b033c41d88284386fcee63f2f374e7db875aa50dbef6ed`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w7-20260922/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `38fd9e312dd998aa0625cb3810149d69b0f293c17ae1cb68aebc9cf14e5136a7`。
- `USER-PAUSE.json` 是 `.ai/task/repair-w7-20260922/USER-PAUSE.json` 的逐字节副本，SHA-256 为 `64d09ed5e3a3d886049ebd69a047adafa16e782a12497a3de9d1399f1af85a85`。
- `ADJUDICATION-R0.json` 是 `.ai/task/repair-w7-20260922/ADJUDICATION-R0.json` 的逐字节副本，SHA-256 为 `2d4ec1d45d112acd912c8a84f30519d4bd31dd86ecfc944d8996ff1d9a7660a7`。
- `ADJUDICATION-R1.json` 是 `.ai/task/repair-w7-20260922/ADJUDICATION-R1.json` 的逐字节副本，SHA-256 为 `b579bd7e7a5f50a53094a19b2947746c78d2c1e53c476de573a569fd86e171b8`。
- `HOST-SOURCE-SUPPLEMENT.json` 是 `.ai/task/repair-w7-20260922/HOST-SOURCE-SUPPLEMENT.json` 的逐字节副本，SHA-256 为 `b568a3734ab3791018af7e0c841ecf1b14529a4216d3c1163755301c06ba4bd4`。
- `ADJUDICATION-R2.json` 是 `.ai/task/repair-w7-20260922/ADJUDICATION-R2.json` 的逐字节副本，SHA-256 为 `66bd69d55d2c4cb5c45288cd56d0b1c6b459041bbbabfb4c9b776102ded9d022`。
- `HOST-SOURCE-SUPPLEMENT-R3.json` 是 `.ai/task/repair-w7-20260922/HOST-SOURCE-SUPPLEMENT-R3.json` 的逐字节副本，SHA-256 为 `7d65b6579bca7debc229ca7d4807ce1b4f90c111a44255c187cdbdd2f41ecfcb`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未更新仓库根 handoff。宿主完成窗口 7 的闭合与 handoff 后应按 `USER-PAUSE.json` 暂停，不启动批次 254。
