# 宿主说明：f0a2 两条 workset 内旧缺陷一并修复

FINAL f0a2（Opus 5.5）对两条 workset 条目报出与本窗口裁决无关、但经源码确认的一级缺陷。二者都在本窗口已修改的条目内，v2 FINAL 有任何 ISSUE 即失败，记 advisory 不能让 FINAL 通过；宿主判 confirmed，合并为一次 execute-02 修复，不增加条目。

- `9af7773a4c`（科技法师进阶说明，tome-orcs/data/talents/uber/mag.lua）：Arcane Dynamo tinker schematic 译“奥术发电机插件配方”，Steamtech/Physics、Steamtech/Chemistry 译“蒸汽/物理系”“蒸汽/化学系”；本库 tinker＝蒸汽工具（术语 items.tsv 与本窗口 #41）、技能树名作“蒸汽科技/物理”“蒸汽科技/化学”（tome-orcs.lua:300、483）。A.P.E. 缩写未译属本库一贯写法（1140–1150 均不带缩写），记 advisory 不改。
- `b7abfa6898`（梅塔什对话，tome-orcs/data/chats/metash.lua:41）：漏 across the peninsula、for our sakes，增译“算了，”；按「修复对照整句」一并补回 may be the only way、appears to be stalling 两处限定。

窗口 47a 的教训是扩范围会引出长尾；本窗口仅修 reviewer 点名且源码确认的条目，不主动扩大到其他条目。
