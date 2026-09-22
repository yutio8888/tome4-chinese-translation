### 批次核验信息

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-014.md`
- **冻结 SHA-256 核验**：`0036f615f7f8dbc8d73636718808c82447bec3d2702552142aa3839369a2ac35`（核验通过，哈希完全一致）
- **核验条目范围**：`entry-00521` 至 `entry-00560`（共 40 条，已全部逐条覆盖）
- **源码依据**：公共引擎及 Tome 模块通过 `git show` 读取固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，译文比对基于提交 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核报告

#### [entry-00521] 未发现问题
- **位置**：`mod-tome.lua:3700`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色代码 `#GOLD#` 与 `#WHITE#` 匹配闭合；末尾英文冒号对应中文冒号 `：`；源码 `undead.lua:91` 为食尸鬼能力列表引导句，译文完整传达语义。

#### [entry-00522] 细微观察
- **位置**：`mod-tome.lua:3705`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：原文 `- special ghoul talents: ghoulish leap, gnaw and retch` 译为 `- 特殊食尸鬼技能：食尸鬼跳跃、啃噬和腐秽呕吐`。核对术语快照，`Ghoulish Leap` 的 preferred 译名为 `定向跳跃`；但核对固定版本译文库实际技能条目（`mod-tome.lua:31850` 及 `37645`），该技能中文名已登记为 `食尸鬼跳跃`。此处与当前技能实际译名一致，但与术语快照中的 preferred 记录存在分歧，供后续术语库校准参考。

#### [entry-00523] 未发现问题
- **位置**：`mod-tome.lua:3710`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 闭合无误；数值 `14` 与源码 `life_rating = 14`（`undead.lua:101, 126`）一致；`Life per level` 译为 `每等级生命加值` 符合标准惯例。

#### [entry-00524] 未发现问题
- **位置**：`mod-tome.lua:3711`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `12%` 正确对应；源码 `experience = 1.12`（`undead.lua:102, 133`）核验无误。

#### [entry-00525] 未发现问题
- **位置**：`mod-tome.lua:3712`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `-20%` 准确；源码中 `global_speed_base = 0.8`（`undead.lua:103, 130`），即惩罚 -20% 速度，表达吻合。

#### [entry-00526] 未发现问题
- **位置**：`mod-tome.lua:3746`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：源码 `undead.lua:194` 为骷髅解锁描述（`locked_desc`）。四六字韵文节奏对齐，分号及感叹号标点对齐，语义表达准确传神。

#### [entry-00527] 细微观察
- **位置**：`mod-tome.lua:3748`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：原文 `They have access to #GOLD#special skeleton talents#WHITE# and a wide range of undead abilities:` 译为 `它们天生具有#GOLD#特殊骷髅技能#WHITE#和一系列不死系技能：`。后半句 `undead abilities` 引导的下文包括毒素免疫、流血免疫、无需呼吸等被动特质，同 section 的 entry-00521 对应处译为“不死系能力”，此处译为“不死系技能”略显与前半句“特殊骷髅技能”重复，且不如“能力”准确。

#### [entry-00528] 未发现问题
- **位置**：`mod-tome.lua:3754`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `12` 一致；源码中骷髅 `life_rating = 12`（`undead.lua:204, 227`），属性与数值核验准确。

#### [entry-00529] 未发现问题
- **位置**：`mod-tome.lua:3755`（section：`mod-tome/data/birth/races/undead.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `20%` 准确；源码对应 `experience = 1.2`（`undead.lua:205, 235`）。

#### [entry-00530] 未发现问题
- **位置**：`mod-tome.lua:3853`（section：`mod-tome/data/birth/races/yeek.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 正确；数值 `7` 对应源码 `life_rating = 7`（`yeek.lua:125, 134`）。

#### [entry-00531] 未发现问题
- **位置**：`mod-tome.lua:3854`（section：`mod-tome/data/birth/races/yeek.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `-15%` 准确；源码 `experience = 0.85`（`yeek.lua:126, 140`），即经验惩罚为 -15%（经验获取提升 15%）。

#### [entry-00532] 未发现问题
- **位置**：`mod-tome.lua:3855`（section：`mod-tome/data/birth/races/yeek.lua`）
- **依据**：颜色标签 `#GOLD#`、`#LIGHT_BLUE#` 与数值 `35%` 准确；源码 `confusion_immune = 0.35`（`yeek.lua:127, 135`）。

#### [entry-00533] 未发现问题
- **位置**：`mod-tome.lua:3869`（section：`mod-tome/data/birth/worlds.lua`）
- **依据**：源码 `worlds.lua:60` 为战役名称；地名采用 preferred 术语 `马基·埃亚尔`，纪元名 `The Age of Ascendancy` 译为 `卓越纪`，冒号对齐。

#### [entry-00534] 未发现问题
- **位置**：`mod-tome.lua:3875`（section：`mod-tome/data/birth/worlds.lua`）
- **依据**：源码 `worlds.lua:110` 为无尽地下城解锁谜面（`locked_desc`）；译文准确保留了废墟、铁门、解谜等背景机制要素与诗歌语调，标点完整。

#### [entry-00535] 未发现问题
- **位置**：`mod-tome.lua:3881`（section：`mod-tome/data/birth/worlds.lua`）
- **依据**：源码 `worlds.lua:186` 为竞技场战役名称；`The Arena` 对应 preferred 术语 `竞技场`，战役核心目标为挑战擂主，译名切合语境。

#### [entry-00536] 未发现问题
- **位置**：`mod-tome.lua:3897`（section：`mod-tome/data/calendar_allied.lua`）
- **依据**：源码 `calendar_allied.lua:26` 联盟历月份；同文件中第 1 项 `Wintertide` 译为 `霜华`，第 7 项 `Summertide` 译为 `炎华`，对仗工整。

#### [entry-00537] 未发现问题
- **位置**：`mod-tome.lua:3910`（section：`mod-tome/data/calendar_dwarf.lua`）
- **依据**：源码 `calendar_dwarf.lua:23` 矮人历月份；材质名符合快照 preferred 术语 `斯莱特`，后缀“月”与同 section 其余月份（黑铁月、精钢月、赤金月、沃瑞钽月）规则完全一致。

#### [entry-00538] 未发现问题
- **位置**：`mod-tome.lua:3973`（section：`mod-tome/data/chats/alchemist-elvala.lua`）
- **依据**：源码中通过 `tformat(_t(other_alch), other_elixir)` 传参；译文中保留两个 `%s` 且顺序保持为“对手炼金术士”与“药剂名称”；单引号 `'mistake'` 转换为中文双引号 `“不小心出错”`，分号对齐。

#### [entry-00539] 未发现问题
- **位置**：`mod-tome.lua:3987`（section：`mod-tome/data/chats/alchemist-elvala.lua`）
- **依据**：源码 `alchemist-elvala.lua:154`；精灵炼金术士用中性代词“It”指代冒险者，译文用带引号的“它”传神呈现其傲慢态度；`Elixir of Invulnerability` 对应 `无敌药剂`，`Brotherhood` 对应 `兄弟会`，语义准确。

#### [entry-00540] 未发现问题
- **位置**：`mod-tome.lua:4035`（section：`mod-tome/data/chats/alchemist-golem.lua`）
- **依据**：源码 `alchemist-golem.lua:66` 为傀儡改名日志输出；颜色及粗体标签 `#ROYAL_BLUE#`、`#{bold}#`、`#{normal}#` 及占位符 `%s` 均完整匹配无遗漏。

#### [entry-00541] 未发现问题
- **位置**：`mod-tome.lua:4040`（section：`mod-tome/data/chats/alchemist-golem.lua`）
- **依据**：源码 `alchemist-golem.lua:76`；附身法师名字 Telos 对应通用译名“泰勒斯”，其傲慢且自鸣得意的对话性格转换自然贴切。

#### [entry-00542] 未发现问题
- **位置**：`mod-tome.lua:4052`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:83`；颜色动作标签 `#LIGHT_GREEN#*...*#WHITE#` 闭合完整；两个 `%s` 顺序与数量对齐；换行及 `\t\t` 缩进保持一致。

#### [entry-00543] 未发现问题
- **位置**：`mod-tome.lua:4064`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：地名符合 preferred 术语 `马基·埃亚尔`；结合上下文，隐士因炼金事故炸伤臀部，其粗俗暴躁台词中的粗话意向转换自然传神。

#### [entry-00544] 未发现问题
- **位置**：`mod-tome.lua:4067`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:149` 接取任务对话选项；译文“我接受。”准确简明。

#### [entry-00545] 未发现问题
- **位置**：`mod-tome.lua:4068`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:150` 拒绝任务选项；译文“我暂时无法帮助你。”准确。

#### [entry-00546] 未发现问题
- **位置**：`mod-tome.lua:4069`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：动作描述标签 `#LIGHT_GREEN#*...*#WHITE#` 完整；隐士耳聋且多疑的说话风格表达准确，标点完整。

#### [entry-00547] 未发现问题
- **位置**：`mod-tome.lua:4073`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:213` 交代材料清单台词；口吻粗俗诙谐，语义准确。

#### [entry-00548] 未发现问题
- **位置**：`mod-tome.lua:4074`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:214` 告辞选项；译文“我走了。”准确。

#### [entry-00549] 未发现问题
- **位置**：`mod-tome.lua:4080`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:234`；占位符 `%s` 填入药剂名称，格式与语义准确。

#### [entry-00550] 未发现问题
- **位置**：`mod-tome.lua:4081`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:286`（`cond = more_aid`）；玩家交付一件药剂后索取下一个任务的选项，译为“我来接下一步的任务”符合实际游戏操作功能。

#### [entry-00551] 未发现问题
- **位置**：`mod-tome.lua:4087`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:322`；夸张修辞“ADVENTURER KIBBLE”与“VAPOUR”分别译为“冒险家牌肉松”与“粉蒸肉”，贴合疯狂炼金术士戏谑调侃语境。

#### [entry-00552] 未发现问题
- **位置**：`mod-tome.lua:4089`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:332` 最终药剂调制前台词；语义完整，标点对应。

#### [entry-00553] 存在疑点
- **位置**：`mod-tome.lua:4090`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：
  1. 原文末句为：`THE LONGER YOU WAIT, THE MORE LIKELY IT IS THAT YOU'LL RETURN TO A SMOKING CRATER AND ONE TRULY IRATE HALFLING.`
  2. 译文：`最好快点，你在这儿待的时间太长，下次迎接你的可就是一个冒着黑烟怒不可遏的半身人了。`
  3. 核验证据：
     - `SMOKING CRATER`（冒烟的弹坑/大坑）在译文中缺失，被弱化合并成了“冒着黑烟...的半身人”；
     - 原句指玩家若在外面拖延过久，隐士在工坊中再次实验爆炸会导致整栋建筑被炸成“冒烟的弹坑”；而“THE LONGER YOU WAIT”被误译为“你在这儿待的时间太长”（误读为在现场站着太久），导致原文幽默的事故画面感与上下文逻辑受损。

#### [entry-00554] 未发现问题
- **位置**：`mod-tome.lua:4094`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：动作描述标签 `#LIGHT_GREEN#*...*#WHITE#` 匹配；源码 `alchemist-hermit.lua:24` 中隐士的最终奖励是刻印物品 `INFUSION_WILD_GROWTH`（野性生长纹身）；快照规定刻印物品 Infusion 统一译为“纹身”，此处“THIS INFUSION”译为“这个纹身”与游戏底层机制及术语规则完全一致。

#### [entry-00555] 未发现问题
- **位置**：`mod-tome.lua:4099`（section：`mod-tome/data/chats/alchemist-hermit.lua`）
- **依据**：源码 `alchemist-hermit.lua:432`，任务被抢先完成（poached）时的嘲讽台词；讽刺语气与句意传达准确完整。

#### [entry-00556] 未发现问题
- **位置**：`mod-tome.lua:4106`（section：`mod-tome/data/chats/alchemist-last-hope.lua`）
- **依据**：源码通过 `tformat(_t(other_alch), other_elixir)` 传参；译文中两个 `%s` 顺序保持一致（依次为竞争者与药剂），语义完整准确。

#### [entry-00557] 未发现问题
- **位置**：`mod-tome.lua:4110`（section：`mod-tome/data/chats/alchemist-last-hope.lua`）
- **依据**：源码 `alchemist-last-hope.lua:103`；矮人提问“对收钱帮人搜集材料感兴趣吗？”，玩家回复“Always.”译为“一直都有兴趣。”准确对齐问答。

#### [entry-00558] 未发现问题
- **位置**：`mod-tome.lua:4112`（section：`mod-tome/data/chats/alchemist-last-hope.lua`）
- **依据**：英文双关谐音“it suddenly hit me / by 'it' I mean 'my wife'”巧妙处理为“给了我当头一棒 / ‘它’其实是指我老婆”，原汁原味还原笑点，双引号对齐。

#### [entry-00559] 未发现问题
- **位置**：`mod-tome.lua:4116`（section：`mod-tome/data/chats/alchemist-last-hope.lua`）
- **依据**：源码 `alchemist-last-hope.lua:116`；单引号 `'elixirs'` 转换为双引号 `“药剂”`，语气流畅自然。

#### [entry-00560] 细微观察
- **位置**：`mod-tome.lua:4118`（section：`mod-tome/data/chats/alchemist-last-hope.lua`）
- **依据**：
  1. 原文 `They'll put hair on your chest, and possibly your eyelids and fingernails.` 中，`eyelids`（眼皮/眼睑）被泛化译为“脸上”（“可能还能长你脸上或者指甲盖里”）。
  2. 原文 `perhaps the last Taint of Purging left in Maj'Eyal` 意为“也许是马基·埃亚尔剩下的最后一个清除堕落印记”，译文自由添加了“传说中”并译作“唯一的堕落印记——清除印记哦”，存在较自由的意译润色。不过核心地名 `马基·埃亚尔` 与刻印名 `堕落印记——清除印记`（对应源码奖励 `TAINT_PURGING` 及 `mod-tome.lua:9510` 条目）事实核验准确。