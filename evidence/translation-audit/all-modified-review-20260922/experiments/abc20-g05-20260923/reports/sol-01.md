已按冻结顺序复核 40 条。下表是独立审核观察；DLC 源码快照的仓库和 commit 未固定，涉及其运行机制的结论仍有目标版本适用性缺口。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03333 | 存在问题 | C01 |
| entry-03334 | 未发现问题 | 重启、语言切换及格式保留 |
| entry-03335 | 仅建议 | C02 |
| entry-03336 | 未发现问题 | 数量与对象相符 |
| entry-03337 | 未发现问题 | 三名对象及时序相符 |
| entry-03338 | 未发现问题 | 专名与标记相符 |
| entry-03339 | 未发现问题 | 专名相符 |
| entry-03340 | 未发现问题 | 属性数值相符 |
| entry-03341 | 未发现问题 | 属性数值相符 |
| entry-03342 | 未发现问题 | 生命加值相符 |
| entry-03343 | 未发现问题 | 属性数值相符 |
| entry-03344 | 未发现问题 | 生命加值相符 |
| entry-03345 | 存在问题 | C03–C06 |
| entry-03346 | 未发现问题 | 属性数值相符 |
| entry-03347 | 未发现问题 | 属性数值相符 |
| entry-03348 | 未发现问题 | 数值相符 |
| entry-03349 | 未发现问题 | 经验惩罚相符 |
| entry-03350 | 未发现问题 | 专名相符 |
| entry-03351 | 未发现问题 | 装备效果与既有技能名相符 |
| entry-03352 | 未发现问题 | 范围、伤害和治疗比例相符 |
| entry-03353 | 存在问题 | C07 |
| entry-03354 | 未发现问题 | 两项限制相符 |
| entry-03355 | 未发现问题 | 两项许可相符 |
| entry-03356 | 未发现问题 | 全豁免及比例相符 |
| entry-03357 | 未发现问题 | 法术强度及比例相符 |
| entry-03358 | 存在问题 | C08 |
| entry-03359 | 未发现问题 | 移动速度及比例相符 |
| entry-03360 | 未发现问题 | 译文沿袭原文的半数表述 |
| entry-03361 | 存在问题 | C09 |
| entry-03362 | 未发现问题 | 物理强度及比例相符 |
| entry-03363 | 存在问题 | C10 |
| entry-03364 | 存在问题 | C11 |
| entry-03365 | 未发现问题 | 长篇叙事及标记未见可证译文缺陷 |
| entry-03366 | 存在问题 | C12–C13 |
| entry-03367 | 未发现问题 | 标题及职业名相符 |
| entry-03368 | 未发现问题 | 标题及职业名相符 |
| entry-03369 | 未发现问题 | 标题及种族名相符 |
| entry-03370 | 未发现问题 | 标题相符 |
| entry-03371 | 存在问题 | C14–C18 |
| entry-03372 | 存在问题 | C19–C20 |

下列源码路径均相对于冻结包 `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/`。

### C01 | entry-03333 | 存在问题

原文“upload **your addon** directly from here”译为“你可以直接在这里上传”，省去上传对象及“你的”所属关系。即使能从插件开发界面猜出对象，操作说明仍丢失了原文明确的信息。此项只据冻结原译文本判断；addon-dev 源码不可用。

### C02 | entry-03335 | 仅建议

“将翻译文件拷贝去的插件”能表达目标插件，“拷贝去”只是搭配不够自然；没有可证的信息错误。

### C03 | entry-03345 | 存在问题

原文“one fights for the third **with the cultists she taught**”译为“召集邪徒**为复活另一者**而战”。译文加入原句未说明的“复活”目的，并丢失“她教导的邪徒”这一关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:27–32`，`locked_desc`。

### C04 | entry-03345 | 存在问题

原文“**Silence these beings**”译为“静默**他们的声音**”，将处理三个存在本身改成处理声音。相邻成就要求杀死三名恶魔，达成后解锁 Doomelf；这里的解锁提示具有操作含义。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:31–32`；`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/achievements/all.lua:84–107`，`ASHES_OLD_ONES.can_gain/on_gain`。

### C05 | entry-03345 | 存在问题

原文“**maintain your deception**”译为“**隐藏你的踪影**”。维持伪装或欺骗与隐藏行踪不是同一行为。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:31`，`locked_desc`。

### C06 | entry-03345 | 存在问题

原文“**may witness** a new elf’s **conception**”译为“新的精灵**终将诞生**”：可能见证孕育变成必然出生，条件与阶段均改变。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:32`，`locked_desc`。

### C07 | entry-03353 | 存在问题

原文“resistances **shift over time**”译为“依据……改变……免疫”，漏掉逐渐调整的时序。快照中的装备 `act` 每次按当前状态从其他免疫值挪移小额数值，并非一次切换完成。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:315–427`，`Revenant.act`。目标版本是否使用此未固定 DLC 快照待确认。

### C08 | entry-03358 | 存在问题

原文“**all** damage penetration”译为“抗性穿透”，未说明覆盖全部伤害类型。该装备写入的是穿透表的 `all` 项。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:679–682`，`The Black Spike.on_obsidian_power_update`。目标版本适用性待确认。

### C09 | entry-03361 | 存在问题

原文“**Wreckage all about you. Is there anything left inside?**”描写周围残骸，并追问里面是否还有东西；译文“**己身若残，何物能存？**”改成自身残损后的存亡判断，丢失周围残骸与内外关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:740–744`，`The Black Plate.desc`。

### C10 | entry-03363 | 存在问题

原文“**all damage**”是佩戴者所有类型的伤害；“**全体伤害加成**”易指全体成员的伤害加成，改变受益范围。效果实际写在本装备的 `wielder.inc_damage.all`。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:813–816`，`The Black Maul.on_obsidian_power_update`。目标版本适用性待确认。

### C11 | entry-03364 | 存在问题

原文“**all resists**”对应佩戴者的 `resists.all`；“**全体抗性**”易表示全体成员的抗性，且冻结术语子集对这一属性给出“**全部抗性**”。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:854–857`，`The Black Wall.on_obsidian_power_update`；`INPUT.md` 术语子集 `All Resists`。目标版本适用性待确认。

### C12 | entry-03366 | 存在问题

原文“**standard-issue alteration**”译为“**标准化思维修改**”，凭空限定为思维修改。同一冻结源码描述的标准改造还影响短距离传送和内脏避让，不能据此限缩为思维。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:135,189–191`，`training-recall2` 及 `tactics-doomelf` 的叙述。

### C13 | entry-03366 | 存在问题

原文“hold your arms like this so I can get the **bindings** in place”译为“举起胳膊，这样我就能把**它**放好”，省掉即将装上的束缚物，削弱这段记忆中受制于人的关键信息。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:133–137`，`training-recall2.lore`。

### C14 | entry-03371 | 存在问题

原文“**Blow all connectors**”译为“**关闭所有链接传送门**”。前者要求炸断连接结构；与下一句“把平台从大陆分离”相连。译文改成关闭传送门，改变了命令对象及动作。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:226`，`tactics-failed-badass.lore`；普通版本的同一命令见该文件 `:210`。

### C15 | entry-03371 | 存在问题

原文“the pen was rapidly **jerked away**”译为“笔**从手上滑落**”，把快速被扯开改成失手滑落，改变笔迹产生的动作。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`，`tactics-failed-badass.lore`。

### C16 | entry-03371 | 存在问题

原文“**double-bladed katana**”仅译“武士刀”，丢失双刃特征。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`。

### C17 | entry-03371 | 存在问题

原文对手是标作“Ninja Atamathon”的“**giant construct**”；译文仅作“**忍者王阿塔玛森**”，漏掉巨型构装体身份，并加入原文没有的“王”。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`；`INPUT.md` 术语子集对构装实体给出“构装体”。

### C18 | entry-03371 | 存在问题

原文“Your badassery must have **interrupted this demon’s writing**”译为“你的霸气侧漏把这个恶魔**吓尿了**”。原文能确定的是书写被打断；译文删去这一事件并加入惊吓反应。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`。

### C19 | entry-03372 | 存在问题

原文“dissolving **the ground they walk on**”译为“溶解土地”，漏掉被溶解的是敌人脚下的地面，弱化了酸液树魔攻击对象的空间关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:291–295`，`demon-statue-wretchling.lore`。

### C20 | entry-03372 | 存在问题

原文“their acid and **our casters** do their work”译为“令酸液和**法术**能够发挥作用”。己方施法者被改成法术，参与战斗的单位及所属关系丢失。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:295`，`demon-statue-wretchling.lore`。

**读取范围与限制：**读取了冻结包的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `source-access.json.sections` 指定的六个 Ashes 源码单文件：`achievements/all.lua`、`birth/corrupted.lua`、`birth/doomelf.lua`、`general/grids/demon_statues.lua`、`general/objects/world-artifacts.lua`、`lore/demon.lua`；六个文件的 SHA-256 均与清单一致。按 `achievements/all.lua:87–95` 的恶魔名称，另对清单允许的 `data/general/npcs/major-demon.lua` 做了哈希校验及限定词搜索；按 `world-artifacts.lua:80,90,102` 的 `Obliterating Smash` 符号，另对允许的 `data/talents/corruptions/brutality.lua` 做了相同检查。两次搜索均未命中，未据它们形成结论。未读取引擎仓库，未读取其他报告或模型输出，未创建临时文件，未修改仓库。

**越界记录：**开始时曾对冻结包目录执行一次 `ls`，看到了若干未获准读取的文件及目录名称；没有打开其内容。addon-dev 在清单中列为源码不可用。以上仅为审核观察，不声称生产 `DONE_VERIFIED`。
