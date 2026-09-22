### batch-050 译文复核报告

- **复核批次**：batch-050（entry-01385 至 entry-01424，共 40 条）
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-050.md`
  - SHA-256：`2f9a763f3085db79fa7a12259751ba80c9e035b2ba8857028aecaa2747844005`（核对一致）
- **核验依据**：
  - 公开引擎与本体源码：`/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 译文参照版本：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（仅限同 section 译文语境）
  - 术语参照：本批冻结术语快照与源码事实

---

#### 逐条复核记录

##### entry-01385
- **位置**：`mod-tome.lua:20178`（section: `mod-tome/data/quests/charred-scar.lua`）
- **原文**：`Use the portal to go back to the Far East. You *MUST* stop them, no matter the cost.`
- **译文**：`使用传送门到达远东大陆，你必须阻止他们，不惜一切代价。`
- **复核结论**：细微观察
- **依据**：
  1. 动词方向性：玩家是在远东发现双魔通过传送门前往灼烧之痕吸收遗迹魔法后赶回马基·埃亚尔阻止仪式，此处指仪式告一段落后“返回/回到远东”，译文“到达远东大陆”弱化了“go back to（返回/回到）”的前后剧情连贯性；
  2. 格式强调：原文中对代词的强调标记 `*MUST*` 在译文中未保留星号或加粗。

##### entry-01386
- **位置**：`mod-tome.lua:20179`（section: `mod-tome/data/quests/charred-scar.lua`）
- **原文**：`You arrived in time and interrupted the ritual. The sorcerers have departed.`
- **译文**：`你终于及时赶来阻止了仪式，法师们被驱散了。`
- **复核结论**：存在疑点
- **依据**：
  - 核心动词错译：原文“The sorcerers have departed”是指两名法术大师（Elandar 与 Argoniel）已经通过传送门离开/撤离了（源码 `charred-scar.lua:68`：`The Sorcerers flee through a portal`；同文件 `mod-tome.lua:20180` 中同词亦译为“巫师们已经离开”）。译文作“法师们被驱散了”将“离开/离去（departed）”误译为“驱散（dispelled/dispersed）”，不符合剧情事实。

##### entry-01387
- **位置**：`mod-tome.lua:20180`（section: `mod-tome/data/quests/charred-scar.lua`）
- **原文**：`#VIOLET#A portal activates in the distance. You hear the orcs shout, 'The Sorcerers have departed! Follow them!'`
- **译文**：`#VIOLET#远处一个传送门被激活，你听到兽人们吼道：“巫师们已经离开！跟上他们！”`
- **复核结论**：未发现问题
- **依据**：颜色代码 `#VIOLET#` 完整保留，台词引用标点正确，“The Sorcerers have departed”准确译作“巫师们已经离开”，语义忠实。

##### entry-01388
- **位置**：`mod-tome.lua:20181`（section: `mod-tome/data/quests/charred-scar.lua`）
- **原文**：`#VIOLET#The Sorcerers flee through a portal. As you prepare to follow them, a huge faeros appears to block the way.`
- **译文**：`#VIOLET#巫师们从传送门逃跑了，当你准备跟随他们时，一个巨大的法罗挡住了去路。`
- **复核结论**：未发现问题
- **依据**：颜色代码 `#VIOLET#` 完好，实体译名“法罗（faeros）”与游戏全局一致，剧情叙述流畅。

##### entry-01389
- **位置**：`mod-tome.lua:20192`（section: `mod-tome/data/quests/deep-bellow.lua`）
- **原文**：`Your escape from Reknor got your heart pounding and your desire for wealth and power increased tenfold.`
- **译文**：`你从瑞库纳逃了出来，你觉得你的心脏狂跳不止，你对财富和力量的渴望增加了十倍～。`
- **复核结论**：存在疑点
- **依据**：
  - 标点与语域异常：译文句尾出现多余波浪号“～”（“增加了十倍～。”），原文仅为常规英文句号 `.`；在严肃奇幻任务叙述中添加波浪号不符合风格规范。

##### entry-01390
- **位置**：`mod-tome.lua:20193`（section: `mod-tome/data/quests/deep-bellow.lua`）
- **原文**：`Maybe it is time for you to start an adventurer's career. Deep below the Iron Throne mountains lies the Deep Bellow.`
- **译文**：`也许是你开始冒险生涯的时候了，在钢铁王座山脉的深处有个叫深渊咆哮的地下城。`
- **复核结论**：未发现问题
- **依据**：专名“钢铁王座（Iron Throne）”符合术语快照，“深渊咆哮（Deep Bellow）”与全库地名一致，意译自然。

##### entry-01391
- **位置**：`mod-tome.lua:20194`（section: `mod-tome/data/quests/deep-bellow.lua`）
- **原文**：`It has been long sealed away but still, from time to time adventurers go there looking for wealth.`
- **译文**：`那里已被尘封已久，但是还是不断有冒险者前去寻找财宝。`
- **复核结论**：细微观察
- **依据**：“已被尘封已久”存在“已……已久”语法重叠语病（宜为“被尘封已久”或“早已尘封”）；“from time to time”（时常/时不时）译为“不断有”稍有强化，但基本达意。

##### entry-01392
- **位置**：`mod-tome.lua:20195`（section: `mod-tome/data/quests/deep-bellow.lua`）
- **原文**：`None that you know of has come back yet, but you did survive Reknor. You are great.`
- **译文**：`据你所知没有一个人能活着回来，不过你从瑞库纳幸存了下来，你比较牛 X。`
- **复核结论**：存在疑点
- **依据**：
  - 语域失调与粗俗俚语：原文“You are great.”为常规客观赞赏（“你很了不起/你实力超群”），译文使用了市井粗俗网络俚语“你比较牛 X。”，破坏了 RPG 奇幻任务文本的基本语域基调，且凭空加入了弱化程度副词“比较”。

##### entry-01393
- **位置**：`mod-tome.lua:20201`（section: `mod-tome/data/quests/dreadfell.lua`）
- **原文**：`You have heard that near the Charred Scar, to the south, lies a ruined tower known as the Dreadfell.`
- **译文**：`你听说在灼烧之痕南部有一个叫做恐惧王座的荒塔废墟。`
- **复核结论**：未发现问题
- **依据**：专名“灼烧之痕”与“恐惧王座（Dreadfell）”均与术语快照及大地图定位一致，译文准确。

##### entry-01394
- **位置**：`mod-tome.lua:20202`（section: `mod-tome/data/quests/dreadfell.lua`）
- **原文**：`There are disturbing rumors of greater undead, and nobody who reached it ever returned.`
- **译文**：`传说那里有强大的亡灵生物，凡是到达那里的人都有去无回。`
- **复核结论**：未发现问题
- **依据**：“greater undead”译作“强大的亡灵生物”（符合术语亡灵），“有去无回”成语贴切传神，语义完整。

##### entry-01395
- **位置**：`mod-tome.lua:20203`（section: `mod-tome/data/quests/dreadfell.lua`）
- **原文**：`Perhaps you should explore it and find the truth, and the treasures, for yourself!`
- **译文**：`也许你应该去那里一探究竟，顺便可以找到埋藏在那里的财宝！`
- **复核结论**：未发现问题
- **依据**：句意完整通畅，感叹号匹配，“一探究竟”贴合“find the truth”。

##### entry-01396
- **位置**：`mod-tome.lua:20208`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`Back and there again`
- **译文**：`归而复往`
- **复核结论**：未发现问题
- **依据**：严格遵循术语快照 preferred 条目（`Back and there again -> 归而复往`），准确呈现托尔金典故倒装。

##### entry-01397
- **位置**：`mod-tome.lua:20209`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`You have created a portal back to Maj'Eyal. You should try to talk to someone in Last Hope about establishing a link back.`
- **译文**：`你创造了一个回到马基·埃亚尔的传送门，你应该试试找最后的希望的某个人谈谈建立返回通路的事。`
- **复核结论**：未发现问题
- **依据**：专名“马基·埃亚尔”、“最后的希望”符合术语规范，目标指引清晰准确。

##### entry-01398
- **位置**：`mod-tome.lua:20210`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`You talked to the Elder in Last Hope who in turn told you to talk to Tannen, who lives in the north of the city.`
- **译文**：`你和最后的希望的长者交谈，得知要去找城市北边的泰恩。`
- **复核结论**：未发现问题
- **依据**：人物名“泰恩（Tannen）”符合 preferred 术语，地名准确，句式精简通顺。

##### entry-01399
- **位置**：`mod-tome.lua:20214`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`You brought back the diamond and athame to Tannen who asked you to contact Zemekkys to ask some delicate questions.`
- **译文**：`你把共鸣钻石和仪式匕首带回给泰恩；他让你联系泽梅基斯，询问一些敏感问题。`
- **复核结论**：未发现问题
- **依据**：“athame”准确译为 preferred 术语“仪式匕首”，“diamond”准确结合剧情道具全名补足为“共鸣钻石”，人名“泰恩”、“泽梅基斯”规范。

##### entry-01400
- **位置**：`mod-tome.lua:20216`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`Tannen has tricked you! He swapped the orb for a false one that brought you to a demonic plane. Find the exit, and get revenge!`
- **译文**：`泰恩把你耍了！他换了个错的水晶球给你，把你传送到了恶魔的空间，找到出口回去找他算账！`
- **复核结论**：存在疑点
- **依据**：
  - 核心词义偏差：原文“swapped the orb for a false one”是指泰恩用伪造的赝品/假水晶球（源码对应道具 `ORB_MANY_WAYS_DEMON`）调包了玩家的多元水晶球；译文“换了个错的水晶球”容易理解为误拿或操作失误（wrong one），而非恶意伪造掉包（false/fake one）；此外“demonic plane”译作“恶魔的空间”略显口语化，游戏通常统一为“恶魔位面”。

##### entry-01401
- **位置**：`mod-tome.lua:20217`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`Tannen revealed himself as the vile scum he really is and trapped you in his tower.`
- **译文**：`泰恩暴露出了他的确是个卑鄙的人渣，他把你囚禁在他的塔牢里。`
- **复核结论**：未发现问题
- **依据**：人名统一，情感色彩强烈且符合剧情转折（源码中切换至关卡 `tannen-tower`），表意准确。

##### entry-01402
- **位置**：`mod-tome.lua:20220`（section: `mod-tome/data/quests/east-portal.lua`）
- **原文**：`A portal appears in the center of the tower!`
- **译文**：`在塔的中间出现了一个传送门！`
- **复核结论**：未发现问题
- **依据**：弹窗提示文本准确，感叹号一致。

##### entry-01403
- **位置**：`mod-tome.lua:20233`（section: `mod-tome/data/quests/escort-duty.lua`）
- **原文**：`As a reward you %s.`
- **译文**：`作为奖励，你%s。`
- **复核结论**：未发现问题
- **依据**：占位符 `%s` 保持完整，源码中注入的 `self.reward_message` 为动宾短语（如“提升了力量 +1”），拼接后语法完全契合。

##### entry-01404
- **位置**：`mod-tome.lua:20236`（section: `mod-tome/data/quests/escort-duty.lua`）
- **原文**：`Escort the %s to the recall portal on level %s.`
- **译文**：`将%s护送到%s的召回传送门。`
- **复核结论**：未发现问题
- **依据**：
  1. 占位符数量与参数顺序严格一致：第一个 `%s` 为被护送目标 NPC 称谓，第二个 `%s` 为楼层名 `self.level_name`；
  2. 设施名“召回传送门（Recall Portal）”严格遵循 preferred 术语规范（非“回归传送门”）。

##### entry-01405
- **位置**：`mod-tome.lua:20255`（section: `mod-tome/data/quests/grave-necromancer.lua`）
- **原文**：`You have tracked Celia to her husband's mausoleum in the graveyard near Last Hope. It seems she has taken some liberties with the corpses there.`
- **译文**：`你跟踪赛利亚，找到了她亡夫位于最后的希望附近墓地中的陵墓。看来她对那里的尸体做了些出格的事。`
- **复核结论**：未发现问题
- **依据**：地名“最后的希望”正确，“taken some liberties with the corpses”委婉语转化为“做了些出格的事”生动得当。

##### entry-01406
- **位置**：`mod-tome.lua:20256`（section: `mod-tome/data/quests/grave-necromancer.lua`）
- **原文**：`You have laid Celia to rest, putting an end to her gruesome experiments.`
- **译文**：`你埋葬了赛利亚，终结了她阴森恐怖的实验。`
- **复核结论**：未发现问题
- **依据**：“laid ... to rest”译作“埋葬了/使……安息”契合剧情，句式工整，无语病。

##### entry-01407
- **位置**：`mod-tome.lua:20257`（section: `mod-tome/data/quests/grave-necromancer.lua`）
- **原文**：`You have laid Celia to rest, putting an end to her failed experiments. You have taken her heart, for your own experiments. You do not plan to fail as she did.`
- **译文**：`你埋葬了赛利亚，终结了她失败的实验，你拿走了她的心脏为自己的实验做准备，你相信你不会重蹈她的覆辙。`
- **复核结论**：未发现问题
- **依据**：死灵法师专属完成描述传达准确，多句自然衔接，“重蹈覆辙”语义对应精准。

##### entry-01408
- **位置**：`mod-tome.lua:20263`（section: `mod-tome/data/quests/high-peak.lua`）
- **原文**：`You have vanquished the masters of the Orc Pride. Now you must venture inside the most dangerous place of this world: the High Peak.`
- **译文**：`你征服了兽人军团的最高领袖，现在你必须向这个世界最危险的地方挺进：巅峰。`
- **复核结论**：存在疑点
- **依据**：
  1. 阵营专名分歧：原文“Orc Pride”在术语库中固定为“兽人部落”（快照行 504 `Orc Pride -> 兽人部落`；同文件第 20282 行亦译为“兽人部落”），此处译作“兽人军团”造成同任务内专名不一致；
  2. 动词偏差：“vanquished”（击败/铲除）译作“征服了”，与剧情中斩杀四大部落首领的实际行动稍有偏差。

##### entry-01409
- **位置**：`mod-tome.lua:20264`（section: `mod-tome/data/quests/high-peak.lua`）
- **原文**：`Seek the Sorcerers and stop them before they bend the world to their will.`
- **译文**：`找到那些妄图扭曲这个世界的法师并阻止他们。`
- **复核结论**：细微观察
- **依据**：原文“bend the world to their will”（使世界屈从于他们的意志/按其意志重塑世界）意译为“妄图扭曲这个世界”，意思基本传达，但略微改变了原句强调“顺从其意志”的主旨。

##### entry-01410
- **位置**：`mod-tome.lua:20265`（section: `mod-tome/data/quests/high-peak.lua`）
- **原文**：`To enter, you will need the four orbs of command to remove the shield over the peak.`
- **译文**：`想要进去的话，你必须找到那四个指令水晶来移除塔顶的防护罩。`
- **复核结论**：存在疑点
- **依据**：
  1. 地理事实错译：原文“the peak”指巅峰（High Peak，埃亚尔最高雪山），护盾笼罩的是整座山峰/峰顶；译文将其译作“塔顶”，误将山峰当成高塔（可能与恐惧王座或泰尔玛高塔混淆），属于事实性地理错译；
  2. 道具名称不完整：“orbs of command”对应游戏内四件剧情宝物（`Orb of Undeath/Dragon/Elemental/Destruction (Orb of Command)`），其规范译名为“指令水晶球”，此处译作“指令水晶”丢失了“球/宝珠（orb）”的核心实体词。

##### entry-01411
- **位置**：`mod-tome.lua:20268`（section: `mod-tome/data/quests/high-peak.lua`）
- **原文**：`You have won the game!`
- **译文**：`你通关了！`
- **复核结论**：未发现问题
- **依据**：符合中文游戏常规表述，感叹号匹配。

##### entry-01412
- **位置**：`mod-tome.lua:20321`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`Kyless, the one who brought the curse, is dead by your hand.`
- **译文**：`凯勒斯，那个曾经为你带来诅咒的人，死在了你的手上。`
- **复核结论**：未发现问题
- **依据**：人物名采用最新裁定 preferred 术语“凯勒斯”（取代旧译“克里斯”），句式符合中文表达。

##### entry-01413
- **位置**：`mod-tome.lua:20327`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#LIGHT_GREEN#Seek out Kyless' cave in the northern part of the meadow and end him. Perhaps the curse will end with him.`
- **译文**：`#LIGHT_GREEN#找出位于草原北部的凯勒斯的洞穴，然后杀掉他，他的死也许会解除这个诅咒。`
- **复核结论**：未发现问题
- **依据**：颜色标签 `#LIGHT_GREEN#` 完整，专名“凯勒斯”一致，语义准确。

##### entry-01414
- **位置**：`mod-tome.lua:20329`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#LIGHT_GREEN#You may have to revist your past to unlock some secret buried there.`
- **译文**：`#LIGHT_GREEN#你可能需要重访过去，以解开埋藏在那里的秘密。`
- **复核结论**：未发现问题
- **依据**：颜色标签无损，正确理解了英文原文源码拼写错误（revist -> 重访过去），翻译规范。

##### entry-01415
- **位置**：`mod-tome.lua:20337`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#VIOLET#You have begun your hunt for Kyless!`
- **译文**：`#VIOLET#你开始追杀凯勒斯！`
- **复核结论**：未发现问题
- **依据**：颜色代码 `#VIOLET#` 与感叹号一致，专名“凯勒斯”正确。

##### entry-01416
- **位置**：`mod-tome.lua:20338`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#VIOLET#You have a marker to the entrance of Kyless' cave!`
- **译文**：`#VIOLET#你获得了通往凯勒斯洞穴入口的标记！`
- **复核结论**：未发现问题
- **依据**：日志颜色代码与标点完整，文意准确。

##### entry-01417
- **位置**：`mod-tome.lua:20339`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#VIOLET#You have found the entrance to Kyless' cave!`
- **译文**：`#VIOLET#你找到了通往凯勒斯洞穴的入口！`
- **复核结论**：未发现问题
- **依据**：颜色标签正确，专名与标点规范。

##### entry-01418
- **位置**：`mod-tome.lua:20343`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`You recognize this door as the entrance to a second vault. There are some scuffling noises and heavy breathing coming from the other side of the door.`
- **译文**：`你认出来这扇门是通向另一处宝库的门户。你可以听到门的另一边有拖曳的脚步声和沉重的呼吸声。`
- **复核结论**：未发现问题
- **依据**：地图机制“vault”译作“宝库”，细节“拖曳的脚步声和沉重的呼吸声”准确对应猎犬守卫异动，文意通顺。

##### entry-01419
- **位置**：`mod-tome.lua:20344`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#VIOLET#You have found Kyless. You must destroy him.`
- **译文**：`#VIOLET#你找到了凯勒斯，你必须杀死他。`
- **复核结论**：未发现问题
- **依据**：颜色代码保留完整，专名规范，表意明确。

##### entry-01420
- **位置**：`mod-tome.lua:20345`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`Death of Kyless`
- **译文**：`凯勒斯之死`
- **复核结论**：未发现问题
- **依据**：对话弹窗标题简明准确，专名一致。

##### entry-01421
- **位置**：`mod-tome.lua:20346`（section: `mod-tome/data/quests/keepsake.lua`）
- **原文**：`#VIOLET#Kyless is dead.`
- **译文**：`#VIOLET#凯勒斯死了。`
- **复核结论**：未发现问题
- **依据**：日志短句与颜色代码均完整匹配。

##### entry-01422
- **位置**：`mod-tome.lua:20353`（section: `mod-tome/data/quests/kryl-feijan-escape.lua`）
- **原文**：`The Sect of Kryl-Feijan`
- **译文**：`克里尔·费扬教派`
- **复核结论**：未发现问题
- **依据**：恶魔专名“克里尔·费扬”与全库统一，任务名结构无误。

##### entry-01423
- **位置**：`mod-tome.lua:20354`（section: `mod-tome/data/quests/kryl-feijan-escape.lua`）
- **原文**：`You discovered a sect worshipping a demon named Kryl-Feijan in a crypt.`
- **译文**：`你在一个地宫中发现了一个崇拜名为克里尔·费扬的恶魔的教派。`
- **复核结论**：未发现问题
- **依据**：地下城名词“地宫（crypt）”与对应地图“克里尔·费扬地宫”一致，语法层次清晰。

##### entry-01424
- **位置**：`mod-tome.lua:20357`（section: `mod-tome/data/quests/kryl-feijan-escape.lua`）
- **原文**：`You failed to protect her when escorting her out of the crypt.`
- **译文**：`你没能成功地将她护送出这个地宫。`
- **复核结论**：细微观察
- **依据**：原文为“failed to protect her when escorting her out of the crypt”（在护送她离开地宫时未能保护好她），译文略去了主要谓语“protect her”，意译为“没能成功地将她护送出这个地宫”；尽管游戏机制上梅琳达被杀即意味着护送失败，但若能明确“未能保护她”会更紧扣原文失败原因。

---

#### 总结统计
- 复核总数：40 条（entry-01385 至 entry-01424）
- **未发现问题**：32 条
- **细微观察**：3 条（entry-01385、entry-01391、entry-01409、entry-01424 中有 3 处细微观察，entry-01385 兼具语境观察）
- **存在疑点**：5 条
  - `entry-01386`：“departed”（离开/离去）错译为“被驱散了”；
  - `entry-01389`：句尾存在多余波浪号“十倍～。”；
  - `entry-01392`：“You are great.”被翻译为市井粗俗俚语“你比较牛 X。”；
  - `entry-01400`：“a false one”（假水晶球/赝品）误译为“错的水晶球”；
  - `entry-01408`：“Orc Pride”偏离统一阵营术语“兽人部落”误作“兽人军团”；
  - `entry-01410`：“the peak”误译为“塔顶”（巅峰为山峰非高塔），且“orbs of command”简漏为“指令水晶”（应为“指令水晶球”）。