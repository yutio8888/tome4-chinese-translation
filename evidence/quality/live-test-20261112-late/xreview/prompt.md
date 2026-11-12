# ToME4 汉化：两条实机发现的独立复核（只读，有界）

你是独立复核者。只读以下文件，不修改任何文件，不做 git 操作。对每条发现给出 **成立 / 部分成立 / 不成立**，并附简短理由（引用文件:行号）。不要扩展到其他条目。

译文库（格式 `t("英文", "中文", "标签")`）：/workspace/tome4-chinese-translation/mod-tome.lua、tome-orcs.lua
游戏源码：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/class/Object.lua`

## 发现 A
- 界面：Embers 物品「飞行背包」提示中「当使用或装备时」一段显示「避免压力陷阱：  该物品可防止装备者触发压力式陷阱。」
- 位置：mod-tome.lua 约 958 行 `t("Avoid Pressure Traps: ", "避免压力陷阱： ", "_t")`。源码 Object.lua:1932 把标签与说明直接拼接。
- 主张：全角冒号后保留了英文的半角空格，与同一提示框中其他标签（如「移动速度：」）不一致。
- 请判断：这是否为格式缺陷？同族标签（约 948–960 行的 "Blind-Fight: "、"Lucid Dreamer: "、"Quick Weapon Swap:" 等）的现状如何？若要修，应只改这一条，还是全族统一？

## 发现 B
- 界面：Embers 物品「便携式自动材料提取仪」提示。标题和用途行写作「便携式自动材料提取仪」「提取仪」，说明正文却以「APE 是一个多功能工匠工具箱……」开头。
- 位置：tome-orcs.lua 约 1140 行（英文 "The APE is a multifunction tinker toolbox…"）；相邻 1145–1149 行都用「提取仪」或全称。
- 主张：正文保留英文缩写 APE，玩家无法对应到物品名，与相邻条目用词不一致。建议改为「提取仪是……」，或首次出现写作「便携式自动材料提取仪（APE）」。
- 请判断：是否成立？哪种改法更合适？

## 产出
写 /tmp/xreview-late/result.md，每条发现一节，写明结论与理由。最终回复只写一行：`XREVIEW DONE A=<成立|部分成立|不成立> B=<…>`。
