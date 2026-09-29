# entry-03453–entry-03492 复核报告（REVIEWER，translation_contextual_v1，自然语言实验旁路）

40 条都已独立复核：14 条存在问题，4 条待确认，11 条仅建议，11 条未发现问题。所有观察只凭冻结输入和其中列明的 DLC 快照源码得出，不是真值，也不宣称 DONE_VERIFIED。

DLC 来源说明：两个 DLC（Ashes of Urh'Rok 和 Cults）的源码仓库和 commit 都没有固定（unpinned）。所用快照是 source-access.json 列明的 21 个文件，sha256 已全部核对一致。凡依赖机制的结论只在快照内成立，目标版本是否适用仍待确认。本次没有读引擎 commit 下的任何文件。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03453 | 未发现问题 | 与 timed_effects.lua:1054 logPlayer 的 %s 对应；颜色标记保留 |
| entry-03454 | 仅建议 | C01 |
| entry-03455 | 存在问题 | C02–C09 存在问题；C10 建议 |
| entry-03456 | 存在问题 | C11、C12 存在问题；C13 建议 |
| entry-03457 | 待确认 | C14 |
| entry-03458 | 存在问题 | C15、C16 存在问题；C17 待确认；C18 建议 |
| entry-03459 | 未发现问题 | 标记保留；Doomelf＝魔化精灵，与术语一致 |
| entry-03460 | 存在问题 | C19、C20、C21 存在问题；C22、C23 待确认 |
| entry-03461 | 未发现问题 | DemonologistsDLC.lua:57 compare_fields 标签；尾随空格保留 |
| entry-03462 | 未发现问题 | 成就描述 all.lua:46；中文用条件式表述可以接受 |
| entry-03463 | 未发现问题 | 与 demented.lua:82 数值一致 |
| entry-03464 | 仅建议 | C24 |
| entry-03465 | 未发现问题 | 与 demented.lua:84/122 一致（life_rating=3） |
| entry-03466 | 未发现问题 | 与 demented.lua:137/175 一致（life_rating=-4） |
| entry-03467 | 未发现问题 | 与 drem.lua:32/37 的 inc_stats 一致 |
| entry-03468 | 仅建议 | C25 |
| entry-03469 | 未发现问题 | drem.lua:34/51 life_rating=12 |
| entry-03470 | 未发现问题 | drem.lua:35/56 experience=1.12 |
| entry-03471 | 未发现问题 | 与 krog.lua:32/38 一致 |
| entry-03472 | 仅建议 | C26 |
| entry-03473 | 未发现问题 | krog.lua:34/55 life_rating=13 |
| entry-03474 | 未发现问题 | krog.lua:35/63 experience=1.15 |
| entry-03475 | 仅建议 | C27 |
| entry-03476 | 仅建议 | C28 |
| entry-03477 | 仅建议 | C29 |
| entry-03478 | 未发现问题 | digestive-sack.lua:108，物品掉出 |
| entry-03479 | 存在问题 | C30 |
| entry-03480 | 未发现问题 | digestive-sack.lua:139，开袋时 30% 概率触发疾病 |
| entry-03481 | 未发现问题 | space-dwarf-ship.lua:63，已搜刮后的弹窗 |
| entry-03482 | 未发现问题 | fonts.lua:58-59 unused_prodigies+1；%s＝self:getName() |
| entry-03483 | 未发现问题 | fonts.lua:61-62 unused_talents_types+1 |
| entry-03484 | 未发现问题 | fonts.lua:64-65 unused_talents+1 |
| entry-03485 | 未发现问题 | fonts.lua:67-68 unused_generics+1 |
| entry-03486 | 未发现问题 | fonts.lua:70-71 unused_stats+3 |
| entry-03487 | 未发现问题 | fortress-multiverse.lua:41，条件不满足时的 bignews 提示 |
| entry-03488 | 仅建议 | C32 |
| entry-03489 | 仅建议 | C33 |
| entry-03490 | 仅建议 | C34 |
| entry-03491 | 待确认 | C31 |
| entry-03492 | 未发现问题 | blobs.lua:67，mastocytic feeder 描述 |

---

### C01 | entry-03454 | 仅建议
- 原文 "A demon with 3 arms … For experiment. Not for fun. Nope."，译文「长着三只手……不是娱乐，而是实验。」
- 句末调侃的 "Nope." 被略去，「三只手」在中文里有「扒手」的俗义。
- 事实（三条手臂、要切割你、目的是实验）都保留了，只是语气和措辞偏好，所以不计缺陷。
- 来源：searing-halls/npcs.lua:73，mutilator 的 desc。

### C02 | entry-03455 | 存在问题（术语）
- "Many in Maj'Eyal" 译成「在马基埃亚尔」。
- 术语快照中 Maj'Eyal 为 preferred「马基·埃亚尔」，notes 写明维护者已于 2026-08-25 裁定，「马基埃亚尔」已被取代。
- 这是专名，不受 source_tag 差异影响，属于明确适用的术语要求。
- 来源：init.lua:28。

### C03 | entry-03455 | 存在问题（同一专名两译）
- 第一段 "Their Fearscape" 译成「恐惧空间」；Features 第 3 项 "the plains of the Fearscape" 译成「恶魔空间的平原」。
- 同一个专名在同一条目里用了两个名字，读者会以为是两个不同地点，所指的同一性丢失。
- 至于应该统一成哪个名字，属于术语策略：快照中 fearscape＝恶魔空间 只是 existing，context.lua:12 另有「恐惧空间」。这里不就此下结论，只判定条目内部不一致。
- 来源：init.lua:28、33。

### C04 | entry-03455 | 存在问题（语义改写）
- "crack under their scrutiny" 译成「在他们的破坏下开始破碎」。
- scrutiny 是「审视、窥探」，被改写成主动「破坏」，原文措辞的信息改变了。
- 来源：init.lua:28。

### C05 | entry-03455 | 存在问题（遗漏）
- Doombringer 一项的 "feeding on the flames and suffering of their surroundings **to stay alive** while quickly reducing **any group** …" 译成「随后吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬」。
- 吸收火焰与痛苦是「为了维持生存」，这一目的被删，玩法定位信息丢失；"any group" 也缩成了「任何敌人」。
- 属于文本层面可直接证明的遗漏，没有追具体技能机制。
- 来源：init.lua:31。

### C06 | entry-03455 | 存在问题（机制表述偏差）
- "Demons have persistent health, making them a little more precious than disposable … skeletons or summoner beasts" 译成「恶魔具有更持久的生命值，比死灵法师易碎的骷髅……更加珍贵」。
- persistent health 是「生命值会保留、不会重置」，被改成了比较级「更持久」，读起来像是恶魔血更厚或更耐打。
- disposable（用完即弃）译成「易碎」，原句「可保留 vs 一次性」的对比逻辑随之丢失。
- 文本层面可证。恶魔血量保留的实际实现不在本次允许读取的调用链上，具体机制未核验。
- 来源：init.lua:32。

### C07 | entry-03455 | 存在问题（删限定）
- "Shalore who've taken to the demonic alterations **especially well**" 译成「那些被恶魔的力量所改变的永恒精灵」。
- 删掉「适应得尤为好」后，范围从「改造中表现特别好的一部分永恒精灵」扩大成了「所有被改变的永恒精灵」。
- 来源：init.lua:35。

### C08 | entry-03455 | 存在问题（语义）
- "assault your enemies' minds to leave them unsteady in combat" 译成「攻击敌人的精神，使他们难以为继」。
- unsteady 是「站不稳、失衡」，「难以为继」是「无法持续下去」，效果描述的含义改变了。
- 来源：init.lua:35。

### C09 | entry-03455 | 存在问题（所属关系颠倒）
- "Conquer the worst **Urh'Rok's forces** can throw at you" 译成「战胜乌鲁洛克最强大的敌人」。
- 原意是乌鲁洛克的部队派来对付你的最强者；中文「乌鲁洛克最强大的敌人」会读成「与乌鲁洛克为敌的人」，所属关系反了。
- 另外 "metaphorical skulls" 的 metaphorical 被删，译文成了字面上「悬挂头骨」。
- 来源：init.lua:40。

### C10 | entry-03455 | 仅建议
- "a squad of Fire Imps" 译成泛称「火焰恶魔」，也没译出 "a squad"。快照里没有 Fire Imp 的术语，无法认定为术语违例。
- "always wanted" 译成「会想要」，时态有偏移，但不影响信息。
- 牛头人先用「它」后用「他」，代词不一致。
- 以上都属措辞或一致性偏好。

### C11 | entry-03456 | 存在问题（时序与状态改写）
- "As you recover, and your platform of searing earth splits from the main continent" 译成「当你醒来后，你发现你身处一处和主大陆分离的焦土」。
- 原文是「你恢复过来时，脚下平台正在从大陆分裂出去」，是正在发生的事件；译文改成了「醒来后发现已经分离」的既成状态。
- recover 译成「醒来」，还额外引入了原文没有的昏迷。
- 来源：intro-ashes-urhrok.lua:28。

### C12 | entry-03456 | 存在问题（遗漏）
- "floating in the void **between worlds**" 译成「漂浮在虚空中的燃烧大陆」。
- 「世界之间」这个方位信息被删。
- 来源：intro-ashes-urhrok.lua:23。

### C13 | entry-03456 | 仅建议
- "cause the most pain" 译成「更大的痛苦」，最高级变成了比较级。
- handler 加引号译作「主人」属于合法的风格处理。

### C14 | entry-03457 | 待确认
- "Corruptor (Demonologist)" 译成「堕落系（恶魔使者）」，而术语快照中 Corruptor＝腐化者（birth descriptor name，existing）。
- existing 不是强制要求。待确认的是：游戏里建角界面实际显示的职业大类名是否为「腐化者」。如果是，这个解锁标题就和界面名不一致。
- 缺少的证据：该职业描述符的实际显示译名。这属于当前翻译文件，按规则不能读取。
- 来源：unlock-corrupter_demonologist.lua:20。

### C15 | entry-03458 | 存在问题（误译）
- "they have **created many dark cults** to spread fear and terror" 译成「并通过黑暗仪式来传播不安与恐慌」。
- cults（邪教组织）被译成「仪式」，「创建了许多」这层信息也丢了。
- 来源：unlock-corrupter_demonologist.lua:22。

### C16 | entry-03458 | 存在问题（遗漏）
- "Corruptors are spellcasters, **ranged** attackers using magic." 译成「堕落系是施法职业，能使用魔法攻击敌人。」
- 「远程」这个定位属性被删。
- 来源：unlock-corrupter_demonologist.lua:27。

### C17 | entry-03458 | 待确认
- 与 C14 相同：Corruptor 译成「堕落系」，与术语「腐化者」不同，同样缺实际 UI 显示名的证据。

### C18 | entry-03458 | 仅建议
- 同一条内先用「堕落系」、后用「堕落者」。
- "Infect" 译成「注射」，「恶魔之种」和「恶魔种子」两种说法混用。
- "to do your binding"（上游原文就把 bidding 打成了 binding）没有译出，但「控制」已表达从属关系。
- 前三行由单换行改成了空行分段，属于合法排版，不影响显示结构。

### C19 | entry-03460 | 存在问题（解锁信息丢失）
- "and thus **have earned the right to make Doomelf characters**" 译成「……#LIGHT_GREEN#魔化精灵#WHITE# 应运而生」。
- 原文告诉玩家的关键信息是「你现在可以创建魔化精灵角色」，译文改成了叙事性的「应运而生」，玩家读不出自己解锁了可选种族。
- 来源：unlock-race_doomelf.lua:24。

### C20 | entry-03460 | 存在问题（技能信息失真）
- "Instant cast phase door" 译成「使用加速技能，瞬间穿梭空间」。
- instant cast 指施放不耗时，译文读起来更像传送过程本身是瞬间的。
- phase door（术语快照：相位之门，短距离随机传送）的名称没有出现。
- 「加速技能」是原文没有的内容。它是否在暗指某个种族技能名，属于待确认子项：技能定义不在本文件的调用链上，没有读取。
- 来源：unlock-race_doomelf.lua:27。

### C21 | entry-03460 | 存在问题（增译）
- "honed by their rigorous training on the Fearscape" 译成「恶魔空间的烈火和严格训练磨砺了……」。
- 增加了「烈火」这个原文没有的成因。
- 来源：unlock-race_doomelf.lua:22。

### C22 | entry-03460 | 待确认
- "could have told the demons the truth" 译成「恶魔们将无法了解到**有关埃亚尔大陆的**真相」。
- 译文限定了真相的内容，原文没有写明。
- 缺少的证据：相关背景文本。它不在本条源文件的调用链上。

### C23 | entry-03460 | 待确认
- "Can **increase** detrimental effects and **reduce** beneficial ones on their foes" 译成「延长……缩短……」。
- 译文把「增强/削弱」具体化成了持续时间。
- 缺少的证据：魔化精灵种族技能的实现。birth/doomelf.lua 虽在补充快照中，但本文本文件没有引用任何符号引入它，按规则没有读取。

### C24 | entry-03464 | 仅建议
- "+3 Magic" 译成「魔法」，术语快照中 Magic（stat name）＝魔力，但状态是 existing。
- 同组的 context.lua:404/414 等处都一致用「魔法」，属于全库术语策略，不在单条范围内判定为缺陷。

### C25 | entry-03468 | 仅建议
- 同 C24（drem.lua:33）。

### C26 | entry-03472 | 仅建议
- 同 C24（krog.lua:33）。

### C27 | entry-03475 | 仅建议
- "I suddenly feel like I have potential to grow." 译成「我觉得我的潜能增长了。」
- "suddenly" 被略去；「有成长潜力」变成「潜能增长了」，在给属性点的语境下（godfeaster-malyu-escaped.lua:52/72-73）含义基本一致。

### C28 | entry-03476 | 仅建议
- "Fine, be that way. Good luck out there, though." 译成「好吧，就这样吧。祝你一路顺风。」
- 赌气的语气和 though 的转折略弱，信息没有丢失。
- 来源：godfeaster-malyu-escaped.lua:79-80，玩家选择什么都不给的分支。

### C29 | entry-03477 | 仅建议
- "Who..what.. YES!" 译成「是谁…什么…对！我在里面！」
- 对上一句 "There's someone else in here?"（godfeaster-malyu.lua:31）的回应增补了「我在里面」，与语境一致，不改变信息。

### C30 | entry-03479 | 存在问题（动作语义）
- "A not yet digested foe **burst out** from the sack!" 译成「……从消化袋里掉了出来！」
- 源码 digestive-sack.lua:109-117 会在附近空格加入活的 chest_guards（敌对单位）。「冲出」变成被动的「掉出」，同时「未完全消化的敌人掉出来」容易读成掉出一具残骸，失去了「活敌来袭」的提示。

### C31 | entry-03491 | 待确认
- "defence cell of **the Maggot**" 译成「巨大蛆虫的防御细胞」。
- the Maggot 首字母大写，是专指对象；译文加了「巨大」的描述。
- 缺少的证据：该专名（区域或生物）在游戏中的正式译名，不在允许材料内。
- 来源：blobs.lua:55。

### C32 | entry-03488 | 仅建议
- "You think you can open it." 译成「你觉得你可以打开它」，与原文一致，只是「你觉得」略口语化。
- 来源：godfeaster.lua:135 的 door_player_check。

### C33 | entry-03489 | 仅建议
- 同 C32（maggot.lua:136）。

### C34 | entry-03490 | 仅建议
- 同 C32（slimy_godfeaster.lua:135）。

> 更正：上表里 entry-03488/03489/03490 已按 C32–C34 标为「仅建议」。这三条其实只是同一个极轻的措辞偏好，也可以看作未发现问题。以表中「仅建议」为准，不影响缺陷计数。

---

## 读取路径、版本与越界说明
- **冻结输入**：`INPUT.md`（全文）、`source-access.json`、`context.lua`（只 grep 了 Fearscape、Maj'Eyal、Magic 等词及本包条目行）、`entries.json`。
- **entries.json**：只做了 40 条原文、译文与 INPUT 的一致性比对，并打印了字段名。字段名里有 `prior_spotcheck`、`gemini_status`、`cross_status`，我没有读取这些字段的值。
- **sources/**：读取了 source-access `files_sha256` 列出的 21 个本组文件中的相关片段，sha256 全部一致。
  - DLC 快照：`dlc/ashes-urhrok/...` 下 7 个文件，`dlc/cults/...` 下 14 个文件，源码仓库和 commit 均未固定。
- **没有读取**：引擎 commit 下的任何文件、`dlc_additional_sources` 里的任何文件、当前翻译文件、SPEC/STATE/PLAN/SCOPE/FREEZE/BASELINE/SCORING、`reports`/`raw`/`dispatches`，以及其他模型的输出。
- **额外调用链**：没有新增文件。C20、C22、C23 所需的实现文件不在显式调用链上，所以标为待确认。
- **临时文件**：没有创建临时目录或临时文件。
- **仓库**：没有修改任何文件。
- **越界**：无。唯一接近边界的是看到了 entries.json 中上述字段名，但没有读取其值。
