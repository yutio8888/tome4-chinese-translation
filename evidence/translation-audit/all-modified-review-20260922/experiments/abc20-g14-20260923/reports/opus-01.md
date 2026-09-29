# entry-03693–entry-03732 复核报告（REVIEWER，translation_contextual_v1，自然语言实验旁路）

40 条中：存在问题 4 条，待确认 1 条，仅建议 5 条，未发现问题 30 条。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03693 | 仅建议 | C01 |
| entry-03694 | 仅建议 | C02 |
| entry-03695 | 未发现问题 | 与 CultsDLC.lua:363 对应，攻击语义一致 |
| entry-03696 | 未发现问题 | FontSacrifice.lua:151/294 把它拼接在词缀名后，与说明文中的“高级词缀”一致 |
| entry-03697 | 存在问题 | C03；C04、C05 |
| entry-03698 | 未发现问题 | 注册、绑定、自动完成、报错四项信息都在；组件无源码 |
| entry-03699 | 待确认 | C06 |
| entry-03700 | 未发现问题 | %s 保留，补的“物品”无损 |
| entry-03701 | 未发现问题 | %s 与颜色标记保留 |
| entry-03702 | 未发现问题 | 语义完整 |
| entry-03703 | 未发现问题 | 同 03702 |
| entry-03704 | 未发现问题 | 成就名直译，忠实 |
| entry-03705 | 未发现问题 | 用括注区分职业与武器，没有新增信息错误 |
| entry-03706 | 未发现问题 | 术语“夏·图尔”一致，语义完整 |
| entry-03707 | 未发现问题 | 与 empyreal.lua:29/33 的 mag=6 一致 |
| entry-03708 | 未发现问题 | empyreal.lua:30 |
| entry-03709 | 未发现问题 | tinker.lua:74/121 的 life_rating=2 |
| entry-03710 | 未发现问题 | tinker.lua:132/139 |
| entry-03711 | 未发现问题 | tinker.lua:133/139 |
| entry-03712 | 未发现问题 | tinker.lua:134/186（Psyshot 与 Annihilator 也是 -1） |
| entry-03713 | 未发现问题 | tinker.lua:206/210 |
| entry-03714 | 未发现问题 | 本体天赋 ORC_FURY 的效果是泛指伤害加成 |
| entry-03715 | 未发现问题 | orc.lua:117/122 |
| entry-03716 | 未发现问题 | orc.lua:118/122 |
| entry-03717 | 未发现问题 | orc.lua:119/129 |
| entry-03718 | 未发现问题 | orc.lua:120/131 的 experience=1.12 |
| entry-03719 | 仅建议 | C07 |
| entry-03720 | 未发现问题 | whitehooves.lua:120/125 |
| entry-03721 | 未发现问题 | whitehooves.lua:121/125 |
| entry-03722 | 未发现问题 | whitehooves.lua:122/145 |
| entry-03723 | 未发现问题 | whitehooves.lua:123/148 的 experience=1.15 |
| entry-03724 | 未发现问题 | yeti.lua:106/111 |
| entry-03725 | 未发现问题 | yeti.lua:107/111 |
| entry-03726 | 未发现问题 | yeti.lua:108/128 |
| entry-03727 | 未发现问题 | yeti.lua:109/130 的 experience=1.12 |
| entry-03728 | 仅建议 | C08 |
| entry-03729 | 存在问题 | C09、C10、C11、C12；C13 |
| entry-03730 | 仅建议 | C14、C15 |
| entry-03731 | 存在问题 | C16；C17 |
| entry-03732 | 存在问题 | C18、C19、C20；C21 |

**关于“Magic”的译法（不计为 claim）：** 属性行里 Magic 译作“魔法”，术语快照写的是“魔力”。但快照状态是 existing，同目录所有出生描述也都统一用“魔法”。按输入规则第 1、5 条，这不构成改名依据，也不应扩大成全局术语问题，所以没有计入。

---

### C01 | entry-03693 | 仅建议
- **原文／译文：** “promptly swallows and eat Melinda” →“吃下了梅琳达”。
- **观察：** “promptly”（立刻）没有译出。
- **依据：** CultsDLC.lua:353。这是寄生兽模式下替换出来的对话选项，动作由 `good_meal()`（:337-344）执行：杀死 NPC，并加 1 点通用天赋点。选项本身描述的动作、对象、结果都没错，缺的只是语气副词，不影响玩家判断，所以只算建议。
- **旁证：** 同节相邻条目（Fillarel、yeek wayist）用的是“直接吃掉了”。

### C02 | entry-03694 | 仅建议
- 与 C01 相同，“promptly”没有译出。
- **依据：** CultsDLC.lua:358，`good_meal(self.chats.welcome.answers[3].action)`。结果信息没有损失。

### C03 | entry-03697 | 存在问题
- **原文／译文：** “a letter from Protector Myssil of Zigur” →“一份来自守护者米歇尔的信”。
- **问题：** “of Zigur”（伊格的）被整段删掉，寄信人的所属地丢了。
- **依据：** Game.lua:59-69，这是 `Dialog:simpleLongPopup` 弹出的信件正文。标题“Urgent affair in Zigur”虽然提到了伊格，但正文开头原本交代“来自伊格的守护者 Myssil”，这是身份和所属关系信息，不能靠标题让玩家自己推断。
- **状态：** 已证实（语境证据）。
- **其余部分核对无误：** %s（`p.name`）、`#{italic}#`、结尾换行都保留；Ziguranth 译“伊格兰斯”、Zigur 译“伊格”，都符合术语快照里的地点／教团区分。

### C04 | entry-03697 | 仅建议
- **原文／译文：** “From what the scouts can tell they were taken by…” →“侦察员看见他们被……带走”。
- **观察：** 原文是“据侦察员判断”的推断语气，译文变成了亲眼所见，确定性略有抬高。
- **为什么只算建议：** “被死灵法师带走”这个事实主张本身没错，后半句的“可能”也保留了，叙事信息没有实质改变。

### C05 | entry-03697 | 仅建议
- **原文／译文：** “grave news”→“令人震惊的消息”；“show the necromancers filth the True Wrath of the Ziguranth”→“让死灵法师见识一下伊格兰斯的愤怒”。
- **观察：** “grave”的意思是“严重”，不是“震惊”；贬称“filth”和强调词“True”都没译出。
- **为什么只算建议：** 这些都是语气和修辞层面的差别，行动对象和行动要求（解救、惩戒死灵法师）完整。

### C06 | entry-03699 | 待确认
- **原文／译文：** “This item has been sent to the Item's Vault.”→“已被上传到共享仓库”。
- **疑点：** 同节（ItemsVaultDLC.lua）同时有“online item's vault”和“offline item's vault”两套传输日志（见 context.lua 的同节 03700、03701）。如果这句提示也会出现在离线仓库的情形，“上传”（隐含上传到服务器）就不准确；原文“sent”是中性的。
- **缺的证据：** items-vault 列在 unavailable_components 中，看不到这句的调用点，也就无法确认它是否只在在线模式下出现。

### C07 | entry-03719 | 仅建议
- **原文／译文：** “- special whitehoof talents: dead hide, lifeless rush, essence drain” →“- 特殊白蹄天赋：亡者之皮，无生突袭，吸取精华。”
- **观察：** 译文末尾加了句号。同一列表里的其他项（context.lua 同节“- 沉默抗性”“- 流血免疫”等）都不带句号，只是格式不统一，不影响显示或信息。
- **未能核对：** 三个天赋名与天赋定义里的正式中文名是否一致。术语快照没有收录这三项，也不能读取其他翻译文件，所以没有列为 claim。

### C08 | entry-03728 | 仅建议
- **原文／译文：** “…#GOLD#蒸汽科技/物理#LAST#, #GOLD#蒸汽科技/化学#LAST#和两项…”
- **观察：** 中文句子里混用了半角逗号加空格，属于排版偏好。
- **已核对无误：** 占位符 %s（npc.name）和颜色标记都完整；aaf.lua:25-28/35 确实学习 steamtech/physics、steamtech/chemistry 两个技能类别，外加 T_SMITH、T_THERAPEUTICS 两个天赋，与“两项入门制造技能”一致；术语 steamtech、physics、chemistry 都匹配。

### C09 | entry-03729 | 存在问题
- **原文／译文：** “break down metallic items into lumps of metal” →“将金属物品转化为铁块”。
- **问题：** 原文是泛指的“金属块”，译文缩成了“铁”。
- **源码依据：** 提取仪的熔炼逻辑在 orcs 的 superload/mod/class/Actor.lua:299-302：`if o.metallic and o.material_level then local id = "LUMP_ORE"..o.material_level`。产出的矿块按物品材质等级分档，不是固定的铁。
- **状态：** 已证实（DLC 快照，来源未固定）。

### C10 | entry-03729 | 存在问题
- **原文／译文：** “…and infusions into herbs which are used to craft tinkers.” →“将纹身转化为植物。”
- **问题：** 用途从句“which are used to craft tinkers”（用于制造蒸汽配件）整句漏译，玩家看不到这些产物是做什么用的。
- **依据：** quest-artifacts.lua:28-29 的 APE 描述也写着“lumps of ore to server for the creation of tinkers”；Actor.lua:304-309 显示，熔炼纹身（infusion）后收集的是 `HERBS` 材料。
- **状态：** 已证实。

### C11 | entry-03729 | 存在问题
- **原文／译文：** “You will have to choose to use it or the Transmogrification Chest when you destroy items.” →“你可以选择使用它或者转化之盒。”
- **问题：** “when you destroy items”（在销毁物品时）这个适用场合被删掉，读者不知道这个选择是针对什么的；“will have to”（需要做出选择）也被弱化成“可以选择”。
- **依据：** quest-artifacts.lua:33-36 显示 APE 自带 `has_transmo`；:54-57 显示同时有两个销毁来源时（`has_transmo >= 2`）才弹出默认销毁器的选择。
- **状态：** 已证实。

### C12 | entry-03729 | 存在问题
- **原文／译文：** “You can choose the default one by using it with no items to destroy.” →“在里面没有物品时使用它则设置为默认使用。”
- **问题：** 译文把条件缩成了“盒子里没有物品”。
- **源码依据：** quest-artifacts.lua:45-60 的使用逻辑要求两个条件同时满足：背包里没有待熔物品（`nb <= 0`），并且脚下地面也没有物品（`floor == 0`），才会进入“设为默认销毁器”的弹窗。如果地面有物品，:62 会改为询问是否熔炼地面物品。原文“no items to destroy”覆盖了这两处。按译文操作的玩家，盒子是空的但脚下有物品时，会得到与译文不符的结果。
- **状态：** 已证实（DLC 快照，来源未固定）。

### C13 | entry-03729 | 仅建议
- “herbs”译作“植物”，“草药”更贴切。产物身份在 C10 已经列为问题，这里只是用词偏好。
- infusions 译“纹身”符合术语快照（infusions 对应“纹身”，existing），不算问题。

### C14 | entry-03730 | 仅建议
- **原文／译文：** “Several loyal Orcs are eagerly waiting” →“焦急地等待着你”。
- **观察：** “eagerly”偏向“热切、迫不及待”，“焦急”带有担忧色彩，情绪略有偏移。“焦急地等待”在中文里也常用来表达急切，所以没有列为错误。

### C15 | entry-03730 | 仅建议
- 原文说“'DESTRUCTICUS' is etched into one”（刻在其中一把钥匙上），译文“上面写着”没有交代是哪一把，“etched”（刻）也变成了“写”。
- 末句“You should probably head there right away!”译作“你应该马上过去*”，丢了“probably”和感叹号。
- **依据：** destructicus-lead.lua:21-23。这些都不改变剧情信息或玩家操作（下一步只有“Lead the way.”一个选项，:25-27），所以只算建议。术语“毁灭号”“克鲁克部落”一致，@playername@ 保留。

### C16 | entry-03731 | 存在问题
- **原文／译文：** “A strange beaded panel slides in front of you, … to display the outline of an airship” →“一块奇怪的珍珠板从你前方滑过”。
- **问题：** “slides in front of you”是面板滑到你面前停住；“从你前方滑过”是经过后离开。这与后文面板一直显示目标相矛盾，动作语义错误。
- **依据：** destructicus.lua:37 及后续 :44-50，“The beaded panel is suddenly awash with colors…”说明面板一直在玩家面前。
- **状态：** 已证实（语境证据）。

### C17 | entry-03731 | 仅建议
以下几处是措辞或细节损失，都不影响剧情理解和后续选择，所以只算建议：
- “whirrs to life”译作“启动了它的生命”，有翻译腔。
- “its base slightly rotating underneath you”译作“基座开始运转”，丢了“微微”和“在你身下”。
- “beaded”译作“珍珠”，更贴切的是“串珠／珠点”。
- “pins pushing out and pulling back”只译了“伸出”，漏了“缩回”。
- “magnetic force”译作“电磁力量”。

标记核对：`#{bold}#…#{normal}#`、`#{italic}#…#{normal}#` 都完整；“裂天者 毁灭号”符合术语备注。

### C18 | entry-03732 | 存在问题
- **原文／译文：** “a very lost and very confused Fire Imp, flying in the air near nothing of importance” →“在空中无害地飞舞”。
- **问题：** “near nothing of importance”（附近没有任何重要目标）被换成了“无害地”，位置信息丢失，主语属性也变了。原文紧接着说“Firing on it would have little effect whatsoever”，理由正是它附近空无一物；译文的因果依据因此偏移。
- **状态：** 已证实（destructicus.lua:50 的语境）。

### C19 | entry-03732 | 存在问题
- **原文／译文：** “Steam Giant families huddle and weep” →“蒸汽巨人们拥挤而哭泣”。
- **问题：** “families”没有译出。这一段描写的是撤离难民（紧接着是“Atmos Tribe 的残余”），“一家一家的蒸汽巨人”这一平民身份信息丢失；“huddle”（挤成一团）译作“拥挤”，也偏离了原意。
- **状态：** 已证实（destructicus.lua:46 的语境）。

### C20 | entry-03732 | 存在问题
- **原文／译文：** “a few crew members hurrying between the captain's quarters and the engine room” →“一些成员匆忙走过船长室和引擎室”。
- **问题：**
  - “crew members”（船员）被泛化成“成员”，身份丢失，容易和前文的难民混淆。
  - “between A and B”（在两处之间往返奔走）被改成“走过”两个房间，行动路径变了。
- **状态：** 已证实（destructicus.lua:46 的语境）。

### C21 | entry-03732 | 仅建议
以下几处不改变叙事信息，所以只算建议：
- 原文第 2 段与第 3 段之间有空行（源码是“ \n”行），译文中两段直接相连。只是少了一个段落空隔，不导致错误显示或信息结构丢失。
- 小鬼用了人称代词“他”，同文件其他段落用“它”。
- “The view pans around the cabin”译作“视角切换到船舱”，“pans around”（环视）的意思弱化了。

---

## 读取路径与越界说明

**冻结输入（只读）：** 目录 `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/` 下的：
- `INPUT.md`
- `entries.json`（只按字段看了结构和首条）
- `context.lua`
- `source-access.json`

**本组 sources：** 以下 13 个文件的 sha256 都与 `files_sha256` 一致。均为 DLC 快照，来源未固定（unpinned）。
- `sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua`
- `sources/dlc/cults/tome-cults/overload/mod/dialogs/FontSacrifice.lua`
- `sources/dlc/cults/tome-cults/superload/mod/class/Game.lua`
- `sources/dlc/orcs/tome-orcs/data/achievements/special.lua`、`story.lua`
- `sources/dlc/orcs/tome-orcs/data/birth/classes/empyreal.lua`、`tinker.lua`
- `sources/dlc/orcs/tome-orcs/data/birth/races/orc.lua`、`whitehooves.lua`、`yeti.lua`
- `sources/dlc/orcs/tome-orcs/data/chats/aaf.lua`、`destructicus-lead.lua`、`destructicus.lua`

**本体源码：**
- `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/talents/misc/races.lua`
- 引入原因：orc.lua:125 的 `ActorTalents.T_ORC_FURY`。
- 说明：该天赋是本体数据，所以用了引擎 commit。DLC 是否覆盖这个天赋没有核查，它在目标版本上是否适用待确认，但不影响 03714 的结论。

**DLC 追加来源（dlc_additional_sources.orcs，来源未固定，哈希已逐个比对一致）：**
- `.../abc20-20260923/sources/orcs/tome-orcs/data/general/objects/quest-artifacts.lua`：由 aaf.lua:55-57 的 `loadList("/data-orcs/general/objects/quest-artifacts.lua")` 和 `makeEntityByName(…, "APE")` 引入。
- `.../abc20-20260923/sources/orcs/tome-orcs/superload/mod/class/Actor.lua`：由 quest-artifacts.lua:68/81 调用的 `who:transmoInven(…, self)` 引入。orcs 在这个文件里重写了 `transmoInven`（:288-326）。

**不可核验：** items-vault 组件（03698–03703）没有源码，只按文本判断；C06 因此待确认。

**越界与其他：**
- 没有使用临时目录，也没有写任何文件。
- 没有读取当前翻译文件、其他实验材料、SPEC/STATE、历史报告或其他模型输出。
- 没有做整目录搜索，没有读取 locales。
- 没有已知越界。

以上是审核观察，不是最终事实；本报告不构成生产 DONE_VERIFIED。
