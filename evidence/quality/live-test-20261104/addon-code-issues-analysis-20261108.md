# 插件代码问题分析（只读子代理报告，主代理已抽查 Store/CharacterSheet/Object/I18N 源码，2026-11-08）

# ToME4 1.7.6 汉化插件：13 个硬编码问题的根因与插件侧修法（只读分析）

只做了分析，没有改动任何仓库文件，也没有 commit。为了读官方 locale 和 `UseTalents.lua`，我从官方 `tome-1.7.6.team` 里解压了这两个文件到 `/tmp/tomeoff`，这是仓库外唯一的写入。

文中行号均来自固定提交 624a67329fe2。DLC 源码来源未固定，行号以 `/workspace/tome4-dlcs` 为准。

**两个总体结论：**
- **多数问题不是"漏了 `_t`"那么简单。** 根因分三类：
  - 一类是英文字面量根本没提取出来（A、M 中多项）；
  - 一类是同一个 `_t` 键被多处共用（H、L）；
  - 一类是逻辑或拼接问题（C、E、J、K），以及 C 层折行（I）。
- **I18N 机制有一处要注意。** `I18N.lua` 的 `set()` 写 `t()` 条目时，会同时写入该 tag 的表和 `"nil"` 兜底表；`_t(s, tag)` 查不到 tag 专属条目时会落到 `"nil"` 表。
  - 好处：任何 tag 的已有条目都能被 `_t` 命中，所以 B 和成就分类不需要新增条目。
  - 坏处：给通用英文词加新 tag 条目，会改写其他 tag 的兜底值，`null_translation.lua` 覆盖 18 个共享键就是这个原因。
  - 因此下文需要新增的键，建议放进插件自有的补充 locale 文件（仿照 `hooks/load.lua` 里 `I18N:loadLocale("/data-chn-mod/null_translation.lua")` 的做法加载），并尽量用独有键或独有 tag。

插件现有手法：
- `hooks/load.lua`：包装 `Dialog.listPopup`，并在 `Entity:loadList`、`Chat:invoke` 两个 hook 上做修补。
- superload 文件：`engine/Birther.lua`（在 `newBirthDescriptor` 时对 `locked_desc`/`desc` 做 `_t`）、`engine/i18N.lua`（补默认 tag `_t`）、`ClassicPlayerDisplay.lua`（中文时加宽资源条）、`ActorTalents`/`ActorTemporaryEffects`（用 `i18nhelper.replaceFormat` 包装 info 和 long_desc）。
- 加载顺序：插件 weight 是 999999，`Module.lua:436` 按 weight 升序加载 addon，hooks 也按这个顺序绑定。所以插件的 `ToME:load` 回调排在三个 DLC 之后。这一点读源码可确认，仍建议实机验证一次。

---

## A. r7-01：Orcs 战役里被锁职业的 locked_desc 显示英文
- **根因**：`tome-orcs/data/birth/worlds.lua:145-148、168-171`（来源未固定）。Orcs 在 `ToME:load` 时（`OrcCampaign.lua:83` 加载 `worlds.lua`）把已注册的 class/subclass 描述符的 `locked_desc` 直接替换成函数，回退值 `"Once freed, twice shy."` 是裸字面量。
  - 插件的 `superload/engine/Birther.lua` 只在 `newBirthDescriptor` 时包装，事后直接赋值绕开了它。
  - 显示处是 `mod/dialogs/Birther.lua:811/838/870/905/917/958/977` 的 `util.getval(d.locked_desc, self)`，没有再过 `_t`。
  - 这个字面量不在提取结果里：`tome-orcs.lua` 和官方 Orcs locale 都没有它。
  - Skirmisher 不属于这一类：`rogue.lua:227` 用了 `_t`，译文库也有条目（`mod-tome.lua:3094`）。Orcs 战役下它显示的是 `old_lock_desc`，也就是已经翻好的原文。
- **修法**：
  - 补充 locale 加 `t("Once freed, twice shy.", "一朝获释，再难轻信。", "_t")`（这是测试员的建议译文）。
  - 在 `hooks/load.lua` 绑定 `ToME:load`（排在 Orcs 之后），遍历 `Birther.birth_descriptor_def.class` 和 `.subclass`，对函数型 `locked_desc` 包一层 `_t`，用标记防止重复包装：
    ```lua
    for _, kind in ipairs{"class","subclass"} do for _, d in ipairs(Birther.birth_descriptor_def[kind] or {}) do
      if type(d.locked_desc)=="function" and not d.__chn_ld then
        local f=d.locked_desc; d.locked_desc=function(...) local r=f(...) return type(r)=="string" and _t(r) or r end; d.__chn_ld=true
      end end end
    ```
  - 更稳但更重的替代：superload `mod/dialogs/Birther.lua` 的 `init`，在打开对话框时做同样的包装。
  - 只改 locale 不够，因为显示路径不过 `_t`。
- **评估**：改动小。风险低：英文下 `_t` 是恒等，不进存档。需要实机看一眼锁定悬停。

## B. r7-03 / r9-10：商店标题显示 `Store: sword smith`
- **根因**：`engine/Store.lua:122-124` 的 `interact(who, name)` 用 `("Store: %s"):tformat(name or self.name)`。tformat 只翻译格式串，引擎 locale 已有 `"商店：%s"`，但参数 `self.name`（如 `"sword smith"`）是原样传入的。
  - 聊天商店都是 `npc.store:interact(player)` 不传 name，涉及 `last-hope-weapon-store.lua:25`、`angolwen-staves-store.lua:25`、`jewelry-store.lua:137`、`last-hope-lost-merchant.lua:38`、`magic-store.lua:39`、`zigur-mindstar-store.lua:25`，以及 Orcs 的 `kruk-tinker-shop`。
  - Arena 传了 `_t"Gladiator's wares"`；`resolvers.lua:546/577` 传 `self:getName()`，这两处本来就正常。
  - 商店名在 locale 里已有条目，例如 `t("sword smith","铸剑师","entity name")`、`"Tinkers Store"`。
- **修法**：新建 `superload/mod/class/Store.lua`：
  ```lua
  local _M = loadPrevious(...)
  local _i = _M.interact
  function _M:interact(who, name) return _i(self, who, name or _t(self.name, "entity name")) end
  return _M
  ```
  不需要新条目。
- **评估**：改动小。风险很低：只影响显示，存档里的名字不变，DLC 商店一并修好。顺手验证一个商店即可。

## C. r7-07：开局日志「角色切换至 player」
- **根因**：这是时序问题，与译文无关。
  - `mod/class/Game.lua:212-222`：`newGame()` 用 `Player.new{name=self.player_name}` 建角色，此时名字是 loader 默认的 `"player"`（`loader/init.lua:30`），随后立刻 `self.party:setPlayer(player)`。
  - `mod/class/Party.lua:299` 的 `game.logPlayer(actor, "#MOCCASIN#Character control switched to %s.", actor:getName())` 记下的就是改名前的名字。真名要到 Birther 结束后的 `setPlayerName`（`Game.lua:203-210`）才设置。
  - 日志系统在 `Game:run` 里、`newGame` 之前就已就绪，所以推测所有战役都会出现这一行，不只是余烬怒火。
- **修法**：新建 `superload/mod/class/Party.lua` 包装 `setPlayer`。当 `not game.state` 时（`newGame` 里 `self.state` 在第 225 行才创建，读档时一定已存在），临时把 `game.logPlayer` 换成空函数，用 pcall 调原函数后恢复。没有更轻的办法。
- **评估**：改动小。风险低：英文下也会少掉这条无意义日志，属于上游 bug 修正。需实机确认开局日志消失，切换队友时仍正常记录。

## D. r7-08：Orcs 男性平民的 emote_random 是裸字面量
- **根因**：`vaporous-emporium/npcs.lua:59-61`（来源未固定）的 `resolvers.emote_random{chance=0.8, "You won't get my gold!"}` 没有 `_t`；女性版第 72 行有 `_t`，所以 locale 已有条目（`tome-orcs.lua:7700`）。
  - 喊话由 `mod/class/NPC.lua:77-81` 取出后调 `self:doEmote(e, dur)`（`NPC.lua:438`），全程不过 `_t`。
  - 解析后的字符串会存进 NPC 实体，因此已有存档里也是英文。
  - 全库只有这一处裸 emote（核心和三个 DLC 都 grep 过）。
- **修法**：新建 `superload/mod/class/NPC.lua`，包装 `doEmote(text, ...)`，当 `text` 是字符串时先 `_t(text)`。这样通用、对旧存档也生效，而且不需要新条目。
  - 更窄的替代：在 `Entity:loadList` hook 里匹配 `data.file == "/data-orcs/zones/vaporous-emporium/npcs.lua"`，改写 resolver 的 def。但这种做法对已存档的 NPC 无效。
- **评估**：改动小。风险很低。不必专门做实机验证。

## E. r8-02 / cls12-c3-01：盾牌名括号内全角、半角逗号混排
- **根因**：`mod/class/Object.lua:592-596` 的 `getName` 把 `self.add_name` 里的 `#ATTR#` 用 `descAttribute`（第 424 行起）替换后直接拼接。
  - `add_name` 是数据字面量，从不过 `_t`。盾牌的是 `" (#ARMOR#, #SHIELD#)"`（`shields.lua:26`），核心里只有这一个 add_name 带逗号。
  - 括号内的属性片段：`"%s def, %s armour"`（第 473 行）和 `"%s, %s block"`（第 468 行），在译文库 `mod-tome.lua:717-724` 已改成全角逗号；而 add_name 里连接两段的 `", "` 仍是半角。
- **修法一（推荐，代码）**：superload `mod/class/Object.lua` 包装 `getName`：
  ```lua
  local _gn = _M.getName
  function _M:getName(t)
    local an = self.add_name
    if type(an)=="string" then local tr=_t(an,"entity add_name")
      if tr~=an then self.add_name=tr; local ok,r=pcall(_gn,self,t); self.add_name=an; if not ok then error(r) end; return r end end
    return _gn(self,t)
  end
  ```
  补充 locale 加 `t(" (#ARMOR#, #SHIELD#)", " (#ARMOR#，#SHIELD#)", "entity add_name")`。以后其他 add_name 也能按需翻译。
- **修法二（纯译文、零代码）**：把 `mod-tome.lua:717-724` 这组 `descAttribute` 模板改回半角 `", "`，与 add_name 一致。这组模板只在物品名括号里使用，官方 locale 原本就是半角。代价是括号内统一为半角标点。
- **评估**：修法一改动小，`getName` 调用频繁但只多一次查表，风险低，临时换回不进存档，需看拾取、物品栏、日志三处。修法二改动极小、无风险。

## F. r9-09 / cls10-c2-02：装备人偶标签只显示「铁」或被截断
- **根因有两个，cls10-c2-02 的推测不成立。**
  1. 「只显示铁」是设计行为，不是截断。数据里 `short_name = "iron"`（如 `2hswords.lua:40`、`2haxes.lua:40`），`getShortName`（`Object.lua:621-660`）在无词缀时只返回材质名，英文版同样只显示 `iron`。
  2. 长标签被截（r9-09）：第 643-646 行用 `name..", "..table.concat(k, ', ')` 拼接关键词（半角，无 `_t`）；未鉴定时用 `"%s, %sego#LAST#"`。
     - `engine/ui/EquipDollFrame.lua:121-135` 用 `self.font:draw(name, self.w*3, ...)` 绘制。`topleft` 位置的 `x = x - t.width + self.w` 让长标签向左延伸，越出面板就被裁掉。
- **修法**：superload `mod/class/Object.lua` 重写 `getShortName`（约 40 行照抄，再改分隔符）：
  - 分隔符改用补充 locale 的 `_t(", ", "short_name sep")` → `"、"`；
  - 可选：中文下限制关键词数量；
  - 可选：已鉴定且无词缀时直接用 `_t(self.name,"entity name")`（如「铁质巨剑」）代替材质简称。这是 UI 取舍，需要你决定。
  - `getShortName` 只用于人偶和 `Actor.lua:2147-2191` 的武器提示行，影响面可控。
- **评估**：改动小到中。风险低，只影响显示。需要实机看人偶。

## G + H + M（H.Key）：UseTalents 对话框
- **根因**：`mod/dialogs/UseTalents.lua`：
  - 第 78-81 行「鼠标点击」列直接返回 `"LeftClick"`/`"MiddleClick"`，列宽固定 `{60,"fixed"}`。
  - 第 34-54 行 `local function TalentStatus` 用共享键 `_t"Active"`，同一个键还用于 `ShimmerRemoveSustains.lua:40`、boot 的 `Addons.lua:66`，因此不能靠改译文区分。
  - 第 269、328 行用 `"H.Key "..i` 拼接，第 77 行快捷键列 `{75,"fixed"}`。
  - `TalentStatus` 是文件内局部函数，superload 改不到它本身。
- **修法**：superload `mod/dialogs/UseTalents.lua` 包装 `init`。在调用原 `init` 期间临时替换 `TreeList.new`（模块里是在调用时取字段，所以替换有效），拦截 `columns` 后再交给原函数：
  - 列 3：包装原 `display_prop`，结果以 `"#LIGHT_GREEN#".._t"Active"` 开头时，替换成 `_t("Active##use_talents")`（独有键，查不到时回退 `_t"Active"`，英文不受影响）。
  - 列 4：`display_prop` 改成函数，用 `util.getval(item.hotkey,item)` 取值后，用 `gsub("^H%.Key (%d+)", ...)` 套 `("H.Key %d"):tformat(n)`。
  - 列 5：返回 `_t"LeftClick"`、`_t"MiddleClick"`。需要时可把列宽改为由字体量出的宽度。
  - 需要补充 locale 条目：`"Active##use_talents"→"可用"`、`"H.Key %d"→"快捷键 %d"`、`"LeftClick"→"左键"`、`"MiddleClick"→"中键"`。
  - 补充：G 的截断原因是英文 `LeftClick` 在当前字体下超过 60px，翻成两个字即可放下。
- **评估**：改动中（一个文件约 40 行）。风险低到中：依赖 1.7.6 的列顺序，建议按列 `name` 匹配，匹配不到就不改。需要实机验证。

## I. cls07b-07 / cls11b-c3-01 / cls06-c3-02：数字、百分号、句号被折行拆开
- **根因**：中文 locale 在引擎 `data/locales/engine/zh_hans.lua:4` 执行 `setFlag("break_text_all_character", true)`，由 `I18N.lua:123-126` 调用 `core.display.breakTextAllCharacter(true)`。折行有两条路径：
  1. **C 路径，提示框的主路径**：`engine/Tooltip.lua:44/141/154` → `ui/TextzoneList.lua:106-108`；`ui/Textzone.lua:61` 直接调 `font:draw`，对应 `src/core_lua.c:980` 起的 `sdl_font_draw`。
     - 开启任意字符折行后，第 1036-1053 行的内层循环不在空格处停，只按像素宽度逐字测量，超宽就在当前字符处硬切。
     - 因此「165%」会切成「16」「5%」，「3.0」切成「3」「.0」，句号会落到行首，英文单词也会被拆开（ashcults-10 的 `hotke ys`）。
     - 这是 C 代码，插件改不了函数本身。
  2. **Lua 路径**：`engine/utils.lua:1685` 的 `tstring:splitLines`（以及 1115 行的 `string.splitLine`）在 break 模式下调用 `string.splitAtSizeSimple`（1073 行）或 `splitAtSize`（1093 行），同样是逐字切分。Dialog、LogFlasher、makeLineTextures 走这条路径。
- **修法**：
  - **Lua 路径（较轻）**：在 `hooks/load.lua` 覆盖 `string.splitAtSizeSimple` 和 `string.splitAtSize`。
    - 切点落在数字簇 `[%d%.%%%+%-/]` 内部，或右侧以避头标点（`，。、；：？！）」』》%…` 等）开头时，把切点前移。
    - 为防死循环：包装 `tstring.splitLines`，把 `max_width` 存进 upvalue。只有 `size < max_width`（即当前行已有内容）时才允许左半为空，整段移到下一行；否则保持非空的硬切。
  - **C 路径（真正解决提示框问题）**：包装字体 userdata 的 `getmetatable(font).__index.draw`（`utils.lua:1461-1472` 已用同样方式改过 `size`）。
    - 仅当 `core.display.getBreakTextAllCharacter()` 为真、`no_linefeed` 为假、文本含多字节字符时，先用 Lua 预折行：把文本切成单元（一个 CJK 字；一个 ASCII 单词或数字簇；避头标点并入前一单元；`（“《` 并入后一单元），按 `font:size` 贪心填行并插入 `"\n"`，再交给原 `draw`。
    - 这样每行都不超宽，C 就不会硬切。
    - 需要正确跳过 `#COLOR#`、`#{bold}#`（会改变字宽，要 `setStyle` 并在结束时复原）、`#UID:..#`（宽度约等于行高）、`#&..#`，并预留 1-2px 余量以吸收字距差异。
- **评估**：改动中到大（约 120-200 行）。风险中：`font:draw` 是全局入口，涉及性能（提示框重绘频繁，建议按字符串缓存）、`#&` 行数据和 `id_real_line` 计数（`\n` 会让 real line 递增，推测只影响带 `#&` 的列表）。英文 locale 不受影响，因为开关为假时直接透传。必须实机大面积验证。顺带能修好英文单词被拆开的问题。

## J. cls11b-02：装备组切换显示 "main"/"off"
- **根因**：`mod/dialogs/CharacterSheet.lua:63` 初始化时 `self.equip_set = off_weapon_slots and _t"off" or _t"main"`，存进去的是已翻译的值；但第 71 行用 `self.equip_set == "off"` 当内部枚举比较，第 73 行再赋英文 `"main"`/`"off"`。
  - 结果：首次显示是中文，切换一次后变成英文。
  - 第 64、83 行 tformat 不翻译参数；第 74 行日志直接传英文枚举。
  - 还有一个连带功能 bug：`updateEquipDollRefs`（第 364 行起）用 `showset == "main"` 判断，第 470 行传入的若是中文值，会显示错误的武器组；初始为副手组时，第一次切换也会失效。推测英文下不触发。
- **修法**：superload `mod/dialogs/CharacterSheet.lua` 包装 `init`，在原函数之后：
  - 把 `self.equip_set` 规范为英文枚举；
  - 重设 `self.c_equipment.generate`，用 `("[E]quipment: %s set"):tformat(_t(self.equip_set))`；
  - 重写 `self.c_equipment.on_change`（照抄第 66-79 行），日志参数改为 `_t(self.equip_set)`；
  - 最后调一次 `self.c_equipment:generate()`。
  - locale 已有 `t("main","主用","_t")`、`t("off","备用","_t")`，不需要新条目。
- **评估**：改动小到中。风险低，顺带修掉功能 bug。需要实机切换两次验证。

## K. cls11-01：Cults 疯狂值在角色面板显示 `%%`
- **根因**：`tome-cults/overload/mod/class/CultsDLC.lua:47-52` 的 `status_text` 返回的是格式化过一次的 `"100%% (50%% chaotic)"`，设计上要被再次 format：
  - `ClassicPlayerDisplay.lua:99-115` 把它当 `nfmt` 再 `:format()`；
  - `Minimalist.lua:894` 显式 `:format()`。
  - 但 `CharacterSheet.lua:655-657` 优先找 `res_def.CharacterSheet.status_text`。核心资源（如 `resources.lua:113` 的失衡值）都另有定义，Cults 没有，于是直接把含 `%%` 的串作为参数放进 tformat，`%%` 保留下来。英文版同样有这个 bug。
  - 不能改译文去掉 `%%`：那样经典界面的二次 format 会把 `"% ("` 当成格式说明而报错。
- **修法**：在 `hooks/load.lua` 绑定 `ToME:load`（排在 Cults 之后）：
  ```lua
  local d = require("engine.interface.ActorResource").resources_def.insanity
  if d and d.status_text and not (d.CharacterSheet and d.CharacterSheet.status_text) then
    local st=d.status_text; d.CharacterSheet=d.CharacterSheet or {}
    d.CharacterSheet.status_text=function(a) return (st(a)):format() end
  end
  ```
  可以推广成"所有缺少 `CharacterSheet.status_text` 的资源"。
- **评估**：改动小。风险低，英文也一并修好。需看角色面板一眼。

## L. cls08-c3-03 / cls06-c3-05：「抗性改变：+7% 所有」
- **根因**：`Object.lua:1515/1520/1525/1530/1535/1540/1572` 七个属性行（抗性、抗性上限、固定减伤、护盾值上限、穿透、伤害、伤害亲和）都写成 `(" %s"):tformat(item=="all" and _t"all" or ...)`。
  - `_t"all"` 的 tag 是 `_t`，与 `GameOptions.lua:655`（在线事件「全部/仅技术帮助/禁用」）、`timed_effects/mental.lua:2181`（灵能护盾 `eff.what`，而且会存进效果状态）共用。
  - `quest_lumberjack` 有自己的 tag，不受影响。
  - 格式串 `" %s"` 也是共享键，同样不能区分。
- **修法**：superload `mod/class/Object.lua` 包装 `getTextualDesc`（第 1201 行起，七行都在其中的 `desc_wielder` 里）。调用期间临时把 `_G._t` 换成拦截版：当 `s=="all"` 且 tag 为 nil 或 `"_t"` 时，返回补充 locale 的独有键 `_t("all##item_property")`（建议译「全部」，七种属性语境都通顺；「所有抗性」只适用于抗性一行）。用 pcall 后恢复。
  - 能这样做是因为模块用 `package.seeall`，`_t` 在调用时经 `_G` 解析。
  - 核心和 DLC 中，`getTextualDesc` 范围内（含 `Object:descWielder` hook）没有其他 `_t"all"`。
  - 更轻的替代：直接把全局 `"all"` 改成「全部」。在线事件选项用「全部」很自然；灵能护盾的 `display_desc` 也走 `_t(eff.kind)`，会变成「全部灵能护盾」。这需要术语决定，超出本次授权范围。
- **评估**：改动小。风险低到中（临时替换全局 `_t`，必须 pcall 恢复）。需看物品提示。

## M. 其余硬编码英文（已定位部分）
| 项 | 根因 | 修法 | 优先级 |
|---|---|---|---|
| H.Key | `UseTalents.lua:269/328` | 并入 G/H | 高（随 G/H 一起做） |
| 按键绑定分组标题 | `engine/dialogs/KeyBinder.lua:227-235` 用 `group:capitalize()`，不过 `_t`；另外有 4 条 `group=_t"movement"`，导致中文下多出一个「移动」组 | superload `engine/dialogs/KeyBinder.lua` 包装 `generateList`：对 `self.tree` 顶层节点用 `node.nodes[1].k.group` 取原始组名，`_t(group:capitalize())`，可选合并同名组后重排。测试员说库里已有 Action/Actions/Hotkeys 的译文 | 中，改动小 |
| DLC 成就分类 | DLC 的 `category = "Embers of Rage"` 等是裸字面量；`engine/dialogs/ShowAchievements.lua:177-183` 显示原值 | superload 包装 `generateList`（第 153 行），对 `self.list[i].category` 做 `_t`。locale 已有 "Embers of Rage"、"Forbidden Cults"、"Ashes of Urh'Rok"，不需新条目 | 中，改动小 |
| 对话立绘名牌英文名（The Eidolon、Metash） | `mod/dialogs/Chat.lua:86-140` 的 `getActorPortrait` 新建普通 `engine.Entity{name=actor.name}`；`ChatPortrait.lua:33` 调 `getName`，而引擎 `Entity:getName`（`Entity.lua:164`）返回原名，ToME 的 `Actor:getName`（`Actor.lua:2003`）才会做 `_t` | superload `mod/dialogs/Chat.lua` 包装 `getActorPortrait`：结果不是 actor 本身且 `e.name==src.name` 时，改用 `src:getName()` 或 `_t(name,"entity name")` | 中高，改动小 |
| 战役名 Orcs | `Game.lua:807-821` 的 `getSaveDescription` 用 `_t(player.descriptor.world)`，locale 没有 `"Orcs"` 键（Infinite、Arena 推测同样缺） | 最轻：补充 locale 加 `t("Orcs","余烬怒火","birth descriptor name")` 等（源码和 DLC 都没有别处用 `_t"Orcs"`）。存档描述在每次存档时重新生成，旧档要再存一次 | 低，改动极小 |
| 自动探索中断原因 | `engine/interface/PlayerRun.lua:266-360` 的 `runCheck` 返回裸英文（"terrain changed ahead" 等）；第 377 行原样记入日志 | superload `engine/interface/PlayerRun.lua` 包装 `runStop(msg)`，对 msg 做 `_t`，并在补充 locale 加约 6 条原因 | 中，改动小 |
| 快捷栏翻页对话框 | `mod/class/Player.lua:1329-1336` 的 `hotkeyPageTutorial` 用 `simpleLongPopup` 显示裸字面量标题和正文 | 照搬现有 `listPopup` 的做法，在 `hooks/load.lua` 包装 `engine.ui.Dialog.simpleLongPopup`/`simplePopup`，对标题和正文做 `_t`，同时能兜住其他裸字面量弹窗；补充 locale 加原文条目 | 低中，改动小 |
| Birther 种族英文列表 | `tome-ashes-urhrok/superload/mod/dialogs/Birther.lua:34-42`：`races={"human","elf",...}` 直接 `concatNice` 后作为参数传入，tformat 不翻译参数 | 只在首次运行弹出一次。可再叠一层 superload 包装 `init`，临时包装 `self.simpleLongPopup`，对 `#LIGHT_BLUE#…#WHITE#` 段内的词逐个做 `_t(w:capitalize())`。属于 hack | 低 |
| `Steam:` | `tome-orcs/overload/mod/class/OrcCampaign.lua:200` 的 `hookCharacterSheetAttackPower` 用裸 `"#LIGHT_BLUE#Steam:"`；函数在绑定 hook 时已被捕获，替换不了 | superload `CharacterSheet` 覆盖 `_M:triggerHook(hd)`：当 `hd[1]=="CharacterSheet:Attack:power"` 时，临时包装 surface 元表的 `drawColorStringBlended`（`utils.lua:1430` 是 Lua 函数），对字符串做 `_t`，调用后恢复；补充 locale 加 `"#LIGHT_BLUE#Steam:"` | 低中，改动小，属于 hack |

---

## 汇总表
| 问题 | 根因位置 | 修法 | 改动量 | 风险 | 优先级 |
|---|---|---|---|---|---|
| A locked_desc | orcs `worlds.lua:145-171` 事后覆盖；`dialogs/Birther.lua:811` 等不过 `_t` | `ToME:load` 包装函数型 locked_desc + 补充 locale | 小 | 低 | 中 |
| B 商店标题 | `engine/Store.lua:124` | superload `mod/class/Store` 的 `interact` | 小 | 很低 | 高 |
| C 开局「切换至 player」 | `Game.lua:214-222` + `Party.lua:299` | superload `Party:setPlayer`，`not game.state` 时静默 | 小 | 低 | 低中 |
| D 裸 emote | orcs `npcs.lua:60`；`NPC.lua:77-81/438` | superload `NPC:doEmote` 做 `_t` | 小 | 很低 | 中 |
| E 盾牌逗号混排 | `Object.lua:592-596` add_name 不过 `_t` | `getName` 临时翻译 add_name，或把模板改回半角 | 小（或零代码） | 低 | 中 |
| F 人偶标签 | `Object.lua:621-660` + `EquipDollFrame.lua:121-135` | 重写 `getShortName` 的分隔符和取名策略 | 小到中 | 低 | 低中 |
| G/H/H.Key | `UseTalents.lua:34-54、77-81、269、328` | 包装 `init`，拦截 `TreeList.new` 改列 | 中 | 低到中 | 中高 |
| I 折行 | C `sdl_font_draw`（`core_lua.c:1036-1053`）；Lua `utils.lua:1073/1093/1685` | 包装 `font.draw` 做 Lua 预折行 + 覆盖 `splitAtSize*` | 中到大 | 中 | 中（收益大，单独排期） |
| J 装备组 | `CharacterSheet.lua:63/71/74/83/470` | 包装 `init`，枚举保持英文、显示时 `_t` | 小到中 | 低 | 中 |
| K 疯狂值 `%%` | cults `CultsDLC.lua:51` + `CharacterSheet.lua:655` | `ToME:load` 补 `CharacterSheet.status_text` 并 `:format()` | 小 | 低 | 中高 |
| L all→所有 | `Object.lua:1515-1572` 共享 `_t"all"` | `getTextualDesc` 期间拦截 `_t("all")` | 小 | 低到中 | 中 |
| M 按键分组 | `KeyBinder.lua:227-235` | 包装 `generateList` | 小 | 低 | 中 |
| M 成就分类 | `ShowAchievements.lua:177-183` | 包装 `generateList` | 小 | 低 | 中 |
| M 立绘名牌 | `Chat.lua:86-140` + `Entity.lua:164` | 包装 `getActorPortrait` | 小 | 低 | 中高 |
| M 战役名 | `Game.lua:818` | 补充 locale 条目 | 极小 | 低 | 低 |
| M 中断原因 | `PlayerRun.lua:266-377` | 包装 `runStop` + 补充条目 | 小 | 低 | 中 |
| M 翻页教学 | `Player.lua:1332` | 包装 `simpleLongPopup`/`simplePopup` | 小 | 低 | 低中 |
| M 种族列表 | ashes `superload/.../Birther.lua:34-42` | 包装弹窗并后处理文本 | 小 | 低（hack） | 低 |
| M Steam: | orcs `OrcCampaign.lua:200` | `triggerHook` 期间包装 `drawColorStringBlended` | 小 | 低中（hack） | 低 |

**跨问题的共同风险：**
- 除 C、J、K 会顺带修正英文下的上游 bug 外，其余改动在英文 locale 下都是恒等。
- 所有改动都只影响显示，不写存档，因为临时替换的值都会恢复。
- 都依赖 1.7.6 的函数结构：UseTalents 列顺序、CharacterSheet 的 `on_change` 照抄、`getShortName` 照抄在其他版本上可能失配，建议加存在性检查，失配时退回原函数。
- Orcs 和 Cults 的修补应先判断对象存在（例如 `resources_def.insanity`），避免未装 DLC 时出错。

## 建议实施顺序
1. **先建基础设施**：一个插件自有的补充 locale 文件（键要独有，或用独有 tag，避免改写 `nil` 兜底表），并在 `hooks/load.lua` 加一个 `ToME:load` 回调。
2. **第一批（无风险、无需新条目）**：B 商店、D emote、K 疯狂值、成就分类、立绘名牌、A 的包装部分。
3. **第二批（小改动，加补充条目）**：A 的条目、PlayerRun 中断原因、`simpleLongPopup` 包装（翻页教学）、按键分组、战役名、E。
4. **第三批（逻辑修正）**：J 装备组、L 物品 all、G/H/H.Key 的 UseTalents 包装、C 开局日志、F 人偶标签（F 需要先定 UI 取舍）。
5. **单独排期**：I 折行。先做 Lua 路径，再做 `font.draw` 预折行，配大面积实机回归（升级窗口、悬停提示、物品说明、日志）。
6. **可选 hack**：Steam:、Ashes 种族列表。

需要你决定的两点：
- L 是否接受直接把全局 `"all"` 改成「全部」（这是术语决定，超出现有授权）。
- F 人偶在中文下是否改用完整物品名。

**不确定的地方：**
- C 推测所有战役都会出现，只读源码确认，没有实机复现。
- I 里 `\n` 对 `#&` 行数据的影响只是推测。
- `ToME:load` 排在 DLC 之后是读源码得出的，未实机确认。
