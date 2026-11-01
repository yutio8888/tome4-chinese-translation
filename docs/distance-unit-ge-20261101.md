# 距离单位统一为「格」（2026-11-01）

用户于 2026-11-01 决定把距离单位从「码」统一成「格」，要求单独写文档、单独提交，
不混进审核或修复提交。游戏的 range／radius 都按地图格计数，所以用「格」更贴近机制。

## 范围与规则

- 文件：`engine.lua`、`mod-boot.lua`、`mod-tome.lua`、`tome-addon-dev.lua`、`tome-ashes-urhrok.lua`、
  `tome-cults.lua`、`tome-orcs.lua`。`tome-possessors.lua`、`tome-items-vault.lua` 和 `*.copy.lua` 里没有「码」。
- 替换：「码」紧跟在数量后面时改成「格」，可以隔一个空格。数量包括阿拉伯数字、printf 占位符（`%d`、`%0.1f`、`%s` 等）、
  `#VAR#` 颜色或变量标记、`}`／`)` 结尾的插值，以及 一二两三四五六七八九十几百数半。
  另外「穿越码数」改成「穿越格数」。
- 不改：密码、代码、编码、解码、起码，以及 Ashes 石板描述「码成了整整齐齐的一摞」（这里是「堆放」的意思）。
- 同一运行时键在各文件里一起改：替换只看译文文本，同一 (source, tag) 的各行替换结果相同。

## 结果（实测）

| 文件 | 替换数 |
| --- | ---: |
| mod-tome.lua | 225 |
| tome-orcs.lua | 76 |
| tome-cults.lua | 23 |
| tome-ashes-urhrok.lua | 20 |
| 合计 | 344 |

替换后，七个文件里的「码」只剩上面列出的非距离用法。叙事文本里也有六处一起改了：
「十格之外」「几格之外」「一格」「两格」。

## 验证

译文门禁子集（`tools/lite_gates.py` 的 SUBSET，覆盖 strict lint、运行键扫描与分类、术语审计、空白、严格核心构建）的
结果记录在 `evidence/lite-review/repairs/ma-to-ge-20261101/gates.json`。改动过的单元 revision 都变了，
会在轻量审核的后续批次里自动重审。
