# 咨询：ToME4 中文本地化中 `crypt` 的译名方案

## 你的任务

这是一个**独立判断**请求。回答三个问题：

1. 游戏中全部 `crypt` 是否应当**统一**为同一个中文译名？
2. 若统一，应当用哪个译名？给出理由。
3. 若不统一，分派方案是什么？按什么判据分派？各类用什么译名？

**要求**：结论必须能落到下面每一条具体条目上（说明每条取什么），并说明你的方案与既有术语绑定是否冲突。
不要回避取舍——如果某个方案在某几条上明显更差，说出来并说明你为什么仍然（或不再）选它。

## 背景

《Tales of Maj'Eyal》（ToME4）是一款开源 roguelike。本项目维护其简体中文本地化。
译文以 `t("<英文原文>", "<中文译文>", "<kind>")` 的形式存放。

`kind` 的含义：`entity name` / `_t`（通用字符串）/ `talent name`（技能名）/
`log` `logPlayer`（战斗日志）/ `newLore category`。区名、物品名、技能名会显示在 UI 上。

## 一、当前全部 `crypt` 条目（34 行，含上下文与现译）

### A. 区域名与区域内实体（玩家会在地图/界面上看到）

| 位置 | 英文 | 现译 | 说明 |
|---|---|---|---|
| `zones/crypt-kryl-feijan/zone.lua` | `Crypt` | 地窖 | 区名 |
| 同上 | `Dark crypt` | 黑暗地窖 | 区名变体 |
| `achievements/quests.lua` | `Saved Melinda from her terrible fate in the Crypt of Kryl-Feijan.` | 从克里尔·费扬邪教手中把梅琳达从厄运中拯救出来。 | 成就；**crypt 在译文中整个丢失** |
| `quests/kryl-feijan-escape.lua` | `You discovered a sect worshipping a demon named Kryl-Feijan in a crypt.` | 你在一个地窖中发现了一个崇拜名为克里尔·费扬的恶魔的教派。 | 任务文本 |
| 同上 | `You failed to protect her when escorting her out of the crypt.` | 你没能成功地将她护送出这个地窖。 | 任务文本 |
| `zones/shadow-crypt/zone.lua` | `Shadow Crypt` | 阴影地窖 | 区名 |
| `general/encounters/fareast.lua` | `Shadow Crypt` | 阴影地窖 | entity name |
| 同上 | `Entrance to a dark crypt` | 通向阴影地窖之路 | 入口 |
| `general/events/rat-lich.lua` | `Forsaken Crypt` | 废弃地窖 | 事件区名 |
| 同上 | `collapsed forsaken crypt` | 坍塌的废弃地窖 | |
| 同上 | `Stairs seem to lead into some kind of crypt.` | 通往某个地窖的楼梯。 | 地图上楼梯的提示文本 |
| 同上 | `#VIOLET# As you leave the crypt, the stairway collapses in upon itself.` | #VIOLET# 当你离开地窖的时候，楼梯崩塌了。 | 日志 |
| `maps/vaults/greater-crypt.lua` | `, and the crypt rearranges itself around you!` | ，突然，你周围地窖的地形自己改变了！ | 密室地图日志 |

**这三处 crypt 在游戏中分别是什么（世界观事实）：**

- **Crypt of Kryl-Feijan**：早期区域。一个崇拜恶魔 Kryl-Feijan 的邪教在此活动，
  玩家在此救出被作为祭品的 Melinda。内有邪教徒、恶魔、不死生物。
- **Shadow Crypt**：远东区域，与 yeek 克隆体剧情相关。
- **Forsaken Crypt**：随机事件「鼠巫妖」（rat-lich）所在地，巫妖 = 不死法师。
- **greater-crypt**：一种会自行变形的密室（vault）地图。

### B. 通用遭遇文本

| 位置 | 英文 | 现译 |
|---|---|---|
| `general/encounters/maj-eyal.lua` | `You find an entrance to an old crypt. An aura of terrible evil emanates from this place. You feel threatened just standing there.` | 你发现了一个古老地窖的入口，里面笼罩着恐怖的邪恶气息，仅仅站在门口你就已经感受到了它的威胁。 |
| 同上 | `#LIGHT_RED#You carefully open the door and enter the underground crypt...` | #LIGHT_RED#你小心翼翼地打开门，进入了地下的地窖…… |
| 同上 | `Enter the crypt` | 进入地窖 |

### C. 技能名

| 位置 | 英文 | 现译 |
|---|---|---|
| `talents/spells/master-of-bones.lua` | `Call of the Crypt` | 地窖召唤 |

**该技能做什么**（引擎源码中的描述）：
> Call upon the battlefields of old, collecting bones, fusing them with souls, and forging them into skeletal minions.
> Up to %d skeleton warriors of level %d are summoned...

即：召唤古战场的骸骨，与灵魂融合，铸成骷髅仆从。属死灵法师「骸骨大师」系。

### D. 叙事文本（lore / 对话）

| 位置 | 英文片段 | 现译片段 |
|---|---|---|
| `chats/last-hope-melinda-father.lua` | `That is why I got stuck in that crypt, I want to see the world.` | 这也是为什么我会被困在那个地窖里，我想去看看外面的世界。 |
| `lore/elvala.lua` | `This cold, crypt-like hollow was covered in smooth, glistening ice` | 这是个冰冷的、地窖般的空洞，四周覆盖着光滑闪亮的冰块 |
| `lore/fun.lua` | `when a particular land has seen enough bloodshed - battlefields, forest, crypts and graveyards - wights can be seen to rise en masse` | 某片土地经历了足够多的杀戮——无论战场、森林、地窖还是墓园——尸妖便会成群升起 |
| `lore/fun.lua` | `many souls are driven mad in the employ of necromancers, ceaselessly drifting through windswept crypts` | 它们不停的随风飘荡（**crypts 在译文中整个丢失**） |
| `lore/last-hope.lua` | `I am cold and alone in this chilly crypt` | 在这寒冷的地窖中我又冷又孤单 |
| `lore/misc.lua` | `think of derelict, crumbling crypts, cults and demons` | 请想象一下，废弃的远古地窖里巨岩崩碎跌落；疯狂的邪教徒将恶魔…… |
| `init.lua` | `Dreadfell has always been shunned for its haunted crypts` | 恐惧王座一直以来都因闹鬼而为人所避讳。（**crypts 在译文中整个丢失**） |

（注：上表中标「整个丢失」的三处是**漏译**问题，与译名选择是两回事，但会影响「统一」的实际覆盖面。）

## 二、既有术语绑定（选定的译名不得与这些冲突）

下列中文词在本库中**已经绑定给别的英文词**。任何方案若复用它们，就会造成一词两指：

| 中文 | 已绑定的英文 | 例子 |
|---|---|---|
| 洞穴 | `cave` | `Damp Cave`→潮湿洞穴、`ice cave`→冰封洞穴、`cave troll`→洞穴巨魔、`Scintillating Caves`→闪光洞穴（全库数十处） |
| 地穴 | `breeding pits`、`Intimidating Cave` | `Killed the Orc Greatmother in the breeding pits`→在繁衍地穴中；`Intimidating Cave`→恐怖地穴 |
| 墓穴 | `grave`、`tombs` | `grave (opened)`→已打开的墓穴；`grave wight`→墓穴尸妖；`beneath tombstones`→地下墓穴 |
| 墓园 | `graveyard` | 见上表 `lore/fun.lua` 一行 |
| 地窖 | `crypt`（当前） | 本次议题 |

**相关的其它既有译名**（供判断语域一致性）：
`Dreadfell`→恐惧王座、`lich`→巫妖、`wight`→尸妖、`necromancer`→死灵法师、
`undead`→不死生物、`Master of Bones`→骸骨大师。

## 三、语言事实（供参考，不是结论）

- `crypt` 的英文义：教堂或建筑地下的墓室/地下室，主要用于安葬。
- 「地窖」的现代汉语常用义：储藏用的地下室（如菜窖、酒窖）。
- 「墓穴」：埋葬死者的坑穴/墓室。
- 「地宫」：帝王陵墓的地下建筑。
- 「陵寝」「墓室」「幽冥」「冥窟」等亦在候选范围内。

## 四、约束

1. 译名要能同时用作**区名**（显示在地图与界面）、**技能名**、**叙事散文**，三者语域不同。
2. 不得与第二节的既有绑定冲突。
3. 若主张分派方案，判据必须**可机械执行**（例如「按 kind 分」「按是否为专名分」），
   不能是「视语境而定」这种无法落地的说法。
4. 本库既有风格：专名多用意译或音译定名，区名偏好二至四字。

## 五、输出格式

请用中文回答，结构如下：

```
## 结论
（统一 / 不统一，一句话）

## 理由
（论证，包含你考虑过并否决的方案及否决理由）

## 逐条落地
（对第一节 A/B/C/D 四类的每一条，给出你的译名；有分派方案的说明每条归入哪一类）

## 与既有绑定的冲突检查
（逐条对照第二节）

## 你方案的弱点
（诚实列出你的方案在哪些条目上不如替代方案）
```

只读回答，不要修改任何文件。
