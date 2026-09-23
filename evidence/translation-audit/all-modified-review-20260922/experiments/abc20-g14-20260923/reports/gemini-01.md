## 40条译文复核判定表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03693 | 仅建议 | C01 |
| entry-03694 | 仅建议 | C02 |
| entry-03695 | 未发现问题 | 术语、行为主体与标点准确，无信息遗漏 |
| entry-03696 | 未发现问题 | 词缀分类与前导空格格式完整，与界面渲染逻辑相符 |
| entry-03697 | 存在问题 | C03, C04 |
| entry-03698 | 未发现问题 | 前导换行、高亮标签及跨平台账号绑定说明准确 |
| entry-03699 | 未发现问题 | 格式标签与仓库上传提示一致 |
| entry-03700 | 未发现问题 | 占位符消费正确，在线传输失败日志语义完整 |
| entry-03701 | 未发现问题 | 占位符消费正确，离线传输日志语义完整 |
| entry-03702 | 未发现问题 | 仓库冷却限制提示准确，语义完整 |
| entry-03703 | 未发现问题 | 离线仓库冷却限制提示准确，语义完整 |
| entry-03704 | 仅建议 | C05 |
| entry-03705 | 未发现问题 | 职业与武器同名消歧准确，格式无误 |
| entry-03706 | 未发现问题 | 专名夏·图尔与阿马克泰尔准确，剧情成就表述无误 |
| entry-03707 | 未发现问题 | 职业属性加值数值与名称准确，逗号规范 |
| entry-03708 | 未发现问题 | 每等级生命加值标签与格式正确 |
| entry-03709 | 未发现问题 | 职业生命加值数值与标点规范 |
| entry-03710 | 未发现问题 | 属性加值数值与名称准确，全角标点一致 |
| entry-03711 | 未发现问题 | 属性加值数值与名称准确，全角标点一致 |
| entry-03712 | 未发现问题 | 负生命加值数值与格式标签准确 |
| entry-03713 | 未发现问题 | 属性修正数值与名称准确，正确对应原文 |
| entry-03714 | 仅建议 | C06 |
| entry-03715 | 未发现问题 | 兽人种族属性加值数值准确，全角标点一致 |
| entry-03716 | 未发现问题 | 兽人种族负魔力与正属性修正数值准确 |
| entry-03717 | 未发现问题 | 种族生命成长数值与标签格式准确 |
| entry-03718 | 未发现问题 | 经验惩罚百分比数值与标签格式准确 |
| entry-03719 | 未发现问题 | 白蹄种族三大专属天赋名称准确 |
| entry-03720 | 未发现问题 | 种族属性修正数值与正负号准确 |
| entry-03721 | 未发现问题 | 种族属性修正数值与正负号准确 |
| entry-03722 | 未发现问题 | 种族生命成长数值与标签格式准确 |
| entry-03723 | 未发现问题 | 经验惩罚百分比数值与标签格式准确 |
| entry-03724 | 未发现问题 | 雪人种族属性修正数值准确 |
| entry-03725 | 未发现问题 | 雪人种族属性修正数值与正负号准确 |
| entry-03726 | 未发现问题 | 雪人生命成长数值与标签格式准确 |
| entry-03727 | 未发现问题 | 经验惩罚百分比数值与标签格式准确 |
| entry-03728 | 未发现问题 | 占位符、格式代码及蒸汽科技两系名称准确 |
| entry-03729 | 存在问题 | C07, C08, C09, C10 |
| entry-03730 | 存在问题 | C11, C12 |
| entry-03731 | 存在问题 | C13, C14, C15 |
| entry-03732 | 存在问题 | C16, C17, C18 |

---

## 详细观察记录

### C01 | entry-03693 | 仅建议
- **短引**：原文 `#CRIMSON#[The parasite is hungry and promptly swallows and eat Melinda].` / 译文 `#CRIMSON#[寄生兽很饿，吃下了梅琳达]。`
- **内容与偏好说明**：原文中副词 `promptly`（迅速地/毫不犹豫地/直接）在译文中略去未直译，译文“吃下了梅琳达”虽准确表达了吞噬梅琳达的动作与叙事结局，但在对话分支语气上建议可补充“迅速/直接”（如“迅速吃下了梅琳达”），以更完整体现动作的时效紧迫感；此处不改变游戏机制与主旨信息，属措辞偏好。
- **状态**：仅建议
- **语境证据**：`CultsDLC.lua:353`，对话分支选项文本。

### C02 | entry-03694 | 仅建议
- **短引**：原文 `#CRIMSON#[The parasite is hungry and promptly swallows and eat Aeryn].` / 译文 `#CRIMSON#[寄生兽很饿，吃下了艾琳]。`
- **内容与偏好说明**：与 C01 同理，原文 `promptly` 未直接体现，当前译文已达意且信息无损，建议可酌情体现“迅速/立刻”，属措辞偏好。
- **状态**：仅建议
- **语境证据**：`CultsDLC.lua:358`，对话分支选项文本。

### C03 | entry-03697 | 存在问题
- **短引**：原文 `a letter from Protector Myssil of Zigur:` / 译文 `一份来自守护者米歇尔的信：`
- **问题具体内容**：遗漏关键所属地名修饰语 `of Zigur`（伊格的）。米歇尔作为反魔阵营与伊格据点的领袖，其完整头衔与据点指称在信首介绍中至关重要；译文完全漏掉了“伊格的”这一地点/阵营属性。
- **状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/superload/mod/class/Game.lua:59`（DLC公开快照，源码未固定），`Dialog:simpleLongPopup` 触发克罗格营救任务弹窗，信件开头为身份与任务背景交待。

### C04 | entry-03697 | 存在问题
- **短引**：原文 `show the necromancers filth the True Wrath of the Ziguranth!` / 译文 `并让死灵法师见识一下伊格兰斯的愤怒！`
- **问题具体内容**：原文中的名词同位语/定语 `filth`（这些污秽之徒/肮脏的败类）被漏译；此外，修饰教团之怒的定语 `True`（真正的愤怒）亦被漏译，弱化了反魔护卫长对奥术/死灵邪祟的极端憎恶情绪与文本强烈语气。
- **状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/superload/mod/class/Game.lua:66`（DLC公开快照，源码未固定）。

### C05 | entry-03704 | 仅建议
- **短引**：原文 `Once Upon A Time, In the West...` / 译文 `很久很久以前，在西方……`
- **内容与偏好说明**：该成就名与同文件中相邻的一组成就（A Fistful of Gold、For a Few Gold More、The Good, The Bad, and The Yeti）共同致敬著名导演莱昂内的经典西部镖客电影。原文直接化用电影名 *Once Upon a Time in the West*（中文通译《西部往事》）。当前译文采用字面直译在文意上完全成立且通顺，但若能考虑电影片名双关译作《西部往事……》会更具双关趣味；这仅属文化引用风格偏好，字面直译不计作缺陷。
- **状态**：仅建议
- **语境证据**：`dlc/orcs/tome-orcs/data/achievements/special.lua:136`（DLC公开快照，源码未固定）。

### C06 | entry-03714 | 仅建议
- **短引**：原文 `increase all their damage for a few turns.` / 译文 `让他们能在几回合内增加伤害。`
- **内容与偏好说明**：原文 `all their damage` 强调提升“所有造成的伤害”（全类型伤害加成），译文略化为“增加伤害”。在种族天赋特性描述中，虽然语义可大致理解，但建议补充“所有”，更精确地对齐游戏底层机制。
- **状态**：仅建议
- **源码依据**：`dlc/orcs/tome-orcs/data/birth/races/orc.lua:115` 与 `[ActorTalents.T_ORC_FURY]` 效果消费逻辑。

### C07 | entry-03729 | 存在问题
- **短引**：原文 `which are used to craft tinkers.` / 译文 `（整句漏译）`
- **问题具体内容**：严重漏译核心功能目的定语从句。原文解释将物品分解为金属块和药草的目的即为“这些材料用于制造蒸汽配件（tinkers）”，译文在“将纹身转化为植物”之后戛然而止，完全丢失了提取材料是为了制作配件这一最关键的引导性信息。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:42`（DLC公开快照，源码未固定），对话叙述便携提取仪（APE）的核心作用。

### C08 | entry-03729 | 存在问题
- **短引**：原文 `when you destroy items.` / 译文 `（从句漏译）`
- **问题具体内容**：漏译关键条件状语 `when you destroy items`（在摧毁/分解物品时）。原文指明玩家必须在摧毁物品的特定场景下二选一（便携提取仪或转化之盒），译文漏译后变成了“你可以选择使用它或者转化之盒”，丢失了该选择生效的前提条件。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:44`（DLC公开快照，源码未固定）。

### C09 | entry-03729 | 存在问题
- **短引**：原文 `metallic items into lumps of metal and infusions into herbs` / 译文 `将金属物品转化为铁块，将纹身转化为植物`
- **问题具体内容**：术语与词义严重不准。
  1. `herbs` 误译为泛化的“植物”（实为用于调配注射药剂的“药草/草药”）；
  2. `lumps of metal` 错误窄化为“铁块”。在游戏机制中，提取仪分解金属物品产出的是对应材质阶级的各级金属块（如钢铁、矮人钢、沃瑞钽等），绝不仅限于生铁块。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:42` 以及 `dlc/orcs/tome-orcs/data/general/objects/quest-artifacts.lua:28-30` APE 描述。

### C10 | entry-03729 | 存在问题
- **短引**：原文 `You can choose the default one by using it with no items to destroy.` / 译文 `在里面没有物品时使用它则设置为默认使用。`
- **问题具体内容**：机制理解错误导致误导性翻译。便携提取仪（APE）是背包中的可使用任务道具（并非带内部格子的容器），其底层逻辑是检测当前背包或地面是否有待分解物品：若背包和地面均无物品，则弹出确认框将 APE 设为默认转化工具。译文“在里面没有物品时使用它”让玩家误以为该道具内部有储物空间且需要先清空内部，造成操作认知偏差。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:44`；额外引入源码 `dlc/orcs/tome-orcs/data/general/objects/quest-artifacts.lua:45-56` 的 `use` 逻辑：`if nb <= 0 then local floor = ... if floor == 0 then yesnoPopup(_t"Make the Automated Portable Extractor the default item's destroyer?")`。

### C11 | entry-03730 | 存在问题
- **短引**：原文 `You should probably head there right away!*#WHITE#` / 译文 `你应该马上过去*#WHITE#`
- **问题具体内容**：句末标点符号丢失。原文以感叹号 `right away!` 结尾，译文在闭合星号与颜色标签前未加任何标点符号（漏译感叹号 `！`），导致叙事对话句式残缺。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:22`（DLC公开快照，源码未固定）。

### C12 | entry-03730 | 存在问题
- **短引**：原文 `Several loyal Orcs are eagerly waiting ... The word 'DESTRUCTICUS' is etched into one.*` / 译文 `数名忠诚的兽人在宫殿外焦急地等待着你；其中一名兽人走上前，交给你一串钥匙，上面写着“毁灭号”。*`
- **问题具体内容**：
  1. 原文 `eagerly waiting`（热切地/迫不及待地等待）被误译为“焦急地等待”（焦虑担忧），扭曲了兽人士兵急于向酋长展示缴获巨炮钥匙的兴奋与忠诚态度；
  2. 原文 `etched into one` 明确指出字样是“刻在其中一把钥匙上”，译文概括为“交给你一串钥匙，上面写着“毁灭号””，丢失了刻在特定钥匙上的对象所属与雕刻事实。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:20`（DLC公开快照，源码未固定）。

### C13 | entry-03731 | 存在问题
- **短引**：原文 `whirrs to life, its base slightly rotating underneath you.` / 译文 `启动了它的生命，它的基座开始运转。`
- **问题具体内容**：机器描写严重机翻化与细节遗失。
  1. `whirrs to life` 是英语中描述机械“发出嗡鸣声运转/启动”的常见习语，被生硬直译为“启动了它的生命”；
  2. `its base slightly rotating underneath you`（其底座在你身下微微旋转）被笼统译为“它的基座开始运转”，丢失了“在你身下”的位置关系与“微旋调整”的动作细节。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。

### C14 | entry-03731 | 存在问题
- **短引**：原文 `A strange beaded panel slides in front of you` / 译文 `一块奇怪的珍珠板从你前方滑过`
- **问题具体内容**：空间方位与显示设备描述错误。
  1. `slides in front of you` 是指操作台面板滑动移至玩家面前就位（以便后续观察锁定目标），误译为“从你前方滑过”（滑走/掠过），造成动作与后续使用逻辑冲突；
  2. `beaded panel` 结合后文的电磁推拉针阵成像机制，指珠状/凸点针阵式显示屏，误译为“珍珠板”（像珍珠饰品板）。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。

### C15 | entry-03731 | 存在问题
- **短引**：原文 `pins pushing out and pulling back by magnetic force` / 译文 `针伸了出来，被电磁力量控制`
- **问题具体内容**：关键机械动作漏译。针阵显示屏的原理是通过电磁力推起和拉回（pushing out and pulling back）细针来构成三维轮廓，译文仅译出“针伸了出来”，完全漏译了“回缩/拉回”（pulling back），破坏了动态针阵成像的完整运作描写。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。

### C16 | entry-03732 | 存在问题
- **短引**：原文 `flying in the air near nothing of importance.` / 译文 `在空中无害地飞舞。`
- **问题具体内容**：严重错译与信息替换。原文 `near nothing of importance` 指该火焰小鬼在一片无关紧要的空域飞行（周围没有任何重要目标），译者误将后一句的 `harmless`（以最无害的方式炫耀力量）提前捏造并替换成了“无害地飞舞”，导致原文关于目标所处空旷环境的事实信息完全丢失。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:54`（DLC公开快照，源码未固定）。

### C17 | entry-03732 | 存在问题
- **短引**：原文 `a few crew members hurrying between the captain's quarters and the engine room` / 译文 `你看见一些成员匆忙走过船长室和引擎室`
- **问题具体内容**：身份与动作关系描述失真。
  1. `crew members` 指“船员”，被模糊译为“成员”；
  2. `hurrying between A and B` 指“在船长室与轮机室之间匆忙奔波往返”，被错误理解为“走过船长室和引擎室”，改变了船员在飞船关键舱室间来回调度的动作关系。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:50`（DLC公开快照，源码未固定）。

### C18 | entry-03732 | 存在问题
- **短引**：原文 `at you.\n \nThis airship appears` / 译文 `看向你。\n飞船似乎正在疏散`
- **问题具体内容**：段落结构丢失。英文原文在第2段（舱内众生相细节描写）与第3段（玩家的战略定性与灭族按钮抉择）之间设计了空行分割（`\n \n`）。译文仅以单个换行相连，导致第2段与第3段在界面排版中紧密粘连，丢失了文本原有的叙事停顿与视觉层次结构。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:50-52`（DLC公开快照，源码未固定）。

---

## 核验路径与环境记录

1. **实际读取的文件及版本/哈希**：
   - 入口文件：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/INPUT.md`
   - 依赖清单：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/source-access.json`
   - 冻结条目：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/entries.json`
   - 语境上下文：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/context.lua`
   - 本组 DLC 源码文件（公开快照，源码仓库/commit未固定，哈希已核验）：
     - `sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua` (`80e2fe3b8550f162cc04e60212746897864394741074dda096ce4c2a89c67bcd`)
     - `sources/dlc/cults/tome-cults/overload/mod/dialogs/FontSacrifice.lua` (`d599bf6b283a9055f6cf24fc811eb58ef7fcb95aeb11ad22862aa163339b2b3c`)
     - `sources/dlc/cults/tome-cults/superload/mod/class/Game.lua` (`765df32782249dfb0d2db6a80a30c81052b40494456332815d95052ee0aef008`)
     - `sources/dlc/orcs/tome-orcs/data/achievements/special.lua` (`8d66841101e7d248caa48d7a7ffe8ec7c442139f1e2ace345d830b1fd7c512ed`)
     - `sources/dlc/orcs/tome-orcs/data/achievements/story.lua` (`7e784faf8140f6280c5c96543540e676d9e43e28c75c48d548be55e781da36bd`)
     - `sources/dlc/orcs/tome-orcs/data/birth/classes/empyreal.lua` (`b43c98aa728096cddd9c21b110f01062d2257111f64d3c35671a4015d5ede716`)
     - `sources/dlc/orcs/tome-orcs/data/birth/classes/tinker.lua` (`861b8e9bc8ff8ccb64a86a5f9b62f38ac654854a78f4f4004bdc0dace84aecda`)
     - `sources/dlc/orcs/tome-orcs/data/birth/races/orc.lua` (`ca16dcf53d966d9370f0d8eb4ce2be7274baa4a529a2dd53047b1cdbea357349`)
     - `sources/dlc/orcs/tome-orcs/data/birth/races/whitehooves.lua` (`cd8b76bbf482ee7fee50bb8f725a37bc6312ac1f9620f15870f3fa59a8e32249`)
     - `sources/dlc/orcs/tome-orcs/data/birth/races/yeti.lua` (`7b14b94d81eee194a0cba526ad44af8153d9d1a20a4f2786faf36b9ef9a44718`)
     - `sources/dlc/orcs/tome-orcs/data/chats/aaf.lua` (`d69c885524b0d58c49d7155f0df83041452feb5c9d89befe6ec04a42ea9a7725`)
     - `sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua` (`7993d608092641c94db0e1d037ab97ed6ddb21ecd6c7296f932b7d777a044d6c`)
     - `sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua` (`ecf3e77e122a0e3b8321f71ad93355fa284519c4dcb24cba23b50ab05524fc98`)
   - 源码缺失组件：`items-vault` 在 `source-access.json` 中标记为 `unavailable`，复核严格基于对话/日志上下文与格式本身核验，未作任何同名代码越界假设。

2. **额外调用链源码路径引入说明**：
   - 路径：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/orcs/tome-orcs/data/general/objects/quest-artifacts.lua`（哈希：`176a9edc178cbefa9ac3dfa0c9baa05079ebf85d79d1e89fc7a5b1d9ca3f8dfc`，与 `source-access.json` 中 `dlc_additional_sources.orcs` 完全匹配）。
   - 引入调用链来源：`sources/dlc/orcs/tome-orcs/data/chats/aaf.lua:49` 显式调用 `require("mod.class.Object"):loadList("/data-orcs/general/objects/quest-artifacts.lua")` 以加载并赋予玩家任务神器 APE。为核实 entry-03729 中 APE 是否具有内部格子以及“无物品可摧毁时使用”的底层弹窗与默认设置逻辑，单文件读取该道具定义中的 `use_power` 实现。

3. **专属临时目录处理**：
   - 本次复核在仓库外使用用户许可创建的任务专属临时目录 `/tmp/abc20-g14-20260923-spga1unu`。
   - 临时目录仅用于暂存 40 条记录的提取对比纯文本文件，未读取他人材料，且在生成最终输出前已全部安全删除清理完毕。

4. **合规与越界声明**：
   - 全过程未读取任何当前翻译文件、未读取 SPEC/STATE/PLAN/BASELINE、未读取历史或其他实验臂的报告与比对评分，未创建任何子 agent，未修改仓库文件。
   - 无任何越界行为。本报告为独立只读 REVIEWER 审核观察，不代表真值，不宣称 DONE_VERIFIED。
