### batch-072 译文复核报告

#### 哈希与基础核验
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-072.md`
- **文件 SHA-256**：`dc4f01bdc712b591e75ad5d7a594b15b69182ecf1bd82d2b46115817402ad16d`（已核验一致）
- **条目范围**：`entry-02268` 至 `entry-02307`，共 40 条
- **源码依据**：公开核心源码（tome）固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；参考译文基线 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核详情

#### entry-02268
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/stone-alchemy.lua:40`。无占位符，数值 40 ～ 80 与原文一致，术语“炼金宝石”（alchemist gems）、“自然宝石”（natural gemstone）翻译准确，换行与缩进结构（`\n\t\t`）与源码一致。

#### entry-02269
- **判定**：细微观察
- **可核验依据**：`mod-tome/data/talents/spells/stone-alchemy.lua:99`。源码调用为 `game.logPlayer(self, "You imbue your %s with %s.", name, gem:getName{...})`，占位符 `%s` 顺序（第一项为装备名，第二项为宝石名）正确。但译文将 `imbue` 译作“安装”（“你在 %s 上安装了 %s”），相比同技能面板及同类条目通行的“附魔”或“镶嵌”（如 entry-02270 译为“附魔”，`mod-tome.lua:29660` 译为“镶嵌”），用词略显机翻生硬。

#### entry-02270
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/stone-alchemy.lua:105`。源码传参 `tformat(..., self:getTalentLevelRaw(t))`，占位符 `%s` 与 `%d` 顺序及类型完全匹配，永久附魔机制与换行缩进结构完整。

#### entry-02271
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/stone-alchemy.lua:144`。源码传参为 `tformat(range)`，占位符 `%d` 准确对应距离；宝石消耗数量（5 枚）与不可通行地形标记穿越机制描述准确。

#### entry-02272
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/stone.lua:48`。源码传参为 `tformat(count, damDesc(...), damDesc(...))`，占位符 `%d`、`%0.2f`、`%0.2f` 顺序与格式完全一致，5 回合流血与 5 级额外飞弹机制说明准确，换行与缩进匹配。

#### entry-02273
- **判定**：存在疑点
- **可核验依据**：`mod-tome/data/talents/spells/stone.lua:113`。
  1. **换行结构不一致**：源码英文原句第一段包含两句（“You root yourself... effect.”），译文在“融为石头。”后添加了 `\n\t\t`，将其拆成了两段，导致译文比原文多出一处换行与缩进。
  2. **文本翻译瑕疵**：“affinity with the earth”被译为“土壤相关影响”，偏离了“与大地的亲和/共鸣”本意；“any forced movement will end the effect”被译为“任何移动会打断此技能效果”，而技能激活期间本身已无法移动（`never_move`），此处英文特指击退、传送等“强制位移”；“冷却时间回合数：%d%%”中用百分比修饰“回合数”亦存在语病。
  注：5 个 `%d%%` 占位符顺序与抗性类型顺序正确。

#### entry-02274
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/stone.lua:159`。源码传参 `tformat(damDesc(...), radius, duration)`，占位符 `%0.2f`、`%d`、`%d` 顺序与类型完全一致，震慑机制与范围描述准确，换行缩进匹配。

#### entry-02275
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/storm.lua:59`。源码传参 `tformat(radius, damDesc(...), damDesc(...), damDesc(...))`，占位符 `%d`、`%0.2f`、`%0.2f`、`%0.2f` 及转义百分号 `75%%` 格式与顺序均正确，daze 正确对应“眩晕”，换行缩进一致。

#### entry-02276
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/storm.lua:94`。技能名 Hurricane 译为“飓风”，与术语表及全游戏统一译名一致。

#### entry-02277
- **判定**：存在疑点
- **可核验依据**：`mod-tome/data/talents/spells/temporal.lua:67`。
  1. **段落合并**：原文共有 4 个段落，第 2 段为吸收上限与持续时间结束后的力场返还机制，第 3 段为每回合 10% 治疗与 Aegis Shielding 加成；译文将第 2 段与第 3 段合并在同一行中，缺少了一处换行与缩进（`\n\t\t`）。
  2. **风味与机制概念省略**：原文首句“sending it forward in time”与次句“temporal restoration field”的时空技能风味被大幅简化为“吸收你受到的伤害”和“存储的能量会治疗你”，时空回复力场概念被省略；技能名引用“time shield”被译为“时间屏障”（术语库 preferred 统一译名为“时间盾”）。
  注：占位符 `%d`、`%d` 及 `10%%` 顺序与数值均正确。

#### entry-02278
- **判定**：细微观察
- **可核验依据**：`mod-tome/data/talents/spells/temporal.lua:98`。源码英文首段包含“Removes the target... In this state...”两句，译文将其拆分为两段（在中间增加了换行与缩进 `\n\t\t`），使得整体段落数由 3 段变为 4 段。占位符 `%d` 正确，无敌与时间静止机制表述准确。

#### entry-02279
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/thaumaturgy.lua:118`。颜色控制符 `#LIGHT_BLUE#` 与 `#LAST#` 完整闭合，占位符 `%s` 保留，状态描述准确。

#### entry-02280
- **判定**：细微观察
- **可核验依据**：`mod-tome/data/talents/spells/thaumaturgy.lua:216`。源码末句仅写“if you have enough mana”，译文根据 `callbackOnActBase` 中法力不足时强制关闭技能且补满时扣除法力的实际机制，补充了“消耗法力”及“否则解除持续”的机制性阐释说明；首句省译了“residual energies”（残余能量）。占位符 `%d` 与段落格式匹配。

#### entry-02281
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/thaumaturgy.lua:284`。占位符 `%0.2f` 及百分比转义 `+30%%`、`25%%` 完全正确；8 行段落结构与缩进一致；奇术伤害（Thaumic damage）、无尽之焰（Burning Wake）、飓风（Hurricane）、西弗格罗斯形态（Shivgoroth Form）、水晶力场（Crystalline Focus）、绝对零度（Uttercold）等跨技能联动机制与术语均准确无误。

#### entry-02282
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/water.lua:107`。日志文本颜色标签 `#LIGHT_BLUE#` 与 `#LAST#` 完整，词义准确。

#### entry-02283
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/water.lua:177`。源码传参 `tformat(dur, self:getTalentLevelRaw(t), power * 100, power * 100 / 2, 50 + power * 100, tostring(icestorm or ""))`，占位符 `%d`、`%d`、`%d%%`、`%d%%`、`%d%%`、`%s` 顺序与类型完全对应；颜色控制符 `#AQUAMARINE#` 与 `#LAST#` 闭合完整；空行与缩进结构一致。

#### entry-02284
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/wildfire.lua:57`。技能名 Burning Wake 译为“无尽之焰”，与术语库一致。

#### entry-02285
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/spells/wildfire.lua:74`。占位符 `%0.2f` 正确；技能引用 Flame、Flameshock、Fireflash、Blastwave 分别对应游戏内实际技能名“火焰”、“火焰冲击”、“爆裂火球”、“火焰新星”；4 回合每回合造成伤害的地面机制表述准确。

#### entry-02286
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2h-assault.lua:51`。占位符 `%s` 保留，日志与抵抗机制描述准确。

#### entry-02287
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2h-assault.lua:116`。双手武器装备前置限制提示翻译准确，技能名“死亡之舞”符合规范。

#### entry-02288
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:36`。双手武器前置限制提示翻译准确，技能名匹配。

#### entry-02289
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:66`。双手武器前置限制提示翻译准确，对应狂战技能激活。

#### entry-02290
- **判定**：细微观察
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:103`。
  1. **换行结构不一致**：原文末句“The Accuracy bonus... and the Physical Power bonus with your Strength.”为单一自然段，译文将其拆分为两行（“命中受敏捷值加成；\n\t\t物理强度受力量值加成。”），多出了一处换行与缩进。
  2. 占位符 `%d`、`%d`、`%d%%` 顺序及数值对应正确，闪避与护甲（Defense / Armour）减益及震慑定身抵抗机制翻译无误。

#### entry-02291
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:117`。啮齿类生物专有战斗动作文本，保留 `@Source@` 宏标签，趣味化译名符合语境。

#### entry-02292
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:117`。保留 `@Source@` 宏标签，战吼动作描述准确。

#### entry-02293
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:130`。双手武器前置限制提示翻译准确，战争怒吼术语匹配。

#### entry-02294
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:166`。双手武器前置限制提示翻译准确，致命打击技能名匹配。

#### entry-02295
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:216`。双手武器前置限制提示翻译准确，震慑打击技能名匹配。

#### entry-02296
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:229`。占位符 `%s` 保留，日志文本准确。

#### entry-02297
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:259`。双手武器前置限制提示翻译准确，破甲技能名匹配。

#### entry-02298
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:285`。源码调用为 `game.logSeen(self, "#CRIMSON#%s shatters %s shield!", self:getName():capitalize(), target:getName())`，颜色控制符 `#CRIMSON#` 保留，两个 `%s` 占位符顺序一致（攻击者粉碎了目标的护盾）。

#### entry-02299
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:319`。双手武器前置限制提示翻译准确，破刃技能名匹配。

#### entry-02300
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/2hweapon.lua:361`。双手武器前置限制提示翻译准确，血之狂暴技能名匹配。

#### entry-02301
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/acrobatics.lua:99`。无法移动时的前置判定提示，翻译简洁准确。

#### entry-02302
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/acrobatics.lua:60`。源码宏标签 `#Source#`、`#target#` 及颜色标签 `#YELLOW#`、`#LAST#` 均完整保留，撑杆跳动作与日志语境匹配。

#### entry-02303
- **判定**：存在疑点
- **可核验依据**：`mod-tome/data/talents/techniques/acrobatics.lua:208`。
  1. **技能名/术语不一致**：原文技能引用包含“Vault, Tumble, and Trained Reactions”，其中 Tumble 在同技能树定义（`mod-tome.lua:29993`）及术语库中均统一译为“翻筋斗”，但本条译文译作“翻滚”，与本系技能名及术语库不一致。
  2. **换行结构不一致**：原文第 2 段将等级 3 与等级 5 的加成写在同一段，译文将其拆分为两段（“在等级 3 时...”与“在等级 5 时...”），多出了一处换行与缩进。
  注：占位符 `%d`、`%0.1f`、`10%%`、`20%%` 数值与类型无误。

#### entry-02304
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/agility.lua:83`。占位符 `%s` 保留，daze 准确译为“眩晕”。

#### entry-02305
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/agility.lua:170`。源码传参 `tformat(t.getDamage(self,t)*100, t.getDist(self, t))`，占位符 `%d%%` 与 `%d`（击退距离格数）顺序与类型完全对应，移动减冷却机制与投石索需求表述准确。

#### entry-02306
- **判定**：细微观察
- **可核验依据**：`mod-tome/data/talents/techniques/agility.lua:217`。源码中该技能名为 Rapid Shot，但英文报错文本硬编码为“You cannot use Rapid Fire without a bow or sling!”。译文采取意译将技能名泛化为“施放这个技能”，避开了英文原版的名称混淆，且准确传达了武器限制。

#### entry-02307
- **判定**：未发现问题
- **可核验依据**：`mod-tome/data/talents/techniques/agility.lua:237`。源码传参 `tformat(atk, move, turn)`，占位符 `%d%%`、`%d%%`、`%d%%` 及数值转义 `100%%`、`20%%`、`0%%` 完全一致；“命中敌人的远程攻击”准确对应回调中的 `if hitted` 判定；3 行段落与无缩进格式均与源码吻合。

---

### 复核结果汇总

- **覆盖总数**：40 条（`entry-02268` ～ `entry-02307`）
- **未发现问题**：33 条
- **细微观察**：4 条（`entry-02269`、`entry-02278`、`entry-02280`、`entry-02290`、`entry-02306`，主要涉及轻微机翻用词、段落拆分格式差异、源码机制补充说明及原版英文瑕疵的规避）
- **存在疑点**：3 条
  - `entry-02273`：段落拆分多出换行；“affinity with the earth”误译为“土壤相关影响”；“forced movement”被泛化为“任何移动”；“冷却时间回合数：%d%%”语病。
  - `entry-02277`：段落被合并导致少了一处换行缩进；省略了“时空回复力场”概念与未来返还的时空风味；技能名引用译作“时间屏障”（偏离统一术语“时间盾”）。
  - `entry-02303`：同系技能 Tumble 被译为“翻滚”，与该技能在当前文件及术语库中的正名“翻筋斗”不一致；段落多出一处换行拆分。