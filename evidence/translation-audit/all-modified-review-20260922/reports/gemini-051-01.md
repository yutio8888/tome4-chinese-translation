### batch-051 只读译文复核报告

#### 一、文件与环境核验
- **核验文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-051.md`
- **文件 SHA-256 计算值**：`3212138424a400bd886997ff2bb7305689e023e64604835c93aeaea04464b577`（与要求完全一致，核验通过）
- **条目范围**：`entry-01425` 至 `entry-01464`，共 40 条
- **源码与语境基准**：
  - 公开源码固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（`/workspace/t-engine4`，读取 `game/modules/tome/data/quests/` 下各任务脚本）
  - 译文终点基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua` 第 20360 至 20650 行）

---

#### 二、逐条复核记录（全部 40 条）

- **entry-01425** (`mod-tome.lua:20370`)
  - **原文**：`#SLATE#* The beating heart of a powerful necromancer.#WHITE#`
  - **译文**：`#SLATE#* 一颗强大死灵法师跳动的心脏。#WHITE#`
  - **复核结论**：未发现问题
  - **可核验依据**：颜色代码 `#SLATE#`、`#WHITE#` 与列表符 `* ` 完整保留；Necromancer 遵循术语规范译为“死灵法师”；与 `lichform.lua:32` 源码前置条件“提取同类死灵法师心脏”任务描述一致，文意准确流畅。

- **entry-01426** (`mod-tome.lua:20384`)
  - **原文**：`Storming the city`
  - **译文**：`风暴袭城`
  - **复核结论**：未发现问题
  - **可核验依据**：任务名。对应 `lightning-overload.lua:21`，德斯镇遭遇雷暴云与空气元素袭击，“风暴袭城”双关“Storm”的风暴现象与突袭动作，文意精练贴切。

- **entry-01427** (`mod-tome.lua:20387`)
  - **原文**：` * You have dispatched the elementals but the cloud lingers still. You must find a powerful ally to remove it. There are rumours of a secret town in the mountains, to the southwest. You could also check out the Ziguranth group that is supposed to fight magic.`
  - **译文**：` * 你已经消灭了那些元素生物，但是天上乌云并未就此散去。你必须找到一位强大的盟友才能驱散它。传说中，在西南方的山脉之中有一个神秘的小镇，你也能顺便调查一下伊格兰斯——据称这是一个与魔法为敌的组织。`
  - **复核结论**：未发现问题
  - **可核验依据**：前置缩进与星号 ` * ` 保留；elementals 遵循术语表译为“元素生物”；此处“Ziguranth group”指代反魔法教团组织，严格遵循术语规则使用“伊格兰斯”（区别于地名据点“伊格”），文意与逻辑准确。

- **entry-01428** (`mod-tome.lua:20414`)
  - **原文**：`A stairway out appears at your feet. The Lord says: 'And remember, you are MINE. I will call you.'`
  - **译文**：`一道通往外界的楼梯出现在你脚下。刺客领主说道：“记住，你是我的人。我会召唤你的。”`
  - **复核结论**：未发现问题
  - **可核验依据**：源码 `lost-merchant.lua:28` evil 分支；“The Lord”在任务中特指刺客领主（Assassin Lord），明晰译为“刺客领主”消除歧义；英文单引号正确转换为中文全角双引号。

- **entry-01429** (`mod-tome.lua:20421`)
  - **原文**：`After rescuing Melinda from Kryl-Feijan and the cultists you met her again in Last Hope.`
  - **译文**：`在你从克里尔·费扬和邪教徒手中解救了梅琳达之后，你在最后的希望又碰到了她。`
  - **复核结论**：未发现问题
  - **可核验依据**：专有名词 Melinda（梅琳达）、Last Hope（最后的希望）、Kryl-Feijan（克里尔·费扬）均符合规范；叙事时序与人名对应准确。

- **entry-01430** (`mod-tome.lua:20424`)
  - **原文**：`The Fortress Shadow said she could be cured.`
  - **译文**：`堡垒之影说她有可能被治愈。`
  - **复核结论**：未发现问题
  - **可核验依据**：The Fortress Shadow（堡垒之影）角色称谓正确；情态动词“could”译作“有可能被治愈”符合剧情中堡垒管家暂未完全打包票的语境。

- **entry-01431** (`mod-tome.lua:20425`)
  - **原文**：`Melinda decided to come live with you in your Fortress.`
  - **译文**：`梅琳达决定和你一起在堡垒里生活。`
  - **复核结论**：未发现问题
  - **可核验依据**：文意直观准确，与梅琳达入住夏·图尔堡垒事件对应，标点完整。

- **entry-01432** (`mod-tome.lua:20426`)
  - **原文**：`The Fortress Shadow has established a portal for her so she can come and go freely.`
  - **译文**：`堡垒之影为她建造了一个传送门，他让她能够自由来去。`
  - **复核结论**：存在疑点
  - **可核验依据**：原文后半句为目的从句 `so she can come and go freely`（以便/好让她能够自由来去）；译文作“他让她能够自由来去”，引入了原文无对应的主语代词“他”（且堡垒之影实为构装暗影），疑似错字（“好让”误作“他让”）或冗余生硬的主谓重构，建议校准为“好让她能够自由来去”或“以便她能够自由来去”。

- **entry-01433** (`mod-tome.lua:20436`)
  - **原文**：`You met a half-mad lumberjack fleeing a small village, rambling about an untold horror lurking there, slaughtering people.`
  - **译文**：`你遇到了一个从小村庄里逃出来的半疯癫的伐木工人，大声喊着有个没见过的吓人的东西在里面杀人。`
  - **复核结论**：未发现问题
  - **可核验依据**：核验 `town-lumberjack-village/npcs.lua`，村庄潜伏凶手实际为人类诅咒魔化狂人 Ben Cruthdar（The Cursed），故此处“untold horror”系半疯伐木工口中难以言状的可怕怪物，译为“没见过的吓人的东西”口吻生动逼真，符合人物恐慌胡话语境。

- **entry-01434** (`mod-tome.lua:20442`)
  - **原文**：`You saved %s of us, please take this as a reward. (They give you %s)`
  - **译文**：`你救下了我们中的%s人，请你收下这个作为奖励吧。(他们给了你 %s)`
  - **复核结论**：未发现问题
  - **可核验依据**：源码 `lumberjack-cursed.lua:58` 传参为 `self.lumberjacks_died == 0 and _t("all", "quest_lumberjack") or _t"most"` 及物品名称；第一处 `%s` 替换“所有”或“大部分”，在中文中组成“我们中的所有人/大部分人”，语法自洽；第二处物品名带括号说明保留，格式与占位符无异常。

- **entry-01435** (`mod-tome.lua:20451`)
  - **原文**：`You met a novice mage who was tasked to collect an arcane powered artifact.`
  - **译文**：`你碰到了一个法师学徒，他被指派去搜集一件充满奥术力量的神器。`
  - **复核结论**：未发现问题
  - **可核验依据**：novice mage 译为“法师学徒”，arcane powered artifact 译为“充满奥术力量的神器”，名词与属性匹配，文意准确。

- **entry-01436** (`mod-tome.lua:20453`)
  - **原文**：`#SLATE#* Collect an artifact arcane powered item.#WHITE#`
  - **译文**：`#SLATE#* 收集一件充满奥术力量的神器。#WHITE#`
  - **复核结论**：未发现问题
  - **可核验依据**：颜色标签 `#SLATE#`、`#WHITE#` 及星号保留，与前一条目任务目标描述用词完全统一。

- **entry-01437** (`mod-tome.lua:20457`)
  - **原文**：`You receive: %s`
  - **译文**：`你收到：%s。`
  - **复核结论**：未发现问题
  - **可核验依据**：源码 `mage-apprentice.lua:107`，获得物品时打印日志，占位符 `%s` 正确保留，冒号转全角，句末加句号符合中文日志惯例。

- **entry-01438** (`mod-tome.lua:20463`)
  - **原文**：`You found an ancient tome about gems.`
  - **译文**：`你发现一本关于珠宝的旧书。`
  - **复核结论**：细微观察
  - **可核验依据**：本任务涉及珠宝匠 Limmir 及宝石精练（gemcrafting），同 section 后文第 20466 行译为“关于宝石的力量”，此处 gems 译为“珠宝”而非“宝石”，且 ancient tome 弱化译为“旧书”（易被理解为二手普通书而非古籍典册）；虽不阻断任务理解，但在同任务语境内用词略显粗疏与不统一。

- **entry-01439** (`mod-tome.lua:20464`)
  - **原文**：`You should bring it to the jeweler in the Gates of Morning.`
  - **译文**：`你应该把这本书带给晨曦之门的珠宝匠看看。`
  - **复核结论**：未发现问题
  - **可核验依据**：Gates of Morning 严格按地名规范译为“晨曦之门”；文意通顺。

- **entry-01440** (`mod-tome.lua:20477`)
  - **原文**：`You have found an orb of command that seems to be used to open the shield protecting the High Peak.`
  - **译文**：`你找到了一个指令水晶球，似乎是用来开启巅峰护盾的钥匙。`
  - **复核结论**：未发现问题
  - **可核验依据**：High Peak 遵循规范译为“巅峰”，orb of command 译为“指令水晶球”，将破除护盾的机制形象化引申为“开启……的钥匙”，意思明白无误。

- **entry-01441** (`mod-tome.lua:20478`)
  - **原文**：`There seems to be a total of four of them. The more you have the weaker the shield will be.`
  - **译文**：`似乎一共有四个水晶球，你得到的越多，护盾的防御力越弱。`
  - **复核结论**：未发现问题
  - **可核验依据**：四颗指令水晶削弱巅峰护盾机制阐述准确，语义通顺。

- **entry-01442** (`mod-tome.lua:20488`)
  - **原文**：`You have taken upon yourself to cleanse it and deal a crippling blow to the orcs.`
  - **译文**：`你已决意亲自清除此地，给兽人以沉重的一击。`
  - **复核结论**：未发现问题
  - **可核验依据**：术语表中 cleanse 仅约束核心装备词缀为“洁净”，语境动作可自由使用“清除”；cleanse it 结合育种棚语境译为“清除此地”，orcs 译为“兽人”，表意准确有力。

- **entry-01443** (`mod-tome.lua:20497`)
  - **原文**：`Find out if they are in any way linked to the lost staff.`
  - **译文**：`查清楚他们是不是和遗失的法杖有关。`
  - **复核结论**：未发现问题
  - **可核验依据**：指主线失踪的吸收法杖（the lost staff），译文语义忠实、口吻准确。

- **entry-01444** (`mod-tome.lua:20498`)
  - **原文**：`But be careful -- even the Dwarves have not ventured in these old halls for many years.`
  - **译文**：`小心，矮人们已经很多年没有进过那些古老的大厅了。`
  - **复核结论**：未发现问题
  - **可核验依据**：破折号转为逗号符合中文句式，Dwarves 译为“矮人们”，文意贴切。

- **entry-01445** (`mod-tome.lua:20505`)
  - **原文**：`Investigate the bastions of the Pride.`
  - **译文**：`调查兽人部落的基地。`
  - **复核结论**：未发现问题
  - **可核验依据**：任务《The many Prides of the Orcs》（兽人部落）总目标，the Pride 在此指代各兽人部落堡垒，译为“兽人部落的基地”准确通顺。

- **entry-01446** (`mod-tome.lua:20528`)
  - **原文**：`You tried to kill yourself to prevent you from doing something, or going somewhere... you were not very clear.\n`
  - **译文**：`你尝试杀掉自己，以阻止自己做某件事，或去往某个地方……你说得不太清楚。\n`
  - **复核结论**：未发现问题
  - **可核验依据**：结尾换行符保留；省略号转换为中文全角省略号；时空悖论自杀桥段语意传递完整。

- **entry-01447** (`mod-tome.lua:20542`)
  - **原文**：`#LIGHT_BLUE#Your future self kills you! The timestreams are broken by the paradox!`
  - **译文**：`#LIGHT_BLUE#你未来的自己杀死了你！时间流被这个悖论所打破！`
  - **复核结论**：未发现问题
  - **可核验依据**：颜色代码 `#LIGHT_BLUE#` 与感叹号保留；此处 paradox 指祖父悖论这一时空现象，译为“悖论”准确（区分于技能类别/资源数值）。

- **entry-01448** (`mod-tome.lua:20543`)
  - **原文**：`#LIGHT_BLUE#All those events never happened. Except they did, somewhen.`
  - **译文**：`#LIGHT_BLUE#所有这些事件都从未发生过，只不过它们确实在某个时候发生了。`
  - **复核结论**：未发现问题
  - **可核验依据**：颜色代码 `#LIGHT_BLUE#` 保留；巧妙翻译了时空语境下的虚构造词“somewhen”（在某个时间维度/某个时候发生过），语义生动贴切。

- **entry-01449** (`mod-tome.lua:20551`)
  - **原文**：`You should go investigate what is happening there.`
  - **译文**：`你得去调查一下那里发生了什么事。`
  - **复核结论**：未发现问题
  - **可核验依据**：文意准确，标点完整。

- **entry-01450** (`mod-tome.lua:20566`)
  - **原文**：`Till the Blood Runs Clear`
  - **译文**：`直到鲜血流清`
  - **复核结论**：细微观察
  - **可核验依据**：鲜血之环（Ring of Blood）角斗场任务名。英文为成语/文学表达（源自清洗/放血直至清澈无血，引申为战斗直至血流尽），直译作“直到鲜血流清”带有轻微字面直译痕迹（通常中文理解作“直到鲜血流尽”或“直到血水流清”），但不影响任务定位。

- **entry-01451** (`mod-tome.lua:20587`)
  - **原文**：`You found notes from an explorer inside the Old Forest. He spoke about Sher'Tul ruins sunken below the surface of the lake of Nur, at the forest's center.`
  - **译文**：`在古老森林里找到了一个探险者的笔记，里面提到在森林中心的纳尔湖底下有一个沉没的夏·图尔遗迹。`
  - **复核结论**：未发现问题
  - **可核验依据**：Old Forest（古老森林）、lake of Nur（纳尔湖）、Sher'Tul（夏·图尔）三大地名与种族专名完全符合规范，语句通顺。

- **entry-01452** (`mod-tome.lua:20588`)
  - **原文**：`With one of the notes there was a small gem that looks like a key.`
  - **译文**：`和笔记在一起被发现的还有个小小的宝石，样子看上去像一把钥匙。`
  - **复核结论**：未发现问题
  - **可核验依据**：对应进入纳尔遗迹底层的钥匙宝石道具，描述准确。

- **entry-01453** (`mod-tome.lua:20589`)
  - **原文**：`#LIGHT_GREEN#* You used the key inside the ruins of Nur and found a way into the fortress of old.#WHITE#`
  - **译文**：`#LIGHT_GREEN#* 你在纳尔遗迹中使用这把钥匙，找到了通往古老堡垒的入口。#WHITE#`
  - **复核结论**：未发现问题
  - **可核验依据**：颜色代码 `#LIGHT_GREEN#`、`#WHITE#` 及列表符保留；ruins of Nur（纳尔遗迹）与 fortess of old（古老堡垒）表述自然。

- **entry-01454** (`mod-tome.lua:20598`)
  - **原文**：`#RED#* You have forced a recall while in an exploratory farportal zone. The farportal was rendered unusable in the process.#WHITE#`
  - **译文**：`#RED#* 你在探索用远行传送门区域内强制启动了回归之杖，导致这座远行传送门彻底无法使用。#WHITE#`
  - **复核结论**：未发现问题
  - **可核验依据**：exploratory farportal 严格遵循术语规范译为“探索用远行传送门”；forced a recall 结合机制准确译为“强制启动了回归之杖”；颜色码与列表符完整。

- **entry-01455** (`mod-tome.lua:20599`)
  - **原文**：`#LIGHT_GREEN#* You have entered the exploratory farportal room and defeated the horror lurking there. You can now use the farportal.#WHITE#`
  - **译文**：`#LIGHT_GREEN#* 你进入了探索用远行传送门所在的房间，并消灭了潜伏其中的恐魔。现在你可以使用这座远行传送门了。#WHITE#`
  - **复核结论**：未发现问题
  - **可核验依据**：核验源码 `shertul-fortress.lua:149` `spawn_farportal_guardian`，守门 BOSS 实体类型明确为 `type="horror"`，此处译为“恐魔”完全契合生物分类规范；exploratory farportal 术语规范一致；颜色代码完整。

- **entry-01456** (`mod-tome.lua:20602`)
  - **原文**：`\nThe fortress's current energy level is: #LIGHT_GREEN#%d#WHITE#.`
  - **译文**：`\n当前堡垒能量等级：#LIGHT_GREEN#%d#WHITE#。`
  - **复核结论**：未发现问题
  - **可核验依据**：前导换行符保留；数值占位符 `%d` 与颜色标签 `#LIGHT_GREEN#`、`#WHITE#` 完整；标点句号对应。

- **entry-01457** (`mod-tome.lua:20606`)
  - **原文**：`Master, you have sent enough energy to activate the exploratory farportal.\nHowever, there seems to be a disturbance in that room. Please return as soon as possible.`
  - **译文**：`主人，你已经注入了足够启动探索用远行传送门的能量。\n然而，那个房间里似乎有些异动。请尽快回来。`
  - **复核结论**：未发现问题
  - **可核验依据**：换行排版一致；探索用远行传送门术语一致；对堡垒暗影向玩家汇报的语气还原准确。

- **entry-01458** (`mod-tome.lua:20613`)
  - **原文**：`The fortress is not found!`
  - **译文**：`找不到堡垒！`
  - **复核结论**：未发现问题
  - **可核验依据**：源码 `shertul-fortress.lua:205`，堡垒飞行模式退出时未定位到堡垒实体的警告日志，感叹号保留，简洁明了。

- **entry-01459** (`mod-tome.lua:20619`)
  - **原文**：`Enter the caverns of Ardhungol and look for Sun Paladin Rashim.`
  - **译文**：`进入阿尔德胡格山洞寻找太阳骑士拉希姆。`
  - **复核结论**：未发现问题
  - **可核验依据**：Sun Paladin 译为“太阳骑士”，Ardhungol 译为“阿尔德胡格”，caverns 遵循地貌实体子类型规范译为“山洞”，专名与文意全合。

- **entry-01460** (`mod-tome.lua:20620`)
  - **原文**：`But be careful; those are not small spiders...`
  - **译文**：`当心，那里的蜘蛛个头可不小……`
  - **复核结论**：未发现问题
  - **可核验依据**：分号转为逗号符合中文行文习惯，省略号转换为全角中文省略号，语气自然生动。

- **entry-01461** (`mod-tome.lua:20630`)
  - **原文**：`Deep in the Dreadfell you fought and destroyed the Master, a powerful vampire.`
  - **译文**：`在恐惧王座深处你与领主——一个强大的吸血鬼——战斗并消灭了他。`
  - **复核结论**：未发现问题
  - **可核验依据**：核验 `mod-tome.lua` 全文及 `staff-absorption.lua`，恐惧王座最终 BOSS“The Master”全仓库统一称谓为“领主”（如“杀死恐惧王座的领主”等）；破折号夹注符合同位语规范；Dreadfell 规范译为“恐惧王座”。

- **entry-01462** (`mod-tome.lua:20631`)
  - **原文**：`On your way out of the Dreadfell you were ambushed by a band of orcs.`
  - **译文**：`当你走出恐惧王座的时候你受到了一队兽人小队的偷袭。`
  - **复核结论**：细微观察
  - **可核验依据**：句中“一队兽人小队”存在量词与中心语轻微语意重复（“一队……小队”，后文第 20633 行同义句写作“一队兽人伏击”），修辞上略显赘余，但主要信息明确无重大事实错误。

- **entry-01463** (`mod-tome.lua:20634`)
  - **原文**：`They asked about the staff and stole it from you.`
  - **译文**：`他们从你那里得知了法杖的消息，把法杖抢走了。`
  - **复核结论**：存在疑点
  - **可核验依据**：
    1. 原文为 `They asked about the staff and stole it from you.`，即兽人们盘问/索要法杖并将法杖抢走；同 section 第 20632 行 `They asked about the staff.` 即正确译为“他们问起了法杖的事。”。
    2. 核验剧情对话 `dreadfell-ambush.lua:24`，乌克鲁克一登场便质问索要法杖（“Give us the staff NOW”），兽人本已知悉法杖所在，绝非“从玩家处得知法杖消息”；
    3. 核验源码 `staff-absorption.lua:36` 与 `mod-tome.lua:20636`，玩家在后续日志中明确说明“你什么也没告诉他们”（`You told them nothing and vanquished them.`），本句若译为“他们从你那里得知了法杖的消息”，与后文直接产生严重的事实逻辑冲突。建议修正为“他们盘问了法杖的事，并把法杖从你手中抢走了。”。

- **entry-01464** (`mod-tome.lua:20637`)
  - **原文**：`In its remains, you found a strange staff. It radiates power and danger and you dare not use it yourself.`
  - **译文**：`在他的尸体上，你发现了一根奇怪的法杖，它辐射出的力量和危险使你不敢使用它。`
  - **复核结论**：细微观察
  - **可核验依据**：“radiates power and danger”直译为“辐射出的力量和危险”，在中文奇幻语境下略带物理科技术语式的直译色彩（常作“散发着强大而危险的气息/力量与危险”），但整体文意传达准确，不构成阻断性缺陷。

---

#### 三、复核总结

本批次共 40 条条目，复核发现：
- **存在实质疑点（2 条）**：
  1. `entry-01432`：目的从句译文引入无对应主语“他让”（疑似错字“好让”或冗余重构）。
  2. `entry-01463`：将 `asked about the staff` 误译为“从你那里得知了法杖的消息”，曲解兽人盘问/索取语义，并与后续剧情“你什么也没告诉他们”产生逻辑矛盾。
- **细微观察/用词修辞建议（4 条）**：
  1. `entry-01438`：gems 译为“珠宝”而非“宝石”，且 ancient tome 弱化译为“旧书”。
  2. `entry-01450`：`Till the Blood Runs Clear` 直译为“直到鲜血流清”，略带字面直译痕迹。
  3. `entry-01462`：“一队兽人小队”存在量词重复赘余。
  4. `entry-01464`：radiates 译作“辐射出”略带直译腔。
- **其余 34 条条目**：占位符、颜色代码、换行符、标点及专业术语（包括 Ziguranth、exploratory farportal、The Master、Ardhungol 等）均核验准确，标记为「未发现问题」。