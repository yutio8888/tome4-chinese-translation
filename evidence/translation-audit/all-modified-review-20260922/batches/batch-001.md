# batch-001：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00001
位置：engine.lua:15；section：.always_merge；source_tag：nil；args_order：None；special：None

原文：
```text
Exploratory Farportal
```
译文：
```text
探索用远行传送门
```

## entry-00002
位置：engine.lua:339；section：engine/engine/Birther.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Keyboard: #00FF00#up key/down key#FFFFFF# to select an option; #00FF00#Enter#FFFFFF# to accept; #00FF00#Backspace#FFFFFF# to go back.
Mouse: #00FF00#Left click#FFFFFF# to accept; #00FF00#right click#FFFFFF# to go back.

```
译文：
```text
键盘：#00FF00#上/下键#FFFFFF#选择选项，#00FF00#回车#FFFFFF#键确定，#00FF00#退格#FFFFFF#键返回。
鼠标：#00FF00#左键#FFFFFF#确定，#00FF00#右键#FFFFFF#返回。

```

## entry-00003
位置：engine.lua:347；section：engine/engine/Birther.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Recreate
```
译文：
```text
重建同一角色
```

## entry-00004
位置：engine.lua:366；section：engine/engine/Chat.lua；source_tag：log；args_order：None；special：None

原文：
```text
following chain...
```
译文：
```text
追踪链接…
```

## entry-00005
位置：engine.lua:396；section：engine/engine/HotkeysIconsDisplay.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Unknown!
```
译文：
```text
未知！
```

## entry-00006
位置：engine.lua:423；section：engine/engine/Module.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This beta version is meant to be tested without addons, as such the following ones are currently disabled:
#GREY#
```
译文：
```text
本Beta版本设计上用于纯原版测试环境，因此，以下插件被自动禁用：
#GREY#
```

## entry-00007
位置：engine.lua:426；section：engine/engine/Module.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}##PINK#Addons developers can still test their addons by enabling developer mode.#{normal}#
```
译文：
```text
#{italic}##PINK#插件开发者可以通过开启开发者模式继续测试他们的插件。#{normal}#
```

## entry-00008
位置：engine.lua:427；section：engine/engine/Module.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Total playtime of all registered players:%s

```
译文：
```text
注册玩家总游玩时间：%s

```

## entry-00009
位置：engine.lua:438；section：engine/engine/Module.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_RED#Online profile disabled(switching to offline profile) due to %s.
```
译文：
```text
#LIGHT_RED#由于 %s，在线账户已禁用（切换至离线账户）。
```

## entry-00010
位置：engine.lua:459；section：engine/engine/PlayerProfile.lua；source_tag：_t；args_order：None；special：None

原文：
```text
no online profile active
```
译文：
```text
未开启在线账户
```

## entry-00011
位置：engine.lua:523；section：engine/engine/Trap.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s fails to disarm a trap (%s).
```
译文：
```text
%s 拆除陷阱（%s）失败。
```

## entry-00012
位置：engine.lua:524；section：engine/engine/Trap.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s disarms a trap (%s).
```
译文：
```text
%s 拆除了陷阱（%s）。
```

## entry-00013
位置：engine.lua:525；section：engine/engine/Trap.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s triggers a trap (%s)!
```
译文：
```text
%s 触发了陷阱（%s）！
```

## entry-00014
位置：engine.lua:536；section：engine/engine/UserChat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#{bold}#Thank you#{normal}# for you donation, your support means a lot for the continued survival of this game.

Your current donation total is #LIGHT_GREEN#%0.2f euro#WHITE# which equals to #ROYAL_BLUE#%d voratun coins#WHITE# to use on te4.org.
Your Item Vault has #TEAL#%d slots#WHITE#.

Again, thank you, and enjoy Eyal!

#{italic}#Your malevolent local god of darkness, #GOLD#DarkGod#{normal}#
```
译文：
```text
#{bold}#感谢#{normal}# 你的捐赠，你的支持对本游戏的持续运营意义重大。

你的捐款总额为#LIGHT_GREEN#%0.2f 欧元#WHITE# 相当于 #ROYAL_BLUE#%d 个沃瑞钽币#WHITE#，可以在 te4.org 上消费。
你的共享仓库有 #TEAL#%d 个槽位#WHITE#。

再次感谢你，祝你在埃亚尔玩的开心！

#{italic}#你的邪恶的黑暗之神，#GOLD#DarkGod#{normal}#
```

## entry-00015
位置：engine.lua:557；section：engine/engine/UserChat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Requesting...
```
译文：
```text
正在请求…
```

## entry-00016
位置：engine.lua:558；section：engine/engine/UserChat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Requesting user info...
```
译文：
```text
正在请求用户信息…
```

## entry-00017
位置：engine.lua:560；section：engine/engine/UserChat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The server does not know about this player.
```
译文：
```text
服务器里没有这个玩家。
```

## entry-00018
位置：engine.lua:605；section：engine/engine/dialogs/ChatFilter.lua；source_tag：_t；args_order：None；special：None

原文：
```text
First time achievements (recommended to keep them on)
```
译文：
```text
第一次取得成就（建议开启）
```

## entry-00019
位置：engine.lua:606；section：engine/engine/dialogs/ChatFilter.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Important achievements (recommended to keep them on)
```
译文：
```text
重要成就（建议开启）
```

## entry-00020
位置：engine.lua:616；section：engine/engine/dialogs/ChatIgnores.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Click a user to stop ignoring her/his messages.
```
译文：
```text
点击一个用户以停止屏蔽他/她的消息。
```

## entry-00021
位置：engine.lua:626；section：engine/engine/dialogs/DisplayResolution.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Continue? %s
```
译文：
```text
继续吗？%s
```

## entry-00022
位置：engine.lua:627；section：engine/engine/dialogs/DisplayResolution.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (progress will be saved)
```
译文：
```text
 （游戏进度会被保存）
```

## entry-00023
位置：engine.lua:683；section：engine/engine/dialogs/GetQuantity.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enter a quantity.
```
译文：
```text
输入数量。
```

## entry-00024
位置：engine.lua:692；section：engine/engine/dialogs/GetQuantitySlider.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enter a quantity.
```
译文：
```text
输入数量。
```

## entry-00025
位置：engine.lua:700；section：engine/engine/dialogs/GetText.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Must be between %i and %i characters.
```
译文：
```text
必须介于 %i 和 %i 个字符之间。
```

## entry-00026
位置：engine.lua:711；section：engine/engine/dialogs/KeyBinder.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
      Press a key (escape to cancel, backspace to remove) for: %s
```
译文：
```text
      请按键（Esc 键取消，退格键删除）以绑定 %s 的键位
```

## entry-00027
位置：engine.lua:714；section：engine/engine/dialogs/KeyBinder.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Make gesture (using right mouse button) or type it (or escape) for: %s
```
译文：
```text
请输入鼠标手势（使用鼠标右键）或者按键 (或按ESC取消) 以绑定 %s 的键位
```

## entry-00028
位置：engine.lua:736；section：engine/engine/dialogs/ShowAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#GOLD#Achieved on:#LAST# %s
#GOLD#Achieved by:#LAST# %s
%s
#GOLD#Description:#LAST# %s
```
译文：
```text
#GOLD#成就达成时间：#LAST# %s
#GOLD#成就获得者：#LAST# %s
%s
#GOLD#介绍：#LAST# %s
```

## entry-00029
位置：engine.lua:743；section：engine/engine/dialogs/ShowAchievements.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Progress: 
```
译文：
```text
进度： 
```

## entry-00030
位置：engine.lua:783；section：engine/engine/dialogs/ShowErrorStack.lua；source_tag：_t；args_order：None；special：None

原文：
```text
If you already reported that error, you do not have to do it again (unless you feel the situation is different).
```
译文：
```text
如果你已经汇报过了这个错误，你不需要再次进行汇报（除非你认为这一情况和之前有所不同）。
```

## entry-00031
位置：engine.lua:784；section：engine/engine/dialogs/ShowErrorStack.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You #LIGHT_GREEN#already reported#WHITE# that error, you do not have to do it again (unless you feel the situation is different).
```
译文：
```text
你 #LIGHT_GREEN#已经汇报过了#WHITE# 这个错误，你不需要再次进行汇报（除非你认为这一情况和之前有所不同）。
```

## entry-00032
位置：engine.lua:800；section：engine/engine/dialogs/ShowErrorStack.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Log saved to file (click to copy to clipboard):#LIGHT_BLUE#%s
```
译文：
```text
游戏日志已保存到文件（点击复制到剪贴板）:#LIGHT_BLUE#%s
```

## entry-00033
位置：engine.lua:802；section：engine/engine/dialogs/ShowErrorStack.lua；source_tag：log；args_order：None；special：None

原文：
```text
#YELLOW#Error report sent, thank you.
```
译文：
```text
#YELLOW#错误报告已发送，谢谢。
```

## entry-00034
位置：engine.lua:872；section：engine/engine/dialogs/SteamOptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Purge all Steam Cloud saves.
This will remove all saves from the cloud cloud (but not your local copy). Only use if you somehow encounter storage problems on it (which should not happen, the game automatically manages it for you).#WHITE#
```
译文：
```text
删除所有Steam云存档。
这会在Steam云中删除所有的云存档，但不会删除你的本地存档。只有在你遇到存储问题的时候才使用这一功能。（一般情况下这不会发生，游戏会自动管理云存档）#WHITE#
```

## entry-00035
位置：engine.lua:905；section：engine/engine/dialogs/UseTalents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You can bind a talent to a hotkey be pressing the corresponding hotkey while selecting a talent.
Check out the keybinding screen in the game menu to bind hotkeys to a key (default is 1-0 plus control or shift).

```
译文：
```text
你可以把技能绑定到一个快捷键。方法是选择一个技能，然后按下对应的快捷键。
请确认游戏菜单中的快捷键绑定界面，将快捷键绑定到键盘按键(默认绑定位置是1-0+Ctrl/Shift键)。

```

## entry-00036
位置：engine.lua:924；section：engine/engine/dialogs/UserInfo.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Currently playing: 
```
译文：
```text
正在玩： 
```

## entry-00037
位置：engine.lua:927；section：engine/engine/dialogs/UserInfo.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Validation: 
```
译文：
```text
认证状态： 
```

## entry-00038
位置：engine.lua:991；section：engine/engine/dialogs/VideoOptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Activates advanced shaders.
This option allows for advanced effects (like water surfaces, ...). Disabling it can improve performance.

#LIGHT_RED#You must restart the game for it to take effect.#WHITE#
```
译文：
```text
开启高级着色器效果。
这个选项可以激活一些高级的视频效果（例如水面效果……）。关闭它可以提升运行速度。

#LIGHT_RED#你必须重启游戏才能看到效果。#WHITE#
```

## entry-00039
位置：engine.lua:999；section：engine/engine/dialogs/VideoOptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Activates distorting shaders.
This option allows for distortion effects (like spell effects doing a visual distortion, ...). Disabling it can improve performance.

#LIGHT_RED#You must restart the game for it to take effect.#WHITE#
```
译文：
```text
开启扭曲着色器效果，
这个选项可以激活一些扭曲视频特效（例如会造成视觉扭曲的法术）
关闭它可以提升运行速度。

#LIGHT_RED#你必须重启游戏才能看到效果。#WHITE#
```

## entry-00040
位置：engine.lua:1008；section：engine/engine/dialogs/VideoOptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Activates volumetric shaders.
This option allows for volumetricion effects (like deep starfields). Enabling it will severely reduce performance when shaders are displayed.

#LIGHT_RED#You must restart the game for it to take effect.#WHITE#
```
译文：
```text
开启体积着色器效果。
这个选项可以激活一些特殊的视频效果（例如星空特效）。开启它会显著降低运行速度。

#LIGHT_RED#你必须重启游戏才能看到效果。#WHITE#
```

## 相关术语快照
```tsv
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
exploratory farportal	探索用远行传送门	T.GAME.ENTITY	items	_t	preferred	core	夏·图尔堡垒用于前往随机探索区域的远行传送门；与普通 farportal 区分，统一设施、任务与警告文本中的引用
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
unknown	未知	T.UI.LABEL	ui	_t	preferred	global	未知条目/名称占位（15 处）
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
