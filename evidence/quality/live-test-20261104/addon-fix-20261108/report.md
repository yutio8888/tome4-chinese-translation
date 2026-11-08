# addonfix 执行报告（EXECUTOR，2026-11-08）

工作目录：`/workspace/tome4-chn-mod`。没有 git add/commit/push，没有改 `data/locales/zh_hans.lua`，也没有改 `/workspace/tome4-chinese-translation`。
固定源码：`/workspace/t-engine4` 的 624a67329fe2（下称「固定源码」）。DLC 源码：`/workspace/tome4-dlcs`，**来源未固定**。
官方 locale 比对用的是 `~/tome-live/t-engine4-linux64-1.7.6` 里的 te4／tome／三个 DLC 包，解压到 `/tmp/addonfix/off/`，只用来查哪些键已经存在。

## 改动文件（13 个）

| 文件 | 状态 | 对应项 |
|---|---|---|
| `data/chn_supplement.lua` | 新增 | 0（补充词条，共 22 条） |
| `hooks/load.lua` | 修改 | 0、3（K）、6（A）、8 |
| `superload/mod/class/Store.lua` | 新增 | 1（B） |
| `superload/mod/class/NPC.lua` | 新增 | 2（D） |
| `superload/engine/dialogs/ShowAchievements.lua` | 新增 | 4 |
| `superload/mod/dialogs/ShowAchievements.lua` | 新增 | 4（偏离：见下文） |
| `superload/mod/dialogs/Chat.lua` | 新增 | 5 |
| `superload/engine/interface/PlayerRun.lua` | 新增 | 7 |
| `superload/engine/dialogs/KeyBinder.lua` | 新增 | 9 |
| `superload/mod/class/Object.lua` | 新增 | 11（E）、13（L）、16（F） |
| `superload/mod/dialogs/CharacterSheet.lua` | 新增 | 12（J） |
| `superload/mod/dialogs/UseTalents.lua` | 新增 | 14（G/H/H.Key） |
| `superload/mod/class/Party.lua` | 新增 | 15（C） |

（10 战役名只改补充词条，不涉及代码文件。）

新文件的换行和现有文件一致，用 CRLF；`hooks/load.lua` 也保持 CRLF。现有 superload 文件都没有 GPL 头，所以新 superload 文件的 GPL 头照抄的是 `init.lua` 头部的 20 行。

所有包装都满足以下几点：
- 用 `rawget(_M, "__chn_*")` 做防重复包装标记。不用普通字段，是因为单基类继承的子类会经 `__index` 读到父类的标记：mod 的 ShowAchievements 继承自 engine 的 ShowAchievements，用普通字段就会误判为已包装。
- 任何临时替换都用 pcall 保护并恢复原值。
- 新增键查不到时（英文 locale）直接走原行为。

## 逐项说明

### 0 基础设施
- 新增 `data/chn_supplement.lua`，写法仿 `null_translation.lua`：`locale "zh_hans"` 加 `t(...)`。在 `hooks/load.lua` 中紧接 null_translation 之后 `I18N:loadLocale("/data-chn-mod/chn_supplement.lua")`。
- 依据：固定源码 `engine/I18N.lua` 的 `set()` 会同时写 tag 表和 `"nil"` 兜底表。`_t(s, tag)` 默认 tag 是 `"_t"`，`tformat` 用的 tag 是 `"tformat"`，查不到时都会落到 `"nil"` 表。
- **与 SPEC 和报告的不一致（F 分隔符）**：SPEC 写的是 `_t(", ", "short_name sep")`，但官方 tome 和 Ashes 的 locale 里已经有 `t(", ", "，", "_t")`。如果再加一个 `", "` 条目，会把兜底表的值改成「、」，波及所有走兜底的 `", "`；而如果不加条目，`_t(", ", "short_name sep")` 又会返回「，」。所以改用独有键 `", ##short_name"`，查不到时回退到 `", "`。
- 同理，按键分组名用独有键 `"<Group>##keybind_group"`，查不到时回退 `_t(<Group>)`。这样 Debug、Interface、Party 等通用英文词不会进兜底表。
- 自然句条目在固定源码和三个 DLC 中都 grep 过，没有其他同字面量用法：`Once freed, twice shy.`（DLC 内 2 处，都在 orcs 的 `worlds.lua`）、4 条中断原因（只出现在 `PlayerRun.lua` 的 runCheck）、翻页教学（只出现在 `Player.lua:1332`）。
- `Orcs`、`Infinite`、`Arena` 在固定源码和 DLC 中只作为 world 名或 `isDescriptorSet`／`isCampaign` 的参数出现，没有 `_t"Orcs"`、`_t"Arena"`、`_t"Infinite"`。
- 所有 `ToME:load` 修补集中在 `hooks/load.lua` 末尾的一个回调里。

### 1 B 商店标题
- `superload/mod/class/Store.lua` 包装 `interact(who, name, ...)`：`name` 为空时传入 `_t(self.name, "entity name")`。
- 源码：mod `class/Store.lua:279-293` 的 `interact` 最后调 `Store.interact(self, who, name)`；engine `Store.lua:122-124` 是 `("Store: %s"):tformat(name or self.name)`。官方 engine locale 已有 `"Store: %s"`→「商店：%s」（tformat），以及 `"sword smith"`→「铸剑师」（entity name）。
- 与报告一致。报告说的是 superload `mod/class/Store`，mod 版确实自己定义了 `interact`，所以包装 mod 版。

### 2 D 裸 emote
- `superload/mod/class/NPC.lua` 包装 `doEmote(text, ...)`：`text` 是字符串时先 `_t`。
- 源码：mod `class/NPC.lua:77-81`（emote_random）和 `:438`（doEmote）。DLC 里只有 `john-surrender.lua:81` 一处直接调用，用的是已经 `_t` 过的串，再 `_t` 一次没有影响。

### 3 K 疯狂值 `%%`
- `hooks/load.lua` 的 `ToME:load` 遍历 `ActorResource.resources_def`。对有函数型 `status_text`、但没有 `CharacterSheet.status_text` 的资源，补一个版本：`pcall(string.format, text)`，失败时原样返回。
- 源码：
  - Cults 的 `CultsDLC.lua:47-52` 返回 `("%d%%%% (%d%%%% chaotic)"):tformat(...)`，结果是 `"100%% (50%% chaotic)"`；
  - mod `CharacterSheet.lua:655-657` 优先用 `CharacterSheet.status_text`；
  - `Minimalist.lua:894` 的注释写明需要再 format 一次；
  - 核心里的 equilibrium（`resources.lua:85/113`）和 paradox（`:179/204`）都自带 CharacterSheet 版本，不受影响。
- 实际受影响的只有 insanity；推广到全部资源也安全，因为有 pcall 回退。回调可以重复执行：第二次时 CharacterSheet 版本已存在，会跳过。

### 4 成就分类
- **与 SPEC 不一致**：ToME 有自己的 `mod/dialogs/ShowAchievements.lua`，它单基类继承 engine 版并**重写了 `generateList`**（第 26 行）。只包装 engine 版，ToME 的成就界面不会生效。因此 engine 版和 mod 版两个文件都包装了，对 `self.list[i].category` 做 `_t`。
- 现有条目通过兜底表就能命中：`Embers of Rage`→余烬怒火、`Forbidden Cults`→禁忌邪教、`Ashes of Urh'Rok`→乌鲁洛克之烬。

### 5 立绘名牌
- `superload/mod/dialogs/Chat.lua` 包装 `getActorPortrait`。返回的是新建实体（既不是 actor 本身，也不是 replace_display），且 `e.name == src.name` 时，改为 `_t(e.name, "entity name")`。
- 源码：mod `dialogs/Chat.lua:87-157` 有多处 `Entity.new{name=actor.name,...}`；`dialogs/elements/ChatPortrait.lua:33` 调 `getName`；engine `Entity:getName`（`Entity.lua:164`）返回原名；ToME `Actor:getName`（`Actor.lua:2003`）就是 `_t(self.name, "entity name")`。
- 没有用 `src:getName()`，因为物品的 `getName` 会带数量和 add_name。用 `_t` 与 Actor 的结果完全相同。

### 6 A locked_desc
- `ToME:load` 遍历 `Birther.birth_descriptor_def.class`／`.subclass`，对函数型 `locked_desc` 包一层 `_t`，用 `d.__chn_locked_desc` 防重复包装。补充词条加 `"Once freed, twice shy."`→「一朝获释，再难轻信。」（tag `_t`）。
- 源码：orcs `data/birth/worlds.lua:145-148/168-171`（来源未固定）事后替换了 `locked_desc`；`OrcCampaign.lua:83` 在 Orcs 的 `ToME:load`（`hooks/load.lua:23`）里加载 `worlds.lua`。
- 加载顺序依据：engine `Module.lua:436` 按 weight 升序排列 addon，`loadAddon` 按这个顺序把 hooks 放进 hooks_list。本插件的 weight 是 999999，所以 hook 绑在 DLC 之后。

### 7 自动探索中断原因
- `superload/engine/interface/PlayerRun.lua` 包装 `runStop(msg, ...)`：`msg` 是字符串时先 `_t`。
- 源码：engine `PlayerRun.lua` 的 runCheck 返回 6 种裸字面量（第 266-360 行）：
  - `terrain changed ahead`、`terrain ahead blocks`、`terrain change on left side`、`terrain change on right side` 在官方 locale 中缺失，已新增：前方地形变化、前方被地形阻挡、左侧地形变化、右侧地形变化；
  - `terrain change on the left/right` 在官方 engine locale 中已有：左侧地形变化、右侧地形变化。
  - ToME `Player:runCheck`（1207 行起）返回的原因都已经 `_t` 过。
- 说明：ToME 的 Player 多基类继承，`PlayerRun.runStop` 会在 Player 加载时复制过去。superload 在 PlayerRun 首次 require 时就已执行，早于这次复制，所以复制到的是包装后的版本。`Actor:runStop` 是空函数，被后面的 PlayerRun 覆盖，这一点与原游戏行为一致。
- 注意：日志格式串 `"Ran for %d turns (stop reason: %s)."` 在官方 engine locale 里是「自动探索了%d回合」，在本插件里是「奔跑了%d回合…」。本次没有动。

### 8 裸字面量弹窗
- `hooks/load.lua` 包装 `engine.ui.Dialog.simplePopup` 和 `simpleLongPopup`：字符串型的标题和正文做 `_t`，tstring 保持不变。用 `Dialog.__chn_simple_popups` 防重复包装。
- 源码：engine `ui/Dialog.lua:110/127` 的签名是 `(title, text, ...)`；mod `Player.lua:1329-1335` 的 hotkeyPageTutorial。
- 补充词条加标题「快捷栏翻页」和正文（原样保留 4 行、`#{bold}#`／`#{normal}#` 和 Page.Up/Page.Down 键名）。正文的键用 `[[...]]` 原样复制。

### 9 按键绑定分组
- `superload/engine/dialogs/KeyBinder.lua` 包装 `generateList`：用 `node.nodes[1].k.group` 取原始组名，显示名取独有键或 `_t(cap)`；显示名相同的组合并后重新排序。
- 源码：engine `dialogs/KeyBinder.lua:227-236`。组名清单从固定源码 `data/keybinds/*.lua` 和 tome 的 `keybinds/tome.lua` 收集（DLC 中没有 defineAction）：action、actions、debug、hotkeys、interface、inventory、microtransactions - cosmetic、movement、party、user chat，以及 `move.lua:143-161` 的 4 个 `_t"movement"`。
- 已有译文：Action→动作（插件）、Actions→行为、Hotkeys→快捷键、Inventory→物品栏、Movement→移动（entity name 兜底）、movement→移动。
- 新增：调试、界面、队伍、用户聊天、微交易 - 外观。
- 「移动」两组会合并（在 harness 里验证过）。Action（动作，2 个绑定：自动技能、自动确认目标）和 Actions（行为）保持两组，不合并。

### 10 战役名
- 补充词条加 `Orcs`→余烬怒火、`Infinite`→无尽地下城、`Arena`→竞技场，tag 都是 `birth descriptor name`。
- 源码：mod `Game.lua:818/834` 的 `_t(player.descriptor.world)` 会经兜底表命中。`Maj'Eyal` 已有（马基·埃亚尔）。
- 无尽地下城、竞技场取自 `mod-tome.lua` 现有的 display_name 译文（`:3877` 和 `:3884`），Orcs 用 SPEC 指定的译名。
- 存档描述在存档时生成，旧档要重新存一次。

### 11 E 盾牌逗号
- `Object.lua` 包装 `getName(...)`：`_t(add_name, "entity add_name")` 与原值不同时，临时 `self.add_name = tr`，pcall 调原函数，然后用 `rawset` 恢复**原始的 raw 值**（继承来的字段恢复为 nil，不留下自有字段），出错时重新抛出。
- 补充词条：`" (#ARMOR#, #SHIELD#)"`→`" (#ARMOR#，#SHIELD#)"`。
- 源码：mod `Object.lua:592-596`（固定源码行号）。

### 12 J 装备组
- `superload/mod/dialogs/CharacterSheet.lua` 包装 `init`，在原 init 之后：
  - `self.equip_set` 规范为英文 `"off"`／`"main"`，逻辑与原第 63 行相同，只是去掉了 `_t`；
  - 重设 `c_equipment.generate`，标题改为 `tformat(_t(self.equip_set))`；
  - 重写 `on_change`，照抄第 66-79 行，日志参数改为 `_t(self.equip_set)`；
  - 最后调一次 `generate()`。
- 只有在 `c_equipment` 存在且有 generate／on_change 时才动，否则维持原行为。
- 源码核对：`updateEquipDollRefs` 只在第 72 行（on_change）和第 470 行（ShowEquipInven 的 switchSets）被调用，init 期间不会调用，所以 init 之后再规范化是安全的。现有译文：main→主用、off→备用（插件）。

### 13 L 物品「所有」
- `Object.lua` 包装 `getTextualDesc`：调用期间把 `_G._t` 换成拦截版，`s=="all"` 且 tag 为 nil 或 `"_t"` 时返回 `_t("all##item_property")`（「全部」）。pcall 之后无论成功失败都恢复。
- 能这样做的依据：engine `class.lua:27-50` 的 module 环境 `__index=_G`，`_t` 在调用时才解析。
- 7 处 `_t"all"` 的位置已核对：`Object.lua:1515/1520/1525/1530/1535/1540/1572`。
- 已知副作用：getTextualDesc 内部调用的其他函数（如物品附带技能的说明）里，如果也有 `_t"all"`，同样会显示「全部」。固定源码的 Object.lua 中没有其他 `_t"all"`，其他调用链未逐一排查，「全部」在这些语境下也通顺。
- 全局 `all` 的译文未改动，符合裁决 A。

### 14 G/H/H.Key UseTalents
- `superload/mod/dialogs/UseTalents.lua` 包装 `init`：调用期间临时替换 `TreeList.new`，第一次被调用时立即恢复，最后再保险恢复一次。在交给原函数前用 `fixColumns` 改 columns，各列按表头名匹配：
  - `_t"Status"`：原结果以 `"#LIGHT_GREEN#".._t"Active"` 开头时，替换成「可用」。英文下独有键查不到，不做包装。
  - `_t"Hotkey"` 且 `display_prop=="hotkey"`：改成函数，`H.Key N` 套用 `("H.Key %d"):tformat(N)` →「快捷键 N」。
  - `_t"Mouse Click"`：`LeftClick`／`MiddleClick` 做 `_t` →「左键」「中键」。
- 源码：mod `dialogs/UseTalents.lua:34-54/71-84/269/328`；engine `ui/TreeList.lua:105-113`（函数型 display_prop 的结果会调 `:toTString()`，字符串和 tstring 都支持）。
- 「持续」（Sustain）同为 LIGHT_GREEN，但文字不以「激活」开头，不会误替换。
- **待实机确认**：列宽是固定的，快捷键列 75px、鼠标列 60px，需要确认「快捷键 12」能放下。

### 15 C 开局日志
- `superload/mod/class/Party.lua` 包装 `setPlayer`：`game` 存在、`game.state` 为空且有 `logPlayer` 时，临时把 `game.logPlayer` 换成空函数，pcall 后用 `rawset` 恢复 raw 值。
- 源码：mod `Game.lua:212-222`（newGame 先 setPlayer，第 225 行才创建 `self.state`）；`Party.lua:299` 的日志；`logPlayer` 是 uiset 设置的实例字段（`Classic.lua:90`、`Minimalist.lua:503`）。
- 英文下这条无意义日志同样会消失，属于上游 bug 修正。

### 16 F 人偶标签
- `Object.lua` 重写 `getShortName`：照抄固定源码 `Object.lua:621-660`，只把 `name..", "..table.concat(k, ', ')` 中**两处** `", "` 都换成 `_t(", ##short_name")`（「、」，查不到时回退 `", "`）。取名策略保持材质简称，符合裁决 F。
- 未鉴定分支的 `"%s, %sego#LAST#"`／`"%s, %sspecial#LAST#"` 是 tformat 串，本次没动。
- 说明：材质名与第一个关键词之间也换成了「、」，效果如「铁、精准、锋利」。如果希望写成「铁：精准、锋利」这类形式，需要另行裁决。

## 自检
- 13 个文件 `luajit -bl` 全部通过。
- 补充词条用桩函数 `dofile` 可以加载，共 22 条，src 和 dst 都是字符串。
- 插件 `tests/test_talent_description_diff.lua` 通过。
- 另写了离线 mock harness（不在插件仓库内，路径 `/tmp/addonfix/harness/run.lua`、`hooks.lua`），覆盖：
  - Store、NPC、PlayerRun、Party（静默、恢复、异常重抛）；
  - KeyBinder 合并、ShowAchievements、Chat；
  - Object 的 add_name（含 raw 恢复）、all 拦截后全局 `_t` 已恢复、getShortName 分隔符；
  - UseTalents 三列；CharacterSheet 的初值和切换；
  - hooks 的弹窗、K 的 `%%`、A 的 locked_desc，以及重复执行时的幂等。
  - 共 26 项加 hooks 一组，全部通过。
- 这只验证了包装逻辑，**没有在游戏内加载**。`git diff --check` 报的 trailing whitespace 是 CRLF 的 `\r` 造成的，仓库里现有 superload 文件同样是 CRLF。

## 需要实机验证
详见 `verify-checklist.md`。重点：
- 加载无报错（te4_log 里没有 `[ERROR]`／`superload` 相关报错）；
- `ToME:load` 是否确实排在 Orcs/Cults 之后（A、K 的效果即可证明）；
- UseTalents 列宽；
- KeyBinder 合并后的显示；
- 开局日志不再出现「切换至 player」，而切换队友时仍会记录。
