### 批次复核报告：batch-052

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-052.md`
- **文件 SHA-256 核验**：`a7c60a522c958742931779e2ee8b4dd14b030a80abc5571098fc2e78974f11c7`（核对一致）
- **条目范围**：`entry-01465` 至 `entry-01504`，共 40 条，已逐条全部核验
- **公开源码基准**：t-engine4 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均归属于 `mod-tome`）
- **译文基准**：固定 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

#### entry-01465
- **位置**：`mod-tome.lua:20654` (`mod-tome/data/quests/start-allied.lua`)
- **原文**：`Of trolls and damp caves`
- **译文**：`巨魔与潮湿洞窟`
- **结论**：未发现问题
- **依据**：源码 `start-allied.lua:23` 任务名。`troll` 对应 preferred 规范“巨魔”（非食人魔）；仿托尔金章节标题的复数偏正短语译为“巨魔与潮湿洞窟”准确贴切。

#### entry-01466
- **位置**：`mod-tome.lua:20660` (`mod-tome/data/quests/start-allied.lua`)
- **原文**：`#SLATE#* You must explore the Trollmire and find out what lurks there and what treasures are to be gained!#WHITE#`
- **译文**：`#SLATE#* 你必须进入巨魔沼泽去调查那里潜伏着什么怪物并找到那里的宝藏！#WHITE#`
- **结论**：未发现问题
- **依据**：源码 `start-allied.lua:34`。首尾高亮控制码 `#SLATE#* ` 与 `#WHITE#` 完整匹配，专名 `Trollmire` 严格对齐 preferred 规范“巨魔沼泽”，感叹号保留正确，同 section 句式结构一致。

#### entry-01467
- **位置**：`mod-tome.lua:20690` (`mod-tome/data/quests/start-dwarf.lua`)
- **原文**：`Most of your team was killed there and now you and Norgan (the sole survivor besides you) must hurry back to the Iron Council to bring the news.`
- **译文**：`你队伍中大多数人被杀死，现在你和诺尔甘（除你以外的唯一幸存者）必须赶紧回到钢铁议会去汇报这里的情况。`
- **结论**：未发现问题
- **依据**：源码 `start-dwarf.lua:26`。核心阵营地名 `Iron Council` 严格遵循 preferred 术语“钢铁议会”（与“钢铁王座”区分）；人名“诺尔甘”一致，括号补充信息与事实描述准确。

#### entry-01468
- **位置**：`mod-tome.lua:20691` (`mod-tome/data/quests/start-dwarf.lua`)
- **原文**：`Let nothing stop you.`
- **译文**：`不惜一切代价冲出去。`
- **结论**：细微观察
- **依据**：源码 `start-dwarf.lua:27`。原文为祈使句“Let nothing stop you.”（直译为“不要让任何事物阻挡你”/“扫清一切阻碍”）。译文采取意译“不惜一切代价冲出去”，虽然契合矮人突围雷克诺尔的语境，但动作含义相比原文更为具体，属于修辞意译。

#### entry-01469
- **位置**：`mod-tome.lua:20692` (`mod-tome/data/quests/start-dwarf.lua`)
- **原文**：`Both Norgan and you made it home.`
- **译文**：`你和诺尔甘都回到了家。`
- **结论**：未发现问题
- **依据**：源码 `start-dwarf.lua:29`。诺尔甘存活完成子目标的提示文本，人名统一，句意准确，无特殊格式。

#### entry-01470
- **位置**：`mod-tome.lua:20699` (`mod-tome/data/quests/start-point-zero.lua`)
- **原文**：`The unhallowed morass is the name of the 'zone' surrounding Point Zero.`
- **译文**：`混沌之沼是零点圣域周围区域的名字。`
- **结论**：未发现问题
- **依据**：源码 `start-point-zero.lua:24`。`Point Zero` 严格遵循 preferred 规范“零点圣域”；`unhallowed morass` 与该区域通用译名“混沌之沼”（见 `mod-tome.lua:40949`）完全一致。

#### entry-01471
- **位置**：`mod-tome.lua:20700` (`mod-tome/data/quests/start-point-zero.lua`)
- **原文**：`The temporal spiders that inhabit it are growing restless and started attacking at random. You need to investigate what is going on.`
- **译文**：`栖息在那里的时空蜘蛛日益焦躁，开始随机发起攻击。你得去调查一下到底发生了什么事。`
- **结论**：未发现问题
- **依据**：源码 `start-point-zero.lua:25`。怪物名称“时空蜘蛛”与任务动机翻译准确，句式流畅自然。

#### entry-01472
- **位置**：`mod-tome.lua:20728` (`mod-tome/data/quests/start-sunwall.lua`)
- **原文**：`#LIGHT_GREEN#* You are back in Var'Eyal, the Far East as the people from the west call it.#WHITE#`
- **译文**：`#LIGHT_GREEN#* 你回到了瓦·埃亚尔——西方人把这里称作远东。#WHITE#`
- **结论**：未发现问题
- **依据**：源码 `start-sunwall.lua:29`。首尾颜色代码 `#LIGHT_GREEN#* ` 与 `#WHITE#` 匹配；大陆名称 `Var'Eyal` 对应既有术语“瓦·埃亚尔”，破折号衔接解释自然。

#### entry-01473
- **位置**：`mod-tome.lua:20753` (`mod-tome/data/quests/start-undead.lua`)
- **原文**：`You have been resurrected as an undead by some dark powers.`
- **译文**：`你被某种黑暗力量复活为不死生物。`
- **结论**：未发现问题
- **依据**：源码 `start-undead.lua:23`。背景叙述准确，生物类别“不死生物”符合上下文语境。

#### entry-01474
- **位置**：`mod-tome.lua:20754` (`mod-tome/data/quests/start-undead.lua`)
- **原文**：`However, the ritual failed in some way and you retain your own mind. You need to get out of this dark place and try to carve a place for yourself in the world.`
- **译文**：`不过，复活仪式似乎出了点问题，你保留了自己的意识，你必须离开这个黑暗地方并找到属于自己的栖息地。`
- **结论**：细微观察
- **依据**：源码 `start-undead.lua:24`。原文成语“carve a place for yourself in the world”指在世上谋求一席之地或立足于世，译文“找到属于自己的栖息地”偏向字面动物生境（habitat），略欠文采；此外原文断句为两句（句号），译文以逗号粘连。但核心意思表达完整，不影响机制理解。

#### entry-01475
- **位置**：`mod-tome.lua:20755` (`mod-tome/data/quests/start-undead.lua`)
- **原文**：`You have found a very special cloak that will help you walk among the living without trouble.`
- **译文**：`你发现了一个非常神奇的斗篷，可以使你在活人之中自由生活而不会陷入麻烦。`
- **结论**：未发现问题
- **依据**：源码 `start-undead.lua:26`。机制上指不死族专属伪装斗篷（Cloak of Deception），穿戴后可自由出入城镇不被生者敌对，译文对该效果解释通顺达意。

#### entry-01476
- **位置**：`mod-tome.lua:20778` (`mod-tome/data/quests/starter-zones.lua`)
- **原文**：`It is time to explore some new places -- dark, forgotten and dangerous ones.`
- **译文**：`是时候去一些新的地方探索一下了——那些黑暗、被遗忘和危险的地方。`
- **结论**：未发现问题
- **依据**：源码 `starter-zones.lua:25`。双破折号对应中文破折号“——”，三个形容词并列结构准确。

#### entry-01477
- **位置**：`mod-tome.lua:20779` (`mod-tome/data/quests/starter-zones.lua`)
- **原文**：`The Old Forest is just south-east of the town of Derth.`
- **译文**：`在德斯镇东南方向是古老森林。`
- **结论**：未发现问题
- **依据**：源码 `starter-zones.lua:26`。地名 `Old Forest`（古老森林）与 `Derth`（德斯镇）严格符合既有 core 术语表，方位与语法准确。

#### entry-01478
- **位置**：`mod-tome.lua:20780` (`mod-tome/data/quests/starter-zones.lua`)
- **原文**：`The Maze is west of Derth.`
- **译文**：`在德斯镇西面是迷宫。`
- **结论**：未发现问题
- **依据**：源码 `starter-zones.lua:27`。地名“德斯镇”与“迷宫”及西方位指示清晰准确。

#### entry-01479
- **位置**：`mod-tome.lua:20781` (`mod-tome/data/quests/starter-zones.lua`)
- **原文**：`The Sandworm Lair is to the far west of Derth, near the sea.`
- **译文**：`在德斯镇远一点的西面，靠近海岸的地方是沙虫巢穴。`
- **结论**：细微观察
- **依据**：源码 `starter-zones.lua:28`。地名 `Sandworm Lair` 严格遵循 preferred 规范“沙虫巢穴”（不作“沙虫洞穴”）。原文“to the far west of Derth”（德斯镇极西之处）在译文中处理为口语化的“远一点的西面”，语气略偏弱，但结合后半句“靠近海岸的地方”，地理位置辨识无误。

#### entry-01480
- **位置**：`mod-tome.lua:20782` (`mod-tome/data/quests/starter-zones.lua`)
- **原文**：`The Daikara is on the eastern borders of the Thaloren forest.`
- **译文**：`在自然精灵树林的东部边境那里是岱卡拉。`
- **结论**：未发现问题
- **依据**：源码 `starter-zones.lua:29`。地名 `The Daikara` 对应“岱卡拉”，`Thaloren` 对应种族既有术语“自然精灵”，方位表达准确。

#### entry-01481
- **位置**：`mod-tome.lua:20799` (`mod-tome/data/quests/strange-new-world.lua`)
- **原文**：`You arrived through the farportal in a cave, probably in the Far East.`
- **译文**：`你经由远行传送门抵达了一处山洞，大概位于远东大陆。`
- **结论**：未发现问题
- **依据**：源码 `strange-new-world.lua:25`。核心设施 `farportal` 对应“远行传送门”，地名“远东大陆”准确，叙述流畅。

#### entry-01482
- **位置**：`mod-tome.lua:20800` (`mod-tome/data/quests/strange-new-world.lua`)
- **原文**：`Upon arrival you met an Elf and an orc fighting.`
- **译文**：`你碰到了一个精灵在和一个兽人战斗。`
- **结论**：细微观察
- **依据**：源码 `strange-new-world.lua:26`。原文句首时间状语“Upon arrival”（一抵达时/刚到这里）在译文中被省略，直接以“你碰到了...”陈述；结合前一条目已有抵达说明，上下文理解连贯。

#### entry-01483
- **位置**：`mod-tome.lua:20803` (`mod-tome/data/quests/strange-new-world.lua`)
- **原文**：`Fillarel told you to go to the southeast and meet with High Sun Paladin Aeryn.`
- **译文**：`菲拉瑞尔告诉你去东南方会见高阶太阳骑士艾琳。`
- **结论**：未发现问题
- **依据**：源码 `strange-new-world.lua:35`。NPC 头衔 `High Sun Paladin Aeryn` 严格遵循 preferred 规范“高阶太阳骑士艾琳”（保留“高阶”），人名与方位指引准确。

#### entry-01484
- **位置**：`mod-tome.lua:20804` (`mod-tome/data/quests/strange-new-world.lua`)
- **原文**：`Krogar told you to go to the west and look for the Kruk Pride.`
- **译文**：`克洛加尔告诉你去西面寻找克鲁克部落。`
- **结论**：未发现问题
- **依据**：源码 `strange-new-world.lua:37`。阵营专名 `Kruk Pride` 符合既有术语“克鲁克部落”，人名与方位准确。

#### entry-01485
- **位置**：`mod-tome.lua:20812` (`mod-tome/data/quests/temple-of-creation.lua`)
- **原文**：`Ukllmswwik asked you to take his portal to the Temple of Creation and kill Slasul who has turned mad.`
- **译文**：`乌克勒姆斯维奇请求你穿过他的传送门到造物者神庙去杀死发疯了的萨拉苏尔。`
- **结论**：未发现问题
- **依据**：源码 `temple-of-creation.lua:23`。地点名 `Temple of Creation` 符合既有术语“造物者神庙”，人名“乌克勒姆斯维奇”与“萨拉苏尔”对齐，任务指引明确。

#### entry-01486
- **位置**：`mod-tome.lua:20813` (`mod-tome/data/quests/temple-of-creation.lua`)
- **原文**：`Slasul told you his side of the story. Now you must decide: which of them is corrupt?`
- **译文**：`萨拉苏尔告诉了你关于他的故事，你现在必须决定：到底谁才是真正的堕落者？`
- **结论**：细微观察
- **依据**：源码 `temple-of-creation.lua:25`。剧情中乌克勒姆斯维奇与萨拉苏尔互相指责，原文“his side of the story”特指在对立冲突中“他这一方的说法/立场”，译文处理为“关于他的故事”略失对立语境；但后半句“到底谁才是真正的堕落者？”有效拉回了对立选择的焦点。

#### entry-01487
- **位置**：`mod-tome.lua:20826` (`mod-tome/data/quests/temporal-rift.lua`)
- **原文**：`Back and Back and Back to the Future`
- **译文**：`回到、回到、回到未来`
- **结论**：未发现问题
- **依据**：源码 `temporal-rift.lua:20`。时空裂缝任务名，致敬《回到未来》的三次重复结构完全对称，顿号断句自然。

#### entry-01488
- **位置**：`mod-tome.lua:20836` (`mod-tome/data/quests/trollmire-treasure.lua`)
- **原文**：`You have found all the clues leading to the hidden treasure. There should be a way on the third level of the Trollmire.`
- **译文**：`你已经找到了所有有关秘密财宝的线索，在巨魔沼泽第三层应该能找到一条通往那里的路。`
- **结论**：未发现问题
- **依据**：源码 `trollmire-treasure.lua:24`。`Trollmire` 符合 preferred“巨魔沼泽”，隐藏宝藏线索及层数指引翻译准确。

#### entry-01489
- **位置**：`mod-tome.lua:20837` (`mod-tome/data/quests/trollmire-treasure.lua`)
- **原文**：`It looks extremely dangerous, however - beware.`
- **译文**：`注意：看样子那里非常危险。`
- **结论**：未发现问题
- **依据**：源码 `trollmire-treasure.lua:25`。警示词“beware”前置为“注意：”符合中文告示风格，语义完整忠实。

#### entry-01490
- **位置**：`mod-tome.lua:20838` (`mod-tome/data/quests/trollmire-treasure.lua`)
- **原文**：`You have slain Bill. His treasure is yours for the taking.`
- **译文**：`你已经干掉了比尔，他的财宝现在归你了。`
- **结论**：未发现问题
- **依据**：源码 `trollmire-treasure.lua:27`。击杀石巨魔比尔（Bill the Stone Troll）完成任务结算，口语化风格与场景贴合，意思准确。

#### entry-01491
- **位置**：`mod-tome.lua:20857` (`mod-tome/data/quests/tutorial.lua`)
- **原文**：`You must venture in the heart of the forest and kill the Lone Wolf, who randomly attacks villagers.`
- **译文**：`你必须进入森林的中心地带并杀死孤狼——那个肆意屠杀村民的凶手。`
- **结论**：细微观察
- **依据**：源码 `tutorial.lua:24`。目标名称 `Lone Wolf` 严格遵循 preferred 规范“孤狼”（不作“寂寞的狼”）。定语从句“who randomly attacks villagers”（直译为“它会随机袭击村民”）在译文中被大幅意译并加色为“——那个肆意屠杀村民的凶手”，增加了较强的情感色彩与词义衍生。

#### entry-01492
- **位置**：`mod-tome.lua:20872` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`Zemekkys in the Gates of Morning can build a portal back to your homeland for you.`
- **译文**：`晨曦之门的泽梅基斯可以为你建造一座返回故乡的传送门。`
- **结论**：未发现问题
- **依据**：源码 `west-portal.lua:24`。地名 `Gates of Morning` 严格符合既有术语“晨曦之门”，人名与传送门功能翻译准确。

#### entry-01493
- **位置**：`mod-tome.lua:20878` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`Zemekkys points to the location of Vor Armoury on your map.`
- **译文**：`泽梅基斯在你的地图上指出了沃尔军械库的位置。`
- **结论**：未发现问题
- **依据**：源码 `west-portal.lua:51`（`logPlayer`）。兽人军械库地名 `Vor Armoury` 译为“沃尔军械库”，地图标示动作翻译准确。

#### entry-01494
- **位置**：`mod-tome.lua:20879` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`Zemekkys points to the location of Briagh's lair on your map.`
- **译文**：`泽梅基斯在你的地图上指出了布莱亚的巢穴的位置。`
- **结论**：未发现问题
- **依据**：源码 `west-portal.lua:63`（`logPlayer`）。沙龙巢穴地名 `Briagh's lair` 译为“布莱亚的巢穴”，地图指示明确。

#### entry-01495
- **位置**：`mod-tome.lua:20880` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`#VIOLET#Zemekkys starts to draw runes on the floor using the athame and gem dust.`
- **译文**：`#VIOLET#泽梅基斯开始用仪式匕首和宝石粉末在地板上绘制符文。`
- **结论**：未发现问题
- **依据**：源码 `west-portal.lua:73`（`logPlayer`）。高亮标签 `#VIOLET#` 保留完整；道具名 `athame` 严格遵循 preferred 规范“仪式匕首”（不作“祭剑”或“祭祀短剑”），动作翻译准确。

#### entry-01496
- **位置**：`mod-tome.lua:20882` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`#VIOLET#Zemekkys says: 'The portal is done!'`
- **译文**：`#VIOLET#泽梅基斯说道：“传送门已经开启！”`
- **结论**：细微观察
- **依据**：源码 `west-portal.lua:75`（`logPlayer`）。标签 `#VIOLET#` 与引号保留规范。台词“The portal is done!”字面意为“传送门做好了/完成了！”，译文意译为“传送门已经开启！”，虽符合场景中传送门即刻激活就绪的表现，但与字面略有出入。

#### entry-01497
- **位置**：`mod-tome.lua:20883` (`mod-tome/data/quests/west-portal.lua`)
- **原文**：`High Chronomancer Zemekkys`
- **译文**：`高阶时空法师泽梅基斯`
- **结论**：未发现问题
- **依据**：源码 `west-portal.lua:83`（NPC 实体名）。`Chronomancer` 作为 NPC 实体头衔统一译作“时空法师”（与开局职业分类“时空系”严格区分，见 `mod-tome.lua:6287`），头衔“高阶时空法师泽梅基斯”全库一致。

#### entry-01498
- **位置**：`mod-tome.lua:20894` (`mod-tome/data/quests/wild-wild-east.lua`)
- **原文**：`There must be a way to go into the far east from the lair of Golbug. Find it and explore the unknown far east, looking for clues.`
- **译文**：`在高尔布格巢穴内肯定有一条通往远东大陆的路，去寻找线索并找到它，然后探索那未知而遥远的东方。`
- **结论**：存在疑点
- **依据**：源码 `wild-wild-east.lua:24`。
  1. **修饰逻辑颠倒**：原文为“Find it and explore the unknown far east, looking for clues.”，“Find it”指找到通往远东的路，“looking for clues”是探索远东时的伴随动作（探索未知的远东并寻找线索）；译文重组为“去寻找线索并找到它，然后探索...”，将寻找线索错置为找到通路的前置动作。
  2. **专名一致性散化**：同一句中前半句 `far east` 译为“远东大陆”，后半句 `unknown far east` 却意译散化为“那未知而遥远的东方”，脱离了固定地名“远东”。

#### entry-01499
- **位置**：`mod-tome.lua:20904` (`mod-tome/data/resources.lua`)
- **原文**：`Mana represents your reserve of magical energies. Most spells cast consume mana and each sustained spell reduces your maximum mana.`
- **译文**：`法力值代表你存储的魔法能量。大部分法术都要消耗法力值，持续法术技能会降低你的最大法力值。`
- **结论**：未发现问题
- **依据**：源码 `resources.lua:164`。核心资源名 `Mana` 遵循 existing core 规范“法力值”；“持续法术降低最大法力值”完全吻合 ToME 引擎持续技能（sustain cost）机制。

#### entry-01500
- **位置**：`mod-tome.lua:20921` (`mod-tome/data/resources.lua`)
- **原文**：`Psi represents your reserve of psychic energy.`
- **译文**：`灵能值代表你存储的精神力量。`
- **结论**：未发现问题
- **依据**：源码 `resources.lua:343`。核心资源名 `Psi` 严格遵循既有规范“灵能值”，定义简明准确。

#### entry-01501
- **位置**：`mod-tome.lua:20933` (`mod-tome/data/rooms/greater_vault.lua`)
- **原文**：`#GOLD#PLACED GREATER VAULT: %s`
- **译文**：`#GOLD#放置大型宝库：%s`
- **结论**：未发现问题
- **依据**：源码 `greater_vault.lua:51`（调试/作弊日志）。`#GOLD#` 颜色代码与单一 `%s` 占位符完整保留，宝库类型名词准确。

#### entry-01502
- **位置**：`mod-tome.lua:20938` (`mod-tome/data/rooms/lesser_vault.lua`)
- **原文**：`#GOLD#PLACED LESSER VAULT: %s`
- **译文**：`#GOLD#放置小型宝库：%s`
- **结论**：未发现问题
- **依据**：源码 `lesser_vault.lua:47`（调试/作弊日志）。`#GOLD#` 颜色代码与单一 `%s` 占位符完整保留，小型宝库名词准确。

#### entry-01503
- **位置**：`mod-tome.lua:20975` (`mod-tome/data/talents/celestial/celestial.lua`)
- **原文**：`The songs the Fallen sing.`
- **译文**：`堕落者咏唱之歌。`
- **结论**：未发现问题
- **依据**：源码 `celestial.lua:44`。挽歌技能树（`celestial/dirges`）描述，专有名词 `Fallen` 对应太阳骑士进阶职业“堕落者”，文风简练契合。

#### entry-01504
- **位置**：`mod-tome.lua:20977` (`mod-tome/data/talents/celestial/celestial.lua`)
- **原文**：`Signature magics of the Fallen.  The sun shines for the guilty and the innocent alike.`
- **译文**：`堕落者的特有魔法。无论罪恶与否，阳光依然闪耀。`
- **结论**：未发现问题
- **依据**：源码 `celestial.lua:45`。背光面技能树（`celestial/darkside`）描述，职业名“堕落者”一致；后半句典故（马太福音 5:45 隐喻）翻译达意、文学风格自然。

---

### 复核统计与概要

- **总复核条数**：40 条（`entry-01465` 至 `entry-01504`）
- **未发现问题**：32 条
- **细微观察**：7 条（`entry-01468`、`entry-01474`、`entry-01479`、`entry-01482`、`entry-01486`、`entry-01491`、`entry-01496`，主要为修辞意译、偏口语化表达或从句微小省略，不破坏游戏机制与核心专名）
- **存在疑点**：1 条（`entry-01498`：存在逻辑从属重组与专名一致性散化问题）