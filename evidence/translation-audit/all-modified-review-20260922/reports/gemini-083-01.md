# batch-083 译文复核报告

## 一、复核基准与文件核验

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-083.md`
- **文件 SHA-256 核验**：
  - 预期哈希：`fd2d95f110050c4f07582f7044224211fd9412e431b70924f84e396ca7ce25d6`
  - 实测哈希：`fd2d95f110050c4f07582f7044224211fd9412e431b70924f84e396ca7ce25d6`（一致）
- **核验范围**：条目 `entry-02692` 至 `entry-02731`，共计 40 条。
- **源码参考基准**：
  - 固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（`/workspace/t-engine4`）
  - 源码文件：`game/modules/tome/data/timed_effects/mental.lua`
  - 译文版本基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

## 二、逐条复核详情（共 40 条）

### entry-02692
- **位置**：`mod-tome.lua:35896`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`logSeen`
- **原文**：`%s collapses.`
- **译文**：`%s 倒下了。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:214`（效果 `DOMINANT_WILL` 结束时若未存活，触发 `game.logSeen(self, "%s collapses.", self:getName():capitalize())`）。占位符 `%s` 匹配，句末标点一致，语境准确。

---

### entry-02693
- **位置**：`mod-tome.lua:35922`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# moves reluctantly!`
- **译文**：`#F53CBE##Target#移动变得迟缓！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:333`（效果 `GLOOM_SLOW` 的 `on_gain` 回调）。颜色码 `#F53CBE#`、目标标签 `#Target#` 与感叹号均正确保留，语义符合减速机制。

---

### entry-02694
- **位置**：`mod-tome.lua:35928`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The gloom has stunned the target, reducing damage by 50%%, putting 4 random talents on cooldown and reducing movement speed by 50%%.  While stunned talents cooldown twice as slow.`
- **译文**：`目标被黑暗光环震慑，伤害降低 50%%，随机 4 个技能进入 CD，移动速度降低 50%%。在震慑时技能冷却速度变慢一倍。`
- **结论**：存在疑点
- **核验依据**：
  1. **术语不一致/未汉化英文缩写**：原文 `putting 4 random talents on cooldown` 译为 `随机 4 个技能进入 CD`。在全仓库同 section 及术语快照中，`cooldown` 统译为“冷却”，全库仅此一处使用英文缩写“CD”（对比同文件 36007 行对应同类效果 `MADNESS_STUNNED` 译为“4 个随机技能进入冷却”）。
  2. **机制表达严谨性**：后半句 `While stunned talents cooldown twice as slow.` 译为 `在震慑时技能冷却速度变慢一倍。`，中文语境下“速度变慢一倍”在字面数值上可能造成困惑，同文件 36007 行翻译为“技能冷却速度减半”，表达更为准确清晰。
  3. 转义百分号 `50%%` 均正确保留。

---

### entry-02695
- **位置**：`mod-tome.lua:35929`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# is stunned with fear!`
- **译文**：`#F53CBE##Target#被恐惧所震慑！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:353`（效果 `GLOOM_STUNNED` 的 `on_gain` 回调）。颜色代码 `#F53CBE#` 与实体标签 `#Target#` 完整，标点匹配。

---

### entry-02696
- **位置**：`mod-tome.lua:35934`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The gloom has confused the target, making it act randomly (%d%% chance) and unable to perform complex actions.`
- **译文**：`目标因黑暗光环陷入混乱，使其随机行动（%d%% 概率）且不能完成复杂动作。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:381`（效果 `GLOOM_CONFUSED` 的 `long_desc`）。格式化占位符 `%d%%` 完整，括号与句号转换规范，机制翻译契合混乱（confusion）状态规则。

---

### entry-02697
- **位置**：`mod-tome.lua:35935`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# is lost in despair!`
- **译文**：`#F53CBE##Target#在绝望中迷失！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:388`（效果 `GLOOM_CONFUSED` 的 `on_gain` 回调）。颜色与实体标签无误，感叹号匹配，语义通顺。

---

### entry-02698
- **位置**：`mod-tome.lua:35938`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# is dismayed!`
- **译文**：`#F53CBE##Target#陷入惊慌失措！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:411`（效果 `DISMAYED` 的 `on_gain` 回调）。标签与格式匹配，与状态名“惊慌失措”（dismayed）统一。

---

### entry-02699
- **位置**：`mod-tome.lua:35940`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target# overcomes the dismay`
- **译文**：`#Target#从惊慌失措中恢复`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:412`（效果 `DISMAYED` 的 `on_lose` 回调）。原文末尾无句号，译文末尾同样无句号，保留了原结构。

---

### entry-02700
- **位置**：`mod-tome.lua:35945`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Stalking %s. Bonus level %d: +%d accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit.`
- **译文**：`追踪 %s. 等级 %d：+%d 命中，+%d%% 近战伤害，攻击目标时 +%0.2f 仇恨/回合。`
- **结论**：细微观察
- **核验依据**：源码见 `mental.lua:430`（效果 `STALKER` 的 `long_desc`，传入 `eff.target.name, eff.bonus, t.getAttackChange(), t.getStalkedDamageMultiplier() * 100 - 100, t.getHitHateChange()` 共 5 个参数）。
  1. 参数顺序与占位符 `%s`、`%d`、`%d`、`%d%%`、`%0.2f` 完全对应，数值逻辑准确。
  2. 标点与格式观察：译文中在 `%s` 之后使用了半角句点空格 `追踪 %s. 等级 %d：`，未转为中文标点；此外“Bonus level %d”译为“等级 %d”（对比 entry-02702 译为“追踪等级 %d”），略有简省，但不影响实际理解。

---

### entry-02701
- **位置**：`mod-tome.lua:35946`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Prey damage modifier: %d%%.`
- **译文**：`猎捕伤害加成：%d%%。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:434`（效果 `STALKER` 的追加描述 `desc = desc..("Prey damage modifier: %d%%."):tformat(...)`）。占位符 `%d%%` 正确，标点规范。

---

### entry-02702
- **位置**：`mod-tome.lua:35951`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Being stalked by %s. Stalker bonus level %d: +%d accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit.`
- **译文**：`目标被 %s 追踪。追踪等级 %d：+%d 命中，+%d%% 近战伤害，击中目标时 +%0.2f 仇恨/回合。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:463`（效果 `STALKED` 的 `long_desc`）。5 个格式化参数 `%s`、`%d`、`%d`、`%d%%`、`%0.2f` 顺序完整，机制说明准确。

---

### entry-02703
- **位置**：`mod-tome.lua:35952`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：` Prey damage modifier: %d%%.`
- **译文**：` 猎捕伤害加成：%d%%。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:467`（效果 `STALKED` 中拼接的字符串 `desc = desc..(" Prey damage modifier: %d%%."):tformat(...)`）。原文前导空格在译文中严格保留，占位符 `%d%%` 完整。

---

### entry-02704
- **位置**：`mod-tome.lua:35955`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：` (spellpower: %d, mindpower: %d`
- **译文**：` (法术强度：%d，精神强度：%d`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:513`（效果 `BECKONED` 中 `message = message..(" (spellpower: %d, mindpower: %d"):tformat(...)`）。原文前导空格与未闭合的半开左括号在源码与译文中一致，术语“法术强度”与“精神强度”符合统一规则。

---

### entry-02705
- **位置**：`mod-tome.lua:35975`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`Harassed`
- **译文**：`被骚扰`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:683`（效果 `HARASSED` 的描述名 `desc = _t"Harassed"`）。与诅咒系技能“Harass Prey”（骚扰猎物）状态对应准确。

---

### entry-02706
- **位置**：`mod-tome.lua:35976`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target has been harassed by its stalker, reducing damage by %d%%.`
- **译文**：`目标受到追踪者骚扰，伤害降低 %d%%。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:684`（效果 `HARASSED` 的 `long_desc`，格式化传入 `-eff.damageChange`）。占位符 `%d%%` 正确，标点规范。

---

### entry-02707
- **位置**：`mod-tome.lua:35977`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target# has been harassed.`
- **译文**：`#Target#受到骚扰。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:689`（效果 `HARASSED` 的 `on_gain` 回调）。实体标签 `#Target#` 正确，语义通顺。

---

### entry-02708
- **位置**：`mod-tome.lua:35978`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`+Harassed`
- **译文**：`+被骚扰`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:689`（获得效果时的漂浮提示字）。前缀 `+` 正确，效果名统一。

---

### entry-02709
- **位置**：`mod-tome.lua:35979`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target# is no longer harassed.`
- **译文**：`#Target#不再受到骚扰。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:690`（效果 `HARASSED` 的 `on_lose` 回调）。实体标签 `#Target#` 与句号完整，准确反映效果消除。

---

### entry-02710
- **位置**：`mod-tome.lua:35980`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`-Harassed`
- **译文**：`-被骚扰`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:690`（失去效果时的漂浮提示字）。前缀 `-` 正确，效果名统一。

---

### entry-02711
- **位置**：`mod-tome.lua:36004`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# slows in the grip of madness!`
- **译文**：`#F53CBE##Target#陷入疯狂之中速度减缓了！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:857`（效果 `MADNESS_SLOW` 的 `on_gain` 回调）。颜色代码 `#F53CBE#` 与实体标签 `#Target#` 无误，感叹号匹配。

---

### entry-02712
- **位置**：`mod-tome.lua:36012`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Madness has confused the target, lowering mind resistance by %d%% and making it act randomly (%d%% chance)`
- **译文**：`疯狂使目标混乱，降低目标 %d%% 精神抗性，使目标随机行动（%d%% 概率）。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:914`（效果 `MADNESS_CONFUSED` 的 `long_desc`，参数为 `eff.mindResistChange, eff.power`）。两个 `%d%%` 顺序与源码传入顺序一致，术语“精神抗性”准确，译文规范添加末尾句号。

---

### entry-02713
- **位置**：`mod-tome.lua:36083`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target erects a powerful kinetic shield capable of absorbing %d/%d physical%s or acid damage before it crumbles.`
- **译文**：`目标施放一个念力护盾，在碎裂前吸收 %d/%d 物理%s或酸性伤害。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1428`（效果 `KINSPIKE_SHIELD` 的 `long_desc`，参数传入 `self.kinspike_shield_absorb, eff.power, xs`）。占位符 `%d/%d` 与 `%s` 顺序匹配；`%s` 用于动态插入自然/时空伤害类型片段（如 `, 自然`），占位符位置与前后语境自然融合。

---

### entry-02714
- **位置**：`mod-tome.lua:36097`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target erects a powerful charged shield capable of absorbing %d/%d lightning%s or blight damage before it crumbles.`
- **译文**：`目标施放一个充能护盾，在碎裂前吸收 %d/%d 闪电%s或枯萎伤害。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1489`（效果 `CHARGESPIKE_SHIELD` 的 `long_desc`，参数传入 `self.chargespike_shield_absorb, eff.power, xs`）。占位符 `%d/%d` 与 `%s` 匹配，伤害类型“闪电”、“枯萎”与动态扩展 `%s`（暗影/精神）处理一致。

---

### entry-02715
- **位置**：`mod-tome.lua:36116`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Decreases mind save by %d and increases mindpower by %d.`
- **译文**：`降低精神豁免 %d 并增加精神强度 %d。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1565`（效果 `RECEPTIVE_MIND` 的 `long_desc`，参数传入 `eff.save, eff.power`）。占位符 `%d` 匹配，属性术语“精神豁免”（mind save）与“精神强度”（mindpower）完全契合规范。

---

### entry-02716
- **位置**：`mod-tome.lua:36133`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#F53CBE##Target# is plagued by inner demons!`
- **译文**：`#F53CBE##Target#受心魔困扰！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1648`（效果 `INNER_DEMONS` 的 `on_gain` 回调）。颜色码 `#F53CBE#` 与实体标签 `#Target#` 保留完整，感叹号匹配，译文简洁贴切。

---

### entry-02717
- **位置**：`mod-tome.lua:36158`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`Falls dead!`
- **译文**：`死亡！`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1775`（效果 `FRENZY` 结束且生命值降至死线时，漂浮文字 `game.flyers:add(..., _t"Falls dead!", ...)`）。漂浮短文本处理适当，感叹号匹配。

---

### entry-02718
- **位置**：`mod-tome.lua:36163`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The thrill of combat improves the target's maximum life by %d%%, life regeneration by %0.2f, and stamina regeneration by %0.2f.`
- **译文**：`目标被战斗激励提升生命上限 %d%%、提升生命回复 %0.2f、提升体力回复 %0.2f。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1785`（效果 `BLOODBATH` 的 `long_desc`，参数为 `eff.hp, eff.cur_regen or eff.regen, eff.cur_regen/5 or eff.regen/5`）。占位符 `%d%%`、`%0.2f`、`%0.2f` 顺序与类型完全对应，资源术语“生命上限”、“生命回复”、“体力回复”规范准确。

---

### entry-02719
- **位置**：`mod-tome.lua:36180`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`Guarding against melee damage:  Will dismiss up to %d damage from the next %0.1f attack(s)%s.`
- **译文**：`防御近战伤害：减少 %d 点伤害，剩余次数 %0.1f%s。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1899`（效果 `GESTURE_OF_GUARDING` 的 `long_desc`，参数为 `dam, deflects, xs`）。
  1. 占位符 `%d`、`%0.1f`、`%s` 顺序匹配。
  2. 经比对同 section 36179 行，`xs` 对应译文为 `，并有 %d%% 几率发动反击`（不带句号）。当 `xs` 存在时拼接为 `剩余次数 %0.1f，并有 %d%% 几率发动反击。`，当 `xs` 为空时呈现为 `剩余次数 %0.1f。`，标点衔接严密无缝。

---

### entry-02720
- **位置**：`mod-tome.lua:36183`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target is rampaging! (+%d%% movement speed, +%d%% attack speed, +%d%% mind speed`
- **译文**：`目标进入暴走状态！(+%d%% 移动速度，+%d%% 攻击速度，+%d%% 精神速度`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1921`（效果 `RAMPAGE` 的 `long_desc` 开头部分）。三个速度占位符 `%d%%` 匹配，左括号故意未闭合（代码中后续条件追加并在结尾闭合 `)`），译文忠实保留该结构。

---

### entry-02721
- **位置**：`mod-tome.lua:36184`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`, +%d%% physical damage, +%d physical save, +%d mental save`
- **译文**：`, +%d%% 物理伤害，+%d 物理豁免，+%d 精神豁免`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1923`（效果 `RAMPAGE` 中当 `physicalDamageChange > 0` 时追加的片段）。前导逗号保留，三个占位符 `%d%%`、`%d`、`%d` 顺序无误，术语“物理伤害”、“物理豁免”、“精神豁免”规范。

---

### entry-02722
- **位置**：`mod-tome.lua:36193`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`logPlayer`
- **原文**：`#F53CBE#You feel your rampage slowing down. (-1 duration)`
- **译文**：`#F53CBE#你感觉你的暴走正在消退。（-1持续时间）`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:1991`（`RAMPAGE:do_postUseTalent` 中触发 `game.logPlayer`）。颜色码 `#F53CBE#` 保留，数值机制说明准确，括号全半角转换得当。

---

### entry-02723
- **位置**：`mod-tome.lua:36231`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target is surrounded by a psychic field, absorbing 50%% of all damage (up to %d/%d).`
- **译文**：`目标被灵能领域包围，吸收 50%% 所有伤害（最多 %d/%d）。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2212`（效果 `RESONANCE_FIELD` 的 `long_desc`，传入 `self.resonance_field_absorb, eff.power`）。`50%%` 转义正确，`%d/%d` 匹配，术语“灵能领域”统一。

---

### entry-02724
- **位置**：`mod-tome.lua:36246`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target# is no longer gaining feedback.`
- **译文**：`#Target#不再获取反馈值。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2273`（效果 `FEEDBACK_LOOP` 的 `on_lose` 回调）。实体标签 `#Target#` 正确，“反馈值”（Feedback）符合该系资源术语统一译名。

---

### entry-02725
- **位置**：`mod-tome.lua:36249`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`；**args_order**：`[2, 1]`
- **原文**：`The target's subconscious has focused, increasing Mind resistance penetration by +%d%% and turning its attention on %s.`
- **译文**：`目标的潜意识集中在 %s，增加%d%%精神抗性穿透。`
- **结论**：未发现问题
- **核验依据**：
  1. 源码见 `mental.lua:2285`：调用 `("..."):tformat(eff.pen, eff.target:getName():capitalize())`，参数 1 为数值（穿透），参数 2 为目标名称（字符串）。
  2. 引擎国际化规则见 `game/engines/default/engine/I18N.lua:74`（`default_tformat` 会根据 `args_order = {2, 1}` 将传入实参重新映射为 `args[1] = sargs[2]`，`args[2] = sargs[1]`）。
  3. 译文中占位符顺序为 `%s` 随后 `%d%%`，运行时与 `{2, 1}` 重排参数完全契合，机制描述严谨准确。

---

### entry-02726
- **位置**：`mod-tome.lua:36256`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target is asleep and unable to perform most actions.  Every %d damage it takes will reduce the duration of the effect by one turn.`
- **译文**：`目标陷入睡眠，无法执行大多数行动，每受到 %d 伤害缩短 1 回合持续时间。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2305`（效果 `SLEEP` 的 `long_desc`，传入 `eff.power`）。占位符 `%d` 匹配，睡眠机制描述与参数表达准确。

---

### entry-02727
- **位置**：`mod-tome.lua:36262`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`tformat`
- **原文**：`The target is in a deep sleep and unable to perform most actions.  Every %d damage it takes will reduce the duration of the effect by one turn.`
- **译文**：`目标陷入沉睡，无法执行大多数行动，每受到 %d 伤害缩短 1 回合持续时间。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2359`（效果 `SLUMBER` 的 `long_desc`，传入 `eff.power`）。占位符 `%d` 匹配，区分了普通睡眠（Sleep）与沉睡（Slumber）。

---

### entry-02728
- **位置**：`mod-tome.lua:36299`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target#'s focuses.`
- **译文**：`#Target#集中了意志。`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2628`（效果 `HIDDEN_RESOURCES` 的 `on_gain` 回调）。标签 `#Target#` 保留完整，与所属意志（willpower）系机制意图契合。

---

### entry-02729
- **位置**：`mod-tome.lua:36304`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`Spell Feedback`
- **译文**：`法术反馈`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2638`（反魔效果 `SPELL_FEEDBACK` 描述名 `desc = _t"Spell Feedback"`）。效果名翻译准确。

---

### entry-02730
- **位置**：`mod-tome.lua:36307`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`+Spell Feedback`
- **译文**：`+法术反馈`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2643`（效果获得漂浮字）。前缀 `+` 保留，效果名与 entry-02729 统一。

---

### entry-02731
- **位置**：`mod-tome.lua:36309`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`-Spell Feedback`
- **译文**：`-法术反馈`
- **结论**：未发现问题
- **核验依据**：源码见 `mental.lua:2644`（效果移除漂浮字）。前缀 `-` 保留，效果名统一。

---

## 三、复核总结

本批次共复核 40 个条目（`entry-02692` 至 `entry-02731`）：
- **未发现问题**：38 条。占位符、颜色代码、实体标签、参数重排（如 entry-02725 的 `{2, 1}`）均经源码与引擎解析逻辑验证无误。
- **存在疑点**：1 条（`entry-02694`）。`cooldown` 被译为非标准缩写“CD”（全库仅此一处使用“进入 CD”，其余统一为“进入冷却”），且后半句“变慢一倍”相较同类效果条目“冷却速度减半”表达不够严密。
- **细微观察**：1 条（`entry-02700`）。`追踪 %s. 等级 %d：` 存在未中文化半角句点空格，且 `Bonus level` 译为 `等级` 略有简略。