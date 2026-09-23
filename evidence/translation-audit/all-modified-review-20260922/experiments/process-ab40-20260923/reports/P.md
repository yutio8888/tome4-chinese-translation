本报告仅为只读 A/B 研究旁路观察，不构成正式生产 contract 验收，也不宣称 `DONE_VERIFIED`。冻结输入共 40 条；输入文件及 29 份可用 Orcs 源码哈希均与 `FREEZE.json` / `source-access.json` 一致。Possessors 三个 section 的源码状态为 `unavailable`，未以其他组件替代。

### 逐条结论

| entry-ID | 结论 | claim / 简短依据 |
|---|---|---|
| entry-03734 | OK | “浪费这一发”译作“浪费子弹”可等价理解 |
| entry-03740 | ISSUE | C01：漏掉召唤“持续数回合”的限制 |
| entry-03744 | OK | “for now”虽未逐字出现，但后句已明确越界即翻脸，条件结构仍在 |
| entry-03770 | OK | 名称、开放状态及 source_tag 相符 |
| entry-03781 | OK | `stralite → 斯莱特` 符合 global preferred 术语 |
| entry-03841 | ISSUE | C02：把“命中并在其上引爆的实体”扩大成爆炸“波及”的实体 |
| entry-03857 | ISSUE | C03：`Species` 被缩窄为“人种” |
| entry-03858 | ISSUE | C04：把“被拉来时已经着火”改成“拉来时突然着火” |
| entry-03862 | ISSUE | C05–C07：仁政、年度联络信息、城市废墟三处叙事事实变化 |
| entry-03866 | ISSUE | C08：把尚未发生的设想写成已发生经历 |
| entry-03867 | ISSUE | C09–C10：漏掉求救呼声，并把艾琳主动罢手改成被击败 |
| entry-03868 | ISSUE | C11：违反适用的 `Scourge from the West → 西方天灾` preferred 术语 |
| entry-03870 | ISSUE | C12：把奥术力量自身变异风险改成人为扭曲 |
| entry-03873 | OK | 主要事件、推断链及建议均保留 |
| entry-03874 | OK | C13 advisory：`allowed to live` 写成“才被创造”，有时序差异，但可视作造物获准存续的意译 |
| entry-03877 | OK | 警醒对象与兽人历史困境均保留 |
| entry-03891 | ISSUE | C14：把“百分比较高的一种能量”误写成正负能量都如此 |
| entry-03893 | OK | C15 advisory：`%d units long` 写成“墙长 %d”，单位表达欠完整但数值功能仍清楚 |
| entry-03894 | OK | “能施放你所有法术”可表达镜像具备施法者法术；源码克隆实现支持该读法 |
| entry-03915 | ISSUE | C16：遗漏主动取消效果也会触发周围伤害 |
| entry-03920 | OK | 基础攻击触发、范围、免疫与九回合限制完整 |
| entry-03923 | OK | 半径、伤害、35 蒸汽目盲和强度系数均完整 |
| entry-03932 | OK | 近战或远程攻击未命中时反击、每回合一次及耗弹均保留 |
| entry-03955 | OK | 嘲讽装置、反伤、生命、持续时间和属性缩放完整 |
| entry-03962 | OK | 六回合控制、结束死亡及排除对象完整 |
| entry-03976 | OK | 武器倍率、移除浸湿及半径 4 火焰伤害完整 |
| entry-03994 | OK | 半径 4、130% 和奥术伤害完整；“所有目标”未与已读实现形成实质冲突 |
| entry-03995 | OK | 含义准确；同句 preferred 术语的 source_tag 为 `logSeen`，不直接约束本条 `logPlayer` |
| entry-04039 | ISSUE | C17：漏掉 `fully` 和 `damaging actions`，由整次伤害行为取消缩成一般吸收伤害 |
| entry-04042 | OK | 状态获得文本准确 |
| entry-04078 | ISSUE | C18：把施虐者造成痛苦与破坏的描述改成雪人成为杀戮机器 |
| entry-04086 | OK | “叫着”弱于 `shouts`，但未形成实质意义变化 |
| entry-04087 | OK | 虽把 Amulet 明说成“神”，但物品即 `Gardanion, the Light of God`，邻文支持该读法 |
| entry-04100 | OK | Psyshot、Tinker 译名与 DLC 术语一致 |
| entry-04102 | OK | 解锁对象、职业、四项技能及效果完整 |
| entry-04112 | OK | 前导空格和 `%s` 均保留，动态拼接安全 |
| entry-04119 | OK | 对新手可能困惑概括为“不适合新手”属合理警示表达 |
| entry-04121 | OK | 主手武器与副手灵晶两个条件均保留 |
| entry-04126 | OK | 储存额外副本、特殊阶级三分之一且至少一次均保留；机制源码不可用 |
| entry-04127 | OK | 阶级限制、33% 递减、生命与灵能恢复、治疗阻断例外及唯一治疗方式完整；机制源码不可用 |

全部格式参数序列均一致，未发现 `%d`、`%0.2f`、`%s` 或 `%%` 的漏参、错序。

### 原子观察

**C01 — entry-03740**

- 原译短引：`“summon him for a few turns at will”` → `“具有召唤他的能力”`
- 意义变化：漏掉召唤物只持续数回合；译文容易被理解为无持续时间限制。`at will` 的主动可用性质也被弱化。
- 最强反证及处理：前文已说明把约翰绑定到戒指，但没有其他句子补回持续时间，因此不能由语境恢复。
- 判定：`confirmed`
- 证据：`entries.json`；已验哈希源码 `.../chats/john-surrender.lua:117`
- 状态：text_status=译文新增遗漏；snapshot_fact=冻结源码明确写有 `for a few turns`；target_applicability=Orcs 来源未固定，仅适用于本轮哈希快照；影响=机制/操作。

**C02 — entry-03841**

- 原译短引：`“entity it detonates against”` → `“其引爆所波及的任何自主实体”`
- 意义变化：原文保证摧毁导弹撞上并引爆的那个实体；“波及”扩大为爆炸范围内被影响的所有实体。
- 最强反证及处理：整段是夸张广告，但句法中的 `against` 仍限定直接碰撞对象；幽默语气不能抵消范围变化。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/destructicus.lua:37`
- 状态：text_status=译文新增范围扩大；snapshot_fact=冻结广告文本；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C03 — entry-03857**

- 原译短引：`“Assessment of the Species”` → `“关于人种的调查”`
- 意义变化：`species` 是物种；“人种”通常限于人类内部族群。
- 最强反证及处理：同一冻结源码还有标题 `Chapter 48: Steam Giants`，说明该系列讨论非人类物种，不能按“人种”理解。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/misc.lua:136,153`
- 状态：text_status=译文缩窄指称；snapshot_fact=系列标题覆盖蒸汽巨人；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C04 — entry-03858**

- 原译短引：`“had already caught fire when ... pulled it in”` → `“拉入……的时候，这张纸条突然着火了”`
- 意义变化：原文中纸条在被异常拉入时已经着火；译文改成拉入过程触发突然起火。
- 最强反证及处理：后句只说明烧毁速度，没有消除前句的先后与因果区别。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/misc.lua:154`
- 状态：text_status=译文新增时序/因果变化；snapshot_fact=冻结叙事明写 `already`；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C05 — entry-03862**

- 原译短引：`“mercifully brief reign”` → `“短暂的仁政”`
- 意义变化：`mercifully` 修饰“短暂”——幸而统治很短；“仁政”却把统治性质改为仁慈。
- 最强反证及处理：该句把其统治列为正史失去客观性的例外，反而不支持“仁政”。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/palace-fumes.lua:69`
- 状态：text_status=译文新增人物评价；snapshot_fact=冻结原文；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C06 — entry-03862**

- 原译短引：`“yearly messages dropped on the Palace's front steps”` → `“一条在烟雾宫殿前门留下的年度总结信息”`
- 意义变化：每年有人投递信息，变成一条“年度总结”；还把普通 `Palace` 异化为“烟雾宫殿”。
- 最强反证及处理：上下文讨论的是为何至今仍知道联络方式，复数、周期性的投递正是证据；“年度总结”没有文本依据。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/palace-fumes.lua:75`
- 状态：text_status=译文新增对象与地点变化；snapshot_fact=冻结叙事；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C07 — entry-03862**

- 原译短引：`“shards of your ruined cities”` → `“你们文明的废墟”`
- 意义变化：从被毁城市的残骸扩大为整个文明的废墟。
- 最强反证及处理：前文 `trip ... and shatter` 是对族群失败的比喻，但后句明确落到复数 `cities`；没有把城市等同整个文明的依据。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/palace-fumes.lua:73`
- 状态：text_status=译文范围扩大；snapshot_fact=冻结原文；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C08 — entry-03866**

- 原译短引：`“salivated at the prospect of traveling ... and seeing”` → `“他旅行到远东，看到……而垂涎不已”`
- 意义变化：原文只是期待未来去远东观看兽军惨状；译文断言旅程和观看已经发生。
- 最强反证及处理：本段连续叙述实际行为，但 `at the prospect of` 明确把该项标为尚未实现的设想。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/pocket-time.lua:59`
- 状态：text_status=译文新增已发生事件；snapshot_fact=冻结叙事；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C09 — entry-03867**

- 原译短引：`“despite the calls to help ... heard”` → 无对应文字
- 意义变化：漏掉主角曾听见求救却仍未阻止仪式，削弱艾琳责怪主角的理由。
- 最强反证及处理：后句只保留“艾琳归咎于主角”，不能补回主角曾收到求救这一事实。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/pocket-time.lua:86`
- 状态：text_status=译文新增遗漏；snapshot_fact=冻结牺牲分支；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C10 — entry-03867**

- 原译短引：`“Aeryn relented”` → `“艾琳被击败了”`
- 意义变化：艾琳主动罢手变成遭到击败。
- 最强反证及处理：英文后半句的动态代词本身存在可疑指代，但谓词 `relented` 与 `was defeated` 仍不等价；应把上游指代异常单列，不能据此确认译文忠实。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/pocket-time.lua:86`
- 状态：text_status=译文改变事件结果；snapshot_fact=冻结英文存在指代异常但仍写明 `relented`；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C11 — entry-03868**

- 原译短引：`“Scourge from the West”` → `“西方灾星”`
- 意义变化：未使用本包明确裁定的个体称号“西方天灾”。
- 最强反证及处理：术语条目为 `_t / preferred / dlc`，本条同为 `_t` 且属于 Orcs DLC，完整适用；`existing` 保留规则不适用于该 preferred 行。
- 判定：`confirmed`
- 证据：`entries.json`；`terms.json` 中 `terminology/society.tsv:34`；源码 `.../lore/pocket-time.lua:110`
- 状态：text_status=术语不一致；snapshot_fact=冻结术语明确排除“灾星”；target_applicability=dlc scope 覆盖 orcs；影响=叙事事实。

**C12 — entry-03870**

- 原译短引：`“carries the risk of mutating into something”` → `“有着被人扭曲……的危险性”`
- 意义变化：奥术衍生物自身可能变异，变成必须由某个人去扭曲。
- 最强反证及处理：前后论点是奥术固有风险，与是否包装成天体说辞无关；没有人为施术者作为必要条件。
- 判定：`confirmed`
- 证据：`entries.json`；`.../lore/primal-forest.lua:92`
- 状态：text_status=译文改变风险机制的施事；snapshot_fact=冻结叙事论证；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

**C13 — entry-03874**

- 原译短引：`“only allowed to live when they were out of ammunition”` → `“直到他们弹尽粮绝，我们才被创造”`
- 意义变化：从造物经审查后被允许存续，改成众神无话可说后才开始创造。
- 最强反证及处理：上一段已说 `we were still made`，支持“先被造出、再获准活下去”；但也可把设计审查整体概括成创造完成，因此证据不足以确认为错误。
- 判定：`advisory`
- 证据：`entries.json`；`.../lore/weissi.lua:44`
- 状态：text_status=可能的时序弱化；snapshot_fact=冻结原文；target_applicability=未固定 Orcs 源码快照；影响=表达建议。

**C14 — entry-03891**

- 原译短引：`“Whichever ... is a higher percentage regenerates towards its max”` → `“无论是你的正能量还是负能量都将……”`
- 意义变化：原文仅让当前百分比较高的一种能量朝上限恢复；译文可读成正负两者都进行同一变化，而且未表达比较选择。
- 最强反证及处理：实现按正、负能量占各自上限的比例作 `if/else`，只把较高者设为正向恢复，另一者维持/恢复正常衰减。
- 判定：`confirmed`
- 证据：`entries.json`；`.../talents/celestial/energies.lua:60-99,124-125`
- 状态：text_status=机制条件错译；snapshot_fact=已验哈希实现明确二选一；target_applicability=未固定 Orcs 源码快照；影响=机制/操作。

**C15 — entry-03893**

- 原译短引：`“wall %d units long”` → `“一堵墙长 %d”`
- 意义变化：漏掉长度单位词，中文显示略显残缺。
- 最强反证及处理：参数顺序正确，玩家仍可把 `%d` 理解为墙长，未证成机制误导。
- 判定：`advisory`
- 证据：`entries.json`；`.../talents/celestial/reflection.lua:247-250`
- 状态：text_status=表达不完整；snapshot_fact=参数消费正确；target_applicability=未固定 Orcs 源码快照；影响=表达建议。

**C16 — entry-03915**

- 原译短引：`“broken or cancelled”` → 仅写攻击或使用技能“中断效果，同时……造成伤害”
- 意义变化：译文只把结算伤害连接到攻击/技能中断，没有说明玩家主动取消持续效果也会结算。
- 最强反证及处理：实现的 `deactivate` 统一进行范围攻击，除存档清理/重置外，主动取消同样进入该路径。
- 判定：`confirmed`
- 证据：`entries.json`；`.../talents/steam/battlefield-management.lua:58-84,87-92`
- 状态：text_status=机制触发条件遗漏；snapshot_fact=已验哈希实现；target_applicability=未固定 Orcs 源码快照；影响=机制/操作。

**C17 — entry-04039**

- 原译短引：`“fully absorb any damaging actions”` → `“吸收伤害”`
- 意义变化：原文是一定概率完全取消一次造成伤害的行为；译文像是一般伤害吸收，漏掉“完全”和行为级取消。
- 最强反证及处理：实现将数值写入 `cancel_damage_chance`，不是固定数值的伤害减免或护盾。
- 判定：`confirmed`
- 证据：`entries.json`；`.../timed_effects/physical.lua:693-705`
- 状态：text_status=防御机制弱化/模糊；snapshot_fact=已验哈希实现；target_applicability=未固定 Orcs 源码快照；影响=机制/操作。

**C18 — entry-04078**

- 原译短引：`“Whoever tortured ... did an amazing job of pain and destruction”` → `“它的确变成了一个恐怖的杀戮机器”`
- 意义变化：原文评价施虐者极其有效地制造了痛苦与破坏；译文新增雪人成为杀戮机器的结论，且删去对施虐过程的评价。
- 最强反证及处理：后两句只列斯莱特护甲和蒸汽链锯，能支持战斗改造，但不能使两种叙事陈述等价。
- 判定：`confirmed`
- 证据：`entries.json`；`.../zones/gem/npcs.lua:94`
- 状态：text_status=译文替换叙事事实；snapshot_fact=冻结实体描述；target_applicability=未固定 Orcs 源码快照；影响=叙事事实。

### 实际读取文件

冻结研究输入：

- `RULES.md`
- `INPUT-P.md`
- `FREEZE.json`
- `source-access.json`
- `entries.json`
- `context.lua`
- `terms.json`

以上均位于：

`evidence/translation-audit/all-modified-review-20260922/experiments/process-ab40-20260923/`

已读取并核验哈希的源码：

- `sources/dlc/orcs/tome-orcs/data/chats/{destructicus.lua,john-surrender.lua,kaltor-entry.lua}`
- `sources/dlc/orcs/tome-orcs/data/general/grids/slumbering_cave.lua`
- `sources/dlc/orcs/tome-orcs/data/general/objects/steamgun.lua`
- `sources/dlc/orcs/tome-orcs/data/lore/{destructicus.lua,misc.lua,palace-fumes.lua,pocket-time.lua,primal-forest.lua,sunwall.lua,weissi.lua}`
- `sources/dlc/orcs/tome-orcs/data/quests/amakthel.lua`
- `sources/dlc/orcs/tome-orcs/data/talents/celestial/{energies.lua,reflection.lua}`
- `sources/dlc/orcs/tome-orcs/data/talents/steam/{battlefield-management.lua,demolition.lua,engineering.lua,gunslinging.lua,other.lua,psytech-gunnery.lua}`
- `sources/dlc/orcs/tome-orcs/data/talents/uber/mag.lua`
- `sources/dlc/orcs/tome-orcs/data/timed_effects/physical.lua`
- `sources/dlc/orcs/tome-orcs/data/zones/gem/npcs.lua`
- `sources/dlc/orcs/tome-orcs/data/zones/slumbering-caves/{npcs.lua,objects.lua}`
- `sources/dlc/orcs/tome-orcs/overload/data/texts/{unlock-tinker_psyshot.lua,unlock-wyrmic_undead.lua}`
- `sources/dlc/orcs/tome-orcs/overload/mod/dialogs/CreateTinker.lua`

未读取其他任务、报告或未列入入口白名单的文字输入；未写文件，未创建子 agent。