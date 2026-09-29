# abc-40-20260923：40 条译文独立复核报告（REVIEWER，只读）

按 INPUT 的分类逐条给结论，40 条全部覆盖，结果如下：

| 结论 | 条数 | 条目 |
|---|---|---|
| 存在问题 | 4 | 03174、03176、03179、03203 |
| 仅建议 | 8 | 03183、03184、03191、03194、03196、03201、03202、03210 |
| 待确认 | 0 | — |
| 未发现问题 | 28 | 其余各条，逐条列在下面 |

我先用脚本机械比对了 40 条的颜色标记、`#{…}#` 样式标记、格式占位符和首尾空白。所有条目的标记和占位符序列都与原文一致，没有发现运行时格式缺陷。只有 03203 的空行位置不一样（见该条）。冻结源码的 7 个文件都算了 sha256，结果与 source-access.json 一致。

本报告不是生产用的 contract JSON，也不声称 DONE_VERIFIED。

---

## Birther.lua

**entry-03172** `Random!` → `随机！`：**未发现问题**。这是随机建角按钮（Birther.lua:93）。

**entry-03173** `Basic Gameplay (recommended)` → `基本游戏教程（推荐）`：**未发现问题**。这是「Tutorials」对话框里的按钮（Birther.lua:423-424），加上「教程」是按语境补全。

**entry-03174**：**存在问题**（原意，低影响）
- 问题：原文 `will make locked campaigns, races and classes permanently available` 是一句泛指，说的是解锁这几类选项。译文写成 `永久解锁这个战役，种族，职业`，变成了指向当前这一个选项，而且把三类都说上了。
- 依据：`locktext` 在 `generateCampaigns`、`generateDifficulties`、`generatePermadeaths`、`generateRaces`、`generateClasses` 里都有定义（Birther.lua:804/826/858/890/944）。它会拼接到任意被锁选项的描述末尾，包括难度和永久死亡模式选项。玩家在一个被锁的难度选项上会看到「永久解锁这个战役，种族，职业」，这句话与所选对象不符。
- 附带：`Performing certain actions and completing certain quests` 被译成 `完成特定的任务或条件`。「actions」变成了「条件」，「and」变成了「或」，属于轻微偏差。

**entry-03175**：**未发现问题**。只在 `how == "nolore"` 时加在描述前面（Birther.lua:966-967）。`#CRIMSON#…#WHITE#` 和末尾换行都保留了，语义准确。

**entry-03176**：**存在问题**（原意，低影响），另有几处仅属建议
- 问题 1（遗漏）：`While this is a free game that I am doing for fun` 被译成 `尽管这只是我自娱自乐所做的一款游戏`，丢了「free（免费）」。这是捐赠说明里的关键前提。
- 问题 2（理解偏差）：`I certainly will not complain as real life can be harsh sometimes` 被译成 `不会再抱怨现实的诸多压力了`。原文的 `as…` 是原因从句，意思是「生活有时艰难，所以得到资助我当然不会拒绝」。译文把原因变成了抱怨的对象，意思成了「从此不再抱怨生活压力」。
- 仅建议：
  - 标题 `Tales of Maj'Eyal` 在这里译作「马基·埃亚尔的故事」，同一批上下文 DeathDialog（context.lua:313）作「马基·埃亚尔的传说」，游戏标题不统一。`Maj'Eyal` 本身符合术语表 preferred 的「马基·埃亚尔」。
  - `I realize this can not please everybody` 里的 this 指的是可重玩、靠死亡学习的设计，译文写成「这款游戏可能不会被所有人接受」。
  - 第 6、7 行的断行移了位置：`It will help ensure its survival.` 被挪到下一行开头。换行和空行的总数没变，不影响运行。
  - 「不断的」应为「不断地」。「DIY」口语化。
- 旁证：同文件的兄弟弹窗「Custom tiles」（context.lua:66-80）也有同样的遗漏和误读，我只作记录。

**entry-03177** `Donate!` → `捐赠！`：**未发现问题**（Birther.lua:1391/1407）。

**entry-03178**：**未发现问题**。和标题「捐赠者特权」一致，「捐赠者」符合术语 Donator。

## CharacterSheet.lua

**entry-03179**：**存在问题**（理解偏差，低影响）
- 问题：原文 `Displaying %s set for %s` 里的 `for %s` 表示「某角色的」。译文 `展示 %s 套装给 %s 看` 把它理解成展示给该角色看。
- 依据：CharacterSheet.lua:74 调用 `game.logPlayer(self.actor, "...", self.equip_set, self.actor:getName():capitalize())`，第二个参数是这张角色面板所属角色的名字。这里的实际行为是切换到显示该角色的另一套装备，并没有「给谁看」的动作。
- 运行时路径：LogDisplay.lua:122-125 的 `_M:call` 会执行 `str:tformat(...)`，两个 `%s` 顺序不变。「套装」与邻近的 `[E]quipment: %s set` →「装备[E]：%s 套装」一致。
- 另外有一处不归本条的上游情况：`switch_set` 取的是没有翻译的字面值 `"off"`/`"main"`（第 71 行），所以第一个 `%s` 可能显示成英文。

**entry-03180** `Sort:  %s` → `排序：%s`：**未发现问题**。第 94 行按钮文字用的是双空格版本，这个 key 与第 85 行的单空格 `Sort: %s` 是两个不同的条目。

**entry-03181**：**未发现问题**。漫游者种子显示（第 629 行），标记和占位符都完整。

**entry-03182** `die:%+d` → `死亡底线：%+d`：**未发现问题**。第 646 行 `compare_fields(..., "die_at", _t"die:%+d", ...)`，`compare_fields` 用 `outformat:format(value*mod)` 格式化（第 515 行）。die_at 是生命值低于多少才死亡的阈值，「死亡底线」准确。

**entry-03183**：**仅建议**。第 743-744 行显示的是 `life_regen * bound(healing_factor, 0, 2.5)`，治疗系数可以小于 1，也就是减益。「加成后」暗示一定是增加，可以改成更中性的「计入治疗系数后」。和邻近的「治疗系数」一致。

**entry-03184** `Two-Handed, ` → `双手， `：**仅建议**。第 897-898 行拼成 `(text).." ("..text2..")"`，实际显示类似「武器 (双手， 剑):」。全角逗号后面再加 ASCII 空格，排版略怪。不影响运行时。

**entry-03185** ` (disabled)` → ` （被禁用）`：**未发现问题**。第 954/959 行作为 `Offhand%s` 的参数，在被缴械时显示，前导空格保留了，与邻近的「副手%s」衔接正常。

**entry-03186** `Damage affinities:` → `伤害亲和：`：**未发现问题**。第 1235 行，对应 `damage_affinity`，是通用译法。

## DeathDialog.lua

**entry-03187**：**未发现问题**。对话框标题（第 34 行），`#LIGHT_RED#…#LAST#` 包住的位置正确。

**entry-03188**：**未发现问题**。第 350 行，只在已登录时显示。

## Donation.lua

**entry-03189**：**未发现问题**。捐赠功能列表项（第 44 行）。

**entry-03190** → `改变物品外观（幻化）`：**未发现问题**。「幻化」是通行的外观替换用语。冻结材料里这个功能名没有其他译例可以比对。

**entry-03191**：**仅建议**。`%s` 由 `table.concatNice(donation_features, ", ", _t" and ")` 填充（第 48-55 行），位置保留了。
- 第 4 行「希望得到你的帮助」后面缺句号。
- `the (many) hours … were worth it` 被弱化成「时间充满了快乐」，丢了「值得」和「many」。
- `also` 没译出来。

## GameOptions.lua

**entry-03192** → `设置动画速度（越低越快）`：**未发现问题**。这是 smooth_move 的输入框（第 111 行），控制的是移动动画的平滑程度，不是角色移动速度，译作「动画速度」更准确。

**entry-03193**：**未发现问题**。twitch_move 选项名（第 120 行），标记完整。

**entry-03194**：**仅建议**。中文句子里混用了带空格的半角括号「 (只用于经典HUD)」。语义和第 164-166 行的 `checkGameOption("log_lines")` 一致，与邻近的「经典」一致。

**entry-03195** → `消失时间（秒数）`：**未发现问题**。log_fade 的输入框（第 221 行），与邻近的「日志消失时间」一致。术语表里的 Fade「消隐」是技能名，这里不适用。

**entry-03196**：**仅建议**。
- 列表项省掉了「tactical」，例如「生命值条+小框架」。不过它与同文件状态标签 `Combined Small`→「生命值条+小框架」（context.lua:499-500）一致，可以接受。
- 末句漏了「also」和句号。
- 标记 `#{italic}#…#{normal}##WHITE#` 完整。

**entry-03197**：**未发现问题**。

**entry-03198** `From 0(disable) to 10`：**未发现问题**。锐化强度滑块（第 466 行），0 代表关闭。

**entry-03199**：**未发现问题**。scroll_dist 的说明（第 483 行），补出「人物」符合语义。

**entry-03200**：**未发现问题**。第 499-501 行 `util.bound(qty, 1, 100)`，100 代表 disabled（第 496 行）。

**entry-03201**：**仅建议**。
- `show your current character on your currently playing profile` 被扩写成「让你的朋友…看见」，属于解释性增补。
- 第二行用了半角逗号加空格「Discord, 那么」。
- `in either state` 的意思已经被「无效」覆盖。

**entry-03202**：**仅建议**。漏了 `on the online vault`（在线角色库），只保留了「te4.org」。「sad deaths」译作「悲壮之死」语气稍有偏移。

**entry-03203**：**存在问题**（换行／段落结构）
- 问题：机械比对显示，原文空行在第 11 行和第 14 行（以 0 为起点）。前者把 bullet 列表和 `Note that…` 段分开，后者在 `#{bold}##CRIMSON#` 警告段之前。译文空行在第 13、14 行：列表与「注意这个设置…」之间没有空行，警告段前却有两个连续空行。换行总数相同，所以是空行被挪了位置，原文的段落分隔丢了，又多出一个空段。这是第 664 行 Textzone 实际显示的版式，不会破坏运行时。
- 附带（仅建议级）：
  - `Version checks: Addons will not be checked for new versions.` 被译成「插件版本更新：无法更新插件的版本」，把「不检查新版本」说成了「无法更新」，与上一条「仍可手动安装」有点矛盾。
  - 首行漏了句号。
  - `it will still do so` 被意译成「仍然会连接网络」，可以接受。
- 所有 `#{bold}#`、`#{normal}#`、`#CRIMSON#` 标记完整。

**entry-03204**：**未发现问题**（第 724 行）。

## GraphicMode.lua

**entry-03205** → `使用纸娃娃（在玩家身上显示装备）`：**未发现问题**。第 83 行复选框，「纸娃娃」是通行的游戏用语。

**entry-03206**：**未发现问题**（第 84 行）。

## LevelupDialog.lua

**entry-03207**：**未发现问题**。第 89 行，两个 `%s` 顺序对应 `actor:getName(), actor.level`。

**entry-03208**：**未发现问题**。第 266 行，对应「本等级上限」这个分支，与第 270 行的「Stat is at the maximum」是分开的两个条目。

**entry-03209**：**未发现问题**。第 625-629 行 `_t[[` 后紧跟的换行按 Lua 长字符串规则会被丢掉，所以与条目原文一致。4 个 `%d` 和 `#00FF00#…#LAST#` 一一对应。「技能树解锁点」与邻近的「技能树解锁点：%s」「技能树解锁点不足」（context.lua:740/805）一致。

**entry-03210**：**仅建议**（原文本身已与实现不符，译文把说法加强了）
- 核验一：Actor.lua 升级逻辑第 3959-3961 行确认在 10、20、34 级各加 1 个 `unused_talents_types`。
- 核验二：刻印位上限是 5 个。ActorInscriptions.lua:30-31 的 `max_inscriptions` 默认为 3，加上 player-inscription.lua:42 限制的 `inscriptions_slots_added < 2`，一共 5 个。
- 不符之处：刻印位满了再使用刻印时，player-inscription.lua:42-46 只是在对话里多出一个选项「Buy a new slot with one talent category point」，玩家选了才会扣点（第 44 行）。并不会自动扣点。英文 `learning it is automatic` 已经不够准确，译文 `你使用刻印时会自动消耗点数解锁` 又明确说成自动扣点，与实现更矛盾。可以考虑写成「使用刻印时会提示是否用点数解锁」。
- 其余内容准确。

**entry-03211** `Stats: %s` → `属性：%s`：**未发现问题**。第 773/1077 行。

---

## 实际读取的路径与版本

**冻结材料**
- 读了本实验目录下的 `INPUT.md`、`entries.json`（全文）、`source-access.json`。
- `context.lua` 只按关键词查看了相关片段：行 1-5、45-46、65-85、98-118、187-188、209-211、241-242、284-285、313-322、347-359、364、401-402、424-432、454-455、498-504、534-536、740-835 附近。
- `sources/game/modules/tome/dialogs/` 下 7 个文件：Birther、CharacterSheet、DeathDialog、Donation、GameOptions、GraphicMode、LevelupDialog。sha256 都与 source-access.json 一致。

**固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下用 `git show` 读取的上游文件**
- `game/modules/tome/class/Actor.lua`：按 `inscriptions_slots_added|unused_talents_types` 过滤，并读了行 3950-3966。
- `game/modules/tome/class/interface/ActorInscriptions.lua`：过滤后读了行 55-120。
- `game/modules/tome/data/chats/player-inscription.lua`：过滤。
- `game/modules/tome/data/general/objects/scrolls.lua`：过滤，无命中。
- `game/modules/tome/class/Game.lua`：过滤 `logPlayer`、继承声明。
- `game/engines/default/engine/Game.lua`、`GameTurnBased.lua`、`GameEnergyBased.lua`：过滤 `logPlayer`。
- `game/engines/default/engine/LogDisplay.lua`：`_M:call`。
- 两次尝试读取不存在的路径，都失败了：`engine/interface/ActorInscriptions.lua`、`engine/interface/GameMessages.lua`。

**需要如实说明的超出读取范围的操作**
- 我在固定 commit 下对 3 个目录执行了 `git ls-tree --name-only`（`game/modules/tome/class/interface/`、`game/engines/default/engine/interface/`、`game/modules/tome/data/general/objects/`）用来定位文件名。这些是目录列举，没有读取文件内容，也没有执行 `git grep`。
- `game.logPlayer` 在运行时如何绑定到 LogDisplay，我没有沿 uiset 继续追下去。03179 的「tformat 翻译路径」依据的是 LogDisplay:call 的实现，这一环属于部分核验，但不影响该条的语义结论。

我没有读取实验目录里的其他文件、其他模型的输出、历史 findings、STATE 或当前翻译文件，也没有写文件或创建子 agent。