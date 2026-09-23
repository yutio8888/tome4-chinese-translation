# 修复窗口 16 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 7 个 target，并写入本 evidence 目录；source、section、source_tag、args_order、printf 占位符、`%%` 与 markup 均未改变。除任务明确要求恢复的 50 级提示段间空行和星辰契约双 TAB 缩进外，LF 与 TAB 保持冻结 target 基线。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `f14a476f19…`：恢复祝贺句后的段间空行；改为“勇敢地向前并取得胜利”，同时移除原文没有的“最终”。
- `f15f5593c7…`：将原因恢复为“你与它的羁绊之强”；明确光辉引力把范围内敌人拉向被击中的目标；补回 `all damage` 与命中触发语义；全部非空续行恢复两个前导 TAB，并保持 `50%%`、`0%%` 与 `#GOLD#…#LAST#`。
- `f18f9a4e90…`：逐句核对不死猎人指南。恢复“通常持械、有时甚至披甲”、用冰冷钢铁对付吸血鬼、总是得到同样回答、雪巨人问句、众头颅尖叫着要猎人流血，以及巫妖远比传说可怖；删除“刺穿喉咙”“力量象征”等增译并恢复骨巨人句的原因果。紧邻句中明显增删一并修复：骷髅段删除原文没有的粗俗语气与走路描写，吸血鬼段恢复结盟和家族关系及统治低等不死生物的因果，骨巨人段删除“法师老头”等增译，巫妖能力句删除原文没有的“无数”。“野性纹身”保持不变。
- `f19cec2641…`：改为“我往这瓶里加了点好料，不过明早可有你受的”；wife 句保持条件和时序，专名使用库内“堕落印记：清除”。
- `f1e389dfae…`：恢复“以自身为祭品关闭虚空传送门”。
- `f20e44ef63…`：按同族死讯句式改为“牺牲了%s，将维网带给众生”，`%s` 恰一个。
- `f22305679e…`：Venomous 改为“自然伤害”，其余数值、占位符和各行保持。

## 固定源码补查

仅用 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查了 7 条对应源码，以及 `celestial/combat.lua:99-105` 的光辉引力调用。`projectCollect` 与 `pull(target.x, target.y, 5)` 均以被击中目标坐标为中心；其他结果与冻结 `SOURCE-ANCHORS.json`、`SOURCE-CLAIMS.json` 一致。

## 不变量与验证

任务专用 `verify.py` 在最终候选上真实运行两次，均在 target 换行绝对相等断言处退出 1。脚本要求所有 target 的 LF/TAB 与旧 target 逐项相等，但 SPEC 同时明确要求为 `f14a476f19…` 新增段间空行，并把 `f15f5593c7…` 的空格缩进恢复为双 TAB；因此不能在不撤销明确修复或修改禁止写入的 `.ai` 脚本的情况下通过。

补充的只读有界全记录诊断使用与专用脚本相同的 `LocaleLoader` 比较 22,989 条记录，并只对上述两个明确授权结构变化设例外：结果确认恰有 7 个 target 改变，所有其他记录字段不变，printf 占位符、markup 与 at-token 不变；`f14a476f19…` 仅 target LF 增加 1，`f15f5593c7…` 的换行数不变且首行之后每个非空行均以两个 TAB 开头，其他 5 条 LF/TAB 不变。严格 lint、语义 claim 回归和 `git diff --check` 均通过。真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH262.json` 是 `.ai/task/repair-w16-20260923/PREFLIGHT-BATCH262.json` 的逐字节副本，并与其 `.artifacts` 来源逐字节相同；SHA-256 为 `5bc8dc89fa6882b7de5a33711b0940bfe73ff1521058506e2285d876bd3319d2`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w16-20260923/WORKSET.json` 的逐字节副本；SHA-256 为 `e89e742e6b2f2d7f860dc1b713005ede99e9236e7466a13b1313c8f010abae9f`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w16-20260923/SOURCE-ANCHORS.json` 的逐字节副本；SHA-256 为 `4f0f5a18b7ededb6133aacad42213e4fe2cdef4ab186941671ed3e7ae50c27dd`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。专用 verifier 的 SPEC 冲突需由宿主裁决或修正；独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续。本执行未 stage、commit、queue、catalog/migration 或 push，也未更新 handoff。

## 换行不变量补修（新 EXECUTOR 会话）

宿主确认 `f18f9a4e90…`（不死猎人指南）的一级换行不变量缺陷后，本次仅调整该 target 的物理段落边界：将尸妖段 1 处、吸血鬼段 2 处、幽灵段 3 处、巫妖段 1 处被额外拆开的段落并回对应原文段落，共删除 7 个额外段落边界（14 个 LF）。合并未改动任何译文字词，也未触碰其余 6 个 target；各段落、空行及 `    * * *` 分隔行位置现与固定源码逐项一致，source 与 target 均为 72 个 LF。

宿主更新后的专用 verifier 已通过：比较 22,989 条记录，确认仍恰有冻结 workset 的 7 个 target 相对基线变化，并逐条验证 source/target 的 LF 与 TAB、printf 占位符、markup 和 at-token 不变量。本次随后运行严格 lint（30,308 条，0 errors、0 warnings）、语义 claim 回归及 `git diff --check`，均退出 0。此前记录的 verifier 失败属于补修前历史结果，已由本次通过结果取代；本会话仍未 stage、commit、push，未写 `.ai`，也未修改规则、工具、术语库、handoff、catalog 或 migration。

## 二级署名消歧补修（第 2 轮新 EXECUTOR 会话）

依据 `ADJUDICATION-F1.json` 中宿主确认的 `F1-UNDEAD-HUNTER-BYLINE`，本次仅将 `f18f9a4e90…` target 首行从“`#{italic}#一名不死猎人的指南 作者：阿斯拉伯·波利斯#{normal}#`”改为“`#{italic}#一名不死生物猎人的指南 作者：阿斯拉伯·波利斯#{normal}#`”，消除“不死的猎人”歧义。标记、空格、换行以及该条其余文字均未改变；其余 6 个冻结 target 和 `mod-tome.lua:11440–11441` 的窗口外 lore 标题未修改。

任务专用 verifier 比较 22,989 条记录，确认相对冻结基线仍恰有原 workset 的 7 个 target 发生变化，全部不变量通过。严格 lint 检查 30,308 条译文，结果为 0 errors、0 warnings；语义 claim 回归和 `git diff --check` 也均退出 0。本会话只修改授权的 `mod-tome.lua` 行及本 evidence 目录中的 `IMPLEMENTATION.md`、`VALIDATION.json`，未 stage、commit、push，未写 `.ai`，未改术语库、规则、工具、handoff、catalog、migration 或 `pending-user-review.md`，并保留既有无关 untracked 文件。
