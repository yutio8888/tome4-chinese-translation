本批次 batch-063 译文复核报告已完成。

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-063.md`
- **文件 SHA-256 校验**：`88e4aaf03fbcbcaf15f0e94ec5a5ce00cbb0f2b12880f14b1999d3f2a22054e9`（核验一致）
- **源码比对基准**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（引擎公开源码 `t-engine4`）
- **复核条目**：entry-01906 至 entry-01947，共 40 条全部覆盖。

---

### 逐条复核报告

#### entry-01906
- **位置**：`mod-tome.lua:25173`
- **源码位置**：`game/modules/tome/data/talents/gifts/mindstar-mastery.lua`（技能：自然平衡 Nature's Equilibrium）
- **结论**：未发现问题
- **核验依据**：占位符格式与源码参数严格对应（`%d%%` 武器伤害、`%d` 最大治疗量、`10%%` 失衡值比例、`%2.f` 灵晶强度倍率）；主副手心灵利刃传导伤害治疗、失衡值降低机制表述与源码逻辑一致。

#### entry-01907
- **位置**：`mod-tome.lua:25183`
- **源码位置**：`game/modules/tome/data/talents/gifts/moss.lua`（技能：紧抓苔藓 Grasping Moss）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（伤害）、`%d%%`（减速）、`%d%%`（定身概率）、`%d`（持续回合）五个参数顺序及格式无误；苔藓瞬发但同系进入 3 回合冷却机制与源码 `activate_moss` 逻辑一致。首句未直译 "Instantly"，但在第 5 行完整说明了技能瞬发机制。

#### entry-01908
- **位置**：`mod-tome.lua:25195`
- **源码位置**：`game/modules/tome/data/talents/gifts/moss.lua`（技能：滋养苔藓 Nourishing Moss）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（伤害）、`%d%%`（治疗百分比）、`%d`（持续回合）完整对应；吸血治疗自身、自然伤害受精神强度加成与源码逻辑一致。

#### entry-01909
- **位置**：`mod-tome.lua:25207`
- **源码位置**：`game/modules/tome/data/talents/gifts/moss.lua`（技能：滑溜苔藓 Slippery Moss）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（伤害）、`%d%%`（行动失败率）、`%d`（持续回合）完全匹配；复杂行动失败率及精神强度加成机制与源码逻辑一致。

#### entry-01910
- **位置**：`mod-tome.lua:25219`
- **源码位置**：`game/modules/tome/data/talents/gifts/moss.lua`（技能：致幻苔藓 Hallucinogenic Moss）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（伤害）、`%d%%`（混乱概率）、`%d%%`（混乱强度）、`%d`（持续回合）五个参数顺序及类型均匹配；混乱 2 回合与精神强度加成描述符合源码。

#### entry-01911
- **位置**：`mod-tome.lua:25260`
- **源码位置**：`game/modules/tome/data/talents/gifts/mucus.lua`（技能：活体粘液 Living Mucus）
- **结论**：细微观察
- **核验依据**：占位符 `%d%%`（生成几率）、`%d`（存在时间）、`%d`（上限数量）三个参数完全匹配，基于灵巧与暴击延长机制准确；排版存在细微差异：原文第 1 句与第 2 句之间原本有换行及缩进（`Your mucus is brought to near sentience.\n\t\tEach turn...`），译文中合并至同一行（`你的粘液有了自己的感知。每回合有 %d%% 几率...`），行数由 6 行减少为 5 行。

#### entry-01912
- **位置**：`mod-tome.lua:25272`
- **源码位置**：`game/modules/tome/data/talents/gifts/mucus.lua`（技能：粘液漫步 Oozewalk）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（净化负面效果数量）、`%d%%`（施法消耗正常能量比例）正确；净化物理/魔法负面效果、需自身站在粘液上且移动至粘液区域的机制与源码一致。

#### entry-01913
- **位置**：`mod-tome.lua:25288`
- **源码位置**：`game/modules/tome/data/talents/gifts/ooze.lua`（技能：有丝分裂 Mitosis）
- **结论**：存在疑点
- **核验依据**：
  1. **漏译限定说明**：原文第 5 行有关键限制说明 `(limited by talent level and the summoning limit)`（受技能等级和召唤上限限制），译文在对应句子（“你同时最多只能拥有 %d 只浮肿软泥怪，...”）中漏译了该括号限定内容；
  2. **触发机制表述偏差**：原文第 2 行是 `When you take damage`，译文译为“当你受到攻击时”。源码中触发该效果使用的是 `on_take_hit` 钩子，必须承受大于 0 的伤害才能判定分裂，未命中或 0 伤害的受击不触发，“受到伤害”比“受到攻击”更准确；
  3. **末句过度简省**：原文 `%sThe chance to split increases with your Cunning.` 译为 `%s几率受灵巧加成。`，省略了“分裂”。

#### entry-01914
- **位置**：`mod-tome.lua:25300`
- **源码位置**：`game/modules/tome/data/talents/gifts/ooze.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Reabsorb` 译为“再吸收”，术语与上下文一致。

#### entry-01915
- **位置**：`mod-tome.lua:25301`
- **源码位置**：`game/modules/tome/data/talents/gifts/ooze.lua`（技能：再吸收 Reabsorb）
- **结论**：未发现问题
- **核验依据**：原文调用 `tformat(t.getDuration, damDesc(..., t.getDam), 3, t.equiRegen)`。译文调换了第 2 句中半径与伤害的叙述顺序，并在 `mod-tome.lua` 明确注册了参数映射 `{1, 3, 2, 4}`；经核对引擎 `I18N.lua` 中的 `default_tformat` 实现，重排后第 1 个 `%d` 取 duration、第 2 个 `%d` 取半径 3、第 3 个 `%0.1f` 取伤害数值、第 4 个 `%0.1f` 取每回合失衡值恢复量，类型与数值完全对应。

#### entry-01916
- **位置**：`mod-tome.lua:25316`
- **源码位置**：`game/modules/tome/data/talents/gifts/ooze.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Indiscernible Anatomy` 译为“难以辨认的解剖结构”，规范准确。

#### entry-01918
- **位置**：`mod-tome.lua:25327`
- **源码位置**：`game/modules/tome/data/talents/gifts/oozing-blades.lua`（技能：软泥射线 Oozebeam）
- **结论**：未发现问题
- **核验依据**：占位符 `%0.1f` 对应史莱姆伤害，精神强度加成机制表述符合源码。

#### entry-01919
- **位置**：`mod-tome.lua:25331`
- **源码位置**：`game/modules/tome/data/talents/gifts/oozing-blades.lua`（技能：天然酸液 Natural Acid）
- **结论**：存在疑点
- **核验依据**：原文第 3 行 `This damage bonus will improve up to 4 times (no more than once each turn) with later Acid damage you do, up to a maximum of %0.1f%%.`，译文译为“伤害加成能够积累到最多4倍（1回合至多触发1次），最大值 %0.1f%%。”。源码中 `level` 参数从 1 随后续酸伤最多提升 4 次至 5 层（`math.min(5, level)^0.5`），times 在此处表示叠加次数（最多叠加 4 次），而非数值乘以 4（倍数应为 4-fold 或 4 times as much）。译为“最多4倍”属于将“次”误译为“倍”，会使玩家误以为伤害加成百分比被翻了 4 倍。

#### entry-01920
- **位置**：`mod-tome.lua:25339`
- **源码位置**：`game/modules/tome/data/talents/gifts/oozing-blades.lua`（技能：心灵寄生 Mind Parasite）
- **结论**：未发现问题
- **核验依据**：占位符 `%d%%`（概率）、`%d`（技能数量）、`%d`（冷却回合）三个参数与源码 `tformat(t.getChance, t.getNb, t.getTurns)` 对应无误；入脑干扰技能冷却机制表述准确。

#### entry-01921
- **位置**：`mod-tome.lua:25402`
- **源码位置**：`game/modules/tome/data/talents/gifts/sand-drake.lua`（技能：流沙吐息 Sand Breath）
- **结论**：未发现问题
- **核验依据**：实体占位符 `@Source@` 完整保留，战斗信息句式准确。

#### entry-01922
- **位置**：`mod-tome.lua:25403`
- **源码位置**：`game/modules/tome/data/talents/gifts/sand-drake.lua`（技能：流沙吐息 Sand Breath）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（物理伤害）、`%d`（致盲回合）以及字面量 `0.5%%`（物理抗性提升）均匹配；力量、精神暴击率、精神强度加成与源码逻辑一致。

#### entry-01923
- **位置**：`mod-tome.lua:25465`
- **源码位置**：`game/modules/tome/data/talents/gifts/storm-drake.lua`（龙卷风击退日志）
- **结论**：未发现问题
- **核验依据**：占位符 `%s` 正常保留，击退战斗日志简明准确。

#### entry-01924
- **位置**：`mod-tome.lua:25467`
- **源码位置**：`game/modules/tome/data/talents/gifts/storm-drake.lua`（技能：龙卷风 Tornado）
- **结论**：细微观察
- **核验依据**：占位符 `%0.2f`（移动闪电伤害）、`%d`（爆炸半径）、`%0.2f`（爆炸闪电伤害）、`%0.2f`（爆炸物理伤害）、字面量 `1%%` 闪电抗性均正确；但存在两处排版与标点瑕疵：
  1. 译文第 4 行“`伤害受精神强度加成`”末尾遗漏了句号；
  2. 原文第 4 行的独立句子 `The tornado will move a maximum of 20 times.` 在译文中被合并到首句末尾（“...最多移动20次。”），行数由 6 行减少为 5 行。

#### entry-01925
- **位置**：`mod-tome.lua:25480`
- **源码位置**：`game/modules/tome/data/talents/gifts/storm-drake.lua`（技能：闪电吐息 Lightning Breath）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（半径）、`%0.2f`（最小伤害）、`%0.2f`（最大伤害）、`%0.2f`（平均伤害）及字面量 `1%%` 全部匹配；震慑 3 回合及力量、精神强度影响逻辑与源码一致。

#### entry-01926
- **位置**：`mod-tome.lua:25492`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-advanced.lua`（技能：雄壮登场 Grand Arrival）
- **结论**：未发现问题
- **核验依据**：共 10 个格式化占位符（喷火里奇降抗 `%d%%`、三头蛇毒雾 `%0.1f`、雾凇降抗 `%d%%`、火龙幼崽数 `%d`、猎犬降抗 `%d%%`、果冻怪降抗 `%d%%`、米诺陶减速 `%0.1f%%`、乌龟治疗 `%d`、范围 `%d`、持续 `%d`），类型与传参顺序完全一致；眩晕（Dazes）、定身（Pins）等状态术语与机制对齐。（注：列表末项蜘蛛句尾多出一处句号，属轻微标点不齐，不影响理解）。

#### entry-01928
- **位置**：`mod-tome.lua:25560`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-augmentation.lua`（技能：引爆召唤物 Detonate）
- **结论**：未发现问题
- **核验依据**：共 14 个占位符（半径、各召唤兽引爆伤害/亲和/护甲/减速等效果），数值占位符数量、类型、顺序与源码完全吻合；亲和（affinity）、护甲硬度（armour hardiness）等机制词义表达清晰。

#### entry-01929
- **位置**：`mod-tome.lua:25588`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-augmentation.lua`（技能：坚韧 Resilience）
- **结论**：未发现问题
- **核验依据**：占位符 `%0.1f%%`（最大生命加成）、`%d`（延长存活回合）匹配；召唤兽存活与生命增益机制表述准确。

#### entry-01930
- **位置**：`mod-tome.lua:25635`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（技能：凛冬之怒 Winter's Fury）
- **结论**：未发现问题
- **核验依据**：占位符 `%0.2f`（寒冷伤害）、`%d`（持续回合）、字面量 `25%%`（冰冻几率）匹配；意志加成描述符合源码。

#### entry-01931
- **位置**：`mod-tome.lua:25646`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Ritch Flamespitter` 译为“召唤：喷火里奇”，符合召唤系技能命名惯例。

#### entry-01932
- **位置**：`mod-tome.lua:25647`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：实体占位符 `@Source@` 保留完整，召唤战斗信息准确。

#### entry-01933
- **位置**：`mod-tome.lua:25649`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：原文 `Not enough space to summon!` 译为“没有足够的空间召唤！”，感叹号标点与原文一致。

#### entry-01934
- **位置**：`mod-tome.lua:25650`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：占位符 `%s` 保留，全角括号规范，修饰名“野性召唤”准确。

#### entry-01935
- **位置**：`mod-tome.lua:25651`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（技能：喷火里奇 info）
- **结论**：未发现问题
- **核验依据**：4 个 `%d` 占位符分别对应召唤时间、意志、灵巧、体质，传参顺序完全一致；属性继承说明与精神强度加成机制符合源码。

#### entry-01936
- **位置**：`mod-tome.lua:25658`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Hydra` 译为“召唤：三头蛇”，符合术语习惯。

#### entry-01937
- **位置**：`mod-tome.lua:25659`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：占位符 `@Source@` 保留完整，召唤战斗信息准确。

#### entry-01938
- **位置**：`mod-tome.lua:25660`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（三头蛇生物描述）
- **结论**：未发现问题
- **核验依据**：原文 `A strange reptilian creature with three smouldering heads.` 译为“长着三颗灼热冒烟的头颅的奇怪爬行动物。”，文意契合生动。

#### entry-01939
- **位置**：`mod-tome.lua:25661`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（技能：三头蛇 info）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（持续回合）、`%d`（意志）、`%d`（体质）、字面量 `18`（力量）完全一致；毒素/酸液/闪电吐息及属性继承描述符合源码。（首句在句号处进行了拆行排版，内容无缺漏）。

#### entry-01940
- **位置**：`mod-tome.lua:25669`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Rimebark` 译为“召唤：雾凇”，符合术语规范。

#### entry-01941
- **位置**：`mod-tome.lua:25670`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：占位符 `@Source@` 保留完整，召唤信息准确。

#### entry-01942
- **位置**：`mod-tome.lua:25672`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（技能：雾凇 info）
- **结论**：未发现问题
- **核验依据**：4 个 `%d` 占位符分别对应召唤时间、意志、灵巧、体质，数值及类型无误；不可移动与常驻 3 码冰风暴机制表述与源码一致。

#### entry-01943
- **位置**：`mod-tome.lua:25680`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `Fire Drake` 译为“召唤：火龙”，符合命名惯例。

#### entry-01944
- **位置**：`mod-tome.lua:25681`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`
- **结论**：未发现问题
- **核验依据**：占位符 `@Source@` 保留完整，召唤信息准确。

#### entry-01945
- **位置**：`mod-tome.lua:25683`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-distance.lua`（技能：火龙 info）
- **结论**：细微观察
- **核验依据**：占位符 `%d`（召唤时间）、`%d`（力量）、`%d`（体质）、字面量 `38`（意志）及属性继承机制均正确；细微文意观察：原文首句 `burn and crush your foes to death`（烧死并碾碎敌人）在译文中被简略概括为“摧毁敌人”，漏译了火焰烧灼与近战碾碎击杀的具体动作表述。

#### entry-01946
- **位置**：`mod-tome.lua:25701`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-melee.lua`（技能：果冻铺展 Jelly Spread 触发信息）
- **结论**：未发现问题
- **核验依据**：占位符 `@source@`（源码即为小写）保持小写，双感叹号 `！！` 匹配原文 `!!`。

#### entry-01947
- **位置**：`mod-tome.lua:25705`
- **源码位置**：`game/modules/tome/data/talents/gifts/summon-melee.lua`
- **结论**：未发现问题
- **核验依据**：技能名 `War Hound` 译为“召唤：战争猎犬”，术语准确规范。

---

### 复核总结与疑点清单

| 条目编号 | 判定 | 核心核验依据 |
| :--- | :--- | :--- |
| **entry-01911** | 细微观察 | 原文第 1 句与第 2 句之间的换行被合并至同一行，缺失一处换行。占位符与数值机制无误。 |
| **entry-01913** | **存在疑点** | 1. 漏译第 5 行限制条件 `(limited by talent level and the summoning limit)`；<br>2. `When you take damage`（受到伤害）译为“受到攻击”，与源码 `on_take_hit` 受击且承受伤害的触发条件不完全严谨；<br>3. 末句简省，漏译“分裂”。 |
| **entry-01919** | **存在疑点** | 机制误译：`improve up to 4 times` 误译为“积累到最多4倍”，实际为后续酸伤最多叠加/提升 4 次（共 5 层），非数值放大 4 倍。 |
| **entry-01924** | 细微观察 | 1. 第 4 行末尾缺失句号；<br>2. 原文第 4 行移动次数上限被合并至第 1 行末尾。占位符与数值机制无误。 |
| **entry-01945** | 细微观察 | 首句 `burn and crush your foes to death` 简略概括为“摧毁敌人”，漏译烧死与碾碎的具体动作描述。占位符与数值机制无误。 |
| 其余 35 条 | 未发现问题 | 占位符格式、参数映射表、文本语义、技能机制与固定源码完全契合。 |