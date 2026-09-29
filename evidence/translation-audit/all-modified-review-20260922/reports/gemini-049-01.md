本批次为 **batch-049**（条目范围：`entry-01345` 至 `entry-01384`，共 40 条）。
文件 SHA-256 校验结果：`ce34320532d3c5267e60ad0e6fd6a2e9e0ee715c3839885d5fdb77008b78c443`，哈希一致。

本批条目均位于 `mod-tome`，已按规定使用公开源码固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`git -C /workspace/t-engine4 show <commit>:<path>`）及译文终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00` 所在 section 上下文进行逐条比对核验。

---

### entry-01345
- **位置**：`mod-tome.lua:19464`（`mod-tome/data/lore/slazish.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/lore/slazish.lua` 中 `slazish-note-3`。斜体标记 `#{italic}#...#{normal}#`、段落换行、句首引号及尾部双换行完全吻合；专有名词（“Sunwall” -> “太阳堡垒”、“farportal” -> “远行传送门”、“Sher'Tul” -> “夏·图尔”、“Slasul” -> “萨拉苏尔”）均与术语规范一致，语义忠实流畅。

### entry-01346
- **位置**：`mod-tome.lua:19520`（`mod-tome/data/lore/spellhunt.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/lore/spellhunt.lua` 中 `spellhunt-note-1`。原文多段间隔省略号 `...` 均准确转换为全角省略号 `……` 并保留空行结构；专名“Spellhunt”采用推荐规范“魔法狩猎”，“Angolwen”准确对应“安格利文”，“Linaniil”对应“莱娜尼尔”，语意准确无误。

### entry-01347
- **位置**：`mod-tome.lua:19639`（`mod-tome/data/lore/sunwall.lua`）
- **状态**：细微观察
- **依据**：对照源码 `game/modules/tome/data/lore/sunwall.lua` 中 `sunwall-note-1`。译文中专有名词“太阳堡垒”、“弗洛萨斯领主”（Lord Forosyth）、“桑切尔”（Thanchir）均翻译准确。细微观察点在于换行结构：源码中第 1 行末尾（`...tell the kids that I love them.`）与第 2 行（`With that said I shall be...`）之间为单换行 `\n`，而译文在“再告诉孩子们我爱他们。”后增加了一个空行（变为 `\n\n`）产生分段。虽增强了中文排版可读性，但换行结构相比原文稍有变动。

### entry-01348
- **位置**：`mod-tome.lua:19688`（`mod-tome/data/lore/tannen.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/lore/tannen.lua` 中 `tannen-level2`。三段结构严格保留；强调斜体 Markdown `_before_` 准确保留为 `_之前_`；专有名词与核心设定翻译准确：“Angolwen” -> “安格利文”、“Sher'Tul” -> “夏·图尔”、“Ziguranth” -> “伊格兰斯”（按规范指代教团人群）、“Spellblaze” -> “魔法大爆炸”、“drolem” -> “龙傀儡”、“bone-giants” -> “骨巨人”。

### entry-01349
- **位置**：`mod-tome.lua:19825`（`mod-tome/data/lore/zigur.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/lore/zigur.lua` 中 `zigur-potion`。全文 8 个自然段严格对应；“Derth” -> “德斯镇”、“Summertide” -> “炎华之月”、“halfling” -> “半身人”、“arcane” -> “奥术”等名词均准确无误，对话引号与标点规范完整。

### entry-01350
- **位置**：`mod-tome.lua:19878`（`mod-tome/data/maps/towns/last-hope.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/towns/last-hope.lua` 中地块实体 `'Y'`。原文 `Statue of Queen Mirvenia the Inspirer` 准确译为 `鼓舞者米雯尼雅女王的雕像`，与同地图国王托拉克、托克诺雕像格式高度统一。

### entry-01351
- **位置**：`mod-tome.lua:19908`（`mod-tome/data/maps/vaults/auto/greater/paladin-vs-vampire.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/vaults/auto/greater/paladin-vs-vampire.lua`。战斗日志调用 `self:logCombat(who, "#Source# emits dark energies at your feet.")`，占位符 `#Source#` 完整保留于句首，译文“朝你脚下喷吐黑暗能量。”准确传达熔岩腐化地面效果。

### entry-01352
- **位置**：`mod-tome.lua:19911`（`mod-tome/data/maps/vaults/auto/greater/paladin-vs-vampire.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `paladin-vs-vampire.lua` 实体 `'S'` 的 `desc` 属性。原文 `A Human in shining plate armour.` 准确译为 `穿着闪亮板甲的人类。`，句式简洁明了。

### entry-01353
- **位置**：`mod-tome.lua:19964`（`mod-tome/data/maps/vaults/greater-crypt.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/vaults/greater-crypt.lua`。源码由 `game.logPlayer(actor, "Something in the floor clicks ominously%s", ... and _t", and the crypt rearranges itself around you!" or ".")` 拼合，条目译文以逗号开头 `，突然，你周围地宫的地形自己改变了！`，与前导句“什么东西在地上发出了不祥的咔嗒声%s”拼合后逻辑严密，标点闭合正确。

### entry-01354
- **位置**：`mod-tome.lua:20053`（`mod-tome/data/maps/zones/halfling-ruins-last.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/zones/halfling-ruins-last.lua` 中实体 `'>'` 的弹窗提示。原文 `As you enter the tunnel you feel a strange compulsion to go backward.` 准确译为 `当你进入隧道时，你感到一种奇怪的冲动，驱使你往回走。`，叙述自然准确。

### entry-01355
- **位置**：`mod-tome.lua:20059`（`mod-tome/data/maps/zones/shertul-fortress-caldizar.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/zones/shertul-fortress-caldizar.lua`。区域名 `Exploratory Farportal` 严格遵循术语库首选条目（`T.GAME.ENTITY`）翻译为 `探索用远行传送门`。

### entry-01356
- **位置**：`mod-tome.lua:20064`（`mod-tome/data/maps/zones/tannen-tower-1.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/zones/tannen-tower-1.lua` 边界地形实体 `'='`。原文 `open sky` 译为 `开阔的天空`，准确表达塔顶开阔空域障碍地块。

### entry-01357
- **位置**：`mod-tome.lua:20069`（`mod-tome/data/maps/zones/tempest-peak-top.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/maps/zones/tempest-peak-top.lua` 边界实体 `'-'`。原文 `open sky` 译为 `开阔的天空`，与同类山顶边界地块译法统一。

### entry-01358
- **位置**：`mod-tome.lua:20088`（`mod-tome/data/mapscripts/lib/subvault.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/mapscripts/lib/subvault.lua` 中子宝库楼梯耐久状态（`self._use_count < 2` 时更名）。原文 `nearly collapsed hidden vault` 准确译为 `近乎坍塌的隐藏宝库`。

### entry-01359
- **位置**：`mod-tome.lua:20111`（`mod-tome/data/quests/antimagic.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/antimagic.lua` 任务描述。原文 `...join a group called the Ziguranth, dedicated to opposing magic.` 中“Ziguranth”指反魔教团组织，按规范准确译为“伊格兰斯”，全句表达通顺。

### entry-01360
- **位置**：`mod-tome.lua:20120`（`mod-tome/data/quests/arena-unlock.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/arena-unlock.lua` 任务描述。原文末尾无标点，译文规范补齐句号，表达为 `你被一个盗贼邀请，证明你作为一个斗士的能力，以获得进入竞技场的资格。`，符合任务情节。

### entry-01361
- **位置**：`mod-tome.lua:20127`（`mod-tome/data/quests/arena.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/arena.lua` 任务描述。原文感叹号保留，“Arena”遵循规范译为“竞技场”，文风贴切。

### entry-01362
- **位置**：`mod-tome.lua:20130`（`mod-tome/data/quests/arena.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/arena.lua` 获胜文本 `onWin`。颜色标签 `#GOLD#...#WHITE#` 完整对称保留，称号“Challenge of the Master”译为“擂主的挑战”，准确对应游戏内成就与模式名称。

### entry-01363
- **位置**：`mod-tome.lua:20131`（`mod-tome/data/quests/arena.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/arena.lua` 获胜说明段落。原文 `You valiantly fought every creature the arena could throw at you and you emerged victorious!` 准确译为 `你勇敢地战胜了竞技场里的所有生物并赢得了最终胜利！`。

### entry-01364
- **位置**：`mod-tome.lua:20144`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/brotherhood-of-alchemists.lua`。颜色码 `#RED#...#WHITE#` 完整保留，占位符 `%s` 顺序与位置正确；专有名词“Maj'Eyal” -> “马基·埃亚尔”、“Brotherhood of Alchemists” -> “炼金术士兄弟会”完全遵循术语库规范。

### entry-01365
- **位置**：`mod-tome.lua:20150`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `brotherhood-of-alchemists.lua`。颜色码 `#SLATE#...#WHITE#` 及前导标记 `  * '...'` 完整无损，两个 `%s` 占位符（材料名、材料说明）顺序正确无漂移。

### entry-01366
- **位置**：`mod-tome.lua:20153`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `brotherhood-of-alchemists.lua` 任务接取提示。颜色码 `#VIOLET#` 正确保留，界面菜单选项“Show ingredients”准确对应汉化界面的“查看材料”。

### entry-01367
- **位置**：`mod-tome.lua:20154`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `brotherhood-of-alchemists.lua` 奖励分发日志。占位符 `%s` 完整保留，末尾补中文句号符合游戏日志常用排版。

### entry-01368
- **位置**：`mod-tome.lua:20155`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `brotherhood-of-alchemists.lua` 及 `game/modules/tome/data/general/objects/brotherhood-artifacts.lua`（9449 行）。“elixir of the fox”译为“狡诈药剂”，任务与对应实体道具名称完全一致。

### entry-01369
- **位置**：`mod-tome.lua:20156`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9455 行）。“elixir of avoidance”译为“闪避药剂”，任务配方与道具名称完全一致。

### entry-01370
- **位置**：`mod-tome.lua:20157`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9460 行）。“elixir of precision”译为“精准药剂”，任务配方与道具名称完全一致。

### entry-01371
- **位置**：`mod-tome.lua:20158`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9465 行）。“elixir of mysticism”译为“神秘药剂”，任务配方与道具名称完全一致。

### entry-01372
- **位置**：`mod-tome.lua:20159`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9470 行）。“elixir of the savior”译为“守护药剂”，任务配方与道具名称完全一致。

### entry-01373
- **位置**：`mod-tome.lua:20160`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9475 行）。“elixir of mastery”译为“掌握药剂”，任务配方与道具名称完全一致。

### entry-01374
- **位置**：`mod-tome.lua:20161`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9481 行）。“elixir of explosive force”译为“爆炸药剂”，任务配方与道具名称完全一致。

### entry-01375
- **位置**：`mod-tome.lua:20162`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9486 行）。“elixir of serendipity”译为“幸运药剂”，任务配方与道具名称完全一致。

### entry-01376
- **位置**：`mod-tome.lua:20163`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9491 行）。“elixir of focus”译为“专注药剂”，任务配方与道具名称完全一致。

### entry-01377
- **位置**：`mod-tome.lua:20164`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9496 行）。“elixir of brawn”译为“蛮牛药剂”，任务配方与道具名称完全一致。

### entry-01378
- **位置**：`mod-tome.lua:20165`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9501 行）。“elixir of stoneskin”译为“石肤药剂”，任务配方与道具名称完全一致。

### entry-01379
- **位置**：`mod-tome.lua:20166`（`mod-tome/data/quests/brotherhood-of-alchemists.lua`）
- **状态**：未发现问题
- **依据**：对照源码及 `brotherhood-artifacts.lua`（9506 行）。“elixir of foundations”译为“领悟药剂”，任务配方与道具名称完全一致。

### entry-01380
- **位置**：`mod-tome.lua:20173`（`mod-tome/data/quests/charred-scar.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `game/modules/tome/data/quests/charred-scar.lua`。神器名“Staff of Absorption”译为“吸能法杖”，与全库实体名称（11593 行）、任务对话（20866 行）保持全局统一。

### entry-01381
- **位置**：`mod-tome.lua:20174`（`mod-tome/data/quests/charred-scar.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `charred-scar.lua`。原文 `Whatever their plan may be, they must be stopped at all cost.` 译为 `不管他们的目的是要干什么，必须不惜一切代价阻止他们。`，语义明确传达。

### entry-01382
- **位置**：`mod-tome.lua:20175`（`mod-tome/data/quests/charred-scar.lua`）
- **状态**：存在疑点
- **依据**：对照源码 `game/modules/tome/data/quests/charred-scar.lua`：
  - 原文由三句构成：
    1. `The volcano is attacked by orcs.`
    2. `A few Sun Paladins made it there with you.`
    3. `They will hold the line at the cost of their lives to buy you some time.`
  - 当前译文：“火山受到了兽人的攻击，一些太阳骑士正顶在最前线用他们的生命来帮助你争取一些时间。”
  - 疑点：原文第二整句 `A few Sun Paladins made it there with you.`（几名太阳骑士与你一同赶到了那里）在译文中被漏译，缺少了交代这几名太阳骑士是随玩家一同前往灼烧之痕前线的背景信息。

### entry-01383
- **位置**：`mod-tome.lua:20176`（`mod-tome/data/quests/charred-scar.lua`）
- **状态**：未发现问题
- **依据**：对照源码 `charred-scar.lua`。原文 `Honor their sacrifice; do not let the orcs finish their work!` 译为 `向他们的献身精神致敬！不要让兽人们达成所愿！`，祈使语气与标点对应恰当。

### entry-01384
- **位置**：`mod-tome.lua:20177`（`mod-tome/data/quests/charred-scar.lua`）
- **状态**：存在疑点
- **依据**：对照源码 `game/modules/tome/data/quests/charred-scar.lua`：
  - 原文：`You arrived too late. The place has been drained of its power and the sorcerers have left.`
  - 译文：`你来的太晚了，这里的能量已经被吸干，而那些法师已经离开了。`
  - 疑点 1（用字规范）：句首“你来的太晚了”中助词“的”应为结构助词“得”（“你来得太晚了”）。
  - 疑点 2（术语/指称一致性）：此处“the sorcerers”在剧情机制中特指主线战役兽人军团的两位幕后核心施术者（Elandar 与 Argoniel）。在同一任务脚本的后续日志条目中（20180 行 `The Sorcerers have departed!`、20181 行 `The Sorcerers flee through a portal...`），均统一翻译为“巫师们”，而此处被译为了泛称“那些法师”，存在同任务内指称不一致的现象。