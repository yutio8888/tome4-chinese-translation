### batch-066 译文复核报告

**文件哈希核验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-066.md` SHA-256 值为 `2fd7f5f42e02abd6e6097700caf4844b280950755028fe6b426e9cc7febc8356`，核验一致。  
**复核范围**：`entry-02028` 至 `entry-02067`，共 40 条。  
**源码基准**：公开固定源码 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/`）。  
**译文终点**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核记录

#### entry-02028
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2438`（`Bloodrage`）。占位符两个 `%d` 分别传入力量上限 `math.floor(self:getTalentLevel(t) * 6)` 与持续时间 `t.getDuration(self, t)`，译文占位符数量、类型与机制数值完全对应。但在文字风格与语义层面存在明显偏差：原文“Each time one of your foes bites the dust, you feel a surge of power”直译为“每当你的一个敌人倒下，你会感到一股力量涌出”，译文作“每当你让一个敌人扑街，你会漏出一股汹涌的霸气”，不仅使用了“扑街”等网络俚语，且将感知动词“feel”错译为“漏出”（疑为“露出/流出”笔误或过度戏谑化），偏离原文书面语境。

#### entry-02029
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2572`（`Shattering Charge`）。三个 `%d` 依次对应冲锋距离 `range`、伤害下限 `2*dam/3`、伤害上限 `dam`，5 级具有穿墙能力（源码调用 `DamageType.DIG`）。译文占位符数量类型完全匹配，换行及缩进 `\n\t\t` 保留完好，机制描述与源码一致。

#### entry-02030
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2725`（`Reload`）。占位符 `%d` 传入装填量 `self:reloadRate()`，技能不消耗能量（`action` 返回 `true` 且设缴械状态 `EFF_RELOAD_DISARMED`），潜行不打破（`no_break_stealth = true`）。译文占位符与格式（两处段落换行 `\n\t\t` 与 `\n\n\t\t`）均匹配，描述符合机制。

#### entry-02031
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2737`。双持技能名称 `Sweep`，标准译为“横扫”，符合既有习惯。

#### entry-02032
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2757`。触发日志原文为“You cannot use Sweep without dual wielding!”，明确指名技能“Sweep”，而译文作“你只有在双持状态下才能使用这个技能！”，省略了技能名称“横扫”（与前一行前置条件提示“You require two weapons to use this talent.”译文完全雷同）。虽不影响理解，但存在略缩。

#### entry-02033
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2935`（`Sticky Smoke`）。占位符两个 `%d` 依次对应爆炸半径 `self:getTalentRadius(t)` 与视野削减 `t.getSightLoss(self,t)`。机制中附加 `DamageType.STICKY_SMOKE`，使受影响生物无法阻止潜行，且自身不破潜行（`no_break_stealth = true`）。译文占位符、缩进与机制叙述一致。

#### entry-02034
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2962`（`Switch Place`）。战斗日志标签 `#Source#` 与 `#Target#` 标记完整闭合，地形阻挡换位逻辑与源码一致。

#### entry-02035
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:2975`（`Switch Place`）。占位符参数仅有持续时间 `%d`，`50%%` 为字面转义百分比。译文 `%d` 准确承接回合数，`50%%` 转义正确，机制中换位触发 0 伤害武器攻击以触发命中特效，译文表达准确。

#### entry-02036
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3033`（`Nimble Movements`）。消息标签 `@Source@` 保留正确，语义准确。

#### entry-02037
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3059`。技能名 `Hide in Plain Sight` 译为“明处潜行”，准确贴合机制。

#### entry-02038
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3106`（`Hide in Plain Sight`）。参数依次为倍率 `%0.2f`（`t.stealthMult`）、当前潜行强度 `%d`（`t.getChance(fake)`）、预估成功率 `%0.1f%%`（`t.getChance(estimate)`），中间包含每格降低 `10%%` 转义。译文字符格式、转义、占位符顺序与段落换行完全匹配。

#### entry-02039
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3133`（`Unseen Actions`）。参数依次为倍率 `%0.2f`、当前潜行强度 `%d`、预估成功率 `%0.1f%%`，并包含 `10%%` 与 `100%%` 转义。译文占位符类型与顺序严格对齐，段落缩进完整。

#### entry-02040
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3176`（`Mobile Defence`）。占位符两个 `%d%%` 依次对应闪避增益 `t.getDef * 100` 与护甲强度 `t.getHardiness`。机制于 `Combat.lua:1268`（`light_armor` 判定）生效，译文近身闪避与护甲强度表述准确。

#### entry-02041
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3250`（`Strider`）。占位符依次为移速 `%d%%` 与技能冷却缩减 `%d` 回合。所涉及技能 Hack'n'Back（燕回斩）、Rush（冲锋）、Disengage（逃脱）、Evasion（回避）名称全部对齐既有译名，参数顺序无误。

#### entry-02042
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3265`（`Charm Mastery`）。占位符 `%d%%` 对应护符冷却缩减。术语 charms（护符）、wands（魔杖）、totems（图腾）、torques（项圈）翻译均符合术语表标准。

#### entry-02043
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3300`（`Precision`）。原文日志为“You cannot use Precision without dual wielding!”，包含技能名称 Precision，译文作“你只有在双持状态下才能使用这个技能！”，省略了技能名称“弱点打击”。

#### entry-02044
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3325`（`Momentum` 前置条件）。原文为通用表述“this talent”，译文“你需要双持近战武器才能使用这个技能”准确无误。

#### entry-02045
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3330`（`Momentum` 激活日志）。原文 Momentum 正确指名译为“急速切割”，条件限制与逻辑对应准确。

#### entry-02046
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3477`（`Bone Nova`）。占位符依次为半径 `%d`、物理伤害 `%0.2f`、流血总伤害 `%0.2f`（源码中直接计算 `dam/2`），译文占位符格式、参数对应及缩进均一致。

#### entry-02047
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3525`（`Ambuscade` 空间不足日志）。译文“没有足够的空间召唤阴影！”表意清晰准确。

#### entry-02048
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3660`。诅咒系技能名 `Dismay` 译为“惊骇”，符合既有技能译名标准。

#### entry-02049
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3665`（`Dismay`）。占位符 `%0.1f%%`（概率）与 `%d`（持续回合）完全对应。机制附加的受影响状态名为 `EFF_DISMAYED`（在 `timed_effects/mental.lua:404` 中已统一译为“惊慌失措”），译文中“陷入惊慌失措”与该状态效果名称保持了一致。

#### entry-02050
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3746`（`Circle of Blazing Light`）。参数依次为半径 `%d`、正能量回复 `%d`、光伤害 `%0.2f`、火伤害 `%0.2f`、持续回合 `%d`，五个占位符类型与参数顺序严格对应。细微观察在于换行结构：原文首段句末的“The circle lasts %d turns.”在译文中被独立换行为“\t\t阵法持续 %d 回合。”，导致译文比原文多出一行缩进段落，但不影响数值渲染与参数匹配。

#### entry-02051
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/npcs.lua:3961`（`Cold Flames`）。占位符依次为生成点数 `%d`、扩散半径 `%d`、冰冷伤害 `%0.2f`。译文占位符、缩进与法强加成描述均与源码吻合。

#### entry-02052
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:124`（`Attune Mindstar`）。占位符 `%s` 接收物品名称，颜色标签 `#ORANGE#` 与 `#LAST#` 完整配对且位置准确。

#### entry-02053
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:232`（`Ward`）。占位符 `%s` 对应可用结界列表字符串。译文准确说明了护盾按次数抵消伤害的机制，换行与缩进一致。

#### entry-02054
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:330`（`Block` 的 `properties.sp` 拼接文本）。原文句首包含 1 个用于拼接到主描述的半角空格，占位符为 `%d`；译文句首准确保留了半角空格与 `%d`。

#### entry-02055
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:336`（`Block` 的 `properties.br` 拼接文本）。原文句首包含 1 个半角空格，译文准确保留句首空格，语义准确。

#### entry-02056
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:339`（`Block` 主技能描述）。占位符包括格挡值 `%d`、反击字面转义 `200%%`、抗性加成转义 `50%%`，末尾四个 `%s%s%s%s` 分别接收格挡属性字符串、豁免加成文本、反弹文本和治疗文本。译文占位符数量、类型、转义及顺序完全对齐源码。

#### entry-02057
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:568`（`Shivgoroth Form`）。占位符共 5 个：持续时间 `%d`、冰雪风暴等级 `%d`、割伤/震慑抗性 `%d%%`、寒冷抗性 `%d%%`、寒冷伤害治疗转化率 `%d%%`，顺序与类型完全对应。专有名词 shivgoroth 统一采用了术语规范“西弗格罗斯”（避免了“西弗戈洛斯”异译）。

#### entry-02058
- **判定**：存在疑点
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/objects.lua:670`（`Dagger Block`）。原文第一句为：“Raise your dagger into blocking position for one turn, reducing the damage of all physical melee attacks against you by %d.”，明确限定了受减免的伤害类型为“all physical melee attacks”（所有物理近战攻击）。而译文翻译为：“减少所有物理伤害 %d 点。”，漏译了关键限定词“近战”（melee）。虽然在底层 `EFF_BLOCKING` 机制中仅对 `DamageType.PHYSICAL` 做了类型过滤，但文本描述存在客观漏词，导致技能描述与英文原文存在不一致。

#### entry-02059
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:79`（`Overseer of Nations`）。参数依次为致盲免疫 `%d%%`、最大视野 `%d`、感应/夜视范围 `%d`。5 级触发同类生物心灵感应机制。译文占位符、段落缩进及机制叙述一致。

#### entry-02060
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:105`（`Born into Magic`）。参数依次为法术豁免 `%d`、奥术抗性 `%d%%`，包含 `20%%` 加成字面转义。专名“Age of Allure”准确对齐既有纪元术语“厄流纪”，“Conclave”译为“孔克雷夫”。

#### entry-02061
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:116`。高等人类种族大招名称 `Highborn's Bloom`，译为“高等人类之绽放”，直观准确。

#### entry-02062
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:280`（`Timeless`）。占位符三个 `%d` 依次对应负面效果缩减 `t.getEffectBad`、技能冷却缩减 `t.getEffectGood`、增益效果延长 `t.getEffectGood`。源码中增益持续时间通过 `math.min(p.dur*2, p.dur + getEffectGood)` 限制最多延长为原有时间的 2 倍，译文“至多延长为剩余时间的两倍”完全切合源码机制。

#### entry-02063
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:330`（`Verdant`）。占位符 `%d%%` 对应自然与酸性伤害亲和（`damage_affinity`），种族名 Thaloren 译为自然精灵。

#### entry-02064
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:365`（`Nature's Pride` 召唤空间不足日志）。感叹号标点与原文一致，翻译准确。

#### entry-02065
- **判定**：未发现问题
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:620`（`Duck and Dodge`）。源码实参顺序为：`threshold * 100`（arg 1）、`evasion`（arg 2）、`t.getDefense`（arg 3）、`duration`（arg 4）。中文译文调整为中文自然语序：“每当你受到相当于生命值 %d%%（arg 1）...接下来的 %d（arg 4）回合内获得 %d%%（arg 2）躲闪概率和 %d（arg 3）点闪避值”。条目元数据及 lua 注册明确指定重排映射 `{1, 4, 2, 3}`，每个占位符类型与对应实参完全吻合，机制准确。

#### entry-02066
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:630`（`Militant Mind`）。占位符浮点数 `%0.1f` 匹配。细微观察在于属性枚举：原文枚举了全部六项“Physical Power, Physical Save, Spellpower, Spell Save, Mental Save, and Mindpower”，译文概括为“所有强度和豁免”。查验游戏系统，角色属性体系中的确仅存在此三系强度与三系豁免，二者在游戏机制上严格等价，属于归纳性意译。

#### entry-02067
- **判定**：细微观察
- **核验依据**：固定源码位于 `mod-tome/data/talents/misc/races.lua:702`（`Indomitable`）。查阅固定源码，上游源码在 `info` 函数中存在形参传递顺序瑕疵：源码为 `local duration = t.getDuration(...)`、`local count = t.getRemoveCount(...)`，但在格式化时写为 `tformat(duration, count)`，导致首个 `%d` 实际传入了 duration，第二个 `%d` 传入了 count；而在实际动作 `action` 中，移除效果数量由 `getRemoveCount` 控制，免疫回合由 `getDuration` 控制。当前译文未指定 `args_order`（即保持 `None`），忠实于英文原文的排版呈现（首个 `%d` 显示 duration，第二个 `%d` 显示 count）。这属于源码层面的实参顺序瑕疵，译文如实还原了原文显示，未擅自调整。

---

### 复核总结

- **本批覆盖条目**：40 条（`entry-02028` 至 `entry-02067`），全部完成逐条独立核验。
- **存在疑点条目**：1 条（`entry-02058` 漏译 `melee`/近战限定词）。
- **细微观察条目**：6 条（`entry-02028` 词风偏俚语且动词有偏差、`entry-02032` 技能名略译、`entry-02043` 技能名略译、`entry-02050` 句末独立多换行、`entry-02066` 六项属性归纳意译、`entry-02067` 源码上游实参倒置）。
- **未发现问题条目**：33 条。