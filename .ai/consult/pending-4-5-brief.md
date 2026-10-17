# 咨询议题：两条跨批次待裁定的译法规则

你是 ToME4 简体中文本地化项目的外部顾问。本项目对 `game/engines/default`（引擎，
pinned `commit:624a6732`，本机路径 `/workspace/t-engine4`）与 ToME 模块的译文做逐条审核。
译文catalog在仓库根的 `engine.lua` / `mod-boot.lua` / `mod-tome.lua` 等文件里，
格式为 `t("<源文>", "<译文>", "<tag>")`。

**全程只读。禁止修改、创建、删除任何仓库文件，禁止 git 操作。**
（当前有一个进行中的审核批次，任何写入都会破坏它。）

请对下面两个议题各给出一个**可直接执行的规则**，并说明理由与边界情形。

---

## 议题 4：按键提示里的字母大小写

### 现状样例（译文）
```
mod-tome.lua:2320  t("Press 'm' to setup", "按M键设置", "_t")
mod-tome.lua:2491  t("Press 'm' to setup", "按M键设置", "_t")
mod-tome.lua:237   t("Press p to use them.", "请按 p 使用它们。", "_t")
mod-tome.lua:1036  t("Press <control> to compare", "按住 <Ctrl> 键比较", "_t")
engine.lua:1287    t("You may define a hotkey by pressing 'm' and following the instructions there.",
                     "你可以按m键打开按键绑定窗口，遵循上面的指示绑定按键。", "_t")
engine.lua:1259    t("Tactical display disabled. Press shift+'t' to enable.", "战术视图关闭。请按Shift+'t'启用。", "_t")
engine.lua:1264    t("Tactical display enabled. Press shift+'t' to disable.", "战术视图启用。请按Shift+'t'关闭。", "_t")
engine.lua:710     t("      Press a key (escape to cancel, backspace to remove) for: %s",
                     "      请按键（ESC键取消，退格键删除） 以绑定 %s 的键位", "tformat")
```

### 事实依据
引擎的键位绑定格式是 `sym:=<键>:<shift>:<ctrl>:<alt>:<meta>`，同一个字母键**带 shift 与不带 shift
是两个不同绑定**。例如 `game/engines/default/data/keybinds/interface.lua:28`：

```lua
default = { "sym:=h:false:false:false:false", "sym:=m:true:false:false:false" },
```

即 `h`（不带 shift）与 `Shift+m` 绑定到同一动作。其他例子里 `sym:=e:false:true:...` 是 Ctrl+E，
`sym:=e:false:false:...` 是纯 E——同一字母在不同 modifier 下含义完全不同。

### 问题
译文把源文的小写 `'m'` 统一写成「按M键」。在一个 shift 有独立含义的键位系统里，
把小写渲染成大写有让玩家误按 Shift 的风险；但中文语境里「按M键」比「按m键」更常见、更易读，
且源文自身大小写也不完全一致（`'m'`、`p`、`shift+'t'`、`<control>`）。

### 请回答
1. 规则该是「严格保留源文大小写」「一律大写」「一律大写但 modifier 显式写出」还是别的？
2. `<control>`、`escape`、`backspace`、`Enter` 这类具名键怎么统一（`<Ctrl>`？「ESC 键」？）？
3. 「按X键」「按 X 键」「请按 X」——空格与句式怎么定？
4. 给出上面 8 条样例按你的规则改写后的完整译文。

---

## 议题 5：`Physical/Spell/Mental save:` 的「加成」

### 现状样例（译文）
```
mod-tome.lua:854  t("Physical save: ", "物理豁免加成：", "_t")
mod-tome.lua:855  t("Spell save: ",    "法术豁免加成：", "_t")
mod-tome.lua:856  t("Mental save: ",   "精神豁免加成：", "_t")
```
对照组（同一批文件里不带「加成」的写法）：
```
mod-tome.lua:350-352  t("Physical save", "物理豁免", "_t") / t("Mental save", "精神豁免") / t("Spell save", "法术豁免")
mod-tome.lua:2365-67  t("P. save:", "物理豁免：", "_t") 等
mod-tome.lua:159-163  t("#0080FF#P. save#FFFFFF#:  ", "#0080FF#物理豁免#FFFFFF#：", "_t")
```

### 事实依据：这条 runtime key 有两个调用点，值都可能是负数

**调用点 A**——`game/modules/tome/class/Object.lua:1771-1773`，装备对比面板：
```lua
compare_scaled(w, compare_with, field, "combat_physresist", {"combatPhysicalResist", true},
               _t"%+d #LAST#(%+d eff.)", _t"Physical save: ")
compare_scaled(w, compare_with, field, "combat_spellresist",  ..., _t"Spell save: ")
compare_scaled(w, compare_with, field, "combat_mentalresist", ..., _t"Mental save: ")
```
格式串是 `%+d`，显式带符号；对比另一件装备时差值可以是负数。

**调用点 B**——`game/modules/tome/dialogs/LevelupDialog.lua:883 / 907 / 910`，加点收益预览：
```lua
text:add(_t"Physical save: ", color, ("%0.2f"):format(diff * 0.35), dc, true)
```
`diff` 是本次分配的属性点变化量，**退点时为负**，于是显示「物理豁免加成：-0.70」。

### 问题
`save` 本身是属性名，源文的标签是中性的「物理豁免：」；译文加的「加成」在负值时自相矛盾。
但直接删「加成」会与 `mod-tome.lua:350-352` 等已有的纯属性名条目在界面上失去区分度吗？

### 请回答
1. 该不该删「加成」？如果删，`mod-tome.lua:854-856` 与 `2365-2367` 变成同名重复，有没有问题？
2. 有没有比「物理豁免：」更好的中性表述（例如「物理豁免变化：」「物理豁免：」+ 保留符号）？
3. 同源的 `Physical power: `、`Stealth bonus: `、`Trap disarming bonus: `、`Maximum encumbrance: `
   这一族标签，源文有的带 bonus 有的不带，中文该不该跟随源文区分？给出统一判据。
4. 给出 `mod-tome.lua:854-856` 三条的最终译文。

---

## 输出格式
用中文，Markdown，两个议题分开。每个议题给：**结论规则**（一句话）、**理由**、**边界/例外**、
**改写后的译文清单**。不要泛泛而谈，要落到可以直接抄进 catalog 的字符串。
