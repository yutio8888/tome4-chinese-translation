### batch-022 译文复核报告

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-022.md`
- **文件校验**：`7cf63c1ec59fe7ed32f8a6242bceab74cbb775ea52076fe6ec184bcecc50059a`（核对一致）
- **核验源码**：`t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`
- **译文基准**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`
- **复核范围**：`entry-00842` ～ `entry-00881`（共 40 条逐条覆盖）

---

#### entry-00842
- **位置/条目**：`mod-tome.lua:9492`（`entry-00842`）
- **原文**：`vial of clear fluid`
- **译文**：`一瓶透明液体`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/brotherhood-artifacts.lua` 第 47 行 `ELIXIR_FOCUS` 的未鉴定名 `unided_name=_t"vial of clear fluid"`。译文准确，无格式及占位符问题。

#### entry-00843
- **位置/条目**：`mod-tome.lua:9495`（`entry-00843`）
- **原文**：`#00FF00#The elixir has improved your capacity for exercising your core talents.`
- **译文**：`#00FF00#药剂提升了你核心技能的能力。`
- **复核结论**：细微观察
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 52、78 行（`ELIXIR_FOCUS` 增加职业技能点与 `ELIXIR_FOUNDATIONS` 增加通用技能点共用的日志提示）。英文原文为 `capacity for exercising your core talents`（运用/施展核心技能的潜力/能力），译文作「提升了你核心技能的能力」，在语义上略有省略（略去了 exercising 的运用/施展含义，读感偏向技能本身能力而非玩家运用技能的能力）。颜色码 `#00FF00#` 成对闭合，句末标点匹配，基本表意清晰。

#### entry-00844
- **位置/条目**：`mod-tome.lua:9497`（`entry-00844`）
- **原文**：`vial of tan fluid`
- **译文**：`一瓶棕褐色液体`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 58 行 `ELIXIR_BRAWN` 的未鉴定名 `unided_name=_t"vial of tan fluid"`。tan 准确译为棕褐色，符合药水外观描述。

#### entry-00845
- **位置/条目**：`mod-tome.lua:9503`（`entry-00845`）
- **原文**：`A vial of grainy, iron-colored fluid.`
- **译文**：`一瓶颗粒状的铁色液体。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 69 行 `ELIXIR_STONESKIN` 的描述 `desc = _t[[A vial of grainy, iron-colored fluid.]]`。grainy（颗粒状的）与 iron-colored（铁色的）准确对应，句末句号一致。

#### entry-00846
- **位置/条目**：`mod-tome.lua:9507`（`entry-00846`）
- **原文**：`vial of white fluid`
- **译文**：`一瓶白色液体`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 75 行 `ELIXIR_FOUNDATIONS` 的未鉴定名 `unided_name=_t"vial of white fluid"`。译文准确。

#### entry-00847
- **位置/条目**：`mod-tome.lua:9513`（`entry-00847`）
- **原文**：`green`
- **译文**：`绿色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 116 行 `LIFEBINDING_EMERALD` 的 `subtype = "green"`。宝石子分类译为「绿色」，符合分类体系。

#### entry-00848
- **位置/条目**：`mod-tome.lua:9514`（`entry-00848`）
- **原文**：`cloudy, heavy emerald`
- **译文**：`浑浊的厚重翡翠`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 115 行 `unided_name = _t"cloudy, heavy emerald"`。修饰词与名词对应准确。

#### entry-00849
- **位置/条目**：`mod-tome.lua:9515`（`entry-00849`）
- **原文**：`A lopsided, heavy emerald with murky green clouds shifting sluggishly under the surface.`
- **译文**：`一块不规则的厚重翡翠，表面之下有暗绿色的云纹缓缓浮动。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `brotherhood-artifacts.lua` 第 117 行宝石描述，lopsided（不规则的）、murky green clouds（暗绿色云纹）、shifting sluggishly（缓缓浮动）翻译准确通顺，标点完整。

#### entry-00850
- **位置/条目**：`mod-tome.lua:9594`（`entry-00850`）
- **原文**：` of daylight`
- **译文**：`日光之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/ammo.lua` 第 254 行后置词缀 `name = " of daylight", suffix=true`。后缀译为「日光之」，符合中文装备词缀规范。

#### entry-00851
- **位置/条目**：`mod-tome.lua:9595`（`entry-00851`）
- **原文**：`daylight`
- **译文**：`日光`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/ammo.lua` 第 255 行 `keywords = {daylight=true}`。关键词与词缀名称一致。

#### entry-00852
- **位置/条目**：`mod-tome.lua:9627`（`entry-00852`）
- **原文**：`%s resists the grasping vines!`
- **译文**：`%s抵抗了抓取藤蔓！`
- **复核结论**：细微观察
- **可核验依据**：源码 `egos/ammo.lua` 第 513 行日志输出 `game.logSeen(target, "%s resists the grasping vines!", target:getName():capitalize())`。占位符 `%s` 及感叹号保留正确。同 section 第 9624-9625 行中该 ego 名称与关键字译为「抓握之」「抓握」（`of grasping` / `grasping`），此处译为「抓取藤蔓」，两者在用词上存在细微不一致（「抓握」vs「抓取」），但不影响游戏实际含义理解。

#### entry-00853
- **位置/条目**：`mod-tome.lua:9637`（`entry-00853`）
- **原文**：`#YELLOW#%s has their %s spell disrupted for for %d turns!`
- **译文**：`#YELLOW#%s的%s法术被干扰%d回合！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/ammo.lua` 第 351 行（`inquisitor's ` ego 触发时日志）。英文原文包含双词笔误（`for for %d turns`），译文处理为「被干扰%d回合！」，占位符 `%s`（目标）、`%s`（法术名）、`%d`（回合数）顺序与类型完全对应，颜色代码 `#YELLOW#` 正确保留。

#### entry-00854
- **位置/条目**：`mod-tome.lua:9644`（`entry-00854`）
- **原文**：`thought`
- **译文**：`思维`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/ammo.lua` 第 406 行 `thought-forged `（思维锻造的）的关键词 `keywords = {thought=true}`。对应准确。

#### entry-00855
- **位置/条目**：`mod-tome.lua:9651`（`entry-00855`）
- **原文**：`#YELLOW#%s has temporarily forgotten %s for %d turns!`
- **译文**：`#YELLOW#%s暂时遗忘了%s，持续%d回合！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/ammo.lua` 第 462 行（`of amnesia` ego 触发打断技能日志）。三个占位符 `%s`（目标）、`%s`（技能名）、`%d`（回合数）顺序正确，颜色码 `#YELLOW#` 及标点符号完整。

#### entry-00856
- **位置/条目**：`mod-tome.lua:9685`（`entry-00856`）
- **原文**：`cleansing `
- **译文**：`洁净的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/amulets.lua` 第 211 行 `name = "cleansing ", prefix=true`。完全符合术语快照规则（`cleansing ` 前缀名首选「洁净的」）。

#### entry-00857
- **位置/条目**：`mod-tome.lua:9686`（`entry-00857`）
- **原文**：`cleansing`
- **译文**：`洁净`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/amulets.lua` 第 212 行 `keywords = {cleansing=true}`。完全符合术语快照规则（`cleansing` 关键词首选「洁净」）。

#### entry-00858
- **位置/条目**：`mod-tome.lua:9739`（`entry-00858`）
- **原文**：`cleansing `
- **译文**：`洁净的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/armor.lua` 第 96 行护甲前缀 `name = "cleansing "`。符合术语规范。

#### entry-00859
- **位置/条目**：`mod-tome.lua:9740`（`entry-00859`）
- **原文**：`cleansing`
- **译文**：`洁净`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/armor.lua` 第 97 行 `keywords = {cleansing=true}`。符合术语规范。

#### entry-00860
- **位置/条目**：`mod-tome.lua:9757`（`entry-00860`）
- **原文**：` of delving`
- **译文**：`挖掘之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/armor.lua` 第 239 行 `name = " of delving", suffix=true`。后缀名称翻译标准规范。

#### entry-00861
- **位置/条目**：`mod-tome.lua:9758`（`entry-00861`）
- **原文**：`delving`
- **译文**：`挖掘`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/armor.lua` 第 240 行 `keywords = {delving=true}`。与词缀名对应一致。

#### entry-00862
- **位置/条目**：`mod-tome.lua:9775`（`entry-00862`）
- **原文**：`cleansing `
- **译文**：`洁净的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/belt.lua` 第 41 行腰带前缀 `name = "cleansing "`。符合术语规范。

#### entry-00863
- **位置/条目**：`mod-tome.lua:9776`（`entry-00863`）
- **原文**：`cleansing`
- **译文**：`洁净`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/belt.lua` 第 42 行 `keywords = {cleansing=true}`。符合术语规范。

#### entry-00864
- **位置/条目**：`mod-tome.lua:9833`（`entry-00864`）
- **原文**：` of tirelessness`
- **译文**：`不倦之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/boots.lua` 第 26 行鞋类后缀 `name = " of tirelessness", suffix=true`。机制为增加耐力与耐力回复，译为「不倦之」贴切准确。

#### entry-00865
- **位置/条目**：`mod-tome.lua:9834`（`entry-00865`）
- **原文**：`tireless`
- **译文**：`不倦`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/boots.lua` 第 27 行 `keywords = {tireless=true}`。与后缀名对应一致。

#### entry-00866
- **位置/条目**：`mod-tome.lua:9858`（`entry-00866`）
- **原文**：`restorative`
- **译文**：`疗愈`
- **复核结论**：细微观察
- **可核验依据**：源码 `egos/boots.lua` 第 204-205 行前缀 `restorative `（增加治疗系数与生命回复），关键字为 `keywords = {restorative=true}`。同 section 第 9857 行前缀名称译为「振奋的」（`restorative `），而关键字（第 9858 行）译为「疗愈」。虽然「疗愈」机制上准确贴合治疗与生命回复，但与前缀名称用词存在分歧。

#### entry-00867
- **位置/条目**：`mod-tome.lua:9875`（`entry-00867`）
- **原文**：` of force`
- **译文**：`威能之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/boots.lua` 第 363 行后缀 `name = " of force", suffix=true`。机制同时提供法术强度、物理伤害与精神强度，译为「威能之」契合全面增伤机制。

#### entry-00868
- **位置/条目**：`mod-tome.lua:9876`（`entry-00868`）
- **原文**：`force`
- **译文**：`威能`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/boots.lua` 第 364 行 `keywords = {force=true}`。与后缀名对应一致。

#### entry-00869
- **位置/条目**：`mod-tome.lua:9885`（`entry-00869`）
- **原文**：`dreamer's `
- **译文**：`梦者的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/boots.lua` 第 441 行超能系前缀 `name = "dreamer's "`。增加灵巧与意志，译为「梦者的」准确。

#### entry-00870
- **位置/条目**：`mod-tome.lua:9886`（`entry-00870`）
- **原文**：`dreamer`
- **译文**：`梦者`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/boots.lua` 第 442 行 `keywords = {dreamer=true}`。与前缀名对应一致。

#### entry-00871
- **位置/条目**：`mod-tome.lua:9934`（`entry-00871`）
- **原文**：`cleansing `
- **译文**：`洁净的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/charms.lua` 第 338、354 行图腾/护符前缀 `name = "cleansing "`。符合术语规范。

#### entry-00872
- **位置/条目**：`mod-tome.lua:9935`（`entry-00872`）
- **原文**：`cleansing`
- **译文**：`洁净`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/charms.lua` 第 339、355 行 `keywords = {cleansing=true}`。符合术语规范。

#### entry-00873
- **位置/条目**：`mod-tome.lua:9973`（`entry-00873`）
- **原文**：`restorative`
- **译文**：`疗愈`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/cloak.lua` 第 193-194 行披风自然前缀 `restorative `（提供治疗系数、生命回复与自然/枯萎抗性），关键字为 `keywords = {restorative=true}`。同 section 第 9972 行前缀名同样译为「振奋的」，而此处关键字为「疗愈」，与 entry-00866 情况一致，存在前缀名与关键字用词差异。

#### entry-00874
- **位置/条目**：`mod-tome.lua:9978`（`entry-00874`）
- **原文**：` of sorcery`
- **译文**：`咒术之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/cloak.lua` 第 251 行奥术后缀 `name = " of sorcery", suffix=true`。增加魔力、意志与法术暴击，译为「咒术之」准确。

#### entry-00875
- **位置/条目**：`mod-tome.lua:9979`（`entry-00875`）
- **原文**：`sorcery`
- **译文**：`咒术`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/cloak.lua` 第 252 行 `keywords = {sorcery=true}`。与后缀名对应一致。

#### entry-00876
- **位置/条目**：`mod-tome.lua:9982`（`entry-00876`）
- **原文**：`spellcowled `
- **译文**：`法术兜帽的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/cloak.lua` 第 285 行披风前缀 `name = "spellcowled "`。cowl 为兜帽，机制增加魔力、意志与法术抗性，译为「法术兜帽的」准确对应。

#### entry-00877
- **位置/条目**：`mod-tome.lua:10006`（`entry-00877`）
- **原文**：` of delving`
- **译文**：`挖掘之`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/digger.lua` 第 12 行挖掘工具后缀 `name = " of delving", suffix=true`。增加视野范围与力体属性，译为「挖掘之」规范统一。

#### entry-00878
- **位置/条目**：`mod-tome.lua:10007`（`entry-00878`）
- **原文**：`delving`
- **译文**：`挖掘`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/digger.lua` 第 13 行 `keywords = {delving=true}`。与后缀名对应一致。

#### entry-00879
- **位置/条目**：`mod-tome.lua:10024`（`entry-00879`）
- **原文**：`bloodhexed `
- **译文**：`血邪术的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/digger.lua` 第 121 行奥术前缀 `name = "bloodhexed "`。增加力量、意志、物暴与心暴，译为「血邪术的」准确。

#### entry-00880
- **位置/条目**：`mod-tome.lua:10025`（`entry-00880`）
- **原文**：`bloodhexed`
- **译文**：`血邪术`
- **复核结论**：未发现问题
- **可核验依据**：源码 `egos/digger.lua` 第 122 行 `keywords = {bloodhexed=true}`。与前缀名对应一致。

#### entry-00881
- **位置/条目**：`mod-tome.lua:10051`（`entry-00881`）
- **原文**：`natural`
- **译文**：`自然`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/general/objects/egos/gloves.lua` 第 58-59 行 `name = "naturalist's ", prefix=true; keywords = {natural=true}`。前缀名称（第 10050 行）译为「自然主义者的」，而该词缀绑定的关键字为 `natural`。术语快照备注指出 `entity keyword 语境可指“自然主义者”`。此处译为「自然」符合字面本义，但与前缀名称及术语库关于该语境的提示略有出入。

---

### 复核总结
- **全部 40 条已核验完毕**（`entry-00842` 至 `entry-00881`）。
- **未发现硬性结构性问题**：所有占位符（`%s`, `%d`）、颜色码（`#00FF00#`, `#YELLOW#`）、标点及参数顺序均完整准确；符合术语库约束的条目（如 `cleansing` 系列）均准确对齐首选术语。
- **记录 4 处细微观察**：
  1. `entry-00843`：`capacity for exercising` 略省作「核心技能的能力」。
  2. `entry-00852`：`grasping vines` 译作「抓取藤蔓」，与同 section ego 名称「抓握之」用词略有出入。
  3. `entry-00866` 与 `entry-00873`：`restorative` 关键字译作「疗愈」，与同 section 前缀名「振奋的」用词不一致。
  4. `entry-00881`：`natural` 作为 `naturalist's ` 的关键字译作「自然」，术语快照备注提示该处可指「自然主义者」。