### batch-026 译文只读复核报告

#### 1. 复核基准与文件核对
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-026.md`
- **文件校验和**：SHA-256 为 `d59ea5e3b3fa41114ec21a1fbb9ce9ce9bd906dd0399adf7365d0efc5ed74922`（核验一致）
- **条目范围**：`entry-01003` 至 `entry-01043`（注：批次文件中无 `entry-01037`，实际条目共 40 条，已全部逐条覆盖）
- **源码参考**：公开源码 `t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`
- **译文上下文终点**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

#### 2. 逐条复核详情（全部 40 条）

- **entry-01003**：【未发现问题】
  - **位置**：`mod-tome.lua:12360`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:418-419`）
  - **依据**：物品 `Crystal of Focus` 的描述。专名 `Spellhunt` 译为“魔法狩猎”，`Inquisitor Marcus Dunn` 译为“审判官玛库斯·丹”，`antimagic` 译为“反魔法”，均符合术语库与源码机制（反魔角色可发挥额外效果，见源码 424 行）；换行与标点无误。

- **entry-01004**：【未发现问题】
  - **位置**：`mod-tome.lua:12371`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:521`）
  - **依据**：物品 `Orc Feller` 半身人佩戴时的日志提示。颜色标签 `#LIGHT_BLUE#` 与感叹号保留完整，专名 `Herah` 对应盗贼赫拉，属性 `guile and luck`（狡诈和幸运）与源码加成对应，无语法及格式错误。

- **entry-01005**：【未发现问题】
  - **位置**：`mod-tome.lua:12378`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:569-571`）
  - **依据**：物品 `Fists of the Desert Scorpion` 的背景故事描述。专名 `Age of Pyre` 译为“烈火纪”，`Elvala` 译为“埃尔瓦拉”，`Shaloren` 译为“永恒精灵”，`alchemist Nessylia` 译为“炼金术师奈瑟莉亚”，段落换行与标点完整，语义准确流畅。

- **entry-01006**：【未发现问题】
  - **位置**：`mod-tome.lua:12385`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:622`）
  - **依据**：物品 `Gwai's Burninator`（`BASE_ROD`）的未鉴定名。源码描述明确记载其为魔杖（wand），中文全库统一将此类 rod 未鉴定名作“魔杖”，译为“发光的魔杖”符合语境与统一规范。

- **entry-01007**：【未发现问题】
  - **位置**：`mod-tome.lua:12388`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:646`）
  - **依据**：源码调用为 `game.logSeen(who, "%s activates %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。译文 `%s激活了%s%s！` 中 3 个占位符数量与语序均严格吻合（角色名 + 他的/她的 + 物品名），标点匹配。

- **entry-01008**：【未发现问题】
  - **位置**：`mod-tome.lua:12392`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:686`）
  - **依据**：战斧神器 `Blood-Letter` 的名称，译为“放血者”准确贴切，无格式问题。

- **entry-01009**：【未发现问题】
  - **位置**：`mod-tome.lua:12406`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:798`）
  - **依据**：物品 `Telos's Staff Crystal` 镶嵌在傀儡上时的提示。颜色标签 `#ROYAL_BLUE#`、样式标签 `#{bold}#`、`#{normal}#` 及 `%s` 占位符齐全，术语 `golem`（傀儡）符合标准。

- **entry-01010**：【未发现问题】
  - **位置**：`mod-tome.lua:12419`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:887`）
  - **依据**：腰带神器 `Neira's Memory` 触发护盾时的可见日志。`%s` 占位符与感叹号保留，专名 `Neira` 译为“尼耶拉”与同 section 腰带译名一致。

- **entry-01011**：【未发现问题】
  - **位置**：`mod-tome.lua:12422`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:900`）
  - **依据**：皮甲神器 `Nature's Blessing` 的描述。主格专名 `Ziguranth` 译为“伊格兰斯”（符合教团用“伊格兰斯”、地名用“伊格”的术语规范），`Humans and Halflings` 译为“人类与半身人”，语法完整。

- **entry-01012**：【未发现问题】
  - **位置**：`mod-tome.lua:12429`（`mod-tome/data/general/objects/world-artifacts-maj-eyal.lua:978-979`）
  - **依据**：长剑神器 `Witch-Bane` 的描述。`voratun` 译为“沃瑞钽”，`Marcus Dunn` 译为“玛库斯·丹”，`Spellhunt` 译为“魔法狩猎”，换行结构完整，反魔法机制叙述准确。

- **entry-01013**：【未发现问题】
  - **位置**：`mod-tome.lua:12468`（`mod-tome/data/general/objects/world-artifacts.lua:35`）
  - **依据**：蓝色宝石神器 `Windborne Azurite` 的名称，译为“风之蓝铜矿”准确无误。

- **entry-01014**：【未发现问题】
  - **位置**：`mod-tome.lua:12473`（`mod-tome/data/general/objects/world-artifacts.lua:70`）
  - **依据**：神器纹身 `Primal Infusion` 的描述。术语 `wild infusion` 译为“野性纹身”，完全符合术语库既定条目，句意通顺。

- **entry-01015**：【未发现问题】
  - **位置**：`mod-tome.lua:12482`（`mod-tome/data/general/objects/world-artifacts.lua:171`）
  - **依据**：戒指神器 `Vargh Redemption` 的外观描述，译文“这枚碧蓝色的戒指摸起来似乎总是湿润的”表意准确。

- **entry-01016**：【未发现问题】
  - **位置**：`mod-tome.lua:12483`（`mod-tome/data/general/objects/world-artifacts.lua:181-182`）
  - **依据**：源码中通过 `tformat` 传入 4 个参数（半径、持续时间、寒冷伤害、物理伤害）。译文占位符 `%d`、`%d`、`%0.2f`、`%0.2f` 顺序与类型完全对应，`Willpower`（意志）、`cold`（寒冷）、`physical`（物理）、`stun resistance`（震慑抗性）术语准确无误。

- **entry-01017**：【未发现问题】
  - **位置**：`mod-tome.lua:12485`（`mod-tome/data/general/objects/world-artifacts.lua:210`）
  - **依据**：戒指使用主动技能时的场景日志。占位符 `%s`、`%s`（角色名与物品名）与感叹号完全一致，语义准确。

- **entry-01018**：【未发现问题】
  - **位置**：`mod-tome.lua:12488`（`mod-tome/data/general/objects/world-artifacts.lua:233`）
  - **依据**：戒指神器 `Ring of the Dead` 的描述，译文表达准确流畅，无格式问题。

- **entry-01019**：【未发现问题】
  - **位置**：`mod-tome.lua:12489`（`mod-tome/data/general/objects/world-artifacts.lua:238`）
  - **依据**：戒指神器 `Ring of the Dead` 的特殊复活效果描述，表意准确，标点匹配。

- **entry-01020**：【未发现问题】
  - **位置**：`mod-tome.lua:12502`（`mod-tome/data/general/objects/world-artifacts.lua:325`）
  - **依据**：项链神器 `Garkul's Teeth` 的背景描述。`humanoid` 译为“类人生物”，`Garkul the Devourer` 译为“吞噬者加库尔”，表意准确。

- **entry-01021**：【未发现问题】
  - **位置**：`mod-tome.lua:12506`（`mod-tome/data/general/objects/world-artifacts.lua:364`）
  - **依据**：光源神器 `Summertide Phial` 的名称，译为“炎华之瓶”准确无误。

- **entry-01022**：【未发现问题】
  - **位置**：`mod-tome.lua:12508`（`mod-tome/data/general/objects/world-artifacts.lua:370`）
  - **依据**：`Summertide Phial` 的描述，`Summertide` 译为“炎华时节”，语义契合。

- **entry-01023**：【未发现问题】
  - **位置**：`mod-tome.lua:12528`（`mod-tome/data/general/objects/world-artifacts.lua:500`）
  - **依据**：物品 `Blood of Life`（生命之血）饮用时的可见日志。两个 `%s` 占位符与感叹号保留完好，翻译准确。

- **entry-01024**：【未发现问题】
  - **位置**：`mod-tome.lua:12534`（`mod-tome/data/general/objects/world-artifacts.lua:536`）
  - **依据**：靴子神器 `Eden's Guile` 主动技能说明。占位符 `%d%%` 保留正确百分比转义，`Cunning` 译为“灵巧”，`speed` 译为“速度”，符合规范。

- **entry-01025**：【未发现问题】
  - **位置**：`mod-tome.lua:12539`（`mod-tome/data/general/objects/world-artifacts.lua:594`）
  - **依据**：盾牌神器 `Titanic` 的名称，译为“泰坦之盾”符合物品类型与通俗定译。

- **entry-01026**：【未发现问题】
  - **位置**：`mod-tome.lua:12541`（`mod-tome/data/general/objects/world-artifacts.lua:598`）
  - **依据**：盾牌神器 `Titanic` 的描述。材质专名 `stralite` 严格遵照术语库译为“斯莱特”（未误作“蓝皓石”），语句通顺。

- **entry-01027**：【未发现问题】
  - **位置**：`mod-tome.lua:12546`（`mod-tome/data/general/objects/world-artifacts.lua:656`）
  - **依据**：盾牌 `Black Mesh` 格挡特效触发日志。颜色码 `#ORCHID#`、战斗实体标签 `#Source#` 和 `#Target#` 及感叹号均完整保留。

- **entry-01028**：【未发现问题】
  - **位置**：`mod-tome.lua:12547`（`mod-tome/data/general/objects/world-artifacts.lua:659`）
  - **依据**：`Black Mesh` 成功拉近目标时的战斗日志。颜色码 `#ORCHID#`、标签 `#Source#` 与 `#Target#` 正确保留，机制描述一致。

- **entry-01029**：【存在疑点】
  - **位置**：`mod-tome.lua:12548`（`mod-tome/data/general/objects/world-artifacts.lua:662`）
  - **原文**：`#ORCHID#%s resists the tendrils' pull!`
  - **译文**：`#ORCHID#%s抵抗了触须的抓取！`
  - **证据与分析**：
    查阅源码 `world-artifacts.lua:656-663` 的格挡执行链：
    1. 触须必定先触发 `who:logCombat(src, "#ORCHID#Black tendrils from #Source# grab #Target#!")`（即 entry-01027 译文“抓住了#Target#”）；
    2. 随后代码进行击退抗性检测 `local kb = src:canBe("knockback")`；
    3. 若未能击退/拉扯目标，则进入 else 分支打印本句 `game.logSeen(src, "#ORCHID#%s resists the tendrils' pull!", ...)`。
    此处机制抵抗的是击退拉扯（knockback/pull 拖拽/牵引），而译文将其译作“抓取”，导致在战斗日志中与前一句“抓住了目标”产生语义冲突（既然已经抓住了，何来抵抗抓取？），建议定性为将 pull（拉扯/拖拽/牵引）混淆为 grab（抓取）。

- **entry-01030**：【未发现问题】
  - **位置**：`mod-tome.lua:12549`（`mod-tome/data/general/objects/world-artifacts.lua:674`）
  - **依据**：皮甲神器 `Rogue Plight` 的名称，严格遵循术语库核心定译“盗贼之厄”（替代旧版歧义定译“刺客契约”）。

- **entry-01031**：【未发现问题】
  - **位置**：`mod-tome.lua:12551`（`mod-tome/data/general/objects/world-artifacts.lua:677`）
  - **依据**：皮甲神器 `Rogue Plight` 的描述，`rogue` 译为“盗贼”，表意契合。

- **entry-01032**：【细微观察】
  - **位置**：`mod-tome.lua:12552`（`mod-tome/data/general/objects/world-artifacts.lua:686-687`）
  - **原文**：`Transfers a bleed, poison, or wound to its source or a nearby enemy every 4 turns.`
  - **译文**：`每4回合将一项流血、毒素或伤口效果转移给效果来源或者附近的敌人。`
  - **证据与分析**：
    源码 `world-artifacts.lua:707` 明确消费效果子类型：`e.subtype and (e.subtype.bleed or e.subtype.poison or e.subtype.wound)`。
    查术语快照，`wound` 在 `T.GAME.EFFECT combat effect subtype` 下的标准定译为“创伤”，而此处译文译为了日常用词“伤口”（“流血、毒素或伤口效果”）。虽然玩家能理解其含义，但与标准的 effect subtype 术语“创伤”存在细微不一致。

- **entry-01033**：【未发现问题】
  - **位置**：`mod-tome.lua:12553`（`mod-tome/data/general/objects/world-artifacts.lua:728`）
  - **依据**：`Rogue Plight` 转移效果给来源时的玩家日志。颜色标签 `#CRIMSON#` 与感叹号保留，实体译名一致。

- **entry-01034**：【未发现问题】
  - **位置**：`mod-tome.lua:12554`（`mod-tome/data/general/objects/world-artifacts.lua:738`）
  - **依据**：`Rogue Plight` 转移效果给周围敌人时的玩家日志。颜色标签 `#CRIMSON#` 与感叹号保留，实体译名一致。

- **entry-01035**：【未发现问题】
  - **位置**：`mod-tome.lua:12603`（`mod-tome/data/general/objects/world-artifacts.lua:1122`）
  - **依据**：套装 `HELM_KROLTAR` 与 `SCALE_MAIL_KROLTAR` 齐聚回调时的日志。颜色标签 `#GOLD#` 保留，“接触时”在佩戴套装语境下表意通顺。

- **entry-01036**：【未发现问题】
  - **位置**：`mod-tome.lua:12604`（`mod-tome/data/general/objects/world-artifacts.lua:1125`）
  - **依据**：库洛塔套装拆散时的日志。颜色标签 `#GOLD#` 保留，语义准确。

- **关于编号 entry-01037 的说明**：
  - 批次文件 `batch-026.md` 中无 `entry-01037` 序号，在 `entry-01036` 后直接接续 `entry-01038`，批次内实际条目数确为 40 条。

- **entry-01038**：【存在疑点】
  - **位置**：`mod-tome.lua:12614`（`mod-tome/data/general/objects/world-artifacts.lua:1197`）
  - **原文**：`Fashioned by Grand Smith Dakhtun in the Age of Allure, these dwarven-steel gauntlets have been etched with golden arcane runes and are said to grant the wearer unparalleled physical and magical might.`
  - **译文**：`厄流纪由大师级铁匠达克顿打造而成。那些矮人钢臂铠镂刻着金色的奥术符文，据说它们可以赋予穿戴者强大的魔武力量。`
  - **证据与分析**：
    1. **严重主谓语病与断句逻辑错误**：原文是由过去分词状语引导的单句 `Fashioned by Grand Smith Dakhtun in the Age of Allure, these dwarven-steel gauntlets have been etched...`，真正被打造的主体是“这副矮人钢臂铠”（`these dwarven-steel gauntlets`）。译文将其强行拆分成独立句，并把状语“厄流纪”置于句首，导致字面意思变成“厄流纪由大师级铁匠达克顿打造而成”（荒谬地变成了铁匠打造了一个时代！），且第一句缺失主语，第二句主语断裂。
    2. **关键修饰词漏译/弱化**：原文 `unparalleled physical and magical might`（无与伦比的/举世无双的魔武力量），译文仅作普通的“强大的魔武力量”，丢失了 `unparalleled`（无与伦比）的关键修饰。
    3. **指代偏差**：指示代词 `these`（这副/这些）被译作远指的“那些”。

- **entry-01039**：【未发现问题】
  - **位置**：`mod-tome.lua:12644`（`mod-tome/data/general/objects/world-artifacts.lua:1463`）
  - **依据**：布甲神器 `Temporal Augmentation Robe - Designed In-Style` 的名称，致敬《神秘博士》时空法师长袍，译为“时空增益长袍·引领时尚”准确得当。

- **entry-01040**：【未发现问题】
  - **位置**：`mod-tome.lua:12647`（`mod-tome/data/general/objects/world-artifacts.lua:1495`）
  - **依据**：长袍未集齐帽子时的套装描述，译文“奇怪的是，它从不变出帽子”准确自然。

- **entry-01041**：【未发现问题】
  - **位置**：`mod-tome.lua:12650`（`mod-tome/data/general/objects/world-artifacts.lua:1508`）
  - **依据**：帽子神器 `Un'fezan's Cap` 的描述。样式标签 `#{italic}#`、`#{normal}#` 及换行符完好保留，致敬台词“菲斯帽很酷”翻译准确。

- **entry-01042**：【未发现问题】
  - **位置**：`mod-tome.lua:12653`（`mod-tome/data/general/objects/world-artifacts.lua:1541`）
  - **依据**：长袍与帽子套装集齐时的日志。颜色标签 `#STEEL_BLUE#` 保留，句意准确。

- **entry-01043**：【未发现问题】
  - **位置**：`mod-tome.lua:12672`（`mod-tome/data/general/objects/world-artifacts.lua:1710`）
  - **依据**：皮甲神器 `Skin of Many`（众生之皮）的描述。`skins` 译为“皮肤”，恐怖氛围渲染准确，无标点与语法缺陷。

---

#### 3. 疑点与观察汇总表

| 条目编号 | 判定类别 | 涉及文件与位置 | 核心问题摘要 |
| :--- | :--- | :--- | :--- |
| **entry-01029** | 存在疑点 | `mod-tome.lua:12548`<br>`world-artifacts.lua:662` | 原文为 `resists the tendrils' pull!`，对应抗击退拉扯机制（`src:canBe("knockback")`），译文误译为“抵抗了触须的抓取”，与前一句已抓取成功的日志产生直接语义冲突。 |
| **entry-01032** | 细微观察 | `mod-tome.lua:12552`<br>`world-artifacts.lua:686` | 效果子类别 `wound`（effect subtype）被译为日常词“伤口”，未采用术语库标准定译“创伤”。 |
| **entry-01038** | 存在疑点 | `mod-tome.lua:12614`<br>`world-artifacts.lua:1197` | 分词状语硬拆导致主谓断裂与荒谬语义（“厄流纪由大师级铁匠达克顿打造而成”）；且 `unparalleled`（无与伦比的）被弱化为“强大的”，`these` 误译为“那些”。 |

本批次共审查 40 条冻结译文，其中 37 条未发现问题，2 条存在疑点，1 条为细微观察。复核结束。