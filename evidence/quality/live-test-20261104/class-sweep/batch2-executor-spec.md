# 全职业巡检 第二批修复（执行者规格，2026-11-07）

你是 ToME4 简体中文汉化仓库 `/workspace/tome4-chinese-translation` 的执行者，是本任务唯一的写入者。只修改译文文件 `mod-tome.lua`、`tome-orcs.lua`、`tome-cults.lua`、`tome-ashes-urhrok.lua`。**不要 git add / commit / push，不要动 evidence/、tools/、tests/、terminology/。**

输入：`/tmp/clsfix/findings-batch2.jsonl`（51 条实机测试发现）。第一批（已提交）的执行报告在 `/tmp/clsfix/report.json`，可参考其做法；本批若有与第一批重复的问题，先看当前译文是否已改好。对每条：用固定源码核实（`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/...`；DLC 源码在 `/workspace/tome4-dlcs/{orcs,cults,ashes-urhrok}/`，来源未固定，报告里注明），成立就改，不成立不改并说明理由。suggestion 只是参考。

## 硬性规则（与第一批相同）
1. 只改 target；source 与 tag 不变。改完 `python3 /tmp/srccheck.py mod-tome.lua tome-orcs.lua tome-cults.lua tome-ashes-urhrok.lua` 必须全部 identical。
2. 占位符数量与种类不变；target 换行数 = source 换行数；续行行首 TAB 保持。
3. 升级预览空格规则：tformat 技能说明里数值占位符所在 token 连着汉字时须插 ASCII 空格（「%d 点」「抗性， %d」「%d （」）。以 `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict` 0 错误为准。**因此「全角逗号/顿号后、全角括号前的空格」只要是 lint 要求的就必须保留**；只有 lint 不要求的（非数值 token、非 tformat 串）才可删。
4. 同一 source 在多个组件文件里都有条目时同步修改。
5. 原文说明与实现不符时，按实现写（用户 2026-11-02 裁决）；DLC 数值类发现先查实现（第一批里 3 条 DLC 数值就是说明与实现不符、现译贴合实现而保留的）。
6. 修改前查同类问题一并修复并在报告列出；修复要对照整条说明通读，不要只改被点名的半句。
7. 用 Edit 或 Python 精确替换；不要用 shell heredoc 写中文；不要整文件重写。

## 主代理裁决
- 不改（驳回）：
  - cls08-c3-01：ignore_direct_crits 的实现是按比例削减暴击额外伤害（第一批 cls07b-03 已核实 damage_types.lua:131-151），现译与实现一致。
  - cls09-c3-04、cls11b-c3-02、cls06-c3-04：全角标点后/全角括号前的空格是升级预览规则要求的（见规则 3）。若你发现其中某处并非 lint 要求（例如非数值 token），可以删并在报告说明。
  - cls12-c3-01：盾牌名逗号是已知插件代码问题（r8-opus-02）。
- 延后（插件代码）：cls11b-c3-01、cls06-c3-02（引擎折行拆数字，同 cls07b-07）；cls10-c2-02（装备人偶短名截断，同 r9-opus-09）；cls08-c3-03、cls06-c3-05（「抗性改变：+7% 所有」：all 是共享键，需代码侧处理，先确认 all 键的使用面，若确有安全的纯译文改法可提出但不要改）。
- advisory（需术语裁决，不改）：cls05-c1-04（Veteran 技能树「战斗经验」）。
- 其余全部按核实结果修：cls05-c1-01/02/03（任务标题可用「蛇形入侵者」）、cls05-c2-01（若第一批已修则标 already_fixed）、cls05-c2-02（Light radius 统一，按库内多数）、cls05-c3-01/02、cls08-c1-01/02/03、cls08-c2-01..05、cls08-c3-02、cls10-c1-01（先查 friendlyfire）、cls10-c1-02、cls10-c2-01（先查实现是否按百分比）、cls10-c2-03/04/05、cls10-c3-01/02/03、cls12-c1-01（先查实现）、cls12-c1-02、cls12-c2-01/02/03（先查实现）、cls12-c3-02/03、cls09-c3-01/02/03/05、cls11b-c2-01（恢复源串空格，tome-orcs.lua 同键同步）、cls11b-c3-03、cls06-c3-01（键名颜色码后首字符被吞：恢复英文的单引号包裹写法）、cls06-c3-03。
- 「半径」语序（cls08-c3-02、cls09-c3-05、cls12-c3-02）：统一为「半径 %d 格」，同类全库检查。

## 完成标准与报告
- lint strict 0 错误；srccheck 全部 identical；`git diff --check` 无输出。
- 写 `/tmp/clsfix/report2.json`：数组，每条 `{"id","status": "applied|rejected|deferred|advisory|already_fixed","files":[...],"old","new","note"}`；同类扩展另列 `{"id":"<原id>+similar",...}`。
- 最终回复只写一行：`EXECUTOR clsfix2 DONE applied=<n> rejected=<n> deferred=<n>`。
