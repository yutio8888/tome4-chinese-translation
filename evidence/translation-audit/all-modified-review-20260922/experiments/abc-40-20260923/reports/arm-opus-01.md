# 40 条三模型对比试验：独立复核报告（REVIEWER，只读）

40 条逐条复核完毕：**存在问题 3 条，仅建议 11 条，未发现问题 26 条，待确认 0 条**。

七个冻结源文件的 sha256 与 `source-access.json` 一致。40 条的原文与译文都在对应源码行找到了逐字对应。占位符（`%s`、`%d`、`%+d`）、颜色和样式标记、换行总数，40 条全部保持一致。唯一的换行结构偏差在 entry-03203。

## 逐条结论

### Birther.lua

**entry-03172 · 未发现问题**
按钮 `_t"Random!"`（Birther.lua:93）译为「随机！」，准确。

**entry-03173 · 未发现问题**
按钮位于 `Dialog.new(_t"Tutorials")` 对话框内（:423-424），译文加「教程」二字与语境吻合。

**entry-03174 · 仅建议**
- 原文 "Performing certain actions **and** completing certain quests" 译为「完成特定的任务**或**条件」，"actions" 被换成了「条件」，连接词也从「和」变成了「或」。意思大体保留。
- 「这个战役，种族，职业」：这段文字是五处锁定选项共用的（:804/826/858/890/944），「这个」读起来有点别扭。并列项宜用顿号。
- 开头两个 `\n`、`#GOLD#` 都已保留。

**entry-03175 · 仅建议**
"does not make much sense lore-wise" 被译成绝对的「不符合剧情」，丢了 "much" 的缓和语气。只在 `how == "nolore"` 时显示（:966-967），机制上没有影响。`#CRIMSON#`、`#WHITE#` 和末尾 `\n` 都已保留。

**entry-03176 · 存在问题**
- **claim 1（错译）**：原文 "if it can help feed my family a bit I certainly will not complain as real life can be harsh sometimes"，意思是「如果能贴补点家用，我当然不会拒绝，毕竟生活有时很艰难」。译文「我就谢天谢地，不会再抱怨现实的诸多压力了」把「不会抱怨」的对象从收到捐款改成了现实压力，语义被扭曲。证据：Birther.lua:1384。
- 次要：原文第 5 行末的 "It will help ensure its survival." 被挪到下一行开头。换行总数不变，属于无损重排，不算缺陷。
- 术语「马基·埃亚尔」「捐赠者」符合 preferred 规范。

**entry-03177 · 未发现问题**
yesnoLongPopup 的按钮（:1391/1407），译为「捐赠！」。

**entry-03178 · 未发现问题**
"Cosmetic customization is a donator-only feature."（:1730）译为「自定义外观是捐赠者的特权。」，意思完整，「捐赠者」符合术语。

### CharacterSheet.lua

**entry-03179 · 存在问题**
- **claim 1（错译）**：原文 "Displaying %s set for %s"，第二个 `%s` 是 `self.actor:getName():capitalize()`（CharacterSheet.lua:74），意思是「正在显示〈角色〉的〈main/off〉装备组」。译文「展示 %s 套装给 %s 看」把它理解成「展示给某人看」，所属关系译错。
- 运行时链路已核实：`game.logPlayer` → `game.log` → `LogDisplay:call` → `str:tformat(...)`（uiset/Minimalist.lua:492/503、engine/LogDisplay.lua:122-125），所以这条译文确实会生效。两个 `%s` 顺序未变，`#RED#` 已保留。
- 旁注（不在本条范围）：第一个参数 `switch_set` 是未翻译的 "main"/"off" 原始字符串（:71），运行时会显示英文。
- 「套装」与同对话框 `[E]quipment: %s set` →「%s 套装」（context.lua:117）一致，不另计问题。

**entry-03180 · 未发现问题**
原文 "Sort:  %s" 带双空格（:94），译为「排序：%s」，与 context.lua:119 的单空格变体译法一致。

**entry-03181 · 未发现问题**
流浪者种子行（:629），颜色标记和 `%s` 均保留。

**entry-03182 · 未发现问题**
`compare_fields(..., "die_at", _t"die:%+d", ...)`（:646）显示的是 die_at 死亡阈值。「死亡底线：%+d」能表达意思，`%+d` 已保留。

**entry-03183 · 仅建议**
取值是 `life_regen * bound(healing_factor, 0, 2.5)`（:743-744）。healing_factor 可能小于 1，这时是削减而不是「加成」。建议改为「计入治疗系数后」一类的中性说法。格式无误。

**entry-03184 · 仅建议**
拼接结果是 `" ("..text2..")"`（:897-898），会显示成「(双手， 剑)」：全角逗号后面还多一个半角空格，视觉上会空得偏宽。只是排版问题，没有语义缺陷。

**entry-03185 · 仅建议**
缴械时追加在 "#LIGHT_BLUE#Offhand%s" 后面（:954/959），显示成「副手 （被禁用）」：半角空格加全角括号。只是排版问题。

**entry-03186 · 未发现问题**
「伤害亲和」与同 section 冻结邻近译文（context.lua:284）一致。

### DeathDialog.lua

**entry-03187 · 未发现问题**
对话框标题（DeathDialog.lua:34），`#LIGHT_RED#…#LAST#` 已保留。

**entry-03188 · 未发现问题**
只在 `profile.auth` 存在时显示（:350）。与 "Message Log" →「消息日志」（context.lua:324）对仗。

### Donation.lua

**entry-03189 · 未发现问题**
捐赠特性列表项（Donation.lua:44）。「无限命」偏口语，可以接受，标记已保留。

**entry-03190 · 未发现问题**
同一列表（:44），「幻化」是 Shimmering 的常见译法，标记已保留。

**entry-03191 · 仅建议**
- "If you feel that the (many) hours you have spent having fun were worth it" 译为「如果你觉得在游戏中体验的时间充满了快乐」：丢了 "(many)"，"worth it" 被改写成「充满了快乐」。捐赠呼吁的意图保留了。
- 第 4 行「希望得到你的帮助」后缺句末标点。
- `%s` 由 `table.concatNice(donation_features, ", ", _t" and ")` 填入（:54），译文保留了一个 `%s`，运行时正确。

### GameOptions.lua

**entry-03192 · 仅建议**
这个设置是 `smooth_move`（GameOptions.lua:107-116），实际控制生物和投射物的移动动画时长。「设置动画速度」大体对，但丢了 "movement"。建议「移动动画速度」。

**entry-03193 · 未发现问题**
说明文字是 "creatures will do small bumps when moving and attacking"（:119）。「抖动效果」贴合，标记完整。

**entry-03194 · 未发现问题**
（:166）意思完整。中文里夹半角括号，只是风格问题。

**entry-03195 · 未发现问题**
`log_fade` 输入框标题（:221）。术语表里 "Fade → 消隐" 是技能名，不适用于这里。与「日志消失时间」（context.lua:454）一致。

**entry-03196 · 仅建议**
- "small/big tactical frame" 译为「小框架/大框架」，丢了「战术」；"No tactical information at all" 缩成「不显示」。结合标题「战术视图」仍能看懂。
- 斜体句末丢了句号。
- 换行和 `#{italic}#…#{normal}##WHITE#` 标记与原文等价（:336-342）。

**entry-03197 · 未发现问题**
（:452）意思完整，`#WHITE#` 已保留。

**entry-03198 · 未发现问题**
Sharpen 滑块 0–10，0 为关闭（:466-467），译文准确。

**entry-03199 · 未发现问题**
（:483）意思准确，`#WHITE#` 已保留。

**entry-03200 · 未发现问题**
Life Lost Warning：`bound(qty,1,100)`，100 表示 disabled（:496-503），译文与机制一致。

**entry-03201 · 仅建议**
- "show your current character on your currently playing profile on Discord" 被意译成「让你的朋友…看见」，加了「朋友」。
- "doesn't do anything in either state" 译为「这个选项就是无效的」，可以接受。
- 中文里用了半角逗号「Discord, 」。换行和 `#ANTIQUE_WHITE#` 都已保留（:634）。

**entry-03202 · 仅建议**
"on the online vault at te4.org" 译为「在te4.org上」，省掉了「在线角色库」。同组标题用的是「在线角色库」（context.lua:599）。其余意思完整，`\n` 和 `#WHITE#` 已保留（:643）。

**entry-03203 · 存在问题**
- **claim 1（换行结构）**：原文 "…new updates to the game.\n\nNote that…" 有一个空行，把 "Note" 段和列表分开。"…update the game.\n\n#{bold}##CRIMSON#" 前也是一个空行。译文里 "Note" 段前的空行没了，直接贴在列表后面；警告段前却变成两个空行。空行位置从原文第 11/14 行变成了第 13/14 行，换行总数不变，但段落结构变了，不属于无损排版（:664 起的 Textzone）。
- **claim 2（仅建议级）**：
  - "Version checks: Addons will not be checked for new versions" 译为「插件版本更新：无法更新插件的版本」，把「不检查新版本」说成了「无法更新」，但手动更新仍然可以。
  - "info about new updates to the game" 缩成「新闻」。
  - "fun and acclaimed features" 改写成「好用的功能和一些游戏体验」。
- 占位和样式标记 `#{bold}#` 等的顺序完整。

**entry-03204 · 未发现问题**
（:724）意思准确，`#WHITE#` 已保留。

### GraphicMode.lua

**entry-03205 · 未发现问题**
复选框（GraphicMode.lua:83），「纸娃娃」是约定俗成的译法。

**entry-03206 · 未发现问题**
（:84）「渐变，大型贴图，……」可以接受。

### LevelupDialog.lua

**entry-03207 · 未发现问题**
`("Levelup: %s, level %s"):tformat(actor:getName(), actor.level)`（LevelupDialog.lua:89），参数顺序一致。

**entry-03208 · 未发现问题**
（:266）与相邻的「该属性已达到上限」（context.lua:721）对仗。

**entry-03209 · 未发现问题**
四行、四个 `#00FF00#%d#LAST#` 都完整（:625-629）。「技能树解锁点」与同 section 的用法（context.lua:740/805）一致。

**entry-03210 · 未发现问题**
- 各项意思完整（:650-656）。
- 「最多 5 个」有源码支撑：`inscriptions_slots_added < 2`，基础是 3（ActorInscriptions.lua:30-31）。
- 「使用刻印时会自动消耗点数解锁」：实现上是在刻印栏满时弹出对话，由玩家选择 "Buy a new slot with one talent category point"（data/chats/player-inscription.lua:42-47），并不是完全自动。但原文本身就写的是 "automatic"，译文忠实于原文，不算译文缺陷。

**entry-03211 · 未发现问题**
按钮显示 `unused_stats`（:773/1077），「属性：%s」准确。

## 实际读取的路径与版本

- 实验目录：`INPUT.md`、`entries.json`、`source-access.json`。`context.lua` 只按关键词 grep 读取了相关行。
- 冻结源码：`sources/game/modules/tome/dialogs/{Birther,CharacterSheet,DeathDialog,Donation,GameOptions,GraphicMode,LevelupDialog}.lua`，sha256 已校验。
- 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，用 `git -C /workspace/t-engine4 show` 读取了：
  - `game/engines/default/engine/LogDisplay.lua`
  - `game/modules/tome/class/uiset/Minimalist.lua`
  - `game/modules/tome/class/interface/ActorInscriptions.lua`
  - `game/modules/tome/data/chats/player-inscription.lua`
- 需要说明的越界：为了找到 `logPlayer` 和 `max_inscriptions` 的定义，我在固定 commit 上对 `game/` 目录跑了 `git grep`。命中涉及 engine/Game.lua、tome/class/Game.lua、uiset/Classic.lua、boot/example 的 Game.lua、GameState.lua、races.lua、advanced-golemancy.lua，这些文件只看了 grep 命中行，没有打开整个文件。这次搜索超出了 INPUT 限定的「沿调用链读取」和「不得全仓搜索」，结论本身不依赖这些额外命中。

没有读取当前工作树源码、翻译文件、其他报告或其他模型的输出，没有写文件，没有创建子 agent。本报告是自然语言旁路审核，不输出生产 contract JSON，也不声称 DONE_VERIFIED。