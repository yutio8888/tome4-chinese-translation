本批次为 **batch-085**，只读复核已完成。

### 文件哈希核对
- **目标文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-085.md`
- **预期 SHA-256**：`1a3bc01d30705a7fa77764937e92a2232ba5b75d7637d6f7fd090810c5c88fbe`
- **实测 SHA-256**：`1a3bc01d30705a7fa77764937e92a2232ba5b75d7637d6f7fd090810c5c88fbe`（校验一致）
- **条目范围**：`entry-02772` 至 `entry-02811`，共 40 条。
- **核验源码依据**：根据 `source-access.json`，engine/tome 固定 commit 为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`，对应公开源码文件为 `game/modules/tome/data/timed_effects/other.lua`。同 section 译文上下文来自 `mod-tome.lua`。

---

### 逐条复核报告

#### entry-02772
- **原文**：`The creature has found a state of clarity and sees the world for what it is (+%d%% global speed).`
- **译文**：`目标对这个世界有着更加清晰的认识 (+%d%% 全局速度)。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:1992`（`CLARITY` 状态）。源码 `("..."):tformat(eff.power * 100)` 绑定全局速度加成属性 `global_speed_add`，术语 `global speed` 对应“全局速度”，占位符 `+%d%%`、括号及句末标点准确。

#### entry-02773
- **原文**：`While this effect holds you can decide recent history did not happen the way it did.`
- **译文**：`该效果持续时你可以裁定最近发生的事并非以原本的方式发生。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2222`（`REVISIONIST_HISTORY` 状态）。文本准确表述时空系重写历史的技能机制，句意通顺完整。

#### entry-02774
- **原文**：`Zone-wide effect: +10% fire damage, -10% fire resistance, -10% armour, -2 sight range.`
- **译文**：`区域效果：+10% 火焰伤害，-10% 火焰抗性，-10% 护甲值，-2 可视范围。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2276`（`ZONE_AURA_FIRE`）。源码实际修改 `inc_damage[DamageType.FIRE]=10`、`resists[DamageType.FIRE]=-10`、`combat_armor=-10%`、`sight=-2`。术语 `armour` 对应“护甲值”，数值与正负符号完全一致。

#### entry-02775
- **原文**：`Zone-wide effect: +10% cold damage, -10% cold resistance, -10% physical save, -20% confusion immunity.`
- **译文**：`区域效果：+10% 寒冰伤害，-10% 寒冰抗性，-10% 物理豁免，-20% 混乱免疫。`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:2297`（`ZONE_AURA_COLD`）。底层修改 `inc_damage[DamageType.COLD]=10`、`resists[DamageType.COLD]=-10`、`combat_physresist=-10%`、`confusion_immune=-0.2`。各项数值与机制完全对应。细微观察在于术语库中 `cold` 伤害类型标准译名为“寒冷”（同批次 entry-02801、02805 均译为“寒冷”），此处译作“寒冰”，存在批内微小不一致，但机制理解无实质歧义。

#### entry-02776
- **原文**：`Zone-wide effect: +10% lightning damage, -10% lightning resistance, -10% physical power, -20% stun immunity.`
- **译文**：`区域效果：+10% 闪电伤害，-10% 闪电抗性，-10% 物理强度，-20% 震慑免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2318`（`ZONE_AURA_LIGHTNING`）。底层对应 `DamageType.LIGHTNING` 伤害/抗性、`combat_dam`（物理强度）与 `stun_immune`。术语 `physical power`（物理强度）、`stun`（震慑）准确，符号与数值一致。

#### entry-02777
- **原文**：`Zone-wide effect: +10% acid damage, -10% acid resistance, -10% defense, -20% disarm immunity.`
- **译文**：`区域效果：+10% 酸性伤害，-10% 酸性抗性，-10% 闪避，-20% 缴械免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2339`（`ZONE_AURA_ACID`）。底层对应 `DamageType.ACID` 伤害/抗性、`combat_def`（闪避）与 `disarm_immune`。数值、正负号与术语一致。

#### entry-02778
- **原文**：`Zone-wide effect: +10% darkness damage, -10% darkness resistance, -10% mental save, -20% fear immunity.`
- **译文**：`区域效果：+10% 暗影伤害，-10% 暗影抗性，-10% 精神豁免，-20% 恐惧免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2360`（`ZONE_AURA_DARKNESS`）。底层对应 `DamageType.DARKNESS` 伤害/抗性、`combat_mentalresist`（精神豁免）与 `fear_immune`。各项属性、符号及数值一致。

#### entry-02779
- **原文**：`Eerie silence`
- **译文**：`诡异的寂静`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2379`（`ZONE_AURA_MIND` 的 `desc`）。译名准确贴切。

#### entry-02780
- **原文**：`Zone-wide effect: +10% mind damage, -10% mind resistance, -10% spellpower, -20% silence immunity.`
- **译文**：`区域效果：+10% 精神伤害，-10% 精神抗性，-10% 法术强度，-20% 沉默免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2381`（`ZONE_AURA_MIND`）。底层对应 `DamageType.MIND` 伤害/抗性、`combat_spellpower`（法术强度）与 `silence_immune`。术语与符号数值一致。

#### entry-02781
- **原文**：`Zone-wide effect: +10% light damage, -10% light resistance, -10% accuracy, -20% blind immunity.`
- **译文**：`区域效果：+10% 光系伤害，-10% 光系抗性，-10% 命中，-20% 致盲免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2402`（`ZONE_AURA_LIGHT`）。底层对应 `DamageType.LIGHT` 伤害/抗性、`combat_atk`（命中）与 `blind_immune`。术语与符号数值一致。

#### entry-02782
- **原文**：`Zone-wide effect: +10% arcane damage, -10% arcane resistance, -10% armour hardiness, -20% stoning immunity.`
- **译文**：`区域效果：+10% 奥术伤害，-10% 奥术抗性，-10% 护甲强度，-20% 石化免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2423`（`ZONE_AURA_ARCANE`）。底层对应 `DamageType.ARCANE` 伤害/抗性、`combat_armor_hardiness`（护甲强度）与 `stone_immune`。术语与符号数值一致。

#### entry-02783
- **原文**：`Zone-wide effect: +10% temporal damage, -10% temporal resistance, -10% spell save, -20% pinning immunity.`
- **译文**：`区域效果：+10% 时空伤害，-10% 时空抗性，-10% 法术豁免，-20% 定身免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2444`（`ZONE_AURA_TEMPORAL`）。底层对应 `DamageType.TEMPORAL` 伤害/抗性、`combat_spellresist`（法术豁免）与 `pin_immune`。术语与符号数值一致。

#### entry-02784
- **原文**：`Zone-wide effect: +10% physical damage, -10% physical resistance, -10% mindpower, -20% knockback immunity.`
- **译文**：`区域效果：+10% 物理伤害，-10% 物理抗性，-10% 精神强度，-20% 击退免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2465`（`ZONE_AURA_PHYSICAL`）。底层对应 `DamageType.PHYSICAL` 伤害/抗性、`combat_mindpower`（精神强度）与 `knockback_immune`。术语与符号数值一致。

#### entry-02785
- **原文**：`Zone-wide effect: +10% blight damage, -10% blight resistance, -20% healing mod, -20% disease immunity.`
- **译文**：`区域效果：+10% 枯萎伤害，-10% 枯萎抗性，-20% 治疗加成，-20% 疾病免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2486`（`ZONE_AURA_BLIGHT`）。底层对应 `DamageType.BLIGHT` 伤害/抗性、`healing_factor`（治疗加成）与 `disease_immune`。术语与符号数值一致。

#### entry-02786
- **原文**：`Zone-wide effect: +10% nature damage, -10% nature resistance, -10% ranged defense, -20% poison immunity.`
- **译文**：`区域效果：+10% 自然伤害，-10% 自然抗性，-10% 远程闪避，-20% 毒素免疫。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2507`（`ZONE_AURA_NATURE`）。底层对应 `DamageType.NATURE` 伤害/抗性、`combat_def_ranged`（远程闪避）与 `poison_immune`。术语与符号数值一致。

#### entry-02787
- **原文**：`The target is protected by the Eidolon, no creature may harm it (except self-harm).`
- **译文**：`目标受到艾德隆保护，没有生物可以伤害它（自残除外）。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2590`（`EIDOLON_PROTECT`）。底层机制赋予 `invulnerable_others = 1`。神祇译名与豁免例外括号说明准确。

#### entry-02788
- **原文**：`The target is under the effect of the cloak of deception, making it look human.`
- **译文**：`目标受到欺诈斗篷的效果影响，使它看上去像人类一样。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:2607`（`CLOAK_OF_DECEPTION`）。底层逻辑将亡灵种族伪装显示为 `fake_race = "Human"`。道具名称及种族术语准确。

#### entry-02789
- **原文**：`You are suffocating! Each turn you lose an ever increasing percent of your total life (currently %d%%)`
- **译文**：`你正在窒息！每回合按比例损失生命，且越来越多（现在 %d%%）`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:2634`（`SUFFOCATING`）。源码实际按 `self.max_life * eff.dam / 100` 造成伤害，且每回合 `eff.dam = util.bound(eff.dam + 5, 20, 100)` 递增。译文“按比例损失生命”未明确写出“总生命/最大生命”，略偏意译，但递增机制与占位符 `%d%%` 保留准确，无阻断缺陷。

#### entry-02790
- **原文**：`#STEEL_BLUE#You are brought back from your repreive!`
- **译文**：`#STEEL_BLUE#被从避难所带了回去！`
- **复核结论**：存在疑点
- **可核验依据**：对应 `other.lua:2886`（`TEMPORAL_REPRIEVE` 结束逻辑：`game.logPlayer(game.player, "#STEEL_BLUE#You are brought back from your repreive!")`）。译文缺少主语“你”，导致战斗日志直接输出为无主语句“被从避难所带了回去！”，句式残缺；且脱离避难所回到现实的语境在中文日志中表述为“被从避难所带了回来！”或“你脱离了避难所！”更符合方向与实际效果。

#### entry-02791
- **原文**：`#STEEL_BLUE##Source# shares damage with %s fugue clones!`
- **译文**：`#STEEL_BLUE##Source#和%s时空克隆共享伤害！`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:2933`（`TEMPORAL_FUGUE` 的 `delayedLogMessage`）。代码传入 `string.his_her(self)`，在中文运行时求值为“他的/她的/它的”，格式化后为“#Source#和他的时空克隆共享伤害！”，语法通顺，占位符 `#Source#` 与 `%s` 匹配无误。观察在于同 section 前文 36741 行将 `fugue clones` 译作“时空复制体”，此处译为“时空克隆”，存在轻微用词不一致。

#### entry-02792
- **原文**：`Hit Penalty`
- **译文**：`命中惩罚`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3097`（`2H_PENALTY` 状态名称）。单手持双手武器的命中惩罚状态，译名标准准确。

#### entry-02793
- **原文**：
```text
Currently Twisted Anomaly: %s

		%s
```
- **译文**：
```text
当前受控的异常：%s

		%s
```
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3113`（`TWIST_FATE` 描述）。两个 `%s` 分别接收异常技能名称与信息，空行及第二行前导的双制表符 `\t\t` 格式完全对齐。

#### entry-02794
- **原文**：`%s is focusing on this target.`
- **译文**：`%s 正在专注于此目标。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3152`（`WARDEN_S_TARGET` 描述）。`%s` 传入施法者名称 `eff.src:getName()`，占位符与标点准确。

#### entry-02795
- **原文**：`+Warden's Focus`
- **译文**：`+守卫者专注`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3158`。获得状态时的漂字信息，加号前缀与技能译名准确。

#### entry-02796
- **原文**：`-Warden's Focus`
- **译文**：`-守卫者专注`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3159`。失去状态时的漂字信息，减号前缀与技能译名准确。

#### entry-02797
- **原文**：`Zone-wide effect: +20 mindpower, +2 life regen, -1 equilibrium per turn, -20% resistance penetration.`
- **译文**：`区域效果：+20 精神强度，+2 生命恢复，-1 失衡值 / 回合，-20% 抗性穿透。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3192`（`ZONE_AURA_GORBAT`）。底层数值 `combat_mindpower=20`、`life_regen=2`、`equilibrium_regen=-1`、`resists_pen={all=-20}`。术语 `mindpower`（精神强度）、`equilibrium`（失衡值）及各数值符号完全一致。

#### entry-02798
- **原文**：`Zone-wide effect: +20 magic, +2 mana regen, -20 accuracy, -20 stealth power.`
- **译文**：`区域效果：+20 魔法，+2 法力回复，-20 命中，-20 潜行强度。`
- **复核结论**：存在疑点
- **可核验依据**：对应 `other.lua:3213`（`ZONE_AURA_VOR`）。底层代码为 `self:effectTemporaryValue(eff, "inc_stats", {[Stats.STAT_MAG] = 20})`，此处提升的是基础核心主属性“魔力”（Magic/STAT_MAG，见术语快照第 512 行 `Magic -> 魔力`）。译文将其译作“+20 魔法”，与法术/魔法概念混淆，偏离了主属性术语“魔力”。

#### entry-02799
- **原文**：`Zone-wide effect: +20 defense, +20 all saves, -20 spell power.`
- **译文**：`区域效果：+20 闪避，+20 全豁免，-20 法术强度。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3234`（`ZONE_AURA_GRUSHNAK`）。底层提升 `combat_def=20`、三项豁免各 20（全豁免）、降低 `combat_spellpower=-20`。术语与数值完全一致。

#### entry-02800
- **原文**：`Zone-wide effect: +10% critical chance, +20% critical damage, -20% nature and blight resistance.`
- **译文**：`区域效果：+10% 暴击几率，+20% 暴击伤害，-20% 自然抗性和枯萎抗性。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3255`（`ZONE_AURA_RAKSHOR`）。底层提升三系暴击几率 10%、暴击伤害加成 `combat_critical_power=20`、降低自然与枯萎抗性各 20%。术语与数值准确。

#### entry-02801
- **原文**：`Zone-wide effect: Air decreases over time. If you run out of air you will start losing life. Look for bubbles to recover air. The water also reduces stun resistance by 10% and fire damage is reduced by 10%, however cold damage is increased by 10%.`
- **译文**：`区域效果： 空气值随时间损失，空气用光后将损失生命。寻找气泡来回复空气值。水同时令震慑免疫和火焰伤害下降 10%，同时增加 10% 寒冷伤害。`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:3276`（`ZONE_AURA_UNDERWATER`）。底层对应 `stun_immune=-0.1`、`inc_damage COLD=10, FIRE=-10`，数值和机制完全准确。细微观察：中文冒号后多了一个半角空格（`区域效果： 空气值...`）；且后半句重复出现“同时”（“水同时令...同时增加...”）。

#### entry-02802
- **原文**：`Zone-wide effect: The flames of the Fearscape increase all fire and blight damage by 10%, but the weird gravity reduces knockback resistance by 20%.`
- **译文**：`区域效果：恶魔空间的火焰使所有火焰和枯萎伤害增加 10%，但其诡异的重力会使击退抗性降低 20%。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3297`（`ZONE_AURA_FEARSCAPE`）。底层对应 `knockback_immune=-0.2`、`inc_damage FIRE=10, BLIGHT=10`。专有名词 `Fearscape` 译为“恶魔空间”，数值符号准确。

#### entry-02803
- **原文**：`Zone-wide effect: You seem to be outside the normal spacetime continuum. +10% physical resistance, -10% temporal resistance and -20% teleport resistance.`
- **译文**：`区域效果：你似乎处于通常时空之外。+10% 物理抗性，-10% 时空抗性，-20% 传送抗性。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3316`（`ZONE_AURA_OUT_OF_TIME`）。底层对应 `resists PHYSICAL=10, TEMPORAL=-10` 与 `teleport_immune=-0.2`。术语与数值符号完全一致。

#### entry-02804
- **原文**：`Spellblaze Aura`
- **译文**：`魔法大爆炸光环`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3334`（`ZONE_AURA_SPELLBLAZE` 状态名）。专有名词 `Spellblaze` 译为“魔法大爆炸”（符合术语库），准确无误。

#### entry-02805
- **原文**：`Zone-wide effect: The power of the Spellblaze still burns here. -10% resistance to fire, arcane and blight damage, but +10% cold resistance. WARNING: The powerful magic here reflects teleportation magic!`
- **译文**：`区域效果：魔法大爆炸的火焰仍在燃烧，-10% 火焰、枯萎、奥术抗性，+10% 寒冷抗性。警告：强大的魔法能量可能干扰传送法术！`
- **复核结论**：存在疑点
- **可核验依据**：对应 `other.lua:3336`（`ZONE_AURA_SPELLBLAZE`）。原文后半句为明确的肯定句 `WARNING: The powerful magic here reflects teleportation magic!`（反射传送法术），译文译作“可能干扰传送法术！”，将确定性的“反射”（reflects）弱化并改写为了概率性的“可能干扰”，与原文本意及实际机制描述存在偏差；另句首 `The power of the Spellblaze`（魔法大爆炸的威能）被意译为“魔法大爆炸的火焰仍在燃烧”。

#### entry-02806
- **原文**：`Zone-wide effect: Strong scents fill the air and make you feel drowsy. If the timer reaches 0 you will fall into a dreaming sleep state. -10% mind resistance, -20% sleep resistance, +10% nature damage.`
- **译文**：`区域效果： 强烈的气味充满了空气，让你感觉困倦。倒计时结束时，你将进入梦境。-10% 精神抗性，-20% 睡眠免疫，+10% 自然伤害。`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:3355`（`ZONE_AURA_CALDERA`）。底层机制 `sleep_immune=-0.2`（译为睡眠免疫准确对应属性键）、`inc_damage NATURE=10`、`resists MIND=-10`。细微观察：中文冒号后多了一个半角空格（`区域效果： 强烈的气味...`）；“进入梦境”意译自“fall into a dreaming sleep state”，语义符合沉睡机制。

#### entry-02807
- **原文**：`Zone-wide effect: A huge thunderstorm rages above you. +10 lightning damage, -10% stun resistance.`
- **译文**：`区域效果： 强大的雷暴在你头顶轰鸣。+10% 闪电伤害，-10% 震慑免疫。`
- **复核结论**：细微观察
- **可核验依据**：对应 `other.lua:3374`（`ZONE_AURA_THUNDERSTORM`）。底层代码逻辑为 `self:effectTemporaryValue(eff, "inc_damage", {[DamageType.LIGHTNING]=10})` 和 `stun_immune=-0.1`。英文原文漏写了百分号（`+10 lightning damage`），译文依据代码底层 `inc_damage` 的实际百分比机制正确补充为 `+10% 闪电伤害`，符合实际游戏机制；另中文冒号后多了一个半角空格。

#### entry-02808
- **原文**：`Zone-wide effect: Your Phase Door spell is super easy to use here, allowing you to target it regardless of level. Any projectiles is slowed down by 80%.`
- **译文**：`区域效果：你的相位之门法术在这里极其容易施展，不论等级如何，都能指定位置。所有抛射物速度减慢 80%。`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3393`（`ZONE_AURA_ABASHED`）。底层设定 `slow_projectiles_outgoing = 80` 与 `phase_door_force_precise = 1`。相位之门无视技能等级精确指定落点与弹道减速 80% 均准确对应。

#### entry-02809
- **原文**：
```text
Has %d throwing knives prepared:

%s
```
- **译文**：
```text
准备了 %d 把飞刀：

%s
```
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3444`（`THROWING_KNIVES` 描述）。术语 `throwing knives` 对应“飞刀”，占位符 `%d` 与 `%s` 顺序、换行符 `\n\n` 完全对齐。

#### entry-02810
- **原文**：`+Touch of Death!`
- **译文**：`+点穴术！`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3538`（`TOUCH_OF_DEATH` 获得状态漂字）。前缀 `+`、感叹号及技能译名完全一致。

#### entry-02811
- **原文**：`#LIGHT_RED#%s explodes into a shower of gore!`
- **译文**：`#LIGHT_RED#%s爆炸成一团碎肉！`
- **复核结论**：未发现问题
- **可核验依据**：对应 `other.lua:3551`（`TOUCH_OF_DEATH` 死亡爆炸日志）。颜色代码 `#LIGHT_RED#`、占位符 `%s` 及感叹号保持一致，译文贴切。

---

### 复核总结
- **全部条目覆盖**：已完整覆盖 `entry-02772` 至 `entry-02811` 全部 40 条。
- **存在疑点条目（需关注）**：
  1. **entry-02790**：日志消息缺少主语“你”（`#STEEL_BLUE#被从避难所带了回去！`），句式残缺，且“带了回去”语向不妥。
  2. **entry-02798**：基础主属性 `magic`（`Stats.STAT_MAG`，术语库规范为“魔力”）被译为“魔法”，存在概念混淆与术语偏离。
  3. **entry-02805**：`reflects teleportation magic!`（反射传送法术）被弱化改写为“可能干扰传送法术！”，与确定性反射机制偏差。
- **细微观察条目**：
  - `entry-02775`：`cold` 译为“寒冰”（术语库标准为“寒冷”，与批内 02801/02805 存在微小不一致）。
  - `entry-02789`：“按比例损失生命”未显式写出“总生命/最大生命”（代码为 `max_life` 比例扣除）。
  - `entry-02791`：`fugue clones` 在此处译为“时空克隆”，同 section 36741 行译为“时空复制体”。
  - `entry-02801`、`entry-02806`、`entry-02807`：中文冒号后多了一个半角空格。
  - `entry-02807`：英文原文漏写 `%`，译文依据底层源码机制补齐为 `+10% 闪电伤害`，处理恰当。