## 复核结果：entry-03653–entry-03692（共 40 条）

结论：40 条中 **10 条存在问题**、**4 条待确认**、**6 条仅建议**、**20 条未发现问题**。这些是审核观察，不是真值，不构成生产 DONE_VERIFIED。所有 DLC 证据都来自 source-access 列明、哈希已核对一致（23/23）的 cults 快照；该快照的源码仓库和 commit 未固定，目标版本是否适用仍待确认。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03653 | 未发现问题 | CULTS_BOOK_TIMEOUT 的 long_desc（timed_effects.lua:1877），与效果名「禁忌之书」一致 |
| entry-03654 | 未发现问题 | GASTRIC_WAVE_BUFF 施加时清除全部负面效果（timed_effects.lua:2067,2074-2075） |
| entry-03655 | 仅建议 | C01 |
| entry-03656 | 未发现问题 | TWISTED_FORM 的 on_gain（timed_effects.lua:2231） |
| entry-03657 | 未发现问题 | ENTROPIC_ROD 的 on_gain（timed_effects.lua:2306） |
| entry-03658 | 存在问题 | C02 |
| entry-03659 | 仅建议 | C03 |
| entry-03660 | 未发现问题 | 训练假人的 desc（ft-cultist/npcs.lua:136），与 context 的名称「训练用傀儡」一致 |
| entry-03661 | 未发现问题 | ft-cultist/npcs.lua:278，与名称「人类学徒」一致 |
| entry-03662 | 未发现问题 | ft-cultist/npcs.lua:289，与术语 Shalore＝永恒精灵一致 |
| entry-03663 | 未发现问题 | ft-cultist/npcs.lua:301，与术语 Halfling＝半身人一致 |
| entry-03664 | 未发现问题 | ft-haze-cave/grids.lua:110 的 bignews 提示 |
| entry-03665 | 未发现问题 | on_takehit 且 src.is_grung 时触发（ft-haze-cave/npcs.lua:57-61），「伟大的存在」指这些 STORY_NPC |
| entry-03666 | 未发现问题 | game.log 的 %s 就是 emote 文本（ft-haze-cave/zone.lua:179） |
| entry-03667 | 未发现问题 | ft-home/grids.lua:33 地板的 desc |
| entry-03668 | 存在问题 | C04 |
| entry-03669 | 未发现问题 | ft-illusory-castle/grids.lua:96 |
| entry-03670 | 未发现问题 | 两个 %s 依次为颜色和区域名，顺序保留（ft-illusory-castle/zone.lua:340） |
| entry-03671 | 未发现问题 | ft-yaech/grids.lua:55 |
| entry-03672 | 仅建议 | C05 |
| entry-03673 | 待确认 | C06 |
| entry-03674 | 未发现问题 | 钉锤／大锤类武器商店名（test/traps.lua，MAUL_WEAPON_STORE） |
| entry-03675 | 未发现问题 | 灵晶商店名（test/traps.lua，MINDSTAR），单数 Star 译作「之星」 |
| entry-03676 | 未发现问题 | anger_emote，@himher@ 保留（town-kroshkkur/npcs.lua:27） |
| entry-03677 | 未发现问题 | town-kroshkkur/npcs.lua:53，与术语 Drem＝德瑞姆一致 |
| entry-03678 | 待确认 | C07 |
| entry-03679 | 未发现问题 | 同 03674（town-kroshkkur/traps.lua:53） |
| entry-03680 | 未发现问题 | 同 03675（town-kroshkkur/traps.lua:83） |
| entry-03681 | 存在问题 | C08、C09 |
| entry-03682 | 未发现问题 | 聊天回答「Great!」（bonestaff.lua:104） |
| entry-03683 | 存在问题 | C10、C11 |
| entry-03684 | 存在问题 | C12、C13、C14 |
| entry-03685 | 存在问题 | C15、C16、C17 |
| entry-03686 | 仅建议 | C18 |
| entry-03687 | 未发现问题 | 标记与换行对齐；Frenzy「使技能不进入冷却」沿袭上游简化（context 中该效果实为「第一次使用的职业技能不进入冷却」），不是翻译新增 |
| entry-03688 | 未发现问题 | unlock-race_krog.lua:20，与术语 Krog＝克罗格一致 |
| entry-03689 | 存在问题 | C19、C20、C21、C22 |
| entry-03690 | 未发现问题 | unlock-wyrmic_scourge.lua:20 |
| entry-03691 | 存在问题 | C23、C24、C25 |
| entry-03692 | 存在问题 | C26 |

---

### C01 | entry-03655 | 仅建议
「目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，…」这句混用了半角逗号，逗号前还有多余空格。对照 timed_effects.lua:2124 与 2139-2142 的 updateEffect：各数值及其顺序全部正确。confusion_immune −0.04×层数显示为「层数×4 %」，insanity_regen 为 0.5×层数，「精神豁免」「疯狂值」也与术语一致。所以这里只有标点和空格可以统一，属于排版偏好，不是缺陷。

### C02 | entry-03658 | 存在问题
原文「#Target# is bolstered at the sight of the horror!」，译文「#Target#在恐魔的视线中被强化了！」。
- 原文的「at the sight of」是说目标**看到**恐魔而受到鼓舞。
- 译文变成「处于恐魔的视线之中」，把「看」这个动作归给了恐魔，谁看谁被反转了（所属关系错误）。
- 译文还暗示有一个「在对方视野内」的生效条件，源码里没有。HORRIFIC_FORTRESS 在 timed_effects.lua:2322-2345 中，只要 eff.src 还活着就持续（on_timeout 只检查 src 是否存在、是否死亡），不做任何视线判定。
- 状态：存在问题（纯语义，机制证据见上）。

### C03 | entry-03659 | 仅建议
「The rift leads... somewhere.」译作「裂缝通向…某个地方。」。同一实体名在 context.lua:344 译为「时空裂隙」，这里的描述却用「裂缝」；省略号也只用了单个「…」。两者都不改变信息，属于用词和排版统一的偏好（entropic-void/grids.lua:34,39）。

### C04 | entry-03668 | 存在问题
「A page of the tome.」只译成「书页。」，丢了「the tome」这层定指归属，即这是**这本**禁忌之书的一页。该条是 ft-horrors/objects.lua:26-29 中 BASE_LORE 笔记「the truth beyond the veil (i)」的 desc，所在区域就是禁忌之书 FORBIDDEN_TOME_HOME（同文件:35）。译文成了泛指的书页，所属关系信息丢失。影响较轻，但按规则不能因为读者能猜出来就忽略。

### C05 | entry-03672 | 仅建议
「tremors in the worm」译作「虫子在颤抖」。godfeaster 是一条巨型蠕虫，intro 文本里用的是「巨型蠕虫」，「虫子」语气偏轻。信息没有错，属于措辞偏好（godfeaster/zone.lua:138）。

### C06 | entry-03673 | 待确认
「Swordsmith」（source_tag 为 entity name）译作「铸剑铺」，术语快照中是「长剑铁匠铺」（existing，core，城镇商店实体）。
- existing 本身不强制改名。
- 疑点在运行时：固定 commit 的 engine/I18N.lua:41-69、141-143 中，`_t` 与 `I18N:t` 都以 locale 下的 `[tag][src]` 为键，不含 section。
- 因此 cults 的 ("Swordsmith","entity name") 与本体同键条目若译法不同，会互相覆盖（后加载者生效），造成同名商店显示不一致。
- 缺少的证据：本体当前翻译文件中该键的实际 target，以及加载顺序。按规定这两项都不可读。

### C07 | entry-03678 | 待确认
情况同 C06：town-kroshkkur/traps.lua:43 的「Swordsmith」译作「铸剑铺」，与术语快照的「长剑铁匠铺」同键不同译，是否发生运行时覆盖待确认。

### C08 | entry-03681 | 存在问题
原文「You feel the bones of the staff creeking and vibrating in your hand.」，译文「你感受到手中的骨杖在你的手上颤动」只保留了 vibrating，漏掉了 creeking（骨头嘎吱作响）这个感官信息，属于语义信息遗漏（bonestaff.lua:24）。影响较轻。

### C09 | entry-03681 | 仅建议
「手中的骨杖在你的手上」前后重复表达了位置。标记与引号都完整保留，这只是措辞冗余。

### C10 | entry-03683 | 存在问题
原文「Stupid useless pathetic excuse of a "necromancer"!」，译文「像你这样的"死灵法师"竟然会用这样蹩脚的借口！」。
- 「pathetic excuse of a X」是固定骂语，意思是「不配称为 X 的可怜货色」，没有「借口」的意思。
- 按对话顺序，这句话在玩家说出理由之前：玩家先选「I want you to stop summoning the bone horror.」（bonestaff.lua:64），法杖回应本句（:114-115），之后玩家才能答「I have my reasons!」（:117）。所以译文里「用借口」这件事在剧情中尚未发生，属于事实错误。
- 另外「Stupid useless」两个侮辱修饰语也被丢掉了。
- 状态：存在问题。

### C11 | entry-03683 | 仅建议
「The staff stays calm.」译作「法杖平静了下来」。原文是「保持平静」，译文带有「从躁动转为平静」的意味，但核心信息（法杖没有反应）还在，属于措辞偏好。

### C12 | entry-03684 | 存在问题
原文「or leave now while it is safe to do so and let Kroshkkur be destroyed」，译文「你可以现在踏入…传送门或者就这样离开任由克诺什库尔被巨型蠕虫摧毁」（intro-cults.lua:29）。
- 「while it is safe to do so」这个条件和时机被整句删除。
- 「now」从「离开」一项移到了「传送门」一项。
- 结果是「趁现在还安全离开」的条件和时序信息丢失，选项的时间归属也变了。

### C13 | entry-03684 | 存在问题
「If nothing is done it will collide with…」译作「如果再不迅速做出决断，它将会…」。原文的条件是「不采取行动」，译文改成了「不迅速做出决断」，行动变成了决断，还新增了「迅速」这个时间约束，条件被改写。影响轻微，单独列出以便归并。

### C14 | entry-03684 | 仅建议
以下几处是增补、冗余或意象弱化，都没有引入错误事实，所以算措辞层面：
- 「这导致了对许多地表人视为疯狂且被禁止之事的实验，而你们的研究内容也被普通人的社会所禁止」：后半句是译者添加的重复。
- 「希望解开过去的阴影」「追寻禁忌的知识」：属于润色添加。
- 「tunneling directly towards」译作「直接冲向」：失去了「掘地而来」的意象。

### C15 | entry-03685 | 存在问题
「While much of Maj'Eyal shuns the arcane」译作「大部分马基埃亚尔人」（intro-krog.lua:26）。术语快照 Maj'Eyal＝「马基·埃亚尔」为 preferred（_t，T.PN.WORLD），备注写明「马基埃亚尔」已被取代。同文件的 title 在 context.lua:717 也已使用「马基·埃亚尔」。这是适用的术语要求未被遵守。

### C16 | entry-03685 | 存在问题
原文「All Krogs are infused with anti-magic forces as a result of the changes made to their bodies by the Ziguranth.」，译文「作为上面条件的附加作用，克罗格的身体被伊格兰斯的反魔法力量所灌注。」
- 原文的因果是：伊格兰斯**对其身体所做的改造**，结果使克罗格带有反魔法力量。
- 译文把原因改成「上面条件」（即靠自然之力存活），又把反魔法力量归属给伊格兰斯。
- 因果和所属关系都被改写。

### C17 | entry-03685 | 仅建议
- 「Kor'Pul」译作「卡普尔」，术语快照只有 newLore 类目下的「卡·普尔」（existing，标签不同），不构成强制要求。
- 原文段间空行被合并为单换行（原文 7 个 \n，译文 5 个）。段落仍然可以分辨，没有造成信息结构丢失，属于排版差异。

### C18 | entry-03686 | 仅建议
「新职业 : 」冒号前后带半角空格，同类的 03688 用「新种族：」。纯排版不一致。术语「熵教徒」「疯狂系」与快照一致。

### C19 | entry-03689 | 存在问题
原文「But while they are magic users Ziguranth took pity on them…」，译文「然而，伊格兰斯同情他们被强迫而无法选择的命运。」，删去了让步条件「尽管他们是魔法使用者」（unlock-race_krog.lua:24）。这个条件交代了反魔教团同情对象的特殊性，属于语义信息遗漏。

### C20 | entry-03689 | 待确认
原文「Zigur was finally able to create an offshoot…」（:25）中的 Zigur 被译为「伊格兰斯」（教团名）。术语备注要求地点用「伊格」、教团用「伊格兰斯」，「两者不得互换」。但此处的 Zigur 作施事主语，可能是借地名指代教团。是否属于不得互换的情形，需要术语裁决，缺少针对借代用法的明确依据。

### C21 | entry-03689 | 待确认
「Drake infused blood that lets them resist the elements themselves」（:32）译作「可以抵抗元素魔法伤害」。译文比原文多了「魔法」这一限定，把范围收窄或改写为「魔法性质的元素伤害」。是否与实际抗性（应为若干元素伤害类型的抗性）不符，需要克罗格种族天赋定义佐证。本组 sources 中没有该定义，按显式调用链规则也不能从本文件引入，所以待确认。

### C22 | entry-03689 | 仅建议
- 「…摧毁所有自然的敌人」句末缺少终止标点（原文为「!」）。
- 「A mastery of infusions like no others」译作「自然纹身的大师」，弱化了「无人能及」的程度，但「大师」已经表达了卓越。
- 「infusions」译「纹身」与术语一致。
- 以上都属于措辞和排版。

### C23 | entry-03691 | 存在问题
「But even they can be corrupted beyond hope.」译作「就连他们也能够被绝望所腐化。」（unlock-wyrmic_scourge.lua:21）。「beyond hope」意为「无可救药地」，是程度状语；译文把它理解为腐化的施动者「绝望」，意思错误。

### C24 | entry-03691 | 待确认
「Augment Despair: …doing more damage based on detrimental effects」（:29）译作「对方负面效果越多伤害越高」。原文只说伤害「基于负面效果」增加，译文补出了「按数量递增」的关系。是否与天赋实际计算一致，需要 Scourge Drake 天赋定义，本组 sources 中没有，也无法经显式调用链引入。

### C25 | entry-03691 | 仅建议
- 首段后的空行被合并（原文 10 个 \n，译文 9 个）。段落仍可辨，不影响显示结构。
- 「你创建的新龙战士角色可以使用新的…系技能」句末缺标点。
- 「Scourge Drake magic」译「天谴龙的魔法」，与「天谴之龙」写法不统一。
- 均为排版和用词偏好；标记完整。

### C26 | entry-03692 | 存在问题
原文「Damage and cooldowns have a chance to increase or decrease by up to chaotic%.」，译文「伤害和冷却时间将会在 混沌度% 的范围内上下浮动。」
- 「have a chance to」被删掉，把按概率发生写成了必然发生；下一句的「浮动的几率」不能补回这句的断言。
- 该文本作为 description 传给 `ActorResource:defineResource`（CultsDLC.lua:47），在固定 commit 的 engine/interface/ActorResource.lua:45,58 中原样存为 description，没有占位替换。所以「chaotic」→「混沌度」只是文字，与 status_text 的译法（context.lua:856「混沌度」）一致，不是格式问题。
- 问题只在被删掉的概率限定词。

---

## 读取路径与越界说明
- **冻结输入**：experiments/abc20-g13-20260923/INPUT.md、entries.json（target、baseline_target、换行和标记计数）、context.lua（按关键词检索）、source-access.json。另外用 `ls` 看了该目录的文件名列表，但没有打开 SPEC、STATE、PLAN、BASELINE、FREEZE、SCORING、dispatches、raw、reports 的内容。
- **本组 sources**（仓库和 commit 未固定；按 source-access 核对 sha256，23/23 一致）：
  - data/timed_effects.lua
  - zones 下：entropic-void/grids、ft-cultist/npcs、ft-haze-cave/{grids,npcs,zone}、ft-home/grids、ft-horrors/objects、ft-illusory-castle/{grids,zone}、ft-yaech/grids、godfeaster/zone、test/traps、town-kroshkkur/{npcs,traps}
  - hooks/bonestaff.lua
  - overload/data/texts 下六个文件
  - overload/mod/class/CultsDLC.lua
- **本体（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63），均用 `git -C /workspace/t-engine4 show` 单文件读取**：
  - `game/engines/default/engine/I18N.lua`：由各 entry 源文件使用的 `_t` 符号引入，用于判断运行时键的构成（C06/C07）。
  - `game/engines/default/engine/interface/ActorResource.lua`：由 CultsDLC.lua:38 的 require 和 :47 的 `defineResource` 调用引入（C26）。
- **dlc_additional_sources**：只在 source-access.json 中看到了文件名列表，没有读取其中任何文件内容。
- **越界情况**：未越界。没有读取当前翻译文件、其他报告、历史审核或其他语言的 locale，没有创建临时文件或子 agent，也没有修改仓库。
- **无法核验**：C06、C07 缺本体当前译文；C20 缺术语裁决；C21、C24 缺天赋定义，按调用链规则无法引入。
