# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的50项观察及独立盲审的19项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03413 | C01（原问题） | 未提出此缺陷 | C01（原问题） | **漏译宿主的恶魔类型限定，翻译新增。** `unique demons` 变为“史诗生物（Unique）”。后面的“有对应的恶魔种子”是另一个条件，未译出宿主类型。`D/data/talents/corruptions/demonic-pact.lua:364–369` 按 `host.type == "demon"` 分支决定是否按宿主名称匹配种子。 |
| D02 | entry-03416 | C05（原问题） | C03（原问题） | C03（原建议） | **距离上限信息丢失，翻译新增。** `up to %d grids` 变为“%d 码外”；“误差”不能表达可选距离的上限。`D/data/talents/corruptions/demonic-pact.lua:855–875、888–895` 分别消费选点范围和落点散布半径。 |
| D03 | entry-03416 | C06（原问题） | 未提出此缺陷 | 未提出此缺陷 | **随机选择的种子来源集合遗漏，翻译新增。** `from your seeds` 未译出。装备种子是施法前提，不能替代“从这些种子中选择恶魔”的来源信息。`D/data/talents/corruptions/demonic-pact.lua:326–343、851、879–882` 构造穿戴种子列表并从中抽取。 |
| D04 | entry-03419 | C08（原问题） | C05（原问题） | C04（原问题） | **乘算叠加限定遗漏，翻译新增。** `multiplicatively` 未译出。`D/data/timed_effects.lua:805、813–820` 使用 `100 × (1 − 0.92^stacks)`；两层为 15.36%，不是 16%。 |
| D05 | entry-03431 | C15（原问题） | C09（原问题） | C07（原问题） | **回血的近战限定遗漏，翻译新增。** `in melee` 被泛化为“攻击”。`D/data/timed_effects.lua:683–686` 使用 `callbackOnMeleeHit`；`E/game/modules/tome/class/interface/Combat.lua:643` 为近战命中调用点。 |
| D06 | entry-03431 | 未提出此缺陷 | C09（原问题） | C07（原问题） | **回血的伤害条件遗漏，翻译新增。** 原文为 `damage this foe`，译文只要求“攻击”。`D/data/timed_effects.lua:684` 排除空或非正的伤害参数。注意这不是“目标最终必须扣血”：`E/game/modules/tome/class/interface/Combat.lua:627–643` 传入的是近战计算参数，未接收伤害投射器的最终扣血返回值。 |
| D07 | entry-03433 | C17（原问题） | C10（原问题） | C09（原问题） | **惊吓效果的近战限定遗漏，翻译新增。** `melee hits` 变为泛指攻击。`D/data/talents/corruptions/oppression.lua:72–81` 仅通过近战攻击回调施加效果。 |
| D08 | entry-03433 | C17（原问题） | C10（原问题） | C09（原问题） | **成功命中的条件遗漏，翻译新增。** `successful` 未译出，且“每次攻击会刷新”也未保留该条件。`D/data/talents/corruptions/oppression.lua:75` 明确排除 `not hitted`。 |
| D09 | entry-03437 | C19（原问题） | C11（原问题） | C10（原问题） | **指定落点的操作信息遗漏，翻译新增。** `specific location` 未译出。“传送半径”表达距离，却没有表达可指定位置。`D/data/talents/misc/races.lua:55–68` 获取玩家坐标、检查空位后以半径零传送。并不据此认定“半径”必然表示随机。 |
| D10 | entry-03437 | C20（原问题） | 未提出此缺陷 | 未提出此缺陷 | **明确适用的状态名未沿用，翻译新增。** 第二段“停留在相位外 5 回合”明确指向状态，而冻结术语要求 Out of Phase 使用 preferred“脱离现实”、沿用效果定义。`D/data/talents/misc/races.lua:73–77` 设置该效果；`E/game/modules/tome/data/timed_effects/magical.lua:2582–2598` 核实状态身份及加成。缺陷限于明确指称该状态的部分，不强制逐字替换所有叙事性 phase 表述。 |
| D11 | entry-03438 | 未提出此缺陷 | 未提出此缺陷 | C11（原建议） | **重置对象“冷却时间”遗漏，翻译新增。** 原文明确重置两个技能的 `cooldowns`，译文只写重置技能；该句没有其他冷却说明。`D/data/talents/misc/races.lua:133–134` 对两个技能执行 `alterTalentCoolingdown(..., -1000)`。 |
| D12 | entry-03440 | C22（原问题） | C12（原问题） | C12（原问题） | **武器所属对象丢失，翻译新增。** 武器看起来不再危险变为角色“危险度”降低。`D/data/timed_effects.lua:51–52` 为武器附魔的获得／结束日志；`context.lua:466–469` 保留完整成对语境。 |
| D13 | entry-03441 | C23（原建议） | 未提出此缺陷 | 未提出此缺陷 | **火焰燃烧含义丢失，翻译新增。** `blazing` 仅译为“闪耀”。`D/data/timed_effects.lua:156–178` 的两个使用处分别对应武器火焰和包围生物的吞噬火焰，均不是普通发光。英文 `'s` 的缺词／病句来自上游，不能据此统一指定“武器”。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O001 | Sol C01（原问题） | entry-03413 | refuted | “级别”后明确列出普通、精英、稀有等 rank，未变为数值等级；“存活”结合成熟种子语境未引入另一概率。`demonic-pact.lua:665` 先施加种子，`timed_effects.lua:515–518` 才按概率取得成熟种子。 |
| O005 | Gemini C02（原建议） | entry-03413 | mixed | **refuted**：不能把概率直接认作植入动作失败概率，快照在宿主死亡时抽取；**advisory**：多余空格及更清楚的概率措辞。见 `demonic-pact.lua:665`、`timed_effects.lua:515–518`。 |
| O006 | Sol C02（原问题） | entry-03413 | pending | P01；`:655` 确有首次例外，但目标 DLC 版本未固定。 |
| O007 | Opus C02（原问题） | entry-03413 | advisory | “此外”另起回复／复活陈述，不能确定其受高等级条件约束；已有种子“提升等级”也已表达更新对象。`:438–467、495–536` 支持更新与治疗分开理解，现有表述可澄清但不确认两项缺陷。 |
| O008 | Opus C03（原明确未列为缺陷） | entry-03413 | pending | P02；`:467、605、701` 确有点数参数与百分比文本差异；沿袭上游不构成豁免，版本适用性仍缺失。 |
| O009 | Opus C04（原建议） | entry-03413 | advisory | 空格不改变参数或句义。 |
| O014 | Sol C04（原问题） | entry-03416 | pending | P03；`:867–882` 支持回退随机传送，但不能据快照确定目标版本。 |
| O015 | 独立盲审 C04（原待确认） | entry-03416 | pending | P03；观察对源码事实及版本缺口的区分成立。 |
| O018 | Opus C07（原明确未列为缺陷） | entry-03416 | pending | P03；英文和中文都有描述缺口，不能因来自英文而直接排除。 |
| O023 | Gemini C05（原问题） | entry-03420 | advisory | darkness 记录为 existing，非所声称的强制标准；`timed_effects.lua:853` 只能证明伤害类型。与邻文统一可建议，不能据此确认术语错误。 |
| O024 | Opus C09（原建议） | entry-03420 | advisory | “黑暗／暗影”一致性和“开启”的自然程度可改善；上下文已有层数，不足以判为另一机制。 |
| O025 | Sol C06（原问题） | entry-03422 | pending | P04；`:185` 的基础赋值 10 成立，最终时长还经过本体效果处理，且 DLC 版本未固定。 |
| O026 | 独立盲审 C06（原待确认） | entry-03422 | pending | P04；对基础时长与豁免后时长的区分成立。 |
| O027 | Opus C10（原明确未列为缺陷） | entry-03422 | pending | P04；不能把调用参数直接概括成所有目标实际持续 10 回合，也不能豁免上游误述。 |
| O028 | Gemini C06（原待确认） | entry-03424 | pending | P05；`:75` 赋值 4，不能仅按英文 3 判译文错。 |
| O029 | 独立盲审 C07（原待确认） | entry-03424 | pending | P05；效果定义和持续时间接口已核实，目标 DLC 版本对应关系仍缺失。 |
| O030 | Opus C11（原未发现问题） | entry-03424 | pending | P05；快照支持译文，但不足以直接结案为目标版本无问题；倒计时函数也不是完整行动时序证明。 |
| O031 | Sol C07（原问题） | entry-03425 | pending | P06；`:107` 排除 other 和 cross tier 的事实成立，版本适用性未定。 |
| O032 | 独立盲审 C08（原待确认） | entry-03425 | pending | P06；过滤条件与随后按清除数量计伤害已核实。 |
| O033 | Opus C12（原建议） | entry-03429 | advisory | 两种称呼均指第二个选择对象；`infernal-combat.lua:120–128` 未显示对象混淆。 |
| O034 | Sol C08（原问题） | entry-03430 | advisory | `timed_effects.lua:715–731` 确为另加伤害；但完整译句先说源生物受到伤害，没有说减去或转移。“由”不足以独立证明排他的伤害分担机制。 |
| O035 | 独立盲审 C09（原问题） | entry-03430 | advisory | `Actor.lua:3013–3014` 支持回调未扣减原值；文本可消歧，但不能由“由……承受”必然推出源生物减伤。 |
| O036 | Opus C13（原问题） | entry-03430 | advisory | 同 O034；不确认其“暗示”已构成另一明确机制承诺。 |
| O037 | Gemini C07（原问题） | entry-03431 | mixed | **confirmed**：近战及伤害条件遗漏；**refuted**：将回调参数解释为最终有效扣血。`Combat.lua:627–643` 没有把投射器最终结果赋回 `dam`。 |
| O038 | Gemini C08（原问题） | entry-03431 | advisory | `DamageType.DARKNESS` 已核实；术语 existing 不支持“不得译为黑暗”的强制结论。 |
| O039 | Sol C09（原问题） | entry-03431 | mixed | **confirmed**：近战及正伤害参数条件；**refuted**：把译文必然解释为对“曾被刺穿”目标永久有效。前句已提供刺穿、流血 5 回合的局部语境。 |
| O040 | 独立盲审 C10（原问题） | entry-03431 | mixed | **confirmed**：近战及伤害条件遗漏；**refuted**：最终扣血门槛及必然延伸到流血结束后的说法。见 `timed_effects.lua:683–701`、`Combat.lua:627–643`。 |
| O041 | 独立盲审 C11（原待确认） | entry-03431 | pending | P07；效果回调及本体派发中未见该治疗的每回合限制，目标加载组合未固定。 |
| O042 | Opus C14（原问题） | entry-03431 | advisory | 同一段紧接盾击伤害写“额外 50%”，有明确局部参照；`:168` 的基数与此吻合。可表达得更明确，但不因存在理论上的其他读法确认遗漏。 |
| O044 | Opus C16（原明确未列为缺陷） | entry-03431 | pending | P07；本地没有 turn_procs 尚需结合调用链，已补核本体派发；最终仍受版本缺口限制。 |
| O049 | Opus C18（原建议） | entry-03436 | advisory | 已写“角度增加”，数值及角度语境保留；`wrath.lua:206`、`fearfire.lua:186` 支持角度值。单位补全属建议。 |
| O050 | Gemini C10（原问题） | entry-03437 | mixed | **confirmed**：指定落点信息遗漏；**refuted**：“半径”必然表示随机传送。`:55–68` 证明精确选点，但并不证明中文“半径”自带随机含义。 |
| O053 | Opus C19（原问题） | entry-03437 | mixed | **confirmed**：指定落点遗漏；**advisory**：避免读者把范围和散布混淆；不另计“随机传送误述”。 |
| O055 | Opus C21（原建议） | entry-03437 | advisory | All Resists 术语行针对面板标签；“全体抗性”在本句语义等价。 |
| O056 | Gemini C11（原建议） | entry-03438 | mixed | **advisory**：紧接触发伤害的“额外 50%”已有局部基数；**confirmed**：冷却这一重置对象遗漏。两项不合并判建议。 |
| O058 | 独立盲审 C15（原待确认） | entry-03438 | pending | P08；`timed_effects.lua:1051` 排除 `dead`，版本适用性未定。 |
| O059 | 独立盲审 C16（原待确认） | entry-03438 | pending | P09；`:1051` 使用 `<` 排除，等于阈值可通过；沿袭英文，目标版本未定。 |
| O064 | Sol C13（原问题） | entry-03441 | refuted | 只考察 RAGING_FLAMES 后要求统一恢复“武器”，遗漏同字符串在 CURSED_FLAMES 的使用。`:177–178` 指生物周围火焰。该错误对象判断不借用 D13。 |
| O067 | Opus C24（原建议） | entry-03445 | advisory | 空格不对称不改变酸性抗性、亲和或参数。 |
| O068 | 独立盲审 C19（原待确认） | entry-03447 | pending | P10；固定本体确在 `life <= die_at` 进入死亡处理；DLC 显示与设置的目标版本适用性未定。 |
| O069 | Opus C25（原建议） | entry-03448 | advisory | `timed_effects.lua:861、866–869` 显示当前层数，白名单 `demon-seeds.lua:773–774` 消耗该层数。“叠加次数”可改得更清楚，但未显示错误数值或机制。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
