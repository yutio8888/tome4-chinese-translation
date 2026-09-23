## 40条译文复核结果概览

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03653 | 未发现问题 | 语义完整，格式与术语一致 |
| entry-03654 | 未发现问题 | 数值占位符匹配，机制效果描述准确 |
| entry-03655 | 仅建议 | C01：标点半角与逗号前空格排版微调建议 |
| entry-03656 | 未发现问题 | 实体占位符与标点准确 |
| entry-03657 | 未发现问题 | 机制状态描述与术语准确 |
| entry-03658 | 存在问题 | C02：主客体与视线方向误译（at the sight of 误作在视线中） |
| entry-03659 | 未发现问题 | 地块描述准确，省略号保留 |
| entry-03660 | 未发现问题 | 实体说明与操作提示准确 |
| entry-03661 | 未发现问题 | 种族与身份术语一致 |
| entry-03662 | 未发现问题 | 种族与身份术语一致 |
| entry-03663 | 未发现问题 | 种族与身份术语一致 |
| entry-03664 | 未发现问题 | 颜色标签与格式准确 |
| entry-03665 | 未发现问题 | 剧情口语风格与语义准确 |
| entry-03666 | 未发现问题 | 颜色标签、角色名与格式占位符准确 |
| entry-03667 | 未发现问题 | 功能说明清晰准确 |
| entry-03668 | 未发现问题 | 物品描述准确 |
| entry-03669 | 未发现问题 | 颜色标签与事件描述准确 |
| entry-03670 | 未发现问题 | 颜色标签与双格式占位符准确 |
| entry-03671 | 未发现问题 | 颜色标签与文本准确 |
| entry-03672 | 未发现问题 | 颜色标签、警告语意与机制指示准确 |
| entry-03673 | 未发现问题 | 商店实体名准确，existing术语不强制改名 |
| entry-03674 | 未发现问题 | 商店实体名翻译准确 |
| entry-03675 | 未发现问题 | 商店实体名翻译准确 |
| entry-03676 | 未发现问题 | 引擎动态代词占位符@himher@保留正确 |
| entry-03677 | 未发现问题 | 种族与实体名术语准确 |
| entry-03678 | 未发现问题 | 商店实体名准确，existing术语不强制改名 |
| entry-03679 | 未发现问题 | 商店实体名翻译准确 |
| entry-03680 | 未发现问题 | 商店实体名翻译准确 |
| entry-03681 | 存在问题 | C03：骨杖响动creeking漏译，句中重复“手中的…在你的手上” |
| entry-03682 | 未发现问题 | 对话选项简短准确 |
| entry-03683 | 存在问题 | C04：成语词组pathetic excuse of a necromancer严重误译为用蹩脚借口 |
| entry-03684 | 未发现问题 | 剧情长文本、人名标签、格式加粗及机制提示准确无误 |
| entry-03685 | 存在问题 | C05：Maj'Eyal违反preferred术语；C06：改造误译附加作用；C07：你这样克罗格语病错字；C08：卡普尔地名规范建议 |
| entry-03686 | 仅建议 | C09：冒号半角及空格排版微调建议 |
| entry-03687 | 未发现问题 | 解锁背景与种族特性、标签均准确 |
| entry-03688 | 未发现问题 | 种族解锁标题与颜色标签准确 |
| entry-03689 | 存在问题 | C10：Zigur误译伊格兰斯违反preferred术语；C11：句号漏标；C12：反魔种族抗性误加“魔法” |
| entry-03690 | 未发现问题 | 技能系解锁标题与颜色标签准确 |
| entry-03691 | 存在问题 | C13：corrupted beyond hope误译为被绝望所腐化；C14：第3句末尾句号遗漏 |
| entry-03692 | 未发现问题 | 资源机制说明、chaotic%与疯狂值表述准确 |

---

## 详细观察与 Claim 记录

### C01 | entry-03655 | 仅建议
- **原文短引**：`The target is starting to get mad (%d stacks), reducing mind damage resistance by %d%%, mental save by %d, confusion resistance by %d%%, generating %0.1f insanity per turn.`
- **译文短引**：`目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，%d%% 混乱免疫，每回合获得 %0.1f 疯狂值。`
- **问题说明**：译文中逗号格式不一，前两处使用了半角逗号加空格 `(%d 层), `，且第二处逗号前带有异常空格 `精神伤害抗性 , `，后半句则使用了全角中文逗号 `，`。
- **状态**：仅建议。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/data/timed_effects.lua:2124`（`ILLUSORY_CASTLE_MADNESS`）。5个格式化参数及类型（`eff.stacks`、`eff.stacks * 6`、`eff.stacks * 5`、`eff.stacks * 4`、`eff.stacks * 0.5`）全部正确消费，机制数值表达准确；标点与空格微调纯属中文排版美化偏好，不影响运行时文本解析与信息传达。

---

### C02 | entry-03658 | 存在问题
- **原文短引**：`#Target# is bolstered at the sight of the horror!`
- **译文短引**：`#Target#在恐魔的视线中被强化了！`
- **问题说明**：英文介词短语 `at the sight of [something]` 为常见习语，含义为“当看见/目睹某物时”（perceiving/seeing the object）。译文将其误译为“在恐魔的视线中”（in the horror's field of view/sight），主客体视线感知关系完全倒错，将目标目睹恐魔触发强化误写成了目标处于恐魔的视野内。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/data/timed_effects.lua:2330`（`HORRIFIC_FORTRESS`，`on_gain` 回调）。该状态长描述为 `All damages except physical reduced by %d as long as %s is alive.`，效果来源 `eff.src` 为恐魔友军，`Target`（`self`）只要与恐魔同处一室目睹恐魔存活即获得减伤强化；context.lua 同文件第12行类似句式 `Empowered by the sight of black blood` 均正译为“目睹黑血时受到强化”。译文颠倒视线方向属于客观语义错误。

---

### C03 | entry-03681 | 存在问题
- **原文短引**：`You feel the bones of the staff creeking and vibrating in your hand.`
- **译文短引**：`你感受到手中的骨杖在你的手上颤动：`
- **问题说明**：
  1. 原文动作描述为 `creeking and vibrating`（骨节挤压嘎吱作响与震颤），译文仅翻译了 `vibrating`（颤动），完全遗漏了 `creeking`（作者拼写笔误，即 creaking，骨节挤压发出的刺耳嘎吱声）这一核心声音/触觉感知信息。
  2. 译文句式出现“手中的骨杖在你的手上”重叠啰嗦语病。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/hooks/bonestaff.lua:24`（`CommandStaff:SentientOptions` 中 `data.mode == "intro"` 的对话文本）。骨杖作为具有独立意志的活物武器，骨骼摩擦作响（creeking）是其拟人化惊悚特征的关键细节，漏译导致感官描写缺失。

---

### C04 | entry-03683 | 存在问题
- **原文短引**：`Stupid useless pathetic excuse of a #{italic}#"necromancer"#{normal}#! Why refuse to use true power?!`
- **译文短引**：`像你这样的#{italic}#"死灵法师"#{normal}#竟然会用这样蹩脚的借口！为什么要拒绝使用真正的力量？！`
- **问题说明**：英文成语结构 `a pathetic excuse of a [noun]`（或 `excuse for a ...`）是固定侮辱性修辞，意为“差劲透顶/根本不配称为……的可悲货色”。骨杖在此直斥玩家角色根本不配称作死灵法师（“你这个愚蠢没用、根本不配叫‘死灵法师’的可悲废物！”）。译者望文生义，将 `excuse` 单独按名词“借口”直译，并脑补出“死灵法师竟然会用这样蹩脚的借口”，严重扭曲了骨杖对玩家身份的斥责与对话语境。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/hooks/bonestaff.lua:115`（`bone_horror_disabled` 对话节点）。玩家在上一对话中拒绝献出技能点启用骨灵恐魔，骨杖在此表现出轻蔑与愤怒，斥责玩家空有死灵法师之名却拒绝真正的力量；玩家后续回复选项亦为 `I have my reasons!`（我有我的理由！）。译文把对角色名号的贬损误读为指责玩家找借口，属于典型的成语误译与语义失实。

---

### C05 | entry-03685 | 存在问题
- **原文短引**：`While much of Maj'Eyal shuns the arcane...`
- **译文短引**：`虽然大部分马基埃亚尔人都远离奥术魔法...`
- **问题说明**：专有名词 `Maj'Eyal` 译为了 `马基埃亚尔`，违反了术语库的明确规定。
- **状态**：存在问题。
- **依据与消费逻辑**：冻结术语快照中明确收录：`Maj'Eyal | 马基·埃亚尔 | T.PN.WORLD | places | _t | preferred | core | 维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代`。此处属于必须遵循的 `preferred` 术语要求，使用已被取代的旧译构成术语缺陷。

---

### C06 | entry-03685 | 存在问题
- **原文短引**：`All Krogs are infused with anti-magic forces as a result of the changes made to their bodies by the Ziguranth.`
- **译文短引**：`作为上面条件的附加作用，克罗格的身体被伊格兰斯的反魔法力量所灌注。`
- **问题说明**：原文 `as a result of the changes made to their bodies by the Ziguranth` 明确表示克罗格体内充满反魔法力量是“伊格兰斯对其身体进行肉体改造/改变的结果”。译文翻译为“作为上面条件的附加作用”，凭空捏造了“上面条件”，不仅丢失了伊格兰斯对食人魔进行外科肉体改造的关键背景叙事，还引入了逻辑荒谬的机械化措辞。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/intro-krog.lua:26`。结合同文件及 `unlock-race_krog.lua` 叙事（`After lots of painful, but required, experiments Zigur was finally able to create an offshoot...`），伊格兰斯通过对食人魔身体强行剥离符文并注入龙血改造创造了克罗格。译文将肉体改造丢失并误译为“上面条件的附加作用”，属于严重语义失真与无据脑补。

---

### C07 | entry-03685 | 存在问题
- **原文短引**：`yet you a Krog have been kept alive by the powers of nature coursing through your body.`
- **译文短引**：`而你这样克罗格却可以通过你身体内的自然力量存活。`
- **问题说明**：译文“而你这样克罗格却可以通过……”存在明显的语法语病/错别字（缺失量词或虚词，“这样克罗格”应为“作为克罗格”或“这名克罗格”/“这样的克罗格”）。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/intro-krog.lua:24`。同类句式为同位语结构（`you, a Krog, have been...`），译文语句不通，属于语法与文本瑕疵。

---

### C08 | entry-03685 | 仅建议
- **原文短引**：`You have come to an old ruin named Kor'Pul...`
- **译文短引**：`你来到了一个古老的废墟：卡普尔。`
- **问题说明**：地名 `Kor'Pul` 在术语快照中收录为 `卡·普尔`（带间隔号），译文中译为 `卡普尔`。
- **状态**：仅建议。
- **依据与消费逻辑**：术语快照中 `kor'pul | 卡·普尔 | T.NARRATIVE.LORE | status=existing`。根据规则，`existing` 不单独作为强制改名依据，但考虑到同条目已存在 C05 术语违规，建议地名拼写同步规范为规范译名 `卡·普尔`。

---

### C09 | entry-03686 | 仅建议
- **原文短引**：`New Class: #LIGHT_GREEN#Cultist of Entropy (Demented)`
- **译文短引**：`新职业 : #LIGHT_GREEN#熵教徒（疯狂系）`
- **问题说明**：冒号使用了半角冒号且前后留空 `新职业 : `，与相邻解锁条目（如 entry-03688 `新种族：#LIGHT_GREEN#克罗格`、entry-03690 `新技能树：#LIGHT_GREEN#天谴之龙`）的全角冒号 `：` 不一致。
- **状态**：仅建议。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-demented_cultist_entropy.lua:20`。术语 `Cultist of Entropy`（熵教徒）与 `Demented`（疯狂系）消费完全正确无误，标点格式仅属界面一致性与排版偏好建议。

---

### C10 | entry-03689 | 存在问题
- **原文短引**：`After lots of painful, but required, experiments Zigur was finally able to create an offshoot of the ogre race...`
- **译文短引**：`在经过无数痛苦但不可避免的实验后，伊格兰斯终于创造出食人魔的一个亚种。`
- **问题说明**：原文第3段主语为地点专名 `Zigur`，译文将其翻译为了教团全称 `伊格兰斯`，违反了 `preferred` 术语的严格区分要求。
- **状态**：存在问题。
- **依据与消费逻辑**：冻结术语快照中专门对 `Zigur` 与 `Ziguranth` 作出严格区分判定：
  - `Zigur | 伊格 | T.PN.PLACE | preferred | core | 指地点时一律用「伊格」，不得写成「伊格兰斯」。`
  - `Ziguranth | 伊格兰斯 | T.PN.FACTION | preferred | core | 教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换。`
  在本条原文中，第2段 `Ziguranth took pity on them` 正确译为 `伊格兰斯同情他们`，第4段 `staunch protectors of Zigur` 正确译为 `伊格的坚实保护者`，唯独第3段 `Zigur was finally able to create...` 将 `Zigur` 错译成了 `伊格兰斯`，造成同一文本内指代混乱且直接违反 preferred 规则。

---

### C11 | entry-03689 | 存在问题
- **原文短引**：`...to crush all foes of Nature!`
- **译文短引**：`...摧毁所有自然的敌人\n\n你从不死生物的魔爪中救下了一群克罗格...`
- **问题说明**：原文段落末尾有明确感叹号 `!`，译文段末完全漏掉了句末标点符号，句子未收束即直接换行换段。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-race_krog.lua:26`。排版格式中漏掉句末标点属于文本完整性缺陷。

---

### C12 | entry-03689 | 存在问题
- **原文短引**：`- Drake infused blood that lets them resist the elements themselves`
- **译文短引**：`- 他们龙血灌注的身体可以抵抗元素魔法伤害。`
- **问题说明**：原文为“抵抗元素本身”（resist the elements themselves）。译文画蛇添足增加了“魔法”二字，译作“抵抗元素魔法伤害”。这一增译直接违背了游戏设定和技能实际运作机制：克罗格是由伊格兰斯反魔势力创造的反魔种族，其种族天赋 `Drake-Infused Blood`（龙血灌注，源码 `sources/cults/tome-cults/data/talents/misc/races.lua:36`）提供的元素抗性包含物理（Physical）、自然（Nature）、火焰（Fire）、寒冰（Cold）、闪电（Lightning）、酸性（Acid），这些属于各元素能量形态，既非单纯的魔法伤害，更与克罗格敌视奥术魔法（Arcane）的背景冲突。
- **状态**：存在问题。
- **依据与消费逻辑**：克罗格背景强调其反魔法特性（“身体被反魔法力量所灌注”、“摧毁所有自然的敌人”），将龙血抗性误加上“魔法”标签属于机制与设定的双重误导。

---

### C13 | entry-03691 | 存在问题
- **原文短引**：`Drakes are forces of Nature, the ultimate apex predators. But even they can be corrupted beyond hope.`
- **译文短引**：`龙是自然力量的化身，是究极的捕食者。然而，就连他们也能够被绝望所腐化。`
- **问题说明**：英文成语短语 `beyond hope` 表示程度，意为“无可救药地 / 万劫不复地 / 彻底无法挽回地”（hopelessly / without any hope of recovery）。译者看词生义，将其硬译成了“被绝望所腐化”（corrupted by despair），把表示“腐化程度已无法挽救”的副词修饰语错当成了致使腐化的施动者/实体（“绝望”），属于明显的语义误译。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua:21`。背景描述天谴龙（Scourge Drake）源自最强大的巨龙库洛塔被枯萎与恐魔彻底腐化变异，原文旨在说明即使是顶级掠食者的龙也会堕落到“不可救药”的地步，并非被抽象的“绝望”概念腐化。

---

### C14 | entry-03691 | 存在问题
- **原文短引**：`...that can learn the #LIGHT_GREEN#Scourge Drake talents#WHITE#.\n\nTalents:`
- **译文短引**：`...可以使用新的#LIGHT_GREEN#天谴之龙#WHITE#系技能\n\n技能列表：`
- **问题说明**：第三句句末“技能”二字之后漏标了句末句号 `。`，原文末尾有句号 `.`。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua:24`。属于格式与标点漏标缺陷。

---

## 核验材料、版本与审计边界报告

### 1. 实际读取的所有路径与版本声明
- **主配置与输入文件**：
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923/INPUT.md`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923/entries.json`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923/context.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923/source-access.json`
- **涉及的DLC源码单文件（快照哈希固定，源码仓库/commit未固定，unpinned）**：
  - `sources/dlc/cults/tome-cults/data/timed_effects.lua`（sha256: `0d3139eb...`）
  - `sources/dlc/cults/tome-cults/data/zones/entropic-void/grids.lua`（sha256: `76362709...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-cultist/npcs.lua`（sha256: `427cfbeb...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-haze-cave/grids.lua`（sha256: `0daf2315...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-haze-cave/npcs.lua`（sha256: `a635f2db...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-haze-cave/zone.lua`（sha256: `b6e63611...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-home/grids.lua`（sha256: `9b603cd0...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-horrors/objects.lua`（sha256: `3ee604b7...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-illusory-castle/grids.lua`（sha256: `f076d7d3...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-illusory-castle/zone.lua`（sha256: `5aaa62fc...`）
  - `sources/dlc/cults/tome-cults/data/zones/ft-yaech/grids.lua`（sha256: `65a1552e...`）
  - `sources/dlc/cults/tome-cults/data/zones/godfeaster/zone.lua`（sha256: `546167c0...`）
  - `sources/dlc/cults/tome-cults/data/zones/test/traps.lua`（sha256: `fb291aa0...`）
  - `sources/dlc/cults/tome-cults/data/zones/town-kroshkkur/npcs.lua`（sha256: `4ea54357...`）
  - `sources/dlc/cults/tome-cults/data/zones/town-kroshkkur/traps.lua`（sha256: `fb291aa0...`）
  - `sources/dlc/cults/tome-cults/hooks/bonestaff.lua`（sha256: `20d404c6...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/intro-cults.lua`（sha256: `e68e7487...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/intro-krog.lua`（sha256: `6d176a8cf...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/unlock-demented_cultist_entropy.lua`（sha256: `8889d226...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/unlock-race_drem.lua`（sha256: `9fbe2c05...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/unlock-race_krog.lua`（sha256: `a4218856...`）
  - `sources/dlc/cults/tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua`（sha256: `295374bc...`）
  - `sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua`（sha256: `80e2fe3b...`）
- **额外调用的DLC单文件及调用链来源**：
  - `tome-cults/data/talents/misc/races.lua`（sha256: `59b9b67cb...`，列明于 `dlc_additional_sources`）：由 `entry-03689` 的 `unlock-race_krog.lua` 叙述之克罗格种族特性及天赋 `Drake-Infused Blood` 符号引入，核验其抗性类型与元素判定。
- **任务专属临时目录**：
  - `/tmp/abc20-g13-20260923-bkzj4hfe`（存放提取上下文与校验的中间脚本，无他人材料）。

### 2. 越界与合规声明
- **无越界访问**：未读取任何其他模型输出、历史评审报告、SPEC/STATE 或生产结论文件；未遍历未授权源码目录。
- **无状态变更**：未修改仓库内任何文件，未创建任何子 agent。
- **只读性质**：本输出仅为独立只读审核观察，不作任何修改修复，不宣称生产 `DONE_VERIFIED`。
