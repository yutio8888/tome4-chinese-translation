本批次（batch-081）复核完成。在开展复核前已对冻结文件哈希进行校验，SHA-256 值为 `0a34ba4075d9d2abcc17ac28136428ec1afe0b62ea926fe23192800e12f04626`，与要求完全一致。

本批条目全部位于 `mod-tome/data/timed_effects/magical.lua`（在 `mod-tome.lua` 中的行号范围为 35052 至 35500），核验基准为公开固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下的对应源码文件及同 section 语境。条目编号 `entry-02612` 至 `entry-02651` 共 40 条逐条核验结论如下：

---

### entry-02612
- **原文**：`Damage Shield`
- **译文**：`伤害护盾`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:802` 中效果 `DAMAGE_SHIELD` 的 `desc = _t"Damage Shield"`。术语库标准译名 `Damage Shield` -> `伤害护盾`，无参数与控制符，准确无误。

---

### entry-02613
- **原文**：`The target is surrounded by a magical shield, absorbing %d/%d damage %s before it crumbles.`
- **译文**：`目标被一层魔法护盾包围，吸收（%d/%d）伤害%s直到其破裂。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:803`，格式化参数依次传入当前吸收量 `self.damage_shield_absorb`、最大吸收量 `eff.power` 及反射提示文本 `%s`（对应第 35054 行 `(reflecting %d%% back to the attacker)`）。占位符 `%d/%d` 与 `%s` 顺序、类型与数量一致；中文添加全角括号“（%d/%d）”符合同 section（如第 35048 行）一贯排版风格。

---

### entry-02614
- **原文**：`You have expended the power of your Radiance temporarily reducing its radius to 1.`
- **译文**：`你消耗了光辉之力，暂时把光照半径降低到 1 码。`
- **结论**：细微观察
- **可核验依据**：对应源码 `magical.lua:914` 中效果 `RADIANCE_DIM`。机制上 `your Radiance` 指太阳骑士的专属技能“光辉”（`T_RADIANCE`），`its radius` 指光辉光环半径 `radianceRadius(self)`。译文“光照半径”虽与光辉本身提供的照明范围相关，但游戏中基础属性亦有独立的光照范围（`lite`），此处译为“光辉半径”或“其光环半径”能更精准契合技能机制。

---

### entry-02615
- **原文**：`#Target# is no longer cursed.`
- **译文**：`#Target#不再被诅咒。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:937` 中 `CURSE_VULNERABILITY` 的 `on_lose`。`#Target#` 实体标签保留完整，语意准确。

---

### entry-02616
- **原文**：`#Target# no longer vulnerable to disease.`
- **译文**：`#Target#恢复了对疾病的抵抗力。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1047` 中 `CORRUPTING_STRIKE` 效果移除提示。获得时为“对疾病毫无抵抗力”（`on_gain`），移除时译为“恢复了对疾病的抵抗力”，语境自然流畅，标签完整。

---

### entry-02617
- **原文**：`Hurricane`
- **译文**：`飓风`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1161` 中效果 `HURRICANE` 的 `desc`。术语准确。

---

### entry-02618
- **原文**：`+Hurricane`
- **译文**：`+飓风`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1167` 中 `on_gain` 状态栏标识。符号 `+` 与名称一致。

---

### entry-02619
- **原文**：`-Hurricane`
- **译文**：`-飓风`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1168` 中 `on_lose` 状态栏标识。符号 `-` 与名称一致。

---

### entry-02620
- **原文**：`#Target# casts a protective shield just in time!`
- **译文**：`#Target#及时召唤出了一个保护护盾！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1271` 中 `PREMONITION_SHIELD`（感应护盾）触发时的 `on_gain` 日志。`#Target#` 标签保留，感叹号保留，机制符合受到对应伤害前及时升起护盾的特征。

---

### entry-02621
- **原文**：`A divine glyph recently triggered, providing %d%% light and darkness affinity and resistence.`
- **译文**：`圣印最近被触发过，提供 %d%% 光系和暗影伤害亲和与抗性。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1448`（效果 `EMPOWERED_GLYPHS`）。`activate` 函数中赋予 `damage_affinity`（亲和）与 `resists`（抗性），占位符 `%d%%` 匹配正确，伤害类别光系与暗影对应源码机制。

---

### entry-02622
- **原文**：`The target's spellpower has been increased by %d and will continue to increase by %d each turn.`
- **译文**：`目标法术强度已提高 %d，每回合进一步提高 %d。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1733`（效果 `GATHER_THE_THREADS`）。两个 `%d` 依次对应当前累积法强（`eff.cur_power or eff.power`）及每回合增量（`eff.power/5`），参数顺序与类型完全对应。

---

### entry-02623
- **原文**：`Temporal Destabilization`
- **译文**：`时空失稳`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1876`（效果 `TEMPORAL_DESTABILIZATION_START` 的 `desc`）。专名翻译标准。

---

### entry-02624
- **原文**：`Target is destabilized and in %d turns will start suffering %0.2f temporal damage per turn.  If it dies with this effect active after the damage starts it will explode.`
- **译文**：`目标陷入时空失稳状态，%d 回合后将开始每回合受到 %0.2f 点时空伤害。伤害开始后，若目标在该效果持续期间死亡，就会爆炸。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1877`，参数为持续倒计时 `%d`（`eff.dur`）与每回合伤害 `%0.2f`（`eff.dam`），占位符顺序与精度完整保留，爆炸条件机制还原准确。

---

### entry-02625
- **原文**：`+Temporal Destabilization`
- **译文**：`+时空失稳`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1882` 中 `on_gain` 标识。前缀 `+` 与译名一致。

---

### entry-02626
- **原文**：`-Temporal Destabilization`
- **译文**：`-时空失稳`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1883` 中 `on_lose` 标识。前缀 `-` 与译名一致。

---

### entry-02627
- **原文**：`Target is destabilized and suffering %0.2f temporal damage per turn.  If it dies with this effect active it will explode.`
- **译文**：`目标陷入时空失稳状态，每回合受到 %0.2f 时空伤害。如果目标在效果持续时死亡则会爆炸。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1896`（第二阶段持续伤害效果 `TEMPORAL_DESTABILIZATION` 的 `long_desc`）。占位符 `%0.2f` 匹配，死亡引爆机制描述准确。

---

### entry-02628
- **原文**：`The target is moving is %d%% faster.`
- **译文**：`目标移动速度增加 %d%%。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:1917`（效果 `CELERITY`）。英文原文有低级语法冗余（“is moving is”），译文修正了语病并准确映射 `%d%%`（`eff.speed * 100 * eff.charges`）。

---

### entry-02629
- **原文**：`#CRIMSON#A piece of the soul of %s is torn apart by Impending Doom!`
- **译文**：`#CRIMSON#%s的灵魂被灾厄降临撕裂了一片！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2059`（`game.logSeen`）。颜色代码 `#CRIMSON#` 保留，`%s` 接收 `self:getName()`，`Impending Doom` 与技能/效果译名“灾厄降临”一致。

---

### entry-02630
- **原文**：`Abyssal Shroud`
- **译文**：`深渊裹幕`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2099`（效果 `ABYSSAL_SHROUD` 的 `desc`）。专名翻译贴切。

---

### entry-02631
- **原文**：`The target's lite radius has been reduced by %d, and its darkness resistance by %d%%.`
- **译文**：`目标光照范围减少 %d，暗影抗性下降 %d%%。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2100`，参数为减光值 `%d`（`eff.lite`）与减抗值 `%d%%`（`eff.power`），机制还原准确。

---

### entry-02632
- **原文**：`#Target# is free from the abyss.`
- **译文**：`#Target#逃离了深渊。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2106`（`ABYSSAL_SHROUD` 的 `on_lose`）。`#Target#` 标签完整，语意贴切。

---

### entry-02633
- **原文**：`#Target# spins fate.`
- **译文**：`#Target#编织命运。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2127`（`SPIN_FATE` 的 `on_gain`）。`#Target#` 标签完整，专名动词对应命运之丝。

---

### entry-02634
- **原文**：`#Target# is free from the woeful disease.`
- **译文**：`#Target#摆脱了恐怖疾病。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2278`（`WOEFUL_DISEASE` 的 `on_lose`）。`#Target#` 标签完整，语意准确。

---

### entry-02635
- **原文**：`The target is infected by a disease doing %0.2f blight damage per turn.%s`
- **译文**：`目标感染疾病，每回合造成 %0.2f 点枯萎伤害。%s`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2435`（效果 `GHOUL_ROT` 的 `long_desc`）。`%0.2f` 传入 `eff.dam`，`%s` 传入条件追加文本 `ghoulify`（对应第 35329 行）；占位符类型与顺序匹配。

---

### entry-02636
- **原文**：`#Target# is afflicted by ghoul rot!`
- **译文**：`#Target#被食尸鬼的疾病感染！`
- **结论**：细微观察
- **可核验依据**：对应源码 `magical.lua:2441`（`GHOUL_ROT` 的 `on_gain`）。在同 section 第 35328 行及第 35329 行中，该效果与机制均统一译为“尸鬼腐蚀”（`t("Ghoul Rot", "尸鬼腐蚀", "_t")`、`"如果目标在尸鬼腐蚀期间死亡..."`）。此处在 `on_gain` 中意译为“食尸鬼的疾病”，虽语意通顺，但与效果名称未保持统一。

---

### entry-02637
- **原文**：`#Target# is free from the ghoul rot.`
- **译文**：`#Target#摆脱了食尸鬼的疾病。`
- **结论**：细微观察
- **可核验依据**：对应源码 `magical.lua:2442`（`GHOUL_ROT` 的 `on_lose`）。同 entry-02636，此处将 `ghoul rot` 意译为“食尸鬼的疾病”，与同效果的专名“尸鬼腐蚀”不一致。

---

### entry-02638
- **原文**：`#Target# warded against %s!`
- **译文**：`#Target#吸收了%s的攻击！`
- **结论**：存在疑点
- **可核验依据**：对应源码 `magical.lua:2527` 中效果 `WARD` 的 `on_gain` 回调：
  `on_gain = function(self, eff) return ("#Target# warded against %s!"):tformat(DamageType.dam_def[eff.d_type].name), _t"+Ward" end`
  此处是在角色获得该系守护结界（例如施放技能获得火焰守护）时的状态获得提示，此时角色并未受到任何攻击；实际吸收攻击是在随后的 `absorb` 回调中触发并打印日志（第 35351 行：“你的%s守护吸收了伤害！”）。译文处理为“吸收了%s的攻击！”属于获得状态与承受结算的时机/语意混淆，机制上应为“受到抵御%s伤害的守护！”或“获得了抵御%s的守护！”。

---

### entry-02639
- **原文**：
  ```text
  The target is out of phase with reality, increasing defense by %d, resist all by %d%%, and reducing the duration of detrimental timed effects by %d%%.
  These effects cap at 40%%.
  ```
- **译文**：
  ```text
  目标脱离了现实相位，增加 %d 闪避，%d%% 全体伤害抗性并减少 %d%% 所有负面状态的持续时间。
  最高效果为 40%%。
  ```
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2584`（效果 `OUT_OF_PHASE`）。参数依次为防御闪避 `%d`、全抗 `%d%%` 与负面效果缩减 `%d%%`；转义 `%` 与换行完全匹配，术语与机制准确无误。

---

### entry-02640
- **原文**：`#Target# is focused by an arcane vortex!`
- **译文**：`#Target#被奥术漩涡围绕！`
- **结论**：细微观察
- **可核验依据**：对应源码 `magical.lua:2677`（`ARCANE_VORTEX` 的 `on_gain`）。奥术漩涡施加在敌方目标身上并跟随其移动（“An arcane vortex follows the target”），原文“focused by”字面为“被聚焦/被锁定为焦点”，译文意译为“围绕”，虽符合漩涡贴身特效但在字面色彩上略有偏离。

---

### entry-02641
- **原文**：`Fires an arcane explosion each turn doing %0.2f arcane damage in radius 2.`
- **译文**：`每回合触发一个奥术爆炸，在 2 码范围内造成 %0.2f 奥术伤害。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2718`（效果 `AETHER_BREACH` 的 `long_desc`）。浮点占位符 `%0.2f` 保留，范围参数 2 译为 2 码符合惯例。

---

### entry-02642
- **原文**：`#Target# begins channeling arcane through a breach in reality!`
- **译文**：`#Target#从现实的裂口中传导奥术能量！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2723`（`AETHER_BREACH` 的 `on_gain`）。`#Target#` 标签保留；此处 breach 结合以太裂隙语境译为“现实的裂口”，准确恰当。

---

### entry-02643
- **原文**：`The target is afflicted with a magical poison and is suffering %0.2f arcane damage per turn.  All resistances are reduced by 10%%%s.`
- **译文**：`目标被魔法毒素感染，每回合受到 %0.2f 奥术伤害，所有伤害抗性下降 10%% %s。`
- **结论**：存在疑点
- **可核验依据**：对应源码 `magical.lua:2794`（效果 `VULNERABILITY_POISON` 的 `long_desc`）。源码第 2794 行通过动态拼接第二个参数：
  `... All resistances are reduced by 10%%%s."):tformat(eff.src:damDesc("ARCANE", eff.power), poison_effect and (" and poison resistance is reduced by %s%%"):tformat(...) or "")`
  在原英文中，`10%%%s.` 之间无空格。中文译文在 `10%%` 与 `%s` 之间加入了一个半角空格（`10%% %s。`）。当 `poison_effect` 为空时，动态展开结果为 `所有伤害抗性下降 10% 。`（句号前带有多余空格）；当与 entry-02644 拼接时，则展开为 `所有伤害抗性下降 10% ，且...`（全角逗号前带有半角空格），存在排版瑕疵。

---

### entry-02644
- **原文**：` and poison resistance is reduced by %s%%`
- **译文**：`，且毒素抗性下降 %s%%`
- **结论**：存在疑点
- **可核验依据**：对应源码 `magical.lua:2794` 内部动态拼接子句。与 entry-02643 联动时，由于 entry-02643 末尾已带半角空格，导致拼接后出现 `10% ，且...` 的异常空格组合。此外需注意此句开头的全角逗号与主句拼接时的协同标点规范。

---

### entry-02645
- **原文**：`#Target# is magically poisoned!`
- **译文**：`#Target#被魔法毒素感染！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2800`（`VULNERABILITY_POISON` 的 `on_gain`）。`#Target#` 标签保留，语意准确。

---

### entry-02646
- **原文**：`#Target# threads time as a shell!`
- **译文**：`#Target#将时间编织成外壳！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2889`（`TEMPORAL_FORM` 的 `on_gain`）。`#Target#` 标签保留，修辞符合时空法术风格。

---

### entry-02647
- **原文**：`#Target# turns into a losgoroth!`
- **译文**：`#Target#变成了罗斯戈洛斯！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:2946`（`CORRUPT_LOSGOROTH_FORM` 的 `on_gain`）。生物名称 losgoroth 译为“罗斯戈洛斯”，与同 section 译名完全一致。

---

### entry-02648
- **原文**：`%s damage increased by 20%%.`
- **译文**：`%s 伤害增加 20%%。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:3114`（`BORN_INTO_MAGIC`）。`%s` 传入大写的伤害类别名称（`DamageType:get(eff.damtype).name:capitalize()`），占位符与转义百分号完整一致。

---

### entry-02649
- **原文**：`#Target# is energized and protected by the Sun!`
- **译文**：`#Target#被阳光保护并充能！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:3225`（`SUNCLOAK` 的 `on_gain`）。`#Target#` 标签保留，语意准确。

---

### entry-02650
- **原文**：`#Target# is marked by light!`
- **译文**：`#Target#被光之印记标记！`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:3246`（`MARK_OF_LIGHT` 的 `on_gain`）。`#Target#` 标签保留，与技能名“光之印记”契合。

---

### entry-02651
- **原文**：`All healing done to the target will instead turn into %d%% blight damage.`
- **译文**：`目标受到的所有治疗会逆转为 %d%% 枯萎伤害。`
- **结论**：未发现问题
- **可核验依据**：对应源码 `magical.lua:3399`（效果 `HEALING_INVERSION` 的 `long_desc`）。机制上通过 `callbackOnHeal` 将治疗量清零并将其实际比例转换为枯萎伤害（`DamageType.BLIGHT`）。占位符 `%d%%` 匹配，机制描述完全忠实。