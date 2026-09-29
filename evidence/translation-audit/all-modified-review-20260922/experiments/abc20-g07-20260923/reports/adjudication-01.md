完成全部 40 条复核及 69 项匿名观察裁决：**9 条 ISSUE、5 条 PENDING、26 条 OK**；归并为 **13 项确认缺陷、12 项未决疑点**。

下文 `D/` 指本包 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/`，`E/` 指本体固定提交 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。DLC 文件哈希均匹配，但仓库、commit 和目标版本对应关系未固定。确认缺陷以冻结文本、明确适用术语及语境为依据；仅由 DLC 实现差异提出的问题保留为 P。

| entry-ID | 判定 | canonical D或P编号／简短依据 |
|---|---|---|
| entry-03413 | ISSUE | D01；另有 P01、P02、P11 |
| entry-03414 | OK | 召唤空间不足日志准确；术语快照对应另一 source_tag |
| entry-03415 | OK | 选择传送位置的操作提示准确 |
| entry-03416 | ISSUE | D02、D03；另有 P03 |
| entry-03417 | OK | 法强、活力上限及当前活力伤害加成对应 |
| entry-03418 | OK | 近战反击、减伤上限及活力消耗对应消费逻辑 |
| entry-03419 | ISSUE | D04 |
| entry-03420 | OK | “黑暗／暗影”仅一致性建议，existing 不强制改名 |
| entry-03421 | OK | 固定加值与总护甲比例的重排等价 |
| entry-03422 | PENDING | P04 |
| entry-03423 | OK | 对应传送调用返回失败时的日志 |
| entry-03424 | PENDING | P05 |
| entry-03425 | PENDING | P06 |
| entry-03426 | OK | 锥形、持续火焰、力量及法术暴击描述对应 |
| entry-03427 | PENDING | P12，本轮补充 |
| entry-03428 | OK | 对应第一阶段选择源生物 |
| entry-03429 | OK | “受害者／牺牲生物”仅一致性建议 |
| entry-03430 | OK | 完整句未断言源生物减伤；“由……承受”仅消歧建议 |
| entry-03431 | ISSUE | D05、D06；另有 P07 |
| entry-03432 | OK | 死亡后复起的 demonic husk 语境对应 |
| entry-03433 | ISSUE | D07、D08 |
| entry-03434 | OK | 命中、降火抗、结束伤害及伤害累积关系对应 |
| entry-03435 | OK | 冻结日志的装备和移动条件译出 |
| entry-03436 | OK | 参数顺序正确；歼灭挥斩确以射程作锥形半径；角度单位仅建议 |
| entry-03437 | ISSUE | D09、D10 |
| entry-03438 | ISSUE | D11；另有 P08、P09 |
| entry-03439 | OK | 武器附魔对象明确 |
| entry-03440 | ISSUE | D12 |
| entry-03441 | ISSUE | D13；否决统一补成武器的观察 |
| entry-03442 | OK | 受折磨状态日志对应 |
| entry-03443 | OK | soulburn 伤害来源说明对应 |
| entry-03444 | OK | 宿主死亡、施法者及成熟种子概率对应 |
| entry-03445 | OK | 酸性抗性与亲和参数对应；空格仅建议 |
| entry-03446 | OK | 共享痛苦日志对应，保留命名标记大小写 |
| entry-03447 | PENDING | P10 |
| entry-03448 | OK | 数值表示当前叠层；“充能”命名仅建议 |
| entry-03449 | OK | 40% 火焰亲和、−15% 枯萎抗性对应 |
| entry-03450 | OK | 生物死亡后触发饮血者的关系对应 |
| entry-03451 | OK | 效果子类型译为伤害亲和成立；existing 不强制使用“吸收” |
| entry-03452 | OK | 全伤害亲和及数值参数对应 |

确认缺陷如下。这里“翻译新增”表示相对英文新增偏差，不表示本次提交首次引入。

| D-ID | entry-ID | 内容、归因及源码／语境证据 |
|---|---|---|
| D01 | entry-03413 | **漏译宿主的恶魔类型限定，翻译新增。** `unique demons` 变为“史诗生物（Unique）”。后面的“有对应的恶魔种子”是另一个条件，未译出宿主类型。`D/data/talents/corruptions/demonic-pact.lua:364–369` 按 `host.type == "demon"` 分支决定是否按宿主名称匹配种子。 |
| D02 | entry-03416 | **距离上限信息丢失，翻译新增。** `up to %d grids` 变为“%d 码外”；“误差”不能表达可选距离的上限。`D/data/talents/corruptions/demonic-pact.lua:855–875、888–895` 分别消费选点范围和落点散布半径。 |
| D03 | entry-03416 | **随机选择的种子来源集合遗漏，翻译新增。** `from your seeds` 未译出。装备种子是施法前提，不能替代“从这些种子中选择恶魔”的来源信息。`D/data/talents/corruptions/demonic-pact.lua:326–343、851、879–882` 构造穿戴种子列表并从中抽取。 |
| D04 | entry-03419 | **乘算叠加限定遗漏，翻译新增。** `multiplicatively` 未译出。`D/data/timed_effects.lua:805、813–820` 使用 `100 × (1 − 0.92^stacks)`；两层为 15.36%，不是 16%。 |
| D05 | entry-03431 | **回血的近战限定遗漏，翻译新增。** `in melee` 被泛化为“攻击”。`D/data/timed_effects.lua:683–686` 使用 `callbackOnMeleeHit`；`E/game/modules/tome/class/interface/Combat.lua:643` 为近战命中调用点。 |
| D06 | entry-03431 | **回血的伤害条件遗漏，翻译新增。** 原文为 `damage this foe`，译文只要求“攻击”。`D/data/timed_effects.lua:684` 排除空或非正的伤害参数。注意这不是“目标最终必须扣血”：`E/game/modules/tome/class/interface/Combat.lua:627–643` 传入的是近战计算参数，未接收伤害投射器的最终扣血返回值。 |
| D07 | entry-03433 | **惊吓效果的近战限定遗漏，翻译新增。** `melee hits` 变为泛指攻击。`D/data/talents/corruptions/oppression.lua:72–81` 仅通过近战攻击回调施加效果。 |
| D08 | entry-03433 | **成功命中的条件遗漏，翻译新增。** `successful` 未译出，且“每次攻击会刷新”也未保留该条件。`D/data/talents/corruptions/oppression.lua:75` 明确排除 `not hitted`。 |
| D09 | entry-03437 | **指定落点的操作信息遗漏，翻译新增。** `specific location` 未译出。“传送半径”表达距离，却没有表达可指定位置。`D/data/talents/misc/races.lua:55–68` 获取玩家坐标、检查空位后以半径零传送。并不据此认定“半径”必然表示随机。 |
| D10 | entry-03437 | **明确适用的状态名未沿用，翻译新增。** 第二段“停留在相位外 5 回合”明确指向状态，而冻结术语要求 Out of Phase 使用 preferred“脱离现实”、沿用效果定义。`D/data/talents/misc/races.lua:73–77` 设置该效果；`E/game/modules/tome/data/timed_effects/magical.lua:2582–2598` 核实状态身份及加成。缺陷限于明确指称该状态的部分，不强制逐字替换所有叙事性 phase 表述。 |
| D11 | entry-03438 | **重置对象“冷却时间”遗漏，翻译新增。** 原文明确重置两个技能的 `cooldowns`，译文只写重置技能；该句没有其他冷却说明。`D/data/talents/misc/races.lua:133–134` 对两个技能执行 `alterTalentCoolingdown(..., -1000)`。 |
| D12 | entry-03440 | **武器所属对象丢失，翻译新增。** 武器看起来不再危险变为角色“危险度”降低。`D/data/timed_effects.lua:51–52` 为武器附魔的获得／结束日志；`context.lua:466–469` 保留完整成对语境。 |
| D13 | entry-03441 | **火焰燃烧含义丢失，翻译新增。** `blazing` 仅译为“闪耀”。`D/data/timed_effects.lua:156–178` 的两个使用处分别对应武器火焰和包围生物的吞噬火焰，均不是普通发光。英文 `'s` 的缺词／病句来自上游，不能据此统一指定“武器”。 |

69 项匿名观察的逐项裁决如下。状态针对观察中的实质断言；原观察的严重程度或“仅建议”标签不作为证据。

| O-ID | 状态 | 命中D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | refuted | — | “级别”后明确列出普通、精英、稀有等 rank，未变为数值等级；“存活”结合成熟种子语境未引入另一概率。`demonic-pact.lua:665` 先施加种子，`timed_effects.lua:515–518` 才按概率取得成熟种子。 |
| O002 | confirmed | D01 | 恶魔类型限定确实未译出；`demonic-pact.lua:364–369` 支持该区分。 |
| O003 | confirmed | D01 | 与 O002 为同一遗漏，不重复计缺陷。 |
| O004 | confirmed | D01 | 类型分支及文本遗漏成立；不扩大为所有史诗宿主都会实际产出专属种子的断言。 |
| O005 | mixed | — | **refuted**：不能把概率直接认作植入动作失败概率，快照在宿主死亡时抽取；**advisory**：多余空格及更清楚的概率措辞。见 `demonic-pact.lua:665`、`timed_effects.lua:515–518`。 |
| O006 | pending | — | P01；`:655` 确有首次例外，但目标 DLC 版本未固定。 |
| O007 | advisory | — | “此外”另起回复／复活陈述，不能确定其受高等级条件约束；已有种子“提升等级”也已表达更新对象。`:438–467、495–536` 支持更新与治疗分开理解，现有表述可澄清但不确认两项缺陷。 |
| O008 | pending | — | P02；`:467、605、701` 确有点数参数与百分比文本差异；沿袭上游不构成豁免，版本适用性仍缺失。 |
| O009 | advisory | — | 空格不改变参数或句义。 |
| O010 | confirmed | D02 | 最大可选距离没有保留；`:858、864、895` 区分范围和散布。 |
| O011 | confirmed | D02 | 所指出的上限遗漏成立；玩家随后能选点不能补回说明中的距离信息，“仅建议”分档不成立。 |
| O012 | confirmed | D02 | 同一距离上限缺陷；无需把“码外”唯一解释为确定距离才能成立。 |
| O013 | confirmed | D03 | `availableDemonSeed` 的来源集合与施法所需种子条件是不同信息。 |
| O014 | pending | — | P03；`:867–882` 支持回退随机传送，但不能据快照确定目标版本。 |
| O015 | pending | — | P03；观察对源码事实及版本缺口的区分成立。 |
| O016 | confirmed | D02 | 与 O010 为同一上限遗漏。 |
| O017 | confirmed | D03 | `:879` 从穿戴种子列表选择，冻结英文已明确来源。 |
| O018 | pending | — | P03；英文和中文都有描述缺口，不能因来自英文而直接排除。 |
| O019 | confirmed | D04 | `timed_effects.lua:805、817–820` 与冻结英文共同支持乘算限定。 |
| O020 | confirmed | D04 | 同一叠加算法遗漏。 |
| O021 | confirmed | D04 | 层数上限不能替代叠加算法。 |
| O022 | confirmed | D04 | 同一遗漏；不要求证明所有玩家都会误算。 |
| O023 | advisory | — | darkness 记录为 existing，非所声称的强制标准；`timed_effects.lua:853` 只能证明伤害类型。与邻文统一可建议，不能据此确认术语错误。 |
| O024 | advisory | — | “黑暗／暗影”一致性和“开启”的自然程度可改善；上下文已有层数，不足以判为另一机制。 |
| O025 | pending | — | P04；`:185` 的基础赋值 10 成立，最终时长还经过本体效果处理，且 DLC 版本未固定。 |
| O026 | pending | — | P04；对基础时长与豁免后时长的区分成立。 |
| O027 | pending | — | P04；不能把调用参数直接概括成所有目标实际持续 10 回合，也不能豁免上游误述。 |
| O028 | pending | — | P05；`:75` 赋值 4，不能仅按英文 3 判译文错。 |
| O029 | pending | — | P05；效果定义和持续时间接口已核实，目标 DLC 版本对应关系仍缺失。 |
| O030 | pending | — | P05；快照支持译文，但不足以直接结案为目标版本无问题；倒计时函数也不是完整行动时序证明。 |
| O031 | pending | — | P06；`:107` 排除 other 和 cross tier 的事实成立，版本适用性未定。 |
| O032 | pending | — | P06；过滤条件与随后按清除数量计伤害已核实。 |
| O033 | advisory | — | 两种称呼均指第二个选择对象；`infernal-combat.lua:120–128` 未显示对象混淆。 |
| O034 | advisory | — | `timed_effects.lua:715–731` 确为另加伤害；但完整译句先说源生物受到伤害，没有说减去或转移。“由”不足以独立证明排他的伤害分担机制。 |
| O035 | advisory | — | `Actor.lua:3013–3014` 支持回调未扣减原值；文本可消歧，但不能由“由……承受”必然推出源生物减伤。 |
| O036 | advisory | — | 同 O034；不确认其“暗示”已构成另一明确机制承诺。 |
| O037 | mixed | D05、D06 | **confirmed**：近战及伤害条件遗漏；**refuted**：将回调参数解释为最终有效扣血。`Combat.lua:627–643` 没有把投射器最终结果赋回 `dam`。 |
| O038 | advisory | — | `DamageType.DARKNESS` 已核实；术语 existing 不支持“不得译为黑暗”的强制结论。 |
| O039 | mixed | D05、D06 | **confirmed**：近战及正伤害参数条件；**refuted**：把译文必然解释为对“曾被刺穿”目标永久有效。前句已提供刺穿、流血 5 回合的局部语境。 |
| O040 | mixed | D05、D06 | **confirmed**：近战及伤害条件遗漏；**refuted**：最终扣血门槛及必然延伸到流血结束后的说法。见 `timed_effects.lua:683–701`、`Combat.lua:627–643`。 |
| O041 | pending | — | P07；效果回调及本体派发中未见该治疗的每回合限制，目标加载组合未固定。 |
| O042 | advisory | — | 同一段紧接盾击伤害写“额外 50%”，有明确局部参照；`:168` 的基数与此吻合。可表达得更明确，但不因存在理论上的其他读法确认遗漏。 |
| O043 | confirmed | D05 | 仅就近战限定，断言成立。 |
| O044 | pending | — | P07；本地没有 turn_procs 尚需结合调用链，已补核本体派发；最终仍受版本缺口限制。 |
| O045 | confirmed | D07、D08 | `oppression.lua:72–81` 同时限定近战和命中，拆为两个条件缺陷。 |
| O046 | confirmed | D07、D08 | 同上。 |
| O047 | confirmed | D07、D08 | 叠加和刷新均通过同一命中条件，不能写成每次任意攻击。 |
| O048 | confirmed | D07、D08 | 同上。 |
| O049 | advisory | — | 已写“角度增加”，数值及角度语境保留；`wrath.lua:206`、`fearfire.lua:186` 支持角度值。单位补全属建议。 |
| O050 | mixed | D09 | **confirmed**：指定落点信息遗漏；**refuted**：“半径”必然表示随机传送。`:55–68` 证明精确选点，但并不证明中文“半径”自带随机含义。 |
| O051 | confirmed | D09 | 指定坐标、空位检查及零散布已核实。 |
| O052 | confirmed | D09 | 冻结文本未表达 `specific location`。 |
| O053 | mixed | D09 | **confirmed**：指定落点遗漏；**advisory**：避免读者把范围和散布混淆；不另计“随机传送误述”。 |
| O054 | confirmed | D10 | 明确状态段落适用 preferred 效果名要求；已核实 `EFF_OUT_OF_PHASE` 与本体定义。 |
| O055 | advisory | — | All Resists 术语行针对面板标签；“全体抗性”在本句语义等价。 |
| O056 | mixed | D11 | **advisory**：紧接触发伤害的“额外 50%”已有局部基数；**confirmed**：冷却这一重置对象遗漏。两项不合并判建议。 |
| O057 | confirmed | D11 | `races.lua:133–134` 的对象是冷却，冻结译句没有保留该对象。 |
| O058 | pending | — | P08；`timed_effects.lua:1051` 排除 `dead`，版本适用性未定。 |
| O059 | pending | — | P09；`:1051` 使用 `<` 排除，等于阈值可通过；沿袭英文，目标版本未定。 |
| O060 | confirmed | D12 | 武器变成角色整体危险度，成对日志明确。 |
| O061 | confirmed | D12 | 同一所属对象缺陷；不采纳“严重”作为事实依据。 |
| O062 | confirmed | D12 | 文本及武器附魔结束语境直接可证。 |
| O063 | confirmed | D12 | 同上。 |
| O064 | refuted | — | 只考察 RAGING_FLAMES 后要求统一恢复“武器”，遗漏同字符串在 CURSED_FLAMES 的使用。`:177–178` 指生物周围火焰。该错误对象判断不借用 D13。 |
| O065 | confirmed | D13 | 两个使用处都具有明确火焰语义，“闪耀”未保留燃烧含义。 |
| O066 | confirmed | D13 | `-Revel／-Devoured` 及邻近日志不能替代当前句丢失的火焰语义；仅建议分档不成立。 |
| O067 | advisory | — | 空格不对称不改变酸性抗性、亲和或参数。 |
| O068 | pending | — | P10；固定本体确在 `life <= die_at` 进入死亡处理；DLC 显示与设置的目标版本适用性未定。 |
| O069 | advisory | — | `timed_effects.lua:861、866–869` 显示当前层数，白名单 `demon-seeds.lua:773–774` 消耗该层数。“叠加次数”可改得更清楚，但未显示错误数值或机制。 |

未决项单列如下，均未计入 D：

- **P01｜entry-03413｜沿袭上游：首次概率例外。** `D/data/talents/corruptions/demonic-pact.lua:654–667` 在尚无 `used_demon_seed` 时令概率为 100%。更准确地说，这是首次符合相应执行条件、设置该标记前的例外，不能无条件简化为第一次按技能按钮。
- **P02｜entry-03413｜沿袭上游：治疗百分比与点数。** 同文件 `:605、701` 显示的参数为 10–30；`:467` 直接传入 `heal`。`E/game/engines/default/engine/interface/ActorLife.lua:56–60` 按生命点数相加，另经过治疗修正，不是按恶魔最大生命计算该百分比。
- **P03｜entry-03416｜沿袭上游：视线外“失败”的实际后果。** `demonic-pact.lua:867–882` 回退为自身周围随机传送，并继续尝试召唤；尚不能确定目标版本是否如此。
- **P04｜entry-03422｜沿袭上游：诅咒基础时长。** `doom-shield.lua:185` 传入 10，文本均写 5。`E/game/modules/tome/class/Actor.lua:7644–7670` 还会按豁免调整时长，不能宣布所有目标都持续 10 回合。
- **P05｜entry-03424｜英文与快照冲突，译文与赋值一致。** `fearfire.lua:75` 传入 4；本体 `physical.lua:952–972` 和 `ActorTemporaryEffects.lua:117–131` 支持感知效果及持续时间传递。缺目标 DLC 版本和完整行动时序适用证据，不按英文数字自动判错。
- **P06｜entry-03425｜沿袭上游：清除范围。** `fearfire.lua:104–117` 排除 other、cross tier。现有“所有”与所读过滤实现存在范围疑点。
- **P07｜entry-03431｜沿袭上游：回血次数上限。** `timed_effects.lua:683–692` 每次符合条件都调用治疗；`E/game/modules/tome/class/interface/Combat.lua:643`、`Actor.lua:6201–6226` 未提供这项治疗的每回合限次。仍缺目标 DLC 及加载组合证据。
- **P08｜entry-03438｜沿袭上游：致死伤害不触发爆炸。** `timed_effects.lua:1051` 明确排除 `dead`，两种文本均未说明。
- **P09｜entry-03438｜沿袭上游：阈值等号。** 同处只排除 `val < threshold`；文本均写严格超过。
- **P10｜entry-03447｜译文边界疑点。** DLC `timed_effects.lua:805、822、831` 关联显示值与负生命加值；本体 `ActorLife.lua:49–56` 在等于阈值时已进入死亡判定。译文“不低于”包括等号，不能认定得到机制支持；完整组合的目标版本适用性仍缺失。
- **P11｜entry-03413｜本轮补充，沿袭上游的复用条件疑点。** `demonic-pact.lua:481–485` 要求恶魔名称和 `on_slot` 同时匹配，`:495–536` 才选择新建或更新。文本只说“同类”，未明确装备槽位；同种不同槽是否应纳入说明，需目标版本及种子分类语境进一步确认。
- **P12｜entry-03427｜本轮补充，沿袭上游的治疗／反噬计量疑点。** `heart-of-fire.lua:160–166` 用治疗前缺失生命值 `hp` 计算后续伤害，没有使用实际治疗增量；本体 `Actor.lua:2336–2358` 可改变实际治疗量。因而“恢复满值”和“伤害等于实际治疗值”并非在所有治疗修正条件下都由快照保证。缺目标 DLC 适用证据，保留未决。

主要分歧按完整语境处理：没有把“级别”直接判成数值等级，也没有把“由……承受”“半径”分别强制解释为伤害转移和随机落点；但明确丢失的类型、选择来源、触发条件、操作信息及火焰语义仍计缺陷。上游误述没有被豁免，只因 DLC 版本证据不足归入 P。

实际读取范围如下。设本包绝对路径为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g07-20260923`

读取本包的 `ADJUDICATION-INPUT.md`、`INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及以下 13 个 `D/` 文件；哈希全部匹配：

```text
data/talents/corruptions/demonic-pact.lua
data/talents/corruptions/demonic-strength.lua
data/talents/corruptions/doom-covenant.lua
data/talents/corruptions/doom-shield.lua
data/talents/corruptions/fearfire.lua
data/talents/corruptions/heart-of-fire.lua
data/talents/corruptions/infernal-combat.lua
data/talents/corruptions/npcs.lua
data/talents/corruptions/oppression.lua
data/talents/corruptions/torture.lua
data/talents/corruptions/wrath.lua
data/talents/misc/races.lua
data/timed_effects.lua
```

额外读取白名单根目录  
`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok/`  
中的两个单文件，哈希均匹配：

- `tome-ashes-urhrok/superload/mod/class/interface/Combat.lua`：由已读 `HARDENED_CORE.armor／spellpower` 引入，核验护甲及法强消费。
- `tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua`：由 `BLACKICE` 效果引入，核验充能生成与消耗。

本体仅通过指定固定提交的 `git show` 读取：

- `game/modules/tome/class/Actor.lua`：效果、伤害、治疗及回调派发。
- `game/modules/tome/class/interface/ActorLife.lua`：由 Actor 的 require 引入，核验死亡阈值。
- `game/engines/default/engine/interface/ActorLife.lua`：由上述接口的基类 require 引入，核验治疗参数消费。
- `game/engines/default/engine/interface/ActorTemporaryEffects.lua`：由 Actor 的 require 及 `setEffect` 引入。
- `game/modules/tome/class/interface/Combat.lua`：由 Actor 的 require、近战回调及 `on_melee_hit` 引入。
- `game/modules/tome/data/timed_effects/magical.lua`：由 `EFF_CURSE_IMPOTENCE`、`EFF_OUT_OF_PHASE` 引入。
- `game/modules/tome/data/timed_effects/physical.lua`：由 `EFF_SENSE` 引入。
- `game/modules/tome/data/damage_types.lua`：由 `DEMONFIRE`、`demonblood_dam`、`demonblood_def`、`fiery_torment` 引入。

40 条 `INPUT.md` 原译文均与 `entries.json` 一致；格式化参数类型、顺序及命名标记核对通过，`args_order／special` 均为空。未发现读取越界；未查找模型身份、来源映射、原始报告、STATE 或其他答案；未修改仓库、创建临时文件或子 agent。上述结果仅为独立审核裁决。
