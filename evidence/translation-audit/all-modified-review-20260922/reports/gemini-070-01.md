### 校验前置信息

- **复核批次**：`batch-070`
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-070.md`
- **文件 SHA-256 校验**：
  - 预期值：`c4f780543deeea2f18bb1045e6e7acf907497c2b899cb0a9dc1b89e0e6317b71`
  - 实测值：`c4f780543deeea2f18bb1045e6e7acf907497c2b899cb0a9dc1b89e0e6317b71`
  - 结论：**完全一致**
- **复核范围**：`entry-02188` 至 `entry-02227`（共 40 条）
- **核验基准**：
  - 引擎源码固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 译文基准 commit：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

### 逐条复核报告

#### entry-02188
- **条目位置**：`mod-tome.lua:28416` (`mod-tome/data/talents/spells/conveyance.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 `conveyance.lua` line 147 中 `game.logPlayer(self, "The targetted teleport fizzles and works randomly!")`，译文「传送定位失败了，变为随机传送！」准确表达法术失灵转为随机传送机制，感叹号标点一致。

#### entry-02189
- **条目位置**：`mod-tome.lua:28417` (`mod-tome/data/talents/spells/conveyance.lua`)
- **复核结果**：细微观察
- **核验依据**：
  1. 占位符核对：原文 3 个 `%d` 分别对应 `range, radius, t.minRange`，译文中 3 个 `%d` 顺序与类型完全吻合。
  2. 细节观察：
     - 原文第 2 行 `allows you to specify which creature to teleport`，译文增译了说明括号「（怪物或被护送者）」，源码并无此修饰。
     - 原文第 5 行 `Random teleports have a minimum range of %d.`，译文将 minimum range 译为「最小半径」，实际机制为避免随机传送到自身过近距离的最小距离（`target:teleportRandom(x, y, t.getRange(self, t), t.minRange)`）。整体不影响核心理解。

#### entry-02190
- **条目位置**：`mod-tome.lua:28429` (`mod-tome/data/talents/spells/conveyance.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 `conveyance.lua` line 214，占位符 `%d%%`、`%d`、`%d` 分别传入 `chance, maxabsorb, duration`，译文占位符格式与顺序完全对应，伤害转移与护盾破裂条件表述准确。

#### entry-02191
- **条目位置**：`mod-tome.lua:28437` (`mod-tome/data/talents/spells/conveyance.lua`)
- **复核结果**：细微观察
- **核验依据**：占位符 `%d` 与 `%d%%` 数量格式正确；首句 `When you hit a solid surface` 译为「当你击中一个固体表面时」，实际是行走撞入障碍物（墙体）触发穿墙，略带字面直译痕迹，但结合后文「成功穿越」不影响理解。

#### entry-02192
- **条目位置**：`mod-tome.lua:28450` (`mod-tome/data/talents/spells/death.lua`)
- **复核结果**：存在疑点
- **核验依据**：原文第 2 行 `reduce its global speed by 25%% for one turn per effect (up to a maximum of %d)`，机制为目标身上每有 1 个负面效果，减速持续时间就增加 1 回合（最高 %d 回合）。译文表述为「并降低其全局速度 25%% 1回合（最大 %d 回合）」，漏译了关键修饰 `per effect`（每个效果持续 1 回合），且「25%% 1回合」紧挨缺乏衔接词，导致语意产生歧义（像是固定 1 回合与括号内最大回合产生矛盾）。

#### entry-02193
- **条目位置**：`mod-tome.lua:28477` (`mod-tome/data/talents/spells/death.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码传参顺序为暗影抗性 (%d)、护甲 (%d)、防御 (%d)、霜暮伤害 (%0.2f)、范围 (%d)。译文调整为先范围后伤害，元数据正确标注声明了 `args_order：[1, 2, 3, 5, 4]`，重排与译文占位符顺序完全吻合，机制描述准确。

#### entry-02194
- **条目位置**：`mod-tome.lua:28496` (`mod-tome/data/talents/spells/deeprock.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 `deeprock.lua` line 61 格式化参数共 7 个（`%d`, `%s`, `%0.1f%%`, `%0.1f%%`, `%s`, `%d`, `%s`），分别对应持续时间、抗性免疫字串、物伤加成、物穿加成、联动伤害字串、护甲加成及物抗生效字串。译文 7 个占位符与转义百分号严格匹配，顺序无误。

#### entry-02195
- **条目位置**：`mod-tome.lua:28507` (`mod-tome/data/talents/spells/deeprock.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 77，占位符 `%0.1f%%`、`%0.1f%%`、`%s` 对应奥术伤害、奥术抗穿及火山技能描述，译文顺序与术语完全吻合。

#### entry-02196
- **条目位置**：`mod-tome.lua:28511` (`mod-tome/data/talents/spells/deeprock.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 90，占位符 `%0.1f%%`、`%0.1f%%`、`%s` 对应自然伤害、自然抗穿及投掷巨石描述，译文顺序与术语完全吻合。

#### entry-02197
- **条目位置**：`mod-tome.lua:28545` (`mod-tome/data/talents/spells/divination.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 `divination.lua` line 105，占位符 `%d` 对应探图半径（magicMap），译文「有效范围：%d 码」表述清晰准确。

#### entry-02198
- **条目位置**：`mod-tome.lua:28627` (`mod-tome/data/talents/spells/eldritch-shield.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 34 前置检查日志，技能 Eldritch Blow 对应「奥术盾击」，提示无盾牌不可使用，感叹号标点一致。

#### entry-02199
- **条目位置**：`mod-tome.lua:28646` (`mod-tome/data/talents/spells/eldritch-shield.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 125 前置检查日志（源码为 `Eldricth Fury`），技能对应「奥术连击」，译文准确传达无盾牌不可使用。

#### entry-02200
- **条目位置**：`mod-tome.lua:28647` (`mod-tome/data/talents/spells/eldritch-shield.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 145，`%s resists the dazing blows!`，占位符 `%s` 保留，daze 严格遵循术语库 preferred 译为「眩晕」，「%s抵抗了眩晕打击！」无误。

#### entry-02201
- **条目位置**：`mod-tome.lua:28654` (`mod-tome/data/talents/spells/eldritch-shield.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 167 前置检查日志，技能 Eldritch Slam 对应「奥术猛击」，提示无盾牌不可使用，标点准确。

#### entry-02202
- **条目位置**：`mod-tome.lua:28667` (`mod-tome/data/talents/spells/eldritch-stone.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 74，嵌入字符串包含 `%0.1f` 与 `%d%%`，分别对应自然伤害与治疗减免比例，译文格式与百分号转义完全对应。

#### entry-02203
- **条目位置**：`mod-tome.lua:28699` (`mod-tome/data/talents/spells/energy-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 64 战斗日志，`%s` 对应傀儡名称，充能减少技能冷却机制描述准确。

#### entry-02204
- **条目位置**：`mod-tome.lua:28700` (`mod-tome/data/talents/spells/energy-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 69，占位符 `%d%%` 与 `%d` 对应概率与减少冷却回合数；Lightning Infusion 对应术语库 preferred「闪电充能」，机制完全契合。

#### entry-02205
- **条目位置**：`mod-tome.lua:28704` (`mod-tome/data/talents/spells/energy-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 92，弹药检查日志，无占位符，译文「你需要在箭袋中装填炼金宝石。」准确。

#### entry-02206
- **条目位置**：`mod-tome.lua:28705` (`mod-tome/data/talents/spells/energy-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 125，占位符 4 个（`%d`, `%0.2f`, `%0.2f`, `%d`）分别对应半径、物理伤害、闪电伤害、缴械回合，顺序与类型完全吻合，术语「缴械」正确。

#### entry-02207
- **条目位置**：`mod-tome.lua:28713` (`mod-tome/data/talents/spells/energy-alchemy.lua`)
- **复核结果**：细微观察
- **核验依据**：
  1. 占位符核对：5 个参数（`+%d%%`, `%d`, `%0.1f`, `%d`, `%d%%`）在译文中分别对应移动速度、范围、闪电伤害、扣血阈值、获得回合能量，占位符完整无误。
  2. 表达观察：末尾 `gain %d%% of a turn` 译为「获得 %d%% 个额外回合」，源码机制为增加相当于单个回合行动能量的百分比（`turn * game.energy_to_act / 100`），文字表达尚可理解。

#### entry-02208
- **条目位置**：`mod-tome.lua:28780` (`mod-tome/data/talents/spells/eradication.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 166，占位符 `%0.1f%%`、`%d%%`、`%d%%` 对应暗影/寒冷伤害加成、抗性穿透及低血量吸血比例，生命少于 1 点时吸血结算机制描述准确。

#### entry-02209
- **条目位置**：`mod-tome.lua:28788` (`mod-tome/data/talents/spells/explosives.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 46 弹药检查日志，译文准确且与 entry-02205 完全一致。

#### entry-02210
- **条目位置**：`mod-tome.lua:28797` (`mod-tome/data/talents/spells/explosives.lua`)
- **复核结果**：细微观察
- **核验依据**：
  1. 占位符核对：2 个占位符 `%d%%` 与 `%d%%` 对应炸弹保护与外界元素抗性，数量与格式一致。
  2. 细节观察：原文第二句 `it also protects against all side effects of your bombs` 承接上文的保护对象（你、傀儡及友方），源码等级 5 判定 `target ~= self and target ~= golem`；译文表述为「保护你免疫……」，未明确提傀儡，但整体核心机制传达清晰。

#### entry-02211
- **条目位置**：`mod-tome.lua:28801` (`mod-tome/data/talents/spells/explosives.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 157，占位符 `%d`、`%d%%`、`%d%%` 分别对应半径、开阔地形加成（min*100）、狭窄受阻加成（max*100），译文将括号说明调整后语义通畅准确。

#### entry-02212
- **条目位置**：`mod-tome.lua:28848` (`mod-tome/data/talents/spells/fire.lua`)
- **复核结果**：存在疑点
- **核验依据**：条目 source_tag 为 `talent name`，对应法师火系一阶技能。术语快照明确记录 `Flame 火球术 T.GAME.TALENT talents talent name existing core`。当前译文为「火焰」，与术语库 preferred/existing 条目存在明确冲突。

#### entry-02213
- **条目位置**：`mod-tome.lua:28849` (`mod-tome/data/talents/spells/fire.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 80，占位符 `%0.2f` 对应 3 回合灼烧伤害，5 级穿透光束机制描述准确。

#### entry-02214
- **条目位置**：`mod-tome.lua:28884` (`mod-tome/data/talents/spells/frost-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 102，占位符 `%d`、`%0.1f`、`%d` 对应半径、寒冷伤害、定身回合，受影响生物行动但无法移动机制描述准确。

#### entry-02215
- **条目位置**：`mod-tome.lua:28890` (`mod-tome/data/talents/spells/frost-alchemy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 133，占位符 3 个 `%d%%` 对应 affinity、物理抗性、暴击减免几率。affinity 机制在源码中表现为受到该元素伤害时按比例回复生命，译文意译为「受到的……会治疗你」准确反映实际机制。

#### entry-02216
- **条目位置**：`mod-tome.lua:28945` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 114，战斗日志标记 `#Source#` 和 `#Target#` 保留完整，嘲讽机制准确。

#### entry-02217
- **条目位置**：`mod-tome.lua:28948` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 174，占位符 `%s` 匹配，Crush 依据术语快照译为「压碎」，「%s抵抗了压碎！」无误。

#### entry-02218
- **条目位置**：`mod-tome.lua:28976` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 258，战斗日志标记 `#Target#` 与 `#Source#` 保留完整，位移拉近描述准确。

#### entry-02219
- **条目位置**：`mod-tome.lua:28979` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 301，占位符 `%0.2f`、`%d`、`%d%%` 分别对应 DOT 伤害、光环持续回合、火抗加成，灼烧累加与友军免伤机制准确。

#### entry-02220
- **条目位置**：`mod-tome.lua:28989` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 328，占位符 `%d` 与 `%0.2f` 对应爆炸半径与伤害，主人死亡触发条件明确。

#### entry-02221
- **条目位置**：`mod-tome.lua:28995` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 349，占位符 `%s`、`%d`、`%d%%`、`%d%%` 分别接收增减动词（Increases/Decreases）、护甲值、护甲硬度、暴击减免，重甲与板甲对应准确。

#### entry-02222
- **条目位置**：`mod-tome.lua:29000` (`mod-tome/data/talents/spells/golem.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 377，占位符 `%d` 对应毒伤数值，魔力（Magic）加成描述准确。

#### entry-02223
- **条目位置**：`mod-tome.lua:29032` (`mod-tome/data/talents/spells/golemancy.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 77，占位符 `%d`、`%d`、`%d%%` 对应命中、物理强度、伤害加成。Physical Power 严格遵循术语快照 preferred 译为「物理强度」。

#### entry-02224
- **条目位置**：`mod-tome.lua:29067` (`mod-tome/data/talents/spells/grave.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 105，占位符 `%d`、`%0.2f`、`%d` 对应初始半径、每回合寒伤、最大叠加层数，叠层扩径与低血量初始层数机制完全对齐。

#### entry-02225
- **条目位置**：`mod-tome.lua:29079` (`mod-tome/data/talents/spells/grave.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 125，颜色码 `#STEEL_BLUE#` 保留完整，坍缩/爆炸日志提示无误。

#### entry-02226
- **条目位置**：`mod-tome.lua:29080` (`mod-tome/data/talents/spells/grave.lua`)
- **复核结果**：未发现问题
- **核验依据**：源码 line 133，占位符 `%0.2f` 对应内爆寒伤，颜色码 `#PURPLE#` 完整保留；文末提及的技能名「Corpselight」精准指称同树技能「阴燃鬼火」，前后文对应严谨。

#### entry-02227
- **条目位置**：`mod-tome.lua:29143` (`mod-tome/data/talents/spells/master-necromancer.lua`)
- **复核结果**：存在疑点
- **核验依据**：
  1. 占位符核对：5 个占位符（`%d`, `%d%%`, `%d`, `%d`, `%d`）分别对应随从加速回合、非食尸鬼治疗百分比、缩短食尸鬼时间、延长尸爆/液化时间、敌人眩晕回合，顺序类型完全匹配。
  2. 术语疑点：原文第 6 行 `All non-undead foes caught inside are dazed for %d turns.`，译文写为「范围内所有非不死生物的敌人都会被茫然 %d 回合。」。术语快照明确规定 `daze 眩晕 T.GAME.EFFECT combat effect subtype preferred global 与 stun=震慑 区分`，同批次 entry-02200 亦采用「眩晕」，此处使用旧译「茫然」与术语库 preferred 规范及批内一致性存在冲突。

---

### 复核摘要统计

- **复核总数**：40 条 (`entry-02188` ～ `entry-02227`)
- **未发现问题**：34 条
- **细微观察**：4 条 (`entry-02189`, `entry-02191`, `entry-02207`, `entry-02210`)
- **存在疑点**：2 条 (`entry-02192`, `entry-02212`, `entry-02227`，共 3 处疑点)
  1. **entry-02192**：`death.lua` 中漏译 `per effect`（每个效果持续 1 回合），导致「25%% 1回合（最大 %d 回合）」出现机制歧义与语病。
  2. **entry-02212**：`fire.lua` 中技能名 `Flame` 译为「火焰」，与术语快照明确指定的 `Flame -> 火球术 (talent name)` 冲突。
  3. **entry-02227**：`master-necromancer.lua` 中状态名 `dazed` 译为「茫然」，与术语库 preferred 规范 `daze -> 眩晕` 及批内统一性冲突。