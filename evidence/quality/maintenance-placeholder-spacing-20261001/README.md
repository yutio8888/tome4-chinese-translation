# 技能说明占位符补空格（2026-10-01 维护）

**来由**：用户 2026-10-01 指出技能描述中的格式化占位符前后应有空格，否则升级页面预览异常。

**机制**（固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）：
`game/modules/tome/class/Actor.lua:6851` 把 `t.info()` 经 `toTString():tokenize(" ()[],")` 切分；
`game/modules/tome/dialogs/LevelupDialog.lua:1034-1050` 用 `tstring:diffWith`（`game/engines/default/engine/utils.lua:1969`）
按 token 位置逐个比较，不同的 token 整个高亮并附 `[->新值]`。切分只认 ASCII 空格、半角括号、半角逗号与换行，
全角标点不算分隔，颜色标记 `#X#` 在 `toTString` 时已拆成独立元素。因此「物理抗性，%d」「（当前加成：%d）」
「%d%%。此外……」会把整段汉字连同数字一起高亮。

**规则**（用户选定“最小必要”）：范围为 `*/talents/*` 段、`source_tag` 为 `tformat` 的译文，覆盖 11 个清扫组件。
只处理数值占位符（`%d` `%i` `%u` `%x` `%e` `%f` `%g`，可带 `%%`）；`%s` 携带名称、技能名、颜色标记前缀与文本片段
（如「%s的时空克隆体」「%s普通生物#LAST#」），不随等级变化，补空格会改动显示，故不处理。
仅当占位符所在 token 会连带汉字时，插入一个 ASCII 空格：全角闭合标点（，。、；：）等）跟随前文，
正负号与全角开括号（「（」）跟随数字。例：「%d点」→「%d 点」、「抗性，%d」→「抗性， %d」、
「加成：%d）」→「加成： %d）」、「陷阱（%d 侦查」→「陷阱 （%d 侦查」、「%d%%，持续」→「%d%%， 持续」。
只粘标点、不连汉字的（「%d%%。」行尾）不动；不在全角括号内侧加空格（与 `e24e2616` 先例一致）。

**结果**：394 条、590 个空格（mod-tome 305、tome-orcs 53、tome-cults 18、tome-ashes-urhrok 14、tome-possessors 4）。
译文提交 `a2a2d6b78682de7053383c603687f33554a2bf24`。

**守卫**（`apply.py`，仿 `tools/orchestration/sweep.py`）：改后字节经 LuaJIT 重新语义解析；条目数与顺序不变；
source/source_tag/args_order/special/section 不变；目标译文等于计划值、只多出计划位置的 ASCII 空格；
首尾空白、占位符序列、`#...#` 标记序列不变；计划外条目逐字不变；改后再扫无残留；
与改动条目同 runtime key 的范围外记录 0 条。规则无法写成 sweep.py 的全局正则（需按段、tag 与 token 判断），
故用等价守卫的专用脚本。strict lint 0 errors / 0 warnings；17 项门禁全过（`GATES-results.json`，含 12-core-addon-build）。

**catalog / migration**：新 catalog `c88df57ccaac855978d5f6b71e7e004deb1fa71f3b81c10334a8e11df2fcdd3b`，
migration `893816953fb4dfcf0b6976590fd467f11d00fe83abb7f6590db1f1cb48bf36b7`，390 条 revision_changed
（394 − Possessors 4，不在目录组件内），逐条与计划一致（`CATALOG-CHANGE-VERIFICATION.json`）。
这 390 个 successor 须重新审核，不继承旧 done，预计约 5 个批次（390/80）。
