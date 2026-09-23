以下是对冻结输入 `entry-03453` 至 `entry-03492` 的独立复核观察。表中每条均按冻结顺序列出；“存在问题”只表示至少有一项可直接核验的译文问题，不表示整条译文均有误。

| 完整 entry-ID | 四类判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03453 | 未发现问题 | `%s` 的指向及爆炸位置相符 |
| entry-03454 | 存在问题 | C01、C02：身体部位及伤害程度 |
| entry-03455 | 存在问题 | C03–C09、C11；另有待确认 C10 |
| entry-03456 | 存在问题 | C12、C13：看管关系及陨石致死方式 |
| entry-03457 | 未发现问题 | 解锁标题在本组语境下可理解 |
| entry-03458 | 存在问题 | C14–C16：教派、能力范围及对象 |
| entry-03459 | 未发现问题 | 种族名相符 |
| entry-03460 | 存在问题 | C17、C18：增添烈火、改变解锁结果 |
| entry-03461 | 未发现问题 | 装备属性标签相符 |
| entry-03462 | 未发现问题 | 成就条件相符 |
| entry-03463 | 未发现问题 | 属性及数值相符 |
| entry-03464 | 未发现问题 | 属性及数值相符 |
| entry-03465 | 未发现问题 | 忠实对应冻结英文及数值 |
| entry-03466 | 未发现问题 | 忠实对应冻结英文及数值 |
| entry-03467 | 未发现问题 | 属性及数值相符 |
| entry-03468 | 未发现问题 | 属性及数值相符 |
| entry-03469 | 未发现问题 | 忠实对应冻结英文及数值 |
| entry-03470 | 未发现问题 | 百分比相符 |
| entry-03471 | 未发现问题 | 属性及数值相符 |
| entry-03472 | 未发现问题 | 属性及数值相符 |
| entry-03473 | 未发现问题 | 忠实对应冻结英文及数值 |
| entry-03474 | 未发现问题 | 百分比相符 |
| entry-03475 | 仅建议 | C19：成长潜力的措辞 |
| entry-03476 | 未发现问题 | 对话意图相符 |
| entry-03477 | 未发现问题 | 回答符合前后对话 |
| entry-03478 | 存在问题 | C20：滚出变为掉出 |
| entry-03479 | 存在问题 | C21：冲出变为掉出 |
| entry-03480 | 未发现问题 | 烟雾及触发时点相符 |
| entry-03481 | 存在问题 | C22：搜得可用物变为找遍东西 |
| entry-03482 | 未发现问题 | 点数、参数及标记相符 |
| entry-03483 | 未发现问题 | 点数、参数及标记相符 |
| entry-03484 | 未发现问题 | 点数、参数及标记相符 |
| entry-03485 | 未发现问题 | 点数、参数及标记相符 |
| entry-03486 | 未发现问题 | 点数、参数及标记相符 |
| entry-03487 | 未发现问题 | 控制球无响应的意思相符 |
| entry-03488 | 未发现问题 | 门的状态和玩家判断相符 |
| entry-03489 | 未发现问题 | 门的状态和玩家判断相符 |
| entry-03490 | 未发现问题 | 门的状态和玩家判断相符 |
| entry-03491 | 未发现问题 | 防御细胞的描述相符 |
| entry-03492 | 未发现问题 | 攻击细胞的行动与目的相符 |

下列源码行号均指哈希核对通过的 DLC 冻结快照。`A/` 代表本包 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/`，`C/` 代表 `sources/dlc/cults/tome-cults/`。这两个 DLC 快照的源码仓库和 commit 均未固定。

### C01 | entry-03454 | 存在问题

原文“**3 arms**”，译文“三只手”。`A/data/zones/searing-halls/npcs.lua:71–73` 将这句话用作恶魔的实体描述。*Arm* 指手臂，“三只手”只明确了手的数量，改变了描述的身体部位。状态：文本确认。

### C02 | entry-03454 | 存在问题

原文“**mutilate you**”，译文“切割你”。同一实体描述中的 *mutilate* 表示严重伤残、毁损身体；“切割”仅表示切开动作，丢失伤残程度。证据同 `A/data/zones/searing-halls/npcs.lua:73`。状态：文本确认。

### C03 | entry-03455 | 存在问题

原文两处均为“**Fearscape**”；译文在开头写“恐惧空间”，介绍新地区时写“恶魔空间”。同一段 DLC 介绍把同一地点呈现为两个名称，削弱了指代关系。见 `A/init.lua:28、33` 及冻结译文；术语子集也记录了“恶魔空间”，但此项依据是**本条内部不一致**，并非仅凭 `existing` 状态强制改名。状态：文本确认。

### C04 | entry-03455 | 存在问题

原文“barrier … crack **under their scrutiny**”，译文“在他们的**破坏**下开始破碎”。原文说屏障在恶魔的审视、探究下出现裂缝；译文改成了明确的主动破坏行为。见 `A/init.lua:28`。状态：文本确认。

### C05 | entry-03455 | 存在问题

原文“survive the **ensuing stresses**”，译文“在恶魔的**拷问**中存活”。前者泛指随后承受的压力或折磨，后者限定为恶魔施加拷问；原文这一处没有给出该限定。见 `A/init.lua:28`。状态：文本确认。

### C06 | entry-03455 | 存在问题

原文“fighting against **overwhelming odds**”，译文“与**势不可挡的敌人**战斗”。原文强调寡不敌众或胜算悬殊；译文把悬殊局势说成敌人本身不可阻挡。见 `A/init.lua:31`。状态：文本确认。

### C07 | entry-03455 | 存在问题

原文“**demon-cursed minotaur**”，译文“恶魔牛头人”。译文未传达牛头人**受到恶魔诅咒**的关系，读者会将其理解为恶魔种类。见 `A/init.lua:32`。状态：文本确认。

### C08 | entry-03455 | 存在问题

原文“a **squad of Fire Imps**”，译文“火焰恶魔”。*Imp* 的具体种类和 *squad* 的成队数量均消失，只剩宽泛的恶魔称呼。见 `A/init.lua:32`；已读的 `A/overload/mod/class/DemonologistsDLC.lua:105–109` 也明确使用 `fire imp` 名称。状态：文本及快照内名称确认。

### C09 | entry-03455 | 存在问题

同句原文“**pelt your enemies to death**”，译文“将敌人**烧成灰烬**”。原文描述连续投射攻击，译文改成燃尽的结果，改变了攻击方式的呈现。见 `A/init.lua:32`。状态：文本确认；不据此推断实际伤害类型。

### C10 | entry-03455 | 待确认

原文“Demons have **persistent health**”，译文“恶魔具有**更持久的生命值**”。译文易被读成恶魔生命值更多或更耐打；原文更像指生命状态能够持续保留。已读 `A/data/talents/corruptions/corruptions.lua:93–106` 的 `setupDemonSummon` 会复用恶魔对象并清除 `dead`，但所读调用链尚不足以确认完整的生命值保存、死亡和再召唤规则；DLC 目标版本也未固定。状态：待确认，缺召唤对象存取与再次召唤时生命值处理的完整调用证据。

### C11 | entry-03455 | 存在问题

原文“**metaphorical skulls** from your profile page”，译文“将他们的**头骨悬挂**在个人页面上”。原文特意说明“头骨”是比喻；译文呈现为字面展示物，改变了成就陈列的含义。见 `A/init.lua:40`。状态：文本确认。

### C12 | entry-03456 | 存在问题

原文“your **handler**”，译文“你的‘**主人**’”。这里的人负责带领、看管玩家；“主人”增添了所有权关系。见 `A/overload/data/texts/intro-ashes-urhrok.lua:25`。状态：文本确认。

### C13 | entry-03456 | 存在问题

原文说陨石“**lands near you**”，并使看管者当场死亡；译文说“它落在你身边，**砸死**了你的‘主人’”。“砸死”指定直接撞击致死，而原文仅给出附近着陆、冲击波及死亡，没有指定直接砸中。见 `A/overload/data/texts/intro-ashes-urhrok.lua:25`。状态：文本确认。

### C14 | entry-03458 | 存在问题

原文“created many **dark cults**”，译文“通过**黑暗仪式**”。组织被换成仪式，且原文的“建立多个”信息消失。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:22`。状态：文本确认。

### C15 | entry-03458 | 存在问题

原文“use ‘vim’ to power their **special abilities**”，译文“使用活力值来施放他们的**法术**”。“特殊能力”涵盖范围比“法术”宽；译文无依据地限定能力类型。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:34`。状态：文本确认。

### C16 | entry-03458 | 存在问题

原文活力“can only be stolen from your **foes**”，译文“必须从你的**目标**身上偷取”。“目标”不限定敌对关系，放宽了来源范围。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:35`。状态：文本确认；不据此断言所有活力获取机制。

### C17 | entry-03460 | 存在问题

原文仅说在 Fearscape 的“**rigorous training**”磨砺了能力；译文增添“恶魔空间的**烈火**和严格训练”。烈火作为磨砺原因并未出现在该句。见 `A/overload/data/texts/unlock-race_doomelf.lua:22`。状态：文本确认。

### C18 | entry-03460 | 存在问题

原文“have **earned the right to make** Doomelf characters”，译文“魔化精灵**应运而生**”。玩家获得创建该种族角色的权限，被改成种族由此出现，改变了叙述对象和解锁结果。见 `A/overload/data/texts/unlock-race_doomelf.lua:24`。状态：文本确认。

### C19 | entry-03475 | 仅建议

原文“I feel like I have **potential to grow**”，译文“我觉得我的**潜能增长了**”。后者更像潜能已经提高，前者更重成长空间；但该句紧接玩家选择提供属性增益的对话分支（`C/data/chats/godfeaster-malyu-escaped.lua:47–55、72–76`），两者在此均能表达获得成长机会。不足以判定为实质时序错误。状态：仅措辞建议。

### C20 | entry-03478 | 存在问题

原文物品“**rolls** from the sack”，译文“**掉**了出来”。滚出的运动方式被改为掉落。事件在生成物品后显示该日志，见 `C/data/general/events/digestive-sack.lua:104–108`。状态：文本确认。

### C21 | entry-03479 | 存在问题

原文敌人“**burst out** from the sack”，译文“**掉**了出来”。原文强调敌人猛然冲出，译文变为被动掉落；对应事件生成敌人后显示该日志，见 `C/data/general/events/digestive-sack.lua:109–117`。状态：文本确认。

### C22 | entry-03481 | 存在问题

原文“already **scavenged what you could understand and use**”，译文“已经**找遍了**你能理解和使用的东西”。原文表示已搜取得到可用之物，译文只表示搜索过；快照中 `searched_dwarf` 为真时显示此句，首次交互会将物品放入玩家库存，见 `C/data/general/events/space-dwarf-ship.lua:60–71`。状态：文本差异确认，快照行为为佐证；目标 DLC 版本的适用性仍未固定。

### 读取范围与限制

实际读取了指定的 `INPUT.md`、同目录 `entries.json`、`context.lua`、`source-access.json`；`entries.json` 含 40 个连续且不重复的 ID。读取并核对哈希的 `sections` 源码共 21 个：Ashes 的 `data/timed_effects.lua`、`data/zones/searing-halls/npcs.lua`、`init.lua`、三个 `overload/data/texts/` 文件及 `overload/mod/class/DemonologistsDLC.lua`；Cults 的 `data/achievements/all.lua`、`data/birth/{demented,drem,krog}.lua`、两个 `data/chats/godfeaster-malyu*.lua`、两个 `data/general/events/` 文件、五个 `data/general/grids/` 文件及 `data/general/npcs/blobs.lua`。

额外读取且哈希匹配的 Ashes 文件为 `data/birth/{corrupted,doomelf,races_cosmetic}.lua`（由 `DemonologistsDLC.lua:37–39` 的 `loadDefinition` 引入）、`data/talents/misc/races.lua`（同文件第 34 行引入）、`data/general/objects/world-artifacts.lua`（介绍中明确提到 Will of Ul’Gruth，并由同文件第 46–47 行载入）、`data/talents/corruptions/corruptions.lua`（同文件第 35 行引入）及其第 152 行 `load` 的 `demon-seeds.lua`。额外读取且哈希匹配的 Cults 文件为 `overload/mod/class/CultsDLC.lua`（核查出生定义的载入）、`superload/mod/class/{Game,Actor}.lua` 和 `superload/mod/dialogs/LevelupDialog.lua`（沿 Malyu 奖励模式符号核查；这些文件未提供所需的奖励消费证据）。

曾尝试对固定本体 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 读取明确相关的单文件 `game/modules/tome/mod/class/Actor.lua`，但该路径在该 commit 不存在，**没有读到本体源码**；因此没有据此裁定 “Life per level” 的实际计算。未读取其他报告、当前译文文件或其他实验文件；未创建临时文件、子 agent，也未修改仓库。无法完整核验的机制疑点列为 C10。本结果是 REVIEWER 观察，不是生产 `DONE_VERIFIED`。
