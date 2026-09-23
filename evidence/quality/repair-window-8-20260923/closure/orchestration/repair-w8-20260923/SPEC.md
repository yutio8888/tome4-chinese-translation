# 修复窗口8：254批6条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线b626eaf1c30ed389dff0b0a633e393225ea46843。用户2026-09-23授权工具维护后持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。本窗口因unlock-yeek换行不变量及麻痹毒素伤害方向提前修复。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的6个target及evidence/quality/repair-window-8-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf/markup保持不变。唯一格式例外e92433bcba必须恢复原文12个LF（现译13个：把“……有点滑稽。\n不过他们是……”合为一行）；其他条目LF/TAB保持基线。

6条<4-lane阈值外但按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5），审核模型依用户2026-09-23指示。max_cycles默认3。LuaJIT全记录比较恰6个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核255。

范围约束：cunning=灵巧保持（术语库stat名）；ALL_DREAMS仅改成就名；诗句仅改Once flowers rose与Now all lost, now all fled两行（blossoms/beech可顺带贴合同行但不扩大）；龙族传说只修may borne from delusions、Daikara Pass and surrounding mountain chains、over 40'、newly matured四处，不改第一人称增译等advisory；麻痹毒素只改为目标造成的全部伤害降低。排除其他advisory、e923d2b8宿主补充观察、旧Archmage/回忆录pending/RW1-SIB-01/02/已有blocked或其他repair。

## e8fc5b0a4a9d6c3e85ebcbf79ddc5b41a7e1b2c8d28b1a47d34440af8167e8a2

section: mod-tome/data/talents/cursed/cursed.lua
source_tag: _t

source: Each day, you lift your weary body and begin the unending hunt.

target: 你不知疲倦无时无刻狩猎你的下一个目标。

确认依据：cursed.lua:22 endless-hunt 技能树描述：Each day, you lift your weary body and begin the unending hunt。译文“你不知疲倦无时无刻狩猎你的下一个目标”把疲惫的身体反转为不知疲倦，并丢失每天起身开始无尽狩猎的意象，意义相反，需修复。
与 surface 键同一缺陷的独立语境复核：cursed.lua:22 weary 被反转为不知疲倦，丢失 each day 与起身意象并新增下一个目标；确认修复整句。

## e90949f9259fbaa1b4aeb7bbdef559ace4df0d4539c8c53e005c3d8c9dd5d43c

section: mod-tome/data/achievements/quests.lua
source_tag: achievement name

source: Dreaming my dreams

target: 我的梦就是你的梦

确认依据：quests.lua:337–340 ALL_DREAMS 成就名 Dreaming my dreams，desc 为体验并完成 Dogroth Caldera 全部梦境。译文我的梦就是你的梦新增第二人称并改成两人梦境等同的断言，偏离原名含义；surface 与独立 contextual 均指出，宿主据源码确认，应恢复为做着我的梦类表述。
独立语境复核与 surface 一致：成就名新增你的梦、改变含义；确认有界修复标题。

## e92433bcbaf2d4dc438a1651a4cb5214c7e4c8dae5438f8418253e0e829740af

section: mod-tome/data/texts/unlock-yeek.lua
source_tag: _t

source: Yeeks are a mysterious race of small humanoids native to the tropical island of Rel.
Their body is covered with white fur and their disproportionate heads give them a ridiculous look, yet they are a cunning and willful race.
Although they are now nearly unheard of in Maj'Eyal, they spent many centuries as secret slaves to the Halfling nation of Nargol.
They gained their freedom during the Age of Pyre and have since then followed 'The Way' - a unity of minds enforced by their powerful psionics.

You have helped a Yeek Wayist and can now create a new character with the #LIGHT_GREEN#Yeek race#WHITE#.

Race features:#YELLOW#
- Mental domination racial power
- Confusion resistance
- Fast leveling
- Frail body#WHITE#


target: 夺心魔是热带小岛瑞尔岛上比较神秘的人形原住民种族。
他们的身体长着白色的毛发，另外他们有着不成比例的巨大脑袋使他们看上去样子有点滑稽。
不过他们是非常灵巧而且意志强大的种族。
尽管在马基·埃亚尔几乎没有听说过他们，但在烈火纪元之前的漫长岁月里，他们曾是半身人国家纳格尔的秘密奴隶。
他们在烈火纪元获得了自由，并从此遵循“维网”——一种由他们强大的灵能维系的心灵统一。

你帮助了一名夺心魔维网信徒，现在你可以在创建人物时选择新的种族：#LIGHT_GREEN#夺心魔#WHITE#。

种族特点：#YELLOW#
- 拥有精神控制的种族能力
- 混乱抗性
- 升级较快
- 脆弱的身躯#WHITE#


确认依据：unlock-yeek.lua:22–34 原文 12 个换行，译文 13 个：原第 23 行一句被拆成“……有点滑稽。\n不过他们是……”两行，违反 newline 不变量，确认修复（合并为一行）。cunning 译灵巧与术语库 Cunning=灵巧（stat name）一致，不作修复。

## e9253668295a71c738227e4186efa5e9fa86c30ccc629240168490030d584083

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: You see a moss covered statue of a Thalore reciting a poem, over and over.
#{italic}#"Where bright and berried yews did stand,
Where the eldest oaks grew so grand,
Where singing birds once flew to land,
All is dust, all is dead.

Once flowers rose to reach the sky,
Once blossoms fell from beech on high,
Once thrush and owl did screech and cry,
Now all lost, now all fled.

Oaths from Shaloren mages sworn,
Yet spells of fiery rages born,
Our lands of bygone ages torn,
Gone is trust, wrath is red.#{normal}#


target: 你看见，长满青苔的自然精灵雕像，叙述一首诗，一遍又一遍。
#{italic}#“挂满鲜亮浆果紫衫之地
古老橡木生长之地
欢唱鸟儿飞落之地
皆为尘土，皆为虚无

曾经炽热的复仇火焰染红天空
曾经怒放的花儿跌落枝头
曾经欢快的鸟儿泣血啼鸣
今为尘土，今为虚无

尽管永恒精灵法师们誓言在先
但法术的怒火仍撕裂尘世
我们曾经的故土化为废墟
信任不再，愤怒永存#{normal}#


确认依据：所附 observation（cunning 译灵巧）属上一条 yeek 的错位；但本条 misc.lua:530–545 Thalore 诗句自身有独立缺陷：Once flowers rose to reach the sky 被译为曾经炽热的复仇火焰染红天空，把花朵高耸误写成复仇火焰，改变诗意与意象（与下句 blossoms、thrush and owl 同为昔日繁盛），经宿主独立核验确认需修复。
misc.lua:530–545 诗句 Once flowers rose to reach the sky 被虚构为复仇火焰，Now all lost, now all fled 被复写成首节的尘土/虚无；确认修复该两行。blossoms/beech 细节属建议，可在修复同句时顺带贴合但不扩大范围。

## e95173943342a9e768bab3bcbc0709b0fdc636b0973da55b20e3435d18206041

section: mod-tome/data/talents/corruptions/blight.lua
source_tag: tformat

source: A furious storm of blighted poison rages around the caster in a radius of %d for %d turns.  Each creature hit by the storm takes %0.2f blight damage and is poisoned for %0.2f blight damage over 4 turns.
		At talent level 2 you have a chance to inflict Insidious Blight, which reduces healing by %d%%.
		At talent level 4 you have a chance to inflict Numbing Blight, which reduces all damage dealt by %d%%.
		At talent level 6 you have a chance to inflict Crippling Blight, which causes talents to have a %d%% chance of failure.
		Each possible effect is equally likely.
		The poison damage dealt is capable of a critical strike.
		The damage will increase with your Spellpower.

target: 一股强烈的剧毒风暴围绕着施法者，半径 %d 持续 %d 回合。风暴内的生物将进入中毒状态，受到 %0.2f 枯萎伤害并中毒 4 回合受到额外 %0.2f 枯萎伤害。
		技能等级 2 时有几率触发阴险毒素效果，降低 %d%% 治疗系数。
		技能等级 4 时有几率触发麻痹毒素效果，降低 %d%% 伤害。
		技能等级 6 时有几率触发致残毒素效果，%d%% 几率使用技能失败。
		中毒几率在可能的毒素效果中平分。
		毒素伤害可以暴击。
		伤害受法术强度加成。

确认依据：magical.lua:4259–4261 NUMBING_BLIGHT long_desc: All damage it does is reduced by %d%%；blight.lua:212 reduces all damage dealt。译文降低 %d%% 伤害未说明是目标造成的全部伤害，可被读为受到伤害降低，方向歧义属机制描述缺陷，确认修复该行。

## e9884825395b8560158bbeb0af351556ef369bf2154122ad9c0b7ef1a035f989

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: The common man may scoff at the idea of classifying dragons as an intelligent race, but experienced wyrmics know otherwise. Dragons are incredibly long-lived creatures, with some known to survive for thousands of years. Though in their early life they are of a bestial nature, as they advance through the centuries they gain an ever keener and more developed intellect. The eldest of wyrms are sometimes considered the most subtle and intelligent of creatures in Maj'Eyal, capable of telepathic communication and advanced mental abilities, and wyrmics speak of them with the highest reverence.

Dragons come in many shapes and sizes, normally growing from 5' long hatchlings to 20' long mature drakes, with some of the greatest wyrms growing to over 40' in length. They are generally winged, with large lizard-like maws and sharp talons on both their fore and hind legs. They are often noted for the lustrous colour of their scales, normally representing an attunement to one of the key Elements of Eyal. This attunement is unseen in any other race, and some philosophers believe that dragons predate all other races, being formed as raw representations of the elements of nature at the beginning of the world. However this theory may be borne purely from the fanatical delusions of certain wyrmics who have studied the creatures for too long.

All corners of Maj'Eyal show some trace of different types of dragons. The Daikara Pass and surrounding mountain chains are home to a great number of ice and storm dragons. Numerous sand and red dragons can be found in the western desert and hills, and many have been the reports of gigantic sea dragons in the deepest oceans, especially to the south.

Attacks from dragons on humans and halfling settlements are fairly rare, but when they occur they can be truly devastating. Usually they are to feed on livestock, but now and then come attacks from newly matured drakes, seeking out precious metals and gemstones to build up a hoard. Dragon hoards have become a thing of legend, with the greatest wyrms rumoured to protect literal mountains of gold, but in modern times truly sizeable hoards are rare. The dwarves farmed hoarding dragons almost to extinction in the Age of Allure, and most dragons these days retain only modest treasures in their lairs.

Dragons are regularly hunted for their thick scales and their elementally imbued bones. Dragonskin leather is prized amongst armour-workers, as when properly treated it is both light and tough, and oft retains some inkling of the original wyrm's power. Dragon-bone is highly favoured by staff-crafters for its natural attunement to elemental forces, and is sometimes used by fletchers in the crafting of the most delicate yet resilient bows and arrows. However the hunting of dragons for their skin and bones is greatly opposed by many wyrmics, and there is an increasing market for "naturally harvested" drake materials - those taken from dragons which have died of natural causes. Still, demand for all dragon materials is strong with exceptionally high prices paid, and many are the greedy souls that lose their lives each year at the fangs and claws of these magnificent creatures.

target: 一般人也许会嘲笑我把龙作为单独列出的智慧种族，但是经验丰富的龙战士们知道其实不然。龙族是另人难以置信的长寿生命，某些已知的龙族已经存活了数千年之久。尽管在他们早期的生命中，他们兽性的一面比较多，但是随着他们生活几个世纪以后，他们会获得前所未有的超强理解力。那些远古巨龙有时被认为是马基·埃亚尔最狡猾和富有智慧的生物，他们拥有心灵沟通和优秀的精神能力，并且龙战士们始终对龙族有着最崇高的敬意。

龙族有着不同的大小和形状，一般常见于5英尺长的幼仔到20英尺长的成年龙族，某些最强大的龙族体长能达到40英尺。他们通常是带翅膀的、有着蜥蜴般的巨口，前后肢都生有锋利的巨爪。他们通常有着鲜艳色彩的鳞片，通常代表与埃亚尔某种元素的亲和。这种亲和力在任何其他种族都未曾出现过，有些学者认为，龙族先于其他一切种族存在，是在世界之初作为自然元素的原初具现而形成的。然而这个理论只有那些狂热的研究了龙族太久的龙战士信徒们才会相信。

马基·埃亚尔的每一个角落都能发现不同类型的龙族。岱卡拉山脉聚集了很多的冰龙和风龙。大量的沙龙和赤龙可以在西部沙漠和丘陵中找到，并且还有许多报道提到在大洋深处有着巨大的海龙，尤其是在南部地区。

龙族攻击人类和半身人聚居地的事情是少见的，但一旦出现这种情况，通常是毁灭性的灾难。通常它们是为了找牲畜吃，但有时也有来自成年巨龙的攻击，是为了寻找贵金属和宝石来作储藏。龙族的财富已经成为了一种传奇，传说那些最伟大的巨龙守护着真正成山的黄金，但是现在如此多的宝藏几乎没有。矮人们在厄流纪大肆猎捕囤积财宝的龙，使这一类龙几乎绝迹，现在的大部分龙族在巢穴里只有适量的财富。

龙族经常由于它们厚实的鳞片和蕴含元素之力的骨头而被狩猎。龙皮革是护甲制作者们珍视的材料，因为经过适当处理后它既轻便又坚韧，并且通常保留着原龙的一丝力量。龙骨是法杖制作者们最喜爱的材料，因为它与元素力量的天然亲和极高，有时也被用于制造纤薄且柔韧的弓箭。然而，对龙族的不断狩猎引起了许多龙战士们的强烈不满，并且交易“自然采集”的龙族材料的市场也日益增多——那些人只取自然死亡的龙族身上的材料。尽管如此，各类龙族材料的需求依然旺盛，价格也高得惊人，每年都有许多贪婪之徒丧生于这些壮丽生物的尖牙利爪之下。

确认依据：misc.lua:509–519 races-10：may be borne purely from the fanatical delusions 被改为只有信徒才会相信（删 may 并改变主张）；The Daikara Pass and surrounding mountain chains 被缩为岱卡拉山脉；over 40' 丢失 over；newly matured drakes 丢失 newly。确认有界修复这四处；surface 所提第一人称增译仍只记建议。
