# batch-030 译文复核报告

### 一、复核准备与环境核验
- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-030.md`
- **文件哈希核验**：实际计算 SHA-256 为 `9aa78459394fc0743d79617a51e7ed6679b31f1d38d7199395609b35489c0a50`，与给定的冻结哈希完全一致。
- **源码与译文基准**：
  - 公开源码均通过固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 进行只读核对。
  - 译文比对基准为仓库 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。
  - 本批 40 条均属于主模块 `mod-tome`（对应源码路径 `game/modules/tome/`），无 DLC 条目。
- **复核范围**：条目 `entry-01165` 至 `entry-01204`，共 40 条，已实现逐条覆盖。

---

### 二、逐条复核记录

#### entry-01165
- **位置**：mod-tome.lua:13320（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`This mindstar glows with a dim cool light, but seems somehow incomplete.`
- **译文**：`这个灵晶散发着寒冷的微光，但似乎有点残缺。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8124`（神器 `EYE_OF_WINTER` / 冬日之眼 的描述字段 `desc`）。
- **核验结论**：**未发现问题**。
- **依据说明**：占位符与标点一致；术语 `mindstar` 译为“灵晶”标准规范；`cool light` 结合冬日之眼的主题译为“寒冷的微光”，语义准确。

#### entry-01166
- **位置**：mod-tome.lua:13323（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`Crafted for a warlord who wanted to keep his subjects under a stralite grip. Dark thoughts went into the making of these gauntlets, literally.`
- **译文**：`一位军阀为将臣民牢牢掌控于斯莱特之掌中而打造了这副手套。制作过程中确实注入了黑暗的思想。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8184`（神器 `Ruthless Grip` / 无情之握 的描述字段 `desc`）。
- **核验结论**：**未发现问题**。
- **依据说明**：材质名 `stralite` 严格遵循术语库规范统一译为“斯莱特”；原文中化用 iron grip 的“stralite grip”与后文手套具象意象在译文“斯莱特之掌中”得到准确体现，文意通顺。

#### entry-01167
- **位置**：mod-tome.lua:13332（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`explodes a frozen creature (damage scales with willpower)`
- **译文**：`令一个冻结生物爆炸（伤害受意志加成）`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8224`（神器 `Icy Kill` / 冰冷杀戮 的 `special_on_kill.desc`）。
- **核验结论**：**未发现问题**。
- **依据说明**：机制代码为击杀处于 `EFF_FROZEN` 状态的目标时触发范围冰伤害 `30 + who:getWil()*0.5`，属性 `willpower` 准确译为“意志”，括号与机制完全吻合。

#### entry-01168
- **位置**：mod-tome.lua:13337（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`#Source# hurls %s %s at #target#!`
- **译文**：`#Source#把%s%s掷向#target#！`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8294`（神器 `Thunderfall` / 落雷 的 `use_power` 中 `who:logCombat` 调用）。
- **核验结论**：**未发现问题**。
- **依据说明**：源码传参顺序依次为 `who:his_her()`（如“他的/她的”）与 `self:getName(...)`（武器名）。中文译文 `#Source#把%s%s掷向#target#！` 语序及两个 `%s`、战斗标签 `#Source#` 与 `#target#!` 均完全对应且符合语法。

#### entry-01169
- **位置**：mod-tome.lua:13338（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`%s's weapon returns to %s!`
- **译文**：`%s的武器回到了%s手中！`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8306`（神器 `Thunderfall` / 落雷 中 `game.logSeen` 调用）。
- **核验结论**：**未发现问题**。
- **依据说明**：源码传参为 `who:getName():capitalize()` 与 `who:him_her()`，中文结构 `%s的武器回到了%s手中！` 占位符数量与顺序均正确，含义通顺。

#### entry-01170
- **位置**：mod-tome.lua:13340（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`Kinetic energies are focussed in the core of this mindstar.`
- **译文**：`动能集中在这个灵晶的核心里。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8320`（神器 `Kinetic Focus` / 动能之核 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：`mindstar` 译为“灵晶”，`Kinetic energies` 译为“动能”，标点匹配，未见异常。

#### entry-01171
- **位置**：mod-tome.lua:13341（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`You feel two unconnected psionic channels on this item.`
- **译文**：`你感到这件物品上有两条尚未连通的灵能通道。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8343` 与 `8424`（三核灵晶套装未激活时的 `set_desc.trifocus` 描述）。
- **核验结论**：**未发现问题**。
- **依据说明**：`psionic` 规范译为“灵能”，准确反映该物品有另外两个 Focus 可连通的套装机制，句义完整。

#### entry-01172
- **位置**：mod-tome.lua:13342（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`#YELLOW#You feel psionic energy linking the mindstars.`
- **译文**：`#YELLOW#你感受到灵晶之间建立了灵能的连接。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8364, 8374, 8384`（三核灵晶套装激活时的日志 `game.logSeen`）。
- **核验结论**：**未发现问题**。
- **依据说明**：颜色代码 `#YELLOW#` 完好保留，句义完整准确。

#### entry-01173
- **位置**：mod-tome.lua:13345（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`Electrical energies are focussed in the core of this mindstar.`
- **译文**：`电能集中在这个灵晶的核心里。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8401`（神器 `Charged Focus` / 电能之核 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01170 保持严格的句式对称与术语统一，未见异常。

#### entry-01174
- **位置**：mod-tome.lua:13348（section：`mod-tome/data/general/objects/world-artifacts.lua`）
- **原文**：`Thermal energies are focussed in the core of this mindstar.`
- **译文**：`热能集中在这个灵晶的核心里。`
- **源码依据**：`game/modules/tome/data/general/objects/world-artifacts.lua:8471`（神器 `Thermal Focus` / 热能之核 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01170、entry-01173 句式结构一致，表达严谨。

#### entry-01175
- **位置**：mod-tome.lua:13423（section：`mod-tome/data/general/traps/complex.lua`）
- **原文**：`@Target@ walks on a trap, and there is a loud noise.`
- **译文**：`@Target@踩上陷阱，发出了巨大的声音。`
- **源码依据**：`game/modules/tome/data/general/traps/complex.lua:36`（`giant boulder trap` / 滚石陷阱 的 `message` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：引擎层 `Trap.lua:137` 会对 `@Target@` 进行 `tname:capitalize()` 首字母大写替换，大写标签保持无误，语义及标点完整。

#### entry-01176
- **位置**：mod-tome.lua:13438（section：`mod-tome/data/general/traps/complex.lua`）
- **原文**：`The poison spore looks somewhat drained.`
- **译文**：`毒性孢子的能量似乎被抽取了。`
- **源码依据**：`game/modules/tome/data/general/traps/complex.lua:174`（`poison spore` 陷阱在次数 `self.nb <= 0` 移除时的 `game.logSeen`）。
- **核验结论**：**未发现问题**。
- **依据说明**：源码逻辑为孢子陷阱喷毒 3 次耗尽后枯竭移除，译文准确传达了次数耗尽/能量枯竭的情境。

#### entry-01177
- **位置**：mod-tome.lua:13440（section：`mod-tome/data/general/traps/complex.lua`）
- **原文**：`Flames start to appear around @target@.`
- **译文**：`@target@的周围出现了火焰。`
- **源码依据**：`game/modules/tome/data/general/traps/complex.lua:198`（`delayed explosion trap` / 延时爆炸陷阱 的 `message` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：小写占位符 `@target@` 保持完整，标点对应，语义流畅。

#### entry-01178
- **位置**：mod-tome.lua:13444（section：`mod-tome/data/general/traps/complex.lua`）
- **原文**：`Cold flames start to appear around @target@.`
- **译文**：`@target@的周围出现了冰冷火焰。`
- **源码依据**：`game/modules/tome/data/general/traps/complex.lua:247`（`cold flames trap` / 冷焰陷阱 的 `message` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01177 句式完全对称，小写占位符 `@target@` 保留无误。

#### entry-01179
- **位置**：mod-tome.lua:13451（section：`mod-tome/data/general/traps/elemental.lua`）
- **原文**：`elemental`
- **译文**：`元素生物`
- **源码依据**：`game/modules/tome/data/general/traps/elemental.lua:21`（陷阱模板 `TRAP_ELEMENTAL` 的 `type = "elemental"` 定义）。
- **核验结论**：**未发现问题**。
- **依据说明**：source_tag 为 `entity type`，依据术语库快照规则 `elemental -> 元素生物 (entity type 统一为“元素生物”)`，符合实体类型术语规范。

#### entry-01180
- **位置**：mod-tome.lua:13470（section：`mod-tome/data/general/traps/elemental.lua`）
- **原文**：`crackling spot`
- **译文**：`噼啪作响的地点`
- **源码依据**：`game/modules/tome/data/general/traps/elemental.lua:83`（`lightning trap` / 闪电陷阱 的未鉴定名 `unided_name`）。
- **核验结论**：**未发现问题**。
- **依据说明**：与同组其他元素陷阱（corroded spot/burnt spot/frozen spot）的“地点”命名法保持协调，生动表现闪电声。

#### entry-01181
- **位置**：mod-tome.lua:13476（section：`mod-tome/data/general/traps/elemental.lua`）
- **原文**：`A bolt of fire fires onto @target@!`
- **译文**：`一团火焰炸向@target@！`
- **源码依据**：`game/modules/tome/data/general/traps/elemental.lua:118`（`fire blast trap` / 火焰爆炸陷阱 的 `message` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：占位符 `@target@` 与感叹号完好保留；相较于单体火陷阱的“击中”，范围爆炸陷阱译作“炸向”契合 AOE 机制。

#### entry-01182
- **位置**：mod-tome.lua:13487（section：`mod-tome/data/general/traps/elemental.lua`）
- **原文**：`A powerful blast of fire impacts @target@!`
- **译文**：`一团大火球炸向@target@！`
- **源码依据**：`game/modules/tome/data/general/traps/elemental.lua:174`（`dragon fire trap` / 龙火陷阱 的 `message` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：占位符 `@target@` 与感叹号保留完整，表达准确。

#### entry-01183
- **位置**：mod-tome.lua:13524（section：`mod-tome/data/general/traps/teleport.lua`）
- **原文**：`%s resists being teleported!`
- **译文**：`%s 抵抗传送！`
- **源码依据**：`game/modules/tome/data/general/traps/teleport.lua:42`（`teleport trap` 无法传送生物时的 `game.logSeen`）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 占位符与语义完全正确。
  - 细微观察点：译文占位符 `%s` 之后存在一个半角空格（`%s 抵抗传送！`），而同段前一行（13523 行）`%s is teleported away!` 译为 `%s被传送走了！`（未留空格）。此处仅为标点空格风格微瑕，不影响游戏机制与占位符解析。

#### entry-01184
- **位置**：mod-tome.lua:13565（section：`mod-tome/data/ingredients.lua`）
- **原文**：`vial of greater demon bile`
- **译文**：`一瓶大恶魔胆汁`
- **源码依据**：`game/modules/tome/data/ingredients.lua:67`（炼金原料条目名称）。
- **核验结论**：**未发现问题**。
- **依据说明**：`greater demon` 译为“大恶魔”，`bile` 译为“胆汁”，与材料实体命名一致。

#### entry-01185
- **位置**：mod-tome.lua:13572（section：`mod-tome/data/ingredients.lua`）
- **原文**：`honey tree root`
- **译文**：`蜂蜜树的根`
- **源码依据**：`game/modules/tome/data/ingredients.lua:125`（炼金原料条目名称）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01191 实体名称一致，通俗准确。

#### entry-01186
- **位置**：mod-tome.lua:13591（section：`mod-tome/data/ingredients.lua`）
- **原文**：`wretchling eyeball`
- **译文**：`小劣魔之眼`
- **源码依据**：`game/modules/tome/data/ingredients.lua:323`（炼金原料条目名称）。
- **核验结论**：**未发现问题**。
- **依据说明**：`wretchling` 统一对应“小劣魔”，翻译准确。

#### entry-01187
- **位置**：mod-tome.lua:13598（section：`mod-tome/data/ingredients.lua`）
- **原文**：`A length of troll intestines. Fortunately, the troll appears to have eaten nothing in some time.`
- **译文**：`一截巨魔肠子。幸运的是，这只巨魔似乎已经有一段时间没吃东西了。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:26`（`TROLL_INTESTINE` 描述 `desc`）。
- **核验结论**：**未发现问题**。
- **依据说明**：标点严格匹配（两个句号），幽默讽刺口吻传达准确。

#### entry-01188
- **位置**：mod-tome.lua:13611（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Best results occur with tongues never tainted by profanity, so if you happen to know any saintly nagas...`
- **译文**：`最好的结果来自从未被污言秽语亵渎过的舌头，所以如果你正好碰到那些圣洁的娜迦……`
- **源码依据**：`game/modules/tome/data/ingredients.lua:62`（`NAGA_TONGUE` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：术语 `nagas` 译为“娜迦”，省略号保留对应，语义生动贴切。

#### entry-01189
- **位置**：mod-tome.lua:13612（section：`mod-tome/data/ingredients.lua`）
- **原文**：`vial of greater demon bile`
- **译文**：`一瓶大恶魔胆汁`
- **源码依据**：`game/modules/tome/data/ingredients.lua:67`（实体名称 `entity name`）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01184（原料名）完全一致，保持统一。

#### entry-01190
- **位置**：mod-tome.lua:13622（section：`mod-tome/data/ingredients.lua`）
- **原文**：`The severed front half of a minotaur snout, ring and all.`
- **译文**：`从米诺陶口鼻部割下来的前半截，连鼻环一起。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:94`（`MINOTAUR_NOSE` 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：`minotaur snout` 准确翻译为“米诺陶口鼻部”，`ring and all` 译为“连鼻环一起”，形象准确。

#### entry-01191
- **位置**：mod-tome.lua:13633（section：`mod-tome/data/ingredients.lua`）
- **原文**：`honey tree root`
- **译文**：`蜂蜜树的根`
- **源码依据**：`game/modules/tome/data/ingredients.lua:125`（实体名称 `entity name`）。
- **核验结论**：**未发现问题**。
- **依据说明**：与 entry-01185 保持一致。

#### entry-01192
- **位置**：mod-tome.lua:13634（section：`mod-tome/data/ingredients.lua`）
- **原文**：`The severed end of one of a honey tree's roots. It wriggles around occasionally, seemingly unwilling to admit that it's dead... and a *plant*.`
- **译文**：`从蜂蜜树的一根树根上切下来的断端。它偶尔会蠕动下，似乎不承认它已经死了，而且还是个“植物”。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:126`（`HONEY_TREE_ROOT` 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：原文强调标记 `*plant*` 转换为中文双引号 `“植物”`，表现出叙述者的反讽语气，句义通顺。

#### entry-01193
- **位置**：mod-tome.lua:13635（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Keep a firm grip on it. These things will dig themselves right back into the ground if you drop them.`
- **译文**：`牢牢的抓住它，如果你不小心把它掉在地上，它会立刻挖地逃走。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:128`（`HONEY_TREE_ROOT` 的 `alchemy_text` 对话）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 核心含义准确，准确说明若脱手树根会钻入地下的机制/背景。
  - 细微观察点：原作为两句独立句子（句号），译文合为一句（逗号）；“牢牢的抓住它”中修饰动词规范应作“地”（牢牢地）。不影响实际理解。

#### entry-01194
- **位置**：mod-tome.lua:13641（section：`mod-tome/data/ingredients.lua`）
- **原文**：`I know, I know. Where does the eel stop and the tail start? It doesn't much matter. The last ten inches or so should do nicely.`
- **译文**：`我知道，我知道。你想问电鳗的尾巴是哪一段？没有确切的答案。最后 10 英寸或许是最合适的。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:146`（`ELECTRIC_EEL_TAIL` 的 `alchemy_text` 对话）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 设问及前后句整体语气生动风趣，符合炼金术师指引。
  - 细微观察点：原文第三句 `It doesn't much matter.` 本意为“其实无所谓/没那么讲究”，译文轻度意译为“没有确切的答案”，对任务指引无实质负面影响。

#### entry-01195
- **位置**：mod-tome.lua:13647（section：`mod-tome/data/ingredients.lua`）
- **原文**：`You'd think I could get one of these from a local hunter, but they've had no luck. Don't get eaten.`
- **译文**：`你认为我可以从本地的猎户手上取得它吗？甭想了，他们没那个运气。不要被吃掉了。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:164`（`BEAR_PAW` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：将前句转换为设问与回答，生动体现出 NPC 的调侃口吻，核心信息完整。

#### entry-01196
- **位置**：mod-tome.lua:13650（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Ice Wyrms lose teeth fairly often, so you might get lucky and not have to do battle with one. But dress warm just in case.`
- **译文**：`冰龙每隔一段时间会换齿，所以你幸运的话，可以捡到几颗而不需要和它战斗。保险起见穿的暖和点……`
- **源码依据**：`game/modules/tome/data/ingredients.lua:173`（`ICE_WYRM_TOOTH` 的 `alchemy_text` 对话）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 核心含义准确传达（冰龙常换牙，不必硬战但需注意防寒）。
  - 细微观察点：句末原标点为句号，译文转为省略号“……”；“穿的暖和点”规范字形应为“穿得”。

#### entry-01197
- **位置**：mod-tome.lua:13653（section：`mod-tome/data/ingredients.lua`）
- **原文**：`I hear these can be found in a cave near Elvala. I also hear that they can cause you to spontaneously combust, so no need to explain if you come back hideously scarred.`
- **译文**：`我听说这些东西可以在埃尔瓦拉附近的洞穴里找到。我还听说它们会使你自燃，所以要是你回来时遍体伤疤，也用不着解释了。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:182`（`RED_CRYSTAL_SHARD` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：地名 `Elvala`（埃尔瓦拉）与 `cave`（洞穴）规范统一，自燃导致伤痕的文意完整忠实。

#### entry-01198
- **位置**：mod-tome.lua:13656（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Keep this stuff well away from your campfire unless you want me to have to find a new, more alive adventurer.`
- **译文**：`把这个瓶子离你的篝火远一些，我可不想明天重新找一个活的冒险家。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:191`（`FIRE_WYRM_SALIVA` 的 `alchemy_text` 对话）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 核心含义准确（火龙涎易燃，需远离火源防死）。
  - 细微观察点：前半句“把这个瓶子离你的篝火远一些”句式略带把字句杂糅（规范表述多为“让这个瓶子离篝火远一些”或“把这东西放得离篝火远一些”）；此外译文增加了“明天”一词。整体语意明晰。

#### entry-01199
- **位置**：mod-tome.lua:13659（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Unfortunately for you, the chunks that regularly fall off ghouls won't do. I need one freshly carved off.`
- **译文**：`告诉你一个不幸的消息，平时从食尸鬼身上掉下来的肉是不行的。我需要新鲜的，刚切下来的肉。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:200`（`GHOUL_FLESH` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：术语 `ghouls` 统一译为“食尸鬼”，生肉需刚割下不能要腐肉掉落物的要求传达清楚。

#### entry-01200
- **位置**：mod-tome.lua:13662（section：`mod-tome/data/ingredients.lua`）
- **原文**：`That is, a bone from a corpse that's undergone mummification. Actually, any bit of the body would do, but the bones are the only parts you're certain to find when you kick a mummy apart. I recommend finding one that doesn't apply curses.`
- **译文**：`那就是，经过木乃伊化的尸体身上的骨头。实际上，身体的任何部位都可以，只是踢散一具木乃伊后唯一保证能找到的就是骨头了。我推荐你找一具不会施加诅咒的木乃伊。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:209`（`MUMMY_BONE` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：术语 `curses` 译为“诅咒”，对木乃伊碎骨及防诅咒建议的翻译流畅准确。

#### entry-01201
- **位置**：mod-tome.lua:13665（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Yes, sandworms have teeth. They're just very small and well back from where you're ever likely to see them and live.`
- **译文**：`是的，沙虫也有牙齿。它们只是很小，藏得很好，如果你把头伸进去找它你就没法活着回来了。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:218`（`SANDWORM_TOOTH` 的 `alchemy_text` 对话）。
- **核验结论**：**细微观察**。
- **依据说明**：
  - 后半句直译为“长在很靠里面的地方，在你能看到它们还能活命的范围之外”。
  - 细微观察点：译文后半句采用意译“如果你把头伸进去找它你就没法活着回来了”，虽然属于修辞化转译，但极为生动地契合沙虫内部凶险的背景。

#### entry-01202
- **位置**：mod-tome.lua:13667（section：`mod-tome/data/ingredients.lua`）
- **原文**：`Unlike the rest of the black mamba, the severed head isn't moving.`
- **译文**：`不像黑曼巴的其余部分，这颗被斩下的头一动不动。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:226`（`BLACK_MAMBA_HEAD` 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：标点及词义准确对应，未见异常。

#### entry-01203
- **位置**：mod-tome.lua:13670（section：`mod-tome/data/ingredients.lua`）
- **原文**：`As unpleasant-looking as any exposed organ.`
- **译文**：`和任何外露的器官一样难看。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:235`（`SNOW_GIANT_KIDNEY` 的 `desc` 字段）。
- **核验结论**：**未发现问题**。
- **依据说明**：短语结构和词义完全吻合。

#### entry-01204
- **位置**：mod-tome.lua:13671（section：`mod-tome/data/ingredients.lua`）
- **原文**：`I suggest not killing the snow giant by impaling it through the kidneys. You'll just have to find another.`
- **译文**：`我建议你不要从雪巨人的肾脏部位刺死它，否则你不得不寻找另外一个。`
- **源码依据**：`game/modules/tome/data/ingredients.lua:237`（`SNOW_GIANT_KIDNEY` 的 `alchemy_text` 对话）。
- **核验结论**：**未发现问题**。
- **依据说明**：`snow giant` 译为“雪巨人”，`kidneys` 译为“肾脏”，准确传达“若贯穿肾脏刺死则材料损坏需重找”的炼金师建议。

---

### 三、复核总结

1. **未发现问题条目**（共 35 条）：
   `entry-01165`, `entry-01166`, `entry-01167`, `entry-01168`, `entry-01169`, `entry-01170`, `entry-01171`, `entry-01172`, `entry-01173`, `entry-01174`, `entry-01175`, `entry-01176`, `entry-01177`, `entry-01178`, `entry-01179`, `entry-01180`, `entry-01181`, `entry-01182`, `entry-01184`, `entry-01185`, `entry-01186`, `entry-01187`, `entry-01188`, `entry-01189`, `entry-01190`, `entry-01191`, `entry-01192`, `entry-01195`, `entry-01197`, `entry-01199`, `entry-01200`, `entry-01202`, `entry-01203`, `entry-01204`。
   - 所有关键占位符（如 `#Source#`、`#target#`、`@target@`、`@Target@`、`%s` 等）与颜色代码（`#YELLOW#`）均保持完好且参数顺序无颠倒；
   - 术语使用（斯莱特、灵晶、意志、元素生物、食尸鬼、雪巨人等）均严格遵照规则。

2. **细微观察条目**（共 5 条，均不构成阻断性缺陷）：
   - `entry-01183`：占位符 `%s` 后带有多余半角空格（`%s 抵抗传送！`）。
   - `entry-01193`：助词字形“牢牢的”（规范为“地”），断句由两句合为一句。
   - `entry-01194`：`It doesn't much matter.` 意译为“没有确切的答案”。
   - `entry-01196`：末尾标点转为省略号，“穿的”规范应为“穿得”。
   - `entry-01198`：把字句微瑕（“把这个瓶子离你的篝火远一些”），略带增词“明天”。
   - `entry-01201`：后半句进行修辞化意译（“如果你把头伸进去找它你就没法活着回来了”）。

3. **存在阻断实质疑点条目**：0 条。全部条目均能安全用于游戏运行时。