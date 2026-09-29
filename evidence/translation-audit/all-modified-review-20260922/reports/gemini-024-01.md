# batch-024 译文复核报告

### 1. 文件校验信息
- **复核批次**：`batch-024`
- **批次条目范围**：`entry-00922` 至 `entry-00962`（注：文件中无 `entry-00949`，总计 40 条）
- **批次文件 SHA-256 核验**：
  - 预期哈希：`33964b38e100032dd083f64703e4235a2b7acc033ecfac24e42cfcd29fdcac30`
  - 实测哈希：`33964b38e100032dd083f64703e4235a2b7acc033ecfac24e42cfcd29fdcac30`
  - 校验结果：**一致（PASS）**
- **源码参考基准**：
  - 核心/tome 源码 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（按 `source-access.json` 规则通过 `git -C /workspace/t-engine4 show <commit>:<path>` 读取）
  - 本批所有条目均来自 `mod-tome`，不涉及 DLC 或未定位源码的 addon。
  - 译文上下文基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 2. 逐条复核详情（共 40 条）

#### entry-00922
- **位置**：`mod-tome.lua:10866`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`entity keyword`
- **原文**：`daylight`
- **译文**：`日光`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:321-322` 定义 `name = " of daylight", suffix=true, keywords = {daylight=true}`；同 section 语境第 10865 行对应词缀全名译为“日光之”，关键字“日光”与词缀名一致且符合游戏语义。

---

#### entry-00923
- **位置**：`mod-tome.lua:10889`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`entity keyword`
- **原文**：`blaze`
- **译文**：`炽焰`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:501-502` 定义 `name = "blazebringer's ", prefix=true, keywords = {blaze=true}`；同 section 语境第 10888 行词缀全名译为“烈焰行者的”，关键字译为“炽焰”准确对应，未发现语义偏差。

---

#### entry-00924
- **位置**：`mod-tome.lua:10907`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`logSeen`
- **原文**：`#YELLOW#%s has their %s spell disrupted for for %d turns!`
- **译文**：`#YELLOW#%s的%s法术被干扰%d回合！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:686` 调用为 `game.logSeen(target, "#YELLOW#%s has their %s spell disrupted for for %d turns!", target:getName():capitalize(), t.name, turns)`。实参顺序依次为目标名（`%s`）、技能名（`%s`）与回合数（`%d`）。译文占位符数量与参数顺序严格一致；颜色代码 `#YELLOW#` 保持原样无末尾 `#LAST#`；英文原文源码中的“for for”连词笔误在译文中已正确消化为正常的“被干扰%d回合！”，未引入额外冗余。

---

#### entry-00925
- **位置**：`mod-tome.lua:10917`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`tformat`
- **原文**：`Projects up to %d attacks dealing 30%% weapon damage to other random targets in range 7 as mind damage (1/turn)`
- **译文**：`朝周围7格范围内的其他随机目标投射至多 %d 次攻击，每次造成 30%% 精神武器伤害（1次/回合）`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:766-787` 显示该词缀通过 `tformat(targets or 0)` 注入攻击次数，并在触发时调用 `who:attackTargetWith(project_target, combat, engine.DamageType.MIND, 0.3)`，范围为 `radius=7` 的 ball 投射。译文转义百分号 `30%%` 完整保留，占位符 `%d` 匹配，“精神武器伤害”符合武器附带特定属性转化的通用译法，频次限制与范围均准确传达。

---

#### entry-00926
- **位置**：`mod-tome.lua:10919`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`entity keyword`
- **原文**：`thought`
- **译文**：`思维`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:792-793` 定义 `name = "thought-forged ", prefix=true, keywords = {thought=true}`；同 section 第 10918 行词缀全名译为“思维锻造的”，关键字“思维”完全对应。

---

#### entry-00927
- **位置**：`mod-tome.lua:10923`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **Source Tag**：`logSeen`
- **原文**：`#YELLOW#%s has temporarily forgotten %s for %d turns!`
- **译文**：`#YELLOW#%s暂时遗忘了%s，持续%d回合！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `weapon.lua:844` 调用为 `game.logSeen(target, "#YELLOW#%s has temporarily forgotten %s for %d turns!", target:getName():capitalize(), t.name, turns)`。实参顺序为目标名（`%s`）、技能名（`%s`）、回合数（`%d`）。译文占位符类型与顺序对应无误，颜色代码 `#YELLOW#` 完整保留，句意准确。

---

#### entry-00928
- **位置**：`mod-tome.lua:10939`
- **Section**：`mod-tome/data/general/objects/egos/wizard-hat.lua`
- **Source Tag**：`entity name`
- **原文**：`cleansing `
- **译文**：`洁净的`
- **复核结论**：未发现问题
- **可核验依据**：源码 `wizard-hat.lua:98` 定义 `name = "cleansing ", prefix=true`；批次术语快照明确规定 `cleansing `（带尾空格）在 items 实体前缀名中首选译为“洁净的”，符合规范。

---

#### entry-00929
- **位置**：`mod-tome.lua:10940`
- **Section**：`mod-tome/data/general/objects/egos/wizard-hat.lua`
- **Source Tag**：`entity keyword`
- **原文**：`cleanse`
- **译文**：`洁净`
- **复核结论**：未发现问题
- **可核验依据**：源码 `wizard-hat.lua:99` 定义 `keywords = {cleanse=true}`；批次术语快照明确规定 `cleanse` 在核心装备 ego 的 keywords 语境中首选译为“洁净”，符合规范。

---

#### entry-00930
- **位置**：`mod-tome.lua:11005`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`A length of troll intestines. Fortunately, the troll appears to have eaten nothing in some time.`
- **译文**：`一截巨魔肠子。幸运的是，这只巨魔似乎已经有一段时间没吃东西了。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:31` 定义 `define_as = "TROLL_INTESTINE", desc = _t[[A length of troll intestines...]]`；术语 `troll` 准确对应“巨魔”，分句标点与幽默语调传达自然。

---

#### entry-00931
- **位置**：`mod-tome.lua:11018`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`entity name`
- **原文**：`vial of greater demon bile`
- **译文**：`一瓶大恶魔胆汁`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:83` 定义 `define_as = "GREATER_DEMON_BILE", name = "vial of greater demon bile"`；同 section 第 11019 行未鉴定名为“恶魔胆汁”，实体名称翻译准确。

---

#### entry-00932
- **位置**：`mod-tome.lua:11029`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`The severed front half of a minotaur snout, ring and all.`
- **译文**：`从米诺陶口鼻部割下来的前半截，连鼻环一起。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:116` 定义 `define_as = "MINOTAUR_NOSE"`，后文炼金师对白明确提及鼻环（"You'll need to find one with a ring"），译文“连鼻环一起”准确还原了“ring and all”的语义。

---

#### entry-00933
- **位置**：`mod-tome.lua:11039`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`entity name`
- **原文**：`honey tree root`
- **译文**：`蜂蜜树的根`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:159` 定义 `define_as = "HONEY_TREE_ROOT", name = "honey tree root"`；名称直译准确。

---

#### entry-00934
- **位置**：`mod-tome.lua:11041`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`The severed end of one of a honey tree's roots. It wriggles around occasionally, seemingly unwilling to admit that it's dead... and a *plant*.`
- **译文**：`从蜂蜜树的一根树根上切下来的断端。它偶尔会蠕动下，似乎不承认它已经死了，而且还是个“植物”。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:161` 物品描述中对 `*plant*` 的强调，译文使用中文双引号“植物”进行对等讽刺强调，省略号与转折语意处理得当。

---

#### entry-00935
- **位置**：`mod-tome.lua:11073`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`Unlike the rest of the black mamba, the severed head isn't moving.`
- **译文**：`不像黑曼巴的其余部分，这颗被斩下的头一动不动。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:182` 定义 `define_as = "BLACK_MAMBA_HEAD"`；生物名称黑曼巴及特征描述准确流畅。

---

#### entry-00936
- **位置**：`mod-tome.lua:11076`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`As unpleasant-looking as any exposed organ.`
- **译文**：`和任何外露的器官一样难看。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:193` 定义 `define_as = "SNOW_GIANT_KIDNEY"` 描述；简短描述忠实传达原文文意。

---

#### entry-00937
- **位置**：`mod-tome.lua:11088`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`_t`
- **原文**：`Looks much like any other rock, though this one was recently sentient and trying to murder you.`
- **译文**：`它看起来和其他石头没什么两样，只不过这块不久前还具有意识，并且曾试图杀死你。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:232` 定义 `define_as = "XORN_FRAGMENT"` 描述；精准表达了索尔石（xorn）作为活体岩石怪物的特征，行文自然。

---

#### entry-00938
- **位置**：`mod-tome.lua:11094`
- **Section**：`mod-tome/data/general/objects/elixir-ingredients.lua`
- **Source Tag**：`entity name`
- **原文**：`wretchling eyeball`
- **译文**：`小劣魔之眼`
- **复核结论**：未发现问题
- **可核验依据**：源码 `elixir-ingredients.lua:262` 定义 `define_as = "WRETCHLING_EYE", name = "wretchling eyeball"`；怪物 `wretchling` 译为“小劣魔”，名称翻译完全对齐。

---

#### entry-00939
- **位置**：`mod-tome.lua:11126`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity subtype`
- **原文**：`white`
- **译文**：`白色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:23` 基础定义 `newEntity{ define_as = "BASE_GEM", type = "gem", subtype="white", ...}`；宝石子分类为颜色“白色”，准确无误。

---

#### entry-00940
- **位置**：`mod-tome.lua:11132`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem subtype`
- **原文**：`white`
- **译文**：`白色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:83` 定义 `newGem("Diamond", ..., "white", ...)`；提取工具将其形参记录为 `gem subtype`，译为“白色”正确。

---

#### entry-00941
- **位置**：`mod-tome.lua:11137`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`alchemist gem`
- **原文**：`alchemist fire opal`
- **译文**：`炼金火蛋白石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 95` 在 `newGem` 中为 `ALCHEMIST_GEM_*` 生成 `name = "alchemist "..name:lower()`；翻译准确，与宝石名体系一致。

---

#### entry-00942
- **位置**：`mod-tome.lua:11138`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem name`
- **原文**：`fire opal`
- **译文**：`火蛋白石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:95` `newGem("Fire Opal", ...)` 参数提取为 `gem name`；中文标准宝石名称，准确无误。

---

#### entry-00943
- **位置**：`mod-tome.lua:11139`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem subtype`
- **原文**：`red`
- **译文**：`红色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:95` 火蛋白石对应颜色参数为 `red`，子类属性译为“红色”，准确无误。

---

#### entry-00944
- **位置**：`mod-tome.lua:11146`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem subtype`
- **原文**：`yellow`
- **译文**：`黄色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:107` `newGem("Amber", ..., "yellow", ...)` 琥珀对应颜色参数为 `yellow`，译为“黄色”准确。

---

#### entry-00945
- **位置**：`mod-tome.lua:11148`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem subtype`
- **原文**：`green`
- **译文**：`绿色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:111` `newGem("Turquoise", ..., "green", ...)` 绿松石对应颜色参数为 `green`，译为“绿色”准确。

---

#### entry-00946
- **位置**：`mod-tome.lua:11152`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`alchemist gem`
- **原文**：`alchemist sapphire`
- **译文**：`炼金蓝宝石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 119` `newGem("Sapphire", ...)` 生成炼金宝石名称，译为“炼金蓝宝石”标准规范。

---

#### entry-00947
- **位置**：`mod-tome.lua:11154`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`gem name`
- **原文**：`sapphire`
- **译文**：`蓝宝石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:119` 参数提取为 `gem name`，译为“蓝宝石”准确无误。

---

#### entry-00948
- **位置**：`mod-tome.lua:11159`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`alchemist gem`
- **原文**：`alchemist lapis lazuli`
- **译文**：`炼金青金石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 131` 定义 `newGem("Lapis Lazuli", ..., "blue", ...)`；条目本身译为“炼金青金石”符合矿物学与游戏设定，且与同 section 第 11160 行 `t("lapis lazuli", "青金石", "gem name")` 以及 entry-00958（第 11216 行）完全一致。
- **细微观察**：同 section 未在本批次中的第 11215 行存在 `t("lapis lazuli", "天青石", "entity name")`，而第 11160 行与本条采用“青金石”。本条译名“青金石”完全正确，此处仅作为同文件背景的用词观察记录。

---

#### entry-00950
- **位置**：`mod-tome.lua:11189`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`_t`
- **原文**：`Lights terrain (power 100)`
- **译文**：`照亮地形（强度100）`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:89` 中珍珠（Pearl）的炼金炸弹效果定义为 `{ splash={type="LITE", dam=100, desc = _t"Lights terrain (power 100)"} }`；术语快照关于 `power` 在效果属性语境首选为“强度”（区分于物品词缀“能量”），括号使用规范全角括号，准确无误。

---

#### entry-00951
- **位置**：`mod-tome.lua:11192`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity name`
- **原文**：`fire opal`
- **译文**：`火蛋白石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:63, 95` 生成宝石实体 `GEM_FIRE_OPAL` 的 `name = "fire opal"`，译名与 entry-00942 保持一致，标准正确。

---

#### entry-00952
- **位置**：`mod-tome.lua:11193`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity name`
- **原文**：`alchemist fire opal`
- **译文**：`炼金火蛋白石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 95` 生成炼金宝石实体 `ALCHEMIST_GEM_FIRE_OPAL` 的 `name = "alchemist fire opal"`，译名与 entry-00941 保持一致，标准正确。

---

#### entry-00953
- **位置**：`mod-tome.lua:11194`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity subtype`
- **原文**：`red`
- **译文**：`红色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:63, 72, 95` 中 `subtype = color`（即 "red"），作为实体的子类别属性译为“红色”，与 entry-00943 一致。

---

#### entry-00954
- **位置**：`mod-tome.lua:11201`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity subtype`
- **原文**：`yellow`
- **译文**：`黄色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:63, 72, 107` 琥珀实体对应 `subtype = color`（即 "yellow"），译为“黄色”，与 entry-00944 一致。

---

#### entry-00955
- **位置**：`mod-tome.lua:11204`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity subtype`
- **原文**：`green`
- **译文**：`绿色`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:63, 72, 111` 绿松石实体对应 `subtype = color`（即 "green"），译为“绿色”，与 entry-00945 一致。

---

#### entry-00956
- **位置**：`mod-tome.lua:11208`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity name`
- **原文**：`sapphire`
- **译文**：`蓝宝石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:63, 119` 生成宝石实体 `GEM_SAPPHIRE` 的 `name = "sapphire"`，与 entry-00947 一致。

---

#### entry-00957
- **位置**：`mod-tome.lua:11209`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity name`
- **原文**：`alchemist sapphire`
- **译文**：`炼金蓝宝石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 119` 生成炼金宝石实体 `ALCHEMIST_GEM_SAPPHIRE` 的 `name = "alchemist sapphire"`，与 entry-00946 一致。

---

#### entry-00958
- **位置**：`mod-tome.lua:11216`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`entity name`
- **原文**：`alchemist lapis lazuli`
- **译文**：`炼金青金石`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:72, 131` 生成炼金宝石实体 `ALCHEMIST_GEM_LAPIS_LAZULI` 的 `name = "alchemist lapis lazuli"`，译名与 entry-00948 完全一致，准确无误。（同前述细微观察，第 11215 行的 entity name 原为“天青石”，本条采用规范的“青金石”）。

---

#### entry-00959
- **位置**：`mod-tome.lua:11233`
- **Section**：`mod-tome/data/general/objects/gem.lua`
- **Source Tag**：`_t`
- **原文**：`Lights terrain (power 10)`
- **译文**：`照亮地形（强度10）`
- **复核结论**：未发现问题
- **可核验依据**：源码 `gem.lua:162` 中紫黄晶（Ametrine）的炼金炸弹效果定义为 `{ splash={type="LITE", dam=10, desc = _t"Lights terrain (power 10)"} }`；与 entry-00950 结构和用词严格对称，准确无误。

---

#### entry-00960
- **位置**：`mod-tome.lua:11273`
- **Section**：`mod-tome/data/general/objects/heavy-armors.lua`
- **Source Tag**：`entity name`
- **原文**：`stralite mail armour`
- **译文**：`斯莱特锁甲`
- **复核结论**：未发现问题
- **可核验依据**：源码 `heavy-armors.lua:67` 定义 `name = "stralite mail armour", short_name = "stralite"`；术语快照明确规定材质 `stralite` 统一为“斯莱特”（避免旧译“蓝皓石”），同 section 第 11267 至 11276 行中各类金属 `mail armour` 均规范统一为“锁甲”（铁锁甲、钢锁甲、矮人钢锁甲、沃瑞钽锁甲），本条完全契合规范。

---

#### entry-00961
- **位置**：`mod-tome.lua:11274`
- **Section**：`mod-tome/data/general/objects/heavy-armors.lua`
- **Source Tag**：`entity short_name`
- **原文**：`stralite`
- **译文**：`斯莱特`
- **复核结论**：未发现问题
- **可核验依据**：源码 `heavy-armors.lua:67` 定义 `short_name = "stralite"`；术语快照明确首选“斯莱特”，作为材质短名完全对齐。

---

#### entry-00962
- **位置**：`mod-tome.lua:11321`
- **Section**：`mod-tome/data/general/objects/jewelry.lua`
- **Source Tag**：`entity name`
- **原文**：`stralite ring`
- **译文**：`斯莱特戒指`
- **复核结论**：未发现问题
- **可核验依据**：源码 `jewelry.lua:58` 定义 `name = "stralite ring", unided_name = _t"stralite ring", short_name = "stralite"`；术语统一使用“斯莱特”，饰品名称结构一致，准确无误。

---

### 3. 总体复核结论摘要
- **覆盖率**：全部 40 条编号（`entry-00922` 至 `entry-00962`，无 `entry-00949`）均已逐条对照固定 commit 源码、运行机制、占位符及术语快照完成复核，无遗漏。
- **问题汇总**：40 条译文均未发现功能性阻断缺陷、语法错误或参数不匹配，占位符 `%s`/`%d`、转义百分号 `%%`、颜色代码 `#YELLOW#` 均准确保留。
- **观察项**：在 `mod-tome/data/general/objects/gem.lua` 中，本批次的 `entry-00948` 与 `entry-00958` 均准确将 `alchemist lapis lazuli` 翻译为规范的“炼金青金石”；同 section 外非本批次条目（第 11215 行）曾存在旧译“天青石”，后续全局校对时可留意该处未纳批条目的统一性。