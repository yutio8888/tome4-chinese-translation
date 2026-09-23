我按 INPUT.md 审完了 40 条：6 条存在问题，6 条仅建议，28 条未发现问题，没有待确认。越界情况见文末第三节。

## 一、逐条判定表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03172 | 未发现问题 | 按钮文本，对应 Birther.lua:93，译文准确 |
| entry-03173 | 未发现问题 | 教程对话框按钮（Birther.lua:423-424），语义准确 |
| entry-03174 | 存在问题 | C1 |
| entry-03175 | 未发现问题 | 忠实；标记与尾换行已保留 |
| entry-03176 | 存在问题 | C2、C3、C4、C5；S1 |
| entry-03177 | 未发现问题 | 按钮文本 |
| entry-03178 | 未发现问题 | "捐赠者"符合术语快照 Donator |
| entry-03179 | 存在问题 | C6 |
| entry-03180 | 未发现问题 | 按钮文本，%s 已保留 |
| entry-03181 | 未发现问题 | 颜色标记和 %s 已保留 |
| entry-03182 | 未发现问题 | die_at 是死亡阈值，译"死亡底线"贴合；%+d 已保留 |
| entry-03183 | 仅建议 | S2 |
| entry-03184 | 未发现问题 | 后面拼接武器类型（CharacterSheet.lua:897），尾部空格已保留 |
| entry-03185 | 未发现问题 | 缴械时追加在"副手"后（CharacterSheet.lua:954/959），前导空格已保留 |
| entry-03186 | 未发现问题 | 与 context 中的"伤害亲和"一致 |
| entry-03187 | 未发现问题 | 标记已保留 |
| entry-03188 | 未发现问题 | DeathDialog.lua:350，已登录时显示的选项 |
| entry-03189 | 未发现问题 | 用作捐赠功能列表项（Donation.lua:44） |
| entry-03190 | 未发现问题 | 同上 |
| entry-03191 | 仅建议 | S3 |
| entry-03192 | 仅建议 | S4 |
| entry-03193 | 未发现问题 | 与描述"做出小幅颠动"（GameOptions.lua:119）相符 |
| entry-03194 | 未发现问题 | 语义准确 |
| entry-03195 | 未发现问题 | 日志淡出秒数输入框（GameOptions.lua:221） |
| entry-03196 | 仅建议 | S5 |
| entry-03197 | 仅建议 | S6 |
| entry-03198 | 未发现问题 | 锐化滑条 0–10（GameOptions.lua:466） |
| entry-03199 | 未发现问题 | 语义准确 |
| entry-03200 | 未发现问题 | 生命损失警告，100 为禁用（GameOptions.lua:499-501） |
| entry-03201 | 仅建议 | S7 |
| entry-03202 | 未发现问题 | 语义准确 |
| entry-03203 | 存在问题 | C7；S8 |
| entry-03204 | 未发现问题 | 语义准确 |
| entry-03205 | 未发现问题 | "纸娃娃"是通行说法，括注忠实 |
| entry-03206 | 未发现问题 | 语义准确 |
| entry-03207 | 未发现问题 | 两个 %s 顺序为名字、等级（LevelupDialog.lua:89） |
| entry-03208 | 未发现问题 | 触发条件为 stat >= level*1.4+20（LevelupDialog.lua:265-266），"当前等级上限"准确 |
| entry-03209 | 未发现问题 | 四个 %d 和颜色标记按序保留；"技能树解锁点"与 context 一致 |
| entry-03210 | 存在问题 | C8、C9、C10 |
| entry-03211 | 未发现问题 | 按钮显示未分配属性点（LevelupDialog.lua:773） |

## 二、claim 明细

**C1（entry-03174）｜已证实｜翻译新增**
- 原文说完成某些操作和任务会让**被锁定的**战役、种族和职业永久可用。
- 译文是"本选项被锁定……可以永久解锁**这个**战役，种族，职业"，把泛指说成了当前选项本身，并且把它归成战役、种族或职业。
- 源码：同一个 locktext 还用在 `generateDifficulties`（Birther.lua:826/838）和 `generatePermadeaths`（Birther.lua:858/870）。所以在锁定的难度或死亡模式选项下，玩家会看到"解锁这个战役，种族，职业"。这是作用对象错误。
- "Performing certain actions" 译成"条件"属于意译，不单独计。

**C2（entry-03176）｜已证实｜翻译新增**
- 原文 "While this is a **free** game that I am doing for fun"。
- 译文"尽管这只是我自娱自乐所做的一款游戏"丢了"免费"。这句的让步逻辑正是建立在"免费"上，属于事实信息丢失。
- 语境：Birther.lua:1384，在捐赠请求段落里。

**C3（entry-03176）｜已证实｜翻译新增**
- 原文 "I certainly will not complain as real life can be harsh sometimes"：不抱怨的对象是"游戏帮忙养家"，"现实艰难"是原因。
- 译文"我就谢天谢地，不会再抱怨现实的诸多压力了"把原因当成了不抱怨的对象，语义关系改变。

**C4（entry-03176）｜已证实｜翻译新增**
- 原文 "only that you can try as much as you want **without restarting**"。
- 译文"仅仅意味着你可以有着无限多的尝试次数"丢了"不必重开"。这正是无限生命与普通重开的区别，属于条件信息丢失。

**C5（entry-03176）｜已证实｜翻译新增**
- 原文 "I realize this can not please everybody"：从上下文看，"this"指上一句"从死亡中学习"的设计，下半句正是为此开放探索模式。
- 译文"我觉得这款游戏可能不会被所有人接受"把指代换成了整款游戏。

**S1（entry-03176）｜仅建议**
- "get better by learning" 的"变强"、"if they wish"、"find this game good"的措辞有轻微弱化，主旨未丢。
- "It will help ensure its survival." 被移到下一行开头，属于合法排版重排。
- 附注：探索模式弹窗里提到"tile selector"，是上游从 Custom tiles 弹窗（Birther.lua:1398-1402）复制来的原文，译文照译。该句陈述本身不构成机制误述，不计入缺陷。

**C6（entry-03179）｜已证实｜翻译新增**
- 原文 "Displaying %s set for %s"：第二个 %s 是 `self.actor:getName()`，意思是"正在显示该角色的某组装备"。
- 译文"展示 %s 套装给 %s 看"把所属关系变成了"展示给某人看"。
- 源码：CharacterSheet.lua:69-74。这是切换装备页时只切换显示的日志，第一个参数为 main/off。
- "套装"一词沿用 context 中 "[E]quipment: %s set" 的既有译法，不另计。

**S2（entry-03183）｜仅建议**
- 数值是 `life_regen * bound(healing_factor, 0, 2.5)`（CharacterSheet.lua:743）。系数可能小于 1，"加成后"略偏正向。
- 但"加成"在游戏语境里常泛指修正，不构成数值误述。

**S3（entry-03191）｜仅建议**
- "the (many) hours … were worth it" 意译成"时间充满了快乐"，第三段末尾缺句号。
- 劝捐的语用功能等价；%s 由 `table.concatNice` 填充（Donation.lua:54），格式正确。

**S4（entry-03192）｜仅建议**
- 该值是 smooth_move 的动画量，描述写明越高越慢（GameOptions.lua:107-111）。
- "动画速度（越低越快）"与英文同样有字面悖论，括注已消歧，属于沿袭上游的表达。

**S5（entry-03196）｜仅建议**
- "small/big tactical frame" 译成"小框架/大框架"，省去了"战术"。有标题"切换战术信息显示模式"兜底，信息结构未丢。
- 格式标记 #{italic}#、#{normal}#、#WHITE# 已保留。
- 快捷键 shift+T 为照译，未追查按键绑定，不构成疑点。

**S6（entry-03197）｜仅建议**
- "pressing two directions" 译成"同时按两个键"，泛化成"两个键"。"两个方向键"更贴切，但原意可推，不构成错误。

**S7（entry-03201）｜仅建议**
- "show … on your currently playing profile" 意译为"让你的朋友在Discord上看见"，受众表述有变化但功能一致。
- "doesn't do anything in either state" 简化成"无效"，等价。

**C7（entry-03203）｜已证实｜翻译新增**
- 原文 "Version checks: Addons will not be checked for new versions."。
- 译文"插件版本更新：无法更新插件的版本。"把"不检查新版本"改成了"无法更新"。同一段已说明插件"仍可手动安装"，所以"无法更新"与原意不符，混淆了检查与更新。纯语义判断。

**S8（entry-03203）｜仅建议**
- "info about new updates to the game" 译成"新闻"，稍泛化，但标题"游戏内新闻"一致。
- 列表后少一个空行、结尾警示段前多一个空行，属于排版差异，未造成信息结构丢失。

**C8（entry-03210）｜已证实｜沿袭上游描述，且译文加重**
- 原文 "learning it is automatic when using an inscription"；译文"你使用刻印时会自动消耗点数解锁"。
- 实际机制：`setInscription` 在没有空位时只是打开 `player-inscription` 对话（ActorInscriptions.lua:67-83）。对话里出现一个可选项 "Buy a new slot with one talent category point"，前提是 `inscriptions_slots_added < 2`、有未用点数、且不是同名替换（player-inscription.lua:42-46）。
- 升级界面的 Inscriptions 按钮（LevelupDialog.lua:678-692）也需要 yes/no 确认。
- 所以点数不会自动消耗。英文的"automatic"已经不准确，译文明确写出"自动消耗点数"，误述加重。
- 上限 5 与机制相符（`max_inscriptions` 默认 3 加 2，ActorInscriptions.lua:30-31）。

**C9（entry-03210）｜已证实｜翻译新增（上游有遗漏）**
- 译文"每点提升 0.2"暗示同一技能树可以反复投点累加。
- 源码：`learnType`（LevelupDialog.lua:436-438）规定已知技能树只能提升一次（"You can only improve a category mastery once!"），每次 +0.2（LevelupDialog.lua:453）。
- 英文没写一次上限，但也没有按点累加的暗示；"每点"措辞会误导玩家。

**C10（entry-03210）｜已证实｜沿袭上游描述**
- 原文/译文"在 10、20 和 34 级获得点数"。
- 实际（Actor.lua:3959-3961）：在 10、20、34 级获得，50 级以后每逢 (level-4)%30==0（64、94……）也会获得。
- 译文忠实复制了英文的遗漏，面向玩家的描述不完整，属上游问题。

## 三、读取范围与越界说明

**读取的冻结材料：**
- protocol-v2/ 下的 INPUT.md、source-access.json、entries.json（用脚本核对了 40 条 audit_id、source、target 与 INPUT 一致，0 处不符）、context.lua（按关键词检索）。
- sources/game/modules/tome/dialogs/ 下七份冻结源码。

**固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 下的 git show：**
- 上述七份 dialogs 源码：只用于 sha256 比对，七份全部一致。
- `game/modules/tome/class/Actor.lua`
  - 引入依据：LevelupDialog.lua:680-687 使用 actor 对象的 `inscriptions_slots_added`、`max_inscriptions`、`unused_talents_types` 字段，需要查它们的定义。
  - 注意：这是由符号/字段引入，不是 LevelupDialog 的直接 require，属于边界上较弱的引入理由。
  - 用到的是第 37 行 require 与 3959-3961 行。
- `game/modules/tome/class/interface/ActorInscriptions.lua`：由 Actor.lua:37 的 require 引入。
- `game/modules/tome/data/chats/player-inscription.lua`：由 ActorInscriptions.lua:81 的 `Chat.new("player-inscription", …)` 引入。

**越界如实报告：**
- 读取 Actor.lua 时，我把 git show 输出临时写到了 `/tmp/ro_actor_624a.lua`，检索后已删除。这违反了"不写文件"的约束。仓库内没有任何写入。
- 没有读当前翻译文件、当前源码工作树、其他 commit、同目录其他文件、历史报告或其他模型输出；没有整目录搜索；没有创建子 agent。

**核验边界：** 没有无法核验的项目。shift+T 按键绑定、Discord 与网络功能的实现未追查，因为相关判定不依赖它们。

以上是审核观察，不是真值，不宣称 DONE_VERIFIED。
