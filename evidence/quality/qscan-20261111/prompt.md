# ToME4 简中汉化：机械扫描候选核实（只读）

你在核实《马基埃亚尔的传说》(ToME4 1.7.6) 简体中文译文的疑点。**只读**：不得修改任何仓库文件，不 git 写操作；草稿写 /tmp/qscan/LANE/scratch/。

## 输入
`/tmp/qscan/LANE/cand.jsonl`，每行一条：`n` 编号、`f` 译文文件、`sec` 源文件段、`tag` 用途、`en` 英文原文、`zh` 当前译文、`flags` 脚本标出的疑点。
脚本只做了粗筛（数字对不上、引用的技能名没出现、may/chance/up to/at least/not 等限定词或否定在中文里找不到对应字），**大部分是误报**。例如：中文用「一半」「两倍」「破釜沉舟」等写法表达了同样意思、数字写成汉字、限定词换了说法、技能名在该处本来指别的东西（物品名、召唤物名）、否定用「免于」「防止」表达等，都不算问题。

## 判定
逐条读英文与中文，判断译文在该点是否真有缺陷：
- 数值、范围、半径、回合数、百分比、对象与英文不符，或漏掉了带数字的成分；
- 删掉了 may / chance / up to / at least / only / each 等限定，把不确定说成必然、把上限说成定值；否定被丢失或反转；
- 引用的技能／状态名与库内正式译名不一致，导致玩家对不上（先在译文库查该名的正式译法：`/workspace/tome4-chinese-translation/mod-tome.lua`、`tome-*.lua` 中 `t("名称", "译名", "talent name")` 等；术语库 `terminology/*.tsv` 的 preferred 行为定稿）。
发现候选指向的问题之外、同一条里明显的其他错误（误译、漏译、病句）也一并报告。

机制有疑问时查固定版本源码：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/<路径>`（sec 的 `mod-tome/...` 对应 `game/modules/tome/...`，`engine/...` 对应 `game/engines/default/engine/...`）；DLC 在 `/workspace/tome4-dlcs/<orcs|cults|ashes-urhrok>/`（来源未固定，引用注明）。**原文与实现不符时，译文按实现写是有意的，不算错。**

## 不要报告
- 数值占位符与汉字／全角标点之间的 ASCII 空格（升级预览需要，故意保留）。
- 维护者已定译法：Archmage＝元素法师、Parry＝招架、Exhaustion＝力竭、Fatigue＝疲劳值、regain Equilibrium＝降低失衡值、致命一击！、_t"her"＝「她的」、「(%d 护盾吸收)」短格式、徒手伤害也称「武器伤害」、yeek＝夺心魔、The Master＝领主、maim＝断筋、Quiver 栏位＝弹药栏、Combat Veteran＝战斗经验。
- 纯文风偏好、中英都通顺且意思一致的意译。

## 产出
写 `/tmp/qscan/LANE/findings.json`：数组，每条
`{"n":编号,"f":"文件","sec":"…","en":"相关英文片段","zh":"当前译文相关片段","type":"mistranslation|omission|qualifier|number|name|grammar","severity":"major|minor","issue":"中文说明","evidence":"源码路径:行号或库内出处","suggestion":"该条完整的建议译文（保留全部占位符、颜色码、换行与续行 TAB；只改有问题的部分）"}`。
确认无问题的不写。写 `/tmp/qscan/LANE/coverage.txt`：一行 `read=<核完数>/<总数>`。
最终回复只写一行：`QSCAN LANE DONE findings=<n> read=<核完数>/<总数>`。
