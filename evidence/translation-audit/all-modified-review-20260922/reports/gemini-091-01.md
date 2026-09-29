本批次（batch-091，条目 entry-03012 至 entry-03051，共 40 条）已完成逐条只读复核。文件哈希校验一致（SHA-256：`77cc6905a89a963292079ca6612c6749645cb3d79a65c437bd3ca08805ec310a`）。本批条目全部源自 `mod-tome` 组件，源码依据为固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下的公开源码与既有固定译文，现将逐条复核意见报告如下：

---

### entry-03012
- **原文**：`You have %d stat point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 属性点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/mark-spellblaze/objects.lua:51`。占位符 `%d` 正确保留，快捷键提示与数值参数一致，文意准确。

### entry-03013
- **原文**：`You have %d class talent point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 职业技能点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/mark-spellblaze/objects.lua:52`。占位符 `%d` 保留完整，术语“职业技能点数”（class talent point）使用规范。

### entry-03014
- **原文**：`You have %d generic talent point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 通用技能点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/mark-spellblaze/objects.lua:53`。占位符 `%d` 保留完整，术语“通用技能点数”（generic talent point）使用规范。

### entry-03015
- **原文**：`#00FF00#You gain an affinity for blight. You can now learn new Vile Life talents (press p).`
- **译文**：`#00FF00#你获得了与枯萎的紧密联系，现在你可以学习新的邪恶生命技能（按 P 键）。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/mark-spellblaze/objects.lua:66`。颜色码 `#00FF00#` 完整闭合，“Vile Life”准确对应解锁的 `corruption/vile-life` 技能系（邪恶生命）。

### entry-03016
- **原文**：`Green eyes stare out from behind strands of long, golden hair, which falls down in waves over smooth, pale skin. Your eyes are drawn to the bare flesh, but as they look further they see dark scales stretching out into a long serpent's tail. You look up as she moves, her hair parting to reveal a slim and beautiful face with high cheekbones and full lips. Yet for all the allure of this wondrous creature the terror of the serpentine tail sends shivers down your spine.`
- **译文**：`一双绿色的眼睛从缕缕金色长发后凝视着你，那长发如波浪般垂落在光洁苍白的肌肤上。你的目光被裸露的肌肤吸引，但再往下看，就会见到黑色的鳞片一路延伸，化作长长的蛇尾。她一动，发丝分开，露出一张清瘦而美丽的脸庞，颧骨高耸，双唇丰润。然而，纵使这奇异生灵如此诱人，那蛇一般的尾巴带来的恐惧仍让你脊背发凉。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/murgol-lair/npcs.lua:140`（naga nereid 描述）。外貌及神态描写准确传神，标点与分句合理，无漏译。

### entry-03017
- **原文**：`Have you heard, the old forest seems to have been claimed by a new evil!`
- **译文**：`你有听说过吗，古老森林似乎已经被一股新的邪恶势力占据了！`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/old-forest/npcs.lua:83, 137`（替代守卫者 Snaproot 激活传闻）。术语“古老森林”（old forest）准确，传闻口吻契合。

### entry-03018
- **原文**：`It looks at you with cute little eyes before jumping at you with razor sharp teeth.`
- **译文**：`它用无辜的眼神看着你，随即用剃刀般锋利的牙齿扑向你。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/old-forest/npcs.lua:144`（cute little bunny 描述）。归化处理生动自然，准确表达出杀人兔外表无害与瞬间暴起反差的语境。

### entry-03019
- **原文**：`This small orc has a malicious and greedy look in its eyes. Its veins pulse with new life and it moves with surprising speed. Though not fully developed you can still see the muscles forming on its long limbs, leading to clawed fingers and toes.`
- **译文**：`这只小兽人的眼里透露着怨恨和贪婪。它有着旺盛的活力并能以惊人的速度移动。虽然还没完全长大，但是你仍能看到他修长四肢上正在成形的肌肉，末端连着带爪的手指和脚趾。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/orc-breeding-pit/npcs.lua:62`（orc child 描述）。身体发育与肢体动作描写完整，虽后半句出现“他”的人称代词微瑕，但整体语义通畅。

### entry-03020
- **原文**：`This giant, bloated form towers above you. Mucus and slime ooze from every orifice, dripping onto the cavern floor. Orc children fight over the right to feed from her distended teats whilst small babies are regularly emerge from folds of flesh. The sight and the smell make you retch.\nHere stands a tremendous form almost the size of a dragon. Bloated skin rises in thick folds, seeping viscous slime from its wide pores. Hundreds of hanging teats feed a small army of squabbling, fighting young orcs - only the toughest of them are able to gain the precious nutrients to grow stronger, the weaker ones left to wither on the mouldy floor. At the top of this towering hulk is a shrivelled head coated in long tangled hair. Dazed eyes peer out with a mixture of sadness and pain, but as they fix on you they turn to anger, the creature's face contorted with the fierce desire to protect its young.`
- **译文**：`这个巨大臃肿的身影耸立在你面前。粘液和脓液从它身上的每个孔洞渗出，滴落在洞穴的地面上。兽人幼崽们争抢着吸奶的权利，婴儿从它的肉褶中出生，眼前的景象和气味令人作呕。\n站在你面前的是一只跟龙差不多体型的怪物。浮肿的皮肤隆起成厚厚的褶皱，粗大的毛孔渗出粘稠的液体。上百个垂挂的乳头喂养着一群争吵打斗的年轻兽人——只有最强壮的才能获得宝贵的营养变得更强，弱小的只能在发霉的地面上枯萎。在这只庞然大物的顶端是一颗枯萎的头颅，覆着一头蓬乱纠结的长发。茫然的眼神中混合着悲伤与痛苦，但当它们锁定你时，便转为愤怒，这张脸因护崽的强烈渴望而扭曲。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/orc-breeding-pit/npcs.lua:94, 126`（orc mother 与 Orc Greatmother 共用描述）。两段长文本换行对应无误，信息完整传达。

### entry-03021
- **原文**：`The rift leads... somewhere.`
- **译文**：`裂缝通向…某个地方。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/grids.lua:38`（时空裂隙地图格说明）。省略号与简短提示准确传达。

### entry-03022
- **原文**：`elemental`
- **译文**：`元素生物`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/npcs.lua:26`（Epoch 的 type 字段）。符合术语快照 `elemental -> 元素生物`（`T.GAME.ENTITY creatures entity type preferred`）。

### entry-03023
- **原文**：`Epoch`
- **译文**：`纪元`
- **复核结论**：存在疑点
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/npcs.lua:27`（悖论位面具名 Unique boss）。术语快照明确记录：`Epoch -> 亚伯契`（`T.PN.PERSON`，附注：“时空位面具名实体专名；同名天赋及神器 Epoch's Curve 均沿用音译，不按普通名词‘纪元’处理”）。且在固定 commit 的 `game/modules/tome/data/locales/zh_hans.lua:39230` 中固定为 `t("Epoch", "亚伯契", "entity name")`。当前译文译为「纪元」，偏离了术语快照 preferred 规范及固定源码既有译名。

### entry-03024
- **原文**：`A huge being composed of sparking blue and yellow energy stands before you.  It shifts and flows as it moves, at once erratic and graceful.`
- **译文**：`一个由噼啪作响的蓝黄双色能量构成的巨大存在站在你面前。它在移动时不断变形、流动，既飘忽不定又优雅。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/npcs.lua:29`。文意传达准确生动，格式无缺失。

### entry-03025
- **原文**：`Epoch's Curve`
- **译文**：`纪元之弧`
- **复核结论**：存在疑点
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/objects.lua:29`（掉落自 Epoch 的神器长弓）。依据本批术语快照，具名实体 Epoch 及其神器 Epoch's Curve 应沿用专名音译；且在固定 commit 的 `game/modules/tome/data/locales/zh_hans.lua:39236` 中固定为 `t("Epoch's Curve", "亚伯契的弧线", "entity name")`。现译「纪元之弧」与固定源码既有译名及术语快照关于专名音译的说明存在分歧。

### entry-03026
- **原文**：`white ash longbow`
- **译文**：`白蜡长弓`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/objects.lua:29`（Epoch's Curve 的未鉴定名称 `unided_name`）。材质与弓种翻译准确。

### entry-03027
- **原文**：`Epoch's Curve has served the Wardens for generations and was passed from Warden to Warden for many years before being lost.\nAccording to legend it was made from the first ash sapling to sprout after the Spellblaze and carries powers of both time and renewal.`
- **译文**：`在纪元之弧失踪前，它已经世世代代服务于守卫，在守卫之间辗转相传多年。\n根据传说，它是用魔法大爆炸后第一棵抽芽的白蜡树苗制成，拥有时空和恢复的力量。`
- **复核结论**：存在疑点
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/paradox-plane/objects.lua:30`。译文首句中神器名称写作「纪元之弧」，与 entry-03025 一同偏离了术语快照及固定 commit `game/modules/tome/data/locales/zh_hans.lua:39238` 中的既有译名「亚伯契的弧线」。换行与其余句意表达未见格式缺失。

### entry-03028
- **原文**：`This gigantic mass of flesh and stone moves slowly, the ground rumbling with each step it takes. Its body seems to constantly pulsate and reform. Massive stones at the end of each limb form massive blunt weapons.`
- **译文**：`这个由血肉与岩石构成的巨大躯体行动缓慢，每走一步都使大地为之震颤。它的身体看起来在不断地颤动和重塑。每条肢体末端的巨石构成了强大的钝器。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/rak-shor-pride/npcs.lua:107`（Rotting Titan 描述）。躯体特征与重型打击动作翻译贴切准确。

### entry-03029
- **原文**：`The ground shakes as %s steps!`
- **译文**：`当 %s前进时，大地在震动！`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/rak-shor-pride/npcs.lua:136`（腐烂泰坦移动时的震地提示）。占位符 `%s` 完整保留，日志动作表达通顺。

### entry-03030
- **原文**：`The robes of this ancient vampire billow with intense winds. Bolts of lightning arc along its body. In its hand it holds a bow, electricity streaking across it.`
- **译文**：`这只远古吸血鬼的长袍在强风中鼓荡翻涌。闪电在他的周身环绕。他手里握着一把长弓，电弧在这把弓上流转。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/rak-shor-pride/npcs.lua:277`（Arch Zephyr 描述）。长袍翻涌、闪电弧光与弓身雷电的描写翻译精准流畅。

### entry-03031
- **原文**：`Farportal: the Far East`
- **译文**：`远行传送门：至远东大陆`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/reknor/grids.lua:26, 49`。传送门类型及目的地专名翻译规范准确。

### entry-03032
- **原文**：`A huge and muscular orc of unknown breed. He looks both menacing and cunning...`
- **译文**：`一只种类不明、肌肉发达的巨大兽人。他看起来既危险又狡猾……`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/reknor/npcs.lua:33`（Golbug the Destroyer 描述）。省略号及体态、神态特征翻译准确。

### entry-03033
- **原文**：`When last you saw it, this cavern was littered with the corpses of orcs that you had slain. Now many, many more corpses carpet the floor, all charred and reeking of sulfur. An orange glow dimly illuminates the far reaches of the cavern to the east.`
- **译文**：`你上次过来时，这个洞穴里满是你杀死的兽人尸体。现在，更多的尸体铺在了地上，尽皆焦黑，散发着刺鼻的硫磺味。桔色的昏暗灯光照亮了洞穴延伸的东面。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/reknor/npcs.lua:83`（击败高尔布格后返回瑞库纳的弹窗警告）。环境描述层次清晰，色彩与气味词汇对齐准确。

### entry-03034
- **原文**：`Back and there again`
- **译文**：`归而复往`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/reknor/npcs.lua:167`（弹窗标题）。符合术语快照：`Back and there again -> 归而复往`（`T.NARRATIVE.ACHIEVEMENT / T.NARRATIVE.LORE preferred core`），与《霍比特人》原典“There and back again”（去而复归）形成倒装呼应。

### entry-03035
- **原文**：`A huge orc blocks your way to the Iron Council. You must pass.`
- **译文**：`一只阻挡了通向钢铁议会道路的巨大兽人。你必须通过。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/reknor-escape/npcs.lua:37`（Brotoq the Reaver 描述）。专名“钢铁议会”（Iron Council，矮人统治机构）准确，剧情压迫感准确传达。

### entry-03036
- **原文**：`A letter.`
- **译文**：`一封信。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/rhaloren-camp/objects.lua:30, 38`（BASE_LORE 信件描述）。简短原文对应准确。

### entry-03037
- **原文**：`This small humanoid is covered in silky white fur. Its bulging eyes stare deep into your mind.`
- **译文**：`这只矮小的人形生物全身覆盖着丝般顺滑的白色毛发。它凸出的眼睛直视你的内心深处。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ring-of-blood/npcs.lua:30`（Blood Master 描述）。外表及心灵穿透感描写准确。

### entry-03038
- **原文**：`You heal for 2.5%% of the damage you deal.\nHealing during current combat:  #GREEN#%0.2f#LAST#`
- **译文**：`你造成的所有伤害将会回复你相当于伤害值2.5%%的生命值。\n在本次战斗中的回复量：#GREEN#%0.2f#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ring-of-blood/objects.lua:29`（神器 Bloodcaller 的 `special_desc`）。转义百分号 `2.5%%`、浮点格式 `%0.2f`、颜色码 `#GREEN#...#LAST#` 及换行符 `\n` 全部完备无缺失，吸血机制数值表述准确。

### entry-03039
- **原文**：`ritch flamespitter`
- **译文**：`喷火里奇`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ritch-tunnels/npcs.lua:51`。实体子类型 ritch 规范对应“里奇”，前缀 flamespitter 译为“喷火”，完全一致。

### entry-03040
- **原文**：`The orb looks inactive.`
- **译文**：`水晶球看起来对你不起反应。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ruined-dungeon/grids.lua:79`。同 section 内（`ruined-dungeon/grids.lua`）所有的 `orb` 实体与弹窗标题均统一译为“水晶球”（如 `Strange Orb -> 奇特的水晶球`），此处译文与同段上下文术语一致；虽译文有归化语气（“对你不起反应”），但无机制冲突。

### entry-03041
- **原文**：`and left to rot`
- **译文**：`并任其腐烂`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ruins-kor-pul/npcs.lua:42`（The Shade 的 `killer_message`）。属于击杀提示拼接短语（`... was slain by The Shade and left to rot`），译文“并任其腐烂”在语法与语义衔接上准确自然。

### entry-03042
- **原文**：`A journal page, left by an adventurer.`
- **译文**：`由冒险家留下的日记书页。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/ruins-kor-pul/objects.lua:29`（BASE_LORE 描述）。结构定语表达准确。

### entry-03043
- **原文**：`This sandworm seems to not care about your presence at all and simply continues digging its way through the sand.\n\t\nMaybe following it is the only way to move around here...`
- **译文**：`这只沙虫似乎毫不在意你的出现，只顾埋头挖掘。\n\t\n也许跟着它才是在这一带四处走动的唯一办法……`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/npcs.lua:36, 59`。空行、制表符缩进及沙虫挖掘机制提示均完备保留。

### entry-03044
- **原文**：`Before you stands the queen of the sandworms. Massive and bloated, she slithers toward you, calling for her offspring!`
- **译文**：`在你面前站着的是沙虫女皇。她庞大而臃肿，蜿蜒蠕行着向你逼近，同时还在召唤自己的子孙！`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/npcs.lua:77`（Sandworm Queen 描述）。形态与召唤子代动态描写准确生动。

### entry-03045
- **原文**：`The sandworms are gone, devoured by this shrieking, warped horror.`
- **译文**：`沙虫们已经死了，它们被这只尖啸而扭曲的恐怖所吞噬。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/npcs.lua:142`（Corrupted Sand Wyrm 描述）。语意传达清晰完整。细微观察：句中“horror”此处作为同位语修饰巨龙实体，译作“恐怖”略带抽象化色彩，但不影响对剧情与画面的理解。

### entry-03046
- **原文**：`Some people get the weirdest ideas!`
- **译文**：`有些人有最奇怪的想法！`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:29`（Song of the Sands 描述）。口语化反讽语气贴切。

### entry-03047
- **原文**：`#00FFFF#You consume the heart and feel the knowledge of this very old creature fill you!`
- **译文**：`#00FFFF#你吃下了心脏，你感觉被这个古老生物的知识充满！`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:46`。颜色标记 `#00FFFF#` 完整，食用女皇之心的日志提示准确。

### entry-03048
- **原文**：`You have %d stat point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 属性点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:50`。占位符 `%d` 保留，与 entry-03012 格式及文本保持统一。

### entry-03049
- **原文**：`You have %d class talent point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 职业技能点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:51`。占位符 `%d` 保留，与 entry-03013 格式及文本保持统一。

### entry-03050
- **原文**：`You have %d generic talent point(s) to spend. Press p to use them.`
- **译文**：`你有 %d 通用技能点数，按 P 键使用。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:52`。占位符 `%d` 保留，与 entry-03014 格式及文本保持统一。

### entry-03051
- **原文**：`#00FF00#You gain an affinity for nature. You can now learn new Harmony talents (press p).`
- **译文**：`#00FF00#你获得了与自然的紧密联系，现在你可以学习新的元素和谐技能（按 P 键）。`
- **复核结论**：未发现问题
- **可核验依据**：对应固定源码 `game/modules/tome/data/zones/sandworm-lair/objects.lua:65`。颜色标记 `#00FF00#` 完整闭合，“Harmony”准确对应游戏中的 `wild-gift/harmony`（元素和谐）技能系。

---

### 复核总结
- **全部覆核条目数**：40 条（entry-03012 至 entry-03051）
- **未发现问题**：37 条
- **存在疑点**：3 条（entry-03023、entry-03025、entry-03027，均涉及具名实体及神器 `Epoch / Epoch's Curve` 在专名音译「亚伯契」与普通名词意译「纪元」之间的规范偏离与源码冲突）
