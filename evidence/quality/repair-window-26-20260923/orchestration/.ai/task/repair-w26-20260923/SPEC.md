# 修复窗口26：272批5条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线5a396dca863b75ab242ab11fdeb09b3bbafaf422。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的5个target及evidence/quality/repair-window-26-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证，并查同技能/同效果相邻条目已用译法），不自行新造。

5条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处；下列示例措辞仅为方向，落笔时仍须逐词对照原文。LuaJIT全记录比较恰5个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核273。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 思维形态技能系说明（talents/psionic/psionic.lua:49）：Manifest your thoughts as psionic summons.——psionic summons 是灵能召唤物（该系召唤思维形态实体），不是“召唤术”；如“使你的思维具象化为灵能召唤物”。
- 写给威斯曼的信 (1) 正文（lore/misc.lua:90–98，罗尔夫致威斯曼）：逐段重译。第一段 primarily mirth, with a good amount of scorn（主要是好笑，外加不少轻蔑）、Such bravery! Such pluck and derring-do! 都要译出；第二段 a most hideous, bloated, oozing and chittering horror（丑恶、臃肿、渗着黏液、吱吱作响的怪物）、No less than the giant ants' repulsive progenitor（正是巨蚁那令人作呕的始祖/母体，蚂蚁不是白蚁，不加“史前”）、hordes of frenzied chitinous young（成群狂躁的甲壳幼虫/幼蚁）、as though the ground itself was swarming forward to devour me；第三段 revealed to you your folly（让你看清自己的愚蠢）；Old Forest=古老树林、Derth=德斯（本库译名）；Weisman 沿用标题“威斯曼”，Rolf=罗尔夫。LF 结构必须与原文一致：原文共 8 个 LF、9 行（空行下标 1、3、5、7）——称呼后空行、三段正文之间各一空行、末段后空行再署名；现译 9 个 LF，把第二段拆成两段且署名前少空行，须改正。
- 泰坦的箭袋描述（general/objects/world-artifacts.lua:5678）：These massive arrows are honed to a vicious sharpness, and appear to be nearly unbreakable. They seem more like spikes than any arrow you've ever seen.——三个要点都要译出（磨得锋利无比、看上去几乎无法折断、比你见过的任何箭都更像长钉）。
- 阿塔玛森丢失的红宝石眼睛描述（zones/sandworm-lair/objects.lua:109–110）：原文只有 1 个 LF（第一句之后），现译在“虽然”前多 1 个 LF，须删去；managed to deal a crippling blow by killing their leader, Garkul the Devourer 要译出“杀死其首领吞噬者加库尔，给兽人以重创”；阿塔玛森、半身人、烈火纪保持。
- 梅琳达任务日志（quests/love-melinda.lua:28）：Melinda died to a Yaech raiding party at the beach.——补“袭击队”，如“梅琳达在沙滩上死于夺魂魔袭击队之手”；Yaech 保持本库“夺魂魔”。

## fc0f5daae4c09f990685aa7af2d68b51aae3177e24b6e1ae8807e332585f6d41

section: mod-tome/data/talents/psionic/psionic.lua
source_tag: _t

source: Manifest your thoughts as psionic summons.

target: 使你的思维具象化形成灵能召唤术。

确认依据：talents/psionic/psionic.lua:49（624a673）技能系 Thought-Forms（思维形态）说明：Manifest your thoughts as psionic summons.——该系技能召唤思维形态实体，psionic summons 指灵能召唤物；现译“灵能召唤术”把召唤物写成召唤技能（一级 fidelity）。修复为“使你的思维具象化为灵能召唤物”一类。
与 surface 同向：psionic/thought-forms 技能系召唤思维形态实体，psionic summons 是召唤物而非召唤术。并入同条修复。

## fc3dc9f6fba548a879b0c4f236efc65a6a170219fdd925e5fa4b667386026cc3

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: Dear Weisman,

Ah! What feelings your last letters inspired within me... primarily mirth, with a good amount of scorn! Must you continuously assail me with tale after tale of your waving of wooden swords and pestering of toothless mongrels? Allow me to recount your "legends" in a much more succinct manner: One day, I failed to kill a dog. Such bravery! Such pluck and derring-do!

Your petty escapades are made ever more insignificant by the trials I myself have recently overcome. Mere days ago I was trekking through the Old Forest (that's outside Derth, Weisman! Terror must already grip you!) when, by unfortunate happenstance, I came across a most hideous, bloated, oozing and chittering horror! No less than the giant ants' repulsive progenitor! Such hordes of frenzied chitinous young it had at its command, it was as though the ground itself was swarming forward to devour me!

And yet I live. Weisman, I sincerely hope that my letter has revealed to you your folly. Only when you have faced true danger can you call yourself an adventurer. Bore me with your tales no longer.

Rolf

target: 亲爱的威斯曼，

哈哈，你上次的来信真是带给我不少笑料！你这家伙到底要用这些挥舞木剑、纠缠没牙野狗的故事骚扰我到几时？就让我来演示一下你那封信件的正确读法：有一天，我没能杀死一只狗。这真是充满勇气！

你的“英雄事迹”在我近日克服的可怕梦魇面前根本不值一提。数天前我徒步穿越了远古丛林（这可是在德斯镇之外的地域，威斯曼！你可是要被吓的腿软了吧！）在那里，我不幸的遭遇了世上最可怕、最犀利、最凶猛的生物！

满地的史前巨型白蚁，它们在可怕的蚁王指挥下蜂拥而出，试图用那巨大的前颚将我碎尸万段！

即便如此我还是活下来了，威斯曼，我真心希望我的回信能让你知道世界如此巨大，你又如此渺小。只有当你真正经历过像我这样的生死考验后，才配真正称自己为冒险家。别再用你幼稚的故事来烦我了。
罗尔夫

确认依据：lore/misc.lua:86–90 起 letter to Weisman (1)：现译把 bloated, oozing and chittering horror / the giant ants' repulsive progenitor 改写为“最犀利最凶猛的生物”“史前巨型白蚁…蚁王”，漏 Such pluck and derring-do，并把第三段拆成两段、末尾署名前少一个空行，LF 10→9（一级 fidelity + 换行不变量）。整条逐段重译，段落与空行对齐原文；地名用本库译名 Old Forest=古老树林、Derth=德斯。
与 surface 同向并补充：还漏 with a good amount of scorn；revealed to you your folly 被改写为“世界如此巨大，你又如此渺小”，trials 被改写为“可怕梦魇”；署名前应为空行。并入同条逐段重译。

## fc5311ffa7bfbf69181aa62d6d9f8828d3d2cd4faad811e5a5fca534b08ca356

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: These massive arrows are honed to a vicious sharpness, and appear to be nearly unbreakable. They seem more like spikes than any arrow you've ever seen.

target: 巨大而尖锐的箭矢，不，与其说是箭，不如说是长钉。

确认依据：general/objects/world-artifacts.lua:5675–5683 The Titan's Quiver（泰坦的箭袋）描述：现译漏 honed to a vicious sharpness 与 appear to be nearly unbreakable 两个分句，并把 They seem more like spikes than any arrow you've ever seen 压成“不，与其说是箭，不如说是长钉”（一级 completeness）。整条逐句修复。
与 surface 同向并补充：than any arrow you've ever seen 也被省略。并入同条修复。

## fc60ee27ed6e5a51d5c2c42ee7dbec2d6be13a3c47733cb84e1add55b5d6cf13

section: mod-tome/data/zones/sandworm-lair/objects.lua
source_tag: _t

source: One of the ruby eyes of the legendary giant golem Atamathon.
It is said it was made by the halflings during the Age of Pyre as a weapon against the orcs. Even though it was destroyed it managed to deal a crippling blow by killing their leader, Garkul the Devourer.

target: 传奇巨像阿塔玛森的红宝石眼睛之一。
据说它是半身人在烈火纪为了对抗兽人所造的武器。
虽然它被破坏了，但是它也成功地使对方的首领吞噬者加库尔走向死亡。

确认依据：zones/sandworm-lair/objects.lua 阿塔玛森的红宝石眼睛描述：原文 1 个 LF，现译在第二、三句之间多加 1 个 LF（一级换行不变量）；且漏 managed to deal a crippling blow（给兽人以重创）。修复：恢复 1 个 LF，末句补“重创兽人”，阿塔玛森、吞噬者加库尔、烈火纪保持。
与 surface 同向：多出的换行与 crippling blow 缺失。并入同条修复。

## fc7538838d83158ca7a44e0fd8df58d4148e41965915015a634192c0c895df2a

section: mod-tome/data/quests/love-melinda.lua
source_tag: _t

source: Melinda died to a Yaech raiding party at the beach.

target: 梅琳达被沙滩上的夺魂魔杀死了。

确认依据：quests/love-melinda.lua 任务结局日志 Melinda died to a Yaech raiding party at the beach.——现译漏 raiding party（袭击队伍），读作零星遭遇（一级 completeness）。修复为“梅琳达在沙滩上死于夺魂魔袭击队之手”一类；Yaech 保持本库既定“夺魂魔”（mod-tome.lua:9037、39138）。
与 surface 同向：raiding party 缺失。reviewer 对 Yaech 译名证据不足的保留由宿主核实：本库 mod-tome.lua:9037（Yaeches 条目）与 39138（Murgol, the Yaech Lord）均译“夺魂魔”，保持。并入同条修复。
