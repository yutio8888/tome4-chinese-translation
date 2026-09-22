本批次（batch-084）只读译文复核工作已完成。

### 批次文件校验
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-084.md`
- **预期 SHA-256**：`d1c63c11010430a99a9f340f30df4256dfd682b11511d856d243d55f7ed4b7d3`
- **实测 SHA-256**：`d1c63c11010430a99a9f340f30df4256dfd682b11511d856d243d55f7ed4b7d3`（校验一致）
- **核验源码来源**：引擎/模块固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/timed_effects/mental.lua` 与 `game/modules/tome/data/timed_effects/other.lua`）；译文基准 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核报告（entry-02732 ～ entry-02771，共 40 条）

#### entry-02732
- **位置**：`mod-tome.lua:36313` (`mod-tome/data/timed_effects/mental.lua`)
- **结论**：未发现问题
- **依据**：源码 `mental.lua:2658` 为 `EFF_MIND_PARASITE` 获得提示；`#Target#` 标签保留完整；`mind parasite` 译为“精神寄生虫”准确符合语境；标点对应无误。

#### entry-02733
- **位置**：`mod-tome.lua:36315` (`mod-tome/data/timed_effects/mental.lua`)
- **结论**：未发现问题
- **依据**：源码 `mental.lua:2659` 为 `EFF_MIND_PARASITE` 消失提示；`#Target#` 占位符保留，译文“摆脱了精神寄生虫”准确传达 `is free from` 含义。

#### entry-02734
- **位置**：`mod-tome.lua:36332` (`mod-tome/data/timed_effects/mental.lua`)
- **结论**：未发现问题
- **依据**：源码 `mental.lua:2762` 调用 `self:logCombat(target, ..., string.his_her(self))`；`%s` 运行时解析为性别代词“他的/她的/它的”，与后续“灵能武器”组合为“用其/他的灵能武器进行反击”，语法通顺；`#CRIMSON#`、`#LAST#` 颜色代码及 `#Source#`、`#Target#` 占位标签完整。

#### entry-02735
- **位置**：`mod-tome.lua:36391` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:118` 为 `EFF_ELEMENTAL_SURGE_COLD` 状态说明，底层为 `on_melee_hit` 与 `DamageType.ICE`。占位符 `%d`、`%d` 顺序无误。存在两处观察：① 术语差异：`terminology/combat.tsv` 中 `ice` 伤害类型统一译为“寒冰”，此处译文使用了“冰系”；② 句式意译：原文“deals %d ice damage when hit in melee”采取了“获得 %d 冰系近战反伤”的机制向意译，机制正确但术语未对齐“寒冰伤害”。

#### entry-02736
- **位置**：`mod-tome.lua:36414` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:195` 为 `EFF_ABSORPTION_STRIKE` 减益结束提示；`#Target#` 标签保留，“光明的回复”准确对应 `light resistance` 恢复原值。

#### entry-02737
- **位置**：`mod-tome.lua:36429` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:288` 为 `EFF_TREE_OF_LIFE` 获得提示；`#LIGHT_BLUE#` 与 `#Target#` 标签完整保留，扎根状态描述准确。

#### entry-02738
- **位置**：`mod-tome.lua:36435` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:317` 为 `EFF_INFUSION_COOLDOWN` 饱和说明；`infusions` 正确对齐术语“纹身”；占位符 `%d` 对应 `eff.power`，机制说明完整。

#### entry-02739
- **位置**：`mod-tome.lua:36438` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:334` 为 `EFF_RUNE_COOLDOWN` 饱和说明；`runes` 对齐术语“符文”；占位符 `%d` 完整无误。

#### entry-02740
- **位置**：`mod-tome.lua:36441` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:351` 为 `EFF_TAINT_COOLDOWN` 饱和说明。占位符 `%d` 保持一致。观察点：在 `terminology/talents.tsv` 中，`taints`（刻印类型）的推荐标准术语为“污印”，此处译文沿用了局部旧译“堕落印记”（与 36440 行 subtype 译名呼应），与术语库 preferred 规范略有差异。

#### entry-02741
- **位置**：`mod-tome.lua:36460` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:477` 为 `EFF_TIME_DOT`（时间护盾破碎后生成的回血场）获得提示；`#target#`（小写）与源码传参完全一致，语义准确。

#### entry-02742
- **位置**：`mod-tome.lua:36475` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:546` 为 `EFF_CONTINUUM_DESTABILIZATION` 效果名称；“连续体失稳”为时空法术核心既有机制术语，准确无误。

#### entry-02743
- **位置**：`mod-tome.lua:36478` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:552` 获得失稳效果浮动文字；前缀 `+` 与“失稳”词干保持一致。

#### entry-02744
- **位置**：`mod-tome.lua:36480` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:553` 失稳效果消失浮动文字；前缀 `-` 与“失稳”词干保持一致。

#### entry-02745
- **位置**：`mod-tome.lua:36481` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:575` 为 `EFF_SUMMON_DESTABILIZATION` 效果名称；对齐 `Summon 召唤` 术语，译作“召唤失稳”准确。

#### entry-02746
- **位置**：`mod-tome.lua:36491` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:627` 为 `EFF_SEE_THREADS`（命运螺旋）说明；占位符 `%d` 正确对应当前时间线编号 `eff.thread`；语义完整通顺。

#### entry-02747
- **位置**：`mod-tome.lua:36505` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:799` 为 `EFF_SEVER_LIFELINE` 获得提示。占位符 `#Target#` 保留完整。观察点：动词“sever”本义为“切断/斩断/割裂”，同技能描述 36504 行使用了“生命线被切断”，此处译为“生命线被收割了”（收割通常对应 harvest/reap），选词偏离了原词的“切断/断绝”含义。

#### entry-02748
- **位置**：`mod-tome.lua:36508` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:811-812` 为 `EFF_FADE_FROM_TIME` 说明；依次传入造成伤害降低、受到伤害降低、负面状态缩短三个数值，译文中 3 个 `%d%%` 占位符顺序与源码完全吻合，机制描述准确。

#### entry-02749
- **位置**：`mod-tome.lua:36522` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:902` 为 `EFF_ZERO_GRAVITY` 说明；“移动速度降至原来的三分之一”、“击退”（knockback 术语）以及“负重上限大幅增加”与底层机制完全契合，无占位符遗漏。

#### entry-02750
- **位置**：`mod-tome.lua:36528` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:950-960` 为 `EFF_CURSE_OF_CORPSES` 说明。参数映射显式声明为 `{1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13}`，精准适配了中文在 Power 3 中调整占位符语序（原英文为 回合[9] -> 等级[10] -> 生命阈值[11]，中文调整为 回合[9] -> 生命阈值[11] -> 等级[10]）的需求；术语“腐秽呕吐”（Retch）、“亡灵”（Undead）、“食尸鬼”（Ghoul）、“人形生物”（Humanoid）完全对齐术语库。

#### entry-02751
- **位置**：`mod-tome.lua:36540` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1026` 为诅咒唤醒的行尸（`npcWalkingCorpse`）描述文本；译文通顺流畅，无格式缺陷。

#### entry-02752
- **位置**：`mod-tome.lua:36546` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1114-1125` 为 `EFF_CURSE_OF_MADNESS` 说明；全文 11 处占位符（包含正负符号修饰符 `%+d%%`、`%+d`、`%s`、`%0.1f%%`）数量、类型与顺序与源码严格一致；精神抗性、混乱免疫、暴击伤害、副手武器伤害、幸运、敏捷等术语无误。

#### entry-02753
- **位置**：`mod-tome.lua:36557` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1179` 狂热触发时的日志；`#F53CBE#` 颜色代码闭合无误，占位符 `%s` 对应角色名，机制为扣减冷却时间，译文准确。

#### entry-02754
- **位置**：`mod-tome.lua:36559` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1297` 为 `EFF_CURSE_OF_SHROUDS` 名称；译作“帷幕诅咒”，准确规范。

#### entry-02755
- **位置**：`mod-tome.lua:36560` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1298` 为 `short_desc` 短名称；“帷幕”与主名称一致。

#### entry-02756
- **位置**：`mod-tome.lua:36561` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1316` 为状态栏悬浮标题；占位符 `%0.1f` 对应诅咒强度等级，格式一致。

#### entry-02757
- **位置**：`mod-tome.lua:36562` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1319-1330` 为 `EFF_CURSE_OF_SHROUDS` 详细说明；12 处格式化参数与占位符严格匹配；暗影抗性、暗影抗性上限、看破隐形、幸运、体质等术语准确；颜色码完整。

#### entry-02758
- **位置**：`mod-tome.lua:36573` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1391` 为 `EFF_SHROUD_OF_WEAKNESS` 效果名；“虚弱帷幕”准确规范。

#### entry-02759
- **位置**：`mod-tome.lua:36574` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：存在疑点
- **依据**：源码 `other.lua:1392` 为 `EFF_SHROUD_OF_WEAKNESS` 说明。原文为 `The target is enveloped in a shroud that seems to hang upon it like a heavy burden. (Reduces damage dealt by %d%%).`。译文为 `目标笼罩在虚弱帷幕中（造成的伤害降低 %d%%）。`。原文核心描写从句 `that seems to hang upon it like a heavy burden`（宛如沉重的负担悬压在它身上）被完全漏译，且原文通称 `a shroud` 被直接换成了效果名。存在实质性的修辞文本漏译。

#### entry-02760
- **位置**：`mod-tome.lua:36575` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1409` 为 `EFF_SHROUD_OF_PASSING` 效果名；“消逝帷幕”译名契合移动淡出的机制。

#### entry-02761
- **位置**：`mod-tome.lua:36576` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1410` 为 `EFF_SHROUD_OF_PASSING` 说明；占位符 `+%d%%` 保留，全抗性增益说明无误。

#### entry-02762
- **位置**：`mod-tome.lua:36577` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1432` 为 `EFF_SHROUD_OF_DEATH` 效果名；“死亡帷幕”译名准确。

#### entry-02763
- **位置**：`mod-tome.lua:36582` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:1477-1490` 为 `EFF_CURSE_OF_NIGHTMARES` 详细说明；全段 15 处占位符顺序完全正确；精神豁免、物理抗性、意志、幸运、精神/暗影伤害等术语规范。观察点：① Power 3 机制名“Harrow”在技能描述中被译为“折磨”（折磨光环），但在对应触发日志（entry-02764）中却被译为“惊扰”，同机制名词与动词译法分裂；② 译文末行存在多余双空格（“持续 8 回合。  触发几率  在每次你受到打击时提高”）。

#### entry-02764
- **位置**：`mod-tome.lua:36593` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:1532, 1546` 为噩梦诅咒 Harrow 触发时的战斗日志；颜色码 `#F53CBE#` 与两个 `%s` 占位符完整。观察点：如前条所述，此处的动词“harrows”译作“惊扰”，与前一条 entry-02763 的机制名“折磨”不一致。

#### entry-02765
- **位置**：`mod-tome.lua:36600` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：细微观察
- **依据**：源码 `other.lua:1699-1709` 为 `EFF_CURSE_OF_MISFORTUNE` 说明；7 处占位符及其正负号修饰符与源码严格匹配；灵巧、幸运、陷阱、闪避等术语对齐准确。观察点：Power 1+ 句中含有连续双空格排版缺陷（“围绕你的努力都会失败  (+%d%% 避开陷阱的几率)”）。

#### entry-02766
- **位置**：`mod-tome.lua:36611` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1752` 为厄运终结致死触发时的日志；`#F53CBE#` 颜色代码与占位符 `%s` 完整，句意准确。

#### entry-02767
- **位置**：`mod-tome.lua:36612` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1754` 为厄运终结增伤未致死时的日志；“遭受了一记厄运之击”准确对应 `suffers an unfortunate blow`。

#### entry-02768
- **位置**：`mod-tome.lua:36619` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1796` 为 `EFF_CURSED_FORM` 字符串拼接片段；前置空格严格保留以供多段拼接；力量、意志、毒素、疾病等术语完全匹配；占位符 `%d` 与 `%d%%` 无误。

#### entry-02769
- **位置**：`mod-tome.lua:36623` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1888` 为 `EFF_PREDATOR` 猎物减伤列表前缀；前置换行符 `\n` 正确保留；占位符 `%d%%` 与末尾冒号格式无误。

#### entry-02770
- **位置**：`mod-tome.lua:36630` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1941` 为 `EFF_HIGHBORN_S_BLOOM` 效果名；与 26812 行种族技能名“高等人类之绽放”严格统一。

#### entry-02771
- **位置**：`mod-tome.lua:36636` (`mod-tome/data/timed_effects/other.lua`)
- **结论**：未发现问题
- **依据**：源码 `other.lua:1974` 为 `EFF_SOLIPSISM` 唯我状态说明；参数为 `eff.power * 100`，占位符 `-%d%%` 匹配；术语“全局速度”（global speed）严格遵守了术语库的 preferred 核心规范，未误写为整体速度或全体速度。

---

### 复核总结
- **核验条目总数**：40 条（entry-02732 至 entry-02771，无省略遗漏）
- **未发现问题**：34 条
- **存在疑点**：1 条（entry-02759 存在定语从句漏译）
- **细微观察**：5 条（entry-02735 伤害类型术语/句式意译；entry-02740 污印术语偏离；entry-02747 选词偏离；entry-02763 与 entry-02764 机制名/动作日志分歧及多余空格；entry-02765 多余双空格）