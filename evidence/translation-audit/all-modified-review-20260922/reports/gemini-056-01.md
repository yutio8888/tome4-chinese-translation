### 文件哈希核对

- 检查文件：`evidence/translation-audit/all-modified-review-20260922/batches/batch-056.md`
- 期望 SHA-256：`1bca800ccf9e0c68412efce4f9695f0e6642c548aeb74d5e01bd54d6cf8762f5`
- 实际 SHA-256：`1bca800ccf9e0c68412efce4f9695f0e6642c548aeb74d5e01bd54d6cf8762f5`
- 核验结果：**匹配一致**。

本批次覆盖 `entry-01625` 至 `entry-01665`（无 `entry-01639`），共 40 条冻结译文。所有公开源码依据来自 t-engine4 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

---

### 逐条复核报告（共 40 条）

#### entry-01625
- **位置**：`mod-tome.lua:22512`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **复核结论**：存在疑点
- **可核验依据**：
  1. 漏字语病：第 4 行“你猎犬继承你的伤害加成”中缺少助词“的”，应为“你的猎犬”。
  2. 遗漏机制触发时机：该技能为持续技能（`mode = "sustained"`），原文句首为“Upon activation summon a Temporal Hound.”，表明仅在激活/开启技能瞬间立即召唤一只猎犬，译文省略为“召唤一条时空猎犬。”，易使玩家误解为主动施法技能。
  3. 细微歧义：第 3 行“in %d turns”在猎犬死亡后重置倒计时（源码 `p.rest_count = self.summoner:getTalentCooldown(tid)`）的语境下，译为“在 %d 回合内召唤”易被理解为该时间段内的任意时刻，实际应为“经过 %d 回合后”。
  4. 格式核对：10 个占位符（2 个 `%d`、2 个 `%d%%`、6 个 `%d`）数量与参数匹配，百分号转义正确。

#### entry-01626
- **位置**：`mod-tome.lua:22521`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中检测 `hasLOS` 失败时的玩家日志提示，译文“你没有视线。”符合全库同类 `logPlayer` 标准译法，标点一致。

#### entry-01627
- **位置**：`mod-tome.lua:22522`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中猎犬随机闪现失败时的 `logSeen` 提示，译文“法术失败了！”标准统一，感叹号保留正确。

#### entry-01628
- **位置**：`mod-tome.lua:22540`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 `on_pre_use` 检测 `countHounds(self) < 1` 时的日志提示，术语“时空猎犬”与术语快照完全相符，语义准确。

#### entry-01629
- **位置**：`mod-tome.lua:22541`（`mod-tome/data/talents/chronomancy/temporal-hounds.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码调用 `:tformat(damDesc, radius, stat_damage, duration, affinity)`；译文通过参数重排 `{2, 1, 3, 4, 5}` 将 radius（%d）置于 damage（%0.2f）之前，与中文语序“对半径 %d 的锥形范围内……造成 %0.2f 点时空伤害”精确对应；占位符类型与顺序无误，百分号转义正确。

#### entry-01630
- **位置**：`mod-tome.lua:22552`（`mod-tome/data/talents/chronomancy/threaded-combat.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中传送落点判定失败时的 `logSeen` 提示，译文“法术失败了！”标准统一，感叹号无误。

#### entry-01631
- **位置**：`mod-tome.lua:22593`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中克隆体描述 `m.desc = ([[The real %s... or so %s says.]]):tformat(self:getName(), self:he_she())`，2 个 `%s` 分别接收角色名称及代词，占位符匹配，省略号转为中文六角省略号 `……`，格式正确。

#### entry-01632
- **位置**：`mod-tome.lua:22595`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题（细微观察）
- **可核验依据**：固定 commit 源码中克隆生成空间不足时的日志提示；译文保留原文感叹号；术语快照中 `logSeen` 记录虽为句号（`没有足够的空间召唤。`），此处为 `logPlayer` 且原文以 `!` 结尾，保留感叹号忠实于源码文本。

#### entry-01633
- **位置**：`mod-tome.lua:22596`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题（细微观察）
- **可核验依据**：占位符 `%d` 对应 duration；机制上克隆与玩家互不造成伤害（源码中双方伤害乘数降为 0）意译为“你和镜像不会互相伤害”，伤害减 2/3、三者均分、不正常冷却等机制核对源码完全相符；名词上对 Fugue Clone 此处采用“镜像”而非“时间复制体”，属上下文通俗意译，不产生机制误导。

#### entry-01634
- **位置**：`mod-tome.lua:22603`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 `:tformat(duration, braid)` 分别对应 `%d` 与 `%d%%`，转义正确；Rethread 技能名对应同 section 的“重组”；机制与加成描述准确。

#### entry-01635
- **位置**：`mod-tome.lua:22608`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 `on_pre_use` 检测 `checkTimeline(self)` 时的阻断提示，无占位符，语义与语气准确。

#### entry-01636
- **位置**：`mod-tome.lua:22612`（`mod-tome/data/talents/chronomancy/timeline-threading.lua`）
- **复核结论**：未发现问题
- **可核验依据**：源码 `:tformat(duration, power)` 分别对应 `%d` 和 `%d%%`，百分号正确转义；机制核对 `Cease to Exist` 分裂时间线及击杀后返回时间点并斩杀目标的逻辑，译文描述精准。

#### entry-01637
- **位置**：`mod-tome.lua:22631`（`mod-tome/data/talents/chronomancy/timetravel.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中检测 `timetravel_immune` 属性时的提示，占位符 `%s` 匹配，标点一致。

#### entry-01638
- **位置**：`mod-tome.lua:22633`（`mod-tome/data/talents/chronomancy/timetravel.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中地图地形阻挡或临时实体导致的时间旅行失败提示，语义忠实。

#### entry-01640
- **位置**：`mod-tome.lua:22642`（`mod-tome/data/talents/chronomancy/timetravel.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 Temporal Reprieve 被阻断时的提示，英文省略号正确转换为中文省略号 `……`。

#### entry-01641
- **位置**：`mod-tome.lua:22645`（`mod-tome/data/talents/chronomancy/timetravel.lua`）
- **复核结论**：未发现问题（细微观察）
- **可核验依据**：时空避难所掉落 lore 的弹窗文本，术语“时空法师（paradox mage）”、“时空避难所（Temporal Reprieve）”、“转化之盒（transmutation chest）”、“虚空（void）”全部准确；末尾“a crumpled note”译为“一张皱巴巴的笔记”（偏指笔记内容，也可指便签/纸条），语意连贯无误。

#### entry-01642
- **位置**：`mod-tome.lua:22646`（`mod-tome/data/talents/chronomancy/timetravel.lua`）
- **复核结论**：未发现问题
- **可核验依据**：源码 `:tformat(duration)`，占位符 `%d` 正确对应停留回合数，语义简明流畅。

#### entry-01643
- **位置**：`mod-tome.lua:22659`（`mod-tome/data/talents/corruptions/blight.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中腐化技能，术语快照中 corruption 为“堕落”，技能译为“堕落驱散”沿用既有标准。

#### entry-01644
- **位置**：`mod-tome.lua:22672`（`mod-tome/data/talents/corruptions/blight.lua`）
- **复核结论**：未发现问题（细微观察）
- **可核验依据**：源码 `:tformat(radius, duration, dam/4, dam, heal_factor, power, fail)`，7 个占位符（%d, %d, %0.2f, %0.2f, %d%%, %d%%, %d%%）顺序及转义完全吻合；观察点为此处将 Insidious / Numbing / Crippling Blight 译为“阴险毒素/麻痹毒素/致残毒素效果”，而 timed_effects 中对应状态名为“阴险枯萎毒素/麻痹枯萎毒素/致残枯萎毒素”，略去“枯萎”二字，但不影响机制理解。

#### entry-01645
- **位置**：`mod-tome.lua:22718`（`mod-tome/data/talents/corruptions/bone.lua`）
- **复核结论**：未发现问题
- **可核验依据**：源码 `:tformat(damDesc, bonus*100, bonus*100*5, damDesc*2)`，占位符 `%0.2f`、`%d%%`、`%d%%`、`%d` 数量与顺序完全对应，括号使用全角括号 `（%d）`，格式规范。

#### entry-01646
- **位置**：`mod-tome.lua:22748`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/sanguisuge 技能树描述，无占位符，翻译准确自然。

#### entry-01647
- **位置**：`mod-tome.lua:22750`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/torment 技能树描述，语义贴切通顺。

#### entry-01648
- **位置**：`mod-tome.lua:22754`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/bone 技能树描述，准确传达。

#### entry-01649
- **位置**：`mod-tome.lua:22756`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/hexes 技能树描述，准确传达。

#### entry-01650
- **位置**：`mod-tome.lua:22758`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/curses 技能树描述，语义准确。

#### entry-01651
- **位置**：`mod-tome.lua:22762`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/plague 技能树描述，术语“疾病（disease）”相符。

#### entry-01652
- **位置**：`mod-tome.lua:22764`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/scourge 技能树描述，文意贴切。

#### entry-01653
- **位置**：`mod-tome.lua:22766`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/reaving-combat 技能树描述，准确通顺。

#### entry-01654
- **位置**：`mod-tome.lua:22768`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/blood 技能树描述，文意完整。

#### entry-01655
- **位置**：`mod-tome.lua:22770`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/blight 技能树描述，意思准确。

#### entry-01656
- **位置**：`mod-tome.lua:22772`（`mod-tome/data/talents/corruptions/corruptions.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 corruption/shadowflame 技能树描述，术语“恶魔（demonic）”准确。

#### entry-01657
- **位置**：`mod-tome.lua:22823`（`mod-tome/data/talents/corruptions/plague.lua`）
- **复核结论**：未发现问题（细微观察）
- **可核验依据**：源码 `:tformat(damDesc, stat_damage)`，2 个占位符 `%0.2f`、`%d` 正确对应伤害与属性削减值；技能机制（优先未感染且属性高者、优先附近疾病数多者）核对源码算法完全吻合；观察点为“降低其一项物理能力值……%d”后未带量词“点”，略欠流畅，但不影响理解。

#### entry-01658
- **位置**：`mod-tome.lua:22837`（`mod-tome/data/talents/corruptions/plague.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 Catalepsy 爆发疾病伤害时的战斗日志，颜色标签 `#DARK_GREEN#` 与 `#LAST#` 闭合完整，占位符 `%s` 结合中文语序调整至颜色标签前，符合语法与显示规则。

#### entry-01659
- **位置**：`mod-tome.lua:22839`（`mod-tome/data/talents/corruptions/plague.lua`）
- **复核结论**：存在疑点
- **可核验依据**：
  1. 距离单位误用与概念遗漏：原文为“within a radius %d ball”，译文译为“所有 %d 码球形范围内”。在 ToME 机制及全库翻译规范中，法术范围单位均为“半径 %d（格）”，游戏内不存在“码（yards）”作为机制度量单位；且译文漏掉了“半径”概念，既引入了非游戏机制单位，又使范围表述不规范（建议修正为“半径 %d 格球形范围内”或“半径 %d 的球形范围内”）。
  2. 占位符核对：`radius`（%d）、`duration`（%d）、`damage * 100`（%d%%）数量与顺序无误，百分号转义正确。

#### entry-01660
- **位置**：`mod-tome.lua:22862`（`mod-tome/data/talents/corruptions/reaving-combat.lua`）
- **复核结论**：未发现问题
- **可核验依据**：源码 `:tformat(SPbonus, SPbonus*10)`，分别对应 `%0.1f` 与 `%d`，机制核对叠加上限 10 层、持续 3 回合，数值与效果描述准确。

#### entry-01661
- **位置**：`mod-tome.lua:22895`（`mod-tome/data/talents/corruptions/rot.lua`）
- **复核结论**：存在疑点（术语不一致）
- **可核验依据**：
  1. 术语偏离：条目中“a carrion worm mass”译为了“腐尸蠕虫”，而本批术语快照中明确规定 `carrion worm mass` 的实体名为 `腐肉虫群`，并特别标注“统一实体名、生成日志及腐肉虫疾病描述”，此处译名偏离了术语库统一规范。
  2. 占位符与转义：原文调用 `:tformat(resist, affinity, reduction, damDesc, dam)`，其中第 5 个参数 dam 在英文源文本中未被消费；中文译文准确对应了前 4 个占位符（%d%%, %d%%, %d%%, %0.2f），字面量 `15%%` 与 `33%%` 转义正确无误。

#### entry-01662
- **位置**：`mod-tome.lua:22904`（`mod-tome/data/talents/corruptions/rot.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 Worm Walk 传送失败时的提示，译文符合技能命名，感叹号无误。

#### entry-01663
- **位置**：`mod-tome.lua:22940`（`mod-tome/data/talents/corruptions/sanguisuge.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 `:tformat(t.VimOnDeath(self, t))` 对应 `%0.1f`；术语“活力（vim）”、“不死族（non-undead）”、“意志（Willpower）”均与术语规范完全相符，数值 0.5 一致。

#### entry-01664
- **位置**：`mod-tome.lua:22955`（`mod-tome/data/talents/corruptions/scourge.lua`）
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码中 `:tformat(100 * t.getDamage(self, t), t.getIncrease(self, t))` 对应 `%d%%` 与 `%d`；机制核对源码中寻找最低剩余时间的 disease 并增加回合数，描述精准。

#### entry-01665
- **位置**：`mod-tome.lua:22962`（`mod-tome/data/talents/corruptions/scourge.lua`）
- **复核结论**：未发现问题
- **可核验依据**：源码调用 `:tformat(100 * t.getDamage(self, t), damDesc, self:getTalentRadius(t))`；译文在 `mod-tome.lua` 中通过 `{1, 3, 2}` 显式重排参数，将 radius（%d）置于 splash damage（%0.2f）之前，与中文“半径 %d 格范围……造成 %0.2f 酸性伤害”完全吻合，占位符类型与转义无误。

---

### 复核总结汇总

- **覆盖总数**：40 条（`entry-01625` 至 `entry-01665`，无遗漏）。
- **未发现问题**：37 条（其中包含 4 处细微观察，均不构成机制或显示阻断）。
- **存在疑点**：3 条，分别为：
  - `entry-01625`：漏字（“你猎犬”缺少“的”）、漏译技能激活时机（“Upon activation”）；
  - `entry-01659`：机制单位误用与概念缺失（“radius %d”误译为“%d 码”，且缺少“半径”）；
  - `entry-01661`：术语不一致（“carrion worm mass”未统一为术语库规定的“腐肉虫群”，译成了“腐尸蠕虫”）。