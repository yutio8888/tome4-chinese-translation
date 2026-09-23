## 40条译文复核判定总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03493 | 未发现问题 | 语义忠实，巨大蛆虫与防御细胞指代明确 |
| entry-03494 | 未发现问题 | 语义准确，生物体分工与注意力分散表述清晰 |
| entry-03495 | 未发现问题 | 符合光芒恐魔（radiant horror）规范术语，语意贴切 |
| entry-03496 | 存在问题 | C01 |
| entry-03497 | 未发现问题 | 语义准确，触须指环与恶意能量描述忠实 |
| entry-03498 | 存在问题 | C02 |
| entry-03499 | 未发现问题 | 战斗状态脱戒指判定日志语义准确，颜色代码保留 |
| entry-03500 | 未发现问题 | 恐魔（horror）术语正确，占位符与颜色代码保留 |
| entry-03501 | 未发现问题 | 准确对应法杖掌控（Command Staff）技能交互 |
| entry-03502 | 未发现问题 | 选项名称与法术暴击率加成翻译准确 |
| entry-03503 | 未发现问题 | 符合法术豁免（spell save）规范术语 |
| entry-03504 | 未发现问题 | 符合魔力（magic）属性规范术语 |
| entry-03505 | 未发现问题 | 符合意志（willpower）属性规范术语 |
| entry-03506 | 未发现问题 | 闪避（defense）属性加成翻译准确 |
| entry-03507 | 未发现问题 | 移动速度（movement speed）属性加成翻译准确 |
| entry-03508 | 未发现问题 | 符合敏捷（dexterity）属性规范术语 |
| entry-03509 | 未发现问题 | 符合灵巧（cunning）属性规范术语 |
| entry-03510 | 仅建议 | C03 |
| entry-03511 | 存在问题 | C04 |
| entry-03512 | 未发现问题 | 双子武器集齐日志翻译准确，颜色代码保留 |
| entry-03513 | 存在问题 | C05 |
| entry-03514 | 存在问题 | C06 |
| entry-03515 | 未发现问题 | 占位符数量与参数消费顺序（主语/物主代词/物品名）匹配无误 |
| entry-03516 | 未发现问题 | 大地图巡逻队减速机制与格式标签（PURPLE/italic/normal）保留完整 |
| entry-03517 | 存在问题 | C07, C08, C09 |
| entry-03518 | 未发现问题 | 符合魔法大爆炸（Spellblaze）规范术语与章节格式 |
| entry-03519 | 未发现问题 | 符合纹身（infusions）规范术语与章节格式 |
| entry-03520 | 未发现问题 | 符合永恒精灵（Shaloren）规范术语与章节格式 |
| entry-03521 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03522 | 存在问题 | C10, C11, C12 |
| entry-03523 | 未发现问题 | 人名将军头衔与章节格式翻译准确 |
| entry-03524 | 未发现问题 | 地名埃尔瓦拉与章节格式翻译准确 |
| entry-03525 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03526 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03527 | 存在问题 | C13, C14, C15, C16 |
| entry-03528 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03529 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03530 | 未发现问题 | 章节标题翻译准确，格式规范 |
| entry-03531 | 存在问题 | C17, C18, C19, C20 |
| entry-03532 | 未发现问题 | 章节标题“死里逃生”（Spared）契合故事剧情，格式规范 |

---

## 详细复核观察（按 Claim 编号）

### C01 | entry-03496 | 存在问题
- **原文短引**：`A strange tall crystal pusling with nether energies.`
- **译文短引**：`一团发射出虚空能量的高大水晶。`
- **问题说明**：将 `nether energies` 错译为“虚空能量”。在 ToME4 及本 DLC（Cults of Entropy）机制与世界观中，Nether（彼世）与 Void（虚空）为两种完全不同的能量属性与技能派系（对应底层独立的 `DamageType.NETHER` 与 `DamageType.VOID`，以及 `talents/demented/nether.lua` 与 `void.lua`）。同文件 `horror.lua:31` 中的 nethergate 正确且统一地译作“彼世能量”。此处错译为“虚空能量”造成机制属性与设定的混淆。此外，“高大水晶”使用量词“一团”亦不妥。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/npcs/horror.lua:131`（实体 `bursting entropic shard` 的 `desc` 字段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C02 | entry-03498 | 存在问题
- **原文短引**：`When first worn the ring attunes to you, letting you choose a prodigy...`
- **译文短引**：`当你第一次戴上戒指的时候，选择一个觉醒技能...`
- **问题说明**：关键叙事机制从句 `the ring attunes to you`（指环与你建立调谐/共鸣）被完全漏译。译文从时间从句突兀地跳跃至祈使句“选择一个觉醒技能”，脱落了“指环与佩戴者调谐/共鸣”这一核心叙事设定信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:104`（`special_desc` 函数），对应第 205 行穿戴时的共鸣判定 `feel more attuned to...`。DLC 快照 hash 验证一致，未固定 commit。

---

### C03 | entry-03510 | 仅建议
- **原文短引**：`The %s reaches for %s with a tentacle!`
- **译文短引**：`%s使用触手抓握%s！`
- **问题说明**：现有译文占位符顺序与数量消费正确，且代码底层确实通过 `target:pull` 触发拉拽至身边。此处“使用触手抓握”表述稍显机械，若作“伸出触手抓向%s”或“伸出触手抓取%s”在中文中更为顺畅。现有译文表达清晰无事实性缺陷，本条仅属措辞表达偏好建议。
- **状态**：`advisory`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:566`（`CUT_DREM_ARM` 的 `callbackOnAct` 中的 `game.logSeen`）。

---

### C04 | entry-03511 | 存在问题
- **原文短引**：`As you wear the sword you feel it attuning to your Krog body, increasing in power!`
- **译文短引**：`你感受到你的剑和克罗格的身躯共鸣，解放了强大的力量！`
- **问题说明**：遗漏了触发动作的时间条件状语 `As you wear the sword`（当你装备/佩戴此剑时），导致日志脱离了玩家即时穿戴装备的行为语境；同时第二人称所有格 `your Krog body` 被稀释并泛化为类似第三人称的“克罗格的身躯”（丢失了“你身为克罗格的身躯/你的克罗格身躯”的第二人称认同）。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:689`（`ART_PAIR_PERSEVERANCE` 的 `on_wear` 回调中的 `game.logPlayer`）。DLC 快照 hash 验证一致，未固定 commit。

---

### C05 | entry-03513 | 存在问题
- **原文短引**：`...you somehow do not like the idea of having so many parasitic creatures so close to your vulnerable flesh.`
- **译文短引**：`...但是让这么多寄生生物如此接近你脆弱的肉体……实在是太恶心了。`
- **问题说明**：原文核心谓语与主干为表达主角心理上的隐隐抗拒与不情愿（`you somehow do not like the idea of...`，不知怎的你并不喜欢让寄生生物贴近肉体这个念头/感到排斥），译文完全漏译了这一心理主干，而是凭空添加了主观感叹“……实在是太恶心了”，属于叙事语义信息的脱落与不当添枝加叶。此外第 2 句“上面的小蠕虫有时会从上面跳出来”存在“上面”重复累赘。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:800`（实体 `Worm Nest` 的 `desc` 字段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C06 | entry-03514 | 存在问题
- **原文短引**：`As you combine the two pair of shoes you make something marvelous: %s`
- **译文短引**：`当你将这两件鞋子结合时，你制造出了神奇的道具：%s`
- **问题说明**：量词与数量概念错误。原文明确指出 `the two pair of shoes`（指慢行之鞋与快行之鞋“两双鞋”），中文鞋类量词规范应为“双”，误译为“两件”，存在明确的量词使用错误。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:994`（`Shoes of Moving Slowly` 的 `use_simple` 触发合成后的 `game.logPlayer` 日志）。DLC 快照 hash 验证一致，未固定 commit。

---

### C07 | entry-03517 | 存在问题
- **原文短引**：`wide enough for one of our party to fit in with room to spare.`
- **译文短引**：`管径很宽，足够让我们的一个小队在里面行走。`
- **问题说明**：严重曲解叙事实体与物理尺度。`one of our party`（我们队伍中的一人/单个成员）被误译为整支“我们的小队”；`to fit in with room to spare`（容纳一人进入且尚有空余空间，描述圆柱形培养/培育管道容积）被严重曲解为“在里面行走”。结合下文事实，这些管道是浸泡、孕育单个矮人或怪物的培养管（"dwarves sleeping inside tubes"），并非供整支小队行走的巨大隧道，该误译彻底扭曲了叙事场景。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:58`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C08 | entry-03517 | 存在问题
- **原文短引**：`...for such a concentration of these energies simply couldn't exist on Eyal.`
- **译文短引**：`...因为这些能量根本不可能存在于埃亚尔集中出现...`
- **问题说明**：中文语序错乱与语法语病。“存在于埃亚尔集中出现”词序杂糅颠倒，且丢失了 `such a concentration of these energies`（如此高浓度的这种能量）中的核心定语信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:56`（第 3 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C09 | entry-03517 | 存在问题
- **原文短引**：`We wandered into the back of the room where there were yet more tubes.`
- **译文短引**：`我们徘徊到那些还有更多管子的房间里面。`
- **问题说明**：空间方位理解错误。`the back of the room` 指该大厅/房间的后部区域（深处），与前段发现培育机器的中心房间为同一房间；译文误译为“房间里面”，误导玩家以为是穿行进入了另一个独立的新房间。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:70`（第 10 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C10 | entry-03522 | 存在问题
- **原文短引**：`Seemingly they would rather tempt fate and avoid using them.`
- **译文短引**：`似乎他们宁愿接受命运，也要避免使用它们。`
- **问题说明**：严重词义反转。`tempt fate` 为英文常用成语，意为“玩命、铤而走险、抱侥幸心理冒险”，译文却将其完全反向误译为“接受命运”（accept fate），彻底颠倒了永恒精灵宁可抱侥幸心理冒险赌命也不用纹身的心态刻画。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:113`（第 1 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C11 | entry-03522 | 存在问题
- **原文短引**：`Well, I should say to the shalore it may have been basic food and drink, but by thalore standards I was treated pretty lavishly.`
- **译文短引**：`好吧，我应该对永恒精灵说，这可能对它们来说是基本的食物和饮料，但按照自然精灵的标准...`
- **问题说明**：句法断句严重错误。原句 `to the shalore` 是后半句 `it may have been basic food and drink` 的状语（“对于永恒精灵而言，这或许只是粗茶淡饭”），主干为 `Well, I should say [that]...`（“好吧，我得承认/我得说……”）。译文错误将 `to the shalore` 挂在 `say` 后面译作“我应该对永恒精灵说”，破坏了叙事逻辑。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:115`（第 2 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C12 | entry-03522 | 存在问题
- **原文短引**：`When their numbers began to reach more manageable amounts, the chief healer approached to thank me...`
- **译文短引**：`当痊愈士兵的数量开始达到一定程度时，主治医师代表永恒精灵来感谢我的努力。`
- **问题说明**：主语与事实颠倒。`their numbers` 紧承前句 `the number of wounded soldiers began to dwindle`，指需要救治的伤员数量减少到了更容易应付的程度；译文却颠倒主语译为“当痊愈士兵的数量开始达到一定程度时”，歪曲了原文事实陈述。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:131`（第 10 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C13 | entry-03527 | 存在问题
- **原文短引**：`Noting it I said, "You wouldn't happen to know anything regarding items the dwarves might be carrying that the guards at the city gates would confiscate would you?"`
- **译文短引**：`想到这一点，我问道：“你可能还不知道，士兵会没收矮人们携带的物品，知道吗？”`
- **问题说明**：严重反转问话意图与信息流向。原句为委婉提问句型 `You wouldn't happen to know... would you?`（“你碰巧知道城门守卫会没收矮人携带的什么物品吗？”），主角是向信使探听情况；译文却翻译成向信使反问告知的居高临下语气：“你可能还不知道……知道吗？”，彻底颠倒了对话双方的信息交互逻辑。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:222`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C14 | entry-03527 | 存在问题
- **原文短引**：`They say that it's too dangerous for civilians to carry such items. Personally I say it is too dangerous for anyone to be carrying such items, them included.`
- **译文短引**：`我个人认为任何人携带这样的物品都是非常危险的，包括他们自己。`
- **问题说明**：关键句整句脱落漏译。原文前半句 `They say that it's too dangerous for civilians to carry such items.`（他们声称平民携带此类物品太危险了）在译文中完全缺失，导致后半句“我个人认为……”失去了官方说辞作为对比铺垫。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:224`（第 5 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C15 | entry-03527 | 存在问题
- **原文短引**：`...since the blasted mages caused their home to collapse in on them.`
- **译文短引**：`...因为法师制造的爆炸摧毁了他们的家园。`
- **问题说明**：词性与修辞语法误译。`blasted` 在此处为修饰痛恨辱骂法师的形容词（“那些该死的法师们”），译文却将其错译为名词事件“法师制造的爆炸”，改变了主从关系与修辞色彩。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:220`（第 3 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C16 | entry-03527 | 存在问题
- **原文短引**：`...for unleashing the Spellblaze on Maj'Eyal.`
- **译文短引**：`...终将会为在马基埃亚尔引发魔法大爆炸的行为付出代价。`
- **问题说明**：违反明确适用的 preferred 术语规范。本包术语快照明确规定：维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代。译文依然使用已被废止的旧译“马基埃亚尔”，未按规范使用间隔号。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:228`（第 7 段），对应术语快照第 142 行。DLC 快照 hash 验证一致，未固定 commit。

---

### C17 | entry-03531 | 存在问题
- **原文短引**：`I had thought better of you since you killed that Eldoral halfling.`
- **译文短引**：`自从你杀了那个艾德瑞尔半身人，我就更想念你了。`
- **问题说明**：极其荒谬的灾难级误译。`thought better of you` 为英文固定成语，表示“我本以为你还算有骨气/原本还高看你一眼/以为你还算明事理”，译文居然望文生义将其误译为“我就更想念你了”，彻底破坏了反派角色充满杀意与质问的狂热氛围，严重损害叙事质量。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:295`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C18 | entry-03531 | 存在问题
- **原文短引**：`...it was entirely possible that I could have become enthralled to the slavers will and made to do their bidding unquestioningly.`
- **译文短引**：`...我完全有可能被奴役者的意志所吸引，毫无疑问地服从他们的命令。`
- **问题说明**：核心设定与心智控制机制误译。`enthralled to someone's will` 在奇幻心智控制/灵能背景下意为“受其心智控制/彻底被其奴役/沦为受支配的奴仆”（术语快照明确标明 Thrall 为精神支配后的奴仆身份），译文却望文生义误译为“被……所吸引”；同时 `unquestioningly`（毫无异议/盲目不折不扣）被误译为“毫无疑问地”。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:289`（第 1 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C19 | entry-03531 | 存在问题
- **原文短引**：`...leaving a faceless humanoid.`
- **译文短引**：`...留下了一个面目全非的人形。`
- **问题说明**：专有名词与种族特征误译。`faceless` 意为“无脸的/没有面孔五官的”（对应 DLC 中 Drem 族“无面”的核心生理特征，与前文第 340 行 "found a faceless dwarf inside. In other words, a Drem" 严格对应），译文却误译为“面目全非”（面部被毁损残缺），丢失了该心象破灭后露出无面人形的重要种族特征信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:299`（第 6 段）。DLC 快照 hash 验证一致，未固定 commit。

---

### C20 | entry-03531 | 存在问题
- **原文短引**：`...who had thrown me` / `why have you thrown me in here?`
- **译文短引**：`是谁在拉我` / `为什么把我拉到这里？`
- **问题说明**：动作动词误译。`throw` 意为暴力地“扔/摔进”，译文两处均误译为缓和的“拉”，弱化了主角被粗暴摔入帐篷并导致头晕目眩的动作冲击力与遇袭情节。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:291`（第 2 段）。DLC 快照 hash 验证一致，未固定 commit。

---

## 读取路径与合规说明

1. **实际读取的文件路径与哈希校验**：
   - 冻结输入包：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/INPUT.md`
   - 来源与权限清单：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/source-access.json`
   - 审阅条目清单：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/entries.json`
   - 同目录邻近上下文：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/context.lua`
   - 本组 6 个 sections 源码文件（均位于 `sources/dlc/cults/...`，经 SHA256 校验与 `source-access.json` 一致）：
     - `sources/dlc/cults/tome-cults/data/general/npcs/corrupted_blobs.lua`（`76cbc59be306a63bfa17d81904820c3838543a9b8b074554190bca408bbfbec4`）
     - `sources/dlc/cults/tome-cults/data/general/npcs/horror.lua`（`8d63e86d5eb6f7552ec2cdfe598b45618460028236190f246202809c045f461d`）
     - `sources/dlc/cults/tome-cults/data/general/objects/world-artifacts.lua`（`27af5b2ae30c5b2db7f1d585b8334bc28ee1284e771a8a9f5c198f892edbc92a`）
     - `sources/dlc/cults/tome-cults/data/glyph_sequences/cults.lua`（`9d3b29fd6a91fb9ced64581b760fc0026b0fb0bcf9cc687a55399aed76faaabf`）
     - `sources/dlc/cults/tome-cults/data/lore/dremwarves.lua`（`0b8133e8ef00f5b0ca5fcb2f7df1ebec355873ac5dfac9454a85a48084b326e9`）
     - `sources/dlc/cults/tome-cults/data/lore/fay-willows.lua`（`05a3f93c9f5cd5baf52429155fcd4a09b6045ef45fbf3472562d55f5da0e4c6f`）
   - 额外读取的单文件（来自 `dlc_additional_sources` 列明路径，经 SHA256 校验与 `source-access.json` 一致）：
     - `.../sources/cults/tome-cults/data/zones/maggot/zone.lua`（`dc41d3d14196e4c14d5b903ad14e3d15999464af0d0149b5be06869a76f168c5`）
     - `.../sources/cults/tome-cults/data/zones/maggot/npcs.lua`（`05a58af1f0a874ddee6305fdcaa971e790cfe06bca0c5e3f5a57836b2479e0a4`）

2. **额外源码路径的调用链来源**：
   - 由 entry-03493 原文实体描述中的专有名词 `the Maggot` 引入，为确认其属于地下城特定实体/巨型生物生态而非普通泛称，循调用链查验 `tome-cults/data/zones/maggot/` 之区域与生物定义。

3. **版本状态与机制适用性说明**：
   - 本组 40 条全部属于 `cults` DLC 组件，无本体源码依赖。
   - DLC 源码来源于 `source-access.json` 中已哈希固定的公开快照，未固定源码仓库及 commit。上述确认的事实均以该快照文件内容为准；本次确认的问题均属于文本语义严重失真、信息脱落、量词错误或明确适用的术语不符，不依赖未决的引擎与 DLC 目标版本间机制差异。

4. **合规确认**：
   - 全程保持只读，未修改仓库文件，未创建子 agent，未读取其他实验报告或外部模型输出。
   - 无无法核验事项，无越界访问行为。
   - 本输出为独立 REVIEWER 复核观察记录，不声称生产 `DONE_VERIFIED`。
