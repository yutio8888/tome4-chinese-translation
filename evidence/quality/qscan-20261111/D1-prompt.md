# 同一英文、不同译文的一致性核实（只读）

**只读**：不得修改仓库文件，不 git 写操作；草稿写 /tmp/qscan/D1/scratch/。

输入 `/tmp/qscan/D1/cand.jsonl`：每行一个英文串 `en`，以及它在译文库中的全部条目 `variants`（文件 f、源文件段 sec、用途标签 tag、译文 zh）。引擎按（tag, 英文）查表，所以不同 tag 的条目会分别显示。

逐组判断：译法不同是**合理的语境区分**（例如 entity keyword 与 talent type 含义不同、日历月份名与技能名、生物类型与状态子类型），还是**同一事物在玩家眼中被叫成两个名字**（例如某状态效果的名称与产生它的技能名不一致、同一句对话在不同对话树里措辞不同、同一物品名两种写法）。必要时查源码确认各条目的实际用途：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/<路径>`（sec 的 `mod-tome/...` 对应 `game/modules/tome/...`），DLC 在 `/workspace/tome4-dlcs/`（来源未固定）。术语库 `/workspace/tome4-chinese-translation/terminology/*.tsv` 的 preferred 行为定稿；notes 里写明「不按本行」「另一技能」等语境区分的，按其说明不报。

维护者已定译法不报：Archmage＝元素法师、Parry＝招架、Exhaustion＝力竭、Fatigue＝疲劳值、yeek＝夺心魔、The Master＝领主、maim＝断筋、Quiver 栏位＝弹药栏、Combat Veteran＝战斗经验；官方译名只在误译、撞名、专名冲突时才改。

写 `/tmp/qscan/D1/findings.json`：数组，每条 `{"n":编号,"en":"…","keep":"应保留的译法","change":[{"f":"文件","sec":"…","tag":"…","old":"现译","new":"建议"}],"issue":"为什么玩家会混淆","evidence":"源码/术语库出处"}`。合理区分的不写。写 `/tmp/qscan/D1/coverage.txt`：`read=<n>/<总数>`。最终回复只写一行：`D1 DONE findings=<n> read=<n>/<总数>`。
