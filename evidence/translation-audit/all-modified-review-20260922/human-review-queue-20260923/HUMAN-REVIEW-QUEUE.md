# 统一人工批阅队列（合并索引）

由 `build_human_review_queue.py` 合并 campaign 各来源生成：只做索引、原文/译文关联、
Sol 原始 verdict 挂接，不新增语义裁决。每条的模型状态原样保留。
`human_decision` 默认空，等待人工填写；填写后写回 JSON 同名字段。

完整模型原文与全部 raw verdict 见 [HUMAN-REVIEW-QUEUE.json](HUMAN-REVIEW-QUEUE.json)；来源哈希见 [SUMMARY.json](SUMMARY.json)。

## 统计

- 待办记录：**601**；涉及 entry：**559**。
- `batch_093`：6 条 / 6 entry；存在疑点=4、细微观察=2
- `batch_094`：4 条 / 4 entry；存在疑点=1、细微观察=3
- `cross_092`：2 条 / 1 entry；confirmed=2
- `human_review_md`：468 条 / 460 entry；advisory=57、confirmed=390、pending=15、refuted=6
- `remaining_review`：121 条 / 88 entry；advisory=51、confirmed=67、refuted=2、upstream=1
- 挂接的 Sol 原始 verdict 参考记录：1103 条（见 JSON `raw_campaign_verdicts`）。

说明：多 entry 行（如 `entry-01706 / 01709 / …`）按首个 entry 归组，行内列出全部 entry。

> 未合并：`reconciled-20260923/FINDINGS.json` 的 714 canonical claims（实验台账，另有自身 ledger）及其 3050 条未映射 observation。

---

## entry-00004

- 位置：`engine.lua:366`（engine）｜section：`engine/engine/Chat.lua`｜source_tag：`log`
- 原文：`following chain...`
- 现译：`追踪链接…`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00001 | HUMAN-REVIEW | cross-batch-001 | confirmed | 是否整理此失效键译文 |  | delete_dead_key |

<details><summary>hrq-00001 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：chain 译成「链接」有偏差；固定版本调用已删除，当前运行时无影响
```
```
raw verdict: 固定版本日志调用已删除→confirmed; chain 译为链接的语义偏差→confirmed
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00039

- 位置：`engine.lua:999`（engine）｜section：`engine/engine/dialogs/VideoOptions.lua`｜source_tag：`_t`
- 原文：`Activates distorting shaders.
This option allows for distortion effects (like spell effects doing a visual distortion, ...). Disabling it can improve performance.

#LIGHT_RED#You must restart the game for it to take effect.#WHITE#`
- 现译：`开启扭曲着色器效果，
这个选项可以激活一些扭曲视频特效（例如会造成视觉扭曲的法术）
关闭它可以提升运行速度。

#LIGHT_RED#你必须重启游戏才能看到效果。#WHITE#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00002 | HUMAN-REVIEW | cross-batch-001 | confirmed | 是否修正标点、整理换行 |  | fix_punctuation_only |

<details><summary>hrq-00002 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两处标点问题和额外硬换行，影响轻微；「严重排版断裂」程度仅 advisory
```
```
raw verdict: 首行逗号代替句号→confirmed; 第二句句末标点遗漏→confirmed; 额外硬换行→confirmed; 严重排版断裂的程度→advisory
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00041

- 位置：`engine.lua:1029`（engine）｜section：`engine/engine/dialogs/VideoOptions.lua`｜source_tag：`_t`
- 原文：`Request a specific origin point for the game window.
This point corresponds to where the upper left corner of the window will be located.
Useful when dealing with multiple monitors and borderless windows.

The default origin is (0,0).

Note: This value will automatically revert after ten seconds if not confirmed by the user.#WHITE#`
- 现译：`设置游戏窗口的原点。
这个点表示窗口左上角所在的位置。
这一选项用于在使用无边框窗口或者多显示器的场合。

默认原点：(0,0)。

注意：如果用户在十秒后不进行确认，这一数值将会自动恢复原值#WHITE#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00003 | HUMAN-REVIEW | cross-batch-002 | confirmed | 是否改为「十秒内未确认」并补句号 |  | fix |

<details><summary>hrq-00003 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：句号遗漏、十秒确认时间条件表达不准确，低影响
```
```
raw verdict: 缺少句号→confirmed; 十秒确认时间条件→confirmed
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00061

- 位置：`engine.lua:1198`（engine）｜section：`engine/engine/interface/ActorInventory.lua`｜source_tag：`logSeen`
- 原文：`%s picks up (%s.): %s%s.`
- 现译：`%s拾取了（%s）：%s%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00004 | HUMAN-REVIEW | cross-batch-002 | advisory | 可选排版整理，不强制修改 |  | no_change |

<details><summary>hrq-00004 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：快捷键点号删除及全角括号不构成错误
```
```
raw verdict: 快捷键点号与括号→advisory
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00063

- 位置：`engine.lua:1213`（engine）｜section：`engine/engine/interface/ActorInventory.lua`｜source_tag：`logSeen`
- 原文：`%s wears: %s.`
- 现译：`%s 装备了：%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00005 | HUMAN-REVIEW | cross-batch-002 | confirmed | 是否删除空格 |  | fix |

<details><summary>hrq-00005 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：角色名后半角空格，同组日志轻微排版不一致
```
```
raw verdict: 角色名后空格→confirmed
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00069

- 位置：`engine.lua:1238`（engine）｜section：`engine/engine/interface/ActorTalents.lua`｜source_tag：`tformat`
- 原文：`not enough stat: %s`
- 现译：`属性点不足：%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00006 | HUMAN-REVIEW | cross-batch-002 | confirmed | 「属性值不足」或「属性不足」的选择 |  | fix |

<details><summary>hrq-00006 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：检查当前属性值，译成「属性点不足」可能误导
```
```
raw verdict: 属性点与属性值→confirmed
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00075

- 位置：`engine.lua:1272`（engine）｜section：`engine/engine/interface/ObjectActivable.lua`｜source_tag：`tformat`
- 原文：`It can be used to activate talent: %s (level %d).`
- 现译：`可以用于激活技能：%s (等级 %d)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00007 | HUMAN-REVIEW | cross-batch-002 | advisory | 可选统一中文括号 |  | fix |

<details><summary>hrq-00007 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：相邻文本括号形式不同
```
```
raw verdict: 括号形式→advisory
```
```
段末说明：下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。 Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
```
</details>

## entry-00090

- 位置：`engine.lua:1420`（engine）｜section：`engine/modules/boot/class/Game.lua`｜source_tag：`_t`
- 原文：`#GOLD#"Tales of Maj'Eyal"#WHITE# is the main game, you can also install more addons or modules by going to https://te4.org/

When inside a module remember you can press Escape to bring up a menu to change keybindings, resolution and other module specific options.

Remember that in most roguelikes death is usually permanent so be careful!

Now go and have some fun!`
- 现译：`#GOLD#马基·埃亚尔的传说#WHITE# 是主游戏，你也可以在 https://te4.org/ 下载到更多游戏插件和游戏模组。

在游戏模组内，你可以按 Esc 键打开菜单，改变按键绑定，游戏分辨率和其他和模组有关的设置。

请记住，在大部分Roguelike游戏里，角色的死亡都是永久的，请小心！

玩的开心！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00008 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 是否修改这处语病 |  | fix |

<details><summary>hrq-00008 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：结句“玩的开心”应为“玩得开心”
```
```
raw verdict: “玩的开心”应为“玩得开心”→confirmed; 格式与调用有效→confirmed; “玩的开心”用字→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00092

- 位置：`engine.lua:1457`（engine）｜section：`engine/modules/boot/class/Game.lua`｜source_tag：`_t`
- 原文：`Oops! It seems like you have the same addon/dlc installed twice.
This is unsupported and would make many things explode. Please remove one of the copies.

Addon name: #YELLOW#%s#LAST#

Check out the following folder on your computer:
%s
%s
`
- 现译：`糟糕！好像你安装了多份同一个插件/DLC。
这种情况不被支持的，会引发很多BUG。请你移除掉多余的文件。

插件名称：#YELLOW#%s#LAST#

请你检查你电脑里的以下文件夹：
%s
%s
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00009 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 是否改写句法 |  | fix |

<details><summary>hrq-00009 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed： “这种情况不被支持的”语病；占位符与颜色码正确
```
```
raw verdict: “这种情况不被支持的”缺少联系成分→confirmed; 三个 `%s`、颜色码和换行保持正确→confirmed; “这种情况不被支持的”语病→confirmed; 三个 `%s`、颜色码及换行正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00094

- 位置：`engine.lua:1478`（engine）｜section：`engine/modules/boot/class/Game.lua`｜source_tag：`_t`
- 原文：`Welcome to #LIGHT_GREEN#Tales of Maj'Eyal#LAST#!

Before you can start dying in many innovative ways we need to ask you about online play.

This is a #{bold}#single player game#{normal}# but it also features many online features to enhance your gameplay and connect you to the community:
* Play from several computers without having to copy unlocks and achievements.
* Talk ingame to other fellow players, ask for advice, share your most memorable moments...
* Keep track of your kill count, deaths, most played classes...
* Cool statistics for to help sharpen your gameplay style
* Install official expansions and third-party addons directly from the game, hassle-free
* Access your purchaser / donator bonuses if you have bought the game or donated on https://te4.org/
* Help the game developers balance and refine the game

You will also have a user page on #LIGHT_BLUE#https://te4.org/#LAST# to show off to your friends.
This is all optional, you are not forced to use this feature at all, but the developer would thank you if you did as it will make balancing easier.`
- 现译：`欢迎来到#LIGHT_GREEN#马基·埃亚尔的传说#LAST#！

在你开始尝试这个游戏里无数有趣的死法之前，我们想问你一下有关在线游戏的事情。

马基·埃亚尔的传说是一个#{bold}#单人游戏#{normal}#，但也提供了丰富的在线功能，可以增强你的游戏体验，并让你和游戏社区建立联系：
* 在多台电脑上游玩，而不需要复制游戏解锁和成就。
* 与其他玩家在游戏内聊天，寻求建议，分享难忘的时刻…
* 记录你的击杀数量，死亡次数，以及玩得最多的职业…
* 用有趣的统计数据帮你打磨自己的游戏风格
* 在游戏里直接安装官方扩展包和第三方插件，免去手动安装的麻烦
* 如果你购买了游戏或是在 https://te4.org/ 上进行了捐助，你可以获得你的购买者/赞助者独享权益
* 帮助游戏开发者调整游戏平衡，让这个游戏变得更好。

你也会获得一个 #LIGHT_BLUE#https://te4.org/#LAST# 上的用户页面，可以用来向你的朋友炫耀。
这一切都是可选的，你可以自愿使用或者关闭这些功能。如果你愿意开启它们，开发者会感谢你的，因为这会让平衡调整变得更简单。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00010 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | pending | 核对术语记录适用范围；是否统一列表标点 |  | fix |

<details><summary>hrq-00010 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：donator“赞助者/捐赠者”无法用允许输入裁定；00094 的句号位置 claim 为 refuted，列表标点不统一仅 advisory
```
```
raw verdict: `donator` 使用“赞助者”而非报告所称 preferred“捐赠者”→pending; “第六个列表项加了句号”→refuted; 影响：Gemini 指认位置错误。列表末项与前项标点不统一可作为→advisory; `donator` 应统一为“捐赠者”的 claim→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00102

- 位置：`engine.lua:1623`（engine）｜section：`engine/modules/boot/data/talents.lua`｜source_tag：`talent name`
- 原文：`Flame`
- 现译：`火焰`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00011 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 核对术语记录；不要仅凭名称改译文 |  | defer |

<details><summary>hrq-00011 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：boot Flame 是 bolt 火焰攻击；refuted：并非必须改成“火球术”，也不是与主游戏完全同一机制；pending：术语表是否仍写“火球术”
```
```
raw verdict: boot `Flame` 是直接火焰投射攻击→confirmed; “与主游戏 Flame 原型完全一致”→refuted; 因机制应译“火球术”，“火焰”会与伤害类型混淆→refuted; 与项目术语条目 `Flame -> 火球术` 冲突→pending; 该技能是 `bolt` 而非范围火球→confirmed; `Fireflash` 才明确使用 `ball`→confirmed; 因而“火焰”是机制错误、必须改“火球术”→refuted; 项目术语表是否仍规定 `Flame -> 火球术`→pending; Gemini 所称仓库所有现有译文均统一为“火焰”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00105

- 位置：`engine.lua:1697`（engine）｜section：`engine/modules/boot/dialogs/FirstRun.lua`｜source_tag：`_t`
- 原文：`You are about to disable all connectivity to the network.
This includes, but is not limited to:
- Player profiles: You will not be able to login, register
- Characters vault: You will not be able to upload any character to the online vault to show your glory
- Item's Vault: You will not be able to access the online item's vault, this includes both storing and retrieving items.
- Ingame chat: The ingame chat requires to connect to the server to talk to other players, this will not be possible.
- Purchaser / Donator benefits: The base game being free, the only way to give donators their bonuses fairly is to check their online profile. This will thus be disabled.
- Easy addons downloading & installation: You will not be able to see ingame the list of available addons, nor to one-click install them. You may still do so manually.
- Version checks: Addons will not be checked for new versions.
- Discord: If you are a Discord user, Rich Presence integration will also be disabled by this setting.
- Ingame game news: The main menu will stop showing you info about new updates to the game.

#{bold}##CRIMSON#This is an extremely restrictive setting. It is recommended you only activate it if you have no other choice as it will remove many fun and acclaimed features.#{normal}#

If you disable this option you can always re-activate it in the Online category of the Game Options menu later on.`
- 现译：`即将禁止所有网络请求
包括但不仅限于：
- 用户信息：不能登录或者注册。
- 角色备份：不能在te4.org上保存你的角色信息（用来给其他人分享你的炫酷角色）。
- 物品仓库：不能访问你的在线物品仓库（包括存入和取回）。
- 游戏内聊天：游戏内聊天需要连接服务器才能与其他玩家交谈，这将无法使用。
- 购买者/捐助者福利：基础游戏免费，公平发放捐助者奖励的唯一途径是检查他们的在线档案，因此该功能将被禁用。
- 插件便捷下载与安装：你将无法在游戏内看到可用插件列表，也无法一键安装，但仍可手动安装。
- 插件版本检查：插件将不再检查新版本。
- Discord：如果你是 Discord 用户，此设置也会禁用 Rich Presence 集成。
- 游戏内新闻：主菜单将不再显示游戏更新信息。

#{bold}##CRIMSON#这是一个极端的选项。如果不是迫不得已，推荐你不要打开它，这会让你失去很多好用的功能和一些游戏体验。#{normal}#

关闭后，可以通过游戏设置菜单的在线选项卡打开。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00012 | HUMAN-REVIEW | cross-batch-003-004 | confirmed | 是否补句号；核对术语 |  | fix |

<details><summary>hrq-00012 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：首行缺句号；pending：捐助者/捐赠者
```
```
raw verdict: “捐助者”违背 preferred“捐赠者”→pending; 首行缺少句末标点→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00110

- 位置：`engine.lua:1779`（engine）｜section：`engine/modules/boot/dialogs/MainMenu.lua`｜source_tag：`_t`
- 原文：`#{bold}##GOLD#Ashes of Urh'Rok - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction wherever they go.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#New class:#WHITE# Doombringers. These avatars of demonic destruction charge into battle with massive two-handed weapons, cutting swaths of firey devastation through hordes of opponents. Armed with flame magic and demonic strength, they delight in fighting against overwhelming odds
#LIGHT_UMBER#New class:#WHITE# Demonologists. Bearing a shield and the magic of the Spellblaze itself, these melee-fighting casters can grow demonic seeds from their fallen enemies. Imbue these seeds onto your items to gain a wide array of new talents and passive benefits, and summon the demons within them to fight!
#LIGHT_UMBER#New race:#WHITE# Doomelves. Shalore who've taken to the demonic alterations especially well, corrupting their typical abilities into a darker form.
#LIGHT_UMBER#New artifacts, lore, zones, events...#WHITE# For your demonic delight!

`
- 现译：`#{bold}##GOLD#乌鲁洛克之烬 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#很多马基埃亚尔的居民都曾经听说过“恶魔”的名字，它们是一群似乎凭空出现的暴虐生物，无论走到哪里都会带来痛苦和毁灭。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#新职业：#WHITE# 毁灭使者。他们是恶魔毁灭力量的化身，手拿双手武器加入战斗，将敌人化为一片火海。他们的手中掌握着火焰的魔法和恶魔的力量，在与势不可挡的敌人战斗中寻求欢愉。
#LIGHT_UMBER#新职业：#WHITE# 恶魔使者。这些近战施法者手拿盾牌，掌握魔法大爆炸本身的力量，可以从倒下的敌人身上培育出恶魔种子。将这些恶魔种子附魔到你的物品里，可以获得各种全新的技能和被动的能力，并召唤种子里的恶魔来加入战斗！
#LIGHT_UMBER#新种族：#WHITE# 魔化精灵。那些被恶魔的力量所改变的永恒精灵，他们的种族能力被腐化成了黑暗的形态。
#LIGHT_UMBER#更多新神器、新手札、新地图、新事件……#WHITE# 体验恶魔的欢愉吧！

`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00013 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 确认项目标准后再决定是否统一 |  | fix |

<details><summary>hrq-00013 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：写成“马基埃亚尔”，与同批“马基·埃亚尔”不一致；pending：项目 preferred 不能在允许输入内独立核验。来源未固定的 Ashes 简中本地化本身无间隔号
```
```
raw verdict: 译文确实写成“马基埃亚尔”，缺少间隔号→confirmed; “明确违反项目 preferred 术语”→pending; “马基埃亚尔”缺少间隔号→confirmed; 明确违反项目 preferred→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00111

- 位置：`engine.lua:1800`（engine）｜section：`engine/modules/boot/dialogs/MainMenu.lua`｜source_tag：`_t`
- 原文：`#{bold}##GOLD#Embers of Rage - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#One year has passed since the one the Orcs call the "Scourge from the West" came and single-handedly crushed the Orc Prides of Grushnak, Vor, Gorbat, and Rak'Shor.  The Allied Kingdoms, now linked by farportal to their distant, long-lost Sunwall allies, have helped them conquer most of Var'Eyal.  The few remnants of the ravaged Prides are caged...  but one Pride remains.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#A whole new campaign:#WHITE# Set one year after the events of the main game, the final destiny of the Orc Prides is up to you. Discover the Far East like you never knew it. 
#LIGHT_UMBER#New classes:#WHITE# Sawbutchers, Gunslingers, Psyshots, Annihilators and Technomanchers. Harness the power of steam to power deadly contraptions to lay waste to all those that oppose the Pride!  
#LIGHT_UMBER#New races:#WHITE# Orcs, Yetis, Whitehooves. Discover the orcs and their unlikely 'allies' as you try to save your Pride from the disasters caused by the one you call 'The Scourge from the West'.
#LIGHT_UMBER#Tinker system:#WHITE# Augment your items with powerful crafted tinkers. Attach rockets to your boots, gripping systems to your gloves and many more.
#LIGHT_UMBER#Salves:#WHITE# Bound to the tinker system, create powerful medical salves to inject into your skin, replacing the infusions§runes system.
#LIGHT_UMBER#A ton#WHITE# of artifacts, lore, zones, events... 

`
- 现译：`#{bold}##GOLD#余烬怒火 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#自从被兽人称为“西方灾星”的那个人，孤身一人粉碎了格鲁希纳克、沃尔、加伯特和拉克肖四大部落之后，已经过了一年的时间。联合王国现在已经通过远行传送门，和他们失落已久的盟友太阳堡垒建立了联系，帮助他们征服了瓦·埃亚尔大陆的近乎全境。被战火蹂躏的兽人部落的少数残余，现在都被联军关押在监狱里……但是，还有一个部落存活了下来。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#全新战役：#WHITE# 故事发生在主游戏事件的一年之后，兽人部落的最终命运由你决定。去探索一个你从未认识过的远东大陆吧！
#LIGHT_UMBER#全新职业：#WHITE# 链锯屠夫，枪手，念力射手，歼灭者和科技法师。掌握蒸汽的力量，驱动致命的装置，用钢铁洪流粉碎那些胆敢反抗部落的人吧！
#LIGHT_UMBER#全新种族：#WHITE# 兽人，雪人，白蹄。了解兽人和他们那些出人意料的“盟友”，努力将你的部落从那个你们称为“西方灾星”的人所带来的灾难中拯救出来。
#LIGHT_UMBER#嵌件系统：#WHITE# 合成强大的嵌件，用于强化你的物品。包括给你的靴子安装火箭，给你的手套安装抓取系统，乃至许多更多的嵌件。
#LIGHT_UMBER#药剂系统：#WHITE# 在嵌件系统中，合成强大的医疗药剂，用于注入你的皮肤，替代原有的纹身和符文系统。
#LIGHT_UMBER#大量#WHITE# 全新神器、手札、地图和事件！

`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00014 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 以项目术语为准，不以 Gemini 所称 DLC 一致性为准 |  | fix |

<details><summary>hrq-00014 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：出现“西方灾星”；refuted：DLC 并未统一为“西方天灾”或全篇“灵能射手”；pending：项目 canonical
```
```
raw verdict: 两处出现“西方灾星”→confirmed; “DLC 中统一使用‘西方天灾’，所以‘西方灾星’错误”→refuted; “项目 preferred 为‘西方天灾’”→pending; `Psyshots` 必须译为“灵能射手”，DLC 全篇一致→refuted; 项目术语是否要求“灵能射手”→pending; 两处“西方灾星”→confirmed; DLC 统一为“西方天灾”→refuted; 项目 preferred 是否为“西方天灾”→pending; DLC 全篇把 `Psyshot` 译作“灵能射手”→refuted; 项目 canonical 是否为“灵能射手”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00112

- 位置：`engine.lua:1823`（engine）｜section：`engine/modules/boot/dialogs/MainMenu.lua`｜source_tag：`_t`
- 原文：`#{bold}##GOLD#Forgotten Cults - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#Not all adventurers seek fortune, not all that defend the world have good deeds in mind. Lately the number of sightings of horrors have grown tremendously. People wander off the beaten paths only to be found years later, horribly mutated and partly insane, if they are found at all. It is becoming evident something is stirring deep below Maj'Eyal. That something is you.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#New class:#WHITE# Writhing Ones. Give in to the corrupting forces and turn yourself gradually into an horror, summon horrors to do your bidding, shed your skin and melt your face to assault your foes. With your arm already turned into a tentacle, what creature can stop you?
#LIGHT_UMBER#New class:#WHITE# Cultists of Entropy. Using its insanity and control of entropic forces to unravel the normal laws of physic this caster class can turn healing into attacks and call upon the forces of the void to reduce its foes to dust.
#LIGHT_UMBER#New race:#WHITE# Drems. A corrupt subrace of dwarves, that somehow managed to keep a shred of sanity to not fully devolve into mindless horrors. They can enter a frenzy and even learn to summon horrors.
#LIGHT_UMBER#New race:#WHITE# Krogs. Ogres transformed by the very thing that should kill them. Their powerful attacks can stun their foes and they are so strong they can dual wield any one handed weapons.
#LIGHT_UMBER#Many new zones:#WHITE# Explore the Scourge Pits, fight your way out of a giant worm (don't ask how you get *in*), discover the wonders of the Occult Egress and many more strange and tentacle-filled zones!
#LIGHT_UMBER#New horrors:#WHITE# You liked radiant horrors? You'll love searing horrors! And Nethergames. And Entropic Shards. And ... more
#LIGHT_UMBER#Sick of your own head:#WHITE#  Replace it with a nice cozy horror!
#LIGHT_UMBER#A ton#WHITE# of artifacts, lore, events... 

`
- 现译：`#{bold}##GOLD#禁忌邪教 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#不是所有的冒险者都在寻求财富，也不是所有保卫世界的人都心存善念。最近，恐魔在大陆上出现的次数急剧增加。不断有人在偏僻的小路上失踪，有时几年后才被人发现，身体却遭受了恐怖的变异，神智也部分失常，也有时候再也无法寻到踪迹。很明显，在马基·埃亚尔的大地深处，有某种东西正在暗中活动。那种东西——就是你。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#新职业：#WHITE# 扭动者。屈服于腐化的力量，让自己逐渐变成一只恐魔。你可以召唤恐魔在战斗中协助自己，褪去自己的皮肤，融化自己的脸庞，作为攻击的武器。当你的手臂也被转化成触手之后，还有什么敌人能阻挡你呢？
#LIGHT_UMBER#新职业：#WHITE# 熵教徒。这种法师职业使用疯狂的能力，掌控了熵的力量，颠覆了传统的物理定律。它们可以将治疗转换成伤害，并召唤虚空的力量，将敌人粉碎为尘土。
#LIGHT_UMBER#新种族：#WHITE# 德瑞姆。他们是矮人的一支腐化分支，但是因为某种原因，保持了一定程度的理性，而没有完全退化成无意识的恐魔。他们可以进入狂热状态，并学会召唤恐魔。
#LIGHT_UMBER#新种族：#WHITE# 克罗格。他们是被本该杀死他们的力量所转化的食人魔。他们强大的攻击可以震慑敌人，并且他们强壮的力量可以双持任何单手武器。
#LIGHT_UMBER#大量全新地图：#WHITE# 探索瘟疫之穴，在一只巨大蠕虫的身体内杀出一条血路(不要问我你是怎么*进来*的)，探索神秘的出口，以及更多奇异的，充满触手的地图！
#LIGHT_UMBER#新的恐魔：#WHITE# 你喜欢光芒恐魔吗？你一定会喜欢上灼光恐魔的！还有彼世之门，还有熵之碎片，还有其他更多怪物！
#LIGHT_UMBER#厌倦了你自己的头？#WHITE#  把它换成一个舒适惬意的恐魔吧！
#LIGHT_UMBER#大量#WHITE# 全新神器、手札、事件……

`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00015 | HUMAN-REVIEW | cross-batch-003-004 entry-0… | confirmed | 裁定 Writhing One 与 nethergate 的正式译名；不要按本次 Gemini claim 改“瘟疫之穴” |  | fix |

<details><summary>hrq-00015 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：“蠕动者”“天灾之穴”指认；冻结 Cults 简中是“苦痛者”“瘟疫之穴”。confirmed：Nethergames 是 Nethergate 笔误，以及半角括号。pending：扭动者/蜿蜒怪人/苦痛者，以及“彼世之门”还是“虚空之门”
```
```
raw verdict: `Writhing Ones` 的“扭动者”与报告所称项目术语“蜿蜒怪人”冲突→pending; “Cults DLC 实际统一译作‘蠕动者’”→refuted; `Scourge Pits` 应为“天灾之穴”，“瘟疫之穴”错误→refuted; `Nethergames` 是对 `Nethergate` 的笔误→confirmed; 但“彼世之门”是否为项目 canonical→pending; 使用半角括号→confirmed; “扭动者”与项目术语“蜿蜒怪人”冲突→pending; Cults DLC 实际译作“蠕动者”→refuted; “瘟疫之穴”与 DLC 的“天灾之穴”冲突→refuted; `Nethergames` 实为 `Nethergate` 笔误→confirmed; “彼世之门”是已确认 canonical→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00139

- 位置：`mod-boot.lua:282`（boot）｜section：`mod-boot/dialogs/FirstRun.lua`｜source_tag：`_t`
- 原文：`You are about to disable all connectivity to the network.
This includes, but is not limited to:
- Player profiles: You will not be able to login, register
- Characters vault: You will not be able to upload any character to the online vault to show your glory
- Item's Vault: You will not be able to access the online item's vault, this includes both storing and retrieving items.
- Ingame chat: The ingame chat requires to connect to the server to talk to other players, this will not be possible.
- Purchaser / Donator benefits: The base game being free, the only way to give donators their bonuses fairly is to check their online profile. This will thus be disabled.
- Easy addons downloading & installation: You will not be able to see ingame the list of available addons, nor to one-click install them. You may still do so manually.
- Version checks: Addons will not be checked for new versions.
- Discord: If you are a Discord user, Rich Presence integration will also be disabled by this setting.
- Ingame game news: The main menu will stop showing you info about new updates to the game.

#{bold}##CRIMSON#This is an extremely restrictive setting. It is recommended you only activate it if you have no other choice as it will remove many fun and acclaimed features.#{normal}#

If you disable this option you can always re-activate it in the Online category of the Game Options menu later on.`
- 现译：`即将禁止所有网络请求
包括但不仅限于：
- 用户信息：不能登录或者注册。
- 角色备份：不能在te4.org上保存你的角色信息（用来给其他人分享你的炫酷角色）。
- 物品仓库：不能访问你的在线物品仓库（包括存入和取回）。
- 游戏内聊天：游戏内聊天需要连接服务器才能与其他玩家交谈，这将无法使用。
- 购买者/捐助者福利：基础游戏免费，公平发放捐助者奖励的唯一途径是检查他们的在线档案，因此该功能将被禁用。
- 插件便捷下载与安装：你将无法在游戏内看到可用插件列表，也无法一键安装，但仍可手动安装。
- 插件版本检查：插件将不再检查新版本。
- Discord：如果你是 Discord 用户，此设置也会禁用 Rich Presence 集成。
- 游戏内新闻：主菜单将不再显示游戏更新信息。

#{bold}##CRIMSON#这是一个极端的选项。如果不是迫不得已，推荐你不要打开它，这会让你失去很多好用的功能和一些游戏体验。#{normal}#

关闭后，可以通过游戏设置菜单的在线选项卡打开。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00016 | HUMAN-REVIEW | cross-batch-003-004 | pending | 是否改服务名；核对 Donator |  | fix |

<details><summary>hrq-00016 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：捐助者；advisory：“角色备份”缩窄了 vault，但后文补出了用途
```
```
raw verdict: “捐助者”与 preferred“捐赠者”冲突→pending; `Characters vault` 被译为“角色备份”→advisory; 富文本标签配对完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。 Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。
```
</details>

## entry-00164

- 位置：`mod-tome.lua:103`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`log`
- 原文：`#VIOLET#Following build order %s; increasing %s by 1.`
- 现译：`#VIOLET#遵循加点顺序%s;增加一点%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00017 | HUMAN-REVIEW | cross-batch-005-partial | confirmed | 是否把半角分号当作需要修正的格式问题；若改，在 `；` 与 `，` 之间选择 |  | fix |

<details><summary>hrq-00017 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：颜色码和两个 `%s` 顺序正确；confirmed：中文句中无空格半角分号。建议改成全角分号或逗号仅为 advisory
```
```
raw verdict: 颜色码及占位符顺序正确→confirmed; 中文句中使用了无空格的半角分号→confirmed; 建议改为全角分号或逗号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-partial-01.md](reports/sol-005-partial-01.md)。 Sol 的综合结论：半角分号的事实成立，但提升为必须修复只算 advisory；“技能树”是否可接受仍是 pending。译文未修改。
```
</details>

## entry-00165

- 位置：`mod-tome.lua:104`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`log`
- 原文：`#VIOLET#Following build order %s; learning talent category %s.`
- 现译：`#VIOLET#遵循加点顺序%s;学会技能树%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00018 | HUMAN-REVIEW | cross-batch-005-partial | confirmed | 用项目术语决定保留“技能树”或改用“技能类别”等；半角分号是否统一 |  | fix |

<details><summary>hrq-00018 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：颜色码与占位符顺序、半角分号。pending：“技能树”是否为正式译法。改全角标点仅为 advisory
```
```
raw verdict: 颜色码及占位符顺序正确→confirmed; 把 `talent category` 译为“技能树”可以接受→pending; 中文句中使用了无空格的半角分号→confirmed; 建议换成全角中文标点→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-partial-01.md](reports/sol-005-partial-01.md)。 Sol 的综合结论：半角分号的事实成立，但提升为必须修复只算 advisory；“技能树”是否可接受仍是 pending。译文未修改。
```
</details>

## entry-00166

- 位置：`mod-tome.lua:105`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`log`
- 原文：`#VIOLET#Following build order %s; learning talent %s.`
- 现译：`#VIOLET#遵循加点顺序%s;学会技能%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00019 | HUMAN-REVIEW | cross-batch-005-partial | confirmed | 是否统一成全角标点 |  | fix |

<details><summary>hrq-00019 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：颜色码、占位符顺序、半角分号。改全角标点仅为 advisory
```
```
raw verdict: 颜色码及占位符顺序正确→confirmed; 中文句中使用了无空格的半角分号→confirmed; 建议换成全角分号或逗号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-partial-01.md](reports/sol-005-partial-01.md)。 Sol 的综合结论：半角分号的事实成立，但提升为必须修复只算 advisory；“技能树”是否可接受仍是 pending。译文未修改。
```
</details>

## entry-00184

- 位置：`mod-tome.lua:225`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`_t`
- 原文：`You have achieved #LIGHT_GREEN#level 50#WHITE#, congratulations!

This level is special, it granted you #LIGHT_GREEN#10#WHITE# more stat points, #LIGHT_GREEN#3#WHITE# more class talent points and #LIGHT_GREEN#3#WHITE# more generic talent points.
Now go forward boldly and triumph!`
- 现译：`你达到了#LIGHT_GREEN#等级 50#WHITE#，祝贺你！
这个等级很特殊，你可以得到额外的#LIGHT_GREEN#10#WHITE#点属性点，#LIGHT_GREEN#3#WHITE#点职业技能点和#LIGHT_GREEN#3#WHITE#点通用技能点。
现在，勇敢的向前并取得最终的胜利吧！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00020 | HUMAN-REVIEW | cross-batch-005-rest | confirmed | 是否恢复双换行并改状语“地”；新增的“最终”可另定 |  | defer |

<details><summary>hrq-00020 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：50 级弹窗少一段间空行；confirmed：“勇敢的向前”应为“勇敢地向前”；颜色码和 50/10/3/3 顺序正确
```
```
raw verdict: 段间空行缺失→confirmed; “勇敢的向前”存在语法问题→confirmed; 颜色标记和数值顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。 Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。
```
</details>

## entry-00185

- 位置：`mod-tome.lua:232`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`log`
- 原文：`#00ffff#Welcome to level %d [%s].`
- 现译：`#00ffff#欢迎来到等级 %d [ %s ]。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00021 | HUMAN-REVIEW | cross-batch-005-rest | advisory | 若项目要求紧凑格式，可统一为 `[%s]` |  | no_change |

<details><summary>hrq-00021 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：方括号内多空格是事实，但没有强制排版规则，不是明确错误。占位符和颜色码正确
```
```
raw verdict: 方括号内增加空格的事实成立，但不是明确错误→advisory; 占位符和颜色码正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。 Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。
```
</details>

## entry-00191

- 位置：`mod-tome.lua:249`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`logSeen`
- 原文：`%s warps space-time to equip: %s.`
- 现译：`%s扭曲空间，切换武器至：%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00022 | HUMAN-REVIEW | cross-batch-005-rest | confirmed | 是否改为“扭曲时空”一类 |  | fix |

<details><summary>hrq-00022 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`space-time` 只译成“空间”，漏了“时间”；后半句和占位符顺序正确
```
```
raw verdict: “space-time”漏译了“时间”→confirmed; 后半句意译及占位符顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。 Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。
```
</details>

## entry-00195

- 位置：`mod-tome.lua:277`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`logPlayer`
- 原文：`You do not have enough %s to use %s.`
- 现译：`你没有足够的%s施展：%s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00023 | HUMAN-REVIEW | cross-batch-005-rest | confirmed | 是否改为“你没有足够的%s来施展%s。”一类 |  | fix |

<details><summary>hrq-00023 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：资源名、技能名顺序正确；confirmed：“施展：%s”把动宾用冒号断开
```
```
raw verdict: 参数含义和顺序正确→confirmed; “施展：%s”中的冒号造成不自然的动宾断裂→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。 Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。
```
</details>

## entry-00198

- 位置：`mod-tome.lua:353`（tome）｜section：`mod-tome/class/Actor.lua`｜source_tag：`_t`
- 原文：`but fumbles!`
- 现译：`但是失败了！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00024 | HUMAN-REVIEW | cross-batch-005-rest | pending | 先核对母句译文，再决定标点放在母句还是片段 |  | fix |

<details><summary>hrq-00024 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：片段会拼进母句，但母句冻结译文不在本包，不能独立确认缺停顿。失败结果和感叹号保留；“失手”措辞只是建议
```
```
raw verdict: 片段拼接机制已确认，但实际中文母句缺少停顿尚不能独立确认→pending; “但是失败了！”保留失败结果及感叹号；措辞精度建议仅属 advisory→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。 Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。
```
</details>

## entry-00216

- 位置：`mod-tome.lua:403`（tome）｜section：`mod-tome/class/EscortRewards.lua`｜source_tag：`_t`
- 原文：`%s, the lost defiler`
- 现译：`%s，迷路的腐化者`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00025 | HUMAN-REVIEW | cross-batch-006 | confirmed | 人物称谓如何名词化“堕落系”；“堕落者”等候选不能仅凭本条自动确定 |  | defer |

<details><summary>hrq-00025 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Defiler` 是职业大系，译成“腐化者”把上位概念收成子职业 `Corruptor`。refuted：护送 NPC 不会从 Corruptor/Reaver 里随机分配职业
```
```
raw verdict: Defiler 是职业大系，译文把它收成腐化者→confirmed; NPC 可能实际被判定为 Reaver 却显示腐化者→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。 Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。
```
</details>

## entry-00221

- 位置：`mod-tome.lua:469`（tome）｜section：`mod-tome/class/Game.lua`｜source_tag：`logPlayer`
- 原文：`#LIGHT_RED#You may not change level without your own body!`
- 现译：`#LIGHT_RED#你只能用自己的身体离开地图！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00026 | HUMAN-REVIEW | cross-batch-006 | confirmed | 项目里 `level` 统一用“层”“关卡”还是“当前地图”；若必须区分 level/zone，本条要调整 |  | no_change |

<details><summary>hrq-00026 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：源码分开检查 level 与 zone，相邻离开区域的译文也写成“离开地图”。advisory：这仍传达了限制，不足以直接定为明显误译
```
```
raw verdict: level 与 zone 在源码中分开检查，两条译文都写成离开地图→confirmed; 因此构成明显误译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。 Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。
```
</details>

## entry-00223

- 位置：`mod-tome.lua:471`（tome）｜section：`mod-tome/class/Game.lua`｜source_tag：`logPlayer`
- 原文：`#LIGHT_RED#You cannot escape your fate by leaving the level!`
- 现译：`#LIGHT_RED#你不能离开地图以求逃避命运！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00027 | HUMAN-REVIEW | cross-batch-006 | confirmed | 与 00221 共用同一个 level 术语决定；不单独硬改成“离开楼层” |  | no_change |

<details><summary>hrq-00027 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：悖论克隆阻止切换 level。refuted：源码没有把这次调用限定为楼梯。advisory：译成“离开地图”不是功能性错译
```
```
raw verdict: EFF_PARADOX_CLONE 阻止 changeLevelCheck→confirmed; 源码把这次调用限定为楼梯→refuted; 离开地图不够精确但不是功能性错译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。 Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。
```
</details>

## entry-00226

- 位置：`mod-tome.lua:501`（tome）｜section：`mod-tome/class/Game.lua`｜source_tag：`tformat`
- 原文：`Kill (%d)!`
- 现译：`杀死 (%d)！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00028 | HUMAN-REVIEW | cross-batch-006 | advisory | 按既有飘字风格选择，没有必须修改的机制依据 |  | fix |

<details><summary>hrq-00028 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：飘字“杀死（%d）”没有改变死亡事件或数值；“击杀”只是更常见的界面说法
```
```
raw verdict: 死亡飘字，%d 是本次伤害总值→confirmed; 杀死应改为击杀→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。 Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。
```
</details>

## entry-00231

- 位置：`mod-tome.lua:510`（tome）｜section：`mod-tome/class/Game.lua`｜source_tag：`log`
- 原文：`You may not auto-explore with enemies in sight (%s to the %s%s)!`
- 现译：`当有敌人在视野里时，你不能自动探索！(%s 在 %s方%s)！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00029 | HUMAN-REVIEW | cross-batch-006 | confirmed | 是否去掉括号前的感叹号；方向拼接需先核对实际方向词 |  | fix |

<details><summary>hrq-00029 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：括号前后各有一个感叹号。pending：方向词是否会展开成“北面方”，允许输入里没有这八个方向的冻结译文
```
```
raw verdict: 括号前后各有一个感叹号→confirmed; 运行时必然展开为北面方一类→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。 Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。
```
</details>

## entry-00244

- 位置：`mod-tome.lua:674`（tome）｜section：`mod-tome/class/MapEffects.lua`｜source_tag：`_t`
- 原文：` area effect`
- 现译：`范围效果`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00030 | HUMAN-REVIEW | cross-batch-007 | refuted | 无须修改，除非项目另有强制的中文拼接空格规范 |  | refuted |

<details><summary>hrq-00030 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：去掉 ` area effect` 的前导空格没有造成中文拼接缺陷；补回空格会变成“火焰 范围效果”
```
```
raw verdict: 去掉 area effect 前导空格会造成拼接问题→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-007-01.md](reports/sol-007-01.md)。译文未修改。
```
</details>

## entry-00247

- 位置：`mod-tome.lua:719`（tome）｜section：`mod-tome/class/Object.lua`｜source_tag：`tformat`
- 原文：`%s, %d apr, %s element`
- 现译：`%s, %d 护甲穿透，%s 伤害`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00031 | HUMAN-REVIEW | cross-batch-007 | advisory | 选择保留“伤害”，或改成更显式的“元素/属性”；不建议仅凭本条自动修改 |  | fix |

<details><summary>hrq-00031 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`element` 译成“伤害”后与普通 damage 的字面区别消失，但“火焰伤害”一类显示自然，不足以认定为实质误译
```
```
raw verdict: element 译成伤害抹去与 damage 的字面区别，但不足以认定为实质误译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-007-01.md](reports/sol-007-01.md)。译文未修改。
```
</details>

## entry-00254

- 位置：`mod-tome.lua:737`（tome）｜section：`mod-tome/class/Object.lua`｜source_tag：`_t`
- 原文：` APR (max 50%)`
- 现译：` 护甲穿透（最大 50%）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00032 | HUMAN-REVIEW | cross-batch-007 | confirmed | 若统一排版，改为“最大50%”；若允许数字前空格，需要解释为何只有本条例外 |  | no_change |

<details><summary>hrq-00032 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同组 entry-00250–00253 是“最大40%”等无空格写法，只有本条是“最大 50%”。护甲穿透和 50% 数值正确
```
```
raw verdict: 最大 50% 与同组最大40%等排版不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-007-01.md](reports/sol-007-01.md)。译文未修改。
```
</details>

## entry-00284

- 位置：`mod-tome.lua:986`（tome）｜section：`mod-tome/class/Object.lua`｜source_tag：`tformat`
- 原文：`Talent on hit(spell): %s (%d%% chance level %d).`
- 现译：`技能（法术）命中后释放：%s (%d%% 几率等级 %d)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00033 | HUMAN-REVIEW | cross-batch-008 | advisory | 是否改成“法术命中时释放技能”；最小改动可保留 |  | fix |

<details><summary>hrq-00033 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：机制和占位符正确；“技能（法术）命中后释放”稍紧，容易读成技能本身命中
```
```
raw verdict: 法术命中后释放的语序紧凑，但不是明确错译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00286

- 位置：`mod-tome.lua:988`（tome）｜section：`mod-tome/class/Object.lua`｜source_tag：`tformat`
- 原文：`Talent on hit(mindpower): %s (%d%% chance level %d).`
- 现译：`技能（精神）命中后释放：%s (%d%% 几率等级 %d)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00034 | HUMAN-REVIEW | cross-batch-008 | confirmed | 是否与法术、自然两条一起统一语序；不要改成“精神强度命中” |  | fix |

<details><summary>hrq-00034 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：触发条件是来源技能的 `is_mind`，不是精神强度数值。语序仍紧凑
```
```
raw verdict: 机制是 is_mind 而非 Mindpower 数值→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00288

- 位置：`mod-tome.lua:1031`（tome）｜section：`mod-tome/class/Object.lua`｜source_tag：`tformat`
- 原文：`This object's appearance was changed to %s`
- 现译：`这个物品的外观被改变为 %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00035 | HUMAN-REVIEW | cross-batch-008 | confirmed | 主体句号和后续独立句点要一起改，避免只剩西文句点 |  | fix |

<details><summary>hrq-00035 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：主体译文已有句号，源码还会再追加 `_t"."`。refuted：不能确定中间有空格，较可能是 `。.`
```
```
raw verdict: 主体译文已带句号，源码还会再追加句点→confirmed; 精确形态一定是带空格的 。 .→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00298

- 位置：`mod-tome.lua:1115`（tome）｜section：`mod-tome/class/Player.lua`｜source_tag：`logPlayer`
- 原文：`Your antimagic disrupts %s.`
- 现译：`你的反魔法技能打断了 %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00036 | HUMAN-REVIEW | cross-batch-008 | confirmed | 先确认旧条目是否仍被兼容路径使用，再决定保留、改措辞或清理 |  | fix |

<details><summary>hrq-00036 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`forbid_arcane` 阻止使用奥术物品。pending：迁移历史不能在固定 commit 内确认。advisory：`logPlayer` 标签在固定版本没有找到直接消费者
```
```
raw verdict: forbid_arcane 阻止奥术物品，不是技能被打断→confirmed; 历史提交把字符串从 Player.lua 移到 Object.lua→pending; 固定版本中 logPlayer 标签没有直接消费者→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00299

- 位置：`mod-tome.lua:1116`（tome）｜section：`mod-tome/class/Player.lua`｜source_tag：`tformat`
- 原文：`Your antimagic disrupts %s.`
- 现译：`你的反魔法技能打断了 %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00037 | HUMAN-REVIEW | cross-batch-008 | confirmed | 在“你的反魔法干扰了 %s”和“你的反魔法使 %s 无法使用”之间选择 |  | fix |

<details><summary>hrq-00037 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这是当前 `:tformat` 活动译文；“反魔法技能打断了”额外引入技能，并把物品当打断宾语
```
```
raw verdict: 这是活动的 tformat 译文，且“反魔法技能打断了”不够准确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00318

- 位置：`mod-tome.lua:1223`（tome）｜section：`mod-tome/class/Trap.lua`｜source_tag：`log`
- 原文：`#CADET_BLUE#You %s a trap (%s).`
- 现译：`#CADET_BLUE#你%s了一个陷阱(%s)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00038 | HUMAN-REVIEW | cross-batch-008 | confirmed | 让模板不再额外加“了”，并核对所有动作片段都能接宾语 |  | fix |

<details><summary>hrq-00038 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：多个避开动作已带“了”，模板再加“了一个陷阱”。refuted：玩家日志在 `Trap.lua:288`，不是 290
```
```
raw verdict: 动作片段已带了，模板再加了一个，形成双了→confirmed; 玩家日志位于 Trap.lua:290→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。 Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。
```
</details>

## entry-00334

- 位置：`mod-tome.lua:1295`（tome）｜section：`mod-tome/class/generator/actor/Arena.lua`｜source_tag：`log`
- 原文：`#YELLOW#You defeat an experienced enemy!`
- 现译：`#YELLOW#你杀死了一名老练的敌人！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00039 | HUMAN-REVIEW | cross-batch-009 | confirmed | 是否改成更贴近 defeat 的“击败了一名强敌”；不因准确性强制修改。实际日志在 `Arena.lua:555` |  | no_change |

<details><summary>hrq-00039 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：日志在敌人 `on_die` 中，等级差超过 3 时输出。“杀死”没有机制误译
```
```
raw verdict: defeat 译为杀死符合 on_die 触发→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-009-01.md](reports/sol-009-01.md)。译文未修改。
```
</details>

## entry-00344

- 位置：`mod-tome.lua:1379`（tome）｜section：`mod-tome/class/interface/Combat.lua`｜source_tag：`logSeen`
- 原文：`#ORCHID#%s cleverly deflects the attack with %s shield!#LAST#`
- 现译：`#ORCHID#%s用%s的盾牌机智地偏转了这次攻击！#LAST#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00040 | HUMAN-REVIEW | cross-batch-009 | confirmed | 最小修正是删掉占位符后的额外“的” |  | fix |

<details><summary>hrq-00040 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二个 `%s` 展开为“她的/它的/他的”，后面再加“的”会稳定变成“的的盾牌”
```
```
raw verdict: his/her/its 后再加的会叠成的的→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-009-01.md](reports/sol-009-01.md)。译文未修改。
```
</details>

## entry-00345

- 位置：`mod-tome.lua:1380`（tome）｜section：`mod-tome/class/interface/Combat.lua`｜source_tag：`logSeen`
- 原文：`#ORCHID#%s parries the attack with %s dual weapons!#LAST#`
- 现译：`#ORCHID#%s用%s双持武器使这次攻击发生偏斜！#LAST#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00041 | HUMAN-REVIEW | cross-batch-009 | confirmed | 若统一文风可改成“用%s双持武器招架了这次攻击”；否则不必改。日志在 `Combat.lua:482` |  | no_change |

<details><summary>hrq-00041 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：双持这条不会叠词，招架成功会挡住攻击。advisory：“发生偏斜”偏生硬，弱化了招架
```
```
raw verdict: 双持占位符不会叠词，防御成功含义保留→confirmed; 使这次攻击发生偏斜弱化了招架→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-009-01.md](reports/sol-009-01.md)。译文未修改。
```
</details>

## entry-00354

- 位置：`mod-tome.lua:1428`（tome）｜section：`mod-tome/class/interface/PartyIngredients.lua`｜source_tag：`log`
- 原文：`You collect a new ingredient: #LIGHT_GREEN#%s%s (%d)#WHITE#.`
- 现译：`你搜集了一个新的材料：#LIGHT_GREEN#%s%s(%d)#WHITE#。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00042 | HUMAN-REVIEW | cross-batch-009 | confirmed | 无实质待决。“搜集/收集”和空格只是文风 |  | fix |

<details><summary>hrq-00042 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：去掉数量括号前的半角空格不影响占位符和机制
```
```
raw verdict: 去掉数量括号前半角空格不构成问题→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-009-01.md](reports/sol-009-01.md)。译文未修改。
```
</details>

## entry-00368

- 位置：`mod-tome.lua:1579`（tome）｜section：`mod-tome/class/interface/TooltipsData.lua`｜source_tag：`_t`
- 原文：`#GOLD#Equilibrium#LAST#
Equilibrium reflects your standing in the grand balance of nature and how easily you can access Wild Gifts.
The closer it is to 0 the more in-balance you are.
Being too far out of balance may cause your Wild Gifts to fail when called upon.
`
- 现译：`#GOLD#失衡值#LAST#
失衡值是你保持自然平衡的能力，决定了你使用野性系技能的难易程度。
失衡值越接近于0你破坏自然平衡的量越少。
当你的失衡值过高时，你使用野性系技能时可能会失败。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00043 | HUMAN-REVIEW | cross-batch-010 | confirmed | 是否改成“反映你在自然平衡中的状态”一类 |  | fix |

<details><summary>hrq-00043 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：首句把失衡值说成“能力”，容易暗示数值越高越强，和“接近 0 更平衡”相反
```
```
raw verdict: 失衡值被说成能力，方向容易反→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-010-01.md](reports/sol-010-01.md)。译文未修改。Sol 的总括是 3 条 confirmed、8 条 advisory，没有 refuted 或 pending。
```
</details>

## entry-00373

- 位置：`mod-tome.lua:1689`（tome）｜section：`mod-tome/class/interface/TooltipsData.lua`｜source_tag：`_t`
- 原文：`#GOLD#Passive Talents#LAST#
When learned, passive talents permanently alter the user in some way.
The effects are always present and are usually not dispellable or removable, though other effects may counteract or negate them.
Specific information on each talent appears its tooltip.`
- 现译：`#GOLD#被动技能#LAST#
当你学会被动技能之后，它会以某种方式永久性的给玩家带来改变。
这些效果始终存在，通常不会被解除或移除，但是有些特殊效果可能会抵消或消除它们。
有关技能的详细信息，请参阅技能的提示框。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00044 | HUMAN-REVIEW | cross-batch-010 | confirmed | 在“永久改变你/角色/使用者”之间选全篇口吻 |  | fix |

<details><summary>hrq-00044 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：原文改变的是技能使用者，译文后半改成“给玩家”
```
```
raw verdict: 被动改变的是使用者，译文改成了玩家→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-010-01.md](reports/sol-010-01.md)。译文未修改。Sol 的总括是 3 条 confirmed、8 条 advisory，没有 refuted 或 pending。
```
</details>

## entry-00374

- 位置：`mod-tome.lua:1772`（tome）｜section：`mod-tome/class/interface/TooltipsData.lua`｜source_tag：`_t`
- 原文：`#GOLD#Magic#LAST#
Magic defines your character's ability to manipulate the magical energy of the world. It increases your Spellpower, Spell Save, and the effect of spells and other magic items.
`
- 现译：`#GOLD#魔法#LAST#
魔法属性影响你驾驭魔法能量的能力，提升魔法可以提高你的法术强度，提升法术豁免，并提高法术和其他魔法物品的效果。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00045 | HUMAN-REVIEW | cross-batch-010 | confirmed | 标题和属性代称是否统一为“魔力”，魔法能量仍可保留“魔法” |  | fix |

<details><summary>hrq-00045 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这里是基础属性 Magic，面板和源码简中是“魔力”，提示写成“魔法”
```
```
raw verdict: 基础属性 Magic 面板是魔力，提示写成魔法→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-010-01.md](reports/sol-010-01.md)。译文未修改。Sol 的总括是 3 条 confirmed、8 条 advisory，没有 refuted 或 pending。
```
</details>

## entry-00393

- 位置：`mod-tome.lua:2281`（tome）｜section：`mod-tome/class/interface/WorldAchievements.lua`｜source_tag：`tformat`
- 原文：`%s (Roguelike)`
- 现译：`%s（永久死亡模式）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00046 | HUMAN-REVIEW | cross-batch-010 entry-00393… | advisory | 是否给整组后缀定统一排版；不统一也不必单条修改 |  | no_change |

<details><summary>hrq-00046 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：模式和难度含义、占位符都对；单模式用全角括号，复合后缀用半角外括号。多数行号被 Sol 按固定 commit 更正
```
```
raw verdict: 单模式后缀本身正确，只是括号风格不同→advisory; 探索模式后缀本身正确→advisory; 复合后缀含义正确，外层半角括号只是排版→advisory; 噩梦永久死亡后缀正确，只是括号风格→advisory; 疯狂冒险后缀正确，只是括号风格→advisory; 复合后缀正确，只是括号风格→advisory; 绝望冒险后缀正确，只是括号风格→advisory; 绝望永久死亡后缀正确，只是括号风格→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-010-01.md](reports/sol-010-01.md)。译文未修改。Sol 的总括是 3 条 confirmed、8 条 advisory，没有 refuted 或 pending。
```
</details>

## entry-00419

- 位置：`mod-tome.lua:2646`（tome）｜section：`mod-tome/data/achievements/kills.lua`｜source_tag：`_t`
- 原文：`Did over 1500 damage in one attack.`
- 现译：`在一次攻击中造成超过1500点伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00047 | HUMAN-REVIEW | cross-batch-011 | advisory | 是否统一为“超过 1500 点” |  | no_change |

<details><summary>hrq-00047 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：数值正确，只是“超过1500点”和同组“超过 600 点”等空格不一致
```
```
raw verdict: 超过1500点与同组数字空格不一致→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。
```
</details>

## entry-00423

- 位置：`mod-tome.lua:2694`（tome）｜section：`mod-tome/data/achievements/kills.lua`｜source_tag：`_t`
- 原文：`Avoid death 50 times with a life-saving talent.`
- 现译：`使用技能躲避50次死亡。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00048 | HUMAN-REVIEW | cross-batch-011 | confirmed | 选用“保命技能”“免死技能”或“借助技能免于死亡”，并决定数字空格 |  | fix |

<details><summary>hrq-00048 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`life-saving talent` 被写成任意“技能”，漏掉免死/替死限制
```
```
raw verdict: life-saving talent 被泛化为任意技能→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。
```
</details>

## entry-00428

- 位置：`mod-tome.lua:2784`（tome）｜section：`mod-tome/data/achievements/quests.lua`｜source_tag：`_t`
- 原文：`Fought the two Sorcerers and closed three invocation portals.`
- 现译：`在关闭3扇召唤传送门的情况下，与两名巫师交战。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00049 | HUMAN-REVIEW | cross-batch-011 | advisory | 是否按同系列模板改写 |  | no_change |

<details><summary>hrq-00049 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：关闭三扇传送门的条件和数量都对，只是句式与一扇、两扇不平行
```
```
raw verdict: 三扇传送门句式与同系列不统一，机制未错→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。
```
</details>

## entry-00429

- 位置：`mod-tome.lua:2788`（tome）｜section：`mod-tome/data/achievements/quests.lua`｜source_tag：`_t`
- 原文：`Win the game without ever setting foot on Maj'Eyal.`
- 现译：`在没有去过旧大陆的情况下通关游戏。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00050 | HUMAN-REVIEW | cross-batch-011 | confirmed | 专名泛化已有源码依据；正式译名仍待术语记录确认 |  | fix |

<details><summary>hrq-00050 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Maj'Eyal` 被写成“旧大陆”。pending：术语库是否强制“马基·埃亚尔”不在本次允许输入内
```
```
raw verdict: Maj'Eyal 被泛化为旧大陆→confirmed; 术语库强制马基·埃亚尔→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。
```
</details>

## entry-00434

- 位置：`mod-tome.lua:2804`（tome）｜section：`mod-tome/data/achievements/quests.lua`｜source_tag：`_t`
- 原文：`Completed the Master Jeweler quest with Limmir.`
- 现译：`与利米尔一同完成了珠宝匠托付的任务“遗失的知识”。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00051 | HUMAN-REVIEW | cross-batch-011 | confirmed | 保留任务名增补，或收成更贴近原文的说法；若保留，确认“遗失的知识”是否为正式译名 |  | no_change |

<details><summary>hrq-00051 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：任务名是 `Lost Knowledge`。advisory：增补“遗失的知识”有助于检索，但“珠宝匠托付”比源码关系更解释性
```
```
raw verdict: 相关任务正式名是 Lost Knowledge→confirmed; 增补遗失的知识无条件有益→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。
```
</details>

## entry-00443

- 位置：`mod-tome.lua:2864`（tome）｜section：`mod-tome/data/achievements/talents.lua`｜source_tag：`_t`
- 原文：`Unlocked Archmage class and did over one million cold damage (with any item/talent/class).`
- 现译：`解锁元素法师职业并造成超过100万冰冷伤害（使用任意物品/技能/职业）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00052 | HUMAN-REVIEW | cross-batch-012 | confirmed | 提供术语裁决后才能决定“冰冷”还是“寒冷” |  | fix |

<details><summary>hrq-00052 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：统计的是 `COLD` 伤害。pending：必须改成“寒冷伤害”缺少冻结术语依据，“冰冷伤害”本身能传达含义
```
```
raw verdict: 成就统计的是 COLD 伤害→confirmed; 冰冷伤害必须改为寒冷伤害→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。
```
</details>

## entry-00448

- 位置：`mod-tome.lua:2886`（tome）｜section：`mod-tome/data/birth/classes/adventurer.lua`｜source_tag：`_t`
- 原文：`#{bold}##GOLD#This is a bonus class for the chaotically inclined. It is by no means balanced, fun or winnable, it is most of all #{italic}#RANDOM#{bold}#.#WHITE##{normal}#`
- 现译：`#{bold}##GOLD#这是倾向混乱的奖励职业。显然，他并不平衡，也不保证有趣或者能通关。一切为了 #{italic}#随机#{bold}#。#WHITE##{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00053 | HUMAN-REVIEW | cross-batch-012 | confirmed | 是否改成“最重要的是，它完全随机”；代词可改“它”或省略 |  | fix |

<details><summary>hrq-00053 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：格式码完整；“一切为了随机”偏离 `most of all`。advisory：“他”指代职业只是表达问题
```
```
raw verdict: 格式控制码完整→confirmed; 他指代职业不够自然→advisory; 一切为了随机偏离 most of all→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。
```
</details>

## entry-00455

- 位置：`mod-tome.lua:2932`（tome）｜section：`mod-tome/data/birth/classes/celestial.lua`｜source_tag：`_t`
- 原文：`Their way of life is well represented by their motto 'The Sun is our giver, our purity, our essence. We carry the light into dark places, and against our strength none shall pass.'`
- 现译：`他们的生活方式集中体现在他们的座右铭中：太阳是我们的赐予者、我们的纯洁、我们的本质。我们为黑暗带去光明，任何反抗我们的力量都休想通过。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00054 | HUMAN-REVIEW | cross-batch-012 | confirmed | 是否改成“在我们的力量面前，谁也休想通过” |  | fix |

<details><summary>hrq-00054 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：引号改冒号是风格。confirmed：末句把“在我们的力量面前无人通过”说成反抗的力量通过
```
```
raw verdict: 引号改冒号是标点风格→advisory; 末句把力量理解成通过的主体→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。
```
</details>

## entry-00458

- 位置：`mod-tome.lua:2943`（tome）｜section：`mod-tome/data/birth/classes/celestial.lua`｜source_tag：`_t`
- 原文：`Their way of life is well represented by their motto 'We stand betwixt the Sun and Moon, where light and darkness meet. In the grey twilight we seek our destiny.'`
- 现译：`他们的生活方式集中体现在他们的座右铭中：我们站在太阳与月亮之间，光暗交替之界。在灰色的黎明中寻找我们的使命。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00055 | HUMAN-REVIEW | cross-batch-012 | confirmed | 若无相反术语，优先“灰色暮光”或“灰暗暮光” |  | fix |

<details><summary>hrq-00055 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：在该职业里“灰色的黎明”不合适，应靠拢“暮光”。refuted：不能说 twilight 绝对不能指黎明。advisory：“微光/暮色”不如“暮光”贴切
```
```
raw verdict: 灰色的黎明不适合该职业的 twilight→confirmed; twilight 在词义上绝不能指黎明→refuted; 暮光微光暮色同等合适→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。
```
</details>

## entry-00476

- 位置：`mod-tome.lua:3046`（tome）｜section：`mod-tome/data/birth/classes/psionic.lua`｜source_tag：`_t`
- 原文：`Weakness of flesh can be overcome by mental prowess. Find the way and fight for the way to open the key to your mind.`
- 现译：`肉体的软弱可以被精神的强大所克服。寻找道路，并为之奋战，以打开通往你精神世界的钥匙。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00056 | HUMAN-REVIEW | cross-batch-012 | confirmed | 记录解锁限定；决定如何同时保留“道路”和“维网”；英文原句本身也不寻常，修法需人工选定 |  | fix |

<details><summary>hrq-00056 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：线索指向维网，但只有伊克族对话才解锁灵能系；译文漏了 way/The Way 双关；“打开钥匙”搭配不当
```
```
raw verdict: 指向维网行者，但解锁还要求伊克族对话→confirmed; 译文漏了 way 与 The Way 的双关→confirmed; 打开钥匙搭配不当→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。
```
</details>

## entry-00486

- 位置：`mod-tome.lua:3128`（tome）｜section：`mod-tome/data/birth/classes/warrior.lua`｜source_tag：`_t`
- 原文：`Their most important stats are: Dexterity and Strength (when using bows) or Cunning (when using slings)`
- 现译：`他们最重要的属性是：敏捷和力量（装备弓时）或灵巧（装备投石索）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00057 | HUMAN-REVIEW | cross-batch-013 | advisory | 是否只为整齐补上“时” |  | no_change |

<details><summary>hrq-00057 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：后半少了“时”。refuted：这里把 using 译成“装备”没有词义偏移
```
```
raw verdict: 后半括号少了时，结构不对称→advisory; using 译为装备产生词义偏移→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。
```
</details>

## entry-00489

- 位置：`mod-tome.lua:3136`（tome）｜section：`mod-tome/data/birth/classes/warrior.lua`｜source_tag：`_t`
- 原文：`They are adept with two-handed weapons, for the sheer destruction they can bring.`
- 现译：`他们擅长使用双手武器，造成最大的伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00058 | HUMAN-REVIEW | cross-batch-013 | confirmed | 是否改成更贴近“强大的破坏力” |  | fix |

<details><summary>hrq-00058 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“最大的伤害”把修辞收成最高级。confirmed：双手高伤害没有机制错误
```
```
raw verdict: sheer destruction 被写成最大的伤害→advisory; 双手武器高伤害没有机制错误→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。
```
</details>

## entry-00492

- 位置：`mod-tome.lua:3145`（tome）｜section：`mod-tome/data/birth/classes/warrior.lua`｜source_tag：`_t`
- 原文：`Whether a pit-fighter, a boxer, or just an amateur practitioner, the Brawler's skills are still handy today.`
- 现译：`无论是一个职业拳手还是个业余的门外汉，格斗技能直到现在仍然十分有用。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00059 | HUMAN-REVIEW | cross-batch-013 | confirmed | 选定 pit-fighter 译名；业余练习者不宜再写成门外汉 |  | defer |

<details><summary>hrq-00059 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏了 pit-fighter；amateur practitioner 译成“门外汉”把身份说反了
```
```
raw verdict: 漏了 pit-fighter 这一并列身份→confirmed; amateur practitioner 译成门外汉→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。
```
</details>

## entry-00500

- 位置：`mod-tome.lua:3192`（tome）｜section：`mod-tome/data/birth/classes/wilder.lua`｜source_tag：`_t`
- 原文：`Stone Wardens are dwarves trained in both the eldritch arts and the worship of nature.`
- 现译：`岩石守卫是同时研习奥术技艺与自然崇拜的矮人。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00060 | HUMAN-REVIEW | cross-batch-013 | confirmed | 若要跨组件统一，另核术语适用范围；否则可保留 |  | no_change |

<details><summary>hrq-00060 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“奥术技艺”符合该职业的奥术机制。pending：不能据此认定必须改成 Cults 的“骇异”。advisory：诡秘色彩变弱
```
```
raw verdict: 奥术技艺符合该职业的奥术机制→confirmed; Cults 把 eldritch 统一为骇异所以此处偏离→pending; 未保留 eldritch 的诡秘色彩→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。
```
</details>

## entry-00501

- 位置：`mod-tome.lua:3250`（tome）｜section：`mod-tome/data/birth/descriptors.lua`｜source_tag：`_t`
- 原文：`Player is being hunted! Randomly all foes in a radius will get a feeling of where she/he is`
- 现译：`玩家处于被捕猎的状态，随机地，一定半径内的所有敌人都会感知到你所在的位置。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00061 | HUMAN-REVIEW | cross-batch-013 | confirmed | 是否统一人称和感叹号 |  | no_change |

<details><summary>hrq-00061 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：感叹号改逗号，以及“玩家/你”切换。confirmed：被追猎的机制说明准确
```
```
raw verdict: 感叹号改成逗号→advisory; 玩家与你人称切换→advisory; 被追猎的机制说明准确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。
```
</details>

## entry-00522

- 位置：`mod-tome.lua:3705`（tome）｜section：`mod-tome/data/birth/races/undead.lua`｜source_tag：`_t`
- 原文：`- special ghoul talents: ghoulish leap, gnaw and retch`
- 现译：`- 特殊食尸鬼技能：食尸鬼跳跃、啃噬和腐秽呕吐`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00062 | HUMAN-REVIEW | cross-batch-014 | confirmed | 决定改介绍还是校准术语库；不能只凭其他技能条目反向改术语 |  | no_change |

<details><summary>hrq-00062 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这里译成“食尸鬼跳跃”，冻结术语快照的 preferred 是“定向跳跃”
```
```
raw verdict: 食尸鬼跳跃与术语快照定向跳跃不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-014-01.md](reports/sol-014-01.md)。译文未修改。
```
</details>

## entry-00527

- 位置：`mod-tome.lua:3748`（tome）｜section：`mod-tome/data/birth/races/undead.lua`｜source_tag：`_t`
- 原文：`They have access to #GOLD#special skeleton talents#WHITE# and a wide range of undead abilities:`
- 现译：`它们天生具有#GOLD#特殊骷髅技能#WHITE#和一系列不死系技能：`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00063 | HUMAN-REVIEW | cross-batch-014 | confirmed | 是否统一为“不死系能力” |  | fix |

<details><summary>hrq-00063 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“不死系技能”把免疫和生理特性收窄了，同节食尸鬼句用的是“不死系能力”
```
```
raw verdict: 不死系技能收窄了被动能力，且与同节不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-014-01.md](reports/sol-014-01.md)。译文未修改。
```
</details>

## entry-00553

- 位置：`mod-tome.lua:4090`（tome）｜section：`mod-tome/data/chats/alchemist-hermit.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#*Disaster fails to occur. The halfling finally returns and hands you a small vial of sooty glass.*#WHITE#
ENJOY, AND COME BACK ANY TIME IF YOU'RE INTERESTED IN SIMILAR WORK. I HAVEN'T WON YET. THE LONGER YOU WAIT, THE MORE LIKELY IT IS THAT YOU'LL RETURN TO A SMOKING CRATER AND ONE TRULY IRATE HALFLING.`
- 现译：`#LIGHT_GREEN#*还好，没发生任何不幸的事，那个半身人终于回来了，递给你一个黑乎乎的玻璃瓶。*#WHITE#
喝吧！你要是喜欢这份工作的话随时可以回来找我。我还没赢呢！最好快点，你在这儿待的时间太长，下次迎接你的可就是一个冒着黑烟怒不可遏的半身人了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00064 | HUMAN-REVIEW | cross-batch-014 | confirmed | 恢复两个并列对象，并重译“越晚回来” |  | fix |

<details><summary>hrq-00064 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：冒烟的大坑被并进半身人；“待得太久”把未来风险说成当前停留
```
```
raw verdict: 冒烟的大坑被并进半身人描写→confirmed; The longer you wait 被理解成现场待太久→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-014-01.md](reports/sol-014-01.md)。译文未修改。
```
</details>

## entry-00560

- 位置：`mod-tome.lua:4118`（tome）｜section：`mod-tome/data/chats/alchemist-last-hope.lua`｜source_tag：`_t`
- 原文：`Oh, easy. You get a swig of each brew, of course. They'll put hair on your chest, and possibly your eyelids and fingernails. And, if your aid proves the deciding factor, then I've got a real treat for you: perhaps the last Taint of Purging left in Maj'Eyal.`
- 现译：`很简单，每份药剂我都会让你先喝个痛快的。喝下这些药剂会让你长出有男子汉气概的胸毛，可能还能长你脸上或者指甲盖里。而且，要是你的帮助能起决定性作用的话，我还会额外给你一件真正的宝物：传说中马基·埃亚尔唯一的堕落印记——清除印记哦。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00065 | HUMAN-REVIEW | cross-batch-014 | confirmed | 恢复具体部位和“也许”；物品标准名另行核对 |  | fix |

<details><summary>hrq-00065 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：眼皮被写成脸上；perhaps 被写成传说中的唯一。pending：物品中文名是否还需对齐物品栏
```
```
raw verdict: eyelids 被泛化成脸上→confirmed; perhaps the last 被改成传说中唯一→confirmed; 堕落印记中文名是否为物品栏标准名→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-014-01.md](reports/sol-014-01.md)。译文未修改。
```
</details>

## entry-00570

- 位置：`mod-tome.lua:4681`（tome）｜section：`mod-tome/data/chats/assassin-lord.lua`｜source_tag：`log`
- 原文：`As you depart the assassin lord says: 'And do not forget, I own you now.'`
- 现译：`当你离开时，刺客领主说道：”别忘了，你现在归我所有了。”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00066 | HUMAN-REVIEW | cross-batch-015 | confirmed | 开引号改为 `“` |  | fix |

<details><summary>hrq-00066 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：开引号和闭引号都是右双引号 `”`
```
```
raw verdict: 开引号误用了右双引号→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-015-01.md](reports/sol-015-01.md)。译文未修改。
```
</details>

## entry-00574

- 位置：`mod-tome.lua:5070`（tome）｜section：`mod-tome/data/chats/gates-of-morning-main.lua`｜source_tag：`_t`
- 原文：`The people you saw are likely the volunteers of Zemekkys' early experiments regarding the farportals.
He is a mage who resides here in the Sunwall, eccentric but skilled, who believes that creation of a new farportal to Maj'Eyal is possible.
Aside from a few early attempts with questionable results, he hasn't had much luck. Still, it's gladdening to hear that the volunteers for his experiments live, regardless of their location. We are all still under the same Sun, after all.

Actually... maybe it would benefit you if you meet Zemekkys. He would surely be intrigued by that Orb of Many Ways you possess. He lives in a small house just to the north.`
- 现译：`你看到的那些人很可能是泽梅基斯关于远行传送门实验的志愿者。
他是居住在太阳堡垒的一个法师，脾气古怪但是很有能力，他坚信可以创造一个远行传送门达到马基·埃亚尔。
除了他早期的一些尝试获得了一点可疑的结论外，他并不算走运。不过还是很高兴听到他的实验对象还活着，无论他们身在何方。毕竟我们都生活在同一片阳光下。

事实上……也许去见见泽梅基斯对你有好处。他一定会对你手上的多元水晶球感兴趣。他就住在北边的小屋里。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00067 | HUMAN-REVIEW | cross-batch-015 | confirmed | 选“建造一座通往马基·埃亚尔的新远行传送门”或等义说法 |  | fix |

<details><summary>hrq-00067 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：搭配不成立，但不只是把“达到”改成“到达”
```
```
raw verdict: 创造远行传送门达到马基·埃亚尔搭配不成立→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-015-01.md](reports/sol-015-01.md)。译文未修改。
```
</details>

## entry-00579

- 位置：`mod-tome.lua:5136`（tome）｜section：`mod-tome/data/chats/gates-of-morning-main.lua`｜source_tag：`_t`
- 原文：`Sorcerers? I have never heard of them. There were rumours about a new master of the Pride, but it seems they have two.
Thank you for everything. You must continue your hunt now that you know what to look for.`
- 现译：`法师？我从来没听说过他们。传说部落有了一个新的领袖，看样子现在应该有两个。
感谢你所做的一切。既然你已经知道要找的是什么，就必须继续你的追猎。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00068 | HUMAN-REVIEW | cross-batch-015 | advisory | 先做全局术语决定，再决定是否改这一条 |  | no_change |

<details><summary>hrq-00068 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：成就里有“巫师”，但固定简中本身对 Sorcerers 并不统一，不能单凭这条判“法师”错误
```
```
raw verdict: Sorcerers 译成法师与部分成就的巫师不一致，但简中本身不统一→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-015-01.md](reports/sol-015-01.md)。译文未修改。
```
</details>

## entry-00581

- 位置：`mod-tome.lua:5140`（tome）｜section：`mod-tome/data/chats/gates-of-morning-main.lua`｜source_tag：`_t`
- 原文：`Sorcerers? I have never heard of them. There were rumours about a new master of the Pride, but it seems they have two.
I am afraid with the power they gained today they will be even harder to stop, but we do not have a choice.`
- 现译：`法师？我从来没听说过他们。传说部落有了一个新的领袖，看样子现在应该有两个。
恐怕依他们现在所具有的力量我们更难阻止他们了，不过我们别无选择。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00069 | HUMAN-REVIEW | cross-batch-015 | advisory | 与 00579 一起改，不要只改一个分支 |  | no_change |

<details><summary>hrq-00069 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：与 00579 是同一指称的失败分支
```
```
raw verdict: 失败分支的法师应与 00579 联动，不宜单改→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-015-01.md](reports/sol-015-01.md)。译文未修改。
```
</details>

## entry-00604

- 位置：`mod-tome.lua:5978`（tome）｜section：`mod-tome/data/chats/shertul-fortress-butler.lua`｜source_tag：`_t`
- 原文：`Can you try for a human female appearance please?`
- 现译：`请试着变成人类女性的外形？`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00070 | HUMAN-REVIEW | cross-batch-016 entry-00604… | advisory | 成对润色或成对保留 |  | fix |

<details><summary>hrq-00070 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：两句都是“请……？”，语义和换外观机制都对
```
```
raw verdict: 请与问号并用略显翻译腔→advisory; 男性版本同样的请与问号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00615

- 位置：`mod-tome.lua:6287`（tome）｜section：`mod-tome/data/chats/tannen.lua`｜source_tag：`_t`
- 原文：`One last thing. I will need to hold onto the Orb of Many Ways while you search. I lack the expertise this Chronomancer Zemekkys possesses, and have much learning on the subject to do if I am to follow in his footsteps.`
- 现译：`最后一件事，在你搜寻期间，我得暂时保管多元水晶球并加以研究。我缺少时空法师泽梅基斯所拥有的专业知识，如果我要重复他的工作我必须得花些时间研究这些内容。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00071 | HUMAN-REVIEW | cross-batch-016 | advisory | 若润色，只改后一句即可 |  | no_change |

<details><summary>hrq-00071 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“研究”重复有后文依据，不是无根据增译
```
```
raw verdict: 相邻两句重复研究→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00620

- 位置：`mod-tome.lua:6417`（tome）｜section：`mod-tome/data/chats/tutorial-start.lua`｜source_tag：`_t`
- 原文：`
You have completed all the tutorials, and should now know the basics of ToME4. You are ready to step forward into the world to find glory, treasures and be mercilessly slaughtered by hordes of creatures you thought you could handle!

During this tutorial some creatures were adjusted according to the needs of the lessons. In the unforgiving world of Eyal, monsters are rarely this nice!

If you need a reminder of which key does what, you can access the game menu by pressing #GOLD#Escape#WHITE# and checking the key binds. You can also adjust them to suit your needs.

If this is your first time with the game, you will find the selection of races and classes limited. Don't worry; many, many more will become available as you unlock them during your adventures. 

Now go boldly and remember: #GOLD#have fun!#WHITE#
Press #GOLD#Escape#WHITE#, then select #GOLD#Save and Exit#WHITE#, and create a new character!`
- 现译：`
你已经完成了所有的教程，现在你对ToME4的基本情况应该有所了解了。你现在已经准备好去世界中寻找荣耀和财富，然后被一大群你以为自己能应付的怪物无情地屠杀！

在教学过程中，一些怪物为了教学目的被相应地做过修改，不过在真实的埃亚尔世界中，怪物可不会这么简单！

要是你想看看你的按键设置细节，你可以按下#GOLD#Esc 键#WHITE#进入游戏菜单检查按键绑定，你可以更改设置直到你满意为止。

如果你第一次接触这个游戏，你会发现可供选择的种族和职业很有限。别担心，随着你在冒险中不断解锁，更多种族和职业将可供选择。

现在，勇敢的前进吧，并且记住：#GOLD#玩的开心！#WHITE#
按下 #GOLD#Esc 键#WHITE#，选择 #GOLD#保存并退出#WHITE#，然后创建一个新的角色吧！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00072 | HUMAN-REVIEW | cross-batch-016 | confirmed | 是否列入低风险校正 |  | fix |

<details><summary>hrq-00072 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“玩的开心”“勇敢的前进”是助词误用
```
```
raw verdict: 玩的开心应为玩得开心→confirmed; 勇敢的前进应为勇敢地前进→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00621

- 位置：`mod-tome.lua:6472`（tome）｜section：`mod-tome/data/chats/ukllmswwik.lua`｜source_tag：`_t`
- 原文：`This is a death trap! Goodbye.`
- 现译：`这是个陷阱！再见。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00073 | HUMAN-REVIEW | cross-batch-016 | confirmed | 选用“送命的陷阱”或“死路”一类 |  | fix |

<details><summary>hrq-00073 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“陷阱”削弱了 death trap 的致命意味
```
```
raw verdict: death trap 被简化为陷阱→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00623

- 位置：`mod-tome.lua:6557`（tome）｜section：`mod-tome/data/chats/unremarkable-cave-fillarel.lua`｜source_tag：`_t`
- 原文：`It was my pleasure. But may I ask a favor myself? I am not from these lands. I used a farportal guarded by orcs deep below the Iron Throne and was brought here.`
- 现译：`我的荣幸，不过我有个请求。我其实不是这个大陆的人，使用了钢铁王座地下深处，被兽人保护的远行传送门，然后就到了这里。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00074 | HUMAN-REVIEW | cross-batch-016 | confirmed | 不要按善意保护来改；若改，按“位于……、由兽人把守”整理 |  | fix |

<details><summary>hrq-00074 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：“保护”没有把兽人写成友军。confirmed：定语被逗号切断，读起来像使用了地下深处
```
```
raw verdict: 保护把兽人写成善意友军→refuted; 定语结构不清，逗号切断地点→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00634

- 位置：`mod-tome.lua:6817`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`_t`
- 原文：`stabbed`
- 现译：`被刺杀`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00075 | HUMAN-REVIEW | cross-batch-016 | confirmed | 先核对完整死亡模板或实际渲染，再决定是否改 |  | defer |

<details><summary>hrq-00075 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：stabbed 是物理死亡片段。pending：不能证明最终一定显示“被刺杀而死”。advisory：“被刺杀”比刺伤更强
```
```
raw verdict: stabbed 是物理死亡方式片段→confirmed; 运行时一定显示为被刺杀而死→pending; 被刺杀比 stabbed 更强调蓄意→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。
```
</details>

## entry-00644

- 位置：`mod-tome.lua:6957`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`logSeen`
- 原文：`%s resists the frightening sight!`
- 现译：`%s抵抗了恐惧！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00076 | HUMAN-REVIEW | cross-batch-017 | advisory | 是否补回诱因 |  | no_change |

<details><summary>hrq-00076 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：省掉了“可怕景象”，抵抗成功和恐惧机制是对的
```
```
raw verdict: 恐惧压缩了可怕景象，但不是明确误译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00646

- 位置：`mod-tome.lua:6986`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`damage type`
- 原文：`item manaburn arcane`
- 现译：`物品奥术法力燃烧`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00077 | HUMAN-REVIEW | cross-batch-017 | confirmed | 对照冻结术语记录再决定 |  | defer |

<details><summary>hrq-00077 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：奥术法力燃烧有源码依据。pending：术语库是否要求只写“法力燃烧”
```
```
raw verdict: 奥术法力燃烧有源码依据→confirmed; 违反术语库法力燃烧→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00647

- 位置：`mod-tome.lua:7017`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`logPlayer`
- 原文：`#DARK_ORCHID#Your damage shield cannot be extended any farther and has exploded.`
- 现译：`#DARK_ORCHID#你的伤害护盾不能再被延长，终于破碎了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00078 | HUMAN-REVIEW | cross-batch-017 | confirmed | 文风选择“破碎”或“爆裂” |  | no_change |

<details><summary>hrq-00078 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这里只移除护盾，没有爆炸范围伤害。advisory：“终于破碎了”可以接受
```
```
raw verdict: 护盾只是被移除，没有爆炸范围伤害→confirmed; 终于破碎了代替 exploded 可接受→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00650

- 位置：`mod-tome.lua:7048`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`damage type`
- 原文：`draining physical`
- 现译：`物理汲取`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00079 | HUMAN-REVIEW | cross-batch-017 | confirmed | 核对术语记录后再改 |  | fix |

<details><summary>hrq-00079 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：机制是汲取生命并造成物理伤害。pending：是否必须改成“生命汲取”
```
```
raw verdict: 该伤害汲取生命并造成物理伤害→confirmed; 规范译名必须是生命汲取→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00652

- 位置：`mod-tome.lua:7054`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`damage type`
- 原文：`manaworm arcane`
- 现译：`法力蠕虫奥术`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00080 | HUMAN-REVIEW | cross-batch-017 | confirmed | 选“奥术法力蠕虫”或“法力蠕虫（奥术）” |  | fix |

<details><summary>hrq-00080 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“法力蠕虫奥术”语序不自然
```
```
raw verdict: 法力蠕虫奥术语序不自然→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00653

- 位置：`mod-tome.lua:7071`（tome）｜section：`mod-tome/data/damage_types.lua`｜source_tag：`damage type`
- 原文：`manaburn arcane`
- 现译：`奥术法力燃烧`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00081 | HUMAN-REVIEW | cross-batch-017 | pending | 没有术语裁决前不必因忠实度改 |  | defer |

<details><summary>hrq-00081 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：原文就是 manaburn arcane，“奥术”不是增译。pending：术语库是否要求省略属性
```
```
raw verdict: 奥术是原文没有的增译→refuted; 与术语库法力燃烧不一致→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00657

- 位置：`mod-tome.lua:7159`（tome）｜section：`mod-tome/data/general/encounters/fareast.lua`｜source_tag：`_t`
- 原文：`Entrance to a dark crypt`
- 现译：`通向阴影地宫之路`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00082 | HUMAN-REVIEW | cross-batch-017 | advisory | 若强调地格类型可用“阴影地宫入口” |  | fix |

<details><summary>hrq-00082 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“阴影地宫”指向正确，只是把入口说成了路
```
```
raw verdict: 阴影地宫符合目标区域→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00660

- 位置：`mod-tome.lua:7191`（tome）｜section：`mod-tome/data/general/encounters/maj-eyal.lua`｜source_tag：`_t`
- 原文：`You find an entrance to an old crypt. An aura of terrible evil emanates from this place. You feel threatened just standing there.
You hear the muffled cries of a woman coming from inside.`
- 现译：`你发现了一个古老地宫的入口，里面笼罩着恐怖的邪恶气息，仅仅站在门口你就已经感受到了它的威胁。
你听到了里面传来了陌生女人的哭声。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00083 | HUMAN-REVIEW | cross-batch-017 | confirmed | 去掉“陌生”，并补上低沉或隔墙的听感 |  | fix |

<details><summary>hrq-00083 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏了 muffled，并多加了“陌生”
```
```
raw verdict: 漏译 muffled→confirmed; 无依据增加陌生→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。 Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。
```
</details>

## entry-00683

- 位置：`mod-tome.lua:7393`（tome）｜section：`mod-tome/data/general/events/rat-lich.lua`｜source_tag：`logSeen`
- 原文：`%s raises %s %s, and a red light flashes from it's eye sockets!`
- 现译：`%s 令 %s %s站了起来，一道红光从它眼中闪过！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00084 | HUMAN-REVIEW | cross-batch-018 | confirmed | 选用举起、高举或托起；眼窝可一并改 |  | fix |

<details><summary>hrq-00084 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：raises 是举起头骨，不是让它站起来；眼窝被写成眼中。日志实际在 `rat-lich.lua:73`
```
```
raw verdict: raises 被误译为令头骨站起来→confirmed; eye sockets 译成眼中不够准确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。
```
</details>

## entry-00684

- 位置：`mod-tome.lua:7394`（tome）｜section：`mod-tome/data/general/events/rat-lich.lua`｜source_tag：`logSeen`
- 原文：`From the dust of decay a %s forms!`
- 现译：`从灰烬中诞生了一只%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00085 | HUMAN-REVIEW | cross-batch-018 | confirmed | 保留意译，或改成腐朽的尘埃 |  | fix |

<details><summary>hrq-00085 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：dust of decay 译成灰烬，多了燃烧意象
```
```
raw verdict: dust of decay 译成灰烬带入燃烧意象→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。
```
</details>

## entry-00712

- 位置：`mod-tome.lua:7985`（tome）｜section：`mod-tome/data/general/npcs/aquatic_critter.lua`｜source_tag：`_t`
- 原文：`A huge, elongated sea-green reptile, it looks old and impenetrable.`
- 现译：`一只巨大、细长且泛着海绿色的爬行动物。看上去苍老而结实。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00086 | HUMAN-REVIEW | cross-batch-018 | confirmed | 在坚不可摧和较克制的说法之间选择 |  | fix |

<details><summary>hrq-00086 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：impenetrable 译成结实，弱于难以穿透
```
```
raw verdict: impenetrable 译成结实明显弱化→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。
```
</details>

## entry-00713

- 位置：`mod-tome.lua:8009`（tome）｜section：`mod-tome/data/general/npcs/bear.lua`｜source_tag：`_t`
- 原文：`Do you smell like honey? 'Cause this bear wants honey.`
- 现译：`你闻起来像蜂蜜吗？这只熊喜欢蜂蜜哦～。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00087 | HUMAN-REVIEW | cross-batch-018 | confirmed | 是否恢复“想要蜂蜜”，不要补写原文没有的“吃掉你” |  | fix |

<details><summary>hrq-00087 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：wants honey 被改成喜欢蜂蜜并加了萌化语气。advisory：标点累赘；“会吃掉玩家”不是源码明说
```
```
raw verdict: 哦～。标点累赘→advisory; wants honey 被改成喜欢蜂蜜并加萌化语气→confirmed; 原文明确暗示熊会吃掉玩家→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。
```
</details>

## entry-00719

- 位置：`mod-tome.lua:8096`（tome）｜section：`mod-tome/data/general/npcs/crystal.lua`｜source_tag：`_t`
- 原文：`A formation of red crystal. It emits bright red, scorching light.`
- 现译：`一个由红色水晶构成的生物，它散发着耀眼而灼热的红色光芒。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00088 | HUMAN-REVIEW | cross-batch-018 | confirmed | 描述用水晶簇还是保留生物；更窄的一致性主张先不要当已核实 |  | no_change |

<details><summary>hrq-00088 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：formation 被写成生物。refuted：同批基础描述译的是水晶结构，不是生物。pending：其他颜色晶体是否另有惯例
```
```
raw verdict: formation 译成生物增加了原文没有的性质判断→confirmed; 同 section 已统一译成生物所以无问题→refuted; 其他彩色晶体是否另有一致惯例→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。
```
</details>

## entry-00722

- 位置：`mod-tome.lua:8183`（tome）｜section：`mod-tome/data/general/npcs/ghost.lua`｜source_tag：`_t`
- 原文：`It is an unlife of power almost unequaled. An affront to existence, its very touch abuses and disrupts the flow of life, and its unearthly limbs, of purest black, crumble rock and wither flesh with ease.`
- 现译：`它是一种几乎无可匹敌的非生命力量。它是对存在本身的冒犯，它的触碰本身便会侵害并扰乱生命的流动，它那纯粹的不可思议的黑色肢体能够轻松地使岩石崩解，血肉成灰。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00089 | HUMAN-REVIEW | cross-batch-019 | confirmed | 重写首句保留实体中心；用“非尘世的纯黑肢体”一类语序 |  | fix |

<details><summary>hrq-00089 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：首句把实体写成抽象的“非生命力量”；confirmed：“unearthly limbs, of purest black”修饰关系被译错
```
```
raw verdict: 首句误把实体写成抽象的“非生命力量”→confirmed; unearthly limbs, of purest black 的修饰关系处理错误→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00723

- 位置：`mod-tome.lua:8187`（tome）｜section：`mod-tome/data/general/npcs/ghost.lua`｜source_tag：`_t`
- 原文：`A vengeful, screaming soul given form with the breath of Urh'Rok himself. The vapors of the Fearscape seep from its dimension-bending form, withering and searing.`
- 现译：`乌鲁洛克的吐息中诞生，不断嚎叫的复仇之魂。恶魔空间的气息不断从她次元扭曲的身体中渗出，不断灼烧和腐蚀着周围的一切。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00090 | HUMAN-REVIEW | cross-batch-019 | confirmed | 是否改成“使万物枯萎、灼烧”；重复用词只作顺手润色 |  | fix |

<details><summary>hrq-00090 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：withering 译作“腐蚀”有轻微语义偏移。advisory：增译“周围的一切”属合理显化；“不断”连用三次
```
```
raw verdict: withering 译作“腐蚀”有轻微语义偏移→confirmed; 增译“周围的一切”→advisory; 连续三次使用“不断”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00728

- 位置：`mod-tome.lua:8258`（tome）｜section：`mod-tome/data/general/npcs/horror.lua`｜source_tag：`logSeen`
- 原文：`#LIGHT_RED#A carrion worm mass has spawned from %s' wounds!`
- 现译：`#LIGHT_RED#一团腐肉虫从%s的伤口孵化了出来！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00091 | HUMAN-REVIEW | cross-batch-019 | pending | 查冻结术语记录；确认规范后再接受该 finding |  | fix |

<details><summary>hrq-00091 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：carrion worm mass 是否违反固定术语“腐肉虫群”，允许输入不含术语正文，无法独立确认
```
```
raw verdict: 是否违反固定术语 carrion worm mass → 腐肉虫群→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00730

- 位置：`mod-tome.lua:8265`（tome）｜section：`mod-tome/data/general/npcs/horror.lua`｜source_tag：`logSeen`
- 原文：`#AQUAMARINE#As %s falls all its eyes fall to the ground!`
- 现译：`#AQUAMARINE#当%s倒下时它的眼睛掉落在了地上！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00092 | HUMAN-REVIEW | cross-batch-019 | confirmed | 补“所有/全部”并加逗号，可合并处理 |  | defer |

<details><summary>hrq-00092 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 all，丢掉“全部眼睛一并落地”的机制信息；confirmed：条件分句后缺逗号
```
```
raw verdict: 漏译 all→confirmed; 条件分句后缺少逗号→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00731

- 位置：`mod-tome.lua:8266`（tome）｜section：`mod-tome/data/general/npcs/horror.lua`｜source_tag：`entity name`
- 原文：`eldritch eye`
- 现译：`骇异之眼`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00093 | HUMAN-REVIEW | cross-batch-019 | pending | 核对术语记录的 section、source_tag 与备注 |  | fix |

<details><summary>hrq-00093 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：eldritch eye 是否必须按术语音译“艾尔德里奇之意”，意译“骇异之眼”脱离术语时可成立
```
```
raw verdict: 是否必须按术语规则音译为“艾尔德里奇之眼”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00733

- 位置：`mod-tome.lua:8298`（tome）｜section：`mod-tome/data/general/npcs/horror.lua`｜source_tag：`_t`
- 原文：`You don't want to think about what sort of creature this lamprey-like horror was feeding on to grow so large.  Its skin pulsates and writhes, like things are moving underneath...`
- 现译：`你不想知道这个像七鳃鳗一样的恐魔是吃什么才能长这么大的。它的皮肤不停的扭动，就像有东西在下面移动一样……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00094 | HUMAN-REVIEW | cross-batch-019 | confirmed | 补出“脉动/跳动”，整句重写时改用“地” |  | fix |

<details><summary>hrq-00094 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 pulsates；confirmed：“不停的扭动”助词误用
```
```
raw verdict: 漏译 pulsates→confirmed; 状语助词“不停的扭动”不规范→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00740

- 位置：`mod-tome.lua:8402`（tome）｜section：`mod-tome/data/general/npcs/lich.lua`｜source_tag：`_t`
- 原文：`Having thought to discover life eternal, these beings have allowed undeath to rob them of the joys of life. Now they seek to destroy it as well.`
- 现译：`这些存在本以为能求得永生，却让不死之身夺走了生之乐趣。现在，他们同样在毁灭生者。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00095 | HUMAN-REVIEW | cross-batch-019 | confirmed | 改“企图/试图毁灭”；是否回“生命”属忠实度取舍 |  | fix |

<details><summary>hrq-00095 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：seek to destroy 被译成进行体“在毁灭”；advisory：it 由“生命”具体化为“生者”
```
```
raw verdict: it 由“生命”具体化为“生者”→advisory; seek to destroy 被译成正在发生的“在毁灭”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00746

- 位置：`mod-tome.lua:8418`（tome）｜section：`mod-tome/data/general/npcs/losgoroth.lua`｜source_tag：`_t`
- 原文：`Manaworms are losgoroth which feed on the mana of arcane users. If they ever come in contact with a spellcaster, they latch on and start draining mana away.`
- 现译：`法力蠕虫是以施法者的魔力为食的虚空生物。如果它们近距离接触到法师，它们会缠上去并吸干对方的魔力。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00096 | HUMAN-REVIEW | cross-batch-019 | confirmed | 恢复“洛斯格罗斯”专名；核对 Mana 冻结术语 |  | fix |

<details><summary>hrq-00096 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：losgoroth 被泛化成“虚空生物”，与同批“洛斯格罗斯”不一致；pending：两处 mana 是否违反“法力值”
```
```
raw verdict: 两处 mana 是否违反规定译名“法力值”→pending; losgoroth 被泛化为“虚空生物”，丢失种族专名→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00752

- 位置：`mod-tome.lua:8515`（tome）｜section：`mod-tome/data/general/npcs/naga.lua`｜source_tag：`_t`
- 原文：`Before you stands a tall figure -- a very tall figure, propped high by a thick serpent's tail in place of where his legs should rightly be. His torso is human-like, with bulging muscles beneath fitted armour, and large hands gripping a fiercely sharp trident. He glares at you with dark intensity, like a wolf about to pounce on unsuspecting prey.`
- 现译：`在你面前站着一个高大的人影——一个非常高的人形怪物，在腿部长着巨大的蛇尾巴，他以此来支撑他的身体。他的上半身是人形，护甲下面隐约可见发达的肌肉，两只巨大的双手紧握着锋利的三叉戟。他带着阴沉的锐利目光盯着你，像一头随时准备扑向毫无防备猎物的狼。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00097 | HUMAN-REVIEW | cross-batch-019 | confirmed | 改“巨大的双手”或“两只巨大的手”；重写蛇尾句 |  | fix |

<details><summary>hrq-00097 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“两只巨大的双手”量词重复且身体意象错误；confirmed：蛇尾与腿的关系被译反
```
```
raw verdict: “两只巨大的双手”存在量词重复和错误身体意象→confirmed; 蛇尾与腿的关系译得失真→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。 Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。
```
</details>

## entry-00763

- 位置：`mod-tome.lua:8718`（tome）｜section：`mod-tome/data/general/npcs/shivgoroth.lua`｜source_tag：`_t`
- 原文：`Shivgoroth are mighty ice elementals, torn away from their home world by a powerful magic.`
- 现译：`西弗格罗斯是强大的寒冰元素，它们被一股强大的魔法从老家里赶出来。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00098 | HUMAN-REVIEW | cross-batch-020 | confirmed | 改成“被强行带离/从故乡世界剥离”；机制措辞不要写死 |  | fix |

<details><summary>hrq-00098 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：torn away from 被译成“赶出来”，动作性质从被带离变成被驱逐；confirmed：home world 译“老家”丢了 world 且语域偏口语。pending：断言为“跨位面传送”缺源码依据
```
```
raw verdict: torn away from 被译成“赶出来”造成语义偏移→confirmed; home world 译成“老家”遗漏 world 且语域不合→confirmed; 断言这是“跨位面传送”机制→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-020-01.md](reports/sol-020-01.md)。译文未修改。 共 10 个 claim：6 confirmed、2 pending、1 advisory、1 refuted。Sol 同时撤回了 Gemini 报告里“运行时固定伴随三只”的绝对表述，属证据强度修正，仍由人工决定最终措辞。
```
</details>

## entry-00768

- 位置：`mod-tome.lua:8734`（tome）｜section：`mod-tome/data/general/npcs/skeleton.lua`｜source_tag：`_t`
- 原文：`The forces binding this skeleton together are resilient enough to let it hold a shield and swing a weapon as well as it could have in life.  It's still wearing its old armor, in rusty but servicable condition.`
- 现译：`施展在这只骷髅身上的魔法已经足够强大，足以让它像生前一样持盾挥击。它仍然穿着它原来的那件老盔甲，锈迹斑斑却值得信赖。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00099 | HUMAN-REVIEW | cross-batch-020 | confirmed | 是否收束为“锈迹斑斑，但尚能使用” |  | fix |

<details><summary>hrq-00099 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（轻微）：serviceable condition 译成“值得信赖”，强于“尚堪使用”
```
```
raw verdict: serviceable condition 译成“值得信赖”存在语义漂移→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-020-01.md](reports/sol-020-01.md)。译文未修改。 共 10 个 claim：6 confirmed、2 pending、1 advisory、1 refuted。Sol 同时撤回了 Gemini 报告里“运行时固定伴随三只”的绝对表述，属证据强度修正，仍由人工决定最终措辞。
```
</details>

## entry-00780

- 位置：`mod-tome.lua:8953`（tome）｜section：`mod-tome/data/general/npcs/vampire.lua`｜source_tag：`_t`
- 原文：`It is a humanoid with an aura of power. You notice a sharp set of front teeth.`
- 现译：`这是一个散发着力量气场的类人生物，你注意到它长着一副锋利的门牙。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00100 | HUMAN-REVIEW | cross-batch-020 | advisory | 项目要求统一自由叙事用词时再改 |  | no_change |

<details><summary>hrq-00100 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“类人生物”与同批 entry-00778 的“人形生物”不一致，仅行文问题
```
```
raw verdict: 自由描述“类人生物”与同批“人形生物”不一致→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-020-01.md](reports/sol-020-01.md)。译文未修改。 共 10 个 claim：6 confirmed、2 pending、1 advisory、1 refuted。Sol 同时撤回了 Gemini 报告里“运行时固定伴随三只”的绝对表述，属证据强度修正，仍由人工决定最终措辞。
```
</details>

## entry-00781

- 位置：`mod-tome.lua:8969`（tome）｜section：`mod-tome/data/general/npcs/venom-drake.lua`｜source_tag：`_t`
- 原文：`A corrosive venom drake hatchling; not too powerful by itself, but it usually comes with its brothers and sisters.`
- 现译：`一只腐蚀性的毒龙幼仔。它本身并不强大，但是它们经常集体行动。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00101 | HUMAN-REVIEW | cross-batch-020 | confirmed | 改成“与兄弟姐妹一同出现”，审核证据写“配置会尝试添加三只”，不要写成运行时保证 |  | fix |

<details><summary>hrq-00101 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：brothers and sisters 被概括成“集体行动”，遗漏同胞关系；confirmed：后半句单数改复数；confirmed：make_escort 配置要求三只同名护卫，但“运行时必定三只”这一绝对说法 refuted；pending：是否必为“同窝亲生”无机制依据
```
```
raw verdict: brothers and sisters 被概括成“集体行动”→confirmed; 后半句由单数个体改成复数群体→confirmed; make_escort 配置要求生成三只同名护卫→confirmed; “运行时必定伴随三只”的绝对说法→refuted; 护卫必为“同窝孵化”的亲生兄弟姐妹→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-020-01.md](reports/sol-020-01.md)。译文未修改。 共 10 个 claim：6 confirmed、2 pending、1 advisory、1 refuted。Sol 同时撤回了 Gemini 报告里“运行时固定伴随三只”的绝对表述，属证据强度修正，仍由人工决定最终措辞。
```
</details>

## entry-00804

- 位置：`mod-tome.lua:9191`（tome）｜section：`mod-tome/data/general/objects/boss-artifacts-far-east.lua`｜source_tag：`_t`
- 原文：`The massive stone limb of the Rotting Titan, a mass of stone and rotting flesh. You think you can lift it, but it is very heavy.`
- 现译：`腐化泰坦巨大的石质肢体，一大块石头与腐肉的混合体。你觉得自己举得动它，但它非常沉重。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00102 | HUMAN-REVIEW | cross-batch-021 | pending | 核对 `Rotting Titan` 规范译名后再裁决 |  | fix |

<details><summary>hrq-00102 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：源码确认两处指向同一专名 `Rotting Titan`，但冻结输入未含该 NPC 现行中文译名，无法独立证实“腐化/腐烂”不一致
```
```
raw verdict: “腐化泰坦”与 NPC 现行译名“腐烂泰坦”不一致→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-021-01.md](reports/sol-021-01.md)。译文未修改。 共 7 个 claim：4 confirmed、1 pending、1 advisory、1 refuted。两处 refuted/advisory 是对 Gemini severity 的下修，原样转录，未由主代理改写。
```
</details>

## entry-00805

- 位置：`mod-tome.lua:9194`（tome）｜section：`mod-tome/data/general/objects/boss-artifacts-far-east.lua`｜source_tag：`tformat`
- 原文：`knock away other creatures within radius %d), dealing %0.2f to %0.2f physical damage (based on Strength) to each`
- 现译：`击退半径 %d 的生物，造成 %0.2f 到 %0.2f 物理伤害（基于力量）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00103 | HUMAN-REVIEW | cross-batch-021 | confirmed | 改为“击退半径 %d 范围内的其他生物”，措辞自定 |  | fix |

<details><summary>hrq-00103 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏掉 other；confirmed：`within radius %d` 修饰的是作用范围而非生物，译文改了修饰关系
```
```
raw verdict: 漏掉 other，未表达“其他生物”→confirmed; within radius %d 被译成“半径 %d 的生物”，修饰关系错误→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-021-01.md](reports/sol-021-01.md)。译文未修改。 共 7 个 claim：4 confirmed、1 pending、1 advisory、1 refuted。两处 refuted/advisory 是对 Gemini severity 的下修，原样转录，未由主代理改写。
```
</details>

## entry-00820

- 位置：`mod-tome.lua:9332`（tome）｜section：`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`｜source_tag：`_t`
- 原文：`These blackened boots have lost all vestiges of any former glory they might have had. Now, they are a testament to the corruption of the Deep Bellow, and its power.`
- 现译：`这些被玷污的靴子已经丧失了它们以前的荣耀，现在，它们只能作为深渊咆哮的存在以及腐蚀力量的证明。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00104 | HUMAN-REVIEW | cross-batch-021 | confirmed | 去掉“的存在”，按设定裁定 its power 指代与“发黑/玷污”取舍 |  | fix |

<details><summary>hrq-00104 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：无端增译“的存在”，并把 corruption 与 power 糅合成“腐蚀力量”。advisory：blackened 译“被玷污”偏象征
```
```
raw verdict: 无端加入“深渊咆哮的存在”，并把 corruption 与 power 合并成“腐蚀力量”→confirmed; blackened 译成“被玷污”有误→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-021-01.md](reports/sol-021-01.md)。译文未修改。 共 7 个 claim：4 confirmed、1 pending、1 advisory、1 refuted。两处 refuted/advisory 是对 Gemini severity 的下修，原样转录，未由主代理改写。
```
</details>

## entry-00840

- 位置：`mod-tome.lua:9487`（tome）｜section：`mod-tome/data/general/objects/brotherhood-artifacts.lua`｜source_tag：`_t`
- 原文：`vial of yellow fluid`
- 现译：`黄色液体小瓶`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00105 | HUMAN-REVIEW | cross-batch-021 | confirmed | 若要求系列统一，改为“一瓶黄色液体” |  | fix |

<details><summary>hrq-00105 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：与同系列 9 处“一瓶[颜色]液体”句式不一致。refuted：“严重破坏排比”程度被夸大，应按低影响处理
```
```
raw verdict: 与同系列未鉴定名句式不一致→confirmed; 该差异“严重破坏排比一致性”→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-021-01.md](reports/sol-021-01.md)。译文未修改。 共 7 个 claim：4 confirmed、1 pending、1 advisory、1 refuted。两处 refuted/advisory 是对 Gemini severity 的下修，原样转录，未由主代理改写。
```
</details>

## entry-00843

- 位置：`mod-tome.lua:9495`（tome）｜section：`mod-tome/data/general/objects/brotherhood-artifacts.lua`｜source_tag：`logPlayer`
- 原文：`#00FF00#The elixir has improved your capacity for exercising your core talents.`
- 现译：`#00FF00#药剂提升了你核心技能的能力。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00106 | HUMAN-REVIEW | cross-batch-022 | advisory | 若要顺，可改“运用核心技能的能力” |  | no_change |

<details><summary>hrq-00106 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“提升了你核心技能的能力”修饰关系生硬，未造成机制误解；Gemini 所写源码行号不准，实际在 brotherhood-artifacts.lua:203、263
```
```
raw verdict: capacity for exercising 译成“核心技能的能力”，略去运用/施展含义→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。 共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。
```
</details>

## entry-00852

- 位置：`mod-tome.lua:9627`（tome）｜section：`mod-tome/data/general/objects/egos/ammo.lua`｜source_tag：`logSeen`
- 原文：`%s resists the grasping vines!`
- 现译：`%s抵抗了抓取藤蔓！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00107 | HUMAN-REVIEW | cross-batch-022 | confirmed | 在“抓握藤蔓/缠绕藤蔓”中择一，是否强制与 ego 名统一属风格裁决 |  | fix |

<details><summary>hrq-00107 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“抓取藤蔓”与同 ego“抓握之/抓握”不一致，且可被读成“去抓藤蔓”
```
```
raw verdict: 日志“抓取藤蔓”与同 ego“抓握之/抓握”用词不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。 共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。
```
</details>

## entry-00866

- 位置：`mod-tome.lua:9858`（tome）｜section：`mod-tome/data/general/objects/egos/boots.lua`｜source_tag：`entity keyword`
- 原文：`restorative`
- 现译：`疗愈`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00108 | HUMAN-REVIEW | cross-batch-022 | confirmed | 统一方向由人工定；按治疗机制 Sol 认为“疗愈”更直接 |  | fix |

<details><summary>hrq-00108 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：靴子 ego 名称“振奋的”与关键字“疗愈”两套译法，关键字会显示在已鉴定物品名里
```
```
raw verdict: restorative 名称“振奋的”与关键字“疗愈”两套译法割裂→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。 共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。
```
</details>

## entry-00873

- 位置：`mod-tome.lua:9973`（tome）｜section：`mod-tome/data/general/objects/egos/cloak.lua`｜source_tag：`entity keyword`
- 原文：`restorative`
- 现译：`疗愈`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00109 | HUMAN-REVIEW | cross-batch-022 | confirmed | 与 00866 同批裁决，不要分开改 |  | fix |

<details><summary>hrq-00109 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：披风 ego 同样“振奋的/疗愈”割裂
```
```
raw verdict: 披风 ego 同样“振奋的/疗愈”割裂→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。 共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。
```
</details>

## entry-00881

- 位置：`mod-tome.lua:10051`（tome）｜section：`mod-tome/data/general/objects/egos/gloves.lua`｜source_tag：`entity keyword`
- 原文：`natural`
- 现译：`自然`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00110 | HUMAN-REVIEW | cross-batch-022 | refuted | 无必办事项；除非另立“关键词必须与名称词干统一”规则 |  | refuted |

<details><summary>hrq-00110 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：`naturalist's` 与 `natural` 是两个不同源串，术语快照也映射 `natural → 自然`，不要求中文字面相同
```
```
raw verdict: natural 关键字与 naturalist's 名称译法出入→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。 共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。
```
</details>

## entry-00899

- 位置：`mod-tome.lua:10488`（tome）｜section：`mod-tome/data/general/objects/egos/rings.lua`｜source_tag：`entity name`
- 原文：`conjurer's `
- 现译：`魔术师的`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00111 | HUMAN-REVIEW | cross-batch-023 | confirmed | 若要把 conjurer 词根奇幻化，需连关联条目和术语策略整体处理 |  | no_change |

<details><summary>hrq-00111 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：奥术戒指前缀机制描述准确；confirmed：同批 00900/00918/00919 同词根内部一致。advisory：“魔术师”偏舞台魔术；advisory：一致性不等于最佳译法
```
```
raw verdict: conjurer 前缀机制语境（法术强度/魔力/意志）描述准确→confirmed; “魔术师”易联想舞台魔术，奇幻职业感较弱→advisory; 同批 00900/00918/00919 同词根内部一致→confirmed; 内部一致不能单独证明是最佳译法→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-023-01.md](reports/sol-023-01.md)。译文未修改。三条均无 confirmed 的译文错误。 共 11 个 claim：5 confirmed、4 advisory、1 refuted、1 pending。confirmed 均为源码事实与一致性核验，不是译文错误裁决。
```
</details>

## entry-00914

- 位置：`mod-tome.lua:10798`（tome）｜section：`mod-tome/data/general/objects/egos/totems-powers.lua`｜source_tag：`logPlayer`
- 原文：`Not enough space to summon!`
- 现译：`没有足够的空间召唤！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00112 | HUMAN-REVIEW | cross-batch-023 | confirmed | 除非要跨日志语境统一句末标点，否则本条无需修改 |  | refuted |

<details><summary>hrq-00112 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：调用实际在 totems-powers.lua:132，Gemini 行号不准。refuted：按句号改标点不成立，源码是感叹号。pending：术语快照另有 logSeen 句号版本无法在允许输入内确认
```
```
raw verdict: 实际调用在 totems-powers.lua:132，Gemini 行号不准→confirmed; 中文应改用句号的说法→refuted; 术语快照另有 logSeen 句号版本→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-023-01.md](reports/sol-023-01.md)。译文未修改。三条均无 confirmed 的译文错误。 共 11 个 claim：5 confirmed、4 advisory、1 refuted、1 pending。confirmed 均为源码事实与一致性核验，不是译文错误裁决。
```
</details>

## entry-00918

- 位置：`mod-tome.lua:10816`（tome）｜section：`mod-tome/data/general/objects/egos/wands-powers.lua`｜source_tag：`entity name`
- 原文：` of conjuration`
- 现译：`魔术之`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00113 | HUMAN-REVIEW | cross-batch-023 | confirmed | conjuration/conjure 是否统一奇幻化译名，连同戒指条目一起裁决 |  | no_change |

<details><summary>hrq-00113 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：名称在 wands-powers.lua:91；confirmed：与同词根条目字面一致。advisory：“魔术之”奇幻感弱；advisory：Gemini“既有译法故无问题”论证不足
```
```
raw verdict: 名称实际在 wands-powers.lua:91，Gemini 行号不准→confirmed; 与 00919/00899/00900 同词根译法字面一致→confirmed; “魔术之”略显现代泛化，奇幻感较弱→advisory; Gemini“既有译法故无问题”论证不足→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-023-01.md](reports/sol-023-01.md)。译文未修改。三条均无 confirmed 的译文错误。 共 11 个 claim：5 confirmed、4 advisory、1 refuted、1 pending。confirmed 均为源码事实与一致性核验，不是译文错误裁决。
```
</details>

## entry-00972

- 位置：`mod-tome.lua:11460`（tome）｜section：`mod-tome/data/general/objects/lore/misc.lua`｜source_tag：`entity name`
- 原文：`memories of Artelia Firstborn`
- 现译：`首生者亚特莱的记忆`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00114 | HUMAN-REVIEW | cross-batch-025 | pending | 要不要改成“阿特利亚”类形式，交专名策略决定 |  | no_change |

<details><summary>hrq-00114 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“亚特莱”音节可能不完整，源码无官方读音不能判错。pending：所谓“全仓统一译法”无法在允许输入内验证
```
```
raw verdict: Artelia 译“亚特莱”音节可能不完整，但无官方读音不能判错→advisory; “全仓统一译为亚特莱”的支持理由→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-00980

- 位置：`mod-tome.lua:11596`（tome）｜section：`mod-tome/data/general/objects/quest-artifacts.lua`｜source_tag：`_t`
- 原文：`Carved with runes of power, this staff seems to have been made long ago, yet it bears no signs of tarnish.
Light around it seems to dim and you can feel its tremendous power simply by touching it.`
- 现译：`杖身铭刻着符文，这根法杖似乎是很久以前制造的，虽然它毫无侵蚀的痕迹。
它周围的光线会变的暗淡，当你触摸它时可以感受到惊人的魔力。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00115 | HUMAN-REVIEW | cross-batch-025 | confirmed | 修文法；是否补“力量符文/强力符文” |  | fix |

<details><summary>hrq-00115 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“变的暗淡”应为“变得暗淡”。refuted：并非“其余内容完整准确”，`runes of power` 只译成“符文”漏了 `of power`
```
```
raw verdict: “变的暗淡”应为“变得暗淡”→confirmed; 报告称其余内容完整准确→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-00984

- 位置：`mod-tome.lua:11658`（tome）｜section：`mod-tome/data/general/objects/quest-artifacts.lua`｜source_tag：`_t`
- 原文：`This chest is an extension of old Sher'Tul places of power. Any items dropped inside is transported to an other place, processed and destroyed to extract energy.
The byproduct of this effect is the creation of gold, which is useless to process, so it is sent back to you.

When you possess the chest all items you walk upon will automatically be put inside and transmogrified when you leave the level.
To take an item out, simply go to your inventory to move them out of the chest.
Items in the chest will not encumber you.`
- 现译：`这只宝箱是某处古老的夏·图尔力量之地的延伸，任何扔在里面的物品会被自动传送到那个地方，进行处理并摧毁，从里面提取能量。
这个过程的副产物是黄金，由于再加工它毫无意义，所以它会被送回给你。

当你有这只箱子时，所有你经过地面上的物品会被自动捡起，并且当你离开该层时会自动转化。
如果你想保留物品，只需要从宝箱里把它移到包裹中。
在宝箱中的物品不会增加你的负重。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00116 | HUMAN-REVIEW | cross-batch-025 | confirmed | 若要求逐句对应，改为直述“要取出物品，只需……” |  | fix |

<details><summary>hrq-00116 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：无中生有“如果你想保留物品”的目的条件。pending：是否属有意复用无法证明
```
```
raw verdict: 增加“如果你想保留物品”的目的条件→confirmed; 与前一条宝箱说明属有意复用→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-00992

- 位置：`mod-tome.lua:12145`（tome）｜section：`mod-tome/data/general/objects/special-artifacts.lua`｜source_tag：`_t`
- 原文：`turn into a corrupted losgoroth (poison, disease, cut and confusion immune; converts half damage into life drain; does not require breath) for 10 turns`
- 现译：`转变为一只堕落的洛斯格罗斯（毒素、疾病、撕裂和混乱免疫）十回合，转换一半伤害为生命吸收，不需要呼吸。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00117 | HUMAN-REVIEW | cross-batch-025 | confirmed | 重排括号与持续时间；此处改“流血免疫” |  | fix |

<details><summary>hrq-00117 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：括号提前闭合，把“十回合”插进三组效果之间造成断裂。confirmed：`cut` 应按术语译“流血”，现作“撕裂”
```
```
raw verdict: 括号与十回合持续时间的组织断裂→confirmed; cut 译为“撕裂”不符合实际效果与术语→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-00997

- 位置：`mod-tome.lua:12286`（tome）｜section：`mod-tome/data/general/objects/world-artifacts-far-east.lua`｜source_tag：`_t`
- 原文：`This deep red sword weeps blood continuously. It was born in the labs of the orcish corrupter Hurik, who sought to make a crystal that would house his soul after death. But his plans were disrupted by a band of sun paladins, and though most died purging his keep of dread minions, their leader Raasul fought through to Hurik's lab, sword in hand. There the two did battle, blade against blood magic, till both fell to the floor with weeping wounds. The orc with his last strength crawled towards his fashioned phylactery, hoping to save himself, but Raasul saw his plans and struck the crystal with his light-bathed sword. It shattered, and in the sudden impulse of energies the steel, crystal and blood were fused into one.
Now the broken fragments of Raasul's soul are trapped in this terrible artifact, his mind warped beyond all sanity by decades of imprisonment. Only the taste of blood calls him forth, his soul stealing the lifeblood of others to take on physical form again, that he may thrash and wail against the living.`
- 现译：`这把深红色的剑不断的向下滴血。它诞生于兽人堕落者胡里克的实验室。最初，胡里克试图制造一枚能在死后寄存其灵魂的水晶，但他的计划很快被一群太阳骑士打断，尽管大部分骑士在清剿其要塞中的可怕爪牙时战死，但骑士团团长瑞苏尔却单枪匹马杀入了胡里克的实验室。在那里，两位强者展开了对决，利剑与血魔法你来我往，直到他们都重伤倒地。兽人想拼尽最后一分力气，拿到他的命匣，希望能拯救自己，但是瑞苏尔识破了他的阴谋，挥起沐浴着圣光的利剑击碎了水晶。命匣破碎的瞬间，钢铁、水晶与鲜血融为了一体。
如今，瑞苏尔残破的灵魂被困在这件可怕的造物中，数十年的囚禁早已扭曲了他的心智。只有鲜血的味道能唤醒他，他的灵魂窃取他人的生命之血以重获形体，好向生者咆哮哀嚎。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00118 | HUMAN-REVIEW | cross-batch-025 | confirmed | 修文法即可，无阻断项 |  | fix |

<details><summary>hrq-00118 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“不断的向下滴血”应为“不断地”。confirmed：Gemini 对专名与身份的正面判断成立
```
```
raw verdict: “不断的向下滴血”应为“不断地”→confirmed; Gemini 对主要专名与身份的正面判断成立→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-01000

- 位置：`mod-tome.lua:12326`（tome）｜section：`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua`｜source_tag：`tformat`
- 原文：`cure up to %d diseases or poisons (based on Magic)`
- 现译：`治愈至多%d项疾病和毒素（基于魔法）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00119 | HUMAN-REVIEW | cross-batch-025 | confirmed | 统一“基于魔力”；歧义可选改“疾病或毒素状态中的至多 %d 项” |  | fix |

<details><summary>hrq-00119 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“基于魔法”应为“基于魔力”（源码 combatStatScale("mag")）。advisory：“疾病和毒素”有合计上限歧义
```
```
raw verdict: “基于魔法”未准确表达属性来源→confirmed; “疾病和毒素”范围歧义→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-01001

- 位置：`mod-tome.lua:12335`（tome）｜section：`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua`｜source_tag：`tformat`
- 原文：`unleash a destructive wail, destroying terrain and dealing %0.2f physical damage (based on Magic) in a radius of %d`
- 现译：`释放毁灭哀嚎，摧毁地形，造成 %0.2f 物理伤害（基于魔法）伤害半径 %d`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00120 | HUMAN-REVIEW | cross-batch-025 | confirmed | 补成“……物理伤害（基于魔力），半径为 %d” |  | fix |

<details><summary>hrq-00120 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“（基于魔法）伤害半径 %d”缺标点连跑。confirmed：同样应为“基于魔力”
```
```
raw verdict: “（基于魔法）伤害半径 %d”缺标点连跑语病→confirmed; “基于魔法”属性专名偏差→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-01002

- 位置：`mod-tome.lua:12357`（tome）｜section：`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua`｜source_tag：`_t`
- 原文：`A thick staff with a heavy knob on the end.  It was said to be used by the grand alchemist Bolbum in the Age of Allure.  Much renowned is the fear of his students for their master, and the high rate of cranial injuries amongst them.  Bolbum died with seven daggers in his back and his much-cursed staff went missing after.`
- 现译：`这是一根末端带着沉重瘤状杖头的粗大法杖。据说是炼金师鲍尔本在厄流纪使用的法杖。它之所以闻名于世，大部分来源于鲍尔本的学生们对他的恐惧以及被它打伤脑袋的超高几率。鲍尔本被7把匕首插在后背而死，那根被众人诅咒的法杖也从此消失不见。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00121 | HUMAN-REVIEW | cross-batch-025 | confirmed | 选“大炼金术师/伟大的炼金师”；数字格式按仓库风格 |  | fix |

<details><summary>hrq-00121 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`grand` 漏译。advisory：“炼金师”是叙事称谓不必然违反职业术语。advisory：“7把”数字格式
```
```
raw verdict: grand 漏译→confirmed; “炼金师”是否违反职业术语→advisory; seven daggers 译“7把”数字格式→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。 共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。
```
</details>

## entry-01029

- 位置：`mod-tome.lua:12548`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`logSeen`
- 原文：`#ORCHID#%s resists the tendrils' pull!`
- 现译：`#ORCHID#%s抵抗了触须的抓取！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00122 | HUMAN-REVIEW | cross-batch-026 | confirmed | 改成“抵抗了触须的拉扯/牵引”，措辞自选 |  | fix |

<details><summary>hrq-00122 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：抵抗的是触须的拉扯（pull），不是抓取（grab）；源码 656–662 行先抓住再拉近，译文与前一条日志直接冲突
```
```
raw verdict: 抵抗的是触须的拉扯(pull)而非抓取(grab)，译文与前一条日志冲突→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-025-01.md](reports/sol-025-01.md)。译文未修改。 共 6 个 claim：5 confirmed、1 pending。译文未修改。
```
</details>

## entry-01032

- 位置：`mod-tome.lua:12552`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`Transfers a bleed, poison, or wound to its source or a nearby enemy every 4 turns.`
- 现译：`每4回合将一项流血、毒素或伤口效果转移给效果来源或者附近的敌人。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00123 | HUMAN-REVIEW | cross-batch-026 | confirmed | 主代理按术语库核对该条 category/section/source_tag 后再定是否升级 |  | fix |

<details><summary>hrq-00123 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`wound` 是该物品实际筛选的三个效果子类型之一。pending：“必须译为创伤”的术语条目不在允许输入内，无法确认
```
```
raw verdict: wound 是物品实际筛选的效果子类型之一→confirmed; wound 必须译为“创伤”的术语主张→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-025-01.md](reports/sol-025-01.md)。译文未修改。 共 6 个 claim：5 confirmed、1 pending。译文未修改。
```
</details>

## entry-01038

- 位置：`mod-tome.lua:12614`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`Fashioned by Grand Smith Dakhtun in the Age of Allure, these dwarven-steel gauntlets have been etched with golden arcane runes and are said to grant the wearer unparalleled physical and magical might.`
- 现译：`厄流纪由大师级铁匠达克顿打造而成。那些矮人钢臂铠镂刻着金色的奥术符文，据说它们可以赋予穿戴者强大的魔武力量。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00124 | HUMAN-REVIEW | cross-batch-026 | confirmed | 重写首句恢复主体，另选“无与伦比/举世无双”和近指词 |  | fix |

<details><summary>hrq-00124 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：主语错置，达克顿打造的是臂铠不是“厄流纪”；confirmed：`unparalleled` 被弱化；confirmed：`these` 译成“那些”
```
```
raw verdict: 第一句主语错置、断句错误（达克顿打造的是臂铠不是时代）→confirmed; unparalleled 被弱化为“强大的”→confirmed; these 译成“那些”指代偏差→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-025-01.md](reports/sol-025-01.md)。译文未修改。 共 6 个 claim：5 confirmed、1 pending。译文未修改。
```
</details>

## entry-01068

- 位置：`mod-tome.lua:12825`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`logSeen`
- 原文：`%s's %s lashes out in a flaming arc, intensifying the burning of %s enemies!`
- 现译：`%s的%s划出一条烈焰的弧线，加速了%s个敌人身上的燃烧！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00125 | HUMAN-REVIEW | cross-batch-027 | confirmed | 改句式保留物主关系，或按中文习惯处理该占位符，不能删参破坏参数契约 |  | fix |

<details><summary>hrq-00125 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第三个 `%s` 是物主代词（`who:his_her()`），不是敌人数量，现译“%s个敌人”是运行时可见的占位符语义错误
```
```
raw verdict: 第三个 %s 是物主代词，不是敌人数量→confirmed; 译文是运行时可见的占位符语义错误→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-026-01.md](reports/sol-026-01.md)。译文未修改。 共 8 个 claim：6 confirmed、1 advisory、1 refuted、无 pending。Sol 另注明 Gemini 行号偏移（实际 3251、3642、3778），不影响判断。译文未修改。
```
</details>

## entry-01074

- 位置：`mod-tome.lua:12857`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`@Source@ taps the #SALMON#trapped soul#LAST# of %s, xmanifesting %s!`
- 现译：`@Source@放出了%s#SALMON#被束缚的灵魂#LAST#，模仿了%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00126 | HUMAN-REVIEW | cross-batch-027 | confirmed | 改“调用/汲取/借用……力量”一类不暗示灵魂获释的措辞 |  | fix |

<details><summary>hrq-00126 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：占位符、`@Source@`、`#SALMON#`、`#LAST#` 与参数角色完整。confirmed：“放出……被束缚的灵魂”与机制不符（剑只是调用被拘禁灵魂的力量，不会释放）。advisory：“模仿了%s”对应 `xmanifesting`（源码本身疑似拼写错误）
```
```
raw verdict: 占位符、颜色标记与参数角色完整→confirmed; “放出了……被束缚的灵魂”与机制存在语义偏差→confirmed; “模仿了%s”与表面措辞不完全对应→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-026-01.md](reports/sol-026-01.md)。译文未修改。 共 8 个 claim：6 confirmed、1 advisory、1 refuted、无 pending。Sol 另注明 Gemini 行号偏移（实际 3251、3642、3778），不影响判断。译文未修改。
```
</details>

## entry-01081

- 位置：`mod-tome.lua:12872`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`These once brilliant voratun gauntlets appear heavily decayed. Originally used in the spellhunt, they were often used to destroy arcane artifacts, ridding the world of their influence.`
- 现译：`这件沃瑞钽臂铠看起来十分破旧。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00127 | HUMAN-REVIEW | cross-batch-027 | confirmed | 补“曾经辉煌/昔日璀璨”；`decayed` 改“严重朽坏/严重腐蚀” |  | fix |

<details><summary>hrq-00127 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏 `once brilliant`。confirmed：`decayed` 被泛化为“破旧”，与 3723/3778/3802/3826/3850 的阶段词序列冲突。refuted：问题不是漏 `heavily`，程度已由“十分”承接
```
```
raw verdict: 遗漏 once brilliant→confirmed; decayed 的腐朽语义被泛化为“破旧”→confirmed; 遗漏或显著削弱 heavily 程度的说法→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-026-01.md](reports/sol-026-01.md)。译文未修改。 共 8 个 claim：6 confirmed、1 advisory、1 refuted、无 pending。Sol 另注明 Gemini 行号偏移（实际 3251、3642、3778），不影响判断。译文未修改。
```
</details>

## entry-01085

- 位置：`mod-tome.lua:12879`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`attempt to destroy all magic effects and sustains on creatures in a radius %d cone (unnatural creatures are additionally dealt %0.2f arcane damage and stunned)`
- 现译：`在半径%d码弧形区域尝试驱散生物身上的魔法效果和魔法持续技能（至多两项；非自然生物还会额外受到%0.2f奥术伤害并被震慑）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00128 | HUMAN-REVIEW | cross-batch-028 | confirmed | 统一为“锥形区域/范围”；“至多两项”保留，只调括号结构 |  | fix |

<details><summary>hrq-00128 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`cone` 译“弧形区域”与同批 entry-01097“锥形范围”不一致。confirmed：“至多两项”是译文额外添加、但与源码行为一致。refuted：因此它不构成翻译问题。confirmed：占位符保留正确
```
```
raw verdict: cone 译成“弧形区域”与同批“锥形范围”不一致→confirmed; “至多两项”是译文额外添加的信息→confirmed; 添加“至多两项”构成翻译问题→refuted; 占位符 %d/%0.2f 保留正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-027-01.md](reports/sol-027-01.md)。译文未修改。 共 11 个 claim：8 confirmed、2 advisory、1 refuted、无 pending。Sol 引用的 entry-01091/01097 只是同批术语对照，不是交叉对象，未给分档。
```
</details>

## entry-01096

- 位置：`mod-tome.lua:12927`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`Absorbs all darkness (power %d, based on Willpower and Cunning) within its light radius, increasing its own brightness. (current charge %d).`
- 现译：`在光照范围内吸收所有黑暗(强度 %d，基于意志和灵巧) 并增加亮度(当前增幅：%d)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00129 | HUMAN-REVIEW | cross-batch-028 | confirmed | 括号统一全角；改“当前充能/蓄能”或与 entry-01097“吸收量”统一 |  | fix |

<details><summary>hrq-00129 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两个 `%d` 顺序正确。advisory：半角括号与中文标点混排，且空格规则不一致。confirmed：`charge` 是可积累可消耗的蓄能值，“当前增幅”有机制歧义
```
```
raw verdict: 两个 %d 顺序正确→confirmed; 中英文括号、空格混排→advisory; charge 译为“当前增幅”存在机制歧义→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-027-01.md](reports/sol-027-01.md)。译文未修改。 共 11 个 claim：8 confirmed、2 advisory、1 refuted、无 pending。Sol 引用的 entry-01091/01097 只是同批术语对照，不是交叉对象，未给分档。
```
</details>

## entry-01116

- 位置：`mod-tome.lua:13089`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`This green robe is engraved with icons showing clouds and swirling winds. Its original owner, a powerful mage named Proccala, was often revered for both his great benevolence and his intense power when it proved necessary.`
- 现译：`这件绿色长袍上刻有云朵和旋风的图案。它最初的主人，大法师普偌卡拉，因其善行和力量被人们敬畏。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00130 | HUMAN-REVIEW | cross-batch-028 | confirmed | 补回条件语义，不扩写未明说的背景 |  | fix |

<details><summary>hrq-00130 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `when it proved necessary`。advisory：与 `The Calm` 名称的对照属文学解读，源码未明写
```
```
raw verdict: 漏译 when it proved necessary→confirmed; 该从句与 The Calm 名称的特定对照解读→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-027-01.md](reports/sol-027-01.md)。译文未修改。 共 11 个 claim：8 confirmed、2 advisory、1 refuted、无 pending。Sol 引用的 entry-01091/01097 只是同批术语对照，不是交叉对象，未给分档。
```
</details>

## entry-01120

- 位置：`mod-tome.lua:13125`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`release a burst of light and dark damage (scales with Magic)`
- 现译：`爆发光明和黑暗伤害（受魔法加成）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00131 | HUMAN-REVIEW | cross-batch-028 | confirmed | 改成“爆发出光系和暗影伤害（受魔力加成）”一类表述 |  | fix |

<details><summary>hrq-00131 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：光明/黑暗应按伤害类型术语作“光系/暗影”。confirmed：`Magic` 应译“魔力”
```
```
raw verdict: 光明/黑暗伤害偏离固定伤害类型术语（光系、暗影）→confirmed; Magic 应译“魔力”而非“魔法”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-027-01.md](reports/sol-027-01.md)。译文未修改。 共 11 个 claim：8 confirmed、2 advisory、1 refuted、无 pending。Sol 引用的 entry-01091/01097 只是同批术语对照，不是交叉对象，未给分档。
```
</details>

## entry-01127

- 位置：`mod-tome.lua:13176`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`These titanic double-helical arrows seem to have been designed more for knocking down towers than for use in regular combat. They'll no doubt make short work of most foes.`
- 现译：`巨大的双螺旋箭，似乎是为推倒高塔而非常规战斗设计。毫无疑问，它们会迅速干掉敌人。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00132 | HUMAN-REVIEW | cross-batch-029 | confirmed | 是否补“大多数敌人” |  | fix |

<details><summary>hrq-00132 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）：`most foes` 漏“大多数”
```
```
raw verdict: most foes 漏掉“大多数”范围限定→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01132

- 位置：`mod-tome.lua:13192`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`logSeen`
- 原文：`%s focuses time flows through %s %s!`
- 现译：`%s将时间线集中在%s%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00133 | HUMAN-REVIEW | cross-batch-029 | confirmed | 改“通过……汇聚时间流”一类表达 |  | fix |

<details><summary>hrq-00133 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`time flows` 误作“时间线”，`through` 被改成聚焦位置
```
```
raw verdict: time flows 误作“时间线”，through 媒介关系被改成聚焦位置→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01137

- 位置：`mod-tome.lua:13200`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`This surreal dagger crackles with the intensity of a vicious storm.`
- 现译：`这柄超现实的匕首周围环绕有强大的风暴。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00134 | HUMAN-REVIEW | cross-batch-029 | confirmed | 文风选择 |  | fix |

<details><summary>hrq-00134 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）：丢 `crackles` 动态、弱化 `vicious`
```
```
raw verdict: crackles/vicious 的电气动态意象丢失→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01145

- 位置：`mod-tome.lua:13224`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`logPlayer`
- 原文：`You imbue your %s with %s.`
- 现译：`你在 %s 上安装了 %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00135 | HUMAN-REVIEW | cross-batch-029 | advisory | 系统统一“镶嵌”还是“灌注”，由维护者定 |  | no_change |

<details><summary>hrq-00135 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`imbue` 译“安装”，未体现力量注入
```
```
raw verdict: imbue 译“安装”偏机械，未体现力量注入→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01149

- 位置：`mod-tome.lua:13243`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`Reduces all damage by %d%% of current vim or 50%% of the damage, whichever is lower; but at the cost of vim equal to 5%% of the damage blocked. 
Current Bonus: %d`
- 现译：`降低所有伤害相当于%d%%当前活力值的数值，但不超过伤害值的50%%;降低伤害时，消耗相当于被抵消伤害 5%% 的活力值。
当前加成：%d`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00136 | HUMAN-REVIEW | cross-batch-029 | confirmed | 换全角分号 |  | fix |

<details><summary>hrq-00136 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（纯排版）：`50%%;降低伤害时` 半角分号
```
```
raw verdict: `50%%;降低伤害时` 混入半角分号（纯排版）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01155

- 位置：`mod-tome.lua:13277`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`A cautionary tale tells of the ancient warlock by the name of Caim, who fancied himself daily walks through Goedalath, both to test himself and the harsh demonic wastes. He was careful to never bring anything back with him, lest it provide a beacon for the demons to find him. Unfortunately, over time, his sandals drenched in the soot and ashes of the fearscape and the fire followed his footsteps outside, drawing in the conclusion of his grim fate.`
- 现译：`这是一个警示故事，讲的是有个叫凯姆的古代术士，为了勘查地狱般的恶魔荒原，也为了考验自己，自命不凡的认为可以在恶魔的老巢高达勒斯天天散步。他每次从恶魔位面归来都小心翼翼地不敢带回任何东西，生怕成为恶魔找到他的指引。不幸的是，来回很多次以后，他的草鞋浸满了恶魔空间的烟尘和灰烬。地狱之焰随他的脚步被带到了世间，同时也注定了他悲惨的命运。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00137 | HUMAN-REVIEW | cross-batch-029 | confirmed | 保守直译还是保留叙事性意译 |  | fix |

<details><summary>hrq-00137 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：「自命不凡的认为」的/地错误；“恶魔的老巢/地狱之焰”属增饰
```
```
raw verdict: “自命不凡的认为”语法错误；“恶魔的老巢/地狱之焰”属增饰→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01156

- 位置：`mod-tome.lua:13278`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`Each step you take leaves a burning trail behind you lasting 5 turns that deals %d fire damage (based on Spellpower) to foes who enter it.`
- 现译：`你每踏出一步会在脚下留下一条持续5回合的燃烧痕迹，对所有经过的生物造成 %d 火焰伤害（基于法术强度）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00138 | HUMAN-REVIEW | cross-batch-029 | confirmed | 限定为“进入其中的敌人” |  | fix |

<details><summary>hrq-00138 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`to foes who enter it` 被译“所有经过的生物”，暗示伤害自身与友方
```
```
raw verdict: to foes who enter it 被译成“所有经过的生物”，暗示伤害自身友方→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01160

- 位置：`mod-tome.lua:13294`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`This hat's broad brim protects you from biting colds and sudden storms.`
- 现译：`这顶帽子宽阔的帽檐保护您免受呼啸的寒风和突如其来的暴风雨。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00139 | HUMAN-REVIEW | cross-batch-029 | confirmed | 统一称谓与措辞 |  | fix |

<details><summary>hrq-00139 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）：`biting colds` 意象偏移；“您/你”不统一
```
```
raw verdict: biting colds 译“呼啸的寒风”意象偏移；“您/你”不统一→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01161

- 位置：`mod-tome.lua:13298`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`This torque feels tingly to the touch, but seems to enhance your thinking.`
- 现译：`这项圈摸起来让人觉得刺痛，但似乎增强了你的思考。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00140 | HUMAN-REVIEW | cross-batch-029 | advisory | 是否润色，不按机制错误处理 |  | no_change |

<details><summary>hrq-00140 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`tingly` 译“刺痛”偏重、“增强了你的思考”生硬
```
```
raw verdict: tingly 译“刺痛”偏重、“增强了你的思考”生硬→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01162

- 位置：`mod-tome.lua:13310`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`The blade glows faintly blue, and reflects a sky full of stormy clouds.`
- 现译：`剑身泛着淡淡的蓝色，反射出了满天的乌云。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00141 | HUMAN-REVIEW | cross-batch-029 | confirmed | 改“斧刃” |  | fix |

<details><summary>hrq-00141 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`The blade` 是战斧刃部，译文写成剑身
```
```
raw verdict: The blade 指战斧刃部，译文写成剑身→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01163

- 位置：`mod-tome.lua:13314`（tome）｜section：`mod-tome/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`This mindstar glows with a bright warm light, but seems somehow incomplete.`
- 现译：`这个灵晶散发着温暖的微光，但似乎有点残缺。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00142 | HUMAN-REVIEW | cross-batch-029 | confirmed | 改“明亮而温暖的光芒” |  | fix |

<details><summary>hrq-00142 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`bright warm light` 译“微光”，亮度方向相反
```
```
raw verdict: bright warm light 译成“微光”，亮度方向相反→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。 共 11 个 claim：9 confirmed、2 advisory。译文未修改。
```
</details>

## entry-01183

- 位置：`mod-tome.lua:13524`（tome）｜section：`mod-tome/data/general/traps/teleport.lua`｜source_tag：`logSeen`
- 原文：`%s resists being teleported!`
- 现译：`%s 抵抗传送！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00143 | HUMAN-REVIEW | cross-batch-030 | confirmed | 删多余空格 |  | no_change |

<details><summary>hrq-00143 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`%s` 后半角空格不一致。refuted：Gemini 行号不准
```
```
raw verdict: %s 后半角空格不一致→confirmed; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01193

- 位置：`mod-tome.lua:13635`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`Keep a firm grip on it. These things will dig themselves right back into the ground if you drop them.`
- 现译：`牢牢的抓住它，如果你不小心把它掉在地上，它会立刻挖地逃走。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00144 | HUMAN-REVIEW | cross-batch-030 | confirmed | 改“地”；是否拆回两句 |  | fix |

<details><summary>hrq-00144 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“牢牢的抓住”应为“牢牢地”。advisory：两句合并成逗号句；“挖地逃走”对原文的处理。refuted：行号不准
```
```
raw verdict: “牢牢的抓住”应为“牢牢地抓住”→confirmed; 两句合并为逗号句→advisory; “挖地逃走”对 dig themselves right back into the ground 的处理→advisory; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01194

- 位置：`mod-tome.lua:13641`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`I know, I know. Where does the eel stop and the tail start? It doesn't much matter. The last ten inches or so should do nicely.`
- 现译：`我知道，我知道。你想问电鳗的尾巴是哪一段？没有确切的答案。最后 10 英寸或许是最合适的。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00145 | HUMAN-REVIEW | cross-batch-030 | confirmed | 恢复“那没什么要紧”一类原意 |  | fix |

<details><summary>hrq-00145 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`It doesn't much matter.` 被语义改写成“没有确切的答案”。advisory：Gemini 称对任务指引无实质负面影响存疑。refuted：行号不准
```
```
raw verdict: It doesn’t much matter. 存在语义改写→confirmed; Gemini 称对任务指引无实质负面影响→advisory; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01196

- 位置：`mod-tome.lua:13650`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`Ice Wyrms lose teeth fairly often, so you might get lucky and not have to do battle with one. But dress warm just in case.`
- 现译：`冰龙每隔一段时间会换齿，所以你幸运的话，可以捡到几颗而不需要和它战斗。保险起见穿的暖和点……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00146 | HUMAN-REVIEW | cross-batch-030 | confirmed | 改“得”；标点按原句风格 |  | fix |

<details><summary>hrq-00146 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“穿的”应为“穿得”；句号改省略号。refuted：「冰龙常换牙完全准确」不成立；行号不准
```
```
raw verdict: “穿的暖和点”应为“穿得”→confirmed; 句号改为省略号→confirmed; “冰龙常换牙”完全准确的说法→refuted; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01198

- 位置：`mod-tome.lua:13656`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`Keep this stuff well away from your campfire unless you want me to have to find a new, more alive adventurer.`
- 现译：`把这个瓶子离你的篝火远一些，我可不想明天重新找一个活的冒险家。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00147 | HUMAN-REVIEW | cross-batch-030 | confirmed | 改“把这个瓶子拿远一些”；去“明天” |  | fix |

<details><summary>hrq-00147 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：把字句杂糅；无依据增添“明天”。advisory：`stuff` 译“瓶子”。refuted：行号不准
```
```
raw verdict: 把字句杂糅→confirmed; 无依据增添“明天”→confirmed; stuff 译作“瓶子”→advisory; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01201

- 位置：`mod-tome.lua:13665`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`Yes, sandworms have teeth. They're just very small and well back from where you're ever likely to see them and live.`
- 现译：`是的，沙虫也有牙齿。它们只是很小，藏得很好，如果你把头伸进去找它你就没法活着回来了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00148 | HUMAN-REVIEW | cross-batch-030 | confirmed | 收束到原文信息量 |  | fix |

<details><summary>hrq-00148 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：后半句明显扩写；译文另有轻微表达问题。advisory：Gemini 称生动契合背景。refuted：行号不准
```
```
raw verdict: 后半句进行了明显扩写→confirmed; Gemini 称生动且契合背景→advisory; 译文本身还有轻微表达问题→confirmed; Gemini 所引源码行号→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。 译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。
```
</details>

## entry-01205

- 位置：`mod-tome.lua:13677`（tome）｜section：`mod-tome/data/ingredients.lua`｜source_tag：`_t`
- 原文：`Try to get any knots out before returning. Wear gloves.`
- 现译：`在回来之前把打结在上面的其他蠕虫统统清理掉。戴上手套。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00149 | HUMAN-REVIEW | cross-batch-031 | confirmed | 若要贴近原文用“把缠结解开”，不锁定意象 |  | fix |

<details><summary>hrq-00149 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：译文增补“其他蠕虫”属轻微增译。refuted：与物品描述并不构成矛盾。pending：`knots` 是否只能理解为解开自身的结
```
```
raw verdict: 译文增补了“其他蠕虫”→confirmed; 该译法与物品描述中已分离的单条蠕虫相矛盾→refuted; get any knots out 必然只能理解为解开蠕虫自身的结→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-030-01.md](reports/sol-030-01.md)。译文未修改。共 12 个 claim：8 confirmed、2 refuted、1 pending、1 advisory。 译文未修改。entry-01211 的主疑点被 refuted，原样转录。
```
</details>

## entry-01210

- 位置：`mod-tome.lua:13785`（tome）｜section：`mod-tome/data/lore/age-allure.lua`｜source_tag：`_t`
- 原文：`#{bold}#Hompalan's Log Entry 4#{normal}#
#{italic}#Age of Allure 4544#{normal}#

Just when I was getting somewhere the military decide to barge in and take over. Don't they realise what a serious scientific project this is? All they care about is the little stripes on their helmets. Some tell rumours of humans threatening to attack the facility, but I really care not for such trivial politics. Besides, what threat could those stupid lanklegs really be? I suppose I shall have to persevere though, and try to work around these insane security restrictions.


#{bold}#Hompalan's Log Entry 5#{normal}#
#{italic}#Age of Allure 4545#{normal}#

Well, I suppose this whole war thing wasn't just hot wind after all. Apparently there's lots of people dying outside. What a nuisance - I just want to get on with my work without my supplies being cut off. There is one upside though - human test subjects! We're going to get started on them in the coming months.
I must say I'll be glad to get rid of these disgusting yeeks. They disturb me somehow with their oversized heads. Why we ever decided to use these useless creatures as servants is beyond me... At least the human subjects will be able to talk, lacking though they be in true mental capacity.


#{bold}#Hompalan's Log Entry 6#{normal}#
#{italic}#Age of Allure 4546#{normal}#

Test subject A-C: Imploded during transition.
Test subject D: Exploded during transition.
Test subject E: Half transitioned, half remained. Partial success?
Test subject F: Imploded during transition.
Test subject G: Turned to goo during transition.
Test subject H-K: Imploded during transition.
Test subject L: Frozen during transition.
Test subject M: Survived first transition. Imploded 2 seconds after. Progress!
Test subject N: Survived first transition, but in coma. Died after 4 days.

We're really getting somewhere here... Just a shame humans are such messy creatures! Honestly, how much intestines do they need?! Will start on the next set of subjects early in the new year.
`
- 现译：`#{bold}#红帕兰的日志记录四#{normal}#
#{italic}#厄流纪 4544年#{normal}#

正当我的研究刚有进展时，军方就闯进来接管了一切。他们难道没有意识到这是个严肃的科学项目吗？这些人满脑子想的就是头盔上那几道小杠杠。有传言说人类威胁要进攻这座设施，但我根本不在乎这种琐碎的政治。再说，那些愚蠢的长腿能有什么威胁？看来我还是只能坚持下去，想办法绕开这些荒唐的安保限制。


#{bold}#红帕兰的日志记录五#{normal}#
#{italic}#厄流纪 4545年#{normal}#

好吧……看来这场战争并不只是空话。外面显然死了很多人。真麻烦——我只想继续工作，不要断了我的补给。不过倒有一个好处——人类试验品！接下来几个月就要开始在他们身上测试了。
我必须说，能摆脱这些令人作呕的夺心魔真让我高兴。他们那大得过分的脑袋总让我感到不安。我们当初究竟为什么会决定让这些无用的生物当仆从……至少人类试验品能够说话，尽管他们并不具备真正的思考能力。


#{bold}#红帕兰的日志记录六#{normal}#
#{italic}#厄流纪 4546年#{normal}#

实验品 A-C：在传送过程中向内爆裂。
试验品 D：在传送过程中爆炸。
试验品 E：一半传送走了，一半留在原地。这算部分成功？
试验品 F：在传送过程中向内爆裂。
试验品 G：在传送过程中变成肉酱。
试验品 H-K：在传送过程中向内爆裂。
试验品 L：在传送过程中被冻结。
试验品 M：在第一次传送中存活，2秒后向内爆裂，总算是有点进展了。
试验品 N：在第一次传送中存活，但昏迷不醒，于4天后死亡。

我们的实验真的有进展了……只可惜人类真是肮脏的生物！说真的，他们到底需要多少肠子？！明年初就开始测试下一批试验品。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00150 | HUMAN-REVIEW | cross-batch-031 | confirmed | 首项是否统一为“试验品 A-C”，人工决定 |  | fix |

<details><summary>hrq-00150 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同列表“实验品 A-C”与“试验品 D-N”不一致。confirmed：专名、`#{bold}#` 等标签与语义完整
```
```
raw verdict: 同一测试列表“实验品/试验品”不一致→confirmed; 专名、格式标签与主要语义完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-030-01.md](reports/sol-030-01.md)。译文未修改。共 12 个 claim：8 confirmed、2 refuted、1 pending、1 advisory。 译文未修改。entry-01211 的主疑点被 refuted，原样转录。
```
</details>

## entry-01211

- 位置：`mod-tome.lua:13840`（tome）｜section：`mod-tome/data/lore/age-allure.lua`｜source_tag：`_t`
- 原文：`#{bold}#Hompalan's Log Entry 7#{normal}#
#{italic}#Age of Allure 4547#{normal}#

Test subject O: Imploded during transition.
Test subject P: Survived first transition, but turned mad - had to be put down.
Test subject Q: Survived first transition. Imploded on return transition.
Test subject R: Died during first transition.
Test subject S-T: Imploded on return transition.
Test subject U: Survived return transition. Muttered something about hearing a voice before jumping back into portal - imploded. What a nuisance!
Test subject V: Died on return transition.

Running out of letters soon. Also out of subjects for now. Will have to wait for the soldiers to fetch me more.


#{bold}#Hompalan's Log Entry 8#{normal}#
#{italic}#Age of Allure 4548#{normal}#

Test subject W: Shrunk during first transition, before exploding. (error in calibration?)
Test subject X: Returned from second transition missing head. How bizarre.
Test subject Y: Disappeared during transition.
Test subject Z: Survived both transitions. Remarkable!

Subject Z currently raving, but I believe this is due to stressful conditions, not a direct corrosion of mental faculties from the portal use. Will have to study further.
`
- 现译：`#{bold}#红帕兰的日志记录七#{normal}#
#{italic}#厄流纪 4547年#{normal}#

试验品 O：在传送过程中向内爆裂。
试验品 P：在第一次传送中存活，但疯了，不得不被处死。
试验品 Q：在第一次传送中存活，在传送回来的过程中向内爆裂。
试验品 R：在第一次传送中死亡。
试验品 S-T：在返回传送过程中向内爆裂。
试验品 U：在返回传送中存活。他喃喃说了句似乎听见某个声音的话，便又跳进传送门——随后向内爆裂。真麻烦！
试验品 V：在传送回来的过程中死亡。

试验品编号的字母快用完了，眼下试验品也已耗尽。必须等待士兵们给我提供更多的人类。


#{bold}#红帕兰的日志记录八#{normal}#
#{italic}#厄流纪 4548年#{normal}#

试验品 W：在第一次传送中缩小，随后爆炸。（校准错误？）
试验品 X：在传送回来时头没了，真古怪。
试验品 Y：在传送过程中消失不见。
试验品 Z：在两次传送中都存活了下来。了不起！

试验品 Z 目前仍在胡言乱语，但我相信这是紧张环境所致，而非使用传送门直接侵蚀了他的心智。还需进一步研究。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00151 | HUMAN-REVIEW | cross-batch-031 | confirmed | 不必因 second 改；可选显化“第二次” |  | no_change |

<details><summary>hrq-00151 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：`second` 并未漏译，“传送回来”已表达返程。confirmed：格式与叙事信息完整。advisory：“口吻贴合”属文风评价
```
```
raw verdict: 试验品 X 漏译 second→refuted; 格式排版与叙事信息完整→confirmed; 口吻贴合→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-030-01.md](reports/sol-030-01.md)。译文未修改。共 12 个 claim：8 confirmed、2 refuted、1 pending、1 advisory。 译文未修改。entry-01211 的主疑点被 refuted，原样转录。
```
</details>

## entry-01214

- 位置：`mod-tome.lua:14196`（tome）｜section：`mod-tome/data/lore/angolwen.lua`｜source_tag：`_t`
- 原文：`It were some years now since twain of our brightest students left Angolwen, sullied by our veil of secrecy and our silent duty. It still lies heavy on mine heart to think of what they could accomplish within our private circle. I but hope that one day they whilst return, and they whilst understand the reasons behind our solemn mission.

But I must think of the future, for too many are the regrets of mine long past, and to hold their burdens overlong is to be crushed. I must think of ye, young acolytes, who start now in the learning of our lores. I must explain to ye our mission, our purpose, our justification, so that ye understand all what we do and why. In secrecy we operate, trying to heal the harms of our past, trying to build a better future. For our penance is great, and never should it be forgotten in all Eyal the terrors of the Spellblaze.

I should know well, for I were there. But a young mage was I, though not without promise. I knew of the Shaloren mages' experiments on the Sher'Tul ruins. Aye, and I were jealous of the powers they sought to unlock. No fear or caution had I in my arrogant youth, thinking only of opportunities and glory. Heed well that thought...

Two thousand six hundred cycles of the Sun have passed above my head, and yet still I cannot shake the memory of the day the sky turned to flame and the earth was torn to shreds. I felt the magic in the air, the sudden unleashing of arcane energies beyond anyone's control. I knew in an instant that the Shaloren had unlocked the power of the farportals, but the forces were far beyond their expectations. I saw within seconds the streams of blazing energy tear through the sky above our heads, and then rain down in crimson plumes of destruction. It was all I could to put a shield about myself, and the burns I suffered were terrible, such that scars remain to this day. No one about me survived. Still I remember mine sister Neira's shortened scream as she stood beside me, her skin flayed off by the terrible energies, her body consumed by a pyre of flames, her ashes strewn by a great tumult in the earth. Twenty-six centuries have passed and still I do wake to the sound of that scream...

Many were the loved ones I lost that day, and I were not alone. Countless perished across the lands, and countless more died in the chaos which followed. Then the Spellhunt began, and the people rose against the arrogance of the mages and began slaughtering us mercilessly. After the Spellblaze our abilities were in disarray, our mana channels sundered. We were nigh defenceless, and it took great effort to gather many of us together and found the hidden city of Angolwen. A great many mages were killed in the riots that followed, aye and many innocents too, for distrust was rife and the thirst for blood all-consuming. But alas, the suffering did not end there.

The effects of the Spellblaze can still be seen today, in tortured lands and blighted earths. In the Age of Dusk it were much worse. New diseases arose, plagues swept across all cities, civilisations brought to nothing. All our races came close to extinction, and an age of darkness came upon all learning and enlightenment. Feudal lords and bandit gangs fought amongst what little healthy lands were left, whilst the blights continued to ravage what free people remained. That was when I did begin our secret missions to repair the world, to make right the errors of our actions. In silent operation we visited the broken lands and used our powers to heal, not to destroy. Many centuries it took, but at last the aftereffects of the Spellblaze began to diminish, and the people began to rebuild.

Ah, how much hope was in me then. But foolish were I to think it could be so easy. The wounds of Eyal struck deeper than mere diseases on the surface. The poison went down much further, and the cracks tore through the very roots of our world. One dark and stormy day a great cataclysm swept forth from the east, and the land rose 500 leagues into the sky. We could do naught but gasp in horror as whole cities, whole races were swept into the sea. The continents were sheared apart and all of Eyal forever changed. It was a sight to humble even the greatest archmage.

Aye, and humility is what I teach to ye now. Know ye well that there are forces out there which dwarf ye into insignificance. Know as well that they have no glory, no pride, for they are forces of ultimate destruction which bring only terror and pain.

Our mission is to help the world. Our penance is to act in secret. Old wounds remain and new threats do arise, but all must be dealt with from behind our cloak of silence. The mistrust of our ilk still lies deep in people's minds, and there are even those who hate us with a violent passion. But the world is changing, and perhaps one day we shall be accepted again in society. Until then remember well this lesson of humility, and in the open world keep ye secret, and keep ye safe.`
- 现译：`我们最聪慧的两名学生离开安格利文已有数年，他们厌倦了我们隐秘的帷幕和无声的职责。想到他们若留在我们这秘密的圈子里能有何种成就，我心头依然沉重。我只希望他们终有一日归来，并理解我们为何肩负这项庄严的使命。

但我必须思考未来，我遥远的过去已有太多憾事，长期背负它们只会被压垮。我必须想到你们——这些刚开始学习我们知识的年轻学徒。我必须向你们解释我们的使命、目的与理由，让你们明白我们做的一切以及为何要做。我们在秘密中行动，试图治愈过去造成的伤害，试图建立更美好的未来。我们需要做出巨大赎罪，整个埃亚尔都永不应忘记魔法大爆炸的恐怖。

我对此无比了解，因为那时，身为一个年轻法师我就在现场。我听说了永恒精灵法师在夏·图尔遗迹上的实验。是的，我对他们将发掘出的力量感到无比的嫉妒。年少轻狂的我满脑子都是机遇和荣誉的诱惑，一点也不明白谨慎与小心的重要。看看吧，这样的想法带来了什么样的恶果……

两千六百次太阳轮回已从我头顶流过，可我仍无法摆脱那一天天空化为火海、大地被撕成碎片的记忆。我感受到空气中的魔力，感受到远超任何人控制的奥术能量猛然释放。我瞬间明白，永恒精灵已解开远行传送门的力量，但那股力量远超他们的预期。短短几秒间，我看见燃烧的能量洪流撕裂头顶的天空，继而化作绯红的毁灭烟柱倾泻而下。我只来得及给自己罩上护盾，却仍被严重烧伤，疤痕至今尚存。我身边无人生还。我仍记得姐姐尼拉站在我身旁时那声截然而止的尖叫：可怕的能量剥去她的皮肤，火堆般的烈焰吞没她的身体，她的灰烬被大地的剧烈震动抛散。二十六个世纪过去了，我仍会被那声尖叫惊醒……

那天我失去了许多所爱之人，而且绝不只有我。无数人死于各地，更有无数人死于随后的混乱。之后魔法狩猎开始，民众奋起反抗法师的傲慢，毫不留情地屠杀我们。魔法大爆炸后，我们的能力陷入紊乱，法力通道也被切断。我们几乎毫无防卫能力，历尽艰辛才聚集众多法师，建立隐藏城市安格利文。随后的暴乱中，许多法师被杀，也有许多无辜者死去；当时猜忌遍地，嗜血欲望吞噬了一切。但不幸的是，苦难并未到此结束。

魔法大爆炸的影响今日仍随处可见：土地扭曲，大地枯萎。黄昏纪时，情况还要糟得多。新疾病不断出现，瘟疫席卷各座城市，文明化为乌有。所有种族都接近灭绝，知识与启蒙堕入黑暗时代。封建领主和强盗团伙为剩下的少数健康土地争战，枯萎病却继续蹂躏尚存的自由人民。正是在那时，我开始秘密行动，修复世界，弥补我们行为的过错。我们默默访问破碎的土地，用力量治愈，而非毁灭。这耗费了数个世纪，但魔法大爆炸的后果终于开始减退，人们也开始重建。

啊，那时我心中充满希望。可我竟愚蠢地以为事情会如此简单。埃亚尔的伤口比表面的疾病深得多。毒素深入下方，裂缝撕开了我们世界的根基。一个黑暗的风暴日，一场大灾变从东方席卷而来，大地升至天空五百里格之高。整座城市、整个种族被卷入海中，我们只能惊恐地倒吸凉气。各片大陆被生生切开，整个埃亚尔从此永远改变。那番景象，足以令最伟大的大法师也心生谦卑。

是的，这就是为何我要让你学习身为法师的谦卑。让你了解在绝对的力量下你是多么的渺小。让你了解这力量无关荣耀与自豪，它终极的破坏力只会带来痛苦与恐惧。

我们的使命是帮助世界。我们的赎罪是在秘密中行动。旧伤仍在，新威胁又不断出现，但一切都必须在沉默的斗篷后处理。人们心中对我们同类的不信任依然根深蒂固，甚至有人狂热而暴力地憎恨我们。但世界正在改变，也许终有一日，我们会重新被社会接纳。在此之前，牢记这节谦卑之课；踏入外界时保守秘密，保护好自己。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00152 | HUMAN-REVIEW | cross-batch-031 | confirmed | 改成语；`sullied` 定调；听众统一为“你们” |  | fix |

<details><summary>hrq-00152 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“截然而止”是误字应为“戛然而止”；confirmed：`sullied` 译“厌倦”语义偏移；confirmed：后段复数听众被改成单数“你”；confirmed：专名译法准确
```
```
raw verdict: “截然而止”是误字，应为“戛然而止”→confirmed; sullied 译成“厌倦了”语义偏移→confirmed; 后段把复数听众改成单数“你”→confirmed; 核心世界观专名译法准确一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-030-01.md](reports/sol-030-01.md)。译文未修改。共 12 个 claim：8 confirmed、2 refuted、1 pending、1 advisory。 译文未修改。entry-01211 的主疑点被 refuted，原样转录。
```
</details>

## entry-01215

- 位置：`mod-tome.lua:14230`（tome）｜section：`mod-tome/data/lore/angolwen.lua`｜source_tag：`_t`
- 原文：`#{bold}#"What is Magic?"
#{italic}#A study by Archmage Tazimar Tarelion#{normal}#

How uncouth and common a question it must seem, and yet it is the one I am asked most often, even by some of our most learned students. Too often we teach The Art by practice and imitation and concentration on the end effects, without teaching in greater detail of the underlying principles. Just as a musician may merrily play on his harp without knowing how the sound arises from the vibration of the strings, so a mage may make use of magic without realising the true forces at work. In this document I hope to give learning on the nature of magic, and how the underlying effects give rise to all the wondrous fruits we can produce.

Alchemists will tell you that the world is made up of many base materials - lead, copper, iron, gold and so on. They are fixated on splitting things down into these components and investigating how they react with each other. However there is more to the world than this. Certainly they represent the physical make-up of things, but they do not show the forces and energy that bring everything into motion. The forces of fire, cold, lightning and life itself are all very real effects, and these we call the Elements of Eyal. The true archmage is interested in the interactions of the elemental forces of the world, and manipulating them to his or her need.

The elemental forces exist naturally in the world, and are weaved around all things in an all-encompassing canvas. They move, vibrate and resonate with the materials of the world, and the effects of each play heavily on one another. All creatures naturally make use of these elements, and some are more attuned to these threads than others. With great training and practice we can become more attuned to these wild forces ourselves, and in so doing some can match the speed of wolves, the strength of bears, the tenacity of treants and even the immense natural powers of dragons.

But there is another way of gaining access to these elemental forces - a more direct way, though some would call it unnatural. Long ago people discovered with much training how to concentrate their wills to pluck the elemental threads directly. This can release great energies, and these can be shaped to produce real effects in the world. Plumes of fire, bolts of lightning and blasts of ice can all be called forth by those suitably trained. The true masters of magic can go much further, combining many resonant forces to create complex physical effects.

The tapping of threads can be a draining task, requiring much effort of will to sustain. This is what we versed in the arcane call "mana", that mental stamina dedicated to the interaction with the elements of the world. Continual use of magic is like the constant lifting and holding of heavy weights, and eventually one will find one's capacity drained. Practice allows one to build up greater pools of mana, and certain runes and spells can gradually build extra reserves to be called upon as needed.

Magical runes and items are imbued with an attachment to certain elemental threads. This requires delicate work by experienced and gifted enchanters. The most intricate of magical artifacts demand many years of work, using intense mental effort to permanently attune the core materials to the right elemental energies. Gemstones are especially easy to work with in this craft, and alchemists use them often to bring about elemental effects.

Some believe that magic is inherently wrong, that the so-called twisting of the elements with one's will can only lead to terrible things. As students of Angolwen I assume you disagree! Magic is simply an extension of the forces of nature, and are we not natural creatures that use it? But remember that magic is still a powerful force that can be used for good or ill. Magic is indeed a tool of immense value - use it wisely.
`
- 现译：`#{bold}#“魔法究竟是什么？”
#{italic}#大法师塔兹玛·泰尔兰的研究报告#{normal}#

这问题听起来多么粗俗平常，可它偏偏是我最常被问到的问题，甚至一些学识最渊博的学生也会询问。我们太常借实践、模仿和对最终效果的专注来教授魔法技艺，却不更详细地教授底层原理。正如音乐家可以快乐地弹奏竖琴，却不知声音如何由琴弦震动产生，法师也可以运用魔法，却不了解其中真正起作用的力量。我希望在这篇文章中教授魔法的本质，以及底层效应如何结出我们所能创造的一切奇妙果实。

炼金师会告诉你这世界是由许多基本材料构成——铅、铜、铁、金等等。他们专注于将物品分解成基本元素来分析他们是如何互相影响的。但这只是世界的一面，基本元素虽然表现了物质面上世界的构成，却不能解释推动万物运动的力量与能量。火之力、冰之力、闪电之力、乃至生命之力都是真实存在的，而这些力量我们称之为埃亚尔元素。真正的大法师专注于元素之力是如何影响这个世界的，并善于操作这股力量为己所用。

元素之力天然存在于世界，编织在万物周围，构成一幅无所不包的织布。它们与世界中的物质一同移动、震动与共鸣，彼此的效应互相深刻影响。所有生物都会自然地运用这些元素，但有些生物比其他生物更贴合这些丝线。通过大量训练与实践，我们自己也能更贴合这些狂野力量；如此一来，有些人就能匹敌狼的速度、熊的力量、树人的坚韧，甚至巨龙的浩大自然之力。

但还有另一种获得元素之力的方式——一种更直接、虽然有人会称之为不自然的方式。很久以前，人们发现，经过大量训练后，可以集中意志，直接拨动元素丝线。这能释放巨大能量，而这些能量又可被塑造成世界中真实存在的效果。受过适当训练的人可召出火焰烟柱、闪电之箭与寒冰爆流。真正的魔法大师还能走得更远，将多种共鸣力量结合起来，创造复杂的物质效果。

拨动丝线会消耗巨大，需要投入大量意志来维持。我们精通奥术之人将这种专门用于与世界元素互动的精神耐力称为“法力”。持续使用魔法就像不断举起并托住重物，最终会发现自己的能力已被耗尽。练习能让人积累更庞大的法力储备，某些符文与法术也能逐渐积累额外储备，以供需要时调用。

魔法符文和物品都被灌注了与某些元素丝线的联系。这需要经验丰富、天赋过人的附魔师进行精巧作业。最精密的魔法神器需要多年制作，以强大精神力将核心材料永久调谐到正确的元素能量。宝石尤其容易用于这种技艺，炼金师常用它们引发元素效应。

一些人笃信法术的存在本身就是个错误，所谓的凭某人意志扭曲元素之力只能带来可怕的后果。作为安格利文里的学生我假定你们都是不同意这种说法的。魔法只是自然之力的延伸，我们身为自然生物为何不能去尝试运用它？但你们要谨记魔法的存在仍是一柄双刃剑。作为工具它确实能产生极大的价值——明智的使用它。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00153 | HUMAN-REVIEW | cross-batch-032 | confirmed | 改“基本成分/物质组分”“它们”“明智地”；补逗号；一致性另取冻结样本再确认 |  | fix |

<details><summary>hrq-00153 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`base materials/components` 译“基本元素”，混淆物质组分与“埃亚尔元素”，且把无生命组分称作“他们”。confirmed：“明智的使用它”助词误用。confirmed：状语与主句粘连缺停顿。advisory：“双刃剑”替换了“可用于善或恶”。pending：控制码完整、译名同 section 一致的主张证据不足
```
```
raw verdict: base materials/components 译“基本元素”，混淆物质组分与“埃亚尔元素”，并把无生命组分称作“他们”→confirmed; “可用于善行亦可用于恶行”意译成“一柄双刃剑”→advisory; “明智的使用它”的“的”误用→confirmed; “作为安格利文里的学生我假定……”缺少停顿→confirmed; 控制码完整、人名地名与同 section 一致→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-031-01.md](reports/sol-031-01.md)。译文未修改。共 12 个 claim：8 confirmed、3 advisory、1 pending、无 refuted。 译文未修改。一条译名一致性主张因冻结输入不含术语正文保持 pending。
```
</details>

## entry-01216

- 位置：`mod-tome.lua:14450`（tome）｜section：`mod-tome/data/lore/daikara.lua`｜source_tag：`_t`
- 原文：`#{bold}#Relle, Cornac Fighter and Expedition Leader#{normal}#
It knows we're here.  Xann's gone, and I have to assume the worst.  Too late to run.  One option left, a contraption Sodelost ensured us he'd be able to use to get the kill...  shame he didn't leave instructions behind with it, it's unclear how to arm it, and I don't want to add "being charred to a crisp" to my list of troubles today.
I might not know a great deal about artifice, but I know how wild animals work, and for all the praise they get, dragons are no better.  I don't need to know how to rig this device so it goes off when the beast steps on it - I just need to put it inside something it'll eat whole...
#{italic}#Judging from this note's intact state and delicate placement next to a sack covered in assorted animal viscera, the dragon not only avoided setting off the trap, but has kept it as a trophy.  Inside the sack is a disarmed trap featuring a few recognizable alchemical flasks, and a means of mixing them in the right proportion when a pressure plate is triggered to produce a blast of dragonsfire. Figuring out how to arm it is almost as easy as figuring out how to make more traps like it.#{normal}#`
- 现译：`#{bold}#探险队队长，科纳克人战士瑞丽#{normal}#
那条龙知道我们在这里。希安失踪了，我只能作最坏的打算。逃跑已经太迟。只剩一个选择：苏达罗斯特向我们保证，他能用这套装置杀死那条龙……可惜他没把说明留在装置旁边，没人知道该如何启动它，而我可不想让今天的麻烦清单再多出”被烧成焦炭”这一项。
我或许不太懂机关术，却知道野兽会怎么做。龙尽管备受赞颂，在这一点上也不比其他野兽高明。我无需知道怎样把装置设成野兽踩中时触发——只须将它放进某种会被一口吞下的东西里……
#{italic}#从纸条完好无损的状态，以及它被小心摆放在一个沾满各种动物内脏的袋子旁边来看，那条龙不仅没有触发陷阱，还把它当作战利品收藏了起来。袋中有一个已解除的陷阱，装有几只尚能辨认的炼金药瓶；压力板触发时，机关会按正确比例混合其中的药剂，爆发出龙火。弄清如何启动它，几乎与弄清如何制作更多同类陷阱一样简单。#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00154 | HUMAN-REVIEW | cross-batch-032 | confirmed | 首字符换左双引号 |  | fix |

<details><summary>hrq-00154 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`”被烧成焦炭”` 开引号方向错误。confirmed：该 Lore 解锁龙火陷阱，叙事与机制相符
```
```
raw verdict: “被烧成焦炭”开引号方向错误（U+201D）→confirmed; 该 Lore 解锁龙火陷阱，叙事与机制相符→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-031-01.md](reports/sol-031-01.md)。译文未修改。共 12 个 claim：8 confirmed、3 advisory、1 pending、无 refuted。 译文未修改。一条译名一致性主张因冻结输入不含术语正文保持 pending。
```
</details>

## entry-01218

- 位置：`mod-tome.lua:14722`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Two: A Night to Remember#{normal}#

It was three nights later I awoke in darkness from a troubled dream to find my window open, the silk drapes billowing in the breeze.  As my eyes adjusted to the light I saw Linaniil stood at the foot of my bed, a thin azure dress clinging to her skin in the chill night air.  Around her was a cashmere belt inset with opals and woven with pale runes, and gold jewellery adorned her neck and wrists.  A long staff rested lightly in her hands, rubies glistening in its decorated top.  Her red hair stirred in the wind as she gazed at me.
 
“What are you doing here?” I enquired.  I did not bother asking how she managed to sneak into my bedchamber, past many guards.  I knew that no less than a council member would be able to divine her presence when she put her mind to illusion.
 
She looked at me slowly for a moment, before turning her eyes to the rest of the room, analysing my personal space in detail.  “There be a band of orcs marauding in the north,” she said in a distracted tone.  She picked an ornamental dagger from a shelf and looked it over as she spoke.  “They look like to cause trouble for some outlying elven settlements.”
 
“I will summon a raiding party at once,” I said, rising quickly from my bed, unheeding of modesty.
 
“Oh, how boring!” she complained, putting the dagger down and spinning to face me.  “What of the promise ye made to hunt orc together?”
 
“What, just the two of us?”
 
“Aye,” she said, looking my unclad form up and down with a slow gaze, seeming to take delight in the sight.  “Or are ye not man enough?”
 
“A strange question to ask of an elf, my lady.  But I can take this band of orcs myself, I am sure.  If you wish to tag along then I cannot promise to keep you safe.”
 
She laughed then, and the sound was like ringing crystal.  “Very well then!  Get ye your steel stick and we shall see who holds their own best.”  I agreed with a smile, and went to my armoury and shoved on metal greaves and a chain hauberk, my breastplate and steel gauntlets.  Linaniil tutted in surly impatience.  “Must ye wear that tin suit?”
 
“It is my battle gear,” said I, pulling on my visored helm and wrapping a thick cloak round my shoulders.
 
“Ye look like a golem,” she muttered, visibly annoyed.  “Come then, I grow bored.”  She leapt out the window, taking to the air with grace, flying away into the night.
 
I took then my greatsword from its hanging.  It was a simple looking blade, adorned only with a heavy moonstone on its pommel.  But its looks belied its power, for it was forged by the dwarves in their early years, before vanity overcame their works and their weapons became more for show than for battle.  It had an edge that clove through steel and bone with ease, without ever dulling the blade.  Mooncutter it is called, though it is lost to me now.  I gave it a swing through the air before leaping out the window myself, conjuring a cushion of air beneath me and following swiftly after Linaniil.
 
With rapid pace we flew through the scattered clouds in silence for twenty minutes before Linaniil began to descend.  I could see nestled between some low hills were the flames of campfires, and as we came closer the sound of orcish chanting became clear.  “How shall we approach them?” I called out, wondering what tactics the sorceress would want to employ.
 
“Directly,” she said, and with that she made a sudden burst of speed, coming right above the orcish camp and descending in their midst.  With a curse I sped after her, landing by her side and drawing Mooncutter as the orcs rose in fury and alarm, grabbing up their weapons.  As a ring of dark swords and spears and halberds gathered round us Linaniil turned to me with a wild smile.  “Time to dance.”
 
She shot forth a ray of purple arcane energy from her right hand, whilst her left held up her staff, its tip blazing like a torch.  Flames leapt up in tandem from my own blade as I rose it high, and swept it before me in a wide arc, cutting down the nearest brute and sending a shocking wave of fire into the troops behind it.  I pressed forward, forcing back the orcs before me with a roaring hot wind.  Their weapons dropped from their hands as they reached up to cover their faces, and with a grin of satisfaction I rushed to hew their heads off.  But as I swung my blade I was knocked to the ground from behind by a blast of fire, and turning about I saw Linaniil standing in a pillar of flame, her arms outstretched as it expanded around her.  “Too hot for ye, Aranion?” she called out as the orcs nearby were fried to a crisp, their flesh withering into black dust.
 
I grunted, and turned my blade into ice, and with deft sword strokes sent streams of freezing cold into the orcs around her, so that they shattered like glass before the fire ever hit them.  Linaniil cursed my name as she dropped the flames from about her.  “Don’t ruin my fun!” she exclaimed, before teleporting to the other side of the camp and beginning to blast the orcs there.

I laughed and turned on the beasts nearest me, and brought tumults to the earth with each swing, so that they lost their footing and fell to the ground before my sword found their throats.  Then I conjured a mighty spark of lightning, spearing it through their densest ranks, and I rushed along its glowing length hewing down the monsters before they could react.  I laughed again with the fey heat of battle, and I discarded my helm and tore off my platemail, taking joy from moving about the field with ease and slaughtering my inferior foes.  Mooncutter danced through their flesh, and their dark blood gushed and fountained with joyful rhythm.

On the far side of the camp explosions and screams marked Linaniil’s passage, and I saw burning limbs flying into the air and streaks of fire tearing through the night.  The sorceress was wreathed in flames, her eyes shining, and the dancing blaze about her made her look like a nymph of fire incarnate.  No more beautiful and awe-inspiring a sight had I ever beheld.

Seeing their numbers quickly dwindling the orcs began to flee, but I phased to block their retreat and called forth a wave of water, forcing them back against Linaniil’s flames.  There against the wall of fire I dashed them, and great numbers of them fell like leaves scattered in the wind.  Blood spilled thick and plentiful, and with but a few more thrusts of Mooncutter and blasts from Linaniil’s hands the battle was over.  Not a single orc still moved, and well over four hundred lay dead on the ground.
 
Linaniil and I stood facing each other, panting with sudden exhaustion as the adrenaline of the fight left us.  “I lost count,” I said between breaths, “of who slew more…”  She grinned coyly at me, sweat trickling down her face.  Minor cuts and burns left her robe in tatters, with one shoulder strap hanging loose.  Her glistening chest heaved up and down with each breath, and her deep eyes looked at me with naked intensity.
 
She strode forward then, and grabbing me roughly by my hauberk she pulled my lips to hers.  The kiss was hot and fierce, and as she bit my lower lip the course of blood in battle came back to me afresh.  I kissed her again and grabbed her body, pulling her tight to me, our lips locked.  She tore lustfully at my remaining armour, flinging it to the ground, and I slid off her silken clothes, till we were left bare beneath the stars.  Then against a rocky outcrop we pressed against each other, still gasping and sweating from the fight.  There with blazing passion flesh met flesh and our hot moans rose into the cold night sky.`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆 #{normal}#

#{bold}#第二章：难忘之夜#{normal}#

三天后的午夜，我在一场噩梦中惊醒。眼前窗户大开，晦暗的光线中丝织的帘幕在晚风中舞动。随着我的眼睛渐渐适应了夜晚微弱的亮光，我看见莱娜尼尔就站在我的床尾，一袭轻薄的蔚蓝长裙在寒夜的空气里紧贴着她的肌肤。她的腰间环绕着镶嵌着蛋白石和苍色符文的羊绒腰带，颈上腕间环绕着闪耀的金制首饰，一根长杖轻轻搁在她的手中，杖首的装饰上嵌着数颗红宝石，熠熠生辉。清风吹拂，她澄澈的眸子中映出我的影子，红色的长发迎风飘荡。

“你在做什么呢？”，我轻轻问道。我并没有打算询问她到底是如何绕过那些卫兵悄悄潜入我的卧房的。我知道，至少得是议会成员，才能在她专心施展幻象时察觉她的存在。

她明媚的目光轻柔地凝视着我，接着在屋子的四周扫过，仔细分析着房间里的每一个部分。“有一队兽人正在北方四处劫掠，”她稍有些心不在焉地说道，手中漫不经心地把玩着我在架子上放着的一把装饰用匕首，“他们看起来会给一些外围的精灵聚落惹上麻烦。”

“我立刻就召集突击队迎敌。”，我不顾礼仪地从床上坐起。

“唔，那样多无聊啊”，嘟哝着的她将匕首轻轻放下，回身面向着我，“那你许下的、要一起去猎兽人的承诺呢？”

“……什么？就只有我们两个人去吗？”

“是啊”，她的目光在我赤裸的身体上缓缓游移，上下打量，似乎对眼前的景色颇为享受，”还是说你不够男人？”

“对于精灵族来说这还真是个怪问题，我的女士。不过，我可以在此保证，只需要我一个人也可以亲手干掉那些兽人。如果你真的想要一同前行的话，我可能没法确保您的安全。”

她的笑声如同水晶泠泠碰撞般清脆。“那真是太好了！来，拿上你的金属棍子，让我们来看看谁更能撑得住。”我微笑着点头，走进武器库，匆匆套上金属护胫、锁子甲、胸甲和钢制护手。莱娜尼尔不耐烦地咂舌道，“你非得穿上这堆废铜烂铁不可吗？”

“这是我的战斗服”，我戴上头盔，披上斗篷。

“唔，看起来简直就像一只傀儡，”她小声咕哝着，”快来吧，我有点无聊了。”紧接着，她轻巧地越过窗台，优雅地随风而去，在夜空中划出一道弧线。

随后我从剑架上取下我的双手巨剑。乍一眼看上去，这似乎只是一把普通的剑刃，唯一的装饰是剑柄上一颗硕大的月亮石。这把剑由矮人于多年之前所铸，其貌不扬却强韧无比。之后，他们的虚荣和浮华替代了匠人的坚毅，让装备成为了用于炫耀的道具而不是用于战斗的兵器。这把剑的剑锋可以轻易穿透钢铁和骨头，且永不卷刃。它的名字叫做斩月剑，尽管现在已经随着岁月的流逝而不知所踪。我凌空挥动爱剑，随即跃出窗外，在身下唤出气流软垫，迅速追随莱娜尼尔而去。

我们在零散的云层间疾飞，沉默了二十分钟，莱娜尼尔才开始下降。低矮群山之间点缀着营地的篝火；随着我们飞近，兽人的吟唱声渐渐清晰。“我们该怎么接近他们？”我高声问道，想知道这位女魔法师准备采取什么战术。

“直冲进去。”话音刚落，她骤然加速，飞到兽人营地正上方，落在他们中间。我咒骂一声，急忙追上，在她身旁落地并拔出斩月剑；兽人惊怒地起身，纷纷抓起武器。当一圈黑沉沉的刀剑、长矛和戟将我们团团围住时，莱娜尼尔转向我，露出狂野的笑容。

“舞会开始了”

一道紫色的奥术能量从她的右手指尖射出，而她左手高举法杖，杖端如同火炬般被炽焰所缠绕。随着剑刃高举，一团团火焰从我的剑刃上腾跃而起，在我面前呈弧形喷发出来，迅速击倒了最前排的兽人，爆裂的冲击波向他身后的部队席卷而去。我紧逼而前，以咆哮的炽热之风迫退身前的兽人。他们的武器纷纷脱手落地，只能抬手遮挡脸面；我怀着满意的微笑冲上前去，正要斩下他们的头颅。可就在挥剑之际，一团火焰自背后将我击倒。转身望去，只见莱娜尼尔站在熊熊烈火之中，双臂向前伸展，烈焰应之而动。“对你来说是不是有些太热了呢，艾伦尼恩先生？”。在她的谈笑之间，周围的兽人纷纷被烈焰吞噬，转瞬便灰飞烟灭。

我闷哼一声，将剑刃化为坚冰，以精妙的剑技向她周围的兽人劈出道道凛冽寒流，在火焰触及之前便将他们冻成冰雕，碎裂如玻璃。莱娜尼尔咒骂着我的名字，撤去了周身的火焰。”别抢了我的乐子！”她大喊道，随即传送到兽人营地的另一侧，在那里掀起新一轮烈焰。

我大笑着扑向最近的野兽，每一挥都让大地剧震，兽人在震波中失去平衡纷纷倒下，任凭我的利剑穿透他们的喉咙。紧接着，狂暴的闪电在剑锋聚集，如同投枪一般射出，贯穿兽人们最密集的军列；我沿着它发光的轨迹冲锋，在他们还没来得及反应之前挥剑将这些怪物一一劈倒。我在战斗的狂热中再次大笑，丢掉头盔撕下板甲，享受卸甲后在战场上轻快移动、屠戮这些弱小之敌的快乐。斩月剑在他们的血肉间穿梭舞动，他们的黑血喷涌如泉，节奏欢畅。

远处营地爆炸的烟雾和兽人的惨叫声点缀着莱娜尼尔的足迹；我看见燃烧的断肢飞上半空，道道火光撕裂夜色。烈焰缠绕着女魔法师的周身，她的眸子熠熠生辉，四周跃动的火光让她宛如火灵的仙女下凡一般。此情此景，真是我一生所见最为美好最为震撼的那一刻。

剩余的兽人眼看人数锐减，开始逃跑；但我相位移动到他们前方，截断退路，又召来一股洪水，逼他们退回莱娜尼尔的烈焰之中。火墙之前，我将他们击溃，大批兽人如风中落叶般倒下。鲜血大股涌出；斩月剑又刺出几下，莱娜尼尔又轰出几道法术，战斗便结束了。没有一个兽人还能动弹，地上倒着远超四百具尸体。

面对面地，我和莱娜尼尔的身躯矗立在硝烟弥漫的战场上，随着战斗的肾上腺素退去，突如其来的疲惫令两个人气喘吁吁，呼出的气息在空气中凝成雾气。我气喘吁吁地说道，”我已经记不清了，到底是谁杀的更多…”。她害羞地微笑着，汗水从泛红的面颊滴落。战斗中的刀伤和灼烧让她的长袍残破不堪，一侧肩带松松垂落。她泛着光泽的胸膛剧烈起伏，深邃的双眼以赤裸的炽烈目光看着我。

她大步走来，粗暴地揪住我的锁子甲，把我的双唇拉向她。这一吻火热而激烈；她咬住我的下唇，战斗中奔涌的热血顿时再度沸腾。我又吻住她，一把搂住她的身体，将她紧紧拉向自己，双唇始终交缠。她欲火中烧地撕扯我剩下的护甲，将其甩在地上；我也褪下她的丝绸衣裳，直到我们赤裸着站在群星之下。我们靠在一处岩壁上，紧贴着彼此，仍因刚才的战斗喘息流汗。炽烈的激情中，肌肤交融，我们火热的呻吟升入寒冷的夜空。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00155 | HUMAN-REVIEW | cross-batch-032 | confirmed | 四处引号、标点结构统一重排；是否并段、去“先生”属编辑风格 |  | fix |

<details><summary>hrq-00155 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：四处对话以右双引号开引；确认问号句号与引号外标点重复；确认“舞会开始了”另拆段且缺句末标点。advisory：“魔法剑士技能组合”是联想不是机制证据；advisory：`Aranion` 添译“先生”拉远语气
```
```
raw verdict: 四处对话以右双引号作为开引号→confirmed; 问号、句号与引号外标点重复→confirmed; “舞会开始了”另拆成段且缺句末标点→confirmed; 叙事体现“魔法剑士技能组合”、背景“完全契合”→advisory; Aranion 添译“艾伦尼恩先生”语气生硬→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-031-01.md](reports/sol-031-01.md)。译文未修改。共 12 个 claim：8 confirmed、3 advisory、1 pending、无 refuted。 译文未修改。一条译名一致性主张因冻结输入不含术语正文保持 pending。
```
</details>

## entry-01220

- 位置：`mod-tome.lua:14814`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Three: The Farportal#{normal}#

“Why are ye not leader?” asked Linaniil, resting her head in her hand with her naked form strewn across my bed.
 
I looked at her, surprised by the sudden question.  My mind struggled briefly with the strange query, still recovering from the heat of sex but a minute before.  “Why should I be leader?” I asked back.
 
“Because ye are strong, of course,” she responded.  “I deem ye stronger in battle than any of your kin.  Ye should rule with such strength.”
 
I chuckled softly.  “Mere strength is not enough to rule a people.  It requires responsibilities, careful decision making, and above all – politics.  I have no interest in such matters.  Ephinias is far better suited to those sorts of things.  Give me a sword and soldiers to lead into battle and I am content.  Let the leaders worry about where I should point my blade.”

She was quiet a moment, seemingly dissatisfied with that response.  “Ye are not happy with the current plans though.”

For a moment I was struck with shock.  It surprised me how clearly she divined my inner thoughts.  I had not expressed my concerns to anyone, yet she could so easily read me.  Five weeks it had been since we first met, and it seemed like there was nothing I could hide from her keen sight.
 
The preparations for the Spellblaze were well underway.  Turthel of the Kar’Krul had returned to his northern citadel, but he left his daughters as ambassadors to aid in our designs.  It meant Linaniil and I had many an opportunity to meet, though we kept it secret.  Few of my race would understand or approve of such a liaison, and none of us could afford a scandal. Yet I could not resist this human mage’s advancements, nor she mine.
 
“I am a warrior,” I said to her finally, getting brusquely from my bed and recovering my robes.  “I settle my battles facing my foe, not by toying with relics from afar.  It irks me that we must deal with our enemies in such a craven way.”

“But does it not excite ye, using these Sher’Tul ruins?” she said, putting a finger to her lower lip as she still languished in my bed, the sheets sticking tightly to her bare skin.  She seemed visibly aroused by her thoughts.  “Such powers lain dormant for so long, ready to be summoned to our control...  How it were I to command so great a venture!”

I shook my head sadly as I finished buttoning up my doublet.  “I do not trust those ruins.  We Shaloren are mighty, but we have yet to reach the heights of the Sher’Tul, nor do we truly understand the devices they have left behind.  My thoughts are more with your sister Neira on this.  We should stick to what abilities we have mastered, without stretching ourselves to such grand experimentation.”
 
Linaniil looked at me intently, a touch of humour in her dark eyes.  “If ye were leader then ye could stop this.  But then I would have to hate ye.”
 
I allowed myself a thin smile.  “Well, that would indeed be a terrible and dangerous thing.”  I finished dressing whilst Linaniil still lay in my bed, her face reflective.  “I must go now to check on the latest operations at the farportal.  You are welcome to join me.”
 
She shook her head languidly.  “Nay, I wish to rest more.  And besides, hearing their reports would but make me jealous.  Leave me here awhile – I wilst depart in secret later.”
 
I left my chamber then, dark thoughts now brooding at the back of my mind.  The date was coming closer when our plans would come to fruition and the Great Spellblaze would be unleashed.  A heavy foreboding lay over my heart.  Yet the alternatives seemed grim.  The war with the orcs was going badly, with few races able to secure their borders well and attacks from the brutes ever increasing.  Their numbers seemed inexhaustible.  Though they had little skill in warfare they could bring great harm to unprotected townsteads, and in enough force could bring down cities.  One human kingdom had collapsed under their attacks but a week before.  After that many who had initially rejected our plans came begging for our protection.  The Spellblaze seemed our only hope against imminent disaster.
 
Such thoughts were weighing on my mind as I passed from my chambers in the palace, down to the courtyard by the main gate.  Then from the corner of my eye I saw a swish of long red hair, and spun round thinking Linaniil had followed me.  But the golden robes and bright eyes of Neira revealed otherwise.
 
“Expecting someone else?” she asked with a wide smile, seeing the surprised look on my face.
 
“I was deep in thought,” I explained, bowing slightly to greet her.  “I am just on my way to inspect the farportal operations.  Perhaps you-“
 
“I shall join ye,” she said quickly, not waiting for my invitation.  I nodded my assent and guided her to my carriage.
 
As soon as we took off east the mood changed.  “She wilst only hurt ye,” said Neira suddenly.
 
I cursed quietly, understanding her meaning.  “Are there no secrets to be had in all Eyal?” I muttered.
 
“Not between sisters, and especially not between twins.”  She smiled warmly at me, yet there was no humour in her eyes.  “I mean it though.  I love mine sister, but I know her ways.  She be fickle, and willed to do her own thing when she likes.  Do not be surprised when she bores of ye.  Nor hurt.”
 
“I am quite capable of taking care of myself,” I said in clipped tone.
 
She gazed into my eyes a moment and then turned away to stare out the window.  “Well, I have warned ye...” she replied softly, a touch of sadness in her voice.
 
Was it jealousy perhaps that stirred such an outburst?  And for her sister’s attention or for mine?  I never did discover.  The rest of the trip was spent in sullen silence.  The sun was setting behind our carriage, casting a long shadow on the path ahead, and bathing the land about in crimson light.  It seemed for a moment like we rode into some demon’s plane, pitch black shadows melting into blood-red soil, whilst cold white stars began to spear through the sky above.  I shivered suddenly as the ruins came into view.
 
Few Sher’Tul ruins have been discovered which even come close to matching the grandeur of those which were near Elvala.  Many centuries our people spent excavating them, digging deep into the ground, ever careful not to damage or upset the relics.  The centrepiece was the Crystal Tower.  From the surface all that could be seen of it was a wide, even-sided square, which when cleaned of soil revealed a white stone smoother than marble.  But delving down our archaeologists found it plummeted deep, deep below the ground.  Half a mile it went down, the featureless white stone not bearing a single mark or engraving anywhere on its surface, until it ended suddenly and without foundation.  It was like the whole tower was separate from the earth, some strange thing of the stars that had dropped from the skies and lay sleeping beneath the soil.
 
Some years earlier our people had solved the invisible runes that allowed it to be opened, revealing vast crystal-lined halls and chambers arrayed in geometric patterns of sublime beauty.  Light sparked and shone from every surface, and the walls seemed to hum with energy.  Many shafts and passageways could only be navigated by flight, and at the top was found a grand room large enough to encompass the whole palace of Elvala.  At its centre was the farportal, a raised dais forty feet in diameter and crackling with energy upon which slowly spun a cloud of stars.  It was beautiful and frightening, enchanting and terrifying.  No power of the Shaloren could discern its operation, and though through careful experimentation we were able to manipulate its energies, never could we get a true grasp of the forces that lay beneath.

Neira and I descended to the base of the tower, smothered in the cold shadows of the excavated ruins.  I nodded to the guards as we passed through the square white entrance, and Neira’s eyes instantly enlarged in wonder.  The scintillating rooms were eye-catching to be sure, but they were also desolate and empty.  I tried to imagine what it must have looked like when filled with Sher’Tul.  “How did they all die?” I asked under my breath as we traversed the crystal halls, a question many had asked before.
 
The sorceress picked up on my words and laughed softly.  “It be a mystery, of course!  Mine mother once taught me that they killed themselves in a great civil war, using magics far beyond our imaginings.”
 
“I wonder,” said I.  We had our own records, of course, which we didn’t share with the younger races, but they were not so clear-cut as the many myths that had spread over the ages.
 
We reached the central shaft, and from there levitated up past floors and floors of abandoned chambers, living spaces, workshops, storerooms, and many other areas of purpose undivined by our loremasters.  Finally, after ascending for several minutes, we rose into the grand chamber of the farportal, and Neira gasped to see its size.  Her eyes soon settled on the great Sher’Tul farportal, sparks from it reflecting off the roof hundreds of feet above.  About it were bustling many of our Shaloren mages in silken robes, and Ephinias himself was leading the operations.
 
He broke from his advisers as he saw us arrive, and strode towards us with a confident smile on his face.  Though he wore the grey robes of a research mage he still bore his great golden staff, Luminis, token of his position as king.
 
“Ah, General Aranion!” he said, “You have come at last.  And brought the Kar’Krul girl with you; how splendid.”
 
I gave a small bow.  “Your majesty.  I am here for the update on our operations.”
 
“Yes, yes, of course,” he said with a dismissive hand gesture.  “And doubtless the girl is here to make sure we know what we’re doing?”
 
If Neira was offended she covered it up well.  “It would be mine delight to see evidence of ye skill and power over the ruins, lord Ephinias.”
 
The king smiled and nodded then, and called to some of his aides.  “Prepare the topography demonstration, using the acute fire strand.”  He turned back to us then.  “It is not mere skill and power of course that we can show you, but subtlety and scale too.  Now excuse me a moment whilst I join the others.”
 
He went with two of the senior research mages then to the front of the farportal.  They faced each other and began a low humming in unison, and slowly it seemed that the sparks from the farportal began to flicker redly.  Over the course of a few minutes their hum became a higher pitched chant, but softly sung and still in perfect unison.  As they raised their staffs there appeared above the farportal an image in flames, and looking at it both Neira and I marvelled, for we could see clearly that it was an image of ourselves, looking upwards, as if looking we were staring into a mirror.  Our features and movements were all clearly discernible, down the smallest detail, all carved out of flickering orange fire.
 
Then the chanting rose higher and it seemed the image zoomed out, so that we saw the farportal nearby us and the mages gathered about.  And still the focus soared upwards till we were but specks in a wide hall, until the image was displaced by a white square with carven edges dug into the earth about it, and I knew we were looking at the top of the Crystal Tower from above.  The view widened, and I could see the land rushing away, and the city of Elvala to the west.  The chanting rose higher and now the sea could be seen, and the mountains to the north-west, and all the land about.  And soon the continent was visible, right to the frozen north, and the ocean wrapped all about, and it seemed small white stars were dotted about the landscape.  The singing reached a crescendo and before us hung an image of the whole of Eyal, a globe of fire suspended in mid-air, slowly turning.
 
Then the chanting stopped and the image disappeared, and I could hear beside me Neira suddenly gasp for air, as if she had not dared draw breath through the last few minutes.
 
“You see now?” said Ephinias, grinning with pleasure.  “From the smallest detail to the grandest scale we can manipulate the farportal’s energy.  And did you see those white points marked across the image?  They are the other farportals spread across the world, and this one can connect to them all.  With careful, delicate control we can harmonise the energy of them all and use it to our will.  I’m afraid your sword can be no match to this, Aranion.”
 
I had no words to respond, and only nodded softly, still in awe of what I had seen.  Neira seemed the same, and I could see her now staring at the farportal with the same eager eyes as her sister.  She was converted.
 
Yet my hand strayed across the hilt of Mooncutter, and my heart still murmured with unease.`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第三章：远行传送门#{normal}#

“为什么你不准备成为精灵们的领袖呢？”，莱娜尼尔悠闲地躺在我的床上，双手撑着头饶有兴致地问道。

我的思绪还没有从片刻前的温存中缓过来，对于这个突然的问题感到有些惊异。“为什么我会想要成为他们的领袖呢？”，我反问道。

“当然了，因为你的实力是那么的强啊”，她回答道，“我觉得你是你同族中战斗能力最强的一位，这样强大的力量足以让你成为他们的领袖。”

我微笑道，“光靠武力是无法引领族人的。一个优秀的领袖需要勇于承担责任，审慎做出决定，并具有灵活的政治手腕。我对于这方面的事情可没有什么兴趣，毕竟，伊菲尼亚斯陛下在这方面比我擅长多了。只要给我一把剑，让我能够和部下一起驰骋沙场，我就已经心满意足了，让真正的领袖来思考我和我的战士应该与谁作战吧。”

她沉默半晌，看上去对我的回答并不满意，“呐，不过呢，你看起来对目前的计划并不满意。”

这一令人惊讶的提问让我感到一阵震惊，我不知道她究竟是如何瞬间洞悉了我的内心想法。在此之前，我从来没有在任何人面前表现出过我的担忧，然而她一下子就看穿了我的伪装。她和我五个星期前才刚刚见面，然而任何事情都逃脱不了她敏锐的洞察。

关于魔法大爆炸计划的筹备工作正在有条不紊地进行当中。卡库罗尔首领特塞尔已经返回了他位于北方的城堡，然而他的两个女儿仍然作为大使留在这里，协助我们的计划。这意味着莱娜尼尔和我可以时常相见，然而我们始终保守秘密。我高傲的同族们仍然难以接受精灵与人类的浪漫关系，而我们也无法接受可能迎来的流言蜚语。即使这样，我也难以抵御她的魅力，而她也是一样。

“我是一个战士，”许久的沉思后，我从床上爬起，整理我的长袍，“我喜欢亲自面对敌人，而不是借助某件遗物从远处消灭他们。这样的懦夫行径令真正的战士作呕。”

“然而，开发夏·图尔人遗迹中失落的力量不是那么让人心潮澎湃吗？”她呢喃着，手指轻触下唇，光滑的皮肤置身于柔软的被子的紧紧环绕中，仿佛已经被她那恢弘的梦想深深吸引，“这样强大的能量已经在世间沉眠了那么长时间，直到今天，我们强大的魔法可以让我们亲自驾驭它们，把雷霆万钧的恢弘气势掌握在不及盈寸的掌心之中……唉，若能由我亲自统领这般伟业，该有多好！”

搭上上衣的搭扣，我有些遗憾地摇了摇头。“坦率地说，我并不信任这些遗迹的力量。是的，我们永恒精灵的确有着强大的魔法实力。然而，我们渺小的知识比起那些夏·图尔人实在是相距甚远，以至于我们甚至无法理解他们所遗留下来的物件究竟有什么意义。在这一意义上，我的想法更接近你的孪生姐妹尼耶拉。我们应该用稳健的脚步前行，妥善而审慎地使用那些我们所能掌握的能力，而不是猛然把我们的野心扩展到这种庞大的实验之上。”

莱娜尼尔凝望着我，用调笑一般的语调柔声说道，“如果你成为了领袖，你可能会阻止这一切；但那样的话，或许我会一辈子恨你。”

我露出了浅浅的微笑。“嘛，那还真是一件可怕而又危险的事情。”当我更衣完成时，莱娜尼尔仍然在床上休息，眉间若有所思。“我必须要前去了解远行传送门那边工作的最新进展了。如果你乐意的话，请务必和我一同前去。”

她有些倦怠地摇了摇头。“不，我想要再休息一下。还有，听取他们的报告只会让我嫉妒不已。请让我在这里呆一会儿吧——我稍后就会秘密离开。”

我小心地关上卧房的房门，一股阴霾仍然在脑海之中萦绕。随着时间的推进，魔法大爆炸的庞大计划也一天天被提上日程，一股不详的预感涌上心头。命运总是那么残酷，与计划进行的有条不紊相伴的是兽人战线上的节节败退，只有少数几个种族能够防守他们的边境线，而兽人们的进攻却永不停歇，愈演愈烈。他们的数量似乎无穷无尽，永不枯竭。他们虽然不善战，却能重创毫无防备的村镇；只要兵力足够，甚至能攻陷城市。一周前，刚刚有一个人类王国在他们频繁的攻击下不堪其扰，最终溃败。此后，许多起初拒绝我们计划的人都跑来祈求我们的保护。看起来，对于兽人的侵袭这一迫在眉睫的危险，魔法大爆炸可能会成为我们唯一的希望。

我从卧房顺着宫殿向前，混乱的思绪在我的脑海中盘旋，伴随着我漫步过庭院走向大门。眼前红发女子轻盈的身影让我误以为莱娜尼尔已经跟着我一路走来，然而她金色的长袍和明亮的眼睛让我想起了，那是她的孪生姐妹尼耶拉。

“在想着什么人吗？”，她微笑地望着我，观察着刚刚表情细微的变化。

“抱歉，我刚才正在思考一些问题，”我轻轻弯腰对她示意。“我正准备前去督导和远行传送门有关的工作事宜，如果您——”

“我想和您一同前去。”还没等我说完，她就爽快地回应道。我点了点头，领着她坐上我的马车。

马车缓缓前行，尼耶拉的声音突然从我耳边传来。“她这样做只会伤害你。”

我一下子明白了她的意思，感到一阵震惊。“要命，在埃亚尔已经不存在秘密了吗？”我小声说道

“姐妹之间没有什么能隐瞒，尤其我们还是双胞胎。”她温柔地微笑着，然而眼神却没有一丝开玩笑的气息。“我是认真的。我爱我的姐妹，但我了解她的行事风格。她喜怒无常，想怎么做就怎么做。如果她对你感到厌倦，不要惊讶，也不要伤心。”

“我想，我应该有能力整理自己的心情。”我抿嘴说道。

她凝望着我的眼神慢慢移开，遥望着窗外变幻不定的风景。“唉，我想我已经提醒了你…”她柔声回答道，声音中仿佛包含着一阵忧伤。

是嫉妒促使她说出这番话吗？她嫉妒的是姐妹对我的关注，还是我对她姐妹的关注？我始终没有弄清。剩余的旅途中，我和尼耶拉始终保持沉默。夕阳从马车的背后缓缓落下，巨大的阴影投射在向前的小路上，暮色的笼罩将周围的风景染上了一片深红。有一瞬间，我们仿佛在恶魔的位面上漫步，漆黑的阴影慢慢融化在血色的土壤之上，群星惨淡的冷白色光辉似乎瞬间从苍穹直射下来。繁星点点间，遗迹从地平线映入眼帘，让我不禁颤栗。

已发现的夏·图尔遗迹中，鲜有能与埃尔瓦拉附近那一处的宏伟相提并论的。我们的人民花了几个世纪来悉心研究它，调动的工程量庞大无匹深入地下，却又如此小心地不曾损坏和扰乱任何遗迹中的古物。这个遗迹的核心被称为水晶塔。从地面上向下看，我们只能看到巨大的方块，在泥土被清理之后显露出来是比大理石更加光滑的白色石板。继续往下挖掘，白色石板似乎无穷无尽，其表面也没有任何能够给出说明的雕刻和标记，直到半英里后我们找到了它的底部，没有地基那样的设施。这简直就像着整座塔并不是立于地面之上，而是在天空中漂浮，直到某种力量让它从空中坠落，静静地在大地中沉眠了无数的岁月。

若干年前，我们的魔法师找到了遗迹上不可见的符文，终于叩开了遗迹的大门。遗迹内，壮观的水晶大厅以庄严而又优美的几何图案有规律的排布着，就连墙壁似乎也呼吸着能量。许多甬道和通路都只能通过飞行才能到达，而其顶端是一个足以容纳整个埃尔瓦拉宫殿的巨大房间。在它的中央是远行传送门，一个直径四十英尺的高台，巨大能量如同星云般在周围盘旋，噼啪作响。那是何等美丽而可畏，迷人而恐怖的壮观景象。永恒精灵们根本无法理解它工作的真正原理。即使通过小心的实验我们有办法操纵它所具有的能量，我们也永远无法真正知悉到底是什么力量驱动着它。

我和尼耶拉下到塔底，四周笼罩在已发掘遗迹的冰冷阴影中。穿过白色方形入口时，我向卫兵微微点头，尼耶拉则惊奇地睁大了眼睛。这座闪光的大厅的确足够吸引眼球，但是里面空无一物的情景不禁令人感到孤单。我试着去构想许久之前，当这里仍然被夏·图尔人所充满的情景。“为什么夏·图尔人灭亡了呢？”漫步于水晶大厅，我轻声向尼耶拉问出了那个或许问过许多次的问题。

尼耶拉听言微笑起来。“这当然是个谜啦！不过，我的母亲曾经告诉我，夏·图尔人在一场宏大的内战中走向了灭亡，他们所使用的魔法超乎我们任何人的想象。”

“我也想知道。”我回答道。我们当然有自己的记录，只是不曾与较年轻的种族分享；但这些记录远不像历经岁月流传的诸多神话那样结论分明。

我们到达了中央甬道。我们悬浮而起，缓缓上升，眼前一层层废弃的屋室从上方进入我们的视线，然后缓缓地在视野中消失。卧房、工坊、储藏室、还有很多房间就连我们的博学之人也没法猜测出是用来干什么的。在经过几分钟的上升后，我们到达了远行传送门所在的大厅，尼耶拉不禁因惊讶而倒吸一口冷气。她的眼睛很快看到了夏·图尔的远行传送门，闪耀、映照着几百英尺之上的天花板上的图案。在传送门的周围，一大群身穿高级丝绸长袍的永恒精灵法师正在紧张地工作中，而伊菲尼亚斯陛下正亲自指挥着他们。

当他看到我们的到来时，他先行从一旁围绕的皇家顾问身边脱开身来，怀着自信的笑容向我们走来。尽管他穿着魔法研究院的灰色长袍，他的手中仍然拿着那把金色的法杖，辉光杖，作为他国王身份的证明。

“啊！真高兴见到你，艾伦尼恩将军！”他说道，“你终于来了。这位是卡库罗尔的大小姐吧，真是太好了。”

我微微鞠躬。“陛下。我此来是想了解我们行动的最新进展。”

“啊，啊，当然是的，”他有些鄙夷地挥了挥手。“那么不用说，这位小姐一定是来这里确认我们到底会不会用魔法吧。”

尼耶拉的微笑令人无法判断她到底是否是在生气。“能够亲眼见证你们有关遗迹能量的强大能力和丰富技巧将会是我无上的荣幸，伊菲尼亚斯大人。”

国王微笑着点了点头，回身叫来了他的副官。“准备地形演示，使用锐火束。”他回身向我们说道。“我向你们展示的可不只是技巧和能力，而是从精微到庞大的一切细节。现在请二位稍候片刻，我去与他们会合。”

他与其他两名研究院高阶法师一起走到远行传送门面前，互相遥望，四周传来一阵阵和谐的低吟。随着法术的和声在大厅中飘扬，远行传送门周围的闪烁着星星点点的隐约红色。几分钟后，他们的低吟音调渐渐升高，变成了无比默契的轻声吟唱，然而始终保持在完美的协调之中。紧接着，他们高举手中的法杖，远行传送门上方浮现出一幅由火焰构成的影像。在它的悉心雕刻中，慢慢形成了一幅清晰的画卷，呈现出我和尼耶拉两人的图像。所有的特征都如此明晰，所有的动作都精巧符合，下至最小的细节都清晰可辨，简直如同站在一面巨大而澄澈的明镜之前。

紧接着，随着吟唱的歌声越来越大，影像中的视野也愈发宽广，从中呈现出我们身边的远行传送门和周围围绕着的众多法师。视野飞腾而上，眼前所见的东西越来越小，最终化为宏伟大厅内的一个小点。紧接着，画面被一个白色的方形取代，周围是挖掘直入地底的痕迹，显然我们的视野正处于水晶塔的正上方。随着聚焦范围越来越大，大地奔腾而过，西部埃尔瓦拉市的房屋隐约可见。伴随着吟诵之声，我们看到了奔腾的大海，看到了西北的层峦叠嶂。我们看到了整片大陆的全景，北部寒风笼罩的高原被冰雪所覆盖，包围着的海洋似乎无穷无尽，大陆上闪烁着无数的白色小点，如同繁星一般。咏唱达到了高潮，我们从宇宙俯瞰到了埃亚尔星球的全景，在火焰的缭绕中悬浮于半空之中，慢慢转动。

然后咏唱停止了，先前的图像瞬间消失地无影无踪。我似乎听到尼耶拉因为刚才令人窒息的壮观景象而喘不过气来。

“你现在看到了吗？”伊菲尼亚斯陛下大笑着。“我们可以全方位操纵这个远行传送门的所有能量，无论是最小的细节还是最大的范围，一切尽在掌握之中。还有，你看到地图上所标注的那些白点吗？这是世界上其他的远行传送门，而我们的这个传送门可以与它们中的任何一个链接。经过精心的操纵和悉心的控制，我们可以协调他们全部的能量，并用来实现我们的愿望。我想，你的那把剑可干不了这种事情，艾伦尼恩先生。”

我仍然被我刚才所见到的奇景所震惊，无话可说，只能微微点头。尼耶拉似乎也产生了一样的想法，以和她的孪生姐妹一样的热切眼神望着这座远行传送门。是的，她的想法被改变了。

然而，我的手仍然环绕着斩月剑的剑柄，心头隐隐呢喃着不安之情。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00156 | HUMAN-REVIEW | cross-batch-033 | confirmed | 人工待决：按上表逐项决定改写；两项收窄意见不要写进修复理由。译文未修改。 |  | fix |

<details><summary>hrq-00156 · HUMAN-REVIEW 详情</summary>

```
作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-032-01.md](reports/sol-032-01.md)。译文未修改。共 23 个 claim：21 confirmed、1 refuted、1 advisory，无 pending。Gemini「该条存在多处忠实度问题」的主结论被 confirmed。

| 类别 | Sol 分档要点 |
| --- | --- |
| 忠实度/漏译（confirmed） | `be no match to this` 曲解；`Expecting someone else?` 错移；`I wonder` 语气丢失；`know what we’re doing` 窄化；“提上日程”未表达发动日临近；`collapsed under their attacks` 力度降低；`Yet the alternatives seemed grim` 漏译；`naked form` 漏译；`I looked at her` 漏译；`brusquely` 漏译且臆增“许久的沉思后”；`visibly aroused` 被弱化；向东启程与气氛骤变漏译；火花主体漏失并臆增“天花板上的图案” |
| 语法/排版（confirmed） | “像着”错别字；“消失地无影无踪”应为“得”；“远行传送门周围的闪烁着……”句法残缺；三处 `？”，` 标点不规范 |
| 无缺陷项（confirmed） | 单手支头被译成“双手”属动作事实错误；格式控制符完整；点名的核心专名未发现实质错误 |
| 收窄 Gemini（refuted/advisory） | refuted：`I wonder` 并未“反转成附和”；advisory：`collapsed` 被定性“严重”过重，应按“力度降低”处理 |

人工待决：按上表逐项决定改写；两项收窄意见不要写进修复理由。译文未修改。
```
```
raw verdict: be no match to this 被曲解为“宝剑干不了这种事情”→confirmed; Expecting someone else? 被错移为“在想着什么人吗”→confirmed; I wonder 的怀疑/保留语气丢失→confirmed; know what we’re doing 被窄化成“会不会用魔法”→confirmed; “一天天被提上日程”未表达发动日期临近→confirmed; collapsed under their attacks 力度降低→confirmed; Yet the alternatives seemed grim 漏译→confirmed; naked form 漏译→confirmed; 单手支头被译成“双手撑着头”→confirmed; I looked at her 漏译→confirmed; brusquely 漏译并臆增“许久的沉思后”→confirmed; “雷霆万钧……不及盈寸的掌心”属无源码依据扩写→confirmed; visibly aroused by her thoughts 被明显弱化→confirmed; 向东启程及气氛骤变均漏译→confirmed; 火花主体漏失并臆增“天花板上的图案”→confirmed; “像着”是明显文字错误→confirmed; “消失地无影无踪”中“地”误用→confirmed; “远行传送门周围的闪烁着……”句法残缺→confirmed; 三处问号闭引号后又接逗号的标点不规范→confirmed; 格式控制符完整保留→confirmed; Gemini 点名的核心专名未发现实质错误→confirmed; I wonder 被称为“反转成附和”→refuted; collapsed 问题被定性为“严重”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-032-01.md](reports/sol-032-01.md)。译文未修改。共 23 个 claim：21 confirmed、1 refuted、1 advisory，无 pending。Gemini「该条存在多处忠实度问题」的主结论被 confirmed。 人工待决：按上表逐项决定改写；两项收窄意见不要写进修复理由。译文未修改。
```
</details>

## entry-01221

- 位置：`mod-tome.lua:14988`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Four: Before the Dawn#{normal}#

I rode my great grey horse at a low trot, surrounded by my lieutenants and their elite cavalry and spellrangers.  Beside me on a brown mare my squire held high a banner emblazoned with a flame-wreathed sword, symbol of my personal entourage.  The pole seemed to shiver slightly in the young elf’s hands, a sign of nervousness.
 
“Hold that banner firm, boy,” I said in a commanding tone.
 
The squire suddenly sat upright in his saddle, and gripped tight on the banner pole.  “Yes, sire!” he said, alarmed.  “Whatever you say, sire!”  He kept his head faced forward but I could see his eyes glance towards me, desperate for approval.  Whatever I say indeed...  I had seen his gaze on me before, with all the adoration of a young soldier towards his commander, and perhaps a little more.  If I had not the joy of Linaniil’s company then the attention of such a pretty lad would not be unwelcome.  But this was not the time for such thoughts.
 
This would be the day, the day of the Spellblaze, and the boy had every right to be nervous.  It was a few hours after midnight, and already our scouts would be engaged alongside the other races, drawing out the orcs from their hiding places.  We marched through our main offensive lines, where we would hem them in before the great conflagration.  All around were arrayed spears and swords and mail, glistening in the starlight.  Troops upon troops of battlemages in purple robes held aloft glowing staves.  It was a sight to behold.  Yet we knew also the risk of engaging on open ground with the orcs in their full numbers.  If the Spellblaze failed then we would suffer greatly.

I set up camp upon a low hill overlooking the field, and then left my entourage to seek the Kar’Krul army to the north.  As I rode my stallion towards their station I could see smoke rising in the east.  Four thick grey plumes stood out against the pre-dawn light.  They would be villages looted and burned by the orcs as they rampaged against our feigned assaults.  The townsteads would be empty, but after this battle there would be nothing left for their residents to return to.  A small sacrifice in a game of war that spanned the continent.

A fifth column of smoke began to rise, and in the greenish haze of early morn those pillars of smoke suddenly seemed to look like a demonic hand stretching over the world, ready to dig its claws into the earth and rip out the flesh beneath.  This, I knew, was the threat the orcs faced to us all, a menace to all civilisation.  Whatever price we paid to stop them would be a small one.  So I thought.  So we all thought.
 
When I reached the Kar’Krul camp Linaniil came out to meet me.  Her smile was warm at the sight of me, but I could tell from her eyes that she was more excited for the events of the day.  “Just a few more hours,” she whispered like an impatient child.  “This will be fascinating!”
 
As I came in the Kar’Krul pavilion I saw Neira inside, and some of their senior mages and delegates from other human kingdoms.  I knew Turthel would not be with them, as he stayed in his northern city with his people.  It was not cowardice nor age that held him back from the front lines of war.  Indeed, it was said that ever since his wife was killed by the orcs he had to restrain himself from battle, lest his anger overcome him and he destroy friend and foe alike in his rage.  Yet it was known that sometimes he would venture through the lands alone, and he would bring with him a deafening storm of wrath, and the orcs would cower at the rumour of the approach of Turthel, Tempest of the North.
 
Neira and Linaniil commanded the Kar’Krul forces, and from the firm-set look on their archmages’ faces it was clear that they were ready for whatever the day would bring.  Yet Neira looked troubled, doubt evident in her eyes.
 
“What irks your sister?” I whispered to Linaniil.
 
“Some dumb dream,” she responded callously.
 
Neira’s eyes shot up.  “It were not a dream!” she barked.  “An omen it were, I tell ye!”  She turned to me then with pleading eyes.  “Ye must believe me, Aranion.  Something wilst go terribly wrong today.  I saw last night a terrible sight in mine dreams, as if it were a memory of long ago.  There were a burning city, made of glass and silver and marble.  And as it burned I did hear the cries of thousands, tens of thousands, young and old all dying.  And then the city fell, for it had been held in the sky, and it crashed down to the earth with a shattering torment that spilled across the land.  And other cities there were, and pillars of violet light struck up from them, and they did dance around filling the air with the scent of ozone and seared flesh.  Death was everywhere!  Death like none we have ever seen.
 
“It were no mere dream I tell ye.  It be a message, a warning - some forgotten tale of the dangers we play with.  We must stop this thing!”
 
Linaniil was tapping her foot impatiently as her sister raved, but I could see some of the other leaders looking worried.  I knew I had to quiet Neira down, so I drew myself near and put my hands on her shoulders, looking her calmly in the eyes and bringing my face close.
 
“It may well be that this is no dream.  For this is no normal day, and even in all the legends of ages past this will stand out as a day of reckoning.  Our civilisation in under peril, our way of life threatened from the orcish scourge.  We rest upon a knife edge, the world balancing on a pivot, and the wrong sway could tip us into darkness and despair forever.  Our actions today will decide this.  So yes, you have had a warning, you have had a message, and that message is to be strong.  For today we all hold the reins of fate in our palms, and only the steady hand can guide us past the threat of doom that is to come.  Neira, can you be that steady hand?”
 
She looked at me with open and hopeful gaze, her fingers clenched around my wrist as if she sought to draw strength from me.  She nodded slowly then.  “I’m sorry Aranion.  I just... I’ll be strong.”
 
I turned to the others who all seemed rapt by my words.  It was clear that leaving them to their own thoughts could only bring trouble.  I had to pull them into action straight away.  “It begins now!” I shouted.  “Gather your troops and prepare for the march.  Slow and steady we shall advance, carefully shall we hold the battle, and beyond fire and fury we will emerge free and victorious.  This day shall stand in history forever!  This day shall mark a new era for all the races!  The day of the Spellblaze is here!”

They all cheered and rushed to order their troops, taking courage from the duties of command.  Neira went to her own mages, and I left the pavilion alone.  But outside I was ambushed by Linaniil, who pulled me into an empty tent with a playful laugh.
 
“Ye said ye were no leader!” she exclaimed with a grin.  “That were a leader’s speech if ever I heard one.”

I shrugged and smiled modestly.  “I said what I had to.”
 
She drew close then, a sudden flush of worry in her face.  “It were just a dream, right?”  I could see then beneath all the bravado and humour she was mortally scared, her fingers trembling as she gazed into my eyes, yearning for reassurance.
 
“It was just a dream,” I lied, and it is a lie I have paid for with all my heart and soul.  “Everything will be all right.”  I pulled her close and wrapped my arms around her slender frame, and she held tight to me, still trembling slightly.
 
“Thank you, Aranion,” she whispered.  Turning up her face she kissed me, and it was the softest, most delicate kiss she ever gave me.  It was also the last.
 
We parted then, and I began the lonely ride back to my own troops.  My heart was now pounding like a deafening war drum, whilst the words of Neira still echoed round my head.  They stirred up a memory in me of a dream I myself had that morning, but that had laid dormant in my mind till then.  I was lying in my bed, and floating above me was a shape of light and air, like the figure of a creature I had never seen before.  It had long tentacles for arms, and billowing robes fluttered about it slowly.  Where it should have a head there was only a small bump, but I could tell it was focused on me.  It stretched out a long tentacle towards me, as if it were warding against a dark and dangerous threat.  A feeling came over me of terrible foreboding, the looming portent of a doom like no other the world had ever seen.  As the tip of the tentacle neared my brow everything went black.

Was it a dream?  Some strange foretelling?  Or could it have been a true apparition, something trying to give me a direct warning?  But I had no time for such thoughts.  The time of the Spellblaze was nearly upon us, and there could be no room for doubt.  I spurred my horse on to my fate.`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第四章：黎明将至#{normal}#

我骑着高大的灰色战马缓步小跑，一旁并驾齐驱的是我的副手和手下的精锐骑兵与法术游侠。身旁一匹棕色马上，我的侍从高举一面画着被火焰环绕的剑的旗帜——那是我的随从部队的军旗。这个年轻精灵手中的旗杆似乎有些微微晃动，表现出他隐约的紧张之情。

“孩子，把旗帜抓牢了！”我用命令的语调说道。

侍从在马鞍上坐正，牢牢抓住手中的旗帜。“是，长官！”他大声回答道。“一切听你的命令，长官！”他的脸面朝前方，但是我似乎可以看到他的眼神仍然凝视着我，眼中满是渴望被认可的急切。一切听我的命令…嗯哼，我以前也见到过这样的眼神，包含着一名年轻军人对长官的无限憧憬，当然可能还有一点超乎憧憬的东西。如果我没有莱娜尼尔的话，考虑一个这样帅气的小伙子似乎也不错。当然，现在显然并不是想这些的时候。

今天就是魔法大爆炸计划进行的那一天了，那个孩子感到紧张是很正常的。此时已是子夜后数小时，我们的侦察兵应已与其他种族并肩交战，将藏身的兽人引了出来。我们穿过主攻阵线，准备在那场大火降临前把兽人合围。四周长矛、刀剑与锁甲列阵，在星光下闪耀。一队队身穿紫袍的战斗法师高举发光的长杖。那真是难得一见的奇景。然而，我们也知道，在开阔地带迎战齐集的兽人大军风险极大。一旦魔法大爆炸失败，我们必将损失惨重。

我在一旁的小丘上扎寨以确保对战场的全局把握，随后留下随从，亲自骑马前去联系驻扎在北方的卡库罗尔支援军。当我骑着战马向哨所奔驰之时，隐约见到狼烟从东方升起，四条灰色的烟流在黎明前的光照笼罩下摇曳。那是被兽人们焚烧劫掠的村舍，他们刚刚被我们的佯攻部队所吸引前来这里。村子里的居民已经预先撤离，然而经此一役，他们已经注定无家可归。在这场横跨大陆的战事中，他们只是战争中渺小的牺牲品罢了。

第五道烟尘从远方升起，在清晨绿色薄雾的笼罩下，这些烟柱如同伸展到世界各地的魔爪，正准备撕开地面，吞噬一切。这个恶魔就是兽人，它是对我们任何种族的威胁。无论付出什么代价来阻止他们都不过分。这就是我当时的想法，这就是我们所有人当时的想法。

当我到达卡库罗尔的营地，莱娜尼尔亲自出来迎接我。她看到我时笑容温暖，但我从她眼中看得出，真正令她兴奋的是今日即将发生的大事。“只剩几个小时了，”她像个等不及的孩子般低声说道，“一定会精彩极了！”

我走进卡库罗尔的营地，在里面看到了尼耶拉和其他高阶法师与来自人类诸王国的代表。我知道特塞尔不会亲自前来，因为他要和他的人民呆在一起。这并不是因为懦弱和衰老让他远离前线。实际上，据说自从他的爱妻被兽人所杀之后，他便不得不克制自己、避免投入战斗，以防止他的仇恨夺去他的理智，让他在暴怒中不分敌我地大开杀戒。然而，众所周知，他有时仍会独自走遍北方的冻土，所到之处总伴随着震耳欲聋的狂怒风暴。兽人们只要听到特塞尔，北之暴风的名字就会闻风丧胆。

尼耶拉和莱娜尼尔指挥着卡库罗尔的部队，从那些大法师凝重的表情可以看出他们为这一天可能发生的一切做好了准备。然而，尼耶拉的眼神却包含着无尽的困扰之情。

“你的孪生姐妹怎么了？”我悄然问向莱娜尼尔。

“一些无聊的梦而已。”她没好气地说道。

尼耶拉的眼神突然激动起来。“这不是梦！”她大喊道。“我告诉你们，这是未来的预兆！”她转过头来，用哀求的眼神望着我。“你必须相信我，艾伦尼恩先生，今天一定会出大事的！我昨晚在梦中见到一幅恐怖的场景，仿佛它是许久之前的记忆一般。我看见一座由玻璃、白银和大理石建成的城市正在燃烧。城中成千上万人的哭喊传入我耳中，老幼皆在死去。随后，那座原本悬在空中的城市坠向大地，以震碎一切的苦难猛击地面，冲击横扫大地。还有其他城市，一道道紫色光柱从其中冲天而起，在空中舞动，弥漫出臭氧与焦烂血肉的气味。到处都是死亡！是我们从未见过的死亡。”

“我告诉你的并不仅仅是梦境！这是一条信息，一条警告——这是一段逝去的传说，因为我们根本不了解我们在把一场多么大的危险视同儿戏！计划必须被终止！”

在尼耶拉慷慨激昂的怒吼声中，莱娜尼尔不耐烦地抖着脚，但是我看到许多其他的领袖看起来有些动摇。我知道为了计划的进行必须让她冷静下来，所以我向前走去，双手放在她的肩上，冷静地望着她的双眼，慢慢向她说道。

“这很可能确实不是一个梦。你知道，世界上没有一天不处在危险之中，而今天则是比任何时代的任何传奇中的日子都要重要的一天。我们的文明正处在危险之中，我们的生活方式正遭受兽人们野蛮侵袭的威胁。我们的命运宛如悬于刀尖之上，我们的和平生活正摇摇欲坠，任何错误的决断都会让我们跌入黑暗和绝望的深渊。今天，我们将会做出最大的决断。所以你说的对，你收到了一个消息，你受到了一条警告。而我们所应该做的，就是回应这个警告，就是变得足够坚强。今天，我们要紧握希望的缰绳，我们要扼住命运的咽喉，只有这双真正坚实的双手才能引领我们逃离袭来的毁灭，才能给我们带来真正的和平。尼耶拉小姐，你能成为我们坚实的双手吗？”

她用开朗和充满希望的目光望着我，手指紧握住我的手腕，仿佛要从我的身上汲取力量。她慢慢地点了点头。“对不起，艾伦尼恩阁下。我只是……我会变得坚强的。”

我转向那些被我的演说所感动的人。显然，如果放着他们不管只会带来麻烦，我必须让他们立即开始行动。“现在开始！”我大喊道。“集结你们的军队，做好行军准备。我们将缓慢而稳健地推进，谨慎地把握战局；越过烈火与愤怒，我们终将赢得自由与胜利。今天，将会永载史册！今天，将会给所有种族带来新的纪元！魔法大爆炸之日已然到来！”

被刚才的命令所鼓舞，所有人欢呼着冲向前去，组织起他们的部队。尼耶拉回身组织其她手下的法师，而我独自离开了帐篷。一出门，我就撞见了莱娜尼尔，她一边和我嬉戏一边大笑着，连拉带推把我带进了一旁的空帐篷里。

“你说过你不准备成为领袖的！”她笑着说道。“你刚才的演说真是比我见到的任何领袖更加优秀。”

我耸了耸肩，谦虚地笑道。“我只是说了一些我该说的话。”

她向我走近，一瞬间的忧虑从她的脸上闪过。“这只是个梦，对吧？”在她平日幽默的语调中，隐约可以觉察到她极度恐惧的心情。她的手指稍稍颤抖，仿佛在渴望着我的保证。

“这只是一个梦而已，”我撒了一个小小的谎，却不知道，这个谎言的代价即使用我的一生也无法赔付。“一切都会好起来的。”我亲昵地拉住她，轻轻拥抱住她纤弱的身躯，她用力抱紧我，还在微微颤抖之中。

“谢谢你，艾伦尼恩。”她悄然说道。她转过头，与我长吻。这是我和她所经历的最柔软，最细腻的一个吻，也是我和她的最后一个吻。

我们就此别过，我独自一人策马返回部队。我的心脏如震耳欲聋的战鼓般怦怦作响，尼耶拉的话仍在脑中回荡。它们唤醒了我今晨做过的一场梦；此前，那梦一直沉在记忆深处。在梦中，我躺在床上，上方漂浮着一道由光与空气构成的身影，像某种我从未见过的生物。它以长长的触手为臂，宽大的长袍在身周缓缓飘动。头部本该在的位置只有一个小小的隆起，但我能感觉到它正注视着我。它向我伸出一条长触手，仿佛要警告我提防某种黑暗而危险的威胁。一股可怕的不祥预感攫住了我：一场世界前所未见的灾厄正在迫近。当触手尖端接近我的眉心时，一切归于黑暗。

这只是一个梦吗？还是某种未来的预兆？或者这是一个真正的幽灵，想要直接对我发出警告？然而，当时的我没有时间思考这些。魔法大爆炸的时刻即将到来，现在已经没有怀疑的余地了。我策马扬鞭，命运的车轮滚滚转动。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00157 | HUMAN-REVIEW | cross-batch-034 | confirmed | confirmed：`no normal day` 译反且漏 `day of reckoning`；confirmed：“希望的缰绳/扼住命运的咽喉/真正的和平”均为无依据增译；confirmed：`the steady hand` 单数比喻被破坏；confirmed：`rip out the flesh beneath` 的大地—血肉意象被泛化；confirmed：“这个恶魔就是兽人”“任何种族”改变原句关系；confirmed：“组织其她手下的法师”表面文本缺陷；confirmed：`taking courage from the duties of command` 施受关系被改变；c… |  | fix |

<details><summary>hrq-00157 · HUMAN-REVIEW 详情</summary>

```
raw verdict: no normal day 被译反，并漏掉 day of reckoning→confirmed; “希望的缰绳／扼住命运的咽喉／真正的和平”均为无依据增译→confirmed; the steady hand 的单数比喻被破坏→confirmed; rip out the flesh beneath 的大地—血肉意象被泛化→confirmed; “该血肉意象明确呼应被焚村镇生灵”只是合理解读，不是源码明示→advisory; “这个恶魔就是兽人”及“任何种族”改变了原句关系→confirmed; “组织其她手下的法师”是表面文本缺陷→confirmed; taking courage from the duties of command 施受关系被改变→confirmed; Turning up her face 被译成反向动作→confirmed; “与我长吻”属于无依据增添→confirmed; “长吻必然与轻柔细腻冲突”不能成立→refuted; pavilion 被重复译成“营地”→confirmed; doubt 被弱化且被无依据强化为“无尽的困扰”→confirmed; raved 的贬义语境被改成偏褒义的“慷慨激昂”→confirmed; bringing my face close 被漏掉并换成无依据动作→confirmed; bravado 漏译，“平日”无依据→confirmed; 两处敬称均属增译，且彼此不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-033-01.md](reports/sol-033-01.md)。译文未修改。共 17 个 claim：15 confirmed、1 advisory、1 refuted，无 pending。 人工待决：逐项决定改写；refuted/advisory 两项不要写进修复理由。译文未修改。
```
</details>

## entry-01222

- 位置：`mod-tome.lua:15094`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Five: The Day of the Spellblaze#{normal}#

I loosened Mooncutter in its sheath as the troops marched forwards.  My grip tightened on the reins, holding my horse in check lest it gallop ahead in the excitement, and I could see my squire to my left doing the same.  The tension in the air was palpable.  Before us, less than a mile away, the vanguard of the orcish armies was now visible.  We had stirred up their nest and they had responded in full force.  They were like a shadowy blight that swallowed up the horizon, a great pestilence that threatened to consume the world.  Before me the armies of the Shaloren seemed small in comparison, but I knew our strength was not told by mere numbers.

Trumpets blared from the bulwarks at the front, as they readied to engage with the first wave when needed.  To the north were archers to crumble the initial resistance, and at their flank a legion of spellriders, their hands glowing with arcane energies as they sat atop their fearsome steeds.  On the south was the regular cavalry, the greatswords, the armoured knights and the main bulk of our mages, readying support spells.  Here and there senior battlemages were dotted about, ready to move swiftly to points of intense activity and blast it away.  There was no need to have more than one of them in any place - alone they could decimate a score of orcs with ease.

Drums beat loudly in the distance, and a clamour arose from the enemy.  They had with them trained beasts and trolls, and were arrayed in swords and maces and crude armours.  One took up a loud howl and others joined in, and the air seemed to reverberate with their ugly voices.

The cacophony was unsettling, but my army responded with a display of power.  Swords and speartips rose into the air, and crackles of lightning shot up to the heavens, the sparks shining off the gleaming blades and armour.  The orcish army gasped in dismay.  The eastern skyline was beginning to glow red, and we knew the dawn would break any moment now, the signal for the start of the Great Spellblaze.

“The day is here!” one of our warriors shouted out, and it was taken up elsewhere by the marching troops.  “The day is here!” they began to chant, anticipating the glory to come.  “The day is here!” my squire sang, his voice full of youthful joy and hope.  “The day is here!” we all shouted in unison, the pride of the Shaloren kingdom in our hearts as we watched the first rays of sunlight shine out from the horizon.  “The day is here!  The day is here!  The day is-”

Silence.  All at once our voices dropped, and a terrible brooding silence swept over the battlefield.  We could feel it, every one of us, so attuned are our race to the flows of magic.  It was like having the breath sucked from one’s lungs, or the earth disappear from beneath one’s feet.  All our mana channels were gone, changed suddenly, arcane energies beyond all reach.  Groans and murmurs began to arise, as mages clutched at their heads in sudden despair.  I saw my squire lurch forwards in his saddle and begin to vomit uncontrollably, my standard slipping from his hand, whilst others fell to the ground in pain.  I struggled to battle an overwhelming migraine, blotches appearing in front of my eyes, and with great effort of will I managed to keep control of myself and began to seek out new paths of mana.

But there was something wrong, terribly wrong.  Like a river run off its course the flow of magic across the whole of Eyal had changed.  What could have caused this?  And now I had to fight years of attunement and training that had taught me to naturally rely on the known flows and courses so that I might find new paths, new sources.  And as I did so I put my powers into divination, and what I discovered shocked me to my core.

The orcs saw us in disarray and began to charge.  But my attention was turned west, not east, towards Elvala and the Crystal Tower where our leaders had been manipulating the Sher’Tul farportal.  But the tower, I felt, was gone - crumpled into the earth, and from there now emanated a wave of white-hot flame.  The orcs tore into our army with little resistance, their weapons tearing through the elven troops, but they were soon met by a wave of destructive energy far greater.

“Shields!” I shouted out as the whole sky turned redder than blood, but above the sudden deafening roar of roasting air I was not heard.  It would have helped little anyway, defenceless as my army was without their usual sources of mana.  Spears of flame streaked down on our heads, shearing through flesh and steel in an instant and sinking into the earth.  The ground shook, and lava blasted up from the deep holes torn into the rock.

I put an arcane shield about myself with a great effort of will.  I saw my squire raise a hand to do the same, but a blaze tore off his arm.  He didn’t even get to scream before another wave burned through the top half of his torso.  Spurting blood evaporated instantly, and the air became full of red mist and fire.  I leapt from my horse as it neighed and stumbled and fell burning into ash.

Another wave came, and I tried to strengthen my shield, but the force of it took me off my feet and sent me flying.  I was thrashed through the air like a swirling leaf, unable to do anything more than struggle to maintain my protection.  All about my army was being utterly decimated, ranks and ranks of soldiers and mages burnt to a crisp or torn apart by the raw energies.  The orcs were the same, and a huge rent in the ground swallowed great numbers of their troops.  Blasts of lava soon thundered upward and rained down for miles around, turning into glowing rivers of death that swept across the consumed landscape.

How I managed to stay alive I am still not sure.  I almost slipped from consciousness at several points, but by a mental tenacity I never knew I had I managed to stay focused and keep my protective shield active.  I became less aware of my surroundings, not knowing if the bubble of my ward was floating through air or fire or blood, or swallowed into the depths of Eyal into some hell never before witnessed.  At last, after what seemed like a tortuous age, the wave of energy passed, and I found myself lying alone on an outcrop of cracked and parched earth, the air a haze of heat about me.

I struggled to my feet and looked around, seeing nothing but desolation in all directions.  Steam and smoke rose from rents in the ground, and blood, limbs and ashes were strewn about all over.  Nothing was alive.  In a daze I despaired that I was alone of the hundreds of thousands who had stood here but a short while before.  Friends and comrades, mentors and students, people I had never known and ones I was dearly close to - all gone.  A sudden pain lanced my heart as I thought of Linaniil.  She could not be dead, surely?

I gritted my teeth and summoned the energy to levitate, and as I rose I began to get my bearings around the changed landscape.  Slowly I pushed north-east, passing over devastation beyond belief.  I struggled to keep a grip on my sanity as the scent of burnt flesh and blood surrounded me, my vision filled with a horrored landscape beyond imagination, the utter silence more deafening than any sound I had ever heard.  Eventually I came near to where the Kar’Krul army had stood, and cast about the ruined land for some sign of life.  Then faintly I detected something, some small sliver of life, and searching it out I found her.

Her clothes had been mostly burned off, her hair half turned to ash, and blood was seeping freely from burns all across her body.  A weak shield still hummed over her, but as I knelt down and laid a hand on her it vanished.  Quietly she gasped a breath before whispering, “Neira”, and sinking into unconsciousness.  She was still alive, but barely.  I looked about and saw no signs of her sister, or of any of the rest of her troops, other than the scorched flesh and blackened bones that marked the scourging path swept by the blaze.

I began to cast what healing spells I could on Linaniil, but I could tell it was not enough, and my weakened powers could not hope to save her.  I began to cry openly, thinking of all I had lost this day, all that had gone so terribly wrong.  Hope had turned to crisis, and the cruelty of fate was far too much for me to bear.  Cradling my dying love’s head in my lap I turned my face to the sky and screamed.  Torment was in my cracked voice, and I raged against all the injustice of life and the futility of war, surrounded on all sides by blood and bones and ashes.  They had once been souls and lives with hopes and dreams, now all cast away like dust in the wind, and I lamented their deaths and my despair.

But mine was just one voice, one torment, a single note in the great cacophony that spread across the continent.  Millions of lives lost and shattered, millions of voices raised in anguish and torture and suffering, as the devastation continued over all Maj’Eyal from the ultimate force of destruction, the Spellblaze.`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第五章：魔法大爆炸之日#{normal}#

随着军队向前前进，我的斩月剑也将出鞘。我的手中握紧缰绳，以免我的战马因为过于兴奋而向前奔驰，我一旁的侍从也握紧缰绳，神情严肃。空气中弥漫着紧张的气氛。放眼向前望去，在不到一英里的地方，兽人军队的前锋已经清晰可见。我们惊动了他们的巢穴，他们便倾巢而出。他们庞大的军势，宛如一道枯萎的暗影，正在缓缓吞噬着地平线下的一切。他们就像一场滔天瘟疫，眼看就要将这个世界吞噬殆尽。在我们前方的永恒精灵军队在他们庞大的军力面前看起来是那么渺小，但我知道我们的力量可不是由数量决定的。

最前方的防线吹响了号角，准备在需要时迎击第一波冲锋。战场北方部署着弓箭手，负责粉碎敌军最初的抵抗；侧翼则是一支法术骑手军团，他们骑在可怖的坐骑上，双手闪耀着奥术能量。南方是常规骑兵、双手剑士、重甲骑士和法师主力，正在准备支援法术。战场各处还散布着资深的战斗法师，随时准备迅速赶往战况最激烈之处，用强大的魔法荡平敌军。任何地方都无需部署两人——他们孤身一人便能轻易消灭二十个兽人。

战鼓在远方震天作响，敌阵中鼓噪声四起。他们带着受训的野兽与巨魔，兽人们手持刀剑和钉头锤，身披粗制铠甲。其中一个兽人扯开嗓子长嚎，其他兽人也随之附和，空气似乎因那丑陋的声音而震颤。

他们的战吼令人不安，但我们的军队迅速用我们的方式用力量对他们的挑衅进行了回应。他们高举手中的长剑和长矛，剑尖与矛尖迸发出噼啪作响的闪电，直冲天际，火花映亮闪耀的剑刃与铠甲。兽人大军惊恐地倒吸一口凉气。东方天际开始泛红；我们知道黎明即将到来，那就是伟大的魔法大爆炸开始的信号。

“就是今天！”我们的一个战士发出了呐喊，很快，周围的士兵也重复了他的呐喊。“就是今天！”，他们开始吟唱，期待着即将到来的荣耀。“就是今天！”，我的侍从开始歌唱，他的声音充满了年轻的喜悦和希望。“就是今天！”我们合力发出喊声，随着黎明的第一丝曙光从地面升起，永恒精灵王国的荣耀在我们的心头闪耀。“就是今天！就是今天！就是今——”

沉默。突然间，周围一片万籁俱寂，可怕的沉寂仿佛突然间席卷了整个战场。因为我们的种族和魔法天然的联系，我们所有人都在那一瞬间感受到了那种可怕的体验。那就像是一瞬间体验自己的呼吸被一下子掐断的窒息感，或是脚下站立的大地一瞬间被抽走一般的无助。在那一瞬间，我们的法力通道突然间消失了，奥术能量一下子从我们的手边远去。随着人群的呻吟和低语，一旁的法师们在无尽的绝望中抱紧了自己的头。我看到我的侍从在他的马鞍上摇摇欲坠，无法控制地呕吐起来，我的军旗也从他的手中滑落。其他人纷纷倒在地上，在剧痛中挣扎。我用尽意志强忍着排山倒海般的偏头痛，视野中只剩下一块块模糊不清的景象。我试图控制自己，寻找新的法力通道。

但是，一定有什么东西出错了，那是多么可怕的错误。整个埃亚尔的魔法流动突然发生了巨大的变化，就像河流突然偏离了自己的河道一样荒谬。现在，我不得不和我经受多年的魔法训练所抗争。我过去已知依赖着那些已知的魔法流动，然而现在我却必须奋力寻找新的能量源。我用尽全力，把自己仅存的力量试图用于启动侦查系魔法，在那一刻，我发现的一切让我深深感到震惊。

兽人看到我们混乱不堪的样子，下令全军突击。然而我的注意力很快从兽人所在的东面转移到了西面，试图望向埃尔瓦拉和我们的领袖用来操纵夏·图尔传送门的水晶塔。然而，我感觉水晶塔已经消失——它向内坍缩、碎入大地，一股白热的火焰浪潮正从那里扩散开来。兽人几乎没有遇到抵抗便杀入我们的军队，武器撕裂精灵兵士，但他们很快便遭遇了远为强大的毁灭性能量浪潮。

那一刻，天空化为了鲜血般的炽红。“打开护盾！”我试图大喊出声，然而灼热空气的震耳轰鸣迅速盖过了我的声音。当然，即使我能喊出声来也没有多少意义，因为我的军队失去了惯常的魔力来源，几乎毫无防备。烈焰长矛从天而降，瞬间贯穿血肉与钢铁，深深没入大地。地面剧烈震动，岩浆从岩层中被撕开的深孔里喷涌而出。

我竭尽意志，在身周撑起一道奥术护盾。我的侍从也伸出手试图照做，然而一道烈焰瞬间夺走了他的手臂。在他来得及惨叫之前，另一股火浪便烧穿了他的上半身。喷涌的鲜血顷刻蒸发，空气中只剩红雾与烈火。战马嘶鸣着踉跄倒下，在烈焰中化作灰烬；我纵身跃离马背。

又一股冲击波袭来，我试图强化我的护盾，然而这股力量太过强大，直接将我从地上连根拔起，掀飞出去。我被冲击波掀到空中，仿佛暴风中的一片树叶，只能在灾难中颤抖着试图保全自己。我们的军队在那一瞬间被彻底毁灭，无数士兵和法师被强大的能量烧成灰烬，撕成碎片。兽人的命运也是同样悲惨，大地的裂变将他们的军队吞噬，掉入无尽深渊。岩浆随即轰鸣着冲天而起，又如雨般洒落方圆数英里，化作一条条炽亮的死亡河流，横扫已被吞没的大地。

我不知道，我是怎么在这样恐怖的灾难中幸存的。巨大的冲击力无数次让我几乎失去意识，然而不知是什么样的韧性让我坚持集中注意力，不让自己的防护盾被攻击打破。灾难的景象渐渐在视野中变得模糊，我不知道包裹我的这个小小泡泡是否仍然在这片充满火与血的空气中浮动，还是已经坠入了撕裂的大地中无人知晓的无尽深渊。在经过了对我来说如同一个世纪一样漫长的痛苦折磨之后，一阵阵的冲击波终于停止了。我发现我独自躺在一片被撕裂烧灼的大地上，空气中弥漫着酷热。

我挣扎着站起来，环顾四周，只看到四面八方的荒凉景象。蒸汽和烟雾从地面的裂缝中涌出，四周只剩下散落的血肉，残肢和灰烬。周围没有看到任何一个幸存者。在一瞬间的茫然中，我很快感受到了那份绝望：不久前站在这里的数十万人中，只剩下我一个幸存者。无论是朋友还是战友，无论是导师还是学生，无论是我从未认识的人还是我曾经非常接近的人——一切都逝去了。当我想到莱娜尼尔的时候，一股剧烈的痛苦刺穿了我的心房。她是不会死的，对吧？

我咬紧牙关，召唤了用于悬浮的能量，随着我的身体慢慢升起，周围被摧残的万物景象慢慢进入我的眼中。我慢慢地向东北方向前进，四周尽是满目疮痍。四周焚烧的血肉的气息环绕着我，我竭尽全力试图抓住仅存的一丝理智，然而周围尽是超越我的想象的恐怖景象，废土中无尽的寂静比我听到的最为震耳欲聋的声音更加摧残着我的精神。最终，我找到了卡库罗尔军队曾经驻守的地方仅存的遗迹，在无尽的废土中，我试图寻找仅存的生命的迹象。最终，我发现了一些微弱的信号，那是多么微弱的一丝生命，顺着那个线索，我最终找到了她。

她的衣服几乎全部被烧毁，她的长发一半被烧成了灰烬，鲜血在她身上无数的创口缓缓向外流淌。她的身上还残留着微弱的护盾能量，然而当我跪下，把手放在她身上的时候，那个护盾就消失了。她微弱地呼吸着，呢喃着“尼耶拉”的声音，然后很快陷入了无意识之中。她还活着，但是已经奄奄一息。我向四周望去，没有任何她的孪生姐妹的迹象，也没有任何卡库罗尔的士兵。四周只剩下烧焦的血肉和骨骼化成的焦炭，昭示着魔法大爆炸带来的毁灭。

我开始在莱娜尼尔身上释放我所有的治疗魔法，但是我知道这些都远远不够，我的能力几乎全失，根本不可能有拯救她的希望。想到发生的这一切恐怖的遭遇，想到在这一瞬间我失去了我曾经拥有的一切，我开始放声痛哭。我们的希望瞬间变成了毁灭，命运的残酷让我无法承受。抱着我正在死去的爱人的脸庞，我向着天空发出怒吼。呜咽着嘶哑的嗓音，周围只剩下血肉、白骨和尘埃，我对命运的不公和这场战争的毫无意义发出绝望的咆哮。在那一瞬间，无数有着自己希望和梦想的灵魂，在顷刻间化为了风中的尘埃，他们无意义的痛苦和死亡在我的心头只留下无尽的绝望。

但是，相比之下，我的痛苦只是传遍整个大陆的无尽的苦痛中多么微小的一个而已。在那一刻，数以百万的生命毁灭破碎，数以百万的人在痛苦和折磨中发出绝望的怒吼。在那一刻，终极的毁灭力量带来的无尽灾厄将会继续在马基·埃亚尔蔓延。这，就是魔法大爆炸。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00158 | HUMAN-REVIEW | cross-batch-035 | confirmed | confirmed：格式与控制字符无问题；confirmed：“我过去已知依赖着”错别字（已知/一直）；confirmed：两处 `！”`，` 冗余标点；confirmed：`head in my lap` 译成“抱着……脸庞”；confirmed：`crisis` 译“毁灭”并加“瞬间”；confirmed：`burns` 泛化成“创口”；confirmed：末段声音/音符隐喻被抹平；confirmed：`bulwarks` 译“防线”；confirmed：“用我们的方式用力量……”句式套叠；confirmed：瞬时模板词高频重复。refuted：`seeping freely` 被“反向… |  | fix |

<details><summary>hrq-00158 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 格式与控制字符配对无问题→confirmed; “我过去已知依赖着”错别字（已知/一直）→confirmed; 两处 `！”`，` 冗余标点→confirmed; `head in my lap` 译成“抱着……脸庞”→confirmed; `crisis` 译成“毁灭”并添加“瞬间”→confirmed; `burns` 泛化成“创口”→confirmed; `seeping freely` 被“反向表达”→refuted; 该处仍有轻微信息损失→advisory; 末段声音／音符隐喻被抹平→confirmed; `Kar’Krul` 与“卡·克鲁尔”跨文本不一致→pending; `bulwarks` 译为“防线”→confirmed; “用我们的方式用力量……”句式套叠→confirmed; 瞬时模板词高频重复→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-034-01.md](reports/sol-034-01.md)。译文未修改。共 13 个 claim：10 confirmed、1 refuted、1 advisory、1 pending。 人工待决：术语类 pending 需主代理按术语库核对后才能升级；refuted 项不进修复理由。译文未修改。
```
</details>

## entry-01223

- 位置：`mod-tome.lua:15168`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Six: A Changed Eyal#{normal}#

Perhaps what happened will never be truly understood.  What Sher’Tul ruins survived the Spellblaze have been little touched since - the burned hand learns its lesson.  But we know that Ephinias and his mages lost control somehow, whatever delicacy and balance they wrought with coming untangled.  At the moment they tried to connect to the other farportals the imbalance was reverberated, resonated, magnified beyond control.  The farportal in the Crystal Tower imploded in a fraction of a second, killing all within and crushing the land about.  The energies in the Sher’Tul relics then erupted in a blaze of white light, turning the air to fire and the ground to ruin.  The blaze swept eastwards, rolling over our battle with an unstoppable destructive force, and then carrying on towards the Thaloren lands.  Most of the ancient forests of Shatur were ripped from their roots, and the lands lain cursed ever since.

Meanwhile the other farportals all over Maj’Eyal erupted, white stone cracking and vast swathes of energy spilling forth.  All of the Cornac lands to the west were turned to desert, the dwarven halls of Korhek crumpled, the midvale plains were risen up as mountains and Lake Nur formed in their wake.  In the south the ancient tower of Darafel was collapsed, and the forests beside it morphed into an ever-broiling scar of lava and blackened earth.  Far in the east the Naloren farportal, the largest of all in Maj’Eyal, disappeared in a vast earthquake that swallowed everything for miles around, and boiling water spewed up to fill its cavernous depths.

And whilst this destruction was wrought the incredible energies disrupted all of the mana flow around Eyal.  Streams of energy that followed set, slowly changing courses, now were flooded and droughted, warped and split.  The threads of the elements were in vast disarray, and any attuned to magic suddenly found themselves far away from their accustomed power sources.

Even the Heavens were changed.  The wandering star of Vor disappeared, the constellations were tilted off their normal course, and the seasons rent harsher since.  Some say the moons dimmed and the sun went whiter after that day.  I do not know.  The whole world has seemed darker to me.

The numbers killed are beyond count.  The initial destruction took at least five million lives, and the terror that followed claimed far more.  For though it had been a day of tragedy and immeasurable woe, it was to be followed by a bloody age of darkness and torment.

But none of this I knew as I lay weeping in the aftermath, cradling in my lap the one life I cared about.  In abject misery I called on all the healing powers I could to bring her back to me for but one moment.  Her heart beat softly, and her eyes opened, but seemed glassy and far away.

“Linaniil,” I whispered, and her dark eyes turned towards my face.  I tried to mumble an apology, to say I was sorry and was unable to help her, but emotions overcame my voice.  Her gaze at me was empty, as if she looked right through me, before she turned her eyes away.  Slowly she raised a hand to an amulet about her neck, and with a light touch it glowed and then cracked.  Her eyes closed again but I could feel the power from the artifact pumping into her, strengthening her heart-beat and mending her flesh.  She was unconscious and still badly wounded, but for now the mortal threat was gone.

My thoughts were mixed - glad she was no longer at death’s door, but worried she might relapse, and at the back of my mind scared of that empty look she had given me.  Could she possibly forgive my part in this?

Carefully I picked up her frail body, and began the journey back to Elvala.  Two days it took on foot, through blasted and ruined ground.  On the passage I came across other survivors, refugees now leaving their destroyed homes, heading to the city to seek shelter.  I tried to nurse Linaniil as best I could, giving her water during brief periods of waking and dressing her wounds, but true healing could not happen till I reached the city.

Elvala was a quiet chaos, oppressed by fear and uncertainty, an air of dread filling all the streets.  The news had broken that our army had been entirely wiped out - there would be no loved ones returning to their families, and the sound of stifled mourning was to be heard in all corners of the city.

I took Linaniil straight to the healing grounds in the palace and gave her to the doctors with the strictest instructions.  They were swamped by casualties, but followed my orders without question, tending immediately to her wounds and applying tinctures and regenerative spells.

It was as I watched over her quietly that a party bustled loudly into the grounds.  I recognised at their head was Perissa, a senior court official.  At her side was an elderly human who immediately went to where Linaniil lay.

“General Aranion!” announced Perissa loudly, “I heard you were here, but I could scarce believe it.  Thank the threads you have returned to us!  This is a grave time; we must talk at once.”

But I ignored her as I saw the human touch Linaniil’s hand, and her eyes gently open.  “Cuilan?” she murmured softly.

“Aye, it is me, my lady,” he said quietly.  “I have been sent here by your father.  He has ordered me to pass you this.”  And with that he brought forth a golden ring set with a fiery ruby.  I recognised it immediately as the Ring of Kar’Krul, worn by the mighty Turthel.  Linaniil sat up quickly, wincing from the pain, but with her eyes locked on the ring as it was placed in her hand.

“But mine father...”

“I’m sorry, my lady.  It brings me great sorrow to bear you this news.  Your father and his court are dead.  His last act was to instruct me to bring this ring to you and your sister.  Neira...” he said glancing about.  “Is she...?”  He saw the look in Linaniil’s eyes and dipped his head despondently.  “I see.  I am terribly sorry.  It becomes my duty then, my lady, to declare you the new leader of the Kar’Krul.”

“General Aranion,” interjected Perissa.  “I really must speak with you now!”

“Wait!” I barked, and turned to the human Cuilan.  “What is happening here?  How could one such as Turthel be killed?”

The man looked at me then with a wan sadness in his eyes, before turning to address Linaniil.  “Yesterday, the day after the terrible Spellblaze, as we began some attempt at reconstruction, still struggling to realign our mana paths, a murmur began amongst the people.  It spoke thus: The Kar’Krul circle of mages had betrayed the ordinary people.  They accused us of siding with the elves to destroy non-mages, of toying with terrible powers beyond our control, of deliberately massacring them out of evil and malice.  We could not logic with them, they would listen to no reason, and they rose up in violent anger.  They attacked many of us, with farming instruments and whatever weapons they could find.  Our defences were weak, and striking back just made the crowd fiercer.  We retreated to your father’s home, begging for help, but he shook his head and said he could not fight back.  They came for us then, storming his palace, and Turthel ordered all to put up no resistance.  He handed me his ring, saying to seek you out in Elvala, and then stepped outside to face the crowds.  He didn’t resist!  The people... they... they...”  He lapsed into sullen silence, shaking his head in sorrow.  He looked like he wanted to cry, but had no tears left to shed.  Linaniil’s face was graven and she stared hard at the ring.

Perissa grabbed me then and turned me to her attention.  “This is what I need to speak with you about, General Aranion.  If this human’s tale is to be believed then we are in very grave danger!  Scout reports suggest there is a body of humans coming here from the north as we speak.  From what this human says they seek retribution - they wish to slaughter us all.  A storm of wrath lies on our borders and we are defenseless!  We need you desperately to organise our defence, to protect our city and our people.”

I felt numb, the events overwhelming me.  “But who leads us?” I said.

“There is no one.  What royals are known to be alive are not suited.  We are entering a time of war, a terrible time like no other we have ever faced.  We need military leadership.  You, General Aranion, you must be our leader.”

I held Perissa’s gaze then and saw the wisdom in her words.  My duty as a Shaloren was clear.  But my heart tremored as I turned to look at Linaniil.

“This be our path then, Aranion,” she said quietly, raising herself from the bed and carefully placing the ring on the middle finger of her right hand.  “I must tend to mine people, and ye to yours.  We will not meet again.”

“But your wounds-” I tried to object.

“Will never heal!” she cried, hate dripping from her voice.  Her eyes were like cold and impenetrable ice, a smouldering anger deep within.  “Come, Cuilan, we must leave this place.”  And with that they departed, Linaniil walking tall and proud in spite of her injuries.

I closed off my heart and my emotions then, lest they overwhelm me.  My duty was before me, and the events of the past had to be locked away from memory.

The ceremony was organised in under an hour, and I was anointed leader of the Grand Council of Elvala, head of the Shaloren people.  On my order rangers began transporting in survivors from outpost settlements, whilst I commanded our remaining mages to begin a new endeavour around our city walls.

The first waves of the storm of hate came the next day.  Human peasants and farmers, ordinary workers armed poorly, their looted swords and spears badly wielded.  I stood alone at our gates as they approached, Mooncutter in my hand.  When the first few charged at me I thrust the blade into the soil and tore a great chasm in the earth, and our mages summoned forth mists and smoke that rose from the ground and began to surround our whole city.  As the peasants stumbled in confusion archers started firing from our walls.  What few made it through the smoke and arrows I took on, tearing Mooncutter through their flesh with little resistance.  Their blood gushed out in the gallons, drenching our ground, staining my skin.  It was like a warm shower over my boiling emotions, a bath of blood to wash over my sins.

The Shroud of Elvala was begun, as our whole city was wreathed in cloud and smoke.  Our shield, our mask, our hiding.  It would last for centuries, the only dealings with the outside world being in furtive secrecy.
`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第六章：被改变的埃亚尔#{normal}#

或许，我们永远不会知道当天到底发生了什么。魔法大爆炸后幸存下来的夏·图尔遗迹，自此几乎无人敢碰——这一教训对人们来说已经足够深刻了。我们唯一知道的是，不管伊菲尼亚斯曾经拥有多么精妙和平衡的控制，在那一刻，他们失控了。在他们连接到其他传送门的一瞬间，微小的不平衡迅速被回响，共振，放大，瞬间失去了控制。在不到一秒钟的时间里，水晶塔中的远行传送门向内坍缩，杀死了其中所有人，并压垮四周的大地。随后，夏·图尔遗迹中的能量化作耀眼白光爆发，将空气化为火焰，将大地化为废墟。大火迅速向东袭来，用它势不可挡的毁灭力量将我们战场上的一切全部摧毁，然后直接席卷向自然精灵的领地。夏特尔的远古森林纷纷被连根拔起，从此，那片大地被永远诅咒。

同时，在马基·埃亚尔的其他远行传送门都纷纷爆发，磐石也被其撕裂，大量的能量向外涌出。西部科纳克人王国的土地迅速化为了沙漠，矮人大厅科尔赫克倒塌了，中部的平原隆起成为山脉，中间形成了纳尔湖。在南部，远古高塔德拉斐尔倒塌了，周围的森林化为被永远灼热的岩浆和黑石覆盖的焦土。在遥远的东方，纳鲁精灵所拥有的，整个马基·埃亚尔最大的传送门，被一场剧烈的地震所吞噬。剧烈的地震吞噬了周围数英里内的一切，沸水喷涌而出，填满了地震留下的巨大空腔。

当这场毁灭发生时，惊人的能量扰乱了环绕埃亚尔的所有法力流动。能量的流动曾经遵循相对固定、缓慢变化的路线，如今却忽而洪泛，忽而枯竭，被扭曲、被分裂。元素脉络陷入极度混乱，任何与魔法调谐的人都突然发现，自己已远离惯用的力量之源。

就连苍穹也发生了变化。在星间漫游的沃尔之星消失了，星座也偏离了他们正常的轨道，季节变化变得远比以前更为极端。有人说，从那以后，月亮变得更暗，而太阳也变得更白。我不知道这些。在我眼里，整个世界从那一刻起都变得黯淡了。

这一切的受难者数不胜数。最初的破坏至少夺走了五百万人的生命，而随后的恐怖事件则造成了更大的毁灭。因为，这不仅是悲剧和无尽灾厄的一天，而且还带来了一个充满黑暗和折磨的血腥时代。

然而，在我在灾难之中抱着我生命中最重视的人的身体，放声痛哭的一刻，我还不知道之后所发生的那些无尽的困难。在无尽的痛苦中，我试图使用我所有的治疗力量，试图能够挽回她的生命，哪怕只是延长她一秒钟的时间。她的心跳微弱，睁开的双眸如玻璃一样，离我的距离仿佛在两个世界一样那么遥远。

“莱娜尼尔，”我轻声低语，她黑色的眼睛转向我的脸庞。我试图呢喃着说出我的道歉，试图说出我无法拯救她的痛苦，但我实在是没有办法说出口。她望向我的目光空灵无物，仿佛穿透了我的身体，然后慢慢转向了另一个地方。她的手中慢慢拿起了她脖子上的一串吊坠，在那一瞬间，吊坠发出了一束光芒，然后碎裂了。她的眼睛再一次闭上，但我能感受到，她刚刚拿着的神器的力量已经灌注进了她的身体里，修复着她的肉体，她的心跳也不再那么微弱。她仍然处在无意识中，仍然身受重伤。然而现在，致命的威胁已经消失了。

我的心中百感交集——我为她逃离死神的拥抱感到欣喜，但又对她的虚弱状态感到担忧。而且，她刚才看向我时空洞的眼神让我心如刀割。她会原谅我在这场灾难中扮演的角色吗？

我小心地抱起她脆弱的身躯，慢慢走向返回埃尔瓦拉的路。在灼烧的废土之上，我走了两天的时间。在路上，我能看到其他的幸存者，他们是逃离自己被摧毁的家园的灾民，正在试图在城市里找到避难所。我试图尽我所能护理莱娜尼尔，不断给她水，处理着她的伤口，但只有我到达城市的时候才能找到真正的治疗师。

埃尔瓦拉处在一片寂静的混乱之中，人们被不确定性和恐怖所压倒，每一条街道都弥漫着恐惧的气息。有关我们的军队全军覆灭的消息已经传了开来——他们的家人再也没法看到自己的亲人回到家园，城市的每一个角落里都充满了令人窒息的痛苦哀悼。

我把莱娜尼尔带到了王宫的医院，让最好的治疗师给她治疗。医院里现在已经满是受伤的灾民，他们对我的指令没有半点疑虑，立刻使用药剂和治疗性的法术处理了她的伤口。

正当我静静地看着她时，一群人吵吵嚷嚷地冲了进来。我认出他们的头领是佩里萨，王廷中的高级官员。在她身边的是一位年长的人类，他立即走向莱娜尼尔躺在的地方。

“艾伦尼恩将军！”佩里萨大喊道，“我听说你在这里，真是难以置信。感谢命运之线！现在是严峻的时刻，我们必须马上谈谈。”

但我没有理她，我看到那个人类轻碰了莱娜尼尔的手，她的眼睛缓缓张开。“崔岚？”她低声呢喃道。

“嗯，是我，小姐”，他轻声说道。“我是奉你父亲之命来到这里的。他命我把这个交给你。”他的手中拿出了一枚纯金的戒指，上面镶嵌着火焰般的红宝石。我一下子认了出来，正是强大的特塞尔所佩戴的卡库罗尔之戒。莱娜尼尔一下子坐了起来，似乎仍然在痛苦中挣扎，但她的眼睛紧盯着她手中的那枚戒指。

“但是，我父亲…”

“我很抱歉，小姐。向您传达这个消息实在是让人无比悲痛。你的父亲和他王廷里所有的人都已经去世了。他给我最后的指令就是让我把这枚戒指带给你和你的孪生姐妹。尼耶拉……”，他向周围看去。“她…？”他看到了莱娜尼尔的目光，失落的慢慢低下头。“我明白了。我真的十分抱歉。那么，我有责任宣布这件事。小姐，我要宣布，你现在就是卡库罗尔的新领袖。”

“艾伦尼恩将军！”佩里萨打断了他的发言，“我真的必须马上和你谈谈！”

“等等！”，我怒吼起来，转向崔岚。“到底发生了什么？特塞尔这么强大的人怎么可能被杀？”

那个男人看向我，眼中充满了无尽的悲伤，然后又重新看向莱娜尼尔。“昨天，也就是可怕的魔法大爆炸之后的一天。我们本来准备开始重建工作，大部分人还在调整自己的法力通道的。然而，在人群中出现了一种谣言。他们说：卡库罗尔的法师们背叛了普通人。他们指责我们和永恒精灵合谋，想要操纵超越想象的可怕力量，故意展开这种邪恶恐怖的屠杀，试图清除所有不是法师的人。我们无法说服他们，他们什么也不肯相信，愤怒地开始了暴动。他们使用农具或者他们能够找到的任何东西攻击我们。我们根本没有能力保护自己，试图反击只是让人群变得更加愤怒。我们撤退到你父亲的宫廷，请求他帮助我们，但是他摇了摇头，说他绝不会伤害自己的人民。那些人跟随我们，冲进了特塞尔的宫殿，但是特塞尔命令我们放弃抵抗。他把他的戒指交给了我，然后一个人走了出去，直面了外面的人群。他根本没有抵抗！那些人……他们……他们……”，他悲伤地陷入沉默，痛苦地摇着头。他仿佛看上去想要痛哭失声，但是已经失去了眼泪。莱娜尼尔面如死灰，用凝重的眼神注视着那枚戒指。

佩里萨抓住我，强制把我的脸转向她的方向。“这就是我要跟你说的事情，艾伦尼恩将军。如果有关人类的事情是真的话，那么我们现在已经处在非常危险的境地了！在我们说话的时候，就有哨兵向我们报告，一群人类正在从北方向我们这边过来。那些人类说他们要寻求复仇——他们要杀光我们！现在，我们的国境已经被愤怒的浪潮所包围，而我们已经毫无防备，孤立无援！我们需要你组织我们的防御，我们要保护我们的城市和我们的人民。”

我仍然处于麻木的状态，这一连串的事件把我吓倒了。“但是谁来领导我们？”我问道。

“没有人。即使还有王族还活着，他们也不适合现在的状况。我们现在已经进入了战争的时代，这是我们中间的任何人都没有经历过的可怕的时代。我们需要军人来领导这一切。你，艾伦尼恩将军，你必须成为我们的领袖。”

我迎上佩里萨的目光，领会到了她话语中的智慧。我作为一个永恒精灵的责任已经很清楚了。但当我看向莱娜尼尔的时候，我的心还是忍不住颤抖。

“这就是我们的道路，艾伦尼恩”，她静静地说着，从床上爬了起来，小心翼翼在右手中指上戴上了那枚戒指。“我必须领导我的人民，而你需要领导你的人民。我们永远不会再相见了。”

“但是你的伤口——”我试图反对

“那份伤痛永远不会痊愈！”她怒吼着，话语中透露着恨意。她的眼神像一块冰，无法穿透的冰，那是一份内心深处深藏的愤怒。“来吧，崔岚，我们必须离开这个地方。”。然后，他们离开了。莱娜尼尔尽管还受着伤，仍然高傲地走着。

我封闭了我的心房，压制了我的感情。我不能让这些感情压倒我的责任。我还有我必须要做的事情，过去发生的一切都将永远在记忆中被封存。

继位仪式在一小时以内就开始了。我受膏成为埃尔瓦拉最高议会的领导，永恒精灵人民的领袖。在我的指挥下，我们的游侠开始从周围的哨站和定居点撤离幸存者，而我命令剩下的法师围绕我们的城墙开始新的努力。

第一波仇恨的浪潮在第二天就席卷而来。人类的农民和工人组成了这群人，装备简陋，笨拙地挥舞着掠来的刀剑和长矛。我独自一人站在城门外，手持斩月剑，迎向他们。当他们冲向我的时候，我将长剑插入大地，在大地上撕开一道裂痕。我们的法师迅速让一层层重叠浓厚的迷雾从地面上升起，环绕了我们的整个城市。当那些农民陷入混乱的时候。弓箭手们开始从城墙上向下射击。只有几个人能够躲过烟雾和箭雨的夹击，我的斩月剑可以十分轻松地穿透那些仅存的人的血肉。他们的鲜血从身体中喷出，渗透了周围的大地，沾染了我的身体。我心头沸腾的感情沐浴在鲜血之中，那是我所犯下的罪恶的血雨。

埃尔瓦拉的帷幕升起了，整座城市被迷雾所覆盖。这是我们的盾牌，我们的面纱，我们的藏身之所。这持续了几个世纪，在此期间和外界的一切交易都被严格守秘。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00159 | HUMAN-REVIEW | cross-batch-036 | confirmed | confirmed：格式控制符与段落结构；confirmed：`this human` 指代被译错；confirmed：`none of this I knew` 时间指代错；confirmed：`saying to seek you out in Elvala` 漏译；confirmed：`I took on` 漏掉主动接战；confirmed：第 28 段漏句末标点；confirmed：第 29 段重叠标点；confirmed：第 32 段从句被句号截断；confirmed：第 22 段时间状语断裂；confirmed：`relapse` 弱化为“虚弱状态”；confirmed：`sca… |  | fix |

<details><summary>hrq-00159 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 格式控制符及段落结构→confirmed; `this human` 的指代被译错→confirmed; `none of this I knew` 的时间指代→confirmed; `saying to seek you out in Elvala` 漏译→confirmed; `I took on` 漏掉主动接战→confirmed; 第 28 段漏句末标点→confirmed; 第 29 段重叠标点→confirmed; 第 32 段从句被句号截断→confirmed; 第 22 段时间状语断裂→confirmed; `relapse` 被弱化为“虚弱状态”→confirmed; `scared of that empty look` 被译成“心如刀割”→confirmed; `empty` 译为“空灵无物”→confirmed; `white stone` 译为“磐石”→confirmed; `dealings with the outside world` 译为“交易”→confirmed; “白石是所有夏·图尔遗迹的普遍标志性材质”这一广义设定主张→pending; Gemini 称寻人遗命为“关键情节枢纽”略有夸大→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-035-01.md](reports/sol-035-01.md)。译文未修改。共 16 个 claim：14 confirmed、1 pending、1 advisory，无 refuted。Sol 总评：Gemini 的核心事实疑点大多成立，`this human` 指代倒错与 `none of this` 时间倒错最明确。 人工待决：两处“关键情节遗漏”按 Sol 的收窄意见评估影响，不按完全丢失情节计。译文未修改。
```
</details>

## entry-01224

- 位置：`mod-tome.lua:15300`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Seven: Into Darkness#{normal}#

We veiled our guilt, cloaked our crimes.  Though we had some communication with the outside through halfling traders and the odd disguised Shaloren adventurer, we remained mute to the world at large, hidden from their accusing gaze.  Outside our quiet walls others had not the luxury of hiding.  The Spellhunt was begun, and it knew no mercy.

Ordinary people rose up against what they perceived as the arrogance of the mages, a revolt against the power of the few that had ruined the lives of so many.  Any suspected of sorcery or ties to the Art were cruelly dealt with.  There was sympathy for none, and many innocents fell victim to the unquenchable thirst for retribution.  The madness swept across the whole of Maj’Eyal.

Law and order had broken down.  Armies, territories and whole cities had been destroyed or ravaged by the Spellblaze, with many areas left completely uninhabitable.  Kingdoms fell and tyrants arose.  Bandits picked at the bones of civilisation like vultures on a rotten corpse.

An organisation called the Ziguranth, thought dead long ago, came into resurgence, gaining popular support from the people in their anti-magic crusade.  We heard of some mages going into hiding, but inevitably being rooted out, or fleeing desperately from place to place.  Dark tales also arose of necromancers and fell wizards creating dungeons and strongholds, fending off or evading attacks, and beginning reigns of terror.

And one tale came to my ears of a group of mages that managed to band together and stay in hiding, though always on the run from the chasing Ziguranth.  The story from outside was that they were led by a demon with fiery hair, fiercely glowing eyes and hands wrapped in flames, that fought with blazing wrath and could be opposed by none.  I knew that description well...

I carried out my reign, my duty, taking care of the Shaloren people.  We were safe from attackers, secure in our supplies through discrete trade, and slowly building back some of what we had lost.  But both fear and shame prevented us from showing our face to the world.

Fifteen long years passed before I awoke one night in my council chambers, the crescent Wintertide moon softly illuminating a shape near the end of my bed.  The figure was tall and slim, wrapped in tight-fitting wools and furs.  Her crimson hair stirred gently as she stood with her back to me.  Memories arose of a night long ago, in a more innocent time, when a younger me and a younger her first became close.

I barely dared to whisper her name, afraid that she might disappear, an apparition or a dream that could be broken by a spoken word.  “Linaniil,” I softly mouthed.  She turned to me, and I saw those same dark eyes I remembered.  But they were surrounded by lines of care, the markings of years of strain and responsibility clear on her face.

Rising from my bed I gathered a robe about me.  I took a few steps towards her but stopped, not able to move myself any further.  I wanted to be near her, to put my arms around her, but it felt as if she were across a wide chasm from me, a gulf of time and pain between us.

“I have come for help, Aranion,” she said in a low voice, not quite meeting my gaze.  “There be something I seek, and ye must aid me in achieving it.”  I did not understand, but I nodded my assent.  “Get ye dressed and ready then.  There be a long journey ahead of us.”

She stepped towards the window, her back towards me again, waiting as I put on a stralite mail and gathered my sword.  When she noticed I was ready she levitated out, and I followed.

We whistled through the air, travelling northwards at great speed.  The lands swept beneath us, and the climate grew colder as we went further and further north.  Hours passed in intrepid silence, till we were flying above snowy tundra.  We soared past plains of white and grey before we reached a low range of hills.  Here Linaniil slowed and descended, and I went down beside her.  We came to rest before a dark opening at the foot of the hills.

Linaniil stood for a while staring at the black cave.  Fear radiated from her face, but her eyes were hard and determined.  “It is here,” she said quietly, her voice steady.  I followed her gaze, trying to guess what secrets this remote place contained, but I could sense nothing special.

She marched forwards and I followed, until we came right up to the shadowed opening.  Linaniil hesitated a moment, staring into the blackness, before finally stepping inside and being swallowed from sight.  I could feel it then, the sensation that something ancient lay in this place.  My skin tingled and my arcane attunement felt on fire.  This dark cave held some mysterious force, secluded from all knowledge since the oldest days of Eyal.  There was something here that could change the destiny of the world.

I took a deep breath and stepped forwards.`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第七章：进入黑暗#{normal}#

我们掩藏了自己的罪恶，遮蔽了自己的罪行。虽然我们通过半身人商人和偶尔乔装出行的永恒精灵冒险者与外界保持着些许联系，但面对整个世界，我们依旧沉默，躲在他们谴责的目光之外。可在我们寂静的城墙之外，其他人没有这份藏身的奢侈。魔法狩猎开始了，并且毫无怜悯。

普通人站了起来，反抗那些他们眼中傲慢的法师，反抗那少数人的力量——正是这种力量毁掉了无数人的生活。任何被怀疑通晓巫术或与奥术有牵连的人都会被残酷对待。他们不同情任何人，许多无辜者都变成了这场不可抑制的报复欲望的受害者。疯狂席卷了整个马基·埃亚尔。

法律和秩序已经完全崩溃。魔法大爆炸带来的灾难肆虐摧毁了无数的军队，领土和城市，许多土地都变得完全无法居住。王国倒台，暴君取而代之。强盗们如同腐烂尸体上的秃鹫，在文明的废墟上四处横行霸道。

一个名为伊格兰斯、外界以为早已消亡的组织，突然重新兴起。他们在民众反对魔法的狂热中获得了广泛的支持。我听说，有些法师躲藏了起来，但终究难免被揪出来，或是拼命地不断东躲西藏。还有另一些黑暗的故事，那些死灵法师和堕落的巫师为了抵抗或躲避攻击，修筑了地牢和堡垒，开始了恐怖的统治。

我还听到了另一个故事，有一群法师决定团结，一起隐藏起来，然而他们仍然不断在伊格兰斯的袭击下被迫逃跑。在那些外面世界的传说里，那些法师被一个有着火焰一样的头发，烈焰一般的双眼，手中裹挟着火焰的恶魔所领导。她用愤怒的烈焰战斗，没人能够战胜她。我对于这样的描述很是熟悉……

我仍然继续着我的统治，继续着我的职责，保护永恒精灵人民。我们已经不用害怕袭击者，可以通过零散的交易确保我们的补给，并且正在慢慢重建我们所失去的东西。但是，畏惧和羞愧仍然让我们不敢向世界展示我们自己。

十五年后的一个夜晚，我在我的议会室里醒来，看到霜华之月的月牙微光照亮了我床位的一个身影。那是一个高大而苗条的身影，身穿紧身的羊毛与毛皮衣物。她背对着我，深红的长发在空中起舞。我想到了无数年前的夜晚，那是我还更加天真的时代，年轻时的我和年轻时的她第一次如此靠近的那个夜晚。

我简直不敢说出她的名字，生怕这一切都只是我的一场梦境，当我说出那个名字的时候，这个美好的梦境就会破裂而消失殆尽。“莱娜尼尔…”我轻声说道。她的身体转向我，我看到我记忆中的那双黑色的眼睛。然而，她的脸上已经充满了操劳的痕迹，岁月、压力和责任已经在她的脸上留下了痕迹。

我从床上起来，穿上我的长袍。我朝着她的方向前进了几步，但停了下来，不敢再次继续前进。我想要接近她，想要再一次和她相拥，但那一瞬间，我们之间仿佛又有了一道巨大的藩篱——时间和苦痛的鸿沟已经阻隔了我们。

“我是来这里请求帮忙的，艾伦尼恩”，她用低沉的声音说道，目光却不大敢与我对视。“我有一些想要寻求的东西，你必须帮我实现它。”我不明白这意味着什么，但我还是点头同意。“穿好衣服，准备出发吧。前面还有很长的一段路要走。”

她走向窗台，再一次背对着我，直到我穿上斯莱特锁甲，拿起我的剑。当她注意到我已经准备好了的时候，她向外飞去，而我也紧随其后。

我们在空中呼啸而过，以极快的速度向北飞行。望向我们脚下所飞过的大地的痕迹，随着我们向北方越走越远，气候越来越冷。在一片沉默中，时间缓缓流逝，我们飞越白雪皑皑的苔原。我们掠过了白色和灰色的平原，到达了一片低山丘陵。莱娜尼尔在这里减速并下降，我也紧随在她的身后。我们在山脚下的一个黑暗的洞口前停了下来。

莱娜尼尔站在这里，凝望着眼前黑色的山洞。她的脸上散发着些许恐惧，但她的眼睛充满意志和决心。“它在这里，”她用坚定的口气平静地说道。我循着她的目光，试图猜测这个遥远的地方包含着什么秘密，但我没有察觉到任何特别之处。

她不断向前，我紧随其后，直到我们来到了一个被阴影覆盖的入口。莱娜尼尔迟疑了一会儿，望向洞口的黑暗，然后终于走了进去，从视野中消失了。我可以感受到，某种古老的力量正在这里沉睡。我的皮肤一阵刺痛，体内的奥术亲和如同燃烧起来。这个黑暗的洞穴里蕴藏着某种神秘力量，自埃亚尔最古老的时代起便不为人知。这里的某样东西足以改变世界的命运。

我深吸一口气，向前走去。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00160 | HUMAN-REVIEW | cross-batch-037 | advisory | 若纳入本轮润色，恢复“眼睛周围布满操劳的皱纹” |  | fix |
| hrq-00161 | HUMAN-REVIEW | cross-batch-037 | confirmed | 先确认仓库对话标点体例，再决定优先级 |  | fix |
| hrq-00162 | HUMAN-REVIEW | cross-batch-037 | confirmed | 改“床尾的一个身影”或更贴 near 的“床尾附近的一个身影” |  | fix |

<details><summary>hrq-00160 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：眼周皱纹特写被泛化成“脸上的痕迹”，且相邻分句重复“痕迹”
```
```
raw verdict: 「床位」应为「床尾」（near the end of my bed）→confirmed; 眼周皱纹特写被泛化且“痕迹”重复→advisory; 直接引语逗号位于后引号之外（低影响排版）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-036-01.md](reports/sol-036-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。
```
</details>

<details><summary>hrq-00161 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）：直接引语逗号置于后引号之外；Sol 认为 Gemini 视为中性的“排版习惯差异”略显宽松
```
```
raw verdict: 「床位」应为「床尾」（near the end of my bed）→confirmed; 眼周皱纹特写被泛化且“痕迹”重复→advisory; 直接引语逗号位于后引号之外（低影响排版）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-036-01.md](reports/sol-036-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。
```
</details>

<details><summary>hrq-00162 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：「床位」应为「床尾」，源码 `near the end of my bed`（elvala.lua:429），同章第二夜也用 `at the foot of my bed`
```
```
raw verdict: 「床位」应为「床尾」（near the end of my bed）→confirmed; 眼周皱纹特写被泛化且“痕迹”重复→advisory; 直接引语逗号位于后引号之外（低影响排版）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-036-01.md](reports/sol-036-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。
```
</details>

## entry-01225

- 位置：`mod-tome.lua:15366`（tome）｜section：`mod-tome/data/lore/elvala.lua`｜source_tag：`_t`
- 原文：`#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Eight: Forbidden#{normal}#

Light sprung from Linaniil’s staff, and she cast about a luminescence, revealing a narrow icy passageway that led downwards.  It was deathly cold, and our breaths condensed in clouds as we made our way down the wending tunnels.  My skin pricked, and all my senses seemed on edge.

“What is down here?” I asked, my curiosity all-consuming.

“Power,” Linaniil responded, not looking at me as she spake, continuing to follow the path.  “And power be what I seek.  I am afeared for mine people, but have not the strength to protect them as I wouldst like.  With what be here, perhaps, I shall have the power to make a safe haven.  This be a place of legend amongst mine people, and I have scouted it out over many years.  Today I shall finally reach what lies at the centre.”

“And why do you need me?”

She didn’t respond, but carried onwards.  We reached a split in the tunnel, and without hesitation Linaniil took the left path.  It led further and further underground.  We came to blockages, but by arcane force the sorceress easily cleared a way.

As we passed through a large cavern I sensed movement, and drew Mooncutter quickly.  What looked like a disembodied limb, or some great thrashing worm, was writhing towards us pathetically.  Linaniil send a blast of fire towards it - it squealed and went still.

And then more movement, a hundred movements.  From crevasses and holes in the walls and ceiling there burst out dozens upon dozens of the worm-like creatures, their maggoty bodies flapping rigorously, fanged mouths opening up and screaming torturous sounds.  Linaniil growled and began sending torrents of flame towards the approaching horde.  I covered her back, slicing open their pale green flesh and sending strokes of lightning through their ranks.  In under a minute we had dispatched them all.

I prodded a corpse with my foot and it collapsed into sludge.  “What strange creatures,” I commented.  I looked at Linaniil for some explanation but she simply proceeded forward.  I followed after, keeping my sword in hand and watching closely for further attacks.

At the other end of the cavern a wall of ice blocked our way.  Linaniil held up the Ring of Kar’Krul, and the jewel on it began to blaze.  The ice melted away slowly, revealing a passage to another, smaller chamber.

This cold, crypt-like hollow was covered in smooth, glistening ice on all sides.  The walls were square and straight, and ancient pillars of marble were dotted about the room.  On the pillars and walls were weathered runes and symbols.  I came close to study some, but couldn’t recognise them from any of my studies.  “What was this place?” I asked, turning to Linaniil.  “It seems older even than Sher’Tul.”

She ran her hand over one of the walls, tracing the outline of a door.  “It be a temple to Quekorja, god of a race whose name somehow escapes my mind.  The were killed off by the Sher’Tul long before our races were born.  They did build this temple in honour of Quekorja, and the last of them did die here defending her.”

I looked about in awe.  Though I had explored many Sher’Tul ruins I hadn’t seen anything like this.  The architecture was simple but elegant.  There was a crude beauty to it all.  I turned back to the door Linaniil was examining.

She was trying to open it, but was obviously struggling to find a way.  “There be some key, some puzzle to open this,” she muttered.  “But I can nay solve it - the secret be lost to time.”  She growled in anger and stood back.  Holding out her staff she unleashed a blast of arcane force from it, violently splitting the stone door apart and tearing open a passage to a chamber beyond.

Many things suddenly happened at once.  From beyond I felt a pulse of energy, a huge surge of power that I had never felt before.  Linaniil was focussed on it intensely.  But noise came from all around of creatures moving asudden.  From the cave we had entered from there was a shriek of a hundred wailing voices, and the floor beneath our feet trembled.  Rocks fell from the ceiling and out burst horrific creatures with spiked limbs and smooth, triangular faces.  From the trembling ground arose a strange ethereal being of light, with long tentacles for limbs.  And as I turned to face these threats I saw that in the previous cavern the worms had come back to life, and were now coalescing into a huge mass of putrid flesh.

I tried to cut through the being of light, but my sword barely slowed as it passed through it, and the flames I summoned seemed to have little effect.  It raised a tentacle towards me and an intensely bright beam of light shone from it through my torso, filling my flesh with searing pain.  I jumped back and send a wave of ice at it, tearing off a tentacle and pushing it further away.  Meanwhile Linaniil had reduced one of the spiked creatures to a pile of ash, but her arcane shield was collapsing beneath the slashes of the others, and more were spilling from the ceiling.  In the entranceway the mass of worms was pressing through, and from the mouths of the flailing bodies came spits of burning acid.

We were at severe risk of getting surrounded in this confined space, the numbers too many to take on at once.  “Over here!” shouted Linaniil, as she dashed through the door she had split apart.  I followed, slashing my blade through the mass of worms, causing it to lurch back screeching in pain, and spearing a blast of lightning through one of the spiked creatures, splitting open its head.  It continued to attack me, but I parried and cut its arm off, dancing around it and reaching the doorway.  With my back to the opening I brought up a wall of water and sent it flooding into the chamber, pushing the horrors away as I leapt backwards through the door.

As soon as I passed through Linaniil thrust her staff into the ground and a pillar of rock rose upwards, sealing off the opening.  I could hear thrashing and thumping sounds from the other side, but for now we seemed safe.  “What were those things?!” I asked incredulously, as I scanned around the open cavern for signs of any more creatures.  It was a large space, but everything was still, and I could see no other entrances.

“Scions of Amakthel,” she responded calmly.  “The butchered god seeks to break his chains.  But he needs more power...  And here in this dark, forgotten place is part of that power he seeks.”

“And what is here?  What terrible power lies here that would draw both you and those horrors?!”

“Quekorja,” she said.

“Quekorja?  The... the god?”  I couldn’t believe I what I was hearing.  “Was it not slain by the Sher’Tul?”

“Aye, that it were.  But there be power even in a slain god.  Look behind ye, Aranion.”

I turned then, wondering what she wanted me to behold.  It took me a moment to see it, but when I did I gasped in shock.  The far wall of this great cavern was not merely a wall.  It was covered in a thick layer of ice, but beneath at its centre I could make out a huge yellow eye.  And around that eye I could trace out a giant form.  Dark grey skin covered a bulging head, topped with three great curved horns, which sat atop a long, thick body with six limbs.  It was deathly still and chillingly ancient, seeming more like part of the rock than anything that had once been alive.  I couldn’t believe what I was seeing, but I could feel it.  In that corpse was still power, immense power, like nothing I had ever felt before.

“This be it,” said Linaniil.  “One of the few corpses of the gods left to find in Maj’Eyal.  And I shall take its power as mine own.”

“This is insane!” I shouted.  “You have no idea if that is safe or not.  You don’t know what it will do to you!”

She chuckled darkly.  “Aye, that be true.  But that is why I have brought ye here.”  I looked at her in confusion and she chuckled again.  “Ye still know not your purpose here.  Did ye think I took ye here for protection?  That I couldst not handle those horrors on mine own?  No, there be a different reason I have brought ye.  When I absorb this corpse, when I take its power for mine own, I do not know what wilst become of me.  It may kill me.  Or it may drive me mad, it may turn me into something terrible.  Should that happen, Aranion, you art the only one I know with the strength to kill me.”

The words hit me like a blow to the chest.  “Kill you?  But I couldn’t...”

“But ye must!” she said firmly.  “After all ye have done... all the torture ye have brought my life... ye owe me this.”  I looked deep into her eyes and saw the turmoil of emotions within, the pain and agony of all that had befallen her, the hatred and blame of those who had wronged her, the guilt and shame for not being able to do more herself.  And deep inside still some touch of love for me and what we had shared.  I reached out my hand and stroked her soft hair, my fingers touching lightly against the side of her face.  I leaned in close and she closed her eyes, turning her face up to me as I moved my lips towards hers.

“No!” she suddenly cried, pushing me back.  “It cannot be!”  She swiftly turned from me, and I saw a tear drip down one cheek.  “The world has changed, Aranion.  I have a duty before me, and none can walk that path beside me.”  And with that she began to run, staff in hand, towards the great eye whose dead gaze was locked behind the wall of ice.  I sprinted after her, but she was faster, and with running leap she thrust the base of her staff through the ice and into the center of the god’s eye.

The ice cracked with a deafening thunder, and the giant yellow eye pulsed before exploding in a ball of light.  I stopped and covered my eyes as white light flooded the room and shards of ice flew through the air.  I could barely make out Linaniil, bathed in light, hanging with one hand from her staff, her hair and robes blown backwards as she reached forwards with her other arm.  Slowly, intrepidly, she placed her hand into the centre of the ball of light where the eye had been, and shadows danced about the cavern as she wrapped her fingers round that luminous sphere, before squeezing tight.

The cavern shook, her staff shattered, the wall creaked and split before wholly blasting apart.  The corpse of the dead god collapsed into a stream of silver and in a roaring cacophony rushed towards Linaniil, tearing apart her robes and sinking into her skin.  She floated in the air, limbs outstretched as the vast energy poured into her flesh.  She opened her mouth as if to scream and light burst out, and light spilled from her eyes and ears.  The cavern quaked dangerously and rocks fell from the walls and ceiling.  But in seconds it was over, the corpse of the god fully absorbed, the light in Linaniil’s eyes went out, and she dropped to the ground like a stone.

Then the horrors broke through, the collapsing cavern having made an opening for them, and immediately they sped hungrily to where Linaniil lay.  “No!” I cried, rushing to intercept them.  “You cannot have her!”

I sliced off the head of a spiked creature and put up a wall of fire ahead of the rest of them as I backed towards Linaniil’s body.  She looked dead, with no sign of movement or breathing, but I had no time to check.  The being of light and tentacles passed through my flames without resistance, and I ran sparks along my sword as I tore it up the centre of the monster.  It shot light through my torso and I coughed up blood, but I forced my sword in deeper and ran a flood of arcane energy through it, blowing the thing apart.  More spiked creatures came, and I took care of my footing whilst parrying and chopping on my left and sending waves of flame to my right.

The mass of worms broke through the wall, and with it two more luminous horrors, and some fiend of darkness and nightmares, and I could see behind others were spilling through.  I put up a shield as rays of light shot towards me, and sent balls of frost back at them.  One of the light beings fell, whilst the other was slowed.  The dark thing came quickly, and the mass of worms not far behind, so I sliced my sword across the ground, sending heat through it, and turned the stone into a mass of lava.  The dark thing came around it, and I felt an aura of deathly cold from it as it approached.  I hacked at it desperately, and it shot back speared limbs towards my chest that seemed to suck all strength from me.  With a roar I shot a pulse of flames down my blade and it burst apart.  The worms charged directly over the lava, squealing in pain as a bulk of them were burned, but coming at me with speed.  I adjusted my grip, getting ready to make deft strokes to stay out of its range, but a lance of light then shot through my leg, dropping me to one knee with a scream.  The mass of worms rushed at me then, and I dug my sword deep into their midst, but the worms crawled over my arms, digging their acidic teeth into my flesh and reaching for my neck.  With my left arm I cast a blanket of flames over them, burning my arm along with the screeching worms.  They pulled away slightly, but the being of light was approaching from the side, a tentacle flaring up in luminescent energy, and three spiked horrors were behind it.  My right arm was burnt, my left leg injured, my mail pocked with holes, and my mana reserves were running low.  But I gritted my teeth in determination - I could not back from this fight.  I rushed at the mass of worms with my sword held firm.

It exploded in a fiery mess, and an intense wave of force and fire blasted across the cavern, turning the other horrors to ash, and even burning through the luminous being - a low scream arising from it as the flames tore it apart.  I gasped, not knowing whence this blaze had come, until I turned around and saw Linaniil.  She was standing tall, her robes burnt off, flames dancing up and down her skin, bright light shining from her eyes.  Heat seemed to radiate from her.  I kept my grip on my sword, not sure if this was the Linaniil I knew, or some other force born of her union with the dead god.

She laughed suddenly, and it was a harsh laugh that I had not heard her make before.  “What a fool I have been,” she said, almost to herself.  “I brought ye here in case ye had to stop me.  But now...  Now mine power exceeds ye by a long distance.  Ye would have no hope of opposing me!”  She made a low sound somewhere between a laugh and a sigh.  “Ah, but ye have no cause to worry.  I am still me.  Mostly.  And through pain and sacrifice I have achieved the power I desired.  The power I need.”

I let my sword dip and breathed heavily, relief mingled with trepidation sweeping through me, whilst the withdrawing adrenalin of battle left me feeling exhausted.  I looked Linaniil over, her pale skin now glowing, her eyes brimming with energy and vitality.  I saw the power she had was not in mere force, but that she had taken on the ageless nature of the gods.  A power forbidden to all creatures was now hers and hers alone.

“What now?” I said quietly.

“Now, ye go home, and I go to make mine home, a sanctuary for me and mine people.”

“Will we meet again?”

She smiled sadly.  “Mayhaps.  Mayhaps not.  The world changes quicker than predictions can tell.  But if we do meet again it shall be in a place that does not yet exist - the city of Angolwen.”  She raised an arm then and from it shot a tremendous pulse of arcane energy, the violet light shooting to the roof of the cavern and spearing through, deep through, till it split the rock apart right through to the open sky a mile above.  Sunlight spilled down, splashing over Linaniil’s lithe form.  It had been many hours since this long long night had begun.

“But for now, farewell Aranion,” she said as she began to float from the ground.  And then she sped up and soared out of sight.

I lay down on the cold stone, resting for a while, slowly healing my wounds and recovering my strength.  I reflected on the events since the evening before, thinking back on the trials of all the races of Maj’Eyal.  War, disease and death threatened all equally.  Was Linaniil beyond that now?  How would a taste of immortality affect her?

It was then that thought for our race came to me.  In ages past we had searched for immortality.  Our ancestral leaders had obsessed over it, but out of vanity, pride and a fear of death.  What would the real effects be if all our society were to be gifted with it?  With immortal life we might separate ourselves from the strifes and wars of the world.  It would give us a perspective beyond the petty squabbles and prideful competition of the other races.

I dug through the ice and rocks and found still some trace of the dead god Quekorja, faint though it were.  I gathered all that was left and made the long journey back to Elvala.  There I retreated to my labs, studying the remains for years before finally unlocking its secrets.  It was thus that immortality for our race was born, and it has changed our outlook on the world ever since.

We stood apart from the others then, not engaging in war, finding a new respect for life.  It was not till Garkul the Devourer assaulted our gates in the Age of Pyre that we ever had cause for large scale war again, and I rode out to face him in combat.

But ah, that is another tale, one indeed of many tales, in the long and rich history of the Tales of Maj’Eyal...`
- 现译：`#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第八章：禁忌#{normal}#

莱娜尼尔释放了一个照明术，光亮从莱娜尼尔的杖尖射出，照亮了通向洞穴内部的狭长的寒冰通道。周围寒冷刺骨，我们缓步向前，呼出的水汽在空气中结成了云雾。我满身鸡皮疙瘩，感觉我的感官快要到极限了。

“下面到底是什么？”我怀着好奇心问道。

“力量。”莱娜尼尔答道。说话时她并未看我，只继续沿路前行。“我所寻求的正是力量。我为我的族人忧心，却没有足够的力量如愿保护他们。有了这里的东西，或许我就有力量建起一处安全的避风港。此地在我的族人中只存在于传说，而我已侦察多年。今日，我终于会抵达它的中心。”

“那么你需要我做什么？”

她没有回应，而是继续往前走。我们到达了隧道的一个分岔处，莱娜尼尔毫不犹豫地走了左边的小路。它通向越来越深的地下。我们遇到了一些障碍，但莱娜尼尔轻易便以奥术力量清开了道路。

当我们经过一个大洞窟时，我感觉到了有什么东西在移动，迅速拔出了斩月剑。那东西看起来像某种脱离身体的断肢，或者某种巨大的蠕虫，可怜地向我们扭动着。莱娜尼尔向它发出一团火球——它发出一声尖叫，再也不动了。

然后，我感受到了更多移动的东西，数量数以百计。从墙壁和天花板上的缝隙和洞里，数十个蠕虫般的生物突然钻了出来。它们蛆一样的身体使劲地拍打着，尖牙张开，发出痛苦的尖叫声。莱娜尼尔咆哮着，开始向正在逼近的虫群发射火焰。我掩护她的背后，切开他们苍白的绿色身体，并向他们发射闪电。不到一分钟，我们就把他们都清除掉了。

我用脚踢了一具尸体，尸体化为了污泥。“多么奇怪的动物啊，”我评论道。我看了看莱娜尼尔，希望她能有什么解释，但她只是继续向前走。我紧随其后，手里拿着剑，密切提防着进一步的攻击。

在洞穴的另一端，一堵冰墙堵住了我们的路。莱娜尼尔举起了卡库罗尔的戒指，其上的宝石开始燃烧。冰慢慢融化，露出通向另一个更小的房间的通道。

这是个冰冷的、地宫般的空洞，四周覆盖着光滑闪亮的冰块。这里的墙壁是规整的方形，房间里散布着古老的大理石柱子。在柱子和墙壁上满是风化的符文和符号。我试图靠近研究它们，但我无法认出任何东西来，这超出了我的学识。“这里以前是什么地方？”我转向莱娜尼尔问道，“它看起来甚至比夏·图尔还古老。”

她将手伸向墙壁，勾勒出一个门的轮廓。“这是奎科加的一座神庙，是一个名字不知为何被我遗忘了的种族之神。远在我们的种族出生之前，这个种族就已被夏·图尔人灭绝了。他们曾经为了纪念奎科加而建造了这座神庙，而他们中的最后一批人为了保卫奎科加本人而在这里战死。”

我敬畏地看着周围的一切。虽然我曾探索过很多夏·图尔遗址，但我从未见过这样的景象。这座建筑简洁而优雅，表现出一种粗糙的美感。我转身望向莱娜尼尔正在检查的门。

她试图打开这扇门，但好像很难找到一个方法。“一定有某种钥匙…或者靠解决某种难题来打开它，”她喃喃地说。“但我解决不了——这里的秘密已经随着时间流逝而消失了。”她发出愤怒的咆哮，向后退开。她拿出她的法杖，释放出一股奥术力量，强行地将石头门分开，撕开一条通往下一个房间的通道。

在那一瞬间，发生了许多事情。从远处，我感受到了一股能量，一股我从未感受过的巨大力量。莱娜尼尔强烈地关注着这份能量。但很快，四周传来有生物在四处移动的噪音。我们进入的山洞里发出了上百生物的哀嚎和尖啸，我们脚下的地板也开始在颤抖。岩石从天花板上掉下来，从里面冒出来了一些可怕的生物，长着有尖刺的四肢和光滑的三角形脸孔。从颤抖的地面中升起了一个光组成的奇怪的虚幻存在，它有着长长的四肢触手。当我转身面对这些威胁时，我看到在前一个洞穴里的蠕虫已经恢复生机，他们现在正在融合成一大堆腐烂的肉。

我试图斩断那个发光的生物，但我的剑穿过他的身体时似乎没有受到任何阻挡，我召唤的火焰似乎也没有什么效果。它向我伸出一根触手，一束强烈的光线从中发射出来，穿透我的身体，我的血肉感受到灼烧一般的痛苦。我向回跳了一步，向它发出一团冰风，撕下了它的一根触手，并将它推了开来。与此同时，莱娜尼尔将其中一个长着尖刺的生物化为了灰烬，但她的奥术护盾在其他生物的攻击下坍塌了，更多怪物从天花板上涌出。那团翻腾的蠕虫怪物也挤过入口，虫体上的一张张嘴喷出灼热的酸液。

我们在这个狭窄的空间会有很大的被包围的风险，他们的数量实在太多，无法立刻解决。“走这里！”莱娜尼尔大声喊道，她冲破了她分开的门。我紧跟向前，用我的刀片切开了那些蠕虫团，使它在痛苦中尖叫起来。同时，我发出一道闪电，穿过了某个长着尖刺的怪物，打破了他的脑袋。它试图继续攻击我，但我格挡了它，切下了它的手臂，在怪物的包围下起舞般闪避着他们的攻击，终于到达了门口。我面对着背后的怪物，建起一座水墙，然后释放一股洪水冲进了这个房间，把那些恐魔推到了外面，顺便跳进了我背后的门中。

在我通过的同时，莱娜尼尔将自己的法杖猛戳地面，一根石柱向上升起，封闭了入口。我可以听到另一边发出的撕裂和撞击声，但现在我们似乎已经安全了。“那些东西是什么？！”我怀疑地问道，同时观察这个开放的洞穴，寻找有没有其他生物的迹象。这个洞穴似乎是一个很大的空间，但一切都很平静，我也看不到其他入口。

“阿马克泰尔的子嗣”，她冷静地回答道。“那位遭到残害的神正挣扎着想要挣脱锁链，但他需要更多的力量…而这个阴暗，被遗忘的地方有着他想要的一部分能量。”

“那么那到底是什么？这里到底有什么可怕的力量，能够吸引你和这些恐魔？！”

“奎科加”，她回答道。

“奎科加？那个…那个神？” 我不敢相信我听到了什么。  “它不是已经被夏·图尔人杀死了吗？”

“是的，就是这样。但即使是已死之神也还残留着力量。你看看后面，艾伦尼恩。”

我转过身，想知道她想让我看到的到底是什么。我花了一点时间才发现了它，但在发现它的一瞬间我惊慌失措。这个巨大洞穴的墙不仅仅是一面墙而已。它被覆盖在厚厚的冰层里，但在冰层的中心，我看到了一个巨大的黄色眼睛。顺着那个眼睛周围搜寻，我找到了这个庞然大物的身体。深灰色的皮肤覆盖着它凸起的头部，顶部有三个巨大的弯角，长着六肢的长而厚的身体之上。它已经死了，冰冷古老的身躯看起来就像是岩石的一部分，而不是某种曾经活着的东西。我不敢相信我看到的东西，但我能够感受到它的存在。在那尸体里仍然有着力量，有着巨大的力量，那是我以前从未感受过的力量。

“它就在这里”，莱娜尼尔说道。“这是在埃亚尔还能找到的为数不多的已死之神的尸体。现在，我要取走它的力量为我所用。”

“这太疯狂了！”我大喊出声。“你根本不知道这种力量是否安全。你不知道这种力量会给你带来什么！”

她发出了神秘的笑声。“是的，你说得对。所以我把你带到了这里。”我迷惑地看着她，她又笑了起来。“看来你还是不知道你来这里的目的。你以为我带你来时需要你的保护？你觉得我没法亲自干掉这些恐魔吗？不，我带你来另有别的原因。当我吸收这个尸体的时候，当我夺取它的力量为我所用的时候，我不知道会发生什么。它可能会杀了我，或者可能会让我发疯，甚至可能让我变成某种可怕的东西。如果发生这种情况的话，艾伦尼恩，你是我知道的人中唯一有能力杀死我的人。”

这句话对我来说如同当头一棒。“杀了你？但我做不到……”

“但你必须这么做！”她坚定地说。“在你对我做了那样的事情之后……在你给我的生命中带来那么多痛苦之后……这是你欠我的。”我深深地看向她的眼睛，看到了她内心情感的波动，看到了她遭受的无数痛苦和磨难，看到了她对加害者的仇恨和责怪，看到了她不能够帮助更多人时内心无尽的内疚和羞愧……还有，在她内心深处的那仅存的有关我和我们爱的回忆。我伸出手，拂过她柔软的头发，手指轻轻地抚摸着她的脸庞。我靠得很近，她闭上了眼睛，当我将嘴唇移向她的时候，她的脸转向了我。

“不！”她突然发出一声哀鸣，把我一把推开。“不可能！”她迅速转身背对我，我看到眼泪从她的脸颊划过。“世界已经变了，艾伦尼恩。我肩负着使命，谁也不能陪我走上这条路。”随后，她手持法杖向前跑去，奔向在冰墙中封锁着的巨大眼睛。我试图追上她，但她速度更快。然后，她一跃而起，将自己法杖的一端猛地插入了已死之神的眼睛的中央。

冰块破裂时发出震耳欲聋的雷声，巨大的黄色眼睛在爆炸中化为了一团闪烁的光球。白光淹没了房间，冰块的碎片在空中飞舞，我不得不停下来遮住眼睛。我几乎看不见莱娜尼尔的身影，她沐浴在强光之中，一只手紧握她的法杖，她的头发和长袍被冲击力向后吹去，而她的另一只手却仍然继续向前伸去，慢慢地，她无畏地把手伸进了眼睛所在的光球的中心，随着岩壁上她影子的飞舞，她的手指环绕住那个发光的球体，紧紧握住。

山洞开始震动，她的法杖被瞬间破碎，墙壁嘎吱作响，劈裂，然后完全炸开。已死神的尸体崩溃成一股银色的气流，咆哮着喧嚣地冲向了莱娜尼尔，撕裂了她的长袍，渗入了她的皮肤。随着巨大能量涌入她的肉体，她漂浮在空中，四肢伸展开来。她张开嘴巴，好像正在尖叫，强烈的光线从她的嘴里，眼睛和耳朵中射出。这个洞穴开始危险地震动，岩石从墙壁和天花板上掉下来。但是几秒钟之后，神的尸体完全被吸收了，莱娜尼尔眼中的光线熄灭了，她像一块石头一样掉到了地上。

然后，恐魔冲了过来。塌陷的洞穴为他们开了一个洞口，他们饥肠辘辘地冲向莱娜尼尔所在的地方。“不！”，我大叫着，冲上去拦截他们。“你们不能夺走她！”

我向莱娜尼尔的身体靠近，同时切下了一个有尖刺的怪物的脑袋，然后用一道火墙阻隔了剩下的怪物。她看上去就像死了一样，没有任何活动和呼吸的迹象，但是我没有时间仔细检查了。那些发着光的触手怪物轻松穿过了我所造出的火墙，我冲上前去，试图用我的剑刃刺穿这个怪物的核心。它射出一道光芒穿透了我的身体，我咳出血来，但我奋力将我的剑刃刺入更深，往里面灌注了一道奥术能量，将那个怪物炸了个粉碎。更多长着尖刺的怪物冲了过来，我迈动步伐，在左侧格挡和切开它们的同时，向着右侧射出了一团团火焰。

那团蠕虫团穿透了墙壁，伴随着它的是另外两个闪烁着光辉的恐魔，还有一些某种暗影和噩梦的魔鬼。我能看到，还有更多的恐魔在朝我们涌来。当那道光线射向我的时候，我打开了一个能量护盾，然后向他们发射了霜冻之球。一个发光的怪物倒下了，而另一个的行动则被减缓了。那个黑暗的东西也走了过来，那团蠕虫团则紧随其后。我把我的剑划过地面，将热能传导到地面上，把地上的石头化为了灼热的岩浆。那个黑暗的存在朝我接近过来，我能感受到它的身上散发出致死的寒意。我拼命地砍向它，而它则把它的触手如同长矛一般直射过来，准备吸走我的力量。我怒吼一声，让一道火焰沿剑刃奔涌而下，将它炸得四分五裂。那些蠕虫踩着岩浆直冲过来，它们中的大部分都被烧成了灰烬，但它们整体的速度没有丝毫减弱。我调整了握剑的手势，准备以轻捷的挥砍将它们挡在攻击范围之外。然而就在这时，一束光线击中了我的大腿，我单膝跪地，发出痛苦的尖叫。那团蠕虫团继续冲向我，我试图用剑刺入蠕虫团的中央，但蠕虫很快爬遍了我的手臂，用他们酸性的牙齿啃噬着我的血肉，接近我的脖子。我用左臂施法，向它们覆下一层火焰，连同尖叫的蠕虫一起灼伤了自己的手臂。虫群微微退开了，但那个发光的生物从另一侧接近了我，它的触手闪耀着光辉的能量。三个长着刺的恐魔围绕在它的后面。我的右臂严重烧伤，我的左腿也受了伤，我的锁甲已经满目疮痍，而我的法力也已经快要消耗光了。但我决心咬牙坚持——在这场战斗中我无路可逃。我紧握手中的剑，冲向那团蠕虫团。

然而，它却在我的面前炸成了一团火焰。一股强大力量的波动席卷了整个山洞，火焰在周围炸开，将其他的恐魔化为了灰烬，甚至连那些发光的存在也不例外——当火焰把它烧尽时，它发出一声低沉的哀鸣。我喘息着，不知道这股强大的烈焰到底从哪里来，直到我回头看到了莱娜尼尔的身影。她正屹立在我的面前，长袍已经被烈焰烧毁。火焰在她的身旁起舞，她的眼睛放射出明亮的光芒。她的身边散发着灼热的气息。我手中紧握着我的长剑，不知道这到底是我知道的那个莱娜尼尔，还是因为她和已死之神的融合中产生的另一种存在。

她突然笑了，那笑声刺耳而陌生。“我真是个傻瓜，”她像自言自语般说道，“我带你来，是为了万一必要时由你阻止我。可现在……如今我的力量已远远超过你。你根本没有希望与我抗衡！”她低低发出一声，介于笑与叹息之间。“啊，不过你不必担心。我还是我。大体上吧。我历经痛苦与牺牲，终于获得了我渴望的力量，也是我需要的力量。”

我垂下剑，大口喘息，释然与不安交织着席卷全身；战斗的激情退去后，我只觉精疲力竭。我打量着莱娜尼尔：她白皙的肌肤如今泛着光，双眼充满能量与活力。我看出她拥有的不只是蛮力，她还承袭了众神不受岁月侵蚀的本质。这份对一切生灵而言都属禁忌的力量，如今只归她一人所有。

“现在怎么办？”我轻轻问道。

“现在，你可以回家，而我则要建造我的家园，一个为我和我的人民建立的避难所”

“我们还会再见面吗？”

她忧伤地笑了。“也许会。也许不会。这个世界正在风云变幻之中，我们无法预知会发生什么。但如果我们还会再见面的话，我们会在一个现在还不存在的地方——安格利文魔法城相见。”然后，她伸出一只手，射出一道奥术能量的脉冲。紫罗兰的闪光射向洞穴的顶部，将其射穿，然后一直延伸，直到它彻底击穿了我们上方一英里厚的岩层，露出了天空的姿态。阳光从中倾泻而下，洒落在莱娜尼尔的轻盈身形之上。看来，我们所经历的这个漫漫长夜已经过去了很长时间。

“不过现在，再见，艾伦尼恩”，她的身体慢慢飞向空中，然后加快了速度，消失在了我的视线当中。

我躺在冰冷的石头上，休息了一段时间，慢慢地愈合伤口并恢复力量。我回顾了自傍晚以来的事件，回顾了马基·埃亚尔所有种族所经历的磨难。战争，疾病和死亡威胁着我们的每一个人。莱娜尼尔现在超越了这一切吗？永生不死的滋味又会给她什么样的影响呢？

然后，我想到了有关我们种族的前途。在过去的岁月，我们曾经追求永生的力量。我们古代的领袖曾经多么为此着迷，但那都是出于虚荣，骄傲和对死亡的恐惧。如果我们的种族都能获得永生的恩赐，那么结果又会怎么样呢？永恒的生命会把我们从外部世界的冲突和战争隔绝。它会给我们一种新的视野，超越其他种族琐碎而骄傲的无止境的争执。

我挖开冰块和岩石，发现了已死之神奎科加的力量还有一些残余，尽管所剩的已经十分微弱。我把剩下的遗骸全部收集起来，把它们带回了埃尔瓦拉。在那里，我回到我的实验室，研究遗骸多年，终于揭开了它的秘密。从此，我们的种族获得了不朽的力量，这永远改变了我们对世界的看法。

我们独立于其它种族之间的纷争，并不参与毫无意义的战争，寻求一种对生命的新的尊重。直到吞噬者加库尔在烈火纪袭击了我们的大门，我们才重新开始了大规模战争，而我则亲自在战场上直面了他。

啊，不过，这就是另一个故事了。那是在漫长而充实的历史之中，马基·埃亚尔的传说中的另一个故事…`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00163 | HUMAN-REVIEW | cross-batch-038 | confirmed | 人工待决：两项 pending 需主代理按术语库/前序冻结文本核对后才能定。译文未修改。 |  | fix |

<details><summary>hrq-00163 · HUMAN-REVIEW 详情</summary>

```
作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-037-01.md](reports/sol-037-01.md)。译文未修改。共 19 个 claim：17 confirmed、2 pending、无 refuted/advisory。Sol 总评：Gemini 指出的断裂病句、方位错误、动作失真、漏标点、单复数与漏译均成立。

| 组 | Sol 分档 |
| --- | --- |
| 病句/方位/动作（全 confirmed） | “长着六肢的长而厚的身体之上”断裂病句；“我面对着背后的怪物”方位矛盾；“顺便跳进了我背后的门中”；`blade` 译“刀片”；“她冲破了她分开的门” |
| 标点（全 confirmed） | 第 41 段末漏句号；多处引号外标点 |
| 实体 `luminous horror` | confirmed：此处确指该游戏实体；**pending**：固定中文实体名是否必须是“金色恐魔”；confirmed：“还有一些某种……”语病 |
| 战斗动作（全 confirmed） | 单数误作复数；漏译剑上电火花并添“试图” |
| 其他措辞（全 confirmed） | `hanging with one hand from her staff`；“她的法杖被瞬间破碎”；“已死神的尸体”；`all my senses seemed on edge` |
| 正面项 | confirmed：富文本标记与占位符完整；confirmed（仅限本条目内部）：人名地名专名一致；**pending**：与传记前序章节“严格一致”的跨章节主张 |

人工待决：两项 pending 需主代理按术语库/前序冻结文本核对后才能定。译文未修改。
```
```
raw verdict: “长着六肢的长而厚的身体之上”构成断裂病句→confirmed; “我面对着背后的怪物”方位矛盾→confirmed; “顺便跳进了我背后的门中”动作失真→confirmed; `blade` 译为“刀片”→confirmed; “她冲破了她分开的门”→confirmed; 第 41 段末尾漏句号→confirmed; 多处引号外标点→confirmed; 此处确实指游戏实体 `luminous horror`→confirmed; “固定中文实体名为金色恐魔”→pending; “还有一些某种暗影和噩梦的魔鬼”语病→confirmed; 发光触手生物单数误作复数→confirmed; 漏译剑上电火花并添加“试图”→confirmed; `hanging with one hand from her staff`→confirmed; “她的法杖被瞬间破碎”→confirmed; “已死神的尸体”→confirmed; `all my senses seemed on edge`→confirmed; 富文本标记和占位符→confirmed; 人名、地名和专名保持一致（仅限本条目内部）→confirmed; 与传记前序章节译名“严格一致”的跨章节主张→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-037-01.md](reports/sol-037-01.md)。译文未修改。共 19 个 claim：17 confirmed、2 pending、无 refuted/advisory。Sol 总评：Gemini 指出的断裂病句、方位错误、动作失真、漏标点、单复数与漏译均成立。 人工待决：两项 pending 需主代理按术语库/前序冻结文本核对后才能定。译文未修改。
```
</details>

## entry-01228

- 位置：`mod-tome.lua:15875`（tome）｜section：`mod-tome/data/lore/fun.lua`｜source_tag：`_t`
- 原文：`#{italic}#An undead hunter's guide, by Aslabor Borys#{normal}#

So, apparently I'm a legend now. Hah, knock a vampire's head off with a greatmaul and suddenly you're up there with Toknor and Mirvenia apparently. More and more often these days I get novice adventurers coming up to me, asking me for advice when it comes to battling the undead. My first instinct was to tell them to get back home and become bakers or gardeners or something. If they need crib notes for combat they obviously aren't cut out for it.

But then I was thinking, these are good kids. Heck, I'd buy every man and woman in the world who's bumped off a ghoul a free drink if I could. If they want help when it comes to putting down necromancer slime and their chilling creations, I would be more than happy to oblige. Not much of a writer, but let's see. First...

#{bold}#1. Ghouls#{normal}#

Every once in a while, people come to me and say "Are all necromancers truly evil?" "Surely necromancy could be used for good!" "Isn't it wrong to discriminate against others simply because of the magicks they practice?" To these people, the first thing I usually say - shortly after giving them a black eye - is to take a look at a ghoul. Take a good, long look. Take in the diseased, putrescent flesh. Take in the oozing, exposed organs. Take in its features, slowly rotting to mulch. It used to be a person. It used to have a family, people who loved it. Now it's a walking corpse, its only desire being death and the mad, all-encompassing consumption of living flesh. Are all necromancers truly evil? A thousand times, yes.

Even this most basic of undead minions can strike terror into the unprepared. The multitude of diseases that a normal ghoul carries are contagious in a manner many adventurers do not truly appreciate until they see the sores and necrosis visibly spreading up their arm from where a ghoul bit them. Such maladies must be dealt with promptly: if bitten by a ghoul, immediately plunge the afflicted area in scalding hot water, then wrap it quickly in clean cloth lined with mugwort and quartz powder. The wound must remain dressed for three weeks, with new dressings applied every four days, and make sure to burn the old ones! Failing the above, a wild infusion also works splendidly.

    * * *


#{bold}#2. Skeletons#{normal}#

What guide to the undead would be complete without mentioning the humble skeleton? Despite these clattering and chittering bones of the deceased often looking so fragile that a stiff breeze could break them apart, in many ways they are more dangerous than their ghoul cousins.

With no masses of rotted and ruined flesh to reanimate, necromancers can commit themselves fully to bestowing some level of fighting skill on a reanimated skeleton, and since a fighter's weapons will often last as long as his bones will, skeletons are usually armed and sometimes even armoured. The potential skill of a skeleton doesn't stop at melee weapons either - fallen archers take up their bows once again, and although difficult by comparison, some necromancers can even grant dead mages their magic powers once again.

Some adventurers find themselves baffled when it comes to fighting skeletons. How do you destroy a foe who, by all rights, should be destroyed already? To these adventurers, I say take heart. The more broken and incomplete a body is, the more effort it takes to keep it reanimated. As most necromancers see skeletons as the lowest of low peons, you can expect a few good blows to easily dissipate the minimal effort their masters put into creating them.

    * * *


#{bold}#3. Wights#{normal}#

Wights are an odd duck amongst the undead, often not created by necromancers specifically, but instead rising of their own volition when the conditions are right. Wights are by no means individual souls, but often part of a gestalt; when a particular land has seen enough bloodshed - battlefields, forest, crypts and graveyards - wights can be seen to rise en masse, a near-physical representation of the battles and turmoil the land has faced. Sadly, it is for this reason that necromancers often facilitate the creation of wights regardless, for no other study or profession causes so much blood or death.

Those who have had encounters with wights often describe them as indistinct skeletal figures, wrapped in flowing cloaks that become faded and incorporeal at their edges, while strange lights dance where their eyes should remain. Survivors tell of a peculiar sense of exhaustion when in close proximity to them, as though merely being close to these figments of death causes one's life force to sputter and fade. Regardless of this and their ghostly appearance however, it has been recorded that steel and strength of arms is yet enough to destroy them, or at least to erase them for the time being. It's just a shame that such battles are likely to simply create more of them in the long run...

    * * *


#{bold}#4. Vampires#{normal}#

Vampires are so far removed from other varieties of undead it seems almost unreal. What grants them their longevity? How do they retain such great intelligence? Beyond their sallow complexion and drawn features, why do they not decay and decompose as their ghoulish siblings do? The study of vampiric nature is one long list of unanswered questions, each new study adding yet more to the ever-growing pile.

As said before, a vampire's greatest strength is its resemblance to a living man, both in mind and body. Thanks to this, vampires are known for residing comparatively close to normal towns and villages far more than other undead. Some have even been known to keep their lairs within these communities themselves! Despite their resemblance however, there are many telltale signs of vampirism: Unnaturally pale skin, long and distinctive fangs, an aversion to sunlight, and much more besides. In an effort to avoid close inspection, some vampires are known to masquerade as men of wealth, often cloistering themselves in remote locations to discourage prying eyes.

But perhaps the most astonishing thing regarding vampires is their propensity for alliance and familial relationships. No other undead being even approaches matching the incomprehensible tangle of clans, broods, families and bloodkin that vampires create for themselves. It is for this reason that vampires often end up becoming rulers of lesser undead themselves, commanding them as a normal necromancer would. So, in turn, treat them as you would a necromancer - with cold steel.

    * * *


#{bold}#5. Spirits#{normal}#

During my travels, I have noticed that some communities in the wild no longer bury their deceased as is the norm in larger settlements. Some folk burn the corpses of their fallen, committing their ashes to the earth instead. When asked why they perform this peculiar practice, I always receive the same answer: Necromancers. Fearful of their dead rising up to slay them at the whims of delusional, murderous filth, they believe that with the burning of the dead, their spirits are forever beyond the reach of a necromancer's bony fingers.

Alas, this is not true. While fire may burn away a man's physical being, no flame can touch his spirit. Unfortunately, necromancers can. Bereft of both body and freedom, many souls are driven mad in the employ of necromancers, ceaselessly drifting through windswept crypts, harrying any unfortunate wanderers they encounter with a multitude of curses and hexes. Worst of all are those spirits who embrace their newfound purpose, causing them to grow in power at a frightening rate. No other being in Maj'Eyal is so obviously abhorrent to existence itself as these "dreads"; it is almost as though creation itself wants these beings gone from her world. It is my hope that you, and many others, oblige her wish.

    * * *


#{bold}#6. Bone Giants#{normal}#

One of the most horrific, vomit-inducing expressions of the necromancer's so-called "art" is the bone giant. Not content with merely profaning the bodies of singular souls, some ambitious necromancers work to bind the bodies of countless skeletons together, creating hideous engines of destruction that can stand many times higher than the height of a normal man.

It is a deadly mistake to liken these abominations to the golems alchemists and archmages employ. Wilful and fey as they are, normal mages often only craft golems for utility and their own protection, while necromancers create bone giants for the sole purpose of dealing death, and the only limit to their destructive capability is the necromancer's twisted imagination. Ever fought a snow giant? Imagine one with six arms and fingers like blades, wrought of sharpened ribs. Imagine one with countless skulls lining every inch of its wretched body, all screaming for your blood to be spilt as it thrashes spinal columns like whips from its disfigured hands! After facing one of these grotesque amalgamations, you'll be begging to go back to the Daikara to pick on simple, frost-rimed sub-men.

    * * *


#{bold}#7. Liches#{normal}#

Hate made flesh. Evil made pure. Death incarnate. The culmination of a necromancer's work. Whatever you know liches as, I can tell you that they do not match the countless myths and legends that surround their terrible figures. They surpass them.

Once a powerful necromancer finally crosses the border between life and death, the abyssal power that they could only initially grasp in dribs and drabs becomes theirs to control totally. It is often said that unexpected quakes, crops failing, and the leaves simultaneously falling from the trees heralds the birth of a lich. Lords of the undead, liches can annihilate ghouls and skeletons, banish dreads with a glance, and reduce bone giants to powder within moments.

As to how to actually destroy one? Well, tell you what. If you manage to defeat one of these abominations, be a dear and write a guide for me, for I have absolutely, positively, no idea.

    * * *`
- 现译：`#{italic}#一名不死猎人的指南 作者：阿斯拉伯·波利斯#{normal}#

这么说，我如今也成传奇人物了。哈，不过是用大槌敲掉一个吸血鬼的脑袋，转眼就有人把我和图库纳、米雯尼雅相提并论。最近越来越多的新手冒险者跑来问我，该怎样对付不死生物。我的第一反应，是叫他们回家当面包师、园丁，随便做点别的。打架还得看小抄，显然就不是这块料。

不过转念一想，这些孩子都不坏。见到世上任何一个干掉过食尸鬼的男人或女人，我都乐意请上一杯。要是他们需要帮忙收拾死灵法师那帮渣滓和他们阴森森的造物，我当然愿意效劳。我不太会写东西，不过试试看吧。首先……

#{bold}#1、食尸鬼#{normal}#

时不时有人来问我：“所有死灵法师真的都邪恶吗？”“死灵法术难道不能用于善事？”“仅仅因为别人修习某种魔法就歧视他们，难道不是错的吗？”对这些人，我通常先赏一只乌眼青，然后叫他们好好看看食尸鬼。仔仔细细看个够：染病腐败的血肉，裸露在外、不断渗液的脏器，还有渐渐烂成泥浆的面孔。它从前也是个人，也曾有家庭，有爱它的人。如今却成了一具行尸走肉，唯一的欲望就是死亡，以及疯狂地吞噬一切活人的血肉。所有死灵法师真的都邪恶吗？千真万确，是。

即使是这种最基础的不死仆从，也足以让毫无准备的人胆寒。普通食尸鬼携带的多种疾病极易传染；许多冒险者直到亲眼看见溃疡与坏死从被咬处沿手臂蔓延，才真正明白危险。这类病症必须立刻处理：若被食尸鬼咬伤，马上将患处浸入滚烫的热水，再迅速用内衬艾蒿与石英粉的干净布料包好。伤口必须包扎三周，每四天更换一次敷料，而且务必烧掉旧敷料！做不到这些，用野性纹身也很有效。

    * * *


#{bold}#2、骷髅#{normal}#

要是不死族狩猎指南里都没有最常见的骷髅那还算个屁指南？虽然这些亡灵身上的白骨在走路时上下乱颤，搞得一副弱柳扶风的样子，但是从许多方面来说，它们都远比自己的食尸鬼表亲要危险多了。

因为骷髅身上通常不会有那么多累赘腐肉，死灵法师得以全身心的投入对骷髅战斗能力的授予，同时由于战士们生前所用的武器几乎和他们的骨头一样经久耐用，我们遇到的骷髅兵大多都是持有武器或是全副武装的。何况骷髅对我们的威胁并不仅仅是近身战：死去的弓箭手会再度拿起弓；虽然更为困难，有些死灵法师甚至能让死去的法师重获魔法力量。

不少冒险者在面对骷髅时都疑惑不解——如何摧毁一个早已死的不能再死的骷髅。对于这些冒险者，我只想说：鼓起勇气吧。骷髅的身躯越是遭到破坏残缺，死灵法师们驱动它们所要消耗的法力就越大。因为大多数的死灵法师都将骷髅视为最低等的奴隶，相信在你数个重击之后就能驱除死灵法师附着于其身上的微弱法力。

    * * *


#{bold}#3、尸妖#{normal}#

尸妖是不死生物中的异类，往往并非由死灵法师特意创造，而是在条件成熟时自行出现。尸妖绝不是单独的灵魂，而常是某种集合意识的一部分；某片土地经历了足够多的杀戮——无论战场、森林、地宫还是墓园——尸妖便会成群升起，几乎是这片土地所受战争与动荡的实体化身。遗憾的是，死灵法师仍常常促成尸妖诞生，因为没有别的学问或行当会制造如此多的鲜血与死亡。

与尸妖战斗过的人经常将其描述为：一具轮廓模糊的骷髅身形，裹着飘动的褪色长袍，袍角逐渐变淡、虚化，本该是眼睛的位置则跳动着诡异的光。幸存者们则述说只要靠近这种诡异的生物，仅仅是靠近这些死亡的化身，自己的生命力就会不住地衰减、消逝。

万幸的是，尸妖虽然看上去很像鬼魂，已经被证实它们还是能被武器和腕力所消灭，至少是暂时消除了它们的威胁。无奈的是，这种战斗长远来说只是变相的壮大了尸妖族群而已。

    * * *


#{bold}#4、吸血鬼#{normal}#

吸血鬼与其他种类的不死生物相去甚远，简直令人难以置信。是什么让他们如此长寿？而他们又是如何保留这样强大的智力？暂且不提他们萎黄的面色与消瘦的五官，他们为何不像食尸鬼同类一样腐烂分解？

关于吸血鬼本质的研究仍有许多未解之谜，而每个新课题似乎也只是增加了更多的谜题而已。

如前所述，吸血鬼最大的优势，是身心都与活人极其相似。因此，比起其他不死生物，吸血鬼往往住得离普通城镇和村庄近得多；有些甚至直接把巢穴设在这些社区之中！

然而再怎么像人，吸血鬼仍有许多显眼征兆：不自然的苍白皮肤、细长醒目的尖牙、畏惧阳光，等等。为了躲避近距离盘查，有些吸血鬼会伪装成富人，常年幽居偏远之地，不让好奇者靠近。

但也许吸血鬼最让人称奇的地方，是他们纷繁复杂的系谱和族群。他们自发组建部族、血盟、家族等不可思议的集群，这是其他不死族无法望其项背的。借助团体的力量，吸血鬼常常成为弱小不死族的主宰者，像一名普通的死灵法师一样操作指挥着自己的奴隶。所以，请你也像对付死灵法师一样对付他们——用钢剑刺穿他们的喉咙。

    * * *


#{bold}#5、幽灵#{normal}#

在我的旅程中，我注意到荒野中的一些社区已不再像较大的聚居地通常那样埋葬死者。取而代之的是，他们会将死者的尸体焚化并将骨灰撒落在大地之上。当我询问他们这奇怪行为背后的意义时，几乎都是同样的原因：死灵法师。

他们害怕死者会在妄想而嗜杀的渣滓驱使下爬起来杀害自己，于是相信焚烧尸体能让灵魂永远逃出死灵法师枯骨般手指的掌握。

可惜事实并非如此。火焰能烧毁人的肉身，却没有任何火焰能够触及灵魂。

更为不幸的是，死灵法师却可以触到。同时失去身体和自由的痛苦，让许多灵魂在死灵法师的奴役下疯狂了，它们不停地飘荡在风蚀的地宫之中，用种种诅咒与妖法折磨着任何不幸与之遭遇的游荡者。

最糟糕的是那些接受了自己新使命的灵魂，它们的力量会以惊人的速度增长。在马基·埃亚尔，没有任何生物像这些“噩灵”一样如此明显地为存在本身所憎恶——仿佛造物本身也想将它们从这个世界抹去。希望你和更多人能遂她所愿。

    * * *


#{bold}#6、骸骨巨人#{normal}#

死灵法师所谓的“艺术”中最恐怖、最令人作呕的表现之一，就是骸骨巨人。有些野心勃勃的死灵法师不满足于只亵渎一具遗骸，便把无数骷髅的骨架缚在一起，造出比常人高出数倍的丑恶毁灭机器。

将骸骨巨人与法师或炼金术士的傀儡一视同仁是大错特错的。尽管这些法师老头们偏执又古怪，但通常法师们制造傀儡的目的只是用来当苦力或自卫。而死灵法师创造骸骨巨人的唯一目就是制造死亡，对一只骸骨巨人能力的唯一限制竟然只是其创造者扭曲的想象力。你有没有与一向被视为力量象征的雪巨人战斗过？那就想象一下长着六只胳膊的骸骨巨人吧——手指由削尖的肋骨制成，如刀刃般锋利；再想象无数头颅悬挂在这具骸骨巨人每一寸肢体上，它们都尖叫着怒吼着，因为你的每滴鲜血都令其饥渴无比。它用畸形的双手挥舞脊柱作鞭！你若有幸见识了这扭曲的混合体，恐怕会巴不得回到岱卡拉，去欺负那些头脑简单、浑身覆霜的低等类人生物。

    * * *


#{bold}#7、巫妖#{normal}#

他的身体由憎恨组成，他是纯粹的邪恶、死亡的化身，死灵法师的无上杰作。我能明确的告诉你巫妖并不是你想象中的那样，关于它的无数传奇和神话也的确有所失实。

他的恐怖远超于此。

当一名强大的死灵法师最终超越了生死界限后，他从前只能零星借用的地狱力量一下子完全服从于他。传说中，大地莫名的震颤、谷物奇怪的枯萎、树叶的同时凋零都预示着一只巫妖的诞生。作为至高的不死之主，巫妖能瞬间泯灭无数食尸鬼与骷髅，眨眼间将噩灵驱散，片刻就使骸骨巨人灰飞烟灭。

至于消灭巫妖的确切方法嘛……这么说吧，如果你成功的摧毁了这样的怪物，亲爱的请你一定要为我写一篇指南。因为我真的，完全，没有办法。

    * * *`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00164 | HUMAN-REVIEW | cross-batch-039 | advisory | 文风是否收敛由人工定 |  | fix |
| hrq-00165 | HUMAN-REVIEW | cross-batch-039 | advisory | 若要求严格贴合改“尽管如此”；拆段仅在要求结构对应时恢复 |  | fix |
| hrq-00166 | HUMAN-REVIEW | cross-batch-039 | confirmed | 改回“力量/心力/维持其复苏的力量” |  | fix |
| hrq-00167 | HUMAN-REVIEW | cross-batch-039 | confirmed | 改回“因关系网络而成为统治者”“以冰冷的钢铁相待” |  | fix |
| hrq-00168 | HUMAN-REVIEW | cross-batch-039 | confirmed | 去掉男性限定；查授权术语记录后再定 abyssal |  | fix |
| hrq-00169 | HUMAN-REVIEW | cross-batch-039 | confirmed | 删除明确增饰；“有幸”是否保留属文风 |  | fix |

<details><summary>hrq-00164 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“算个屁指南”“弱柳扶风”更粗俗且丢“强风吹散”意象，但叙述者本就口语粗豪
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

<details><summary>hrq-00165 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：尸妖段增“万幸的是”。advisory：单段被拆成多段、标题顿号
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

<details><summary>hrq-00166 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`effort` 两次被具体化为“法力”，固定实现（master-of-bones.lua:233-274）只在施放末尾扣一次法力，无受损程度关联
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

<details><summary>hrq-00167 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：吸血鬼段增译并改写因果（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）。Sol 提醒“严重增译”程度标签不必照收
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

<details><summary>hrq-00168 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：巫妖段强行男性化并增“身体”（源码为复数/中性 `liches`/`they`）。refuted：“巫妖超越传说”被曲解不成立，后句已表达。pending：`abyssal power` 是否必须译“深渊力量”
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

<details><summary>hrq-00169 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：骸骨巨人段多处虚构修饰（“法师老头”“一向被视为力量象征”“每滴鲜血都令其饥渴”“有幸”）
```
```
raw verdict: 吸血鬼段增译与因果改写（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）→confirmed; 骸骨巨人段多处虚构修饰（法师老头、一向被视为力量象征、每滴鲜血、有幸）→confirmed; “算个屁指南”“弱柳扶风”粗鄙化并丢失“强风吹散”意象→advisory; `effort` 两次被具体化为“法力”，固定实现不支持受损程度关联→confirmed; 巫妖段强行男性化并增加“身体”→confirmed; “巫妖超越传说”被曲解→refuted; `abyssal power` 必须译为“深渊力量”→pending; 尸妖段增加“万幸的是”→advisory; 段落切分与标题标点（拆段客观存在、顿号属正常本地化）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。 译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。
```
</details>

## entry-01230

- 位置：`mod-tome.lua:16072`（tome）｜section：`mod-tome/data/lore/high-peak.lua`｜source_tag：`_t`
- 原文：`I am increasingly certain that what I gave my love was not the Blood of Life.

Her demeanor has...  changed, but not in the way one would expect.  If I had given her the essence of some god the Sher'Tul wounded and exsanguinated for a trophy, or a blight-ridden demon, or something else that would affect her mental state, I would expect her to start acting oddly - with more cruelty, more arrogance, less #{italic}#humanity.#{normal}#  Instead...  she acts like she knows the world is about to end and can't tell anyone.  She mutters about needing to use the contents of that ruin, one that we still can't even tell Angolwen #{italic}#exists#{normal}#, to bring about a new order of magocracy like the one Tannen wants "before it's too late."  Something is gnawing at her, and she dreads that I may find out what, but otherwise...  she's almost #{italic}#too#{normal}# rational.

She is terrified of losing me, losing this world, losing #{italic}#herself#{normal}# - but to what, I have no idea.  Ultimately, it does not matter what is running through her mind; I will study the texts in this ruin for summoning rituals, farportal schematics, or something else that would fulfill her plan for her.  She will get to see this "Gerlyk" once, for herself - and then his magic will be absorbed and it will be over.  Whatever this creature is, it can't give orders when it's dead.`
- 现译：`我越来越确信，我给爱人的并非生命之血。

她的举止……变了，却不是预想中的变化。假如我给她的是某位被夏·图尔击伤、放干鲜血作为战利品的神祇精华，或者某个浑身枯萎之力的恶魔精华，又或者任何会影响心智的东西，我本以为她会开始举止反常——变得更加残忍、更加傲慢、少几分#{italic}#人性#{normal}#。然而……她的表现就像知道世界即将毁灭，却不能告诉任何人。她不断喃喃，说必须利用那座遗迹里的东西——我们甚至还不能告诉安格利文这座遗迹#{italic}#存在#{normal}#——建立一种新的魔法统治秩序，就像泰恩所希望的那样，“趁一切还来得及”。有什么东西正啃噬着她，她害怕我会查明真相；可除此之外……她几乎#{italic}#理智得过了头#{normal}#。

她害怕失去我，失去这个世界，失去#{italic}#她自己#{normal}#——可会被什么夺走，我毫无头绪。说到底，她脑中究竟有何念头并不重要；我会研究遗迹里的典籍，寻找召唤仪式、远行传送门图纸，或任何能替她完成计划的东西。她将亲眼见到一次这个“盖里克”——仅此一次；随后他的魔力会被吸收，一切便会结束。不管这个生物是什么，死后就不能再发号施令。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00170 | HUMAN-REVIEW | cross-batch-040 | confirmed | 斜体范围是否收束属排版取舍 |  | no_change |

<details><summary>hrq-00170 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：对应 `elandar-1`，正文与专名含义相符；confirmed：控制标签闭合、标点合理。advisory：`too` 的斜体范围被扩大为“理智得过了头”
```
```
raw verdict: 对应 elandar-1，正文及专名含义相符→confirmed; 控制标签闭合且标点处理合理→confirmed; `too` 斜体范围被扩大为“理智得过了头”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-039-01.md](reports/sol-039-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 refuted、1 pending。 译文未修改。Sol 三条正文核对均以源码条目 ID 对照，正面结论也原样记录。
```
</details>

## entry-01245

- 位置：`mod-tome.lua:16538`（tome）｜section：`mod-tome/data/lore/keepsake.lua`｜source_tag：`_t`
- 原文：`#{italic}#This is a page from what you assume is Kyless' journal.#{normal}#

Berethh found something in the woods...a dead man and a few dead trolls.
At first we thought they killed each other but there weren't any wounds we could see. It was something awful though; you could see it in their faces.
Berethh just wanted to leave. He didn't like the way it felt. But I just couldn't pass up a free opportunity like that.
They had some money on them and some other things which we divided up. The man also had a book, which I took.
I've been studying it. It seems like some kind of magic, but nothing like any of the magic I've heard in stories.
It's more like a language. A way of thinking or calling out with your mind. I'm learning it now.
I hear what sound like whispers in my head. And I've found I can whisper back.
My mind can reach out. Control things. Control people. But there's more. Something is out there. I have to reach out.
Once I've mastered this I may be able to use it to advance in the caravan. I'm tired of just being a porter.
`
- 现译：`#{italic}#你感觉这应该是凯勒斯日记中的一页。#{normal}#

贝里斯在森林中发现了什么——一具男尸和几具巨魔尸体。
一开始我们以为他们同归于尽，身上却看不出任何外伤。可他们显然遭遇了什么可怕的事，从他们脸上就看得出来。
贝里斯只是想离开。他不喜欢这种诡异的气氛。但这种白捡的便宜，我怎么可能错过。
他们身上有一些钱和其他东西，我们瓜分了它们。那人身上还有一本书，我拿走了它。
我一直钻研着那本书。那看起来似乎是某种魔法，但是却不像任何传说中所述的魔法体系。
这更像是某种语言。一种用心灵思考或呼唤的方式。我正在学习这种语言。
我听见脑海中传来窃窃私语般的声音。我发现自己也能以低语回应。
我的心灵能够向外探触。我可以控制物体，控制别人。但还不止如此。外面还有某种存在。我必须把心灵探得更远。
一旦我掌握了它，也许就能靠它来帮我在商队中获得晋升。我已经厌倦了只能当搬运工。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00171 | HUMAN-REVIEW | cross-batch-040 | confirmed | 是否顺译该破折号结构 |  | no_change |

<details><summary>hrq-00171 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：对应 `keepsake-kyless-journal-2`，正文、标签与叙事准确。advisory：“发现了什么——”有不定代词直译痕迹
```
```
raw verdict: 对应 keepsake-kyless-journal-2，正文、标签与心灵操控叙事准确→confirmed; “发现了什么——”略有不定代词直译痕迹→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-039-01.md](reports/sol-039-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 refuted、1 pending。 译文未修改。Sol 三条正文核对均以源码条目 ID 对照，正面结论也原样记录。
```
</details>

## entry-01247

- 位置：`mod-tome.lua:16562`（tome）｜section：`mod-tome/data/lore/keepsake.lua`｜source_tag：`_t`
- 原文：`#{italic}#This is a page from what you assume is Kyless' journal.#{normal}#

I've come so far in the last year. The other merchants listen to me now. They think I have a real gift for trade.
The weak-minded peasants we trade with are so easy to control though. They practically give me their money.
But the real money and power rests with the bandits. Those two that ambushed me got what they deserved. So did the rest of their camp.
The fear on their faces when I struck was priceless. They must have had more gold than the caravan makes in a year!
I got some help carrying it off to a nearby cave. A few more encounters like that and I'll be rich.
Until then, I'll stay with the caravan. The only prolem is Jak. He doesn't trust me.
I guess I threaten his authority. Not sure what I'll have to do about that...
`
- 现译：`#{italic}#你感觉这应该是凯勒斯日记中的一页。#{normal}#

在过去一年内我进步神速。现在其他商人都愿意听从我了。他们认为我真的有商业天赋。
那些跟我们做买卖的农民意志薄弱，实在太容易控制了。他们简直是在把钱白送给我。
但是真正的钱财与力量却掌握在那些强盗手里。上次那两个偷袭我的人已经得到了他们应有的惩罚。他们营地里的其他人也一样。
我攻击他们时，他们脸上惊恐的表情令我感到无比快意。他们的黄金想必比商队一年赚的还多！
我叫了些帮手帮我把战利品抬到附近的洞穴里。再有几次这样的遭遇，我就能发财了！
在那之前，我还会和商队呆在一起。眼下只有一个问题，那就是贾克。他并不信任我。
我猜是因为我对他的权威构成了威胁。我还不知道该怎么处理这件事……
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00172 | HUMAN-REVIEW | cross-batch-040 | confirmed | 是否按规范改“待在”，属用字规范决定 |  | fix |

<details><summary>hrq-00172 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：对应 `keepsake-kyless-journal-3`，剧情准确；confirmed：`priceless` 译“令我感到无比快意”合乎语境；refuted：把该译法当误译的主张不成立。pending：“呆在一起”通假俗写规范应为“待在一起”
```
```
raw verdict: 对应 keepsake-kyless-journal-3，人物与强盗藏金剧情准确→confirmed; `priceless` 译“令我感到无比快意”是合乎语境的意译→confirmed; 将该译法视作误译的主张→refuted; “呆在一起”通假俗写，规范应为“待在一起”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-039-01.md](reports/sol-039-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 refuted、1 pending。 译文未修改。Sol 三条正文核对均以源码条目 ID 对照，正面结论也原样记录。
```
</details>

## entry-01252

- 位置：`mod-tome.lua:16622`（tome）｜section：`mod-tome/data/lore/keepsake.lua`｜source_tag：`_t`
- 原文：`A figure squats in the darkness with his face turned your way. At first you're not sure if Kyless recognizes you.
His face seems twisted by hunger and madness. But soon it softens and he begins to look more like the Kyless of old.
He speaks your name in recognition but doesn't move. Slowly, almost imperceptibly, the air in the room begins to change.
A charge seems to fill the space around you. Small gusts of wind pick up and scatter dust across the floor.
You feel as if the room itself is coming to bear upon you. Kyless smiles and then attacks.
`
- 现译：`黑暗中蹲伏着一个面朝你的人。一开始，你无法确认凯勒斯是否认出了你。
他的面容仿佛因饥饿与疯狂而扭曲。但很快，他的神情缓和下来，渐渐恢复了昔日的模样。
他一动不动，叫出了你的名字。慢慢地，你发觉这个空间里的空气发生了几不可察的变化。
你感到四周仿佛充满了某种能量。阵阵微风吹起，卷散了地面上的尘土。
你感到整个空间似乎都压向了你。凯勒斯嘴角扬起一抹微笑，向你发起了攻击……
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00173 | HUMAN-REVIEW | cross-batch-041 | confirmed | 无必办项 |  | no_change |

<details><summary>hrq-00173 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：整体未发现问题。advisory：句号改省略号属修辞润色
```
```
raw verdict: 整体未发现问题→confirmed; 句号改为省略号属于修辞润色→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01256

- 位置：`mod-tome.lua:16683`（tome）｜section：`mod-tome/data/lore/kor-pul.lua`｜source_tag：`_t`
- 原文：`Aha, I have found the accursed undead that plague this nefarious dungeon! The skeletal fool was thankfully no match for me! I suppose it helped that he had no arms...

I've found myself an old shield that in spite of a few dents seems serviceable enough. Some of these rats are BIG, and giving them a strong bash with the shield helps to stop their poisonous bites before I get my sword to their necks. I also found a few gems - I may have to hunt round for more. Not out of any personal greed of course, but my noble quest requires that I gather resources to defeat the great evils in this land and back home!

Diamonds are my favourite, so sparkly.`
- 现译：`啊哈，我总算找到了占据这邪恶地牢的可憎不死族！谢天谢地，那个骷髅蠢货根本不是我的对手！不过我想，它没有双臂大概也帮了点忙……

我在这找到了一面老旧的盾牌，它虽有几处凹痕但仍堪用。这里有些老鼠特别大，给它们一个强力的盾击能在我用剑切开它们脖子前阻止它们带毒的撕咬。
我还发现了一些宝石——看来我得继续四处搜寻更多宝石。必须申明的是，这肯定不是出于任何贪念，只是因为我崇高的任务需要我收集更多的资源，好打败这里和故乡的强大邪恶势力！

我最喜欢钻石了，一闪一闪亮晶晶～。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00174 | HUMAN-REVIEW | cross-batch-041 | confirmed | 并回段落、去重标点 |  | fix |

<details><summary>hrq-00174 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二段被额外单换行切开；confirmed：末尾 `～。` 标点连用
```
```
raw verdict: 第二段被额外单换行切开→confirmed; 末尾存在 `～。` 标点连用→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01259

- 位置：`mod-tome.lua:16826`（tome）｜section：`mod-tome/data/lore/last-hope.lua`｜source_tag：`_t`
- 原文：`#{italic}#A study into Southspar's most unusual ruler.#{normal}#

Chances are you haven't heard of Southspar.

And why would you have? It was naught but a tiny, provincial island kingdom off the coast of Tar'Eyal that existed within the Ages of Allure and Dusk. By all accounts, Southspar was a pleasant place to live; temperate climate, healthy trade relations with mainland human kingdoms, and by great luck, the island upon which the kingdom sat held great deposits of the much-valued metal stralite.

Despite this good fortune though, Southspar was doomed to mediocrity. Why? The actions of its ruler. By all accounts a bumbling, octogenarian dotard, his name lost to the mists of time, this mouldy monarch mismanaged Southspar almost to its demise. The Dwarves of the Iron Throne, having heard of the stralite beneath the island, manipulated the king into mining it and selling it to them for a fraction of its true worth. Also, despite Southspar's decidedly puny military power, the king saw fit to send whatever troops he could muster to aid mainland human kingdoms in their great and many wars against the halflings, who up to this point had barely registered Southspar's existence. Not only were the undertrained, ill-equipped troops crushed like vermin before the superior halfling forces, but also these foolhardy attacks succeeded in attracting the halflings' attention to their secluded island. Almost immediately, the raids began.

From what records remain, the king was mystified by the decline of his nation, believing to the end that every action he took had been the right one. He passed away soon after the halfling raids began. Whether it was suicide, assassination, or simple old age is unknown. The king never married and had no children, the only remaining member of his family being a distant cousin, a young man named Drake.

And so it was that Drake ascended to the throne, and Southspar entered a golden age.

#{bold}#1. Drake and the Halfling Horde.#{normal}#

To the newly crowned Drake, the most obvious and immediate threat to Southspar was the growing raids and sorties being held by the halflings. To this end, he ordered a complete and total reconstruction of Southspar's military, turning them from a ragtag bunch of militia into a small yet devastatingly efficient engine of war. Drake knew that the only advantage his forces held over the halflings was their knowledge of the island, and so bade them to travel stealthily, carry small, armour-defeating stralite knives rather than spears and swords, and only engage with the halflings strictly on their own terms. Southspar's newly assembled "Army of Rogues" was a success. Although the halflings were great in number, strike after surgical strike from Drake's army weighed heavily on their morale, and finally, grumpily declaring Southspar "not worth the bother", the halfling forces withdrew.

Southspar celebrated its peace and its newly found military might, but for Drake, the celebration was short-lived. The stralite he had used to craft his Army of Rogues' knives and armour was stralite that wasn't going into the Dwarves' pockets, and they were far from happy. Drake formulated a plan - by the time he was through, the Dwarves would be even further from happy.

#{bold}#2. Drake and the Stralite Stratagem.#{normal}#

The Dwarves have always been a secretive race. Even now only a select few know the location of their "Iron Council", and in the days of Southspar there were still those who considered Dwarves nothing but myth. Being a monarch in possession of large amounts of stralite can open even the most concealed of doors, however... Drake had requested an audience with the Iron Council, and the Dwarves, expecting said audience to be a humble apology and promises of further stralite for the gold they were paying, readily accepted.

What they got, in reality, was quite different. Gone was the ineffectual king of Southspar's past, and now the Dwarves found themselves facing a young, hard-eyed human who was demanding that the amount of gold that the Dwarves were paying for Southspar's stralite be increased twenty-fold.

To say the Dwarves scoffed at this would be an understatement; open, derisive laughter hits nearer the mark. Despite Southspar's recent repulsion of the halflings, the Dwarves of the Iron Throne saw no problem in taking Southspar's stralite by force. In his heart, Drake knew they could accomplish this, and it was to this end that he had brought the small pouch around his neck to the Council.

Drake held the small, drakeskin pouch high, opened it and emptied its contents onto the floor: Stralite, ground to dust, muddied with dirt and base metals, made unusable and worthless. The Dwarves of the Council gasped in horror at this waste, one (if rumours are to be believed) even fainting on the spot. Drake went on to say that, if his demands were not met, the entirety of the stralite beneath his island would meet the same fate as the stralite cast upon the chamber's floor.

By the time Drake left the Iron Council, the Dwarves had agreed to pay thirty times the previous amount.
`
- 现译：`#{italic}#对南晶岛不同寻常统治者的研究报告#{normal}#

你可能从未听说过南晶岛。

为什么你从未听说过呢？因为这是一个穷乡僻壤的岛国，在厄流纪和黄昏纪时，它坐落于塔·埃亚尔的海岸边。人人都说，南晶岛是一个适宜居住的地方：温和的气候，与大陆上的人类王国保持着良好的贸易关系，最幸运的是，整个王国坐落的这个岛屿拥有丰富的斯莱特矿脉。

尽管拥有这样的好运，南晶岛仍注定平庸一生。为什么？一切都要归咎于它的统治者。据说，那是一个行事笨拙、年逾八旬且老糊涂的国王，他的名字早已被时间掩盖，他腐朽的统治几乎葬送了整个南晶岛。钢铁王座的矮人们，自从听说这岛屿下埋藏了很多斯莱特矿，便利用这个国王去开采并将斯莱特以一个极低的价格卖给他们。同时，尽管南晶岛只有微不足道的军事力量，老国王仍执意把能召集到的军队派去援助大陆上的人类王国，参与他们与半身人的多场战争；在此之前，半身人甚至几乎不知道南晶岛的存在。他们训练不足、装备落后的部队不但在半身人强大的军事力量下如害虫般被碾碎，这些莽撞的进攻还成功吸引了半身人对偏僻岛屿的注意。袭击几乎随即开始。

从现存的记录来看，国王对国家的衰落困惑不已，直到最后仍坚信自己的每一步都是正确的。在半身人开始袭击后不久，他便去世了。不管这是自杀、暗杀或者老死，都成了一个谜。老国王从未结婚，没有子女，他的家族剩下的只有他的远房表亲——一位叫德瑞克的少年人。

所以德瑞克继承了王位，南晶岛也由此进入了黄金时代。

#{bold}#1、德瑞克和半身人部落。#{normal}#

对于新加冕的德瑞克，最大也最明显的威胁来自半身人日益频繁的袭击和出击。为此，他下令彻底重建南晶岛的军队，将一群乌合之众般的民兵改造成规模虽小却极其高效的战争机器。德瑞克知道，己方对半身人唯一的优势就是熟悉岛上地形。因此，他命令部队隐秘行动，携带小巧而能破甲的斯莱特匕首，不用长矛和刀剑，并且只在对己方有利的条件下与半身人交战。南晶岛新建的“游击军”取得了成功。半身人虽人数众多，德瑞克的军队一次次精准打击却沉重挫伤了他们的士气；最后，半身人恼怒地宣称南晶岛“不值得费事”，撤军而去。

南晶岛欢庆胜利和它新建的游击力量。但是对德瑞克来说，这番庆祝没有持续多久。他用于打造游击军匕首和护甲的斯莱特没有落入矮人的口袋，他们为此十分不满。德瑞克已经拟定了一个计划——等计划完成，矮人们会更加恼火。

#{bold}#2、德瑞克和斯莱特战略。#{normal}#

矮人一直是个神秘的种族。即便如今，也只有极少数人知道他们的“钢铁议会”位于何处；而在南晶岛存在的年代，仍有人认为矮人不过是神话。然而，一位拥有大量斯莱特的国王，就连最隐蔽的大门也能敲开……德瑞克请求钢铁议会接见。矮人们以为这次会面会是一场卑躬屈膝的道歉，并承诺按他们支付的价钱继续供应斯莱特，于是爽快地答应了。

但实际上，矮人们发现理想和现实有很大的差距。昏庸的老国王去世了，他们面对的是一位年轻、目光冷硬的人类——这位年轻人甚至要求矮人们把南晶岛斯莱特的收购价提高到原来的二十倍。

说矮人对此嗤之以鼻都算轻了；他们分明是在放声讥笑。尽管南晶岛不久前才击退半身人，钢铁王座的矮人仍认为以武力夺取岛上的斯莱特毫无困难。德瑞克心里清楚他们确实做得到，正为威慑他们，他才把颈间的小口袋带到了议会。

德瑞克高举着这只龙皮口袋并打开了它，里面的物品掉落了一地：磨成粉并掺杂了杂质和其他金属的斯莱特——这种斯莱特无法使用且毫无价值。议会的矮人们震惊于这种恐怖的浪费，某个矮人（如果传闻是真的）甚至晕了过去。德瑞克继续说，如果不满足他的要求，整个南晶岛蕴藏的斯莱特矿都会变成这样。

当德瑞克离开钢铁议会时，矮人们以30倍的价钱签订了协议。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00175 | HUMAN-REVIEW | cross-batch-041 | confirmed | 专名与职业双关待术语核对；序号统一 |  | fix |

<details><summary>hrq-00175 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`peace` 译“胜利”；confirmed：`newly found military might` 被窄化；confirmed：`Army of Rogues` 译“游击军”损失命名词义；pending：是否必然是 Rogue 职业双关；advisory：标题序号与二十/30 写法不统一
```
```
raw verdict: `peace` 译成“胜利”→confirmed; `newly found military might` 被窄化为“新建的游击力量”→confirmed; `Army of Rogues` 译“游击军”损失命名词义→confirmed; 必然是 Rogue 职业双关→pending; 标题序号及二十／30 写法不统一→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01262

- 位置：`mod-tome.lua:17299`（tome）｜section：`mod-tome/data/lore/last-hope.lua`｜source_tag：`_t`
- 原文：`#{bold}#
Here rests Raymond Gaustadnes
#{normal}#84 - 120#{italic}#
The Pixels finally got him...
#{normal}#`
- 现译：`#{bold}#
雷蒙德·加斯塔德在这里长眠
#{normal}#84 - 120#{italic}#
像素们终于还是逮到他了……
#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00176 | HUMAN-REVIEW | cross-batch-041 | pending | 需专名/彩蛋依据才能定 |  | defer |

<details><summary>hrq-00176 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：`Gaustadnes` 漏译 `-nes`；pending：是否为对 ToME 像素画师的致敬
```
```
raw verdict: Gaustadnes 漏译末尾 `-nes`→pending; 这是对 ToME 像素画师的致敬→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01263

- 位置：`mod-tome.lua:17473`（tome）｜section：`mod-tome/data/lore/last-hope.lua`｜source_tag：`_t`
- 原文：`#{bold}#
Foursaw the Clown
#{normal}#82 - 114#{italic}#
We laughed
Until we saw
The joke was over
#{normal}#`
- 现译：`#{bold}#
小丑先觉
#{normal}#82 - 114#{italic}#
我们笑着
直到察觉
笑话已经结束
#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00177 | HUMAN-REVIEW | cross-batch-041 | confirmed | 无必办项 |  | no_change |

<details><summary>hrq-00177 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：格式与年份无问题。advisory：“先觉/察觉”双关译法可议
```
```
raw verdict: 格式、年份均无问题→confirmed; 先觉／察觉成功传达双关→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01267

- 位置：`mod-tome.lua:17570`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`#{bold}#Tract of Anarchy#{normal}#

For the years following the cataclysm, chaos reigned. Their culture, their way of life, it was as broken and fractured as the land itself. Nalorë civilisation was reduced to a few isolated and feeble settlements, scratching out meagre existences as land, mind and body was warped in both shape and spirit.

Faced with the idea of their great race failing – another victim of the Spellblaze, a footnote in the annals of history – impassioned pleas were sent to their elven brothers: The Shalorën, the Thalorën. Aid was even requested from human and halfling, embroiled in their own petty squabbles as they were.

The Nalorën received no answer.`
- 现译：`#{bold}#无序之治#{normal}#

大灾难之后的那些年里，混乱当道。他们的文化，他们的生活方式，都如同这片大地本身一样支离破碎。纳鲁文明只剩下几个孤立而脆弱的定居点，在土地、心智与肉体形神俱扭的境况中勉强求生。

面对自己这个伟大种族行将覆灭的前景——沦为魔法大爆炸的又一个牺牲品，史书上的一个脚注——他们向兄弟种族永恒精灵与自然精灵发出了恳切的求援。他们甚至向彼时正深陷自家琐碎内斗的人类和半身人求助。

纳鲁精灵没有收到任何回应。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00178 | HUMAN-REVIEW | cross-batch-041 | confirmed | 统一系列译名，标题按 `Tract` 更正 |  | fix |

<details><summary>hrq-00178 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：正文标题把 `Tract` 错成“治”并与系列译法冲突。refuted：“拾取名与打开名不一致”的说法；refuted：“无序之治”逻辑自相矛盾
```
```
raw verdict: 正文标题把 `Tract` 错成“治”并与系列译法冲突→confirmed; “拾取物品名是无序之卷、打开变无序之治”的说法→refuted; “无序之治”本身严重逻辑自相矛盾→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。 译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。
```
</details>

## entry-01270

- 位置：`mod-tome.lua:17594`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`At long last, the temple finally reveals its secrets to me, and my plans can be set in motion. Lithe in form, faultless in combat, unmatched in speed both above the waves and beneath... nature couldn't have hoped to create such a race as nagas. With the Temple of Creation now open to me however, we may become so much more. With my guidance, my careful shaping of the Sher'Tul's magicks, under my expert hand our great race shall soon reach its zenith. A new tract shall soon be written: The Tract of the Devourer.
`
- 现译：`终于，神庙向我敞开了神秘之门，我的计划终于可以实施了。柔软的身体，完美的战斗能力，无与伦比的两栖机动性……大自然怎么会创造出娜迦这样的种族？不管怎样，当造物主神庙之门为我打开，我们可以变的更加强大。在我的指引和对夏·图尔魔法的仔细改造下，我们的伟大种族会很快趋于巅峰。新的篇章即将写就：《吞噬者之卷》。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00179 | HUMAN-REVIEW | cross-batch-042 | confirmed | 术语对齐 + 改“得” |  | fix |

<details><summary>hrq-00179 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：娜迦赞叹句语气失真；confirmed：“Temple of Creation”术语不一致；confirmed：“变的”应为“变得”
```
```
raw verdict: 娜迦赞叹句的语气失真→confirmed; “Temple of Creation”术语不一致→confirmed; “变的”应为“变得”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01271

- 位置：`mod-tome.lua:17598`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Dear Rolf,

I hope this letter finds you well. I must apologise for this recent dry spell in our communication; my adventures across Maj'Eyal have taken many exciting and perilous turns as of late. What turns do I speak of, you ask? I know how you delight in reading the accounts of my exploits, so I shall waste no further time on this pre-amble.

Imagine, if you will, a wolf. Imagine a beastly wolf, a wolf with strength, ferocity and a lust for flesh matching that of an entire pack of its lesser kind. You too may have some small experience with these "wargs" as the locals are wont to call them. Now... imagine one the size of a bear. Truly, as I travelled the lands surrounding Derth did I come across such a monstrous, awe-inspiring, lupine adversary. With fangs of a length to match my own blade, I entered combat against this lupine lord and its skulking brood. To my regret I failed in slaying the beast, but I assure you - simply surviving against such feral rage is an honour worthy of recognition and renown.

And indeed, would there have been much glory in killing such a creature? True, I would have had enough to fur to line each and every boot and hat in Derth, but legends must live on. They are what give this world its very spirit!

With eager anticipation for your reply,
Weisman`
- 现译：`亲爱的罗尔夫，

我希望这封信可以安全的到达你手。我必须为我们最近这段时间疏于联系道歉：最近，我在马基·埃亚尔各地的冒险经历又有了许多惊险刺激的转折。你问我说的是什么转折？我知道你很喜欢阅读我的冒险事迹，所以客套话我就不多说了。

想像一下，一只庞大如熊的饿狼，赤眼如炙，饥渴的吞噬着它周围一切的生命。这只暴君所带来的威胁远超一整群它弱小的同类。你也许亦曾对付一些当地人口中所谓的座狼，但想象一下这只如同熊一般巨大的“好家伙”。事实上，当我在周围的旅行时，不巧就遭遇到了这样一只令人生畏的贪婪怪物，它挥舞的獠牙比我的剑还要长。于是我与这只座狼王和它的狼子狼孙们展开了激烈的搏斗。可惜的是我最终并没有杀死这只野兽，但我能自豪的说，能从这场战斗中存活就已经是值得称道的了。

再说，杀死这样的生物又能有多大荣耀呢？对，我确实会得到一大堆狼毛，多到足以给德斯镇每双靴子和每顶帽子做毛皮衬里，但我的内心告诉自己这种传说中的生物必须让其繁衍下去。因为正是它们，赋予了这个世界真正的灵魂！

殷切的期盼着你的回信，
威斯曼`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00180 | HUMAN-REVIEW | cross-batch-042 | confirmed | 补地名、按原文结构重写 |  | fix |

<details><summary>hrq-00180 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏掉德斯镇；confirmed：递进结构被打乱并加入原文没有的描写；confirmed：“挥舞的獠牙”误写动作；confirmed：“让传说延续”被改成“让生物繁衍”
```
```
raw verdict: 漏掉德斯镇→confirmed; 递进结构被打乱并加入原文没有的描写→confirmed; “挥舞的獠牙”误写动作→confirmed; “让传说延续”被改成“让生物繁衍”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01272

- 位置：`mod-tome.lua:17618`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Dear Weisman,

Ah! What feelings your last letters inspired within me... primarily mirth, with a good amount of scorn! Must you continuously assail me with tale after tale of your waving of wooden swords and pestering of toothless mongrels? Allow me to recount your "legends" in a much more succinct manner: One day, I failed to kill a dog. Such bravery! Such pluck and derring-do!

Your petty escapades are made ever more insignificant by the trials I myself have recently overcome. Mere days ago I was trekking through the Old Forest (that's outside Derth, Weisman! Terror must already grip you!) when, by unfortunate happenstance, I came across a most hideous, bloated, oozing and chittering horror! No less than the giant ants' repulsive progenitor! Such hordes of frenzied chitinous young it had at its command, it was as though the ground itself was swarming forward to devour me!

And yet I live. Weisman, I sincerely hope that my letter has revealed to you your folly. Only when you have faced true danger can you call yourself an adventurer. Bore me with your tales no longer.

Rolf`
- 现译：`亲爱的威斯曼，

哈哈，你上次的来信真是带给我不少笑料！你这家伙到底要用这些挥舞木剑、纠缠没牙野狗的故事骚扰我到几时？就让我来演示一下你那封信件的正确读法：有一天，我没能杀死一只狗。这真是充满勇气！

你的“英雄事迹”在我近日克服的可怕梦魇面前根本不值一提。数天前我徒步穿越了远古丛林（这可是在德斯镇之外的地域，威斯曼！你可是要被吓的腿软了吧！）在那里，我不幸的遭遇了世上最可怕、最犀利、最凶猛的生物！

满地的史前巨型白蚁，它们在可怕的蚁王指挥下蜂拥而出，试图用那巨大的前颚将我碎尸万段！

即便如此我还是活下来了，威斯曼，我真心希望我的回信能让你知道世界如此巨大，你又如此渺小。只有当你真正经历过像我这样的生死考验后，才配真正称自己为冒险家。别再用你幼稚的故事来烦我了。
罗尔夫`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00181 | HUMAN-REVIEW | cross-batch-042 | confirmed | 专名与句法按源码回改 |  | fix |

<details><summary>hrq-00181 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：Old Forest 专名偏离；confirmed：巨蚁始祖被实质改写；confirmed：外观与群体动作被改写；confirmed：漏译 `Such pluck and derring-do!`。advisory：自然段被拆分
```
```
raw verdict: Old Forest 专名偏离→confirmed; 巨蚁始祖被实质改写→confirmed; 怪物外观与群体动作被改写→confirmed; 漏译 `Such pluck and derring-do!`→confirmed; 自然段被拆分→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01273

- 位置：`mod-tome.lua:17637`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Dear Rolf the Antslayer,

Ha! Such trials you have overcome! Forget dragons and demons, here we have a hero who has survived against ants! I shall deliver this joyous news to Last Hope with all haste - perhaps there shall be a parade in your honour!

I hope you registered the sarcasm in my previous words, but I obviously cannot expect much from one who struggles with insects. Allow me to share with you knowledge of a beast rather more fitting for a true adventurer to behold. My travels had taken me south, and as I walked one night along an abandoned mountain pass, imagining what treasures and trials the next day may bring, a brilliant light filled my vision! I stood in its radiance, the land around me illuminated so that it almost appeared to be in broad daylight, and that was when I saw it.

Such a magnificent sight! With wings of fire, leaving the air itself hissing and smouldering in its wake, I could only watch with rapt amazement as it alighted on a rocky outcrop mere yards away from me, the stone beneath its talons warping from its tremendous heat. It was at that moment, Rolf, that I realised that this was what being an adventurer was about - there is always more in this world of ours to amaze and astonish us.

Learn from my experiences,
Weisman`
- 现译：`亲爱的弑蚁者罗尔夫，

哈！你克服了何等的艰难险阻！去他妈的巨龙与恶魔，这下我们有了一位战胜了蚂蚁的英雄！我真该用加急快递将你这英雄事迹传到最后的希望，也许那里的人会为你的壮举准备一场隆重的庆典！

我希望你听懂了我之前话语中的讽刺，不过对一个连虫子都对付不了的人，我显然也指望不了太多。

请允许在下与你分享这一则真正冒险家必备的野兽知识吧。我一路向南，当某天晚上我途径一条废弃的山道，我正满脑子想着第二天将会遇到的刺激冒险与惊人的宝藏时，突然一道冲天的亮光几乎闪瞎了我的双眼！在这光芒之下，我的四周亮如白昼，便是此时我看见了它。

真是难以言喻的壮丽景象！巨鸟煽动着烈焰之翼，所过之处空气本身都嘶嘶作响、余烟袅袅。

我惊讶地看到它停在几码之外的岩石上。它立足的岩石亦在那灼人的高热下扭曲变形。就在此时，我总算明白了成为一名冒险家的真正意义，我们这个世界上，总还有更多令人惊叹、令人震撼的事物。

希望你能从我的经验里学到些什么。
威斯曼`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00182 | HUMAN-REVIEW | cross-batch-042 | confirmed | 删增饰与粗口，口吻取舍 |  | fix |

<details><summary>hrq-00182 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：无依据加入“巨鸟”且“煽动”用字错误；confirmed：“去他妈的”加入原文没有的粗口。advisory：“加急快递”现代口吻；advisory：两处段落拆分
```
```
raw verdict: “加急快递”存在明显现代口吻→advisory; 无依据加入“巨鸟”且“煽动”用字错误→confirmed; “去他妈的”加入原文没有的粗口→confirmed; 两处段落被拆分→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01275

- 位置：`mod-tome.lua:17677`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Weisman,

The tentacles. I still remember them. They have lashed into my mind as they lashed into my flesh. How can nature abide such a... a... being in her realm? What dark plane of existence could it have been born from? How can creation itself tolerate such an aberration?!

How did we survive? I have no clue. All I can remember is pain, and panic, and fear. All I could think of was getting away, fleeing... to my shame, all other thoughts left me. Thoughts of you, home, the world... all I could do was keep hacking away at the... things between myself and freedom. Perhaps that is why it didn't... no. I shall not think on it. The beast is certain to fill my nightmares tonight, I won't allow it to fill my waking thoughts.

Rest easy, brother. It may have taken your eye, but think of what else it could have taken. Anyway, I shall be leaving for the tavern soon. Maybe I can drown the images of that monster in a sea of ale.

Make sure you write the words on your next letter nice and big,
Rolf`
- 现译：`威斯曼，

该死的触须，我仍然记得他们。他们插入我血肉的同时也侵入了我的思维。大自然怎能忍受这样的……怪物……存在于自己的领域？这可怕的生物究竟来自何等黑暗的位面？造物主本身是如何忍受这样恐怖存在的？！

我完全不记得我们是如何幸存下来的。残存的记忆里只有痛苦、惊慌与恐惧。依稀记得当时大脑里唯一的念头就是我必须立刻逃走，远离这个鬼地方……惭愧的是，当时其它所有的想法都离我而去。

对于你的牵挂，对于家的怀念，对于世界的眷恋，都已经被我抛诸脑后，唯一萦绕在脑子里的想法就是不停劈砍挡在我与自由之间的……那些东西。

也许这就是为什么它没有……不！也许我不应该再想它了。既然这野兽一定会在我今晚的噩梦中出现，至少清醒时我不能允许它再充斥我的大脑。

好好休息吧，兄弟，它虽然夺走了你的眼睛，但想想最坏的情况下它本会夺走……不管怎么说，我马上就要前往酒馆了，希望麦芽酒能让我从恐惧中缓解出来。

希望你下封信上的字又大又美，
罗尔夫`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00183 | HUMAN-REVIEW | cross-batch-042 | confirmed | 重译该句、代词回正 |  | fix |

<details><summary>hrq-00183 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`nice and big` 误成“又大又美”；confirmed：触手代词及动作有偏差。advisory：内心独白拆成三段
```
```
raw verdict: `nice and big` 被误解成“又大又美”→confirmed; 触手代词及动作均有偏差→confirmed; 内心独白被拆成三段→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01277

- 位置：`mod-tome.lua:17714`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Weisman,

By my ancestors' profits I hope you receive this message in good health and spirits. Please, old friend - there is no need to impress upon me your valour, I know full well how courageous you are. Please, do not go after that... that thing! If I must drag you away physically, that is what I shall do, but I beg of you, please, consider another foe to fight!

Your friend,

Rolf.`
- 现译：`威斯曼，

祖先保佑，你接到这封信时身体安康。老朋友，你没必要向我证明你的勇武，我已完全了解你是多么的勇敢。请千万不要回去和那东西战斗！如果非得我亲自把你拖走，那我就这么做。但我还是求你，换个战斗的对手吧！

你的朋友，

罗尔夫。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00184 | HUMAN-REVIEW | cross-batch-042 | pending | 双关需彩蛋/设定依据 |  | fix |

<details><summary>hrq-00184 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“profits”财富意象被抹平。pending：罗尔夫是否确定是矮人、是否 profits/prophets 双关
```
```
raw verdict: “profits”财富意象被抹平→advisory; “罗尔夫确定是矮人”及 profits/prophets 双关→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01278

- 位置：`mod-tome.lua:17728`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Last Will and Testament of Rolf Two-Axes

I have failed. Oh by the great wyrm's maw, I have failed! The beast Weisman set out to slay was dead already by another's hand, but its corruption remained still. When I arrived in its chamber, Weisman was already half-gone; he was hacking away at foes only he could see. When I tried to stop him, he turned his axe on me... I am beaten and broken, hiding in some crevasse away from... from my own friend, who through the corruption in this place has been perverted into a monstrosity my axes were unable to fell. I hold no doubt that this is the last time I shall put quill to parchment, as even now I can hear my old friend's perverted voice.. calling to me. I bequeathe my belongings to any who slay ...
#{italic}#(the ink blotch seems to indicate Weisman had caught up to his old friend, one-half of that abomination)#{normal}#`
- 现译：`双斧罗尔夫的遗嘱

我失败了。啊，以巨龙之巨口起誓，我失败了！威斯曼此行本要猎杀的那头野兽，早已死在他人之手，但它的腐化仍然残留于此。当我赶到它的巢穴时，威斯曼已经神智尽失；他正朝着只有他自己看得见的敌人挥斧乱砍。我想要阻止他，可他把斧头转向了我……我遍体鳞伤、心力交瘁，只能躲进某道裂隙中，躲开……躲开我自己的朋友，他已被此地的腐化扭曲成我的双斧无法放倒的骇人怪物。我毫不怀疑这是我最后一次提笔，因为此刻我已能听见老友那扭曲的声音……在呼唤着我……我之财物将赠予任何能杀死…
#{italic}#（这点点污渍似乎叙说着威斯曼最终抓住了他的老朋友，他们以这种怪物的形式永远地团聚在了一起）#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00185 | HUMAN-REVIEW | cross-batch-042 | confirmed | 改回客观旁注、收束程度词 |  | fix |

<details><summary>hrq-00185 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：旁注改成煽情式“永远团聚”；confirmed：`half-gone` 译“神智尽失”程度过重。refuted：并非完全抹掉“两人合为怪物”机制
```
```
raw verdict: 旁注由客观记录改成煽情式“永远团聚”→confirmed; 译文完全抹掉“两人合为怪物”机制→refuted; `half-gone` 译成“神智尽失”程度过重→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01280

- 位置：`mod-tome.lua:17737`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`#{italic}#This scroll looks ancient, possibly going back millennia, but has been incredibly well-preserved.#{normal}#

I remember when I first woke, and I drew my first breath, and the fresh young air of the world filled me with vitality. I opened my eyes, and above me stood a figure of outstanding radiance. She was tall and slim, crowned in silver hair that fell to the ground in silken tresses. Her skin was pale to the point of luminance, and her eyes were brighter than the stars.

I watched her for what felt like a century, and she watched me, and I saw tears form in her eyes. I did not have a voice yet, but I thought, "Why does she look so sad?" And I felt then her reply in my thoughts, "For you are beautiful, and far more beautiful than all else in the world. But this is a world of pain and sorrow, and I cannot bear to think of my creation come to harm. I will give you strength to endure many years, and a voice to express all desires, but the burden of sadness will follow you forever. At that thought I weep..."

I felt then strength come into my limbs, and a voice rise in my throat. I rose to the ground and I looked around, and in awe of the world around me and the stars above me I sang loudly for joy. And the woman smiled as she heard my voice, and her tears stopped, so I continued to sing for a while to entertain her. But then I said, "Am I alone?" She nodded, and said, "There are no others like you." At this I felt sad, and she could see the loneliness in my heart. She seemed to hesitate a moment, and said, "Though it pains me, I cannot deny your desires. You will sleep now, and when you awaken you will be among people like yourself, and you will walk out into this broken world and try to mend it."

As she finished speaking I instantly fell into a trance, and when I awoke I saw the world had changed, and there was now a blazing light in the sky - it was the new-born Sun. And I saw all around dozens more people like me, and others similar in appearance but varying in traits and abilities. I woke them up, and gathered them together, and we all expressed delight in each other's being, and named ourselves Alor?. But the woman was gone, and no others knew anything about her, and my searches for any trace of her were in vain.

Times passed and changed, and other creatures were found, and oft they were fell and vile and we did war with them. Then we found the Sher'Tul, and they delighted in our beauty, and taught us the ways of the Arts. And then the War came, and some of us helped them in their battles, but soon we saw we had no place beside such masters, and we retreated to the woods as the War raged to its catastrophic conclusion.

In all those centuries I still searched for the woman and found no trace. I know that the gods were all hunted down, and I remember the thorough searches of the Sher'Tul in their holy war. I grow old now, and some of those who first woke with me have passed away, and each passing night seem ever colder and lonelier. But still at times when I lie asleep I see her face or I hear her voice, and I know that one day, somehow, I will see her again.`
- 现译：`#{italic}#这个卷轴看起来十分古老，也许它的历史能追溯到千年之前，但其保存的完好程度却令人吃惊。#{normal}#

我依稀记得自己第一次醒来，第一次呼吸，这个世界新鲜的空气使我充满了活力。当我睁开双眼，便看见一尊美丽的身躯静候在我身旁。她高挑而纤瘦，一袭及地的银色秀发如丝般柔顺。她雪白的肌肤似乎散发着莹莹的光芒，双眸如晨星般闪耀。

看到她的一瞬几乎让我的时间停滞，她也温情的望着我，我隐约看到她两眼流出了泪水。虽然这时的我还没有办法发出声音，但是我在想为何她看起来如此悲伤，突然我的脑海里感觉到她的呢喃，“你是这么的美丽，比世上任何东西都要美丽。但这世界却充满了痛苦和悲伤，我怎能忍受我所创造之物被这世界所侵害。我将赐予你力量来忍受时间的流逝，赋予你声音来表达自身的所有欲望，但沉重的悲伤却将伴随你到永远，我为此哭泣……”

我感到力量涌入了四肢，声音从咽喉中奔放而出。我站起来环顾四周，发现了广袤的世界与耀眼的星空，我大声的歌唱着欢乐。这女人听到了我的歌唱，她笑了，她不再流泪。所以我继续歌唱了一会儿来取悦她。但随后我说，“我是独一无二的吗？” 她点了点头，说：“没有其它的人像你一样了。” 听到这句话，我感到很悲伤，而她似乎看穿了我心中的孤寂。女人犹豫了一会，说：“虽然这会让我痛苦，但我绝不会否定你的欲望，你将再次沉睡，当你醒来时，将会被许许多多和你一样的人所包围，而你的宿命将是走进这个破碎的世界并修复它。”

她一说完我便立刻再次陷入沉睡，当我醒来时发现世界变了，空中燃起了一道耀眼的光芒——这就是新生的太阳。接着我看到周围许许多多和我一样的人们，还有一些人虽然长相相同却有着迥异的能力与个性。我将他们唤醒并聚集起来，我们都为有同伴而感到高兴，并决定称呼自己为阿洛。但是那个女人已经离去了，除了我没有任何人见过她，我对她踪迹的一切搜寻都徒劳无果。

时光如水，岁月如梭，我们发现了其它生物，但它们往往邪恶而凶残，于是我们对其发动了战争。接着我们发现了夏·图尔，他们倾慕于我们的美丽，并传授了我们艺术之道。在随后的战争中，我们某些人想在他们的战斗中给予帮助，但很快我们发现在这些大师身旁，我们只是累赘而已。于是我们退回丛林，直到战争出现了灾难性的结果。

在数个世纪里我都在不停的寻找那个女人，但却一无所获。我知道所有的神明都已经被猎杀，也记得夏·图尔在圣战中的彻底搜捕。现在我也老了，与我一同醒来的人中，有些已经逝去，每个夜晚都是那么的清冷孤寂，但每每在我沉睡之时我仍能看到她的面容，听到她的声音，总有一天我会再次见到她。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00186 | HUMAN-REVIEW | cross-batch-042 | confirmed | 改问句与助词；专名与反转程度按收窄意见处理 |  | fix |

<details><summary>hrq-00186 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“一个世纪”意象被改写；confirmed：`Am I alone?` 误作“我是独一无二的吗”；confirmed：两处“的”应为“地”。refuted：并非“极长时间→极短一瞬”完全反转。pending：`Alor?` 处理为“阿洛”是否正确
```
```
raw verdict: “极长时间被翻成极短一瞬”的完全反转→refuted; “一个世纪”具体意象确实被改写→confirmed; `Am I alone?` 误作“我是独一无二的吗”→confirmed; `Alor?` 处理为“阿洛”是否确定正确→pending; 两处“的”应为“地”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。 译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。
```
</details>

## entry-01282

- 位置：`mod-tome.lua:17791`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Many are the tales of how our world was made, from the absurd to the romantic to the horrific. But they are all mere myths, with no more than seeds of truth to even the most reliable. The history of our race goes back far, but it is tantalisingly scant in details from before we met the other races. Indeed, it is only through our battles with the others that we halflings have any ancient records at all.

The elves one would suspect of having the greatest knowledge of elder times, but they are aloof and silent. One must judge from this that either they do not know, or that the truth ashames them. The latter would certainly not surprise me.

The humans have more myths than they have brain cells. It seems that each village has several versions of their own local tales, usually passed down orally over the ages. It is clear that not a single element of any of their myths can be construed to contain any essence of the truth.

The dwarves are reticent about the subject of how they were made. They say that such talk is "not profitable". However upon further pressing (and bribing) they will open up a little further. They as a race are of the most fervent belief that they were the last people to be made in Maj'Eyal. They say they are the "final product". Their word for all other races in fact translates directly to "prototype". This mostly singular outlook does of course seem absurd, but one need only look at the rest of dwarven society to see that they are an absurd race with ridiculous ideals. If they are what they consider perfection then I thank whatever god made me that I am flawed!

The subject of gods is of course a difficult one. Clearly there are no divine forces at work in the world today. But the world as we know it did not come from nothing, and even the great Sher'Tul clearly did naught more than manipulate the world - they did not make it.

By logical conjecture one can only presume that some great being made the world. This must have been a benevolent being, for it is clear that "He" created creatures separate from himself to walk the earth. Clearly this is we halflings. We are the only race that truly appreciates the world. We do not warp it with magic experiments like the Shaloren, nor hide from it like the Thaloren. We do not bring destruction like the orcs, or petty greed like the dwarves. And our understanding and knowledge is so far advanced than the humans that it is hard to understand why we share the same world with them at all. We were quite clearly the first of the current races to be created, and our natural feelings of entitlement to all there is in Maj'Eyal must stem from this.

Now that this has been clearly analysed in logical terms, one must consider the source of the other races. It is impossible that they were made by the same god - truly impossible. What strange being could create our race, so gifted and rounded, and yet make such warped and twisted creatures as the dwarves and humans? No, clearly other gods were responsible, lesser gods than our own which copied his grand design. But with fudging fingers and inelegant touches the works of their design were clearly far inferior to the subtleties and perfection which crafted us.

However there remains the matter of the Sher'Tul. Clearly these were of greater power than us, and yet they disappeared. One must presume that our god made this race before us, but was somehow unhappy with them, and so removed them and made us instead. We are not as powerful as the Sher'Tul - not yet at least - but we have our own gifts that evidently give us a greater place in our creator's heart. This would explain why we were the first race to unlock the powers of the Sher'Tul farportals. We had a natural affinity to the works of our elder brethren.

So what happened to these gods after they had made the races which we see today? One must presume strife between them, and that they killed themselves, or took their battle away from the world. Our creator, seeing the other gods killed or left, must have then entrusted the world to us halflings, knowing that we would rule over it in his stead. This is why at every point in history we have played a pivotal role in the shaping of our world. It is our rightful inheritance, and it is our duty to rule it well.`
- 现译：`关于这个创世的故事有许多版本，有的荒诞不经，有的浪漫无比，有的则令人恐惧。但他们都只不过是神话而已，即使其中最可信的也只包含些许真相的种子。我们的种族历史悠久，但是与其它种族有交集前的历史记载较为稀少。事实上，唯有通过与其它种族的战争，我们才留下了这些古老的记载。

精灵们可能拥有关于古代历史最多的知识，但他们对此沉默寡言。一种普遍的推测是真正的历史要么就并不为其所知，要么就是会让其蒙羞而被故意隐藏了起来。而后者一点都不会让我们感到奇怪。

人类稀奇古怪的传说比他们的脑细胞还多，他们的每个村庄都有数个版本的创世故事，这些故事通常都是经由祖祖辈辈们一代代口述而流传下来。很明显，这些故事都没有根据，毫不可信。

矮人们则对他们的起源保持着奇怪的沉默。他们宣称讨论历史“不能盈利”。但在进一步施压（与贿赂）后，这些家伙也是会透露一点细节的。他们的种族内普遍认为自身是马基·埃亚尔里最后被创造出的——被称为“最终之作”。在他们的语言中其他的种族被称为“原型”。这个观点真是荒诞，而且我们只需一眼就能发现矮人的本质，他们本就是个有着可笑形象的荒诞社会，如果他们真是神最完美的作品，那感谢神明在我身上创造的缺陷！

对于神明的研究当然是道难题，苦于今日并没有发现什么神圣力量残存于世。可是世界并不是凭空创造出来的，就算是伟大的夏·图尔也只是凭着自己的意愿改造世界而已，他们并没有创世。

先从理论上来看，只能推测出是一种伟大的存在创造了这个世界。他一定亲切又和蔼，因为很明显他创造了大陆上繁荣的生命，而我们半身人正是他伟大的产物。我们可以说是唯一真正能够欣赏这个世界的种族。我们不会像永恒精灵一样用奇怪的魔法力量扭曲这个世界，亦不会像自然精灵一样消极避世。我们不会像兽人一样带来无尽的破坏，也不会像矮人一样贪婪无度。而且，我们所理解和掌握的知识比起人类来实在先进太多，真不明白为何要和他们分享同一个世界。我们半身人一定是现存种族里最先被创造出来的，这显然赋予了我们对马基·埃亚尔天然的所有权。

现在从逻辑上来说已经很清楚了，必须考证其他种族的起源。因为他们不可能由同一个上帝所创造——真的不可能。是什么神奇的存在创造了我们的种族，使我们如此全面而有天赋，然后再创造那些畸形扭曲的生物，比如矮人和人类？不，很显然其他创造者也很负责，但比起我们的创造者来差了一些。只要通过对比我们和他们手工制作的“艺术品”就可以看出，他们是多么的粗糙不堪，而我们是多么的完美。

然而夏·图尔的存在又该如何解释。很显然那是比我们更加强大的种族，尽管他们已经消失了。可以肯定我们的创造者在我们之前制造了他们，但是可能不满意他们，于是将他们移除，另外创造了我们。虽然我们没有夏·图尔人那么强大——至少目前还没有——但是我们有自己的天赋，显然在我们伟大的创造者心中占有着更重要的位置。这样就可以解释为什么我们是第一个打开夏·图尔传送门的种族。因为我们和我们的兄弟种族有着天然的联系。

那么在那些神创造了这些种族后又发生了什么？肯定是他们之间发生了纠葛，或者他们同归于尽，亦或是他们的战场远离了这个世界。我们的创造者，看到其他众神，或是被杀或是离开，肯定是将这个世界委托给了我们半身人，因为他知道我们将代替他掌管这个世界。这就是为何在历史的每一个节点上，我们都在世界的塑造中扮演了关键角色。这是我们当之无愧的继承权，治理好这个世界也是我们的职责。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00187 | HUMAN-REVIEW | cross-batch-043 | confirmed | 改动词结构、补“我们半身人” |  | fix |

<details><summary>hrq-00187 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`were responsible` 译成“其他创造者也很负责”；confirmed：`we halflings` 仅译“我们”丢失族称。advisory：`the same god` 译“同一个上帝”
```
```
raw verdict: `were responsible` 译成“其他创造者也很负责”→confirmed; `the same god` 译成“同一个上帝”→advisory; `we halflings` 仅译成“我们”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-042-01.md](reports/sol-042-01.md)。译文未修改。共 16 个 claim：13 confirmed、3 advisory、无 refuted/pending。 译文未修改。
```
</details>

## entry-01283

- 位置：`mod-tome.lua:17826`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Eyal was raised from Darkness,
And One came who made a blinding light called Sun,
But Eyal flinched and said, "It is too bright!"
So Gerlyk spun Eyal around; thus his face was half-time in light and half-time in shadow,
But in shadow Eyal became lonely and cried.

And so Gerlyk made him two younger sisters who danced around Eyal
And kept him in good spirits.
But the moonsisters became jealous of their brother's affection,
Threatening to fight and scream.
Thus Gerlyk separated them so that Eyal would only ever dance with one at a time.

In the summer Eyal dances with the moonsister Altia.
She sings songs of joy and laughter,
And brings friends and family together,
And she glows yellow with mirth.
In the winter Eyal dances with the moonsister Felia.
She tells tales of times begone,
And makes men walk alone in thought,
And she glows blue with solemness.

But in the time between,
When both sisters are slimly seen on each side of Eyal,
Glaring at each other from behind their brother's belly,
Then the world goes still, and the winds hold their breath, and the oceans lie flat.
For this is the Time of Balance, when the Darkness rises deepest, and all life is in peril.
Aye, and Gerlyk did say, "Let no man walk abroad this night, lest Darkness catch him and take him forever."
Aye, and Gerlyk did walk abroad that night, into Darkness beyond, and has ne'er since been seen.`
- 现译：`埃亚尔从黑暗中升起，
创造者制造了一团耀眼的光叫做太阳，
但是埃亚尔认为这团光过于刺目，
于是盖里克让埃亚尔自转起来；这样它的面孔一半时间沐浴光明，一半时间沉入黑暗，
但是埃亚尔黑暗的那面感觉很孤单并伤心的哭泣。

所以盖里克为他造了两个妹妹，她们围绕着埃亚尔起舞，
让他保持好心情。
但是月亮姐妹开始争风吃醋，妒忌对方得到哥哥的宠爱，
以武力威胁并大声嚷嚷。
于是盖里克将她们分开这样埃亚尔只能和其中一位跳舞。

夏天埃亚尔和月亮女神亚缇娅共舞。
她笑着唱着快乐的歌，
让朋友和家人欢聚，
她闪耀着欢乐的金色。
冬天埃亚尔和月亮女神菲莉娅共舞。
她讲述着往昔的故事，
使人们独自行走在沉思中，
她闪耀着肃穆的蓝色。

但在交替之时，
两姐妹只能在埃亚尔两端，
隔着哥哥的身躯互相怒视。
世界在这一刻静止了，清风不再吹拂，大海也不再掀起波澜。
这就是平衡日，是黑暗最深的时刻，万物都处在危险之中。
盖里克说：“没有人能走入今晚的黑夜，否则黑暗将抓住他并使他永坠黑暗。”
然后，盖里克走入了这样的黑夜，进入了无尽的黑暗，并再也没出现过。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00188 | HUMAN-REVIEW | cross-batch-043 | confirmed | 补月相与叹词，`moonsister` 回到“月 Sister/月姊妹”一类 |  | fix |

<details><summary>hrq-00188 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏 `slimly seen` 月相意象；confirmed：`walk abroad` 理解与两处 `Aye` 遗漏（核心语义）；confirmed：`moonsister` 增译“月亮女神”。advisory：叹词风格
```
```
raw verdict: 遗漏 `slimly seen` 的月相意象→confirmed; `walk abroad` 的理解及两处 `Aye` 遗漏（核心语义）→confirmed; `walk abroad`／`Aye` 的叹词风格→advisory; `moonsister` 增译为“月亮女神”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-042-01.md](reports/sol-042-01.md)。译文未修改。共 16 个 claim：13 confirmed、3 advisory、无 refuted/pending。 译文未修改。
```
</details>

## entry-01286

- 位置：`mod-tome.lua:17921`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`I fell asleep in a dark hollow, but my sleep was troubled by terrible dreams. The dreams are so vivid in my mind!

I saw the red star, and it became a land of fire floating in the night sky, full of black creatures with yellow eyes and hungry red mouths. And beyond the red star, far beyond was a dim world, but fractured and split all about its surface. As the world spun the split continents crushed against each other, and lava spilled up, and lands sunk into the ground. Demonic mouths screamed up as they disappeared into fiery death. It was if the world was tearing itself apart, but some force of will was desperately trying to keep it held together.

And I saw then in the centre of the world, as it spun and crumpled and crunched, a vast figure with a horned head and outstretched limbs and shining white eyes. It held tight to the innards of the world, holding it together against forces threatening to pull the whole planet apart. The giant face contorted and screamed in pain and fury.

“Urh'Rok,” a deep voice spoke within my head. “Our god, our saviour, holder of our world. In the name of Urh'Rok we seek vengeance against Amakthel and the Sher'Tul. The petty world of Eyal shall fall!” And then I woke up, and I felt sure something was nearby, looking for me. I fled instantly.

Am I going mad? The name “Urh'Rok” still rebounds through my skull and my vision is dimmed. Perhaps I have been wearing this ring too long...

Yes, yes, this is all clearly an illusion! A strange nightmare that I shall wake up from. I shall take the ring off, and go visit the lovely moonstone again. Once I see the stars all shall be well...`
- 现译：`我在一片黑暗的山洞中渐渐睡去，但是我的睡眠被一个可怕的梦吵醒了。即使刚睡醒的脑袋仍然一团浆糊，那个梦仍然在我的脑海中异常清晰。

我看到眼前红色的星星越来越大，原来，那是一片在夜空中漂浮着的燃烧的大陆，上面满是有着黄色眼睛和贪婪的红色大嘴的黑色生物。在红色星星的上方遥远的地方是一片黑暗的世界，但是那个世界似乎被某种力量切得支离破碎。在这个世界旋转的过程中，破碎的大陆互相撞击，岩浆的波浪浮浮沉沉，陆地沉入地底。我听到恶魔般的吼叫，那是大陆上的生物被烈火吞没时的绝望呻吟。似乎这个世界被完全撕裂开来，但是某种意志的力量努力试图将他们固定在一起。

视野中，随着这个世界逐渐旋转，逐渐被挤压碎裂，我隐约能看到那个世界的中心。在那里，是一个拥有闪烁的白色眼睛，头上长角的巨大影像。它向外伸展而出的强壮四肢紧紧抓着世界的核心，试图将它连结在一起，来对抗那些不断将这颗星球撕裂的可怕力量。在剧烈的痛苦和愤怒中，巨人的表情被其扭曲，发出怒吼。

“乌鲁洛克，”一个深沉的声音在我的脑海中响起。“我们的神，我们的救世主，保护世界之人。以乌鲁洛克的名义，我们将向阿马克泰尔和夏·图尔人复仇。渺小的埃亚尔世界终将陨落！”我被噩梦所惊醒，直觉告诉我有什么东西就在附近，正在搜寻着我。我立刻拔腿就跑。

是我的脑子出了什么问题吗？那个奇怪的名字，“乌鲁洛克”仍然在我的心头回响，我的视野也变得昏暗起来。大概是我戴了这个戒指太久了的副作用的缘故……

唉，对，这一定是我的幻觉！我早该从这个怪梦里醒来了。我应该赶紧脱下这个该死的戒指，回去看看我可爱的月亮石们。只要能让我看见美丽的星空，一切都一定会好起来的……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00189 | HUMAN-REVIEW | cross-batch-043 | confirmed | 逐句按源码回改，删除两处增译 |  | fix |

<details><summary>hrq-00189 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：七处——增添“刚睡醒的脑袋仍然一团浆糊”；`beyond the red star` 译“红色星星的上方”；`keep it held together` 译“将他们固定在一起”；`the lovely moonstone` 误作复数；`I shall wake up from` 译“我早该……醒来”；增添“该死的戒指”；`lava spilled up` 译“岩浆的波浪浮浮沉沉”
```
```
raw verdict: 增添“刚睡醒的脑袋仍然一团浆糊”→confirmed; `beyond the red star` 译为“红色星星的上方”→confirmed; `keep it held together` 译为“将他们固定在一起”→confirmed; `the lovely moonstone` 误作复数“月亮石们”→confirmed; `I shall wake up from` 译成“我早该……醒来了”→confirmed; 增添“该死的戒指”→confirmed; `lava spilled up` 译成“岩浆的波浪浮浮沉沉”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-042-01.md](reports/sol-042-01.md)。译文未修改。共 16 个 claim：13 confirmed、3 advisory、无 refuted/pending。 译文未修改。
```
</details>

## entry-01290

- 位置：`mod-tome.lua:17978`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`I begin my writings with a study of the humans, currently the most populous of the races in Maj'Eyal. The greatest kingdom in number are by far the Cornacs, but mention should also be made of the Sholtar and Mardrop kingdoms, and the Higher bloodline. The biggest human population centre is around the citadel of Last Hope, though many other settlements exist across all corners of Maj'Eyal.

Cornacs are normally around 5'9", with generally dark hair, brown eyes and ruddy features. Most Cornacs take up roles as tradesmen, farmers, or other manual labour jobs. It is a sad fact that the majority of bandit groups tend to be dominated by Cornacs. Cornac families tend to be large, and since the Age of Dusk their population has expanded rapidly, especially in the farming lands in the west and around Last Hope in the south.

Sholtar are generally 5'11", with dark skin, hair and eyes. They originate from the south-east of Maj'Eyal, and are few in number since the Cataclysm tore much of their land into the sea. Their affinity with nature is renowned, and they are often found employed as healers, infusion crafters or wyrmic huntsmen.

Mardrop humans are all but extinct, after the Spellhunt and the plagues during the Age of Dusk. They were known to be powerful spellcasters, and as such were prime targets by the spellhunters. However some trace of them can still be found, as their fiery hair and freckled skin oft can appear in those of distant descent. A few are rumoured to still possess citadels and towers in remote locations.

Highers are on average 6'0", with fair hair and skin and blue or grey eyes. The majority of scholarly roles are taken up by Highers, and they tend to fill most of the noble classes. Some say this is due to discrimination and elitism, though these may simply be jealous sentiments. There are also rumours that the superior intellects of Highers are due to arcane experiments instigated by the ancient Conclave during the Age of Allure, but I have found no records to support this idea and must consider it to be baseless. The Higher bloodline is renowned as a mark of excellence, and mixing with lower bloods is strongly frowned upon.

All human kingdoms were united by King Toknor the Brave in the Age of Pyre, and remain under the rule of his son King Tolak the Fair. A full discussion of the long human history would require a far more detailed document.`
- 现译：`我从人类的研究开始，他们目前是马基·埃亚尔人口最多的种族。若论人口数量，科纳克王国远超其他人类王国。此外，肖尔塔王国和马卓普王国以及高等人类这一血统支系也值得一提。最大的人类聚居地在最后的希望要塞周围，另外还有许多聚居地存在于马基·埃亚尔的每个角落。

科纳克人基本身高在5英尺9英寸左右，有着黑色的头发、棕色的眼睛以及红润的肌肤。大多数科纳克人选择商人、农民或者其他体力劳动职业。不幸的是，大部分强盗组织也更倾向于被科纳克人控制。科纳克人的家族很庞大，并且自黄昏纪以来他们的人口增长极快，特别是在西部农业地区和南部的最后的希望一带，这种现象尤为明显。

肖尔塔人基本身高在5英尺11英寸左右，黑皮肤黑头发黑眼睛。他们起源于马基·埃亚尔的东南地区，自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。他们以自然亲和著称，并且经常作为治疗师、注能物工匠或龙战士猎手行走于世。

在黄昏纪的魔法狩猎与瘟疫之后，马卓普人几乎灭绝。他们以强大的施法者著称，也因此成为猎魔者的首要目标。不管怎样，他们的血统特征——火红的头发以及生有雀斑的皮肤，仍会出现在遥远后裔的身上。有部分传言说他们仍住在某些遥远的地方的城堡或高塔里。

高等人类基本身高在6英尺左右，有着金色的头发、白皙的皮肤和蓝色或灰色的眼睛。大多数学者都是高等人类，贵族阶层也大多由他们占据。有人说这都是歧视和精英理论所导致的，虽然这可能只是简单的嫉妒情绪。也有传言说高等人类的高智商是厄流纪时期孔克雷夫法师们的实验成果，但是我找不到任何证据来支持这一论点，我只能认为这种说法毫无根据。高等人类的血统被认为是优秀的标志，与低等血统通婚则为世所不齿。

在烈火纪，勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子公正之王托拉克的手中。一份关于人类漫长历史的全面报告需要更加详细的文本来叙述。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00190 | HUMAN-REVIEW | cross-batch-043 | confirmed | 事件名回“大灾变”；猎称按术语统一 |  | defer |

<details><summary>hrq-00190 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Cataclysm` 译“大爆炸”，与 `Spellblaze` 混淆（应为“大灾变”）。advisory：`spellhunters` 译“猎魔者”易与 demon 混淆
```
```
raw verdict: `Cataclysm` 译为“大爆炸”（应为大灾变）→confirmed; `spellhunters` 译为“猎魔者”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-042-01.md](reports/sol-042-01.md)。译文未修改。共 16 个 claim：13 confirmed、3 advisory、无 refuted/pending。 译文未修改。
```
</details>

## entry-01292

- 位置：`mod-tome.lua:18000`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`There are two main kingdoms of halflings, the Eldoral and the Nargol, though both mix often. All halflings are just under 4' tall, and are generally noted for their large feet and curly hair. Eldoral are usually fair-haired and blue-eyed. Nargol tend to be darker in hair and complexion, with hazel eyes, and oft slightly shorter than their cousins. Halflings are known for their intelligence and quick wit, but also their arrogance in dealing with other races - something they do not deny, for they say it is well-deserved.

Halflings used to be the most dominant race in Maj'Eyal, with control of many strategic Sher'Tul ruins and rule over great swathes of land. The recorded wars between humans and halflings are numerous, and the halflings were the most often victors. However the Age of Pyre brought them great ruin, for the orcs seemed to target them more fiercely than any other race, and many of their communities were wiped out. This has forced them to rely more on trade with other races in modern times, especially with the humans.

The Eldorals used to have a kingdom in the north of the continent, but most of it was destroyed during the wars with the orcs, and not much has been rebuilt. However they do still have many agricultural settlements such as Derth, albeit shared with other races. The Eldoral are known for their great healers and farmers, and their slingers are considered the best in all the lands.

The Nargols once had many strong fortifications in the south of Maj'Eyal, but though they suffered less than the Eldoral in the Age of Pyre they still lost great numbers, and much of their centres of population dwindled. The rise of Last Hope has accelerated this process, as many communities are subsumed into the city's suburbs. Nargols are known as great jewellers, alchemists and rune-crafters, and possess some of the best tactical minds of all the races. Many generals and military advisers are employed from their kingdom.

The most famous of all halflings is Queen Mirvenia, most famed for her saving of King Toknor in Last Hope from a siege of orcs. Mystery still surrounds how she managed to bypass the winter's icy floes with her army to reach the citadel in time to rescue Toknor. Some have hypothesised that she enlisted the aid of sorcerers, but none of her troops would talk about the journey afterwards. She wed King Toknor in the second year of the Age of Ascendancy, and gave birth to the first known mixed race child - Tolak the Fair.
`
- 现译：`主要的半身人王国有2个，艾德瑞尔和纳格尔，虽然他们经常生活在一起。所有的半身人身高都略低于4英尺，并且以他们的大脚板和卷曲的头发而闻名。艾德瑞尔人有着浅色的头发和蓝色的眼睛。纳格尔人则有着颜色较深的头发和皮肤以及褐色的眼睛，通常比艾德瑞尔人要稍矮一些。半身人以聪明机智而闻名，但在与其他种族打交道时也十分傲慢——他们并不否认，因为他们认为这份傲慢理所当然。

半身人曾经是马基·埃亚尔最具统治地位的种族，他们控制着许多具有战略价值的夏·图尔废墟，并统治着广袤的土地。史书上记载，人类和半身人之间曾发生过许多次交锋，半身人通常是最后的赢家。但是烈火纪带给他们巨大的灾难，因为兽人们对半身人种族格外仇视，他们的许多族群都被杀光。这使得他们在现代更加依赖与其他种族的贸易往来，尤其是与人类。

艾德瑞尔人曾经在大陆的北面有一个王国，但是大部分在兽人战争时期被完全摧毁，只有少部分重建。不过他们仍拥有许多如德斯镇这样的农业聚居地，尽管是与其他种族共居。艾德瑞尔人以出色的治疗师和农夫著称，并且他们的投石者被认为是世界上最优秀的。

纳格尔人曾经在马基·埃亚尔的南部建造了坚固的防御工事，虽然他们在烈火纪遭受了相对艾德瑞尔来说较少的苦难，他们仍然失去了很多人，大量人口聚居区就此凋敝。最后的希望的崛起加速了这一进程，许多聚居区被并入了这座城市的近郊。纳格尔人以出色的珠宝匠、炼金术师和符文师著称，并且在所有种族中拥有最出色的战术头脑。许多将军和军事顾问都出自他们的王国。

在半身人中最著名的则是米雯尼雅女王，她在最后的希望的兽人围城之战中救出了勇者图库纳国王，自此一战成名。她如何带领军队穿越凛冬的浮冰，及时抵达要塞救下图库纳，始终是个未解之谜。有人猜想她雇佣了一些术士，但是她的军队之后从未有人透露过关于那次援救的详细情况。她在卓越纪的第二年嫁给了勇者图库纳国王，并生下了有记载以来的第一个混血孩子——公正之王托拉克。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00191 | HUMAN-REVIEW | cross-batch-044 | confirmed | 与第一章逐条对照 + 术语核对 |  | fix |

<details><summary>hrq-00191 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：末尾换行差异；confirmed：“勇者图库纳”“公正之王托拉克”有上下文依据；confirmed：无占位符缺失。pending：与现行第一章译法是否完全一致；pending：术语是否均符合术语表。advisory：`enlisted the aid of sorcerers` 译“雇佣了一些术士”
```
```
raw verdict: 末尾换行差异→confirmed; “勇者图库纳”“公正之王托拉克”有上下文依据→confirmed; 与现行第一章译法完全一致→pending; `enlisted the aid of sorcerers` 译“雇佣了一些术士”→advisory; 术语均符合术语表→pending; 无占位符缺失→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-043-01.md](reports/sol-043-01.md)。译文未修改。共 20 个 claim：10 confirmed、5 pending、4 advisory、1 refuted。 译文未修改。refuted 项是对 Gemini 术语推断的下修，原样转录。
```
</details>

## entry-01294

- 位置：`mod-tome.lua:18019`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`The dwarves are an exceptionally secretive and quiet race, reluctant to talk about themselves to outsiders unless hefty bribes are paid. Many times in their history they have cut off all contact with the other races for no known reason, shutting tight the great iron doors that cover the trade passages to their mines and their cavernous cities. However of late they have become more open with the outside world, and I have even had the pleasure of receiving the unique distinction of being allowed to enter their main city, the Iron Throne, and speaking with several of their guild leaders.

Dwarves are around 5' tall, with generally brown or grey hair. They are usually stocky and muscular, and known to be very resistant to any physical suffering. Their females can be hard to distinguish from their males, but can usually be identified by the beads braided into their beards. All dwarves are highly proud of their beards, and take immaculate care of them. The greatest insult to a dwarf is to belittle his beard, and the greatest sign of suffering in a dwarf is for him to tear at his beard.

Dwarves are known especially for their smithwork and artificing, which is unrivalled amongst all the other races. They also make cunning merchants, known to drive a hard bargain. Their society consists of a fairly strict caste system, with families belonging to guilds of miners, smelters, craftsmen, and so on, and deviance into work outside of one's guild of birth is almost unheard of. However there is no perceived inequality between guilds, with each having equal representation on their ruling Committee of Guilds. Who actually acts as figurehead is unknown to outsiders though, and no amount of bribing will encourage any dwarf to speak on the subject. When it is mentioned in passing their allusions to a leader are normally marked by an almost religious reverence.

Their skill with metal is renowned above all else. Dwarven steel is considered the most durable material for use in construction, and dwarves are the finest workers with stralite and voratun, precious metals of immense value. They trade heavily in their crafts from their capital the Iron Throne, but allow no outsiders in - instead they send innumerable merchant caravans out to all the cities to ply their wares.

As well as the many merchant dwarves one may meet there are also a great deal of young dwarves who venture beyond their halls of stone. These are generally of adventuring fare, and it is encouraged in dwarven society to experience something of the wider world in one's younger years. This is known to them as being "smithed upon the anvil of the world". In private though some senior dwarves admit that this activity is promoted to help with their "market research strategy".`
- 现译：`矮人是非常神秘且低调的种族，一般来说，除非付出重金贿赂，否则他们不会谈论任何与己有关的事。历史上，他们曾多次因不为人知的缘由切断与外界的联系，落下的钢铁大门隔绝了外界的交易通道以及通往他们矿井和地下城市的道路。不过，近来他们对外界越来越开放，我甚至获得了进入他们首都——钢铁王座的殊荣，并有幸与他们的几位公会首领交谈。

矮人们基本身高在5英尺左右，有着棕色或灰色的头发。他们通常身材敦实、肌肉结实，并以超强的物理抵抗能力而闻名于世。他们的性别通常较难区分，但可以通过编入胡须的珠饰来辨认。所有的矮人都非常自豪于他们的大胡子，并且对他们的胡子非常爱护。对于矮人来说，贬低他的胡子就是最大的侮辱，而矮人极度痛苦时会撕扯自己的胡子。

矮人擅长锻造和精工，这一点在所有种族中都是无与伦比的。他们同时精于商业，擅长讨价还价。他们的社会有着相当严格的等级制度，家庭通常会隶属于矿业公会、冶炼公会、工匠公会等等，脱离出身公会另谋生计的个人几乎从未听说过。不过，在公会之间并无地位不平等之说，各公会在统领众公会的公会委员会中拥有平等的代表权。谁实际担任名义领袖，外人不得而知，再多的贿赂也不能使任何矮人就此开口。当话题偶然被提及时，他们对那位领袖的暗示几乎总带着一种近乎信仰的敬畏。

他们对金属的加工技艺也是举世闻名的。矮人钢被认为是建筑中最耐久的材料，而矮人也是加工斯莱特和沃瑞钽这两种价值连城的贵金属的最佳工匠。他们在首都——钢铁王座中进行大量的交易，但是从不欢迎外来者——相反，他们会指派无数商队到各个城市去售卖货物。

在众多的矮人商人出现的同时，越来越多的年轻矮人更加倾向于从他们的石头洞穴里出去冒险。他们一般以探险为业，在矮人社会中，一个人在年轻的时候出去闯荡是值得鼓励和赞扬的。矮人称这种经历为在“世界之砧”上锤炼自己。不过私下里，一些年长的矮人承认推广这项活动是为了帮助他们的“市场调查策略”。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00192 | HUMAN-REVIEW | cross-batch-044 | confirmed | 修措辞；术语待核 |  | fix |

<details><summary>hrq-00192 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`physical suffering` 译“物理抵抗能力”；confirmed：`halls of stone` 译“石头洞穴”弱化意象；confirmed：段落与格式无异常。pending：钢铁王座、斯莱特、沃瑞钽等是否符合术语库
```
```
raw verdict: `physical suffering` 译“物理抵抗能力”→confirmed; `halls of stone` 译“石头洞穴”弱化意象→confirmed; 钢铁王座、斯莱特、沃瑞钽等符合术语库→pending; 段落完整、引号和格式无异常→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-043-01.md](reports/sol-043-01.md)。译文未修改。共 20 个 claim：10 confirmed、5 pending、4 advisory、1 refuted。 译文未修改。refuted 项是对 Gemini 术语推断的下修，原样转录。
```
</details>

## entry-01296

- 位置：`mod-tome.lua:18037`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Though the elven races look very similar in appearance, they are extremely distinct in history, culture, mindset and many subtle physical traits, so I shall write of each of them separately. All elves are marked by their long, pointed ears and high cheek-bones, but other features can vary greatly. It should be noted that they call themselves as a whole "Elore", which means "siblings", yet the interactions between these brothers and sisters are oft strained.

Shaloren (or Shalore - lit "siblings of grace") are on average 6'2", with bright hair and blue or purple eyes. They are usually slim and lightly built, more marked for their mental prowess than their physical strengths. They are however known to be extremely swift of movement and light of foot. But of particular note is their magical affinity, which is far stronger than any other race, and their intense powers of will.

The Shaloren have a long history of magic-use which continues to this day. Though other races shun the dangers of magic to a large degree, the Shaloren embrace it, and it is still widely used throughout their society. However they are careful to hide this in their dealings with other races. The Shaloren were the ones that began the Spellblaze, though they would soon have it forgotten, and the memories of blame run deep amongst many. During the Spellhunt in the Age of Dusk they locked their city doors and shrouded the whole region in mist, only coming out in secrecy. It took many centuries before they were accepted again in wider society, and still they are treated with intense distrust.

Their capital city is Elvala, in the south-west peninsula, and they have very few settlements outside of this. They have naturally long lives, and their mastery of the arcane arts has allowed them to extend their lives indefinitely. The eldest immortals make up their Council of Elders, which is headed by their King Aranion Gayaeil. Death is a particular fascination amongst the Shaloren, and early kings of their race were said to build great tombs for themselves whilst experimenting in flesh preservation and necromancy. The Shaloren of course deny this.

They deal with other races seldom, preferring to keep a low profile, and most of their trade is done through halfling intermediaries. A few rune-crafters and enchanters sometimes travel to other major cities to do business, and some brash youths are known to explore further afield.`
- 现译：`虽然乍一看，精灵们都差不多，但是他们还是有着不同的历史、文化、观念和许多微妙的生理特征，所以我将会分开写他们。所有的精灵都有着非常明显的标志——尖尖的耳朵和高颧骨，至于其他特征则差异极大。必须说的是，他们称自己为整体的“Elore”，意即“兄弟姐妹”，然而这些兄弟姐妹间的关系通常是比较紧张的。

永恒精灵（Shalore，字面意为“优雅的兄弟姐妹”）通常身高6英尺2英寸左右，有着阳光般灿烂的头发和蓝色或紫色的眼睛。他们身材苗条，体格轻盈，更以精神智慧而非体格强健著称。他们以迅捷的移动速度和轻快的步伐而闻名。但是最值得注意的是他们的魔法亲和力，这一点其他任何种族中都是无法相提并论的，同时他们还拥有强大的意志。

很久以前，永恒精灵们便学会了魔法的运用，而这点也一直延续至今。虽然其他种族认为魔法充满了巨大的威胁，永恒精灵们却热爱着它，并且广泛运用于整个社会。不过，在他们与其他种族交流时，他们仍小心地隐藏魔法。永恒精灵正是发动魔法大爆炸的元凶，虽然他们很快便设法让此事被人遗忘，但是归咎于他们的记忆却深埋于许多人心中。在黄昏纪的魔法狩猎期间，他们紧闭城门并用一层薄雾笼罩着整片区域，偶尔悄悄地溜出来。许多世纪后他们才为世人所接受，但是大家对他们仍心存猜忌。

他们的首都在埃尔瓦拉，西南半岛地区，其他地方则很少见到他们居住。他们有着很长的寿命，并且他们在魔法上的造诣允许他们无限延长他们的寿命。其中最年长的那些不死者组成了由精灵王艾伦尼恩·加威尔为首的长老会。永恒精灵对死亡尤为痴迷，相传过去的国王为自己建造了奢华的坟墓并在里面研究肉身保存与亡灵法术。当然，永恒精灵们是矢口否认的。

他们很少与其他种族直接往来，一直过着低调的生活，大部分的贸易是通过半身人中间人来完成的。少数符文师和附魔师有时会前往其他主要城市做生意，另外还有一些莽撞的年轻人去更远的地方闯荡。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00193 | HUMAN-REVIEW | cross-batch-044 | confirmed | 补 `or`、统一引号风格 |  | fix |

<details><summary>hrq-00193 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `or` 且保留 `Shalore` 拉丁拼写；confirmed：内容对应完整。advisory：`arcane arts` 译“魔法”；advisory：引号风格与 entry-01298 不一致。pending：关键事件与专名是否均符合规范
```
```
raw verdict: 漏译 `or` 且保留 `Shalore` 拉丁拼写→confirmed; `arcane arts` 译“魔法”→advisory; 引号风格与 entry-01298 不一致→advisory; 关键事件和专名均符合规范→pending; 内容对应完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-043-01.md](reports/sol-043-01.md)。译文未修改。共 20 个 claim：10 confirmed、5 pending、4 advisory、1 refuted。 译文未修改。refuted 项是对 Gemini 术语推断的下修，原样转录。
```
</details>

## entry-01298

- 位置：`mod-tome.lua:18055`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`The Thaloren (or Thalore - lit "siblings of wrath") are on average 6'4", with dark brown hair and hazel or green eyes. They are generally of muscular build, and known for their physical prowess. They are renowned to be of a fey mindset - as quick to furious violence as they are to joyous song. Their relations with the Shaloren are particularly strained, as they strongly oppose their brethren's use of magic.

Their capital city is Shatur, hidden deep within the northern woods, and they are loathe to let any outsiders even approach the surrounding forest. Archers and fighters carefully patrol their borders, ready to rain down death from the trees on any who encroach. Their leader is Queen Nessilla Tantaelen, and they are said to live in extensive dwellings carved into giant trees, but little else is known about their society.

Those who choose to leave the fastness of the forest tend to be of unique disposition with unusual attitudes and traits. Oft they are musicians, bowmasters or skilled warriors. However they are sometimes mistrusted heavily, as rumour has it that many of those who leave Shatur are actually criminals expelled for the very worst crimes. In any case they tend to be natural loners who wander the world on their own personal quests.

The Thaloren do business very rarely with the outside world, but when they do it is normally for metals and certain foodstuffs that they cannot get themselves. Usually in trade they sell woodcraft and fine silks. This is the only legal source of elven-wood, a rare commodity that is often sought after for fletchwork. Black market sources rely on poachers to cut trees from the Shatur forest - an immensely risky business, but also very profitable for the high prices paid by Shaloren mages for an elven-wood staff.`
- 现译：`自然精灵（或木精灵——字面意为「愤怒的同胞」）平均身高约 6 英尺 4 英寸，有着深棕色的头发和淡褐色或绿色的眼睛。他们大多体格健硕，以强悍的体魄闻名。他们以喜怒无常的性情著称——既会骤然陷入狂暴的杀戮，也会同样迅捷地放声欢歌。他们与永恒精灵的关系尤为紧张，因为他们强烈反对同族对魔法的使用。

他们的首都是夏特尔，深藏于北方的丛林之中；他们厌恶任何外来者，甚至不容外人接近周围的森林。弓箭手与战士小心地巡守边界，随时准备从树上向任何入侵者倾泻死亡。他们的领袖是女王奈希拉·坦泰兰，据说他们居住在雕凿于巨树之中的宽敞居所里，但外界对他们的社会所知甚少。

那些选择离开这片森林堡垒的精灵，往往性情独特、态度与秉性异于常人。他们常是乐师、弓术大师或身手不凡的战士。不过他们有时也备受猜忌，因为传言说许多离开夏特尔的人其实是因最恶劣的罪行而被放逐的罪犯。无论如何，他们大多是天生的独行者，为着各自的个人追寻而浪迹世界。

自然精灵极少与外界通商，一旦通商，通常是为了换取他们无法自给的金属和某些食物。他们通常出售木制品和上等丝绸。这是精灵木的唯一合法来源——那是一种珍稀商品，常被用于制箭。黑市货源则依赖偷猎者从夏特尔森林中盗伐树木——这是一桩极其危险的营生，但也利润丰厚，因为永恒精灵法师愿为一根精灵木法杖付出高价。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00194 | HUMAN-REVIEW | cross-batch-044 | confirmed | 分支指称需全库核对后再定 |  | no_change |

<details><summary>hrq-00194 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Thalore` 与 `Thaloren` 是同一种族的不同形式。refuted：“木精灵脱离官方源码既有用法”不成立。advisory：会让读者误以为存在两个分支。pending：“木精灵”是否全库仅此一处
```
```
raw verdict: `Thalore` 与 `Thaloren` 指同一种族的不同形式→confirmed; “木精灵”是当前译文自行意译、脱离官方源码既有用法→refuted; “木精灵”在全库仅此一处→pending; 会让读者误以为存在两个分支→advisory; 其余专名和段落完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-043-01.md](reports/sol-043-01.md)。译文未修改。共 20 个 claim：10 confirmed、5 pending、4 advisory、1 refuted。 译文未修改。refuted 项是对 Gemini 术语推断的下修，原样转录。
```
</details>

## entry-01302

- 位置：`mod-tome.lua:18083`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Ogres have never been a thriving race, starting from their abrupt appearance as soldiers and laborers for the Conclave during the Allure Wars (unexplained aside from a highly implausible story from the Conclave's Overseers about a lost mountain tribe).  Left without homes or proper runic training after the war's end, they were forced to found their own tribes and rediscover the fields of rune and infusion creation for themselves, and though their numbers dropped rapidly, they enjoyed a brief period of relative success as nomadic rune-traders, virtually unaffected by the Spellblaze.  The Spellhunt nearly proved to be their undoing, as their monstrous size and rune-covered skin made them popular targets; they were thought to be extinct, and only in recent years has the city of Elvala revealed that some Ogres took refuge there during this time.  Their descendants still live today, fearful of persecution but gradually beginning to explore outside Elvala for the first time in ages.

Ogres' most striking feature is their size, by far the largest of any intelligent race; they average at roughly 8'4" tall, and most are nearly half as wide with muscle.  They have a similar range of skin tones to humans, although slightly grayer on the whole; their hair tends to be dark brown or black, and their eyes run the gamut from black to bright blue to purple, presumably a side-effect of runic mis-transcription.  Their angular facial features invite some impolite comparisons to Orcs, with strong jawlines, disproportionately large mouths and teeth, and squarish heads, but otherwise resemble those of humans.  It would be remiss of me to describe Ogres' appearance without mentioning the intricate, glowing pattern of runes covering their skin from head to toe, although the exact patterns and colors vary.  

Although they excel at physical tasks for obvious reasons, and the necessity of careful inscription has made their finger dexterity (and penmanship) rather impressive, their limb movements tend to be slow and clumsy due to their size, and they tire quickly if they over-exert themselves during strenuous labor.  Their slow speech, incredible appetites, and lack of interest in arts or most scholarly concerns has led to a misconception that they are dim-witted; however, Ogres forced into studious tasks have performed admirably, and one needs only look at their runic patterns to know the patient study and artistic vision they are capable of, if properly motivated.  This may tie into the humble, duty-bound mindset that seems to be an inherent property of the species - most Ogres show absolutely no interest in leadership or impressing others, only completing tasks in the most reliable manner possible, and such strategies tend to be rather simple.

While Shalore use of magic is (arguably) a choice, Ogres have no such luxury.  Their inscriptions are as crucial to their well-being and structural integrity as any internal organ, and attempts by Ziguranth to "cleanse" captured Ogres of their runes invariably lead to them first collapsing under their own weight, then their organs shutting down one by one; one can assume that their natural infusions are just as vital.  As such, Ogre reproduction is a careful task; a newborn can live for a few months unaltered, but after this the parents must give their child a thorough regimen of runic inscription and herbal infusions.  The parents typically perform this task together, using each others' runes as a reference, and any mistakes made in the transcription will affect the child's health and development (usually adversely, though it is believed that transcription errors are responsible for mitigating Ogres' once-uncontrollable tempers).  As such, the inscribed patterns are as much of an influence on the child's development as the physical and mental traits of his or her parents.	

Due to the safety and comfort of Elvala, and their mistrust of much of the outside world, most Ogres who leave their home do so for trade purposes; no longer using Shaloren as couriers, some have begun to enter the growing market of runes and infusions, and have proven very successful thanks to their natural talent in this area.  Those few who could be considered "adventurers" tend to pack up their things and leave abruptly, not for glory or riches, but because they see a recurring source of misery in the world and wish to dispose of it themselves as a public service.  It is not uncommon for an Ogre to sigh in frustration after hearing about a hijacked shipment of grain, head out, return a few days later with the blood of a once-persistent bandit clan stuck to his club, and go right back to tending his crops.`
- 现译：`食人魔从来不是一个昌盛的种族。在厄流纪的长期征战中，这个种族突然出现在世人的视线里，作为孔克雷夫的工人和士兵。孔克雷夫的长老会宣称他们是在崇山峻岭中找到了隐藏于世间许久的食人魔，然而这个故事难以置信，漏洞百出，使得目前食人魔的产生仍然原因不明。在旷日持久的战争结束后，流离失所的他们无家可归，也没有接受过系统化的符文训练，只能被迫重新建立起自己的部落，自行重新摸索出符文与纹身的制作之道。尽管这一过程伴随着大规模的人口减员，他们作为游牧的符文商人度过了一段相对成功的日子，基本没有受到魔法大爆炸的影响。接踵而来的魔法狩猎几乎让这个种族就此灭绝。因为他们怪异的体格和满身符文的皮肤，他们迅速成为猎魔者的首要目标。几乎所有人都认为这个种族已经灭绝，直到近几年埃尔瓦拉城才透露，当年曾有一批食人魔在此避难。他们的后代仍然生活在今天，尽管仍然畏惧着外人的迫害，他们中的少数仍然尝试着向埃尔瓦拉以外的区域前去探索。

食人魔们最引人注目的特征是他们高大的体格，目前是所有智慧种族中体格最为硕大的一个。他们通常身高在8英尺4英寸左右，大多数人浑身的肌肉使他们的宽度几乎达到身高的一半。就像人类一样，他们也有各种类似的不同肤色，但总体而言比较偏灰色。它们的头发趋向于呈黑色或深褐色，眼睛的颜色分布在从黑色到湖蓝色到紫色的广泛色域内，想必是符文转录错误引发的副作用。他们面部的棱角引发了一些与野蛮的兽人族的令人不快的比较，连同强壮的下颌，不成比例地巨大的嘴巴和牙齿，以及方形的头。然而在其他方面，他们十分类似于人类。当然，最为不得不提的是，错综复杂地闪烁着的符文遍布于他们全身，从头到脚，尽管确切的图案和颜色各不相同。

他们一眼看上去就很适合体力任务，并且对于管理符文的重要性使他们手指变得十分灵巧，就连写出来的书法也令人印象深刻。然而，由于他们的庞大体型，他们的肢体动作往往显得缓慢而笨拙。并且，他们如果在艰苦的劳动中透支体力就会很快变得无比疲倦。他们语速缓慢，胃口令人难以置信的大，对艺术和科学基本没有兴趣，引发了广泛的误解，让人们往往趋向于认为这是一个低智商的种族。然而事实上，即便是被迫从事学术工作的食人魔，也表现得令人钦佩。只需要看看他们所制的符文图案，就能了解到他们只要需要的情况下就能发挥出多么伟大的艺术造诣和技术水平。这可能与一种谦卑而尽责的心态有关，这种心态似乎是该种族与生俱来的属性——大部分食人魔对领导他人或者给他人留下深刻的印象毫无兴趣，只一心关注于用最可靠的方式完成他们所做的事，而这种方式往往是最简单而毫不花哨的一种。

或许即使是永恒精灵也有可能放弃魔法的力量，但是食人魔可没有这样的奢侈。他们身上的符文对他们的健康和身体结构的完整性而言，其重要性不亚于任何一个内脏器官。伊格兰斯曾试着“净化”所捕获食人魔身上的符文，结果导致他们先因自身重量而瘫倒，随后器官一个接一个停止工作。可以假定，他们身上的纹身也相当重要。因此，食人魔的生育是一个十分复杂的过程。婴儿们可以保持没有符文的状态几个月，在此之后父母必须在他的身上铭刻一套包含各种符文和纹身的复杂的整体。父母们通常一起完成这项铭刻工作，使用彼此的符文作为参考，并且在这个转录的过程中的任何错误都会影响孩子的健康和发育。通常这一影响是不利的，然而因祸得福，似乎也正是转录错误缓解了食人魔们过去火爆的脾气。因此，孩子们身上所铭刻的符文和纹身对它们未来的发展，和父母本身的身心特质同样重要。

由于埃尔瓦拉的安逸舒适以及食人魔对外部世界根深蒂固的不信任，绝大多数离开家园的食人魔仅仅是为了一些商业目的。不再需要永恒精灵作为他们的中介人，一些人已经开始进入纹身和符文这一不断增长的市场，他们在这方面的天赋使他们在这一领域大获成功。而那些少数可以被视为冒险家的人，往往只是收拾好自己的东西突然离开，不为荣耀和财富，只为消除世界上不断出现的苦难与不幸而为他人奉献。经常听到这样的故事，一个食人魔偶尔听到有满载粮食的货船被劫的消息，立即出发。几天之后，他带着狼牙棒上那伙长期为患的强盗的血回来，然后继续回到乡间照料他的庄稼。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00195 | HUMAN-REVIEW | cross-batch-045 | confirmed | 逐句按源码回改；埃尔瓦拉查术语记录 |  | fix |

<details><summary>hrq-00195 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`careful inscription` 误作“管理符文”；confirmed：`patient study` 与 `if properly motivated` 语义漂移；confirmed：`Conclave's Overseers` 译“孔克雷夫的长老会”缺乏依据；confirmed：`hijacked shipment of grain` 过度具体化为“满载粮食的货船被劫”；confirmed：无占位符、五段结构对应。pending：「全部专名均符合规范」中“埃尔瓦拉”在本批术语快照无记录
```
```
raw verdict: `careful inscription` 误作“管理符文”→confirmed; `patient study` 与 `if properly motivated` 均发生语义漂移→confirmed; `Conclave's Overseers` 译“孔克雷夫的长老会”缺乏依据→confirmed; `hijacked shipment of grain` 被过度具体化为“满载粮食的货船被劫”→confirmed; 无占位符、五段结构对应→confirmed; 全部专名均符合规范（埃尔瓦拉在本批术语快照中无记录）→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-044-01.md](reports/sol-044-01.md)。译文未修改。共 10 个 claim：8 confirmed、2 pending、无 refuted/advisory。 译文未修改。Sol 同时确认了 Gemini 的正面项（占位符与结构），原样记录。
```
</details>

## entry-01306

- 位置：`mod-tome.lua:18119`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Ah, the legendary Sher'Tul! How any scholar does love to write about them. Indeed, the texts are many, but the facts are few, as so little is known about this crucible race. The most learned and factual academic on the subject is the renowned explorer and archaeologist Darwood Oakton, but he has alas been missing for several months at the time of writing. I will attempt to summarise here some of his key discoveries.

The Sher'Tul lived over ten thousand years ago, during what is referred to as the Age of Haze. The name of the race we know from the elves, who speak of the ancient beings with awe and reverence, yet know little else about them. Ruins of fantastical Sher'Tul structures have been found all across Maj'Eyal, and some have been observed in sunken lands off the coasts, implying that in their time the Sher'Tul must have ruled unopposed all across the world.

The farportals were first discovered by the halflings during the Age of Allure, and after much experimentation they were found to be able to transport items and creatures over vast distances. The arcane powers behind these incredible artifacts are still far beyond the understanding of the greatest minds of our time. The one attempt to truly tap into these powers ended in disaster - the Shaloren moved all known farportals to a remote spot near their capital, and their most powerful mages were overwhelmed as they unleashed the Spellblaze, killing them instantly and tearing apart the continent. What remains of farportals are left in the world have since been left untouched.

Of their physical appearance we know almost nothing, as there is no surviving artwork or records which depict themselves. However they must have been of similar form to other common races, as their ruins contain stairs, doorways and rooms not unfit for humans. Oakton estimates from his studies of their tools and artifacts that they would have stood around 5'4" tall, with uncommonly long limbs and fingers.

What caused them to become extinct is unknown, though many theories abound. The most popular in academic circles at the moment is that their mighty magics were their undoing, turned upon their own people during some great civil strife. Other theories hold weight though - Archiman Garybald, Professor of Demonic Studies, believes that the extensive uses of arcane energies by the Sher'Tul may have attracted twisted forces from other worlds which wiped out the ancient race. Some even believe that they are not truly extinct, but are in hiding, or have left this world for elsewhere. I fear the truth may never be fully known, but the ongoing study and examination of the relics they have left behind continues to provide immense value and inspiration.`
- 现译：`啊，传奇的夏·图尔！学者们是多么爱研究他们啊。事实上，相关的文献很多，但有事实根据的很少，所以有关该种族的信息也较少。最权威的研究是基于知名探险家和考古学家达沃德·欧卡顿的发现，但遗憾的是，截至本文写就之时，他已失踪好几个月了。在此，我将总结下他关键性的几个发现。

夏·图尔生活在距今一万多年前，被称为混沌纪的时代。这个种族的名字来源于精灵族，他们以敬畏之情述说着古代种族，即便如此，他们也对其知之甚少。在马基·埃亚尔大陆上，夏·图尔如梦似幻的废墟结构被找出并探索，有的废墟甚至位于海洋中沉没的大陆上，暗示着夏·图尔人曾经一度无可匹敌地统治过整个世界。

传送门的首次发现是在厄流纪，被半身人发现，在大量的实验后他们发现可以将物品和生物传送到很远的地方。这些奇迹背后的奥术原理仍远远超出我们能够理解的范围。唯一一次真正尝试利用这些力量的行为以灾难告终——永恒精灵将所有已知的传送门搬到了靠近他们首都的偏僻之处，他们最强大的法师在释放魔法大爆炸时被力量所吞噬，瞬间死亡，大陆也因此分崩离析。那些在大陆上剩下的传送门，至今无人敢碰。

关于他们的长相几乎没有人说得清，因为没有任何留存的艺术作品或记录来描述他们的外貌。然而他们肯定与其他种族有着类似的特征，因为他们的废墟中存在着适合人类的楼梯、门廊和房间。欧卡顿通过研究他们的工具和遗迹，得出了这样的结论：他们大约高5英尺4英寸左右，有着异常修长的四肢和手指。

他们绝迹的原因始终是个未解之谜，尽管有着各种猜想。在考古界最流行的说法是他们强大的魔法毁灭了自己，内战使他们消弭在历史中。其他理论——阿奇曼·加里伯德，恶魔研究教授则相信，夏·图尔人大量使用奥术能量，可能因此引来了异界的扭曲力量，最终导致整个种族的毁灭。有的人则更相信他们不是真的绝迹了，而是隐匿了起来，或者离开了这个世界。我恐怕真相永远无人知晓，但是对夏·图尔文明的深入研究仍有着非常重要的价值和意义。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00196 | HUMAN-REVIEW | cross-batch-045 | confirmed | 补谓语、放宽学界范围；`crucible` 译法定夺 |  | fix |

<details><summary>hrq-00196 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Other theories hold weight though` 判断谓语漏译；confirmed：`academic circles` 缩窄为“考古界”；confirmed：`crucible` 修饰语被省略。pending：`crucible` 具体译法
```
```
raw verdict: `Other theories hold weight though` 的判断谓语漏译→confirmed; `academic circles` 被缩窄为“考古界”→confirmed; `crucible` 修饰语确实被省略→confirmed; `crucible` 具体译法→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-044-01.md](reports/sol-044-01.md)。译文未修改。共 10 个 claim：8 confirmed、2 pending、无 refuted/advisory。 译文未修改。Sol 同时确认了 Gemini 的正面项（占位符与结构），原样记录。
```
</details>

## entry-01308

- 位置：`mod-tome.lua:18137`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`No text would be complete without at least a brief note of some of the more brutish races which infest our world. These do not hold any civilised society of note, nor in general do they seem capable of any form of higher thought or culture, but they are still of interest to study for any who take delight in analysing beings of more primitive intellect.

Trolls come in two main types - Kezrak and Moltep, or stone and forest trolls as they are colloquially known. Stone trolls infest many mountain chains to the north-east, and some have been known to wander further afield in search of food or to spread violence. They are generally over 8' high, with extremely pronounced muscular strength and a thick, solid hide which bears the appearance of coal or granite. Forest trolls are generally found in dense woods or swamps, with the Trollmire east of Derth being especially infamous. They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons, though their greenish hide is not as thick and their musculature less developed. All trolls have intensely fast metabolisms, capable of healing from grievous wounds within a matter of hours. At birth they measure just eight inches long, but within two years grow to full maturity, and rarely live beyond ten years old. They used to be considered little more than beasts, but towards the end of the Age of Pyre many were trained as fighters by the orcs, and were even taught the basics of language and certain battle tactics, making them much more dangerous. Though the orcs are gone their servants remain, and their remote breeding areas and intense birth rates have so far scampered attempts to eradicate them completely.

Giants live mostly around the mountainous peaks surrounding the Daikara Pass. They vary greatly in size, but are normally at least 10' tall. They look somewhat like large, deformed humans, with swollen or distended facial features and much longer, swinging limbs. They live in nomadic tribes, moving from peak to peak with the seasons, feeding on wild deer and goats. They are usually peaceful creatures, only turning violent when their territory is encroached or their young are threatened. There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare and normally isolated to particularly harsh winters. Giants seem to have no developed culture or language worth mentioning, but have been noted to show interactions of limited intelligence and to commune well in groups.

Nagas were once believed to be mere myth, but reliable reports and even the capturing of dead physical samples has shown them to be real creatures. The upper half of their body is humanoid in form, with blonde hair and an extremely thin build, but the lower half is like that of a giant snake's tail. They stand around 6' tall on land, though their tails extend several feet further. They have been encountered off the eastern and south-eastern coasts of Maj'Eyal, which seems to indicate some exotic civilisation beneath the waves. Records of them exist only from the last few hundred years, and only more recently have they been interpreted as more than just the wild fantasies of inebriated sailors. They can breathe in air and underwater, possessing both lungs and gills, and have been reported to move with surprising speed on the ground. One might think them simply odd monsters, but they decorate themselves in jewellry and craft weapons and armour from materials found on the sea-bed, such as supple mail formed from layers of thick shark-hide. This would suggest an advanced culture, but communication with them so far has proved impossible. It is not known if they are capable of complex speech, but to date their only response to those who encounter them has been extreme violence, and fishermen in the east are always wary of coming across these vicious creatures.

The origin of Demons is not wholly known, but it is clear that they are capable of intelligence and so I feel the need to describe them somewhat here. It is known that they can be summoned by certain magical rites, and minor demons were oft in the employ of evil sorcerers during the Age of Dusk. The main theory, which is supported by certain studies by Shaloren archmages, seems to indicate that they come from another world than our own, with connections formed through intense arcane energies. It must be a truly terrifying place to host such foul denizens. Demons vary immensely in appearance and power, as much as the creatures of our own world vary. They generally have blueish blood and metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness. All seem versed in magical abilities to some degree, and the strongest of them possess truly terrifying powers. Luckily they are exceptionally rare, and seem to be much less common in modern times since magic has fallen out of use.`
- 现译：`任何完整的著述都少不了至少简要提及那些肆虐于我们世界的野蛮种族。他们没有任何值得一提的文明社会，一般来说也不具备高等思维或文化，但是对于那些热衷于分析低等智慧生物的人而言，他们仍然值得研究。

巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生活于东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度和更为发达的言语能力，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。近几百年才有关于他们的记载，而且只是近来人们才开始认为他们不只是醉酒水手的荒诞幻想。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常流着泛蓝的血液，血肉与皮肤呈金属质感，往往会与我们的空气产生奇异反应——有些燃起火焰，有些释放出可怕的酸液或喷吐出黑暗之云。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00197 | HUMAN-REVIEW | cross-batch-046 | confirmed | 逐句回改 |  | fix |

<details><summary>hrq-00197 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×4：`communities` 误作“市民”；`move faster` 重复翻译；`towards the end of` 漏译；`swinging` 漏译
```
```
raw verdict: `communities` 误作“市民”→confirmed; `move faster` 被重复翻译→confirmed; `towards the end of` 漏译→confirmed; `swinging limbs` 中 `swinging` 漏译→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01310

- 位置：`mod-tome.lua:18155`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`The common man may scoff at the idea of classifying dragons as an intelligent race, but experienced wyrmics know otherwise. Dragons are incredibly long-lived creatures, with some known to survive for thousands of years. Though in their early life they are of a bestial nature, as they advance through the centuries they gain an ever keener and more developed intellect. The eldest of wyrms are sometimes considered the most subtle and intelligent of creatures in Maj'Eyal, capable of telepathic communication and advanced mental abilities, and wyrmics speak of them with the highest reverence.

Dragons come in many shapes and sizes, normally growing from 5' long hatchlings to 20' long mature drakes, with some of the greatest wyrms growing to over 40' in length. They are generally winged, with large lizard-like maws and sharp talons on both their fore and hind legs. They are often noted for the lustrous colour of their scales, normally representing an attunement to one of the key Elements of Eyal. This attunement is unseen in any other race, and some philosophers believe that dragons predate all other races, being formed as raw representations of the elements of nature at the beginning of the world. However this theory may be borne purely from the fanatical delusions of certain wyrmics who have studied the creatures for too long.

All corners of Maj'Eyal show some trace of different types of dragons. The Daikara Pass and surrounding mountain chains are home to a great number of ice and storm dragons. Numerous sand and red dragons can be found in the western desert and hills, and many have been the reports of gigantic sea dragons in the deepest oceans, especially to the south.

Attacks from dragons on humans and halfling settlements are fairly rare, but when they occur they can be truly devastating. Usually they are to feed on livestock, but now and then come attacks from newly matured drakes, seeking out precious metals and gemstones to build up a hoard. Dragon hoards have become a thing of legend, with the greatest wyrms rumoured to protect literal mountains of gold, but in modern times truly sizeable hoards are rare. The dwarves farmed hoarding dragons almost to extinction in the Age of Allure, and most dragons these days retain only modest treasures in their lairs.

Dragons are regularly hunted for their thick scales and their elementally imbued bones. Dragonskin leather is prized amongst armour-workers, as when properly treated it is both light and tough, and oft retains some inkling of the original wyrm's power. Dragon-bone is highly favoured by staff-crafters for its natural attunement to elemental forces, and is sometimes used by fletchers in the crafting of the most delicate yet resilient bows and arrows. However the hunting of dragons for their skin and bones is greatly opposed by many wyrmics, and there is an increasing market for "naturally harvested" drake materials - those taken from dragons which have died of natural causes. Still, demand for all dragon materials is strong with exceptionally high prices paid, and many are the greedy souls that lose their lives each year at the fangs and claws of these magnificent creatures.`
- 现译：`一般人也许会嘲笑我把龙作为单独列出的智慧种族，但是经验丰富的龙战士们知道其实不然。龙族是另人难以置信的长寿生命，某些已知的龙族已经存活了数千年之久。尽管在他们早期的生命中，他们兽性的一面比较多，但是随着他们生活几个世纪以后，他们会获得前所未有的超强理解力。那些远古巨龙有时被认为是马基·埃亚尔最狡猾和富有智慧的生物，他们拥有心灵沟通和优秀的精神能力，并且龙战士们始终对龙族有着最崇高的敬意。

龙族有着不同的大小和形状，一般常见于5英尺长的幼仔到20英尺长的成年龙族，某些最强大的龙族体长能达到40英尺。他们通常是带翅膀的、有着蜥蜴般的巨口，前后肢都生有锋利的巨爪。他们通常有着鲜艳色彩的鳞片，通常代表与埃亚尔某种元素的亲和。这种亲和力在任何其他种族都未曾出现过，有些学者认为，龙族先于其他一切种族存在，是在世界之初作为自然元素的原初具现而形成的。然而这个理论只有那些狂热的研究了龙族太久的龙战士信徒们才会相信。

马基·埃亚尔的每一个角落都能发现不同类型的龙族。岱卡拉山脉聚集了很多的冰龙和风龙。大量的沙龙和赤龙可以在西部沙漠和丘陵中找到，并且还有许多报道提到在大洋深处有着巨大的海龙，尤其是在南部地区。

龙族攻击人类和半身人聚居地的事情是少见的，但一旦出现这种情况，通常是毁灭性的灾难。通常它们是为了找牲畜吃，但有时也有来自成年巨龙的攻击，是为了寻找贵金属和宝石来作储藏。龙族的财富已经成为了一种传奇，传说那些最伟大的巨龙守护着真正成山的黄金，但是现在如此多的宝藏几乎没有。矮人们在厄流纪大肆猎捕囤积财宝的龙，使这一类龙几乎绝迹，现在的大部分龙族在巢穴里只有适量的财富。

龙族经常由于它们厚实的鳞片和蕴含元素之力的骨头而被狩猎。龙皮革是护甲制作者们珍视的材料，因为经过适当处理后它既轻便又坚韧，并且通常保留着原龙的一丝力量。龙骨是法杖制作者们最喜爱的材料，因为它与元素力量的天然亲和极高，有时也被用于制造纤薄且柔韧的弓箭。然而，对龙族的不断狩猎引起了许多龙战士们的强烈不满，并且交易“自然采集”的龙族材料的市场也日益增多——那些人只取自然死亡的龙族身上的材料。尽管如此，各类龙族材料的需求依然旺盛，价格也高得惊人，每年都有许多贪婪之徒丧生于这些壮丽生物的尖牙利爪之下。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00198 | HUMAN-REVIEW | cross-batch-046 | confirmed | 改错别字、恢复指代 |  | fix |

<details><summary>hrq-00198 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：“另人难以置信”错别字；`those` 指代误读；`borne purely from … delusions` 语义重心变化
```
```
raw verdict: “另人难以置信”是错别字→confirmed; `those` 的指代被误读→confirmed; `borne purely from ... delusions` 语义重心变化→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01312

- 位置：`mod-tome.lua:18235`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`In Age of Allure rose an archmage high
With power beyond compare
And the people poor would not come nigh
His dark and terrible lair

Whilst crops fell dead in drought and blight
And children grew diseased
The wizard dread stole in the night
To pillage what he pleased

But a hero came with shining sword
And a will of solid steel
Not seeking fame or high reward
He followed but his zeal

"From Zigur I come on righteous quest
To battle foes arcane
I will not succumb to magic detest
I will end this evil reign"

And so he rode on pure-white steed
To the warlock's hold
That dank abode of dark misdeed
He entered brave and bold

There battle blazed beyond all sight
Sword clashed with spell
Blood was razed in fearsome fight
Scream followed yell

A beam was cast of arcane pure
Piercing mail and shield
But still steadfast with flesh secure
The hero did not yield

A slash tore through the wizard's cloth
His hat dropped to the ground
From loose grip flew his staff so wroth
Thus fell the mage renowned

Now bare of skin and weaponless
Here lay but a man
No arcane sin could now redress
The blood that freely ran

"Fool warlock dead, you were too vain
To gifts of Nature trust
Your faith instead in tools arcane
Now to Nature you are dust"`
- 现译：`厄流纪崛起一位大法师
有着无与伦比的能力
贫苦百姓不敢靠近
他黑暗而可怕的巢穴

当作物死于干旱和枯萎
感染疾病的孩童增长
巫师在夜里偷偷的潜入
来掠夺他想要的一切

但是来了一位英雄，他手持宝剑
并且他拥有磐石般的意志
不求名利与荣耀
但求问心无愧

“来自伊格我肩负着使命
打败邪恶巫师是我的义务
我不会屈服于可怕的魔法
我将结束这邪恶的统治”

于是他骑着一匹骏马
向巫师的巢穴前进
幽暗的洞穴吞噬着一切
他却凛然不惧

战斗之激烈难以想象
那是剑与魔法的火花
战斗伴随着鲜血的绽放
怒吼声与尖叫声此起彼伏

一束纯净的奥术射线
撕裂了护甲与盾牌
但他仍坚定信念
英雄永不屈服

刀光划过了巫师的衣袍
他的帽子掉在了地上
法杖也因失去控制而落下
臭名昭著的法师终于陨落

如今赤身裸体、手无寸铁
这里只躺着一个凡人
奥术之罪再也无法弥补
那自由流淌的鲜血

“愚蠢的术士已死，你太过自负
未将信任交给自然的恩赐
你的信念转向了奥术之器
如今你已归于尘土”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00199 | HUMAN-REVIEW | cross-batch-046 | confirmed | 逐句回改 |  | fix |

<details><summary>hrq-00199 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×4：`children grew diseased` 语法误读；`renowned` 被加“臭名昭著”；`zeal` 误作“问心无愧”；`to Nature` 漏译
```
```
raw verdict: `children grew diseased` 语法误读→confirmed; `renowned` 被加入“臭名昭著”贬义→confirmed; `zeal` 误作“问心无愧”→confirmed; `to Nature` 漏译→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01313

- 位置：`mod-tome.lua:18334`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`You wake suddenly from your unexpected slumber and attempt to quickly regain your bearings. However, you are not prepared for the bizarre vision that greets you: instead of land and sky you see only amorphous shapes and varying degrees of light. A strange psychedelic haze permeates the air and otherworldly colors and shadows flicker in and out of your peripheral vision. 
As you begin to come to grips with this strange environment, you realize with horror that you cannot move! Your body feels as if it is completely without weight and try as you may you cannot budge an inch. You experience a sense of Déjà Vu as you recall past nightmares of being paralyzed. That's when it strikes you: you never woke up at all, you're still asleep! This epiphany is only reinforced when you notice a strange phenomenon: mirror copies of yourself are being slowly projected from where you stand and are moving about of their own volition.
They all seem to be focused on something in particular, but what? Just as soon as you set your mind to discerning what your dreamselves are focusing on, you feel it. With horror, you realize that you are not alone here. 
Somehow, your foe has invaded your very subconcious and is attacking you in your dreams. Still unable to move, your lucid mind races on how to handle such an insane and horrible situation. On a whim you concentrate on one of your projections and you find that you can control it. 
Free now to face this nightmare, you turn to find your foe. While you have a sense that having one of your dreamselves destroyed may not by itself be catastrophic, what would happen if several or many are cut down? Unwilling to find out, you resolve yourself to end this offensive intrustion into your mind.`
- 现译：`你从意料外的沉睡中骤然醒来，试图尽快辨明自己身在何处。然而，你对眼前离奇的场景毫无准备：没有陆地，没有天空，只有不断变化的形状和光线。迷幻的烟雾弥漫在空气中，各色阴影在视野中飞舞……
当你的眼睛渐渐习惯这幅奇怪的场景时，你惊恐地发觉你动不了了！你的身体似乎完全没有重量，任你如何挣扎也移动不了一寸。更奇怪的是，当你回想起麻痹的噩梦时，有种似曾相识的感觉，正当此时，你忽然意识到：自己根本没有醒来，仍处于沉睡之中！你突然注意到奇怪的现象，让你更加确信这一点：你自己的镜像正在逐渐从你站的位置产生，并自主行动。
他们似乎都集中精神于某个东西，但那个是什么？正在你思考你的梦中自我在关注什么时，你感觉到了它。你惊恐地意识到，这里不止你一个人。
你的敌人侵入了你的潜意识，开始在梦境中攻击你。虽然依旧不能动，但你的大脑也开始思考如何在这疯狂而恐怖的处境下存活。当你试着集中精神到你的梦中自我上时，你发现你能够控制它。
终于能自由行动去面对这场噩梦，你转身寻找你的敌人，虽然你感觉到让你的一个梦中自我被摧毁似乎不会成为灾难，但如果有数个乃至许多个梦中自我相继被摧毁呢？那会发生什么，你不愿去探究，于是下定决心终结这场对你心灵的侵犯。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00200 | HUMAN-REVIEW | cross-batch-046 | confirmed | 补漏译；不要把“被动天赋”写进裁决依据 |  | fix |

<details><summary>hrq-00200 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×5：`otherworldly` 漏译；`peripheral vision` 泛化；`flicker in and out` 误作“飞舞”；`lucid` 漏译（有设定呼应）；`On a whim` 漏译。advisory：无源省略号。refuted：Gemini 称 `Lucid Dreamer` 是“被动天赋”
```
```
raw verdict: `otherworldly` 漏译→confirmed; `peripheral vision` 泛化为“视野”→confirmed; `flicker in and out` 误作“飞舞”→confirmed; 无源省略号→advisory; `lucid` 漏译且确有设定呼应→confirmed; Gemini 称 `Lucid Dreamer` 是“被动天赋”→refuted; `On a whim` 漏译→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01314

- 位置：`mod-tome.lua:18345`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Dear graverobber,

Try to be a little faster next time.

Love, #{italic}#Eden#{normal}#`
- 现译：`亲爱的盗墓贼，

下次记得快一点。

你钟爱的#{italic}#艾登#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00201 | HUMAN-REVIEW | cross-batch-046 | confirmed | 修主客关系 |  | fix |

<details><summary>hrq-00201 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Love, Eden` 主客关系改变；confirmed：样式与换行无问题
```
```
raw verdict: `Love, Eden` 主客关系改变→confirmed; 样式和换行没有问题→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01315

- 位置：`mod-tome.lua:18375`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`#{bold}#How to Summon a Phoenix#{normal}#
	  10 pouches faeros ash
	  5 vials fire wyrm saliva
	  3 red crystal shards
	  3 pouches bone giant dust
	  1 vial greater demon bile
	  1 skeleton mage skull
	  pinch of luminous horror dust

This is a long and complex ceremony, and all steps must be followed precisely if you wish to succeed. Heed well that for the errant fool who takes on what they cannot finish, there will be consequences. To play with fire and assert your dominance over the flames comes with risks if you overestimate your power. 
	
The ritual begins with a vessel; any man will do. Bind them in place with flame secure bindings, and give a sound gag. The gag isn't strictly necessary, but the screams of agony tend to be quite distracting and inspirit mistakes after a few days.

Take 2 vials fire wyrm saliva and dissolve 2 pouches faeros ash in each. Be sure to dissolve completely. A few fireballs at the vial can do the trick if they're stubborn. Using one of the prepared vials, begin to etch the saliva in the skin of the vessel, heating it so that it brands the shape of --- 

#{italic}#The remainder of the scroll has been singed into a pile of char, illegible and scattering into a cloud of ash as you grasp it#{normal}#
	`
- 现译：`#{bold}#如何召唤凤凰#{normal}#
	  10袋法罗的灰烬
	  5瓶火龙涎
	  3块红色水晶碎片
	  3袋骨巨人骨灰
	  1瓶大恶魔胆汁
	  1个骷髅法师头骨
	  一小撮金色恐魔的粉尘

这是一个漫长而复杂的仪式，如果你想要成功的话，就必须严格遵循所有的步骤。要知道，自视过高的蠢材如果冒险进行自己没有能力掌控的仪式，一定会迎来自己应得的下场。如果你高估了自己掌控火焰的力量，那么等待你的只有玩火自焚的结局。

仪式需要一份祭品，随便哪个人都可以。用防火胶布把他绑住，塞住他的嘴巴。虽然塞住嘴巴这一步不是必须的，但是那个人痛苦的惨叫会让人相当分心，几天下来容易让你在仪式中出错。

取2瓶火龙涎，每瓶各溶入2袋法罗的灰烬。一定要充分溶解。如果还有没有完全溶解的部分，就往瓶子里放几个小火球。使用一瓶准备好的溶液，用火龙涎在祭品的皮肤上蚀刻，加热使其烙出——的形状——

#{italic}#卷轴的剩余部分已经被烧焦了，无法辨认。当你抓到这份卷轴的时候，那些残存的纸页就化为了灰烬#{normal}#
	`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00202 | HUMAN-REVIEW | cross-batch-046 | confirmed | 删臆造物件；查“法罗”术语记录 |  | fix |

<details><summary>hrq-00202 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“防火胶布”加入源码没有的物件类型；confirmed：`luminous horror dust` 用冻结术语；confirmed：清单缩进与样式完整。advisory：截断破折号改双侧包裹。pending：“法罗的灰烬”是否固定译名
```
```
raw verdict: “防火胶布”加入源码不存在的物件类型→confirmed; 截断破折号改成双侧包裹→advisory; `luminous horror dust` 使用了冻结术语→confirmed; “法罗的灰烬”是固定译名→pending; 清单缩进和样式标签完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01316

- 位置：`mod-tome.lua:18410`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Your arcane abilities have been interfered with!

Eyal is a torn world, and the forces of nature can react strongly to the arcane energies that seek to manipulate them. Some items and areas are imbued with anti-magic, a natural energy that disrupts magical abilities and effects. There are even those who have learned to harness anti-magic into their own wild abilities, and who use them to hunt down and destroy those who practise magic. So beware, caster! It is a hostile world ye wander in.`
- 现译：`你的奥术能量被干扰了！

埃亚尔是一个被撕裂的世界，自然力量会对试图操纵它们的奥术能量产生强烈反应。某些物品和地方被灌输了反魔力量，这是一种能干扰魔法能力和效果的自然能量。甚至还有一些人学会了驾驭反魔力量，将其融入自身的野性能力中，用于猎捕并摧毁魔法使用者。小心，施法者！你漫游的世界并不友好。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00203 | HUMAN-REVIEW | cross-batch-046 | confirmed | 视术语决定是否改 |  | fix |

<details><summary>hrq-00203 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`arcane abilities` 译“奥术能量”；confirmed：其余核心词义与排版无异常
```
```
raw verdict: `arcane abilities` 被译成“奥术能量”→confirmed; 其余核心词义和排版无异常→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。 译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。
```
</details>

## entry-01317

- 位置：`mod-tome.lua:18417`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`I must say, as time grows, I feel so do I grow more and more inclined to distance myself from the calling of an 'adventurer', like so many you can find roaming the countryside. I feel like the myth of a wandering hero has blinded too many with promise of easy fame and riches, with no eye for the other kind of fortune.

Hear me out on this.

Nowadays most don't really recognize how fascinating the world we live in truly is. It is vast, more than you can imagine. I can safely promise, any wild thought you can muster up, dear reader, will not come close to the truth. Such is the breadth of wonders, I would probably dismiss most of what I have seen as myth, be I not there myself. And even then sometimes, I had to wonder whether I could trust my eyes.

Perhaps I'm being too vague, or maybe these promises leave much to be desired. After all, adventuring is not all fun and exotics, it is before all danger and a constant threat of death, or worse. So then if you wish me to be more concrete, think of derelict, crumbling crypts, cults and demons, hungry forests full of monsters and forces beyond time and place. True, there is overwhelming awe, thrill even, but the reason that so little detail reaches you, is because so little live to tell.

What does reach us then, are not people, but objects. Artifacts of great power, legacy of the past. Surely, any drunkard might like to tell tales after a pint or two, but a magical sword is a proof of its own and it keeps quiet of what it has seen. So, a great hero is usually easy to recognize, being practically a walking history book. Clad in half the age of important events which he probably has no idea about.

It is important to remember, that every artifact has a meaning, beings of great power and importance behind them. Stories, that now slowly wane into nothing. This is why it is not artifacts that make an adventurer. It is his great deeds, the will to dare where nobody did before. It is not important if you get known in the process or not, after all, if you were truly great, maybe you will leave behind a legacy of your own.

-#{italic}#Kestin Highfin#{normal}#`
- 现译：`我必须说，随着漫长的冒险岁月，我似乎与那些在你们眼中的“冒险家”，也就是那群在乡间小路上的流浪者们渐行渐远。我想，或许是那些流浪英雄的神话使得那些金钱和荣誉的诱惑蒙蔽了你的双眼，让你们忽视了真正的财富就在我们的身边。

诸君啊，敬请听我一言。

现在，许多年轻人根本无法理解，我们身处的这个世界究竟是多么神奇而又美好，远远超出了任何人的想象。我向你们中任何一人保证，亲爱的读者啊，无论是在你脑海中多么狂野的梦想，在那无比瑰丽的真实世界面前都是那么渺小，这就是真正奇迹的恢弘气势。若非我亲身在场，我多半会把自己亲眼所见的大半都当作神话；纵然亲历，有时我仍不免怀疑自己的眼睛。

或许，我的描述有些过于模糊，或许，这些保证有些难以置信。毕竟，冒险并不总是充满了探索未知的喜悦——那是前所未有的危险，无时无刻不伴随着死亡的威胁，甚至更糟。所以，如果你想要让我用语言描述的话——请想象一下，废弃的远古地宫里巨岩崩碎跌落；疯狂的邪教徒将恶魔从异次元唤来；随着远处猛兽的咆哮，外表平和的森林展露了它嗜血的本性；还有，与之伴随的，超越时空约束的强大力量。这就是真实的冒险，任何人都会为其壮丽景象所倾倒，为其沉醉——尽管，我们所能了解的实在只是冒险旅途的吉光片羽，毕竟只有极少一部分的人能生还下来，告诉我们他们真实的经历。

那么，最终传到我们手上的并不是人，而是物：那是身怀强大力量的神器，是往昔留下的遗产。当然，在灌下一两杯之后任何一个醉鬼都能够信口开河，胡诌一通；然而，一把灌注着强大魔力的利刃从来不会说谎，它们是冒险史诗的诚实记录者，然而始终保持缄默，从不多言。所以说，一个伟大的英雄往往在装备上就引人注目。他们如同活动着的历史，身上的每一件物品都诉说着宏大的史诗，其中至少有一半连他的主人都没有丝毫了解。

要记住重要的是，每一件神器的背后都有其意义，都代表着曾经手持它们的那些强大而重要的存在。然而他们的故事如今正渐渐被人淡忘。这就是为什么说，成就一个冒险家的并不是神器，而是他的伟大事迹，是敢为天下先的勇气。你的功绩是否为人所知并不重要——毕竟，如果你真的足够伟大，或许你也会留下属于自己的传奇。

——#{italic}#科斯汀·赫菲因#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00204 | HUMAN-REVIEW | cross-batch-047 | confirmed | 扩写与范围词回改；身份解释不要写进修复理由 |  | fix |

<details><summary>hrq-00204 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：并列意象被大幅扩写；confirmed：“大多数人”缩窄成“许多年轻人”；confirmed：`before all` 误作“前所未有”；confirmed：`too many` 改第二人称并增义。refuted：“他的主人”并未把英雄误认成另一位主人
```
```
raw verdict: 并列意象被大幅扩写→confirmed; “大多数人”被缩窄为“许多年轻人”→confirmed; `before all` 被误作“前所未有”→confirmed; `too many` 被改成第二人称并有额外增义→confirmed; “他的主人”本身并未把英雄误认成另一位主人→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。 译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。
```
</details>

## entry-01318

- 位置：`mod-tome.lua:18444`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Congratulations, sir and/or madam. Whether by invitation, discovering it on your own, or simply being enough of a thorn in our side to recruit rather than dispose of, you have gained the secrets of chronomancy. The ultimate power of time - the ability to reset and try again if you fail, the ability to save time by seeing the results of investigations before they happen. Though our powers are bound to post-Spellblaze Eyal, they are those of nigh-omnipotence with enough patience.

But trust me - "enough patience" is one nasty limiting reagent. You're going to be running out of that fast when you've spent the last week trying to dismantle an Age of Dusk-era house-of-cards system of causally interdependent tyrannies without causing dwarven extinction, and a plague just broke out right when you had things almost perfect, for the sixth time--

Look. The point is, there's a reason the person who writes the invitations and the mission statements isn't someone out in the field - and you're lucky enough to be working for someone who understands that you need more flexibility than idealism allows. Our squad knows that to stay sane, we have to know when "time flows forward at a rate of one second per second" isn't the only rule we have to break. That it's generally okay to skip the trial and just deal with a temporally hazardous jackass as you see fit, if you've foreseen a guilty verdict - as long as your investigations are solid when you actually conduct them (and you do have to do the work once in a while, or you'll only be capable of seeing yourself procrastinating). And if you just need to not be watched, you should know that there are a few decades in the Age of Dusk we and a few other squads recognize as "fair game" - whatever experiments you've wondered about or horrors you want to inflict, just keep it to the time period of infinite forgotten evils and it doesn't hurt anything in the grand scheme. Trust me, we've checked - nothing in that time period matters unless you've got another Spellblaze to set off.

But most importantly, you should know: Zemekkys is even lazier than I am, but he has status to maintain. If you continually violate his will, there will come a point at which you will be informed that you have been caught and should stop resisting. Accept whatever fate he doles out for you. If you do not stop, there will come a point where he will be forced to make an example of you so severe that the entire cosmos will notice your non-existence. Obviously we can't be sure how many of us he's done this to (if any) or how it works, but we're pretty sure that the result looks like something starting with a W.

Everyone here wants the same thing - keep spacetime stable, have fun with your powers, cheat at a few lotteries - but we've got cover to maintain and, in theory, an actual job to do if something ever cracks that Sher'Tul shield or the Greigu find a way to bypass a portal-filter. Scratch backs when yours gets scratched, don't make so much noise that the system comes crashing down on your head, and you'll enjoy your stay in eternity.

Welcome to Point Zero, agent. Enclosed are timespace coordinates to what is, quite literally, the best roast-yeti restaurant that could possibly exist - I'll have the squad meet you there and then. Thank me later.

[i]-Galsamae[/i]

PS: You might encounter a... benefactor of sorts in your travels. You'll know it when you see it, ham-fistedly yanking its puppets back from the brink of death; if you see it for yourself, we regret to inform you that you've taken a one-way trip off prime Timeline-E4-RL territory for a doomed offshoot unless "he" feels like weaving you back in - and it tends to only do that to people who narrowly avert its engineered apocalypses through incredible power or luck. If you have been chosen by its schemes, play along and you might get brought back from the temporal graveyard that is the Timeline-E4-EXPADV subnetwork. We do not know what it is - a runaway creation of our own, a competing culture's weapon, or something far above ourselves - but if it has hostile intent, it has already won. So far it's been... mostly cooperative. Just make a point not to remind it that we're its competition.`
- 现译：`女士们先生们，恭喜你。无论是你受到了时空的邀请，是你自己发现了这一切的秘密，还是作为我们曾经的眼中钉，觉得比起对付还是招揽你更好，总之，你已经获得了时空魔法的奥秘。我们掌握有关时间的终极力量——能够在你失败时不断重试，能够通过预知结果来节约时间，甚至在调查发生前就看到结果。尽管我们的能力被限制在于魔法大爆炸后的埃亚尔，只要你有足够的耐心，我们将可以无所不知，无所不能。

不过，相信我——“足够的耐心”已经是足够令人讨厌的限制了。如果你曾经花费整整一周的时间，试图拆解黄昏纪暴君你方唱罢我登场的政治游戏，还不能让矮人一族因此灭绝；结果就在一切眼看近乎完美的时候，一场瘟疫偏偏爆发了，毁掉你满盘的计划——而且这已经是第六次了——很快你也会丧失耐心的。

看。这就是问题的关键。那些任务说明和邀请之所以不是由一线人员撰写的，是有原因的——你也有同样的幸运，我们知道在你的工作中需要的“灵活性”远比理想主义更重要。我们的小队知道要保持理智，我们也知道“每过一秒就有一秒钟的时间流过”也只是我们要打破的众多规律之一。如果你能够预见到一个有罪判决，在时空中不经审判处理掉一个潜在的罪犯也不是什么大事——只要你的调查可以被证明是确凿可信的（而且总有一天你要亲自做这件事，否则你只能看到自己不停拖延）而且，如果你只是想要一个不被监视的地方，你知道，在黄昏纪的一些时代被我和其他几个小队当做了“公平竞赛”的区域——无论你想要做什么样的实验，或者想要给其他人带来怎样的恐怖，只要你到那些有关无尽的被遗忘的邪恶的时间段去做，这不会对事情的大局产生任何影响。相信我，我们已经确认了——这段时间发生的一切事情都无足轻重，除非你真有本事引发第二次魔法大爆炸。

不过你还是要知道一些最重要的事情：虽然泽梅基斯比我还懒，但他也有他要维持的东西。如果你不停违抗他的意志，总有一天，你会被告知，你已经被抓到了，请你停止抵抗。接受他为你安排的命运。如果你仍然负隅顽抗的话，很快，他会不得不把你作为一个严厉的例子，以至于整个宇宙都会注意到你的灭亡。很显然，我们也不确定他真的对谁做过这样的事情，或者是他到底会做什么，不过，我们可以确定，你的命运会和某个以“W-”开头的东西差不多。

这里的所有人都有一致的目标——保持时空稳定，享受自己的力量，和概率开个玩笑——但是我们有要维持的掩护身份，并且，理论上来说，当有人摧毁了夏·图尔防护罩或者Greigu找到了一个方法穿越传送门屏障之类的事情发生时，我们是真的有事可做的。别人帮了你的忙，你也要记得还回去；但别把动静弄得太大，免得整个系统在你头顶崩塌。如此这般的话，你就能享受这份永恒。

欢迎来到零点圣域，特工。这里面装的时空坐标指向的东西，只有我们可以毫不客气地说，是有史以来可能存在的最好的烤雪人餐厅——我的小队会在那时那地等你。一会儿谢。
[i]-加尔萨麦[/i]

注：你可能会在旅途中遇到一些……某种意义上的恩人。当你看见它时就会认出它——它正笨拙地把它的傀儡从死亡边缘拽回来。如果你亲眼见证了这一切，我们很遗憾地通知你，你已经踏上一条单程旅途，离开了作为主时间线的E4-RL辖域，落入一条注定灭亡的支线——除非“他”愿意把你重新编织回来。而它似乎一般只会对那些凭借惊人的力量或运气、堪堪躲过它一手策划的末日的人这么做。如果你已被它的算计选中，那就顺着演下去，你或许能从E4-EXPADV时间轴子网络那座时间坟场里被带回来。我们不知道它是什么 —— 到底是我们自己失控的创造物，是某个竞争对手的武器，或者远远超出我们自己的东西 —— 但是如果它有敌意，它已经赢了。到目前为止，它一直是……处在合作的状态。请注意不要提醒它我们是它的竞争对手。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00205 | HUMAN-REVIEW | cross-batch-047 | confirmed | 六处按源码回改 |  | fix |

<details><summary>hrq-00205 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`fair game`→“公平竞赛”；confirmed：`a few decades`→“一些时代”；confirmed：`once in a while`→“总有一天”；confirmed：烤雪人餐厅句增“只有我们”；confirmed：单数 benefactor 译成复数；confirmed：“被限制在于”句法杂糅。advisory：`Thank me later`→“一会儿谢”生硬
```
```
raw verdict: `fair game` 误译为“公平竞赛”→confirmed; `a few decades` 误译为“一些时代”→confirmed; `once in a while` 误译为“总有一天”→confirmed; 烤雪人餐厅句增加“只有我们”→confirmed; `Thank me later` 译“一会儿谢”生硬→advisory; 单数 benefactor 被译成复数“一些……恩人”→confirmed; “被限制在于”句法杂糅→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。 译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。
```
</details>

## entry-01319

- 位置：`mod-tome.lua:18474`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Each morning I wake, happy I'm alive;
the traps of this tomb won't claim me today.
Though its curse of hunger eats at my insides,
I curse it one better by having outstayed.

Say a curse for the goblins' tortures that remained,
and a curse for the gods who stole half the world.
Say a curse for the chill that leaves magic drained,
and a curse for the star that grew dark as it swirled

But most important of all is to note,
in spite of fate's bias, only we survived.
Curse the dead all you want, but we've stayed afloat;
we're the only ones blessed with the skillset to thrive.

Our wit, strength, and teamwork outweigh cosmic powers;
they've done what they could but Spydrë is [b]ours.[/b] `
- 现译：`每个清晨醒来都庆幸自己还活着
这座墓穴的陷阱今天仍未能索我的命
尽管它饥饿的诅咒啃噬着我的脏腑
我却以活得比它更久回敬了这道诅咒

诅咒哥布林留下的那些酷刑
诅咒窃走半个世界的神祇
诅咒抽干魔力的严寒
诅咒旋转着黯淡下去的星辰

但最要紧的是记住
纵使命运偏私，唯有我们幸存
尽情诅咒亡者吧，我们却依然屹立
唯有我们被赋予了兴盛的本事

我们的智慧、力量与协作胜过宇宙伟力
它们已尽其所能，但斯派德[b]属于我们[/b]。 `

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00206 | HUMAN-REVIEW | cross-batch-047 | confirmed | 诗文本身不判错；一致性另取冻结样本 |  | fix |

<details><summary>hrq-00206 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`won’t claim me today` 决意语气丢失。advisory：粗体句点移到标记外；advisory：诗歌标点体例风格化。pending：“斯派德”跨条目一致性结论
```
```
raw verdict: 粗体标记中的句点被移到标记外→advisory; 诗歌标点体例风格化变化→advisory; `won’t claim me today` 决意语气丢失→confirmed; “斯派德与同 section 及装备译名一致”的完整一致性结论→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。 译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。
```
</details>

## entry-01320

- 位置：`mod-tome.lua:18509`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`#{italic}#(The handwriting of this diary entry is poor at best. Whoever wrote this was in poor health.)

#{bold}#53rd Allure, Year 603 of the Age of Pyre#{normal}#

I have done it! My fool of a master said I was not ready for the rites of lichdom, that I would attract undue attention... what utter idiocy. Already I can feel the transformation taking place, and I am certain that this weakness will only be momentary. My master was foolish to leave the Grimoire of Mortality Transcended open and unattended! All I needed was a bone from a magical creature, and as luck would have it, I had found a skeletal corpse of a dragon not far from our tower. The other ingredients were trivial and in possession of my master... surely he will be astounded that I, Zilquick the Eternal, will have transcended mortality!

(Another entry is written beneath this one, in a much more elegant and controlled script.)

Zilquick the Eternal, hah! What an unbearable buffoon, and I am glad his pride was his undoing. The young fool used up the Ruby of Eldoral in creating his phylactery, however; I must acquire a new phylactery for myself. On the bright side, my incompetent apprentice did illustrate why a bone from a creature slain by my own hand is important: the dragon bone he chose had left to fester a mold infection, and the mold somehow infused itself with the bone's inherent magical properties, altering the magical composition of the spell. I do hope whoever finds this note shall kill this "lich" using the most painful means available, and shall deposit him someplace where he is sure to be found.
Oh, look. He is trying to harm me with spells, but all he can manage is a corruption of his own name: Z'quikzshl.`
- 现译：`#{italic}#（这篇日记的字迹很差。写日记之人似乎健康状况不佳。）

#{bold}#烈火纪603年，厄流月53日#{normal}#

我完成了！我愚蠢的主人说我没有做巫妖的条件，我会引来不必要的关注……说什么蠢话。我已经感觉到了身上的变化，并且我确信这虚弱只是暂时的。我的主人竟然愚蠢到忘记合上《死亡转化禁书》！我需要的只是一根魔法生物的骨头，幸运的是，我在塔周围不远处找到了一具龙族的骨架。其他材料都太次，并且完全被主人所掌控……他肯定会震惊于我，不朽的兹基克，将会超越生死！

（这段文字下面还写着另一段记录，笔迹更加优雅工整。）

不朽的兹基克，哈！多么愚蠢的小丑。我很高兴他的骄傲最终毁掉了自己。然而讨厌的是，这个年轻的傻小子在制作他的命匣时用光了艾德瑞尔之石，所以我也必须为我自己做一只命匣。从好的一面来说，我那不成器的学徒从反面说明了为什么我们应该使用亲手杀死的生物的骨架作为死亡转化的道具：他所选择的那具龙骨正在发霉溃烂，并且附在上面的霉菌似乎利用了骨头内的魔法能量，改变了咒语的魔法组成。我真心希望任何发现这篇手稿的人能以最残忍的方式杀死这只“巫妖”并把他丢到一个肯定会被人找到的地方。
哦，看呐，它正在试图用法术攻击我，不过他所能做的只是拥有一个堕落的名字：兹基克茨。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00207 | HUMAN-REVIEW | cross-batch-047 | confirmed | 改末句与指代；剧情解释不写成事实 |  | fix |

<details><summary>hrq-00207 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：末句 `manage/corruption` 被曲解；confirmed：同句“它／他”指代不统一；confirmed：`trivial` 误作“太次”。refuted：Gemini 对“他无法施法，只能发出名字声音”的剧情解释无源码支持。pending：“太次”是否与红宝石昂贵性直接矛盾
```
```
raw verdict: 末句 `manage/corruption` 被曲解→confirmed; Gemini 对“他无法施法，只能发出名字声音”的进一步解释无源码支持→refuted; 同一句“它／他”指代不统一→confirmed; `trivial` 被误译为“太次”→confirmed; “太次”与艾德瑞尔红宝石昂贵性构成直接矛盾→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。 译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。
```
</details>

## entry-01321

- 位置：`mod-tome.lua:18529`（tome）｜section：`mod-tome/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`Dirge of the Naloren

There once was a village
the Nalore held dear,
but when Ol' Walrog came t'pillage,
they cowered in fear.

He trampled their men
and their babes newly born,
and seeing it finished,
he summoned a storm.

So remember old Shellsea
as she was in the past,
for Ol' Walrog sent the gale
that drowned her at last.`
- 现译：`纳鲁精灵的挽歌

从前有一个村庄
为纳鲁人所珍爱
可当乌尔罗格前来劫掠
他们只能在恐惧中颤抖

他践踏村庄的人民
不放过初生的孩童
眼见此事已了
他唤起一场风暴

所以，请记住贝壳之海
记住她昔日的模样
因为乌尔罗格放出的飓风
终究将她淹没。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00208 | HUMAN-REVIEW | cross-batch-047 | confirmed | 保留专名；标点按体例统一 |  | no_change |

<details><summary>hrq-00208 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Shellsea` 是前述村庄专名。advisory：诗歌标点前后不统一
```
```
raw verdict: `Shellsea` 是前述村庄的专名→confirmed; 诗歌标点前后不统一→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。 译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。
```
</details>

## entry-01326

- 位置：`mod-tome.lua:19079`（tome）｜section：`mod-tome/data/lore/orc-prides.lua`｜source_tag：`_t`
- 原文：`Sher'Tul ruin matches description from high command. Investigation begun, but slow. Looks like it crashed into the ground long ago - hard to access many areas. Target item has been described by command as a staff. Do not know why a staff so important. Surely the ultimate weapon should be a sword or axe, like that wielded by the great Garkul?

Have heard many rumours against high command lately - strange rumours, indeed. Perhaps by completing this mission I shall get closer to them so that I might seek the truth...

...

Curses and banes! Some bastard blaze-born THIEF has raided the ruins! And a halfling no less, a curr-damned halfling! I am pyred with rage!

He got in during dusk somehow, crawling through a tunnel too narrow for my workers to reach. He grabbed a staff from the ruins and snuck out past my orcs! The dirty, treacherous sneak has run away, and my career with him! I have sent scouts to track him, but he is proving elusive. But I will not let him escape! This is unforgiveable!

...

We've followed the tracks of the wretch. It seems as if he met up with a dwarf and a human near a town called Derth, and they travelled south-east from there. Following the three of them was much easier than the sneak alone, but we still must take care to remain hidden. Our orders from high command strictly forbid showing ourselves, and we must avoid battle as much as possible. I have a trained team of archers and fighters with me that know how to stay hidden in the woods.

The thief and his cursed allies have entered an old ruined tower called Dreadfell. It an ancient place, known to be filled with undead in its dungeons. If we break in we're bound to cause a stir, and so close to the big human town east of here... I am not sure how to proceed, and have sent a message to command requesting instructions. For now we wait in the woods, keeping an eye on the entrance for any change. If anyone comes out from the tower with that staff they will face my wrath!

...

Word is finally back from command - hold position and wait for the staff to emerge. If it doesn't happen soon then they will send their own agents in time.

In time! Bah! This will be my ruin if it comes to that. If there is any appearance of the staff I must snatch it and get back East as soon as possible...`
- 现译：`夏·图尔废墟与最高统帅部的描述完全一致。调查已经展开，但进展缓慢。看起来它在很久以前就坠毁到了地面上——许多区域都难以进入。统帅部将目标物品描述为一根法杖。不知道为何一根法杖会如此重要。最强的终极兵器难道不该是剑或战斧吗，就像伟大的加库尔所挥舞的那样？

最近听到了许多针对最高统帅部的流言——确实是些古怪的流言。或许通过完成这次任务，我能更接近他们，从而探寻真相……

……


该死！诅咒降临！不知哪个天杀的烈焰杂种盗贼洗劫了废墟！而且竟然是个半身人，一条该死的半身人杂种狗！我真是怒火中烧！

不知怎的，他趁着黄昏潜入了进去，爬过了一条连我的劳工都进不去的狭窄地道。他从废墟里夺走了一根法杖，竟然从我的兽人身边偷偷溜了出去！这个肮脏阴险的潜行者逃之夭夭了，我的前程也随之搭了进去！我已派斥候追踪他，但这厮极其狡猾。但我决不能让他逃脱！这绝对不可饶恕！

……


我们循着那个无赖的踪迹一路追踪。看来他在一个叫德斯镇的地方与一名矮人和一名人类会合，随后一同向东南进发。跟踪他们三个人比跟踪单独一个潜行者容易得多，但我们仍必须格外谨慎以保持隐蔽。最高统帅部的指令严禁我们暴露行踪，且必须尽可能避免战斗。我随身带领着一支训练有素的弓箭手与战士小队，他们懂得如何在林中隐匿。

那个盗贼和他该死的同党已经进入了一座名为恐惧王座的古老废弃高塔。那是一处古老的地方，地牢中素以塞满不死亡灵而著称。如果我们强行闯入必将引起骚动，况且此处离东面的人类大城镇又是如此之近……我拿不准该如何行事，已向统帅部发信请示指令。眼下我们潜伏在林中，密切注视着入口处的动静。若是有人带着那根法杖从塔里出来，定要承受我的滔天怒火！

……

统帅部终于传回了回信——坚守阵地，等待法杖现身。若是近期内仍未出现，他们届时会派出自己的密探。

届时！呸！真到了那个地步我就彻底完了。一旦那根法杖露面，我必须一把抢下它，以最快的速度返回远东……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00209 | HUMAN-REVIEW | cross-batch-048 | confirmed | 是否要求三处分段严格统一，低优先级 |  | no_change |

<details><summary>hrq-00209 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：前两处分隔符后各多一个空行，第三处没有（源码每处只一空行）
```
```
raw verdict: 前两处分隔符后各多出一个空行，第三处没有→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。 译文未修改。
```
</details>

## entry-01328

- 位置：`mod-tome.lua:19211`（tome）｜section：`mod-tome/data/lore/sandworm.lua`｜source_tag：`_t`
- 原文：`I have stared in the mouths of crimson wyrms
And felt the claws of drakes so sleek
But through deserts dry and sandy storms
There is something else I seek

In the trail of giant worms I walk
Through tunnels of sand below
Of arcane tools let there be no talk
It's on the wyrmic path I go!`
- 现译：`我曾凝视赤红巨龙的巨口深处
也曾领教矫健幼龙利爪
可穿过干旱荒漠与沙暴
我所追寻的另有其物

我循着巨型沙龙的踪迹
穿行在地下沙土隧道
休要再提那些奥术器具
我走的是龙战士之道！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00210 | HUMAN-REVIEW | cross-batch-048 | confirmed | 改“巨型沙虫”；附加论据需主流程另取冻结文本 |  | fix |

<details><summary>hrq-00210 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`giant worms` 译“巨型沙龙”混淆 worm/wyrm；confirmed：破坏诗中龙／虫对照。pending：同 section 另两处已译“沙虫”“传奇巨虫”的附加论据（冻结输入未收录那两处）
```
```
raw verdict: `giant worms` 译“巨型沙龙”混淆 worm 与 wyrm→confirmed; 同 section 另两处已译“沙虫”“传奇巨虫”的附加论据→pending; 该错译破坏诗歌的龙／虫对照逻辑→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。 译文未修改。
```
</details>

## entry-01331

- 位置：`mod-tome.lua:19358`（tome）｜section：`mod-tome/data/lore/shertul.lua`｜source_tag：`_t`
- 原文：`which you do not understand: #{italic}#'Sho ch'zun Eyal mor donuth, ik ranaheli donoth trun ze.'#{normal}#`
- 现译：`不明意义的文字：#{italic}#“Sho ch'zun Eyal mor donuth, ik ranaheli donoth trun ze.”#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00211 | HUMAN-REVIEW | cross-batch-048 | advisory | 若要统一引号，作为整个 section 的独立排版决策 |  | no_change |

<details><summary>hrq-00211 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：外层直单引号被改成中文双引号，冻结语境本身风格混杂
```
```
raw verdict: 外层直单引号被改成中文双引号，属标点风格变化→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。 译文未修改。
```
</details>

## entry-01333

- 位置：`mod-tome.lua:19365`（tome）｜section：`mod-tome/data/lore/shertul.lua`｜source_tag：`_t`
- 原文：`#{italic}#'But AMAKTHEL came, and his might surpassed all else, and the petty gods fled before his glory. And he made the Sun from his breath and held it above the world and said, "All that this light touches shall be mine, and this light shall touch all the world.'#{normal}#`
- 现译：`#{italic}#但阿马克泰尔来了，他的勇武震慑了众人，伪神们慑服于他的荣耀。他深呼吸后把太阳高举到了世界之上，说：“阳光所至，即我所至，这光芒将照亮全世界。”#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00212 | HUMAN-REVIEW | cross-batch-048 | confirmed | 按源码整段重译，不逐词补丁 |  |  |

<details><summary>hrq-00212 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×4：`made the Sun from his breath` 漏“创造太阳”；`fled before his glory` 反向译成“慑服”；`All that this light touches shall be mine` 所有权宣告遗漏；`his might surpassed all else` 窄化为“勇武震慑众人”。Sol 建议整句重译
```
```
raw verdict: `made the Sun from his breath` 误译，遗漏“创造太阳”→confirmed; `the petty gods fled before his glory` 被反向译成“慑服”→confirmed; `All that this light touches shall be mine` 所有权宣告被遗漏→confirmed; `his might surpassed all else` 被窄化为“勇武震慑众人”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。 译文未修改。
```
</details>

## entry-01334

- 位置：`mod-tome.lua:19370`（tome）｜section：`mod-tome/data/lore/shertul.lua`｜source_tag：`_t`
- 原文：`which you do not understand: #{italic}#'Ik AMAKTHEL cosio SHER'TUL, ik baladath peris furko masa bren doth benna zi, ik blod is "Fen makel ath goru domus ik denz tro ala fron."'#{normal}#`
- 现译：`不明意义的文字：#{italic}#“Ik AMAKTHEL cosio SHER'TUL, ik baladath peris furko masa bren doth benna zi, ik blod is "Fen makel ath goru domus ik denz tro ala fron."”#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00213 | HUMAN-REVIEW | cross-batch-048 | advisory | 统一嵌套引号规则后再处理，不升级为正确性问题 |  |  |

<details><summary>hrq-00213 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：外层中文双引号与内部半角双引号形成嵌套
```
```
raw verdict: 外层中文双引号与内部半角双引号形成嵌套→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。 译文未修改。
```
</details>

## entry-01347

- 位置：`mod-tome.lua:19639`（tome）｜section：`mod-tome/data/lore/sunwall.lua`｜source_tag：`_t`
- 原文：`Loremaster Verutir here. I have been assigned to write an official chronicle of the history of the Sunwall. This will be my notebook as I interview people and travel from place to place. If you are reading this, you are either my patron (thanks again, sir!), a sneak (get out of my journal!), or the finder of my corpse. If the last, please take this to Lord Forosyth of the town of the Sunwall for a reward, tell my wife how I died, and tell the kids that I love them.
With that said I shall be starting this project by investigating the Elves and their connection to the Sunwall. They should be one of the easier races to interview considering their life expectancy and their penchant for remembering their own history. Of course, there aren't as many of them around as there used to be.
...
Unfortunately though, our local Elves are also unwilling to talk to me about their history, saying they do not have records of the earlier times. However, there is a fellow Thanchir who I hear would be happy to help. The only problem is that he lies on the other side of a huge encampment of orcs, so I will need an escort to help me. We will see how that goes. I have heard things about those adventurer escorts ...`
- 现译：`博学者温罗提在此。我受命撰写一部太阳堡垒官方史。这本笔记将记录我四处旅行、采访众人的过程。如果你正在读它，那你要么是我的资助人（再次感谢您，先生！），要么是个偷看者（滚出我的日记！），要么是发现我尸体的人。若是最后一种，请把它带给太阳堡垒城的弗洛萨斯领主领取酬谢，告诉我的妻子我是怎么死的，再告诉孩子们我爱他们。

闲话到此，我将从调查精灵及其与太阳堡垒的联系开始这项工作。考虑到精灵的寿命和他们热衷于铭记自身历史的性情，他们应该是较容易采访的种族之一。当然，如今这里的精灵已经不像过去那么多了。
……
然而不幸的是，当地精灵也不愿向我讲述他们的历史，说他们没有早期时代的记录。不过我听说，有位名叫桑切尔的人很乐意帮忙。唯一的问题是，他人在一座庞大兽人营地的另一边，所以我需要一名护卫协助。到时候再看吧。我可听说过有关那些冒险者护卫的传闻……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00214 | HUMAN-REVIEW | cross-batch-049 | confirmed | 项目若要求严格换行则删空行，否则可保留 |  |  |

<details><summary>hrq-00214 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“再告诉孩子们我爱他们。”后多一个空行（源码单换行）。Sol 建议按排版 advisory 处理，因该处正是话题转换、中文分段有可读性
```
```
raw verdict: “再告诉孩子们我爱他们。”后多出一个空行（双换行）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-048-01.md](reports/sol-048-01.md)。译文未修改。共 5 个 claim：4 confirmed、1 pending、无 refuted/advisory。 译文未修改。Sol 明确 `confirmed` 只代表 claim 事实成立、不代表严重度。
```
</details>

## entry-01382

- 位置：`mod-tome.lua:20175`（tome）｜section：`mod-tome/data/quests/charred-scar.lua`｜source_tag：`_t`
- 原文：`The volcano is attacked by orcs. A few Sun Paladins made it there with you. They will hold the line at the cost of their lives to buy you some time.`
- 现译：`火山受到了兽人的攻击，一些太阳骑士正顶在最前线用他们的生命来帮助你争取一些时间。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00215 | HUMAN-REVIEW | cross-batch-049 | confirmed | 补回该层意思，句式可调 |  |  |

<details><summary>hrq-00215 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `A few Sun Paladins made it there with you.`，丢失“太阳骑士与你一同抵达”的剧情关系
```
```
raw verdict: 漏译 `A few Sun Paladins made it there with you.`→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-048-01.md](reports/sol-048-01.md)。译文未修改。共 5 个 claim：4 confirmed、1 pending、无 refuted/advisory。 译文未修改。Sol 明确 `confirmed` 只代表 claim 事实成立、不代表严重度。
```
</details>

## entry-01384

- 位置：`mod-tome.lua:20177`（tome）｜section：`mod-tome/data/quests/charred-scar.lua`｜source_tag：`_t`
- 原文：`You arrived too late. The place has been drained of its power and the sorcerers have left.`
- 现译：`你来的太晚了，这里的能量已经被吸干，而那些法师已经离开了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00216 | HUMAN-REVIEW | cross-batch-049 | confirmed | 改“得”；称谓一致性需另取冻结译文再定 |  |  |

<details><summary>hrq-00216 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“你来的太晚了”应为“来得”；confirmed：`the sorcerers` 由执行链确认特指 Elandar 与 Argoniel。pending：同任务后文是否统一译“巫师们”（冻结输入未含 `mod-tome.lua:20180-20181` 目标译文）
```
```
raw verdict: “你来的太晚了”的“的”应为“得”→confirmed; `the sorcerers` 特指 Elandar 与 Argoniel→confirmed; 同任务后文统一译“巫师们”，当前“那些法师”构成译名不一致→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-048-01.md](reports/sol-048-01.md)。译文未修改。共 5 个 claim：4 confirmed、1 pending、无 refuted/advisory。 译文未修改。Sol 明确 `confirmed` 只代表 claim 事实成立、不代表严重度。
```
</details>

## entry-01385

- 位置：`mod-tome.lua:20178`（tome）｜section：`mod-tome/data/quests/charred-scar.lua`｜source_tag：`_t`
- 原文：`Use the portal to go back to the Far East. You *MUST* stop them, no matter the cost.`
- 现译：`使用传送门到达远东大陆，你必须阻止他们，不惜一切代价。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00217 | HUMAN-REVIEW | cross-batch-050 | confirmed | 改回“返回”、补强调 |  |  |

<details><summary>hrq-00217 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“到达”弱化 `go back to` 的返回方向；confirmed：遗漏 `*MUST*` 强调
```
```
raw verdict: “到达”弱化了 `go back to` 的返回方向→confirmed; 遗漏 `*MUST*` 的强调→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01386

- 位置：`mod-tome.lua:20179`（tome）｜section：`mod-tome/data/quests/charred-scar.lua`｜source_tag：`_t`
- 原文：`You arrived in time and interrupted the ritual. The sorcerers have departed.`
- 现译：`你终于及时赶来阻止了仪式，法师们被驱散了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00218 | HUMAN-REVIEW | cross-batch-050 | confirmed | 改“已离开/已离去” |  |  |

<details><summary>hrq-00218 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`departed` 错成“被驱散了”
```
```
raw verdict: `departed` 错成“被驱散了”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01389

- 位置：`mod-tome.lua:20192`（tome）｜section：`mod-tome/data/quests/deep-bellow.lua`｜source_tag：`_t`
- 原文：`Your escape from Reknor got your heart pounding and your desire for wealth and power increased tenfold.`
- 现译：`你从瑞库纳逃了出来，你觉得你的心脏狂跳不止，你对财富和力量的渴望增加了十倍～。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00219 | HUMAN-REVIEW | cross-batch-050 | confirmed | 删“～”，语域整体定 |  |  |

<details><summary>hrq-00219 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：原文无句尾波浪号，译文凭空加“～”。advisory：波浪号是否符合该任务语域
```
```
raw verdict: 原文没有句尾波浪号，译文凭空加入“～”→confirmed; 波浪号必然不符合该任务整体语域→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01391

- 位置：`mod-tome.lua:20194`（tome）｜section：`mod-tome/data/quests/deep-bellow.lua`｜source_tag：`_t`
- 原文：`It has been long sealed away but still, from time to time adventurers go there looking for wealth.`
- 现译：`那里已被尘封已久，但是还是不断有冒险者前去寻找财宝。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00220 | HUMAN-REVIEW | cross-batch-050 | confirmed | 改“时有”、修语病 |  |  |

<details><summary>hrq-00220 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“不断有”强化 `from time to time` 频率。advisory：“已被尘封已久”语病
```
```
raw verdict: “已被尘封已久”构成明确语病→advisory; “不断有”强化了 `from time to time` 的频率→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01392

- 位置：`mod-tome.lua:20195`（tome）｜section：`mod-tome/data/quests/deep-bellow.lua`｜source_tag：`_t`
- 原文：`None that you know of has come back yet, but you did survive Reknor. You are great.`
- 现译：`据你所知没有一个人能活着回来，不过你从瑞库纳幸存了下来，你比较牛 X。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00221 | HUMAN-REVIEW | cross-batch-050 | confirmed | 去“比较”、换俚语 |  |  |

<details><summary>hrq-00221 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：增加“比较”弱化肯定程度。advisory：“牛 X”属粗俗网络俚语
```
```
raw verdict: “牛 X”属不合语域的粗俗网络俚语→advisory; 增加“比较”弱化了肯定程度→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01400

- 位置：`mod-tome.lua:20216`（tome）｜section：`mod-tome/data/quests/east-portal.lua`｜source_tag：`_t`
- 原文：`Tannen has tricked you! He swapped the orb for a false one that brought you to a demonic plane. Find the exit, and get revenge!`
- 现译：`泰恩把你耍了！他换了个错的水晶球给你，把你传送到了恶魔的空间，找到出口回去找他算账！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00222 | HUMAN-REVIEW | cross-batch-050 | confirmed | 改“假冒的水晶球”类；位面术语待核 |  |  |

<details><summary>hrq-00222 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`false one` 误成“错的水晶球”，未表达蓄意造假/掉包。pending：`demonic plane` 是否必须统一“恶魔位面”
```
```
raw verdict: `false one` 误成“错的水晶球”，未表达蓄意造假与掉包→confirmed; `demonic plane` 必须统一为“恶魔位面”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01408

- 位置：`mod-tome.lua:20263`（tome）｜section：`mod-tome/data/quests/high-peak.lua`｜source_tag：`_t`
- 原文：`You have vanquished the masters of the Orc Pride. Now you must venture inside the most dangerous place of this world: the High Peak.`
- 现译：`你征服了兽人军团的最高领袖，现在你必须向这个世界最危险的地方挺进：巅峰。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00223 | HUMAN-REVIEW | cross-batch-050 | confirmed | 回“兽人部落/氏族”与“击败/覆灭” |  |  |

<details><summary>hrq-00223 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Orc Pride` 错用“兽人军团”；confirmed：`vanquished` 译“征服了”不符实际行动
```
```
raw verdict: `Orc Pride` 错用“兽人军团”→confirmed; `vanquished` 译“征服了”不符合实际行动→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01409

- 位置：`mod-tome.lua:20264`（tome）｜section：`mod-tome/data/quests/high-peak.lua`｜source_tag：`_t`
- 原文：`Seek the Sorcerers and stop them before they bend the world to their will.`
- 现译：`找到那些妄图扭曲这个世界的法师并阻止他们。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00224 | HUMAN-REVIEW | cross-batch-050 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00224 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`bend the world to their will` 译“扭曲这个世界”改变强调重点
```
```
raw verdict: `bend the world to their will` 译“扭曲这个世界”改变强调重点→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01410

- 位置：`mod-tome.lua:20265`（tome）｜section：`mod-tome/data/quests/high-peak.lua`｜source_tag：`_t`
- 原文：`To enter, you will need the four orbs of command to remove the shield over the peak.`
- 现译：`想要进去的话，你必须找到那四个指令水晶来移除塔顶的防护罩。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00225 | HUMAN-REVIEW | cross-batch-050 | confirmed | 改“峰顶”与“宝珠”类 |  |  |

<details><summary>hrq-00225 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`the peak` 错译“塔顶”；confirmed：`orbs of command` 译“指令水晶”遗漏 `orb` 实体
```
```
raw verdict: `the peak` 错译为“塔顶”→confirmed; `orbs of command` 译“指令水晶”遗漏 `orb` 实体信息→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01424

- 位置：`mod-tome.lua:20357`（tome）｜section：`mod-tome/data/quests/kryl-feijan-escape.lua`｜source_tag：`_t`
- 原文：`You failed to protect her when escorting her out of the crypt.`
- 现译：`你没能成功地将她护送出这个地宫。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00226 | HUMAN-REVIEW | cross-batch-050 | confirmed | 补谓语 |  |  |

<details><summary>hrq-00226 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏主要谓语 `protect her`
```
```
raw verdict: 译文遗漏主要谓语 `protect her`→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。 译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。
```
</details>

## entry-01432

- 位置：`mod-tome.lua:20426`（tome）｜section：`mod-tome/data/quests/love-melinda.lua`｜source_tag：`_t`
- 原文：`The Fortress Shadow has established a portal for her so she can come and go freely.`
- 现译：`堡垒之影为她建造了一个传送门，他让她能够自由来去。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00227 | HUMAN-REVIEW | cross-batch-051 | pending | 只按错字/语感处理，不按实质误译改写 |  |  |

<details><summary>hrq-00227 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：“目的从句被实质误译”不成立。advisory：“他让”生硬并引入未明确的性别代词。pending：“他让”是否是“好让”错字
```
```
raw verdict: 目的从句被实质误译→refuted; “他让”生硬并引入原文未明确的性别代词→advisory; “他让”是“好让”的错字→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01438

- 位置：`mod-tome.lua:20463`（tome）｜section：`mod-tome/data/quests/master-jeweler.lua`｜source_tag：`_t`
- 原文：`You found an ancient tome about gems.`
- 现译：`你发现一本关于珠宝的旧书。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00228 | HUMAN-REVIEW | cross-batch-051 | confirmed | 改“宝石”“古老典籍”；一致性核后定 |  |  |

<details><summary>hrq-00228 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`gems` 译“珠宝”不精确；confirmed：`ancient tome` 译“旧书”弱化年代与典籍感。pending：与第 20466 行“宝石的力量”是否统一
```
```
raw verdict: `gems` 译“珠宝”不够精确→confirmed; `ancient tome` 译“旧书”弱化年代与典籍感→confirmed; 与当前译文第 20466 行“宝石的力量”不统一→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01450

- 位置：`mod-tome.lua:20566`（tome）｜section：`mod-tome/data/quests/ring-of-blood.lua`｜source_tag：`_t`
- 原文：`Till the Blood Runs Clear`
- 现译：`直到鲜血流清`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00229 | HUMAN-REVIEW | cross-batch-051 | pending | 需上下文/设定依据再定 |  |  |

<details><summary>hrq-00229 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“直到鲜血流清”直译感。pending：英文是否必然理解为战至血流尽
```
```
raw verdict: “直到鲜血流清”有字面直译感→advisory; 英文必然应理解为战至血流尽／清洗至无血→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01462

- 位置：`mod-tome.lua:20631`（tome）｜section：`mod-tome/data/quests/staff-absorption.lua`｜source_tag：`_t`
- 原文：`On your way out of the Dreadfell you were ambushed by a band of orcs.`
- 现译：`当你走出恐惧王座的时候你受到了一队兽人小队的偷袭。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00230 | HUMAN-REVIEW | cross-batch-051 | confirmed | 去重复 |  |  |

<details><summary>hrq-00230 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“一队兽人小队”量词重复
```
```
raw verdict: “一队兽人小队”存在重复→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01463

- 位置：`mod-tome.lua:20634`（tome）｜section：`mod-tome/data/quests/staff-absorption.lua`｜source_tag：`_t`
- 原文：`They asked about the staff and stole it from you.`
- 现译：`他们从你那里得知了法杖的消息，把法杖抢走了。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00231 | HUMAN-REVIEW | cross-batch-051 | confirmed | 按“盘问/索取”重译，修复逻辑冲突 |  |  |

<details><summary>hrq-00231 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：`asked about` 误成“从你那里得知了消息”；兽人接触前已知法杖并直接索要；与“你什么也没告诉他们”冲突
```
```
raw verdict: `asked about` 被误译成“从你那里得知了消息”→confirmed; 兽人在接触玩家前已知法杖并直接索要→confirmed; 现译与“你什么也没告诉他们”冲突→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01464

- 位置：`mod-tome.lua:20637`（tome）｜section：`mod-tome/data/quests/staff-absorption.lua`｜source_tag：`_t`
- 原文：`In its remains, you found a strange staff. It radiates power and danger and you dare not use it yourself.`
- 现译：`在他的尸体上，你发现了一根奇怪的法杖，它辐射出的力量和危险使你不敢使用它。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00232 | HUMAN-REVIEW | cross-batch-051 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00232 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“辐射出的力量和危险”直译腔
```
```
raw verdict: “辐射出的力量和危险”带生硬直译感→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。 译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。
```
</details>

## entry-01468

- 位置：`mod-tome.lua:20691`（tome）｜section：`mod-tome/data/quests/start-dwarf.lua`｜source_tag：`_t`
- 原文：`Let nothing stop you.`
- 现译：`不惜一切代价冲出去。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00233 | HUMAN-REVIEW | cross-batch-052 | confirmed | 是否接受戏剧化意译；忠实版“别让任何东西阻挡你” |  |  |

<details><summary>hrq-00233 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Let nothing stop you.` 译“不惜一切代价冲出去”多出代价与突围两层含义
```
```
raw verdict: `Let nothing stop you.` 译“不惜一切代价冲出去”，增加“付出代价”与“向外突围”两层含义→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01474

- 位置：`mod-tome.lua:20754`（tome）｜section：`mod-tome/data/quests/start-undead.lua`｜source_tag：`_t`
- 原文：`However, the ritual failed in some way and you retain your own mind. You need to get out of this dark place and try to carve a place for yourself in the world.`
- 现译：`不过，复活仪式似乎出了点问题，你保留了自己的意识，你必须离开这个黑暗地方并找到属于自己的栖息地。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00234 | HUMAN-REVIEW | cross-batch-052 | confirmed | 改“在这个世界谋得一席之地”；可顺带断句 |  |  |

<details><summary>hrq-00234 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`carve a place for yourself` 译“找到属于自己的栖息地”，应为在世上谋得一席之地。advisory：原文两句被逗号连接
```
```
raw verdict: `carve a place for yourself` 被译成“找到属于自己的栖息地”（应为在世上谋得一席之地）→confirmed; 原文两句被逗号连接→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01479

- 位置：`mod-tome.lua:20781`（tome）｜section：`mod-tome/data/quests/starter-zones.lua`｜source_tag：`_t`
- 原文：`The Sandworm Lair is to the far west of Derth, near the sea.`
- 现译：`在德斯镇远一点的西面，靠近海岸的地方是沙虫巢穴。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00235 | HUMAN-REVIEW | cross-batch-052 | confirmed | 改“德斯镇遥远的西面” |  |  |

<details><summary>hrq-00235 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`far west` 被“远一点的西面”弱化
```
```
raw verdict: `far west` 被“远一点的西面”弱化→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01482

- 位置：`mod-tome.lua:20800`（tome）｜section：`mod-tome/data/quests/strange-new-world.lua`｜source_tag：`_t`
- 原文：`Upon arrival you met an Elf and an orc fighting.`
- 现译：`你碰到了一个精灵在和一个兽人战斗。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00236 | HUMAN-REVIEW | cross-batch-052 | advisory | 可选补“刚抵达时” |  |  |

<details><summary>hrq-00236 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：省略 `Upon arrival`；前句已交代抵达，无实质 completeness 问题
```
```
raw verdict: 译文省略 `Upon arrival`→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01486

- 位置：`mod-tome.lua:20813`（tome）｜section：`mod-tome/data/quests/temple-of-creation.lua`｜source_tag：`_t`
- 原文：`Slasul told you his side of the story. Now you must decide: which of them is corrupt?`
- 现译：`萨拉苏尔告诉了你关于他的故事，你现在必须决定：到底谁才是真正的堕落者？`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00237 | HUMAN-REVIEW | cross-batch-052 | confirmed | 改“他这一方的说法” |  |  |

<details><summary>hrq-00237 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`his side of the story` 误成“关于他的故事”，削弱双方各执一词结构
```
```
raw verdict: `his side of the story` 被误处理成“关于他的故事”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01491

- 位置：`mod-tome.lua:20857`（tome）｜section：`mod-tome/data/quests/tutorial.lua`｜source_tag：`_t`
- 原文：`You must venture in the heart of the forest and kill the Lone Wolf, who randomly attacks villagers.`
- 现译：`你必须进入森林的中心地带并杀死孤狼——那个肆意屠杀村民的凶手。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00238 | HUMAN-REVIEW | cross-batch-052 | confirmed | 收束为“会随机袭击村民”或保留戏剧化 |  |  |

<details><summary>hrq-00238 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`randomly attacks villagers` 强化成“肆意屠杀村民的凶手”
```
```
raw verdict: `randomly attacks villagers` 被强化成“肆意屠杀村民的凶手”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01496

- 位置：`mod-tome.lua:20882`（tome）｜section：`mod-tome/data/quests/west-portal.lua`｜source_tag：`logPlayer`
- 原文：`#VIOLET#Zemekkys says: 'The portal is done!'`
- 现译：`#VIOLET#泽梅基斯说道：“传送门已经开启！”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00239 | HUMAN-REVIEW | cross-batch-052 | refuted | 无必办；严格贴字才改“传送门完成了” |  |  |

<details><summary>hrq-00239 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：`The portal is done!` 译“传送门已经开启”**不成立**，源码显示 done 后即 functional 可用；Sol 另注 Gemini 行号 `:75` 应为 `:80`
```
```
raw verdict: `The portal is done!` 译“传送门已经开启”与场景不符→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01498

- 位置：`mod-tome.lua:20894`（tome）｜section：`mod-tome/data/quests/wild-wild-east.lua`｜source_tag：`_t`
- 原文：`There must be a way to go into the far east from the lair of Golbug. Find it and explore the unknown far east, looking for clues.`
- 现译：`在高尔布格巢穴内肯定有一条通往远东大陆的路，去寻找线索并找到它，然后探索那未知而遥远的东方。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00240 | HUMAN-REVIEW | cross-batch-052 | confirmed | 调整行动顺序句；统一地名 |  |  |

<details><summary>hrq-00240 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：寻找线索的动作关系被颠倒（应先找到传送门进入远东，再调查线索）；confirmed：同一 `far east` 被译成两个地理称呼。Sol 另注 Gemini 行号 `:24` 应为 `:26`
```
```
raw verdict: 寻找线索的动作关系被颠倒（应先找到传送门进入远东，再调查线索）→confirmed; 同一 `far east` 被译成两个不同地理称呼→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。
```
</details>

## entry-01508

- 位置：`mod-tome.lua:21014`（tome）｜section：`mod-tome/data/talents/celestial/chants.lua`｜source_tag：`tformat`
- 原文：`You have learned to sing the praises of the Sun, in the form of three defensive Chants.
			Chant of Fortitude: Increases your mental save by %d and maximum life by %d%%.
			Chant of Fortress: Increases your physical save by %d, your physical resistance by %d%%, your armour by %d and your armour hardiness by 15%%.
			Chant of Resistance: Increases you spell save by %d, your fire/cold/lightning/acid resistances by %d%% and reduces all damage that comes from distant enemies (3 spaces or more) by %d%%.
			You may only have one Chant active at a time.`
- 现译：`你学会了三种防御赞歌，以此咏唱对太阳的赞颂：
			坚韧赞歌：增加 %d 精神豁免，%d%% 最大生命值
			堡垒赞歌：增加 %d 物理豁免，%d%% 物理抗性，%d 护甲，15%% 护甲强度
			元素赞歌：增加 %d 法术豁免，%d%% 火焰 /寒冷 /闪电 /酸性抗性，减少三格外敌人对你造成的伤害 %d%%。
			你同时只能激活一种赞歌。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00241 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：8 个占位符正确。advisory：句号与斜杠空格不统一 |  |  |

<details><summary>hrq-00241 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 8 个占位符数量/类型/顺序正确→confirmed; 标点与斜杠空格不统一→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01509

- 位置：`mod-tome.lua:21029`（tome）｜section：`mod-tome/data/talents/celestial/chants.lua`｜source_tag：`tformat`
- 原文：`Your skill at Chanting now extends the cloak of light, increasing your light radius by %d.
		Also, when you start a new Chant, you will be cured of all cross-tier effects and cured of up to %d debuffs.
		Chant of Fortitude cures mental effects.
		Chant of Fortress cures physical effects.
		Chant of Resistance cures magical effects.`
- 现译：`咏唱赞歌的娴熟技艺让光明得以扩散，增加 %d 光照半径。
		每次你咏唱新的赞歌时，你将解除自身的越层效果（失去平衡、法术冲击和思维封锁），并额外解除 %d 项相应类型的负面状态。
		坚韧赞歌：解除精神负面状态
		堡垒赞歌：解除物理负面状态
		元素赞歌：解除魔法负面状态。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00242 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：两个 `%d` 正确；confirmed：机制为“先清当前赞歌类型全部 cross-tier 效果，再随机清最多 `%d` 个同类型普通负面状态”。refuted：Gemini 称括号补充“不影响实质机制理解”过于乐观 |  |  |

<details><summary>hrq-00242 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 两个 `%d` 占位符正确→confirmed; 只解除当前赞歌类型全部 cross-tier 效果并随机解除最多 `%d` 个同类型普通负面状态→confirmed; Gemini 称括号补充“不影响实质机制理解”过于乐观→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01510

- 位置：`mod-tome.lua:21053`（tome）｜section：`mod-tome/data/talents/celestial/circles.lua`｜source_tag：`tformat`
- 原文：`Creates a circle of radius %d at your feet; the circle protects you from silence effects while you remain in its radius while silencing and dealing %d light damage to everyone else who enters. The circle lasts %d turns.`
- 现译：`在你的脚下制造一个 %d 码半径范围的法阵，当你在法阵内，它会使你免疫沉默效果，并沉默进入此范围的其他所有生物，对其造成 %d 光系伤害。
		法阵持续 %d 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00243 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：三个 `%d` 顺序正确。advisory：末句另起一行 |  |  |

<details><summary>hrq-00243 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 半径/伤害/持续时间三个 `%d` 顺序正确→confirmed; 译文把最后一句另起一行→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01512

- 位置：`mod-tome.lua:21076`（tome）｜section：`mod-tome/data/talents/celestial/combat.lua`｜source_tag：`tformat`
- 原文：`Infuse your weapon with the power of the Sun, adding %0.1f light damage on each melee hit.
		Additionally, if you have a temporary damage shield active, melee hits will increase its power by %d once per turn.
		The damage dealt and shield bonus will increase with your Spellpower.`
- 现译：`使你的武器充满太阳能量，每次近战命中造成 %0.1f 光系伤害。
		如果你同时打开了临时伤害护盾，每回合一次，你的近战攻击命中可以增加护盾 %d 强度。
		伤害和护盾加成受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00244 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：`%0.1f`/`%d` 对齐；confirmed：版本差异属实——“强化护盾持续至少 2 回合”在冻结英文与译文都缺（源码 `shield.dur = math.max(2, shield.dur)`） |  |  |

<details><summary>hrq-00244 · HUMAN-REVIEW 详情</summary>

```
raw verdict: `%0.1f` 与 `%d` 对齐→confirmed; 版本差异存在：强化护盾持续时间至少 2 回合的语句在冻结英文与译文中都缺失→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01514

- 位置：`mod-tome.lua:21091`（tome）｜section：`mod-tome/data/talents/celestial/combat.lua`｜source_tag：`tformat`
- 原文：`Your weapon attacks burn with righteous fury, dealing %d%% of your lost HP as additional Fire damage (up to %d, Current:  %d).
		Targets struck are also afflicted with a Martyrdom effect that causes them to take %d%% of all damage they deal for 4 turns.
		The bonus damage can only occur once per turn.`
- 现译：`你使用武器攻击时，造成相当于 %d%% 你已损失的生命值的火焰伤害，至多 %d 点，当前 %d 点
		然后令目标进入殉难状态，受到 %d%% 自己造成的伤害，持续 4 回合。
		每回合最多触发一次额外伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00245 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：四占位符正确。advisory：首行缺句末标点、未保留英文括号 |  |  |

<details><summary>hrq-00245 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 四个占位符含义与顺序正确→confirmed; 首行“当前 %d 点”无句末标点、未保留英文括号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01516

- 位置：`mod-tome.lua:21110`（tome）｜section：`mod-tome/data/talents/celestial/crusader.lua`｜source_tag：`tformat`
- 原文：`You strike your foe with your two handed weapon, dealing %d%% weapon damage.
		If the attack hits, all foes in radius 2 will have their light resistance reduced by %d%% and their damage reduced by %d%% for 5 turns.`
- 现译：`你用双手武器攻击敌人，造成 %d%% 武器伤害。
		如果攻击命中，半径 2 以内的敌人光系抗性下降 %d%%，伤害下降 %d%% , 持续 5 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00246 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：三个 `%d%%` 对应正确。advisory：`%d%% , 持续` 逗号空格不规范 |  |  |

<details><summary>hrq-00246 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 三个 `%d%%` 对应武器伤害/光抗削减/伤害削减→confirmed; `%d%% , 持续` 中英文逗号空格不规范→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01517

- 位置：`mod-tome.lua:21116`（tome）｜section：`mod-tome/data/talents/celestial/crusader.lua`｜source_tag：`tformat`
- 原文：`While wielding a two handed weapon, your critical strike chance is increased by %d%%, and your melee criticals instill you with righteous strength, increasing all physical and light damage you deal by %d%%, stacking up to 3 times.
		In addition, your melee critical strikes leave a lasting lightburn on the target, dealing %0.2f light damage over 5 turns and reducing opponents armour by %d.
		The damage increases with your Spellpower.`
- 现译：`当装备双手武器时，你的暴击率增加 %d%% , 同时你的近战暴击会引发光明之力，增加 %d%% 物理和光系伤害加成，最多叠加 3 次。
		同时，你的近战暴击会在目标身上留下灼烧痕迹，5 回合内造成 %0.2f 光系伤害，同时减少 %d 护甲。
		伤害受法强加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00247 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：四占位符正确。advisory：逗号前多余空格；advisory：“灼烧痕迹”未体现独立 `EFF_LIGHTBURN` 状态（无权威中文名） |  |  |

<details><summary>hrq-00247 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 四个占位符正确→confirmed; 首行逗号前多余空格→advisory; “灼烧痕迹”未体现独立 `EFF_LIGHTBURN` 状态→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01518

- 位置：`mod-tome.lua:21122`（tome）｜section：`mod-tome/data/talents/celestial/crusader.lua`｜source_tag：`tformat`
- 原文：`Infuse your two handed weapon with light while spinning around.
		All creatures in radius one take %d%% weapon damage.
		In addition while spinning your weapon shines so much it deals %d%% light weapon damage to all foes in radius 2.
		At level 4 your spinning blade creates a shield that blocks all damage for 1 turn.`
- 现译：`旋转一周，同时将光明之力充满武器。
		半径 1 以内的敌人将受到 %d%% 武器伤害，同时半径 2 以内的敌人将受到 %d%% 光系武器伤害。
		技能等级 4 或以上时，在旋转时你会制造一层护盾，吸收 1 回合内的所有攻击。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00248 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：两个 `%d%%` 对应半径1/2 伤害；advisory：两行合一行无遗漏。refuted：Gemini 称 4 级护盾“对齐无误”不准确，实为 `cancel_damage_chance = 100` 免疫所有伤害 |  |  |

<details><summary>hrq-00248 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 两个 `%d%%` 与半径1/半径2 两次伤害对应正确→confirmed; 两行伤害说明合并为一行无内容遗漏→advisory; Gemini 称 4 级护盾机制“对齐无误”不准确（实为免疫所有伤害）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01528

- 位置：`mod-tome.lua:21308`（tome）｜section：`mod-tome/data/talents/celestial/glyphs.lua`｜source_tag：`tformat`
- 原文：`Destabilize your glyphs, triggering every glyph in radius 10 with an enemy standing on it.
		At talent level 2 glyphs triggered this way will leave a residue of themselves on the ground, dealing damage each turn for %d turns.
		#ffd700#Sunlight#LAST#:  %0.2f light damage.
		#7f7f7f#Moonlight#LAST#:  %0.2f darkness damage.
		#9D9DC9#Twilight#LAST#:  %0.2f light and %0.2f darkness damage`
- 现译：`激发所有圣印，10格内所有上方站着敌人的圣印将被触发。
		技能等级2时，该效果触发的圣印将在地面遗留能量，在 %d 回合内持续造成伤害。
		#ffd700#日光圣印#LAST#：%0.2f 光系伤害。
		#7f7f7f#月光圣印#LAST#：%0.2f 暗影伤害。
		#9D9DC9#暮光圣印#LAST#：%0.2f 光系和 %0.2f 暗影伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00249 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：五占位符与颜色标签正确。advisory：补句号与“圣印”后缀属可接受整理 |  |  |

<details><summary>hrq-00249 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 五个占位符与颜色标签正确→confirmed; 末行补句号、补“圣印”后缀属可接受整理→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01531

- 位置：`mod-tome.lua:21343`（tome）｜section：`mod-tome/data/talents/celestial/guardian.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Crusade without a shield!`
- 现译：`使用十字军打击必须使用盾牌！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00250 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：改写语义等价，正确源码 `guardian.lua:183-203`（Gemini 写成 `:149`）。pending：`Crusade` 是否已定名“十字军打击” |  |  |

<details><summary>hrq-00250 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 否定句改写为必要条件句语义等价；正确源码位置 guardian.lua:183-203 而非 Gemini 的 :149→confirmed; 同 section 已将 `Crusade` 定名“十字军打击”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01534

- 位置：`mod-tome.lua:21433`（tome）｜section：`mod-tome/data/talents/celestial/light.lua`｜source_tag：`tformat`
- 原文：`A magical zone of Sunlight appears around you, healing and shielding all within a radius of %d for %0.2f per turn and increasing healing effects on everyone within by %d%%. The effect lasts for %d turns.
		Existing damage shields will be added to instead of overwritten and have their duration set to 2 if it isn't higher.
		If the same shield is refreshed 20 times it will become unstable and explode, removing it.
		It also lights up the affected area.
		The amount healed will increase with the Magic stat`
- 现译：`阳光倾泻在你周围 %d 码范围内，每回合治疗所有单位 %0.2f 生命值，给予其等量的护盾，并增加此范围内所有人 %d%% 治疗效果。此效果持续 %d 回合。
		如果已经存在护盾，则护盾将会增加等量数值，如果护盾持续时间不足 2 回合，会延长至 2 回合。
		当同一个护盾被刷新 20 次后，将会因为不稳定而破碎。
		它同时会照亮此区域。
		治疗量受魔力值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00251 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：四占位符正确；confirmed：`HEALING_POWER` 治疗+护盾+至少2回合+20次移除。advisory：英文无句号中文补句号 |  |  |

<details><summary>hrq-00251 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 四个占位符与治疗/护盾/增幅/持续时间正确→confirmed; `HEALING_POWER` 同时治疗、创建或累加护盾、至少 2 回合、20 次移除→confirmed; 英文末行无句号而中文补句号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01536

- 位置：`mod-tome.lua:21483`（tome）｜section：`mod-tome/data/talents/celestial/radiance.lua`｜source_tag：`tformat`
- 原文：`You are so infused with sunlight that your body glows permanently in radius %d, even in dark places.
		Your vision and body adapt to this glow, giving you %d%% blindness resistance, %d%% light resistance, and %d%% light affinity.
		The light radius overrides your normal light if it is bigger (it does not stack).
		`
- 现译：`你的体内充满了阳光，即使身处黑暗之中，身体也会永久发出半径 %d 的光芒。
		你的眼睛和身体适应了光明，获得 %d%% 目盲免疫，%d%% 光系抗性和 %d%% 光系伤害亲和。
		光照超过你的灯具时取代之，不与灯具叠加光照。
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00252 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：四占位符正确；confirmed：`blindness resistance`→“免疫”符合 `blind_immune`。refuted：把 `normal light` 限定为“灯具”不准确（实为 `self.lite` vs `radiance_aura`）。pending：“光系伤害亲和/吸收”术语裁决 |  |  |

<details><summary>hrq-00252 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 四个占位符正确（radiance_aura/blind_immune/光抗/damage_affinity）→confirmed; `blindness resistance` 表达为“免疫”符合 `blind_immune`；“目盲/致盲”属用词裁决→confirmed; 把 `normal light` 限定为“灯具”不准确→refuted; “光系伤害亲和”是否应改“光系伤害吸收”→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01543

- 位置：`mod-tome.lua:21610`（tome）｜section：`mod-tome/data/talents/celestial/twilight.lua`｜source_tag：`logPlayer`
- 原文：`Not enough space to summon!`
- 现译：`没有足够的空间召唤！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00253 | HUMAN-REVIEW | cross-batch-053 | confirmed | confirmed：源码为感叹号版本且位置 `twilight.lua:215-219`；confirmed：与术语快照句号规则不一致。advisory：仅标点差异 |  |  |

<details><summary>hrq-00253 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 源码确为 logPlayer 的感叹号版本（twilight.lua:215-219）→confirmed; 译文感叹号忠实但与术语快照句号规则不一致→confirmed; 差异只在标点不影响机制→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01554

- 位置：`mod-tome.lua:21815`（tome）｜section：`mod-tome/data/talents/chronomancy/bow-threading.lua`｜source_tag：`tformat`
- 原文：`Fire an arrow for %d%% weapon damage and call up to 2 wardens, depending on available space, that will each fire a single arrow before returning to their timelines.
		The wardens are out of phase with normal reality and deal %d%% less damage but shoot through friendly targets. All your arrows, including arrows from Shoot and other talents, now phase through friendly targets without causing them harm.
		
		Bow Threading talents will freely swap to your bow when activated if you have one in your secondary slot. You may use the Shoot talent in a similar manner.`
- 现译：`发射一支灵矢造成 %d%% 武器伤害，并且根据可用空间，召唤最多两个守卫，各自发射一枚灵矢然后回到他们自己的时间线中。
		守卫处在现实位面之外，灵矢的伤害减少 %d%%，但能够穿过友好目标。同时，你发射的所有来自射击或者其他技能的箭矢，都可以穿透友军并且不会造成伤害。

		激活螺旋灵弓技能可以自由切换到你的弓（必须装备在副武器栏位上）。此外，当你使用远程攻击时也会触发这个效果。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00254 | HUMAN-REVIEW | cross-batch-054 | confirmed | 是否恢复天赋名 |  |  |
| hrq-00255 | HUMAN-REVIEW | cross-batch-053 entry-01554… | confirmed | confirmed：采用第二座跃迁门实际子技能有源码依据；confirmed：`%d` 对应该子技能有效距离 |  |  |

<details><summary>hrq-00254 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：占位符及顺序正确；confirmed：末句把特定 `Shoot` 天赋泛化为“远程攻击”。advisory：“守卫伤害降低”译“灵矢伤害降低”但当前行为等价
```
```
raw verdict: 占位符及顺序正确→confirmed; 末句把特定的 `Shoot` 天赋泛化成“远程攻击”→confirmed; “守卫伤害降低”译“灵矢伤害降低”，当前行为等价→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。
```
</details>

<details><summary>hrq-00255 · HUMAN-REVIEW 详情</summary>

```
raw verdict: 占位符及顺序正确→confirmed; 末句把特定的 `Shoot` 天赋泛化成“远程攻击”→confirmed; “守卫伤害降低”译“灵矢伤害降低”，当前行为等价→advisory; 主动采用第二座跃迁门实际子技能有源码依据→confirmed; 单个 `%d` 对应该子技能有效距离→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。 译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。
```
</details>

## entry-01557

- 位置：`mod-tome.lua:21879`（tome）｜section：`mod-tome/data/talents/chronomancy/chronomancer.lua`｜source_tag：`_t`
- 原文：`Weave the threads of fate.`
- 现译：`编织你的命运。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00256 | HUMAN-REVIEW | cross-batch-054 | confirmed | 补 threads 意象；例证需另取冻结文本 |  |  |

<details><summary>hrq-00256 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：增译“你的”并漏 `threads` 意象。pending：Gemini 所举 Spin Fate 叠加“命运之丝”例证
```
```
raw verdict: 增译“你的”并漏掉 `threads` 意象→confirmed; Gemini 所举 Spin Fate 叠加“命运之丝”例证→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。
```
</details>

## entry-01563

- 位置：`mod-tome.lua:21913`（tome）｜section：`mod-tome/data/talents/chronomancy/chronomancy.lua`｜source_tag：`tformat`
- 原文：`Choose an activatable spell that affects only you, does not require a target, and does not have a fixed cooldown.  When you take damage that reduces your life below %d%% the spell will automatically cast.
		This spell will cast even if it is currently on cooldown, will not consume a turn or resources, and uses the talent level of Contingency or its own, whichever is lower.
		This effect can only occur once every %d turns and takes place after the damage is resolved.

		Current Contingency Spell: %s`
- 现译：`选择一个只会影响你并且不需要选中目标的非固定冷却时间主动法术。当你受到伤害并使生命值降低到 %d%% 以下时，自动释放这个技能。
		即使选择的技能处于冷却状态也可以释放  ，并且不消耗回合或资源，技能等级取意外术与所选法术两者中较低的一方。
		这个效果每 %d 回合只能触发一次，并且在伤害结算之后生效。

		当前选择技能：%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00257 | HUMAN-REVIEW | cross-batch-054 | confirmed | 删空格 |  |  |

<details><summary>hrq-00257 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：三占位符正确；confirmed：“释放  ，”含两个多余半角空格
```
```
raw verdict: 三个占位符及顺序正确→confirmed; “释放  ，”含两个多余半角空格→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。
```
</details>

## entry-01565

- 位置：`mod-tome.lua:21925`（tome）｜section：`mod-tome/data/talents/chronomancy/chronomancy.lua`｜source_tag：`tformat`
- 原文：`You peer into three possible futures, allowing you to explore each for %d turns.  When the effect expires, you'll choose which of the three futures becomes your present.
		If you know Foresight you'll gain additional defense and chance to shrug off critical hits (equal to your Foresight values) while See the Threads is active.
		This spell splits the timeline.  Attempting to use another spell that also splits the timeline while this effect is active will be unsuccessful.
		If you die in any thread you'll revert the timeline to the point when you first cast the spell and the effect will end.
		This spell may only be used once per zone level.`
- 现译：`你窥视三种可能的未来，允许你分别进行探索 %d 回合。当效果结束，你选择三者之一成为你的现在。
		如果你学会了深谋远虑，当你使用命运螺旋时，将获得额外的闪避和无视暴击伤害几率（数值等于深谋远虑的奖励）。
		这个法术会使时间线分裂。当此技能激活的时候，使用其他分裂时间线的技能将会失败。
		如果你在任何一条时间线上死亡，你将使时间线回到你使用技能的地方，并且技能效果结束。
		这个技能每个楼层只能使用一次。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00258 | HUMAN-REVIEW | cross-batch-054 | confirmed | 改“时点/时刻”类 |  |  |

<details><summary>hrq-00258 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：时间回溯点被译成空间“地方”
```
```
raw verdict: 把时间回溯点译成空间“地方”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。
```
</details>

## entry-01576

- 位置：`mod-tome.lua:22025`（tome）｜section：`mod-tome/data/talents/chronomancy/gravity.lua`｜source_tag：`tformat`
- 原文：`Sends out a blast wave of gravity in a radius %d cone, dealing %0.2f base physical (gravity) damage and knocking back targets caught in the area.
		Targets knocked into walls or other targets take 25%% additional damage and deal 25%% damage to targets they're knocked into.
		Closer targets will be knocked back further and the damage will scale with your Spellpower.`
- 现译：`在半径 %d 码的锥形范围内释放一股爆炸性的重力冲击波，造成 %0.2f 物理（重力）伤害并击退范围内目标。
		被击飞至墙上或其他单位的目标受到额外 25%% 伤害，并对被击中的单位造成 25%% 伤害。
		离你越近的目标将会被击飞得更远。受法术强度影响，伤害按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00259 | HUMAN-REVIEW | cross-batch-054 | confirmed | 是否补单位属风格 |  |  |

<details><summary>hrq-00259 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：数值占位符正确。advisory：原文无“码”，译文额外指定单位
```
```
raw verdict: 数值占位符均正确→confirmed; 原文没有“码”，译文额外指定该单位→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。
```
</details>

## entry-01586

- 位置：`mod-tome.lua:22102`（tome）｜section：`mod-tome/data/talents/chronomancy/induced-phenomena.lua`｜source_tag：`talent name`
- 原文：`Epoch`
- 现译：`纪元`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00260 | HUMAN-REVIEW | cross-batch-055 | confirmed | 术语核对后再定音译 |  |  |

<details><summary>hrq-00260 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：现译与固定简中译名不一致（Epoch→纪元）。pending：是否必然指同名专名实体、必须音译“亚伯契”
```
```
raw verdict: 现译与固定简中译名不一致（Epoch→纪元）→confirmed; 该天赋必然指同名专名实体，必须音译为亚伯契→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-054-01.md](reports/sol-054-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 pending、1 refuted。
```
</details>

## entry-01588

- 位置：`mod-tome.lua:22122`（tome）｜section：`mod-tome/data/talents/chronomancy/matter.lua`｜source_tag：`tformat`
- 原文：`Weave matter into your flesh, becoming incredibly resilient to damage.  While active you gain %d armour, %d%% resistance to stunning, and %d%% resistance to cuts.
		The bonus to armour will scale with your Magic.`
- 现译：`你的血肉被改变，对伤害的抗性提高。激活时增加 %d 护甲，%d%% 震慑免疫，%d%% 流血免疫。
		护甲加成受魔力值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00261 | HUMAN-REVIEW | cross-batch-055 | confirmed | 补呼应；`Magic` 译法待术语 |  |  |

<details><summary>hrq-00261 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：省略 weave matter 动作及与技能名的呼应；confirmed：护甲/震慑免疫/流血免疫与机制吻合。advisory：`Magic` 译“魔力值”
```
```
raw verdict: 省略 weave matter 的具体动作及与技能名的呼应→confirmed; `Magic` 译作“魔力值”有问题→advisory; 护甲、震慑免疫、流血免疫与机制吻合→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-054-01.md](reports/sol-054-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 pending、1 refuted。
```
</details>

## entry-01605

- 位置：`mod-tome.lua:22286`（tome）｜section：`mod-tome/data/talents/chronomancy/spacetime-folding.lua`｜source_tag：`tformat`
- 原文：`Lay Warp Mines in a radius of 1 that teleport enemies away from you and inflict %0.2f physical and %0.2f temporal (warp) damage.
		The mines are hidden traps (%d detection and %d disarm power based on your Magic) and last for %d turns.
		The damage caused by your Warp Mines will improve with your Spellpower.`
- 现译：`在半径 1 的范围里埋设地雷，将敌人传送远离你身边并造成 %0.2f 物理和 %0.2f 时空伤害。
		地雷是隐藏的陷阱（%d 侦查强度 %d 解除强度基于魔法），持续 %d 回合。
		伤害受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00262 | HUMAN-REVIEW | cross-batch-055 | confirmed | 补 warp；不按漏译改主语 |  |  |

<details><summary>hrq-00262 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `(warp)`／“（扭曲）”。refuted：末句省略“时空地雷的”主语构成漏译不成立
```
```
raw verdict: 漏译 `(warp)`／“（扭曲）”→confirmed; 末句省略“时空地雷的”主语构成漏译→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-054-01.md](reports/sol-054-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 pending、1 refuted。
```
</details>

## entry-01617

- 位置：`mod-tome.lua:22388`（tome）｜section：`mod-tome/data/talents/chronomancy/spellbinding.lua`｜source_tag：`tformat`
- 原文：`Extends the duration of the selected chronomancy spell by %d%%.
		Each spell can only be spellbound in one way at a time.
		
		Current Extended Spell: %s`
- 现译：`将选定时空法术的持续时间延长 %d%%。
		每个法术同时只能通过一种方式获得时空增效。
		
		当前延展法术：%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00263 | HUMAN-REVIEW | cross-batch-055 | confirmed | 是否统一系内译法 |  |  |

<details><summary>hrq-00263 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：占位符正确。advisory：与同系三条 spellbound 译法不一致（事实已证实）
```
```
raw verdict: 占位符正确→confirmed; 与同系三条的 spellbound 译法不一致（不一致事实已证实）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-054-01.md](reports/sol-054-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 pending、1 refuted。
```
</details>

## entry-01625

- 位置：`mod-tome.lua:22512`（tome）｜section：`mod-tome/data/talents/chronomancy/temporal-hounds.lua`｜source_tag：`tformat`
- 原文：`Upon activation summon a Temporal Hound.  Every %d turns another hound will be summoned, up to a maximum of three hounds. If a hound dies you'll summon a new hound in %d turns.  
		Your hounds inherit your increased damage percent, have %d%% physical resistance and %d%% temporal resistance, and are immune to teleportation effects.
		Hounds will get, %d Strength, %d Dexterity, %d Constitution, %d Magic, %d Willpower, and %d Cunning, based on your Magic stat.`
- 现译：`召唤一条时空猎犬。
		每隔 %d 回合召唤另一条时空猎犬，直至最多 3 条。
		当一条猎犬死去时，你将在 %d 回合内召唤一条新的猎犬。
		你猎犬继承你的伤害加成，有 %d%% 物理和 %d%% 时空抗性，对传送效果免疫。
		猎犬将拥有 %d 力量，%d 敏捷，%d 体质，%d 魔法，%d 意志和 %d 灵巧，基于你的魔法。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00264 | HUMAN-REVIEW | cross-batch-056 | confirmed | 补“的”与激活条件；回合措辞不改 |  |  |

<details><summary>hrq-00264 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“你猎犬”缺“的”；confirmed：遗漏 `Upon activation`；confirmed：占位符与百分号格式正确。refuted：“将在 %d 回合内召唤”应改“%d 回合后”不成立
```
```
raw verdict: “你猎犬”缺少“的”→confirmed; 遗漏 “Upon activation”→confirmed; “将在 %d 回合内召唤”应改成“%d 回合后”→refuted; 占位符与百分号格式正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-055-01.md](reports/sol-055-01.md)。译文未修改。共 8 个 claim：7 confirmed、1 refuted、0 advisory/pending。
```
</details>

## entry-01659

- 位置：`mod-tome.lua:22839`（tome）｜section：`mod-tome/data/talents/corruptions/plague.lua`｜source_tag：`tformat`
- 原文：`All your foes within a radius %d ball infected with a disease enter a cataleptic state, stunning them for %d turns and dealing %d%% of all remaining disease damage instantly.`
- 现译：`所有 %d 码球形范围内感染疾病的敌人进入僵硬状态，震慑它们 %d 回合并立即爆发 %d%% 剩余所有疾病伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00265 | HUMAN-REVIEW | cross-batch-056 | confirmed | 改为“半径 %d 码”类表述 |  |  |

<details><summary>hrq-00265 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“%d 码球形范围”误用单位并遗漏半径概念；confirmed：占位符数量和顺序正确
```
```
raw verdict: “%d 码球形范围”误用单位并遗漏半径概念→confirmed; 占位符数量和顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-055-01.md](reports/sol-055-01.md)。译文未修改。共 8 个 claim：7 confirmed、1 refuted、0 advisory/pending。
```
</details>

## entry-01661

- 位置：`mod-tome.lua:22895`（tome）｜section：`mod-tome/data/talents/corruptions/rot.lua`｜source_tag：`tformat`
- 原文：`Your body has become a mass of living corruption, increasing your blight and acid resistance by %d%% and blight affinity by %d%%.
On taking damage greater than 15%% of your maximum health, the damage will be reduced by %d%% and a carrion worm mass will burst forth onto a nearby tile, attacking your foes for 5 turns.
You can never have more than 5 worms active from any source at a time.
When a carrion worm dies it will explode into a radius 2 pool of blight for 5 turns, dealing %0.2f blight damage each turn and healing you for 33%% of that amount.`
- 现译：`你的身体已经腐败，增加 %d%% 枯萎和酸性抗性，%d%% 枯萎伤害亲和。
		每当你受到大于最大生命值 15%% 的伤害时，该伤害将减少 %d%%，同时在相邻的格子生成一团腐尸蠕虫，攻击你的敌人 5 回合。
		无论来源为何，你同时最多只能拥有 5 只蠕虫。
		蠕虫死亡时将爆炸，产生半径 2 的枯萎毒池，持续 5 回合，每回合造成 %0.2f 枯萎伤害，并按该伤害的 33%% 治疗你。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00266 | HUMAN-REVIEW | cross-batch-056 | confirmed | 按术语统一；死参数说明记录即可 |  |  |

<details><summary>hrq-00266 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`carrion worm mass` 未统一“腐肉虫群”；confirmed：占位符正确、第五参数未被文本消费
```
```
raw verdict: `carrion worm mass` 未统一为“腐肉虫群”→confirmed; 占位符正确，第五个参数未被文本消费→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-055-01.md](reports/sol-055-01.md)。译文未修改。共 8 个 claim：7 confirmed、1 refuted、0 advisory/pending。
```
</details>

## entry-01689

- 位置：`mod-tome.lua:23218`（tome）｜section：`mod-tome/data/talents/cunning/artifice.lua`｜source_tag：`tformat`
- 原文：`Throw a vial of volatile liquid that explodes in a radius %d cloud of smoke lasting %d turns.  The smoke blocks line of sight, and enemies within will have their vision range reduced by %d.
		Use of this talent will not break stealth, and creatures affected by the smokes can never prevent you from activating stealth, even if their proximity would normally forbid it.
		#YELLOW#Prepared with: %s#LAST#`
- 现译：`扔出烟雾弹，产生半径 %d 的烟雾，持续 %d 回合。烟雾阻挡视野，所有烟雾中的敌人视野下降 %d。
		使用该技能不解除潜行。被烟雾影响的生物不能阻止你潜行。
		#YELLOW#准备于：%s#LAST#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00267 | HUMAN-REVIEW | cross-batch-057 | advisory | 无必办项 |  |  |

<details><summary>hrq-00267 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：条目结论仅属排版/风格
```
```
raw verdict: 条目结论仅属排版/风格（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-056-01.md](reports/sol-056-01.md)。译文未修改。共 5 个 claim：2 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。refuted 是对 Gemini 表述强度的下修，原样转录。
```
</details>

## entry-01700

- 位置：`mod-tome.lua:23246`（tome）｜section：`mod-tome/data/talents/cunning/artifice.lua`｜source_tag：`logSeen`
- 原文：`%s uses a grappling hook to pull %s %s!`
- 现译：`%s使用钩爪来拉动%s向%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00268 | HUMAN-REVIEW | cross-batch-057 | advisory | 无必办项 |  |  |

<details><summary>hrq-00268 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：条目结论仅属排版/风格
```
```
raw verdict: 条目结论仅属排版/风格（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-056-01.md](reports/sol-056-01.md)。译文未修改。共 5 个 claim：2 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。refuted 是对 Gemini 表述强度的下修，原样转录。
```
</details>

## entry-01703

- 位置：`mod-tome.lua:23255`（tome）｜section：`mod-tome/data/talents/cunning/artifice.lua`｜source_tag：`tformat`
- 原文：`Your grappling hook deals %d%% unarmed damage when it hits, plus a further %0.2f physical and %0.2f nature damage over 4 turns.`
- 现译：`被钩爪击中的生物受到 %d%% 徒手伤害，在 4 回合内受到 %0.2f 流血伤害和 %0.2f 自然毒素伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00269 | HUMAN-REVIEW | cross-batch-057 | confirmed | 按伤害类型表回改措辞 |  |  |

<details><summary>hrq-00269 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：钩爪追加的是流血与中毒效果；confirmed：把 `physical` 写成“流血伤害”遗漏实际伤害类型。refuted：`nature` 被写成“自然毒素伤害”**并非“完全丢失”自然伤害类型**（Sol 注措辞仍属 advisory）
```
```
raw verdict: 钩爪追加的是流血效果和中毒效果→confirmed; 把 physical 写成“流血伤害”遗漏实际伤害类型→confirmed; 把 nature 写成“自然毒素伤害”完全丢失自然伤害类型→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-056-01.md](reports/sol-056-01.md)。译文未修改。共 5 个 claim：2 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。refuted 是对 Gemini 表述强度的下修，原样转录。
```
</details>

## entry-01706

- 位置：`mod-tome.lua:23297`（tome）｜section：`mod-tome/data/talents/cunning/called-shots.lua`｜source_tag：`tformat`
- 原文：`Your mastery of called shots is unparalleled. and you gain %d%% bonus critical chance and %d%% critical damage with your Called Shots Talents. At rank 3 the cooldowns of all of your Called Shots Talents are reduced by 2 each. At rank 5 you gain %d%% Physical resistance penetration with all Called Shot attacks.`
- 现译：`你对射击的掌握程度无与伦比。你的精准射击系技能获得 %d%% 额外暴击几率和 %d%% 额外暴击伤害。
		在第 3 级时，所有精准射击系技能冷却时间降低两回合。
		在第 5 级时，你的精准射击技能获得 %d%% 物理抗性穿透。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00270 | HUMAN-REVIEW | cross-batch-058 entry-01706… | confirmed | 按 Gemini 原报告逐条修；完整措辞见报告 |  |  |

<details><summary>hrq-00270 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：各 1 条 confirmed（条目结论成立）
```
```
raw verdict: 条目结论成立（confirmed）→confirmed; 条目结论成立（confirmed）→confirmed; 条目结论成立（confirmed）→confirmed; 条目结论成立（confirmed）→confirmed; 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-057-01.md](reports/sol-057-01.md)。译文未修改。共 13 个 claim：10 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-01732

- 位置：`mod-tome.lua:23449`（tome）｜section：`mod-tome/data/talents/cunning/poisons.lua`｜source_tag：`tformat`
- 原文：`Enhance your Deadly Poison with a stoning agent.  Whenever you apply Deadly Poison, you afflict your target with an additional earth-based poison that inflicts %d nature damage per turn (stacking up to %d damage per turn) for %d turns.
		After either %d turns or the poison has run its course (<100%% chance, see effect description), the target will be turned to stone for %d turns.
		The damage scales with your Cunning.`
- 现译：`在你的武器上涂上石化毒素，额外造成每轮 %d 点自然伤害（可叠加至 %d），持续 %d 回合。
		%d 回合后或者毒素效果结束后（几率小于100%%，请参见效果介绍），目标将被石化 %d 回合。
		受灵巧影响，伤害按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00271 | HUMAN-REVIEW | cross-batch-058 | confirmed | 按源码补效果与单位；统一用词 |  |  |

<details><summary>hrq-00271 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：漏掉致命毒素增强及触发关系；漏掉 `earth-based poison`；第二个 `%d` 缺每回合伤害单位。advisory：每轮／回合混用
```
```
raw verdict: 漏掉致命毒素增强及触发关系→confirmed; 漏掉 earth-based poison→confirmed; 第二个 `%d` 缺少每回合伤害单位→confirmed; 每轮／回合混用→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-057-01.md](reports/sol-057-01.md)。译文未修改。共 13 个 claim：10 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-01740

- 位置：`mod-tome.lua:23519`（tome）｜section：`mod-tome/data/talents/cunning/stealth.lua`｜source_tag：`tformat`
- 原文：`Enters stealth mode (power %d, based on Cunning), making you harder to detect.
		If successful (re-checked each turn), enemies will not know exactly where you are, or may not notice you at all.
		Stealth reduces your light radius to 0, increases your infravision by 3, and will not work with heavy or massive armours.
		You cannot enter stealth if there are foes in sight within range %d%s.
		Any non-instant, non-movement action will break stealth if not otherwise specified.

		Enemies uncertain of your location will still make educated guesses at it.
		While stealthed, enemies cannot share information about your location with each other and will be delayed in telling their allies that you exist at all.`
- 现译：`进入潜行模式（潜行点数 %d，基于灵巧），让你更难被侦测到。
		如果成功（每回合都重新检查），敌人将不会知道你在哪里，或者根本不会注意到你。
		潜行将光照半径减小至 0，增加3点夜视能力，并且不能在装备重甲或板甲时使用。
		如果敌人在半径 %d %s 内，你不能进入潜行。
		除非特别说明，任何非瞬间非移动技能均会打破潜行。

		即使不知道你位置的敌人，仍然会猜测你可能在的位置。
		潜行时，敌人无法彼此分享有关你所在位置的信息，并且会延迟向盟友通报你的存在。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00272 | HUMAN-REVIEW | cross-batch-058 | confirmed | 修空格；放宽措辞 |  |  |

<details><summary>hrq-00272 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`%d` 与 `%s` 拼接产生双空格；confirmed：action 被缩窄为技能
```
```
raw verdict: `%d` 与 `%s` 拼接产生双空格→confirmed; action 被缩窄为技能→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-057-01.md](reports/sol-057-01.md)。译文未修改。共 13 个 claim：10 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-01742

- 位置：`mod-tome.lua:23557`（tome）｜section：`mod-tome/data/talents/cunning/survival.lua`｜source_tag：`tformat`
- 原文：`You notice the small things others do not notice, allowing you to "see" creatures in a %d radius even outside of light radius.
		This is not telepathy, however, and it is still limited to line of sight.
		Also, your attention to detail increases stealth detection and invisibility detection by %d, and you gain the ability to detect traps (+%d detect 'power').
		The detection abilities improve with Cunning.`
- 现译：`你注意到他人注意不到的细节，甚至能在阴影区域“看到”怪物，%d 码半径范围。
		注意此能力不属于心灵感应，仍然受到视野的限制。
		同时你的细致观察使你侦察潜行和隐身的能力增加 %d，使你发现周围的陷阱的能力增加 %d。
		上述侦测能力均受灵巧加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00273 | HUMAN-REVIEW | cross-batch-058 | advisory | 不按漏机制改；power 字样可选 |  |  |

<details><summary>hrq-00273 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：refuted：“漏掉 `+` 导致数值机制缺失”不成立。advisory：省略 power 字样
```
```
raw verdict: 漏掉 `+` 导致数值机制缺失→refuted; 省略 power 字样→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-057-01.md](reports/sol-057-01.md)。译文未修改。共 13 个 claim：10 confirmed、2 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-01751

- 位置：`mod-tome.lua:23647`（tome）｜section：`mod-tome/data/talents/cunning/traps.lua`｜source_tag：`tformat`
- 原文：`%sTier %d: %s#LAST#
%s`
- 现译：`%s材质等级 %d：%s#LAST#
%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00274 | HUMAN-REVIEW | cross-batch-059 | confirmed | 统一“阶级 %d”（同批 entry-01747 用“最高阶级”）或“等级” |  |  |

<details><summary>hrq-00274 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Tier %d` 是陷阱精通技能门槛而非材质等级；confirmed：现译属跨语境误用“材质等级”
```
```
raw verdict: `Tier %d` 表示陷阱精通要求，而非装备材质等级→confirmed; 当前译文属跨语境误用“材质等级”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-058-01.md](reports/sol-058-01.md)。译文未修改。共 9 个 claim：7 confirmed、1 advisory、1 pending、0 refuted。 译文未修改。Sol 明确串文根因不影响对译文错误本身的确认。
```
</details>

## entry-01767

- 位置：`mod-tome.lua:23757`（tome）｜section：`mod-tome/data/talents/cunning/traps.lua`｜source_tag：`tformat`
- 原文：`Lay a trap that explodes into a radius 2 cloud of freezing vapour when triggered.  Foes take %0.2f cold damage and are pinned for 3 turns.
		The freezing vapour persists for 5 turns, dealing %0.2f cold damage each turn to foes with a 25%% chance to freeze.
		This trap can use a primed trigger and a high level lure can trigger it.%s`
- 现译：`放置一个陷阱，激活后产生半径 2 的冰冻气体，造成 %0.2f 寒冷伤害并定身 3 回合。
		冰冻气体持续 5 回合，每回合造成 %0.2f 伤害，有 25%% 几率冻结。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00275 | HUMAN-REVIEW | cross-batch-059 | confirmed | 若求逐项完整，补“每回合造成 %0.2f 寒冷伤害” |  |  |

<details><summary>hrq-00275 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二段遗漏第二次伤害的“寒冷”属性；confirmed：占位符无损坏。advisory：有“冰冻气体”语境，影响较低
```
```
raw verdict: 第二段遗漏第二次伤害的“寒冷”属性→confirmed; 占位符没有损坏→confirmed; “不影响理解”（冰冻气体提供较强语境）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-058-01.md](reports/sol-058-01.md)。译文未修改。共 9 个 claim：7 confirmed、1 advisory、1 pending、0 refuted。 译文未修改。Sol 明确串文根因不影响对译文错误本身的确认。
```
</details>

## entry-01785

- 位置：`mod-tome.lua:24033`（tome）｜section：`mod-tome/data/talents/cursed/cursed.lua`｜source_tag：`_t`
- 原文：`Each day, you lift your weary body and begin the unending hunt.`
- 现译：`你不知疲倦无时无刻狩猎你的下一个目标。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00276 | HUMAN-REVIEW | cross-batch-059 | confirmed | 三处按源码回改；根因保留为推测即可 |  |  |

<details><summary>hrq-00276 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`weary body` 反译成“不知疲倦”；confirmed：`Each day` 被改成“无时无刻”；confirmed：`begin the unending hunt` 被改写成“狩猎你的下一个目标”。pending：是否受相邻 `next victim` 串文影响（根因推测）
```
```
raw verdict: `weary body` 被反译成“不知疲倦”→confirmed; `Each day` 被改成“无时无刻”→confirmed; `begin the unending hunt` 被改写成“狩猎你的下一个目标”→confirmed; 该改写可能受相邻 `next victim` 串文影响→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-058-01.md](reports/sol-058-01.md)。译文未修改。共 9 个 claim：7 confirmed、1 advisory、1 pending、0 refuted。 译文未修改。Sol 明确串文根因不影响对译文错误本身的确认。
```
</details>

## entry-01788

- 位置：`mod-tome.lua:24039`（tome）｜section：`mod-tome/data/talents/cursed/cursed.lua`｜source_tag：`_t`
- 原文：`Let loose the hate that has grown within.`
- 现译：`释放你内心激增的愤怒。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00277 | HUMAN-REVIEW | cross-batch-060 | confirmed | 查术语记录后定“仇恨”；措辞如“释放你内心积聚的仇恨” |  |  |

<details><summary>hrq-00277 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`hate` 是正式资源概念，译“愤怒”弱化体系关联；confirmed：`has grown within` 是“滋生/积聚”非“激增”。pending：术语是否强制不用“愤怒”
```
```
raw verdict: `hate` 是正式资源概念，译“愤怒”弱化与核心“仇恨”体系关联→confirmed; 术语规范明确要求统一不用“愤怒”→pending; `has grown within` 是“在内心滋生／积聚”，不是“激增”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01798

- 位置：`mod-tome.lua:24093`（tome）｜section：`mod-tome/data/talents/cursed/dark-sustenance.lua`｜source_tag：`logPlayer`
- 原文：`You can only gain sustenance from your foes!`
- 现译：`你只能从敌人身上吸取！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00278 | HUMAN-REVIEW | cross-batch-060 | confirmed | 若补，与 Feed 系列既有译名协调 |  |  |

<details><summary>hrq-00278 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：省略 `sustenance` 宾语；confirmed：不会造成机制误解。advisory：是否补“养分/力量/精华”
```
```
raw verdict: 译文省略 `sustenance` 的宾语→confirmed; 不会造成机制误解（提示核心是只能以敌人为对象）→confirmed; 是否补“养分／力量／精华”属文风选择→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01803

- 位置：`mod-tome.lua:24129`（tome）｜section：`mod-tome/data/talents/cursed/darkness.lua`｜source_tag：`tformat`
- 原文：`Sends a torrent of searing darkness through your foes, doing %d darkness damage. There is a 25%% chance the rushing darkness will blind them for 3 turns and cause them to lose track of their target.
		If you know the Creeping Darkness talent, a short-lived trail of darkness is left in the beam's wake. Its damage is identical to that of Creeping Darkness's.
		The damage will increase with your Mindpower. You do +%d%% damage to anything that has entered your creeping dark.`
- 现译：`向敌人发射一股灼热的黑暗能量，造成 %d 点黑暗伤害。黑暗能量有 25%% 概率致盲目标 3 回合并使它们丢失当前目标。
			如果你掌握黑暗之雾技能，会在射线范围内留下短暂的黑暗尾迹，其伤害等同于黑暗之雾的伤害。
			伤害受精神强度加成。你对任何进入黑暗之雾的人造成 +%d%% 伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00279 | HUMAN-REVIEW | cross-batch-060 | confirmed | 确认正式术语；末句改“目标/生物” |  |  |

<details><summary>hrq-00279 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`DARKNESS` 与同批“暗影伤害抗性”称谓不一致；confirmed：`anything` 译“人”过窄（源码为 Actor）；confirmed：占位符顺序无误。pending：术语库是否唯一规定“暗影伤害”
```
```
raw verdict: `DARKNESS` 伤害与同批“暗影伤害抗性”称谓不一致→confirmed; 术语库唯一规定必须译“暗影伤害”→pending; `anything` 译成“人”范围过窄（源码为 Actor）→confirmed; `%d`、`25%%`、`+%d%%` 数量和顺序无问题→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01804

- 位置：`mod-tome.lua:24135`（tome）｜section：`mod-tome/data/talents/cursed/darkness.lua`｜source_tag：`tformat`
- 原文：`Spawn tendrils of darkness to pursue a single target for up to 12 turns, leaving behind a trail of creeping darkness as they move. Targets seized by the tendrils are pinned for %d turns and shrouded in darkness. The darkness deals %0.2f damage per turn to those within.
		The damage will increase with your Mindpower. You do +%d%% damage to anything that has entered your creeping dark.`
- 现译：`召唤黑暗触手攻击某个敌人，持续12回合。当黑暗触手移动时，黑暗之雾会跟随蔓延。
			被触手抓住的敌人会被定身 %d 回合并被黑暗笼罩，每回合黑暗会造成 %0.2f 点伤害。
			伤害受精神强度加成。你对任何进入黑暗之雾的人造成 +%d%% 伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00280 | HUMAN-REVIEW | cross-batch-060 | confirmed | 与 01803 统一措辞 |  |  |

<details><summary>hrq-00280 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：三参数对应正确；confirmed：末句 `anything` 译“人”仍过窄
```
```
raw verdict: 三个格式化参数对应正确→confirmed; 末句 `anything` 译“人”仍过窄→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01807

- 位置：`mod-tome.lua:24168`（tome）｜section：`mod-tome/data/talents/cursed/endless-hunt.lua`｜source_tag：`tformat`
- 原文：`Let hate fuel your movements. While active, you gain %d%% movement speed. The recklessness of your movement brings you bad luck (Luck -3).
		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
		Sustaining Surge while Dual Wielding grants %d additional Defense.
		Movement speed and dual-wielding Defense both increase with the Willpower stat.`
- 现译：`让杀意激发你敏捷的身手，提高你 %d%% 移动速度。不顾一切的移动会带给你厄运（-3 幸运）。
		分裂攻击、无所畏惧和杀意涌动不能同时开启，并且激活其中一个也会使另外两个进入冷却。
		双持武器时，杀意涌动还会提高你 %d 的闪避。
		移动速度和双持时的闪避增益受意志加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00281 | HUMAN-REVIEW | cross-batch-060 | confirmed | 是否要求技能风味直译资源名 |  |  |

<details><summary>hrq-00281 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`hate` 意译“杀意”非可确认误译。confirmed：占位符与互斥/冷却说明一致
```
```
raw verdict: `hate` 意译“杀意”并非可确认误译→advisory; 两个占位符对应移动速度与双持 Defense，互斥与冷却说明一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01820

- 位置：`mod-tome.lua:24317`（tome）｜section：`mod-tome/data/talents/cursed/one-with-shadows.lua`｜source_tag：`tformat`
- 原文：`You empathy with your shadows causes the line between you and your shadows to blur.
		You lose %d%% light resistance, but gain %d%% darkness resistance and affinity. You also gain %0.2f%% all resistance for each shadow in your party.`
- 现译：`你与阴影之间的共鸣，使彼此的界限逐渐模糊。
		你的光系伤害抗性变化 %d%%，并获得 %d%% 暗影伤害抗性和伤害亲和。你的队伍里每有一个阴影，就获得 %0.2f%% 所有伤害抗性。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00282 | HUMAN-REVIEW | cross-batch-060 | confirmed | 可接受现适配；改写须同时考虑负数实参 |  |  |

<details><summary>hrq-00282 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：负数参数判断正确；译文“变化 -15%”忠实；占位符顺序正确
```
```
raw verdict: 负数参数判断正确（`lose -15%` 实际形成）→confirmed; 译文“变化 %d%%”代入 -15 后忠实反映降低 15 点光抗→confirmed; 三个占位符及顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01823

- 位置：`mod-tome.lua:24366`（tome）｜section：`mod-tome/data/talents/cursed/primal-magic.lua`｜source_tag：`logPlayer`
- 原文：`Selects a displacement location...`
- 现译：`选择一个转移目标…`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00283 | HUMAN-REVIEW | cross-batch-060 | confirmed | 与 `Displace` 既定译名统一，明确是目的地坐标 |  |  |

<details><summary>hrq-00283 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这里是地面选点而非生物目标；confirmed：“选择一个转移目标”有交互歧义
```
```
raw verdict: 这里是地面选点而非生物目标（半径 0 + 可移动检查）→confirmed; 译成“选择一个转移目标”存在交互歧义→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-059-01.md](reports/sol-059-01.md)。译文未修改。共 19 个 claim：15 confirmed、2 pending、2 advisory、0 refuted。 译文未修改。2 条 pending（术语记录类）留主代理核对。
```
</details>

## entry-01835

- 位置：`mod-tome.lua:24511`（tome）｜section：`mod-tome/data/talents/cursed/shadows.lua`｜source_tag：`tformat`
- 原文：`While this ability is active, you will continually call up to %d level %d shadows to aid you in battle. Each shadow costs 5 hate to summon. Shadows are weak combatants that can: Use Arcane Reconstruction to heal themselves (level %d), Blindside their opponents (level %d), and Phase Door from place to place.
		Shadows ignore %d%% of the damage dealt to them by their master.`
- 现译：`当此技能激活时，你可以召唤 %d 个等级 %d 的阴影帮助你战斗。每个阴影需消耗 5 点仇恨值召唤。
		阴影是脆弱的战士，它们能够：使用奥术重组治疗自己（等级 %d），使用闪电突袭攻击敌人（等级 %d），使用相位之门进行传送。
		阴影无视主人对它们造成的 %d%% 伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00284 | HUMAN-REVIEW | cross-batch-061 | confirmed | 改“持续召唤至多 %d 个……”，按机制完整性处理 |  |  |

<details><summary>hrq-00284 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏 `continually` 与 `up to`（持续技能、上限 1–4 个、自动补充）
```
```
raw verdict: 遗漏 `continually` 与 `up to` 两层机制信息（持续技能且上限1–4个）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-061-01.md](reports/sol-061-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。2 条 refuted 是对 Gemini 判断的下修，原样转录。
```
</details>

## entry-01838

- 位置：`mod-tome.lua:24528`（tome）｜section：`mod-tome/data/talents/cursed/shadows.lua`｜source_tag：`logCombat`
- 原文：`#PINK#The shadows converge on #Target#!`
- 现译：`#PINK#阴影被集中至 #Target#！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00285 | HUMAN-REVIEW | cross-batch-061 | confirmed | 统一润色为“阴影向 #Target# 集中！” |  |  |

<details><summary>hrq-00285 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：该日志属进攻分支；confirmed：与 01839 中文完全相同。advisory：单独看本条尚不足以确认独立机制误译
```
```
raw verdict: 该日志属于敌对目标的进攻分支→confirmed; 与 entry-01839 使用完全相同的中文译文→confirmed; 单独看本条尚不足以确认独立机制误译→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-061-01.md](reports/sol-061-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。2 条 refuted 是对 Gemini 判断的下修，原样转录。
```
</details>

## entry-01839

- 位置：`mod-tome.lua:24530`（tome）｜section：`mod-tome/data/talents/cursed/shadows.lua`｜source_tag：`logCombat`
- 原文：`#PINK#The shadows form around #Target#!`
- 现译：`#PINK#阴影被集中至 #Target#！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00286 | HUMAN-REVIEW | cross-batch-061 | confirmed | 改“阴影在 #Target# 周围列阵！”；是否加“护卫”由人工定 |  |  |

<details><summary>hrq-00286 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：攻防语境差异成立，现译丢失防守语义（`form around` 被译成与进攻相同）
```
```
raw verdict: Gemini 对攻防语境差异的判断成立，现译丢失防守语义→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-061-01.md](reports/sol-061-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。2 条 refuted 是对 Gemini 判断的下修，原样转录。
```
</details>

## entry-01851

- 位置：`mod-tome.lua:24737`（tome）｜section：`mod-tome/data/talents/gifts/corrosive-blades.lua`｜source_tag：`tformat`
- 原文：`Channel acid through your psiblades, extending their reach to create a beam doing %0.1f Acid damage (which can disarm them).
		The damage increases with your Mindpower.`
- 现译：`在你的心灵利刃里充填酸性能量，延展攻击范围，形成一道射线，造成 %0.1f 点酸性缴械伤害。
		伤害受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00287 | HUMAN-REVIEW | cross-batch-061 | confirmed | 恢复条件关系“并可能缴械”；概率数值是否写明另议 |  |  |

<details><summary>hrq-00287 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：酸性伤害 + 可能触发缴械。refuted：“浓缩但未造成机制歧义”不成立（25% 概率、可免疫）
```
```
raw verdict: 技能确造成酸性伤害并附带可能触发的缴械→confirmed; Gemini “浓缩但未造成机制歧义”不成立（缴械非必然）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-061-01.md](reports/sol-061-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。2 条 refuted 是对 Gemini 判断的下修，原样转录。
```
</details>

## entry-01861

- 位置：`mod-tome.lua:24890`（tome）｜section：`mod-tome/data/talents/gifts/eyals-fury.lua`｜source_tag：`tformat`
- 原文：`Your devotion to nature has made your body more attuned to the natural world and resistant to unnatural energies.
		You gain %d Spell save, %0.1f%% Arcane resistance, and %0.1f%% Nature damage affinity.
		You defy arcane forces, so that any time you take damage from a spell, you restore %0.1f Equilibrium each turn for %d turns.
		The effects increase with your Mindpower.`
- 现译：`你对自然的虔诚让你的身体更亲近自然世界，对非自然力量也更具抵抗力。
		你获得 %d 点法术豁免，%0.1f%% 奥术抗性，以及 %0.1f%% 自然伤害亲和。
		由于你和奥术力量对抗，每次你受到法术伤害时，你每回合回复 %0.1f 点失衡值，持续 %d 回合。
		效果受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00288 | HUMAN-REVIEW | cross-batch-061 | confirmed | 改“每回合降低／减少 %0.1f 点失衡值” |  |  |

<details><summary>hrq-00288 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：效果是每回合降低失衡值；confirmed：“回复失衡值”可能被读反。refuted：Gemini“未算翻译错误”不成立
```
```
raw verdict: 该效果实际是每回合降低失衡值→confirmed; “回复 %0.1f 点失衡值”可能被理解为失衡增加→confirmed; Gemini “严格遵照英文原文未算翻译错误”结论不成立→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-061-01.md](reports/sol-061-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。2 条 refuted 是对 Gemini 判断的下修，原样转录。
```
</details>

## entry-01868

- 位置：`mod-tome.lua:24956`（tome）｜section：`mod-tome/data/talents/gifts/fungus.lua`｜source_tag：`tformat`
- 原文：`Surround yourself with a myriad of tiny, nearly invisible, reinforcing fungi.
		You gain %d maximum life and %d life regeneration.
		The effects will increase with your Willpower.`
- 现译：`使你自身周围环绕无数微不可见、有治疗作用的孢子。
		你获得 %d 最大生命值，%d 生命回复。
		效果受意志值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00289 | HUMAN-REVIEW | cross-batch-062 | confirmed | 统一改“真菌”“强化作用”类措辞 |  |  |

<details><summary>hrq-00289 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`fungi` 译“孢子”不准（真菌≠孢子）；confirmed：`reinforcing` 译“有治疗作用的”未覆盖 max_life
```
```
raw verdict: `fungi` 译“孢子”不准确（真菌与孢子非同一概念）→confirmed; `reinforcing` 译“有治疗作用的”语义偏移（未覆盖 max_life）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01870

- 位置：`mod-tome.lua:24969`（tome）｜section：`mod-tome/data/talents/gifts/fungus.lua`｜source_tag：`tformat`
- 原文：`Your fungus reaches into the primordial ages of the world, granting you ancient instincts.
		Each time you receive non-regeneration healing you gain %0.1f%% of a turn per 100 life healed.  This effect can't add energy past 2 stored turns and overhealing is not counted.
		Also, regeneration effects on you will decrease your equilibrium by %0.1f each turn.
		The turn gain increases with your Mindpower.`
- 现译：`你的孢子可以追溯到创世纪元，你可以传承来自远古的天赋。
		每当你获得一个非回复的治疗效果，每治疗 100 点生命值，你获得 %0.1f%% 个回合。
		这一效果最多获得 2 个回合。
		同时，每当你受到回复作用时，每回合你的失衡值将会减少 %0.1f。
		增益回合受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00290 | HUMAN-REVIEW | cross-batch-062 | confirmed | 补机制句与“最多储存两回合能量”；拆行仅在要求结构时合并 |  |  |

<details><summary>hrq-00290 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译“过量治疗不计入”（关键机制）；confirmed：`Your fungus` 译“你的孢子”。advisory：四行变五行的拆行
```
```
raw verdict: 漏译“过量治疗不计入”→confirmed; 原文四行译文五行的拆行变化→advisory; `Your fungus` 译“你的孢子”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01891

- 位置：`mod-tome.lua:25019`（tome）｜section：`mod-tome/data/talents/gifts/gifts.lua`｜source_tag：`_t`
- 原文：`Cover the floor with natural mucus.`
- 现译：`用粘液覆盖地面。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00291 | HUMAN-REVIEW | cross-batch-062 | advisory | 可改“天然/自然生成的粘液” |  |  |

<details><summary>hrq-00291 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`natural mucus` 漏译 `natural`
```
```
raw verdict: `natural mucus` 漏译 `natural`→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01895

- 位置：`mod-tome.lua:25031`（tome）｜section：`mod-tome/data/talents/gifts/gifts.lua`｜source_tag：`_t`
- 原文：`Unleash nature's fury against foes around you.`
- 现译：`向敌人释放自然的愤怒。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00292 | HUMAN-REVIEW | cross-batch-062 | confirmed | 补“向你周围的敌人” |  |  |

<details><summary>hrq-00292 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `around you` 空间限定
```
```
raw verdict: 漏译 `around you` 空间限定→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01899

- 位置：`mod-tome.lua:25114`（tome）｜section：`mod-tome/data/talents/gifts/malleable-body.lua`｜source_tag：`tformat`
- 原文：`Your body is more like that of an ooze, you can split into two for %d turns.
		Your original self has the original ooze aspect while your mitosis gains the acid aspect.
		If you know the Oozing Blades tree all the talents inside are exchanged for those of the Corrosive Blades tree.
		Your two selves share the same healthpool.
		While you are split both of you gain %d%% all resistances.
		Resistances will increase with Mindpower.`
- 现译：`你的身体变得像软泥怪一样，你可以分裂成2个，持续 %d 回合。
		你的本体获得原始的软泥特性，而分裂体则获得酸性特性。
		如果你习得软泥之刃系技能树，则该技能树会变为腐蚀之刃技能树。
		你和分裂体共享生命。
		当你分裂时，你和分裂体增加 %d%% 所有抵抗。
		抵抗受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00293 | HUMAN-REVIEW | cross-batch-062 | confirmed | 按术语改；名称一致性待取冻结条目 |  |  |

<details><summary>hrq-00293 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`all resistances` 译“抵抗”不符术语（应为“抗性/全部抗性”）。pending：技能树名“利刃/之刃”一致性（冻结输入无法证明）
```
```
raw verdict: “软泥之刃/腐蚀之刃”与前文“利刃”不一致（冻结输入无法证明）→pending; `all resistances / Resistances` 译“抵抗”不符本批术语“抗性”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01905

- 位置：`mod-tome.lua:25165`（tome）｜section：`mod-tome/data/talents/gifts/mindstar-mastery.lua`｜source_tag：`tformat`
- 原文：`Smash your psiblades into the ground, creating a tide of crystallized leaves circling you in a radius of 3 for 7 turns.
		All foes hit by the leaves will start bleeding for %0.2f per turn (cumulative).
		All allies hit will be covered in leaves, granting them %d%% chance to completely avoid any damaging attack.
		Damage and avoidance will increase with your Mindpower and Mindstar power (requires two mindstars, multiplier %0.2f).`
- 现译：`将你的心灵利刃砸入地面，在你周围 3 码半径范围内形成一圈盘旋的结晶树叶，持续 7 回合。
		被树叶击中的敌人会开始流血，每回合受到 %0.2f 点伤害（可叠加）。
		所有被树叶覆盖的同伴，获得 %d%% 概率完全免疫任何伤害。
		伤害和免疫几率受精神强度和灵晶强度加成（需要 2 只灵晶，加成比例 %0.2f）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00294 | HUMAN-REVIEW | cross-batch-062 | advisory | 可改“免受伤害几率”；重复措辞不改 |  |  |

<details><summary>hrq-00294 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`avoid/avoidance` 译“免疫”过泛。refuted：未重复“流血伤害”不构成问题
```
```
raw verdict: `avoid/avoidance` 译“免疫/免疫几率”过于泛化→advisory; 未在数值后再次写明“流血伤害”构成问题→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-062-01.md](reports/sol-062-01.md)。译文未修改。共 11 个 claim：6 confirmed、3 advisory、1 pending、1 refuted。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-01911

- 位置：`mod-tome.lua:25260`（tome）｜section：`mod-tome/data/talents/gifts/mucus.lua`｜source_tag：`tformat`
- 原文：`Your mucus is brought to near sentience.
		Each turn, there is a %d%% chance that a random spot of your mucus will spawn a Mucus Ooze.
		Mucus Oozes last %d turns and will attack any of your foes by spitting slime at them.
		You may have up to %d Mucus Oozes active at any time (based on your Cunning).
		Any time you deal a mental critical, the remaining time on all of your Mucus Oozes will increase by 2.
		The spawn chance increases with your Mindpower.`
- 现译：`你的粘液有了自己的感知。每回合有 %d%% 几率，随机一个滴有你的粘液的格子会产生一只粘液软泥怪。
		粘液软泥怪会存在 %d 回合，会向任何附近的敌人释放史莱姆喷吐。
		同时场上可存在 %d 只粘液软泥怪。（基于你的灵巧值）
		每当你造成一次精神暴击，你的所有粘液软泥怪的存在时间会延长 2 回合。
		生成概率受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00295 | HUMAN-REVIEW | cross-batch-063 | advisory | 仅在要求段落结构时恢复 |  |  |

<details><summary>hrq-00295 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：原文前两句换行被合并
```
```
raw verdict: 原文前两句的换行被合并→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-063-01.md](reports/sol-063-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 排版判断的下修，原样转录。
```
</details>

## entry-01913

- 位置：`mod-tome.lua:25288`（tome）｜section：`mod-tome/data/talents/gifts/ooze.lua`｜source_tag：`tformat`
- 原文：`Your body is more like that of an ooze.
		When you take damage, you may split and create a Bloated Ooze nearby within your line of sight.
		This ooze has as much health as twice the damage you took (up to a maximum of %d, based on your Mindpower and maximum life).
		The chance to split equals the percent of your health lost times %0.2f.
		You may have up to %d Bloated Oozes active at any time (limited by talent level and the summoning limit), and all damage you take will be split equally between you and them so long as this talent is active.
		Bloated Oozes last for %d turns, are very resilient (%d%% all damage resistance to damage not coming through your shared link), and regenerate life quickly.
		%sThe chance to split increases with your Cunning.`
- 现译：`你的身体构造变的像软泥怪一样。
		当你受到攻击时，你有几率分裂出一个浮肿软泥怪，其生命值为你所承受的伤害值的两倍（最大 %d，基于你的精神强度和最大生命值）。
		分裂几率为你损失生命百分比的 %0.2f 倍。
		你同时最多只能拥有 %d 只浮肿软泥怪，你所承受的所有伤害会在你和浮肿软泥怪间均摊。
		每只浮肿软泥怪存在 %d 回合，对非均摊的伤害的抗性很高（%d%% 对全部伤害的抗性），同时生命回复快。
		%s几率受灵巧加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00296 | HUMAN-REVIEW | cross-batch-063 | confirmed | 三处按源码回改 |  |  |

<details><summary>hrq-00296 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：漏译“受技能等级和召唤上限限制”；“受到攻击”错误扩大/改变触发条件；末句省略“分裂”只写“几率受灵巧加成”
```
```
raw verdict: 漏译“受技能等级和召唤上限限制”→confirmed; “受到攻击”错误扩大或改变触发条件→confirmed; 末句省略“分裂”，只写“几率受灵巧加成”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-063-01.md](reports/sol-063-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 排版判断的下修，原样转录。
```
</details>

## entry-01917

- 位置：`mod-tome.lua:25317`（tome）｜section：`mod-tome/data/talents/gifts/ooze.lua`｜source_tag：`tformat`
- 原文：`Your body's internal organs are indistinct, disguising your vital areas.
		You have a %d%% chance to shrug off all direct critical hits (physical, mental, spell).
		In addition you gain %d%% resistance to disease, poison, wounds and blindness.`
- 现译：`你体内的器官模糊难辨，掩盖了你的要害部位。
		你受到的直接暴击（物理、精神、法术）的额外伤害降低 %d%%。
		你将额外获得 %d%% 的疾病、毒素、流血和目盲免疫。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00297 | HUMAN-REVIEW | cross-prior-spot06 | confirmed | Sol 建议改为「致盲免疫」；保留报告供维护者取舍。与上一轮宿主 advisory 不同，本轮不由宿主再裁决。 |  |  |

<details><summary>hrq-00297 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：mod-tome.lua:25321 ｜ confirmed：目盲/致盲术语不一致
```
```
raw verdict: 暴击机制→refuted; wounds/流血→refuted; blindness/目盲→confirmed
```
```
段末说明：# 人工复核清单（持续更新） 以下只转录交叉 REVIEWER 意见，不代表 ORCHESTRATOR 自行裁决或修复授权。 暴击机制、wounds/流血两项被 Sol 判为 refuted，源码证据见 reports/sol-prior-01.md。译文未修改。
```
</details>

## entry-01919

- 位置：`mod-tome.lua:25331`（tome）｜section：`mod-tome/data/talents/gifts/oozing-blades.lua`｜source_tag：`tformat`
- 原文：`You gain %d%% Nature resistance.
		When you deal Acid damage to a creature, you gain a %0.1f%% bonus to Nature damage for %d turns. 
		This damage bonus will improve up to 4 times (no more than once each turn) with later Acid damage you do, up to a maximum of %0.1f%%.
		The resistance and damage increase improve with your Mindpower.`
- 现译：`你的自然抗性增加 %d%%。
		当你造成酸性伤害时，你的自然伤害增加 %0.1f%%，持续 %d 回合。
		伤害加成能够积累到最多4倍（1回合至多触发1次），最大值 %0.1f%%。
		抗性和伤害加成受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00298 | HUMAN-REVIEW | cross-batch-063 | confirmed | 改“最多提升 4 次”类表述 |  |  |

<details><summary>hrq-00298 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“最多4倍”把提升次数误译成倍率
```
```
raw verdict: “最多4倍”把提升次数误译成倍率→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-063-01.md](reports/sol-063-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 排版判断的下修，原样转录。
```
</details>

## entry-01924

- 位置：`mod-tome.lua:25467`（tome）｜section：`mod-tome/data/talents/gifts/storm-drake.lua`｜source_tag：`tformat`
- 原文：`Summon a tornado that moves very slowly towards the target, following it if it changes position.
		Each time it moves every foes within radius 2 takes %0.2f lightning damage and is knocked back 2 spaces.
		When it reaches the target it explodes in a radius of %d, knocking back targets and dealing %0.2f lightning and %0.2f physical damage.
		The tornado will move a maximum of 20 times.
		Damage will increase with your Mindpower.
		Each point in storm drake talents also increases your lightning resistance by 1%%.`
- 现译：`召唤一个龙卷风，它会向着目标极为缓慢地移动，并在目标移动时跟随目标，最多移动20次。
		每当它移动时，半径2范围内的所有敌人会受到 %0.2f 闪电伤害，并被击退2格。
		当它碰到目标的时候，会在 %d 码范围内引发爆炸，击退目标，并造成 %0.2f 闪电和 %0.2f 物理伤害。
		伤害受精神强度加成
		每点雷龙系的天赋可以使你增加闪电抗性 1%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00299 | HUMAN-REVIEW | cross-batch-063 | advisory | 补句号；不按拆句改 |  |  |

<details><summary>hrq-00299 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“伤害受精神强度加成”缺句号。refuted：“最多移动20次”并入首句属排版瑕疵不成立
```
```
raw verdict: “伤害受精神强度加成”缺少句号→advisory; 把“最多移动20次”并入首句属排版瑕疵→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-063-01.md](reports/sol-063-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 排版判断的下修，原样转录。
```
</details>

## entry-01945

- 位置：`mod-tome.lua:25683`（tome）｜section：`mod-tome/data/talents/gifts/summon-distance.lua`｜source_tag：`tformat`
- 原文：`Summon a Fire Drake for %d turns to burn and crush your foes to death. Fire Drakes are behemoths that can burn foes from afar with their fiery breath.
		It will get %d Strength, %d Constitution and 38 Willpower.
		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
		Their Strength and Constitution will increase with your Mindpower.`
- 现译：`召唤一只火龙来摧毁敌人，持续 %d 回合。
		火龙是可以从很远的地方烧毁敌人的强大生物。
		它拥有 %d 点力量，%d 点体质和 38 点意志。
		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
		火龙的力量和体质受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00300 | HUMAN-REVIEW | cross-batch-063 | advisory | 是否补两层动作属文风 |  |  |

<details><summary>hrq-00300 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory（仅部分成立）：`burn and crush your foes to death` 概括成“摧毁敌人”，漏掉烧灼与碾碎
```
```
raw verdict: `burn and crush your foes to death` 概括成“摧毁敌人”，漏掉烧灼与碾碎→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-063-01.md](reports/sol-063-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 refuted、0 pending。 译文未修改。1 条 refuted 是对 Gemini 排版判断的下修，原样转录。
```
</details>

## entry-01970

- 位置：`mod-tome.lua:25806`（tome）｜section：`mod-tome/data/talents/gifts/venom-drake.lua`｜source_tag：`tformat`
- 原文：`Spray forth a glob of acidic moisture at your enemy.
		The target will take %0.2f Mindpower-based acid damage.
		Enemies struck have a 25%% chance to be Disarmed for three turns, as their weapon is rendered useless by an acid coating.
		At Talent Level 5, this becomes a piercing line of acid.
		Every level in Acidic Spray additionally raises your Mindpower by 4, passively.
		Each point in acid drake talents also increases your acid resistance by 1%%.`
- 现译：`向你的敌人喷出一团酸液。
		目标会受到 %0.2f 点基于精神强度的酸性伤害。
		受到攻击的敌人有 25 %%几率被缴械 3 回合，因为酸液将他们的武器给腐蚀了。
		在技能等级 5 时，这道酸液可以穿透一条线上的敌人。
		每点技能等级被动地增加精神强度 4 点。
		每一点毒龙系技能同时也能增加你的酸性抗性 1%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00301 | HUMAN-REVIEW | cross-batch-064 | confirmed | 统一写法 `25%%几率` 或 `25%% 几率` |  |  |

<details><summary>hrq-00301 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（影响仅 advisory）：`25 %%几率` 格式化后成 `25 %几率`，`%%` 前空格不消失
```
```
raw verdict: `25 %%几率` 格式化后显示为 `25 %几率`，留下异常空格（影响级别仅 advisory）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-064-01.md](reports/sol-064-01.md)。译文未修改。共 6 个 claim：6 confirmed、0 其他。Sol 明确三档性质不同。 译文未修改。Sol 的分档直接决定修复优先级，原样转录。
```
</details>

## entry-01976

- 位置：`mod-tome.lua:25875`（tome）｜section：`mod-tome/data/talents/misc/horrors.lua`｜source_tag：`tformat`
- 原文：`Bites the target for %d%% weapon damage, potentially causing it to bleed for %d%% weapon damage over five turns.
		If the target is affected by the bleed it will send the devourer into a frenzy for %d turns (which in turn will frenzy other nearby devourers).
		The frenzy will increase global speed by %d%%, physical crit chance by %d%%, and prevent death until -%d%% life.`
- 现译：`咬伤目标，造成 %d%% 武器伤害，可能让目标进入流血状态，在五回合内造成 %d%% 武器伤害。
		如果目标进入流血状态，吞噬者会进入狂热状态 %d 回合（也会让周围的其他吞噬者进入狂热状态）。
		狂热状态会增加全局速度 %d%% , 物理暴击率 %d%% , 同时降至 -%d%% 生命时才会死去。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00302 | HUMAN-REVIEW | cross-batch-064 | confirmed | 按中文排版改全角逗号 |  |  |

<details><summary>hrq-00302 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（影响仅 advisory）：末行两处带前置空格的半角逗号 `%d%% ,`
```
```
raw verdict: 末行两处使用带前置空格的英文半角逗号 `%d%% ,`（影响级别仅 advisory）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-064-01.md](reports/sol-064-01.md)。译文未修改。共 6 个 claim：6 confirmed、0 其他。Sol 明确三档性质不同。 译文未修改。Sol 的分档直接决定修复优先级，原样转录。
```
</details>

## entry-01980

- 位置：`mod-tome.lua:25892`（tome）｜section：`mod-tome/data/talents/misc/horrors.lua`｜source_tag：`tformat`
- 原文：`Summon a storm of swirling blades to slice your foes, inflicting %d physical damage and bleeding to anyone who approaches for %d turns.
		The damage and duration will increase with your Mindpower.`
- 现译：`召唤旋转剑刃风暴将敌人切成碎片，对进入风暴的敌人造成 %d 点物理伤害并令其流血 %d 回合。
		伤害和流血持续时间受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00303 | HUMAN-REVIEW | cross-batch-064 | confirmed | 按建议句式重写：“……使其流血，风暴持续 %d 回合” |  |  |

<details><summary>hrq-00303 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**confirmed（实质问题）**：第二个 `%d` 是旋刃风暴持续时间，不是流血时长（流血固定 5 回合）；现译把 `%d` 挂到流血并漏掉风暴持续
```
```
raw verdict: 第二个 `%d` 是旋刃风暴的存在时间而非流血持续时间；流血固定 5 回合（实质问题）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-064-01.md](reports/sol-064-01.md)。译文未修改。共 6 个 claim：6 confirmed、0 其他。Sol 明确三档性质不同。 译文未修改。Sol 的分档直接决定修复优先级，原样转录。
```
</details>

## entry-01984

- 位置：`mod-tome.lua:25923`（tome）｜section：`mod-tome/data/talents/misc/horrors.lua`｜source_tag：`tformat`
- 原文：`Open a hole in space, summoning an animated blade for 10 turns.`
- 现译：`在空间中打开一个孔洞，召唤一把活化之剑 10 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00304 | HUMAN-REVIEW | cross-batch-064 | confirmed | 作为历史陈旧键单独清理，不与 01980 同级修复 |  |  |

<details><summary>hrq-00304 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：固定版实为 15 回合；10 回合条目在固定版不命中（仅 locale 数据）；旧条目语义本身准确
```
```
raw verdict: 固定版本实际使用 15 回合→confirmed; 10 回合条目在固定版本不会命中（仅 locale 数据中有）→confirmed; 旧条目对旧英文的翻译在语义上准确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-064-01.md](reports/sol-064-01.md)。译文未修改。共 6 个 claim：6 confirmed、0 其他。Sol 明确三档性质不同。 译文未修改。Sol 的分档直接决定修复优先级，原样转录。
```
</details>

## entry-01988

- 位置：`mod-tome.lua:25973`（tome）｜section：`mod-tome/data/talents/misc/inscriptions.lua`｜source_tag：`tformat`
- 原文：`Activate the infusion to endure even the most grievous of wounds for %d turns.
		While Heroism is active, you will only die when reaching -%d life.
		The duration and life will increase by 1%% for every 1%% life you have lost (currently %d life, %d duration)
		If your life is below 0 when this effect wears off it will be set to 1.`
- 现译：`激活这个纹身可以让你忍受致死的伤害，持续 %d 回合。
		当英勇纹身激活时，你的生命值只有在降低到 -%d 生命时才会死亡。
		你每失去 1%% 生命值，持续时间和生命值下限就会增加 1%%。
		（目前 %d 生命值，%d 持续时间）
		效果结束时，如果你的生命值在 0 以下，会变为 1 点。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00305 | HUMAN-REVIEW | cross-batch-065 | confirmed | 历史键单独清理；版式与措辞低优先级 |  |  |

<details><summary>hrq-00305 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：这是历史遗留文本（旧串只在 `zh_hans.lua`，现行技能描述已含“生命≤0 最多+100%”）。advisory：括号数值拆行；advisory：“致死的伤害”略加词
```
```
raw verdict: 括号数值被拆成独立行（仅版式）→advisory; “致死的伤害”略有加词→advisory; 这是历史遗留文本（旧串仅存于 zh_hans.lua）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-01989

- 位置：`mod-tome.lua:25981`（tome）｜section：`mod-tome/data/talents/misc/inscriptions.lua`｜source_tag：`tformat`
- 原文：`die at -%d; dur %d; cd %d`
- 现译：`-%d 死亡底线；持续 %d; 冷却 %d`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00306 | HUMAN-REVIEW | cross-batch-065 | confirmed | 统一分号 |  |  |

<details><summary>hrq-00306 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：中英文分号混用
```
```
raw verdict: 中英文分号混用（`-%d 死亡底线；持续 %d;`）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-01994

- 位置：`mod-tome.lua:26029`（tome）｜section：`mod-tome/data/talents/misc/inscriptions.lua`｜source_tag：`tformat`
- 原文：`Activate the rune to teleport up to %d spaces within line of sight.  Afterwards you stay out of phase for %d turns. In this state all new negative status effects duration is reduced by %d%%, your defense is increased by %d and all your resistances by %d%%.`
- 现译：`激活符文，传送到视野内 %d 格内的指定位置。之后，你会脱离相位 %d 回合。在这种状态下，所有新的负面效果的持续时间减少 %d%%，你的闪避增加 %d，你的全体伤害抗性增加 %d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00307 | HUMAN-REVIEW | cross-batch-065 | advisory | 是否要求技能说明复用状态栏名 |  |  |

<details><summary>hrq-00307 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“脱离相位”与状态名“脱离现实”不一致，但本句描述性短语本身准确
```
```
raw verdict: “脱离相位”与效果名“脱离现实”不一致（本句描述性短语本身准确）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02000

- 位置：`mod-tome.lua:26137`（tome）｜section：`mod-tome/data/talents/misc/inscriptions.lua`｜source_tag：`tformat`
- 原文：`Activate the infusion to endure even the most grievous of wounds for %d turns.
		While Heroism is active, you will only die when reaching -%d life.
		The duration and life will increase by 1%% for every 1%% life you have lost, to a maximum of 100%% at 0 life or less (currently %d life, %d duration)
		If your life is below 0 when this effect wears off it will be set to 1.`
- 现译：`激活这个纹身可以让你忍受致死的伤害，持续 %d 回合。
		当英勇纹身激活时，你的生命值只有在降低到 -%d 生命时才会死亡。
		你每失去 1%% 生命值，持续时间和生命值下限就会增加 1%%，在生命值降至 0 或更低时最多提高 100%%。
		（目前 %d 生命值，%d 持续时间）
		效果结束时，如果你的生命值在 0 以下，会变为 1 点。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00308 | HUMAN-REVIEW | cross-batch-065 | advisory | 版式取舍 |  |  |

<details><summary>hrq-00308 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：当前数值括号被拆行（信息完整）
```
```
raw verdict: 当前数值括号被拆行→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02004

- 位置：`mod-tome.lua:26213`（tome）｜section：`mod-tome/data/talents/misc/misc.lua`｜source_tag：`_t`
- 原文：`Use the onboard short-range teleport of the Fortress to beam down to the surface.
	Requires being in flight above the ground of a planet.`
- 现译：`使用堡垒自带的短程传送装置“哔”的一下回到地面。
	需要在某个星球的空中飞行。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00309 | HUMAN-REVIEW | cross-batch-065 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00309 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`beam down` 译“哔的一下”口语化（三个信息点保留）
```
```
raw verdict: `beam down` 译“哔的一下”过于口语化→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02015

- 位置：`mod-tome.lua:26343`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`_t`
- 原文：`@Source@ rushes out, claws sharp and ready!`
- 现译：`@Source@冲了出去，用尖利的爪子攻击！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00310 | HUMAN-REVIEW | cross-batch-065 | confirmed | 按源码回改动作描述 |  |  |

<details><summary>hrq-00310 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`claws sharp and ready` 被动作化为“用尖利的爪子攻击”，实际动作是冲向目标并定身
```
```
raw verdict: `claws sharp and ready` 被动作化为“用尖利的爪子攻击”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02022

- 位置：`mod-tome.lua:26417`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Start to sever the lifeline of the target. After 4 turns, if the target is still in line of sight of you, its existance will be ended (%d temporal damage).`
- 现译：`引导法术离断目标的生命线，如果 4 回合之后目标仍然在视线内则会立即死亡(%d 时空伤害)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00311 | HUMAN-REVIEW | cross-batch-065 | confirmed | 三处按源码重写，避免“引导法术”误导 |  |  |

<details><summary>hrq-00311 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：并非引导法术（4 回合效果挂目标）；施法者可自由移动施技；实际结算是时空伤害而非无条件立即死亡
```
```
raw verdict: 并非引导法术（一次性 action 挂 4 回合效果于目标）→confirmed; 施法者随后可移动和使用其他技能→confirmed; 实际结算是时空伤害而非无条件立即死亡→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02023

- 位置：`mod-tome.lua:26441`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Engulfs your hands (and weapons) in a sheath of frost, dealing %0.2f cold damage per melee attack and increasing all cold damage by %d%%.
		The effects will increase with your Spellpower.`
- 现译：`将你的双手（及武器）笼罩在寒冰之中，每次近战攻击造成 %0.2f 冰冷伤害，并提高 %d%% 冰冷伤害。
		效果受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00312 | HUMAN-REVIEW | cross-batch-065 | confirmed | 按术语改 |  |  |

<details><summary>hrq-00312 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两处“冰冷伤害”应按术语“寒冷”
```
```
raw verdict: 两处“冰冷伤害”应按术语为“寒冷”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02024

- 位置：`mod-tome.lua:26456`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Calls forth a powerful beam of lightning doing %0.2f to %0.2f lightning damage (%0.2f average).
		The damage will increase with your Mindpower.`
- 现译：`召唤一股强烈的闪电束造成 %0.2f 至 %0.2f 伤害（平均 %0.2f）。
		伤害受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00313 | HUMAN-REVIEW | cross-batch-065 | confirmed | 补闪电伤害 |  |  |

<details><summary>hrq-00313 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏 `lightning` 伤害类型
```
```
raw verdict: 遗漏 lightning 伤害类型→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02025

- 位置：`mod-tome.lua:26476`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`A punch to the body that deals %d%% damage, drains %d of the target's stamina per combo point, and dazes the target for %d to %d turns, depending on the amount of combo points you've accumulated.
		The daze chance will increase with your Physical Power.
		Using this talent removes your combo points.`
- 现译：`对目标的身体发出强烈的一击，造成 %d%% 伤害，每点连击点消耗 %d 目标体力并眩晕目标 %d 到 %d 回合（由你的连击点数决定）。
		眩晕概率受物理强度加成
		使用此技能会消耗当前所有连击点。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00314 | HUMAN-REVIEW | cross-batch-065 | confirmed | 补句号 |  |  |

<details><summary>hrq-00314 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二行缺句号
```
```
raw verdict: 第二行缺句号→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02026

- 位置：`mod-tome.lua:26482`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`When gaining a combo point, you have a %d%% chance to gain an extra combo point.  Additionally, your combo points will last %d turns longer before expiring.
		The chance of building a second combo point will improve with your Cunning.`
- 现译：`当获得 1 个连击点时有 %d%% 概率
		额外获得 1 个连击点。
		此外你的连击点持续时间会延长 %d 回合。
		额外连击点获得概率受灵巧加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00315 | HUMAN-REVIEW | cross-batch-065 | confirmed | 并句 |  |  |

<details><summary>hrq-00315 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：概率与“额外获得”之间被硬拆行
```
```
raw verdict: 概率与“额外获得”之间被硬拆行→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02027

- 位置：`mod-tome.lua:26488`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Superior cunning and training allows you to outthink and outwit your opponents' physical and mental assaults.  Increases Defense by %d and Mental Save by %d.
		The Defense bonus will scale with your Dexterity, and the save bonus with your Cunning.`
- 现译：`大量的训练使你能保持清醒的头脑，增加 %d 近身闪避和 %d 精神豁免。
		受敏捷影响，闪避按比例加成；
		受灵巧影响，精神豁免按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00316 | HUMAN-REVIEW | cross-batch-065 | confirmed | 按源码恢复三层信息 |  |  |

<details><summary>hrq-00316 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：背景句被明显压缩（漏灵巧、智取、肉体/精神攻击三层）
```
```
raw verdict: 背景句被明显压缩（漏灵巧、智取、肉体/精神攻击）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-065-01.md](reports/sol-065-01.md)。译文未修改。共 16 个 claim：11 confirmed、5 advisory、0 pending/refuted（Sol 明确无必须挂起项）。 译文未修改。Sol 提示 01988 与 batch-064 的 01984 同属历史陈旧键，宜一并纳入专门清理。
```
</details>

## entry-02028

- 位置：`mod-tome.lua:26499`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Each time one of your foes bites the dust, you feel a surge of power, increasing your strength by 2 (stacking up to a maximum of %d) for %d turns.`
- 现译：`每当你让一个敌人扑街，你会漏出一股汹涌的霸气，增加你 2 点力量，上限 %d，持续 %d 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00317 | HUMAN-REVIEW | cross-batch-066 | confirmed | 改回“感到力量涌起”类；俚语是否保留属文风 |  |  |

<details><summary>hrq-00317 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`feel a surge of power` 译“漏出一股汹涌的霸气”（“漏出”方向错、power 戏剧化）。advisory：`bites the dust` 译“扑街”属网络俚语
```
```
raw verdict: `feel a surge of power` 译“漏出一股汹涌的霸气”（向外漏出且 power 戏剧化）→confirmed; `bites the dust` 译“扑街”属网络俚语色彩→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02032

- 位置：`mod-tome.lua:26539`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Sweep without dual wielding!`
- 现译：`你只有在双持状态下才能使用这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00318 | HUMAN-REVIEW | cross-batch-066 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00318 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）
```
```
raw verdict: 条目结论成立（低影响完整性）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02043

- 位置：`mod-tome.lua:26615`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Precision without dual wielding!`
- 现译：`你只有在双持状态下才能使用这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00319 | HUMAN-REVIEW | cross-batch-066 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00319 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（低影响）
```
```
raw verdict: 条目结论成立（低影响）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02050

- 位置：`mod-tome.lua:26667`（tome）｜section：`mod-tome/data/talents/misc/npcs.lua`｜source_tag：`tformat`
- 原文：`Creates a circle of radius %d at your feet; the circle lights up affected tiles, increases your positive energy by %d each turn and deals %0.2f light damage and %0.2f fire damage per turn to everyone else within its radius.  The circle lasts %d turns.
		The damage will increase with your Spellpower.`
- 现译：`在你的脚下制造一个 %d 码半径的法阵，它会照亮范围区域，每回合增加 %d 正能量，并对范围内除你之外的所有生物每回合造成 %0.2f 光系伤害和 %0.2f 火焰伤害。
		阵法持续 %d 回合。
		伤害受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00320 | HUMAN-REVIEW | cross-batch-066 | confirmed | 版式取舍 |  |  |

<details><summary>hrq-00320 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（排版性，影响 advisory 级）
```
```
raw verdict: 条目结论成立（排版性，影响 advisory 级）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02058

- 位置：`mod-tome.lua:26777`（tome）｜section：`mod-tome/data/talents/misc/objects.lua`｜source_tag：`tformat`
- 原文：`Raise your dagger into blocking position for one turn, reducing the damage of all physical melee attacks against you by %d. If you block all of an attack's damage, the attacker will be vulnerable to a deadly counterstrike (a normal attack will instead deal 200%% damage) for one turn and be left disarmed for 3 turns.
		The blocking value will increase with your Dexterity and Cunning.`
- 现译：`举起你的匕首来格挡攻击一回合，减少所有物理伤害 %d 点。如果你完全格挡了一次攻击的伤害，攻击者将进入致命的被反击状态（对其进行的下一次武器攻击伤害增加到 200%%）一回合并被缴械三回合。
		格挡值受敏捷值和灵巧值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00321 | HUMAN-REVIEW | cross-batch-066 | confirmed | 不因漏词补“近战”；上游问题另行记录 |  |  |

<details><summary>hrq-00321 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：表面文本漏 `melee`。refuted：“中文把机制描述错了”不成立（源码实现无近战限制）。advisory：应作为**英文上游**说明不准确处理，不要在中文补“近战”
```
```
raw verdict: 表面文本漏掉 `melee`（英文有 physical melee attacks）→confirmed; “因此中文把机制描述错了”（源码实现无近战限制）→refuted; 应作为英文上游说明不准确的 advisory，不要在中文补“近战”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02066

- 位置：`mod-tome.lua:26894`（tome）｜section：`mod-tome/data/talents/misc/races.lua`｜source_tag：`tformat`
- 原文：`Halflings have always been a very organised and methodical race; the more foes they face, the more organised they are.
		If two or more foes are in sight your Physical Power, Physical Save, Spellpower, Spell Save, Mental Save, and Mindpower are increased by %0.1f per foe (up to 5 foes).`
- 现译：`半身人向来是一个有组织、有条理的种族，敌人越多他们越团结。
		如果有 2 个或多个敌人在你的视野里，每个敌人都会使你的所有强度和豁免提高 %0.1f（最多 5 个敌人）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00322 | HUMAN-REVIEW | cross-batch-066 | confirmed | 归纳可保留 |  |  |

<details><summary>hrq-00322 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：六项属性被归纳成“所有强度和豁免”。refuted：“归纳导致机制信息缺失”不成立
```
```
raw verdict: 六项属性被归纳成“所有强度和豁免”→confirmed; 归纳导致机制信息缺失→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02067

- 位置：`mod-tome.lua:26898`（tome）｜section：`mod-tome/data/talents/misc/races.lua`｜source_tag：`tformat`
- 原文：`Halflings have one of the most powerful military forces in the known world and have been at war with most other races for thousands of years.
		Removes %d stun, daze, or pin effects and grants immunity to stuns, dazes and pins for %d turns.`
- 现译：`半身人拥有已知世界最强大的军事力量之一，数千年来一直与大多数其他种族交战。
		移除 %d 个震慑、眩晕或定身效果，并使你对震慑、眩晕和定身免疫 %d 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00323 | HUMAN-REVIEW | cross-batch-066 | confirmed | 记入上游问题清单，译文低优先级 |  |  |

<details><summary>hrq-00323 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：上游源码参数顺序缺陷（译文层面 advisory 级）
```
```
raw verdict: 上游源码参数顺序缺陷（译文层面 advisory 级）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-066-01.md](reports/sol-066-01.md)。译文未修改。共 11 个 claim：7 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。Sol 明确：真正可确认的译文语义问题只有 02028。两条 refuted 是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02069

- 位置：`mod-tome.lua:26910`（tome）｜section：`mod-tome/data/talents/misc/races.lua`｜source_tag：`tformat`
- 原文：`Orcs have been the prey of the other races for thousands of years, with or without justification. They have learnt to withstand things that would break weaker races.
		When your life goes below 50%% your sheer determination cleanses you of %d mental debuff(s) based on talent level and Willpower.  This can only happen once every %d turns.
		Also increases physical save by %d.`
- 现译：`其他种族对兽族的猎杀持续了上千年，不管是否正义。你们已经学会忍受那些会摧毁弱小种族的灾难。
		当你的生命值降低到 50%% 以下，你强大的意志移除你身上最多 %d 个精神负面效果（基于技能等级和意志）。该效果每 %d 回合最多触发一次。
		额外增加 %d 物理豁免。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00324 | HUMAN-REVIEW | cross-batch-067 | confirmed | 称谓统一 |  |  |

<details><summary>hrq-00324 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“Orcs”译“兽族”；confirmed：占位符与机制数值正确。advisory：“They”改“你们”
```
```
raw verdict: “Orcs”译为“兽族”→confirmed; “They”改为“你们”→advisory; 占位符和机制数值正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02074

- 位置：`mod-tome.lua:27062`（tome）｜section：`mod-tome/data/talents/psionic/absorption.lua`｜source_tag：`tformat`
- 原文：`Surround yourself with a forcefield, reducing all incoming damage by %d%%.
		Such a shield is very expensive to maintain, draining 5%% of your maximum psi per turn initially plus an addition 5%% for each turn it has been maintained. For example, on turn 2 it will drain 10%%.
		Current drain rate: %0.1f psi/turn`
- 现译：`用力场环绕自己，减少受到的所有伤害 %d%%
		维持这样的护盾代价非常昂贵：初始每回合消耗你 5%% 的最大灵能值，此后每多维持一回合再额外增加 5%%。例如第 2 回合会消耗 10%%。
		目前的灵能值消耗：每回合 %0.1f 灵能值`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00325 | HUMAN-REVIEW | cross-batch-067 | confirmed | 补句号 |  |  |

<details><summary>hrq-00325 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：减伤与逐回合灵能消耗描述正确。advisory：首行缺句末标点
```
```
raw verdict: 首行缺少句末标点→advisory; 减伤与逐回合灵能消耗描述正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02081

- 位置：`mod-tome.lua:27179`（tome）｜section：`mod-tome/data/talents/psionic/discharge.lua`｜source_tag：`tformat`
- 原文：`Unleash your subconscious on the world around you.  While active, you fire up to %d bolts each turn (one per hostile target) that deal %0.2f mind damage.  Each bolt consumes 5 Feedback.
		Feedback gains beyond your maximum allowed amount may generate extra bolts (one bolt per %d excess Feedback per target), but no more than %d extra bolts per turn. 
		This effect is a psionic channel, increasing the range of Mind Sear, Psychic Lobotomy, and Sunder Mind to 10 but will break if you move.
		The damage will scale with your Mindpower.`
- 现译：`将你的潜意识释放到周围的世界。当此技能激活时，每回合你最多射出 %d 个灵能值球（每个敌方目标一个），造成 %0.2f 精神伤害。每个灵能值球消耗 5 点反馈值。
		当获得的反馈值超出最大值时，你会产生额外的灵能值球（每个目标每超出 %d 反馈值产生 1 个灵能值球），但是每回合产生的额外灵能值球数量不会超过 %d。
		此技能运用了灵能通道，所以当你移动时会中断此技能。
		特别地，当你开启此技能时，心灵灼烧、心灵脑叶切除和碾碎心灵的攻击范围将变为10格。
		受精神强度影响，伤害按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00326 | HUMAN-REVIEW | cross-batch-067 | confirmed | 改回飞弹类措辞 |  |  |

<details><summary>hrq-00326 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed×3：`bolts` 译“灵能值球”；每枚飞弹消耗 5 Feedback；四占位符正确
```
```
raw verdict: `bolts` 译成“灵能值球”→confirmed; 每枚飞弹消耗 5 Feedback→confirmed; 四个占位符数量/类型/顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02097

- 位置：`mod-tome.lua:27318`（tome）｜section：`mod-tome/data/talents/psionic/dream-smith.lua`｜source_tag：`tformat`
- 原文：`Crush your enemy with your Dream Hammer, inflicting %d%% weapon damage.  If the attack hits, the target is stunned for %d turns.
		Stun chance improves with your Mindpower.  Learning this talent increases your Physical Power for Dream Hammer damage calculations by %d and all damage with Dream Hammer attacks by %d%%.
		`
- 现译：`用你的梦之巨锤碾碎敌人，造成 %d%% 武器伤害。如果攻击命中，则目标会被震慑 %d 回合。
		震慑几率受精神强度加成
		学习此技能会增加 %d 点你使用梦之巨锤时的物理强度，同时使梦之巨锤造成的所有伤害提升 %d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00327 | HUMAN-REVIEW | cross-batch-067 | confirmed | 补句号 |  |  |

<details><summary>hrq-00327 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：伤害/震慑时间/物理强度参数正确。advisory：末尾缺句号
```
```
raw verdict: “震慑几率受精神强度加成”末尾缺句号→advisory; 伤害/震慑时间/物理强度与增幅参数正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02103

- 位置：`mod-tome.lua:27380`（tome）｜section：`mod-tome/data/talents/psionic/feedback.lua`｜source_tag：`tformat`
- 原文：`Use Feedback to replenish yourself.  This heals you for %d life, and restores %d stamina, %d mana, %d equilibrium, %d vim, %d positive and negative energies, %d psi energy, and %d hate.
		The heal and resource gain will improve with your Mindpower.`
- 现译：`使用反馈值来补充自己。治疗 %d 生命值并回复 %d 点耐力，%d 点法力，%d 点失衡值，%d 点活力，%d 点正能量和负能量，%d 点灵能值及 %d 点仇恨值。
		增益效果受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00328 | HUMAN-REVIEW | cross-batch-067 | confirmed | 按术语改 |  |  |

<details><summary>hrq-00328 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`stamina` 译“耐力”；confirmed：八参数及资源对应正确
```
```
raw verdict: `stamina` 译成“耐力”→confirmed; 八个参数及资源对应关系正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02106

- 位置：`mod-tome.lua:27408`（tome）｜section：`mod-tome/data/talents/psionic/finer-energy-manipulations.lua`｜source_tag：`tformat`
- 原文：`By carefully synchronizing your mind to the resonant frequencies of your psionic focus, you strengthen its effects.
		For conventional weapons, this increases the percentage of your willpower and cunning that is used in place of strength and dexterity for all weapon attacks, from 60%% to %d%%.
		For mindstars, this increases the chance to pull enemies to you by +%d%%.
		For gems, this increases the bonus stats by %d.`
- 现译：`通过小心的同步你的精神和灵能聚焦的共振频率，强化灵能聚焦的效果
		对于武器，提升你的意志和灵巧来代替力量和敏捷的百分比，从 60%% 到 %d%%.
		对于灵晶，提升 %d%% 将敌人抓取过来的几率。
		对于宝石，提升 %d 额外全属性。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00329 | HUMAN-REVIEW | cross-batch-067 | confirmed | 修标点；不因正号改语义 |  |  |

<details><summary>hrq-00329 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：行首句号与半角句点混用；confirmed：“全属性”增译符合实现；confirmed：三参数顺序正确。refuted：省略 `+%d%%` 正号**不构成**语义问题
```
```
raw verdict: 第一行缺句号、第二行混用半角句点→advisory; 省略 `+%d%%` 中的正号构成语义问题→refuted; “全属性”增译符合实际实现→confirmed; 三个格式参数顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02107

- 位置：`mod-tome.lua:27420`（tome）｜section：`mod-tome/data/talents/psionic/focus.lua`｜source_tag：`tformat`
- 原文：`Focus energies into a beam to lash all creatures in a line with physical force, doing %d Physical damage and knocking them off balance (-15%% damage penalty) for 2 turns.
		The damage will scale with your Mindpower.`
- 现译：`汇聚能量形成一道光束，鞭笞一条直线上的所有生物，造成 %d 点物理伤害并使它们失去平衡两轮（-15%% 伤害）。
		伤害受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00330 | HUMAN-REVIEW | cross-batch-067 | confirmed | 两轮改“回合”；penalty 可选补 |  |  |

<details><summary>hrq-00330 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`for 2 turns` 译“两轮”；confirmed：伤害/降伤/时长机制准确。refuted：省略 `penalty` **不构成**机制信息丢失（清晰度问题记 advisory）
```
```
raw verdict: `for 2 turns` 译成“两轮”→confirmed; 省略 `penalty` 导致机制信息丢失→refuted; 该省略的清晰度问题→advisory; 物理伤害、15% 降伤与持续时间机制准确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-067-01.md](reports/sol-067-01.md)。译文未修改。共 20 个 claim：13 confirmed、5 advisory、2 refuted、0 pending。 译文未修改。2 条 refuted 是对 Gemini“机制信息丢失”定性的下修，原样转录。
```
</details>

## entry-02109

- 位置：`mod-tome.lua:27517`（tome）｜section：`mod-tome/data/talents/psionic/mental-discipline.lua`｜source_tag：`tformat`
- 原文：`Your expertise in the art of energy projection grows.
		Aura cooldowns are all reduced by %d turns. Aura damage drains energy more slowly (+%0.2f damage required to lose a point of energy).`
- 现译：`你增加了在灵能值运用方面的知识。
		所有光环的冷却时间减少 %d 回合。光环消耗灵能值变的更慢（消耗每点灵能值所需伤害值 +%0.2f）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00331 | HUMAN-REVIEW | cross-batch-068 | confirmed | 改措辞与“变得” |  |  |

<details><summary>hrq-00331 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`energy projection` 译“灵能值运用”偏；confirmed：“变的更慢”字词错误；confirmed：占位符与 tformat 顺序相符
```
```
raw verdict: `energy projection` 译“灵能值运用”偏离原意→confirmed; “变的更慢”是字词错误（应为“变得”）→confirmed; %d、%0.2f 与 tformat(cooldown, mast) 数量和顺序相符→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02110

- 位置：`mod-tome.lua:27521`（tome）｜section：`mod-tome/data/talents/psionic/mental-discipline.lua`｜source_tag：`tformat`
- 原文：`Your expertise in the art of energy absorption grows. Shield cooldowns are all reduced by %d turns, the amount of damage absorption required to gain a point of energy is reduced by %0.1f, and the maximum energy you can gain from each shield is increased by %0.1f per turn.`
- 现译：`你增加了在灵能值吸收方面的知识。所有护盾的冷却时间减少 %d 回合。护盾额外增加灵能值所需伤害值减少 %0.1f，每个护盾的最大能量吸收量增加 %0.1f 每回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00332 | HUMAN-REVIEW | cross-batch-068 | confirmed | 统一“每回合可获能量上限”表述与译名 |  |  |

<details><summary>hrq-00332 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：‘最大能量吸收量’易被读成护盾上限（歧义）。refuted：该歧义的“实际消费逻辑归因”不成立。confirmed：同句 energy 译名前后不一；confirmed：参数一致
```
```
raw verdict: “最大能量吸收量”易被读成护盾吸收上限（译文歧义）→confirmed; 该歧义的“实际消费逻辑归因”不成立→refuted; 同句 energy 先译“灵能值”后译“能量”，内部不一致→confirmed; %d、两个 %0.1f 与 tformat 参数一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02113

- 位置：`mod-tome.lua:27540`（tome）｜section：`mod-tome/data/talents/psionic/mentalism.lua`｜source_tag：`tformat`
- 原文：`Clears your mind of current mental effects, and blocks additional ones over 6 turns.  At most, %d mental effects will be affected.`
- 现译：`净化你当前所有的精神状态，并在接下来的 6 回合内免疫新增的精神状态。最多一共（净化和免疫）能影响 %d 种精神状态。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00333 | HUMAN-REVIEW | cross-batch-068 | confirmed | 依赖后句限定即可，低优先 |  |  |

<details><summary>hrq-00333 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：共享配额符合代码；confirmed：%d 对应 getRemoveCount。advisory：前句孤立看会过度概括
```
```
raw verdict: “净化和免疫共享最多 %d 次配额”符合代码→confirmed; 前句“净化你当前所有的精神状态”孤立看会过度概括→advisory; %d 正确对应 getRemoveCount→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02115

- 位置：`mod-tome.lua:27545`（tome）｜section：`mod-tome/data/talents/psionic/mentalism.lua`｜source_tag：`tformat`
- 原文：`Activate to project your mind from your body for %d turns.  In this state you're invisible (+%d power), can see invisible and stealthed creatures (+%d detection power), can move through walls, and do not need air to survive.
		All damage you suffer is shared with your physical body, and while in this form you may only deal damage to 'ghosts' or through an active mind link (mind damage only in the second case.)
		To return to your body, simply release control of the projection.`
- 现译：`激活此技能可以使你的灵魂出窍，持续 %d 回合。在此效果下，你处于隐形状态（+%d 强度），并且可以看到隐形和潜行单位（+%d 侦查强度），还可以穿过墙体，并且无需呼吸。
		你受到的所有伤害都会与身体共享，当你处于此形态下你只能对“鬼魂”类怪物造成伤害，或者通过激活一种精神通道来造成伤害。
		注：后一种情况下只能造成精神伤害。
		要回到你的身体里，只需释放灵魂体的控制即可。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00334 | HUMAN-REVIEW | cross-batch-068 | confirmed | 术语核对后定 pending |  |  |

<details><summary>hrq-00334 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：`subtype=="ghost"` 判定对象确认（“鬼魂”无错认）需术语佐证。confirmed：括号拆“注”不改语义；confirmed：三参数一致
```
```
raw verdict: 判定对象是 subtype "== ghost"（“鬼魂”无对象错认）→pending; 英文括号拆成“注”未改变语义→confirmed; 三个 %d 与 tformat(duration, power, power) 一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02125

- 位置：`mod-tome.lua:27629`（tome）｜section：`mod-tome/data/talents/psionic/other.lua`｜source_tag：`tformat`
- 原文：`The telekinetically-wielded ranged weapon uses Willpower in place of Strength, and Cunning in place of Dexterity, to determine Accuracy and damage respectively.
			Combat stats:
			Range: %d
			Accuracy: %d
			Damage: %d
			APR: %d
			Crit: %0.1f%%
			Speed: %0.1f%%`
- 现译：`念动远程武器使用意志和灵巧来分别代替力量和敏捷，以决定命中和伤害。
			战斗属性：
			范围：%d
			命中：%d
			伤害：%d
			护甲穿透：%d
			暴击率：%0.1f%%
			攻击速度：%0.1f%%`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00335 | HUMAN-REVIEW | cross-batch-068 | confirmed | 记入上游问题，不在中文改 |  |  |

<details><summary>hrq-00335 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：英文说明自身顺序写反、中文忠实继承；confirmed：参数一致
```
```
raw verdict: 英文说明自身把 Accuracy 与 damage 顺序写反，中文忠实继承→confirmed; 四个 %d、两个 %0.1f%% 与 tformat 一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02128

- 位置：`mod-tome.lua:27692`（tome）｜section：`mod-tome/data/talents/psionic/projection.lua`｜source_tag：`tformat`
- 原文：`Fills the air around you with crackling energy.
		If you have a gem or mindstar in your psionically wielded slot, this will do %0.1f Lightning damage to all adjacent enemies, costing %0.1f energy per creature. 
		If you have a conventional weapon in your psionically wielded slot, this will add %0.1f Lightning damage to all your weapon hits, costing %0.1f energy per hit.
		When deactivated, if you have at least %d energy, a massive spike of electrical energy jumps between up to %d nearby targets, doing up to %0.1f Lightning damage to each with a 50%% chance of dazing them.
		#{bold}#Activating the aura takes no time but de-activating it does.#{normal}#
		To turn off an aura without spiking it, deactivate it and target yourself. The damage will improve with your Mindpower.
		You can only have two of these auras active at once.`
- 现译：`将你周围的空气充满噼啪响的电能。
		如果你的灵能武器槽佩戴的是宝石或灵晶，会对所有相邻的敌人造成 %0.1f 的闪电伤害，每个生物消耗 %0.1f 能量。
		如果你的灵能武器槽佩戴的是武器，每次攻击附加 %0.1f 的闪电伤害，每次攻击消耗 %0.1f 能量。
		当关闭该技能时，如果你拥有最少 %d 点能量，巨大的电能会释放为在最多 %d 个邻近目标间跳跃的闪电，对每个目标造成至多 %0.1f 的闪电伤害，且 50%% 的概率令他们眩晕。
		#{bold}#激活光环是不消耗时间的，但是关闭它则需要消耗时间。#{normal}#
		如果要关闭光环且不发射射线，关闭它并选择你自己为目标。伤害随着精神强度而增长。
		你同时只能激活两种此类光环。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00336 | HUMAN-REVIEW | cross-batch-068 | confirmed | 改 `spiking` 措辞 |  |  |

<details><summary>hrq-00336 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`spiking` 译“发射射线”不准；confirmed：`daze`→“眩晕”与内部机制相符；confirmed：七参数与粗体标记一致
```
```
raw verdict: `spiking` 译“发射射线”不够准确→confirmed; `daze` 由 LIGHTNING_DAZE 实现，译“眩晕”与内部机制相符→confirmed; 五个 %0.1f、两个 %d、一个 50%% 与 tformat 七参数一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02141

- 位置：`mod-tome.lua:27826`（tome）｜section：`mod-tome/data/talents/psionic/psionic.lua`｜source_tag：`_t`
- 原文：`Nothing exists outside the minds ability to perceive it.`
- 现译：`没有任何事物能逃脱精神力量的感知。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00337 | HUMAN-REVIEW | cross-batch-068 | confirmed | 文风取舍 |  |  |

<details><summary>hrq-00337 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：意译造成语义重心变化
```
```
raw verdict: 译文确有意译造成的语义重心变化→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-068-01.md](reports/sol-068-01.md)。译文未修改。共 19 个 claim：16 confirmed、1 advisory、1 refuted、1 pending。 译文未修改。1 条 refuted、1 条 pending 原样转录。
```
</details>

## entry-02148

- 位置：`mod-tome.lua:27892`（tome）｜section：`mod-tome/data/talents/psionic/slumber.lua`｜source_tag：`tformat`
- 原文：`Enter a sleeping target's dreams for %d turns.  While in the Dreamscape, you'll encounter the target's invulnerable sleeping form as well as dream projections that it will spawn every other turn to defend its mind.
		Projections inflict 50%% less damage than the original, unless the target has Lucid Dreamer active.
		When the Dreamscape ends, for each projection destroyed, the target's life will be reduced by 10%% and it will be brainlocked for one turn.
		In the Dreamscape, your damage will be improved by %d%%.
		The damage bonus will improve with your Mindpower.`
- 现译：`进入某个睡眠状态目标的梦境中，持续 %d 回合。当你位于梦境空间中时，你将会遇到目标无敌的睡眠形态，每 2 回合它会制造出 1 个梦境守卫来保护它的心灵。
		除非目标激活了清晰梦境，否则梦境守卫造成的伤害比本体低 50%%。
		当梦境空间的效果结束时，你每摧毁一个梦境守卫，目标生命值会减少 10%%，并且受到持续 1 回合的思维封锁效果（可叠加）。
		在梦境空间中时，你的伤害会提高 %d%%。
		伤害增益受精神强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00338 | HUMAN-REVIEW | cross-batch-069 | confirmed | 统一为“梦境投影”；括号说明可留 |  |  |

<details><summary>hrq-00338 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`dream projection` 译“梦境守卫”，与实体名“梦境投影”及日志不一致；confirmed：占位符完整。advisory：“（可叠加）”是符合机制的解释性增补
```
```
raw verdict: `dream projection` 译“梦境守卫”，与实体名“梦境投影”及日志不一致→confirmed; “（可叠加）”是符合机制的解释性增补→advisory; 占位符完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02149

- 位置：`mod-tome.lua:27906`（tome）｜section：`mod-tome/data/talents/psionic/solipsism.lua`｜source_tag：`tformat`
- 原文：`You believe that your mind is the center of everything.  Permanently increases the amount of psi you gain per level by 5 and reduces your life rating (affects life at level up) by 50%% (one time only adjustment).
		You also have learned to overcome damage with your mind alone, and convert %d%% of all damage you receive into Psi damage and %d%% of your healing and life regen now recovers Psi instead of life.
		Converted Psi damage you take will be further reduced by %0.1f%% (%0.1f%% from character level with the remainder further reduced by %0.1f%% from talent level).
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		The first talent point also increases your solipsism threshold by 20%% (currently %d%%), reducing your global speed by 1%% for each percentage your current Psi falls below this threshold.`
- 现译：`你相信你的心灵是世间万物的中心。
		每级永久性增加你 5 点灵能值，并减少你 50%% 的生命成长（影响升级时的生命增益，但只在学习此技能时永久影响一次）
		同时你学会用心灵来承受伤害，转化 %d%% 生命削减为灵能值削减，并且 %d%% 的治疗值和回复值会转化为灵能值的增长。
		转化成的灵能值削减将进一步被减少 %0.1f%% （%0.1f%% 来自于人物等级，%0.1f%% 来自于技能等级。）
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能时，你的唯我临界点会增加 20 %%（当前 %d%%），你的灵能值每低于这个临界点 1 %%，你的所有速度减少 1 %%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00339 | HUMAN-REVIEW | cross-batch-069 | confirmed | 按源码补计算关系；增补数值待核 |  |  |

<details><summary>hrq-00339 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`global speed` 译“所有速度”；confirmed：遗漏“对剩余部分继续减伤”的连续计算；confirmed：“高于基础值10／低于10”属非原文增补；confirmed：占位符正确。pending：增补数值是否对应首次学习调整。advisory：第二行缺句号
```
```
raw verdict: `global speed` 译“所有速度”→confirmed; 遗漏“对剩余部分继续减伤”的连续计算关系→confirmed; “高于基础值10／低于10”属非原文增补→confirmed; 该增补中精确数值是否对应首次学习调整→pending; 占位符正确→confirmed; 第二行缺少句号→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02150

- 位置：`mod-tome.lua:27917`（tome）｜section：`mod-tome/data/talents/psionic/solipsism.lua`｜source_tag：`tformat`
- 原文：`You now substitute %d%% of your Mental Save for %d%% of your Physical and Spell Saves throws (so at 100%%, you would effectively use mental save for all saving throw rolls).
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		Learning this talent also increases your solipsism threshold by 10%% (currently %d%%).`
- 现译：`你现在使用 %d%% 精神豁免值来替代 %d%% 物理和法术豁免（即 100 %%时精神豁免完全替代所有豁免）。
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能也会增加你 10 %%唯我临界点（当前 %d%%）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00340 | HUMAN-REVIEW | cross-batch-069 | confirmed | 删空格；增补是否保留 |  |  |

<details><summary>hrq-00340 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：三占位符正确。advisory：基础值10及负体质反向影响增补；advisory：`100 %%`、`10 %%` 多余空格
```
```
raw verdict: 三个 `%d%%` 占位符正确→confirmed; 基础值10及负体质反向影响的增补→advisory; `100 %%`、`10 %%` 的多余空格→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02153

- 位置：`mod-tome.lua:27929`（tome）｜section：`mod-tome/data/talents/psionic/solipsism.lua`｜source_tag：`tformat`
- 原文：`Each time you take damage, you roll %d%% of your mental save against it.  A successful saving throw can crit and will reduce the damage by at least 50%%.
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		The first talent point also increases your solipsism threshold by 10%% (currently %d%%).`
- 现译：`每当你受到伤害时，你会使用 %d%% 精神豁免来鉴定。鉴定时精神豁免可能暴击，至少减少 50%% 的伤害。
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能也会增加你 10 %%唯我临界点（当前 %d%%）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00341 | HUMAN-REVIEW | cross-batch-069 | confirmed | 改“检定”；增补取舍 |  |  |

<details><summary>hrq-00341 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：占位符正确。advisory：“鉴定”应为“检定/判定”；advisory：基础值10增补
```
```
raw verdict: 占位符正确→confirmed; “鉴定”应为“检定/判定”→advisory; 基础值10的增补→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02181

- 位置：`mod-tome.lua:28344`（tome）｜section：`mod-tome/data/talents/spells/animus.lua`｜source_tag：`tformat`
- 原文：`You draw constant power from the souls you hold within your grasp.
		If you hold at least 2, your mana regeneration is increased by %0.1f per turn.
		If you hold at least 5, your spellpower is increased by %d.
		If you hold at least 8, all your resistances are increased by %d.`
- 现译：`你从掌握的灵魂中持续汲取力量，根据当前灵魂数量获得以下效果：
		2 个以上：你的每回合法力值恢复速度增加 %0.1f。
		5 个以上：你的法术强度增加 %d。
		8 个以上：你的全体伤害抗性增加 %d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00342 | HUMAN-REVIEW | cross-batch-069 | advisory | 是否统一数值格式 |  |  |

<details><summary>hrq-00342 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：给抗性数值补上 `%`
```
```
raw verdict: 译文给抗性数值补上 `%`→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02187

- 位置：`mod-tome.lua:28406`（tome）｜section：`mod-tome/data/talents/spells/conveyance.lua`｜source_tag：`tformat`
- 原文：`Teleports you randomly within a small range of up to %d grids.
		At level 4, it allows you to specify which creature to teleport.
		At level 5, it allows you to choose the target area (radius %d).
		If the target area is not in line of sight, there is a chance the spell will partially fail and teleport the target randomly.
		The range will increase with your Spellpower.`
- 现译：`在 %d 码范围内随机传送你自己。
		在等级 4 时，你可以传送指定生物（怪物或被护送者）。
		在等级 5 时，你可以选择传送位置（半径 %d）。
		如果目标位置不在你的视线里，则法术有可能失败，变为随机传送。
		影响范围受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00343 | HUMAN-REVIEW | cross-batch-069 | confirmed | 收窄或删除括注 |  |  |

<details><summary>hrq-00343 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两占位符正确；confirmed：“（怪物或被护送者）”属非原文增补且范围过窄
```
```
raw verdict: 两个 `%d` 占位符正确→confirmed; “（怪物或被护送者）”属非原文增补且范围过窄→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-069-01.md](reports/sol-069-01.md)。译文未修改。共 18 个 claim：10 confirmed、7 advisory、1 pending、0 refuted。 译文未修改。1 条 pending（增补数值来源）留主代理核对。
```
</details>

## entry-02189

- 位置：`mod-tome.lua:28417`（tome）｜section：`mod-tome/data/talents/spells/conveyance.lua`｜source_tag：`tformat`
- 原文：`Teleports you randomly within a large range (%d).
		At level 4, it allows you to specify which creature to teleport.
		At level 5, it allows you to choose the target area (radius %d).
		If the target area is not in line of sight, there is a chance the spell will partially fail and teleport the target randomly.
		Random teleports have a minimum range of %d.
		The range will increase with your Spellpower.`
- 现译：`在 %d 码范围内随机传送。
		在等级 4 时，你可以传送指定生物（怪物或被护送者）。
		在等级 5 时，你可以选择传送位置（半径 %d）。
		如果目标位置不在你的视线里，则法术有可能失败，变为随机传送。
		随机传送的最小半径为 %d。
		影响范围受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00344 | HUMAN-REVIEW | cross-batch-070 | confirmed | 删括注；最小半径质疑不采纳 |  |  |

<details><summary>hrq-00344 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：增译“（怪物或被护送者）”无据且缩窄可选目标。refuted：Gemini“minimum range 译最小半径不符合机制”的质疑不成立
```
```
raw verdict: 增译“（怪物或被护送者）”缺乏依据并缩窄可选目标→confirmed; “minimum range 译成最小半径不符合机制”这一质疑→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02191

- 位置：`mod-tome.lua:28437`（tome）｜section：`mod-tome/data/talents/spells/conveyance.lua`｜source_tag：`tformat`
- 原文：`When you hit a solid surface, this spell tears down the laws of probability to make you instantly appear on the other side.
		Teleports up to %d grids.
		After a successful probability travel you are left unstable, unable to do it again for a number of turns equal to %d%% of the number of tiles you blinked through.
		The range will improve with your Spellpower.`
- 现译：`当你击中一个固体表面时，此法术撕碎概率法则，令你瞬间出现在另一面。
		传送最大距离为 %d 码。
		成功穿越后，你会陷入不稳定状态，在相当于穿越码数 %d%% 的回合内无法再次穿越。
		传送距离受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00345 | HUMAN-REVIEW | cross-batch-070 | confirmed | 按语境重译触发条件 |  |  |

<details><summary>hrq-00345 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“当你击中一个固体表面时”字面直译造成触发方式偏差
```
```
raw verdict: “当你击中一个固体表面时”带字面直译造成的触发方式偏差→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02192

- 位置：`mod-tome.lua:28450`（tome）｜section：`mod-tome/data/talents/spells/death.lua`｜source_tag：`tformat`
- 原文：`Press your advantage when your foes are starting to crumble.
		For every detrimental effect on the target you deals %0.2f frostdusk damage (with diminishing returns) and reduce its global speed by 25%% for one turn per effect (up to a maximum of %d).
		The diminishing returns on damage bonus works this way:
		- 2 effects: %0.2f
		- 5 effects: %0.2f
		- 10 effects: %0.2f
		- 15 effects: %0.2f
		And so on...
		Damage increases with your Spellpower.
		`
- 现译：`利用敌人的痛楚打击敌人。
		目标每具有一个负面效果，造成 %0.2f 霜暮伤害（有收益衰减），并降低其全局速度 25%% 1回合（最大 %d 回合）。
		伤害加成的收益衰减如下面所示：
		- 2 个效果：%0.2f 伤害
		- 5 个效果：%0.2f 伤害
		- 10 个效果：%0.2f 伤害
		- 15 个效果：%0.2f 伤害
		以此类推。
		伤害受法术强度加成。
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00346 | HUMAN-REVIEW | cross-batch-070 | confirmed | 补 per effect 限定 |  |  |

<details><summary>hrq-00346 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译 `one turn per effect`，现译易被读成固定一回合
```
```
raw verdict: 漏译 `one turn per effect`，现译易被理解成固定持续一回合→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02207

- 位置：`mod-tome.lua:28713`（tome）｜section：`mod-tome/data/talents/spells/energy-alchemy.lua`｜source_tag：`tformat`
- 原文：`Infuse your body with lightning energy, bolstering your movement speed by +%d%%.
		Each turn, a foe within range %d will be struck by lightning and be dealt %0.1f Lightning damage.
		In addition, damage to your health will energize you.
		At the start of each turn in which you have lost at least %d life (20%% of your maximum life) since your last turn, you will gain %d%% of a turn.
		The effects increase with your Spellpower.`
- 现译：`将闪电能量填充到身体中，增加 %d%% 移动速度。
		每回合半径 %d 内的一个敌人将会被闪电击中，造成 %0.1f 点闪电伤害。
		另外，对你的伤害会激活你。
		每次你的回合开始时，如果自上个回合以来你损失了至少 %d 点生命（20%% 最大生命值），你将获得 %d%% 个额外回合。
		上述效果均随法术强度提升。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00347 | HUMAN-REVIEW | cross-batch-070 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00347 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“获得 %d%% 个额外回合”数值关系保留但不精确自然
```
```
raw verdict: “获得 %d%% 个额外回合”大致保留数值但不够精确自然→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02210

- 位置：`mod-tome.lua:28797`（tome）｜section：`mod-tome/data/talents/spells/explosives.lua`｜source_tag：`tformat`
- 原文：`Grants %d%% protection to you, your golem and other friendly creatures against the elemental damage of your own bombs, and against external elemental damage (fire, cold, lightning and acid) by %d%%.
		At talent level 5 it also protects against all side effects of your bombs.`
- 现译：`提高你、你的傀儡和其他友好生物对自己炸弹 %d%% 的元素伤害抗性，并增加 %d%% 对外界元素伤害（火焰、寒冷、闪电和酸性）的抗性。
		在技能等级 5 时它同时会保护你免疫你的炸弹所带来的特殊效果。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00348 | HUMAN-REVIEW | cross-batch-070 | confirmed | 补保护对象；引用不入证据链 |  |  |

<details><summary>hrq-00348 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二句只写“保护你”，遗漏傀儡与其他友方。refuted：Gemini 所称源码五级判定 `target ~= self and target ~= golem` 不实（该引用不能作证据）
```
```
raw verdict: 第二句只写“保护你”，遗漏傀儡与其他友方生物→confirmed; Gemini 所称源码存在 `target ~= self and target ~= golem` 五级判定→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02212

- 位置：`mod-tome.lua:28848`（tome）｜section：`mod-tome/data/talents/spells/fire.lua`｜source_tag：`talent name`
- 原文：`Flame`
- 现译：`火焰`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00349 | HUMAN-REVIEW | cross-batch-070 | confirmed | 按术语改 |  |  |

<details><summary>hrq-00349 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：技能名「Flame」与术语快照冲突（应为“火球术”）
```
```
raw verdict: 技能名「Flame」与冻结术语快照冲突（应为“火球术”）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02227

- 位置：`mod-tome.lua:29143`（tome）｜section：`mod-tome/data/talents/spells/master-necromancer.lua`｜source_tag：`tformat`
- 原文：`Sends out a surge of undeath energies into your aura.
		All minions inside gain 25%% speed for %d turns
		All non-ghoul minions are healed by %d%%.
		If you know Call of the Mausoleum, the time remaining to the next free ghoul is reduced by %d.
		if you know Corpse Explosion or Putrescent Liquefaction the duration of those effects are increased by %d.
		All non-undead foes caught inside are dazed for %d turns.
		In addition all your minions (created after you learn this spell) have a passive health regeneration.`
- 现译：`在你的光环中放出一股不死能量。
		范围内所有随从获得 25%% 速度，持续 %d 回合。
		所有非食尸鬼的随从被治疗 %d%%。
		如果你掌握陵墓召唤技能，到下一个免费食尸鬼的时间降低 %d。
		如果你掌握夺命尸爆或腐烂液化技能，这些效果的持续时间延长 %d。
		范围内所有非不死生物的敌人都会被茫然 %d 回合。
		此外，你的所有随从（在学会该法术后制造的）获得额外被动生命回复。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00350 | HUMAN-REVIEW | cross-batch-070 | confirmed | 按术语改 |  |  |

<details><summary>hrq-00350 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`dazed` 译“茫然”与术语及效果身份冲突（应为“眩晕”）
```
```
raw verdict: `dazed` 译“茫然”与冻结术语及实际效果身份冲突（应为“眩晕”）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-070-01.md](reports/sol-070-01.md)。译文未修改。共 9 个 claim：6 confirmed、2 refuted、1 advisory、0 pending（与 Sol 自身汇总一致）。 译文未修改。2 条 refuted 中有 1 条是 Gemini 源码引用不实，原样转录并标注不可引用。
```
</details>

## entry-02252

- 位置：`mod-tome.lua:29537`（tome）｜section：`mod-tome/data/talents/spells/spells.lua`｜source_tag：`_t`
- 原文：`Harness the power of the storm to incinerate your foes.`
- 现译：`使用风暴的力量打击你的目标。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00351 | HUMAN-REVIEW | cross-batch-071 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00351 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（条目结论成立，完整措辞见报告）
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-071-01.md](reports/sol-071-01.md)。译文未修改。共 7 个 claim：6 confirmed、1 advisory、0 refuted/pending。 译文未修改。Sol 主动补充的 `and→或者` 属新增交叉发现，原样转录。
```
</details>

## entry-02258

- 位置：`mod-tome.lua:29549`（tome）｜section：`mod-tome/data/talents/spells/spells.lua`｜source_tag：`_t`
- 原文：`Conveyance is the school of travel. It allows you to travel faster and to track others.`
- 现译：`学习传送，使你能更快的旅行或者追踪目标。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00352 | HUMAN-REVIEW | cross-batch-071 | confirmed | **优先处理连接词**（and→或），再润色的/地 |  |  |

<details><summary>hrq-00352 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“更快的旅行”应为“更快地旅行”；confirmed（Sol 补充发现）：原文 `and` 并列被译成“或者”，使“更快旅行/追踪他人”看似互斥
```
```
raw verdict: “更快的旅行”应为“更快地旅行”（动词结构）→confirmed; 原文 `and` 并列被译成“或者”，使两项能力看似互斥（Sol 交叉补充发现）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-071-01.md](reports/sol-071-01.md)。译文未修改。共 7 个 claim：6 confirmed、1 advisory、0 refuted/pending。 译文未修改。Sol 主动补充的 `and→或者` 属新增交叉发现，原样转录。
```
</details>

## entry-02259

- 位置：`mod-tome.lua:29551`（tome）｜section：`mod-tome/data/talents/spells/spells.lua`｜source_tag：`_t`
- 原文：`Divination allows the caster to sense its surroundings, and find hidden things.`
- 现译：`侦查技能可以使施放者能侦查周围环境，搜寻隐藏的东西。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00353 | HUMAN-REVIEW | cross-batch-071 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00353 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed（条目结论成立）
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-071-01.md](reports/sol-071-01.md)。译文未修改。共 7 个 claim：6 confirmed、1 advisory、0 refuted/pending。 译文未修改。Sol 主动补充的 `and→或者` 属新增交叉发现，原样转录。
```
</details>

## entry-02265

- 位置：`mod-tome.lua:29638`（tome）｜section：`mod-tome/data/talents/spells/staff-combat.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Blunt Thrust without a staff weapon!`
- 现译：`你需要一把法杖来施展该技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00354 | HUMAN-REVIEW | cross-batch-071 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00354 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory（排版/风格）
```
```
raw verdict: 条目结论属排版/风格（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-071-01.md](reports/sol-071-01.md)。译文未修改。共 7 个 claim：6 confirmed、1 advisory、0 refuted/pending。 译文未修改。Sol 主动补充的 `and→或者` 属新增交叉发现，原样转录。
```
</details>

## entry-02267

- 位置：`mod-tome.lua:29640`（tome）｜section：`mod-tome/data/talents/spells/staff-combat.lua`｜source_tag：`tformat`
- 原文：`Hit a target for %d%% melee damage and stun it for %d turns.
		Stun chance will improve with Spellpower.
		At level 5, this attack cannot miss.`
- 现译：`挥动法杖对目标造成 %d%% 近程伤害并震慑目标 %d 回合。
		震慑概率受法术强度加成
		在等级 5 时，此攻击必中。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00355 | HUMAN-REVIEW | cross-batch-071 | confirmed | 补句号；改“近战伤害” |  |  |

<details><summary>hrq-00355 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：第二行缺句号；confirmed：`melee damage` 应为“近战伤害”（源码 `is_melee=true`），现译“近程伤害”不准
```
```
raw verdict: 第二行缺少句号→confirmed; `melee damage` 译“近程伤害”不准确，应为“近战伤害”（is_melee=true）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-071-01.md](reports/sol-071-01.md)。译文未修改。共 7 个 claim：6 confirmed、1 advisory、0 refuted/pending。 译文未修改。Sol 主动补充的 `and→或者` 属新增交叉发现，原样转录。
```
</details>

## entry-02269

- 位置：`mod-tome.lua:29662`（tome）｜section：`mod-tome/data/talents/spells/stone-alchemy.lua`｜source_tag：`logPlayer`
- 原文：`You imbue your %s with %s.`
- 现译：`你在 %s 上安装了 %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00356 | HUMAN-REVIEW | cross-batch-072 | confirmed | 统一“附魔”或“镶嵌” |  |  |

<details><summary>hrq-00356 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两 `%s` 含义顺序正确。advisory：“安装”与同技能“附魔”不一致（快照无 Imbue 条目）
```
```
raw verdict: 两个 `%s` 含义和顺序正确→confirmed; “安装”与同技能“附魔”不一致（术语快照无 Imbue 条目）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02273

- 位置：`mod-tome.lua:29694`（tome）｜section：`mod-tome/data/talents/spells/stone.lua`｜source_tag：`tformat`
- 原文：`You root yourself into the earth, and transform your flesh into stone.  While this spell is sustained, you may not move, and any forced movement will end the effect.
		Your stone form and your affinity with the earth while the spell is active has the following effects:
		* Reduces the cooldown of Earthen Missiles, Pulverizing Auger, Earthquake, and Mudslide by %d%%.
		* Grants %d%% Fire Resistance, %d%% Lightning Resistance, %d%% Acid Resistance, and %d%% Stun Resistance.
		Resistances scale with your Spellpower.`
- 现译：`你将自己扎根于土壤并使你的肉体融入石头。
		当此技能被激活时你不能移动并且任何移动会打断此技能效果。
		当此技能激活时，受你的石化形态和土壤相关影响，会产生以下效果：
		* 减少岩石飞弹、粉碎钻击、地震和山崩地裂冷却时间回合数：%d%%
		* 获得 %d%% 火焰抗性，%d%% 闪电抗性，%d%% 酸性抗性和 %d%% 震慑抵抗。
		受法术强度影响，抗性按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00357 | HUMAN-REVIEW | cross-batch-072 | confirmed | 位移句按英文保留“强制位移”或按源码改写；不要采用 Gemini 解释 |  |  |

<details><summary>hrq-00357 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`affinity with the earth` 译“土壤相关影响”丢亲和义；confirmed：`forced movement` 泛化丢“强制”；confirmed：冷却“回合数：%d%%”语义错；confirmed：五 `%d%%` 顺序正确。advisory：新增换行。refuted：Gemini“击退/传送会结束技能”机制结论**不成立**（`never_move` 无解除回调）
```
```
raw verdict: 新增换行属实（仅排版）→advisory; `affinity with the earth` 译“土壤相关影响”丢失亲和含义→confirmed; `forced movement` 被泛化成“任何移动”，缺“强制”限定→confirmed; Gemini“击退、传送等强制位移会结束技能”的机制结论→refuted; “减少……冷却时间回合数：%d%%”语义有误（实为百分比冷却缩减）→confirmed; 五个 `%d%%` 顺序正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02277

- 位置：`mod-tome.lua:29743`（tome）｜section：`mod-tome/data/talents/spells/temporal.lua`｜source_tag：`tformat`
- 原文：`This intricate spell instantly erects a time shield around the caster, preventing any incoming damage and sending it forward in time.
		Once either the maximum damage (%d) is absorbed, or the time runs out (%d turns), the stored damage will return as a temporal restoration field over time (5 turns).
		Each turn the restoration field is active, you get healed for 10%% of the absorbed damage (Aegis Shielding talent affects the percentage).
		The shield's max absorption will increase with your Spellpower.`
- 现译：`这个复杂的法术在施法者周围立刻制造一个时间屏障，吸收你受到的伤害。
		一旦达到最大伤害吸收值（%d）或持续时间（%d 回合）结束，存储的能量会治疗你，持续 5 回合，每回合回复总吸收伤害的 10%%（强化护盾技能会影响该系数）。
		最大吸收值受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00358 | HUMAN-REVIEW | cross-batch-072 | confirmed | 按快照统一“时间盾”；决定是否恢复完整时空概念 |  |  |

<details><summary>hrq-00358 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：省略“送往未来/时间回复力场”；confirmed：“时间屏障”违反快照（Time Shield→时间盾）；confirmed：数值关系正确。advisory：中间两段合并
```
```
raw verdict: 原文四段被合并中间两段→advisory; 省略“将伤害送往未来”与“时间回复力场”两个概念→confirmed; “时间屏障”与冻结术语快照不一致（Time Shield → 时间盾）→confirmed; 两个 `%d` 与 `10%%` 数值关系正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02278

- 位置：`mod-tome.lua:29750`（tome）｜section：`mod-tome/data/talents/spells/temporal.lua`｜source_tag：`tformat`
- 原文：`Removes the target from the flow of time for %d turns. In this state, the target can neither act nor be harmed.
		Time does not pass at all for the target, no talents will cooldown, no resources will regen, and so forth.
		The duration will increase with your Spellpower.`
- 现译：`将目标从时光的流动中移出，持续 %d 回合。
		在此状态下，目标不能动作也不能被伤害。
		对于目标来说，时间是静止的，技能无法冷却，也没有能量回复……
		持续时间受法术强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00359 | HUMAN-REVIEW | cross-batch-072 | confirmed | 无必办 |  |  |

<details><summary>hrq-00359 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：机制表述正确；confirmed：唯一 `%d` 正确。advisory：多一处换行
```
```
raw verdict: 两句被拆成两段（多一处换行）→advisory; 机制表述正确（invulnerable/time_prison/no_timeflow）→confirmed; 唯一 `%d` 保留正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02280

- 位置：`mod-tome.lua:29790`（tome）｜section：`mod-tome/data/talents/spells/thaumaturgy.lua`｜source_tag：`tformat`
- 原文：`By weaving arcane triggers around you feet you can use the residual energies of your beam spells for free movement.
		Each time you cast a beam spell you can move right afterwards without spending a turn.
		This spell has %d charges. Once all charges are spent it unsustains.
		If you exit combat with some charges left it will after 10 turn regenerates its charges, if you have enough mana.`
- 现译：`你将奥术力量编织于双脚，可以使用射线类法术来进行免费移动。
		每当你释放一个射线类法术，你可以立刻移动一次，不需要消耗时间。
		这一法术有 %d 次充能。当充能耗尽时，这一法术将会解除持续。
		若你在尚有剩余充能时脱离战斗，则在脱离战斗 10 回合后，只要法力充足便会消耗法力补满充能，否则解除持续。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00360 | HUMAN-REVIEW | cross-batch-072 | confirmed | 是否补“残余能量”属风味 |  |  |

<details><summary>hrq-00360 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：补写的“消耗法力补满充能否则解除”有直接源码依据；confirmed：`%d` 与段落正确。advisory：省略 `residual energies`
```
```
raw verdict: 补充“消耗法力补满充能，否则解除持续”有直接源码依据→confirmed; 首句省略 `residual energies` 意象→advisory; `%d` 及段落结构正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02290

- 位置：`mod-tome.lua:29932`（tome）｜section：`mod-tome/data/talents/techniques/2hweapon.lua`｜source_tag：`tformat`
- 原文：`You enter an aggressive battle stance, increasing Accuracy by %d and Physical Power by %d, at the cost of -10 Defense and -10 Armour.
		While berserking, you are nearly unstoppable, granting you %d%% stun and pinning resistance.
		The Accuracy bonus increases with your Dexterity, and the Physical Power bonus with your Strength.`
- 现译：`进入狂暴的战斗状态，以减少 10 点闪避和 10 点护甲的代价增加 %d 点命中和 %d 点物理强度。
		开启狂暴时你无人能挡，增加 %d%% 震慑和定身抵抗。
		命中受敏捷值加成；
		物理强度受力量值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00361 | HUMAN-REVIEW | cross-batch-072 | confirmed | 仅格式 |  |  |

<details><summary>hrq-00361 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：三占位符顺序与全部属性修正覆盖准确。advisory：末句拆两行
```
```
raw verdict: 末句被拆为两行→advisory; 三个占位符顺序正确且覆盖全部属性修正→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02303

- 位置：`mod-tome.lua:30008`（tome）｜section：`mod-tome/data/talents/techniques/acrobatics.lua`｜source_tag：`tformat`
- 原文：`You gain greater facility with your acrobatic moves, lowering the cooldowns of Vault, Tumble, and Trained Reactions by %d, and their stamina costs by %0.1f.
		At Rank 3 you also gain 10%% global speed for 1 turn after Trained Reactions activates. At rank 5 this speed bonus improves to 20%% and lasts for 2 turns.`
- 现译：`你使用杂耍系技能更加得心应手，降低撑杆跳、翻滚和受训反应的冷却时间 %d 回合，降低技能的体力消耗 %0.1f。
		在等级 3 时，每当受训反应触发，你获得 10%% 的全局速度 1 回合。
		在等级 5 时，速度加成变为 20%%，持续 2 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00362 | HUMAN-REVIEW | cross-batch-072 | confirmed | 统一“翻筋斗” |  |  |

<details><summary>hrq-00362 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Tumble` 应按快照为“翻筋斗”；confirmed：`%d` 等保留正确。advisory：等级3/5 拆段
```
```
raw verdict: `Tumble` 译“翻滚”与术语快照“翻筋斗”不一致→confirmed; 等级3/5 效果被拆成两段→advisory; `%d`、`%0.1f`、`10%%`、`20%%` 保留正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02306

- 位置：`mod-tome.lua:30039`（tome）｜section：`mod-tome/data/talents/techniques/agility.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Rapid Fire without a bow or sling!`
- 现译：`你需要一把弓或者投石索来施放这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00363 | HUMAN-REVIEW | cross-batch-072 | confirmed | 改为“需要装备投石索”；技能名不用 `Rapid Fire` |  |  |

<details><summary>hrq-00363 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：英文报错 `Rapid Fire` 与实际技能名 `Rapid Shot` 不一致，译文“这个技能”避开错误名。refuted：Gemini“准确传达武器限制”**不成立**——有效前置是投石索（`archerPreUse(...,"sling")`）
```
```
raw verdict: 英文报错 `Rapid Fire` 与实际技能名 `Rapid Shot` 不一致，译文用“这个技能”避开了错误名→confirmed; Gemini 称译文“准确传达武器限制”与实际执行门禁不符（需投石索）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-072-01.md](reports/sol-072-01.md)。译文未修改。共 25 个 claim：16 confirmed、7 advisory、2 refuted、0 pending。Sol 自述口径：confirmed=有文本/源码支持，refuted=与源码冲突，advisory=现象存在但仅风格/排版。 译文未修改。2 条 refuted 均是对 Gemini 机制推断的下修，原样转录。
```
</details>

## entry-02312

- 位置：`mod-tome.lua:30077`（tome）｜section：`mod-tome/data/talents/techniques/archery.lua`｜source_tag：`tformat`
- 原文：`Fire a precise shot dealing %d%% weapon damage, with 100 increased accuracy. This shot will bypass other enemies between you and your target.
Only usable against marked targets, and consumes the mark on hit.`
- 现译：`瞄准目标头部发射穿透性弹药，造成 %d%% 武器伤害。
此次攻击额外获得 100 命中，且能穿透目标以外单位。
只能对被标记的单位使用，命中时消耗该标记。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00364 | HUMAN-REVIEW | cross-batch-073 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00364 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02319

- 位置：`mod-tome.lua:30115`（tome）｜section：`mod-tome/data/talents/techniques/assassination.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Coup de Grace without dual wielding!`
- 现译：`你需要双持武器来施展这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00365 | HUMAN-REVIEW | cross-batch-073 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00365 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：风格/排版
```
```
raw verdict: 条目结论属风格/排版（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02326

- 位置：`mod-tome.lua:30194`（tome）｜section：`mod-tome/data/talents/techniques/bloodthirst.lua`｜source_tag：`tformat`
- 原文：`You delight in the inflicting of wounds, providing %d physical power.
		In addition when you make a creature bleed its physical damage resistance is reduced by %d%% (but never below 0%%).
		Physical power depends on your Strength stat.`
- 现译：`你沉醉于撕裂伤口的兴奋中，增加 %d 物理强度。
		同时，每次你让敌人流血时，它的物理抗性下降 %d%% （但不会小于 0%%）
		物理强度加成受力量影响。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00366 | HUMAN-REVIEW | cross-batch-073 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00366 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02327

- 位置：`mod-tome.lua:30200`（tome）｜section：`mod-tome/data/talents/techniques/bloodthirst.lua`｜source_tag：`tformat`
- 原文：`You enter a battle frenzy for %d turns. During that time, you can not use items, healing has no effect, and your health cannot drop below 1.
		At the end of the frenzy, you regain %d%% of your health per foe slain during the frenzy.
		While Unstoppable is active, Berserker Rage critical bonus is disabled as you lose the thrill of the risk of death.`
- 现译：`你进入疯狂战斗状态 %d 回合。
		在这段时间内你不能使用物品，并且治疗无效，此时你的生命值无法低于 1 点。
		状态期间你每杀死一个敌人，都会在状态结束时回复 %d%% 最大生命值。
		当进入无双状态时，由于你失去了死亡的威胁，狂战之怒不能提供暴击加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00367 | HUMAN-REVIEW | cross-batch-073 | pending | 主代理按术语库核对后再定 |  |  |

<details><summary>hrq-00367 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**pending**：主张证据不足，需冻结术语/源码佐证
```
```
raw verdict: 条目主张证据不足（pending）→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02337

- 位置：`mod-tome.lua:30288`（tome）｜section：`mod-tome/data/talents/techniques/combat-training.lua`｜source_tag：`tformat`
- 原文：`You become better at using your armour to deflect blows and protect your vital areas. Increases Armour value by %d, Armour hardiness by %d%%, and reduces the chance melee or ranged attacks critically hit you by %d%% with your current body armour.
		(This talent only provides bonuses for heavy mail or massive plate armour.)
		At level 1, it allows you to wear heavy mail armour, gauntlets, helms, and heavy boots.
		At level 2, it allows you to wear shields.
		At level 3, it allows you to wear massive plate armour.
		%s`
- 现译：`你使用防具来偏转攻击和保护重要部位的能力加强了。
		根据现有防具，提高 %d 护甲值和 %d%% 护甲强度，并减少 %d%% 近战和远程攻击的暴击几率。
		（这项技能只对重甲或板甲提供加成。）
		在等级 1 时，能使你装备锁甲、金属手套、头盔和重靴。
		在等级 2 时，能使你装备盾牌。
		在等级 3 时，能使你装备板甲。
		%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00368 | HUMAN-REVIEW | cross-batch-073 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00368 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02343

- 位置：`mod-tome.lua:30369`（tome）｜section：`mod-tome/data/talents/techniques/dualweapon.lua`｜source_tag：`logPlayer`
- 原文：`You must dual wield to manage contact with your target!`
- 现译：`你只有在双持状态下才能使用这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00369 | HUMAN-REVIEW | cross-batch-073 entry-02343… | advisory | 统一由编辑决定 |  |  |

<details><summary>hrq-00369 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：均属风格/排版
```
```
raw verdict: 条目结论属风格/排版（advisory）→advisory; 条目结论属风格/排版（advisory）→advisory; 条目结论属风格/排版（advisory）→advisory; 条目结论属风格/排版（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02345

- 位置：`mod-tome.lua:30379`（tome）｜section：`mod-tome/data/talents/techniques/dualweapon.lua`｜source_tag：`tformat`
- 原文：`With a quick shift of your momentum, you execute a surprise unarmed strike in place of your normal offhand attack.
		This allows you to attack with your mainhand weapon for %d%% damage and unarmed for %d%% damage.  If the unarmed attack hits, the target is confused (%d%% power) for %d turns.
		The chance to confuse increases with your Accuracy.`
- 现译：`你迅速移动，用徒手攻击敌人。
		造成 %d%% 主手武器伤害，%d%% 徒手伤害。
		若徒手攻击命中，敌人将被混乱（%d%% 强度）%d 回合。
		混乱几率受命中加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00370 | HUMAN-REVIEW | cross-batch-073 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00370 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-073-01.md](reports/sol-073-01.md)。译文未修改。共 10 个 claim（每条目一 claim）：4 confirmed、5 advisory、1 pending、0 refuted；与 Sol 自身汇总一致。 译文未修改。完整 claim 措辞以报告为准，STATE 记录为逐条目 verdict 摘要。
```
</details>

## entry-02352

- 位置：`mod-tome.lua:30431`（tome）｜section：`mod-tome/data/talents/techniques/duelist.lua`｜source_tag：`logPlayer`
- 原文：`You cannot use Lunge without dual wielding!`
- 现译：`你需要双持武器来施展这个技能！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00371 | HUMAN-REVIEW | cross-batch-074 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00371 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory（风格/排版）
```
```
raw verdict: 条目结论属风格/排版（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02354

- 位置：`mod-tome.lua:30444`（tome）｜section：`mod-tome/data/talents/techniques/excellence.lua`｜source_tag：`tformat`
- 原文：`Your reflexes are lightning-fast, if you spot a projectile (arrow, shot, spell, ...) you can instantly shoot at it without taking a turn to take it down.
		You can shoot down up to %d projectiles.`
- 现译：`你的反射神经像闪电一样快。当你瞄准抛射物（箭矢、弹药、法术等）时，你能马上击落它而不消耗时间。
		你最多能击落 %d 个目标。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00372 | HUMAN-REVIEW | cross-batch-074 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00372 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02356

- 位置：`mod-tome.lua:30456`（tome）｜section：`mod-tome/data/talents/techniques/excellence.lua`｜source_tag：`tformat`
- 原文：`Activating this talent enhances your reflexes to incredible levels.  Each time you are attacked in melee, you have a %d%% chance get a defensive shot off in time to intercept the attack, fully disrupting it (including extra blows from certain talents), dealing %d%% archery damage, and knocking the attacker back %d tiles.
		Activating this talent will not interrupt reloading.`
- 现译：`激活该技能会大幅强化你的反射神经。每次你受到近战攻击，你有 %d%% 的几率及时进行一次防御性射击来拦截并完全瓦解对方这次攻击（包括某些技能带来的额外打击），造成 %d%% 射击伤害，同时击退对方 %d 码。激活这项技能不会中断装填弹药。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00373 | HUMAN-REVIEW | cross-batch-074 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00373 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02360

- 位置：`mod-tome.lua:30524`（tome）｜section：`mod-tome/data/talents/techniques/grappling.lua`｜source_tag：`tformat`
- 原文：`Enhances your grapples with additional effects. All additional effects will apply to every grapple with no additional save or resist check.
		#RED#Talent Level 1:  Reduces physical power by %d
		Talent Level 3:  Silences
		Talent Level 5:  Reduces global action speed by %d%%`
- 现译：`增强你的抓取，获得额外效果，所有效果不需通过其他豁免或抵抗鉴定。
		#RED# 等级 1：减少 %d 物理强度
		等级 3：沉默
		等级 5：目标减速 %d%%`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00374 | HUMAN-REVIEW | cross-batch-074 | confirmed | 补机制限定；术语核对 |  |  |

<details><summary>hrq-00374 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏“全局行动速度”机制限定；confirmed：`#RED#` 后多空格。pending：术语是否规范为“全局速度”
```
```
raw verdict: 译文遗漏“全局行动速度”这一机制限定→confirmed; 术语规范为“全局速度”→pending; `#RED#` 后多一个空格→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02380

- 位置：`mod-tome.lua:30682`（tome）｜section：`mod-tome/data/talents/techniques/munitions.lua`｜source_tag：`tformat`
- 原文：`Fires a special shot based on your currently loaded ammo:
Incendiary - Fire a shot that deals %d%% weapon damage as fire and covers targets in radius %d in sticky pitch for %d turns, reducing global speed by %d%% and increasing fire damage taken by %d%%.
Venomous - Fire a shot that deals %d%% weapon damage as nature and explodes into a radius %d cloud of crippling poison for %d turns, dealing %0.2f nature damage each turn and giving affected targets a %d%% chance to fail talent usage.
Piercing - Fire a shot that explodes into a radius %d burst of shredding shrapnel, dealing %d%% weapon damage as physical and removing %d beneficial physical effects or sustains.
The poison damage dealt increases with your Physical Power, and status chance increases with your Accuracy.`
- 现译：`根据当前装填的弹药进行一次特殊的射击
燃烧弹- %d%% 火焰武器伤害。在半径 %d 码范围内用粘稠的沥青包裹敌人 %d 回合，减少 %d%% 全局速度并增加其受到的火焰伤害 %d%%。
剧毒弹- %d%% 自然武器伤害。爆炸会形成半径 %d 的致残毒气云，持续 %d 回合，每回合造成 %0.2f 自然伤害并使目标使用技能有 %d%% 几率失败。
穿甲弹- 在半径 %d 码范围内爆炸，造成 %d%% 物理武器伤害，并移除 %d 个有益的物理效果或持续技能。
毒素伤害受物理强度加成，状态触发几率受命中加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00375 | HUMAN-REVIEW | cross-batch-074 | advisory | 文风取舍 |  |  |

<details><summary>hrq-00375 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory（风格/排版）
```
```
raw verdict: 条目结论属风格/排版（advisory）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02381

- 位置：`mod-tome.lua:30692`（tome）｜section：`mod-tome/data/talents/techniques/munitions.lua`｜source_tag：`tformat`
- 原文：`You create enhanced versions of your ammunition, granting them additional effects.
Incendiary - The explosion radius is increased by 1, and the ground beneath is ignited dealing an additional %0.2f fire damage each turn for 3 turns.
Venomous - Inflicts leeching poison, dealing %0.2f nature damage over 3 turns and causing you to heal for 100%% of all damage the poison deals to the target.
Piercing - Punctures the target’s armor, increasing all damage they take by %d%% for 3 turns.
You only have a limited amount of this ammo, causing this talent to have a cooldown.
The damage dealt will increase with your Physical Power, and status chance increases with your Accuracy.`
- 现译：`你制造出强化版弹药，获得额外效果：
燃烧弹- 爆炸范围增加 1, 点燃地面每回合额外造成 %0.2f 火焰伤害持续 3 回合。
剧毒弹- 感染吸血毒素，3 回合内造成 %0.2f 毒素伤害，毒素造成的 100%% 伤害会治疗你。
穿甲弹- 击穿目标护甲，目标受到的所有伤害增加 %d%% 持续 3 回合。
你的强化版弹药有限，所以技能有冷却时间。
伤害受物理强度加成，状态触发几率受命中加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00376 | HUMAN-REVIEW | cross-batch-074 | confirmed | 按原报告修 |  |  |

<details><summary>hrq-00376 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：条目结论成立
```
```
raw verdict: 条目结论成立（confirmed）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-074-01.md](reports/sol-074-01.md)。译文未修改。共 8 个 claim：4 confirmed、3 advisory、1 pending、0 refuted。 译文未修改。单 claim 条目在 STATE 中以 verdict 摘要记录，完整措辞以报告为准。
```
</details>

## entry-02391

- 位置：`mod-tome.lua:30811`（tome）｜section：`mod-tome/data/talents/techniques/sniper.lua`｜source_tag：`logPlayer`
- 原文：`You are being observed too closely to enter Concealment!`
- 现译：`你被近距离观察，不能进入 隐匿 状态！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00377 | HUMAN-REVIEW | cross-batch-075 | confirmed | 排版取舍 |  |  |

<details><summary>hrq-00377 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“隐匿”两侧多余空格（排版）
```
```
raw verdict: “隐匿”两侧多余空格（排版）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02392

- 位置：`mod-tome.lua:30812`（tome）｜section：`mod-tome/data/talents/techniques/sniper.lua`｜source_tag：`tformat`
- 原文：`Enter a concealed sniping stance, increasing your weapon's attack range and vision range by %d, giving all incoming damage a %d%% chance to miss you, and causing your Headshot, Volley and Called Shots to behave as if the target was marked.
Any non-instant, non-movement action will break concealment, but the increased range and vision and damage avoidance will persist for 3 turns, with the damage avoidance decreasing in power by 33%% each turn.
This requires a bow to use, and cannot be used if there are foes in sight within range %d.`
- 现译：`进入隐匿的狙击状态，增加武器攻击范围和视野 %d 格，所有受到的伤害有 %d%% 几率被完全抵消，爆头、齐射和精巧射击视为目标已被标记。
所有非瞬时非移动行为将打破隐匿状态，攻击范围与视野的加成和伤害回避效果将额外持续 3 回合，伤害回避效果每回合减少 33%%。
该技能需要弓来使用；如果视野内 %d 格范围内有敌人，则不能使用。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00378 | HUMAN-REVIEW | cross-batch-075 | confirmed | 局部对齐 |  |  |

<details><summary>hrq-00378 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：Called Shots→“精巧射击”与正式译名“精准射击”不一致
```
```
raw verdict: Called Shots 译为“精巧射击”，与正式译名“精准射击”不一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02393

- 位置：`mod-tome.lua:30818`（tome）｜section：`mod-tome/data/talents/techniques/sniper.lua`｜source_tag：`tformat`
- 原文：`Fire an arrow tipped with a smoke bomb inflicting %d%% damage and creating a radius %d cloud of thick, disorientating smoke. Those caught within will have their vision range reduced by %d for 5 turns.
The distraction caused by this effect reduces the cooldown of your Concealment by %d turns. If the cooldown is reduced to 0, you instantly activate Concealment regardless of whether foes are too close.
The chance for the smoke bomb to affect your targets increases with your Accuracy. This requires a bow to use.`
- 现译：`发射一个带着烟雾弹的箭头造成 %d%% 伤害并制造一个半径为 %d 的烟雾。被困在内的人将减少视野 %d 格 5 回合。
此效果将减少你隐匿技能 %d 回合冷却时间。如果冷却时间减到 0, 无论敌人是否太近，都可立即激活隐匿。
烟雾弹影响目标的几率受命中值加成。该技能需要弓来使用。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00379 | HUMAN-REVIEW | cross-batch-075 | confirmed | 标点直修；完整性取舍 |  |  |

<details><summary>hrq-00379 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：半角标点 `0, `；confirmed：省略 `thick, disorientating smoke` 修饰；advisory：“带着烟雾弹的箭头”生硬
```
```
raw verdict: 半角标点 `0, ` 与中文正文不一致→confirmed; `thick, disorientating smoke` 压缩为“烟雾”，省略修饰（轻微完整性损失）→confirmed; “带着烟雾弹的箭头”略生硬→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02394

- 位置：`mod-tome.lua:30824`（tome）｜section：`mod-tome/data/talents/techniques/sniper.lua`｜source_tag：`tformat`
- 原文：`Enter a calm, focused stance, increasing physical power and accuracy by %d, projectile speed by %d%% and the chance to mark targets by an additional %d%%.
This makes your shots more effective at range, increasing all damage dealt by %0.1f%% per tile travelled beyond 3, to a maximum of %0.1f%% damage at range 8.
The physical power and accuracy increase with your Dexterity. This requires a bow to use.`
- 现译：`进入一个平静，专注的姿态，增加 %d 物理强度和命中，抛射物速度增加 %d%% 并且标记目标的几率增加 %d%%。
这让你在射程内射击更有效：对三格外目标的距离每增加一格，伤害增加 %0.1f%%，8 格距离时达到最大值（%0.1f%%）。
物理强度和命中受敏捷值加成。该技能需要弓来使用。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00380 | HUMAN-REVIEW | cross-batch-075 | confirmed | 改写措辞 |  |  |

<details><summary>hrq-00380 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`at range` 误写“在射程内”
```
```
raw verdict: `at range` 误写成“在射程内”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02399

- 位置：`mod-tome.lua:30844`（tome）｜section：`mod-tome/data/talents/techniques/strength-of-the-berserker.lua`｜source_tag：`tformat`
- 原文：`Shout your warcry in a frontal cone of radius %d. Any targets caught inside will be confused (50%% confusion power) for %d turns.`
- 现译：`在你的正前方大吼形成 %d 码半径的扇形战争怒吼。任何在其中的目标会被混乱（50%%强度）%d 回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00381 | HUMAN-REVIEW | cross-batch-075 | advisory | 术语清晰度 |  |  |

<details><summary>hrq-00381 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：括号内省略“混乱”
```
```
raw verdict: 括号内省略“混乱”（50% confusion power）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02422

- 位置：`mod-tome.lua:30940`（tome）｜section：`mod-tome/data/talents/techniques/techniques.lua`｜source_tag：`_t`
- 原文：`Training and techniques to improve mobility and evade your enemies.  On the battlefield, positioning is paramount.`
- 现译：`强化闪避和移动能力，确保你始终处于战斗的上风。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00382 | HUMAN-REVIEW | cross-batch-075 | confirmed | 文风选择 |  |  |

<details><summary>hrq-00382 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“站位/走位至关重要”泛化
```
```
raw verdict: “站位/走位至关重要”泛化为“始终处于战斗的上风”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02425

- 位置：`mod-tome.lua:30968`（tome）｜section：`mod-tome/data/talents/techniques/techniques.lua`｜source_tag：`_t`
- 原文：`Unarmed Boxing techniques that may not be practiced in massive armor or while a weapon or shield is equipped.`
- 现译：`徒手拳击格斗技术，你不能装备板甲、武器和盾牌。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00383 | HUMAN-REVIEW | cross-batch-075 | confirmed | 改为施展限制 |  |  |

<details><summary>hrq-00383 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：施展限制误写“不能装备”（机制误导）
```
```
raw verdict: 施展限制误写成“不能装备”板甲/武器/盾牌→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02426

- 位置：`mod-tome.lua:30970`（tome）｜section：`mod-tome/data/talents/techniques/techniques.lua`｜source_tag：`_t`
- 原文：`Finishing moves that use combo points and may not be practiced in massive armor or while a weapon or shield is equipped.`
- 现译：`使用你累积的连击点数发动致命的终结一击，你不能装备板甲、武器和盾牌。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00384 | HUMAN-REVIEW | cross-batch-075 | confirmed | 后半必修；前半文风 |  |  |

<details><summary>hrq-00384 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同上“不能装备”；advisory：“致命的”+单数化
```
```
raw verdict: 后半句同样把“无法施展”误写成“不能装备”→confirmed; 添加“致命的”、复数类别写成单数“终结一击”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02427

- 位置：`mod-tome.lua:30972`（tome）｜section：`mod-tome/data/talents/techniques/techniques.lua`｜source_tag：`_t`
- 原文：`Grappling techniques that may not be practiced in massive armor or while a weapon or shield is equipped.`
- 现译：`抓取敌人的技巧，你不能装备板甲、武器和盾牌。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00385 | HUMAN-REVIEW | cross-batch-075 | confirmed | 可能涉及类别名一致性，需裁定 |  |  |

<details><summary>hrq-00385 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同上装备禁令；advisory：Grappling techniques 译窄
```
```
raw verdict: 后半句装备禁令误译同上→confirmed; `Grappling techniques` 译为“抓取敌人的技巧”偏窄→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02428

- 位置：`mod-tome.lua:30976`（tome）｜section：`mod-tome/data/talents/techniques/techniques.lua`｜source_tag：`_t`
- 原文：`Teaches various martial arts techniques that may not be practiced in massive armor or while a weapon or shield is equipped.`
- 现译：`高级徒手格斗技能，不能装备板甲、武器和盾牌。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00386 | HUMAN-REVIEW | cross-batch-075 | confirmed | 按本条原文重译 |  |  |

<details><summary>hrq-00386 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：混入相邻类别 Advanced、漏译 Teaches；confirmed：装备禁令误译
```
```
raw verdict: 前半句把 `Teaches various martial arts techniques` 错写成“高级徒手格斗技能”（混入相邻类别 Advanced、漏 Teaches）→confirmed; 后半句再次把施展限制写成装备禁令→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-075-01.md](reports/sol-075-01.md)。译文未修改。共 15 个 claim：11 confirmed、4 advisory、0 pending、0 refuted，全部基于固定 commit `624a6732…`。 译文未修改。02425–02428 四条「存在疑点」全部被 Sol 逐条确认（其中伴随的 advisory 单独分档）。
```
</details>

## entry-02435

- 位置：`mod-tome.lua:31034`（tome）｜section：`mod-tome/data/talents/techniques/throwing-knives.lua`｜source_tag：`tformat`
- 原文：`You can throw knives with lightning speed, increasing your attack speed with them by %d%% and giving you a %d%% chance when striking a target in melee to throw a knife at a random foe within 7 tiles for 100%% damage. 
		This bonus attack can only trigger once per turn, and does not trigger from throwing knife attacks.`
- 现译：`你可以闪电般地投掷你的飞刀。增加 %d%% 攻击速度，近战攻击时有 %d%% 几率投掷一把飞刀随机对 7 格范围内的一名敌人造成 100%% 伤害。
		每回合仅触发 1 次，不会被投掷飞刀触发。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00387 | HUMAN-REVIEW | cross-batch-076 | confirmed | 补“飞刀”限定 |  |  |

<details><summary>hrq-00387 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：飞刀专属攻速被泛指“攻击速度”（机制范围误导）
```
```
raw verdict: 飞刀专属攻速加成被泛指为“攻击速度”→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02439

- 位置：`mod-tome.lua:31076`（tome）｜section：`mod-tome/data/talents/techniques/tireless-combatant.lua`｜source_tag：`tformat`
- 原文：`Any time you do not have an opponent in a square adjacent to you, you gain %0.1f Stamina regeneration. At talent level 3 or more, you also gain an equal amount of life regen when Breathing Room is active.`
- 现译：`当没有敌人与你相邻的时候，你获得 %0.1f 体力回复。技能等级 3 及以后，这个技能带给你等量的生命回复。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00388 | HUMAN-REVIEW | cross-batch-076 | refuted | 可选可读性优化，非必修 |  |  |

<details><summary>hrq-00388 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：遗漏触发前提不成立——“这个技能”承接首句条件，未产生不同机制
```
```
raw verdict: 遗漏 “when Breathing Room is active” 触发前提→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02449

- 位置：`mod-tome.lua:31188`（tome）｜section：`mod-tome/data/talents/techniques/weaponshield.lua`｜source_tag：`tformat`
- 原文：`Hit your target with your shield 3 times for %d%% damage then quickly return to a blocking position.  The bonus block will not check or trigger Block cooldown.`
- 现译：`用盾牌拍击目标 3 次，造成 %d%% 盾牌伤害，然后迅速进入格挡状态。
		这次额外格挡既不检查也不触发格挡技能的冷却（冷却中仍可获得）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00389 | HUMAN-REVIEW | cross-batch-076 | confirmed | 是否保留括注 |  |  |

<details><summary>hrq-00389 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：括注“冷却中仍可获得”有源码依据（`ignore_cd=true`），不构成错误
```
```
raw verdict: 括注“冷却中仍可获得”有源码依据，不构成机制错误→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02451

- 位置：`mod-tome.lua:31195`（tome）｜section：`mod-tome/data/talents/techniques/weaponshield.lua`｜source_tag：`tformat`
- 原文：`Enter a protective battle stance allowing you to defend yourself more proficiently while using a shield.
		Increases Armour by %d, Block value by %d, and reduces Block cooldown by 2.
		Increases stun and knockback resistance by %d%%.
		The Armor and Block bonuses increase equally with your Dexterity and Strength.`
- 现译：`进入一个保护性的战斗姿态，让你在使用盾牌的同时更熟练地保护自己。
		提升护甲值 %d，格挡值 %d，减少格挡冷却 2 回合。
		提升眩晕和击退抗性 %d%%。
		护甲和格挡值加成受你的敏捷和力量值影响。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00390 | HUMAN-REVIEW | cross-batch-076 | confirmed | 可补等权表述 |  |  |

<details><summary>hrq-00390 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：遗漏力量/敏捷等权贡献细节
```
```
raw verdict: 遗漏力量与敏捷等权贡献的细节→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02456

- 位置：`mod-tome.lua:31266`（tome）｜section：`mod-tome/data/talents/uber/const.lua`｜source_tag：`tformat`
- 原文：`Thanks to your newfound knowledge of corruption, you've learned some tricks for toughening your body... but only if you are healthy enough to withstand the strain from the changes.
		Improves your life by 500, your defense by %d, your armour by %d, your armour hardiness by 20%% and your saves by %d as your natural toughness and reflexes are pushed beyond their normal limits.
		Your saves armour and defense will improve with your Constitution.`
- 现译：`多亏了你在枯萎能量上的新发现，你学到一些方法来增强你的体质。但是只有当你有一副强壮的体魄时方能承受这剧烈的变化。
		增加你 500 点生命上限，%d 点闪避，%d 护甲值，20%% 护甲强度，%d 所有豁免，你天生的韧性和反应能力突破了自然极限。
		豁免、护甲和闪避受体质值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00391 | HUMAN-REVIEW | cross-batch-076 | pending | **需术语负责人裁定** |  |  |

<details><summary>hrq-00391 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：`corruption`→“枯萎能量”是否混淆 corruption/blight，冻结输入无术语裁决
```
```
raw verdict: `corruption` 译作“枯萎能量”是否混淆 corruption/blight→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02460

- 位置：`mod-tome.lua:31291`（tome）｜section：`mod-tome/data/talents/uber/cun.lua`｜source_tag：`logSeen`
- 原文：`You unleash a blast of #DARK_GREEN#virulent blight!#LAST#!`
- 现译：`你释放出 #DARK_GREEN#枯萎疾病#LAST#爆炸！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00392 | HUMAN-REVIEW | cross-batch-076 | confirmed | 标点/界面文风 |  |  |

<details><summary>hrq-00392 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：双感叹号规整；confirmed：颜色标签前多余空格
```
```
raw verdict: 规整原文双感叹号→advisory; 颜色标签前多余空格→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02466

- 位置：`mod-tome.lua:31322`（tome）｜section：`mod-tome/data/talents/uber/cun.lua`｜source_tag：`logSeen`
- 原文：`#VIOLET#%s assembles %s!`
- 现译：`#VIOLET#%s 重组为 %s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00393 | HUMAN-REVIEW | cross-batch-076 | confirmed | 按参数顺序重写 |  |  |

<details><summary>hrq-00393 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`assembles`→“重组为”主宾颠倒（日志语义错误）
```
```
raw verdict: `assembles` 译作“重组为”，主宾关系颠倒→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-076-01.md](reports/sol-076-01.md)。译文未修改。共 8 个 claim：5 confirmed、1 refuted、1 pending、1 advisory（本次交叉首次出现 refuted）。 译文未修改。entry-02439 的 Gemini 存疑被 **refuted**（转交范围不预设结论的直接例证）；entry-02456 保持 pending 待人工术语决定。
```
</details>

## entry-02474

- 位置：`mod-tome.lua:31333`（tome）｜section：`mod-tome/data/talents/uber/cun.lua`｜source_tag：`tformat`
- 原文：`Surround yourself with an elemental aura that stores damage you deal.
		Whenever you have stored %d damage of one type you unleash a powerful blast at a random enemy dealing %d damage of that type in radius %d and granting you one of the following effects:

		Physical:		Cleanses 1 physical debuff and grant immunity to physical debuffs for 2 turns.
		#PURPLE#Arcane:#LAST#		Increases your mind and spell action speeds by 30%% for 3 turns.
		#LIGHT_RED#Fire:#LAST#		Increases all damage dealt by %d%% for 3 turns.
		#1133F3#Cold:#LAST#		Turns your skin into ice for 3 turns increasing armor by %d and dealing %d ice damage to attackers.
		#ROYAL_BLUE#Lightning:#LAST#	Increases your movement speed by %d%% for 2 turns.
		#YELLOW#Light:#LAST#		Reduces all cooldowns by 20%% for 3 turns.
		#LIGHT_GREEN#Nature:#LAST#		Cleanses 1 magical debuff and grant immunity to magical debuffs for 2 turns.

		Each effect can only happen once per 10 player turns.  This does not count as a typical cooldown.
		The damage and some effect powers increase with your Cunning and the threshold with your level.
		%s`
- 现译：`你被元素光环笼罩，存储你造成的元素伤害。
		当你积累的某类伤害达到 %d 时，你会向一个随机的敌人发射一次强力的爆炸，造成 %d 的该类型伤害，爆炸半径 %d 码，并对你自己附加以下的附加效果：

		物理：清除 1 个物理负面特效并给予 2 回合物理负面特效豁免。
		#PURPLE#奥术 :#LAST# 增加你的精神和施法速度 30%%，持续 3 回合。
		#LIGHT_RED#火焰 :#LAST# 增加你所造成的所有伤害 %d%%，持续 3 回合。
		#1133F3#寒冷 :#LAST# 将你的皮肤变成冰，增加护甲 %d，对攻击者造成 %d 冰冻伤害，持续 3 回合
		#ROYAL_BLUE#闪电 :#LAST# 你的移动速度提升 %d%%，持续 2 回合。
		#YELLOW#光系 :#LAST# 技能冷却时间减少 20%%，持续 3 回合。
		#LIGHT_GREEN#自然 :#LAST# 清除 1 个魔法负面特效并给予 2 回合魔法负面特效豁免。

		同种效果最多每 10 回合触发一次。这不是普通的技能冷却。
		伤害和效果强度受灵巧值加成，伤害阈值受等级加成。
		%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00394 | HUMAN-REVIEW | cross-batch-077 | confirmed | 排版直修 |  |  |

<details><summary>hrq-00394 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：冒号前多余空格、寒冷效果缺句号；confirmed：8 个占位符及百分号正确
```
```
raw verdict: 冒号前多余空格、寒冷效果缺句号→confirmed; 8 个占位符及百分号保持正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-077-01.md](reports/sol-077-01.md)。译文未修改。共 13 个 claim：8 confirmed、4 pending、1 advisory、0 refuted。 译文未修改。4 条 pending 全部指向“需提供冻结术语条目”而非语义分歧，按契约保持 pending 等人工。
```
</details>

## entry-02489

- 位置：`mod-tome.lua:31513`（tome）｜section：`mod-tome/data/talents/uber/mag.lua`｜source_tag：`tformat`
- 原文：`You infuse blighted energies into all of your summons, granting them Bone Shield (level 3) and a bonus to Spellpower equal to your Magic.
		Your Wilder Summons and Necrotic Minions will gain special corrupted talents (level 3), other summons will gain 10%% Blight damage conversion and Virulent Disease (level 3).
		#GREEN#Wilder Summons:#LAST#
		- War Hound: Gnaw
		- Jelly: Curse of Defencelessness
		- Minotaur: Ruin
		- Golem: Acid Blood
		- Ritch: Life Tap
		- Hydra: Blood Spray
		- Rimebark: Poison Storm
		- Fire Drake: Flame of Urh’Rok
		- Turtle: Elemental Discord
		- Spider: Blood Grasp
		#GREY#Necrotic Minions:#LAST#
		- Skeleton Mages: Bone Spear
		- Skeleton Archers: Bone Spike
		- Skeleton Warriors: Ruin
		- Bone Giants: Bone Spike and Ruin
		- Ghouls: Virulent Disease
		- Dread: Slumber
		%s
		`
- 现译：`你把枯萎能量灌注进你的召唤生物中，让他们获得白骨护盾（等级 3），并获得相当于你魔力值的法术强度加成。
		你的自然召唤和死灵随从将会得到特殊的枯萎技能（等级 3），其他的召唤物将会获得 10%% 枯萎伤害转换，并获得剧毒瘟疫（等级 3）。
		#GREEN#自然召唤：#LAST#
		- 战争猎犬：啃噬
		- 果冻怪：无防备诅咒
		- 米诺陶：毁伤
		- 岩石傀儡：酸性血液
		- 喷火里奇：生命分流
		- 九头蛇：鲜血喷射
		- 雾凇：剧毒风暴
		- 火龙：乌鲁洛克之焰
		- 乌龟：元素狂乱
		- 蜘蛛：鲜血支配
		#GREY#死灵随从：#LAST#
		- 骷髅法师：白骨之矛
		- 骷髅弓箭手：白骨尖刺
		- 骷髅战士：毁伤
		- 骨巨人：白骨尖刺和 毁伤
		- 食尸鬼：剧毒瘟疫
		- 梦魇：沉睡
		%s
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00395 | HUMAN-REVIEW | cross-batch-077 | confirmed | **需术语条目裁定 Dread** |  |  |

<details><summary>hrq-00395 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Dread`→“梦魇”对象识别错误；pending：正式替换词必定是“噩灵”？；confirmed：“白骨尖刺和 毁伤”多空格；pending：其余技能名是否均对齐？
```
```
raw verdict: `Dread` 译作“梦魇”存在对象识别错误→confirmed; 正式替换词必定是“噩灵”→pending; “白骨尖刺和 毁伤”多一个空格→confirmed; 其余技能名对应正常→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-077-01.md](reports/sol-077-01.md)。译文未修改。共 13 个 claim：8 confirmed、4 pending、1 advisory、0 refuted。 译文未修改。4 条 pending 全部指向“需提供冻结术语条目”而非语义分歧，按契约保持 pending 等人工。
```
</details>

## entry-02500

- 位置：`mod-tome.lua:31700`（tome）｜section：`mod-tome/data/talents/uber/str.lua`｜source_tag：`tformat`
- 原文：`During your studies of celestial forces you came in contact with an entity far beyond Eyal: the living incarnation of a Star!
		By allying yourself with it you can gain its power!

		Grants multiple benefits:
		- The strength of your bond is so strong that you can now #GOLD#wield a two-handed weapon and a shield together#LAST#
		- 50%% of all damage you deal is converted to #GOLD#light damage#LAST#
		- #GOLD#Gravitic Effulgence#LAST#: whenever your Weapon of Light hits the damage is now a radius 2 sphere and all foes in range 5 are drawn to it. (You can toggle this effect)
		- The damage and chance to trigger of #GOLD#Searing Sight#LAST# is doubled
		- Whenever #GOLD#Sun's Vengeance#LAST# triggers the remaining cooldown of Judgement is reduced by 6.
		- If you also know #GOLD#Irresistible Sun#LAST#, it will set the fire and light resistances of those affected to 0%%

		#{italic}##GOLD#Will you bind yourself to the Distant Sun?#{normal}#
		`
- 现译：`在研习天体之力时，你接触到了距离埃亚尔大陆极其遥远的存在：一颗恒星的化身！
        与它结盟，你将获得它的力量。

        增益：
        - 你的力量如此强大，你可以#GOLD#同时装备双手武器和盾牌#LAST#
        - 50%% 伤害转化为 #GOLD#光系伤害#LAST#
        - #GOLD#光辉引力#LAST#：光明之刃变成半径2的球形伤害，且可以将5格范围内的敌人拉过来（你可以开关此效果）。
		- #GOLD#灼热之视#LAST# 的伤害和触发概率翻倍
        - #GOLD#阳光之怒#LAST# 触发时，裁决的剩余冷却时间减少6回合。
        - 若你也习得 #GOLD#无御之日#LAST#，它将使受影响者的光系和火焰伤害抗性降低为 0%%

		#{italic}##GOLD#你会同遥远的太阳联合吗？#{normal}#
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00396 | HUMAN-REVIEW | cross-batch-077 | confirmed | 补语义；需术语输入 |  |  |

<details><summary>hrq-00396 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`strength of your bond`→“你的力量如此强大”误译；confirmed：标签/百分号/机制完整；pending：关联技能中文名对齐？
```
```
raw verdict: `strength of your bond` 误译为“你的力量如此强大”→confirmed; 标签、百分号和核心机制完整→confirmed; 所有关联技能中文名均已对齐→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-077-01.md](reports/sol-077-01.md)。译文未修改。共 13 个 claim：8 confirmed、4 pending、1 advisory、0 refuted。 译文未修改。4 条 pending 全部指向“需提供冻结术语条目”而非语义分歧，按契约保持 pending 等人工。
```
</details>

## entry-02506

- 位置：`mod-tome.lua:31869`（tome）｜section：`mod-tome/data/talents/undeads/ghoul.lua`｜source_tag：`tformat`
- 原文：`Gnaw your target for %d%% damage.  If your attack hits, the target may be infected with Ghoul Rot for %d turns.
		Each turn, Ghoul Rot inflicts %0.2f blight damage.
		Targets suffering from Ghoul Rot rise as friendly ghouls when slain.
		Ghouls last for %d turns and can use Gnaw, Ghoulish Leap, Stun, and Rotting Disease.
		The blight damage scales with your Constitution.`
- 现译：`啃噬目标，造成 %d%% 伤害。如果你的攻击命中，目标可能感染食尸鬼腐烂疫病，持续 %d 回合。
		食尸鬼腐烂疫病每回合造成 %0.2f 枯萎伤害。
		目标被杀死时会变成为你作战的友方食尸鬼。
		食尸鬼傀儡持续 %d 回合，可以使用啃噬、食尸鬼跳跃、震慑和腐烂疫病。
		受体质影响，枯萎伤害按比例加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00397 | HUMAN-REVIEW | cross-batch-077 | confirmed | **术语一致性决定** |  |  |

<details><summary>hrq-00397 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：4 个占位符正确；confirmed：“食尸鬼跳跃”符合本段语境；pending：与“定向跳跃”冲突？；advisory：建议保留“食尸鬼跳跃”
```
```
raw verdict: 4 个占位符类型和顺序正确→confirmed; “食尸鬼跳跃”符合本段实际技能语境→confirmed; 与正式术语“定向跳跃”冲突→pending; 建议保留“食尸鬼跳跃”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-077-01.md](reports/sol-077-01.md)。译文未修改。共 13 个 claim：8 confirmed、4 pending、1 advisory、0 refuted。 译文未修改。4 条 pending 全部指向“需提供冻结术语条目”而非语义分歧，按契约保持 pending 等人工。
```
</details>

## entry-02520

- 位置：`mod-tome.lua:32306`（tome）｜section：`mod-tome/data/texts/intro-tutorial.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#Welcome to Tales of Maj'Eyal!#LAST#

This tutorial will present you with a short quest to familiarise yourself with the game.
You are a Human adventurer sent into the forest by the local village to dispose of the "Lone Wolf".

This tutorial character is more powerful than a normal starting character and has infinite lives.
A normal character has limited lives, and once you run out, you stay dead (unless you found or accomplished things that allow you to resurrect).

During this tutorial you will be guided by dialog boxes such as this one, explaining how things work.
Dialog boxes can be dismissed by pressing Escape or clicking outside of their zone (or on the title bar).

Now press #LIGHT_BLUE#escape#LAST# or #LIGHT_BLUE#click outside#LAST# this dialog to close it and proceed.
`
- 现译：`#LIGHT_GREEN#欢迎你来到 ToME 4！#LAST#

这个教程会安排给你一个简短的任务以帮助你熟悉这个游戏。
你是一个人类冒险者，被当地村庄派到森林里去消灭“孤狼”。

这个教程角色比普通开始游戏时的游戏角色要强大的多，而且拥有无限生命。
普通角色的生命数有限，一旦耗尽便会永久死亡（除非你找到或完成了能让你复活的事物）。

在这个教程游戏过程中，你会碰到很多像这样的弹出对话框，来解释游戏的内容。
对话框可以通过按 Esc 键或者点击框外其他地方或者单击对话框标题来关闭。

现在按下#LIGHT_BLUE#Esc 键#LAST#或者#LIGHT_BLUE#点击对话框外#LAST#即可关闭此对话框并继续。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00398 | HUMAN-REVIEW | cross-batch-078 | confirmed | 品牌风格；如需升级需另供对照 |  |  |

<details><summary>hrq-00398 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：全称缩写为“ToME 4”；pending：与成就／手札译名不一致（无冻结对照）；confirmed：颜色码/孤狼/按键无丢失
```
```
raw verdict: 游戏全称被缩写为“ToME 4”→advisory; 与成就／手札常规译名不一致（无冻结对照）→pending; 颜色码、孤狼、按键提示无丢失→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02521

- 位置：`mod-tome.lua:32352`（tome）｜section：`mod-tome/data/texts/message-last-hope.lua`｜source_tag：`_t`
- 原文：`@playername@, this message is of utmost importance.

The staff you left at Last Hope is gone. A raid of orcs ambushed the guards that were transporting it to a secret vault.
Our troops managed to capture one of the orcs and made him talk.
He did not know much, but he did speak about "masters" in the Far East.
He spoke about Golbug -- this seems to be a warmaster in Reknor -- leading a raid to send a "package" through a portal.

This calls for urgency; should you find this Golbug or the portal, please investigate.

               #GOLD#-- Tolak, King of the Allied Kingdoms`
- 现译：`@playername@，这份报告极其重要。

你留在最后的希望的法杖不见了。一群兽人伏击了正将它押送往秘密金库的守卫。
我们的部队设法俘虏了其中一个兽人，并让他开了口。
他知道的不多，但他提到了远东大陆的“主人”。
他提到了高尔布格，貌似是瑞库纳的一位战争领主，带领一场袭击，以便将一个“包裹”送过传送门。

事情非常紧急；如果你找到这个高尔布格或那个传送门，请务必调查。

			   #GOLD#-- 托拉克，联合王国国王。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00399 | HUMAN-REVIEW | cross-batch-078 | confirmed | 缩进需游戏内截图 |  |  |

<details><summary>hrq-00399 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：落款缩进/句号；**refuted**：“ShowText 不影响显示”不成立（制表符原样绘制、句号可见）；confirmed：占位符/专名正确
```
```
raw verdict: 落款缩进（制表符 vs 空格）与句号不同→advisory; “在 ShowText 中不影响显示”缺乏成立基础→refuted; 占位符与主要专名保存正确→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02522

- 位置：`mod-tome.lua:32371`（tome）｜section：`mod-tome/data/texts/message-last-hope.lua`｜source_tag：`_t`
- 原文：`@playername@, this message is of utmost importance.

Our elders searched the old texts looking for clues about the staff of which you spoke.
It turns out to be a powerful object indeed, able to absorb the power of places, and beings.
This must not fall in the wrong hands, which certainly include orcish hands.
While you were gone, one of our patrols met a group of orcs led by Ukruk. We could not stop them, but we managed to capture one of them.
He did not know much, but he did speak about "masters" in the Far East.
He spoke about meeting with Golbug -- this seems to be a warmaster in Reknor -- to send a "package" through a portal.

This calls for urgency; should you find this Golbug or the portal, please investigate.

               #GOLD#-- Tolak, King of the Allied Kingdoms`
- 现译：`@playername@，这份报告极其重要。

我们的长老从古老文献中查找你提到的那个法杖的线索。
它的确是一件非常强大的物品，可以吸收地点和生物的力量。
所以它绝对不能落入坏人的手中，很显然包括兽人。
你不在的时候，我们的一个巡逻队遭遇了乌克鲁克带领的一群兽人，
我们没法阻止他们，不过我们抓了他们中的一个。

他知道的不多，但他提到了远东大陆的“主人”。
他提到了与高尔布格会面——貌似是瑞库纳的一位战争领主——以便将一个”包裹”送过传送门。

事情非常紧急；如果你找到这个高尔布格或那个传送门，请务必调查。

			   #GOLD#-- 托拉克，联合王国国王。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00400 | HUMAN-REVIEW | cross-batch-078 | confirmed | 引号可直接修 |  |  |

<details><summary>hrq-00400 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：**“包裹”起始引号错误（双右引号 U+201D）**；advisory：额外空行；advisory：落款排版
```
```
raw verdict: “包裹”起始引号错误（两个 U+201D）→confirmed; 额外空行改变段落组织→advisory; 落款排版问题与 entry-02521 相同→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02523

- 位置：`mod-tome.lua:32407`（tome）｜section：`mod-tome/data/texts/tutorial/done.lua`｜source_tag：`_t`
- 原文：`#GOLD#Congratulations !#WHITE#

You have completed this small tutorial, and should now know the basics of ToME4. You are ready to step forward into the world to find glory, treasures and be mercilessly slaughtered by hordes of creatures you thought you could handle!
During this tutorial some creatures were adjusted to the need of the teachings, beware, in the real world trolls are not usually this nice!

If you need a reminder of which key does what, you can access the game menu by pressing #GOLD#Escape#WHITE# and checking the key binds (you can also adjust them to your needs).

As this is probably your first time with the game you will find there is a limited number of races and classes available to play, many many more do exist but you will unlock them while playing.

Now go boldly and remember: #GOLD#Have fun!#WHITE#
Press Escape, save & exit and create a new character!
`
- 现译：`#GOLD#恭喜你！#WHITE#

你完成了这个简单教程，应该已经了解 ToME4 的基础。现在你已准备好踏入这个世界，寻找荣耀与财富，并被一群你自以为能对付的怪物无情屠杀！
在教程中，一些生物为了配合教学进行了调整；记住，在真实世界里，巨魔通常不
会这么友善！

如果你想知道快捷键的功能，你可以按 #GOLD#Esc#WHITE#键进入游戏菜单检查按键设定(你也可以
根据你的需要改变设置)。

也许这是你第一次玩这个游戏，你会发现可供游玩的种族和职业数量有限；游戏中还存
在许多其他种族和职业，你会在游戏过程中解锁它们。

现在，勇敢前进并记住：#GOLD#好好享受游戏的乐趣！#WHITE#
请按下 Esc 键，保存并退出游戏，建立一个新的角色吧！
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00401 | HUMAN-REVIEW | cross-batch-078 | confirmed | 版面确认后清理换行 |  |  |

<details><summary>hrq-00401 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：词内硬换行；advisory：半角括号；confirmed：语义与颜色标签完整
```
```
raw verdict: 存在切断词语的硬换行→confirmed; 使用半角括号→advisory; 语义与颜色标签总体完整→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02524

- 位置：`mod-tome.lua:32437`（tome）｜section：`mod-tome/data/texts/tutorial/levelup.lua`｜source_tag：`_t`
- 原文：`In ToME4 a character's power depends on her/his level: players can get up to level 50.

Each level brings more life and resources (like stamina, mana, etc.) and different kinds of points that can improve your character:
* #GOLD#Stat points#WHITE#: They allow you to raise the six main stats: Strength, Dexterity, Magic, Willpower, Cunning and Constitution. You get 3 points per level.
* #GOLD#Class talent points#WHITE#: Class talents define the core functions of your class. You gain 1 point every level, plus 1 extra point on multiples of 5.
* #GOLD#Generic talent points#WHITE#: Generic talents provide utility and/or more power, but are not always specific to your class. You gain 1 point on levels that aren't multiples of 5.
* #GOLD#Category talent points#WHITE#: They allow you to improve your mastery of a talent category (increasing the power of all talents inside) or to learn a new talent category.

Levels are gained when experience reaches 100%. You gain experience from killing a hostile creature whose level is similar to yours.

To open the character levelup screen either press 'p' or right-click on yourself and choose 'Levelup'.

Now open the levelup screen and assign your points.
`
- 现译：`在ToME4中角色的能力取决于他/她的人物等级：角色最高可以升级至50级。

每升一级你会获得更多的生命值和其他能量值（比如体力、法力等等）。另外还能获得
不同的点数来提升你的角色。
* #GOLD#属性点数#WHITE#：允许你提升6个主要属性：力量、敏捷、魔力、意志、灵巧和体质。每等级你能获
得3个点数。
* #GOLD#职业技能点数#WHITE#：职业技能是你的职业的核心能力，每升一级获得1点，每5级额外获得1点。
* #GOLD#通用技能点数#WHITE#：通用技能是非职业限定的一些角色提升技能，在等级不是 5 的倍数时，你每升一级获得 1 点。
* #GOLD#技能树解锁点#WHITE#：可以提高你对某一技能树内所有技能的掌握程度，或者也可以解锁一个新的技能树。

每当你的经验值获得达到100%时你就升级了。你可以通过杀死和你等级差不多的怪物
来获得经验值。

按下 'p' 键，或者右键点击你自己并选择“升级”，即可打开升级面板。

现在，打开你的升级面板，进行升级操作。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00402 | HUMAN-REVIEW | cross-batch-078 | confirmed | 需提供术语条目 |  |  |

<details><summary>hrq-00402 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：数值规则一致；pending：术语库合规无冻结输入；confirmed：多处行内硬换行
```
```
raw verdict: 数值规则翻译与原文一致→confirmed; “六项属性译名完全符合术语库”（无冻结术语输入）→pending; 存在多处行内硬换行→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02530

- 位置：`mod-tome.lua:32784`（tome）｜section：`mod-tome/data/texts/tutorial/stats/stats7.lua`｜source_tag：`_t`
- 原文：`Suppose you're an archmage, and you blast somebody with the Flameshock spell. 

This spell does fire damage, which is determined by your #LIGHT_GREEN#Spellpower#WHITE#. #GOLD#Combat stats#WHITE# are not used to mitigate damage, so the defender is going to take the full force of the spell, barring fire resistance (which is a subject for another tutorial).

The spell will also attempt to stun the target. Stunning, you recall, is a physical effect, so the target defends with their #LIGHT_GREEN#Physical save#WHITE#. However, unlike the previous example, the source of this stun is a spell. You will thus compare your #LIGHT_GREEN#Spellpower#WHITE# to the target's #LIGHT_GREEN#Physical save#WHITE# to determine the success of the stun.
`
- 现译：`假如你是一个元素法师，你用火焰冲击打击某个目标。

法术造成的火焰伤害由你的 #LIGHT_GREEN#法术强度#WHITE#决定。
#GOLD#战斗属性#WHITE# 并不是用来减轻伤害的，所以防御者会受到全部法术伤害，
实际受到伤害量与火焰抗性相关（这是另一个教程的主题）。

法术另外也会尝试震慑目标，说起震慑你会回想起来这是一个物理效果，所以目标
以 #LIGHT_GREEN#物理豁免#WHITE# 来计算。
然而和前面的例子不同，震慑的来源是一个法术，所以你用你的 #LIGHT_GREEN#法术强度#WHITE# 与目标的
#LIGHT_GREEN#物理豁免#WHITE# 来决定震慑的成功率。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00403 | HUMAN-REVIEW | cross-batch-078 | confirmed | 是否允许偏离英文补条件 |  |  |

<details><summary>hrq-00403 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：判定关系正确；**refuted**：Gemini“与源码完全一致”过度（震慑免疫也是例外，属原教程简化）；confirmed：行内硬换行
```
```
raw verdict: 法术强度与物理豁免判定关系正确→confirmed; “机制叙述与源码逻辑完全一致”过度成立（震慑免疫也是例外）→refuted; 存在行内硬换行→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02533

- 位置：`mod-tome.lua:33109`（tome）｜section：`mod-tome/data/texts/tutorial/stats-scale/scale3.lua`｜source_tag：`_t`
- 原文：`#GOLD#Combat stat#WHITE# scores are between one and one-hundred, with special color coding applied for each interval of twenty. The colors are the same hues as those used in inventory text to indicate gear quality.

These subintervals of twenty we'll call #GOLD#tiers#WHITE# from now on.
`
- 现译：`#GOLD#战斗属性#WHITE# 范围为1～100，每隔20会用一种不同颜色来显示，在装备提示文字中也
用类似的色调来表示装备的品质。

现在起这每个20的间隔，我们称之为 #GOLD#层级#WHITE#。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00404 | HUMAN-REVIEW | cross-batch-078 | confirmed | 是否统一清理折行 |  |  |

<details><summary>hrq-00404 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：区间/tier 正确；confirmed：额外硬换行
```
```
raw verdict: 区间与 tier 定义翻译正确→confirmed; 存在额外硬换行→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02534

- 位置：`mod-tome.lua:33121`（tome）｜section：`mod-tome/data/texts/tutorial/stats-scale/scale4.lua`｜source_tag：`_t`
- 原文：`A summary of the #GOLD#combat stat#WHITE# tiers:

#B4B4B4#Tier 1#WHITE# scores, those from one to twenty, are displayed in #B4B4B4#grey#WHITE#.
#FFFFFF#Tier 2#WHITE# scores, those from twenty-one to forty, are displayed in #FFFFFF#white#WHITE#.
#00FF80#Tier 3#WHITE# scores, those from forty-one to sixty, are displayed in #00FF80#green#WHITE#.
#0080FF#Tier 4#WHITE# scores, those from sixty-one to eighty, are displayed in #0080FF#blue#WHITE#.
#8d55ff#Tier 5#WHITE# scores, those from eighty-one to one-hundred, are displayed in #8d55ff#purple#WHITE#.
`
- 现译：`一个 #GOLD#战斗属性#WHITE# 层级的颜色列表：

#B4B4B4#层级1#WHITE#：1～20，显示为 #B4B4B4#灰色#WHITE#。
#FFFFFF#层级2#WHITE#：21～40，显示为 #FFFFFF#白色#WHITE#。
#00FF80#层级3#WHITE#：41～60，显示为 #00FF80#绿色#WHITE#。
#0080FF#层级4#WHITE#：61～80，显示为 #0080FF#蓝色#WHITE#。
#8d55ff#层级5#WHITE#：81～100，显示为#8d55ff#紫色#WHITE#。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00405 | HUMAN-REVIEW | cross-batch-078 | confirmed | 统一留空格或都去 |  |  |

<details><summary>hrq-00405 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：五组区间与颜色码对应；advisory：第五行颜色码前缺空格（五行不统一）
```
```
raw verdict: 五组区间与颜色码全部对应→confirmed; 第五行颜色码前缺少空格（五行不统一）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-078-01.md](reports/sol-078-01.md)。译文未修改。共 22 个 claim：12 confirmed、6 advisory、2 pending、2 refuted。 译文未修改。两条 pending 均因冻结输入不含术语库/对照条目，不是语义分歧；一条 refuted 撤回 Gemini 的机制背书（原教程简化，非本条翻译失真）。
```
</details>

## entry-02538

- 位置：`mod-tome.lua:33287`（tome）｜section：`mod-tome/data/texts/tutorial/stats-tier/tier4.lua`｜source_tag：`_t`
- 原文：`Let's take a closer look at these new timed effects. The easiest way to do that is to have them inflicted on you.

Ahead are a series of bored elves who will happily blast you with whatever spell they have handy. Examine the tooltip of each effect they inflict on you.

`
- 现译：`让我们再仔细研究一下这些新的持续效果的机制。最简单的方法就是让这些效果作用在你自己身上。

前面有几个无聊的精灵，他们会很高兴在你身上施展各种他们所学会的法术，测试一下这些持续效果在你身上的作用，注意查看鼠标提示。

`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00406 | HUMAN-REVIEW | cross-batch-079 | confirmed | 文风取舍 |  |  |

<details><summary>hrq-00406 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：增补“测试……”并弱化 each effect 提示；confirmed：换行完好
```
```
raw verdict: 增补“测试一下这些持续效果”并弱化 each effect 提示→confirmed; 换行结构未见破坏→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02541

- 位置：`mod-tome.lua:33605`（tome）｜section：`mod-tome/data/texts/unlock-afflicted_cursed.lua`｜source_tag：`_t`
- 原文：`Through ignorance, greed or folly, the Cursed served some dark design and are now doomed to pay for their sins.
Their only master now is the hatred they carry for every living thing.
Drawing strength from the death of all they encounter, the Cursed become terrifying combatants.
Worse, any who approach the Cursed can be driven mad by their terrible aura.
Some of them, however, strive to redeem their faults by using their Cursed powers to battle evil.

You have "lifted" the curse of Ben Cruthdar. You can now create new characters with the #LIGHT_GREEN#Cursed class#WHITE#.

Cursed are heavy melee warriors, focusing all their hatred into their blows.
Class features:#YELLOW#
- Engulf your foes in your Gloom, weakening, confusing, stunning and damaging them
- Hunt your prey, tracking them and marking them for death
- Powerful melee combatant#WHITE#

The Cursed use hate, a resource that grows as they kill their foes and decreases while standing idle.
Most of their talents are more effective with high hate.
`
- 现译：`被诅咒者因无知、贪婪或愚行而为某个黑暗阴谋效力，如今必须为自己的罪孽付出代价。
如今，他们唯一的主人，是他们对一切生灵怀有的仇恨。
他们从遇到的一切生灵的死亡中汲取力量，成为恐怖的战士。
更可怕的是，任何接近被诅咒者的人都会受其可怕光环影响而发狂。
不过其中的一些人努力弥补过错，用自己的被诅咒之力与邪恶战斗。

你战胜了本·克鲁塞达尔的诅咒，现在你创建角色时可以选择一个新的职业 #LIGHT_GREEN#被诅咒者#WHITE#。

被诅咒者是重型近战战士，将所有仇恨倾注于自己的攻击。
职业特点：#YELLOW#
- 用你的黑暗光环将你的对手吞没，削弱、混乱、震慑和对他们造成伤害
- 追踪你的猎物，将其标记为必死目标
- 强大的近战能力#WHITE#

被诅咒者使用仇恨值；该资源在他们杀死敌人时增长，静止不动时减少。
他们的大多数技能在仇恨值较高时效果更强。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00407 | HUMAN-REVIEW | cross-batch-079 | confirmed | 补反讽 |  |  |

<details><summary>hrq-00407 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`"lifted"` 引号反讽被平化；confirmed：Gloom/hate/stunned/confused 映射与固定简中一致
```
```
raw verdict: `"lifted"` 的引号与反讽被平化→confirmed; Gloom/hate/stunned/confused 映射与固定简中一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02545

- 位置：`mod-tome.lua:33711`（tome）｜section：`mod-tome/data/texts/unlock-campaign_arena.lua`｜source_tag：`_t`
- 原文：`The arena, a way of violent entertainment. 
A delight for the audience, a source of wealth and glory. A place where aspiring fighters, former adventurers and those cursed to fight
eternally gather to hack away at each other.

You have unlocked the Arena and can now create new characters in a new campaign: #LIGHT_GREEN#The Arena#WHITE#.

The arena pits you against multiple enemies in an open field, making your battle tactics important for survival.
Campaign features:#YELLOW#
- No quests, plots, friendly creatures or ways out: only you against all odds.
- Exclusive scoring system where the faster you kill, the more you earn. Scores are kept for bragging rights!
- Pure hack and slash MAYHEM!
- Your champion becomes the new master of the arena, allowing you to challenge your own champions!
`
- 现译：`竞技场是一种暴力娱乐方式。
为了取悦观众，获得财富和荣耀的地方。在那里，有志之士、以前的冒险家和那些受永远战斗之诅咒的人互相厮杀。

你解锁了竞技场，现在你可以创建一个新人物进行新的战役模式：#LIGHT_GREEN#竞技场#WHITE#。

竞技场模式中你将在开阔场地上与多个敌人战斗，为了存活下来，战斗策略至关重要。
战役特点：#YELLOW#
- 没有任务、剧情、友善生物或逃生途径：只有你独自面对一切逆境。
- 这里有一个积分系统，你越快杀死你的对手得分越高，分数可是你向别人夸耀的资本哦！
- 尽情砍杀吧！
- 你的冠军将成为竞技场的新主宰，让你可以挑战自己的冠军们！
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00408 | HUMAN-REVIEW | cross-batch-079 | confirmed | 修句；文风 |  |  |

<details><summary>hrq-00408 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同位描述改目的表达成不完整句；advisory：“哦！”与 MAYHEM 文风；confirmed：末尾无额外 `#WHITE#`
```
```
raw verdict: 同位描述被改成目的表达，形成不完整句→confirmed; “哦！”与 MAYHEM 译法属文风选择→advisory; 末尾无额外 `#WHITE#`，与源码一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02552

- 位置：`mod-tome.lua:33838`（tome）｜section：`mod-tome/data/texts/unlock-corrupter_corruptor.lua`｜source_tag：`_t`
- 原文：`Every power has a dark side, including the arcane forces.
Corruptors are mages that deal in dark, blighted, demonic magic to attain their goals.
Not all of them are evil, though; some are simply selfish and concerned only with their own power.

You have been taught their ways by the Grand Corruptor and can now create new characters with the #LIGHT_GREEN#Corruptor class#WHITE#.

Corruptors are spellcasters, ranged attackers using magic.
Class features:#YELLOW#
- Plague your foes with deadly and contagious diseases
- Hex and curse your foes, hindering and withering them away
- Sap the life of your victims to heal yourself
- Master demonic energies to burn and destroy. You can even summon a part of the demon plane, the Fearscape, to trap your foes.#WHITE#

Corruptors use "vim" to power their special abilities.
Vim is the life force of all beings. It does not regenerate, and can only be stolen from your foes.
`
- 现译：`所有的力量都有其黑暗的一面，包括奥术。
腐化者是使用黑暗、枯萎和恶魔法术来达到目的法师。
并非所有的腐化者都是邪恶的，有些人只是单纯自私地只关心其个人力量而已。

大腐化者教会了你堕落系法术，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#腐化者#WHITE#。

腐化者是使用魔法进行远程攻击的法师。
职业特点：#YELLOW#
- 使你的目标感染并传播致命的疾病
- 对敌人施加邪术和诅咒，妨碍并使其逐渐凋零
- 从目标身上吸取生命，治疗自身
- 掌握恶魔能量来燃烧和毁灭。你甚至可以召唤恶魔位面的一部分——恶魔空间——来困住敌人。#WHITE#

腐化者使用活力值来施展他们的特殊能力。
活力是所有生物的生命力量，它不会再生，只能从敌人身上窃取。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00409 | HUMAN-REVIEW | cross-batch-079 | confirmed | 直修语病 |  |  |

<details><summary>hrq-00409 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“达到目的法师”漏“的”（明确语病）；confirmed：专名有固定证据、标签闭合
```
```
raw verdict: “达到目的法师”漏“的”，明确语病→confirmed; Grand Corruptor/Fearscape/Vim 有固定简中证据，标签闭合→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02555

- 位置：`mod-tome.lua:34022`（tome）｜section：`mod-tome/data/texts/unlock-difficulty_madness.lua`｜source_tag：`_t`
- 原文：`You won the game on Insane mode.  You are one of the best players!
But fear not because the game is just about to get even more unfair on you!

Welcome to Madness!

Madness features:#YELLOW#
- All zone levels increased by 150% + 6
- All creature talent levels increased by 170%
- Rare creatures are far more frequent and random bosses start to appear
- Bosses will have randomly selected talents
- Player is being hunted! Randomly all foes in a radius will get a feeling of where she/he is
- Player can earn Madness version of achievements if also playing in Roguelike or Adventure permadeath mode.

#WHITE#May you suffer many fun and unfair deaths!
`
- 现译：`你在疯狂模式下通关了游戏。你是最好的玩家之一 !
不过，别害怕，因为游戏会变得更加不公平！

欢迎来到绝望模式！

绝望模式的特点 :#YELLOW#
- 所有区域等级提高 150% + 6
- 所有怪物的技能等级增加 170%
- 稀有怪产生频率大幅增加，同时出现随机 Boss
- Boss 将随机获得技能
- 玩家成为了猎物！随机地，一定半径内的所有敌人都会感知到你所在的位置
- 如果同时在永久死亡模式或冒险模式下游玩，玩家可以获得绝望难度版本的成就

#WHITE# 祝你玩的愉快，死的开心！
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00410 | HUMAN-REVIEW | cross-batch-079 | confirmed | 直修 |  |  |

<details><summary>hrq-00410 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：空格不规范、“玩的愉快”→“玩得愉快”；confirmed：难度/模式映射正确
```
```
raw verdict: `之一 !`、`特点 :`、`#WHITE# 祝你……` 空格不规范；“玩的愉快”应为“玩得愉快”→confirmed; 难度与模式映射正确（Insane/Madness/Adventure/Roguelike）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02557

- 位置：`mod-tome.lua:34056`（tome）｜section：`mod-tome/data/texts/unlock-divine_anorithil.lua`｜source_tag：`_t`
- 原文：`In the uttermost east, on the continent known only as the Far East, dwell the last remnants of Elves and Humans, fighting the Orc Pride and the many perils of the Far East.

Anorithil are mages who are trained in special magic to focus the powers of the Sun and Moons.
They have learned to harness the energy of both shadows and light in their battle against the Pride.
Their motto is: "We stand betwixt the Sun and Moons, where light and darkness meet. In the grey twilight we seek our destiny."

You have helped one of them and can now create new characters with the #LIGHT_GREEN#Anorithil class#WHITE#.

Anorithil are pure spellcasters that rely on positive and negative energies.
Class features:#YELLOW#
- Burn your foes from afar with the light and fire of the Sun
- Head into battle enhanced by your powerful Sun Chants and Moon Hymns
- Engulf your foes in the shadows
- Set glyphs of power to confuse and control your foes#WHITE#

Anorithil use "positive and negative energy" to use their special abilities.
These are filled by some of their spells and depleted by others, making them alternate their talents.
`
- 现译：`在遥远的东方，称为远东大陆的地方，居住着幸存下来的精灵和人类，与兽人部落和远东大陆的种种危险战斗。

星月术士是接受过聚集太阳与月亮神力的特殊魔法训练的法师。
他们在与兽人部落的战斗中学会了如何同时掌控光与影的能量方法。
他们的座右铭是：“我们站在太阳与月亮之间，光明与黑暗交汇的地方，在灰色的暮光中寻找我们的命运。”

你帮助了他们中的一位，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#星月术士#WHITE#。

星月术士是依靠正能量和负能量的纯粹施法者。
职业特点：#YELLOW#
- 用太阳的光与火灼烧远处的敌人
- 使用太阳赞歌和月亮圣诗在战斗中强化你的力量
- 用阴影吞噬你的敌人
- 放置强力圣印来混乱和控制你的敌人#WHITE#

星月术士使用正能量和负能量来施展他们的特殊能力。
其中一些法术会填充这些能量，另一些则会消耗它们，因此他们需要交替使用技能。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00411 | HUMAN-REVIEW | cross-batch-079 | confirmed | 改句式 |  |  |

<details><summary>hrq-00411 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“如何……的方法”句式混用；confirmed：核心语义一致、标签闭合
```
```
raw verdict: “学会了如何……的方法”混用句式→confirmed; Orc Pride、太阳赞歌/月亮圣诗、正负能量语义一致，标签闭合→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02559

- 位置：`mod-tome.lua:34096`（tome）｜section：`mod-tome/data/texts/unlock-divine_sun_paladin.lua`｜source_tag：`_t`
- 原文：`In the uttermost east, on the continent known only as the Far East, dwell the last remnants of Elves and Humans, fighting the Orc Pride and the many perils of the Far East.

Sun Paladins are warriors who are trained in special magic to focus the powers of the Sun.
Paragons of all that is good, they are nonetheless terrible in their battle against the Pride.
Their motto is: "The Sun is our giver, our purity, our essence. We carry the light into dark places, and against our strength none shall pass."

You have discovered the Gates of Morning and can now create new characters with the #LIGHT_GREEN#Sun Paladin class#WHITE#.

Sun Paladins are heavy melee with spellcasting support.
Class features:#YELLOW#
- Burn your foes from afar with the light and fire of the Sun
- Head into battle enhanced by your powerful Chants
- Channel the power of the Sun through your weapon
- Become a walking fortress, protected by your shield#WHITE#

Sun Paladins use "positive energy" to power their special abilities.
It is filled by some of their spells and depleted by others, making them alternate their talents.
`
- 现译：`在遥远的东方，称为远东大陆的地方，居住着幸存下来的精灵和人类，与兽人部落和远东大陆的种种危险战斗。

太阳骑士是受过特殊魔法训练的战士，他们学会聚焦太阳的力量施展他们的特殊能力。
他们是一切善的典范，但在与兽人部落的战斗中依然可怕。
他们的座右铭是：“太阳是我们的赐予者、我们的纯洁、我们的本质。我们将光明带入黑暗之地，凭借我们的力量，无人能够通过。”

你发现了晨曦之门，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#太阳骑士#WHITE#。

太阳骑士是以法术辅助的重型近战职业。
职业特点：#YELLOW#
- 用太阳的光与火灼烧远处的敌人
- 使用太阳赞歌在战斗中强化你的力量
- 将太阳之力灌注进你的武器
- 成为一座移动的堡垒，使用你的盾牌进行防御#WHITE#

太阳骑士使用正能量来施展他们的特殊能力。
某些法术会充满正能量，而另一些法术会消耗它，因此他们需要交替使用技能。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00412 | HUMAN-REVIEW | cross-batch-079 | confirmed | 是否删增补 |  |  |

<details><summary>hrq-00412 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：增补“施展他们的特殊能力”；confirmed：晨曦之门/正能量有证据
```
```
raw verdict: 增补“施展他们的特殊能力”→confirmed; Gates of Morning/positive energy 有固定简中证据→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02565

- 位置：`mod-tome.lua:34230`（tome）｜section：`mod-tome/data/texts/unlock-mage_necromancer.lua`｜source_tag：`_t`
- 原文：`Necromancy, the forbidden art.
Necromancy, the black art.

During the Age of Dusk and the Age of Pyre the world went through a tortured era. Kingdoms were shattered, whole races suppressed, and diseases ran wild, killing millions.
It was a dark time and amidst the chaos came the bringers of terror: the necromancers.
Though they always existed, and will always exist whilst our souls are open to temptation, this was their true age of glory.
The so-called 'noble' archmages regard necromancers as fallen brothers that must be corrected... or removed. But necromancers consider themselves misunderstood practitioners of an art that others are too scared or too feeble to touch. And oh, what great powers those arts do bring....

You have learnt the basics of necromancy, killed a real one, and can now create new characters with the #LIGHT_GREEN#Necromancer class#WHITE#.

Necromancers are dark spellcasters, attuned to death itself. Their ultimate goal is their own eternal life, often as a Lich.
Class features:#YELLOW#
- Cast darkness and ice infused spells to destroy your foes
- Summon an army of undead minions to do your bidding
- Use your minions as pawns, sacrificing them in various cruel and unusual ways
- Embark on the quest of your life: Lichdom#WHITE#

All mages use mana to cast their spells.
It slowly replenishes over time.
`
- 现译：`死灵法术，被禁忌的魔法。
死灵法术，黑暗的魔法。

在黄昏纪元和烈火纪元，世界进入了一个扭曲的时代。国家分裂，整个种族遭到压迫，疫病肆虐，杀死了数百万人。
这是一个黑暗的时代，恐怖的制造者——死灵法师来到了这个混乱的时代。
死灵法师过去一直存在，将来也永远存在，只要灵魂仍向诱惑敞开。这个时代是他们荣耀的时代。
那些所谓的”高贵”的元素法师们认为死灵法师是他们走入歧途的兄弟，必须予以纠正或者消灭。但是死灵法师们认为自己是被误解的从业者，他们深入了别人不敢或者没有能力掌控的魔法领域，而正是这种魔法给他们带来了强大的力量。

你已经学会了死灵法术的基础，并且杀死了一个死灵法师，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#死灵法师#WHITE#。

死灵法师专精于黑暗魔法和死亡本身。他们的终极目标是获得永生，通常以成为巫妖的形式实现。
职业特点：#YELLOW#
- 施放黑暗和冰系魔法摧毁你的目标
- 召唤一支不死随从大军听候你的命令
- 将你的随从当作棋子，以各种残酷而奇特的方式牺牲他们
- 踏上你一生的追求：成为巫妖#WHITE#

所有的法师使用法力值来释放他们的法术。
法力值会随着时间缓慢恢复。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00413 | HUMAN-REVIEW | cross-batch-079 | confirmed | **专名对齐** |  |  |

<details><summary>hrq-00413 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：前引号用右双引号；confirmed：近距离重复；**refuted**：`Age of Pyre` 应为“派尔纪元”非“烈火纪元”
```
```
raw verdict: “所谓的”高贵”的”前引号错误（右双引号）→confirmed; “黑暗的时代…混乱的时代”近距离重复（低影响文风）→confirmed; `Age of Pyre` 并非“烈火纪元”，固定简中为“派尔纪元”（撤回 Gemini 专名主张）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02568

- 位置：`mod-tome.lua:34302`（tome）｜section：`mod-tome/data/texts/unlock-mage_tempest.lua`｜source_tag：`_t`
- 原文：`Since the dawn of time mages have experimented with the elements.
While most mages are content using the Air school, a few of them took their research deeper and created Storm magic.
At its core lies the Tempest, a storm so powerful it can even damage creatures normally immune.

You have mastered storm magic and can now create new Archmage characters that can learn the #LIGHT_GREEN#Storm talents#WHITE#.

Talents:
- #YELLOW#Nova: #WHITE#Unleash a lightning nova around you, dazing and damaging creatures caught inside
- #YELLOW#Shock: #WHITE#Fire a fast bolt of lightning, dazing the target
- #YELLOW#Hurricane: #WHITE#Call down a Hurricane on any creatures you daze, creating a lightning storm around each of them
- #YELLOW#Tempest: #WHITE#Master the Tempest and pierce even through lightning immunities
`
- 现译：`自始以来法师们进行着各种元素试验。
大多数法师满足于使用大气系魔法，少数人则深入研究，创造出了风暴魔法。
其核心是“无尽风暴”，其威力甚至足以伤害通常免疫闪电的生物。

你掌握了风暴系魔法，现在你可以创建一个新的可以学习 #LIGHT_GREEN#风暴系技能#WHITE# 的元素法师角色。

技能：
- #YELLOW# 闪电新星：#WHITE# 对你的四周施放闪电新星，对周围生物造成闪电伤害并带有眩晕效果。
- #YELLOW# 闪电之击：#WHITE# 发射一道快速的闪电箭，眩晕目标
- #YELLOW# 飓风：#WHITE# 召唤风暴攻击你眩晕的目标，产生围绕他们的闪电对其造成伤害。
- #YELLOW# 无尽风暴：#WHITE# 掌握无尽风暴，甚至能穿透目标的闪电免疫。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00414 | HUMAN-REVIEW | cross-batch-079 | confirmed | **专名对齐**；统一空格 |  |  |

<details><summary>hrq-00414 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`#YELLOW#` 后空格与句末标点不统一；advisory：“自始以来”生硬；**refuted**：`Hurricane` 固定名是“风暴之怒”非“飓风”；confirmed：`daze→眩晕` 一致
```
```
raw verdict: `#YELLOW#` 后增空格、句末标点不统一（不破坏颜色码）→confirmed; “自始以来”略生硬（润色意见）→advisory; `Hurricane` 固定技能名是“风暴之怒”而非“飓风”（撤回“四个技能名严格一致”）→refuted; `daze→眩晕` 与固定简中一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02570

- 位置：`mod-tome.lua:34330`（tome）｜section：`mod-tome/data/texts/unlock-mage_thaumaturgist.lua`｜source_tag：`_t`
- 原文：`You have killed a boss by only using beam spells and nothing else, showing a deeper understanding of this type of spells.

You have unlocked the #LIGHT_GREEN#High Thaumaturgist class evolution#WHITE# for Archmages.

Features:
- #YELLOW#Wide Beams#WHITE#: Flame, Manathrust, Lightning, Pulverizing Auger and Ice Shards permanently become 3-wide beam spells.
- Access to the Thaumaturgy spell category containing the spells:
  - #YELLOW#Orb of Thaumaturgy#WHITE#: By placing a thaumaturgy orb on the ground you can duplicate all beam spells you cast.
  - #YELLOW#Multicaster#WHITE#: Casting beams becomes so easy for you that you can weave in random non-beam spells when you cast one.
  - #YELLOW#Slipstream#WHITE#: Flow through the battlefield with ease, when you cast a beam spell you can move one tile for free.
  - #YELLOW#Elemental Array Burst#WHITE#: The ultimate beam spell, the culmination of your deep understanding of magic. A 3-wide beam of pure thaumic energy that can never be resisted.


Class evolutions are selected as prodigies and grant new ways to build and expand your class and are only visible to the concerned class.
`
- 现译：`你仅用射线法术、不使用其他技能杀死了一个boss，展示了你对这类法术的深入理解。

你解锁了元素法师的#LIGHT_GREEN#高阶奇术师#WHITE#职业进阶。

职业特性：
- #YELLOW#宽射线#WHITE#: 火球术，奥术射线，闪电术，粉碎钻击和寒冰箭永久成为宽度为3的射线技能。
- 获得奇术系技能，拥有以下能力：
  - #YELLOW#奇术之球#WHITE#: 在地上放置奇术之球，会复制你释放的射线类法术。
  - #YELLOW#多重施法#WHITE#: 你可以在释放射线类法术的同时交织释放随机非射线法术。
  - #YELLOW#能量滑流#WHITE#: 在战场上自由行动，当你使用射线类法术的时候可以不消耗回合移动一格。
  - #YELLOW#元素阵爆发#WHITE#: 终极射线法术，是你对魔法理解的精华。这一宽度为3的纯粹奇术能量永远无法被抵抗。


职业进阶是一种觉醒技，它们可以给予你新的方法来强化你的职业。只有相关的职业才能看到它们。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00415 | HUMAN-REVIEW | cross-batch-079 | confirmed | 补译；本地化收尾 |  |  |

<details><summary>hrq-00415 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：漏译中心词 `beam`；confirmed：残留小写 `boss`；confirmed：技能名与 `觉醒技` 一致
```
```
raw verdict: 中心词 `beam` 被漏译（只剩“宽度为3的纯粹奇术能量”）→confirmed; 首句保留小写英文 `boss`，本地化不完整（低影响）→confirmed; 五个基础法术、四个奇术技能名及 `prodigies→觉醒技` 与固定简中一致→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-079-01.md](reports/sol-079-01.md)。译文未修改。共 25 个 claim：21 confirmed、2 advisory、2 refuted、0 pending。 译文未修改。两条 **refuted** 都是撤回 Gemini 的专名正确性主张，依据固定简中 locale 映射（派尔纪元、风暴之怒）。
```
</details>

## entry-02576

- 位置：`mod-tome.lua:34475`（tome）｜section：`mod-tome/data/texts/unlock-psionic_solipsist.lua`｜source_tag：`_t`
- 原文：`Solipsists are powerful psionicists that believe that the world is made up of nothing more than the thoughts and dreams of those that live in it.
This power does not come without a price, however.  The Solipsist must constantly fight with their own ego in order to keep a clear view of reality, lest they fall into a state of solipsism, the belief that the world and those that live in it are nothing more than figments of their own mind.

You've experienced the power of dreams first hand and may now create characters with the #LIGHT_GREEN#Solipsist class#WHITE#.

Solipsists use the power of thought and dreams to manipulate the world around them.
Class features:#YELLOW#
- Distort the fabric of reality
- Store and discharge psionic feedback
- Summon powerful warriors birthed from your own consciousness
- Convert damage you take into Psi damage and keep yourself alive with your mental reserves
- Put your foes to sleep, enter their dreams, and become their worst nightmare#WHITE#

Solipsists use their mind to manipulate the world around them.
They require energy to do so, which they recover naturally over time, and through methods others use to heal the body.
`
- 现译：`织梦者是强大的灵能力者，他们相信世界是由思想和人们的梦境组成的。
这种力量并非毫无代价，织梦者必须不断与自己的自我抗争，以保持对现实的清晰认识，以免陷入唯我论状态，认为世界和生活在其中的人们不过是自己心灵的幻象。

你先前已经体验过梦境的力量了，现在你可以在创建人物时选择新的职业 #LIGHT_GREEN#织梦者#WHITE#。

织梦者利用思想和梦境的力量掌控身边的天地。
职业特点：#YELLOW#
- 能够扭曲现实位面
- 可储存并释放反馈能量
- 从意识中召唤强大的战士
- 将你受到的伤害转化为灵能值损失，并用精神储备维持自己的生命
- 使你的敌人陷入沉睡，进入它们的梦境，成为对方的梦魇。#WHITE#

织梦者利用思想和梦境的力量掌控身边的天地。
他们需要灵能来做这一切，而他们的灵能既可以通过自然回复，也可以通过其他人恢复生命值的方法来回复。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00416 | HUMAN-REVIEW | cross-batch-080 | confirmed | 文风取舍 |  |  |

<details><summary>hrq-00416 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：伤害转灵能描述符合机制；advisory：重复译法带入 `dreams`；advisory：冒号/句号非缺陷
```
```
raw verdict: 灵能伤害转化描述符合机制（无缺陷）→confirmed; 末段重复译法带入了原文没有的 `dreams`→advisory; 解锁句无冒号、列表末项独有句号属实（非完整性/运行时问题）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02579

- 位置：`mod-tome.lua:34541`（tome）｜section：`mod-tome/data/texts/unlock-rogue_marauder.lua`｜source_tag：`_t`
- 原文：`Some rogues live by strength rather than cunning, relying on vicious attacks instead of stealth and subterfuge. These bandits maraud the land, lightly armoured and wielding dual weapons, taking what they can by force.

You have learned the value in causing sheer damage in combat and can now create characters with the #LIGHT_GREEN#Marauder class#WHITE#.

Marauders are highly mobile rogues with a range of dextrous techniques and tactics at their disposal. Class features:#YELLOW#
- Move with ease around the battlefield, dancing around your foes and avoiding their attacks
- Wield dual weapons and unleash devastating techniques on your opponents
- Rely on pure thuggery to cripple your enemies before taking them down#WHITE#

Marauders use stamina to fuel their techniques, which replenishes slowly over time.
`
- 现译：`有些盗贼依靠力量而非诡计生存，以凶狠的攻击取代潜行与欺骗。这些强盗身着轻甲、双持武器，横行各地，以武力夺取一切。

你已经明白在战斗中造成巨大伤害的价值，现在你在创建人物时可以选择新的职业 #LIGHT_GREEN#掠夺者#WHITE#。

掠夺者是机动性极高的盗贼，掌握着各种灵巧的技术与战术。
职业特点：#YELLOW#
- 轻松穿行战场，在敌人之间起舞并避开他们的攻击。
- 双持武器，对敌人施展毁灭性的技法。
- 依靠纯粹的暴力重创敌人，再将其击倒。#WHITE#

掠夺者使用体力值来施放他们的技能，体力值会随时间缓慢恢复。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00417 | HUMAN-REVIEW | cross-batch-080 | confirmed | 排版取舍 |  |  |

<details><summary>hrq-00417 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：标签与职业特征完整；advisory：`Class features:` 移行；advisory：无冒号不构成缺陷
```
```
raw verdict: 颜色标签配对完整，职业特征与体力资源翻译完整（无缺陷）→confirmed; `Class features:` 移到新行（可读性排版调整）→advisory; 解锁句无冒号属实，但中文句法仍成立（不构成缺陷）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02586

- 位置：`mod-tome.lua:34673`（tome）｜section：`mod-tome/data/texts/unlock-wanderer.lua`｜source_tag：`_t`
- 原文：`You have wanderer quite a lot since your birth!
You can now create new characters with the #LIGHT_GREEN#Wanderer class#WHITE#.

Wanderers start the game with 3 randomly selected class trees, 1 randomly selected generic tree and Combat Training.
Every 5 levels the gain a new random class tree and every 10 levels they gain a new generic tree.
They are a #{bold}#bonus#{normal}# class, in no way meant to be balanced or even working with all possible talent combos.
Use at your own risk, and have fun.`
- 现译：`从出生以来，你已旅行过许多地方！
现在你在创建人物时可以选择新的职业：#LIGHT_GREEN#流浪者#WHITE#。

流浪者开始游戏时拥有三系随机职业技能，一系随机通用技能，以及战斗训练系。
每升五级将获得额外一系随机职业技能，每升10级将获得额外一系随机通用技能。
他们是一种 #{bold}# 奖励 #{normal}# 职业，没有经过任何的平衡测试，也不保证技能可用。
风险自负，游戏愉快。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00418 | HUMAN-REVIEW | cross-batch-080 | confirmed | 去空格；体例 |  |  |

<details><summary>hrq-00418 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：合理修正英文笔误且标签成对；confirmed：`奖励` 标签内多余空格；advisory：数字体例不统一
```
```
raw verdict: 合理修正英文笔误，`#{bold}#`/`#{normal}#` 成对（无缺陷）→confirmed; `#{bold}# 奖励 #{normal}#` 引入多余空格→confirmed; “每升五级”与“每升10级”数字体例不统一→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02598

- 位置：`mod-tome.lua:34849`（tome）｜section：`mod-tome/data/texts/unlock-yeek.lua`｜source_tag：`_t`
- 原文：`Yeeks are a mysterious race of small humanoids native to the tropical island of Rel.
Their body is covered with white fur and their disproportionate heads give them a ridiculous look, yet they are a cunning and willful race.
Although they are now nearly unheard of in Maj'Eyal, they spent many centuries as secret slaves to the Halfling nation of Nargol.
They gained their freedom during the Age of Pyre and have since then followed 'The Way' - a unity of minds enforced by their powerful psionics.

You have helped a Yeek Wayist and can now create a new character with the #LIGHT_GREEN#Yeek race#WHITE#.

Race features:#YELLOW#
- Mental domination racial power
- Confusion resistance
- Fast leveling
- Frail body#WHITE#
`
- 现译：`夺心魔是热带小岛瑞尔岛上比较神秘的人形原住民种族。
他们的身体长着白色的毛发，另外他们有着不成比例的巨大脑袋使他们看上去样子有点滑稽。
不过他们是非常灵巧而且意志强大的种族。
尽管在马基·埃亚尔几乎没有听说过他们，但在烈火纪元之前的漫长岁月里，他们曾是半身人国家纳格尔的秘密奴隶。
他们在烈火纪元获得了自由，并从此遵循“维网”——一种由他们强大的灵能维系的心灵统一。

你帮助了一名夺心魔维网信徒，现在你可以在创建人物时选择新的种族：#LIGHT_GREEN#夺心魔#WHITE#。

种族特点：#YELLOW#
- 拥有精神控制的种族能力
- 混乱抗性
- 升级较快
- 脆弱的身躯#WHITE#
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00419 | HUMAN-REVIEW | cross-batch-080 | confirmed | 文风取舍 |  |  |

<details><summary>hrq-00419 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：专名与标签完整；advisory：复句拆硬换行（**部分修正 Gemini 表述**，非空行段落）；advisory：显式加入“在烈火纪元之前”
```
```
raw verdict: 专名与颜色标签对应完整（无缺陷）→confirmed; 复句拆成两个硬换行句（非空行分隔段落，部分修正 Gemini 表述）→advisory; 显式加入“在烈火纪元之前”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02599

- 位置：`mod-tome.lua:34882`（tome）｜section：`mod-tome/data/timed_effects/floor.lua`｜source_tag：`tformat`
- 原文：`The target is near a font of life, granting %+0.2f life regeneration, %+0.2f equilibrium regeneration, %+0.2f stamina regeneration and %+0.2f psi regeneration.  (Only living creatures benefit.)`
- 现译：`目标靠近生命之泉，增加 %+0.2f 生命回复，%+0.2f 失衡值回复，%+0.2f 体力回复和 %+0.2f 灵能回复。不死族无法获得此效果。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00420 | HUMAN-REVIEW | cross-batch-080 | confirmed | 补机制限定 |  |  |

<details><summary>hrq-00420 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`%+0.2f` 全部正确；confirmed：“仅活体生物受益”→“不死族无法获得”**不完整**
```
```
raw verdict: 四个 `%+0.2f` 数量、顺序、资源对应正确（无缺陷）→confirmed; “仅活体生物受益”译成“不死族无法获得”是不完整的机制描述→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02601

- 位置：`mod-tome.lua:34884`（tome）｜section：`mod-tome/data/timed_effects/floor.lua`｜source_tag：`_t`
- 原文：`The target is near a spellblaze scar, granting +25% spell critical chance, +10% fire and blight damage but critical spells will drain arcane forces.`
- 现译：`目标接近魔法大爆炸伤痕，获得 25%法术暴击率，增加 10%火焰和枯萎伤害，但是法术暴击会消耗法力值。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00421 | HUMAN-REVIEW | cross-batch-080 | confirmed | 改译 |  |  |

<details><summary>hrq-00421 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`arcane forces`→“法力值”**缩窄资源范围**
```
```
raw verdict: `arcane forces` 单独译成“法力值”错误缩窄资源范围→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02609

- 位置：`mod-tome.lua:35003`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`_t`
- 原文：`Improves senses, allowing the detection of unseen things.`
- 现译：`强化感知，可以看到看不到的东西。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00422 | HUMAN-REVIEW | cross-batch-080 | advisory | 润色与否 |  |  |

<details><summary>hrq-00422 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：Gemini“口语化但机制准确”成立
```
```
raw verdict: Gemini“口语化但机制基本准确”判断成立→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-080-01.md](reports/sol-080-01.md)。译文未修改。共 16 个 claim：8 confirmed、8 advisory、0 refuted、0 pending。 译文未修改。本组全部为 confirmed/advisory，无 refuted/pending；confirmed 中多条是「无缺陷」正面确认。
```
</details>

## entry-02614

- 位置：`mod-tome.lua:35068`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`tformat`
- 原文：`You have expended the power of your Radiance temporarily reducing its radius to 1.`
- 现译：`你消耗了光辉之力，暂时把光照半径降低到 1 码。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00423 | HUMAN-REVIEW | cross-batch-081 | advisory | 是否复现技能专名 |  |  |

<details><summary>hrq-00423 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“光照半径”机制准确，非误译
```
```
raw verdict: “光照半径”机制准确，非误译（最多技能名指代不鲜明）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02636

- 位置：`mod-tome.lua:35331`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`_t`
- 原文：`#Target# is afflicted by ghoul rot!`
- 现译：`#Target#被食尸鬼的疾病感染！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00424 | HUMAN-REVIEW | cross-batch-081 | confirmed | 统一策略 |  |  |

<details><summary>hrq-00424 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：同一 `GHOUL_ROT` 效果命名不一致（“食尸鬼的疾病” vs 固定简中“尸鬼腐蚀”）
```
```
raw verdict: 同一 GHOUL_ROT 效果命名不一致（“食尸鬼的疾病” vs 固定简中“尸鬼腐蚀”）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02637

- 位置：`mod-tome.lua:35332`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`_t`
- 原文：`#Target# is free from the ghoul rot.`
- 现译：`#Target#摆脱了食尸鬼的疾病。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00425 | HUMAN-REVIEW | cross-batch-081 | confirmed | 与 02636 一并 |  |  |

<details><summary>hrq-00425 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：移除提示同样不一致，**需与 02636 同策略、不能单边改**
```
```
raw verdict: 移除提示同样不一致（需与 02636 同策略，不能单边改）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02638

- 位置：`mod-tome.lua:35347`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`tformat`
- 原文：`#Target# warded against %s!`
- 现译：`#Target#吸收了%s的攻击！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00426 | HUMAN-REVIEW | cross-batch-081 | confirmed | 句式重写 |  |  |

<details><summary>hrq-00426 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“吸收了%s的攻击”把获得状态误写成已承受攻击（明确语义错误）
```
```
raw verdict: “吸收了%s的攻击”把 on_gain 误写成已承受攻击（明确语义错误）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02640

- 位置：`mod-tome.lua:35379`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`_t`
- 原文：`#Target# is focused by an arcane vortex!`
- 现译：`#Target#被奥术漩涡围绕！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00427 | HUMAN-REVIEW | cross-batch-081 | refuted | 无 |  |  |

<details><summary>hrq-00427 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：“被奥术漩涡围绕”准确，无需拘泥 `focused by` 字面
```
```
raw verdict: “被奥术漩涡围绕”准确表达实际空间关系（无需拘泥 focused by 字面）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02643

- 位置：`mod-tome.lua:35393`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`tformat`
- 原文：`The target is afflicted with a magical poison and is suffering %0.2f arcane damage per turn.  All resistances are reduced by 10%%%s.`
- 现译：`目标被魔法毒素感染，每回合受到 %0.2f 奥术伤害，所有伤害抗性下降 10%% %s。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00428 | HUMAN-REVIEW | cross-batch-081 | confirmed | 删空格 |  |  |

<details><summary>hrq-00428 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`10%% %s` 前多加半角空格（可见排版缺陷）
```
```
raw verdict: `10%% %s` 在 %s 前多加半角空格（确定的可见排版缺陷）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02644

- 位置：`mod-tome.lua:35394`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`tformat`
- 原文：` and poison resistance is reduced by %s%%`
- 现译：`，且毒素抗性下降 %s%%`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00429 | HUMAN-REVIEW | cross-batch-081 | refuted | 无（修复归 02643） |  |  |

<details><summary>hrq-00429 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：空格责任在 02643；本条全角逗号拼接正确
```
```
raw verdict: 异常空格责任在 02643；本条开头全角逗号拼接正确→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-081-01.md](reports/sol-081-01.md)。译文未修改。共 7 个 claim：4 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。两条 refuted 明确了**修复责任边界**：02643 删空格即可，02644 不动。
```
</details>

## entry-02688

- 位置：`mod-tome.lua:35800`（tome）｜section：`mod-tome/data/timed_effects/magical.lua`｜source_tag：`_t`
- 原文：`#Target# picks up the remains of its fallen comrade.`
- 现译：`#Target# 捡起了同伴的骨头。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00430 | HUMAN-REVIEW | cross-batch-082 | confirmed |  |  |  |

<details><summary>hrq-00430 · HUMAN-REVIEW 详情</summary>

```
作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-082-01.md](reports/sol-082-01.md)。译文未修改。共 4 个 claim：1 confirmed、2 refuted、1 advisory、0 pending。

| Claim | Sol 分档 | 人工待决 |
| --- | --- | --- |
| `fallen` 未明确落词 | confirmed（轻微）：译文无“倒下/阵亡”对应成分 | 是否要求逐词保留（可改“倒下同伴的骸骨”） |
| “核心语境信息丢失” | **refuted**：效果只在骷髅/骨巨人死亡粉碎时触发，“捡骨头”已强烈暗示死亡 | 无 |
| `remains`→“骨头”语义偏差 | **refuted**：源码即 `bones` 拾取消费逻辑，贴合机制 | 无（仅文体） |
| “骨头”风格降级 | advisory：技能说明本身用 `bones`，语境自然一致 | 文体裁决 |

译文未修改。Gemini 的「存在疑点」被 Sol 拆解为 1 confirmed（轻微）+ 2 refuted + 1 advisory——**条目级标签不等于条目被整体确认**。
```
```
raw verdict: `fallen` 未被明确译出（轻微完整性）→confirmed; “核心语境信息丢失”的进一步判断（骷髅死亡语境已强烈暗示）→refuted; `remains`→“骨头”构成语义偏差（源码即粉碎后的 bones）→refuted; “骨头”较“遗骸／残骸”风格降级（纯文体偏好）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-082-01.md](reports/sol-082-01.md)。译文未修改。共 4 个 claim：1 confirmed、2 refuted、1 advisory、0 pending。 译文未修改。Gemini 的「存在疑点」被 Sol 拆解为 1 confirmed（轻微）+ 2 refuted + 1 advisory——**条目级标签不等于条目被整体确认**。
```
</details>

## entry-02694

- 位置：`mod-tome.lua:35928`（tome）｜section：`mod-tome/data/timed_effects/mental.lua`｜source_tag：`tformat`
- 原文：`The gloom has stunned the target, reducing damage by 50%%, putting 4 random talents on cooldown and reducing movement speed by 50%%.  While stunned talents cooldown twice as slow.`
- 现译：`目标被黑暗光环震慑，伤害降低 50%%，随机 4 个技能进入 CD，移动速度降低 50%%。在震慑时技能冷却速度变慢一倍。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00431 | HUMAN-REVIEW | cross-batch-083 | confirmed | 术语裁定；改写表述 |  |  |

<details><summary>hrq-00431 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：pending：“CD”与既有术语不一致（需冻结术语输入）；confirmed：“冷却速度变慢一倍”表述含混；confirmed：两个 `50%%` 正确
```
```
raw verdict: “CD”与既有术语不一致→pending; “技能冷却速度变慢一倍”表述含混→confirmed; 两个 `50%%` 均正确保留→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-083-01.md](reports/sol-083-01.md)。译文未修改。共 7 个 claim：3 confirmed、2 advisory、1 refuted、1 pending。 译文未修改。1 pending 等术语库输入；refuted 表明 Gemini 的触发条件质疑不成立。
```
</details>

## entry-02700

- 位置：`mod-tome.lua:35945`（tome）｜section：`mod-tome/data/timed_effects/mental.lua`｜source_tag：`tformat`
- 原文：`Stalking %s. Bonus level %d: +%d accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit.`
- 现译：`追踪 %s. 等级 %d：+%d 命中，+%d%% 近战伤害，攻击目标时 +%0.2f 仇恨/回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00432 | HUMAN-REVIEW | cross-batch-083 | confirmed | 句点/术语体例 |  |  |

<details><summary>hrq-00432 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：占位符数量/顺序/数值来源正确；**refuted**：“攻击目标时”已准确表达触发条件；advisory：`%s` 后半角句点；advisory：“Bonus level”简化
```
```
raw verdict: 占位符数量、顺序和数值来源正确→confirmed; “攻击目标时”准确表达触发条件→refuted; `%s` 后保留半角句点→advisory; “Bonus level”简化为“等级”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-083-01.md](reports/sol-083-01.md)。译文未修改。共 7 个 claim：3 confirmed、2 advisory、1 refuted、1 pending。 译文未修改。1 pending 等术语库输入；refuted 表明 Gemini 的触发条件质疑不成立。
```
</details>

## entry-02735

- 位置：`mod-tome.lua:36391`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`Armor increased by %d, deals %d ice damage when hit in melee.`
- 现译：`护甲增加 %d，获得 %d 冰系近战反伤。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00433 | HUMAN-REVIEW | cross-batch-084 | confirmed | 术语裁定 |  |  |

<details><summary>hrq-00433 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“近战反伤”机制准确、参数顺序正确；pending：`ice`→“寒冰”需术语条目
```
```
raw verdict: “近战受击反伤”是机制准确的压缩表达，参数顺序正确→confirmed; `ice` 应译“寒冰”（需 terminology/combat.tsv，冻结输入不含）→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02740

- 位置：`mod-tome.lua:36441`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`The more you use taints, the longer they will take to recharge (+%d cooldowns).`
- 现译：`你使用堕落印记的次数越多，堕落印记的冷却时间越长 (+%d 冷却时间)。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00434 | HUMAN-REVIEW | cross-batch-084 | confirmed | 术语裁定 |  |  |

<details><summary>hrq-00434 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：TAINT_COOLDOWN 占位符完整；pending：`taints` preferred 译法
```
```
raw verdict: TAINT_COOLDOWN 占位符与机制含义完整→confirmed; `taints` preferred 译法“污印”及旧称呼应（不在冻结输入内）→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02747

- 位置：`mod-tome.lua:36505`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`#Target#'s lifeline is being severed!`
- 现译：`#Target#的生命线被收割了！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00435 | HUMAN-REVIEW | cross-batch-084 | confirmed | 改译 |  |  |

<details><summary>hrq-00435 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`severed`→“被收割了”词义偏差（应为生命线被切断）
```
```
raw verdict: `severed`→“被收割了”词义偏差（源码为 lifeline 被切断）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02759

- 位置：`mod-tome.lua:36574`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`The target is enveloped in a shroud that seems to hang upon it like a heavy burden. (Reduces damage dealt by %d%%).`
- 现译：`目标笼罩在虚弱帷幕中（造成的伤害降低 %d%%）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00436 | HUMAN-REVIEW | cross-batch-084 | confirmed | 补译 |  |  |

<details><summary>hrq-00436 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`like a heavy burden` 漏译；advisory：“虚弱帷幕”语境化成立
```
```
raw verdict: `like a heavy burden` 完整描写成分漏译→confirmed; `a shroud`→“虚弱帷幕”语境化（效果名即 Shroud of Weakness）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02763

- 位置：`mod-tome.lua:36582`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`Horrible visions fill your mind.
#CRIMSON#Penalty : #WHITE#Plagued by Visions: Your mental save has a 20%% chance to be reduced by %d%% when tested.
#CRIMSON#Power 1+: %sRemoved from Reality: %+d Physical Resistance, %+d Maximum Physical Resistance
#CRIMSON#Power 2+: %s%+d Luck, %+d Willpower
#CRIMSON#Power 3+: %sHarrow: When a foe attempts to inflict a detrimental effect upon you, your harrowing aura retaliates against a random foe in range 10, dealing %d mind and %d darkness damage.
#CRIMSON#Power 4+: %sNightmare: Each time you are damaged by a foe there is a chance (currently %d%%) of triggering a radius %d nightmare (summon Terrors and chances to slow, deal %d Mind damage, and deal %d Darkness damage) for 8 turns. The chance grows each time you are struck but fades over time.`
- 现译：`你的脑海中充斥恐怖景象。
#CRIMSON# 惩罚：#WHITE# 扰乱幻象：受检定时，你的精神豁免有 20%%概率减少 %d%%
#CRIMSON# 强度 1+：%s 从现实消失：%+d 物理抗性，%+d 物理抗性上限
#CRIMSON# 强度 2+：%s%+d 幸运，%+d 意志
#CRIMSON# 强度 3+：%s 折磨：当敌人试图对你造成负面效果时，你的折磨光环会对 10 范围内的一个随机敌人进行报复，造成 %d 精神和 %d 暗影伤害。
#CRIMSON# 强度 4+：%s 噩梦：每次被敌人所伤有概率 (当前 %d%%) 触发一个范围为 %d 码的噩梦（有减速、召唤梦魇和直接造成%d精神、%d暗影伤害的效果）持续 8 回合。  触发几率  在每次你受到打击时提高，同时随时间下降。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00437 | HUMAN-REVIEW | cross-batch-084 | confirmed | 统一策略；改译 |  |  |

<details><summary>hrq-00437 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：15 参数正确、Harrow 词根不一、双空格；advisory：名动可不同词；pending：术语库合规；**confirmed（Sol 新增）**：`Plagued by Visions`→“扰乱幻象”语义倒置
```
```
raw verdict: 15 个格式参数类型与顺序均相符（`20%%` 为字面）→confirmed; Harrow 本条“折磨”与 entry-02764“惊扰”用词根不一→confirmed; 名动不必机械同词，但同一机制当前译法削弱对应识别→advisory; 末句两处连续双空格 `。  触发几率  在`→confirmed; “精神豁免、物理抗性等术语全部规范”缺冻结术语证据→pending; **Sol 未被指出**：`Plagued by Visions`→“扰乱幻象”语义倒置→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02764

- 位置：`mod-tome.lua:36593`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`logSeen`
- 原文：`#F53CBE#%s harrows %s!`
- 现译：`#F53CBE#%s惊扰%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00438 | HUMAN-REVIEW | cross-batch-084 | confirmed | 统一策略 |  |  |

<details><summary>hrq-00438 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：日志/颜色码完整、用词差异成立；advisory：“惊扰”语气偏弱
```
```
raw verdict: 同一 Harrow 触发日志，颜色码与两个 `%s` 完整保留→confirmed; 与 entry-02763“折磨”用词不同这一事实成立→confirmed; “惊扰”语气偏弱，是否必修取决于统一策略→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02765

- 位置：`mod-tome.lua:36600`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`Mayhem and destruction seem to follow you.
#CRIMSON#Penalty : #WHITE#Lost Fortune: You seem to find less gold in your journeys.
#CRIMSON#Power 1+: %sMissplaced Endeavours: The endeavours of those around you begin to fail (+%d%% chance to avoid traps).
#CRIMSON#Power 2+: %s%+d Luck, %+d Cunning
#CRIMSON#Power 3+: %sMissed Opportunities: Opportunities are fleeting, and those close to you begin to miss them (+%d%% evasion).
#CRIMSON#Power 4+: %sUnfortunate End: The damage you deal will increase by %d%% if the increase would be enough to kill your opponent.`
- 现译：`混乱与毁灭似乎追随着你。
#CRIMSON# 惩罚：#WHITE# 霉运：在你的旅途中找到的金币减少。
#CRIMSON# 强度 1+：%s 失败的努力：围绕你的努力都会失败  (+%d%% 避开陷阱的几率)。
#CRIMSON# 强度 2+：%s%+d 幸运，%+d 灵巧
#CRIMSON# 强度 3+：%s 错失良机：机会转瞬即逝，你身边的人会错失良机 (+%d%% 躲闪概率)。
#CRIMSON# 强度 4+：%s 厄运终结：如果提高后的伤害足够杀死对手的话，你将可以提高 %d%% 的伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00439 | HUMAN-REVIEW | cross-batch-084 | confirmed | 改译×2；术语核验 |  |  |

<details><summary>hrq-00439 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：Gemini 占位符计数 7 错（实际 9）；confirmed：9 参数保留、双空格；pending：术语核验；**confirmed×2（Sol 新增）**：`those around you` 主语误读、自动增伤被译成可选能力
```
```
raw verdict: Gemini“7 处占位符”计数错误（实际 9 个）→refuted; 译文保留全部 9 个参数，类型与顺序相符→confirmed; “术语对齐准确”无法在冻结输入内核验，且“闪避”概括不精确→pending; Power 1 行“失败”与左括号间连续双空格→confirmed; **Sol 未被指出**：`those around you` 误读为“围绕你的努力”→confirmed; **Sol 未被指出**：Power 4 自动增伤被译成可选择能力式表述→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-084-01.md](reports/sol-084-01.md)。译文未修改。共 22 个 claim：14 confirmed、4 pending、3 advisory、1 refuted。其中 **3 条 confirmed 是 Sol 自行发现、Gemini 未指出**。 译文未修改。本组是**双向纠错样本**：Sol 修正 Gemini 计数错误，同时补充 3 条 Gemini 漏掉的 confirmed。
```
</details>

## entry-02775

- 位置：`mod-tome.lua:36662`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: +10% cold damage, -10% cold resistance, -10% physical save, -20% confusion immunity.`
- 现译：`区域效果：+10% 寒冰伤害，-10% 寒冰抗性，-10% 物理豁免，-20% 混乱免疫。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00440 | HUMAN-REVIEW | cross-batch-085 | advisory | 批内统一 |  |  |

<details><summary>hrq-00440 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“寒冰”与本批“寒冷”同词不一致
```
```
raw verdict: “寒冰”与本批次“寒冷”批内不一致（同一 COLD）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02789

- 位置：`mod-tome.lua:36707`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`You are suffocating! Each turn you lose an ever increasing percent of your total life (currently %d%%)`
- 现译：`你正在窒息！每回合按比例损失生命，且越来越多（现在 %d%%）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00441 | HUMAN-REVIEW | cross-batch-085 | confirmed | 补“最大生命” |  |  |

<details><summary>hrq-00441 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：未说明比例基数（实为**最大生命**比例递增扣血）
```
```
raw verdict: 未明确损失的是最大生命比例（按 `max_life*dam/100` 扣血）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02790

- 位置：`mod-tome.lua:36739`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`logPlayer`
- 原文：`#STEEL_BLUE#You are brought back from your repreive!`
- 现译：`#STEEL_BLUE#被从避难所带了回去！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00442 | HUMAN-REVIEW | cross-batch-085 | confirmed | 改“带了回来” |  |  |

<details><summary>hrq-00442 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：缺“你”可省；confirmed：“带了回去”方向不当
```
```
raw verdict: 缺“你”致句式生硬（日志语境可省主语，非语法错误）→advisory; “带了回去”方向不当（日志出现时角色已回到来源地点）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02791

- 位置：`mod-tome.lua:36742`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`delayedLogMessage`
- 原文：`#STEEL_BLUE##Source# shares damage with %s fugue clones!`
- 现译：`#STEEL_BLUE##Source#和%s时空克隆共享伤害！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00443 | HUMAN-REVIEW | cross-batch-085 | pending | 需另供对照条目 |  |  |

<details><summary>hrq-00443 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：占位符句式成立（`%s`=所有格代词）；pending：“时空克隆/复制体”不一致待对照
```
```
raw verdict: 占位符形成不通顺句子（`%s` 为所有格代词，本地化后结构成立）→refuted; “时空克隆”与“时空复制体”批内不一致（关联译文不在冻结批次）→pending
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02798

- 位置：`mod-tome.lua:36788`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: +20 magic, +2 mana regen, -20 accuracy, -20 stealth power.`
- 现译：`区域效果：+20 魔法，+2 法力回复，-20 命中，-20 潜行强度。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00444 | HUMAN-REVIEW | cross-batch-085 | confirmed | 术语裁定 |  |  |

<details><summary>hrq-00444 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Magic`→“魔法”混淆核心属性（应为“魔力”）
```
```
raw verdict: 核心属性 `Magic` 译作“魔法”（应为核心属性名，通常“魔力”）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02801

- 位置：`mod-tome.lua:36794`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: Air decreases over time. If you run out of air you will start losing life. Look for bubbles to recover air. The water also reduces stun resistance by 10% and fire damage is reduced by 10%, however cold damage is increased by 10%.`
- 现译：`区域效果： 空气值随时间损失，空气用光后将损失生命。寻找气泡来回复空气值。水同时令震慑免疫和火焰伤害下降 10%，同时增加 10% 寒冷伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00445 | HUMAN-REVIEW | cross-batch-085 | advisory | 润色 |  |  |

<details><summary>hrq-00445 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：冒号后空格、连续两次“同时”
```
```
raw verdict: 冒号后多余半角空格、连续两次“同时”→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02805

- 位置：`mod-tome.lua:36800`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: The power of the Spellblaze still burns here. -10% resistance to fire, arcane and blight damage, but +10% cold resistance. WARNING: The powerful magic here reflects teleportation magic!`
- 现译：`区域效果：魔法大爆炸的火焰仍在燃烧，-10% 火焰、枯萎、奥术抗性，+10% 寒冷抗性。警告：强大的魔法能量可能干扰传送法术！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00446 | HUMAN-REVIEW | cross-batch-085 | confirmed | 恢复确定语气；机制另行核查 |  |  |

<details><summary>hrq-00446 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：“反射传送”被改成“可能干扰”（确定性被改）；**refuted**：“burns”火焰隐喻译法非错误。**附注**：Sol 指出该状态 `activate` 未实现传送反射，英文描述本身待另行核查
```
```
raw verdict: “反射传送魔法”被改成“可能干扰传送法术”（确定性与性质被改）→confirmed; “The power … burns”译“火焰仍在燃烧”构成错误（原句即火焰隐喻）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02806

- 位置：`mod-tome.lua:36802`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: Strong scents fill the air and make you feel drowsy. If the timer reaches 0 you will fall into a dreaming sleep state. -10% mind resistance, -20% sleep resistance, +10% nature damage.`
- 现译：`区域效果： 强烈的气味充满了空气，让你感觉困倦。倒计时结束时，你将进入梦境。-10% 精神抗性，-20% 睡眠免疫，+10% 自然伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00447 | HUMAN-REVIEW | cross-batch-085 | advisory | 润色 |  |  |

<details><summary>hrq-00447 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory×2：冒号后空格；“进入梦境”弱化“沉睡”状态
```
```
raw verdict: 冒号后多余半角空格→advisory; “进入梦境”弱化“陷入沉睡”状态（数值无误）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02807

- 位置：`mod-tome.lua:36804`（tome）｜section：`mod-tome/data/timed_effects/other.lua`｜source_tag：`_t`
- 原文：`Zone-wide effect: A huge thunderstorm rages above you. +10 lightning damage, -10% stun resistance.`
- 现译：`区域效果： 强大的雷暴在你头顶轰鸣。+10% 闪电伤害，-10% 震慑免疫。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00448 | HUMAN-REVIEW | cross-batch-085 | advisory | 只清空格 |  |  |

<details><summary>hrq-00448 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：冒号后空格；**refuted**：译文补 `%` 正确（源码 `inc_damage=10` 即百分比）
```
```
raw verdict: 冒号后多余半角空格→advisory; 补出英文遗漏的 `%` 造成错误（源码实为百分比增幅，译法准确）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-085-01.md](reports/sol-085-01.md)。译文未修改。共 14 个 claim：4 confirmed、6 advisory、3 refuted、1 pending。 译文未修改。entry-02805 附带一个**超出英中忠实度的机制疑问**（状态是否真反射传送），已按原文记录待人工另行核查。
```
</details>

## entry-02828

- 位置：`mod-tome.lua:37132`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`Improves senses, allowing the detection of unseen things.`
- 现译：`强化感知，可以看到看不到的东西。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00449 | HUMAN-REVIEW | cross-batch-086 | advisory | 润色 |  |  |

<details><summary>hrq-00449 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：“看到看不到的东西”偏口语，detection 比“看到”稍窄
```
```
raw verdict: “看到看不到的东西”偏口语，且 detection 范围比“看到”稍窄（不反转机制）→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-086-01.md](reports/sol-086-01.md)。译文未修改。共 8 个 claim：3 confirmed、3 advisory、2 refuted、0 pending。 译文未修改。02849/02850 是**同组整体问题**：Sol 明确 refuted 单方归因，宿主模板与两个片段需一并处理。
```
</details>

## entry-02830

- 位置：`mod-tome.lua:37192`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`#Target# prepares %s!`
- 现译：`#Target#准备了%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00450 | HUMAN-REVIEW | cross-batch-086 | confirmed | 联合两短语重定句型 |  |  |

<details><summary>hrq-00450 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`准备了%s` 与运行时短语结合后语法生硬
```
```
raw verdict: `准备了%s` 与运行时插入短语结合后语法生硬（“准备了为下一次击杀”不通顺）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-086-01.md](reports/sol-086-01.md)。译文未修改。共 8 个 claim：3 confirmed、3 advisory、2 refuted、0 pending。 译文未修改。02849/02850 是**同组整体问题**：Sol 明确 refuted 单方归因，宿主模板与两个片段需一并处理。
```
</details>

## entry-02846

- 位置：`mod-tome.lua:37383`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`logSeen`
- 原文：`%s has re-opened a cursed wound!`
- 现译：`%s再次遭受被诅咒的创伤！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00451 | HUMAN-REVIEW | cross-batch-086 | advisory | 文风 |  |  |

<details><summary>hrq-00451 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：意译可接受但弱化 wound re-opened 意象；合并还可能加深治疗削减
```
```
raw verdict: “再次遭受被诅咒的创伤”可接受意译，但弱化 wound re-opened 意象且合并还可能加深治疗削减→advisory
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-086-01.md](reports/sol-086-01.md)。译文未修改。共 8 个 claim：3 confirmed、3 advisory、2 refuted、0 pending。 译文未修改。02849/02850 是**同组整体问题**：Sol 明确 refuted 单方归因，宿主模板与两个片段需一并处理。
```
</details>

## entry-02849

- 位置：`mod-tome.lua:37431`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`each turn.`
- 现译：`每回合。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00452 | HUMAN-REVIEW | cross-batch-086 | confirmed | **与宿主、02850 整体裁决** |  |  |

<details><summary>hrq-00452 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`每回合。` 被重排进句中造成错误断句
```
```
raw verdict: `每回合。` 被插入宿主句中间产生错误断句（须与宿主、02850 一并裁决）→confirmed
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-086-01.md](reports/sol-086-01.md)。译文未修改。共 8 个 claim：3 confirmed、3 advisory、2 refuted、0 pending。 译文未修改。02849/02850 是**同组整体问题**：Sol 明确 refuted 单方归因，宿主模板与两个片段需一并处理。
```
</details>

## entry-02850

- 位置：`mod-tome.lua:37432`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`and is losing one physical effect turn.`
- 现译：`每回合失去一个物理效果并`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00453 | HUMAN-REVIEW | cross-batch-086 | confirmed | 宿主统一承担句号 |  |  |

<details><summary>hrq-00453 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：**refuted**：“每回合”有 `on_timeout` 依据；advisory：未涵盖维持战技；confirmed：缺句末标点；**refuted**：并非本条导致 02849 错误
```
```
raw verdict: 无依据加入“每回合”（`on_timeout` 逐回合路径，有源码依据）→refuted; “失去一个物理效果”未涵盖维持中的战技（轻微低估范围）→advisory; 当前分支拼装缺少句末标点（宜由宿主模板统一承担）→confirmed; 前置从句设计本身导致 02849 错误（02849 直接原因是自带句号被重排句中）→refuted
```
```
段末说明：作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-086-01.md](reports/sol-086-01.md)。译文未修改。共 8 个 claim：3 confirmed、3 advisory、2 refuted、0 pending。 译文未修改。02849/02850 是**同组整体问题**：Sol 明确 refuted 单方归因，宿主模板与两个片段需一并处理。
```
</details>

## entry-02856

- 位置：`mod-tome.lua:37514`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`#Target# defiantly reasserts %s connection to nature!`
- 现译：`#Target#重新和自然建立%s联系！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00454 | HUMAN-REVIEW | cross-batch-087 | confirmed | 是否补语气；结合本地化 `his/her/its` 重定句式 |  |  |

<details><summary>hrq-00454 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`defiantly` 漏译（语气丢失，机制/占位符无损）；**refuted**：`%s` 语序顺畅之说（`his_her` 为所有格，现译“建立他的/她的联系”欠自然）
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-087-01.md](reports/sol-087-01.md)。译文未修改。共 7 个 claim：5 confirmed、1 refuted、1 advisory。 译文未修改。本条 refuted 说明 Gemini 的“语序顺畅”判断不成立；02866 属同效果内专名一致性问题。
```
</details>

## entry-02858

- 位置：`mod-tome.lua:37532`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`The target stands strong, increasing all resistances by %0.1f%% and resistance caps by %0.1f%%.`
- 现译：`目标十分强大，增加全体抗性 %0.1f%%, 全体抗性上限 %0.1f%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00455 | HUMAN-REVIEW | cross-batch-087 | confirmed | 改“屹立不倒”类表达；标点统一 |  |  |

<details><summary>hrq-00455 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：两个 `%0.1f%%` 顺序与 `resists.all`/`resists_cap.all` 对应正确；confirmed：`stands strong`→“十分强大”语义偏移（应为挺立/屹立）；confirmed：半角逗号排版
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-087-01.md](reports/sol-087-01.md)。译文未修改。共 7 个 claim：5 confirmed、1 refuted、1 advisory。 译文未修改。本条 refuted 说明 Gemini 的“语序顺畅”判断不成立；02866 属同效果内专名一致性问题。
```
</details>

## entry-02866

- 位置：`mod-tome.lua:37558`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`logSeen`
- 原文：`Some leeches drop off %s!`
- 现译：`寄生虫从%s处脱落！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00456 | HUMAN-REVIEW | cross-batch-087 | confirmed | 统一为“部分寄生水蛭……”；`%s` 搭配“身上/处” |  |  |

<details><summary>hrq-00456 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`leeches`→“寄生虫”与同效果 02861–02865“寄生水蛭”不一致，且 `Some`“部分/一些”未体现
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-087-01.md](reports/sol-087-01.md)。译文未修改。共 7 个 claim：5 confirmed、1 refuted、1 advisory。 译文未修改。本条 refuted 说明 Gemini 的“语序顺畅”判断不成立；02866 属同效果内专名一致性问题。
```
</details>

## entry-02891

- 位置：`mod-tome.lua:37712`（tome）｜section：`mod-tome/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`#Target##OLIVE_DRAB# no longer resonates with %s%s#LAST# damage!`
- 现译：`#Target##OLIVE_DRAB# 不再和%s%s#LAST#伤害共鸣！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00457 | HUMAN-REVIEW | cross-batch-087 | advisory | 中文排版惯例取舍（改 02891 或同时给 02890 保留） |  |  |

<details><summary>hrq-00457 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`#OLIVE_DRAB#` 后半角空格（02890 已删、02891 保留，均源自英文原文）；标签与 2 占位符结构完好
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-087-01.md](reports/sol-087-01.md)。译文未修改。共 7 个 claim：5 confirmed、1 refuted、1 advisory。 译文未修改。本条 refuted 说明 Gemini 的“语序顺畅”判断不成立；02866 属同效果内专名一致性问题。
```
</details>

## entry-02921

- 位置：`mod-tome.lua:37978`（tome）｜section：`mod-tome/data/zones/arena/zone.lua`｜source_tag：`log`
- 原文：`%sClear bonus: %s%s%s! Score bonus: %s%s%s! Danger bonus: %s%s%s! Rank bonus: %s%s%s!`
- 现译：`%s全清奖励：%s%s%s! 分数奖励：%s%s%s! 危险度奖励：%s%s%s! 级别奖励：%s%s%s！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00458 | HUMAN-REVIEW | cross-batch-088 | confirmed | 是否统一为全角（或保留 ASCII 分隔） |  |  |

<details><summary>hrq-00458 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：四项奖励分句前三处半角 `! `、末处全角 `！`，原文统一半角；13 个 `%s` 与颜色码完好
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-088-01.md](reports/sol-088-01.md)。译文未修改。3 个 claim 全部 confirmed，无 refuted/pending。 译文未修改。三条均为排版/用词层面的真实但轻微问题。
```
</details>

## entry-02927

- 位置：`mod-tome.lua:38083`（tome）｜section：`mod-tome/data/zones/charred-scar/npcs.lua`｜source_tag：`tformat`
- 原文：`Go %s! We will hold the line!`
- 现译：`去吧%s!我们会坚守防线！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00459 | HUMAN-REVIEW | cross-batch-088 | confirmed | 至少首处改全角；可选更自然呼语语序 |  |  |

<details><summary>hrq-00459 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`去吧%s!我们会坚守防线！` 标点不一致、句界不佳；`%s` 功能正确
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-088-01.md](reports/sol-088-01.md)。译文未修改。3 个 claim 全部 confirmed，无 refuted/pending。 译文未修改。三条均为排版/用词层面的真实但轻微问题。
```
</details>

## entry-02929

- 位置：`mod-tome.lua:38122`（tome）｜section：`mod-tome/data/zones/conclave-vault/npcs.lua`｜source_tag：`entity name`
- 原文：`degenerated ogric mass`
- 现译：`退化的食人魔碎肉`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00460 | HUMAN-REVIEW | cross-batch-088 | confirmed | `mass` 改“血肉团/聚合体”；`degenerated` 命名策略 |  |  |

<details><summary>hrq-00460 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`degenerated ogric mass`→“退化的食人魔碎肉”与 `huge mass of deformed flesh` 形态不符
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-088-01.md](reports/sol-088-01.md)。译文未修改。3 个 claim 全部 confirmed，无 refuted/pending。 译文未修改。三条均为排版/用词层面的真实但轻微问题。
```
</details>

## entry-02937

- 位置：`mod-tome.lua:38228`（tome）｜section：`mod-tome/data/zones/daikara/zone.lua`｜source_tag：`_t`
- 原文：`BOOM!`
- 现译：`火山喷发！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00461 | HUMAN-REVIEW | cross-batch-089 | advisory | 是否统一保留拟声（“轰！”类） |  |  |

<details><summary>hrq-00461 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：advisory：`BOOM!`→“火山喷发！”与正文语境一致，仅损失拟声突发感，非缺陷
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-089-01.md](reports/sol-089-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。02937 的 Gemini 观察被裁为非缺陷（advisory），未升级。
```
</details>

## entry-02957

- 位置：`mod-tome.lua:38422`（tome）｜section：`mod-tome/data/zones/dreams/zone.lua`｜source_tag：`_t`
- 原文：`Dream ???`
- 现译：`梦境 ??？`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00462 | HUMAN-REVIEW | cross-batch-089 | confirmed | 统一为“？？？”或保留“???” |  |  |

<details><summary>hrq-00462 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Dream ???`→“梦境 ??？”确为两个半角 `?` + 一个全角 `？`
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-089-01.md](reports/sol-089-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。02937 的 Gemini 观察被裁为非缺陷（advisory），未升级。
```
</details>

## entry-02967

- 位置：`mod-tome.lua:38557`（tome）｜section：`mod-tome/data/zones/golem-graveyard/npcs.lua`｜source_tag：`_t`
- 原文：`ACTIVATING PAIN GIVING SUBMODULES!`
- 现译：`启动痛苦强化模组！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00463 | HUMAN-REVIEW | cross-batch-089 | confirmed | 改“致痛子模块”类表达 |  |  |

<details><summary>hrq-00463 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`PAIN GIVING SUBMODULES` 意为“施加痛苦”，译“痛苦强化”词义偏移且弱化 `sub-`；纯喊话无机制影响
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-089-01.md](reports/sol-089-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。 译文未修改。02937 的 Gemini 观察被裁为非缺陷（advisory），未升级。
```
</details>

## entry-02973

- 位置：`mod-tome.lua:38568`（tome）｜section：`mod-tome/data/zones/golem-graveyard/objects.lua`｜source_tag：`_t`
- 原文：`One of the ruby eyes of the legendary giant golem Atamathon.
It is said it was made by the halflings during the Age of Pyre as a weapon against the orcs. Even though it was destroyed, it managed to deal a crippling blow by killing their leader, Garkul the Devourer.`
- 现译：`传奇巨型傀儡阿塔玛森的红宝石眼睛之一。
据说它是半身人在烈火纪为了对抗兽人所造的武器。虽然它被破坏了，但是它也成功地使对方的首领吞噬者加库尔走向死亡。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00464 | HUMAN-REVIEW | cross-batch-090 | confirmed | 是否补“给对方以重创” |  |  |

<details><summary>hrq-00464 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`deal a crippling blow`（对兽人阵营的重创）未译出，仅保留杀死加库尔的事实
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-090-01.md](reports/sol-090-01.md)。译文未修改。3 个 claim：2 confirmed、1 advisory。
```
</details>

## entry-02982

- 位置：`mod-tome.lua:38735`（tome）｜section：`mod-tome/data/zones/high-peak/grids.lua`｜source_tag：`_t`
- 原文：`A farportal is a way to travel incredible distances in the blink of an eye. They usually require an external item to use. You have no idea if it is even two-way.
This one seems to go to an unknown place, seemingly out of this world. You dare not use it.`
- 现译：`传送门是可以在眨眼间将你传送出很远距离的工具。它们通常需要一件关键道具来激活。你不知道这道门是否为双向的。
这道门似乎通向未知之地，似乎为世外之地，你不太敢使用它。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00465 | HUMAN-REVIEW | cross-batch-090 | confirmed | 正文是否统一专用名；可选合并重复 |  |  |

<details><summary>hrq-00465 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：正文 `A farportal` 简称“传送门”，与同 section 实体名“远行传送门”不一致；advisory：连续“似乎”源自原文 `seems/seemingly`，非忠实度错误
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-090-01.md](reports/sol-090-01.md)。译文未修改。3 个 claim：2 confirmed、1 advisory。
```
</details>

## entry-03023

- 位置：`mod-tome.lua:39312`（tome）｜section：`mod-tome/data/zones/paradox-plane/npcs.lua`｜source_tag：`entity name`
- 原文：`Epoch`
- 现译：`纪元`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00466 | HUMAN-REVIEW | cross-batch-091 | confirmed | 以“亚伯契”为规范还是废弃旧译统一“纪元”（需术语策略裁决并全链同步） |  |  |

<details><summary>hrq-00466 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Epoch` 为悖论位面唯一实体名；本批冻结术语 `Epoch→亚伯契`（T.PN.PERSON）及固定 zh_hans `t("Epoch","亚伯契","entity name")`
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-091-02.md](reports/sol-091-02.md)。译文未修改。3 个 claim 全部 confirmed。 说明：首次派发 sol-091-01 时宿主 cross 包误指 batch-092，其「Gemini 快照依据不存在」的推理无效；已更正输入并改派 sol-091-02，下列结论以替代复核为准（原报告 [sol-091-01.md](reports/sol-091-01.md) 仅作历史留档）。 译文未修改。本组暴露的是既有译文与冻结术语/旧版 locale 的专名体系冲突，不是运行时缺陷。
```
</details>

## entry-03025

- 位置：`mod-tome.lua:39318`（tome）｜section：`mod-tome/data/zones/paradox-plane/objects.lua`｜source_tag：`entity name`
- 原文：`Epoch's Curve`
- 现译：`纪元之弧`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00467 | HUMAN-REVIEW | cross-batch-091 | confirmed | 后半“的弧线/之弧”中文措辞可另行润色 |  |  |

<details><summary>hrq-00467 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：`Epoch's Curve`→“纪元之弧”偏离冻结术语约束与固定既有名“亚伯契的弧线”；术语快照在 Epoch 条注释中点名该神器
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-091-02.md](reports/sol-091-02.md)。译文未修改。3 个 claim 全部 confirmed。 说明：首次派发 sol-091-01 时宿主 cross 包误指 batch-092，其「Gemini 快照依据不存在」的推理无效；已更正输入并改派 sol-091-02，下列结论以替代复核为准（原报告 [sol-091-01.md](reports/sol-091-01.md) 仅作历史留档）。 译文未修改。本组暴露的是既有译文与冻结术语/旧版 locale 的专名体系冲突，不是运行时缺陷。
```
</details>

## entry-03027

- 位置：`mod-tome.lua:39320`（tome）｜section：`mod-tome/data/zones/paradox-plane/objects.lua`｜source_tag：`_t`
- 原文：`Epoch's Curve has served the Wardens for generations and was passed from Warden to Warden for many years before being lost.
According to legend it was made from the first ash sapling to sprout after the Spellblaze and carries powers of both time and renewal.`
- 现译：`在纪元之弧失踪前，它已经世世代代服务于守卫，在守卫之间辗转相传多年。
根据传说，它是用魔法大爆炸后第一棵抽芽的白蜡树苗制成，拥有时空和恢复的力量。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00468 | HUMAN-REVIEW | cross-batch-091 | confirmed | 随 03025 一并处理 |  |  |

<details><summary>hrq-00468 · HUMAN-REVIEW 详情</summary>

```
Sol 分档：confirmed：描述正文重复同一神器名，必须与 03025 同步改，否则名称/说明不一致
```
```
段末说明：作者是 Pi/CPA/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-091-02.md](reports/sol-091-02.md)。译文未修改。3 个 claim 全部 confirmed。 说明：首次派发 sol-091-01 时宿主 cross 包误指 batch-092，其「Gemini 快照依据不存在」的推理无效；已更正输入并改派 sol-091-02，下列结论以替代复核为准（原报告 [sol-091-01.md](reports/sol-091-01.md) 仅作历史留档）。 译文未修改。本组暴露的是既有译文与冻结术语/旧版 locale 的专名体系冲突，不是运行时缺陷。
```
</details>

## entry-03058

- 位置：`mod-tome.lua:39725`（tome）｜section：`mod-tome/data/zones/shertul-fortress/grids.lua`｜source_tag：`log`
- 原文：`#VIOLET#You enter the swirling portal and in the blink of an eye you set foot in a strangely familiar zone, right next to a farportal...`
- 现译：`#VIOLET#你进入了传送漩涡，一眨眼功夫你发现你到了一个熟悉的地方，在另一个远行传送门旁边……`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00469 | cross-092 | cross-batch-092 | confirmed | 原文中的 `strangely` 漏译 |  |  |
| hrq-00470 | cross-092 | cross-batch-092 | confirmed | 遗漏 `strangely` 弱化了“熟悉但异样”的叙事反差 |  |  |

<details><summary>hrq-00469 · cross-092 详情</summary>

```
**结论：confirmed**

**证据：**

- 固定源码 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
- 源码路径：`game/modules/tome/data/zones/shertul-fortress/grids.lua:124`
- 原文为：
  > `you set foot in a strangely familiar zone`
- 冻结译文为：
  > `你发现你到了一个熟悉的地方`

译文表达了 `familiar` 的“熟悉”，但没有对应 `strangely` 的“奇怪地、莫名地、异样地”等含义，因此属于可客观确认的语义细节遗漏。

**影响：**

不影响运行、格式、颜色标记或游戏机制；影响限于叙事忠实度。玩家仍能理解到达了熟悉场所，但无法从这句日志中直接感受到这种熟悉感本身带有异常或难以解释之处。

**人工待决点：**

需由维护者决定是否将这一细微遗漏纳入修复范围。若修复，可考虑表达为“一个莫名熟悉的地方”或“一个异样地熟悉的区域”；具体措辞属于文风裁决。

---
```
</details>

<details><summary>hrq-00470 · cross-092 详情</summary>

```
**结论：confirmed**

**证据：**

同一固定版本中，传送目标明确是特殊地点 `caldizar-space-fortress`：

- `game/modules/tome/data/zones/shertul-fortress/grids.lua:120-125`
  - 第 120 行注释为 `Caldizar space fortress`
  - 第 122 行切换至 `shertul-fortress-caldizar`
  - 第 124 行使用 `strangely familiar zone`

进入该区域后的后续文本进一步明确这种反差：

- `game/modules/tome/data/zones/shertul-fortress-caldizar/zone.lua:74`
  > `somewhere familiar. The smooth walls and gentle lighting remind you of your fortress. And yet it feels different too.`

即“某处很熟悉……让你想起自己的堡垒，但感觉又有所不同”。因此，`strangely familiar` 并非无关紧要的泛化修饰，而是在提前建立“似曾相识却不正常”的叙事基调。现译仅保留“熟悉”，确实削弱了这一反差。

**影响：**

属于轻微叙事语气和信息完整性问题，不影响剧情流程或机制理解。由于紧接着的区域进入文本仍会说明“熟悉但不同”，整体剧情信息没有丢失，只是首条传送日志的铺垫力度下降。

**人工待决点：**

是否要求首条日志完整保留这层反差，属于译文质量阈值判断。若当前批次只处理明显误译，可记为低优先级；若要求细节忠实，则有充分依据修正。Gemini 所称“细微观察”可作为严重度参考，但其标签本身不构成裁决依据。
```
</details>

## entry-03092

- 位置：`mod-tome.lua:40038`（tome）｜section：`mod-tome/data/zones/telmur/npcs.lua`｜source_tag：`_t`
- 原文：`Everybody thought Telos dead and his spirit destroyed, but it seems he still lingers in his old place of power.`
- 现译：`所有人都认为泰勒已经形神俱灭了，但现在看起来他似乎仍徘徊在他旧日的力量之所。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00471 | batch-093(待交叉) |  | 存在疑点 |  |  |  |

<details><summary>hrq-00471 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40038`；`mod-tome/data/zones/telmur/npcs.lua`
- **原文**：`Everybody thought Telos dead and his spirit destroyed, but it seems he still lingers in his old place of power.`
- **译文**：`所有人都认为泰勒已经形神俱灭了，但现在看起来他似乎仍徘徊在他旧日的力量之所。`
- **复核结论**：存在疑点
- **依据**：专名翻译在同 section 语境及上下文中不一致。同 section 的 `mod-tome.lua:40037` 为 `t("The Shade of Telos", "泰勒斯之影", "entity name")`，`mod-tome.lua:40046` 为 `t("Telos's Staff (Bottom Half)", "泰勒斯的法杖（下半部）", "entity name")`，`mod-tome.lua:40048` 为 `t("The bottom part of Telos' broken staff.", "泰勒斯折断法杖的下半部。", "_t")`，均统一译为“泰勒斯”。此处译文将人名“Telos”误译为了“泰勒”，容易与主线 NPC 泰恩（Tannen）或泰尔兰（Tarelion）产生混淆。
```
</details>

## entry-03112

- 位置：`mod-tome.lua:40275`（tome）｜section：`mod-tome/data/zones/town-derth/traps.lua`｜source_tag：`entity name`
- 原文：`Swordsmith`
- 现译：`铸剑铺`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00472 | batch-093(待交叉) |  | 存在疑点 |  |  |  |

<details><summary>hrq-00472 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40275`；`mod-tome/data/zones/town-derth/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。相关术语快照明确登记：`Swordsmith | 长剑铁匠铺 | T.GAME.ENTITY | places | entity name | existing | core | 城镇商店实体`。当前译文采用了“铸剑铺”，与术语快照指定的“长剑铁匠铺”不一致。
```
</details>

## entry-03114

- 位置：`mod-tome.lua:40313`（tome）｜section：`mod-tome/data/zones/town-elvala/traps.lua`｜source_tag：`entity name`
- 原文：`Swordsmith`
- 现译：`铸剑铺`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00473 | batch-093(待交叉) |  | 存在疑点 |  |  |  |

<details><summary>hrq-00473 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40313`；`mod-tome/data/zones/town-elvala/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。同 entry-03112，术语快照登记为“长剑铁匠铺”（城镇商店实体），当前译文为“铸剑铺”。
```
</details>

## entry-03118

- 位置：`mod-tome.lua:40361`（tome）｜section：`mod-tome/data/zones/town-gates-of-morning/traps.lua`｜source_tag：`entity name`
- 原文：`Sarah's Herbal Infusions`
- 现译：`萨拉的草药浸剂店`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00474 | batch-093(待交叉) |  | 细微观察 |  |  |  |

<details><summary>hrq-00474 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40361`；`mod-tome/data/zones/town-gates-of-morning/traps.lua`
- **原文**：`Sarah's Herbal Infusions`
- **译文**：`萨拉的草药浸剂店`
- **复核结论**：细微观察
- **依据**：该商店源码绑定 `GATES_POTION`，实际售卖的是自然刻印“纹身”（`type="scroll", subtype="infusion"`）。英文实体名属于双关/字面招牌（表面为草药浸剂/茶，实为纹身店）。译文“萨拉的草药浸剂店”直译了该店名招牌，语义通顺，与 entry-03129（最后的希望同名店铺）保持一致。
```
</details>

## entry-03122

- 位置：`mod-tome.lua:40403`（tome）｜section：`mod-tome/data/zones/town-irkkk/traps.lua`｜source_tag：`entity name`
- 原文：`Swordsmith`
- 现译：`铸剑铺`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00475 | batch-093(待交叉) |  | 存在疑点 |  |  |  |

<details><summary>hrq-00475 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40403`；`mod-tome/data/zones/town-irkkk/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。同 entry-03112、entry-03114，术语快照登记为“长剑铁匠铺”（城镇商店实体），当前译文为“铸剑铺”。
```
</details>

## entry-03129

- 位置：`mod-tome.lua:40509`（tome）｜section：`mod-tome/data/zones/town-last-hope/traps.lua`｜source_tag：`entity name`
- 原文：`Sarah's Herbal Infusions`
- 现译：`萨拉的草药浸剂店`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00476 | batch-093(待交叉) |  | 细微观察 |  |  |  |

<details><summary>hrq-00476 · batch-093(待交叉) 详情</summary>

```
- **位置**：`mod-tome.lua:40509`；`mod-tome/data/zones/town-last-hope/traps.lua`
- **原文**：`Sarah's Herbal Infusions`
- **译文**：`萨拉的草药浸剂店`
- **复核结论**：细微观察
- **依据**：同 entry-03118，源码绑定 `POTION` store（机制为出售纹身 Infusion），译文直译店铺招牌，与晨曦之门同名店保持一致。
```
</details>

## entry-03137

- 位置：`mod-tome.lua:40586`（tome）｜section：`mod-tome/data/zones/town-point-zero/traps.lua`｜source_tag：`entity name`
- 原文：`Swordsmith`
- 现译：`铸剑铺`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00477 | batch-094(待交叉) |  | 细微观察 |  |  |  |

<details><summary>hrq-00477 · batch-094(待交叉) 详情</summary>

```
- **编号**：entry-03137
- **位置**：`mod-tome.lua:40586`（`mod-tome/data/zones/town-point-zero/traps.lua`）
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **结论**：细微观察
- **核验依据**：源码中对应零点圣域的剑类商店入口（`SWORD_WEAPON_STORE`）。术语快照中词头记录为“长剑铁匠铺”（`Swordsmith	长剑铁匠铺	T.GAME.ENTITY	places	entity name`）。经查 `mod-tome.lua`，全库所有 5 处城镇商店（第 40275、40313、40403、40586、40618 行）均统一译为“铸剑铺”。“铸剑铺”符合中文商业门牌表达且全库完全统一，但与术语快照存在细微字面出入。

---
```
</details>

## entry-03139

- 位置：`mod-tome.lua:40618`（tome）｜section：`mod-tome/data/zones/town-shatur/traps.lua`｜source_tag：`entity name`
- 原文：`Swordsmith`
- 现译：`铸剑铺`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00478 | batch-094(待交叉) |  | 细微观察 |  |  |  |

<details><summary>hrq-00478 · batch-094(待交叉) 详情</summary>

```
- **编号**：entry-03139
- **位置**：`mod-tome.lua:40618`（`mod-tome/data/zones/town-shatur/traps.lua`）
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **结论**：细微观察
- **核验依据**：源码对应夏特尔镇的剑类武器商店（`SWORD_WEAPON_STORE`）。同 entry-03137，全库城镇商店均统一译为“铸剑铺”，与术语快照“长剑铁匠铺”存在字面差异。

---
```
</details>

## entry-03149

- 位置：`mod-tome.lua:40781`（tome）｜section：`mod-tome/data/zones/tutorial-combat-stats/grids.lua`｜source_tag：`_t`
- 原文：`Teaches the player 'Shove'.`
- 现译：`可习得技能“推挤”。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00479 | batch-094(待交叉) |  | 细微观察 |  |  |  |

<details><summary>hrq-00479 · batch-094(待交叉) 详情</summary>

```
- **编号**：entry-03149
- **位置**：`mod-tome.lua:40781`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Shove'.`
- **译文**：`可习得技能“推挤”。`
- **结论**：细微观察
- **核验依据**：源码对应 `LEARN_PHYS_KB` 的描述。译文采用中文双引号对应英文单引号，且与相邻日志行（第 40782 行“你学会了技能推挤”）一致。观察到同文件实体名第 40780 行使用了“冲撞”（“启蒙符文：冲撞”），talent name 处（第 27003 行）使用了“击退攻击”；虽存在同名技能在跨条目间的译名差异，但当前条目表意准确，无机制误导。

---
```
</details>

## entry-03167

- 位置：`mod-tome.lua:41138`（tome）｜section：`mod-tome/data/zones/wilderness/grids.lua`｜source_tag：`_t`
- 原文：`Capital city of the Allied Kingdoms ruled by King Tolak`
- 现译：`联合王国首都（托拉克统治）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00480 | batch-094(待交叉) |  | 存在疑点 |  |  |  |

<details><summary>hrq-00480 · batch-094(待交叉) 详情</summary>

```
- **编号**：entry-03167
- **位置**：`mod-tome.lua:41138`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：`Capital city of the Allied Kingdoms ruled by King Tolak`
- **译文**：`联合王国首都（托拉克统治）`
- **结论**：存在疑点
- **核验依据**：
  1. **漏译头衔**：英文原文为 `ruled by King Tolak`，译文为“（托拉克统治）”，漏译了“国王”（King）头衔。
  2. **句式与同 section 不一致且添加了多余括号**：同文件下文第 41146 行夏特尔描述为“自然精灵领地的首都，由奈希拉·坦泰兰统治”（`Capital city of Thaloren lands, ruled by Nessilla Tantaelen`），第 41148 行埃尔瓦拉描述为“永恒精灵领地的首都，由阿兰尼恩·葛艾尔统治”（`Capital city of Shaloren lands, ruled by Aranion Gayaeil`），均采用规范的“……首都，由……统治”句式。此处使用了括号且省略了“国王”头衔，建议统一译为如“联合王国首都，由托拉克国王统治”。

---
```
</details>

## entry-03735

- 位置：`tome-orcs.lua:350`（orcs）｜section：`tome-orcs/data/chats/destructicus.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#*The Steam Giants are too great a threat to allow their escape - you will not have them simply return someday to finish what they attempted, and wipe out your Pride.  You press the #{italic}#"PREVIOUS TARGET"#{normal}# button, and fire on the airship.  There is a great roar and a flash of flame; you see its missile flying away from you through the window, as you see it racing towards your view, and the terrified passengers, on the scrying panel.

It reaches its mark, and the panel goes dark as a tremendous, multicolored blast fills your vision through the window.
 
The Steam Giants are no more.
 
The secondary charges from the warhead detonate, as burning debris falls into the sea, and the ongoing display serves as a signal to all the Orcs of Var'Eyal, and anyone else who may be watching: This is the fate of all who would try to eradicate the Orcs.  The previous millennia of oppression, genocide, and bullying are over: your people will never be pushed around like this again.
 
A nagging thought in the back of your head insists that you now know how the Sun Paladins felt, how King Toknor felt, how the halflings felt, how everyone that has always committed such atrocities against the Orcs felt.  It can keep whining all it wants - your people are finally safe.*#WHITE#`
- 现译：`#LIGHT_GREEN#*让蒸汽巨人们逃离太过危险 - 你不能允许他们这样简单的离开，然后将来某日再实现其图谋，消灭你的部落。你按下#{italic}#"上一名目标"#{normal}# 按钮，朝飞船开火。一阵巨大的轰鸣声和一道强烈的火光闪过，你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。

导弹到达了目的地，巨大的爆炸堵塞了你透过窗户的视线，面板随之变暗。

蒸汽巨人消失了。

弹头的次级装药引爆，燃烧的残骸坠入大海，这场持续的烟火盛宴成为大陆上所有兽人，甚至所有能看到这一盛景的生物的信号：
这就是所有试图消灭兽人的种族的命运。千年的压制、欺凌和屠杀被终结了：你的人民再也不会沦落如斯。

无法摆脱的念头自你脑后升腾，你现在明白了太阳骑士的感受，明白了图库纳国王的感受，明白了半身人的感受，明白了所有曾对兽人施以暴行的人的感受。
随它哀诉去吧————但你的人民终于安全了。*#WHITE#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00481 | remaining | remaining:rem-01:C01 | confirmed |  |  |  |

<details><summary>hrq-00481 · remaining 详情</summary>

```
### C01 | entry-03735 | confirmed

原译短引：“你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。”

原文把**窗外导弹远去**与**探知面板上导弹迎面冲向画面和乘客**并列呈现。前文已写明面板显示飞船内部。译文漏掉“on the scrying panel”，把两个视角合成了窗外远眺；“飞向你视线远处”也没有传达面板画面中的迎面而来。即使将“视线”宽泛理解为画面视线，译文仍未交代画面的载体，因此疑点成立。证据：[源码 destructicus.lua 第44–50、73–76行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/destructicus.lua:73)、[冻结译文第350行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:350)。
```
</details>

## entry-03738

- 位置：`tome-orcs.lua:410`（orcs）｜section：`tome-orcs/data/chats/john-surrender.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#[bind him to the ring]#WHITE# No, you are more useful alive and broken to me!`
- 现译：`#LIGHT_GREEN#[将他绑定到戒指上]#WHITE# 不，你活着对我更有用！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00482 | remaining | remaining:rem-01:C02 | confirmed |  |  |  |

<details><summary>hrq-00482 · remaining 详情</summary>

```
### C02 | entry-03738 | confirmed

原译短引：“不，你活着对我更有用！”

原文是“alive **and broken**”：约翰活着且被摧垮，两种状态共同限定“更有用”。译文只保留“活着”。前一句约翰请求死亡和安息，随后该选项将其绑定到戒指；语境不能替代选项台词中漏掉的“broken”。疑点成立，但不必把它限定为某一种具体的肉体折磨。证据：[源码 john-surrender.lua 第97–103行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-surrender.lua:97)、[冻结译文第410行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:410)。
```
</details>

## entry-03741

- 位置：`tome-orcs.lua:426`（orcs）｜section：`tome-orcs/data/chats/john-worldmap.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#*As you approach you recognize Outpost Leader John. But there is a kind of terrible darkness, you can feel his hatred crystallize the air.*#WHITE#
@playername@. You malevolent creature! #{bold}#YOU KILLED HER! YOU MURDEROUS DOG!#{normal}#
You #{italic}#dare#{normal}# carry her ring around like a trophy! I can feel it on you. Give it back! DIE!`
- 现译：`#LIGHT_GREEN#*当你靠近时，你认出了那是前哨站首领约翰。但他身边环绕着可怕的黑暗，你能感受到他的仇恨令空气结晶。*#WHITE#
@playername@ 你这个残忍的畜生！#{bold}#你杀了她！你这条残忍的狗！#{normal}#
你 #{italic}#竟敢#{normal}# 带着她的戒指作为战利品！我能感觉到它在你身上。拿出来，受死吧！！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00483 | remaining | remaining:rem-01:C03 | advisory |  |  |  |

<details><summary>hrq-00483 · remaining 详情</summary>

```
### C03 | entry-03741 | advisory

原译短引：“拿出来，受死吧！！”

“Give it back!”明说归还戒指；“拿出来”没有明说归还，削弱了约翰索回艾琳遗物的诉求。不过，约翰紧接着说感觉戒指在玩家身上，并要求玩家拿出它；在这一对峙中，“拿出来”仍可理解为交出戒指。保留表达澄清建议，不判确认错译。证据：[源码 john-worldmap.lua 第25–33行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-worldmap.lua:25)、[冻结译文第426–428行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:426)。
```
</details>

## entry-03747

- 位置：`tome-orcs.lua:467`（orcs）｜section：`tome-orcs/data/chats/kaltor-shop.lua`｜source_tag：`_t`
- 原文：`Welcome back, @playername@!  You see this, customers?  This fearsome, savage master of battle was so impressed by my products that he came back for more!
#LIGHT_GREEN#*He points to a new poster on the wall next to him, showing your face and the caption #{bold}#"KALTOR: THE CHOICE OF DESTROYERS!"#{normal}#*#WHITE#

So, what'll it be?`
- 现译：`欢迎回来，@playername@! 来看看这个，顾客们？这位可怕而野蛮的战斗大师也对我的产品印象深刻，现在他又回来买东西了！
#LIGHT_GREEN#*他指向墙上贴着的新海报，上面是你的脸和一行大字 #{bold}#"卡托尔：破坏者的选择！"#{normal}#*#WHITE#

那么，你要做什么呢？`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00484 | remaining | remaining:rem-01:C04 | advisory |  |  |  |

<details><summary>hrq-00484 · remaining 详情</summary>

```
### C04 | entry-03747 | advisory

原译短引：“那么，你要做什么呢？”

商店回访语境下，“So, what'll it be?”自然可译为“想买点什么？”，现译不够像店主招呼顾客。但 Flash 所称“必然是在问选购商品，误译成盘问行动意图”证据不足：该对白接入的选项同时包括**看货、攻击和不购物**。“你要做什么呢？”可以概括这些选择，未造成明确的选项意义错误。将原 confirmed 判断下调为措辞建议。证据：[源码 kaltor-shop.lua 第24–31、40–45、66–69行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:24)、[冻结译文第467–470行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:467)。
```
</details>

## entry-03748

- 位置：`tome-orcs.lua:474`（orcs）｜section：`tome-orcs/data/chats/kaltor-shop.lua`｜source_tag：`_t`
- 原文：`#LIGHT_GREEN#*Kaltor is busy packing some of his goods away in crates; he hands one to a worker, carrying it out the back door, before turning to you.*#WHITE#
	Make it quick, @playername@. Not to be rude, but there's a private airship out there with my name on it, and I'd rather have a bird's-eye view of what you're about to do than a front-row seat.`
- 现译：`#LIGHT_GREEN#*卡托尔忙着打包货物；他将箱子递给一个工人带到后门，然后转过头和你说话。*#WHITE#
	快点吧，@playername@。不是我粗鲁，但现在有一艘我的飞船在外面，我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00485 | remaining | remaining:rem-01:C05 | confirmed |  |  |  |

<details><summary>hrq-00485 · remaining 详情</summary>

```
### C05 | entry-03748 | confirmed

原译短引：“我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。”

“bird’s-eye view”与“front-row seat”对比的是**从飞船上远观**和**留在现场近距离目睹**。译文把后者写成单纯“坐在椅子上”，丢失“前排、近在事发处”的位置关系，令对比变成站与坐。即使将 *seat* 作字面座位理解，*front-row* 仍未译出。疑点成立；源码足以支持远近对比，无须推断飞船高度或具体灾害。证据：[源码 kaltor-shop.lua 第48–51行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:48)、[冻结译文第474–475行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:474)。
```
</details>

## entry-03772

- 位置：`tome-orcs.lua:957`（orcs）｜section：`tome-orcs/data/general/npcs/sunwall-mage.lua`｜source_tag：`entity name`
- 原文：`astral conjurer`
- 现译：`星空魔术师`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00486 | remaining | remaining:rem-01:C06 | advisory |  |  |  |

<details><summary>hrq-00486 · remaining 详情</summary>

```
### C06 | entry-03772 | advisory

原译短引：“星空魔术师”。

源码将 *astral conjurer* 定义为持杖、施展星辰法术的法师实体；“魔术师”在现代汉语中容易让人想到舞台表演，“星界唤术师”等称呼可能更贴近角色。然而“魔术师”也能在奇幻语境中泛指施法者，现译未把实体误指成确定的另一种职业或机制。保留命名风格建议。证据：[源码 sunwall-mage.lua 第114–131行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/npcs/sunwall-mage.lua:114)、[冻结译文第957行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:957)。
```
</details>

## entry-03799

- 位置：`tome-orcs.lua:1499`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`These boots have a %d%% chance to fail to operate properly (reduced by Cunning).`
- 现译：`火箭靴有%d%%几率失败（随灵巧降低）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00487 | remaining | remaining:rem-02:C01 | advisory |  |  |  |

<details><summary>hrq-00487 · remaining 详情</summary>

```
### C01 | entry-03799 | advisory

原译“火箭靴有%d%%几率失败”。该物品名为 *Anti-Gravity Boots*，英文用“These boots”指代它；另有名为 `%s rocket boots` 的工匠插件。风味描述确实说这双鞋靠火箭升空，因此“火箭靴”有语境依据，但会与插件名称混淆。建议改为“这双靴子有%d%%几率无法正常运作”。证据：快照 1381、1490–1499；兽人源码 142–151、174；`tinkers/mechanical.lua` 29–32。
```
</details>

## entry-03801

- 位置：`tome-orcs.lua:1509`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`fire a poisonous bolt out to range %d that deals %d nature damage and afflicts the target with crippling poison (%d%% fail chance) that deals %d addition nature damage over %d turns (damage based on Cunning)`
- 现译：`发射一支射程最远为 %d 码的毒箭，造成 %d 点自然伤害，并导致目标被致残毒素（%d%% 行动失败几率），在 %d 回合内造成 %d 点额外自然伤害（伤害受灵巧值加成）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00488 | remaining | remaining:rem-02:C02 | confirmed |  |  |  |

<details><summary>hrq-00488 · remaining 详情</summary>

```
### C02 | entry-03801 | confirmed

原译“并导致目标被致残毒素（%d%%行动失败几率）”在“被致残毒素”后缺少谓语，未完整表达 *afflicts the target with crippling poison*；可推知“感染”之意，但句子本身残缺。改为“并使目标感染致残毒素”即可。`{1,2,3,5,4}` 的占位符重排正确，不属于此问题。证据：快照 1509；兽人源码 275–280、290–299。
```
</details>

## entry-03807

- 位置：`tome-orcs.lua:1551`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`tformat`
- 原文：`(cooling down: %d turns)`
- 现译：`(冷却时间：%d 回合)`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00489 | remaining | remaining:rem-02:C03 | advisory |  |  |  |

<details><summary>hrq-00489 · remaining 详情</summary>

```
### C03 | entry-03807 | advisory

原译“冷却时间：%d 回合”。源码传入 `maxp - self.power`，数值是当前剩余回合；“冷却时间”也可作笼统状态标签，因此属于精度建议。建议“冷却中：%d 回合”。证据：快照 1551–1553；兽人源码 579–582。
```
</details>

## entry-03809

- 位置：`tome-orcs.lua:1560`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`Through a combination of magic and airborne probes, these shots incite powerful bolts of lightning to strike your target from above, frying them and those around them!`
- 现译：`这些弹药通过魔法和探针从天空引导强力的闪电冲击你的目标，灼烧目标及周边的单位！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00490 | remaining | remaining:rem-02:C04 | advisory |  |  |  |

<details><summary>hrq-00490 · remaining 详情</summary>

```
### C04 | entry-03809 | advisory

原译“通过魔法和探针从天空引导……”。*airborne probes* 的“升空”属性没有直接落在“探针”上；但“从天空引导”保留了空中方位，读者仍可能理解为空中探针。可改“通过魔法和空中探针……”。证据：快照 1558–1561；兽人源码 641–646。
```
</details>

## entry-03811

- 位置：`tome-orcs.lua:1569`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`Release a burst of shrapnel, dealing physical damage equal to your steampower in a cone from the target of radius 4.`
- 现译：`释放榴弹，在半径4锥形范围内造成等于蒸汽强度的物理伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00491 | remaining | remaining:rem-02:C05 | confirmed |  |  |  |

<details><summary>hrq-00491 · remaining 详情</summary>

```
### C05 | entry-03811 | confirmed

原译“释放榴弹，在半径4锥形范围内……”把 *shrapnel*（弹片）译成榴弹，并漏掉 *from the target*。源码以目标坐标设置锥形起点，遗漏会影响范围理解。建议“从目标处向外迸射弹片，在半径4的锥形范围内……”。证据：快照 1566–1569；兽人源码 714–720。
```
</details>

## entry-03815

- 位置：`tome-orcs.lua:1613`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`every third hit always crits.`
- 现译：`第三下攻击必定暴击。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00492 | remaining | remaining:rem-02:C06 | confirmed |  |  |  |
| hrq-00493 | remaining | remaining:rem-02:N01 | upstream |  |  |  |

<details><summary>hrq-00492 · remaining 详情</summary>

```
### C06 | entry-03815 | confirmed

原译“第三下攻击必定暴击”缺少 *every* 的循环含义，且 *hit* 比“攻击”更明确地限定命中。装备效果的“第三下”可被读作每轮第三下，但也可读作仅首次第三下；建议写“每累计命中三次，下一次攻击获得暴击加成”。源码计数归零证明循环存在；其触发时序另见 N01，不能据此断言“第三次命中当次必暴击”。证据：快照 1611–1613；兽人源码 1081–1090。
```
</details>

<details><summary>hrq-00493 · remaining 详情</summary>

```
**N01｜原文与源码机制不一致，非中文新增错译。** Golden Gun 的 `special_on_hit` 在命中后的处理阶段才累计计数；第三次计数时将 `physcrit` 设为 100 并清零。弓射流程先计算暴击，再调用该效果，因此源码支持的是为后续攻击设置暴击率，而非英文所说“每第三次命中当次必定暴击”。此外，效果调用受目标存活条件限制。证据：兽人源码 1081–1090；固定引擎 commit `624a673` 的 `game/modules/tome/class/interface/Archery.lua` 377、548–556。
```
</details>

## entry-03823

- 位置：`tome-orcs.lua:1740`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`There is an attached note.
 
'I've spilt the heartsblood of my work, feeling it pound, like a heart, in my palms.
Some people just can't let go until they've bled dry.'`
- 现译：`上面粘着一页笔记。

'我将我的心血之作分离，感受它的跳动，像心脏一样跳动，在我的手心里。
总有些人不到血流尽，不撒手。'`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00494 | remaining | remaining:rem-02:C07 | confirmed |  |  |  |

<details><summary>hrq-00494 · remaining 详情</summary>

```
### C07 | entry-03823 | confirmed

原译“我将我的心血之作分离”将 *spilt*（洒出）处理成了“分离”，改变了与 *heartsblood*、*bled dry* 呼应的流血意象。“心血之作”可作意译，但不能使“spilt”变为“分离”。建议按“洒出／流尽心血”重译该句。证据：快照 1739–1746；兽人源码 2082–2091。
```
</details>

## entry-03827

- 位置：`tome-orcs.lua:1791`（orcs）｜section：`tome-orcs/data/general/objects/world-artifacts.lua`｜source_tag：`_t`
- 原文：`How do these even work?`
- 现译：`这玩意到底怎么用？`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00495 | remaining | remaining:rem-02:C08 | advisory |  |  |  |

<details><summary>hrq-00495 · remaining 详情</summary>

```
### C08 | entry-03827 | advisory

原译“这玩意到底怎么用？”偏向询问使用方法；*How do these even work?* 结合漆黑护目镜的描述，更像惊讶其如何起作用。“怎么用”在口语中也可能泛指如何运作，故保留为建议。可改“这东西到底怎么起作用？”证据：快照 1789–1792；兽人源码 2387–2396。
```
</details>

## entry-03845

- 位置：`tome-orcs.lua:2041`（orcs）｜section：`tome-orcs/data/lore/emporium.lua`｜source_tag：`_t`
- 原文：`CLOSING SALE
for
KALTOR's FIREARMS, ARMOR, AND OTHER MARTIAL SUNDRIES
 
It is with a heavy heart that I must announce our closing.  After over twenty years of service, I am shutting my doors - the people of the Atmos Tribe apparently wish to trust the Guard with their well-being, and the Guard chooses to maintain the weapons it already has rather than purchase things like the #{italic}#BRILLIANT AUTO-LOADING ORC EXPELLER#{normal}# (only 30 gold!), or the #{italic}#PRESSURE-ENHANCED SLASHPROOF COMBAT SUIT#{normal}# (only 450 gold!).  I even offered discount options such as the #{italic}#LIL SURPRISE#{normal}# (now only 15 gold!), and yet the city would have none of it.  It would seem my services, and my talents, are simply not wanted.
 
Even if you have no fear of the orcish tribes, ritch swarms, and other assorted threats that lurk just outside our city walls, please consider purchasing some of my wares.  They are truly beautiful displays of craftsmanship, and would do well as a desk sculpture or (if properly disarmed) a child's toy.  If nothing else, you will be ensuring that a once-proud artisan with great love and respect for his craft need not resort to begging on the streets.`
- 现译：`卡托尔的军火、护甲和军用杂货店即将停业

我心情沉重地宣布我们店的停业。二十年的经营后，我要关门了————气之部族的居民显然想要用他们的全身心信任守卫们，而守卫们却想维持原来的配备，而不是去购置像是“#{italic}#光辉灿烂的自动装填的兽人驱除器#{normal}#”（仅售30金币！）或者是“#{italic}#增压的防挥砍的战斗服#{normal}#”（仅售450金币！）。我甚至推出了像是“#{italic}#小小大惊喜#{normal}#”（现在仅售15金币！）这样的优惠，但是这个城市不愿意买任何一件。看上去我的竭诚服务和才华横溢真的没人需要。

即使你们一点也不怕那些兽人部落、里奇虫群和在我们城市外游荡的各种威胁，请还是考虑一下要不要买我的一些东西。它们确实美丽得体现了匠人精神，而且可以做好的书桌摆设品或者是孩子的玩具（如果做好了保险措施的话）。如果你愿意伸出援手的话，你可以让一个热爱又尊重他的作品，曾经自豪的工艺大师不再被迫流落街头乞讨。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00496 | remaining | remaining:rem-03:C01 | advisory |  |  |  |

<details><summary>hrq-00496 · remaining 详情</summary>

```
### C01 | entry-03845 | advisory

原译“用他们的全身心信任守卫们”尚可理解为完全信任，但 *well-being* 更明确指把自身安危托付守卫；“如果你愿意伸出援手”也保留劝购意图，却把 *If nothing else* 的“至少如此”改成了意愿条件。两处均建议澄清，未达到确认错译的程度。见[原文 emporium.lua:52](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/emporium.lua:52>)、[译文 tome-orcs.lua:2049](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2049>)及2051行。
```
</details>

## entry-03849

- 位置：`tome-orcs.lua:2195`（orcs）｜section：`tome-orcs/data/lore/gem.lua`｜source_tag：`_t`
- 原文：`#{italic}#(You hear loud, mechanical rumbling; in the distance, you hear sounds of struggling and bludgeoning, swords slicing through flesh, steamguns being fired, and shouts of pain from giant and horror alike.  Parmor sounds panicked.)#{normal}#

"Mayday, mayday, we are bailing out!  Tantalos is gone, and we are NOT going back for him!  Scrap the tunnel to the Palace of Fumes, scrap the entire damn council, we're getting as far away from here as we can--"  Loud hissing.  "MOTHER OF--!"  Grunts, squishing, slashing.  "Flooring it all the way to the damn Sunwall, we're taking the first farportal off this continent whether those tinies like it or not!  Guess this technically counts as treason, mutiny, whatever, but if the Council's hearing this, BLOW IT OUT YOUR STEAM-HOLES, WE'D RATHER LIVE!  Altitude rising, surface approaching, this is H.C. Parmor signing off--"`
- 现译：`#{italic}#（你听到了巨大的，机械的轰鸣声。在远处，你听到挣扎和殴打的声音，听到利刃刺破血肉，蒸汽枪的枪声，以及巨人和恐魔发出的痛苦怒吼。帕默的声音听起来惊慌失措。）#{normal}#

“求救，求救，我们在撤离！坦塔洛斯完蛋了，我们绝对不会再回去救他的！去你妈的烟雾宫殿的隧道，去你妈的天杀的议会，我们必须赶紧跑，越远越好——”巨大的嘶嘶声。“狗娘——！”撞击声，挤压声，破碎声。“给我朝太阳堡垒前进，我们要使用这个大陆上的第一个远行传送门，不管你们这些家伙喜不喜欢！我可不管这是不是什么叛国、谋反，去他妈的，如果你们议会在听着的话，放你娘的蒸汽孔，老子只想活下去！海拔上升，准备接近地面，这里是 H.C. 帕默，播报完毕——”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00497 | remaining | remaining:rem-03:C02 | confirmed |  |  |  |

<details><summary>hrq-00497 · remaining 详情</summary>

```
### C02 | entry-03849 | confirmed

原译“这个大陆上的第一个远行传送门”将逃亡语境中的 *the first farportal off this continent* 读成按建造或排列顺序的“第一个”；这里是要搭上最先能离开大陆的传送门。“你们这些家伙”也把 *those tinies* 的第三人称矮小者改为第二人称。即使“第一个”勉强可指最先可用者，后半句的人称和蔑称仍无法等价。见[gem.lua:65](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/gem.lua:65>)、[译文:2199](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2199>)。
```
</details>

## entry-03851

- 位置：`tome-orcs.lua:2218`（orcs）｜section：`tome-orcs/data/lore/internment-camp.lua`｜source_tag：`_t`
- 原文：`#{italic}#To: Guard Captain Galsamae
From: Administrator Quellop#{normal}#

It's good to see that you and your followers have arrived safely! Hopefully you're settling in all right; thank you for coming, and pass my thanks on to the Elvala diplomats for getting you here on such short notice. I hope this is the first step in your kind - you Ogres, of course, but also the Shaloren who sent you here - joining forces with the Allied Kingdoms.

There are no Ziguranth here in the Far East, and the orcs in this camp have been compliant so far, on account of Mindwall's elaborate illusions. It's the most humane way to deal with them that we've found so far - we hope that his influence will have a permanent calming effect on them over time, but until then, they're happy and docile in their little dream-world. All you have to do is protect against any stragglers outside the walls looking to break their kin out of here, and patrol the halls to make sure any orcs who've managed to shake off the illusions are swiftly apprehended and dealt with. This should be a pretty easy job - if you need any particular help or provisions, though, let me know and I'll do what I can!

Sincerely,
Administrator Quellop

#{bold}#---#{normal}#

#{italic}#To: Administrator Quellop
From: Guard Captain Galsamae#{normal}#

We need four more chairs in the break room.

-Galsamae

#{bold}#---#{normal}#

#{italic}#To: Guard Captain Galsamae
From: Administrator Quellop#{normal}#

I'm sorry, but we can't really afford that, as the budget for amenities and luxuries is stretched pretty thin here as-is. Please try to keep your requests limited to necessities - even with Last Hope's merchants competing on price, the security over by the farportal means it's still not cheap to get things here.

Regretfully,
Administrator Quellop`
- 现译：`#{italic}#致：卫队队长加尔萨迈
来自：管理员夸洛普#{normal}#


很高兴看到你和你的随从已经安全抵达！感谢你的光临，也感谢埃尔瓦拉的外交官能在这么短的时间内联系到你过来，希望你能在这里安顿下来。我希望这将会成为你们一族——当然，不仅是你们食人魔，也包括派遣你们过来的永恒精灵——与联合王国的合作部队的良好的第一步。

在远东这里没有伊格兰斯。得益于意念之墙精巧的幻象技术，关押在这里的兽人都十分顺从。到目前为止，这是我们找到的和他们打交道的最人道的方法——我们希望，随着时间流逝，他的能力最终可以对这些兽人起到永久的镇定效果。不过，在那之前，他们都会这样傻乎乎地，温顺而快乐生活在梦中的小小世界里。你所需要的就是守住这里的围墙，不能让外部的游荡的兽人进来救走他们的同族。同时，还要巡逻这里的大厅，确保那些成功脱离幻象的兽人被我们迅速逮捕和解决。这应该会是一件非常容易的工作——但是，如果你需要任何特别帮助或补给的话，请立刻告诉我，我将尽我所能帮助你！

此致，
管理员夸洛普

#{bold}#---#{normal}#

#{italic}#致：管理员夸洛普
来自：卫队队长加尔萨迈#{normal}#

请在休息室里增加四把椅子。

——加尔萨迈

#{bold}#---#{normal}#

#{italic}#致：卫队队长加尔萨迈
来自：管理员夸洛普#{normal}#

很抱歉，但是我们实在买不起这些。我们能花在设施和非必需品上的预算，和往常一样，已经被压缩到了极限。请尽可能只需求必需品——尽管最后的希望的商人们用低廉的价格相互竞争，但考虑到远行传送门的严密安保，在这里要想买到东西仍然十分不便宜。

充满抱歉，
管理员夸洛普`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00498 | remaining | remaining:rem-03:C03 | confirmed |  |  |  |

<details><summary>hrq-00498 · remaining 详情</summary>

```
### C03 | entry-03851 | confirmed

原译“与联合王国的合作部队的良好的第一步”把 *joining forces with the Allied Kingdoms* 拆成了名词“合作部队”。原句的行动主体是“你们一族”，包括食人魔和派遣他们的永恒精灵，意思是他们与联合王国携手。即使把“合作部队”宽读为联合力量，译句仍表示与某支部队建立关系，并使句法不通。见[internment-camp.lua:31](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/internment-camp.lua:31>)、[译文:2249](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2249>)。
```
</details>

## entry-03852

- 位置：`tome-orcs.lua:2523`（orcs）｜section：`tome-orcs/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`I'm not going to lie to you: things aren't going great.  Between the Doomelf escape incidents, the deaths of Khulmanar and a great deal of our more expensive combatants at the hands of the Anomaly, and the disappearance of the First Duathedlen, we've been set back pretty far this year.  As such, your orders are simple: lay low.  Stay out of sight, and conduct passive observation until we can get a foothold and a new plan.

And regarding the First Duathedlen - quit your murmuring right now.  I've seen his track record, and I know most of you know it too, which is why we can safely say that despite his... nature, his loyalty is [b]not[/b] in question - we can assume his abrupt cessation of communication is a necessary part of his investigations, and not him going rogue.  If you see him, tell us of his whereabouts, but do not interfere.

[i](The letter is signed with an unreadable but formal-looking demonic seal.)[/i] `
- 现译：`我准备实话实说：事情的进展并不顺利。除了魔化精灵的逃亡事件之外，还有库马纳的死，我们众多精英卫兵在那场异常中的牺牲，以及第一位多瑟顿的失踪…我们今年的损失已经够严重了。所以，给你们的命令很简单：保持低调。远离敌人的视线，进行被动的观察，直到我们可以获得一个新的立足点，开展新的计划。

还有，有关第一位多瑟顿的事情——你现在就别抱怨这些了。我看到过他的记录，我知道你们大部分人也都看过，这就是为什么我可以放心的说，尽管他的…本性如此，但他的忠诚是[b]无可挑剔[/b]的——我们可以假定，他的突然失联是他进行的调查的一个重要组成部分，而并不是他叛逃了。如果你看到了他，请告诉我们他的位置，但千万不要干涉他的行动。

[i]（这封信是用一个难以辨认，但看起来很正式的恶魔印章签署的。）[/i] `

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00499 | remaining | remaining:rem-03:C04 | confirmed |  |  |  |

<details><summary>hrq-00499 · remaining 详情</summary>

```
### C04 | entry-03852 | confirmed

原译“库马纳的死，我们众多精英卫兵在那场异常中的牺牲”弱化了 *at the hands of the Anomaly* 的致死关系；原文将库马纳及一批战斗人员的死亡都归于 Anomaly。“在……中牺牲”可暗示灾难致死，却未明确施害关系，且“精英卫兵”无从对应 *more expensive combatants*。可确认译文偏差；仅凭本处文本不能进一步确认 Anomaly 的具体实体身份。见[misc.lua:45](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua:45>)、[译文:2527](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2527>)。
```
</details>

## entry-03853

- 位置：`tome-orcs.lua:2545`（orcs）｜section：`tome-orcs/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`The anti-scrying nexus you folk set up here is damn impressive, as is the time-release pseudo-rune powered by it - hard to find a spare spot on my skin for it, but I can feel it working for a few days after I'm back in Maj'Eyal.  Great for making sure we can get away from the West portal and disperse without the A.K. catching on or tracking us to a common point of convergence.

Got a proposal, though.  With a few little tweaks, I could make one that doesn't require the bearer's consent to use.  You aren't the only ones buying slaves from me, and when I get a customer who wants them taken right back to the West, we have to do the anti-scrying enchantments ourselves.  I don't know if you've noticed, but proper mages still aren't easy to come by - I barely made a profit last time I did it.

Say the word, and I'll send over the temporary rune design so you can set the nexus to recognize it.  No charge from me - if you accept it, it'll pay for itself.

[i](You assume the elaborate, glowing shape below is an Ogric equivalent to a signature.)[/i] `
- 现译：`老兄，你们设置的反侦测水晶真他妈够劲的，还有这个被它驱动的延时释放的伪符文——我的皮肤上没有什么空位了，但我能感受到，这玩意儿在我回马基埃亚尔之后几天都能用。这肯定能保证，我们可以安心从西部的传送门逃走，绝对不会被联合王国抓到，他们也肯定没法追踪我们的痕迹。

现在，我现在有一个想法。只要稍微整一下，我就可以让这玩意儿不需要使用者的意愿就能工作。你不是唯一一个从我这里买奴隶的人，要是你想把他们带回西部去的话，我们可得好好做点反侦测的准备。我不知道你有没有注意到，但合格的法师如今还是很难请到——上次，我差点把老本都给赔光了。

只要你一句话，我就把这个临时的符文设计发给你，你设置好水晶就能用了。我不收你的钱——只要你愿意用，这笔投入很快就能回本。

[i]（你猜想，下面画着的这个精心设计的，闪闪发光的图案，在食人魔文化里有着和签名一样的用途。）[/i] `

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00500 | remaining | remaining:rem-03:C05 | confirmed |  |  |  |

<details><summary>hrq-00500 · remaining 详情</summary>

```
### C05 | entry-03853 | confirmed

原译“要是你想把他们带回西部”把 *when I get a customer who wants them taken right back to the West* 中另一个买家的要求，移到了收信人身上。前句“你不是唯一一个从我这里买奴隶的人”虽可让读者猜到有其他买家，却不能使随后明确的“你想”与原文等价；反侦测附魔的触发情形因此被改写。见[misc.lua:76](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua:76>)、[译文:2553](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2553>)。
```
</details>

## entry-03854

- 位置：`tome-orcs.lua:2559`（orcs）｜section：`tome-orcs/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`We get it: it's our fault the farportal mailing system isn't perfect.  Our people are still working on undoing that jury-rigged configuration that keeps your portal from transporting anything that isn't living - and if we get it wrong, that means people start getting teleported into walls again.  It's already a damn miracle you can get through the portal without coming out naked on the other side, let alone still carrying your backpacks and all their contents.

In the meantime: we're still losing a few letters going through the mailing system, and the lost ones could end up teleported to pretty much anywhere.  They could end up ten feet from the portal, or they could end up right in some A.K. busybody's hands, or they could just warp themselves right up Urh'Rok's nose for all we know.  Likewise, anything written on those notes could end up exactly where you don't want them, wherever that might be.

My point is, when you're writing those letters, write them like King Tolak's looking over your left shoulder and your grandmother's looking over your right - or at least show SOME semblance of subtlety.  Don't complain about the prices of "illegal potions," complain about "extra-strength medicine."  Don't ask about safety accommodations for "slaves," ask about "private servants."  And please, for the love of Linaniil, [i]stop calling the farportal a farportal![/i]  The A.K. doesn't even know we [i]have[/i] this thing yet, and we don't want to give them any ideas on where or how to start looking.  Call it a courier, or a pack golem, or a trained uruivellas for all I care.

-Korbek

PS: Yes, I'm breaking my own rules with this letter - you idiots clearly don't understand subtlety, so I can't assume you'd understand a subtly-written letter.  Yes, I'm aware there's a chance this letter could end up in enemy hands.  No, the irony of that situation would not be lost on me.  Yes, I will hurt whoever thinks they're clever by bringing up any of the preceding.`
- 现译：`我们知道：远行传送门邮递系统并不完美这件事当然是我们的过错。我们还在努力修复那个让传送门无法传送任何非活物的临时配置——如果我们搞砸了的话，那么很快就会又有人被传送到墙里了。你能够这样穿过远行传送门，而不是裸体出现在另一边，包里的东西都完好无损，已经他妈的是一件奇迹了，好不好。

与此同时：我们的邮递系统仍然会丢失几封信，这些丢失的邮件可能会出现在任何地方。据我所知，可能会出现在传送门十英尺以内的地方，也有可能出现在某个联合王国好事者的手里，还有可能出现在乌鲁洛克的鼻子底下，都有可能。也就是说，你写的每一封信都有可能出现在你最不希望出现的地方，不管那是多么遥远的地方，明白吗。

我想说的就是，当你写信的时候，请你想象一下，托拉克国王就在你左边看着，你奶奶站在你右边看着——或者，至少你得明白什么叫隐晦一点，好吗？别再抱怨“非法药剂”的价格了，你能说“大力药”吗？别再讨论使用“奴隶”的安全设施了，可以用“私人仆人”这词吗？还有，拜托，为了莱娜尼尔的爱，[i]别再把远行传送门叫做远行传送门了，好吗！[/i]联合王国甚至还不知道我们[i]有[/i]这个东西，可以不要再给他们侦查的线索了吗？随便你叫他什么，快递员，邮递傀儡，训练好的乌尔维拉斯，随你怎么说都行，拜托了。

——库贝克

注：是的，我知道我自己这份信打破了规则——你们这些白痴连隐晦的重要性都不知道，我怎么指望能用一份隐晦的信让你们明白？是的，我知道这份信也有可能落到敌人手里。不，别指望你能用这个场景的讽刺性来笑话我。是的，谁敢列出以上我所说的任何一条，来显示自己很聪明，我就打烂你的嘴。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00501 | remaining | remaining:rem-03:C06 | confirmed |  |  |  |
| hrq-00502 | remaining | remaining:rem-03:N01 | confirmed |  |  |  |

<details><summary>hrq-00501 · remaining 详情</summary>

```
### C06 | entry-03854 | confirmed

原译“为了莱娜尼尔的爱”把催促对方住口的 *for the love of Linaniil* 译成生硬的字面爱意；可宽读为感叹语，但原句语气未清楚传达。“使用‘奴隶’的安全设施”还将 *safety accommodations for “slaves”* 的受益对象改成“使用奴隶”的设施。不过，*accommodations* 在此也可指安全安排或设施，Flash 断定其必为“食宿安置”不成立。见[misc.lua:91](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua:91>)、[译文:2571](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2571>)。
```
</details>

<details><summary>hrq-00502 · remaining 详情</summary>

```
### N01 | entry-03854 | confirmed

原译以“大力药”替换 *extra-strength medicine*。原文要求用听似合法的“强效药”掩饰“非法药剂”，*extra-strength* 修饰药效或剂量；“大力药”则通常指增强力气的药，改变了药品性质。把它宽读成“效力很大的药”虽能解释译者意图，却不是这句告诫读者采用的自然说法，建议改为“强效药物”一类措辞。见[misc.lua:91](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua:91>)、[译文:2571](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:2571>)。
```
</details>

## entry-03856

- 位置：`tome-orcs.lua:2625`（orcs）｜section：`tome-orcs/data/lore/misc.lua`｜source_tag：`_t`
- 原文：`To think such an advanced civilization was hiding nearly right under our noses!  Not that the proximity made it any easier for me to conduct my research - it seems that unless you're a Sunwall citizen, a blood relative of King Tolak, or a merchant with enough gold to bribe the guards to look the other way, it's nearly impossible for a civilian to use the portal to the East.  Fortunately, Grand Councilor Kasyros himself was shown my writings to give him a basic overview of all the species his people were unfamiliar with, and he requested my presence to study his people.

Steam Giants are strikingly similar to what humans would look like, were they 8-10 feet tall and slightly on the stocky side (in contrast to the gangly, yet deceptively strong giants of Daikara).  Their most distinguishing physical trait is almost certainly their steam, for which they are named - their skin has numerous pores and vents which are capable of emitting pressurized steam.  They have limited conscious control over this; at rest they are nearly invisible and emit either a gentle mist or nothing at all, but they can will them to seal shut or distend widely, which, in addition to being rather disconcerting to watch, emits a stream or burst of pressurized steam.

Rather ingeniously, they have figured out how to use this steam to power and operate a wide array of metallic contraptions.  Although the giants' oldest texts have been lost to occasional fires and other disasters, they claim that the first bit of "steam-tech" was a simple whistle; from there, they discovered a sort of pressurized stone-cleaner, and from there more and more complex contraptions.  A similar effect can theoretically be achieved by using a furnace to boil water, but this method requires attention and adjustment that comes as naturally to the Steam Giants as breathing; perhaps it is this intuitive quality that made it so easy for them to accomplish so much with it.

The Steam Giants of the Atmos Tribe have hidden in the Clork mountains for ages; it is truly fortunate for them that the Spellblaze missed them entirely, for they were so concentrated and so few in number that it surely would have eradicated them.  They have kept their interactions with other races to a minimum; while Grand Councilor Kasyros claims this was due to fear of both what the outside world could do to them, and what their careless intervention could do to outsiders, most of the other Atmos I spoke to claimed to merely find the "lesser races" to be boorish and unpleasant.  (This is an entirely understandable view, seeing as their only neighbors until just recently have been Orcs.) 

While this isolation has given them peace to let their society develop, it has also fostered a strain of sophistry and disconnection to reality, according to Kasyros, who has begun open trade with the Sunwall and Allied Kingdoms to grant his citizens some fresh perspective.  I could not hope to fully analyze this society during my brief stay; the only deeper insight worth noting I was able to see is that they value physical fitness almost exactly as much as intellectual pursuits, perhaps owing to the fact that steam-tech can be made more powerful through more efficient construction OR simply being able to force out more steam from one's vents.  Their government, accordingly, is chosen by an apparent compromise between democracy and bloodsport (aside from a brief period under King Traglamar, which Kasyros would only tell me "was deeply embarassing for all involved").  Although I cannot say how it reflects on the Atmos people in a greater sense, I feel I must make special note that they have learned how to make the best absinthe I have ever tasted.

Alas, I was not able to study them for long enough to learn more than this.  Kasyros tells me he cannot accompany me any longer, for he has arranged a meeting with the Hero of Maj'Eyal - something about using an exploratory farportal for disposal purposes?  Whatever the case, although most of our contact with the Atmos is still done via constructs dropped from airships, we will soon gain the opportunity to meet more of them in person, and perhaps outsiders other than myself will soon be allowed to see their cities for themselves.  Their help in crushing the Kruk Rebellion and thwarting their leader's attempts to commandeer [b]IMMOLATUS, IMPUDENT RAVAGER OF THE HEAVENS[/b] has ensured that they will be enduring allies with us for an age to come.`
- 现译：`想想看吧，就在我们的眼皮底下，竟然藏着这样一个高度发达的文明！然而，我们之间这样的接近，并没有给我的研究提供什么方便——除非你是太阳堡垒的公民，托拉克国王本人的亲戚，或者是腰缠万贯的富商，能用足够的钱贿赂卫兵网开一面。否则，像我这样的平民，几乎没有任何使用远行传送门通往远东的机会。幸运的是，卡西罗斯议长本人曾经读过我的书，用以了解这个世界上他的族人所不熟悉的那些众多种族。现在，他邀请我亲自研究他的族人。

蒸汽巨人看起来与人类惊人地相似，他们身高8-10英尺，身材稍显矮胖，这与岱卡拉那些瘦高但出人意料地强壮的巨人形成了鲜明的对比。他们最具标志性的外貌特征是他们身上的蒸汽，这就是他们被命名为蒸汽巨人的原因——他们的皮肤上有许多毛孔和通风口，可以从中排出高压的蒸汽。他们可以对排气的行为进行有限的主动控制；在休息的时候，他们的排气行为通常是不可见的，只能依稀看到轻柔的薄雾，或者干脆什么也看不到。但是，他们也可以主动封闭或扩张排气口，放出一股气流或一团高压蒸汽，这样的场景看起来颇为令人不安。

他们相当巧妙地想到了使用这股蒸汽来驱动和操纵各种各样的金属装置的方法。尽管这些巨人们最早的文字记录被偶然的火灾和其他的灾害摧毁了，他们声称，最早的“蒸汽科技”只是一种简单的哨子。在此之后，他们发明了使用加压蒸汽清洁物体表面的方法，然后逐渐发明了一系列越来越复杂的装置。原理上，使用炉子来加热水也可以产生蒸汽，达到类似的效果，不过这种需要操作者仔细关注、控制蒸汽，而这一切对于蒸汽巨人来说都如同呼吸一样简单。或许，正是因为这种直观的感觉，让他们可以如此轻松地用蒸汽实现这样多的东西。

气之部族的蒸汽巨人在克拉克山脉中藏匿了几个世纪；幸运的是，他们从未受到魔法大爆炸的影响，考虑到他们的生存环境如此集中，人口又是这么稀少，这样的灾害恐怕会完全灭绝他们。他们尽力将与其他种族之间的互动降低到最低限度。按照卡西罗斯议长的说法，这是因为他们既害怕外部世界可能对它们造成的威胁，也害怕他们不谨慎的发明可能会给外面世界的人带来怎样的影响，但按照我从其他气之部族的人的说法，他们只是觉得那些“下等种族”又粗野又令人不快而已。（考虑到直到不久之前，他们唯一的邻居就是兽人，我完全可以理解他们的这种看法）

按照卡西罗斯的说法，尽管和外界的隔绝给了他们社会发展所需要的和平空间，这同时也助长了他们社会中倡导诡辩，脱离现实的思想。因此，他最近开始了和太阳堡垒与联合王国之间的开放贸易，希望能给他的族人带来一些看待问题的全新视角。由于我只有短暂停留在这里的机会，并没有时间能够深入分析他们的社会。因此，我唯一能够注意到的，他们社会中的深层因素，就是他们将身体健壮看的和对智慧的追求同样重要。也许这是因为，他们的蒸汽科技的力量，不仅可以来源于精巧高效的设计，[b]也[/b]可以来自于能够从排气孔中喷出更多蒸汽的，强大的肉体力量。因此，他们的政府，是通过某种由民主体制和血腥竞技结合而成的制度选拔出来的（除了国王特拉格拉玛统治的短暂时期，卡西罗斯只告诉我，“这件事对所有相关人员来说都是相当尴尬的”）。尽管我不知道这是否反映了气之部族人的某种重要品质，我觉得我还有必要特别提一句，他们还掌握着酿造我所尝过的最好的苦艾酒的技术。

唉，我没有机会研究他们足够长的时间，所以我的发现只有这些了。卡西罗斯告诉我，他不能再陪我了，因为他和马基·埃亚尔的英雄之间已经安排好了一场聚会——好像是有关使用探险远行传送门来进行垃圾清理？不管怎样，尽管我们大部分人和气之部族之间唯一的沟通的渠道，就是从飞艇上掉下来的装置，我们很快就会获得和更多他们面对面接触的机会。也许，未来还会有除了我之外的来访者，被许可亲自访问他们美丽的城市。他们在粉碎克鲁克叛乱，以及阻止他们的领袖强占[b]撼天动地，无耻的天空肆虐者[/b]中所作出的贡献，已经向我们证明，他们将会是我们未来一段时间中当之无愧的盟友。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00503 | remaining | remaining:rem-03:C07 | confirmed |  |  |  |

<details><summary>hrq-00503 · remaining 详情</summary>

```
### C07 | entry-03856 | confirmed

原译“不谨慎的发明”将 *careless intervention* 的对外介入错作发明；“排气行为通常是不可见的”把 *they* 所指的毛孔、排气口换成排气行为。若只看薄雾描述，后者可勉强理解为排气不明显，但不能解释随后“封闭或扩张它们”的指代。末段又把专名 *IMMOLATUS* 译成“撼天动地”，丢失名称。三处均有文本反证。见[misc.lua:139](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua:139>)、143、147行及[译文:2637](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260920260922/remaining-review-20260923/snapshots/tome-orcs.lua:2637>)、2641、2645行。
```
</details>

## entry-03860

- 位置：`tome-orcs.lua:2690`（orcs）｜section：`tome-orcs/data/lore/palace-fumes.lua`｜source_tag：`_t`
- 原文：`A Plea from the Volunteer's Bureau of Gaming:

Once again, we find ourselves faced with an election for the competition of Chief Councilor.  While this is the most prestigious position in our government, it should not be forgotten that is also arguably the most complex, and the one bearing the greatest responsibility for the fate of our people.  A Chief Councilor's duties require not only cautious, reasoned foresight, but a quick wit to get emergencies under control in little time; yet, he or she must be aware of the precedent set or the unintended consequences of such decisive action, never acting rashly or out of ill temper.  Such a leader would wield our citizens and our military like a drunkard with a glass bottle, not caring if his weapon is shattered in the process. He or she must be able to develop creative solutions to problems but be open to outside advice, to be a character judge capable of selecting his or her most valuable acquaintances and a persuader to convince them to do the tasks for which they are most suited...  suffice to say, there are a great many mental skills required.  Accordingly, the competition should be one that tests all these skills.

This election, we are formally endorsing the board game [i]Automobiles and Automatons v9.8,[/i] a refined variant of the game introduced last year in a competition for the Marshall of the City Guard.  Its "oil-punk" science-fantasy setting, although perhaps easy to brush off as irrelevant to our reality, has its own consistent internal rules, forcing its players to learn a new status quo and work with it, as our leaders must be willing to learn from ongoing events and rapidly adapt to them; yet, since the game has been out for a year already and there are already numerous books about strategies for it, it also tests our candidates' long-term memory, as our leaders must be able to remember our history, to repeat our ancestors' successes but not their failures.  The rules of v9.8 are somewhat, but not entirely, different from those of previous versions, making these strategy books only partially accurate, just as our ancestors' wisdom only reflected the world they lived in, not the increasingly different one of the present.

v9.8 uses the "Crumbling Divide" map, providing a barrier that eliminates the possibility of an aggressive player gaining an early victory, tests the players' ability to plan in the long term, and yet due to the presence of non-player foes on either side, they still must be able to make plans in the short-term that will ensure their survival and leave them in an advantageous position when the barrier fades.  Non-player foes follow a predictable set of rules, eliminating luck as a factor, and our necropsychs have found a method of copying the same spiritual consciousness into two figurines, meaning that both players will be using identical sets of Negotiator figurines to demonstrate their diplomatic finesse.  (As always, the figurines are designed to release their spirits after no more than one month, ensuring that this process is as humane as possible to the deceased.)

The consumer edition of this game, v6.0, has won countless awards for its engaging and challenging play, with special attention given to the diverse array of viable strategies and skills tested by it.  Both sides agreed it was a fair game in the Marshall's election, as v1.0; v9.8 is unlikely to disappoint as a method of selecting our next leader.  Vote for [i]Automobiles and Automatons v9.8[/i] this year, and you will not be let down by its winner.`
- 现译：`游戏志愿者局的请愿：

又一次，我们面临着选举议长的比赛了。这是政府中最有名望的职位，但也别忘了它可以说是最复杂的职位，承担着我们人民命运的最大责任。一个议长不仅需要谨慎而理性的远见，也需要在短期内解决紧急事态的急智；并且，他或她必须明白这些决定的先例以及非预期后果，行动既不冒进也不出于心血来潮。否则，这样的领袖会像是一个醉鬼拿着玻璃瓶那样，轻率地对待我们的人民和军队，而不关心那武器是否会破碎。他或她必须能创造性地解决问题，同时包容外界的建议，还要做一个知人者，能选出他或她身边最具价值的人才，以及一个说客，能说服这些人去做他们最适合的工作……可以说，成为议长需要很多精神上的技能。因此，这个竞赛必须要考验所有这些技能。

这次选举，我们隆重推出桌面游戏[i]汽车与机器人第9.8版[/i]，一款去年曾用于选出城市卫兵团长的游戏的改良版。它基于“石油朋克”的科幻设定，或许会被认为与现实不符而被人忽略，但它有着它严谨的内部规则，会迫使其玩家学习新的环境并掌握它，就像我们的领袖们也必须愿意从正在进行的事件中学习并迅速适应它们；并且，由于这个游戏已经推出了一年，有无数关于游戏策略的书已经被出版，玩这个游戏也能测试候选人的长时记忆，因为我们的领袖必须得以史为鉴知兴衰。9.8版本的规则和之前的版本略有不同，但却并非完全不同。这样，那些策略书籍仅仅是部分准确的，就像我们祖先的智慧只能反映他们所处的时代，而不是面临巨变的今日。

9.8版本使用“破碎两极”地图，地图中有一个结界，这消除了那些具有侵略性的玩家获得快速胜利的可能性，测试了玩家们长期谋划的能力，而且因为两侧都有非玩家敌人，他们仍然要有短期计划，以保证生存，并在结界消散后占据优势。非玩家的敌人遵循可预测的规则，排除了运气因素，我们的通灵师也找出了一个把相同意识复制到两个模型中的办法，这意味着双方玩家都会使用相同的谈判者模型来体现他们的外交手腕。（和往常一样，这个模型被设计成在使用后一个月内解放里面的灵魂，以确保这一过程对于亡者来说尽量人道。）

这一游戏的消费者版本，6.0版，以它令人沉浸又富于挑战的游戏性已获得了无数奖项，尤其因它不同类型的多变策略，以及其对多种技能的综合考验备受瞩目。在1.0版本的游戏用于选出卫兵队长时，双方都同意游戏是公平的；作为选出我们下一个领袖的方式，9.8版本绝对不会令人失望。今年，投[i]汽车与机器人第9.8版[/i]一票吧，你不会为它的胜者而失望的。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00504 | remaining | remaining:rem-04:C01 | confirmed |  |  |  |
| hrq-00505 | remaining | remaining:rem-04:C02 | advisory |  |  |  |
| hrq-00506 | remaining | remaining:rem-04:C03 | advisory |  |  |  |
| hrq-00507 | remaining | remaining:rem-04:N01 | confirmed |  |  |  |

<details><summary>hrq-00504 · remaining 详情</summary>

```
### C01 | entry-03860 | confirmed

原译“隆重推出”把 *formally endorsing* 的正式支持、推荐写成推出游戏。最强等价读法是“推出”也可指提出候选方案；但这里直接接“桌面游戏”，容易读成发布产品，丢失公投中的支持立场。建议改为“正式推荐”或“公开支持”。游戏已有一年这一点不能单独证明 9.8 版也早已上市。证据：B:26、P:27,38。
```
</details>

<details><summary>hrq-00505 · remaining 详情</summary>

```
### C02 | entry-03860 | advisory

同一篇文献先称 *Marshall of the City Guard* 为“城市卫兵团长”，后称 *Marshall’s election* 为“选出卫兵队长时”。两处确属同一职位。最强等价读法是“团长”“队长”都能泛指卫兵指挥者，读者仍可从选举语境认出同一人；故属篇内称谓统一建议，不据此认定两个职位被实质混淆。建议统一用词。证据：B:26,30、P:38,42。
```
</details>

<details><summary>hrq-00506 · remaining 详情</summary>

```
### C03 | entry-03860 | advisory

“精神上的技能”对应 *mental skills*，前文列的是远见、急智、识人和说服能力。“精神”可能显得生硬。最强等价读法是“精神上的技能”在这串举例后仍可理解为心智能力；没有证据表明读者必然理解成游戏中的灵能机制。可润色为“心智能力”或“才智”，不按机制错译处理。证据：B:24、P:36。
```
</details>

<details><summary>hrq-00507 · remaining 详情</summary>

```
### N01 | entry-03860 | confirmed

另发现原译“在**使用后**一个月内解放里面的灵魂”增添了计时起点。英文只说模型设计成 *after no more than one month* 释放灵魂，没有说从游戏使用结束后才开始计算。最强等价读法是使用与灵魂进入模型可能同时发生，但文本未作此限定。建议删除“使用后”，保留“不超过一个月”。证据：B:28、P:40。
```
</details>

## entry-03861

- 位置：`tome-orcs.lua:2708`（orcs）｜section：`tome-orcs/data/lore/palace-fumes.lua`｜source_tag：`_t`
- 原文：`Councilor Tantalos, unlike that cowardly wimp Chief Councilor Kasyros, knows just what to do to solve the steam shortages, and isn't afraid to do it!  Even though he can't reveal his plan yet for security reasons, the Geothermal Authority and our military's highest generals have assured us that his plan would work, without requiring us to ration steam usage or regulate our appliances; let's see Tantalos show that old geezer what-for, and end this drought for good!

VOTE FISTICUFFS`
- 现译：`坦塔洛斯议员，不像卡西罗斯议长那位懦弱的窝囊废。他知道该如何解决蒸汽短缺的问题，也不怕去执行这一方案！即使由于安全原因，他现在还不能公布计划，地热局和我们军队高级将领已经向我们保证，他的计划一定会奏效，我们再也无需节省蒸汽用量或是管控我们的器具；让我们看看坦塔洛斯怎样让那个老东西难堪，并永远结束蒸汽枯竭！

[b]请投肉搏战[/b]`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00508 | remaining | remaining:rem-04:C04 | confirmed |  |  |  |
| hrq-00509 | remaining | remaining:rem-04:C05 | advisory |  |  |  |

<details><summary>hrq-00508 · remaining 详情</summary>

```
### C04 | entry-03861 | confirmed

源码口号只有纯文本大写 *VOTE FISTICUFFS*，原译加入 `[b]请投肉搏战[/b]`。最强等价读法是粗体模拟英文大写的强调；但它仍新增了源文本没有的富文本标记，改变格式内容。建议移除标签。这里确认的是标记增添，未据此声称运行时会显示错误。证据：B:46、P:52。
```
</details>

<details><summary>hrq-00509 · remaining 详情</summary>

```
### C05 | entry-03861 | advisory

*show that old geezer what-for* 译成“让那个老东西难堪”，保留了对政敌的羞辱，却弱化了“给他点颜色瞧瞧”的挑衅力度。最强等价读法是政治竞选口号中的“难堪”也可以指让对手败阵，未必承诺实际殴打；因此不把肉搏口号推定为字面暴力。建议酌情增强语气。证据：B:44、P:50。
```
</details>

## entry-03864

- 位置：`tome-orcs.lua:2808`（orcs）｜section：`tome-orcs/data/lore/palace-fumes.lua`｜source_tag：`_t`
- 原文：`(Ink has been spilled on this transcript - you can only read certain passages.)

???: "[...]ame me for this!  YOUR mechanics examined that airship, YOUR equipment was used to repair it, and it's YOUR fault it went down!"

NASHAL: "Yes, and I told you to call the attack off the moment I heard the news - the Loyalist's wand as a fire-support tool was far too valuable to conduct the invasion without it.  But no, Palaquie had to insist on going right then--"

PALAQUIE: "My visions do not lie.  It was the best way forward.  Our odds of success at that point, low as they were, were still better than if we had let Pendor's inflexible, time-dependent plan sit and--"

PENDOR: "DON'T YOU EVEN START, YOU YETI-LOVI--[...]"

[...]

Motion made to record the statement that Councilor Pendor would not know decent equipment if it shot or stabbed him in the face passed, 3-1, with Councilor Tantalos abstaining.

Motion made to record the statement that Councilor Tormak's robes smell of absinthe and vagrants passed, 3-1, with Councilor Tantalos abstaining.

Motion made to begin an official inquiry passed 3-1, with Councilor Tantalos abstaining.  The first order of business at the next session will be determining whether or not Councilor Nashal's state-of-the-art mining and extracting equipment is capable of extracting her head from her--

[...]

TANTALOS: "If you are all quite finished with this rubbish...  How bad is the situation, exactly?  I want details and facts, not blame."

TORMAK: "You don't want blame because this whole thing was YOUR idea!  It's YOUR fault we--"

Motion to censure Councilor Tantalos for defenestrating Councilor Tormak has failed, 1-1 (tie broken by Chief Councilor status), with Palaquie, Nashal, and Pendor abstaining.

[...]

TANTALOS: "So, a few wastrels in the marketplace are gone, and the Kruk have moved on to the mainland.  As far as I am concerned, they are not presently our responsibility - these 'Allied Kingdoms' and 'Sunwall' folk can deal with them.  Thanks to Pendor's scouts, we have a weapon we can point at the Kruk Pride homeland as a deterrent, which should buy us even more time.  We should use this time to bolster our defenses...  and consider additional options.  Meeting adjourned."

PALAQUIE: "Additional options?"

TANTALOS: "The meeting has been adjourned.  You should be training our necropsychs, Councilor."`
- 现译：`（墨水被洒在这个记录上————你只能读到一些段落。）

？？？：“[……]怪我！那架飞船是你的机械师检查的，是在用你的设备修理它，也是因为你的错它才坠落！”

纳沙尔：“是吗，我在听到那个消息时也告诉你了要取消攻击————忠诚者的魔杖作为火力支援工具太珍贵了，我们进攻的时候绝对离不了它。但不，帕拉奎非要坚持当即出发————”

帕拉奎：“我眼前的景象不会作假。那是前进最好的方法。我们那时的成功几率虽然低，还是强于假如让潘多尔做主，用那个不灵活，依靠时机的方案————”

潘多尔：“你再说一句看看，你这个恋雪人————[……]”

[……]

记录下“潘多尔议员不知道什么是优良的设备，除非亲自射到或者刺到他脸上”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

记录下“托马克议员的长袍闻起来有苦艾酒和流浪汉的味道”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

进行官方调查的动议以3比1的投票通过，议员坦塔洛斯弃权。接下来进行调查的第一部分，将会决定是否纳沙尔议员的最新式采矿和提取工具能够将她的头从她的————

[……]

坦塔洛斯：“如果你们都闹够了……到底情况有多糟糕？我想要细节和事实，而不是抱怨。”

托马克：“你不想要抱怨是因为整件事都是你的主意！这是你的错所以我们————”

谴责坦塔洛斯议员把托马克议员扔出窗外的动议未被通过（1比1，平局被议长否决），议员帕拉奎、纳沙尔和潘多尔弃权。

[……]

坦塔洛斯：“所以，商场里的那些饭桶死了，克鲁克兽人已经开始在大陆行动。据我所知，这目前不是我们应当担心的————那些“联合王国”和“太阳堡垒”的家伙们可以对付。多亏了潘多尔的斥候，我们有了一个武器，可以作为一个威慑力量对准克鲁克部落的老家，这会给我们争取更多的时间。我们应该用这段时间加强守备……并考虑其他方案。散会。”

帕拉奎：“其他方案？”

坦塔洛斯：“已经休会了。你现在应该去训练我们的通灵师，议员。”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00510 | remaining | remaining:rem-04:C06 | confirmed |  |  |  |
| hrq-00511 | remaining | remaining:rem-04:C07 | confirmed |  |  |  |
| hrq-00512 | remaining | remaining:rem-04:C08 | confirmed |  |  |  |

<details><summary>hrq-00510 · remaining 详情</summary>

```
### C06 | entry-03864 | confirmed

两处 *blame* 均译作“抱怨”。最强等价读法是争吵时的抱怨可能包含指责；但托马克紧接着说“这是你的错”，争点明确是事故责任归属。“我想要事实，而不是抱怨”“你不想要抱怨”因此偏离原意。建议分别改作“指责／追责”等与上下句衔接的说法。证据：B:110,112、P:139–141。
```
</details>

<details><summary>hrq-00511 · remaining 详情</summary>

```
### C07 | entry-03864 | confirmed

“接下来进行调查的第一部分”把 *the first order of business at the next session* 写成调查阶段。最强等价读法是官方调查刚获通过，下一次会议可能讨论调查；但原句明确指定“下次会议”的首项议程，并借拔出纳沙尔头颅开玩笑，并未划分调查步骤。建议译为“下次会议的首项议程”。证据：B:106、P:135。
```
</details>

<details><summary>hrq-00512 · remaining 详情</summary>

```
### C08 | entry-03864 | confirmed

“据我所知”将 *As far as I am concerned* 的个人立场变成知情范围；同句 *not presently our responsibility* 又译为“不是我们应当担心的”，把责任判断变成忧虑程度。最强等价读法是说话人确实在表态不愿介入，但两处合起来仍削弱了主动推卸责任的意思。建议改为“在我看来，他们目前不归我们负责”。证据：B:118、P:147。
```
</details>

## entry-03865

- 位置：`tome-orcs.lua:2874`（orcs）｜section：`tome-orcs/data/lore/palace-fumes.lua`｜source_tag：`tformat`
- 原文：`TANTALOS: "Tell the others of the unfortunate developments, Palaquie."

PALAQUIE: "The Kruk Orcs, under %s, appear to have pushed to the last bastion of the Sunwall forces...  none of my visions predict this ending favorably for anyone of non-Orcish descent.  With the Sunwall gone, there will be no further distractions for the Kruk.  In short, the Sunwall are doomed - and we are next."

TANTALOS: "Where there's a will, Palaquie, there's a way.  What of the Migratory Leviathan?  Nashal, do you have any idea where--"

NASHAL: "About that...  Kasyros stole it when everything started going to slag.  We'd take it back, but he's using it to evacuate civilians.  We'd end up using too many bullets on our own people that belong in the Kruk Orcs."

TANTALOS: "Unfortunate, but we'll surely be able to convict him of treason once this all blows over.  Pendor, you've been working with our marksmen - how are they doing?"

PENDOR: "Scared scrapless, Your Honor, but they're learning quick.  I managed to snatch up some newer Flameshot rifles from Kaltor's surplus, and our Retaliators are as strong as ever."

TANTALOS: "Splendid to hear.  And what of that backup weapon you had mentioned - what was that name again, #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF-#{normal}#"

TORMAK: "It's gone.  The mages I sent with Pendor's runners...  their invisibility spells were inadequate.  The Orcs found them...  if it's any consolation, they don't appear to have realized what the keys are for, or what it's capable of.  I'm...  I'm sorry."

Lengthy pause.

TANTALOS: "...I think it's time."  Removes a briefcase from behind the podium, and opens it to show the other Councilors its contents, before closing it and holding it again.  Councilors Palaquie, Tormak, and Nashal audibly gasp.  Motion to strike all description of its contents from the record passed, 3-2.

TORMAK: "You can't be serious!  How is that going to make the situation BETTER?"

PALAQUIE: "It cannot."

NASHAL: "I can't agree with this, Councilor Tantalos, your predecessor had a point--"

TANTALOS: Pounds fist, breaking podium.  "That doddering old coward knew NOTHING!"  Pause; sighs.  "None of us do.  All we know is, this eye's almost certainly useful for more than making declogging draught from its tears, and the person who wants it is the type of person who casually digs holes to the center of Eyal.  We've tried everything; the time for a last resort has come, and we are in dire need of a miracle.  This... 'Loyalist' is the only possible source of miracles around, and if infinite energy and blasting holes through the planet are within his capabilities, then disposing of these barbarians should be quite simple."

PALAQUIE: "If our ancestors are to believed, this could result in a fate worse than our own destruction--"

TANTALOS: "Would everyone who doesn't have any #{italic}#better#{normal}# ideas cease their jabbering before I cease it #{italic}#for them?#{normal}#"

[Silence.]

TANTALOS: "As I thought.  Nashal, prepare the G.E.M. and a retinue of guards and mechanics.  There is business I must attend to.  Meeting adjourned."`
- 现译：`坦塔洛斯：“告诉大家现在的不利形势，帕拉奎。”

帕拉奎：“克鲁克兽人，在%s的带领下，看上去已经攻到太阳堡垒军的最后一个堡垒了……我的各个预测景象都不会倾向于任何非兽人血统的一方获取胜利。太阳堡垒陷落后，对于克鲁克兽人就没有什么阻碍了。简而言之，太阳堡垒气数已尽————而我们是下一个。”

坦塔洛斯：“帕拉奎，有志者事竟成。“迁徙的利维坦”怎么样了？纳沙尔，你知不知道它在————”

纳沙尔：“那个啊……在事态变得糟糕的时候，卡西罗斯偷走了它。我们想要把它夺回来，但是他正在用它撤离平民。如果那样的话，我们会把大量本应用在克鲁克兽人身上的子弹，射向我们自己的人民的。”

坦塔洛斯：“真不走运，不过一切结束后我们一定能定他叛国罪。潘多尔，你最近在训练我们的枪手吧————他们怎样了？”

潘多尔：“那群废物们吓得不轻，尊敬的议长，但是他们进步得很快。我从卡尔托剩下的货物中收集了一些新式的喷火步枪，而我们的复仇者部队处在巅峰状态。”

坦塔洛斯：“听起来真不错。那个你提到过的备用武器————叫什么来着，#{bold}#毁天灭地、无礼的贯穿者————#{normal}#”

托马克：“它不见了。那些我派给潘多尔的传令兵的法师……他们的隐形咒语不准。兽人们找到了他们……若这算是一点安慰，他们似乎还没意识到钥匙是做什么用的，也不知道那些武器能做什么。我……我很抱歉。”

漫长的沉默。

坦塔洛斯：“……我认为是时候了。”从讲台后拿出一个手提箱，打开给其他议员看里面的东西，又合上它把它收起来。帕拉奎、托马克和纳沙尔议员都发出喘气声。清除有关箱子里东西的记录的动议以3比2通过。

托马克：“你别开玩笑吧！这东西怎么能改善现在的情况？”

帕拉奎：“它不能。”

纳沙尔：“我不能同意这样做，坦塔洛斯议员，您的前任的观点确实有道理————”

坦塔洛斯：挥拳砸桌子，把讲台砸烂了。“那个走不稳路的老懦夫什么也不知道！”停顿；叹气。“我们也都不知道。我们知道的是，这个眼的作用肯定不仅仅是用它的泪水来做清淤药水，而想要它的人，是那种可以随心所欲挖出通向埃亚尔地心的洞的人。我们已经试过了所有方案；最后挣扎的时刻来临了，我们相当渴望一个奇迹。这个……“忠诚者”是我们身边唯一可能的奇迹来源，如果无限能源和在星球中间穿洞在他的能力限度之内，那么把那群野蛮人赶走应该非常简单。”

帕拉奎：“如果我们的祖先可信的话，这可能比我们自身的毁灭更糟糕————”

坦塔洛斯：“你们这些想不出#{italic}#更好#{normal}#主意的人能不能闭上叽叽喳喳的嘴，在我来#{italic}#帮你们#{normal}#闭上之前？”

[沉默。]

坦塔洛斯：“这就对了。纳沙尔，准备好GEM，随从的守卫和机械师。我还有要做的事情。散会。”`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00513 | remaining | remaining:rem-04:C09 | confirmed |  |  |  |
| hrq-00514 | remaining | remaining:rem-04:C10 | confirmed |  |  |  |
| hrq-00515 | remaining | remaining:rem-04:C11 | advisory |  |  |  |
| hrq-00516 | remaining | remaining:rem-04:N02 | confirmed |  |  |  |

<details><summary>hrq-00513 · remaining 详情</summary>

```
### C09 | entry-03865 | confirmed

“毁天灭地”与术语快照对 *DESTRUCTICUS* 明列的“毁灭号”相冲突，备注还明确排除前者。最强等价读法是本句为夸张喊名，且术语记录的 `source_tag` 是 `_t`、本条是 `tformat`；但它仍指同一武器专名，备注明确覆盖叙词，`dlc` 范围适用于 orcs。建议按专名改为“毁灭号”。证据：B:180、P:170、T:1257–1264。
```
</details>

<details><summary>hrq-00514 · remaining 详情</summary>

```
### C10 | entry-03865 | confirmed

*invisibility spells were inadequate* 说的是隐形法术不足以避开兽人发现；“隐形咒语不准”通常指准确性，未清楚表达隐蔽效果不足。最强等价读法是口语中的“不准”也可能泛指法术不灵，但本句没有瞄准目标，且下句明确是被发现。建议改为“隐形法术不够有效”或“没能瞒过兽人”。证据：B:182、P:172。
```
</details>

<details><summary>hrq-00515 · remaining 详情</summary>

```
### C11 | entry-03865 | advisory

*disposing of these barbarians* 译为“把那群野蛮人赶走”，语气较轻。最强等价读法成立：*dispose of* 可泛指解决威胁，驱逐也是一种解决方式；原句虽提到强大破坏力，并未明确指定杀尽兽人。因此不能据此确认“灭绝意图”被错译。若要贴近冷酷语气，可用不预设具体方式的“除掉／解决掉”。证据：B:194、P:184。
```
</details>

<details><summary>hrq-00516 · remaining 详情</summary>

```
### N02 | entry-03865 | confirmed

另发现“那些武器能做什么”把 *what it’s capable of* 的单数指代写成复数武器。前文谈一件备用武器及其钥匙；最强等价读法是多把钥匙可能让人联想到多件装备，但原句的 *it* 仍指这件武器。建议改为“它能做什么”。证据：B:180,182、P:170,172。
```
</details>

## entry-03871

- 位置：`tome-orcs.lua:3307`（orcs）｜section：`tome-orcs/data/lore/sunwall.lua`｜source_tag：`tformat`
- 原文：`We've done it... we've finally done it. Well, granted, our %s did much of the work, but the result is the same: neither the East nor the West will ever need to fear Orcish rule again. The Prides have been crushed, the survivors have been contained, and our patrols are mopping up the few remaining bands of futile stragglers. Our long-lost allies from the West have come to support us with materials and manpower, and we can finally turn this entire continent into something beautiful. For the first time, Sunwall will not be the solitary bastion of civilization on Var'Eyal.

And yet...

There is one group that remains.  A tiny Orcish pride, really more of a small town, managed to evade our savior's wrath...  a single weed on the edges of our pristine garden, a troubling ember threatening to set the whole continent aflame.  King Tolak has noble aims in trying to set a better example than his vengeful father, but I doubt he'd risk redeeming the Orcs if he'd been through what we have.  The Allied Kingdoms don't know what it's like to live in fear of the Prides, knowing that at any moment they could overrun the Sunwall and take our heads as trophies.  They've got a farportal to hide behind, and don't have to think about their homes and families falling to the same horror that we've been struggling against for our entire lives.  If they did...  suffice to say, they wouldn't have bothered putting up a comfortable camp for the surviving Orcs until the continent was truly safe.

By the Sun...  why would our High Paladin agree to this treaty?  After what we've all been through...

The Orcish scouts are getting bolder.  They've been approaching closer before fleeing, and coming more frequently.  They haven't engaged us yet, but it's only a matter of time...  and all I'm allowed to do is sit and wait on this ugly little bridge, as the West watches from a continent away.  Staring at an open wound, waiting for it to become infected, because they'd rather make a pretty little bow out of the bandages.`
- 现译：`我们做到了……终于做到了。好吧，诚然，大部分工作是我们的%s完成的，但结果并无不同：东方和西方都再也不必惧怕兽人统治。四大兽人部落已被粉碎，幸存者受到控制，巡逻队正在扫荡所剩无几、徒劳流窜的残兵。失散已久的西方盟友带着物资和人力前来支援，我们终于可以把整片大陆建设得更加美好。太阳堡垒将第一次不再是瓦·埃亚尔唯一的文明堡垒。

然而……

仍有一群兽人存在。一个小小的兽人部落——其实更像一座小镇——躲过了救世主的怒火……如整洁花园边缘的一株杂草，又像威胁点燃整片大陆的一点余烬。托拉克国王试图树立比复仇心切的父亲更好榜样，志向固然高尚；可若他经历过我们所经历的一切，我怀疑他是否还会冒险去拯救兽人。联合王国不知道活在四大部落阴影下是什么滋味，不知道太阳堡垒随时可能被攻陷、我们的头颅被割下当作战利品的恐惧。他们有远行传送门可作屏障，无需担心家园和亲人遭遇我们一生都在抗争的同样恐怖。如果他们也要担这种心……只消说，在大陆真正安全之前，他们绝不会费心为幸存兽人搭起舒适营地。

以太阳之名……经历这一切之后，我们的至高太阳骑士为何还会同意这份条约？

兽人斥候越来越大胆。他们逃走前会靠得更近，出现得也更频繁。虽然尚未交战，却只是时间问题……而我获准做的只有坐在这座难看的小桥上等待；西方人则从另一个大陆远远观望。就像盯着一道敞开的伤口，等它感染，只因他们宁愿把绷带系成漂亮的蝴蝶结。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00517 | remaining | remaining:rem-04:C12 | refuted |  |  |  |

<details><summary>hrq-00517 · remaining 详情</summary>

```
### C12 | entry-03871 | refuted

“至高太阳骑士”对应本句 *our High Paladin*，词义可通。所引术语记录实际是完整专名 *High Sun Paladin Aeryn*，`scope` 为 `core`，而本条是 orcs DLC 中省去姓名的称谓；不能据该记录强制本句改成“高阶太阳骑士”。为全库风格统一而调整仍可讨论，但原疑点所称的术语违规不成立。证据：B:228、S:37、T:1807–1814；适用规则见 [RULES.md:6](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md:6)。
```
</details>

## entry-03875

- 位置：`tome-orcs.lua:3579`（orcs）｜section：`tome-orcs/data/lore/weissi.lua`｜source_tag：`_t`
- 原文：`If you would indulge us...  Next to you is a tablet that was just carved by our machines, moments before you arrived.  If our curse holds, it will be completely illegible, but if it has been lifted, it will bear our name.  A blatant, distinct word that is an undeniable mark of our existence, a sign that no matter how it may have wanted to, the universe could not forget us.  Look to your right, and learn the name of those who have far more right to exist than you do, who have fought far harder for it, and will sink their hooks so deep into reality that it must either lift them up or be dragged into the depths with them.  Learn the name feared by existence itself!

#{italic}#(You look to your right, and see a tablet which has been broken into fragments.  The fragments are still arranged roughly in the right shape, and you can read a single word; another, larger fragment bears a sentence.)#{normal}#

`
- 现译：`如果你还愿意继续听下去的话……在你身边，是一块石板，是在你过来时前刚刚由我们的机器雕刻完成的。如果我们的诅咒还在持续下去，上面的字将会是完全无法辨认的，而如果诅咒被解除，这上面会刻着我们的名字。那是一个显眼、独特的名字，是我们存在的无可否认的标志。一个表明，宇宙也忘不了我们。往你右边看，看看我们这个群体的名字，这一群体比你们远远更有权利存在，却不得不为了那权利比你们都努力地斗争，他们奋力将钩子扎入最深的现实，让现实不得不要么将他们连根拔起，要不被他们一道拖进深渊。看吧，这个被存在本身畏惧的名字！

#{italic}#（你往右看，看到一块破裂成碎片的石板。石板仍然按照正确的形状排列，你可以读到一个词；另一个大一些的碎片上有个句子。）#{normal}#

`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00518 | remaining | remaining:rem-11:C01 | confirmed |  |  |  |
| hrq-00519 | remaining | remaining:rem-11:N01 | advisory |  |  |  |

<details><summary>hrq-00518 · remaining 详情</summary>

```
### C01 | entry-03875 | confirmed

原译“让现实……将他们连根拔起”把 *lift them up* 译成了拔除。最强等价读法是：既然前文说“将钩子扎入现实”，这里的“拔起”也许指拔起钩子；但英文宾语 *them* 指维西一族，并与“现实被他们拖入深渊”构成托起或同坠的选择。建议改为“让现实要么托起他们，要么与他们一道坠入深渊”。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3579)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua:107)。
```
</details>

<details><summary>hrq-00519 · remaining 详情</summary>

```
**N01 | entry-03875 | advisory**：“宇宙也忘不了我们”省去了 *no matter how it may have wanted to* 所含的“即便宇宙想忘记”意味。同篇已交代宇宙敌视维西一族，读者可由上下文补足，故建议润色为“即便宇宙想忘记，也无法忘记我们”，不另列确认错译。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3583)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua:107)。
```
</details>

## entry-03883

- 位置：`tome-orcs.lua:3893`（orcs）｜section：`tome-orcs/data/quests/yeti-abduction.lua`｜source_tag：`_t`
- 原文：`Call a trained yeti to your side.`
- 现译：`召唤雪人来协助你。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00520 | remaining | remaining:rem-11:C02 | advisory |  |  |  |

<details><summary>hrq-00520 · remaining 详情</summary>

```
### C02 | entry-03883 | advisory

原译“召唤雪人来协助你”省去 *trained*。最强等价读法成立：同 section 的任务说明已交代野雪人会受训，使用动作又译作“召唤受训练的雪人来帮助你”，玩家仍可理解召来的对象。道具说明单独出现时补上“受训”会更明确；建议润色，不列确认错译。证据：[同 section 原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3887)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua:45)。
```
</details>

## entry-03890

- 位置：`tome-orcs.lua:3965`（orcs）｜section：`tome-orcs/data/talents/celestial/energies.lua`｜source_tag：`tformat`
- 原文：`Increases your movement speed by %0.2f%% per percent of positive energy and your casting speed by %0.2f%% per percent of negative energy, up to a maximum of %0.2f%% at 80%%. Sustained energy still counts toward the maximum.`
- 现译：`每 1%% 的正能量增加 %0.2f%% 的移动速度，每 1%% 的负能量增加 %0.2f%% 施法速度，在 80%% 时达到最大值，为 %0.2f%%. 持续能量仍然算向最大值。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00521 | remaining | remaining:rem-11:C03 | advisory |  |  |  |

<details><summary>hrq-00521 · remaining 详情</summary>

```
### C03 | entry-03890 | advisory

原译“持续能量仍然算向最大值”生硬，容易让“持续能量”被读作持续恢复的能量。最强等价读法是：读者结合技能语境，仍可把“持续”理解为维持技能占用的能量；源码注释也明确谈及 *sustains* 对可用上限的影响。因此保留表达澄清建议，改作“维持技能占用的能量仍计入上限”，不据此断定数值机制译错。证据：[原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3965)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/energies.lua:32)。
```
</details>

## entry-03892

- 位置：`tome-orcs.lua:3977`（orcs）｜section：`tome-orcs/data/talents/celestial/reflection.lua`｜source_tag：`_t`
- 原文：`Create a distortion at the target tile, knocking back all projectiles and changing their direction to face away if possible.`
- 现译：`在目标所在地创造一个地块，击退所有的飞行物如果可能的话还会改变他们的方向。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00522 | remaining | remaining:rem-11:C04 | confirmed |  |  |  |

<details><summary>hrq-00522 · remaining 详情</summary>

```
### C04 | entry-03892 | confirmed

原译“在目标所在地创造一个地块”把 *distortion* 丢失，并把地点 *at the target tile* 误作创造对象。最强等价读法是“地块”仅指效果位置；但“创造一个地块”的句法明确说创造地块，邻近技能另有真正造墙的描述，不能替它补出“扭曲”。建议译为“在目标地块制造一处扭曲，击退投射物，并尽可能使其转向外侧”。证据：[同 section 原译](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:3977)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/reflection.lua:135)。
```
</details>

## entry-03912

- 位置：`tome-orcs.lua:4559`（orcs）｜section：`tome-orcs/data/talents/steam/automated-butchery.lua`｜source_tag：`tformat`
- 原文：`You send a saw mounted on an automated steam propulsor to assault a foe, dealing %0.2f physical damage each turn for 4 turns and silencing it.
		At the end of the duration, the saw explodes for %0.2f fire damage and flies back, pulling the target up to %d tiles towards you.
		The damage will increase with your Steampower.`
- 现译：`你用自动蒸汽弹射器向敌人发射一把链锯，造成 %0.2f 物理伤害并沉默敌人，持续 4 回合。
		持续时间结束后，链锯爆炸，造成 %0.2f 的火焰伤害并飞回，将目标向你的位置拉扯 %d 格。
		伤害受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00523 | remaining | remaining:rem-12:C01 | confirmed |  |  |  |

<details><summary>hrq-00523 · remaining 详情</summary>

```
### C01 | entry-03912 | confirmed

原译「造成 %0.2f 物理伤害并沉默敌人，持续 4 回合」漏掉伤害频率。最强等价读法是将“持续 4 回合”同时理解为伤害和沉默的持续时间，但它仍不能说明 **%0.2f 是每回合伤害**。源码的效果每回合施加 `eff.power` 物理伤害。建议补出“每回合造成”。证据：`snapshots/tome-orcs.lua:4559-4563`；冻结源码 `tome-orcs/data/talents/steam/automated-butchery.lua:66-93`、`tome-orcs/data/timed_effects/physical.lua:445-464`。
```
</details>

## entry-03913

- 位置：`tome-orcs.lua:4573`（orcs）｜section：`tome-orcs/data/talents/steam/automated-butchery.lua`｜source_tag：`tformat`
- 原文：`You override all security measures of your tinkers, allowing you to reset the cooldown of %d of most of your steamtech talents of tier %d or less and instantly increases your steam level by %d%% of the maximum.
		In addition for 6 turns your maximum steam capacity is doubled, but steam regeneration is halved.
		#{italic}#Master of Tech, Master of Death!#{normal}#`
- 现译：`你开启全部插件的超频模式，重置最多 %d 个蒸汽科技技能（%d 层级或以下）的冷却时间，直接恢复 %d%% 蒸汽值。
		在 6 回合内，蒸汽值最大值翻倍，但是恢复值减半。
		#{italic}#科技至尊、死亡之主！！#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00524 | remaining | remaining:rem-12:C02 | advisory |  |  |  |

<details><summary>hrq-00524 · remaining 详情</summary>

```
### C02 | entry-03913 | advisory

原译「直接恢复 %d%% 蒸汽值」省略了英文的“最大值的”。通常可将“恢复百分比蒸汽值”理解为按上限计算，故不足以判为确定错译；明确写成“恢复最大蒸汽值的 %d%%”更清楚。源码按 `getMaxSteam() * eff.regen` 增加蒸汽。证据：`snapshots/tome-orcs.lua:4573-4577`；冻结源码 `tome-orcs/data/talents/steam/automated-butchery.lua:169-179`、`tome-orcs/data/timed_effects/physical.lua:402-413`。
```
</details>

## entry-03918

- 位置：`tome-orcs.lua:4796`（orcs）｜section：`tome-orcs/data/talents/steam/butchery.lua`｜source_tag：`tformat`
- 原文：`You temporarily overcharge the saw motors, increasing the effective talent level of all saw talents by %d%% for %d turns.
		#{italic}#The pain shall never stop!#{normal}#`
- 现译：`链锯引擎临时进入过载模式，增加 %d%% 的链锯相关技能有效等级，持续 %d 回合。
		#{italic}#无尽地痛苦#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00525 | remaining | remaining:rem-12:C03 | advisory |  |  |  |

<details><summary>hrq-00525 · remaining 详情</summary>

```
### C03 | entry-03918 | advisory

原译「无尽地痛苦」中的“地”用字不当，也把原文“The pain shall never stop!”的陈述句改成了短语。最强等价读法是将它视作表达“痛苦无尽”的风味短句；核心意思尚可辨认。建议改为“痛苦永不停歇！”证据：`snapshots/tome-orcs.lua:4796-4798`；冻结源码 `tome-orcs/data/talents/steam/butchery.lua:127-130`。
```
</details>

## entry-03921

- 位置：`tome-orcs.lua:4930`（orcs）｜section：`tome-orcs/data/talents/steam/elusiveness.lua`｜source_tag：`tformat`
- 原文：`The thrill of the hunt invigorates you. For each foe in radius %d around you, you gain 20%% movement speed (up to %d%%).
		Current bonus: %d%%.`
- 现译：`被猎杀的危险令你激动不已。
		半径 %d 内每有一个敌人，你获得 20%% 移动速度（最多 %d%%）。
		当前加成：%d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00526 | remaining | remaining:rem-12:C04 | confirmed |  |  |  |

<details><summary>hrq-00526 · remaining 详情</summary>

```
### C04 | entry-03921 | confirmed

原译「被猎杀的危险令你激动不已」把 *the thrill of the hunt* 的狩猎者视角改成被猎杀者视角。周围敌人带来速度加成，可以解释角色为何兴奋，但不能证明原文采用了“被猎杀”的叙事。建议改为“狩猎的快感令你振奋”。证据：`snapshots/tome-orcs.lua:4929-4933`；冻结源码 `tome-orcs/data/talents/steam/elusiveness.lua:67-99`。
```
</details>

## entry-03924

- 位置：`tome-orcs.lua:4969`（orcs）｜section：`tome-orcs/data/talents/steam/engineering.lua`｜source_tag：`tformat`
- 原文：`Sometimes, being a master tinker requires taking risks; yours are more calculated than others.
		Gain %d cunning, %d physical save, %d%% resistance to self-inflicted damage, and %d%% chance to avoid being critically hit.`
- 现译：`成为大师意味着你经历了更多危险，你的计算力也超越凡人。
		增加 %d 灵巧，%d 物理豁免，%d%% 自身伤害抗性，%d%% 几率避免暴击。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00527 | remaining | remaining:rem-12:N01 | confirmed |  |  |  |

<details><summary>hrq-00527 · remaining 详情</summary>

```
### N01 | entry-03924 | confirmed

原译「成为大师意味着你经历了更多危险，你的计算力也超越凡人」改变了原文“技艺大师有时须冒险，而**你的风险比别人算得更周全**”。“经历了更多危险”和“计算力超越凡人”均非原文所述。后续属性数值译法无此问题。证据：`batches/rem-12.md` 的 `entry-03924`；冻结源码 `tome-orcs/data/talents/steam/engineering.lua:127-130`。
```
</details>

## entry-03925

- 位置：`tome-orcs.lua:4985`（orcs）｜section：`tome-orcs/data/talents/steam/furnace.lua`｜source_tag：`tformat`
- 原文：`While Furnace is on your armour is so hot from the furnace it dissipates parts of all energy based attacks against you.
		All non physical, non mind damage is reduced by %d (current %d).
		Each turn this happens you gain a molten point (up to 10), decreasing the efficiency of the reduction by 25%%.
		Molten points are removed upon running or resting.
		#{italic}#Hot liquid metal, the fun!#{normal}#
		`
- 现译：`你的护甲温度极高，能驱散部分能量攻击。
		所有非物理、非精神伤害降低 %d 点（当前 %d）。
		每回合该效果触发时，你获得 1 点融化点数（最多 10 点），使减伤效率降低 25%%。
		奔跑或休息时会清除融化点数。
		#{italic}#火热的液态金属，乐趣无穷！#{normal}#
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00528 | remaining | remaining:rem-12:C05 | confirmed |  |  |  |

<details><summary>hrq-00528 · remaining 详情</summary>

```
### C05 | entry-03925 | confirmed

原译「你的护甲温度极高，能驱散部分能量攻击」漏掉“**熔炉开启时**”这一生效条件。最强等价读法是借相邻的“熔炉”技能说明推知条件，但本条被动说明单独阅读会显得常驻；源码也先检查熔炉是否激活。建议补明条件。证据：`snapshots/tome-orcs.lua:4984-4995`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:56-67,88-97`。
```
</details>

## entry-03926

- 位置：`tome-orcs.lua:5007`（orcs）｜section：`tome-orcs/data/talents/steam/furnace.lua`｜source_tag：`tformat`
- 原文：`When you reach 10 molten points your armour overheats, reaching temperatures so high that they cauterize up to %d detrimental physical effects on you.
		A special medical injector injects you with a fire immunity serum at that precise moment to make you immune to the burning effect.
		When this happens all molten points are consumed and trigger a Furnace Vent at the creature that triggered the last molten point.
		This effect drains 15 steam when triggered, and will not trigger if steam is too low.
		#{italic}#It's only a flesh burn!#{normal}#
		`
- 现译：`当你达到 10 点融化点数时，你的护甲过热，温度极高，以至于 %d 个负面物理状态被高温驱散。
		同时，一个特殊的医疗注射器会为你注射火焰免疫血清，令你免疫烧伤效果。
		该效果触发时，消耗所有融化点数，并自动对最后一次提供融化点数的生物触发一次通风孔效果。
		该效果将消耗 15 点蒸汽。蒸汽不足时不能触发。
		#{italic}#只是肉体在燃烧！#{normal}#
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00529 | remaining | remaining:rem-12:C06 | advisory |  |  |  |
| hrq-00530 | remaining | remaining:rem-12:N02 | confirmed |  |  |  |

<details><summary>hrq-00529 · remaining 详情</summary>

```
### C06 | entry-03926 | advisory

原译「只是肉体在燃烧！」保留了“只是”的轻描淡写语气，但把 *a flesh burn* 表成整个肉体正在燃烧，失去局部烫伤的笑点。它是风味句，不改变技能机制；建议改为“区区皮肉烫伤罢了！”证据：`snapshots/tome-orcs.lua:5007-5017`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:170-177`。
```
</details>

<details><summary>hrq-00530 · remaining 详情</summary>

```
### N02 | entry-03926 | confirmed

原译「%d 个负面物理状态被高温驱散」漏掉 *up to*，把“**最多 %d 个**”写成固定移除 `%d` 个。源码将该数值作为 `removeEffectsFilter` 的移除上限。证据：`snapshots/tome-orcs.lua:5007-5012`；冻结源码 `tome-orcs/data/talents/steam/furnace.lua:157-161,170-177`。
```
</details>

## entry-03931

- 位置：`tome-orcs.lua:5089`（orcs）｜section：`tome-orcs/data/talents/steam/gunslinging.lua`｜source_tag：`tformat`
- 原文：`You have learned to fire while moving.
		In one motion, you fire your double steamguns (100%% weapon damage, 1 tile range penalty) and may then move to an adjacent tile (unless pinned to the ground or immobilized).
		This talent can be activated for up to %d consecutive turns before it goes on cooldown, and takes time according to your steamtech speed or movement speed (if you move), whichever is slower.
		When Strafe ends you may instantly reload between %d and %d ammo (based on the number of strafes you performed and your ammo capacity).`
- 现译：`你学会如何在移动中射击。
		在射击（100%% 武器伤害，射程 -1）的同时你能移动到相邻的一格。
		该技能在冷却前能激活连续 %d 个回合，消耗时间取决于蒸汽速度和移动速度较慢者。
		扫射结束后，你立刻获得 %d 到 %d 弹药（取决于扫射期间你消耗的弹药与你的弹药容量）。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00531 | remaining | remaining:rem-12:C07 | confirmed |  |  |  |

<details><summary>hrq-00531 · remaining 详情</summary>

```
### C07 | entry-03931 | confirmed

原译「你能移动到相邻的一格」漏掉“被定身或无法移动时除外”；「取决于扫射期间你消耗的弹药」则把**扫射次数**误作**消耗弹药数**。即使把“在移动中射击”视为一般技能概述，这两处仍会误导具体判定。源码的装填公式使用 `turns` 与弹药容量，移动分支另检查移动限制。原文“双持蒸汽枪”在相邻的使用前提示中已明确，建议在本说明补出，但不单列为确定缺陷。证据：`snapshots/tome-orcs.lua:5086-5095`；冻结源码 `tome-orcs/data/talents/steam/gunslinging.lua:28-40,53-89`。
```
</details>

## entry-03933

- 位置：`tome-orcs.lua:5112`（orcs）｜section：`tome-orcs/data/talents/steam/gunslinging.lua`｜source_tag：`tformat`
- 原文：`Your cunning and dexterity allow you to fire incredible trick shots that can hit multiple targets.
		You precisely aim your trick shot to ricochet amongst foes you can see so that whenever it hits something solid (creature or solid wall), it will bounce towards the next closest foe.
		It may ricochet up to %d times (or until it misses) within range 5 of your first target and will not target the same foe twice.
		Your shot deals %d%% weapon damage on its first strike, but loses %d%% damage and %d(%d%%) accuracy with each bounce.`
- 现译：`你的灵敏让你能射出同时击中多个敌人的子弹。
		你精确地瞄准敌人，子弹命中后将弹射至其他目标上。
		子弹最多弹射 %d 次，只能在第一个目标周围 5 码范围内弹射，不会命中同一个目标两次。
		第一次命中将造成 %d%% 武器伤害，之后每次弹射下降 %d%% 伤害和 %d （%d%%）命中。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00532 | remaining | remaining:rem-12:C08 | confirmed |  |  |  |

<details><summary>hrq-00532 · remaining 详情</summary>

```
### C08 | entry-03933 | confirmed

原译「子弹命中后将弹射至其他目标」未说明击中**实体或坚固墙壁**均可跳弹，也未说明**未命中即中断**。这些不是“最多弹射 %d 次”能够涵盖的条件；源码分别处理撞墙与未命中。原译「灵敏」可宽泛涵盖灵巧、敏捷，但原文明确列出两项属性，建议补全。另须谨慎：源码先按距**首个目标**的距离排序候选者，不能仅凭英文“next closest foe”宣称它每次都重新寻找距当前撞击点最近的敌人。证据：`snapshots/tome-orcs.lua:5111-5118`；冻结源码 `tome-orcs/data/talents/steam/gunslinging.lua:177-183,192-241,246-254`。
```
</details>

## entry-03939

- 位置：`tome-orcs.lua:5186`（orcs）｜section：`tome-orcs/data/talents/steam/heavy-weapons.lua`｜source_tag：`logSeen`
- 原文：`%s resists the stunning shock!`
- 现译：`%s抵抗了震慑打击！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00533 | remaining | remaining:rem-13:C01 | advisory |  |  |  |

<details><summary>hrq-00533 · remaining 详情</summary>

```
### C01 | entry-03939 | advisory

原译“`%s抵抗了震慑打击！`”与紧邻的 *stunning blow* 共用“打击”，未体现此处 *shock* 是扩散冲击。最强等价读法是两句都在报告抵抗震慑，玩家仍能理解结果；故仅建议改为“震慑冲击”。证据：`S:5183–5195`；`D/talents/steam/heavy-weapons.lua:720–738`。
```
</details>

## entry-03940

- 位置：`tome-orcs.lua:5210`（orcs）｜section：`tome-orcs/data/talents/steam/heavy-weapons.lua`｜source_tag：`logSeen`
- 原文：`%s slams into something solid, emitting a pulse of stunning lightning!`
- 现译：`%s击中了某物，放出一股震慑闪电冲击！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00534 | remaining | remaining:rem-13:C02 | confirmed |  |  |  |

<details><summary>hrq-00534 · remaining 详情</summary>

```
### C02 | entry-03940 | confirmed

原译“`%s击中了某物`”容易读成主动击打，且丢失 *solid*。这里 `%s` 是被击退后撞上障碍物的目标。最强等价读法是“击中”也可宽泛表示碰撞，但在该战斗日志中仍不足以交代撞墙情境。建议“`%s撞上了坚固的物体`”。证据：`S:5208–5217`；`D/talents/steam/heavy-weapons.lua:965–990`。
```
</details>

## entry-03946

- 位置：`tome-orcs.lua:5320`（orcs）｜section：`tome-orcs/data/talents/steam/mecharachnid.lua`｜source_tag：`tformat`
- 原文：`Leap into your mecharachnid, assuming direct control of it for %d turns. While piloting it, all damage dealt is increased by %d%%, resistances are increased by %d%%, and all of its talents cooldown twice as fast.`
- 现译：`跳入机械蜘蛛，直接控制它 %d 回合。当控制它的时候，它所造成的所有伤害增加 %d%%，抗性增加 %d%%，所有技能冷却时间减半。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00535 | remaining | remaining:rem-13:C03 | advisory |  |  |  |

<details><summary>hrq-00535 · remaining 详情</summary>

```
### C03 | entry-03946 | advisory

原译“`所有技能冷却时间减半`”可通俗表达冷却更快；源码实际是在驾驶效果期间每回合额外减少一次冷却值，并跳过 `fixed_cooldown` 技能，不是改写基础冷却时间。为避免误读，建议“技能冷却速度加快一倍”。英文自身的 *all* 也比实现宽泛，不把这部分算作中文新增错误。证据：`S:5318–5320`；`D/talents/steam/mecharachnid.lua:690–700`；`D/timed_effects/other.lua:442–452`。
```
</details>

## entry-03950

- 位置：`tome-orcs.lua:5374`（orcs）｜section：`tome-orcs/data/talents/steam/mechstar.lua`｜source_tag：`tformat`
- 原文：`When you fire your metalstar, your also establish a psionic bloodlink with the shrapnel still inside for %d turns.
		Each turn the victims are drained for %0.2f physical damage, half of which heals you (each additional victim healing is reduced by half).
		If the victim move more than twice away from the radius of Metalstar (currently %d) the effect stops.
		This damage does not break daze and increases with your Steampower.`
- 现译：`每次你使用灵晶射击时，你将与灵晶碎片建立血液灵能联系，持续 %d 回合。
		每回合目标将受到 %0.2f 物理伤害，一半伤害值将转化为治疗。
		每增加一名额外目标，其带来的治疗量进一步减半。
		当目标距离超过金属灵晶范围（当前 %d）的两倍时，效果中止。
		该伤害不会打断眩晕效果，受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00536 | remaining | remaining:rem-13:C04 | confirmed |  |  |  |

<details><summary>hrq-00536 · remaining 详情</summary>

```
### C04 | entry-03950 | confirmed

原译“`使用灵晶射击`”未沿用同节技能名“金属灵晶”；“`与灵晶碎片建立……联系`”遗漏碎片仍留在目标体内；“`范围（当前 %d）的两倍`”又把已经乘二的显示值写成还需再乘二。等价读法可把“灵晶射击”理解为动作描述，却无法消除后两处信息损失。建议按“发射金属灵晶”“残留在目标体内的碎片”“两倍半径（当前 %d 格）”改写。证据：`S:5369–5381`；`D/talents/steam/mechstar.lua:22–45,64–81`。另须区分源码行为：状态在距离**达到**阈值时即断开，而英文及中文都写“超过”；这是沿袭英文的机制描述问题，不计中文新增错译。证据：`D/timed_effects/physical.lua:742–750`。
```
</details>

## entry-03951

- 位置：`tome-orcs.lua:5403`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`_t`
- 原文：`Allows you to create tinkers.`
- 现译：`使用该技能来制造药剂、附着物等道具。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00537 | remaining | remaining:rem-13:C05 | advisory |  |  |  |

<details><summary>hrq-00537 · remaining 详情</summary>

```
### C05 | entry-03951 | advisory

原译“`制造药剂、附着物等道具`”以例子解释 *tinkers*，没有必然错误；但它将类别名改成不完整的举例。冻结术语记录为“蒸汽工具”，状态是 `existing`，不强制统一。建议如需明确类别，写“制造蒸汽工具”。证据：`S:5402–5403`；`D/talents/steam/other.lua:125–142`；`T:1521`。
```
</details>

## entry-03953

- 位置：`tome-orcs.lua:5416`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`Fires your ammo at an enemy in range %d for %d%% weapon damage.  If this tinker is made of voratun you will fire an additional shot.
			This shot is a ranged melee attack but will use the ranged procs of your ammo as well.`
- 现译：`向在 %d 码范围内的一个敌人开火造成 %d%% 的武器伤害。如果手炮是由沃瑞钽钢制作的，你能多一次额外的射击。射击是远程攻击将会触发弹药特效。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00538 | remaining | remaining:rem-13:C06 | confirmed |  |  |  |

<details><summary>hrq-00538 · remaining 详情</summary>

```
### C06 | entry-03953 | confirmed

原译“`射击是远程攻击将会触发弹药特效`”遗漏 *melee*，使特殊的远程近战攻击看似普通远程攻击，也抹去了“虽属近战攻击，仍触发弹药远程特效”的转折。建议明确写“远程近战攻击，但也会触发弹药的远程特效”。原译“沃瑞钽钢”也与本次 `preferred` 术语“沃瑞钽”不符，可在同条修正。证据：`S:5414–5417`；`D/talents/steam/other.lua:332–360`；`T:1609`。源码按技能等级决定额外射击，英文却称由沃瑞钽材质决定；中文沿袭英文，此机制不一致**不计中文新增错误**。证据：`D/talents/steam/other.lua:315–320,344–359`。
```
</details>

## entry-03960

- 位置：`tome-orcs.lua:5483`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`Throw a cone of healing with radius %d, healing other mechanical creatures (steam spiders) for %d.
		The healing will increase with your Steampower.`
- 现译：`释放一片锥形半径 %d 码的修理器，修复机械生物（蒸汽蜘蛛）%d 生命值。
　　治疗量受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00539 | remaining | remaining:rem-13:C07 | confirmed |  |  |  |

<details><summary>hrq-00539 · remaining 详情</summary>

```
### C07 | entry-03960 | confirmed

原译“`修复机械生物`”漏掉 *other*。最强等价读法是读者会从施法语境推知治疗别人，但文字仍未排除自身；源码明确要求 `act ~= self`。建议“修复**其他**机械生物”。证据：`S:5482–5485`；`D/talents/steam/other.lua:839–840,853–864,907–912`。
```
</details>

## entry-03967

- 位置：`tome-orcs.lua:5552`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and explodes within radius %d, which does %0.2f physical damage.
		This talent does not use ammo as it is the ammo.`
- 现译：`你使用蒸汽枪在射程内制造一场特殊的爆炸。
　　当每一个弹片击中它的目标，造成正常蒸汽枪伤害和半径 %d 码内的爆炸，造成 %0.2f 的物理伤害，
　　这个技能不使用弹药。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00540 | remaining | remaining:rem-14:C01 | confirmed |  |  |  |
| hrq-00541 | remaining | remaining:rem-14:C02 | confirmed |  |  |  |
| hrq-00542 | remaining | remaining:rem-14:C03 | confirmed |  |  |  |

<details><summary>hrq-00540 · remaining 详情</summary>

```
### C01 | entry-03967 | confirmed

原译“每一个弹片”将 `each shot` 变成爆炸后的碎片；源码实际先取得蒸汽枪射击目标并执行 `archeryShoot`，每次射击命中后才触发爆炸。将“弹片”宽泛理解为弹丸仍不符合此处先射击、后爆炸的顺序。证据：`S:5552–5555`、`O:1327–1343`。
```
</details>

<details><summary>hrq-00541 · remaining 详情</summary>

```
### C02 | entry-03967 | confirmed

“这个技能不使用弹药”保留了结果，遗漏 `as it is the ammo` 所说的“技能本身就是弹药”。结果相同不足以覆盖原句的因果及设定。证据：`S:5552–5555`、`O:1341–1343`。
```
</details>

<details><summary>hrq-00542 · remaining 详情</summary>

```
### C03 | entry-03967 | confirmed

“在射程内制造一场特殊的爆炸”可概括最终效果，但遗漏向射程内一处地点**发射爆炸弹**的动作和落点；源码也明确执行射击。这是叙事动作与目标的具体信息缺失。证据：`S:5552–5555`、`O:1332–1343`。
```
</details>

## entry-03970

- 位置：`tome-orcs.lua:5594`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`You fire a special hook shot with your steamgun(s) at a target creature or location.
		If you target a creature, they are pulled up to %d tiles towards you.
		If you target an empty tile, you are pulled up to %d tiles towards it.
		This talent does not use ammo as it is the ammo.`
- 现译：`你使用蒸汽枪发射特殊弹药打击目标或某处
如果你的目标是一个生物，他们被拉向你 %d 码
如果你的目标是一个空地，你会被拉向空地 %d 码
这个技能不使用弹药。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00543 | remaining | remaining:rem-14:C04 | confirmed |  |  |  |
| hrq-00544 | remaining | remaining:rem-14:C05 | confirmed |  |  |  |
| hrq-00545 | remaining | remaining:rem-14:C06 | advisory |  |  |  |

<details><summary>hrq-00543 · remaining 详情</summary>

```
### C04 | entry-03970 | confirmed

两处“被拉向……%d 码”均漏掉 `up to`，读起来承诺移动足额距离；原文只给最大格数。拉动调用使用该数值作为距离参数，不能据此保证实际总能移动满额。证据：`S:5594–5601`、`O:1583–1599,1603–1606`。
```
</details>

<details><summary>hrq-00544 · remaining 详情</summary>

```
### C05 | entry-03970 | confirmed

原译“这个技能不使用弹药”遗漏“技能本身就是弹药”的因果分句；与 C02 同类。证据：`S:5594–5601`、`O:1603–1606`。
```
</details>

<details><summary>hrq-00545 · remaining 详情</summary>

```
### C06 | entry-03970 | advisory

“特殊弹药打击目标或某处”没有写出 `hook shot` 的钩弹特征；“打击”也可能暗示造成伤害，而所见技能动作是拉动。最强等价读法是“打击”仅表示朝目标发射，后文已解释拉动，因此记为澄清建议。证据：`S:5594–5601`、`O:1581–1606`。
```
</details>

## entry-03971

- 位置：`tome-orcs.lua:5610`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`You fire a special voltaic shot with your steamgun(s) at a target for 100%% weapon damage as lightning.
		The shot will release powerful electrical currents at up to %d nearby enemies. 
		Each bolt does %0.2f lightning damage.
		This talent does not use ammo as it is the ammo.
		Bolt damage scales with Steampower.`
- 现译：`你使用蒸汽枪发射特殊弹药打击目标造成 100%% 闪电武器伤害。
这将释放强大的电流，打击周围 %d 的敌人。
每个闪电球造成 %0.2f 的闪电伤害
这个技能不使用弹药
闪电球伤害受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00546 | remaining | remaining:rem-14:C07 | confirmed |  |  |  |
| hrq-00547 | remaining | remaining:rem-14:C08 | confirmed |  |  |  |
| hrq-00548 | remaining | remaining:rem-14:C09 | confirmed |  |  |  |
| hrq-00549 | remaining | remaining:rem-14:C10 | advisory |  |  |  |

<details><summary>hrq-00546 · remaining 详情</summary>

```
### C07 | entry-03971 | confirmed

“闪电球”把 `bolt` 具体化为球体；本技能对附近敌人的续发效果采用 `beam` 投射及闪电粒子。即使把“球”作宽泛的闪电称呼，也会给出错误的形状印象。证据：`S:5610–5616`、`O:1670–1677,1690–1694`。
```
</details>

<details><summary>hrq-00547 · remaining 详情</summary>

```
### C08 | entry-03971 | confirmed

“打击周围 %d 的敌人”漏掉 `up to`，并缺少人数的量词。源码按技能等级设循环上限，附近敌人用尽会提前退出；译为“附近至多 %d 名敌人”才保留限制。证据：`S:5610–5616`、`O:1670–1675,1691–1695`。
```
</details>

<details><summary>hrq-00548 · remaining 详情</summary>

```
### C09 | entry-03971 | confirmed

“这个技能不使用弹药”遗漏 `as it is the ammo`；同 C02。证据：`S:5610–5616`、`O:1690–1694`。
```
</details>

<details><summary>hrq-00549 · remaining 详情</summary>

```
### C10 | entry-03971 | advisory

“特殊弹药”未呈现 `voltaic`，但紧接着已说明闪电武器伤害及电流效果，玩家仍能识别弹药性质。补出“电气／伏特”可使首句更完整。证据：`S:5610–5616`、`O:1690–1694`。
```
</details>

## entry-03972

- 位置：`tome-orcs.lua:5628`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`You fire a special botanical shot with your steamgun(s) at a target for 100%% weapon damage as nature.
		The shot will release spores which grow into Nourishing Moss in a radius of %d for %d turns.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss has vampiric properties and heals the user for %d%% of the damage done.
		This talent does not use ammo as it is the ammo.
		Moss damage scales with Steampower.`
- 现译：`你使用蒸汽枪发射特殊弹药打击目标造成 100%% 自然武器伤害。
将释放孢子生长成半径 %d 的苔藓 %d 回合。
每回合苔藓造成 %0.2f 自然伤害对半径内的每一个敌人。
这种苔藓有吸血特性，伤害的 %d%% 治愈使用者。
这个技能不使用弹药
苔藓伤害受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00550 | remaining | remaining:rem-14:C11 | confirmed |  |  |  |
| hrq-00551 | remaining | remaining:rem-14:C12 | confirmed |  |  |  |
| hrq-00552 | remaining | remaining:rem-14:C13 | confirmed |  |  |  |

<details><summary>hrq-00550 · remaining 详情</summary>

```
### C11 | entry-03972 | confirmed

“苔藓”遗漏 `Nourishing Moss` 的 `Nourishing`，使具名效果变成泛称；源码使用 `DamageType.NOURISHING_MOSS`。后文的吸血说明不能补回效果名称。证据：`S:5628–5635`、`O:1750–1755,1771–1776`。
```
</details>

<details><summary>hrq-00551 · remaining 详情</summary>

```
### C12 | entry-03972 | confirmed

“这个技能不使用弹药”遗漏“技能本身就是弹药”的因果分句；同 C02。证据：`S:5628–5635`、`O:1771–1776`。
```
</details>

<details><summary>hrq-00552 · remaining 详情</summary>

```
### C13 | entry-03972 | confirmed

“造成 %0.2f 自然伤害对半径内的每一个敌人”是明显不通顺的语序，应写成“对……造成……伤害”。同项所提 `botanical` 被泛化为“特殊弹药”也值得补出，但其植物性质可从孢子、苔藓读出；确认的问题是句法，修饰语遗漏作为建议。证据：`S:5628–5635`、`O:1771–1773`。
```
</details>

## entry-03973

- 位置：`tome-orcs.lua:5649`（orcs）｜section：`tome-orcs/data/talents/steam/other.lua`｜source_tag：`tformat`
- 原文：`You fire a special toxic shot with your steamgun(s) at a target for 100%% weapon damage as blight.
		The shot will release heavy metals into the target, inflicting %0.2f blight damage per turn and reducing their global speed by %d%% for %d turns.
		This talent does not use ammo as it is the ammo.
		Toxin strength scales with Steampower.`
- 现译：`你使用蒸汽枪发射特殊弹药打击目标造成 100%% 枯萎武器伤害。
向目标释放重金属，造成每回合 %0.2f 枯萎伤害，并且降低整体速度 %d%% %d 回合。
这个技能不使用弹药。
枯萎伤害受蒸汽强度加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00553 | remaining | remaining:rem-14:C14 | confirmed |  |  |  |
| hrq-00554 | remaining | remaining:rem-14:C15 | confirmed |  |  |  |
| hrq-00555 | remaining | remaining:rem-14:C16 | confirmed |  |  |  |
| hrq-00556 | remaining | remaining:rem-14:C17 | advisory |  |  |  |

<details><summary>hrq-00553 · remaining 详情</summary>

```
### C14 | entry-03973 | confirmed

“整体速度”与本轮 `global speed → 全局速度` 的 global、`tformat`、preferred 术语记录直接冲突，记录还明确排除“整体速度”。证据：`S:5649–5653`、`T:960–968`、`O:1846–1847`。
```
</details>

<details><summary>hrq-00554 · remaining 详情</summary>

```
### C15 | entry-03973 | confirmed

“枯萎伤害受蒸汽强度加成”将 `Toxin strength` 限缩为伤害。命中时，同一个随蒸汽强度变化的 `getPower` 同时传给毒素的 `power` 和减速的 `speed`；“伤害”不能说明后一效果也成长。证据：`S:5649–5653`、`O:1829–1832,1846–1850`。
```
</details>

<details><summary>hrq-00555 · remaining 详情</summary>

```
### C16 | entry-03973 | confirmed

“这个技能不使用弹药”遗漏 `as it is the ammo`；同 C02。证据：`S:5649–5653`、`O:1846–1849`。
```
</details>

<details><summary>hrq-00556 · remaining 详情</summary>

```
### C17 | entry-03973 | advisory

“特殊弹药”未写 `toxic`，但下一句已交代向目标释放重金属并施加毒素相关效果；性质仍可从上下文辨认。首句补“剧毒”更完整。证据：`S:5649–5653`、`O:1846–1849`。
```
</details>

## entry-03977

- 位置：`tome-orcs.lua:5742`（orcs）｜section：`tome-orcs/data/talents/steam/sawmaiming.lua`｜source_tag：`tformat`
- 原文：`You "gently" slam your saws into the wounds of a creature, dealing %d%% weapon damage and deepening the wounds.
		All bleeding wounds durations are increased by %d turns and the damage by %d%% (this may be done only once per bleeding effect).
		When this happens a gush of blood is projected in a narrow cone of radius 4, dealing %0.2f physical damage to all creatures.
		The power and damage improves with your Steampower.
		#{italic}#The marvels of technology, now at the service of true butchery!#{normal}#`
- 现译：`你 " 轻柔 " 地将链锯放在目标的伤口上，造成 %d%% 武器伤害并加深伤口。
		所有流血伤口持续时间增加 %d 回合，伤害增加 %d%% （每项流血最多触发一次）。
		效果触发时，血流将喷射而出，对 4 码锥形范围内所有生物造成 %0.2f 物理伤害。
		伤害受蒸汽强度加成。
		#{italic}#一切技术，皆为屠杀 !#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00557 | remaining | remaining:rem-14:C18 | advisory |  |  |  |
| hrq-00558 | remaining | remaining:rem-14:C19.1 | advisory |  |  |  |
| hrq-00559 | remaining | remaining:rem-14:C19.2 | confirmed |  |  |  |

<details><summary>hrq-00557 · remaining 详情</summary>

```
### C18 | entry-03977 | advisory

原译“伤害受蒸汽强度加成”可能概括流血伤害增幅与喷血伤害，不能直接断言玩家只会理解为后者；写明两项更清楚。初审报告称 `getDamageInc` 是实际流血增幅函数，但冻结源码的效果执行处调用的是 `getDamage`，`getDamageInc` 只出现在说明的格式化参数中。因此其“两项独立函数分别驱动两种实际效果”的论证**不成立**；源码与英文说明之间的这一差异应另行记录，不能算中文新增错误。证据：`S:5742–5750`、`M:64–66,79–86,92–98`。
```
</details>

<details><summary>hrq-00558 · remaining 详情</summary>

```
### C19 | entry-03977 | advisory（C19.1）／confirmed（C19.2）

原译“将链锯放在目标的伤口上”弱化 `slam ... into` 的猛烈动作；结合引号中的“轻柔”，建议改写以保留反讽，但主要动作仍可理解，故 **C19.1 advisory**。原译“4 码锥形范围”则遗漏 `narrow`；源码将锥角设为 25，狭窄是实际范围特征，故 **C19.2 confirmed**。证据：`S:5742–5749`、`M:85–86,93–96`。
```
</details>

<details><summary>hrq-00559 · remaining 详情</summary>

```
### C19 | entry-03977 | advisory（C19.1）／confirmed（C19.2）

原译“将链锯放在目标的伤口上”弱化 `slam ... into` 的猛烈动作；结合引号中的“轻柔”，建议改写以保留反讽，但主要动作仍可理解，故 **C19.1 advisory**。原译“4 码锥形范围”则遗漏 `narrow`；源码将锥角设为 25，狭窄是实际范围特征，故 **C19.2 confirmed**。证据：`S:5742–5749`、`M:85–86,93–96`。
```
</details>

## entry-03984

- 位置：`tome-orcs.lua:5853`（orcs）｜section：`tome-orcs/data/talents/steam/thoughts-of-iron.lua`｜source_tag：`tformat`
- 原文：`Melding psionics with steamtech you create 5 mind drones at your sides that fly towards your target.
		If they encounter a creature they will latch on it and bore into its skull for 6 turns, disrupting its thoughts.
		Disrupted creatures have %d%% chances to fail to use talents and suffer a -%d%% reduction to fear and sleep immunity.`
- 现译：`将灵能和蒸汽科技结合，你在身边制造 5 只精神雄蜂飞向目标。
		雄蜂接触到生物时，将进入其大脑 6 回合，干扰思考能力。
		受影响的生物有 %d%% 几率使用技能失败，同时恐惧和睡眠免疫减少 %d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00560 | remaining | remaining:rem-14:C20 | advisory |  |  |  |

<details><summary>hrq-00560 · remaining 详情</summary>

```
### C20 | entry-03984 | advisory

“进入其大脑”传达侵入与干扰结果，却省去 `latch on it` 的附着动作及 `bore into its skull` 的钻入头骨画面。补足可改善叙事；核心效果仍可理解。英文 `-%d%% reduction` 的双重负号不可机械照译：效果代码确实降低恐惧、睡眠免疫，现译这一点正确。证据：`S:5853–5857`、`I:103–107`、`E:77–90`。
```
</details>

## entry-03985

- 位置：`tome-orcs.lua:5890`（orcs）｜section：`tome-orcs/data/talents/steam/turrets.lua`｜source_tag：`logPlayer`
- 原文：`Not enough space to summon!`
- 现译：`没有足够的空间召唤！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00561 | remaining | remaining:rem-14:C21 | refuted |  |  |  |

<details><summary>hrq-00561 · remaining 详情</summary>

```
### C21 | entry-03985 | refuted

原译感叹号与英文相符；静态标点差异按本轮规则不算缺陷。初审所引 preferred 记录的 `source_tag` 为 `logSeen`，本条冻结输入为 `logPlayer`，也不能把该记录当作本条必须逐字匹配的依据。证据：`S:5890`、`T:993–1001`、`R:6`。
```
</details>

## entry-03990

- 位置：`tome-orcs.lua:5951`（orcs）｜section：`tome-orcs/data/talents/uber/cun.lua`｜source_tag：`tformat`
- 原文：`You are adept at wreaking havoc onto your foes!
		Any time you deal damage to a creature you apply the Incoming Disasters effect for 20 turns.
		Each time you (or any others) would try to apply a cross-tier effect to this creature, you also try to apply the other two.
		In addition your physical, steam, spell and mind powers are increased by %d.
		The powers increase scales of your Cunning.`
- 现译：`你很擅长给你的敌人带来灾难！
		任何时候你对一个生物造成伤害，你会对它施加灾难临近效果，持续20回合。
		每次你（或任何其他目标）尝试对这个生物施加越层效果时，也将尝试施加其他两个越层效果。
		此外，你的物理，蒸汽，法术和精神强度增加 %d。
		强度增加值受灵巧值加成。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00562 | remaining | remaining:rem-15:C01 | advisory |  |  |  |

<details><summary>hrq-00562 · remaining 详情</summary>

```
### C01 | entry-03990 | advisory

原译“你（或任何其他目标）”中，“目标”容易指向承受效果的生物；原文 `any others` 指其他施加方。**等价读法**是该词位于“尝试施加”的主语位置，读者仍可理解为行动方，因此保留为澄清建议。冻结源码在受效果生物身上联动判定，未限定某个施加者：[Combat.lua:29](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Combat.lua:29>)；译文见 [快照:5951](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:5951)。建议用“其他人”或“其他来源”。
```
</details>

## entry-03996

- 位置：`tome-orcs.lua:6002`（orcs）｜section：`tome-orcs/data/talents/uber/mag.lua`｜source_tag：`_t`
- 原文：`Any spell damage you deal to it will ripple around in radius 4 as 160% arcane damage.`
- 现译：`其受到的法术伤害转化为波纹，对半径 4 内的所有目标造成等同于该伤害 160% 的奥术伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00563 | remaining | remaining:rem-15:C02 | confirmed |  |  |  |

<details><summary>hrq-00563 · remaining 详情</summary>

```
### C02 | entry-03996 | confirmed

原译“其受到的法术伤害”遗漏 `you deal to it`，将触发来源扩大。**等价反证**不成立：冻结源码明确要求伤害来源为装置召唤者，且来自法术：[mag.lua:25](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:25>)；原文和译文见 [快照:6002](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6002)。建议补“你对其造成的”。

同一源码的运行计算为 **130%**，而此条英文 NPC 描述及其中文均写 **160%**（[mag.lua:34](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:34>)、[mag.lua:82](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:82>)）。这是英文描述与冻结行为的差异，**不计为中文新增错译**。
```
</details>

## entry-03997

- 位置：`tome-orcs.lua:6019`（orcs）｜section：`tome-orcs/data/talents/uber/mag.lua`｜source_tag：`tformat`
- 原文：`Technomancers are Archmages that dabble in steam technology to enhance their already formidable arsenal of spells.
		Once this class evolution is taken, you gain the following:
		- Arcane Dynamo tinker schematic
		- Steamtech/Physics category (unlocked)
		- Steamtech/Chemistry category (locked)
		- An Automated Portable Extractor (A.P.E.)
		- One point in the Physics talent Smith and two in Mechanical and Electricity
		- Spell/Galvanic Technomancy category (locked) - deals with fire and lightning
		- Spell/Terrene Technomancy category (locked) - deals with earth and water
		- Spell/Occult Technomancy category (locked) - deals with time and arcane
		- The ability to unlock one of the three Technomancy categories for free

		Once put in a robe, the Arcane Dynamo will regenerate Steam each time mana is spent and increase Spellpower based on current steam level.

		#{bold}#As soon as this evolution is used you will need to craft the Arcane Dynamo to place in a robe to benefit from all the powers of the Technomancer.#{normal}#`
- 现译：`科技法师是一些特殊的元素法师，他精通于蒸汽科技，用科技的力量来强化他们已经足够强大的法术力量。
		当你选择这一项进阶职业的时候，你获得以下能力：
		- 奥术发电机插件配方
		- 蒸汽/物理系 （已解锁）
		- 蒸汽/化学系 （未解锁）
		- 一个便携式自动材料提取仪。
		- 1级铁匠技能，2级机械和电子技能。
		- 法术/科技法术：放电系 （未解锁）- 使用火焰和闪电
		- 法术/科技法术：寒岩系 （未解锁）- 使用土和水
		- 法术/科技法术：玄机系 （未解锁）- 使用时间和奥术
		- 你可以免费解锁三个科技法术系的其中之一。

		当你装备长袍的时候，奥术发电机会在你消耗法力值的时候自动产生蒸汽，并根据蒸汽等级提升法术强度。
		#{bold}#当你完成这职业进阶的时候，你应该尽快制造一个奥术发电机，装备在长袍中，以使用科技法术的力量。#{normal}#`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00564 | remaining | remaining:rem-15:C03 | confirmed |  |  |  |
| hrq-00565 | remaining | remaining:rem-15:N01 | confirmed |  |  |  |

<details><summary>hrq-00564 · remaining 详情</summary>

```
### C03 | entry-03997 | confirmed

**C03.1** 原译“当你装备长袍的时候”把“将奥术发电机装入长袍”改成玩家穿上长袍。末段“装备在长袍中”提供部分线索，但不能消除本句的动作和前提偏差。装置限定衣物槽位：[electricity.lua:101](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/electricity.lua:101>)；原译见 [快照:6031](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6031)。

**C03.2** 原译“蒸汽等级”将当前蒸汽量写成等级。**等价反证**不成立：法强公式直接读取 `getSteam()`，不是技能等级：[other.lua:1912](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:1912>)。建议分别改为“装入长袍后”“当前蒸汽量”。
```
</details>

<details><summary>hrq-00565 · remaining 详情</summary>

```
### N01 | entry-03997 | confirmed

首句原译“精通于蒸汽科技”把原文 `dabble in steam technology` 的涉猎、尝试程度提升为精通，是独立的叙事意义偏差。**等价反证**是职业最终可能熟练运用科技，但不能覆盖此句明确的程度用词。原文见 [mag.lua:193](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/mag.lua:193>)，译文见 [快照:6033](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6033)。建议用“涉猎蒸汽科技”。
```
</details>

## entry-04000

- 位置：`tome-orcs.lua:6060`（orcs）｜section：`tome-orcs/data/talents/uber/wil.lua`｜source_tag：`tformat`
- 原文：`Activate a special focusing device that extends all your ranged spells and psionic powers range by 3 (only works on those with range 2 or more and up to 10 max).
		The use of this device is very strenuous, increasing fatigue by 20%% while active.`
- 现译：`启动一个特殊的聚焦装置来使你的所有远程魔法和精神技能射程延长 3 （仅对射程至少为 2 的技能生效，且上限为 10）。
		使用这个装置非常的费力，启动时会增加 20%% 疲劳。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00566 | remaining | remaining:rem-15:C04 | advisory |  |  |  |

<details><summary>hrq-00566 · remaining 详情</summary>

```
### C04 | entry-04000 | advisory

原译“启动时会增加 20%% 疲劳”可能被读成仅在启动瞬间发生；原文 `while active` 指开启期间。**等价读法**是“启动时”也可指从启动起持续生效，故列澄清建议。源码将疲劳作为持续技能的临时属性：[wil.lua:20](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/uber/wil.lua:20>)；译文见 [快照:6060](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6060)。建议写“开启期间”。
```
</details>

## entry-04001

- 位置：`tome-orcs.lua:6074`（orcs）｜section：`tome-orcs/data/timed_effects/floor.lua`｜source_tag：`_t`
- 原文：`The target is warm from the campfire. Increasing steam regeneration by 6/turn, stun immunity by 30% and stamina regeneration by 4/turn.`
- 现译：`目标被营火温暖。蒸汽回复 +6，震慑免疫 +30%，体力回复 + 4。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00567 | remaining | remaining:rem-15:C05 | advisory |  |  |  |

<details><summary>hrq-00567 · remaining 详情</summary>

```
### C05 | entry-04001 | advisory

原译“蒸汽回复 +6”“体力回复 + 4”省去原文两处 `/turn`。**等价读法**是“回复”属性本身按回合结算，数值与效果未变；补“每回合”可让单位更清楚。“+ 4”的空格仅属格式。源码属性见 [floor.lua:42](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/floor.lua:42>)；原译见 [快照:6074](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6074)。
```
</details>

## entry-04008

- 位置：`tome-orcs.lua:6167`（orcs）｜section：`tome-orcs/data/timed_effects/mental.lua`｜source_tag：`_t`
- 原文：`A mind drone bores into #Target#!`
- 现译：`一个精神雄蜂飞入#Target#！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00568 | remaining | remaining:rem-15:C06 | confirmed |  |  |  |

<details><summary>hrq-00568 · remaining 详情</summary>

```
### C06 | entry-04008 | confirmed

原译“精神雄蜂飞入”只表达移动，遗漏 `bores into` 的钻入动作。**等价反证**不成立：相关技能说明将“飞向目标”与“附着并钻入头骨”写为先后两个动作：[thoughts-of-iron.lua:103](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/thoughts-of-iron.lua:103>)；状态获得日志见 [mental.lua:85](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/mental.lua:85>)。建议用“钻入”。
```
</details>

## entry-04014

- 位置：`tome-orcs.lua:6269`（orcs）｜section：`tome-orcs/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`The target has been injected with chemicals, reducing all saves by %d.`
- 现译：`目标被化学药剂注射，降低所有豁免 %d。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00569 | remaining | remaining:rem-16:C01 | advisory |  |  |  |

<details><summary>hrq-00569 · remaining 详情</summary>

```
### C01 | entry-04014 | advisory

原译“目标被化学药剂注射”略生硬，且“药剂”似乎成了施动者。最强等价读法是将其理解为“目标被注射了化学药剂”；三类豁免降低的含义没有偏差。建议仅作语序润色。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6269)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua:518)。
```
</details>

## entry-04015

- 位置：`tome-orcs.lua:6272`（orcs）｜section：`tome-orcs/data/timed_effects/other.lua`｜source_tag：`tformat`
- 原文：`Engaged in automated repairs, preventing any action but increasing life regen by %d, all resistances by %d%% and preventing death until falling below -%d life.`
- 现译：`进入自动修复模式，无法行动，但生命恢复速率增加 %d，生命值回满时立即结束该模式，全部抗性提升 %d%%，死亡生命下限为 -%d。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00570 | remaining | remaining:rem-16:C02 | confirmed |  |  |  |

<details><summary>hrq-00570 · remaining 详情</summary>

```
### C02 | entry-04015 | confirmed

原译增加“生命值回满时立即结束该模式”。**回满后解除**有源码依据；等价反证是 `on_timeout` 确实在 `self.life == self.max_life` 时移除效果。但检查发生在角色的定时效果处理阶段，并非生命值变化当刻；“立即”给出了源码未保证的时序。建议改为“生命值回满后结束该模式”。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6272)、[DLC 效果](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua:538)、固定 engine `game/engines/default/engine/interface/ActorTemporaryEffects.lua:76–110`。三个占位符顺序无误。
```
</details>

## entry-04018

- 位置：`tome-orcs.lua:6318`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Bullets shot are percussive:  When striking, they have a %d%% chance to knock back and a %d%% chance to stun.`
- 现译：`子弹处于冲击状态：%d%% 概率击退，%d%% 概率震慑。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00571 | remaining | remaining:rem-16:C03 | advisory |  |  |  |

<details><summary>hrq-00571 · remaining 详情</summary>

```
### C03 | entry-04018 | advisory

原译“%d%% 概率击退，%d%% 概率震慑”省略了 *When striking*。最强等价读法是：句首已限定为射出的子弹，玩家可自然理解为击中时判定；源码也仅在命中挂钩中执行。补上“命中时”可更明确，现译不构成实质错译。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6318)、[效果文案](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:95)、[命中处理](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Archery.lua:60)。
```
</details>

## entry-04019

- 位置：`tome-orcs.lua:6320`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Bullets shot are combustive:  When striking their target, they explode (radius 2) for %d fire damage.`
- 现译：`子弹处于爆炸状态：对 2 码范围内的敌人造成 %d 火焰伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00572 | remaining | remaining:rem-16:C04 | confirmed |  |  |  |

<details><summary>hrq-00572 · remaining 详情</summary>

```
### C04 | entry-04019 | confirmed

原译“对 2 码范围内的敌人造成 %d 火焰伤害”保留了范围和伤害，却未说明**子弹命中目标后**才爆炸、范围以**命中目标**为中心。最强等价读法是玩家从“子弹处于爆炸状态”推知会在命中时爆炸，但现句仍未交代爆炸位置。建议写明“命中目标时爆炸（半径 2）”。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6320)、[效果文案](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:105)、[命中与目标坐标](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Archery.lua:60)。
```
</details>

## entry-04022

- 位置：`tome-orcs.lua:6348`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Provides a frost aura, giving you +%d%% fire, light, and lightning affinity.`
- 现译：`提供烈火光环，使你获得 +%d%% 火焰、光系和闪电伤害亲和。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00573 | remaining | remaining:rem-16:C05 | advisory |  |  |  |

<details><summary>hrq-00573 · remaining 详情</summary>

```
### C05 | entry-04022 | advisory

原译“烈火光环”与该句英文 *frost aura* 字面不同。等价反证更强：同一效果名为 `FIERY_SALVE`，赋予火焰、光系、闪电亲和；相邻道具说明也写 *fiery aura*。这是有证据支持的上游文案修正，不判中文错译。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6346)、[关联道具说明](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6780)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:181)。
```
</details>

## entry-04023

- 位置：`tome-orcs.lua:6354`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Provides a frost aura, giving you +%d%% blight, mind and acid affinity.`
- 现译：`提供静水光环，使你获得 +%d%% 枯萎、精神和酸性伤害亲和。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00574 | remaining | remaining:rem-16:C06 | advisory |  |  |  |

<details><summary>hrq-00574 · remaining 详情</summary>

```
### C06 | entry-04023 | advisory

原译“静水光环”与该句英文 *frost aura* 字面不同。等价反证是效果名 `WATER_SALVE`、水子类型、枯萎／精神／酸性亲和，以及相邻道具说明的 *water aura*；可判为上游文案沿用错误的合理修正。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6352)、[关联道具说明](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6784)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:205)。
```
</details>

## entry-04028

- 位置：`tome-orcs.lua:6404`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`The saw embedded in #Target# flies back its source.`
- 现译：`#Target#身上的链锯飞回主人的方向。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00575 | remaining | remaining:rem-16:C07 | advisory |  |  |  |

<details><summary>hrq-00575 · remaining 详情</summary>

```
### C07 | entry-04028 | advisory

原译“飞回主人的方向”将 *its source* 具体化为“主人”。最强等价读法是玩家能据战斗语境将“主人”理解为飞锯施加者；源码中的目标确为 `eff.src`，故方向未译反。“施加者处”更准确，也避免将施加者与所有者混同。[快照](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6404)、[冻结源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:445)。

**完整疑点映射：** C01→entry-04014 advisory；C02→entry-04015 confirmed；C03→entry-04018 advisory；C04→entry-04019 confirmed；C05→entry-04022 advisory；C06→entry-04023 advisory；C07→entry-04028 advisory。新增疑点：无。

**读取与版本限制：** 读取了指定入口、其引用的 `RULES.md`、`rem-16.md`、`gemini-rem-16.md`、`source-access.json`、`terms.json`，以及本批相关的 `snapshots/tome-orcs.lua`；核对了登记的 orcs `other.lua`、`physical.lua`、`bullets-mastery.lua`、`Archery.lua`，四者 SHA256 均与 `source-access.json` 一致。C02 另核对固定 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `ActorTemporaryEffects.lua`。orcs DLC 仅固定这些文件的快照哈希，**未固定 DLC 仓库 commit 或目标 1.7.4 版本**；上述机制结论适用于所读冻结源码，不能据此声称已核验正式 1.7.4 发行行为。
```
</details>

## entry-04035

- 位置：`tome-orcs.lua:6445`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`#Target# somehow catches the falling steamguns.`
- 现译：`#Target# 接住了蒸汽枪。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00576 | remaining | remaining:rem-17:C01 | confirmed |  |  |  |

<details><summary>hrq-00576 · remaining 详情</summary>

```
### C01 | entry-04035 | confirmed

原译“`#Target# 接住了蒸汽枪。`”保留了接住武器这一主干，但省去 *somehow* 的意外感和 *falling* 的下落动作。前一句明确写将蒸汽枪抛向空中；战斗日志虽可简写，仍不足以传达原句的戏谑场面。建议“`#Target# 不知怎么接住了落下的蒸汽枪。`”。证据：[译文快照第 6444–6445 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6444)、[源码第 602–603 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:602)。
```
</details>

## entry-04046

- 位置：`tome-orcs.lua:6500`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`#Target# is suffering and fails to concentrate on dealing damage.`
- 现译：`#Target# 忍受痛苦，不能集中精力制造伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00577 | remaining | remaining:rem-17:C02 | advisory |  |  |  |

<details><summary>hrq-00577 · remaining 详情</summary>

```
### C02 | entry-04046 | advisory

原译“`忍受痛苦，不能集中精力制造伤害`”能表达受苦导致伤害下降。“忍受”略带主动耐受意味，“制造伤害”也较生硬；“遭受痛苦，无法集中精力造成伤害”更自然。相邻解除句“痛苦减轻了”支持这一语感建议，但不足以判定原译错义。证据：[快照第 6499–6501 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6499)、[源码第 875–886 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:875)。
```
</details>

## entry-04047

- 位置：`tome-orcs.lua:6515`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`The target is surrounded by a crackling web of lightning, reducing all damage taken by %d.`
- 现译：`目标被闪电之网覆盖，减少所受到的所有伤害 %d。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00578 | remaining | remaining:rem-17:C03 | advisory |  |  |  |

<details><summary>hrq-00578 · remaining 详情</summary>

```
### C03 | entry-04047 | advisory

原译“`被闪电之网覆盖`”没有写出 *crackling* 的声响；“覆盖”也比 *surrounded by* 更偏表面附着。不过闪电之网及全伤害固定减免均已传达，“覆盖”可作护盾意象理解。可润色为“被噼啪作响的闪电之网环绕”。证据：[快照第 6514–6515 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6514)、[源码第 956–977 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:956)。
```
</details>

## entry-04049

- 位置：`tome-orcs.lua:6525`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`_t`
- 原文：`#target# surges with power!`
- 现译：`#target#力量强化！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00579 | remaining | remaining:rem-17:C04 | advisory |  |  |  |

<details><summary>hrq-00579 · remaining 详情</summary>

```
### C04 | entry-04049 | advisory

原译“`#target#力量强化！`”概括了力量增强，却弱化 *surges with power* 的涌动感。它与解除句“力量消退了”相配，状态提示仍成立；“力量涌动！”是可选润色。证据：[快照第 6525–6527 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6525)、[源码第 1033–1042 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1033)。
```
</details>

## entry-04053

- 位置：`tome-orcs.lua:6557`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`logCombat`
- 原文：`#Source# #LIGHT_RED#strikes down at#LAST# #Target#!`
- 现译：`#Source# #LIGHT_RED#打击#LAST# #Target#！`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00580 | remaining | remaining:rem-17:C05 | advisory |  |  |  |

<details><summary>hrq-00580 · remaining 详情</summary>

```
### C05 | entry-04053 | advisory

原译“`打击`”省去了 *strikes down at* 的动作力度，但保留了攻击者、目标和颜色标记。源码证明这是钳制期间的尾部武器自动攻击；它未证明攻击必然具有固定的空间方向，因此 Flash 建议的“向下猛击”不宜作为机制事实强制采用。“猛击”可作润色。证据：[快照第 6552–6557 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6552)、[源码第 1312–1323 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1312)。
```
</details>

## entry-04054

- 位置：`tome-orcs.lua:6568`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`The target is surrounded by a toxic cloud or radius %d. Enemies within will suffer %d%% talent failure, %d%% reduced healing, and take %0.2f additional acid damage from melee and ranged attacks.`
- 现译：`目标被半径为 %d 的瘴气毒云包围。被困在其中的敌人会有 %d%% 的技能失败几率，降低%d%% 治疗效果，并且在受到近战和远程攻击的时候受到 %0.2f 额外酸性伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00581 | remaining | remaining:rem-17:N01 | advisory |  |  |  |

<details><summary>hrq-00581 · remaining 详情</summary>

```
### N01 | entry-04054 | advisory

原译“`被困在其中的敌人`”比英文 *Enemies within* 多出受困意味。源码显示毒云向范围内目标施加瘴气效果，所核对的效果定义没有定身条件；但“被困在毒云中”也可能只是叙事说法，尚不足以确认玩家会理解为无法离开。建议改为“处于其中的敌人”。证据：[快照第 6568 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6568)、[源码第 1405–1409、1438–1444 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1405)。

**来源与版本限制：**实际读取了指定入口、同目录 `RULES.md`、`batches/rem-17.md`、Flash 的 `reports/gemini-rem-17.md`、`source-access.json`、`terms.json`、本批同 section 的 `snapshots/tome-orcs.lua` 上下文，以及登记的 `physical.lua`、`artillery.lua` 冻结源码。两份源码的本地 SHA256 均与[来源登记](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json:376)相符；`orcs` DLC 的仓库 commit 和目标 1.7.4 版本**未固定**。机制结论只适用于这些哈希固定的公开源码快照，不宣称已核验 1.7.4 发行态。未读取其他报告或任务状态。
```
</details>

## entry-04055

- 位置：`tome-orcs.lua:6572`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Affected by toxic chemicals. Has %d%% talent failure, %d%% reduced healing, and takes %0.2f additional acid damage from melee and ranged attacks.`
- 现译：`被有毒化学物质影响。%d%% 技能失败率，降低 %d%% 治疗效果，每回合第一次被带有武器类型的近战或远程攻击命中时，受到额外 %0.2f 酸性伤害。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00582 | remaining | remaining:rem-17:C06 | advisory |  |  |  |

<details><summary>hrq-00582 · remaining 详情</summary>

```
### C06 | entry-04055 | advisory

原译增写“`每回合第一次被带有武器类型的近战或远程攻击命中时`”。源码在 `callbackOnHit` 中检查攻击来源的 `weapon_type`，并以目标的 `turn_procs.miasma` 阻止再次触发，支持武器条件和单回合一次的说明。它比英文及相邻光环说明详细，但没有据此确认中文新增机制错误。Flash 所称“100% 吻合”过于绝对：本次核验能直接确认上述回调条件，未把所有攻击类型的消费路径逐一穷尽。证据：[快照第 6568、6572 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6568)、[源码第 1465–1499 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1465)。
```
</details>

## entry-04056

- 位置：`tome-orcs.lua:6574`（orcs）｜section：`tome-orcs/data/timed_effects/physical.lua`｜source_tag：`tformat`
- 原文：`Hovering in place, gaining %d%% evasion, %d%% movement speed and launching a powerful rocket barrage each turn.`
- 现译：`目标悬浮在空中，获得 %d%% 躲闪概率，%d%% 移动速度；可手动使用火箭弹幕再次发射，使用其他任何技能会立即结束该效果。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00583 | remaining | remaining:rem-17:C07 | advisory |  |  |  |

<details><summary>hrq-00583 · remaining 详情</summary>

```
### C07 | entry-04056 | advisory

原译“`可手动使用火箭弹幕再次发射，使用其他任何技能会立即结束该效果`”与英文“每回合发射”明显不同。冻结源码显示效果赋予 `Rocket Barrage` 技能，使用其他技能后移除效果；技能说明也写明可主动再次发射。故中文是有源码依据的机制澄清，本项只备案英文表述差异，不计中文错译。证据：[快照第 6573–6574 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6573)、[效果源码第 1502–1535 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1502)、[技能源码第 175–182、187–218 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/artillery.lua:175)。
```
</details>

## entry-04066

- 位置：`tome-orcs.lua:6777`（orcs）｜section：`tome-orcs/data/tinkers/therapeutics.lua`｜source_tag：`_t`
- 原文：`A powerful salve that can clean physical detrimental effects from your body and grant a frost aura (cold, darkness and nature affinity).
To be used with the medical injector implant.`
- 现译：`一个可以清除你身上的负面物理效果并获得一个寒霜光环（增加寒冷、暗影和自然伤害亲和）的强大药剂。
需通过医疗注射器植入体使用。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00584 | remaining | remaining:rem-18:C01 | advisory |  |  |  |

<details><summary>hrq-00584 · remaining 详情</summary>

```
### C01 | entry-04066 | advisory

原译“**可以清除你身上的负面物理效果并获得一个寒霜光环**”让“获得”在字面上承接“药剂”作主语；英文则是药剂 *grant a frost aura*。但结合“你身上”和“需通过医疗注射器植入体使用”，读者仍可将其理解为使用者获得光环，未形成可确认的机制错译。保留为表达澄清建议；可改作“并使你获得寒霜光环”。依据：[冻结译文第 6777–6779 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:6777)、[DLC 冻结源码第 53–56 行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/therapeutics.lua:53)。Flash 报告所列源码“51–53 行”不准确；描述实际位于第 55–56 行。

| 原疑点 | 条目 | 核验状态 | 处理 |
|---|---|---|---|
| C01 | entry-04066 | advisory／仅建议 | 保留措辞建议；无新增疑点 |
```
</details>

## entry-04088

- 位置：`tome-orcs.lua:7456`（orcs）｜section：`tome-orcs/data/zones/slumbering-caves/objects.lua`｜source_tag：`saySimple`
- 原文：`#GOLD#The light of the Amulet envelops you, then subsides. You feel stronger. (+1 Prodigy Points)`
- 现译：`#GOLD#神的光辉充盈着你的全身，然后渐渐消退。你感觉更加强大了。（+1觉醒点）`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00585 | remaining | remaining:rem-19:C01 | advisory |  |  |  |

<details><summary>hrq-00585 · remaining 详情</summary>

```
### C01 | entry-04088 | advisory

原译短引：“**神的光辉**充盈着你的全身”。英文明确写 *the light of the Amulet*；物品源码也将其定义为护符，并在佩戴时输出该句。[护符源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/slumbering-caves/objects.lua:35) 第 35–39、52–58 行。最强等价读法是物品名含 *the Light of God*，“神的光辉”可借指这件护符的光；因此不能据此断言译文写成了神亲自降临。建议明确为“护符的光芒”，保留叙事主体。
```
</details>

## entry-04092

- 位置：`tome-orcs.lua:7901`（orcs）｜section：`tome-orcs/overload/data/texts/unlock-mage_technomancer.lua`｜source_tag：`_t`
- 原文：`#{bold}##GOLD#EUREKA!#LAST##{normal}#

As an archmage you are trained into the intricacies of the arcane forces, but as a tinker you know how to build and create. And suddently it hit you!
#{italic}#You now understand how to combine magic and technology!#{normal}#

You have unlocked the #LIGHT_GREEN#Technomancer class evolution#WHITE# for Archmages.

Features:#YELLOW#
- Occult Technomancy: Use a rapidly spinning steamsaw to rip appart reality itself and project arcane and temporal onslaughts
- Galvanic Technomancy: Create galvanic rods that link up to create deadly fields of fire and lightning to burn down your foes
- Terrene Technomancy: Craft and control swarms of micro spiderbots to damage and debilitate your foes with water and earth forces
- Arcane Dynamo: Casting spells generates steam and steam increases spellpower
- Access to physics and chemistry: All Technomancers know the basics of crafting tinkers
#WHITE#

Class evolutions are selected as prodigies and grant new ways to build and expand your class and are only visible to the concerned class.
`
- 现译：`#{bold}##GOLD#我发现了！#LAST##{normal}#

作为一个元素法师，你在多年的训练中掌握了周围奥术力量的深奥知识，而作为一个工匠，你也掌握了建造和创造的能力。然后有一天，你突然发现了！
#{italic}#你掌握了把魔法和科技结合起来的技术！#{normal}#

你解锁了元素法师的#LIGHT_GREEN#科技法师 职业进阶#WHITE#。

职业特性：#YELLOW#
- 科技法术：玄机系——使用高速旋转的蒸汽链锯切裂现实，用奥术和时间的力量撕碎敌人。
- 科技法术：放电系——使用放电柱，链接出死亡的领域，用火焰和闪电的力量烧毁敌人。
- 科技法术：寒岩系——创造和控制蜘蛛机器人虫群，用水和土的力量毁灭敌人。
- 奥术发电机：施放法术会制造蒸汽，蒸汽会提升法术强度。
- 获得物理学和化学技术：所有科技法师都掌握创造插件的技术。
#WHITE#

职业进阶是一种觉醒技，它们可以给予你新的方法来强化你的职业。只有相关的职业才能看到它们。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00586 | remaining | remaining:rem-19:C02 | confirmed |  |  |  |

<details><summary>hrq-00586 · remaining 详情</summary>

```
### C02 | entry-04092 | confirmed

原译短引：“用水和土的力量**毁灭敌人**”。英文并列写 *damage and debilitate your foes*；“毁灭”只笼统表达伤害，未传达削弱敌人的特性。[解锁文本源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-mage_technomancer.lua:31) 第 31 行。最强等价读法是宣传性概括，但该列表逐项介绍职业特性，省去并列作用构成信息缺失。可改为“用水和土的力量伤害并削弱敌人”。
```
</details>

## entry-04101

- 位置：`tome-orcs.lua:8071`（orcs）｜section：`tome-orcs/overload/data/texts/unlock-tinker_psyshot.lua`｜source_tag：`_t`
- 原文：`You have found extremely old machines powered by advanced psionics and technology. Psionics without a living mind was never thought possible.
You can now create new characters with the #LIGHT_GREEN#Psyshot class#WHITE#.

Psyshots are Tinkers that merge psionics and steamtech in a lethal blend, wielding a steamgun in one hand and a mindstar in the other.
Class features:#YELLOW#
- Project mindstar attacks with each bullet you fire
- Inspire dread to weaken your foes to your gunslinging
- Manipulate the very air around your victims
- Enter a psionic gestalt with your steam generators, boosting them#WHITE#

All Tinker classes use Steam for their powers.
`
- 现译：`你找到了一些由先进灵能与科技驱动的极其古老的机器。没有生命心智的灵能从未被认为可能存在。
现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#灵能射手#WHITE#。

灵能射手是融合灵能与蒸汽科技、形成致命组合的工匠职业，一手持蒸汽枪一手持灵晶。
职业特色：#YELLOW#
- 将灵晶的攻击投射到你发射的子弹中。
- 激发敌人的恐惧，让敌人在你的枪法前无处遁形。
- 操纵你的受害者身边的空气。
- 与你的蒸汽发生器进入灵能格式塔，从而强化它们。#WHITE#

所有工匠系职业使用蒸汽作为能量。
`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00587 | remaining | remaining:rem-19:C03 | confirmed |  |  |  |

<details><summary>hrq-00587 · remaining 详情</summary>

```
### C03 | entry-04101 | confirmed

原译短引：“让敌人在你的枪法前**无处遁形**”。英文是 *weaken your foes to your gunslinging*，重点为削弱敌人；“无处遁形”转向无法躲藏，不能等价表达。[解锁文本源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-tinker_psyshot.lua:27) 第 27 行；[惊骇天赋源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/dread.lua:49) 第 49–53、69–72 行也展示了削弱效果。最强等价读法是修辞性的“无法抵挡”，仍无法保留 *weaken*。**初审将其具体解释为降低枪击抗性，现有证据不足以支持这一更窄的机制说法**；修正应只承诺“削弱敌人”。
```
</details>

## entry-04106

- 位置：`tome-orcs.lua:8143`（orcs）｜section：`tome-orcs/overload/mod/class/OrcCampaign.lua`｜source_tag：`_t`
- 原文：`%s, the experimenting tinker`
- 现译：`%s，实验的工匠`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00588 | remaining | remaining:rem-19:C04 | advisory |  |  |  |

<details><summary>hrq-00588 · remaining 详情</summary>

```
### C04 | entry-04106 | advisory

原译短引：“%s，**实验的工匠**”。英文 *the experimenting tinker* 指进行实验的工匠；同一事件说明她测试新蒸汽科技时迷路。[事件源码](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/OrcCampaign.lua:389) 第 389–395 行。最强等价读法是“实验的工匠”在称号中仍可理解为做实验的人，故不判错译；“%s，进行实验的工匠”更清楚。

**映射汇总：**C01 → advisory；C02 → confirmed；C03 → confirmed（不采纳初审的“降低枪击抗性”具体解释）；C04 → advisory。新增疑点：无。20 条中存在问题 2 条、仅建议 2 条、未发现问题 16 条、待确认 0 条。

**实际读取与版本限制：**读取了指定入口、`RULES.md`、`batches/rem-19.md`、`reports/gemini-rem-19.md`、`source-access.json`、`terms.json`、本批在 `snapshots/tome-orcs.lua` 的相关同节上下文，以及上引四份 DLC 源码；另读取 `dread.lua`、`OrcCampaign.lua` 和 `PartyTinker.lua` 的相关调用处。所读五份主要源码与来源索引登记的 SHA256 均匹配。本批属于 orcs DLC；冻结文件可确认文本及所示快照行为，**DLC 仓库 commit 和目标游戏版本未固定，不能声称已核验 1.7.4 正式版**。
```
</details>

## entry-04109

- 位置：`tome-orcs.lua:8177`（orcs）｜section：`tome-orcs/overload/mod/class/interface/PartyTinker.lua`｜source_tag：`saySimple`
- 原文：`Created tinker: %s`
- 现译：`创造插件：%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00589 | remaining | remaining:rem-20:C01 | advisory |  |  |  |

<details><summary>hrq-00589 · remaining 详情</summary>

```
### C01 | entry-04109 | advisory

原译“**创造插件：%s**”表达了制成物品的结果。最强等价读法成立；“制作插件”更贴合操作语境，但不足以判为错译。冻结源码在 `PartyTinker.lua:135-145` 创建物品后发出该日志；快照见 `snapshots/tome-orcs.lua:8177`。`terms.json:1521` 的 `tinker→蒸汽工具` 是 *existing* 实体类型记录，不据此强制改掉此处已有的“插件”。
```
</details>

## entry-04110

- 位置：`tome-orcs.lua:8178`（orcs）｜section：`tome-orcs/overload/mod/class/interface/PartyTinker.lua`｜source_tag：`log`
- 原文：`Learnt new tinker schematic: #LIGHT_GREEN#%s`
- 现译：`已学习新的配方：#LIGHT_GREEN#%s`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00590 | remaining | remaining:rem-20:C02 | advisory |  |  |  |

<details><summary>hrq-00590 · remaining 详情</summary>

```
### C02 | entry-04110 | advisory

原译“**已学习新的配方**”省去 `tinker`。`PartyTinker.lua:168-174` 表明这里学习的是工匠配方，补作“插件配方”会更明确；但在该系统中，“配方”及随后显示的名称足以让原译成立。`schematic→配方` 符合 `terms.json:1587`；快照见 `snapshots/tome-orcs.lua:8178`。
```
</details>

## entry-04115

- 位置：`tome-orcs.lua:8341`（orcs）｜section：`tome-orcs/superload/mod/dialogs/debug/DebugMain.lua`｜source_tag：`_t`
- 原文：`The Steam Council has been called to order, with Chief Councilor Tantalos presiding.

TANTALOS: "Greetings, my fellow- heh, now [i]lesser[/i] Councilors!  It is my pleasure to finally lead the proceedings.  The agenda for today..." Ruffles through papers. "Is irrelevant, for I have a solution to every malady mentioned therein.  The first order--"

KASYROS: "With all due respect, Chief Councilor, the agenda--"

TANTALOS: "Is.  [i]Irrelevant.[/i]  Tormak?  You've been scrying on potential sources of geothermal energy, would you care to inform the others where you see the most potential?"

TORMAK: Sighs. "Right under the Kruk orcs, unfortunately.  It's a promising source for sure, the magma powering it hasn't drained out like it has under us, but digging there would...  well, we all know how quickly they turned construction tools into weapons to rival our own.  If we went in there with the state-of-the-art mining equipment necessary to--"

TANTALOS: Laughter. "Mining equipment!  What manner of fool do you take me for?  Palaquie, tell me what's going through the minds of those silly little waist-height warriors, rummaging through the mainland for Orcish rebels." Holds up hand to silence Councilor Emeritus Kasyros. "This IS relevant, I assure you."

PALAQUIE: "Discontent...  revolving around hidden, long-fermented resentment. Some want the Kruk exterminated, others imprisoned.  Neither can afford direct intervention, but some form of support will assuredly be available."

TANTALOS: "So, with the right negotiation, we can get these tinies, who have [i]endless[/i] experience fighting Orcs, to assist us and make any sort of action in Kruk territory more manageable.  At a bare minimum, we can obtain weaponry that has long proved sufficient for slashing Orcish throats...  although we'll need it custom-fit for our size, naturally."

PALAQUIE: "They have a race whose armor would work.  A tight fit, but sufficient."

TANTALOS: "Even better!  And...  Kasyros, I'm going to let [i]you[/i] tell me what the people care about most.  I'm sure your bruises are adequate reminders of the citizens' will?"

KASYROS: [Statement was deemed excessively profane and stricken from the record by 4-2 vote.]

TANTALOS: "Such undignified conduct!  All because you can't accept that the public wants their steam back.  More than they want those filthy little greenskins around, more than they fear getting their hands dirty, more than they want [i]your[/i] way of doing things.  So!  It's resolved that we have much to gain from this, it's resolved that we have or can obtain the means to carry it out, and it's resolved that it is what the voting public desires.  I see no need for further debate.  Nashal, I'd like to speak to you after this about a wand.  Meeting adjourned."

[At this time, Councilor Kasyros gave a lengthy speech before officially resigning from the Council.  It has been recorded in a separate document.] `
- 现译：`在坦塔洛斯议长的主持下，蒸汽议会正式开会。

坦塔洛斯：“你们好啊，我的同……哈，现在是[i]下级[/i]议员们！这是我的荣幸，能够终于主事。今日的议程……”翻动手中的文件。“无关紧要，因为我已经为所有要解决的问题有了一个对应的方案。首先————”

卡西罗斯：“尊敬的议长，议程————”

坦塔洛斯：“这是[i]无关紧要[/i] 的。托马克？你一直在占卜潜在的地热能源，你能告诉大家哪里最有潜力吗？”

托马克：叹气。“不幸的是，就在克鲁克兽人的地盘底下。那确实是个有潜力的源头，提供能源的岩浆可不像我们地盘底下的都枯竭了，但是在那里挖掘会……好吧，我们都知道他们能多快的把建筑工具变成能威胁我们的武器。如果我们把能用来开采的最新式采矿工具带过去————”

坦塔洛斯：大笑。“采矿工具！你把我当成是怎样的傻瓜？帕拉奎，告诉我那些在大陆上到处搜寻兽人反叛者的齐腰高的小傻战士们在想什么。”举起手打断荣誉终身议员卡西罗斯。“我保证，真的无关紧要。”

帕拉奎：“不满……以及隐藏的，长期发酵的怒火。有些人想消灭克鲁克兽人，也有人想监禁他们。不论是哪种，我们都没法直接介入，不过确实可以提供某种支持。”

坦塔洛斯：“那么，在恰当的协商后，我们可以让那些有[i]无数[/i]兽人作战经验的小东西，来协助我们，让在克鲁克兽人境内的一切行动更易掌控。最少，我们可以取得那些已被长期证明能割断兽人喉咙的武器装备……自然，我们确实得想法子改成我们的尺寸。”

帕拉奎：“他们有个种族，护甲可以给我们用。穿起来有点紧，但是足够了。”

坦塔洛斯：“那就更好了！还有……卡西罗斯，我想让[i]你[/i]告诉我人民最在意什么。我敢肯定，你身上的伤痕一定能提醒你，公民们的意志是什么，对吧？”

卡西罗斯：[这一表述被视作过分的亵渎，以4比2的投票，通过从记录中削除。]

坦塔洛斯：“真是不成体统的发言啊！只是你们不能接受群众想要回他们的蒸汽。比起想要那些狡猾的小绿人们在身边，比起他们害怕把自己的手弄脏，比起想要以[i]你们[/i]的方法做事，更想要蒸汽。所以！这决定了我们从这方案里获益良多，决定了我们有或能找到解决困难的方式，也决定了这是选民们想要的。我看不需要进一步讨论了。纳沙尔，之后我想跟你讨论一个魔杖的事情。散会。”

[同时，卡西罗斯议员也在从议会正式辞职时做了一个不短的演讲。演讲被另一个文件记载。] `

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00591 | remaining | remaining:rem-20:C03 | confirmed |  |  |  |
| hrq-00592 | remaining | remaining:rem-20:C04 | confirmed |  |  |  |
| hrq-00593 | remaining | remaining:rem-20:C05 | confirmed |  |  |  |
| hrq-00594 | remaining | remaining:rem-20:C06 | advisory |  |  |  |
| hrq-00595 | remaining | remaining:rem-20:N01 | confirmed |  |  |  |
| hrq-00596 | remaining | remaining:rem-20:N02 | advisory |  |  |  |

<details><summary>hrq-00591 · remaining 详情</summary>

```
### C03 | entry-04115 | confirmed

原译“**我保证，真的无关紧要**”与 `This IS relevant` 正好相反。前文称议程 *irrelevant*，此处坦塔洛斯强调自己转谈的方案**确实相关**；不存在能保留反义词的等价读法。建议改为“我保证，这确实切题”。证据：`palace-fumes.lua:90-100`、`snapshots/tome-orcs.lua:8375`。
```
</details>

<details><summary>hrq-00592 · remaining 详情</summary>

```
### C04 | entry-04115 | confirmed

原译“**不论是哪种，我们都没法直接介入**”把 `Neither` 所指的两派人变成说话者一方。最强等价读法是“我们”泛指参与讨论的人，但前句的“有些人……也有人……”及后句向他们争取支援，均支持“**两方都无力直接介入**”。证据：`palace-fumes.lua:98-102`、`snapshots/tome-orcs.lua:8377`。
```
</details>

<details><summary>hrq-00593 · remaining 详情</summary>

```
### C05 | entry-04115 | confirmed

原译“**狡猾的小绿人**”将 `filthy` 的“肮脏、污秽”换成了“狡猾”，改变了辱骂的具体含义；两词在此没有足够的等价读法。建议按原文的蔑称处理。证据：`palace-fumes.lua:110`、`snapshots/tome-orcs.lua:8387`。
```
</details>

<details><summary>hrq-00594 · remaining 详情</summary>

```
### C06 | entry-04115 | advisory

原译“**这决定了我们从这方案里获益良多**”弱化了 `It's resolved that...` 连续三次作出议会决议的口吻。结合会议及散会语境，读者仍可将“决定了”理解为议会已定下结论，故暂列文体澄清建议；“决议认定……”更准确。证据：`palace-fumes.lua:88-110`、`snapshots/tome-orcs.lua:8387`。
```
</details>

<details><summary>hrq-00595 · remaining 详情</summary>

```
### N01 | entry-04115 | confirmed

原译“**过分的亵渎**”把 `excessively profane` 指向亵渎神圣事物；此处描述的是卡西罗斯发言**粗俗、满口脏话**，随后被投票从记录中删去。“亵渎”缺乏该段的宗教对象作等价支撑。证据：`palace-fumes.lua:108`、`snapshots/tome-orcs.lua:8385`。
```
</details>

<details><summary>hrq-00596 · remaining 详情</summary>

```
### N02 | entry-04115 | advisory

末句原文是卡西罗斯在**正式辞职前**作了长篇演说，译文“**在从议会正式辞职时**”模糊了先后。它也可宽泛指辞职过程，故建议明确为“正式辞职前”。证据：`palace-fumes.lua:112`、`snapshots/tome-orcs.lua:8389`。
```
</details>

## entry-04116

- 位置：`tome-possessors.lua:5`（possessors）｜section：`tome-possessors/data/achievements/possessors.lua`｜source_tag：`_t`
- 原文：`Kill your own Doomed Shade in the body of Bill.`
- 现译：`使用比尔的身体杀死你自己的被诅咒的影子。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00597 | remaining | remaining:rem-10:C01 | confirmed |  |  |  |

<details><summary>hrq-00597 · remaining 详情</summary>

```
### C01 | entry-04116 | confirmed

原译“**被诅咒的影子**”把 *Doomed Shade* 当作普通描述。固定版本的本体源码确有以 `Doomed Shade of %s` 命名的玩家分身；冻结术语将职业 *Doomed* 记为“末日使者”。最强的等价读法是把 *doomed* 泛指“遭厄运的”，但在已有同名实体的语境中，“被诅咒的”会错指。建议译为“末日使者之影”等。此项确认的是**名称译法**；本体实体定义不能证明 Possessors 成就的触发机制。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:5>)；本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/data/zones/shadow-crypt/npcs.lua:86–104`；[术语快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json:36>)。
```
</details>

## entry-04123

- 位置：`tome-possessors.lua:56`（possessors）｜section：`tome-possessors/data/talents/psionic/battle-psionics.lua`｜source_tag：`tformat`
- 原文：`You concentrate to create a psionic block field all around you for 5 turns.
		While the effect holds all damage against you have a %d%% chance to be fully ignored.
		When damage is cancelled you instinctively make a retaliation mind strike against the source, dealing %0.2f mind damage. (The retaliation may only happen 2 times per turn.)
		`
- 现译：`创造一个持续 5 回合的灵能盾牌围绕你。
		技能生效时有 %d%% 几率会无视伤害。
		如果伤害被无视，你会对目标进行反击，造成 %0.2f 精神伤害。（每回合最多 2 次）
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00598 | remaining | remaining:rem-10:N01 | advisory |  |  |  |

<details><summary>hrq-00598 · remaining 详情</summary>

```
### N01 | entry-04123 | advisory

原文说伤害被取消后“**against the source**”反击伤害来源；译文写“**对目标进行反击**”。“目标”可被读作造成该次伤害者，故尚不足以确认错指，但脱离战斗语境时指代不清。建议明确为“向伤害来源反击”。[冻结批次原文与译文](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-10.md>)。
```
</details>

## entry-04129

- 位置：`tome-possessors.lua:119`（possessors）｜section：`tome-possessors/data/talents/psionic/deep-horror.lua`｜source_tag：`tformat`
- 原文：`For a brief moment your whole body becomes etheral and you dash into a nearby creature and all those in straight line behind it (in range %d).
		You reappear on the other side, with %d more psi and having dealt %0.2f mind damage to your targets.
		`
- 现译：`短暂的一瞬间，你的整个身体变得飘渺，你对附近一个生物进行一次直线冲锋 (范围 %d)。
		你再次出现在另一边，获得 %d 灵能值并对目标造成 %0.2f 精神伤害。
		`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00599 | remaining | remaining:rem-10:C02 | confirmed |  |  |  |

<details><summary>hrq-00599 · remaining 详情</summary>

```
### C02 | entry-04129 | confirmed

原译“**对附近一个生物进行一次直线冲锋**”遗漏 *and all those in straight line behind it*，后句又以单数“目标”承接原文复数 *targets*。即使“直线冲锋”暗示沿线移动，也没有表达该生物后方的其他生物同样受招。建议补出“及其后方直线上的所有生物”，并用复数指代承接伤害。此为冻结文本可直接证明的漏译；未核实 DLC 的实际运行行为。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:119>)。
```
</details>

## entry-04137

- 位置：`tome-possessors.lua:270`（possessors）｜section：`tome-possessors/data/talents/psionic/psionic-menace.lua`｜source_tag：`tformat`
- 原文：`You point your ghastly finger at a foe affected by Ghastly Wail and send a psionic impulse to tell it to simply die.
		The target will take %d%% of the life it already lost as mind damage.
		On targets of rank boss or higher the damage is limited to %d.
		If the target dies from the Finger and is of a type you can already absorb it is directly absorbed into your bodies reserve.
		If you do not have two mindstars equiped, but have them in your off set, you instantly automatically switch. The wild psionic powers are incompatible with the focused nature of psiblades.`
- 现译：`用手指对受到恐怖嚎叫效果影响的敌人射出一道冲击波。
		目标将受到相当于其已损失生命值 %d%% 的精神伤害。
		对 boss 或者更高阶级的目标伤害最高为 %d。
		如果目标死于死亡一指，且其类型是你已经可以吸收的，则直接吸收到你的身体储备中。
		如果你没有双持灵晶，但在备用武器组里装备了它们，你会立刻自动切换到那组武器。此技能与心灵利刃不兼容。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00600 | remaining | remaining:rem-10:C03 | advisory |  |  |  |

<details><summary>hrq-00600 · remaining 详情</summary>

```
### C03 | entry-04137 | advisory

原译“**射出一道冲击波**”保留了向敌人发出力量的读法，但省去 *ghastly finger* 的阴森形象，以及 *tell it to simply die* 的精神命令意象。后续伤害、上限和吸收条件仍有翻译，因此作为叙事忠实度建议保留，不判为机制错译。可改为“以阴森的手指指向……发出一道命其死去的灵能脉冲”。[译文快照](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:266>)。
```
</details>

## entry-04141

- 位置：`tome-possessors.lua:356`（possessors）｜section：`tome-possessors/data/talents/psionic/ravenous-mind.lua`｜source_tag：`tformat`
- 原文：`As long as you have at least a stack of Sadist you can radiate agony to all those you see in radius %d with 80%% or lower life left.
		For 5 turns their mind will be so focused on their own pain that they will deal %d%% less damage to you.`
- 现译：`当你至少有一层虐待狂效果时，你可以将自己的痛苦分享给半径 %d 内所有可见的、生命值 80%% 或更低的敌人。
		持续 5 回合，他们的头脑将如此专注于自己的痛苦，对你的伤害减少 %d%%。`

| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |
|---|---|---|---|---|---|---|
| hrq-00601 | remaining | remaining:rem-10:C04 | confirmed |  |  |  |

<details><summary>hrq-00601 · remaining 详情</summary>

```
### C04 | entry-04141 | confirmed

原译“**将自己的痛苦分享给**”给痛苦增添了玩家所有格；原文仅说向符合条件者 *radiate agony*，随后明确说敌人专注于“他们自己的痛苦”。“分享”可以作传递痛苦的修辞等价读法，却不能支持新增的“自己的”，且会改变痛苦归属。建议改为“向……辐射痛苦”。这是文本语义判定，不宣称已核实 DLC 效果实现。[同段上下文与译文](</home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:342>)。
```
</details>
