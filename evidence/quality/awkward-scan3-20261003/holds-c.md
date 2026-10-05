# C 档搁置 21 条的处理

2026-10-05。主代理逐条查源码上下文（本体按版本清单固定的 `624a6732`，三个 DLC 用本机检出、来源未固定）给出结论；用户同意修改其中的错译与润色两类。改动经 GPT-6.1 Sol 独立复核（14 组 16 行，确认完整读到），无异议。

| 位置 | 结论 | 依据 |
|---|---|---|
| mod-tome.lua:5987 | 改（错译） | 堡垒中没有 archives 房间，源码中该词只出现于此句；官方日文、韩文版均理解为“档案中有解决办法”。 |
| mod-tome.lua:11465 | 改（错译） | 正文开头即称各族传说“都只是神话”，随后以逻辑推论世界由何而来；分析对象是创世本身。同文的 `mod-tome.lua:17766` 一并修改。 |
| mod-tome.lua:18420 | 改（错译） | 正文是给新特工的欢迎信（结尾“Welcome to Point Zero, agent”），Orientation 指新人指引。 |
| mod-tome.lua:19333 | 改（错译＋拼接） | 源码把“There is some text underneath ”与后一片段直接拼接；原前缀拼出“下面有一行文字不明意义的文字：”或缺冒号。另 powerful auras 误作“强大领域”，god-like 误作“上古巨神”。第 2、3、5、6、7 幅前缀同改为“下方写着”（与第 4 幅一致），第 8 幅前缀补冒号。 |
| mod-tome.lua:19336 | 维持（随前缀修复） | 片段本身不改；前缀改为“下方写着”后拼接为“下方写着不明意义的文字：……”。 |
| mod-tome.lua:4644 | 改（润色） | %s 为工具技能名；同一技能树中 prepared 译作“已准备”。 |
| mod-tome.lua:5403 | 改（润色） | 该选项只在已找到治疗办法后出现，随后 Melinda 问“Please tell me you can help!”；something 宜作“有些眉目”。 |
| tome-orcs.lua:583 | 改（润色） | 第一个 %s 填“学习／提升”，拼出“[学习 技能 X (+1 等级)]”。同运行键的 `mod-tome.lua:425`（护送奖励）同用法，按跨组件同步一并修改。 |
| tome-cults.lua:1852 | 改（润色） | 本章讲亡灵穿过迷雾帷幕涌向埃尔瓦拉；DOA 双关无法直译，“死亡到来”意思偏虚。 |
| mod-tome.lua:4263 | 维持 | 玩家上一句问“想必他已经安全到家了吧？”，he did 即平安到家。 |
| mod-tome.lua:4643 | 维持 | 该对话中 mastery 一律译“强化”（“强化哪件工具？”及各“……强化”技能名）。 |
| mod-tome.lua:4645 | 维持 | 同上；第三个 %s 是强化技能名。 |
| mod-tome.lua:4660 | 维持 | 两个 %s 依次为工具名与工具栏技能名，“将 %s 装备至 %s”方向正确。 |
| mod-tome.lua:4724 | 维持 | 紧接玩家问“你是怎么跟我说话的？”，curious 为“好奇”。 |
| mod-tome.lua:4726 | 维持 | “日耀神使”为术语库 preferred 译名。 |
| mod-tome.lua:5104 | 维持 | 玩家刚选“毁灭水晶球”，that 即该水晶球；同组分支译法一致。 |
| mod-tome.lua:5105 | 维持 | 同上（巨龙水晶球）。 |
| mod-tome.lua:5538 | 维持 | 上一句玩家说多年来把安格利文当作家，补出“把那里当作家”是必要的。 |
| mod-tome.lua:19361 | 维持 | 术语库定“弑神者”为九名夏·图尔人的称号，DLC lore 亦称这九人为 Godslayers。 |
| tome-ashes-urhrok.lua:1782 | 维持 | %s 填“背叛／屠戮”，拼出恶魔断续的台词，可读，与 DLC 官方中文一致（DLC 源码未固定）。 |
| tome-orcs.lua:2637 | 维持 | “Wei...”是故意截断（正文说该页已烧毁），保留“Wei……”；“人种”与同系列标题一致（DLC 源码未固定）。 |

## 改动对照

| 位置 | 英文 | 原译 | 新译 |
|---|---|---|---|
| mod-tome.lua:5987 | Demonic taint. Yes I have a way to help in the archives. However this is a long process, the subject will need to live here for a while.<br>She will have to spend 8 hours per day in the regeneration tank. | 恶魔污染。是的，我有办法在档案区帮她。不过这个过程很漫长，她需要在这里住上一段时间。<br>她每天必须在再生槽中待上 8 小时。 | 恶魔污染。是的，档案里记载着可以帮她的方法。不过这个过程很漫长，她需要在这里住上一段时间。<br>她每天必须在再生槽中待上 8 小时。 |
| mod-tome.lua:11465 | a logical analysis of creation, by philosopher Smythen | 创世传说的逻辑分析，哲学家斯迈森著 | 对创世的逻辑分析，哲学家斯迈森著 |
| mod-tome.lua:17766 | a logical analysis of creation, by philosopher Smythen | 创世传说的逻辑分析，哲学家斯迈森著 | 对创世的逻辑分析，哲学家斯迈森著 |
| mod-tome.lua:18420 | Warden-Master Galsamae's Orientation Notes | 时空守卫大师加尔萨麦的时空导航笔记 | 时空守卫大师加尔萨麦的新人须知 |
| mod-tome.lua:19333 | You see here a mural showing a dark and tortured world. Large, god-like figures with powerful auras fight each other, and the earth is torn beneath their feet.<br>There is some text underneath  | 你能在这壁画上看到一个黑暗和痛苦的世界。有着强大领域的上古巨神们在互相厮杀，大地在他们脚下龟裂。<br>下面有一行文字 | 你能在这壁画上看到一个黑暗和痛苦的世界。散发着强大气场、形似神明的巨大身影在互相厮杀，大地在他们脚下龟裂。<br>下方写着 |
| mod-tome.lua:19339 | In this picture a huge god with glowing eyes towers above the land, and in his right hand he holds high the sun. The other gods are running from him, wincing from the light.<br>There is some text underneath  | 画中，一位双眼发光的巨神高耸于大地之上，右手高举着太阳。众神纷纷逃离他，被光芒刺得直皱眉。<br>下面有一行文字 | 画中，一位双眼发光的巨神高耸于大地之上，右手高举着太阳。众神纷纷逃离他，被光芒刺得直皱眉。<br>下方写着 |
| mod-tome.lua:19345 | This picture shows the huge god holding some smaller figures in his hands and pointing out at the lands beyond. You imagine these figures must be the Sher'Tul.<br>There is some text beneath  | 这幅画显示巨神手中托着一些小小的身影，并指向远方的大陆。你猜这些身影一定就是夏·图尔人。<br>下面有一行文字 | 这幅画显示巨神手中托着一些小小的身影，并指向远方的大陆。你猜这些身影一定就是夏·图尔人。<br>下方写着 |
| mod-tome.lua:19357 | This mural shows nine Sher'Tul standing side by side, each holding aloft a dark weapon. Your eyes are drawn to a runed staff held by the red-robed figure in the centre. It seems familiar somehow...<br>There is some text beneath  | 这幅壁画显示了九个夏·图尔人肩并肩站着，每人手里都高举着一件黑色武器。画面中央，红袍者手中的符文法杖吸引了你的注意。它看起来很眼熟……<br>下面有一行文字 | 这幅壁画显示了九个夏·图尔人肩并肩站着，每人手里都高举着一件黑色武器。画面中央，红袍者手中的符文法杖吸引了你的注意。它看起来很眼熟……<br>下方写着 |
| mod-tome.lua:19363 | You see images of epic battles, with Sher'Tul warriors fighting and slaying god-like figures over ten times their size.<br>There is some text underneath  | 你在这幅壁画上看到一幕幕史诗般的战斗——夏·图尔战士们正与体型超过自身十倍、形似神明的存在厮杀，并将其斩灭。<br>下面有一行文字 | 你在这幅壁画上看到一幕幕史诗般的战斗——夏·图尔战士们正与体型超过自身十倍、形似神明的存在厮杀，并将其斩灭。<br>下方写着 |
| mod-tome.lua:19369 | You see the red-robed Sher'Tul striking the huge god with the dark, runed staff. Bodies litter the floor around them, and the golden throne behind is bathed in blood. The light in the god's eyes seems faded.<br>There is some text underneath  | 你看到红袍夏·图尔人用那根刻有符文的黑色法杖攻击巨神。周围尸横遍地，后方的黄金王座浸满鲜血。巨神眼中的光芒似乎已经黯淡……<br>下面有一行文字 | 你看到红袍夏·图尔人用那根刻有符文的黑色法杖攻击巨神。周围尸横遍地，后方的黄金王座浸满鲜血。巨神眼中的光芒似乎已经黯淡……<br>下方写着 |
| mod-tome.lua:19375 | The large mural shows the great god spread on the ground, with the dark staff held against his chest. Sher'Tul surround him, some hacking off his limbs, cutting out his tongue, and binding him with chains. A burst of light flares up from where a tall Sher'Tul warrior is gouging his eye with a black-bladed halberd. In the background a Sher'Tul mage beckons to a huge chasm in the ground.<br>The text beneath says simply  | 这幅巨大的壁画上，真神瘫倒在地，那根黑色法杖抵在他的胸口。夏·图尔人围绕着他，有的砍下他的肢体，有的割下他的舌头，还有的用锁链将他捆住。一名高大的夏·图尔战士正用黑刃长戟剜他的眼睛，剜眼之处迸发出一阵光芒。远处，一名夏·图尔法师朝地面上的巨大深渊示意。<br>下面的文字只有一句 | 这幅巨大的壁画上，真神瘫倒在地，那根黑色法杖抵在他的胸口。夏·图尔人围绕着他，有的砍下他的肢体，有的割下他的舌头，还有的用锁链将他捆住。一名高大的夏·图尔战士正用黑刃长戟剜他的眼睛，剜眼之处迸发出一阵光芒。远处，一名夏·图尔法师朝地面上的巨大深渊示意。<br>下面的文字只有一句： |
| mod-tome.lua:4644 | #LIGHT_BLUE# You enhance your preparation of %s. | #LIGHT_BLUE# 你强化了对 %s 的准备。 | #LIGHT_BLUE# 你强化了已准备的 %s。 |
| mod-tome.lua:5403 | About what happened on the beach, I think I have found something. | 关于海滩上发生的事，我想我找到办法了。 | 关于海滩上发生的事，我想我有些眉目了。 |
| tome-orcs.lua:583 | [%s talent %s (+%d level(s))] | [%s 技能 %s (+%d 等级)] | [%s技能 %s（+%d 级）] |
| mod-tome.lua:425 | [%s talent %s (+%d level(s))] | [%s 技能 %s (+%d 等级)] | [%s技能 %s（+%d 级）] |
| tome-cults.lua:1852 | Escapades of Fay Willows [Book 5, Chapter 1] - Dead On Arrival | 菲·维莉欧斯的冒险 [第5卷，第1章] - 死亡到来 | 菲·维莉欧斯的冒险 [第5卷，第1章] - 亡者来袭 |
