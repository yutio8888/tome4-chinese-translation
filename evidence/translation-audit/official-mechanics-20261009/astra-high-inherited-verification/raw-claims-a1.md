已完成全部 **310 项**逐项校准，未修改任何文件。冻结输入 SHA256 与指定值一致；输入列出的 187 份源码快照均通过哈希核对。旧 `confirmed` 不作为事实保留。

按角色契约实际列出的 **7 个字段**返回，不另造第八字段。以下结论是校准建议，最终状态及是否应用仍由宿主裁决。

为压缩重复路径，源码定位使用以下明确缩写：

- **C/**＝固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/`；**T/**＝其 `data/talents/`，**B/**＝`data/birth/`，**O/**＝`data/general/objects/`，**X/**＝`data/timed_effects/`。
- **E/**＝同一固定 commit 的 `game/engines/default/`。
- **A/**＝`tome-ashes-urhrok/`，**U/**＝`tome-cults/`，**R/**＝`tome-orcs/`。DLC 定位后的 `@` 值为已核对 SHA256 的前 12 位；完整值由冻结输入的 `source_verification` 唯一确定。**所有 DLC 结论均仅适用于该快照，源码来源／commit 未固定。**
- 各行只给需要替换的最小句段；未涉及的占位符、颜色标记及内容保持不变。表中的“无需修改”表示不作为必修问题，不代表禁止日后润色。

| Finding ID | Assessment | Design/AC basis | Observable impact | Personal-project proportionality | Minimum sufficient action | Rationale |
|---|---|---|---|---|---|---|
| M001 | keep | 属性指称准确 | 把魔力属性写成泛指魔法 | 单词修订即可 | 精神强度加成句中的“魔法”改为“魔力”。 | C/class/interface/Combat.lua:2127–2128 直接读取 `getMag()`；T/celestial/darkside.lua:64–80 与意志属性并列。两版均遗留该称呼。 |
| M002 | keep | 触发主体准确 | 感染能力归给了被攻击方 | 修正主体即可 | “站在荒芜之地的生物造成伤害时，有40%几率使受害者感染疾病；每回合最多触发一次。” | X/floor.lua:84–90 给区域内生物添加 `blighted_soil`；C/data/damage_types.lua:708–715 检查的是伤害来源 `src`，不是受害者。英文也存在方向误导。 |
| M003 | downgrade | 显示含义清楚 | “总计”略含糊，但不证明累计消耗误读 | 不值得强制修订 | 无需修改；可选“%d，当前能量%d/%d”。 | C/class/Object.lua:2221 的外层已有消耗标签，三个参数依次为消耗、当前值、上限；当前译文没有明确声称后两项是累计消耗。 |
| M006 | downgrade | 可读性 | 仅段间空行差异 | 不作为必修 | 无需修改。 | T/celestial/hymns.lua:393–402；五部分信息仍分开，未发现内容、参数或标记丢失。缺少同样数量的空行不足以证明可见缺陷。 |
| M007 | keep | 伤害类型一致 | 暗影类型出现另一名称 | 局部对齐即可 | 伤害类型处统一为“暗影伤害”。 | T/celestial/hymns.lua:75–78、178–181、248–251 实际使用 `DARKNESS`；420–421 为对应说明。冻结术语将该类型定为“暗影”。 |
| M008 | downgrade | 护盾持续时间 | 可能少一点上限语气 | 可选澄清 | 无需修改；可选“最多持续%d回合”。 | T/celestial/light.lua:104–116 同时给出吸收量与持续时间；X/magical.lua 的护盾会耗尽。常规“持续”并不保证护盾在吸收量耗尽后仍存在。 |
| M009 | keep | 属性指称准确 | 缩放属性名称错误 | 局部修订 | “魔法”改为“魔力”。 | T/celestial/other.lua:198 的缩放读取魔力属性，非泛指魔法。官方与当前译文均保留旧称。 |
| M010 | keep | 条件与时序准确 | 可误以为减冷却与增益同时取得 | 补互斥条件即可 | “若阳光射线正在冷却，则使其冷却减少1回合；否则获得持续2回合的增益。” | T/celestial/sun.lua:145–155 使用 `if … else`；两种效果互斥。 |
| M011 | downgrade | 伤害承受方清楚 | 现句有轻微主语歧义 | 不作为机制错误 | 无需修改；可选“目标感染疾病，每回合受到%0.2f点枯萎伤害。%s”。 | X/magical.lua:2432–2446 确实伤害感染者，但汉语“感染疾病，每回合造成伤害”可自然理解为疾病造成伤害，未明确把伤害施加给他人。 |
| M012 | narrow | 风味信息完整 | 遗漏变化速度与表面杂乱感 | 低成本补短语 | 将末句改为“光芒在鳞甲表面迅速变幻，看似杂乱无章”。 | O/boss-artifacts-far-east.lua:138 明示快速、看似杂乱；属于外观信息，不影响护甲机制。 |
| M013 | keep | 属性指称准确 | 自动闪电缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | O/boss-artifacts-far-east.lua:339–342、390 使用 `getMag()` 计算闪电效果。 |
| M014 | downgrade | 随机效果准确 | 可以更明确随机性 | 不作为必修 | 无需修改；可选“随机施加其中一种效果”。 | C/data/damage_types.lua:3878–3905 随机选择四种状态之一；现译用“或”列举，没有承诺玩家选择或同时施加。 |
| M018 | defer_to_user | 高复用机制名称 | 同一机制跨条称呼不同 | 应统一策略后处理 | 当前不自动修改；若宿主选定“异常”，仅对本条相应机制名对齐。 | T/chronomancy/flux.lua:156–208 指向同一延后异常系统；代码能确定指称相同，不能独自决定“异常／异变”的全局译名。 |
| M020 | defer_to_user | 专名策略 | 音译后缀不一致疑点 | 不凭代码改专名 | 当前无需修改；由宿主确定 telugoroth 的统一音译。 | X/magical.lua:2882–2884 仅确定实体为 telugoroth，无法证明“泰鲁戈洛斯”这一音译本身错误。 |
| M021 | downgrade | 数值名称准确 | 无实际数值差异 | 不作为必修 | 无需修改。 | X/magical.lua:3219–3228 指向最大生命值；“最大生命”与“最大生命值”在此同义，未改成当前生命。 |
| M022 | keep | 装备范围准确 | 可误以为任意护甲均可合成 | 补部位即可 | 将“护甲”改为“躯干护甲”。 | O/boss-artifacts-maj-eyal.lua:1253–1255 限制 `BODY`，并非所有护甲槽。 |
| M023 | keep | 属性指称准确 | 触发伤害缩放属性错名 | 局部修订 | 属性处“魔法”改为“魔力”。 | O/boss-artifacts.lua:133–144 使用 `getMag()` 计算相关伤害及减速。 |
| M024 | downgrade | 名称显示 | 仅名称末尾句号 | 不值得必修 | 无需修改。 | O/brotherhood-artifacts.lua:234 为未鉴定名称；句号不会改变对象识别或运行行为，未提供截断等可见故障证据。 |
| M025 | keep | 属性指称准确 | 警觉缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | T/chronomancy/guardian.lua:125–154 的对应计算读取魔力属性。 |
| M026 | reject | 机制含义准确 | 无已证实误导 | 不为同义词制造修复 | 无需修改。 | T/chronomancy/induced-phenomena.lua:335–337 的 expanding 对应“扩展”成立；并未把扩张阶段写成收缩阶段。“膨胀”只是另一措辞。 |
| M027 | downgrade | 可读性 | 首段新增换行 | 不作为必修 | 无需修改。 | T/chronomancy/other.lua:121–130；首选紊乱值与调谐说明仍相连，新增换行没有改变适用条件。 |
| M028 | narrow | 属性准确；排版适度 | 魔力错名成立，换行不构成必修 | 只改单词 | “魔法”改为“魔力”；不强制恢复源串换行。 | T/chronomancy/other.lua:218 使用 `STAT_MAG`；218–232 的段落差异不改变其加成或豁免。 |
| M029 | keep | 属性指称准确 | 地雷缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | T/chronomancy/spacetime-folding.lua:217 对应 `getMag()`。 |
| M031 | keep | 判定频率与概率准确 | 混淆施法失败和持续技能关闭概率 | 修机制句即可 | “每层使施法失败几率提高10%%，并使每个持续法术每回合有额外1%%几率被关闭；最多叠至50%%和5%%。” | O/egos/ammo.lua:622–627 添加层数；X/physical.lua:2137–2157 累积强度；C/class/Actor.lua:5886–5888 在施法时判失败，728–735 对各持续法术逐回合按强度十分之一判定。 |
| M033 | keep | 叙述语气准确 | “or so”被译成并列选择 | 一句修订 | “真正的%s……至少%s自己是这么说的。” | T/chronomancy/timeline-threading.lua:128–142；两个参数依次为姓名和代词，原句表达对自称身份的保留。 |
| M034 | downgrade | 缩放对象清楚 | “伤害”可更精确为比例 | 可选澄清 | 无需修改；可选“分摊比例受法术强度加成”。 | T/chronomancy/timeline-threading.lua:196–210 确实缩放分摊比例；现译前句已给百分比，“伤害受加成”未必被理解为独立固定伤害。 |
| M035 | downgrade | 日志名称一致 | 全称与简称差异 | 不强制统一 | 无需修改。 | X/magical.lua:5028–5040 的日志与描述指向同一 Corpselight；“阴燃鬼火／鬼火”未证明造成技能混认。 |
| M036 | downgrade | 状态因果 | 可进一步写明来源光环 | 无需重复上下文 | 无需修改。 | X/mental.lua:298–313 的效果是降低伤害，现译准确；未写出完整光环名称不改变效果。 |
| M037 | downgrade | 状态因果 | 未重述减速来源 | 不作为必修 | 无需修改。 | X/mental.lua:315–334 使用全局速度减益；现句准确给出效果，状态标题已提供语境。 |
| M038 | keep | 命中条件准确 | 未命中也可能被理解为获得仇恨 | 补“命中”即可 | “每回合命中猎物时获得相应仇恨。”保留原数值。 | X/mental.lua:420–431；C/class/interface/Combat.lua:729–734 仅命中设置标志，C/class/Actor.lua:468–479 消费该标志。 |
| M039 | keep | 判定频率与概率准确 | 与弹药版本相同的机制误读 | 同条局部修订 | “每层使施法失败几率提高10%%，并使每个持续法术每回合有额外1%%几率被关闭；最多叠至50%%和5%%。” | O/egos/mindstars.lua:533–538 调用同一效果；X/physical.lua:2137–2157、C/class/Actor.lua:728–735、5886–5888 证明两种判定不同。 |
| M041 | keep | 抗性类型准确 | “抵抗”未对应伤害抗性 | 局部对齐 | 改为“所有伤害抗性降低”。保留原数值。 | T/corruptions/curses.lua:133–141；X/magical.lua:929–944 修改 `resists.all`，不是状态豁免。 |
| M042 | downgrade | 技能称谓一致 | 邪术被泛称诅咒 | 低优先级用词 | 无需修改；可选将本条名称引用对齐为“支配邪术”。 | T/corruptions/hexes.lua:143–170 指向 `DOMINATION_HEX`；当前机制未改变，“诅咒”作为泛称不证明另一技能被施放。 |
| M043 | downgrade | 武器范围清楚 | “任意类型”可强调，但现句未排除类型 | 不强制补字 | 无需修改；可选“允许你双持任意类型的单手武器”。 | T/corruptions/reaving-combat.lua:26–41、C/class/Actor.lua:4967–4973 放宽单手武器副手限制；现译已说“双持单手武器”，没有额外限定。 |
| M044 | keep | 目标阵营准确 | 触发对象被扩大到友方等目标 | 单词修订 | 相应“目标”改为“敌人”。 | T/corruptions/reaving-combat.lua:52–62 检查 `reactionToward(target)<0`。 |
| M045 | keep | 触发类别准确 | 把近战命中泛化为任意伤害 | 修条件句 | “受到近战攻击命中时……” | T/corruptions/reaving-combat.lua:91–106；C/class/interface/Combat.lua:931–935 仅在近战命中流程调用溅射。 |
| M046 | keep | 伤害类型一致 | 酸性类型旧称遗留 | 局部对齐 | “酸系伤害”改为“酸性伤害”。 | T/corruptions/rot.lua:392–397 使用 `ACID`；冻结伤害类型术语为“酸性”。 |
| M047 | reject | 风味与机制区分 | 无独立伤害类型误述 | 不修同义风味 | 无需修改。 | T/corruptions/shadowflame.lua:75–79 的火焰与暗影数值已正确；“黑暗之炎”是风味称呼，不是新增的伤害类型。 |
| M048 | keep | 资源名称准确 | 法力回复写成魔力回复 | 局部修订 | 日志中的“魔力”改为“法力值”；保留所有 `%s`。 | O/egos/staves.lua:265–269 修改 `mana_regen`，不是 `mag` 属性。 |
| M049 | keep | 属性指称准确 | 魔杖缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | O/egos/wands-powers.lua:43–45 使用 `combatStatScale("mag",…)`。 |
| M050 | keep | 判定频率与概率准确 | 施法失败与持续法术关闭混同 | 修机制句即可 | “每层使施法失败几率提高10%%，并使每个持续法术每回合有额外1%%几率被关闭；最多叠至50%%和5%%。” | O/egos/weapon.lua:705–711；X/physical.lua:2137–2157、C/class/Actor.lua:728–735、5886–5888 与前两种物品使用同一机制。 |
| M051 | keep | 冷却例外准确 | 可误以为固定冷却也缩短 | 补例外即可 | “固定冷却时间的技能不受影响。” | T/corruptions/torment.lua:136–149 明确排除 `fixed_cooldown`。 |
| M055 | defer_to_user | 距离单位策略 | “码／格”跨条不一致 | 不据此发起全局替换 | 当前无需修改；宿主确定单位策略后可将本条“码”改为“格”。 | T/cunning/survival.lua:27–47 使用地图距离；代码不能决定本项目统一采用哪种中文单位。 |
| M056 | keep | 冷却与施放耗时区分 | 错误描述技能节奏 | 局部修订 | “召唤技能的冷却时间延长%d回合。” | X/other.lua:583–596 写入负的 `talent_cd_reduction`；C/class/Actor.lua:6885 将其从冷却长度中减去，结果是延长冷却。 |
| M057 | narrow | 属性与参数顺序准确 | 除魔力错名外，等级与血量阈值错位 | 修本条两处即可 | “魔法”→“魔力”；相应句改为“每%d回合可释放一次等级%d的腐秽呕吐，触发条件为生命值降至%d%%以下。” | X/other.lua:953–960 参数依次为冷却、技能等级、生命阈值；当前译文把后两项交换。不得只修属性后宣称该机制句准确。 |
| M059 | keep | 属性门槛准确 | 准备条件中的属性错名 | 局部修订 | “20魔法”改为“20魔力”。 | T/cunning/traps.lua:1312–1383 的门槛检查魔力属性。 |
| M060 | downgrade | 免疫概率的中文名称 | 无机制方向或数值错误 | 不凭字段名要求改译 | 无需修改。 | X/other.lua:3295–3307 修改 `knockback_immune`，但其值作为概率使用；“击退抗性降低20%”能够表达该效果，不能仅因字段含 immune 判错。 |
| M062 | downgrade | 叙述指代 | “那个地方”与先行词衔接成立 | 不强制润色 | 无需修改。 | O/quest-artifacts.lua:378–383 已交代远处力量之地；当前“那个地方”有明确先行词，不影响转化功能。 |
| M066 | keep | 装备槽位准确 | 诅咒覆盖范围被扩大 | 补部位 | 将相关“护甲”改为“躯干护甲”。 | T/cursed/cursed-aura.lua:59–67 的范围是 `BODY` 与披风，非全部护甲。 |
| M068 | narrow | 风味完整 | 遗漏轻装形象 | 一处短语即可 | “轻装上阵，只带着一柄剑。” | O/world-artifacts-maj-eyal.lua:353 明示 lightly armoured；不据此推导实际装备限制。 |
| M069 | downgrade | 可读性 | 仅段落布局差异 | 不作为必修 | 无需修改。 | T/cursed/cursed-aura.lua:299–300；效果与数值齐全，没有换行改变条件归属的证据。 |
| M070 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | T/cursed/cursed-aura.lua:349；新增换行不改变诅咒效果。 |
| M071 | downgrade | 可读性 | 空行布局不同 | 不作为必修 | 无需修改。 | T/cursed/cursed-form.lua:73–74；机制句仍完整，未见参数或标记损坏。 |
| M072 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | T/cursed/cursed-form.lua:107；分段未改变适用条件。 |
| M073 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | T/cursed/cursed-form.lua:122；信息完整，未证明显示故障。 |
| M074 | downgrade | 可读性 | 额外换行 | 不作为必修 | 无需修改。 | T/cursed/dark-figure.lua:143；当前各机制仍可顺序阅读。 |
| M075 | downgrade | 可读性 | 段落数量不同 | 不作为必修 | 无需修改。 | T/cursed/endless-hunt.lua:84–88；没有由换行引起条件或效果遗漏。 |
| M076 | downgrade | 可读性 | 空行与列表布局不同 | 不作为必修 | 无需修改。 | T/cursed/fears.lua:188–197；条目边界仍可辨认，无已证实运行影响。 |
| M079 | keep | 击退成功条件 | 把有条件成功写成必然 | 补概率语气 | 将“被击退”改为“可能被弹开”。 | T/cursed/slaughter.lua:193–218 还受体型、命中／豁免、击退免疫及可用位置影响。 |
| M080 | keep | 属性指称准确 | 护盾缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | O/world-artifacts-maj-eyal.lua:883–888 读取 `getMag()`。 |
| M082 | keep | 选取目标准确 | 可误解为最近任意生物 | 补敌对限定 | “最近的敌人”。 | T/cursed/primal-magic.lua:48–58 只选择敌对目标。 |
| M083 | keep | 普通攻击与突袭关系 | 漏掉未触发突袭时仍会攻击 | 修一处句段 | “敌对目标会受到阴影攻击，并有%d%%几率遭到闪电突袭。” | T/cursed/shadows.lua:634–645 先设置集中目标，再独立判定突袭；并非概率失败便不攻击。 |
| M085 | downgrade | 可读性 | 换行布局不同 | 不作为必修 | 无需修改。 | T/cursed/punishments.lua:304–306；作用与数值均保留，未见条件错接。 |
| M086 | downgrade | 可读性 | 段落分隔不同 | 不作为必修 | 无需修改。 | T/cursed/shadows.lua:468–469；差异仅布局。 |
| M087 | downgrade | 可读性 | 风味段落布局不同 | 不作为必修 | 无需修改。 | O/world-artifacts.lua:412–413；无内容、参数或功能差异。 |
| M091 | keep | 武器适用范围 | 错误限定只能用匕首 | 去除多余限定 | 将相应“匕首”改为“副手武器”，或直接写“额外招架”。 | X/physical.lua:3767–3777；T/techniques/duelist.lua:39–49 检查双持及招架条件，未限制匕首。 |
| M092 | downgrade | 可读性 | 换行布局不同 | 不作为必修 | 无需修改。 | T/cursed/strife.lua:102–104；作用条件与数值未因换行改变。 |
| M093 | downgrade | 可读性 | 空行不同 | 不作为必修 | 无需修改。 | T/cursed/strife.lua:276–277；未证明可见缺陷。 |
| M094 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/cursed/strife.lua:420–422；机制完整，不需要逐字复制英文排版。 |
| M095 | narrow | 参数顺序优先于排版 | 半径与武器伤害数值交换 | 只修同句参数归属 | “造成%d%%寒冷武器伤害，覆盖前方半径%d的锥形范围，并有一定几率冻结目标。” | T/gifts/cold-drake.lua:71–75 的参数为伤害百分比、半径；当前译文先放半径。排版主张降级，但本句存在客观数值错位。 |
| M096 | downgrade | 可读性 | 换行布局不同 | 不作为必修 | 无需修改。 | T/gifts/fire-drake.lua:78–82；内容、数值与作用范围仍完整。 |
| M097 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/gifts/fungus.lua:101–104；没有参数或条件损失。 |
| M098 | narrow | 风味完整 | 比喻强度略被削弱 | 一句局部润色 | “它能像最锋利的剑一样劈开护甲，又能像沉重的棍棒一样造成重击。” | O/world-artifacts.lua:2024–2025 明示最锋利的剑和重棍；不涉及武器分类或数值。 |
| M099 | keep | 已冻结职业指称 | 腐化者被写成堕落者 | 局部对齐 | “兽人堕落者”改为“兽人腐化者”。 | O/world-artifacts.lua:2316 使用 corruptors；冻结职业记录为 Corruptor＝腐化者，无需另立术语策略。 |
| M100 | keep | 技能失败与普通行动区分 | 可误以为移动和普通攻击也失败 | 缩小作用范围 | “剧毒使目标使用非瞬发技能时有%d%%几率失败；普通攻击和移动不受影响。” | T/gifts/higher-draconic.lua:140–144；X/physical.lua:300–325 添加 `talent_fail_chance`；C/class/Actor.lua:5965–5976 排除 innate、无能量技能等，不是所有行动失败。 |
| M102 | keep | 属性指称准确 | 装备缩放属性错名 | 局部修订 | 属性处“魔法”改为“魔力”。 | O/world-artifacts.lua:3114–3135 读取 `getMag()` 与敏捷，非魔法类别。 |
| M103 | keep | 触发条件准确 | 可误以为立即获得抗性 | 补受到伤害条件 | “受到%s伤害时，相应抗性提高%d，持续5回合。” | X/physical.lua:4112–4135 的伤害回调在对应伤害到来时施加共鸣抗性；并非挂上待触发状态便已有抗性。 |
| M104 | keep | 抗性与增伤区分 | 错把降抗当作固定比例增伤 | 修效果名称 | “所有伤害抗性降低%d%%。” | X/physical.lua:3931–3945 修改 `resists.all`；C/data/damage_types.lua:352–373 的抗性结算说明其最终增伤并非固定比例。 |
| M105 | downgrade | 浮动提示可辨认 | “贯通”可能较含糊 | 可选统一名称 | 无需强制修改；可选“+护甲刺穿！”。 | X/physical.lua:3932–3942 显示的是目标获得减益的短提示；没有数值声称攻击方穿甲提高。 |
| M106 | narrow | 参数顺序准确 | 爆发伤害与半径交换 | 修同句即可 | “此外，无论此次攻击是否命中，都会造成%0.2f点同类型伤害，波及半径%d内的生物。” | T/gifts/higher-draconic.lua:98–103 的顺序为武器百分比、爆发伤害、半径、速度；当前第二、第三项反置。单纯换行不必修。 |
| M107 | downgrade | 可读性 | 段落不同 | 不作为必修 | 无需修改。 | T/gifts/mucus.lua:259–264；信息与格式参数仍完整。 |
| M109 | keep | 伤害类型一致 | 寒冷类型旧称 | 局部对齐 | “冰冷伤害”改为“寒冷伤害”。 | T/gifts/summon-distance.lua:333–338 使用 `COLD`，冻结类型名为寒冷。 |
| M110 | keep | 属性指称准确 | 爆发缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | O/world-artifacts.lua:4762–4767 的计算使用 `getMag()`。 |
| M111 | keep | 属性指称准确 | 隐形强度缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | O/world-artifacts.lua:5320–5328 使用灵巧与魔力属性。 |
| M112 | narrow | 外观信息完整 | 苔藓覆盖例外与黏液质感遗漏 | 局部风味修订 | “除正面的木雕眼睛外，帽子上长满了苔藓；浓稠的绿色黏液从眼角缓缓流下。” | O/world-artifacts.lua:5557 明示例外与稠度；只确认外观信息，不提高为机制问题。 |
| M114 | reject | 风味比喻可成立 | 无已证实错误 | 不以属性数值否定比喻 | 无需修改。 | O/world-artifacts.lua:5624–5636 的 rejuvenating properties 可以表达恢复青春／活力；实际回复属性不能反证风味比喻。 |
| M115 | downgrade | 可读性与信息完整 | 上限句换位置 | 不作为必修 | 无需修改。 | T/gifts/storm-drake.lua:194–199；上限20的信息仍在，未因排版遗失。 |
| M116 | downgrade | 格式与信息完整 | 字面百分号、换行差异 | 不作为运行缺陷 | 无需修改。 | T/gifts/summon-distance.lua:619–622；相关 `%%` 是字面百分号，不消耗参数，中文百分比信息仍完整。 |
| M117 | downgrade | 格式与信息完整 | 字面百分号、换行差异 | 不作为必修 | 无需修改。 | T/gifts/summon-distance.lua:735–738；没有因此发生参数错位或继承比例丢失。 |
| M118 | downgrade | 格式与信息完整 | 百分比表达形式不同 | 不作为必修 | 无需修改。 | T/gifts/summon-distance.lua:898–901；字面百分号不是数值参数，现译保留比例含义。 |
| M119 | downgrade | 格式与信息完整 | 换行及百分比形式不同 | 不作为必修 | 无需修改。 | T/gifts/summon-melee.lua:177–180；属性继承说明完整，无参数消耗变化。 |
| M120 | downgrade | 字面字符与参数区分 | 无已证实运行影响 | 不因字符计数强制改写 | 无需修改。 | T/gifts/summon-distance.lua:491–494；`%%` 仅输出百分号，中文仍表达对应比例，不是格式参数遗漏。 |
| M121 | downgrade | 吸收数量表述 | 可补“部分”，但现句未说全部 | 可选澄清 | 无需修改；可选加入“部分”。 | T/gifts/summon-melee.lua:271–277 实际吸收90%；现句没有“全部吸收”的明确承诺，不能直接判为100%。 |
| M122 | narrow | 移除数量明确 | “一个”可能被误读为三类合计一个 | 加“各”即可 | “各移除1个物理、精神和魔法负面效果。” | T/misc/inscriptions.lua:116–118 分别对三类执行一次移除。保留原治疗量等参数。 |
| M124 | narrow | 属性与参数顺序准确 | 光伤数值与半径交换 | 同条两处修订 | “在%d码范围内召唤一个静止光球，持续15回合，照亮周围区域，每回合造成%d点光系伤害，波及半径%d内的敌人；伤害基于魔力和力量。” | O/world-artifacts.lua:6598–6605 的参数依次为距离、伤害、半径；伤害读取 `getMag()` 和 `getStr()`。 |
| M126 | keep | 风味忠实 | 新增“本我”“秽尸”改变诗意 | 四行局部修订 | `窃取的血肉，\n\t窃取的苦痛，\n\t将其舍弃，\n\t便是重生。` | O/world-artifacts.lua:7293–7296 的 it 承接所夺之物，没有本我或秽尸；两版均保留了这些增义。 |
| M128 | keep | 属性名称 | 初始属性错名 | 单词修订 | 本行“魔法”→“魔力”。 | B/classes/afflicted.lua:55–62 列出 Magic 属性；C/load.lua:185 将其定义为 `mag`。 |
| M129 | keep | 属性名称 | 初始属性错名 | 单词修订 | 本行“魔法”→“魔力”。 | B/classes/afflicted.lua:126–130；Magic 对应 `mag`，不是泛称魔法。 |
| M130 | keep | 属性名称 | 初始属性错名 | 单词修订 | 本行“魔法”→“魔力”。 | B/classes/celestial.lua:67–74；与其他五项主属性并列。 |
| M131 | downgrade | 格式与信息完整 | 百分号及换行形式不同 | 不作为必修 | 无需修改。 | T/gifts/summon-melee.lua:298–301；字面百分比含义完整，不涉及参数替换次序。 |
| M132 | downgrade | 格式与信息完整 | 字面百分比、排版差异 | 不作为必修 | 无需修改。 | T/gifts/summon-melee.lua:413–416；无数值或继承项目遗漏。 |
| M133 | downgrade | 格式与信息完整 | 字面百分比、排版差异 | 不作为必修 | 无需修改。 | T/gifts/summon-melee.lua:534–537；百分号本身不消耗格式参数。 |
| M134 | downgrade | 格式与信息完整 | 字面百分比、排版差异 | 不作为必修 | 无需修改。 | T/gifts/summon-utility.lua:209–212；当前中文保留继承比例，未证明运行问题。 |
| M135 | downgrade | 格式与信息完整 | 字面百分比、排版差异 | 不作为必修 | 无需修改。 | T/gifts/summon-utility.lua:323–326；未出现参数归属或信息损失。 |
| M136 | defer_to_user | 冻结候选与固定源码对应 | 不能确认该旧键在目标版本命中 | 先确认键身份 | 当前不修改该旧键；宿主确认实际生效键。若对应新版，需保留“生命值降至0或以下时，加成最多为100%%”。 | T/misc/inscriptions.lua:245–248 的固定源串含上述上限，冻结英文键没有。不能把不同键直接当作单纯布局差异。 |
| M137 | keep | 已冻结状态名称 | 同一状态出现不同正式名称 | 本条对齐即可 | “脱离相位”改为“脱离现实”。 | T/misc/inscriptions.lua:675–686 施加 `EFF_OUT_OF_PHASE`；冻结术语明确该状态采用“脱离现实”，不需新设策略。 |
| M139 | keep | 制作者与受益者区分 | 把为军阀打造写成军阀亲自打造 | 修主宾关系 | “这副手套是为一位想用斯莱特之掌牢牢控制臣民的军阀打造的。” | O/world-artifacts.lua:8174 使用 crafted for，而非 crafted by；当前仍保留主体转换。 |
| M142 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/misc/inscriptions.lua:1145–1146；数值与条件完整，未证明排版故障。 |
| M144 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/celestial.lua:150；C/load.lua:183–188 定义主属性 Magic。 |
| M145 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/chronomancer.lua:70；对应 `STAT_MAG`。 |
| M146 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/chronomancer.lua:159；对应主属性而非魔法类别。 |
| M147 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/corrupted.lua:54；C/load.lua:185 将 Magic 映射为 `mag`。 |
| M148 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/corrupted.lua:124；与力量等属性并列。 |
| M149 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/mage.lua:68；该栏为主属性修正。 |
| M150 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/mage.lua:152；对应 `mag`。 |
| M151 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/psionic.lua:55；主属性修正行。 |
| M152 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/psionic.lua:147；C/load.lua:185 的 Magic 定义适用。 |
| M153 | keep | 伤害与控制区分 | 寒冷伤害被称作冰冻伤害 | 局部修订 | “冰冻伤害”改为“寒冷伤害”。 | T/misc/npcs.lua:573–580 使用 `COLD`；伤害类型不是冰冻控制状态。 |
| M154 | keep | 伤害与控制区分 | 易把寒冷加震慑理解为冰冻 | 局部修订 | 伤害处“冰冻”改为“寒冷”。 | T/misc/npcs.lua:714–721 使用 `COLDSTUN`；C/data/damage_types.lua:1320–1328 造成寒冷伤害并施加震慑，不施加冰封。 |
| M155 | keep | 到达条件准确 | 可误以为冲锋未到达也定身 | 补条件即可 | “到达目标身边后，尝试将其定身5回合。” | T/misc/npcs.lua:1004–1012 在距离达标后检查定身条件，不是无条件施加。 |
| M156 | downgrade | 材料提示清楚 | 指代稍省略 | 不作为必修 | 无需修改；可选“最好找一个戴着贵重鼻环的”。 | C/data/ingredients.lua:96–102 的材料标题提供鼻部语境；“带有圆环”不构成物品类型反转。 |
| M157 | keep | 地理指称准确 | 大陆写成整个世界 | 局部修订 | 改为“马基·埃亚尔”，删除将其泛化为世界的措辞。 | B/classes/rogue.lua:167 指 Maj’Eyal，而非整个 Eyal。 |
| M158 | keep | 护甲限制准确 | 错误排除所有重甲 | 改具体护甲类别 | 相应“重甲”改为“板甲”。 | B/classes/warrior.lua:345；C/class/Actor.lua:5787–5797、C/class/interface/Combat.lua:2691–2697 检查 `massive`，不是 `heavy`。 |
| M159 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/rogue.lua:52；C/load.lua:185 定义 `mag`。 |
| M160 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/rogue.lua:108；该数值为主属性修正。 |
| M161 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/rogue.lua:172；Magic与其他主属性并列。 |
| M162 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/rogue.lua:234；对应 `mag`。 |
| M163 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/warrior.lua:54；C/load.lua:185 的属性定义适用。 |
| M164 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/warrior.lua:192；初始属性栏并非法术强度。 |
| M165 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/warrior.lua:268；对应主属性Magic。 |
| M166 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/warrior.lua:349；对应 `mag`。 |
| M167 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/wilder.lua:57；该行是主属性修正。 |
| M168 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/wilder.lua:119；与意志、灵巧并列。 |
| M169 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/wilder.lua:190；C/load.lua:185 明确定义。 |
| M170 | downgrade | 可读性 | 句中换行略生硬 | 仅润色级别 | 无需修改；可选合并被拆开的句子。 | T/misc/npcs.lua:2348–2349；概率与后续效果仍相连，没有丢失条件或数值。 |
| M171 | downgrade | 可读性 | 段落不同 | 不作为必修 | 无需修改。 | T/misc/npcs.lua:2422–2423；未发现格式参数变化。 |
| M172 | keep | 伤害与抗性类型一致 | 寒冷类型名称不对应 | 局部对齐 | 相关伤害、亲和及抗性名称统一为“寒冷”。 | T/misc/objects.lua:568–571、X/magical.lua:3026–3042 使用 `COLD` 的亲和与抗性，不是独立“冰冻”类型。 |
| M173 | keep | 属性指称准确 | 恩赐缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | T/misc/races.lua:173–182 在魔力与敏捷之间取较高者。 |
| M174 | keep | 伤害类型一致 | 寒冷类型旧称 | 局部对齐 | “冰冷伤害”改为“寒冷伤害”。 | T/misc/npcs.lua:3961–3962 使用 `COLD`。 |
| M175 | downgrade | 可读性 | 持续时间另起一行 | 不作为必修 | 无需修改。 | T/misc/npcs.lua:3746–3747；持续时间仍明确归属该法阵。 |
| M176 | downgrade | 材料名称忠实 | “毒牙”可能增添毒性联想 | 低优先级命名 | 无需强制修改；可选“吸血鬼领主的獠牙”。 | C/data/ingredients.lua:321–327 只写 fang，未明说毒性；但缺少独立反证证明该材料必定无毒，不应提高为机制错误。 |
| M177 | keep | 线索因果准确 | 人为隐藏被译成自然腐朽 | 修一行 | “隧道被毁，只为将它深藏。” | B/races/giant.lua:52–57 的 ruined so it wouldn’t be found 明确给出毁坏目的。 |
| M178 | keep | 已冻结历史事件名 | 专名被泛化为猎魔行动 | 局部对齐 | “猎魔行动”改为“魔法狩猎”。 | B/races/giant.lua:60 使用 Spellhunt；冻结记录明确将其与 Spellblaze 区分。 |
| M180 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/classes/wilder.lua:268；对应 `mag`。 |
| M181 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/construct.lua:54；C/load.lua:185 定义主属性Magic。 |
| M182 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/dwarf.lua:67；主属性修正行。 |
| M183 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/elf.lua:108；对应 `mag`。 |
| M184 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/elf.lua:147；与意志、灵巧并列。 |
| M185 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/giant.lua:65；该值为主属性修正。 |
| M186 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/halfling.lua:106；对应主属性Magic。 |
| M187 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/human.lua:138；C/load.lua:185 的 `mag` 定义适用。 |
| M188 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/human.lua:169；主属性修正行。 |
| M189 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/undead.lua:99；不是魔法伤害或法术强度。 |
| M190 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/undead.lua:194；对应 `mag`。 |
| M191 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | B/races/yeek.lua:148；与其他主属性并列。 |
| M193 | downgrade | 暴击概念清楚 | “致命攻击”有歧义但已被上下文解释 | 可选术语对齐 | 无需强制修改；可选将“致命攻击”改为“暴击”。 | C/class/interface/TooltipsData.lua:276–280 标题是暴击率，正文明确“附带额外伤害”，并未声称必定致死。 |
| M194 | keep | 参数角色准确 | 装备所属角色被写成观看者 | 一句修订 | `#RED#正在展示%s装备组，所属角色：%s（装备未切换）` | C/dialogs/CharacterSheet.lua:74 参数依次为装备组、角色名称；不是向第二个参数所指之人展示。 |
| M196 | downgrade | 速度说明清楚 | 可补例子，但现句成立 | 不增补必修解释 | 无需修改。 | C/class/interface/TooltipsData.lua:281–284 已说明相对正常速度、越高越快；遗漏“同时间更多次”不构成反向描述。 |
| M197 | downgrade | 速度说明清楚 | 首句可润色 | 不作为必修 | 无需修改。 | C/class/interface/TooltipsData.lua:363–366；当前200%对100%的例子已明确相对正常值，足以消除首句歧义。 |
| M203 | downgrade | 可读性 | 句段换行不同 | 不作为必修 | 无需修改；可选合并被拆开的短语。 | T/psionic/dream-forge.lua:279–283；没有由换行引起机制遗漏。 |
| M204 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/psionic/mentalism.lua:225–227；条件、数值与参数齐全。 |
| M205 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/psionic/nightmare.lua:185–188；未见显示截断或条件错接。 |
| M206 | downgrade | 可读性 | 提示分段不同 | 不作为必修 | 无需修改。 | C/dialogs/LevelupDialog.lua:658–659；提示内容与选择含义保留。 |
| M207 | keep | 哲学陈述忠实 | 感知决定存在被改成全知 | 一句修订 | “心灵无法感知之物，便不存在。” | T/psionic/psionic.lua:48 是唯我论的存在论陈述，并非精神力量能感知一切。 |
| M209 | keep | 技能冷却机制准确 | 误以为打断正在施放的技能 | 修动词 | “使主动技能陷入冷却。” | C/data/general/traps/annoy.lua:34–45 从可用主动技能中选取并设置冷却，不执行施法中断。 |
| M211 | downgrade | 可读性 | 换行布局不同 | 不作为必修 | 无需修改。 | T/psionic/psychic-assault.lua:177–179；机制句完整。 |
| M212 | downgrade | 可读性 | 分段与空行不同 | 不作为必修 | 无需修改。 | T/psionic/solipsism.lua:59–63；资源和转化说明未被排版改变。 |
| M213 | keep | 属性名称准确 | 魔力属性错名 | 局部修订 | 属性处“魔法”改为“魔力”。 | A/data/talents/corruptions/demon-seeds.lua:701–711 @555c11932fb3；对应魔力属性缩放，非魔法类别。 |
| M214 | keep | 叠加算法准确 | 可误按层数直接相加亲和 | 补乘法叠加 | “每层提供8%%伤害亲和，按乘法叠加，最多%d层。” | A/data/talents/corruptions/doom-covenant.lua:48–54 @e7f8cb9df054；A/data/timed_effects.lua:803–821 @eb183d02dba8 使用 `100×(1−0.92^层数)`。 |
| M215 | keep | 护盾充能对象准确 | 把增加剩余护盾写成提高上限 | 修效果句 | “伤害护盾、时间护盾、转移护盾：额外补充相当于初始吸收量%d%%的护盾值。” | T/spells/aegis.lua:149–160 调用 `on_aegis`；X/magical.lua:756–757、847–848 及 X/other.lua:415–444 增加当前剩余吸收量，未统一提高所称最大值。 |
| M216 | keep | 持续时间以代码为准 | 持续时间低报一半 | 数字局部修订 | 将诅咒持续“5回合”改为“10回合”。 | A/data/talents/corruptions/doom-shield.lua:173–185 @f1a7dc7a6f11 实际以10回合施加；英文5回合同样与实现冲突。 |
| M217 | downgrade | 翻译缺陷与实现例外分离 | 非燃烧击杀也会耗冷却，但现译未保证每次必触发 | 不把实现细节塞入文本 | 当前无需修改；记录上游冷却时机异常。 | A/data/talents/corruptions/heart-of-fire.lua:31–41 @9169ec6910a9 在检查燃烧前启动冷却。“每5回合一次”的上限表述仍成立，不能直接判成翻译错误。 |
| M218 | keep | 回血触发次数准确 | 错误加入每回合一次限制 | 删除错误限制 | 删除“每回合至多一次”，保留近战命中与回血数值。 | A/data/talents/corruptions/infernal-combat.lua:160–168 @8de1db047d8a；A/data/timed_effects.lua:674–688 @eb183d02dba8 无回合限流；C/class/interface/Combat.lua:643 每次命中都会回调。 |
| M219 | defer_to_user | 触发距离与格式参数准确 | 将维持距离当成触发距离 | 需宿主决定显示参数修正 | 触发句应为“对%d格内的生物造成伤害，且其生命值不高于33%%时……”；须先把首参数改为实际触发距离4，后续维持距离参数保留。 | A/data/talents/corruptions/spellblaze.lua:82–102 @7121480755bd：触发检查距离≤4，说明首参数却使用可变维持半径；仅调换中文无法令原参数同时准确。 |
| M221 | narrow | 状态日志忠实 | 火焰消退被写成不再闪耀 | 用兼容两处的短句 | `#Target#的火焰熄灭了。` | A/data/timed_effects.lua:149–178 @eb183d02dba8 同一源句用于火焰效果；中性“火焰熄灭”兼容身体及武器相关语境。 |
| M222 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/psionic/thought-forms.lua:600–603；参数及效果完整。 |
| M223 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/psionic/thought-forms.lua:621–622；未证明布局造成误读。 |
| M224 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | A/data/talents/corruptions/heart-of-fire.lua:171 @9169ec6910a9；换行未改变效果。 |
| M225 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | A/data/talents/corruptions/infernal-combat.lua:69–71 @8de1db047d8a；数值及条件未损失。 |
| M226 | keep | 随机选取关系 | 可误以为指定或统一施放一种邪术 | 补“各随机” | “立即向最多%d个随机敌人各施放一种随机邪术或诅咒，不消耗时间，也不触发冷却。” | T/spells/dreadmaster.lua:196–207 为每个随机目标分别随机选取 `is_hex` 或 `is_curse` 技能。 |
| M227 | keep | 属性指称准确 | 魔力属性错名 | 局部修订 | “魔法属性”改为“魔力属性”。 | A/data/general/objects/world-artifacts.lua:49–51 @b8a9216d5dbd 使用 `getMag()`。 |
| M228 | keep | 属性名称 | 初始Magic错名 | 单词修订 | “魔法”→“魔力”。 | A/data/birth/corrupted.lua:57–61 @a61a4733cfc0；属性数据对应 `mag`。 |
| M229 | keep | 属性名称 | 初始Magic错名 | 单词修订 | “魔法”→“魔力”。 | A/data/birth/corrupted.lua:121–125 @a61a4733cfc0；与意志、灵巧并列。 |
| M230 | keep | 属性名称 | 初始Magic错名 | 单词修订 | “魔法”→“魔力”。 | A/data/birth/doomelf.lua:39–43 @d770eea753fb；对应主属性 `mag`。 |
| M231 | keep | 属性指称准确 | 身体强化属性错名 | 局部修订 | “魔法”改为“魔力”。 | T/spells/enhancement.lua:180–194 使用 `STAT_MAG`。 |
| M233 | keep | 命中条件准确 | 未命中也可能被理解为回复法力 | 补命中条件 | “近战攻击命中时回复相应法力值。”保留原数值。 | T/spells/enhancement.lua:126–150 设置命中回复；C/class/interface/Combat.lua:1020–1023 位于命中分支。 |
| M234 | narrow | 解锁诗指代与条件 | 告发对象、隐藏身份及可能语气偏移 | 保留诗性，不写攻略 | “三者能向它们告发精灵造下的恐怖……让这些生灵噤声，维持你的伪装，届时你或能见证新精灵的诞生……”其余诗行保持。 | A/data/birth/doomelf.lua:27–32 @d770eea753fb；A/data/achievements/all.lua:84–107 @9dac1c92bd16 检查三名特定敌人的击杀，不支持另造“精灵祝福”等条件。 |
| M235 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/arcane.lua:135–138；数值与条件完整。 |
| M236 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/dreadmaster.lua:257–259；未证明布局问题。 |
| M237 | keep | 亲和与暴击减伤准确 | 把确定减免写成概率闪避暴击 | 修两处机制句 | “寒冷伤害亲和提高%d%%，物理抗性提高%d%%；直接暴击的额外伤害降低%d%%（物理、精神、法术）。” | T/spells/frost-alchemy.lua:118–142 设置 `damage_affinity` 与 `ignore_direct_crits`；C/data/damage_types.lua:130–155 确定性削减暴击额外倍率，325–328 计算亲和治疗。 |
| M238 | defer_to_user | 受益主体与上游数值冲突 | 将护盾减伤写成全身减伤；低血加成未实现 | 需分开文本修正与代码决策 | 可先改首句为“寒冬护盾承受的伤害减少%d%%”；第二个占位符的低生命加成需宿主处理上游计算后再定稿。 | T/spells/glacial-waste.lua:101–140 仅处理护盾承伤；238–242 的显示乘1.33，但实际减伤路径未应用该提升。不能给第二个 `%d` 编造真实效果。 |
| M239 | narrow | 普通修饰语忠实 | 把 eldritch 变成疑似专名 | 一处风味修订 | “你的傀儡皮肤闪烁着诡异的能量。” | T/spells/golem.lua:337–340 的 eldritch 修饰 energies，未指某个名为艾尔德里奇的实体；反伤机制无需改动。 |
| M240 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/fire.lua:134–135；效果与参数未改变。 |
| M241 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/golem.lua:508–509；没有内容丢失。 |
| M242 | narrow | 控制状态与风味区分 | “被混乱”易被理解为实际混乱状态 | 只消除状态误指 | “你与傀儡交换位置；原本攻击你的敌人有%d%%几率转而攻击傀儡。” | T/spells/golemancy.lua:496–500 只改变目标，没有施加混乱效果。排版本身降级；英文 confused 在此是风味表述。 |
| M243 | keep | 伤害类型一致 | 寒冷类型旧称 | 局部对齐 | “冰冷伤害”改为“寒冷伤害”。 | T/spells/ice.lua:69–98 使用 `COLDNEVERMOVE`；C/data/damage_types.lua:1437–1447 转发寒冷伤害并另行定身。 |
| M244 | keep | 已冻结技能名称 | 引用的技能无法与实际技能名对应 | 局部对齐 | “精神光束”改为“心灵灼烧”。 | U/data/talents/demented/controlled-horrors.lua:225–267 @a123514fa090 赋予 `T_MIND_SEAR`；冻结术语明确 Mind Sear＝心灵灼烧。 |
| M245 | keep | 豁免类别名称 | 法术豁免被称作魔法豁免 | 局部对齐 | “魔法豁免”改为“法术豁免”。 | U/data/talents/demented/controlled-horrors.lua:290–298 @a123514fa090 读取 `combatSpellResist()`。 |
| M246 | defer_to_user | 距离单位策略 | “码／格”不一致 | 不自动扩大统一范围 | 当前无需修改；按宿主既定单位策略处理。 | U/data/talents/demented/controlled-horrors.lua:319–323 @a123514fa090 使用地图距离；无数值或范围本身错误。 |
| M247 | narrow | 技能类别与触发条件 | 虚空／彼世混指，且省略战斗和每回合限制 | 修本条必要条件 | “战斗中施放非瞬发疯狂法术时，每回合最多产生一朵彼世火花”；“下一次虚空法术”→“下一次彼世法术”；“魔法属性”→“魔力属性”。 | U/data/talents/demented/nether.lua:299–323 @4ee9687b048c 检查 `in_combat` 与回合标志，强化对象为 Nether 树；排版无需强制恢复。 |
| M248 | keep | 属性指称准确 | 魔力属性错名 | 局部修订 | 属性处“魔法”改为“魔力”。 | U/data/talents/demented/oblivion.lua:79–83 @3242012a234a 对主属性增益使用魔力。 |
| M249 | downgrade | 速度范围清楚 | “整体”与“全局”同义 | 不作为机制错误 | 无需修改；可选“全局速度”。 | U/data/talents/demented/rift.lua:536–542 @23ca78691a34 修改 `global_speed_base`；现译没有缩成移动或攻击速度。 |
| M250 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/doom.lua:372–375 @e68880092dbc；参数及效果完整。 |
| M251 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/madness.lua:62–64 @33e274b4e1f1；无已证实排版误导。 |
| M252 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/nether.lua:72–73 @4ee9687b048c；信息完整。 |
| M253 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/oblivion.lua:297–299 @3242012a234a；未见参数或条件损失。 |
| M254 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/scourge-drake.lua:101–102 @4dfe91fbc940；该布局主张没有可观察缺陷证据。 |
| M255 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | U/data/talents/demented/tentacles.lua:160–165 @038841bc39a9；列表和机制仍完整。 |
| M256 | keep | 范围形状准确 | 圆形范围与锥形范围可能混淆 | 补形状即可 | 将“范围2码的脓液喷射”改为“半径2码的锥形脓液喷射”。 | U/data/talents/demented/path-of-horror.lua:33、64–76 @e688d681d044 使用 `type="cone"`，并在移动前按跳跃方向投射；不是周围圆形爆炸。 |
| M257 | keep | 资源回复频率准确 | 可误以为每次攻击都获得疯狂 | 补每回合限制 | “以异变之手攻击非友方目标时，每回合最多获得一次相应疯狂值。” | U/superload/mod/class/interface/Combat.lua:29–55 @286287389763 使用 `tentacle_insanity_gain` 回合标志；不要求该次攻击命中。 |
| M258 | downgrade | 数量上限表达 | “最多”可更严谨 | 不作为必修 | 无需修改；可选在数量前加“最多”。 | T/spells/meta.lua:100–113 在候选耗尽时退出；技能说明给出可移除数量通常已表达容量，末尾换行不影响含义。 |
| M259 | narrow | 豁免类别准确 | 法术豁免错名 | 只改单词 | “魔法豁免”改为“法术豁免”。 | T/spells/rime-wraith.lua:120–126、X/magical.lua:5307–5334 修改 `combat_spellresist`；C/class/Actor.lua:6885–6887 支持当前冷却长度说明，无需另改成冷却流逝减慢。 |
| M260 | downgrade | 速度范围清楚 | 整体／全局同义 | 不作为必修 | 无需修改；可选“全局速度”。 | U/data/talents/misc/misc.lua:249–258 @3b37fe925ecb 对应全局速度效果，未被译成单项速度。 |
| M261 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | U/data/talents/misc/misc.lua:301–304 @3b37fe925ecb；攻击说明和参数完整。 |
| M262 | keep | 属性指称准确 | 伤害缩放属性错名 | 局部修订 | “魔法”改为“魔力”。 | U/data/talents/misc/races.lua:55–77 @59b9b67cb0a3 使用魔力属性计算伤害。 |
| M263 | keep | 地点与组织区分 | 制造者被写成地点 | 局部对齐 | “伊格”改为“伊格兰斯”。 | U/data/talents/misc/races.lua:358–361 @59b9b67cb0a3 使用 Ziguranth，指反魔教团；冻结术语区分该组织与 Zigur 地点。 |
| M264 | defer_to_user | 实现与显示参数冲突 | 显示概率未参与实际处决判定 | 需宿主处理上游接口 | 可先把属性“魔法”改为“魔力”；处决句应表达“咬中后，若目标生命值不高于20%%且可被即死，则将其杀死”，但需同步移除／调整无效概率参数，不能直接替换原模板。 | U/data/talents/misc/races.lua:385–411 @59b9b67cb0a3 没有概率掷骰；显示的 `getChance()` 仅用于说明，不能保留为真实处决概率。 |
| M265 | downgrade | 速度范围清楚 | 整体／全局同义 | 不作为必修 | 无需修改；可选“全局速度”。 | U/data/talents/misc/races.lua:424–429 @59b9b67cb0a3 修改全局速度；当前未缩小作用类别。 |
| M266 | keep | 抗性类型一致 | 暗影类型旧称 | 局部对齐 | “黑暗抗性”改为“暗影抗性”。 | U/data/talents/misc/races.lua:441–453 @59b9b67cb0a3 使用 `DARKNESS` 抗性。 |
| M267 | narrow | 状态结束日志 | “被消耗”指代不明 | 短句修订 | `#Target#不再衰竭。` | U/data/timed_effects.lua:794–802 @0d3139ebf8a4 的 wasting away 描述目标衰竭，不是某个可消耗物品被使用。 |
| M269 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/stone.lua:128–132；数值与条件完整。 |
| M270 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/spells/temporal.lua:112–114；未证明布局损害语义。 |
| M271 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/2hweapon.lua:102–104；机制完整。 |
| M272 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/2hweapon.lua:204–206；格式参数仍对应原效果。 |
| M274 | narrow | 实际承伤类型 | “冰系”可被误当独立抗性类别 | 只改伤害类型词 | 伤害处改为“寒冷伤害”；冻结几率说明保持。 | T/spells/water.lua:45–67 使用 `ICE`；C/data/damage_types.lua:1357–1370 实际转发 `COLD`，再独立判定冰冻。不能把两部分合成独立冰系抗性。 |
| M275 | keep | 伤害类型一致 | 寒冷类型未按冻结名称 | 局部对齐 | “冰系伤害”改为“寒冷伤害”。 | T/spells/water.lua:92–112 的冰雾投射最终造成寒冷伤害；不是另一伤害抗性类别。 |
| M276 | keep | 伤害类型一致 | 寒冷类型旧称 | 局部对齐 | 伤害处“冰系”改为“寒冷”。 | T/spells/water.lua:228–252 的冰风暴使用寒冷伤害体系，冻结控制另行处理。 |
| M277 | defer_to_user | 首次施加与叠加行为冲突 | 首层实际降豁免／闪避，叠加后转为增加 | 上游实现问题，不能一词修好 | 当前不把“提高”统一改成“降低”；宿主决定修复上游首次施加符号，或提供随实际状态变化的说明。 | U/data/timed_effects.lua:1628–1634、1645–1652 @0d3139ebf8a4：`activate` 对豁免／闪避取负，`on_merge` 取正；静态单方向译文无法覆盖两种状态。 |
| M278 | reject | 可达状态与证据充分性 | 未证明高层说明会显示首次施加的负值 | 不将推测列为必修 | 无需修改此高层说明；首次施加缺陷由M277处理。 | U/data/timed_effects.lua:1601、1628–1640 @0d3139ebf8a4：该句仅在层数>6时出现，正常叠加已经使用正值。补查 U/data/talents/demented/calamity.lua:46–56 @7a65b4d2d7a9 每次施加1层，未证明首次直接7层的正常路径。 |
| M279 | keep | 致死伤害与必死结果区分 | 错误保证另一目标死亡 | 修触发及结果句 | “受到致命伤害时，将这次伤害转移给所选目标。”保留当前已正确的层数治疗优先关系。 | U/data/timed_effects.lua:1705–1760 @0d3139ebf8a4 投射伤害而非调用必死；C/data/damage_types.lua:2864–2869 将VOID分成时空／暗影伤害，不能保证受害者死亡。 |
| M280 | downgrade | 名称与属性说明区分 | 标题“力量”可能有联想 | 不凭标题推断属性承诺 | 无需修改；可选“扭曲进化：威力”。 | U/data/timed_effects.lua:2246–2258 @0d3139ebf8a4 实际增加伤害，标题 Power 可译为一般力量；描述未声称增加STR。 |
| M283 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/acrobatics.lua:270–271；内容完整。 |
| M284 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/archery.lua:266–268；没有格式参数丢失。 |
| M285 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/battle-tactics.lua:94–95；未改变触发条件。 |
| M286 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/bloodthirst.lua:47–49；机制和数值齐全。 |
| M287 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/bloodthirst.lua:72–73；无已证实可见缺陷。 |
| M288 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/bloodthirst.lua:122–124；条件归属未改变。 |
| M289 | downgrade | 可读性 | 额外换行 | 不作为必修 | 无需修改。 | T/techniques/buckler-training.lua:167；单段拆分没有改变效果。 |
| M290 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | U/data/birth/demented.lua:79–87 @22fa8c409878；对应 `mag` 属性。 |
| M291 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | U/data/birth/demented.lua:140–149 @22fa8c409878；主属性修正行。 |
| M292 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | U/data/birth/drem.lua:33–37 @a42cea275f0a；属性数据对应 `mag`。 |
| M293 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | U/data/birth/krog.lua:33–38 @5c802aa76867；Magic与其他主属性并列。 |
| M294 | reject | 继承问题身份与命名含义 | 未证明省略“能量”造成误指 | 不造必修名称问题 | 无需修改。 | U/data/damage_types.lua:215–230 @6ec5f1659e60；“反熵”仍指同一类型，且官方为“反熵能量”、当前才缩短，不能声称该省略是官方遗留缺陷。 |
| M295 | keep | 充能公式与爆炸位置 | 把递增写成不断乘0.33，并暗示终点爆炸 | 修两处机制句 | “传送后在原位置引发爆炸”；“基础伤害为%0.2f；首层充能提高33%%，之后每层新增的增幅比前一层减少33%%。” | R/data/talents/psionic/psionic-fog.lua:84–109 @6bda2c01ed42 使用 `2−0.67^层数`，在 `ox,oy` 投射；不是逐层衰减总伤害。 |
| M296 | keep | 充能回复公式 | 回复随层数增加被译成减少 | 修倍率句 | “首层充能使回复量提高33%%，之后每层新增的增幅比前一层减少33%%。” | R/data/talents/psionic/psionic-fog.lua:125–140 @6bda2c01ed42 对蒸汽及治疗均乘 `2−0.67^层数`。 |
| M297 | narrow | 以实际伤害为准 | 原主张偏重“免费”，但固定百分比确实错误 | 修数字；可顺带明确时序 | “到达时立即进行一次不额外耗时的近战攻击，造成130%武器伤害。” | R/data/talents/misc/objects.lua:155–188 @da286e18579a 实际攻击倍率为1.3，非英文与当前译文的180%；附带攻击在同一行动中执行。 |
| M298 | defer_to_user | 参数顺序与显示公式 | 伤害／半径错位，减速显示也不符实际 | 需宿主处理上游参数 | 首句可改为“造成%0.2f点光系伤害和%0.2f点暗影伤害，波及半径%d的范围”；两项减速百分比须先修正传入值，再保留原占位符描述。 | R/data/talents/celestial/energies.lua:190–219 @2439377daeeb 参数为光伤、暗伤、半径；R/data/damage_types.lua:116–130 @19256d267343 的减速未按说明参数所用能量占比缩放。 |
| M299 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/combat-training.lua:106–111；内容和数值完整。 |
| M300 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/conditioning.lua:91–94；未见条件错接。 |
| M301 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/dualweapon.lua:258–259；参数含义未被排版改变。 |
| M302 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/excellence.lua:177–178；无信息缺失。 |
| M303 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/finishing-moves.lua:195–196；机制句完整。 |
| M304 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/finishing-moves.lua:262–264；无参数或条件损失。 |
| M305 | narrow | 属性准确；排版适度 | 魔力错名成立 | 只改单词 | “魔法”改为“魔力”；不强制改分段。 | T/techniques/magical-combat.lua:241–248 的计算使用 `getMag()`；段落差异没有独立影响证据。 |
| M306 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | R/data/talents/steam/artillery.lua:180–182 @ac57d7e21377；内容完整。 |
| M308 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | R/data/talents/steam/heavy-weapons.lua:72–80 @0b4f50fb9226；技能列表与数值保留。 |
| M309 | defer_to_user | 实际与显示倍率冲突 | 徒手伤害显示错误 | 上游显示计算需处理 | 保留现有句式与占位符；宿主先把徒手倍率参数从“基础倍率×1.25”改为“基础倍率+1.25”的对应百分数。 | T/techniques/dualweapon.lua:187–208 实际攻击为加1.25，说明参数却乘1.25；单改中文无法把第二个 `%d` 变成正确伤害。 |
| M310 | keep | 命中范围准确 | 漏掉路径两侧1格目标 | 补范围 | “攻击路径及其周围1格内的所有敌人。” | T/techniques/dualweapon.lua:426–454 对路径沿途使用半径1范围选取目标，非仅直线路径格。 |
| M311 | keep | 招架与格挡区分 | 招架引用不统一 | 局部对齐 | 将该机制的“抵挡”改为“招架”。 | T/techniques/duelist.lua:61–75 施加 `EFF_PARRY`，按副手武器处理；不是盾牌格挡技能。 |
| M312 | keep | 招架引用一致 | 节奏条件不易与招架对应 | 局部对齐 | 将相应“抵挡”改为“招架”。 | T/techniques/duelist.lua:79–118 定义 Tempo 的防御触发及收益；其 parry 引用应与同树招架一致，不扩展为盾牌格挡。 |
| M313 | downgrade | 耗时说明 | “额外回合”略冗余 | 不作为必修 | 无需修改。 | T/techniques/conditioning.lua:156–168 设置 `no_energy=true`；“不会消耗额外回合”在激活语境下没有明确承诺错误耗时。 |
| M314 | keep | 每回合触发与终止条件 | 高估连击叠层，并误述后续命中终止条件 | 修两句 | “每回合首次命中指定目标时，链锯伤害加成提高%d%%；若该回合首次命中其他敌人，效果结束。” | R/data/talents/steam/automated-butchery.lua:23–52 @a429d63fbf7d；R/data/timed_effects/physical.lua:417–435 @d33320991489 先检查回合标志，再比较目标；同回合后续命中不会再次叠层或触发该终止分支。 |
| M316 | keep | 独立概率判定 | 误以为合并成一个整体概率 | 修概率句 | “惩戒命中后，目标每有一个效果，就独立有%d%%几率使其冷却减少1回合。” | R/data/talents/steam/battlefield-management.lua:166–172 @2799a7df70a5 对效果逐个掷骰并分别减少冷却。 |
| M317 | downgrade | 名称一致性 | 喷火器／火焰喷射器同义 | 不作为机制错误 | 无需修改；可选按技能正式名称对齐。 | R/data/talents/steam/heavy-weapons.lua:783–788 @0b4f50fb9226 指同一装置，未证明“喷火器”误指其他装备。 |
| M318 | defer_to_user | 高复用武器命名 | 榴弹／手榴弹跨条策略 | 由宿主统一 | 当前不自动修改；宿主若采用发射器语境的“榴弹”，仅对本条相应称呼对齐。 | R/data/talents/steam/demolition.lua:120–145 @66e61a2898f5 使用榴弹发射器技能；是否全局统一名称不由此条自动授权。 |
| M319 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/pugilism.lua:260–261；数值与条件完整。 |
| M321 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/strength-of-the-berserker.lua:138–141；未见显示或参数故障。 |
| M322 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/superiority.lua:130–131；信息完整。 |
| M325 | keep | 递减比例准确 | 每个额外目标的蒸汽收益高报 | 修一个比例 | “每多一名受害者，新增蒸汽回复量减少70%%。” | R/data/timed_effects/physical.lua:754–758 @d33320991489 使用 `steam×0.3^nb`；R/data/talents/steam/mechstar.lua:93–99 @e6e5f57a088f 的66%说明也不符实现。 |
| M326 | keep | 距离边界准确 | 相等边界被误写成仍有效 | 单词修订 | “距离达到金属灵晶半径的两倍（当前为%d）时，效果便会终止。” | R/data/talents/steam/mechstar.lua:64–81 @e6e5f57a088f；R/data/timed_effects/physical.lua:742–751 @d33320991489 使用 `>=`，不是 `>`。 |
| M327 | defer_to_user | 上游参数传递正确性 | 显示速度增益未实际生效 | 不能靠译文掩盖实现缺陷 | 当前不改成另一个动态承诺；宿主先决定修正速度效果的 `power` 参数，随后沿用“全局速度提高%d%%，持续2回合”。 | R/data/talents/steam/mecharachnid.lua:197–205 @d4a229c03317 把速度放在匿名数组项；E/engine/interface/ActorTemporaryEffects.lua:124–128 与 X/physical.lua:605–616 因缺 `power` 使用默认0.1。 |
| M329 | downgrade | 可读性 | 分段／缩进不同 | 不作为必修 | 无需修改。 | T/techniques/unarmed-discipline.lua:102–105；等级条件、颜色标记及连击点说明保留。 |
| M330 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | T/techniques/unarmed-training.lua:111；速度与取消条件仍清楚。 |
| M331 | downgrade | 可读性 | 单段拆分 | 不作为必修 | 无需修改。 | T/techniques/weaponshield.lua:135；额外格挡的冷却说明未丢失。 |
| M332 | downgrade | 可读性 | 分段／缩进不同 | 不作为必修 | 无需修改。 | T/techniques/weaponshield.lua:284–287；范围、击退、眩晕及刷新条件仍有对应文字。 |
| M333 | downgrade | 共享条件表达 | 第二句未重复相邻敌人条件 | 不强制重复条件 | 无需修改；可选“在此条件下，技能等级达到3时还获得等量生命回复”。 | T/techniques/tireless-combatant.lua:36–70 的生命回复嵌套于同一条件；现译“这个技能带给”自然承接前句，没有明确无条件回复承诺。 |
| M334 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/techniques/weaponshield.lua:361–364；负生命阈值、结束处理及缩放说明完整。 |
| M335 | narrow | 伤害标签准确 | 暗影标签旧称成立 | 只改类型标签 | `#GREY#黑暗`改为`#GREY#暗影`，保留标记；不强制改排版。 | T/uber/cun.lua:192–204 的 Darkness 对应暗影类型；空行和列表布局本身没有独立故障证据。 |
| M336 | downgrade | 可读性 | 分段不同 | 不作为必修 | 无需修改。 | T/uber/mag.lua:65–66；伤害减免、穿透、恢复时机与闪避加成仍完整。 |
| M337 | downgrade | 可读性 | 空行与列表缩进不同 | 不作为必修 | 无需修改。 | T/uber/mag.lua:124–131；技能列表仍由 `%s` 插入，没有因此丢失技能。 |
| M338 | narrow | 具体技能指称准确 | 把重力牵引写成另一异常技能 | 只改技能名 | 将“异常重力井”改为“异常：重力牵引”；排版不作必修。 | X/magical.lua:2912–2916 赋予 `T_ANOMALY_GRAVITY_PULL`；T/chronomancy/anomalies.lua:1029 定义该技能，1264 另有 Gravity Well，两者不是同一技能。 |
| M339 | keep | 伤害类型一致 | 寒冷类型旧称 | 局部对齐 | “冰冷”改为“寒冷”。 | T/uber/cun.lua:250 及后续伤害统计检查使用 `DamageType.COLD`。 |
| M340 | keep | 属性系数准确 | 魔力系数被泛称魔法加成 | 局部修订 | “额外获得50%%魔力属性系数”。 | T/uber/mag.lua:140–144；C/class/interface/Combat.lua:1675–1680 向武器 `dammod.mag` 加0.5，不是笼统魔法增伤。 |
| M341 | downgrade | 同一物体指称 | 链锯／飞锯名称不统一 | 可选日志对齐 | 无需强制修改；可选“嵌在#Target#身上的锯刃飞回了原处”。 | R/data/timed_effects/physical.lua:445–473 @d33320991489 指向同一自动锯刃；当前返回方向没有颠倒，名称差异不足以证明机制误读。 |
| M342 | downgrade | 同一物体指称 | 链锯／飞锯名称不统一 | 可选日志对齐 | 无需强制修改；可选“锯刃将#Source#拖向#Target#！”。 | R/data/timed_effects/physical.lua:469–470 @d33320991489 的日志参数与拉拽方向对应；当前保留了正确源、目标标记。 |
| M343 | downgrade | 速度范围清楚 | 整体／全局同义 | 不作为机制错误 | 无需修改；可选“全局速度”。 | R/data/timed_effects/physical.lua:807–825 @d33320991489 修改 `global_speed_add`；现译未写成单项速度。 |
| M344 | downgrade | 驱散术语一致 | “解除”较泛，但上下文完整 | 可选对齐 | 无需强制修改；可选将相关“解除”统一为“驱散”。 | T/uber/mag.lua:78–85 使用 `callbackOnDispel`；现译保留防护、6回合及终止持续技能的关系，没有改变机制。 |
| M346 | downgrade | 可读性 | 换行／空白差异 | 不作为必修 | 无需修改。 | T/uber/str.lua:217–218；疲劳、负重、力量及体型数值齐全。 |
| M347 | downgrade | 可读性 | 空行与缩进不同 | 不作为必修 | 无需修改。 | T/uber/wil.lua:390–410；技能树交换、遗忘及资源转换说明完整，未见因布局遗漏项目。 |
| M348 | keep | 抗性类型一致 | 暗影抗性旧称 | 局部对齐 | “黑暗抗性”改为“暗影抗性”。 | T/uber/mag.lua:416–417 实际增加 `COLD` 与 `DARKNESS` 抗性，467–468 为相应说明。 |
| M352 | keep | 属性指称准确 | 光伤缩放属性错名 | 局部修订 | “灵巧加魔法”改为“灵巧加魔力”。 | R/data/general/objects/world-artifacts.lua:687–696 @4d1225a3e957 使用 `getCun()+getMag()`。 |
| M353 | narrow | 外观结构完整 | 刀刃与弹簧机关的连接关系遗漏 | 一句风味修订 | “这件披风装有一系列连接着弹簧机关的刀刃。” | R/data/general/objects/world-artifacts.lua:925 @4d1225a3e957 明确 attached to various spring mechanisms；只确认结构描述，不推导新增装备机制。 |
| M354 | downgrade | 风味指代 | “附近”的参照可更明确，但原文亦含糊 | 不据此推导武器范围 | 无需强制修改；可选“一把能将近处的一切化为灰烬的枪”。 | R/data/general/objects/world-artifacts.lua:1053 @4d1225a3e957 的 “As long as its nearby” 本身有指代／拼写歧义，不能用一句风味文确定精确距离机制。 |
| M356 | keep | 反击目标准确 | 漏掉攻击者，似可任选突袭目标 | 补对象即可 | “受伤时：对攻击者发动闪电突袭（范围6）。” | R/data/general/objects/world-artifacts.lua:1995–2018 @4d1225a3e957 使用 `force_target=src`。实际还有回合限制及距离分支，但本条最小修订是恢复明确对象。 |
| M357 | defer_to_user | 英文与实现冲突 | 所述5%阈值与代码差百倍，边界也不同 | 由宿主决定上游修复策略 | 不直接按英文保留“5%”；若明确按当前实现描述，应为“若自身每回合流血伤害达到最大生命值的500%，攻击会触发劈击”。 | R/data/general/objects/world-artifacts.lua:2106–2112 @4d1225a3e957 比较 `cut.power/max_life < 5`；R/data/timed_effects/physical.lua:773–802 @d33320991489 的 `power` 是伤害量，非百分数。 |
| M360 | defer_to_user | 物品专名与资源名策略 | 名称“魔力线圈”不等于机制误写 | 不自动重命名物品 | 当前无需修改；宿主若确定重命名为“法力线圈”，再统一名称引用。 | R/data/tinkers/electricity.lua:35–36 @495edeff7292；当前机制已正确写法力回复、法术命中。专名中的“魔力”不能直接等同于属性声明。 |
| M361 | keep | 部分抗性与完全免疫区分 | 低阶装置被说成完全免疫缴械 | 修短语 | “提高抵抗缴械的能力”。 | R/data/general/objects/tinkers/mechanical.lua:85–96 @11ceae3916a5 的 `disarm_immune=0.5+0.1*i`，低阶仅60%–90%；R/data/tinkers/mechanical.lua:79–80 @0d61ef7b7bee 的概述不能一概写完全免疫。 |
| M362 | keep | 目标类型与拉拽方向 | 自身移动被错误限定为击中生物 | 修一句 | “可将生物拉向你，或将你拉向目标空地的特殊弹头。” | R/data/talents/steam/other.lua:1589–1607 @4a12c05410e5：有生物则拉生物，无生物则拉自身；R/data/tinkers/explosive.lua:311–313 @93dec33cd5d2 为该弹头概述。 |
| M363 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/classes/empyreal.lua:29 @b43c98aa7280；+6 Magic为主属性修正。 |
| M364 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/classes/tinker.lua:73 @861b8e9bc8ff；+0 Magic仍是属性栏，不是魔法类别。 |
| M365 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/classes/tinker.lua:133 @861b8e9bc8ff；与意志、灵巧并列。 |
| M366 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/classes/tinker.lua:206 @861b8e9bc8ff；主属性修正行。 |
| M367 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/classes/tinker.lua:285 @861b8e9bc8ff；对应主属性Magic。 |
| M368 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/races/orc.lua:118、122 @ca16dcf53d96；数据明确 `mag=-1`。 |
| M369 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/races/whitehooves.lua:121、125 @cd8b76bbf482；数据明确 `mag=2`。 |
| M370 | keep | 属性名称 | Magic错名 | 单词修订 | “魔法”→“魔力”。 | R/data/birth/races/yeti.lua:107–111 @7b14b94d81ee；该栏仍是Magic主属性。 |
| M371 | narrow | 地理指称准确 | 把大陆写成世界 | 修地点短语 | “曾不止一次危及整个马基·埃亚尔。” | R/data/birth/races/orc.lua:27 @ca16dcf53d96 指 all of Maj’Eyal；官方的世界泛化在当前“马基埃亚尔世界”中仍有残留，问题不只缺间隔号。 |
| M372 | downgrade | 专名拼写一致 | 仅间隔号不一致，地点已正确 | 低优先级对齐 | 无需强制修改；可选“马基·埃亚尔”。 | R/data/birth/races/orc.lua:28 @ca16dcf53d96；当前已指正确大陆，且已修正四个／五个部落关系。不能把缺间隔号提高为范围或机制错误。 |
| M373 | keep | 通用限制与具体物品区分 | 世界传送限制缩成回归之杖限制 | 用通用动作表达 | “在隧道尽头放置炸弹后，你才能使用回城传送！” | R/superload/mod/class/Actor.lua:140–147 @2b332d29bf60 拦截 `canBe("worldport")`，不是检查某一根回归之杖。 |
| M374 | keep | 槽位语义准确 | 备用槽可能是主手，却固定写副手 | 通用槽位描述 | `%s将%s装备到了备用槽位。` | E/engine/interface/ActorInventory.lua:534–543 使用动态 `offslot`；C/class/Actor.lua:4965–4972 的石盾分支会返回 `MAINHAND`，构成“必为副手”的直接反证。 |