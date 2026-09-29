# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03533–entry-03572 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g10-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以可核验的实际源码行为为准。本体固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。
3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。
4. 追调用链时，本体只能git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03533 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03533
位置：tome-cults.lua:1375；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]Over time the Nargol Kingdom apparently caught the ones behind those twisted incidents I had witnessed, and more that followed after I left. They publicly executed those who they believed to be the culprits and planted their heads on stakes within the walls of the city. Despite this though, burning events and other depraved actions would begin to be taken up by the citizenry itself. The messengers may have been killed, but the message they spread persisted.[/i]

Abruptly before giving the halfling even a moment to respond, the human seemingly began raving at the halfling saying, "You don't seriously mean to spare her? She's in league with the Shaloren, she's in league with magic!" The humans tone progressively got more emotional as the tirade continued, "Have you forgotten our mission and what we are charged to do. This THALORE has turned HER BACK on NATURE! She Must Di-" The human stopped talking as the halfling raised a hand up in a motion to stop and in a deeper tone than what I would expect from someone of such a small size, calmly replied back, "Enough." The human’s body shrank back at this, and though masked I could sense the disbelief and dismay from the body language.

The halfling put down the hand before finally responding with an explanation, stating, "Our mission is to root out the foul practitioners of the arcane and to make sure no further tragedies occur from magic's failings." The halfling took a deep breath before continuing to say, "This thalore is no spellcast-." The human abruptly cut off the halfling from speaking to yell with great fury, "SO WHAT!? She has associated with the Shaloren! THE ONES WHO CAUSED THE SPELL-" Once again the halfling put up a hand and again the human ceased to talk. Finally silent, the halfling put down the hand and I slowly felt some of the pressure on me relax. Somewhat tensely, the human finally turned away in disgust before heading towards entrance to the tent.

As the human left, I could feel the halfling proceed to get off of me and step away. Slowly I made to get up as the halfling turned its head to look in my direction. As I came to my feet I decided to ask, "Who are you really?" Turning its body fully towards me, the halfling seemingly paused a moment before answering me, "Do you wish to truly know?" It was my turn to pause as this question was put to me. These fanatics had been responsible for the sickening spectacle that I had witnessed outside. I was also now angry due to my treatment within the tent, now seemingly driving me to seek out an explanation. Finally replying to the halfling I replied, "I want to know why."

The halfling remained silent, emotions covered by the mask, and body language indicating nothing to me either. The only thing I could tell about the halfling was the military attire being worn. I noticed what seemed like a complete set of leather armor with gloves and boots included. Seemingly we merely stood looking at each other not saying anything. Was the halfling perhaps looking for something within me? I don't know. What I can tell you with each passing moment I was becoming angrier and more full of rage inside. Having enough of the silence and wanting my answer, I was about to begin shouting before at last the halfling stated, "Because nature has suffered enough, has it not?"

The sentence that was uttered struck deeply. I was immediately reminded of the reasons I had headed down to Elvala, of the rage and anger that had driven me to make the journey. But the actions of these masked individuals seemed less about exacting revenge for the wrong done to nature. No, it seemed closer to a vendetta against magic, and with the Spellblaze came an excuse to kill the practitioners of magic and destroy their works. Regaining my composure I replied, “Does that justify killing the innocent?" To this I could feel a dark emotion rise from the halfling. I had truly hit a nerve within the halfling. In the instant after that though, all I could feel was pain.

I didn't even see the halfling move, before I felt the punch connect with my stomach. Looking down I saw the halfling below just as a fist connected with the bottom of my jaw. Stunned by the blow I stumbled a bit before falling down. Now looking up at the halfling, I could see the rage emanating towards me, towards the words I had just uttered. "Innocent? There is no innocence in those who pervert nature and her design. There can be no forgiveness for them either." I should have been afraid of the halfling at this point, but the anger inside me fueled me to go forward. As I got to my feet I fired back, "Does that justify the atrocious display I saw outside then? To take random people from their homes, charge them with what you see as wrongdoings, and then execute them in a fiery display?"

The halfling dropped to a less hostile stance and replied, "If you are referring to the people we named, then know that they were all defilers of nature. Potion brewers, runemasters, a blacksmith who specialized in magical artefact creation, and more than a dozen mages capable of casting spells. We have done great care in identifying various users who twist nature to their whims..." The halfling trailed off to take a breath before continuing with the final sentence. "As for how we killed them, a message needs to be sent, to be seared into the hearts and minds of the citizens of this city and elsewhere. Perhaps you may not have the stomach for it, if so I suggest you go back to your little forest thalore. This won't be the last display you will likely see."

I don't know what made me more angry at that point, the seemingly callous nature of the halfling or the suggestion to simply go back home. What I did know was that I was livid. Seemingly the halfling noticed this and tried to reorient its posture. Attempting to redirect my anger, the halfling quickly opined, "Of course, you seem like you are made of sterner composition than most. Head to the south shoreline, then turn east. You'll find a path leading towards our base." Registering the words I took a moment to analyze them in my head, before asking, "And why should I do that?" Without missing a beat the halfling quickly replied back, "You wish to know why, do you not? Go talk to our instructors if you truly wish to know who we are."

With this the halfling turned to leave the tent. The anger within me had not subsided much, but I made no further attempt to confront the halfling. Battered and bruised I sank down to the ground and rested a moment. Pulling one of the infusions I had recently purchased from the market, I began to treat my wounds. When I felt I was in better shape I got up again and left the tent. Looking up I noticed the evening sky, and decided that I would be staying one more night in the Nargol Kingdom. I made my way back to the inn where I slept in a bed until the next day. When I left I headed straight to the gates of the city to make my way out. There I pondered where my next destination would be, before finally heading south.
```
译文：
```text
[i]过了一段时间，纳格尔王国似乎抓住了我所目睹的那些扭曲事件的幕后黑手，而在我离开后，更多的事情接踵而至。他们公开处决了那些他们认为是罪魁祸首的人，并把他们的头插在城墙内的木桩上。尽管如此，市民开始自发发动火刑事件和其他各种堕落行为。信使的同伙们可能已经被杀了，但他们传播的信息仍然存在。[/i]

在半身人还没有来得及回应之前，人类开始对半身人大吼道：“你不是真的想饶了她吗？她是和永恒精灵一伙的，是和魔法一伙的！”，人类的语气变得越来越情绪化，“你是否忘记了我们的使命，忘记了我们要做的事情。这个自然精灵已经背叛了大自然！她必须被…”人类突然停止了说话，只见半身人举起一只手示意停下，用比我对这么小个儿的人所期望的更深沉的语调，平静地回答说：“够了。”人类一下子退缩了，虽然他戴着面具，但我能感觉到他身体语言的不信任和沮丧。

半身人放下手，最后做出解释，说：“我们的任务是铲除邪恶的奥术使用者，并确保不再因为魔法的失败引发悲剧。”半身人深吸一口气，然后继续说，“这个自然精灵不是施法者——”人类突然打断了半身人的说话，愤怒地喊道，“那又怎样！？她和永恒精灵有联系！那些引起魔法大——”半身人再一次举起手来，人类再一次停止说话。四周一片寂静，半身人放下了手，我慢慢感觉到了对我的压力稍稍放松了一些。在紧张的气氛中，人类终于厌恶地转过身去，然后走向帐篷的入口。

在人类离开后，我能感觉到半身人从我的身上起来，走开了。我慢慢地站起来，半身人转过头看着我的方向。在我站起来后，决定问：“你到底是谁？”半身人把身子完全转向我，似乎停了一会儿才回答我：“你真的想知道吗？”当被问到这个问题之后，我了停下来。这些狂热分子对我在外面看到的令人作呕的景象负有责任。而我在帐篷里的待遇也让我充满了愤怒，但这愤怒现在似乎驱使我寻找一个解释。最后我回答半身人说：“我想知道为什么。”

半身人保持沉默，他的面具掩盖着情绪，肢体语言对我也毫无意义。关于半身人，我唯一能说的就是他所穿的军装。我注意到他好像穿着一套完整的皮甲，包括手套和靴子。我们似乎只是站在那里看着对方，什么也没说。那个半身人是不是在找我内心的东西？我不知道。我能告诉你的是，随着时间的流逝，我内心变得越来越愤怒。我受够了沉默，想要得到回答，我正要开始喊叫，这时半身人说：“因为大自然已经受够了，不是吗？”

我被那句话深深地打动了，我想起了我去埃尔瓦拉的原因，想起了驱使我踏上旅程的仇恨与愤慨。但这些蒙面人的所作所为，似乎并不是为了报复对自然的错误。不，这似乎更像是对魔法的仇杀，以魔法大爆炸作为借口，以此开展杀死魔法使用者并摧毁他们作品的恶行。我恢复了镇静，回答说：“难道为此滥杀无辜也是对的吗？”这时，我能感觉到一种黑暗的情绪从半身人身上升起。我真的戳到了那个半身人的弱点。在那之后的一瞬间，我所能感觉到的只是疼痛。

我甚至没看到半身人的动作，就感觉到一拳打在了我的肚子上。我向下看，看到下方的半身人又是一拳打中我的下巴。我被那一击震慑，跌跌撞撞地摔倒了。现在我抬头看那半身人，感受到他朝我释放的愤怒，不断朝着我刚才说的那些话涌来。“无辜？那些歪曲自然和她的设计的人是没有清白的。他们也永远不能被原谅。”我本应该害怕半身人的，但我内心的愤怒促使我向前。当我站起身来时，我回击道：“那难道能证明，我当时在外面看到的残暴的表演是正当的？把无辜的人从他们的家里带走，指控他们做了你认为是错误的事，然后在火刑架上处决他们？”

半身人摆出了一个不那么敌对的姿态，回答说：“如果你指的是我们名单上的那些人，你就知道，他们都是自然的亵渎者。药水酿造师，符文师，一个专门制作魔法工艺品的铁匠，还有十几个能够施法的法师。我们非常小心地识别出各种各样的魔法使用者，他们把自然扭曲成自己的突发奇想……”半身人拖着脚步喘口气，然后继续念最后一句话。“至于我们如何杀死他们，我们需要发出一个信息，让这个城市和其他地方的市民铭记在心。也许你对它没有胃口，如果是这样的话，我建议你回到你的小森林去，自然精灵。这将不会是你可能看到的最后一次展示。”

我不知道是什么让我在那一点上更生气，是半身人冷酷无情的本性，还是他对我干脆回家的建议。我只知道我脸色发青。似乎半身人注意到了这一点，并试图调整自己的姿势。为了转移我的怒气，半身人很快地说：“当然，你看起来比其他人都要更加顽固。向南岸线走，然后向东拐。你会找到一条通向我们基地的路。”我把这些话记在脑子里，想了一会儿，然后问，“我为什么要这么做？”半身人毫不迟疑地回答道：“你想知道为什么，不是吗？如果你真的想知道我们是谁，就去和我们的导师谈谈。”

说完，半身人转身离开帐篷。我内心的愤怒并没有平息太多，但我没有进一步尝试去面对那个半身人。我遍体鳞伤，倒在地上休息了一会儿。我拿出一只市场上买的纹身，开始治疗伤口。当感觉到自己的身体状况好了一些时，我又站起来离开了帐篷。抬头一看，我看到了夜晚的天空，决定在纳格尔王国再住一晚。我回到旅店，在那里我直睡到第二天。当我离开时，我直奔城门出去。在那里，我考虑了一下下一步的目的地，最后决定向南走。
```

## entry-03534
位置：tome-cults.lua:1412；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 1] - Blackened Shoreline
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第1章] - 黑暗的海岸
```

## entry-03535
位置：tome-cults.lua:1413；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]Truly there was no place showing more damage in all of Eyal than its southern shoreline. Though I have not traveled to the eastern side of the continent, I can't imagine it potentially being destroyed to the extent that it has been here. These lands will never fully heal, but I do hope it will serve as a reminder the to Shaloren, to never brashly use magic in such a way again.[/i]

Following the travel instructions that I had received from the halfling, I proceeded south. I did not know why I didn't just travel north back home, something about the anger burning within me fueled me to find the instructors of these masked fanatics. As I traveled south the sky would begin to turn a shade of colors from blue to purple and then a blackish red, and before long I couldn't even see the sun anymore. There was no sign that any of the lands around me escaped the destructive energies of the Spellblaze here. Eventually after a full day of travel, I set up camp near some burnt out trees. There was little to forage for in the destroyed wilderness, but I was able to find some edible berries and mushrooms to feed myself with and save on my provisions.

The next day I continued on my journey. After a few hours I reached the southern shoreline, a grotesque sight to say the least. The waters bubbled as if being boiled and the ground was charred black. What trees or plants that still stood were completely burnt, dead and lifeless; as was the wildlife that had not escaped, their corpses left untouched by the bugs and worms. Looking up all I could see was dark clouds against a blackened sky. To the east I noticed small pools of lava escaping to the surface. Some of the lava formed small lakes or streams of red hot death which I cautiously had to avoid. Looking to the north I noticed the lands jaggedly shooting out unnaturally towards the sky.

Moving closer towards the raised landscape I noticed that they rose as high as a mountain in the distance. Climbing a hill I saw how the unnatural rocks formed twisting chasms and pointy spikes that would almost certainly be suicide to traverse. Remembering back to the shaloren soldiers I had treated in Elvala, I quickly realized why they had moved northwards to come home. The center of the continent where the Midvale Plains had been located were now no more. Now the plains had been replaced by this deadly gauntlet of rock that would certainly kill anyone inside it, and likely anyone who had been living on the plains before the Spellblaze.

Beginning to travel through the devastated landscape I had to be careful. As I made my way east the light of the sun was seemingly snuffed out by the smoke and debris of the area and the only way I could see my footing was from the glow of the nearby lava dotting the landscape. I don't know for how many days I would travel eastwards, but my progress though the lands was slow. Eventually I would see a river of lava flowing down to the open sea, and beyond that the burnt out remains of what I assumed was a forest. Seeing my way blocked, I looked north and noticed a clearing in the land and so I continued my way there to see if I could find safe passage.

I carefully made my way up the terrain to a plateau and saw a small opening appear in the jutted mountains up ahead. While the land I crossed was hilly, I was able to find decent footing through the lethal landscape of deadly drops and pitfalls. Slowly I made my way through, finding a path leading downwards into what I hope would lead to the other side. Suddenly though in the distance I could see the figure of a group advancing fast towards me. Drawing closer to me, one of the figures in the group saw me, yelled out to the others, and they slowed to a cautious crawl. As they approached, I was a bit of a miss as to what race these beings were.

They were tall, even taller than me, and I could see their bulging mass of muscles on their bodies from quite a distance away. Something also glistened on their skin, which as they grew closer I noticed to be glowing insignias similar to those I saw on runes in Elvala. Getting into earshot, one of the beings finally called out, "If you plan on taking us back, be prepared for a fight!" At that moment I realized that these were yet more victims of those masked fanatics. In a sign to show I wasn't hostile I put my belongings on the ground and stepped back from them. The action seemed to take the beings back a bit, and though still on edge they assumed a less aggressive stance.

"You aren't aligned at all with those zealots are you? My apologies for any distress we may have caused you." I merely shook me head as their words reached me, before proceeding to ask who they were and what had happened. "Never seen an ogre before I assume? We are, or we were, a nomadic tribe that wandered the lands as peddlers. Mostly we sold runes and infusions but we also sold other various small trinkets too. Then magic rained down from the sky and the earth opened up, destroying everything and killing many. We immediately went to help those we could in a nearby human city."

At this point tears began to stream down the ogres face. Continuing to speak between sobs the ogre continued, "I'm not sure why, but a small band attack us." At this point the ogre began to cry to the point that it was unable to speak, and seeing this another ogre continued, "We were bound in chains and taken to a small settlement just beyond this path. There we were subjected to insane experiments, something about 'cleansing us', and we witnessed a great many ogres die in grotesque and horrible ways. Realizing we would meet a similar fate we broke out of our bonds and made to escape from our cages." The ogre paused for a bit, looking behind me at the devastated landscape, then stated, "Although I'm not exactly sure where we may run to."
```
译文：
```text
[i]的确，在整个埃亚尔，没有一个地方比它的南部海岸线受到更大的破坏。虽然我还没有去过大陆的东边，但我无法想象它会被破坏到这样的程度。这里的土地永远不会完全愈合，我真的希望它能提醒人们，不要再以这种方式肆无忌惮地使用魔法。[/i]

按照半身人给我的旅行指示，我向南走去。我不知道为什么我不去北方回家，也许我内心的愤怒驱使我找到这些蒙面狂热者的导师。当我往南走的时候，天空开始从蓝色变成紫色，然后变成了暗红色，不久我甚至看不到太阳了。一切迹象表明，我周围没有任何一片土地逃脱了魔法大爆炸的侵袭。经过一整天的旅行，我终于在一些被烧毁的树旁安营扎寨。在被毁的荒野里，几乎没有什么可供觅食的东西，但我找到了一些可食用的浆果和蘑菇来养活自己，省下了我的粮食。

第二天我继续旅行。几个小时后，我到达了南部海岸，周围是一片怪诞的景象。水沸腾了，地面烧黑了。那些仍然屹立着的树木和植物被完全烧毁，死气沉沉；还有那些没有逃走的野生动物，它们的尸体里连虫子和蛆虫都没有。抬头一看，只见乌云密布在漆黑的天空中。在东面，我注意到有小的熔岩池溢出了地表。一些熔岩形成了小湖泊或炽热的死亡溪流，我不得不谨慎避开。往北望去，我注意到那些荒芜的土地不自然地向天空伸去。

向凸起的地貌走近时，我注意到它们像远处的一座山一样高。爬上一座小山，我看到了这些不自然的岩石是如何形成扭曲的裂缝和尖尖的尖刺的，想要穿越他们简直就是在自杀。回忆起我在埃尔瓦拉治疗过的永恒精灵士兵，我很快意识到他们为什么选择向北进军回家。米德瓦尔平原所在的大陆中心现在已经不复存在了。现在平原已经被这些致命的尖石所碾碎了，这个过程恐怕杀死了里面的所有人，很可能是在魔法大爆炸之前生活在平原上的任何物种。

开始穿越这片荒芜的土地时，我必须小心。当我往东走的时候，太阳的光芒似乎被这片区域的烟雾和碎片遮住了，唯一能让我看清自己脚下的，就是附近散布在这片土地上的熔岩的光辉。我不知道我会向东旅行多长时间，但我在这片荒芜土地上的旅程是极度缓慢的。最后，我看到一条熔岩河流入了公海，在那尽头，我看到了一片森林的烧尽的残骸。我觉察到路被堵住了，就往北看，注意到那里有一块空地，于是我继续往那儿走，看能否找到安全的通道。

我小心翼翼地向高原走去，看到前面突出的群峦中出现了一个小洞。虽然我穿越的土地是丘陵地带，但我成功地在致命的悬崖和峭壁的可怕景象中找到勉强可以立足的地方。我慢慢地走过去，找到了一条通向我希望通向的另一边的路。突然，我发现一个团体的身影正在向我快速前进，尽管还在远处。他们离我越来越近，其中一个人看见了我，向其他人高喊，他们放慢脚步，小心翼翼地前行。当他们走近时，我有点不明白这些家伙是什么种族的。

他们很高，甚至比我还高，我能从很远的地方看到他们身上隆起的肌肉。他们的皮肤上有着一些闪光的东西，当他们越来越近时，我注意到覆盖在他们身上的是闪光的纹样，和我在埃尔瓦拉的符文上看到的相似。在他们和我之间到了能够互相听到声音的时候，他们大声喊道：“如果你打算把我们带回去，就要做好和我们战斗的准备！”在那一刻，我意识到他们是那些蒙面狂热者的其他受害者。为了表示我没有敌意，我把我的东西放在地上，然后退后。这一举动似乎让他们后退了一点，尽管仍然和我对峙着，但他们采取了一种不那么咄咄逼人的姿态。

“你和那些狂热份子不是一伙的，对吗？我为我们可能给你带来的任何痛苦表示歉意。”听到他们的话，我摇了摇头，然后问他们是谁，发生了什么事。“看来你以前从没见过食人魔？我们是，或者说我们曾经是一个游牧部落，作为小贩在这片土地上游荡。我们主要卖符文和纹身，但我们也卖其他各种小饰品。突然间，魔法从天而降，大地裂开，摧毁了一切，杀死了许多人。我们立即前去帮助附近一个人类城市的人们。”

这时，泪水开始顺着食人魔的脸流下来。食人魔继续啜泣着说，“我不知道为什么，但是一只小队袭击了我们。”这时食人魔开始哭到说不出话来，另一个食人魔继续说，“我们被他们用铁链拷住，被带到了一个小定居点，就在这条路的另一边。在那里，他们在我们的身上进行了疯狂的实验，他们声称这是要‘净化我们’。我们目睹了很多食人魔以怪异和可怕的方式死去。意识到我们会遇到类似的命运，我们挣脱了束缚，从笼子里逃了出来。”食人魔停了一会儿，看着我身后那片被毁坏的土地，然后说，“尽管，我们也不知道我们还能跑到哪里去。”
```

## entry-03536
位置：tome-cults.lua:1446；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 2] - The Fleeing Ogres
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第2章] - 逃跑的食人魔
```

## entry-03537
位置：tome-cults.lua:1484；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 3] - Battle Preparations
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第3章] - 准备战斗
```

## entry-03538
位置：tome-cults.lua:1518；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 4] - To Battle!
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第4章] - 加入战斗！
```

## entry-03539
位置：tome-cults.lua:1556；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 5] - Dark Resolve
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第5章] - 黑暗的决心
```

## entry-03540
位置：tome-cults.lua:1602；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 3, Chapter 6] - Hateful Wrath
```
译文：
```text
菲·维莉欧斯的冒险 [第3卷，第6章] - 仇恨愤怒
```

## entry-03541
位置：tome-cults.lua:1636；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 1] - Exhaustive Travel
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第1章] - 穷途末路
```

## entry-03542
位置：tome-cults.lua:1670；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 2] - Seeking Sanctuary
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第2章] - 寻求庇护
```

## entry-03543
位置：tome-cults.lua:1704；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 3] - The Enchantress
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第3章] - 女巫
```

## entry-03544
位置：tome-cults.lua:1705；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]Alreiwen Taeil the foolhardy enchantress. Easily the worst conversationalist I have ever met, and among all the shaloren I know of none that has a greater ego than hers. Still, I respect her sense of justice as well as her gifted abilities in the arcane. Who knows what fate may have happened to the ogres had she not been present when I made the request for their entry.[/i]

Along the way the young mage probed me with varying questions relating to my travels and the events that I had witnessed or been a part of. Of those questions asked though, the ones involving the treatment of the ogres have stuck out in my mind the most. "So the ogres, I've heard a little bit about them. While they never really traveled here to Elvala, I've heard stories of their altruism and heroics. But, from what you told me about those crazed lunatics, it seems rather odd that they wouldn't have killed the ogres outright. I mean they have obviously managed to merge their bodies with arcane runes, what more reason is there for someone who hates magic to just kill them then and there. For what purpose do you think they would be kept alive?"

I responded coldly to the question, "I do not know the reason, nor do I care. For what purpose would you attempt to discern any meaning from their mad actions anyways? I see little reason for you or any shalore to care." Laughing at this, the young shalore replied "perhaps you are right, but just because these 'cultists' seem to act mad to you, doesn't mean that they pursue whatever their doctrines are aimlessly. They will be our enemies for sure in the future, but hopefully before we ever truly encounter them we can at least know their motives. If we can understand how they act, we can understand what moves they will make, and we can make plans to counter their schemes as a result."

Continuing on, I noticed that the shalore was intently looking at me, or rather at the back of my neck. "Judging from where the rune I crafted was placed, I guess the ogres helped you with inscribing my Rune of Return?" Taking a moment to process what the shalore said, I soon spouted, "You crafted?" The shalore smiled and laughed a bit before continuing, "Indeed I did, a masterwork produced by the best enchantress in Elvala! Though I'm wondering why you didn't graft it on to your own skin yourself, or are the Thaloren really 'that' backwards when it comes to the arcane?" I remember the cold expression I gave, which she immediately picked up on before replying, "Right, I'll try to keep that in mind the next time I meet a thalore."

Nearing the outer edges of Elvala where the Shroud was, the enchantress asked where exactly the ogres would be. I noted to her that I had left them in the same place where I had entered through the Shroud on my first visit, and promptly led her to that spot of my initial entry. Standing stoically, she raised her arms and seemed to sing in a low harmonic sound, and almost immediately the misty smoke began to part. Any skepticism I had as to what she planned was soon replaced with astonishment as a tunnel smaller in size than the one I had traversed formed in front us. From the other side of the tunnel I could see the distant figures of the ogres appear.

Not missing a beat, I could see the ogres begin to move towards us. After a few minutes the first of them began to run inside Elvala's walls before collapsing to the ground. Behind us I noticed a growing crowd of onlookers gathering to witness the unexpected event in front of them. As the last ogre exited from the tunnel, the mage put her arms down, and with it the Shroud fell as well. Finished, she too fell backwards to the ground and gasped heavily for air, seemingly drained of of all her energy after the amazing feat. Looking up at me with a smile on her face she made a simple statement in between deep breaths, "It is done. You have led the ogres to their safety."

"Indeed, though this wasn't the proper way to go about it.” I heard a voice state behind me. Turning around to see the general, I quickly noticed the large company of guards breaking through the onlookers and making our way towards us. For a moment I wondered if there would be trouble, but the general eventually gave the order to the soldiers to help carry the ogres to the healers. As the general began to approach the enchantress his eyes seem to dart quickly towards me. Stopping for a moment to give me a quick look over, he stated in a quiet but authoritative voice, "You should head over with the ogres as well.” before continuing on past me towards the enchantress. Standing above the young shalore as she slowly caught her breathe, I could see him fold his arms.

Deciding for now it would be best to follow the orders of the general, I proceeded to make my way to Elvala's medical facilities as well. Naively thinking I would look for the chief healer and see how I could help out, I made my way into the building, and asked the closest healer where I could find him. I can still remember the shock on the face of the healer's face, as it hadn't even occurred to me at that time that the general had suggested that I head to the healers for my own injuries, not for those of the ogres. It didn't take long for what seemed like one healer after another to be called over, before it seemed like half of the healers in the building were tending to me, including some of those that were originally tending to the ogres.

I can't say I remembered much of what happened either, I couldn't even remember feeling any pain for any of the injuries I apparently had, though the healers recognized how critical those injuries were. I was promptly whisked away to one of the empty beds and given several anesthetic infusions, which subsequently caused me to black out. I would learn later that the healers were aghast at how brutally injured I truly was, but were truly horrified when the regenerative infusions they applied seemingly failed to have much effect, despite how many they applied. It would take my body a few months to recover, not to mention countless infusions. Even to this day I am told to be careful of injury due to how long it takes for me to heal.

Eventually when I woke up, and after the healers had checked me over, I was told to wait as someone wished to visit me. After a period of time I was greeted by the enchantress once more. "I see you are doing alright, you’re certainly quite tough thalore. Don't worry about the ogres, Aranion has granted them the asylum here as requested." She spoke proudly though I could sense a hint of disappointment in her voice. "Now then, I realize you have only woken up, but Aranion wants me to get the story from you as to what transpired after you had left for the Nargol Kingdom to the point when you came back to Elvala. Perhaps as well you might shed some light on why exactly it took you so long to heal as well?"  
```
译文：
```text
[i]鲁莽的女巫阿尔雷温·泰尔。也是我见过的最不会聊天的人，在我所认识的所有永恒精灵中，没有人比她更自负。不过，我尊重她的正义感以及她在奥术力量方面的天赋。如果我请求食人魔进入时她不在场，没有人知道他们的命运会怎样。[/i]

一路上，年轻的法师向我提出了各种各样的问题，这些问题与我的旅行以及我所目睹或参与的事件有关。不过，在她提出的这些问题中，那些涉及对食人魔进行治疗的问题在我脑海中最为突出。“所以食人魔，我听说了一些关于他们的事。虽然他们从未真正到过埃尔瓦拉，但我听说过他们的利他主义和英雄事迹。但是，从你告诉我的那些疯狂的疯子看来，他们不直接杀死食人魔这一点似乎很奇怪。我的意思是，他们显然已经将自己的身体和奥术符文结合在一起了，没有什么理由阻止那些讨厌魔法的人在各处屠杀他们。你认为他们为什么会活着？”

我冷冷地回答这个问题，“我不知道原因，也不在乎。不管怎样，你想从他们疯狂的行为中辨别出什么意义？”年轻的永恒精灵笑着说：“也许你是对的，但这些‘邪教徒’在你面前表现如此疯狂，并不意味着他们漫无目的地追求自己的教义。他们在未来肯定是我们的敌人，但希望在真正遇到他们之前，我们至少能知道他们的动机。如果我们能够理解他们的行动方式，就能理解他们将采取什么行动，也就能够因此制定计划来对抗他们的计划。”

接着，我注意到永恒精灵正聚精会神地盯着我，或者更确切地说是盯着我的后颈。“从你把我制作的符文放在哪里来判断，我猜是食人魔帮你刻下了我的回归符文？”我花了一点时间才理解那个永恒精灵说的话，然后叫出声来：“是你制作的？”永恒精灵笑了笑，然后继续说：“当然是我了，埃尔瓦拉最好的女巫创作的杰作！不过，我想知道你为什么不自己把它铭刻到自己的皮肤上，或者说，当涉及到奥术的时候，自然精灵真的是‘这么落后’吗”我露出了冷冰冰的表情，她立即回答道，“好吧，下次我遇到自然精灵的时候，我会尽量记住这一点。”

在靠近埃尔瓦拉帷幕的边缘时，女巫问那些食人魔究竟在哪里。我告诉她，我把他们留在了我第一次来时穿过帷幕进入的地方，并迅速把她带到了我最初进入的那个地方。她坚忍地站着，举起双臂，似乎在低沉的和声中歌唱，迷雾几乎立刻烟消云散。我对她计划的任何怀疑很快就被惊讶所取代，因为一条比我走过的那条小的隧道形成在我们面前。从隧道的另一边我可以看到远处出现的食人魔。

我看到食人魔开始毫不迟疑地向我们跑来。几分钟后，他们中的第一个开始跑进埃尔瓦拉的墙里，然后倒在地上。在我们身后，我注意到越来越多的旁观者聚集在一起，目睹眼前发生的意外事件。当最后一个食人魔从隧道里出来时，法师放下了双手，帷幕也随之合上了。说完，她也倒在地上，喘着粗气，似乎这一惊人的壮举耗尽了她所有的精力后。她仰望着我，脸上带着微笑，在两次深呼吸之后作了一个简单的陈述：“一切都结束了。你把食人魔带到了对他们来说安全的地带。”

“的确，尽管这不是解决问题的正确方法。”我听到身后传来一个声音。转过身去看将军，我很快注意到一大群卫兵冲破围观的人群，朝我们走来。我一时想知道我们会不会有麻烦，但将军最终命令士兵们帮忙把食人魔带到治疗师身边。当将军走进向巫时，他的目光扫过了我。将军停下来，快速看了我一眼，用一种安静但富有权威的声音说：“你也应该和食人魔一起过去。”然后继续从我身边走过，走向女巫。我看到女巫站在年轻的永恒精灵前方，她慢慢地屏住呼吸，双臂合拢。

现在的我决定最好听从将军的命令，我也跟着去了埃尔瓦拉的医疗机构。我天真地认为我应该去找主治医师，看看我能帮上什么忙，就走进楼里，问离我最近的治疗师在哪里能找到他。我仍然记得那个治疗师脸上的震惊，因为当时我甚至没有想到，将军建议我去治疗师那里是为了治疗我自己的伤，而不是那些食人魔的伤。没过多久，一个接一个的治疗师就被叫来了，然后大楼里似乎有一半的治疗师在照顾我，包括一些最初照顾食人魔的人。

我已经不太记得发生过的事情，我甚至记不起我之前受到的那些创伤有什么痛苦，尽管治疗师们很快意识到这些伤害有多严重。我被迅速带到其中一张空床上，给了我几次麻醉剂注射，结果我昏倒了。后来我才知道，治疗师们对我的真实伤势已经感到无比震惊，但当他们发现自己使用的再生纹身似乎没有产生多大效果，无论使用多少的时候，他们的惊讶程度就更大了。我的身体需要几个月才能恢复，更不用说使用了无数次的纹身了。即使到今天，我也被告知要小心受伤，因为我需要更多时间才能痊愈。

最后，当我醒来，在医生检查了我之后，我被告知要稍等一下，因为有人想来看我。过了一段时间，女巫又来迎接我了。“我看你恢复得不错，你确实很坚强。不用担心那些食人魔，艾伦尼恩已经按照要求批准了他们在这里避难。”她骄傲地说，虽然我能感觉到她的声音中有一丝失望的味道。“现在，你终于醒了，但艾伦尼恩想让我问问你，有关你离开纳格尔王国回到埃尔瓦拉的路途中，到底发生了什么样的故事。或许，你也可以解释一下，为什么你也要花这么长时间才能痊愈？”
```

## entry-03545
位置：tome-cults.lua:1742；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 4] - Terrifying Interview
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第4章] - 可怕的访谈
```

## entry-03546
位置：tome-cults.lua:1743；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]I do not know if Alreiwen has forgiven me, for the terror I had inflicted on her, or the hatred within me she must have felt. While it was but a mere moment, I could tell that all my rage had been channeled into her very being, the same rage that I had filled those fanatics with from before. At that moment I could tell she knew how potentially dangerous I was. Rei, if you are reading this then know how truly sorry I am for what happened.[/i]

For the next two hours, the enchantress proceeded to grill me as to what had happened after I had left Elvala. In great detail I informed her of my experiences within the Nargol Kingdom, and my subsequent travel along the southern shoreline of Maj'Eyal. Every so often the inquisitive shalore would ask me questions about the fanatics I had witnessed and the events I had seen them carry out or suspected them of having a part in. To be honest I couldn't tell if it was for her own satisfaction or perhaps if Aranion had indeed asked her in hopes of learning more about the fanatics. Eventually as our conversation came to a close, that was perhaps when the more eventful part of our discussion came up.

"So, that mostly concludes more or less what Aranion sent me here for,” she began, before continuing to state, "however, the healers also wanted me to ask you a few questions in regards to your body. I'm not sure if you have been told yet, but you have been in this hospital bed for several months now, despite injuries that should have healed in a few weeks. You wouldn't perhaps have an explanation for why this is?" Immediately I wondered if perhaps what had happened on that charred battlefield was connected with the slow recovery time of my body as I had finally begun to realize that something was wrong with me by that point. I can't say I was too interested in talking about that instance, not wanting to remember what had happened either.

"I wouldn't know why that would be.” I replied as I turned my head to look away from the enchantress. Despite not being able to see the shalore's face, I could immediately tell that she saw through me immediately. "So you do have some idea then.” she cheerfully responded. I glanced at her in disgust, noticing a gleam of satisfaction beaming from her eyes, although I couldn't tell what she would be satisfied from. "I'm also guessing that it somehow involves your recent fighting experience, judging from your reactions." I couldn't help but dart my eyes away, realizing that was only telling her how easily and accurately she was reading me. She seemed to giggle a little bit at this, which only served to annoy me and wish that she would go away more.

"The ogres I spoke to talked at great length about how you had led them here to Elvala, of how without your help they would likely not have survived in the fight against their pursuers. However, the more we spoke, the more it became clear that something was amiss. Curiously no ogre would say much in regards to you in whatever battle it was that you fought, despite how important you were to apparently winning it. From what I can understand there were many ogres with you too. How were you so paramount in the ogres getting here? I heard from the Rangers that you held your own against a couple of wolves, but armed fighters are clearly a step above some hungry animals, and you don't strike me as having much in the way of combat experience."

The enchantress intently examined me as she spoke, analyzing me for any hint or clue I would give her. For my part I was actively attempting to repress my memories of those recent events, to not relive the mix of emotions that had taken hold of me at that time, to leave them silent. Intent on digging further into me though, the enchantress continued to press on, to meet that darker version of myself. "What is it that you are hiding about yourself, that the ogres seemingly wouldn't mention about you? What unmentionable thing did you perhaps do to help the ogres through their plight?" The enchantress continued on with the probing questions one after the other, endlessly, never stopping, until finally I decided that she needed to stop.

"CEASE ASKING ME THESE QUESTIONS NOW!" The phrase swiftly escaped from me, though I had no intention of stating it as abruptly or forcefully as I did. The young shalore was immediately taken aback from my statement, her eyes widened and the smile that one could mistake for a permanent fixture on her face now gone. She began to shiver and sweat profusely all at once before stammering out "Wha-What?" She shook in her chair, and I could feel fear emanating from her body. I paused again for a moment, feeling a sense of satisfaction. This sensation I felt, it felt similar from something before. And then I realized all at once what was happening. My emotions were beginning to take a hold of me once more.

Immediately I pulled every force of my being away from the enchantress. She instantly jumped out of the chair and scrambled away from me, gasping as the pressure I had exerted was lifted. Her eyes were wide now, catching a full glimpse of the darker me, and she wanted nothing more than to actively hide away. "I'm sorry" was all I could muster to say. She looked at me, seemingly now appearing much older than before. Shakily she made her way to the door to leave the room, to get to safety, to get away from me. Sometime after she was gone I would realize that a guard would be stationed outside my room, and I'm pretty sure that guard was not there before the enchantress had come.

Eventually as I recovered enough to move around a bit I was finally released from the care of the healers. I was given a dwelling in a secluded part of Elvala and a pair of guards were stationed outside of it at all times. Although I never asked, I was sure they were there to confine me from the rest of the citizens of Elvala, and them from me. I didn't blame the shaloren for this as even now I could feel something driving me, influencing my thoughts, wanting to lash out. Who knows what sort of actions I might have been pushed to do, or whether I may have gone into a mad killing rage against the Shaloren; the irony of which is not lost on me considering my initial reasons for leaving Thaloren lands so long ago.
```
译文：
```text
[i]我不知道阿尔雷温是否原谅了我，原谅我给她带来的恐惧，或者她一定感受到了我内心的仇恨。虽然那只是一瞬间，但我可以看出，我所有的愤怒都已经转移到了她身上，就像我从前对那些狂热分子充满的愤怒一样。在那一刻，她终于意识到了我有多危险。雷，如果你读到这篇文章，你就知道我对所发生的事是多么的抱歉。[/i]

接下来的两个小时里，女巫继续盘问我离开埃尔瓦拉后发生了什么。我非常详细地向她讲述了我在纳格尔王国的经历，以及后来我沿着马基·埃亚尔的南部海岸旅行的经历。好奇的永恒精灵常常会问我一些问题，关于我所目睹的狂热分子，以及我看到他们所进行的、或者怀疑他们参与的事件。老实说，我不知道是艾伦尼恩确实问过她，希望更多地了解狂热分子，还是这一切只是为了满足她自己的好奇心。最后，当我们的谈话接近尾声时，我们谈到了更重要的部分。

“所以，这基本上可以断定，艾伦尼恩派我来这里是为了什么，”她开始继续说，“然而，治疗师也希望我问你几个关于你身体的问题。我不确定他们是否告知了你这件事，但你已经在这张病床上躺了几个月了，尽管几周后你应该会痊愈。你可能没有知道这是为什么？”我很快就想，也许在那烧焦的战场上发生的事情，与我身体恢复缓慢有关，因为我终于开始意识到我当时有点不对劲。然而，我对于谈论那件事情实在并不那么感兴趣，也不想记得发生了什么。

“我不知道为什么会这样。”我转过头去看那个女巫，回答说。尽管我看不见那个永恒精灵的脸，但我可以立刻看出她立刻看穿了我的想法。“看来，你一定知道些什么。”她高兴地回答。我注意到她眼里流露出满足的光芒，厌恶地瞥了她一眼，尽管我不知道她在满足于什么。“从你的反应来看，我也在猜测这可能与你最近的打斗经历有关，”我忍不住把眼睛移开，却意识到这只不过是在告诉她，她对我反应的解读是多么精确。她对此咯咯地笑，这只让我恼火，希望她离我更远些。

“我和那些食人魔聊了很久，谈到你是如何把他们带到埃尔瓦拉的，没有你的帮助，他们很可能无法在与追捕者的战斗中幸存下来。然而，我们说得越多，就越清楚出了问题。奇怪的是，没有一个食人魔谈论你在那场战斗是怎样战斗的，尽管你对于赢得那场战斗显然至关重要。据我所知，你身边也有很多食人魔。你怎么能在食人魔面前这么重要？我从游侠那里听说，你自己对付了几只狼，但武装的战士显然比一些饥饿的动物强大很多，而且你看起来也没什么战斗经验。”

女巫一边说话，一边仔细地打量着我，分析着我给她的任何暗示和线索。就我而言，我正积极地试图压抑自己对最近那些事件的记忆，不去重温当时控制着我的各种情绪，让它们保持沉默。不过，女巫一心想深入挖掘我的内心深处，继续向我施压，想要看见我那更阴暗的一面。“你在隐藏什么，那些食人魔为什么不愿提起你？你是不是做了什么难以启齿的事，来帮助食人魔渡过难关？”女巫继续一个接一个地问试探性的问题，没完没了地问，从来不停，直到最后我决定她需要停下来。

“别再问我这些问题了！”这句话很快就从我口中脱口而出，尽管我无意像刚才那样突然或有力地说出来。年轻的永恒精灵立刻被我的话吓了一跳，她的眼睛睁大了，她脸上一直挂着的笑容也突然消失了。她开始颤抖，大汗淋漓，然后结结巴巴地说：“什…什么？”她在椅子上发抖，我能感觉到她身体里流露出的恐惧。我又停顿了一会儿，却感到很满足。我感觉到的这种感觉和以前的感觉很相似。然后我立刻意识到发生了什么：我的情绪又开始控制我了。

我立刻把我所有的力量都从女巫身上拉开。她立刻从椅子上跳下来，从我身边跑了出去，大声喘着气，从我施加的压力中逃离。她现在睁大了眼睛，看到了那个黑暗的我的真相，只想主动躲起来。我唯一能做的只有呢喃着“对不起”。她看着我的样子，似乎刹那间变得比以前老了许多。她摇摇晃晃地走到门口，离开房间，离开我，到了安全的地方。她走后不久，一个警卫开始驻扎在我的房间外面。我敢肯定，在女巫来之前，那里没有这样的警卫。

最后，当我恢复到可以走动的程度时，我终于从治疗师的照顾中解脱出来。我被安排在埃尔瓦拉一个僻静的地方居住，两个卫兵一直驻扎在外面。虽然我从来没有问过，但我确信他们是来把我和埃尔瓦拉的其他市民隔离开来的。我没有责怪永恒精灵，因为即使是现在，我也能感觉到有什么东西在驱使我，影响我的思想，想大发雷霆。没有人知道我会在这样力量的驱使下采取什么样的行动，也不知道我是否会对永恒精灵进行疯狂的杀戮；讽刺的是，这是我很久以前离开自然精灵土地的最初原因。
```

## entry-03547
位置：tome-cults.lua:1776；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 5] - Festival of Happiness
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第5章] - 快乐节
```

## entry-03548
位置：tome-cults.lua:1814；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 4, Chapter 6] - Rebuilding Anew
```
译文：
```text
菲·维莉欧斯的冒险 [第4卷，第6章] - 焕然一新
```

## entry-03549
位置：tome-cults.lua:1852；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 1] - Dead On Arrival
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第1章] - 死亡到来
```

## entry-03550
位置：tome-cults.lua:1886；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 2] - Elvala Under Attack
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第2章] - 被攻击的埃尔瓦拉
```

## entry-03551
位置：tome-cults.lua:1920；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 3] - Leadership From The Front
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第3章] - 前线的领袖
```

## entry-03552
位置：tome-cults.lua:1954；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 4] - Confrontation
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第4章] - 对峙
```

## entry-03553
位置：tome-cults.lua:1988；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 5] - Staff of Bones
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第5章] - 白骨法杖
```

## entry-03554
位置：tome-cults.lua:2022；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 6] - Evil Malice
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第6章] - 恶毒
```

## entry-03555
位置：tome-cults.lua:2023；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]There is truly no other way to describe the necromancer that I met but completely evil. One might consider the magic hating fanatics I had written about in my earlier books as evil, but even from them I could sense that they were attempting to bring about a better world, despite how twisted their actions might have been. This fiend of undeath though, I could sense no goodwill from, and the actions undertaken seemed to be only for the purpose of personal amusement. Judging from emotions that I could feel from the magic as well, I don't think that necromancy could ever be used by anyone other than those of an evil nature.[/i]

As I felled the bone giant I could hear the necromancer clapping once more. "Very good, well done, quite the display. Your bones will truly be worth adding to my staff,” the necromancer stated in sinister tone. Turning my head towards necromancer I stated boldly, "It will take more than your mere bone giant to kill me." Seemingly caught in thought to my statement the necromancer replied, "Hmmm, bone giant, quite the name. Yes, I think that will do nicely as a name. Of course, you seem to be misunderstanding something. The bone giant, as you call it, is not quite dead yet." Registering the words, I didn't have much time to react before I could feel a hard blow swat me from the side.

Snapping my eyes to what had hit me, I immediately realized that the bone giant was indeed not defeated as it stepped forward to stand in between me and the necromancer. What's more, it had seemed that it had reassembled itself into a new fiendish form that was ready to do battle. As the bone giant approached to attack me I could hear the voice of the necromancer in the background as are battle began to start again. "These Bone Giants as you call them are quite something aren't they. I got inspiration for them from the Nargols when they fought against the Conclave in the Allure Wars. You see, few know this but the Nargols actually used necromancy to ultimately win their fight against the Conclave."

I could hear the necromancer wheeze and cackle in the background for a moment, but I was more concerned with the bone giant attacking me. Somewhat exhausted from beating it down the first time I lacked the strength to overcome its defenses a second time and bring it down again. I slowly proceeded to back away in order to buy some time and examine my options in regards to what I might be able to do to defeat it. The swirling barrier of bones were already circling its body, and I knew that I wouldn't be able to do any lasting damage against it as a result. Sooner or later I would have to commit to fighting it fully, and I knew that I would want to make that commitment on my own terms.

Distressingly however, finding an opportunity was made more difficult as the necromancer continued to prattle on. "These bone giants as you call them, they can be formed in a variety of ways to kill and as you can see they are quite durable. I'm actually quite thankful that you managed to rip through it as you did just now, I can already see ways in which I can improve my next one." Concluding the sentence the necromancer began to laugh and wheeze once more. It was quite infuriating, and I'm not even sure why I remember the necromancer's words so vividly. However, I would not be bested by the bone giant and I decided that I would try to make a final stand and bring it down again.

I rushed into the bone giant, taking a quick swipe that knocked a few bones away. Noticing that the bone barrier didn't absorb the blow I quickly realized that it had since dissipated. Sensing that I only had a brief moment before it would come back, I fully committed to unleashing as much power as I could within the next strike. Hitting with all the strength I could muster I quickly knocked away a good chunk of the bone giant’s mid section, causing it to stumble a bit. Once again like before it attempted to shift its bones around in order to maintain itself, but my attacks were chipping bones away bit by bit. However, the bone giant would not allow itself to be defeated so easily.

With a quick motion the bone giant shot forth one of its limbs against me, once again ripping against my flesh with painful spikes. Not discouraged by this in the slightest however, I let loose my heat beam rune and ignited its bones, and more importantly I relieved the pain from the blow. As I resumed my attacks I could hear the raspy voice in the background seemingly comment, "Hmm, runes... ohhh! I know, I'll graft some runes onto the next one! What interesting ideas you are giving me." Still focused on my fight, I continued to strike it again and again until finally the bone giant fell apart. Not sure if it would get up again I continued to hack at it until I had completely disassembled it.

Forgetting about the necromancer though, I immediately felt my body go numb, and quickly noticed ice forming all around my body. Immobilized, I darted my eyes around before spying the necromancer with an outstretched hand. Slowly the necromancer approached me, coming around to my left arm where my heat beam rune was inscribed. Putting its hand under what I assumed to be its chin, the necromancer noted, "Not once but twice you have defeated my bone giant. I suspected you might be able to bring it down once, but bringing it down again right after was quite unexpected. Now, I really have to wonder who you are? You appear to be a thalore to me, but what were you doing in Elvala? Hmmm."

Continuing around me to stand in front before circling around to my right, necromancer continued to make "hmm, hmm" sounds. Proceeding to stop the necromancer began to muse aloud once more, "Quite surprising seeing you use runes. Are you a criminal exiled from the forests perhaps? Wait, what's this second rune you have inscribed?" While I couldn't see the necromancer I could feel the intent staring at the Rune of Return that had been inscribed on the back of my neck. From behind a remark rang out, "Ahh, interesting. A shaloren design but judging from the markings it appears an ogre's handiwork was involved in inscribing this rune if I am not mistaken. Quite intriguing."

The necromancer continued to talk aloud for several moments as he circled around me again and again, which was fine by me. I could feel the arcane energy replenishing within my heat beam rune, and when I had the chance I would activate it and release myself from my icy imprisonment. Perhaps aware of my intent though the necromancer quickly glanced at my eyes before stating, "You are quite an oddity aren't you? However, you aren't much the conversationalist so there is little reason for me to keep you alive. I can easily study your corpse instead of leaving you alive you see." I could sense the magic beginning to accumulate in one of the necromancer's hands as he concluded by saying, "Farewell thalore." 
```
译文：
```text
[i]我遇到的死灵法师，除了完全邪恶之外，实在没有别的办法来形容。有人可能会认为我在早前的书中写的那些讨厌魔法的狂热分子是邪恶的，但即使是从他们身上，我也能感觉到他们试图带来一个更美好的世界，尽管他们的行为可能是过于扭曲的。不过，在这个不死之魔那里，我感觉不到任何善意，他所采取的行动似乎只是为了个人娱乐。从我能从魔法中感受到的情绪来看，我认为死灵法术只会被完全邪恶之人使用。[/i]

当我击倒这个骨巨人时，我又听到了死灵法师的鼓掌声。“很好，做得很好，挺好看的。你的骨头真的值得加在我的杖上，”死灵法师用阴险的语气说。我把头转向死灵法师，大胆地说：“要杀死我，你的骨巨人还远远不够。”死灵法师似乎陷入了对我的陈述的思考中，回答道：“嗯，骨巨人，这个名字很不错。是的，我想这个名字很不错。当然，你好像误解了什么。你所说的骨巨人还没完全死，”听到这些话，我还没来得及反应，就感觉到一记重击从侧面打中了我。

我猛地一眨眼睛，立刻意识到这个骨巨人并没有被打败，它走上前来站在我和死灵法师之间。更重要的是，它似乎已经重新组合成一个新的恐怖形态，准备好战斗。战斗又开始了，当骨巨人接近攻击我时，我可以听到背景中死灵法师的声音：“你所说的这些骨巨人是很了不起的，不是吗。我从纳格尔人那里得到灵感，这是他们在厄流战争中对抗孔克雷夫时使用的武器。你看，很少有人知道这一点，但纳格尔人实际上利用死灵法术最终赢得了与孔克雷夫的战斗。”

我能听到死灵法师在背景中喘息和咯咯地笑了一会儿，但我更担心的是攻击我的骨巨人。第一次击倒它让我有些疲惫不堪，我没有力量再次战胜它的防御，并再次击倒它。我慢慢地往后退，以便争取一些时间，并思考我还可以选择什么来击败它。骨头的漩涡屏障环绕着它的身体盘旋，因此，我知道现在没法对它造成任何持久的伤害。迟早，我会找到一个机会发动一次全力打击，而我正在积极寻找这一机会。

然而，令人沮丧的是，寻找机会十分困难，而死灵法师仍然在继续喋喋不休：“你所说的这些骨巨人，它们可以组合成多种形态，来进行各式各样的杀戮。你可以看到它们非常耐用。我真的很感激，看到你刚才那样把它撕开的方式，我已经想到了改进下一个的方法。”在结束这句话后，死灵法师又开始大笑和喘息。这真是太让人恼火了，我甚至不知道为什么我能如此生动地记住死灵法师的话。然而，我不会被骨巨人打败，我决定我会努力背水一战，并再次把它打倒。

我冲进了骨巨人，快速地进行斩击，把几根骨头都打掉了。注意到骨盾没有吸收我的攻击，我很快意识到它已经消散了。我意识到，我只有很短的时间，骨盾很快又会重新出现，我必须在下一次攻击中释放尽可能多的力量。我使出全力的打击，很快就把巨人中段的一大块骨头打掉，导致它绊倒了。它再次像以前一样试图移动它的骨头，以维持自己，但我的攻击一点一点地削掉骨头。然而，骨巨人不会让自己这么容易被打败。

骨巨人迅速地向我伸出一只骨爪，用痛苦的尖刺再一次撕开我的肉。然而，我丝毫没有因此而气馁，启动了热能射线符文，点燃了它的骨头，更重要的是，这减轻了它的打击带来的痛苦。我继续攻击时，能听到死灵法师刺耳的声音，似乎在评论着我，“嗯，符文……哦！我知道，我会把一些符文装在下一个骨巨人身上！你给了我这么多有趣的想法。”但我仍然专注于我的战斗，一次又一次地打击它，直到最后看到骨巨人崩溃。我不确定它是否会再次复活，于是继续攻击它，直到我完全将其打成粉碎。

不过，我忘记了死灵法师的存在。一瞬间，我突然感觉到身体麻木了，很快就注意到自己的身体周围结冰了。我一动不动地四处张望，发现了对着我伸出一只手的死灵法师。死灵法师慢慢地靠近我，走向我的左臂，在那里刻着我的热束符文。死灵法师把手放在我认为是它下巴的地方，说道：“你打败了我的骨巨人，不是一次而是两次。我以前以为你也许能干掉它一次，但能够紧接着再次干掉它，确实出乎我的意料。现在，我真的想知道你是谁？在我看来，你是一个自然精灵，但你在埃尔瓦拉做什么？嗯……”

死灵法师从我的前面，慢慢绕到我的右边，继续发出“嗯，嗯”的声音。终于，死灵法师停了下来，又一次说道：“很惊讶看到你能使用符文。你该不会是个被从森林里放逐出来的罪犯吧？等等，你刻的第二个符文是什么？”尽管我看不见死灵法师，我能感觉到它凝视着刻在我脖子后面的返回符文。一句话从后面响起，“啊，有趣。一个永恒精灵的设计，但从标记来看，如果我没有记错的话，铭刻这个符文似乎是食人魔的工艺。很有趣。”

死灵法师在我周围一圈又一圈地转来转去，他继续大声地说了几句话，这对我来说是一个好机会。我能感觉到我的热能射线符文重新聚集着奥术能量，只要再等一会儿，我就可以重新激活它，把自己从冰冷的监牢中释放出来。或许感受到了我的意图，死灵法师很快瞥了我一眼，然后说：“你真是个怪人，不是吗？不过，你不太健谈，所以我没什么理由让你活着。我可以很容易地研究你的尸体，而不需要让你活着，”我可以感觉到死灵法师的一只手开始积聚魔法，他最后说，“永别了，自然精灵。”
```

## entry-03556
位置：tome-cults.lua:2060；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 7] - Powers of Undeath
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第7章] - 不死的力量
```

## entry-03557
位置：tome-cults.lua:2094；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 5, Chapter 8] - From the Brink of Death
```
译文：
```text
菲·维莉欧斯的冒险 [第5卷，第8章] - 自死亡的边缘
```

## entry-03558
位置：tome-cults.lua:2130；section：tome-cults/data/lore/kroshkkur.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The story of Kroshkkur is not a peaceful one. Those of us who gathered here know that we have no place anywhere else. The surface would never accept us, for our forms are terrible for them to behold. Even in the depths of Eyal, we have had to fight for our place in the world. These endless tunnels and the creatures within them have sought to destroy us. They hunger for our very souls.

When Kroshkkur was first discovered, it was infested with horrors. We cut them down and attempted to restore the strange arcane machines we found here. Alas, we found it to be damaged and could only partially restore it. But, even that small amount of power it held was enough to give us safety. Many followed us after that, outcasts who were looking for a haven in a hostile underground. Intelligent beings who do not belong anywhere else, seekers of forbidden knowledge and those who have seen too much for mortal eyes to bear are just a few who have made their homes here.

Since then, we have studied. We have divined this world's secrets and delved into the dark places which surface dwellers dare not look, out of fear of what might be looking back. We have no such fear, for we are the things looking back. In these places, we have found out many truths and discovered magic which will change the course of Eyal's history.

We will bide our time down here in the dark and turn this place into a beacon of knowledge. If this world will not give us a place in it, then we shall simply take one for ourselves. We shall make ourselves known to the surface when the time is right, and show them that we aren't just scattered, mindless beings for them to sweep aside.
```
译文：
```text
克诺什库尔的往事并不安宁。聚集在这里的人们都知道自己别无归宿。地表上的人们永远不会接受我们，因为在他们眼中我们的姿态太过恐怖。而就算在埃亚尔的地下深处，我们的容身之地也来之不易。在无尽的地道居住着的生物日夜追杀着我们，想将我们的灵魂吞噬殆尽。

我们最初发现克诺什库尔时，里面住满了恐魔。我们杀了它们，并试图修复这里奇怪的奥术机械，但它损坏严重，我们只能将其部分修复。但仅仅是它所具有的这一小部分力量，也足以给我们带来安宁。之后，更多流浪者追随着我们来到了这里，以在充满敌意的地下寻求一处庇护。他们当中有在别处无处容身的智慧生物、有寻求着禁忌知识的先知，还有目睹了太多凡人的目光所不能承受之物的人。

之后我们便开始学习。我们领悟了世界的秘密，潜入了地表居民看都不敢看，恐惧着被其中不知是什么的东西凝望的无尽深渊。我们并没有这种恐惧，因为我们正是在其中凝视着他们的那些存在。在这些地方，我们找到了许多真相，发现了能够改变埃亚尔历史进程的禁忌魔法。

我们会在这片黑暗之中等待着时机，将这里变成一座知识的灯塔。如果这个世界不给我们容身之处，我们就自己去夺取它。当时机正确之时，我们就将让地表知道我们的存在，告诉他们，我们并不只是一群被他们当做害虫一样轻轻扫开的，毫无心智的乌合之众。
```

## entry-03559
位置：tome-cults.lua:2184；section：tome-cults/data/lore/kroshkkur.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Quekorja was the god of time and possibilities. What stands out about Eyal's myths regarding Quekorja is how wildly inconsistent they are. In particular, tales after the Godhunt tend to have a far less favourable outlook of the god than pre-Godhunt myths. Speculation regarding this is due to Quekorja supposedly taking an interest in written history and appointing its own librarians to record its tales. Since there are no surviving records of this library existing, this theory is considered to be pure conjecture and has no concrete evidence to validate it. There have been some unusual records found too, supposedly written by the same authors on the same dates, but wildly varying in their tone and their description of the god itself. Given the god's ability to control time, it is thought these notes might be from alternate timelines, further obscuring the truth about the god itself.

Quekorja was also thought to be responsible for the creat...[i](You know you read this section, but you can't actually remember it. It is almost like something has deliberately erased it from your mind.)[/i]

According to the records of Anglowen, Quekorja was slain during the Godhunt and its body discovered by the mage Linaniil. Linaniil managed to absorb a small portion of the god's power through a dangerous ritual. This tiny shard of power she acquired made her an archmage without peer, a testament to the sheer might of the gods.
```
译文：
```text
奎科加是时间和可能性之神。在埃亚尔关于奎科加的神话传说中，最突出的一点就是它们之间有着极大的矛盾，而在弑神之战之后的传说中它的形象远不如前。对此的猜测是奎科加自己可能十分爱好书写历史，指派了自己的记录者来记录自己的故事，但并没有证据表明有这样一个图书馆存在，因而这种理论被认为只是没有依据的臆测，没有实际证据的支持。另外还有一些不寻常的记录，本应是同一个作者在同一天写的，但其语调和对此神的描述却大相径庭。由于奎科加能够操控时间，因而有观点认为这些记录其实是来自别的时间线。这更加增添了奎科加的神秘。

奎科加也被认为创……[i]（你记得你读过这段文字，但就是记不起其内容，就好像它是被有意从你的脑海中抹去了一样。）[/i]

根据安格列文的记载，奎科加在弑神之战之中被杀死了，它的尸体后来被法师莱娜尼尔发现。她成功通过一个危险的仪式吸收了此神的一小部分力量，而就是这微小的力量也使她成为了无可匹敌的大法师。这也证实了诸神的力量是多么的强大。
```

## entry-03560
位置：tome-cults.lua:2214；section：tome-cults/data/lore/kroshkkur.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Urh'Rok is supposedly a god from the world Mal'Rok, who created the race we know as demons. All of the myths regarding Urh'Rok depict him as being a benevolent and thoughtful god, one which had a deep and intimate relationship with his creations. The demons affectionately refer to him as their Father and they have nothing but praise to sing of him. Since there are not many different sources to cross reference, it may not be possible to get an unbiased examination of Urh'Rok's personality.

Their homeworld is described as a collection of fragmented continents held together only by Urh'Rok's will. According to the demons, this was the result of a great cataclysm which came through a Sher'Thul far portal. Their records state this cataclysm occurred roughly at the same time as the Spellblaze did on Eyal. This suggests that the Spellblaze had far reaching consequences beyond our current understanding and could have impacted multiple worlds.

Despite the benevolent and gentle demeanour he has been attributed in his myths, demons have frequently declared their atrocities committed against Eyalites in his name. This contrast in his attitude toward Eyalites and his own creations does not suggest a benevolent disposition, but rather one similar to a father protecting his spoiled children. His existence proves that gods are not a phenomena which are isolated to simply Eyal, but may exist on countless other worlds too.
```
译文：
```text
乌鲁洛克被认为是玛·洛克世界的神，创造了我们称作恶魔的种族。所有关于乌鲁洛克的神话都将其描述为一个仁慈而体贴的神，与他的造物有着深厚的感情。恶魔们亲切地将他称作“父亲”，对他的形容只有无尽的赞歌。由于并没有很多其他来源的佐证，很难对乌鲁洛克的真实个性做出公正客观的评述。

恶魔的家乡被描述为一片破碎的大陆，仅仅因为乌鲁洛克的意志才聚集在一起。据恶魔们说，这是一场从夏·图尔人的远行传送门中释放出的巨大灾难造成的结果。根据它们的记载，这场灾难发生的时间与魔法大爆炸大致吻合，提示魔法大爆炸的影响可能触及了众多的世界而远远超出我们的理解。

虽然乌鲁洛克在神话中的形象和蔼可亲，恶魔们却经常以他的名义来对埃亚尔的居民实施各种暴力。这种对埃亚尔居民和他自己的造物截然相反的态度表明他并非真的仁慈，而更像是一个保护着、溺爱着孩子的父亲。他的存在证明了神并非仅仅是埃亚尔独有的现象，还可能存在于其他无数的世界之上。
```

## entry-03561
位置：tome-cults.lua:2312；section：tome-cults/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Message from the Assassin's Lord
```
译文：
```text
来自刺客领主的消息
```

## entry-03562
位置：tome-cults.lua:2383；section：tome-cults/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Only one person escaped alive from the summoning of the Unspeakable Thing. She believed that, despite the failure of her fellow students and the horror of what she saw, The Teacher's wisdom still had value in the apocalyptic world created by the Spellblaze. After all, is it not better to know about the horrors out there than it is to be ignorant of their existence? She began to pass on the power of entropy onto others, and they too passed it on. The ones who learned this forbidden lore became known as the Cultists of Entropy.

What became of The Teacher is unknown. Perhaps it didn't survive the encounter with the Unspeakable Thing, or perhaps it returned to its home somewhere far beyond Eyal.
```
译文：
```text
不可名状的恐怖降临之时，只有一个人幸存逃离。她坚信，尽管她的同学们失败地召唤出了她所看到的无法言说的恐怖，但导师的智慧教诲在魔法大爆炸后这个灾变后的世界仍然有着无法替代的价值。毕竟，比起那些恐怖本身，对恐怖的无知不是更加糟糕吗？她开始向其他人传授有关熵的力量的知识，而这一知识也就这样代代相传。那些掌握了这些禁忌知识的人，现在被称为熵教徒。

没有人知道“导师”去了哪里。也许，他没能在不可名状的恐怖之下幸存；也许，他离开了埃亚尔，回到了自己遥远繁星中的家园。
```

## entry-03563
位置：tome-cults.lua:2441；section：tome-cults/data/lore/zones.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The whispers... Even as I'm running away, the whispers don't stop. It echoes over and over again. I can feel the walls of my mind crumbling down. It wants me to go back. I won't go back, not after what happened. All of them died, melted and devoured, broken and torn asunder... The writhing mass, the endless aberrant things... One drake towered above them all. It whispered to me, just like in my dreams... It had no eyes, but it looked right through me. All of my mortal emotions, thoughts and dreams were laid bare before its hideous visage... And it laughed. It laughed with a horrid, psychic shriek.

It wants me to go back. It wants me to return so it can finish what it started. No, no, no. I must write this report. Tell the Ziguranth. I must send this away, I... I... I must go back it wants me to go back I-I-I [i](Nothing but a series of erratic and completely incoherent scribblings follow. Judging by where you found this letter, he did not make it back to Zigur.)[/i] 
```
译文：
```text
那些低语……我想要逃跑，可这些低语丝毫没有停止。它在我的脑海中不断回响。我能感受到我心灵的壁垒摇摇欲坠。它想要我回去。我绝不会回去，不管发生了什么都不会。他们都死了。融解，吞噬，破损，撕裂……扭动的肉块，无穷无尽的憎恶……还有，高耸于那些恐怖存在之上的一条巨龙。它朝我发出耳语，就像之前出现在我梦中的情景一样……它没有眼睛，但它仿佛已经看穿了我。我作为凡人的思维、情感，还有那份挥之不去的噩梦，都赤裸地展现在那种怪物丑陋的面貌面前……它发出了笑声。它发出了恐怖，癫狂的尖笑。

它要我回去。它要我回去，完成它的任务。不，不，不。我必须写完这份报告。我必须把这份报告交给伊格兰斯。我…我…我…我必须回去。它希望我回去。我—我—我 [i]（接下来的内容里，已经看不到任何成型的文字，只剩下一团混乱疯狂的杂碎笔迹。从你找到这封信的位置来看，恐怕，他并没能把这个消息带回伊格。）[/i] 
```

## entry-03564
位置：tome-cults.lua:2491；section：tome-cults/data/lore/zones.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Being an adventurer is supposed to be fun. You know, get out there, kill a couple monsters, grab some loot, spend all the loot money you made and repeat. There's always something new out there to plunder, if you get in there before everyone else. But sometimes, people like to lock their loot behind dumb puzzles. Like this one. I've been sitting here just trying different combinations in this thing. All day, all night, different combinations. The way this stupid thing works doesn't make any sense at all! Most people who make puzzles like these usually leave some hints, but I've got nothing to work with!

So, my approach has been to just keep trying different combinations until something eventually works. I'll record the combination down in this journal and then give it a tick or a cross. That way I can keep track of what works and what doesn't. There had better be an amazing reward for all this work...

#{italic}#(The list appears to have nothing but crosses next to combinations, except for the very last one at the bottom. Surprisingly, it has neither a tick nor a cross next to it. Maybe he did not get a chance to test it?)#{normal}#
%s
```
译文：
```text
当个冒险家本来应该是有趣的。你知道的，就像这样，到处走来走去，杀杀怪物，捡捡装备，把装备卖掉换成钱，然后再重复一遍。只要你能比别人先行动一步，你总能找到四处掠夺的机会。但是有时候，那些人喜欢把战利品锁在愚蠢的谜题里面，就像这个一样。我坐在这里，不停地尝试着不同的组合。我日夜不休，不停尝试，毫无结果。这种愚蠢的东西根本毫无意义！大部分人如果想要设计个谜题，总得弄点线索吧？可我什么都没找到！

所以，我唯一的办法就是不停尝试不同的组合，直到奏效为止。我在日志上记录下那些组合，然后给那些组合打钩或者打叉。这样我就知道哪些组合是有用的，而哪些不是。真是种该死的工作，希望最后能给我弄点好点的奖励……

#{italic}#（这个列表上列举着的几乎所有的组合都打着叉，除了最后一行以外。令人奇怪的是，这个组合既没有打钩也没有打叉。也许，他已经没有机会去试试这个组合到底好不好了？）#{normal}#
%s
```

## entry-03565
位置：tome-cults.lua:2626；section：tome-cults/data/talents/demented/calamity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your touch carries an entropic curse, marking your victims for a terrible fate. Each time you deal damage to a target, they are Jinxed for 5 turns. This stacks up to 10 times, reducing saves and defense by %0.2f and critical strike chance by %0.2f%%.
			This can only be applied once per target per turn and will fade entirely if you break line of sight with your target for more than 2 turns.
```
译文：
```text
你的触碰伴随着熵之诅咒，为目标带来悲惨的命运。每当你对目标造成伤害时，目标将被厄运诅咒 5 回合。厄运可以叠加 10 层，每层减少 %0.2f 豁免和闪避，%0.2f%% 暴击率。
		每个目标每回合只能受到一层诅咒。如果在过去 2 回合里目标消失在你的视线中，所有诅咒都会消退。
```

## entry-03566
位置：tome-cults.lua:2632；section：tome-cults/data/talents/demented/calamity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you apply Jinx to an enemy, you have a %d%% chance to siphon some of their luck for yourself for 5 turns. This stacks up to 10 times, increasing saves and defense by %0.2f and critical strike chance by %0.2f%%.
		If you know Preordain, stacks beyond 6 also grant a %d%% chance for you to entirely avoid damage taken.
```
译文：
```text
每当你向敌人施加厄运诅咒，有 %d%% 几率吸取敌人的运气为你所用，持续 5 回合。这个效果最多叠加 10 层，每层增加 %0.2f 豁免和闪避，%0.2f%% 暴击率。
		如果你同时学会了命中注定，六层以上的每层幸运使你获得 %d%% 几率完全避免受到的伤害。
```

## entry-03567
位置：tome-cults.lua:2647；section：tome-cults/data/talents/demented/chronophage.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are surrounded by a vortex of entropic energy that feeds on the timelines of others. Each time you cast a spell random targets in radius 10 begin rapidly aging and decaying, reducing all stats by %d for 8 turns, stacking up to %d times.
			Up to %d stacks total will be applied to enemies each cast with a max of 2 stacks on the same target.
```
译文：
```text
吸收他人时间的熵能漩涡围绕着你。当你释放法术时，半径 10 格内的随机目标将迅速老化、凋零，所有属性降低 %d，持续 8 回合，效果可叠加 %d 层。
			每次施法可以释放最多 %d 层加速衰老，但同一目标一次最多增加 2 层效果。
```

## entry-03568
位置：tome-cults.lua:2670；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your bond with horrors to summon three decaying devourers for %d turns.
The decaying horrors cannot move and will attack all hostile creatures around them. They possess the talents Bloodbath, Gnashing Teeth and Frenzied Bite.
All its primary stats will be set to %d (based on your Magic stat), life rating increased by %d, and all talent levels set to %d.  Many other stats will scale with level.
Your increased damage, damage penetration, critical strike chance, and critical strike multiplier stats will all be inherited.
```
译文：
```text
你利用和恐魔的联系召唤三个持续 %d 轮的腐败的吞噬者。
		腐败的吞噬者不能移动，能攻击周围所有敌对生物。它们拥有浴血奋战、咬牙切齿和狂乱撕咬技能。
		它们的所有主属性将设为 %d（基于你的魔法属性），生命成长增加 %d，所有技能等级设为 %d。许多其他属性与技能等级相关。
		它们将继承你的伤害加成、伤害抗性穿透、暴击几率和暴击伤害系数。
```

## entry-03569
位置：tome-cults.lua:2680；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your bond with horrors to summon a decaying bloated horror for %d turns.
The decaying horror cannot move and will attack all hostile creatures in range of it. It possesses the talents Mind Disruption and Mind Sear.
All its primary stats will be set to %d (based on your Magic stat), life rating increased by %d, and all talent levels set to %d.  Many other stats will scale with level.
Your increased damage, damage penetration, critical strike chance, and critical strike multiplier stats will all be inherited.
		
```
译文：
```text
你利用和恐魔的联系召唤一个持续 %d 回合的腐败的浮肿恐魔。
		腐败的恐魔不能移动，能攻击范围内的所有敌对生物。它拥有精神干扰和精神光束技能。
		它们的所有主属性将设为 %d（基于你的魔法属性），生命成长增加 %d，所有技能等级设为 %d。许多其他属性与技能等级相关。
		它们将继承你的伤害加成、伤害抗性穿透、暴击几率和暴击伤害系数。
		
```

## entry-03570
位置：tome-cults.lua:2691；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You forcefully try to turn a creature into an horror.
If the target fails a magical save against your Spellpower, its appearance turns into that of a horror for %d turns, making all other creatures hostile to it.
Enemies near the target will have their target cleared on application.
This spell does not work on horrors.
```
译文：
```text
你强行让一个生物变化为恐魔。
		如果目标生物未能通过魔法豁免，%d 回合内它的相貌将转变为恐魔，令周围其他生物与之敌对。
		目标生物周围的敌人将重新考虑其攻击目标。
		该法术对恐魔无效。
```

## entry-03571
位置：tome-cults.lua:2699；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You attune your horrors to the dead god Amakthel, increasing your summoned horrors damage by %d%%.
At talent level 3, your Decaying Devourers spell will summon 4 additional Devourers adjacent to random enemies nearby and your Bloated Horror will learn the Agony talent.
At talent level 5, victims of your Horrific Display spell will pull enemies in radius 10 1 space towards them each turn.
The damage increase is based on your Spellpower.
```
译文：
```text
你将你的恐魔和已死之神阿马克泰尔同化，增加恐魔 %d%% 伤害。
		技能等级 3 后，你的腐败的吞噬者法术将额外召唤四名吞噬者在随机敌人周围，你的浮肿恐魔将学会极度痛苦。
		技能等级 5 后，恐怖展示的受害者每回合会把范围 10 码内的敌人拉近 1 码。
伤害加成受法术强度加成。
```

## entry-03572
位置：tome-cults.lua:2762；section：tome-cults/data/talents/demented/disfigured-face.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your tongue turns into a diseased tentacle that you use to #{italic}#lick#{normal}# enemies in a cone.
		Licked creatures take %d%% tentacle damage that ignores armor and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.
		
		If at least one enemy is hit you gain %d insanity.
		
		Disease damage will increase with your Spellpower.
```
译文：
```text
你的舌头化作疫病触手，让你能 #{italic}#舔舐#{normal}# 锥形范围内的敌人。
		被舔舐的敌人受到无视护甲的 %d%% 触手伤害并获得一种持续 %d 回合的随机疾病，每回合造成 %0.2f 枯萎伤害并减少力量、敏捷或体质 %d 点。
		如果你至少命中了一名敌人，你获得 %d 疯狂值。
		疾病伤害受法术强度加成。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Defiler	堕落系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Library	图书馆	T.GAME.ENTITY	places	entity name	existing	core	城镇实体
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mind Sear	心灵灼烧	T.GAME.TALENT	talents	talent name	preferred	core	sear 指灼烧；技能机制虽为射线，名称不增译“光束”
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Runemaster	大师符文店	T.GAME.ENTITY	places	entity name	existing	core	城镇商店实体
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Tumble	翻筋斗	T.GAME.TALENT	talents	talent name	existing	core	
Wilder	野性系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
book	书	T.GAME.ENTITY	items	entity type	existing	global	
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
potion	药水	T.GAME.ENTITY	items	entity type	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
trance	入定	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	灵能系技能类型；指专注的入定状态，不是幻想
unknown	未知	T.UI.LABEL	ui	_t	preferred	global	未知条目/名称占位（15 处）
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
