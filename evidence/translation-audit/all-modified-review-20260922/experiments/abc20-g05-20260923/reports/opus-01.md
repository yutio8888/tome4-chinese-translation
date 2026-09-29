我是 REVIEWER（translation_contextual_v1，自然语言实验旁路），40 条已全部独立复核。这是审核观察，不是真值，也不代表生产 DONE_VERIFIED。我没有创建临时文件、没有改仓库、没有读其他报告，也没有创建子 agent。

**汇总：** 存在问题 7 条；仅建议 4 条；待确认 0 条；未发现问题 29 条。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03333 | 未发现问题 | tformat `%s`、颜色标记、换行都保留，语义完整（addon-dev 缺源码，只做文本核对） |
| entry-03334 | 未发现问题 | 开头换行和 `%s` 保留，语义准确（缺源码，只做文本核对） |
| entry-03335 | 未发现问题 | 语义准确（缺源码，只做文本核对） |
| entry-03336 | 未发现问题 | 实现按激活次数累计，不按种类去重；译文没说“种类”，和实现并不冲突 |
| entry-03337 | 未发现问题 | 三个专名与 context 里各处一致，语义完整 |
| entry-03338 | 未发现问题 | 标记保留，专名与 demon_statues、lore 条目一致 |
| entry-03339 | 未发现问题 | 同上 |
| entry-03340 | 未发现问题 | +4/+0/+2 与 `stats={str=4,con=2,…}` 一致 |
| entry-03341 | 仅建议 | C07 |
| entry-03342 | 未发现问题 | +3 与 Doombringer 的 `life_rating = 3` 一致 |
| entry-03343 | 未发现问题 | 与 Demonologist 的 `stats={str=3,con=2,mag=4}` 一致 |
| entry-03344 | 未发现问题 | 与 `life_rating = 2` 一致 |
| entry-03345 | 存在问题 | C01、C02 |
| entry-03346 | 未发现问题 | 与 `inc_stats` 一致 |
| entry-03347 | 仅建议 | C08 |
| entry-03348 | 未发现问题 | 与 `life_rating = 9` 一致 |
| entry-03349 | 未发现问题 | 与 `experience = 1.12` 一致 |
| entry-03350 | 未发现问题 | 专名一致 |
| entry-03351 | 未发现问题 | 与 `obliterating_smash_wall = 1` 相符 |
| entry-03352 | 未发现问题 | 本体 FIRE_DRAIN 实测 `healfactor = 0.1`；半径 2，不伤友军 |
| entry-03353 | 存在问题 | C03 |
| entry-03354 | 未发现问题 | 与 `special_desc` 的分支一致，“重置”与同物品的其他译文一致 |
| entry-03355 | 未发现问题 | 同上 |
| entry-03356 | 未发现问题 | 三项豁免都 `= power`，“每点+1”等价 |
| entry-03357 | 未发现问题 | `combat_spellpower = power` |
| entry-03358 | 存在问题 | C04 |
| entry-03359 | 未发现问题 | `movement_speed = power/40`，即每点 2.5% |
| entry-03360 | 未发现问题 | 源码是 `math.ceil(power/2)`；原文同样没提取整，属上游措辞，不是翻译新增 |
| entry-03361 | 存在问题 | C05 |
| entry-03362 | 未发现问题 | `combat_dam = power` |
| entry-03363 | 未发现问题 | `inc_damage = {all = power}` |
| entry-03364 | 仅建议 | C06（源码 `ceil(power*0.4)` 的取整原文也没提，不计） |
| entry-03365 | 存在问题 | C09；另有 C10 属建议 |
| entry-03366 | 存在问题 | C11、C12；另有 C13 属建议 |
| entry-03367 | 未发现问题 | 括号里的职业名与术语一致 |
| entry-03368 | 未发现问题 | 同上 |
| entry-03369 | 未发现问题 | 种族名与术语一致 |
| entry-03370 | 未发现问题 | 语义准确 |
| entry-03371 | 存在问题 | C14–C18；另有 C19 属建议 |
| entry-03372 | 仅建议 | C20 |

### C01 | entry-03345 | 存在问题
- 原文：“Silence these beings, **maintain your deception**”；译文：“静默他们的声音，**隐藏你的踪影**”。
- 原文是“继续维持你的欺瞒”，译文改成了“藏好行踪”，“欺瞒”这层意思没了。
- 依据：doomelf.lua:26-31 的 `locked_desc` 是 Doomelf 种族的解锁提示诗。“三者可以向恶魔诉说精灵造成的恐怖”，所以要让三者噤声、把欺瞒维持下去。这是纯语义判断。

### C02 | entry-03345 | 存在问题（影响较轻）
- 原文：“one fights for the third with the cultists **she taught**”；译文：“之一召集邪徒为复活另一者而战”。
- “她亲手教出的邪徒”被改成“召集邪徒”，丢了两点：这个恶魔是女性，而且邪教是她传授的。这两点正是用来辨认对象的提示。
- 依据：同文件的解锁条件是成就 The Old Ones（achievements/all.lua:85-107，击杀三者后 `setAllowedBuild("race_doomelf")`）。lore 条目里莎西·凯希以女性口吻自述，也与邪徒有关（见 context.lua:656-692 的上下文）。
- 另：“复活另一者”对应 “for the third”，属于 lore 支持的引申，不计。

### C03 | entry-03353 | 存在问题
- 原文：“Status resistances shift **over time** to match…”；译文：“依据你中的负面状态改变你的状态免疫。”
- 译文丢了“随时间逐渐”这个时序，读起来像一次性立即改变。
- 依据：world-artifacts.lua:315-400，Revenant 的 `act`。每次物品行动时，它检查身上现有的眩晕、混乱、定身、沉默效果；对每一种命中的状态，循环 5 次，每次从其他免疫各扣 0.01、转加到这一项。所以是渐进的转移。

### C04 | entry-03358 | 存在问题
- 原文：“Increases **all** damage penetration by 1%…”；译文：“每点“阴影强度”增加1%抗性穿透。”
- 译文丢了“全体（所有伤害类型）”这个范围。同组的 03363“全体伤害加成”、03364“全体抗性”都保留了“全体”。
- 依据：world-artifacts.lua:679-682，`self.wielder.resists_pen = {all = power}`。

### C05 | entry-03361 | 存在问题
- 原文：“"Wreckage all about you. Is there anything left inside?"”；译文：“己身若残，何物能存？”
- 原文说残骸在“你四周”，并问（铠甲或你）“里面”还剩什么。译文把残骸移到“己身”，还加了一个原文没有的条件“若”，“inside”也丢了。残骸的所在从周围变成了自身，语义被改写。
- 依据：world-artifacts.lua:743，The Black Plate（重甲）的 `desc`。这是纯语义判断。

### C06 | entry-03364 | 仅建议
- 译文“全体抗性”；术语快照里 All Resists 的首选译法是“全部抗性”（preferred，core，注明是角色面板行，对应 `resists.all`）。
- 为什么只算建议：这条术语针对本体面板标签，这里是 DLC 物品的描述句。“全体抗性”与同组 03363 的“全体伤害加成”风格一致，不构成错误。

### C07 | entry-03341 | 仅建议
- 译文“+2 魔法”；术语 Magic/mag 是“魔力”（stat name，existing）。
- 为什么只算建议：这条术语状态是 existing，不是强制改名依据。同文件的 Doombringer 描述也用“魔法”，属于一致性偏好。数值正确。

### C08 | entry-03347 | 仅建议
- 同 C07（“+3 魔法”）。

### C09 | entry-03365 | 存在问题
- 最后一段原文：“while **a wretchling** presses it to your forehead”；译文：“一个**猥琐小怪**把它按上你额头”。
- wretchling 是 DLC 里一个具体的恶魔种类。同 DLC 其他地方都译作“酸液树魔”（context.lua:574 的 “demon statue: wretchling”，entry-03372）。译成“猥琐小怪”，读者就认不出是哪种恶魔，前文“豌豆滴淌着酸液”等改造描述也对不上号。
- 依据：demon.lua:291-296 的 lore id `ashes-urhrok-demon-statue-wretchling`。
- 格式方面：187 个方括号段和 34 个 [louder] 一一对应，标记计数和 16 段落结构都完整。原文结尾的换行在译文中没了，不影响显示，不计。

### C10 | entry-03365 | 仅建议
- 原文：“only cause [hairline fracture] to their own [garden]”；译文：“却只给他们自己的**星球**造成一道[发丝裂纹]，伤及他们的[花园]”。
- 译文在方括号外加了“星球”作解释，提前揭开了“花园＝星球”这个谜底。
- 为什么只算建议：没丢失原文信息，只是加了原文刻意隐藏的解释。

### C11 | entry-03366 | 存在问题
- 原文：“loyalty reinforcement there, **standard-issue alteration**”；译文：“忠诚强化在那，**标准化思维修改**”。
- 原文是恶魔对身体、魔力的“标准改造”，译文加了“思维”，改造的对象变成了心智。
- 依据：同文件 demon.lua:146-199 的作战简报写到“Having been exposed to our alteration magic…”（doombringer）和“Our standard alterations have synergized with this Shalore's natural reactive magic”（doomelf，指改造后获得的相位传送能力）。可见 alteration 指的是能力或躯体改造。

### C12 | entry-03366 | 存在问题
- 原文：“Just **step on the plate** here, and hold your arms like this so I can get **the bindings** in place...”；译文：“站在那里别动，举起胳膊，这样我就能把它放好……”
- 丢了“踏上底板”，也丢了“束缚／捆绑”，只剩一个指代不明的“它”。原文的反讽在于玩家欢天喜地地被绑上，这层信息没了。纯语义判断。

### C13 | entry-03366 | 仅建议
- “your handler”译成“你的“主人””，开头还加了“记住，”。属于措辞增色，不影响事实，算偏好。

### C14 | entry-03371 | 存在问题
- 原文：“Highest priority is now **isolating** <?=player.name?>, building a stadium **around** <?=player:him_her()?>…”；译文：“正在对 <?=player.name?> 启动最高优先级措施，**为** <?=player:him_her()?> 建造一个体育场…”
- 首要任务“隔离玩家”被省掉；体育场“围住玩家”变成“为玩家建造”。原文“把目标关进体育场、卖票观看”的“围困”含义没了。
- 依据：对照 demon.lua:200-214 的普通版，那里的首要任务是 “containing … to prevent further damage”，本条是它的恶搞版。

### C15 | entry-03371 | 存在问题
- 原文：“**Blow** all connectors, break platform off the continent”；译文：“**关闭**所有链接**传送门**…”
- “炸毁”被弱化成“关闭”；connectors 被具体化成“传送门”，源码里没有这个依据。
- 依据：普通版 demon.lua:210 附近写着 “Blow all connectors, break platform of[f]…”，是断开平台的毁灭性指令。

### C16 | entry-03371 | 存在问题
- 原文：“like the pen was **rapidly jerked away** … Your badassery must have **interrupted this demon's writing**.”
- 译文：“那是笔从手上**滑落**留下的痕迹…看起来，你的霸气侧漏把这个恶魔**吓尿了**。”
- “笔被猛地扯开”变成了“滑落”；结论“你打断了它的书写”被改写成“吓尿了”。便条中断的原因，也就是玩家闯入打断，这层信息丢了。
- 依据：普通版结尾是 “You must have interrupted this demon's writing.”，本条是在它基础上的变体。

### C17 | entry-03371 | 存在问题
- 原文：“wielding a **double-bladed** katana and fighting a **giant construct** labelled "Ninja Atamathon."”；译文：“手里拿着武士刀，正在和“忍者王阿塔玛森”对战。”
- 丢了“双刃”和“巨型构装体”，还丢了“标着……字样”这层关系。纯语义判断。

### C18 | entry-03371 | 存在问题
- 原文：“routed by **target's** overwhelming badassery”，不分性别；译文：“被**他的**霸气侧漏吓退”。
- 这里写死了男性代词。本条后文用 `<?=player:him_her()?>` 按玩家性别动态生成，所以女性角色看到的会是“他的”，指代错误。

### C19 | entry-03371 | 仅建议
- 原文：“stained with **what appear to be** motorcycle tire-tracks”；译文：“被摩托车轮胎的痕迹弄脏了”。
- “看上去像”这层保留语气丢了。这是风味文本，不涉及机制，算偏好。

### C20 | entry-03372 | 仅建议
- 原文：“dissolving the ground **they walk on**”；译文只有“溶解土地”，没说溶解的是敌人脚下的地面。
- 开头“极快的速度、庞大的数目以及……的皮肤，”缺少“凭借”之类的连接词，成了残句。
- 为什么只算建议：原文要点（冲锋、逐个扑杀、使敌人无助）都在，只是表达略欠完整。

---

### 读取范围与越界情况
**实际读取的路径：**
- 实验目录（只读）：`INPUT.md`（部分内容经工具溢出文件 `/home/paseo/.claude/projects/-home-paseo--paseo-worktrees-2p1pqszt-translation-spotcheck-20260921/f701fdf9-c018-4801-9e4f-8b1293ee659e/tool-results/bp9hmxx0s.txt` 读取，内容就是 INPUT 本身）、`entries.json`（包括 baseline_target 字段）、`context.lua`（只做分段查看和 grep）、`source-access.json`。
- 本组 sources 共 6 个文件，sha256 与 source-access 全部一致：`data/achievements/all.lua`、`data/birth/corrupted.lua`、`data/birth/doomelf.lua`、`data/general/grids/demon_statues.lua`、`data/general/objects/world-artifacts.lua`、`data/lore/demon.lua`。**DLC 源码仓库和 commit 均未固定。**

**本体额外读取（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63，用 `git show` 读单文件）：**
- `game/modules/tome/data/damage_types.lua`：因为 world-artifacts.lua:142 调用了 `engine.DamageType.FIRE_DRAIN`，读它的定义（line 1247 起）。
- `game/engines/default/engine/interface/WorldAchievements.lua`：因为 demon_statues.lua:90 调用了 `world:gainAchievement("ASHES_ALL_STATUES")`，读 `gainAchievement`（line 125 起）。

**无法核验与越界：**
- 以上两处是 DLC 调用的本体函数。本体 commit 能否适用于 DLC 的目标版本存在缺口，我没有核实。tome 模块的 World 类如何挂载这个 interface，我也没有另读。
- addon-dev 组件（03333–03335）列为 unavailable，只做了文本和格式核对。
- 03351 的技能名“歼灭挥斩”在其他翻译文件里是否一致，按规则不能读，没有核验。
- 我对实验目录执行过一次 `ls`，看到了 SPEC/STATE/PLAN/SCORING 等文件名，但没有读取它们的内容；也没有读 dispatches/、raw/、reports/。
- 没有读当前翻译文件、其他实验、历史报告或 locales，没有做整目录搜索。没有发生其他越界。
