# 译文复核报告：batch-054（条目 entry-01545 至 entry-01584，共 40 条）

- **冻结文件哈希核验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-054.md`
  - SHA-256：`7ad394102479f06bfdef2b8a3b921ea9d9a7b460446ffb3376cb9da6ac298168`（核验一致）
- **源码基准**：固定引擎 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/talents/chronomancy/...`）
- **译文终点**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua`）

---

### entry-01545
- **位置**：`mod-tome.lua:21655`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：logSeen`
- **原文**：`The spell fizzles!`
- **译文**：`法术失败了！`
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:257`（`game.logSeen(self, "The spell fizzles!")`）。无占位符，感叹号标点与原文语义严格匹配。

---

### entry-01546
- **位置**：`mod-tome.lua:21656`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：tformat`
- **原文**：`You swap locations with a random target.`
- **译文**：`你和一个随机目标交换位置。`
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:267`（`info` 描述）。无占位符，句号对齐，换位异常描述准确。

---

### entry-01547
- **位置**：`mod-tome.lua:21659`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：tformat`
- **原文**：
  ```text
  50%% chance that damage the caster takes will be warped to a set target.
  		Once the maximum damage (%d) is absorbed, the time runs out, or the target dies, the shield will crumble.
  ```
- **译文**：
  ```text
  施法者所承受的伤害有 50%% 的概率转移给指定连接的目标。
  		一旦吸收伤害达到上限（%d），持续时间到了或目标死亡，护盾会破碎掉。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:317`（参数为 `self:getShieldAmount(...)`）。`50%%` 转义百分号与 `%d` 伤害数值占位符完整保留，换行缩进对应，机制描述准确。

---

### entry-01548
- **位置**：`mod-tome.lua:21679`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：logPlayer`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:550`（`game.logPlayer(self, "Not enough space to summon!")`）。无占位符，译文保留感叹号与源码原文严格一致（虽术语库 `logSeen` 登记为句号版本，但此处源码为 `logPlayer` 且原文即为感叹号）。

---

### entry-01549
- **位置**：`mod-tome.lua:21728`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：tformat`
- **原文**：`Places between three and six talents of up to 5 targets in a radius %d ball on cooldown for up to %d turns.`
- **译文**：`让半径 %d 范围内最多五个单位的三到六个技能进入最多 %d 回合的冷却。`
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:1258`（参数依次为 `getAnomalyRadius(self, t)` 与 `getAnomalyDuration(self, t)`）。两个 `%d` 占位符顺序与含义（半径、冷却回合）完全一致，句号对齐。

---

### entry-01550
- **位置**：`mod-tome.lua:21771`；`section：mod-tome/data/talents/chronomancy/anomalies.lua`；`source_tag：tformat`
- **原文**：`Summons three to six tornados.`
- **译文**：`召唤三到六道龙卷风。`
- **复核结论**：未发现问题
- **核验依据**：源码 `anomalies.lua:1927`（`info` 描述）。无占位符，句号对齐，龙卷风量词与含义准确。

---

### entry-01551
- **位置**：`mod-tome.lua:21790`；`section：mod-tome/data/talents/chronomancy/blade-threading.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Attack with your melee weapons for %d%% weapon damage as physical and temporal (warp) damage. If either attack hits you may stun, blind, pin, or confuse the target for %d turns.
  		
  		Blade Threading talents will freely swap to your dual-weapons when activated if you have them in your secondary slots.  Additionally you may use the Attack talent in a similar manner.
  ```
- **译文**：
  ```text
  使用近战武器攻击目标，造成 %d%% 物理和时空（扭曲）属性的武器伤害。如果任意一次攻击命中，你可以使目标震慑、致盲、定身或混乱 %d 回合。

  		激活螺旋灵刃系技能时，如果副武器栏位中有双持武器，便会自动切换至它们。普通攻击技能也能以同样方式切换。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `blade-threading.lua:63`（参数为 `damage, duration`）。占位符 `%d%%` 与 `%d` 顺序正确；四种状态“震慑、致盲、定身或混乱”严格对应 `stun, blind, pin, or confuse` 标准术语；段落缩进与机制切换说明准确。

---

### entry-01552
- **位置**：`mod-tome.lua:21796`；`section：mod-tome/data/talents/chronomancy/blade-threading.lua`；`source_tag：logSeen`
- **原文**：`The spell fizzles!`
- **译文**：`法术失败了！`
- **复核结论**：未发现问题
- **核验依据**：源码 `blade-threading.lua:110`（`Blink Blade` 传送受阻失败日志）。感叹号对齐，准确无误。

---

### entry-01553
- **位置**：`mod-tome.lua:21802`；`section：mod-tome/data/talents/chronomancy/blade-threading.lua`；`source_tag：logSeen`
- **原文**：`%s resists the temporal shear!`
- **译文**：`%s 抵挡了时空切变！`
- **复核结论**：未发现问题
- **核验依据**：源码 `blade-threading.lua:244`（`game.logSeen(target, "%s resists the temporal shear!", target:getName():capitalize())`）。`%s` 占位符保留，感叹号对齐。

---

### entry-01554
- **位置**：`mod-tome.lua:21815`；`section：mod-tome/data/talents/chronomancy/bow-threading.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Fire an arrow for %d%% weapon damage and call up to 2 wardens, depending on available space, that will each fire a single arrow before returning to their timelines.
  		The wardens are out of phase with normal reality and deal %d%% less damage but shoot through friendly targets. All your arrows, including arrows from Shoot and other talents, now phase through friendly targets without causing them harm.
  		
  		Bow Threading talents will freely swap to your bow when activated if you have one in your secondary slot. You may use the Shoot talent in a similar manner.
  ```
- **译文**：
  ```text
  发射一支灵矢造成 %d%% 武器伤害，并且根据可用空间，召唤最多两个守卫，各自发射一枚灵矢然后回到他们自己的时间线中。
  		守卫处在现实位面之外，灵矢的伤害减少 %d%%，但能够穿过友好目标。同时，你发射的所有来自射击或者其他技能的箭矢，都可以穿透友军并且不会造成伤害。

  		激活螺旋灵弓技能可以自由切换到你的弓（必须装备在副武器栏位上）。此外，当你使用远程攻击时也会触发这个效果。
  ```
- **复核结论**：细微观察
- **核验依据**：源码 `bow-threading.lua:120`。
  1. 占位符 `%d%%`（武器伤害比例）与 `%d%%`（伤害减免比例）保留且顺序正确。
  2. 末句 `You may use the Shoot talent in a similar manner.` 在前句中 `Shoot` 被统一翻译为技能名“射击”（`来自射击或者其他技能的箭矢`），但末句译为了“当你使用远程攻击时也会触发这个效果”（参考 entry-01551 中 `Attack talent` 译为“普通攻击技能”，此处更精确应为“射击技能也能以同样方式切换”），但实际机制语义传达无误。
  3. 第二句中 `and deal %d%% less damage` 原指守卫本体造成的伤害减少 %d%%（源码 `m.generic_damage_penalty = ...`），译文表述为“灵矢的伤害减少 %d%%”，因该克隆守卫出场仅施放一记 Arrow Stitching 即死亡，实际运行结果完全等价。

---

### entry-01555
- **位置**：`mod-tome.lua:21833`；`section：mod-tome/data/talents/chronomancy/bow-threading.lua`；`source_tag：logSeen`
- **原文**：`You do not have line of sight.`
- **译文**：`你没有视线。`
- **复核结论**：未发现问题
- **核验依据**：源码 `bow-threading.lua:267`（`Arrow Echoes` 视线检查）。句号对齐，语义准确。

---

### entry-01556
- **位置**：`mod-tome.lua:21877`；`section：mod-tome/data/talents/chronomancy/chronomancer.lua`；`source_tag：_t`
- **原文**：`Manipulate raw energy by addition or subtraction.`
- **译文**：`通过增加或减少来操纵原始能量。`
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancer.lua:42`（天赋系 `energy` 描述）。无占位符，句号对齐，准确流畅。

---

### entry-01557
- **位置**：`mod-tome.lua:21879`；`section：mod-tome/data/talents/chronomancy/chronomancer.lua`；`source_tag：_t`
- **原文**：`Weave the threads of fate.`
- **译文**：`编织你的命运。`
- **复核结论**：存在疑点
- **核验依据**：源码 `chronomancer.lua:43`（天赋系 `fate-weaving` 描述：`description = _t"Weave the threads of fate."`）。
  1. 英文原文为 `Weave the threads of fate.`，并未出现代词 `your`（“你的”）。
  2. 对比下一行 entry-01558 `Weave the threads of spacetime.` 准确译为 `编织时空线。`；
  3. 时空系 Fate Weaving（命运编织）的核心机制概念即为“命运之丝/线”（如 `Spin Fate` 获得并叠加“命运之丝”）。译文“编织你的命运”增译了“你的”，且漏译了核心意象 `threads`（线/丝），导致与相邻条目风格不统一且脱离了技能树意象。

---

### entry-01558
- **位置**：`mod-tome.lua:21881`；`section：mod-tome/data/talents/chronomancy/chronomancer.lua`；`source_tag：_t`
- **原文**：`Weave the threads of spacetime.`
- **译文**：`编织时空线。`
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancer.lua:44`（天赋系 `spacetime-weaving` 描述）。句号对齐，准确传达了 `threads of spacetime`。

---

### entry-01559
- **位置**：`mod-tome.lua:21900`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  You peer into the future, sensing creatures and traps in a radius of %d for %d turns.
  		If you know Foresight you'll gain additional defense and chance to shrug off critical hits (equal to your Foresight bonuses) while Precognition is active.
  ```
- **译文**：
  ```text
  你预知未来，感知半径 %d 以内的生物和陷阱，持续 %d 回合。
  		如果你学会了深谋远虑，那么在你激活这个技能的时候，你可以获得额外的闪避和无视暴击伤害几率（数值等于深谋远虑的奖励）。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancy.lua:48`（参数为 `range, duration`）。占位符 `%d`（范围半径）与 `%d`（持续回合）顺序正确；`Foresight` 对应“深谋远虑”，`defense` 对应“闪避”，`shrug off critical hits` 对应“无视暴击伤害几率”，机制准确。

---

### entry-01560
- **位置**：`mod-tome.lua:21904`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Gain %d defense and %d%% chance to shrug off critical hits.
  		If you have Precognition or See the Threads active these bonuses will be added to those effects, granting additional defense and chance to shrug off critical hits.
  		These bonuses scale with your Magic stat.
  ```
- **译文**：
  ```text
  获得 %d 闪避和 %d%% 几率无视暴击伤害。
  		如果你激活了预知未来或者命运螺旋，那么这些技能也会拥有同样的加成，使你获得额外的闪避和无视暴击伤害几率。
  		增益效果受魔力值加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancy.lua:73`（参数为 `defense, crits`）。占位符 `%d` 与 `%d%%` 顺序正确；Magic stat 对应“魔力值”；Precognition（预知未来）与 See the Threads（命运螺旋）技能联动描述准确。

---

### entry-01561
- **位置**：`mod-tome.lua:21910`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：logPlayer`
- **原文**：`#LIGHT_RED#Your Contingency has failed to cast %s!`
- **译文**：`#LIGHT_RED#你的意外术没能触发%s！`
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancy.lua:109`。颜色码 `#LIGHT_RED#` 完好，占位符 `%s` 保留，感叹号对齐，意外术触发失败日志准确。

---

### entry-01562
- **位置**：`mod-tome.lua:21911`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：logPlayer`
- **原文**：`#STEEL_BLUE#Your Contingency triggered %s!`
- **译文**：`#STEEL_BLUE#你的意外术触发了%s！`
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancy.lua:111`。颜色码 `#STEEL_BLUE#` 完好，占位符 `%s` 保留，感叹号对齐，意外术成功触发日志准确。

---

### entry-01563
- **位置**：`mod-tome.lua:21913`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Choose an activatable spell that affects only you, does not require a target, and does not have a fixed cooldown.  When you take damage that reduces your life below %d%% the spell will automatically cast.
  		This spell will cast even if it is currently on cooldown, will not consume a turn or resources, and uses the talent level of Contingency or its own, whichever is lower.
  		This effect can only occur once every %d turns and takes place after the damage is resolved.

  		Current Contingency Spell: %s
  ```
- **译文**：
  ```text
  选择一个只会影响你并且不需要选中目标的非固定冷却时间主动法术。当你受到伤害并使生命值降低到 %d%% 以下时，自动释放这个技能。
  		即使选择的技能处于冷却状态也可以释放  ，并且不消耗回合或资源，技能等级取意外术与所选法术两者中较低的一方。
  		这个效果每 %d 回合只能触发一次，并且在伤害结算之后生效。

  		当前选择技能：%s
  ```
- **复核结论**：细微观察
- **核验依据**：源码 `chronomancy.lua:155`（参数为 `trigger, cooldown, talent`）。
  1. 占位符 `%d%%`、`%d`、`%s` 顺序和含义完全吻合。
  2. 译文第 2 段中 `即使选择的技能处于冷却状态也可以释放  ，`，“释放”与全角逗号之间存在两个多余的半角空格（`释放  ，`），排版稍有瑕疵，但不影响语法解析与运行。

---

### entry-01564
- **位置**：`mod-tome.lua:21923`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：logPlayer`
- **原文**：`The timeline is too fractured to do this now.`
- **译文**：`目前的时间线过于破碎，你现在无法这么做。`
- **复核结论**：未发现问题
- **核验依据**：源码 `chronomancy.lua:176`（`on_pre_use` 中并发时间线检查 `checkTimeline`）。句号对齐，语义精准。

---

### entry-01565
- **位置**：`mod-tome.lua:21925`；`section：mod-tome/data/talents/chronomancy/chronomancy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  You peer into three possible futures, allowing you to explore each for %d turns.  When the effect expires, you'll choose which of the three futures becomes your present.
  		If you know Foresight you'll gain additional defense and chance to shrug off critical hits (equal to your Foresight values) while See the Threads is active.
  		This spell splits the timeline.  Attempting to use another spell that also splits the timeline while this effect is active will be unsuccessful.
  		If you die in any thread you'll revert the timeline to the point when you first cast the spell and the effect will end.
  		This spell may only be used once per zone level.
  ```
- **译文**：
  ```text
  你窥视三种可能的未来，允许你分别进行探索 %d 回合。当效果结束，你选择三者之一成为你的现在。
  		如果你学会了深谋远虑，当你使用命运螺旋时，将获得额外的闪避和无视暴击伤害几率（数值等于深谋远虑的奖励）。
  		这个法术会使时间线分裂。当此技能激活的时候，使用其他分裂时间线的技能将会失败。
  		如果你在任何一条时间线上死亡，你将使时间线回到你使用技能的地方，并且技能效果结束。
  		这个技能每个楼层只能使用一次。
  ```
- **复核结论**：存在疑点
- **核验依据**：源码 `chronomancy.lua:206`，结合 `DeathDialog.lua:249-255`。
  - 原文第 4 段：`If you die in any thread you'll revert the timeline to the point when you first cast the spell and the effect will end.`
  - 译文译为：`如果你在任何一条时间线上死亡，你将使时间线回到你使用技能的地方，并且技能效果结束。`
  - 语法上 `when you first cast the spell` 紧接在 `the point` 之后，充当时间定语从句，指“最初施放该法术的时间点/时刻”；底层机制上，在线程中死亡会调用 `game:chronoRestore("see_threads_base", true)` 回溯整个世界与角色的历史全量快照，本质是时间回溯，并非空间传送。译文将时间点翻译为空间“地方”，容易让玩家误以为是传送回原施法坐标。

---

### entry-01566
- **位置**：`mod-tome.lua:21940`；`section：mod-tome/data/talents/chronomancy/energy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Partially dissipates all incoming damage, reducing it by 30%%, up to a maximum of %d.
  		The maximum damage reduction will scale with your Spellpower.
  ```
- **译文**：
  ```text
  分解一部分受到的伤害。减少 30%% 伤害，最多减少 %d。
  		减少伤害的最大值受法术强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `energy.lua:56`（`Energy Decomposition` 的 `info` 描述，参数为 `decomp`）。`30%%` 转义百分号和 `%d` 伤害上限占位符保留完整，句号对齐，机制清晰。

---

### entry-01567
- **位置**：`mod-tome.lua:21946`；`section：mod-tome/data/talents/chronomancy/energy.lua`；`source_tag：tformat`
- **原文**：
  ```text
  You sap the target's energy and add it to your own, placing up to %d random talents on cooldown for %d turns.
  		For each talent put on cooldown, you reduce the cooldown of one of your talents currently on cooldown by %d turns.
  ```
- **译文**：
  ```text
  你吸收目标的能量并化为己用，最多使 %d 个随机技能进入 %d 回合冷却。
  		每使一个技能进入冷却，你减少你的一个处于冷却中的技能的冷却时间 %d 回合。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `energy.lua:135`（`Energy Drain` 的 `info` 描述，参数为 `talentcount, cooldown, cooldown`）。三个 `%d` 占位符顺序与含义完全对应，句号对齐。

---

### entry-01568
- **位置**：`mod-tome.lua:21960`；`section：mod-tome/data/talents/chronomancy/fate-weaving.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Each time you would take damage from someone else you gain one Spin, increasing your defense and saves by %d for three turns.
  		This effect may occur once per turn and stacks up to three Spin (for a maximum bonus of %d).
  ```
- **译文**：
  ```text
  每当你要受到其他人造成的伤害时，你编织一层命运之丝，使你的闪避和豁免增加 %d，持续三回合。
  		这个效果每回合只能触发一次，丝能叠加三层 (加成最多为 %d)。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `fate-weaving.lua:50`（`Spin Fate` 的 `info` 描述，参数为 `save, save * 3`）。两个 `%d` 占位符位置与数值对应准确；`Spin` 准确译为“命运之丝/丝”，`defense and saves` 对应“闪避和豁免”。

---

### entry-01569
- **位置**：`mod-tome.lua:21987`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：delayedLogMessage`
- **原文**：`#LIGHT_BLUE##Source# converts damage to paradox!`
- **译文**：`#LIGHT_BLUE##Source#将伤害转化为紊乱值！`
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:76`（`Reality Smearing` 伤害转化日志）。`#LIGHT_BLUE#` 颜色代码与 `#Source#` 占位标签完好，`paradox` 遵循术语表（紊乱值），感叹号对齐。

---

### entry-01570
- **位置**：`mod-tome.lua:21989`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：tformat`
- **原文**：
  ```text
  While active 30%% of all damage you take is converted into %0.2f Paradox per point.
  		The Paradox is gained over three turns.
  ```
- **译文**：
  ```text
  当激活这个技能时，你受到的伤害有 30%% 会按每点伤害转化为 %0.2f 紊乱值。
  		这些紊乱值会在三个回合内逐步获得。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:94`（参数传入 `ratio, duration`，但英文原文硬编码了 `three turns`，格式化串中仅有一个 `%0.2f`）。译文保留了 `30%%` 转义百分比与唯一的 `%0.2f` 转化比率占位符，与英文原文结构及运行逻辑完全一致。

---

### entry-01571
- **位置**：`mod-tome.lua:21992`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：talent name`
- **原文**：`Attenuate`
- **译文**：`衰减`
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:101`。技能名翻译规范统一。

---

### entry-01572
- **位置**：`mod-tome.lua:21993`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Deals %0.2f temporal damage over %d turns to all targets in a radius of %d.  Targets with Reality Smearing active will instead recover %d life over four turns.
  		If a target is reduced below 20%% life while Attenuate is active it may be instantly slain.
  		The damage will scale with your Spellpower.
  ```
- **译文**：
  ```text
  对范围内所有目标造成 %0.2f 点时空伤害，伤害分摊到 %d 回合内。技能半径为 %d 格。
  		带有弥散现实效果的目标则改为在四回合内恢复 %d 点生命。
  		衰减生效期间，若目标的生命值降至 20%% 以下，它可能会被立即杀死。
  		伤害受法术强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:143`（参数为 `damDesc(...), duration, radius, damage * 0.4`）。依次对应的 `%0.2f`（伤害）、`%d`（回合）、`%d`（半径）、`%d`（生命恢复）以及 `20%%`（斩杀阈值）共 5 处占位/转义符号全部准确保留；`Reality Smearing`（弥散现实）术语一致。

---

### entry-01573
- **位置**：`mod-tome.lua:22001`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：logPlayer`
- **原文**：`#STEEL_BLUE#Casts %s.`
- **译文**：`#STEEL_BLUE#释放 %s。`
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:166`（`Twist Fate` 施法日志）。颜色码 `#STEEL_BLUE#` 保留，`%s` 保留，句号对齐。

---

### entry-01574
- **位置**：`mod-tome.lua:22004`；`section：mod-tome/data/talents/chronomancy/flux.lua`；`source_tag：tformat`
- **原文**：
  ```text
  If Twist Fate is not on cooldown minor anomalies will be held for %d turns, allowing your spell to cast as normal.  While held you may cast Twist Fate in order to trigger the anomaly and may choose the target area.
  		If a second anomaly occurs while a prior one is held or the timed effect expires the first anomaly will trigger immediately, interrupting your current turn or action.
  		Paradox reductions from held anomalies occur when triggered.
  				
  		Current Anomaly: %s
  		
  		%s
  ```
- **译文**：
  ```text
  若扭曲命运不在冷却中，微小异变会被延后 %d 回合，使你的法术得以正常施放。异变被延后期间，你可以施放扭曲命运来触发该异变，并选择其目标区域。
  		如果已有一个异变被延后时又发生第二个异变，或延后效果到期，第一个异变会立即触发，并打断你当前的回合或行动。
  		被延后异变带来的紊乱值降低会在其触发时结算。

  		当前异变：%s

  		%s
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `flux.lua:201`（参数为 `duration, t_name, t_info`）。占位符 `%d`、`%s`、`%s` 顺序和换行排版完全匹配；异变延后与紊乱值结算机制表述清晰准确。

---

### entry-01575
- **位置**：`mod-tome.lua:22023`；`section：mod-tome/data/talents/chronomancy/gravity.lua`；`source_tag：logSeen`
- **原文**：`%s is knocked back!`
- **译文**：`%s 被击退！`
- **复核结论**：未发现问题
- **核验依据**：源码 `gravity.lua:84`。`%s` 占位符保留，感叹号对齐，击退日志准确。

---

### entry-01576
- **位置**：`mod-tome.lua:22025`；`section：mod-tome/data/talents/chronomancy/gravity.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Sends out a blast wave of gravity in a radius %d cone, dealing %0.2f base physical (gravity) damage and knocking back targets caught in the area.
  		Targets knocked into walls or other targets take 25%% additional damage and deal 25%% damage to targets they're knocked into.
  		Closer targets will be knocked back further and the damage will scale with your Spellpower.
  ```
- **译文**：
  ```text
  在半径 %d 码的锥形范围内释放一股爆炸性的重力冲击波，造成 %0.2f 物理（重力）伤害并击退范围内目标。
  		被击飞至墙上或其他单位的目标受到额外 25%% 伤害，并对被击中的单位造成 25%% 伤害。
  		离你越近的目标将会被击飞得更远。受法术强度影响，伤害按比例加成。
  ```
- **复核结论**：细微观察
- **核验依据**：源码 `gravity.lua:100`（参数为 `radius, damDesc(...)`）。
  1. 占位符 `%d`、`%0.2f` 以及转义百分号 `25%%`、`25%%` 完全对应。
  2. 原文 `in a radius %d cone` 译为“在半径 %d 码的锥形范围内”，添加了“码”字；在 ToME4 网格机制中通常为“格”或纯数值范围（如 entry-01577 的“半径 %d 范围内”，entry-01572 的“半径为 %d 格”），此处用“码”为汉化早期习惯遗留，虽不影响实际理解，但单位存在细微不一致。

---

### entry-01577
- **位置**：`mod-tome.lua:22032`；`section：mod-tome/data/talents/chronomancy/gravity.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Creates a gravity spike in a radius of %d that moves all targets towards the spell's center and inflicts %0.2f physical (gravity) damage.
  		Each target moved beyond the first increases the damage by %0.2f (up to a maximum of %0.2f bonus damage).
  		Targets take reduced damage the further they are from the epicenter (20%% less per tile).
  		The damage dealt will scale with your Spellpower.
  ```
- **译文**：
  ```text
  在半径 %d 范围内制造一个重力钉刺，将所有目标牵引至法术中心，造成 %0.2f 物理（重力）伤害。
  		从第二个单位起，每牵引一个单位将会使伤害增加 %0.2f (最多增加 %0.2f 额外伤害)。
  		离法术中心越远，目标受到的伤害越少（每格减少 20%%）。
  		受法术强度影响，伤害按比例加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `gravity.lua:178`（参数为 `radius, damDesc(damage), damDesc(damage/8), damDesc(damage/2)`）。`%d`、`%0.2f`、`%0.2f`、`%0.2f`、`20%%` 共 5 处参数和转义完全一致，衰减递减机制与法术强度加成表述清晰无误。

---

### entry-01578
- **位置**：`mod-tome.lua:22044`；`section：mod-tome/data/talents/chronomancy/gravity.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Increases local gravity in a radius of %d for %d turns, dealing %0.2f physical (gravity) damage as well as decreasing the global speed of all affected targets by %d%%.
  		The damage done will scale with your Spellpower.
  ```
- **译文**：
  ```text
  增加半径 %d 范围内的重力 %d 回合，造成 %0.2f 物理（重力）伤害，并降低所有目标的全局速度 %d%%。
  		受法术强度影响，伤害按比例加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `gravity.lua:266`（参数为 `radius, duration, damDesc(...), slow*100`）。`%d`、`%d`、`%0.2f`、`%d%%` 4 个占位符完全匹配且顺序一致；`global speed` 正确遵循术语表译为“全局速度”。

---

### entry-01579
- **位置**：`mod-tome.lua:22060`；`section：mod-tome/data/talents/chronomancy/guardian.lua`；`source_tag：delayedLogMessage`
- **原文**：`#STEEL_BLUE##Source# shares damage with %s guardian!`
- **译文**：`#STEEL_BLUE##Source#和%s的守卫共享伤害！`
- **复核结论**：未发现问题
- **核验依据**：源码 `guardian.lua:104`（参数传入 `string.his_her(self)`）。颜色标签 `#STEEL_BLUE#` 与 `#Source#` 完好，`%s` 与“的守卫”搭配符合中文语序，感叹号对齐。

---

### entry-01580
- **位置**：`mod-tome.lua:22068`；`section：mod-tome/data/talents/chronomancy/guardian.lua`；`source_tag：logSeen`
- **原文**：`#ORCHID#%s has recovered!#LAST#`
- **译文**：`#ORCHID#%s恢复了！#LAST#`
- **复核结论**：未发现问题
- **核验依据**：源码 `guardian.lua:145`（负面效果清除日志）。颜色标签 `#ORCHID#` 与 `#LAST#` 闭合完整，`%s` 占位符保留，感叹号对齐。

---

### entry-01581
- **位置**：`mod-tome.lua:22072`；`section：mod-tome/data/talents/chronomancy/guardian.lua`；`source_tag：talent name`
- **原文**：`Warden's Focus`
- **译文**：`守卫者专注`
- **复核结论**：未发现问题
- **核验依据**：源码 `guardian.lua:159`。技能名翻译规范统一。

---

### entry-01582
- **位置**：`mod-tome.lua:22074`；`section：mod-tome/data/talents/chronomancy/guardian.lua`；`source_tag：logPlayer`
- **原文**：`You must pick a focus target.`
- **译文**：`你必须选择一个集中目标。`
- **复核结论**：未发现问题
- **核验依据**：源码 `guardian.lua:186`（未选取目标时的提示）。句号对齐，语义准确。

---

### entry-01583
- **位置**：`mod-tome.lua:22075`；`section：mod-tome/data/talents/chronomancy/guardian.lua`；`source_tag：tformat`
- **原文**：
  ```text
  Attack the target with either your ranged or melee weapons for %d%% weapon damage.  For the next %d turns random targeting, such as from Blink Blade and Warden's Call, will focus on this target.
  		Attacks against this target gain %d%% critical chance and critical strike power while you take %d%% less damage from all enemies whose rank is lower then that of your focus target.
  ```
- **译文**：
  ```text
  使用你的远程或者近战武器对目标造成 %d%% 武器伤害。  在接下来的 %d 回合中，你的随机目标技能，比如闪烁灵刃和守卫召唤将会集中命中目标。
  		对这个目标的攻击获得 %d%% 额外的暴击几率和暴击加成，同时其他分级低于目标的单位对你造成的伤害减少 %d%%。
  ```
- **复核结论**：未发现问题
- **核验依据**：源码 `guardian.lua:207`，结合 `Combat.lua:1961` 与 `magical.lua:4047`。
  1. 占位符共 4 个：`%d%%`（武器伤害）、`%d`（持续回合）、`%d%%`（暴击率与暴击加成）、`%d%%`（减伤比例），顺序与含义完全吻合。
  2. 源码逻辑中 `eff.power` 同时增加暴击几率（`chance + eff.power`）与暴击伤害加成（`crit_power_add + eff.power/100`），中文表述“获得 %d%% 额外的暴击几率和暴击加成”将二者精准合流；
  3. `src.rank < eff.target.rank` 与“其他分级低于目标的单位”完全契合。

---

### entry-01584
- **位置**：`mod-tome.lua:22089`；`section：mod-tome/data/talents/chronomancy/induced-phenomena.lua`；`source_tag：logPlayer`
- **原文**：`You must have Cosmic Cycle active to use this talent.`
- **译文**：`你必须开启宇宙圈才能使用这一技能。`
- **复核结论**：未发现问题
- **核验依据**：源码 `induced-phenomena.lua:159`。严格