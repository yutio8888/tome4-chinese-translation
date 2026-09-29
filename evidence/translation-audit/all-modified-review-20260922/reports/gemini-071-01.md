### 批次校验与前置核验

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-071.md`
- **文件 SHA-256 核验**：`bcc1621d47bddc767baaf083018f61b240628330b3080a34e13932518b8d654d`（校验一致）
- **条目范围**：`entry-02228` 至 `entry-02267`，共 40 条
- **源码基准**：公开源码仓库 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`
- **译文基准**：`mod-tome.lua`（对应固定版本 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`）

---

### 逐条复核报告

#### entry-02228
- **位置**：`mod-tome.lua:29163`（`mod-tome/data/talents/spells/master-necromancer.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Suffer For Me（替我受苦）的回调日志输出 `game:delayedLogDamage(src, self, 0, ("#GREY#(%d to minion: %s)#LAST#"):tformat(remain, m:getName()), false)`。占位符 `%d`（分摊伤害值）与 `%s`（随从名称）顺序完全一致，颜色控制码 `#GREY#` 与 `#LAST#` 闭合完整，括号保留准确。

#### entry-02229
- **位置**：`mod-tome.lua:29183`（`mod-tome/data/talents/spells/master-of-bones.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能名称 `Call of the Crypt`，译为“地宫召唤”，与死灵技能体系命名习惯（如 Call of the Mausoleum 陵园召唤）规范统一。

#### entry-02230
- **位置**：`mod-tome.lua:29184`（`mod-tome/data/talents/spells/master-of-bones.lua`）
- **结论**：未发现问题
- **核验依据**：源码调用 `tformat(t:_getNb(self), math.max(1, self.level + t:_getLevel(self)), t:_getMax(self, true))`。三个 `%d` 占位符按召唤上限、随从等级、掌控上限的顺序严格对应；样式标签 `#GREY##{italic}#...#{normal}#` 闭合无误；换行及首行缩进格式匹配。技能等级 3 改为武装骷髅战士、等级 5 每 3 个战士额外召法师/弓箭手且超限退魂的机制与源码逻辑一致。

#### entry-02231
- **位置**：`mod-tome.lua:29199`（`mod-tome/data/talents/spells/master-of-bones.lua`）
- **结论**：未发现问题
- **核验依据**：源码调用 `tformat(self:getTalentRadius(t), t:_getDamage(self), t:_getHealth(self), t:_getArmor(self), t:_getRetaliation(self))`。5 个占位符 `%d`、`%0.2f`、`%d`、`%d`、`%0.2f` 依次对应半径、流血伤害、生命加成、护甲加成及反击伤害，顺序与类型完全一致。机制中友方随从强化与敌方流血判断准确。

#### entry-02232
- **位置**：`mod-tome.lua:29277`（`mod-tome/data/talents/spells/master-of-flesh.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Putrescent Liquefaction，调用 `tformat(t:_getNb(self), self:getTalentRadius(t), t:_getIncrease(self), damDesc(self, DamageType.FROSTDUSK, t:_getDamage(self)))`。4 个占位符 `%d`、`%d`、`%d`、`%0.2f` 按粉碎上限、云雾半径、每只延长时间、霜暮伤害数值严格匹配；机制中优先选择最老食尸鬼及每被云雾吸收 2 只恢复 1 点灵魂均与源码相符。

#### entry-02233
- **位置**：`mod-tome.lua:29323`（`mod-tome/data/talents/spells/meta.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Spellcraft（法术掌控），调用 `tformat(cooldownred * 100, chance, self:combatTalentSpellDamage(t, 10, 320) / 4)`。3 个动态占位符 `%d%%`、`%d%%`、`%d` 及 1 处硬编码转义百分号 `20%%` 全部保留并正确转义，冷却缩减、友伤空隙概率和法术冲击降抗效果描述与源码一致。

#### entry-02234
- **位置**：`mod-tome.lua:29329`（`mod-tome/data/talents/spells/meta.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Energy Alteration，调用 `tformat(t:_getPct(self))`。占位符 `%d%%` 转义正确；源码中 `death_note.source_talent_mode == "active"` 和持续 6 回合元素转化的机制描述准确，不覆盖自身及仅由直接释放法术触发的限定条件无遗漏。

#### entry-02235
- **位置**：`mod-tome.lua:29335`（`mod-tome/data/talents/spells/meta.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Metaflow，调用 `tformat(talentcount, maxlevel, t:_getDur(self))`。3 个 `%d` 占位符按重置数量、技能阶层上限、爆发持续回合依次对应；非固定冷却限制及技能等级视为 +1 级的机制表述准确。

#### entry-02236
- **位置**：`mod-tome.lua:29363`（`mod-tome/data/talents/spells/necrosis.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Runeskin（符文皮肤），调用 `tformat(t.getLifeBonus(self, t), t.getCrit(self, t), bonus)`。占位符 `-%d`（生命底线/致死下限降低值）、`%0.1f%%`（法暴加成）、`%s`（当前激活状态文本）顺序与格式完整吻合；术语 infusion 译为“纹身”、rune 译为“符文”符合死灵法师无自然纹身限制语境。

#### entry-02237
- **位置**：`mod-tome.lua:29370`（`mod-tome/data/talents/spells/necrosis.lua`）
- **结论**：未发现问题
- **核验依据**：源码技能名 `Spikes of Decrepitude`，译为“衰老尖刺”，符合 decrepitude（衰老/衰弱）与死灵派系译名规范。

#### entry-02238
- **位置**：`mod-tome.lua:29371`（`mod-tome/data/talents/spells/necrosis.lua`）
- **结论**：未发现问题
- **核验依据**：源码调用 `tformat(damDesc(self, DamageType.FROSTDUSK, t.getDamage(self, t)), t.getReduce(self, t))`。占位符 `%0.2f`（霜暮伤害）与 `%d%%`（降伤百分比，已转义）顺序一致；源码中每枚符文随机攻击 1 名敌人、每回合每敌人限 1 次、生命低于 1 时附加降伤状态的机制完全吻合。

#### entry-02239
- **位置**：`mod-tome.lua:29415`（`mod-tome/data/talents/spells/phantasm.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Illuminate，调用 `tformat(radius, damDesc(self, DamageType.LIGHT, dam), turn)`。占位符 `%d`、`%0.2f`、`%d` 顺序准确。源码中 `damDesc` 仅返回数值，实际伤害类型为 `DamageType.LIGHT`，译文显式补充“点光系伤害”提升了可读性且与代码一致；等级 3 致盲除施法者外生物的机制准确。

#### entry-02240
- **位置**：`mod-tome.lua:29486`（`mod-tome/data/talents/spells/rime-wraith.lua`）
- **结论**：未发现问题
- **核验依据**：源码对应技能 Permafrost，调用 `tformat(t:_getSaves(self), t:_getSaves(self))`。两个 `%d` 占位符对应豁免加减数值，两处 `15%%` 百分号均转义完整。友方提升治疗系数、敌方冷却延长 15% 的等级 5 额外效果与源码一致。

#### entry-02241
- **位置**：`mod-tome.lua:29498`（`mod-tome/data/talents/spells/spectre.lua`）
- **结论**：未发现问题
- **核验依据**：源码在检测视线或地形阻挡失败时调用 `game.logPlayer(self, "You do not have line of sight.")`。译文“你没有视线。”与仓库同类视线判定日志译法完全一致。

#### entry-02242
- **位置**：`mod-tome.lua:29499`（`mod-tome/data/talents/spells/spectre.lua`）
- **结论**：未发现问题
- **核验依据**：源码在瞬移失败时记录 `game.logSeen(self, "%s's ghost walk fizzles!", self.name:capitalize())`。占位符 `%s` 正常保留，技能名“游魂行走”及感叹号标点对应完整。

#### entry-02243
- **位置**：`mod-tome.lua:29519`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/arcane` 的描述，译文“用奥术操控魔法源能量，使你能用此能量进行攻击和防御。”忠实表达原文意义。

#### entry-02244
- **位置**：`mod-tome.lua:29521`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/aether` 的描述，译文“释放以太的核心力量，将敌人毁灭。”准确传达原意。

#### entry-02245
- **位置**：`mod-tome.lua:29523`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/fire` 的描述，译文“使用火的威力将你的目标烧成灰烬。”准确传达原意。

#### entry-02246
- **位置**：`mod-tome.lua:29525`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/wildfire` 的描述。术语规范规定技能树名用“焱”，普通描述按语境译为“野火”；译文“使用野火的威力将你的目标烧成灰烬。”完全符合该规则。

#### entry-02247
- **位置**：`mod-tome.lua:29527`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/earth` 的描述，译文“使用土的力量进行攻击和防御。”语义完整通顺。

#### entry-02248
- **位置**：`mod-tome.lua:29529`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/stone` 的描述，译文“使用石的力量进行攻击和防御。”与土系句式统一，语义准确。

#### entry-02249
- **位置**：`mod-tome.lua:29531`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/water` 的描述，译文“使用水的力量淹死目标。”忠实原意。

#### entry-02250
- **位置**：`mod-tome.lua:29533`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/ice` 的描述，译文“使用冰的力量冰冻并粉碎你的目标。”准确对应 freeze and shatter。

#### entry-02251
- **位置**：`mod-tome.lua:29535`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/air` 的描述，原文“fry your foes”结合闪电/空气系特色意译为“轰击你的目标”，符合中文行文习惯。

#### entry-02252
- **位置**：`mod-tome.lua:29537`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：细微观察
- **核验依据**：源码为技能树 `spell/storm` 的描述 `Harness the power of the storm to incinerate your foes.`。译文为“使用风暴的力量打击你的目标。”。原文动词为 `incinerate`（焚化/化为灰烬，如火系 burn to ashes），译文意译为“打击”，语气略有弱化；但鉴于此处为技能分类风味描述，不影响技能机制理解。

#### entry-02253
- **位置**：`mod-tome.lua:29539`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/meta` 的描述，Meta 对应“超魔系”，译文“超魔系法术能改变魔法的效能。”准确。

#### entry-02254
- **位置**：`mod-tome.lua:29541`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/temporal` 的描述 `The school of time manipulation.`，译文“学习操控时间。”通顺准确。

#### entry-02255
- **位置**：`mod-tome.lua:29543`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/phantasm` 的描述，译文“掌控诡计与幻象之力。”准确对应 tricks and illusions。

#### entry-02256
- **位置**：`mod-tome.lua:29545`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/enhancement` 的描述，译文“用魔法强化你的身体。”准确通顺。

#### entry-02257
- **位置**：`mod-tome.lua:29547`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/thaumaturgy` 的描述（英文有拼写变体 pinacle），译文“施放法术的巅峰。”准确。

#### entry-02258
- **位置**：`mod-tome.lua:29549`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：细微观察
- **核验依据**：源码为技能树 `spell/conveyance` 的描述。译文“学习传送，使你能更快的旅行或者追踪目标。”中，“更快的”在语法上作为修饰动词“旅行”的状语，宜作“更快地”；但语义表达清晰无歧义。

#### entry-02259
- **位置**：`mod-tome.lua:29551`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：细微观察
- **核验依据**：源码为技能树 `spell/divination` 的描述。译文为“侦查技能可以使施放者能侦查周围环境，搜寻隐藏的东西。”，其中“可以使……能……”略有句式轻度累赘，但不影响理解。

#### entry-02260
- **位置**：`mod-tome.lua:29553`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/aegis` 的描述，译文“使用奥术力量进行治疗和防御。”准确。

#### entry-02261
- **位置**：`mod-tome.lua:29555`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/explosives` 的描述，译文“用宝石制造各种魔法炸弹。”忠实原意。

#### entry-02262
- **位置**：`mod-tome.lua:29559`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/golemancy` 的描述，译文“学习制造并提升你的傀儡。”准确。

#### entry-02263
- **位置**：`mod-tome.lua:29561`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/advanced-golemancy` 的描述，译文“高级傀儡操纵技巧。”准确。

#### entry-02264
- **位置**：`mod-tome.lua:29564`（`mod-tome/data/talents/spells/spells.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能树 `spell/fire-alchemy` 的描述，译文“操控火焰的炼金法术。”准确。

#### entry-02265
- **位置**：`mod-tome.lua:29638`（`mod-tome/data/talents/spells/staff-combat.lua`）
- **结论**：细微观察
- **核验依据**：源码对应技能 Blunt Thrust（钝器挥击）的施法前置检查 `if not weapon then game.logPlayer(self, "You cannot use Blunt Thrust without a staff weapon!")`。译文处理为“你需要一把法杖来施展该技能！”，将具体的技能名 `Blunt Thrust` 泛化代指为“该技能”，并意译为肯定祈使句（类似前置技能 Channel Staff 的提示信息）。该处理不影响玩家理解需装备法杖的前提，但省略了具体技能专名。

#### entry-02266
- **位置**：`mod-tome.lua:29639`（`mod-tome/data/talents/spells/staff-combat.lua`）
- **结论**：未发现问题
- **核验依据**：源码为技能 Blunt Thrust 击中但目标豁免震慑时的日志 `game.logSeen(target, "%s resists the stunning blow!", target:getName():capitalize())`。英文小写 `stunning blow` 描述此次造成震慑的一击，译文“%s抵抗了震慑打击！”占位符 `%s` 与标点保存完整，含义准确无误。

#### entry-02267
- **位置**：`mod-tome.lua:29640`（`mod-tome/data/talents/spells/staff-combat.lua`）
- **结论**：存在疑点
- **核验依据**：
  1. **标点缺失**：第二行英文原文为 `Stun chance will improve with Spellpower.`（句尾有英文句号），译文第二行为 `\t\t震慑概率受法术强度加成`，句末缺失中文句号。
  2. **术语不一致**：第一行英文 `melee damage` 在全仓库及同类技能中一贯译为“近战伤害”（经全库检索，“近战伤害”出现多处，而“近程伤害”在整个 `mod-tome.lua` 中仅此处出现一次），此处译作“近程伤害”偏离标准术语。
  3. 占位符 `%d%%` 与 `%d` 及等级 5 必中效果数值逻辑与源码吻合。