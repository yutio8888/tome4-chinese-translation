本批次（batch-019）只读译文复核工作已完成。

在开始前，已完成输入文件校验：
- 文件路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-019.md`
- SHA-256 校验值：`ee7ac1225c86ac788bad88d074c0fc8920a7b2549a44fa8910afeab1408c6dc2`（核验一致）
- 公开源码基准：`t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均来自 `mod-tome`）
- 译文上下文基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

# batch-019 逐条复核报告（entry-00721 至 entry-00760）

### entry-00721
- **位置/Section**：`mod-tome.lua:8181` / `mod-tome/data/general/npcs/ghost.lua`
- **原文**：`It is a form that screams its presence against the eye. Death incarnate, its hideous black body seems to struggle against reality as the universe itself strives to banish it.`
- **译文**：`它的可怕形象冲击着你的双眼。它是死亡的化身，它那丑恶的黑色躯体似乎正与现实相抗争，而宇宙本身竭力要将它放逐。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `dread`（ghost.lua:46）。译文将 "screams its presence against the eye" 译为“可怕形象冲击着你的双眼”，准确传达视觉震撼感；后半句结构严谨，无占位符或控制字符，语义完整流畅。

---

### entry-00722
- **位置/Section**：`mod-tome.lua:8183` / `mod-tome/data/general/npcs/ghost.lua`
- **原文**：`It is an unlife of power almost unequaled. An affront to existence, its very touch abuses and disrupts the flow of life, and its unearthly limbs, of purest black, crumble rock and wither flesh with ease.`
- **译文**：`它是一种几乎无可匹敌的非生命力量。它是对存在本身的冒犯，它的触碰本身便会侵害并扰乱生命的流动，它那纯粹的不可思议的黑色肢体能够轻松地使岩石崩解，血肉成灰。`
- **复核结论**：存在疑点
- **核验依据**：对应 NPC `dreadmaster`（ghost.lua:67）。
  1. 首句主干为 "It is an unlife [of power almost unequaled]"，中心词 "unlife" 指代该不死实体自身（具有几乎无可匹敌力量的不死存在），译文译作“它是一种几乎无可匹敌的非生命力量”，将实体名词与修饰属性混淆成了抽象概念“力量”。
  2. "unearthly limbs, of purest black" 中，插入语 "of purest black" 修饰 limbs 的色泽（纯黑肢体），译文作“纯粹的不可思议的黑色肢体”，修饰语层级混乱（将 purest 挪去修饰 unearthly）。

---

### entry-00723
- **位置/Section**：`mod-tome.lua:8187` / `mod-tome/data/general/npcs/ghost.lua`
- **原文**：`A vengeful, screaming soul given form with the breath of Urh'Rok himself. The vapors of the Fearscape seep from its dimension-bending form, withering and searing.`
- **译文**：`乌鲁洛克的吐息中诞生，不断嚎叫的复仇之魂。恶魔空间的气息不断从她次元扭曲的身体中渗出，不断灼烧和腐蚀着周围的一切。`
- **复核结论**：细微观察
- **核验依据**：对应 NPC `ruin banshee`（ghost.lua:119）。末尾状语 "withering and searing"（枯萎与灼烧）被意译为“不断灼烧和腐蚀着周围的一切”，其中 "withering" 意译为“腐蚀”且增译了“周围的一切”；整句中出现了三次“不断”（不断嚎叫……不断从……不断灼烧），行文略有重复。

---

### entry-00724
- **位置/Section**：`mod-tome.lua:8206` / `mod-tome/data/general/npcs/gwelgoroth.lua`
- **原文**：`elemental`
- **译文**：`元素生物`
- **复核结论**：未发现问题
- **核验依据**：对应 `BASE_NPC_GWELGOROTH` 的 `type = "elemental"`（gwelgoroth.lua:26）。完全符合术语规则 `elemental` 在 `entity type` 下统一为“元素生物”的规定。

---

### entry-00725
- **位置/Section**：`mod-tome.lua:8239` / `mod-tome/data/general/npcs/horror-undead.lua`
- **原文**：`This monstrous form of putrid, torn flesh and chipped bone drags its mass towards you, spurting blood and viscera along the way.`
- **译文**：`这团腐烂的碎肉残骨拖着庞大的躯体向你蠕动，沿途喷溅出血液和内脏。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `necrotic abomination`（horror-undead.lua:58）。"drags its mass towards you" 贴切译出拖曳庞大身躯蠕动之感，"putrid, torn flesh and chipped bone" 对仗准确，无占位符。

---

### entry-00726
- **位置/Section**：`mod-tome.lua:8245` / `mod-tome/data/general/npcs/horror-undead.lua`
- **原文**：`This pulsing, quivering form is a deep crimson, and appears to be composed entirely of thick, virulent blood. Waves rhythmically ripple across its surface, indicating a still beating heart somewhere in its body.`
- **译文**：`这个不断跳动不断颤抖的物体是深红色的，似乎完全由浓厚致命的血液组成。在其表面仍有富有节奏的波纹，也许在其身上的某个地方仍有心脏跳动。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `sanguine horror`（horror-undead.lua:140）。虽将 "indicating..."（表明/预示）稍弱化为“也许……”，且将 "form" 译为“物体”（生物语境下“形体/躯体”更佳），但整体意思完整，无事实与机制冲突。

---

### entry-00727
- **位置/Section**：`mod-tome.lua:8256` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：
```text
A bulging rotten robe seems to tear at the seams, with masses of bloated worms spilling out all around the moving form.  Two arm-like appendages, each made up of overlapping mucous-drenched maggots, grasp tightly around the handles of bile-coated waraxes.
Each swing drips pustulant fluid before it, and each droplet writhes and wriggles in the air before splashing against the ground.
```
- **译文**：
```text
一件鼓鼓囊囊的腐烂长袍似乎要从接缝处裂开，成团浮肿的蠕虫从这移动的躯体四周向外涌出。两只臂膀一样的附属物，每只都由沾满黏液的蛆重叠而成，各握着一柄覆有胆汁的战斧。
每一次挥舞都会向前溅出脓液，每一滴脓液在空中扭动翻滚，然后啪嗒一声落在地上。
```
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `worm that walks`（horror.lua:47）。换行格式与原文完全一致；maggots（蛆/蛆虫）与 bile-coated waraxes 对应精准，描写极具画面感。

---

### entry-00728
- **位置/Section**：`mod-tome.lua:8258` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`#LIGHT_RED#A carrion worm mass has spawned from %s' wounds!`
- **译文**：`#LIGHT_RED#一团腐肉虫从%s的伤口孵化了出来！`
- **复核结论**：存在疑点
- **核验依据**：对应 `horror.lua:109` 机制代码（受到单次高伤时调用 `t.spawn_carrion_worm` 产生召唤生物）。
  术语快照中明确规范：`carrion worm mass` -> `腐肉虫群`（`T.GAME.ENTITY`, `creatures`, `entity name`），并注明“统一实体名、生成日志及腐肉虫疾病描述”。此处生成日志将该专有实体名称意译为“一团腐肉虫”，未能遵循术语库统一为“腐肉虫群”的要求。

---

### entry-00729
- **位置/Section**：`mod-tome.lua:8262` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`A shifting form of darkest night that seems to reflect your deepest fears.`
- **译文**：`一团由最深沉的黑夜凝聚而成、不断变幻的形体，似乎映照出你内心深处的恐惧。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `nightmare horror`（horror.lua:145）。"shifting form" 译为“不断变幻的形体”，文笔流畅，意境契合。

---

### entry-00730
- **位置/Section**：`mod-tome.lua:8265` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`#AQUAMARINE#As %s falls all its eyes fall to the ground!`
- **译文**：`#AQUAMARINE#当%s倒下时它的眼睛掉落在了地上！`
- **复核结论**：存在疑点
- **核验依据**：对应 `horror.lua:257`（无头恐魔死亡触发全部眼球守卫死亡的日志）。
  1. 漏译限定词 "all"：机制上是杀死本体时其伴生的全部眼睛随从同时死亡落地，译文漏掉了 "all"（“它的所有/全部眼睛”），削弱了机制全灭特征。
  2. 标点缺陷：“当%s倒下时”之后缺乏停顿逗号。

---

### entry-00731
- **位置/Section**：`mod-tome.lua:8266` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`eldritch eye`
- **译文**：`骇异之眼`
- **复核结论**：存在疑点
- **核验依据**：对应实体 `BASE_NPC_ELDRICTH_EYE`（horror.lua:263，无头恐魔随从小眼）。
  术语库快照中针对 `eldritch`（creatures/entity subtype）的备注明确规定：“专名（Eldritch eye 艾尔德里奇之眼、Eldritch Channeler 埃尔德里奇主宰者）保留音译”。译文在此处采用了意译“骇异之眼”，与术语库备注要求保留音译“艾尔德里奇之眼”存在冲突。

---

### entry-00732
- **位置/Section**：`mod-tome.lua:8296` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`This powerful vortex of ice and lightning somehow gives you the impression of claws, teeth and intense hunger...`
- **译文**：`这个由冰和闪电组成的强大漩涡不知为何给你一种利爪、尖牙和强烈饥饿的印象……`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `maelstrom`（horror.lua:831）。词意对应精准，省略号转换为中文全角省略号，标点规范。

---

### entry-00733
- **位置/Section**：`mod-tome.lua:8298` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`You don't want to think about what sort of creature this lamprey-like horror was feeding on to grow so large.  Its skin pulsates and writhes, like things are moving underneath...`
- **译文**：`你不想知道这个像七鳃鳗一样的恐魔是吃什么才能长这么大的。它的皮肤不停的扭动，就像有东西在下面移动一样……`
- **复核结论**：存在疑点
- **核验依据**：对应 NPC `parasitic horror`（horror.lua:880）。
  1. 原文 "Its skin pulsates and writhes" 包含两个动作 "pulsates"（跳动/脉动）与 "writhes"（蠕动/扭动）。译文仅译出“不停的扭动”，漏译了 "pulsates"。
  2. 助词使用不规范：“不停的扭动”作状语，规范用法宜为“不停地扭动”。

---

### entry-00734
- **位置/Section**：`mod-tome.lua:8308` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`#AQUAMARINE#As #Source# falls you notice that #Target# seems to shudder in pain!`
- **译文**：`#AQUAMARINE#当#Source#倒下时，你发现#Target#似乎因为痛苦而颤抖！`
- **复核结论**：未发现问题
- **核验依据**：对应 `horror.lua:1053` 召唤物死亡反馈机制。颜色代码 `#AQUAMARINE#` 与战斗占位符 `#Source#`、`#Target#` 准确无误，逗号停顿自然。

---

### entry-00735
- **位置/Section**：`mod-tome.lua:8313` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`Animated Sword`
- **译文**：`活化之剑`
- **复核结论**：未发现问题
- **核验依据**：对应实体 `ANIMATED_BLADE` 的 `name`（horror.lua:1136）。译名准确符合通用奇幻与 ToME4 习惯。

---

### entry-00736
- **位置/Section**：`mod-tome.lua:8315` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`#AQUAMARINE#A rift opens and a free floating blade emerges!`
- **译文**：`#AQUAMARINE#时空裂缝打开了，里面出现了一把浮空的刀刃！`
- **复核结论**：未发现问题
- **核验依据**：对应 `horror.lua:1155`（ANIMATED_BLADE 登场生成时间监禁的日志）。颜色代码完整，结合该怪物的时空系（Temporal/Rift）属性，“时空裂缝”意译契合语境。

---

### entry-00737
- **位置/Section**：`mod-tome.lua:8317` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`Distorted Animated Sword`
- **译文**：`扭曲活化之剑`
- **复核结论**：未发现问题
- **核验依据**：对应实体 `DISTORTED_BLADE` 的 `name`（horror.lua:1195）。与 entry-00735 保持前后一致，准确无误。

---

### entry-00738
- **位置/Section**：`mod-tome.lua:8319` / `mod-tome/data/general/npcs/horror.lua`
- **原文**：`#AQUAMARINE#A rift opens and a free floating blade emerges! It looks unstable...`
- **译文**：`#AQUAMARINE#时空裂缝打开了，里面出现了一把浮空的刀刃！它看起来很不稳定…`
- **复核结论**：未发现问题
- **核验依据**：对应 `horror.lua:1229`。颜色代码正确保留，末尾省略号为单三点省略号，表意与语气忠实于原文。

---

### entry-00739
- **位置/Section**：`mod-tome.lua:8326` / `mod-tome/data/general/npcs/horror_aquatic.lua`
- **原文**：`#LIGHT_BLUE#%s explodes into a huge bubble of air!`
- **译文**：`#LIGHT_BLUE#%s爆炸，成为了一个巨大的气泡！`
- **复核结论**：未发现问题
- **核验依据**：对应 `horror_aquatic.lua:51`（水生恐魔死亡生成水下氧气泡网格 WATER_FLOOR_BUBBLE 的机制日志）。占位符 `%s` 与颜色标记 `#LIGHT_BLUE#` 保留完整，气泡表意契合机制。

---

### entry-00740
- **位置/Section**：`mod-tome.lua:8402` / `mod-tome/data/general/npcs/lich.lua`
- **原文**：`Having thought to discover life eternal, these beings have allowed undeath to rob them of the joys of life. Now they seek to destroy it as well.`
- **译文**：`这些存在本以为能求得永生，却让不死之身夺走了生之乐趣。现在，他们同样在毁灭生者。`
- **复核结论**：存在疑点
- **核验依据**：对应 NPC `lich`（lich.lua:60）。
  1. 代词指代错误：末句 "Now they seek to destroy it as well" 中，单数代词 "it" 承接前文的 "life"（生命）或 "the joys of life"（生之乐趣）。译文译为“生者”（living beings / the living，复数概念），指代产生偏移。
  2. 动词语气偏移："seek to destroy" 是“企图/试图/妄图毁灭”，译文作“在毁灭”，将企图意愿改写成了正在进行的既成动作。

---

### entry-00741
- **位置/Section**：`mod-tome.lua:8406` / `mod-tome/data/general/npcs/lich.lua`
- **原文**：`Blacker than the deepest night, this cold cruel form of darkness approaches.  Long ago it laid aside its mortality, but it has not forgotten its power; rather, its malice and hate have bent this undead entity on the destruction of all things living.`
- **译文**：`比最深沉的暗夜还要漆黑，这个冰冷残忍的黑暗形体正在逼近。很久以前它抛弃了自己的凡躯，但并未忘却自身的力量；恰恰相反，它的恶意与仇恨驱使这个不死存在一心毁灭所有活物。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `archlich`（lich.lua:125）。"laid aside its mortality"（抛弃了自己的凡躯）与 "bent ... on ..."（驱使……一心……）译法典雅准确，行文极具张力。

---

### entry-00742
- **位置/Section**：`mod-tome.lua:8408` / `mod-tome/data/general/npcs/lich.lua`
- **原文**：`The seething, pumping, disembodied blood of a horrendously powerful necromancer. To strike it is to bathe in the rivers of the Fearscape itself.`
- **译文**：`来自一位极其强大的死灵法师的沸腾、搏动、脱离躯体的血液。攻击它就等于在恶魔空间本身的河流中沐浴。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `blood lich`（lich.lua:164）。`necromancer`（死灵法师）与 `Fearscape`（恶魔空间）均完全契合术语库规范。

---

### entry-00743
- **位置/Section**：`mod-tome.lua:8413` / `mod-tome/data/general/npcs/losgoroth.lua`
- **原文**：`elemental`
- **译文**：`元素生物`
- **复核结论**：未发现问题
- **核验依据**：对应 `BASE_NPC_LOSGOROTH` 的 `type = "elemental"`（losgoroth.lua:26）。符合 `elemental` 作为 `entity type` 译为“元素生物”的统一定义。

---

### entry-00744
- **位置/Section**：`mod-tome.lua:8415` / `mod-tome/data/general/npcs/losgoroth.lua`
- **原文**：`Losgoroth are mighty void elementals, native to the void between the stars. They are rarely seen on a planet's surface.`
- **译文**：`洛斯格罗斯是强大的虚空元素生物，原生于群星之间的虚空。在星球表面几乎看不到这种生物。`
- **复核结论**：未发现问题
- **核验依据**：对应 `BASE_NPC_LOSGOROTH`（losgoroth.lua:30）。`void elementals` 准确译为“虚空元素生物”，全句通顺传神。

---

### entry-00745
- **位置/Section**：`mod-tome.lua:8417` / `mod-tome/data/general/npcs/losgoroth.lua`
- **原文**：`manaworm`
- **译文**：`法力蠕虫`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `manaworm`（losgoroth.lua:73）。名称准确无误。

---

### entry-00746
- **位置/Section**：`mod-tome.lua:8418` / `mod-tome/data/general/npcs/losgoroth.lua`
- **原文**：`Manaworms are losgoroth which feed on the mana of arcane users. If they ever come in contact with a spellcaster, they latch on and start draining mana away.`
- **译文**：`法力蠕虫是以施法者的魔力为食的虚空生物。如果它们近距离接触到法师，它们会缠上去并吸干对方的魔力。`
- **复核结论**：存在疑点
- **核验依据**：对应 NPC `manaworm`（losgoroth.lua:73）与伤害类型机制（`damage_types.lua:3324`，判定 `target.T_MANA_POOL` 并赋予 `EFF_MANAWORM` 状态，每回合抽取法力值）。
  1. 术语偏离：术语表统一规定 `Mana` 为“法力值”（`T.GAME.RESOURCE`），此处两处 "mana" 均被译成了“魔力”。
  2. 专名未统一：前句中的 "losgoroth" 未采用 entry-00744 确立的音译“洛斯格罗斯”，而是被泛化翻译为“虚空生物”。

---

### entry-00747
- **位置/Section**：`mod-tome.lua:8428` / `mod-tome/data/general/npcs/major-demon.lua`
- **原文**：`Under a shroud of darkness you discern an evil shape.`
- **译文**：`在一片黑暗的笼罩下，依稀可见一道邪恶的身影。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `dúathedlen`（major-demon.lua:76）。译文准确生动。

---

### entry-00748
- **位置/Section**：`mod-tome.lua:8440` / `mod-tome/data/general/npcs/major-demon.lua`
- **原文**：`A burning giant wielding a forge hammer of the underworld in each hand -- weapons imbued by Urh'Rok himself with the power to crush and shape felsteel. Enter their range at your peril.`
- **译文**：`一个浑身燃烧的巨人，双手各持一柄来自地底的锻造巨锤——由乌鲁洛克亲自赋予碾碎和锻造魔钢之力的武器。踏入它们的攻击范围，后果自负。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `forge-giant`（major-demon.lua:250）。破折号转换规范，`felsteel`（魔钢）与 `Urh'Rok`（乌鲁洛克）处理恰当。

---

### entry-00749
- **位置/Section**：`mod-tome.lua:8454` / `mod-tome/data/general/npcs/minor-demon.lua`
- **原文**：
```text
A gaunt vaguely humanoid shape featuring unadorned grey leathery skin. Its arms and legs seem somehow too long and it stands tall, projecting an ominous shadow even in darkness.
Its glowing red eyes shine with both cruelty and a deep frightening intellect.
```
- **译文**：
```text
一个憔悴、隐约近似人类的身影，全身是未经修饰的灰色皮革质地的皮肤。它的胳膊和腿不知为何过于修长。当它耸立在那里的时候，即使在黑暗中也会投下不祥的阴影。
它发光的红色眼睛闪烁着，目光里蕴含着既残酷又深邃可怕的智慧。
```
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `onilug`（minor-demon.lua:93）。段落对应无误，形容词及状语层次翻译细腻。

---

### entry-00750
- **位置/Section**：`mod-tome.lua:8483` / `mod-tome/data/general/npcs/molds.lua`
- **原文**：`A strange sickly green growth on the dungeon floor.`
- **译文**：`地牢地面上一片古怪的病态绿色菌丛。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `green mold`（molds.lua:79）。针对真菌类实体，将 "growth" 译为“菌丛”极为贴切。

---

### entry-00751
- **位置/Section**：`mod-tome.lua:8501` / `mod-tome/data/general/npcs/multihued-drake.lua`
- **原文**：`#YELLOW#%s's skin turns %s!`
- **译文**：`#YELLOW#%s的皮肤变成了 %s！`
- **复核结论**：未发现问题
- **核验依据**：对应 `multihued-drake.lua:216`，多相巨龙变色机制代码。两处占位符 `%s`（龙名称与颜色字符串）参数顺序正确，颜色代码保留完整，空格用于英文颜色插入时的混排隔离，未发现问题。

---

### entry-00752
- **位置/Section**：`mod-tome.lua:8515` / `mod-tome/data/general/npcs/naga.lua`
- **原文**：`Before you stands a tall figure -- a very tall figure, propped high by a thick serpent's tail in place of where his legs should rightly be. His torso is human-like, with bulging muscles beneath fitted armour, and large hands gripping a fiercely sharp trident. He glares at you with dark intensity, like a wolf about to pounce on unsuspecting prey.`
- **译文**：`在你面前站着一个高大的人影——一个非常高的人形怪物，在腿部长着巨大的蛇尾巴，他以此来支撑他的身体。他的上半身是人形，护甲下面隐约可见发达的肌肉，两只巨大的双手紧握着锋利的三叉戟。他带着阴沉的锐利目光盯着你，像一头随时准备扑向毫无防备猎物的狼。`
- **复核结论**：存在疑点
- **核验依据**：对应 NPC `naga myrmidon`（naga.lua:54）。
  1. 严重语病/量词冲突：“两只巨大的双手紧握着锋利的三叉戟”。“双手”在汉语中已代表一对（两只手），“两只巨大的双手”字面等同于四只手。该 NPC 仅为正常双臂娜迦（装备槽 `MAINHAND` 持三叉戟），规范表述应为“两只巨大的手”或“巨大的双手”。
  2. 身体构造描述失真："in place of where his legs should rightly be" 说明是用蛇尾取代了原本应长腿的位置；译文译作“在腿部长着巨大的蛇尾巴”，字面产生“蛇尾长在腿上”的错误图像。

---

### entry-00753
- **位置/Section**：`mod-tome.lua:8527` / `mod-tome/data/general/npcs/ogre.lua`
- **原文**：`A maul-wield ogre. Ready to CRUSH!`
- **译文**：`一个手里拿着重锤的食人魔，随时准备将你一锤击碎！`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `ogre guard`（ogre.lua:47）。食人魔风格传达生动，感叹号保留。

---

### entry-00754
- **位置/Section**：`mod-tome.lua:8597` / `mod-tome/data/general/npcs/orc-rak-shor.lua`
- **原文**：`An orc dressed in black robes. He mumbles in a harsh tongue.`
- **译文**：`一只身穿黑色长袍的兽人。它用刺耳的语言喃喃自语。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `orc necromancer`（orc-rak-shor.lua:45）。表意完整，句读清晰。

---

### entry-00755
- **位置/Section**：`mod-tome.lua:8599` / `mod-tome/data/general/npcs/orc-rak-shor.lua`
- **原文**：`An orc dressed in blood-stained robes. He mumbles in a harsh tongue.`
- **译文**：`一只穿着鲜血斑斑长袍的兽人。它用刺耳的语言喃喃自语。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `orc blood mage`（orc-rak-shor.lua:103）。与前条句式对仗统一，形容词对应准确。

---

### entry-00756
- **位置/Section**：`mod-tome.lua:8609` / `mod-tome/data/general/npcs/orc-vor.lua`
- **原文**：`An orc dressed in bright red robes. He mumbles in a harsh tongue.`
- **译文**：`一只身穿亮红色长袍的兽人。它用刺耳的语言喃喃自语。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `orc pyromancer`（orc-vor.lua:46）。用词准确，前后统一。

---

### entry-00757
- **位置/Section**：`mod-tome.lua:8612` / `mod-tome/data/general/npcs/orc-vor.lua`
- **原文**：`An orc dressed in cold blue robes. He mumbles in a harsh tongue.`
- **译文**：`一只身穿冰蓝色长袍的兽人。它用刺耳的语言喃喃自语。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `orc cryomancer`（orc-vor.lua:82）。"cold blue" 结合冰法师语境译为“冰蓝色”，贴切自然。

---

### entry-00758
- **位置/Section**：`mod-tome.lua:8621` / `mod-tome/data/general/npcs/orc.lua`
- **原文**：`He is a hardy, well-weathered survivor.`
- **译文**：`它是一个强健坚韧、饱经风霜的幸存者。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `orc warrior` / `orc archer`（orc.lua:52, 73）。成语“饱经风霜”翻译精准传神。

---

### entry-00759
- **位置/Section**：`mod-tome.lua:8647` / `mod-tome/data/general/npcs/plant.lua`
- **原文**：`honey tree`
- **译文**：`蜂蜜树`
- **复核结论**：未发现问题
- **核验依据**：对应实体 `honey tree`（plant.lua:91，会召唤蜂群的植物实体）。名称准确无误。

---

### entry-00760
- **位置/Section**：`mod-tome.lua:8674` / `mod-tome/data/general/npcs/rodent.lua`
- **原文**：`Instead of fur, this rat has crystals growing on its back, which provide extra protection.`
- **译文**：`这只耗子背上长的不是毛发而是晶体，它因此获得了额外的保护。`
- **复核结论**：未发现问题
- **核验依据**：对应 NPC `giant crystal rat`（rodent.lua:107）。在同 section 中，`rat` 实体名均统一译为“耗子”（如“巨大水晶耗子”、“巨大灰耗子”），以区别于 `mouse`（“鼠”），描述文本中称其为“耗子”保持了同组一致性；其 `combat_armor = 4, combat_def = 2` 的机制数值与“额外保护”完全契合。

---

### 汇总统计
- 复核总数：40 条（entry-00721 至 entry-00760）
- 未发现问题：33 条
- 存在疑点：6 条（entry-00722、entry-00728、entry-00730、entry-00731、entry-00740、entry-00752）
- 细微观察：1 条（entry-00723）