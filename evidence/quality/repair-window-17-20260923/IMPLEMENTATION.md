# 修复窗口 17 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 5 个 target；source、section、source_tag、args_order、printf 占位符、`%%` 与 markup 均未改变。LF 与 TAB 已逐条恢复为原文结构。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `f277b46e7f…`：猎头者播报改为“取下了 %s 的首级”，并明确本层敌人因此迟疑、失去对玩家的锁定；未使用“暂停”。
- `f2b2afecaf…`：Exploit Weakness 改为“近战攻击命中”才降低目标物理抗性，并恢复原文末尾的 `\n\t\t`。
- `f2d8717e52…`：单项效果提示改为“效果抵抗几率”，正文明确为“完全抵抗该特定效果的几率”，不再与 Status resistance 混同。
- `f30327e69f…`：仅合并教程文本中“不\n会”“(你也可以\n根据”“还存\n在”三处错误硬换行，使译文恢复为与原文一致的 11 个 LF；其余句子不动。
- `f33c065ae5…`：思维形态说明恢复为原文 3 个 LF，续行均保留两个 TAB；补回主属性、两项副属性、三项相等属性、超距重新实体化及精神强度加成等完整含义，并沿用本库“战士 / 盾战士”和“码”，未使用“狂战士 / 大师 / 精英”。

## 源码与术语核验

实施依据为冻结的 `SOURCE-CLAIMS.json`、`SOURCE-ANCHORS.json` 与固定源码摘录。猎头者 `setTarget()` 清除目标、Exploit Weakness 仅在近战命中分支触发、单项效果抵抗提示的回退用途，以及教程和思维形态的原文行结构均与冻结证据一致。专名和技能名在 `mod-tome.lua` 中查证为“思维形态：战士 / 思维形态：盾战士”“精神体战士 / 精神体盾战士”；没有新增译名或修改术语库。

## 不变量与验证

窗口专用脚本通过全记录比较确认恰有 5 个 target 变化，其他记录字段不变；source、source_tag、args_order、printf 占位符、`%%`、markup、LF 与 TAB 均满足冻结约束。严格 lint、语义 claim 回归和 `git diff --check` 均通过，真实命令与结果记录于 `VALIDATION.json`。

## 第 1 轮修复（新会话）

依据 `ADJUDICATION-R0.json` 的唯一 confirmed finding `R0-HEADHUNTER-OVERSTATE`，将猎头者播报 target 从“`#ORCHID#你取下了 %s 的首级，令本层所有敌人迟疑，失去对你的锁定。`”逐字改为“`#ORCHID#你取下了 %s 的首级，令本层所有敌人为之迟疑。`”。本轮未修改其余 4 个 target，也未修改 source、source_tag、占位符或 markup。

修改后运行窗口专用验证、严格 lint、严格语义 claim 回归及 `git diff --check`，四项退出码均为 0。窗口验证仍确认相对冻结基线恰有 5 个 target 变化；严格 lint 检查 30308 条翻译，0 errors、0 warnings。详细命令与结果追加于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH263.json` 是 `.ai/task/repair-w17-20260923/PREFLIGHT-BATCH263.json` 的逐字节副本，SHA-256 为 `728b288e1e2e465db3636939dab01921cae0e4a62363c1c6e9f4713ed1d35fed`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w17-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `fc6e8b0cf9f11cafca377e32b0ef2aaab1f6907df10b67a652c7ec2318389873`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w17-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `44f8ae8fdd9971e203b239473f23be7b6061f5430394ad524fb9b169104024cd`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未更新 handoff。
