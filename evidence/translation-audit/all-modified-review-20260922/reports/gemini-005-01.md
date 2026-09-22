# 译文复核报告：batch-005（条目 entry-00161 至 entry-00200）

## 1. 冻结哈希与核验环境核对
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-005.md`
- **预期 SHA-256**：`7a890c630970417f32b64688901b44f8fb5b1b3f3ee6d63fcc24b2264ee718cc`
- **实测 SHA-256**：`7a890c630970417f32b64688901b44f8fb5b1b3f3ee6d63fcc24b2264ee718cc`（核验一致）
- **源码参考**：依据 `evidence/translation-audit/all-modified-review-20260922/source-access.json`，本批全部 40 条条目均属于 `mod-example_realtime` 与 `mod-tome`，已通过 `git show` 读取固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下的公开源码，译文参考同 section 终点 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。本批不涉及 DLC 及尚未定位源码的 addon。

---

## 2. 逐条复核记录（共 40 条）

### entry-00161
- **位置/Section**：`mod-example_realtime.lua:19` / `mod-example_realtime/class/Game.lua`
- **原文**：`Saving game...`
- **译文**：`保存游戏…`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/example_realtime/class/Game.lua:354` 中 `self.log("Saving game...")`，无占位符与颜色码，省略号标点与日志语义匹配。

---

### entry-00162
- **位置/Section**：`mod-example_realtime.lua:25` / `mod-example_realtime/class/Player.lua`
- **原文**：`LOW HEALTH!`
- **译文**：`生命值低！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/example_realtime/class/Player.lua:105` 中 `game.flyers:add(..., _t"LOW HEALTH!", ...)`，感叹号保留，符合生命值（Health）术语规范。

---

### entry-00163
- **位置/Section**：`mod-example_realtime.lua:44` / `mod-example_realtime/data/damage_types.lua`
- **原文**：`Kill!`
- **译文**：`击杀！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/example_realtime/data/damage_types.lua:32` 中 `game.flyers:add(..., _t"Kill!", ...)`，击杀漂字提示，感叹号保留，翻译准确。

---

### entry-00164
- **位置/Section**：`mod-tome.lua:103` / `mod-tome/class/Actor.lua`
- **原文**：`#VIOLET#Following build order %s; increasing %s by 1.`
- **译文**：`#VIOLET#遵循加点顺序%s;增加一点%s。`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:838` 中 `game.log("#VIOLET#Following build order %s; increasing %s by 1.", b.name, self.stats_def[stat].name)`。颜色标记 `#VIOLET#` 与两个 `%s`（加点方案名、属性名）顺序均一致；译文分句处保留了半角分号 `;` 且无空格（`顺序%s;增加`），排版上建议使用全角分号 `；` 或逗号 `，`。

---

### entry-00165
- **位置/Section**：`mod-tome.lua:104` / `mod-tome/class/Actor.lua`
- **原文**：`#VIOLET#Following build order %s; learning talent category %s.`
- **译文**：`#VIOLET#遵循加点顺序%s;学会技能树%s。`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:860` 中 `game.log("#VIOLET#Following build order %s; learning talent category %s.", b.name, tt)`。占位符与颜色码一致，加点逻辑中 category 译为“技能树”可接受；同 entry-00164，分句处使用了未加空格的半角分号 `;`。

---

### entry-00166
- **位置/Section**：`mod-tome.lua:105` / `mod-tome/class/Actor.lua`
- **原文**：`#VIOLET#Following build order %s; learning talent %s.`
- **译文**：`#VIOLET#遵循加点顺序%s;学会技能%s。`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:880, 901` 中 `game.log("#VIOLET#Following build order %s; learning talent %s.", b.name, t.name)`。占位符与颜色码一致；同 entry-00164，分句处使用了未加空格的半角分号 `;`。

---

### entry-00167
- **位置/Section**：`mod-tome.lua:111` / `mod-tome/class/Actor.lua`
- **原文**：`#CADET_BLUE#You notice a trap (%s)!`
- **译文**：`#CADET_BLUE#你发现了一个陷阱（%s）！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:1734` 中 `game.logPlayer(self, "#CADET_BLUE#You notice a trap (%s)!", trap:getName())`，颜色码 `#CADET_BLUE#` 保留，括号与感叹号全角化，trap 符合“陷阱”术语。

---

### entry-00168
- **位置/Section**：`mod-tome.lua:136` / `mod-tome/class/Actor.lua`
- **原文**：`INVULNERABLE!`
- **译文**：`无敌！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2041` 中 `ts:add({"color", "PURPLE"}, _t"INVULNERABLE!", true)`，浮动/提示文本，感叹号保留，语义准确。

---

### entry-00169
- **位置/Section**：`mod-tome.lua:138` / `mod-tome/class/Actor.lua`
- **原文**：`\nMana:  %s%d / %d#LAST#`
- **译文**：`\n法力值：%s%d / %d#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2047` 中 `("\nMana:  %s%d / %d#LAST#"):tformat(self.resources_def.mana.color, self.mana, self.max_mana, true)`。前导换行符 `\n` 正确保留，颜色参数 `%s` 与数值 `%d / %d`、结尾 `#LAST#` 均完整匹配，Mana 符合“法力值”术语。

---

### entry-00170
- **位置/Section**：`mod-tome.lua:140` / `mod-tome/class/Actor.lua`
- **原文**：`\nVim:  %s%d / %d#LAST#`
- **译文**：`\n活力值：%s%d / %d#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2050` 中 `("\nVim:  %s%d / %d#LAST#"):tformat(self.resources_def.vim.color, self.vim, self.max_vim, true)`。前导换行、颜色占位符 `%s`、数值 `%d / %d` 及 `#LAST#` 均匹配，Vim 符合“活力值”术语。

---

### entry-00171
- **位置/Section**：`mod-tome.lua:142` / `mod-tome/class/Actor.lua`
- **原文**：`\nPositive:  %s%d / %d#LAST#`
- **译文**：`\n正能量值：%s%d / %d#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2053` 中 `("\nPositive:  %s%d / %d#LAST#"):tformat(self.resources_def.positive.color, self.positive, self.max_positive, true)`。前导换行、格式占位符与 `#LAST#` 完整，资源名翻译准确。

---

### entry-00172
- **位置/Section**：`mod-tome.lua:144` / `mod-tome/class/Actor.lua`
- **原文**：`\nNegative:  %s%d / %d#LAST#`
- **译文**：`\n负能量值：%s%d / %d#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2056` 中 `("\nNegative:  %s%d / %d#LAST#"):tformat(self.resources_def.negative.color, self.negative, self.max_negative, true)`。前导换行、占位符与 `#LAST#` 完整，资源名翻译准确。

---

### entry-00173
- **位置/Section**：`mod-tome.lua:148` / `mod-tome/class/Actor.lua`
- **原文**：`#ffa0ff#Predator: +%d acc, +%d apr#LAST#`
- **译文**：`#ffa0ff#猎杀者：+%d 命中，+%d 护甲穿透#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/Actor.lua:2073` 中 `("#ffa0ff#Predator: +%d acc, +%d apr#LAST#"):tformat(predatorATK, predatorAPR)`。颜色码 `#ffa0ff#` 与