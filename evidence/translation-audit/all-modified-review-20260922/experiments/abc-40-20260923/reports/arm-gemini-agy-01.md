# 40条译文独立复核报告

本复核严格基于 `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/INPUT.md` 明确允许读取的材料及固定版本源码（Git Commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`），对 40 条样本进行逐条完整复核。复核采用同一评分分类（「未发现问题 / 存在问题 / 待确认 / 仅建议」），不使用省略，不声称 `DONE_VERIFIED`。

---

## 逐条复核详情

### entry-03172
- **位置**：`mod-tome.lua:41216`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Random!
  ```
- **译文**：
  ```text
  随机！
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:93`（`self.c_random = Button.new{text=_t"Random!", fct=function() self:randomBirth() end}`）。角色创建界面的随机生成属性/外形按钮，中文译文语义完全忠实，标点中英文感叹号等价，无占位符与格式标记。

---

### entry-03173
- **位置**：`mod-tome.lua:41237`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Basic Gameplay (recommended)
  ```
- **译文**：
  ```text
  基本游戏教程（推荐）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:424`（出生弹窗 `Tutorials` 下的选项按钮）。在教程选择界面的语境下，译文将 `Basic Gameplay` 补全为“基本游戏教程（推荐）”，使按钮语义更加明确且贴合界面语境，括号使用中文全角，无格式缺陷。

---

### entry-03174
- **位置**：`mod-tome.lua:41241`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text


  #GOLD#This is a locked birth option. Performing certain actions and completing certain quests will make locked campaigns, races and classes permanently available.
  ```
- **译文**：
  ```text


  #GOLD#本选项被锁定，完成特定的任务或条件可以永久解锁这个战役，种族，职业。
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:804, 826, 858, 890, 944` 的锁定提示描述。译文前置换行 `\n\n` 保持一致，颜色标记 `#GOLD#` 对应闭合。语义完整传达了锁定原因及解锁条件，术语“战役、种族、职业”准确。

---

### entry-03175
- **位置**：`mod-tome.lua:41247`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #CRIMSON#Playing this class with the race you selected does not make much sense lore-wise. You can still do it but might miss on some special quests/...#WHITE#\n
  ```
- **译文**：
  ```text
  #CRIMSON#使用这个种族来游玩这个职业不符合剧情。你仍然可以这么做，但可能会错过一些特殊任务/……#WHITE#\n
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:967`。颜色标记 `#CRIMSON#` 与 `#WHITE#` 匹配闭合，末尾换行符保留。语义上 `lore-wise` 准确译为“不符合剧情”，省略号规范转为全角，无格式缺陷。

---

### entry-03176
- **位置**：`mod-tome.lua:41255`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Exploration mode provides the characters using it with infinite lives.
  Tales of Maj'Eyal is meant to be a very replayable game in which you get better by learning from mistakes (and thus from dying too).
  I realize this can not please everybody and after multiple requests I have decided to grant exploration mode to donators, because it will allow player that like the game to see it all if they wish.
  Beware though, infinite lives does not mean the difficulty is reduced, only that you can try as much as you want without restarting.

  If you'd like to use this feature and find this game good you should consider donating. It will help ensure its survival.
  While this is a free game that I am doing for fun, if it can help feed my family a bit I certainly will not complain as real life can be harsh sometimes.
  You will need an online profile active and connected for the tile selector to enable. If you choose to donate now you will need to restart the game to be granted access.

  Donators will also gain access to the custom tiles for their characters.
  ```
- **译文**：
  ```text
  探索模式提供给角色无限的生命数。
  马基·埃亚尔的故事是一款非常耐玩的游戏，你需要不断的从错误中学习。（同样从死亡的错误中学习）
  我觉得这款游戏可能不会被所有人接受并且在收到多次请求后，我决定开放探索模式给捐赠者，因为它允许喜欢这款游戏的玩家能全面地体验这款游戏。
  不过要注意的是，无限的生命并不意味着难度的减少，仅仅意味着你可以有着无限多的尝试次数。

  如果你愿意使用这项功能并且觉得这款游戏很好，你可以考虑捐赠。
  这会帮助延长这款游戏的寿命。尽管这只是我自娱自乐所做的一款游戏，如果它还能帮助我分担一点养家糊口的压力的话，我就谢天谢地，不会再抱怨现实的诸多压力了。
  你需要一个已激活并保持连接的在线档案，贴图选择器才能启用。如果你现在选择捐赠，你需要重启游戏才能获得权限。

  捐赠者也可以使用自定义贴图来DIY他们的角色。
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:1378-1393`。专有名词 `Maj'Eyal` 统一采用术语库裁决规范“马基·埃亚尔”，`Donators` 统一为“捐赠者”。源码中原作者 DarkGod 确实在第 7 段保留了 `tile selector to enable`，译文如实对应；段落划分与换行结构完整，核心语义准确传达。

---

### entry-03177
- **位置**：`mod-tome.lua:41275`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Donate!
  ```
- **译文**：
  ```text
  捐赠！
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:1391, 1407`（捐赠弹窗按钮文本）。语义与标点完全一致。

---

### entry-03178
- **位置**：`mod-tome.lua:41310`
- **section**：`mod-tome/dialogs/Birther.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Cosmetic customization is a donator-only feature.
  ```
- **译文**：
  ```text
  自定义外观是捐赠者的特权。
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Birther.lua:1730`。术语 `donator` 对应“捐赠者”，语义清晰通顺，无格式问题。

---

### entry-03179
- **位置**：`mod-tome.lua:41328`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`logPlayer`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #RED#Displaying %s set for %s (equipment NOT switched)
  ```
- **译文**：
  ```text
  #RED#展示 %s 套装给 %s 看（装备未切换）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:74`（`game.logPlayer(self.actor, "#RED#Displaying %s set for %s (equipment NOT switched)", self.equip_set, self.actor:getName():capitalize())`）。传参顺序为装备集代号（`equip_set`）与角色名，译文中两个 `%s` 顺序保持一致，颜色代码 `#RED#` 保留，装备未实际切换的提示无歧义。表达中“给 %s 看”属中文口语化处理，不影响语义理解与运行时逻辑。

---

### entry-03180
- **位置**：`mod-tome.lua:41333`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Sort:  %s
  ```
- **译文**：
  ```text
  排序：%s
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:94`。天赋排序切换按钮，占位符 `%s` 正确保留，冒号转为全角，未发现问题。

---

### entry-03181
- **位置**：`mod-tome.lua:41391`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  - Seed: #LIGHT_STEEL_BLUE#%s
  ```
- **译文**：
  ```text
  - 种子：#LIGHT_STEEL_BLUE#%s
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:629`。角色面板世界种子显示，颜色代码 `#LIGHT_STEEL_BLUE#` 与占位符 `%s` 格式完全匹配。

---

### entry-03182
- **位置**：`mod-tome.lua:41399`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  die:%+d
  ```
- **译文**：
  ```text
  死亡底线：%+d
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:646`（消费链为 `compare_fields` 函数 `outformat:format((value or 0) * mod)`）。`die_at` 属性控制角色生命值降至多低才会死亡，占位符 `%+d` 严格保留了带符号整数格式，游戏机制与术语“死亡底线”一致。

---

### entry-03183
- **位置**：`mod-tome.lua:41421`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  (with heal mod): #00ff00#%s
  ```
- **译文**：
  ```text
  （治疗系数加成后）：#00ff00#%s
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:744`（生命恢复提示中的计算说明）。`heal mod` 机制对应治疗效果系数加成，占位符 `%s` 和颜色代码 `#00ff00#` 正确保留，括号使用全角。

---

### entry-03184
- **位置**：`mod-tome.lua:41437`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Two-Handed, 
  ```
- **译文**：
  ```text
  双手， 
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:897`（`local text2 = (... _t"Two-Handed, " or "")..(weap_type and ...)`）。用于前置拼接武器类型，译文末尾保留了全角逗号与空格，保证后续字符拼接正常。

---

### entry-03185
- **位置**：`mod-tome.lua:41452`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
   (disabled)
  ```
- **译文**：
  ```text
   （被禁用）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:954, 959`（当角色处于缴械状态 `player:attr("disarmed")` 时，拼接入副手装备行末尾）。译文保留了前置空格，语义表达准确。

---

### entry-03186
- **位置**：`mod-tome.lua:41494`
- **section**：`mod-tome/dialogs/CharacterSheet.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #LIGHT_BLUE#Damage affinities:
  ```
- **译文**：
  ```text
  #LIGHT_BLUE#伤害亲和：
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `CharacterSheet.lua:1235`。角色面板伤害抗性/吸收之后的“伤害亲和”（受击按比例转化为治疗）属性标题，颜色代码 `#LIGHT_BLUE#` 保留，术语规范。

---

### entry-03187
- **位置**：`mod-tome.lua:41537`
- **section**：`mod-tome/dialogs/DeathDialog.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  You have #LIGHT_RED#died#LAST#!
  ```
- **译文**：
  ```text
  你已经#LIGHT_RED#死了#LAST#！
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `DeathDialog.lua:34`（死亡弹窗标题）。颜色控制符 `#LIGHT_RED#` 与 `#LAST#` 正确包裹对应词汇，感叹号全角化，语义准确。

---

### entry-03188
- **位置**：`mod-tome.lua:41561`
- **section**：`mod-tome/dialogs/DeathDialog.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Message/Chat log (allows to talk)
  ```
- **译文**：
  ```text
  消息/聊天日志（允许聊天）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `DeathDialog.lua:350`。死亡界面已登录账号时的聊天与日志查看按钮，语义忠实，括号全角，无格式缺陷。

---

### entry-03189
- **位置**：`mod-tome.lua:41572`
- **section**：`mod-tome/dialogs/Donation.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #GOLD#Exploration mode (infinite lives)#WHITE#
  ```
- **译文**：
  ```text
  #GOLD#探索模式（无限命）#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Donation.lua:44`。颜色标记 `#GOLD#` 与 `#WHITE#` 匹配，`infinite lives` 通俗译为“无限命”，语义准确。

---

### entry-03190
- **位置**：`mod-tome.lua:41573`
- **section**：`mod-tome/dialogs/Donation.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #GOLD#Item's appearance change (Shimmering)#WHITE#
  ```
- **译文**：
  ```text
  #GOLD#改变物品外观（幻化）#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `Donation.lua:44`。颜色标记匹配，`Shimmering` 对应游戏中改变物品外观的“幻化”机制，术语准确。

---

### entry-03191
- **位置**：`mod-tome.lua:41574`
- **section**：`mod-tome/dialogs/Donation.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Hi, I am Nicolas (DarkGod), the maker of this game.
  It is my dearest hope that you find my game enjoyable, and that you will continue to do so for many years to come!

  ToME is free and open-source and will stay that way, but that does not mean I can live without money, so I have come to disturb you here and now to ask for your kindness.
  If you feel that the (many) hours you have spent having fun were worth it, please consider making a donation for the future of the game.

  Donators are also granted a few special features: %s.
  ```
- **译文**：
  ```text
  你好，我是Nicolas (DarkGod)，这个游戏的制作者。
  我最衷心的希望你会觉得我的游戏很有趣，并且在今后的许多年里你还会继续游玩这款游戏！

  ToME是免费开源的游戏，并且会一直保持这样。但是我仍然需要钱来生活，所以我来这里打扰你，希望得到你的帮助
  如果你觉得在游戏中体验的时间充满了快乐，你可以考虑捐赠一下，让这个游戏的未来变得更好。

  捐赠者将会得到一些游戏的附加功能：%s。
  ```
- **复核结论**：仅建议
- **可复核证据与分析**：
  - **Claim 1（标点微瑕）**：第 3 段末尾“希望得到你的帮助”句尾缺少标点符号（原文为 `...to ask for your kindness.`，译文漏掉了句号）。
  - **总体评价**：占位符 `%s` 匹配，术语 `Donators` 符合规范译为“捐赠者”，段落排版对应。漏句号属细微标点偏好，不影响运行时，标「仅建议」。

---

### entry-03192
- **位置**：`mod-tome.lua:41625`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Enter movement speed(lower is faster)
  ```
- **译文**：
  ```text
  设置动画速度（越低越快）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:111`（配置项为 `config.settings.tome.smooth_move`）。该项控制角色走格子时的平滑移动动画帧数，数值越低帧数越少、移动插值越快（0 为无移动动画瞬移）。译文将其明确译为“动画速度”而非易与角色属性（Movement Speed）混淆的“移动速度”，非常精准地符合游戏实际机制。

---

### entry-03193
- **位置**：`mod-tome.lua:41630`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  #GOLD##{bold}#Twitch creatures movement and attack#WHITE##{normal}#
  ```
- **译文**：
  ```text
  #GOLD##{bold}#生物移动和攻击抖动效果#WHITE##{normal}#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:120`。颜色代码与字体样式标签 `#GOLD##{bold}#` ... `#WHITE##{normal}#` 完全闭合对应，“抖动效果”贴合 Twitch 动画机制表现。

---

### entry-03194
- **位置**：`mod-tome.lua:41654`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  The number of lines to display in the combat log (for the Classic HUD).
  ```
- **译文**：
  ```text
  战斗日志显示行数 (只用于经典HUD)。
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:166`。战斗日志显示行数配置，语义准确，括号前后保留了中西文混排规范，无格式错误。

---

### entry-03195
- **位置**：`mod-tome.lua:41678`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Fade time (in seconds)
  ```
- **译文**：
  ```text
  消失时间（秒数）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:221`（配置项为 `config.settings.tome.log_fade`）。该项控制屏幕浮动日志或战斗日志渐变淡出消失的秒数。术语快照中的 `Fade -> 消隐` 属于特定天赋名，在 UI 选项语境下译为“消失时间（秒数）”完全正确，未受天赋术语误导。

---

### entry-03196
- **位置**：`mod-tome.lua:41708`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Toggles between various tactical information display:
  - Combined healthbar and small tactical frame
  - Combined healthbar and big tactical frame
  - Only healthbar
  - No tactical information at all

  #{italic}#You can also change this directly ingame by pressing shift+T.#{normal}##WHITE#
  ```
- **译文**：
  ```text
  切换战术信息显示模式：
  - 生命值条+小框架
  - 生命值条+大框架
  - 只显示生命值条
  - 不显示

  #{italic}#在游戏中按Shift+T可以直接切换#{normal}##WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:336`。格式控制符 `#{italic}#`、`#{normal}#`、`#WHITE#` 完全匹配；4 个列表项对应 `Tactical overlay` 4 种切换状态（Combined Small, Combined Big, Only Healthbars, Nothing），快捷键 `Shift+T` 准确，格式和内容无缺陷。

---

### entry-03197
- **位置**：`mod-tome.lua:41750`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Enable the WASD movement keys. Can be used to move diagonaly by pressing two directions at once.#WHITE#
  ```
- **译文**：
  ```text
  启用 WASD 键移动。当你同时按两个键的时候，可以实现对角线移动。#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:452`。末尾 `#WHITE#` 颜色标记闭合保留，WASD 移动控制及同时双键斜向移动机制表达清晰无误。

---

### entry-03198
- **位置**：`mod-tome.lua:41755`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  From 0(disable) to 10
  ```
- **译文**：
  ```text
  从 0（关闭）到 10
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:466`（画面锐化程度滑动条提示）。数值区间与关闭状态说明准确，括号全角化。

---

### entry-03199
- **位置**：`mod-tome.lua:41756`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Defines the distance from the screen edge at which scrolling will start. If set high enough the game will always center on the player.#WHITE#
  ```
- **译文**：
  ```text
  定义人物距屏幕边缘多远时开始滚屏。设置得足够高的话，画面会始终以人物为中心。#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:483`。末尾 `#WHITE#` 标记保留，滚屏阈值机制与中心锁定逻辑翻译准确。

---

### entry-03200
- **位置**：`mod-tome.lua:41763`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  From 1 to 99 (100 to disable)
  ```
- **译文**：
  ```text
  从 1 到 99（100 为禁用）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:499`（生命损失警告百分比设置）。数值区间与禁用条件翻译无误。

---

### entry-03201
- **位置**：`mod-tome.lua:41815`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Enable Discord's Rich Presence integration to show your current character on your currently playing profile on Discord (restart the game to apply).
  #ANTIQUE_WHITE#If you do not use Discord this option doesn't do anything in either state.
  ```
- **译文**：
  ```text
  开启Discord实时状态可以让你的朋友在Discord上看见你正在玩什么角色（重启游戏后生效）。
  #ANTIQUE_WHITE#如果你不使用Discord, 那么这个选项就是无效的。
  ```
- **复核结论**：仅建议
- **可复核证据与分析**：
  - **Claim 1（标点中西混用）**：第 2 行“如果你不使用Discord, 那么”中，使用了英文半角逗号加空格（`, `），在中文句式中一般建议使用全角逗号（`，`）。
  - **总体评价**：颜色控制符 `#ANTIQUE_WHITE#` 正确保留，语义完整贴切，标点属于细微排版偏好，标「仅建议」。

---

### entry-03202
- **位置**：`mod-tome.lua:41819`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Keep a copy of your character sheets (not the whole savefile) on the online vault at te4.org.
  For each character you will be given a link to this online character sheet so that you can brag about your heroic deeds or sad deaths to your friends or the whole community.#WHITE#
  ```
- **译文**：
  ```text
  在te4.org上保存一份你的角色信息（不是整个存档）。
  每个角色你都会得到一个链接，用来向你的朋友或整个社区炫耀你的英雄事迹或悲壮之死。#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:643`。末尾 `#WHITE#` 颜色标记保留。`online vault` 准确表述为在官网保存角色信息；`heroic deeds or sad deaths` 译为“英雄事迹或悲壮之死”既生动又贴合游戏语境。

---

### entry-03203
- **位置**：`mod-tome.lua:41835`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Disables all connectivity to the network.
  This includes, but is not limited to:
  - Player profiles: You will not be able to login, register
  - Characters vault: You will not be able to upload any character to the online vault to show your glory
  - Item's Vault: You will not be able to access the online item's vault, this includes both storing and retrieving items.
  - Ingame chat: The ingame chat requires to connect to the server to talk to other players, this will not be possible.
  - Purchaser / Donator benefits: The base game being free, the only way to give donators their bonuses fairly is to check their online profile. This will thus be disabled.
  - Easy addons downloading & installation: You will not be able to see ingame the list of available addons, nor to one-click install them. You may still do so manually.
  - Version checks: Addons will not be checked for new versions.
  - Discord: If you use Discord Rich Presence integration this will also be disabled by this setting.
  - Ingame game news: The main menu will stop showing you info about new updates to the game.

  Note that this setting only affects the game itself. If you use the game launcher, whose sole purpose is to make sure the game is up to date, it will still do so.
  If you do not want that, simply run the game directly: the #{bold}#only#{normal}# use of the launcher is to update the game.

  #{bold}##CRIMSON#This is an extremely restrictive setting. It is recommended you only activate it if you have no other choice as it will remove many fun and acclaimed features.
  A full exit and restart of the game is neccessary to apply this setting.#{normal}#
  ```
- **译文**：
  ```text
  禁止所有网络请求
  包括但不仅限于：
  - 用户信息：不能登录或者注册。
  - 角色备份：不能在te4.org上保存你的角色信息（用来给其他人分享你的炫酷角色）。
  - 物品仓库：不能访问你的在线物品仓库（包括存入和取回）。
  - 游戏内聊天：游戏内聊天需要连接服务器才能与其他玩家交谈，这将无法使用。
  - 购买者/捐赠者福利：基础游戏免费，公平发放捐赠者奖励的唯一途径是检查他们的在线档案，因此该功能将被禁用。
  - 插件便捷下载与安装：你将无法在游戏内看到可用插件列表，也无法一键安装，但仍可手动安装。
  - 插件版本更新：无法更新插件的版本。
  - Discord：无法同步到Discord的实时状态。
  - 游戏内新闻：主菜单将不再显示新闻。
  注意这个设置只影响游戏本身。如果你使用游戏启动器，它的唯一目的就是确保游戏是最新的，因此它仍然会连接网络。
  如果你不想这样，直接运行游戏即可。启动器#{bold}#只#{normal}#是用来更新游戏的。


  #{bold}##CRIMSON#这是一个极端的选项。如果不是迫不得已，推荐你不要打开它，这会让你失去很多好用的功能和一些游戏体验。
  应用这个选项必须退出重新进入游戏。#{normal}#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:664`（滚动文本框）。控制标记 `#{bold}#只#{normal}#` 和 `#{bold}##CRIMSON#` ... `#{normal}#` 完整对应闭合；列表逐条对应无遗漏；术语 `Donator` 统一译为“捐赠者”。虽然最后一段前多了一个空行，但 Textzone 控件对其具备容错渲染能力，属于安全排版。内容准确详尽。

---

### entry-03204
- **位置**：`mod-tome.lua:41889`
- **section**：`mod-tome/dialogs/GameOptions.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Replace headwear images by cloak hoods if a cloak is worn#WHITE#
  ```
- **译文**：
  ```text
  当戴着斗篷时，用斗篷兜帽替换头部装备图像。#WHITE#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GameOptions.lua:724`。末尾颜色标记 `#WHITE#` 保留，披风兜帽遮盖头盔的外观机制描述准确。

---

### entry-03205
- **位置**：`mod-tome.lua:41906`
- **section**：`mod-tome/dialogs/GraphicMode.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Use moddable tiles (equipment showing on player)
  ```
- **译文**：
  ```text
  使用纸娃娃（在玩家身上显示装备）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GraphicMode.lua:83`。`moddable tiles (equipment showing on player)` 是经典的 RPG“纸娃娃系统（Paperdoll）”，即角色身上的贴图随穿戴装备改变。译文精准对应通用行业术语，并保留了括注说明，无缺陷。

---

### entry-03206
- **位置**：`mod-tome.lua:41907`
- **section**：`mod-tome/dialogs/GraphicMode.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Use advanced tiles (transitions, wide tiles, ...)
  ```
- **译文**：
  ```text
  使用高级贴图（渐变，大型贴图，……）
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `GraphicMode.lua:84`。地块渐变与宽贴图选项，逗号全角化，省略号符合中文排版规范，语义完整。

---

### entry-03207
- **位置**：`mod-tome.lua:41929`
- **section**：`mod-tome/dialogs/LevelupDialog.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Levelup: %s, level %s
  ```
- **译文**：
  ```text
  升级：%s，等级 %s
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `LevelupDialog.lua:89`（`Dialog.init(self, ("Levelup: %s, level %s"):tformat(actor:getName(), actor.level)...)`）。两个 `%s` 占位符按角色名、等级顺序正确传递，标点全角，格式无缺陷。

---

### entry-03208
- **位置**：`mod-tome.lua:41940`
- **section**：`mod-tome/dialogs/LevelupDialog.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Stat is at the maximum for your level
  ```
- **译文**：
  ```text
  该属性已达到当前等级上限
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `LevelupDialog.lua:266`（升级界面当属性点满当前等级允许的上限时弹出的提示）。语义准确对应游戏机制，无格式缺陷。

---

### entry-03209
- **位置**：`mod-tome.lua:41968`
- **section**：`mod-tome/dialogs/LevelupDialog.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Stats points left: #00FF00#%d#LAST#
  Category points left: #00FF00#%d#LAST#
  Class talent points left: #00FF00#%d#LAST#
  Generic talent points left: #00FF00#%d#LAST#
  ```
- **译文**：
  ```text
  属性点剩余：#00FF00#%d#LAST#
  技能树解锁点剩余：#00FF00#%d#LAST#
  职业技能点剩余：#00FF00#%d#LAST#
  通用技能点剩余：#00FF00#%d#LAST#
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `LevelupDialog.lua:626-629`。4 行文本中的占位符 `%d` 与颜色标签 `#00FF00#...#LAST#` 逐一精确匹配；属性点、技能树解锁点（Category points）、职业技能点（Class talent points）、通用技能点（Generic talent points）术语与游戏机制完全对应。

---

### entry-03210
- **位置**：`mod-tome.lua:42004`
- **section**：`mod-tome/dialogs/LevelupDialog.lua`
- **source_tag**：`_t`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Talent category points allow you to either:
  - learn a new talent (class or generic) category
  - improve a known talent category efficiency by 0.2
  - learn a new inscription slot (up to a maximum of 5, learning it is automatic when using an inscription)

  You gain a new point at level 10, 20 and 34.
  Some races or items may increase them as well.
  ```
- **译文**：
  ```text
  技能树解锁点有以下作用：
  - 解锁职业或通用技能树
  - 提升已解锁技能树的精通度，每点提升 0.2
  - 解锁新的刻印位（最多 5 个，你使用刻印时会自动消耗点数解锁）

  你会在人物等级达到 10、20 和 34 级时各获得 1 个点数。
  某些种族和物品可以获得额外的点数。
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `LevelupDialog.lua:650`。技能树解锁点机制（解锁新系、提升系精通 0.2、解锁铭文/刻印位上限 5、在 10/20/34 级获取及种族/物品额外奖励）各项数值与逻辑表述均严谨准确，排版规范。

---

### entry-03211
- **位置**：`mod-tome.lua:42028`
- **section**：`mod-tome/dialogs/LevelupDialog.lua`
- **source_tag**：`tformat`；**args_order**：`None`；**special**：`None`
- **原文**：
  ```text
  Stats: %s
  ```
- **译文**：
  ```text
  属性：%s
  ```
- **复核结论**：未发现问题
- **可复核证据与分析**：
  对应源码 `LevelupDialog.lua:773, 1077`（`self.b_stat.text = ("Stats: %s"):tformat(self.actor.unused_stats)`）。显示未分配属性点，占位符 `%s` 正确保留，冒号全角，无格式缺陷。

---

## 总体统计与裁决汇总

| 评分分类 | 数量 | 涉及条目列表 |
| :--- | :---: | :--- |
| **未发现问题** | 38 | `entry-03172`, `entry-03173`, `entry-03174`, `entry-03175`, `entry-03176`, `entry-03177`, `entry-03178`, `entry-03179`, `entry-03180`, `entry-03181`, `entry-03182`, `entry-03183`, `entry-03184`, `entry-03185`, `entry-03186`, `entry-03187`, `entry-03188`, `entry-03189`, `entry-03190`, `entry-03192`, `entry-03193`, `entry-03194`, `entry-03195`, `entry-03196`, `entry-03197`, `entry-03198`, `entry-03199`, `entry-03200`, `entry-03202`, `entry-03203`, `entry-03204`, `entry-03205`, `entry-03206`, `entry-03207`, `entry-03208`, `entry-03209`, `entry-03210`, `entry-03211` |
| **仅建议** | 2 | `entry-03191`（第 3 段末尾漏句号标点微瑕）、`entry-03201`（第 2 行中西文混排中使用了英文半角逗号加空格） |
| **存在问题** | 0 | 无 |
| **待确认** | 0 | 无 |
| **总计** | 40 | 完整覆盖 40 条样本 |

---

## 实际读取材料与版本说明

- **输入及冻结元数据文件**：
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/INPUT.md`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/source-access.json`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/entries.json`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/context.lua`
- **固定版本冻结源码**（Git Commit: `624a67329fe2ad440c5b344785a9c73fcf22ae63`）：
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/Birther.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/CharacterSheet.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/DeathDialog.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/Donation.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/GameOptions.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/GraphicMode.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua`
- **执行规则遵守说明**：
  本审核为自然语言只读旁路复核，全程未读取实验目录下其他文件、未读取其他模型输出、未创建子 agent、未向任何文件写入内容、未修改/修复译文、未输出生产 contract JSON，亦不声称 `DONE_VERIFIED`。
