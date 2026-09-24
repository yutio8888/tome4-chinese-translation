# 批阅裁决台账 — batch-07

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`94867ca7fd0bed17b0e2b0cf1ef75e793a34de41643860ed433ff5f5f15a26be`
- 决策行：40；冻结修订（含孪生载体）：44
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 44 |

## 被驳回／未采纳的模型主张

| entry | 模型主张 | 裁决 | 理由 |
| --- | --- | --- | --- |
| entry-00244 | 去掉 ` area effect` 的前导空格造成中文拼接缺陷 | rejected | 模型主张补回空格。固定源码 MapEffects.lua:23 为 `dam_def.name .. _t" area effect"` 直接拼接，补空格会显示「火焰 范围效果」，反证模型建议有害。 |
| entry-00221 | 「离开地图」构成明显误译 | rejected | 模型自标 advisory。源码 Game.lua:926-936 的 can_change_level 阻止任何换层/换区域，「离开地图」覆盖该限制，功能含义正确；level/zone 统一译法属跨条目策略，非本条缺陷。 |
| entry-00345 | 「使这次攻击发生偏斜」弱化招架，应改「招架」 | rejected | 模型自标 advisory。源码确认招架成功挡住攻击，现译保留防御成功含义，属文风偏好，不构成缺陷。 |
| entry-00185 | 方括号内多空格 | rejected | 模型自标 advisory。用户策略明确纯静态排版不算缺陷；方括号不属「括号不一致」策略范围。 |
| entry-00254 | 「最大 50%」与同组「最大40%」排版不一致 | rejected | 模型自标 advisory；仅为数字前空格差异，属纯静态排版，按用户策略不整理。 |
| entry-00419 | 「超过1500点」与同组「超过 600 点」空格不一致 | rejected | 模型自标 advisory；纯静态排版差异，按用户策略不整理。 |
| entry-00428 | 三扇传送门句式与同系列不平行 | rejected | 模型自标 advisory；条件、数量、机制均正确，句式平行属文风偏好。 |
| entry-00334 | 「杀死」应为「击杀」 | rejected | 模型自标 advisory；日志在敌人 on_die 中输出，「杀死」与触发事实一致，击杀仅为界面习惯差异。 |
| entry-00434 | 「珠宝匠托付」应改为更贴近源码关系 | rejected | 模型自标 advisory；Master Jeweler 对应珠宝匠，译文为可接受意译，任务名已增补，无缺陷。 |
| entry-00393 | 复合后缀外层半角括号 | rejected_on_entry | 本条 entry-00393 本身已是全角；模型所指的半角外层括号实际出现在 entry-00395–00400（同一 hrq-00046 行的其他载体），已按 bracket_fullwidth 修复那些载体。 |
| entry-00184 | 「勇敢的向前」语病、段间缺空行 | accepted_upstream | 缺陷成立，但主工作区 HEAD 11b3e963 已修（已核逐字）。按 SPEC 规则不在本 worktree 重复修改，记 defer；不接受在本分支重复改。 |

## 逐条裁决

| queue_id | entry_id | 文件:行 | 模型意见 | ORCHESTRATOR 裁决 | 是否落实 | 理由 |
| --- | --- | --- | --- | --- | --- | --- |
| hrq-00252 | entry-01536 | mod-tome.lua:21483 | fix | accepted | 是 | 独立核验通过；四个占位符顺序正确；blindness resistance 对应 blind_immune，目盲免疫合理；damage_affinity 对应亲和，无术语证据要求改吸收。normal light 的最强反证是通常光源可指灯具，但源码比较 self.lite 与 radiance_aura，并不限于灯具，故改为常规光照。 |
| hrq-00253 | entry-01543 | mod-tome.lua:21610 | no_change | accepted | 否 | 无需修改；固定源码 logPlayer 用感叹号，现译忠实保留；术语快照中的句号不是本条日志的强制标点。两者差异不影响机制。 |
| hrq-00254 | entry-01554 | mod-tome.lua:21815 | fix | accepted | 是 | 独立核验通过；两个占位符正确。守卫此时只射一箭，“灵矢伤害降低”与当前行为等价；末句虽有前文“射击”可供承接，仍将具体 Shoot 天赋泛化为任意远程攻击，故恢复天赋名。 |
| hrq-00255 | entry-01544 | mod-tome.lua:21621 | no_change | accepted | 否 | 无需修改；源码存在第二座跃迁门和 Jumpgate: Teleport 子技能，单个 %d 是其有效距离，现译正确。此行交叉引用的 Shoot 泛化及守卫伤害是 entry-01554 的 claim，不适用于本条，已在该修订单独裁决。 |
| hrq-00256 | entry-01557 | mod-tome.lua:21879 | fix | accepted | 是 | 独立核验通过；原文是编织命运之丝，现译加“你的”并丢失 threads 意象；补全意象。Spin Fate 叠加命运之丝的模型举例未由本修订证明，不以它为依据。 |
| hrq-00257 | entry-01563 | mod-tome.lua:21913 | fix | accepted | 是 | 独立核验通过；三个占位符及次序正确；释放与逗号之间的两个空格使标点邻接错误，删除该局部多余空格。 |
| hrq-00258 | entry-01565 | mod-tome.lua:21925 | fix | accepted | 是 | 独立核验通过；全文已说明三种未来与死亡后回溯，是可用反证；但 point when you first cast 明确是首次施法时刻，“地方”误指空间地点，故修正。 |
| hrq-00259 | entry-01576 | mod-tome.lua:22025 | no_change | accepted | 否 | 无需修改；全部数值占位符正确；“码”是此处格距的惯用单位补充，没有改变半径与伤害，属表达选择。 |
| hrq-00260 | entry-01586 | mod-tome.lua:22102 | fix | accepted | 是 | 独立核验通过；普通词可译纪元是最强反证，但术语库将同名天赋及实体 Epoch 明列为 core preferred“亚伯契”，故采用专名。 |
| hrq-00261 | entry-01588 | mod-tome.lua:22122 | fix | accepted | 是 | 独立核验通过；护甲、震慑与流血抵抗及占位符已正确，唯首句省略 weave matter 的具体动作和技能名呼应，故补回。Magic 译“魔力值”能理解；对齐现有属性译名“魔力”，并不将 existing 视为强制术语。 |
| hrq-00262 | entry-01605 | mod-tome.lua:22286 | fix | accepted | 是 | 独立核验通过；前两句已建立地雷主体，所以末句省略“时空地雷的”不构成漏译；temporal (warp) 的扭曲子类型却无处承接，补全角括号限定。 |
| hrq-00263 | entry-01617 | mod-tome.lua:22388 | fix | accepted | 是 | 独立核验通过；占位符正确；“时空增效”可泛指 spellbound，但源码四项同句且另三项均译“时空绑定效果”，现译造成同一机制术语分叉，故统一。 |
| hrq-00264 | entry-01625 | mod-tome.lua:22512 | fix | accepted | 是 | 独立核验通过；占位符及百分号正确。首句召唤暗示激活，却未明确 Upon activation，补“激活时”；“你猎犬”缺“的”。“%d 回合内”可指该计时结束，不单独改为“后”。 |
| hrq-00265 | entry-01659 | mod-tome.lua:22839 | fix | accepted | 是 | 独立核验通过；三个占位符数量、顺序正确，格距用“码”成立；“%d 码球形范围”缺 radius 关系，补“半径”。 |
| hrq-00266 | entry-01661 | mod-tome.lua:22895 | fix | accepted | 是 | 独立核验通过；占位符正确；源码第五个未被文本消费的参数不应硬塞进译文。实体名及生成日志均称 carrion worm mass 为“腐肉虫群”，现译“腐尸蠕虫”族内不一致，故对齐。 |
| hrq-00267 | entry-01689 | mod-tome.lua:23218 | no_change | accepted | 否 | 无需修改；烟雾弹概括投掷易挥发液体产生烟云，阻挡视线和降低视野已表达；本条模型结论仅排版或风格，没有确认的机制缺陷。 |
| hrq-00268 | entry-01700 | mod-tome.lua:23246 | no_change | accepted | 否 | 无需修改；固定源码三个 %s 依次为主体、反身代词、方向；现译保持次序和钩爪移动动作。贴字空格属静态排版。 |
| hrq-00269 | entry-01703 | mod-tome.lua:23255 | fix | accepted | 是 | 独立核验通过；同技能完整 info 的流血和中毒效果解释现译词语来源，是最强反证；但本条 short_info 明确列 PHYSICAL 与 NATURE 伤害，现译用“流血”“自然毒素”丢失伤害类型，改回物理和自然。 |
| hrq-00270 | entry-01706 | mod-tome.lua:23297 | fix | accepted | 是 | 独立核验通过；本行五个报告观察中的本条仅是 Called Shots 首句泛化；后文已有“精准射击系”可帮助读者推断，但首句仍从具体技能系缩成射击，补“精准”。三个占位符和机制数值正确。 |
| hrq-00270 | entry-01709 | mod-tome.lua:23310 | fix | accepted | 是 | 独立核验通过；本行五个报告观察中的本条是已知陷阱集合；技能树语境可提示含义，但“学会制造各种功能的陷阱”把集合改为学习制造行为，并虚增功能限定，故改。 |
| hrq-00270 | entry-01711 | mod-tome.lua:23313 | fix | accepted | 是 | 独立核验通过；本行五个报告观察中的本条与陷阱合集平行；类别语境不足以支持“制造各种不同毒素”的动作，原文是已知毒素集合，故改。 |
| hrq-00270 | entry-01718 | mod-tome.lua:23329 | fix | accepted | 是 | 独立核验通过；本行五个报告观察中的本条漏 cunning；Artifice 类别名可暗示精巧工具，却不能代替说明中的限定，故补“精巧”，保留制造和使用。 |
| hrq-00270 | entry-01727 | mod-tome.lua:23437 | fix | accepted | 是 | 独立核验通过；本行五个报告观察中的本条只涉及 Deadly Poison 称谓；同一 poisons.lua 相邻四项均为“致命毒素”，本条“致命剧毒”造成同族分叉，故统一；%d%% 正确。 |
| hrq-00271 | entry-01732 | mod-tome.lua:23449 | fix | accepted | 是 | 独立核验通过；现译保留自然伤害、持续和石化，是最强反证；但把持续增强写成独立武器涂毒，漏施加致命毒素时的触发、土系毒素和第二个 %d 的每回合伤害单位。补齐并统一“回合”。 |
| hrq-00272 | entry-01740 | mod-tome.lua:23519 | fix | accepted | 是 | 独立核验通过；源码 xs 非空时自带前导空格，%d %s 会运行时双空格；删除固定空格。any non-instant, non-movement action 包含普通行动，现译“技能”过窄，改为行动。 |
| hrq-00273 | entry-01742 | mod-tome.lua:23557 | no_change | accepted | 否 | 无需修改；“能力增加 %d”已表达 +%d 的数值方向，省略加号不丢机制；power 由“能力”承接，补显性字样仅属措辞选择。三个数值占位符正确。 |
| hrq-00274 | entry-01751 | mod-tome.lua:23647 | fix | accepted | 是 | 独立核验通过；此 Tier 用于陷阱精通要求，不是装备材质等级；格式参数和颜色标签保持，改“阶级”。 |
| hrq-00275 | entry-01767 | mod-tome.lua:23757 | fix | accepted | 是 | 独立核验通过；冰冻气体上下文已暗示寒冷伤害，是最强反证；但第二段独立的每回合 cold 类型未显性呈现，补寒冷以完整传达机制，所有占位符不变。 |
| hrq-00276 | entry-01785 | mod-tome.lua:24033 | fix | accepted | 是 | 独立核验通过；邻近 next victim 导致串文只是推测；原句 Each day、weary body、begin the unending hunt 分别被改成无时无刻、不知疲倦、狩猎下个目标，其中疲惫被反译，三处按源码修正。 |
| hrq-00277 | entry-01788 | mod-tome.lua:24039 | fix | accepted | 是 | 独立核验通过；诅咒系 hate 为正式资源，译“愤怒”脱离术语库 preferred“仇恨值”体系；此处用“仇恨”表达情绪与资源。has grown within 是内心积聚，不是突发激增。 |
| hrq-00278 | entry-01798 | mod-tome.lua:24093 | no_change | accepted | 否 | 无需修改；“吸取”省略 sustenance 的显性宾语，但同系语境和“只能从敌人身上”已传达对象限制，未造成机制误解；养分、力量、精华没有唯一依据，补词属文风。 |
| hrq-00279 | entry-01803 | mod-tome.lua:24129 | fix | accepted | 是 | 独立核验通过；%d、25%%、+%d%% 数量和顺序正确。darkness 直译黑暗并非错类，但同系与既有 damage type 用“暗影”，对齐；anything 的实际目标可为非人 Actor，“人”过窄，改目标。 |
| hrq-00280 | entry-01804 | mod-tome.lua:24135 | fix | accepted | 是 | 独立核验通过；三个参数正确；前文“敌人”不使末句 anything 限于人形，译“人”过窄；与 entry-01803 同步改“目标”。 |
| hrq-00281 | entry-01807 | mod-tome.lua:24168 | no_change | accepted | 否 | 无需修改；两个占位符对应移动速度和双持 Defense，互斥冷却及增益已正确。hate 在风味句中形容行动动机，“杀意”可承接语境；无证据要求此处必须显示资源名。 |
| hrq-00282 | entry-01820 | mod-tome.lua:24317 | no_change | accepted | 否 | 无需修改；源码 getLightResist 返回 -15，直接代入 lose %d；若机械译失去会形成失去 -15%。现译“变化 %d%%”代入负值正确，另两个占位符也对应暗影抗性亲和及每阴影全抗。 |
| hrq-00283 | entry-01823 | mod-tome.lua:24366 | fix | accepted | 是 | 独立核验通过；地面选点的半径零及可移动检查证明此处要选目的坐标；“目标”虽可泛指位置，却可能误导为选生物，改“转移目的地”。 |
| hrq-00284 | entry-01835 | mod-tome.lua:24511 | fix | accepted | 是 | 独立核验通过；“技能激活时”已表达持续状态，但“可以召唤 %d 个”未传达自动持续补充和 up to 数量上限，改“持续召唤至多”。 |
| hrq-00285 | entry-01838 | mod-tome.lua:24528 | fix | accepted | 是 | 独立核验通过；固定源码该日志在敌对进攻分支，现译与防守日志完全相同；单看“集中”尚不构成机制误译，但两个冻结日志应区别且“被集中”动作主体不明，改为阴影向目标集中。 |
| hrq-00286 | entry-01839 | mod-tome.lua:24530 | fix | accepted | 是 | 独立核验通过；固定源码该日志在友方防守分支，form around 表示围绕目标形成阵势；现译“集中至”丢失环绕且与进攻日志相同，两条均在冻结范围，改为在周围列阵。 |
| hrq-00287 | entry-01851 | mod-tome.lua:24737 | fix | accepted | 是 | 独立核验通过；源码造成酸性伤害，另有可能触发缴械；英文 can disarm 未列数值，现译“酸性缴械伤害”错误合并伤害类型和非必然控制。恢复条件关系，不擅加概率。 |
| hrq-00288 | entry-01861 | mod-tome.lua:24890 | fix | accepted | 是 | 独立核验通过；源码效果是每回合降低 Equilibrium；英文 restore 指资源状态恢复，现译“回复失衡值”可能被读成增加，故明确降低，不能以字面翻译否认机制歧义。 |
| hrq-00289 | entry-01868 | mod-tome.lua:24956 | fix | accepted | 是 | 独立核验通过；后句最大生命和回复数值提供强化作用的上下文反证；但 fungi 是真菌而非孢子，“有治疗作用的”仍未覆盖最大生命值加成，故改“有强化作用的真菌”。 |
| hrq-00290 | entry-01870 | mod-tome.lua:24969 | fix | accepted | 是 | 独立核验通过；原译“最多获得 2 个回合”提示上限，是部分反证；源码限制储存回合能量，过量治疗不计入却完全缺失，补齐并将 fungus 与同节真菌一致。四行变五行是静态拆行，本轮保持换行序列。 |
| hrq-00291 | entry-01891 | mod-tome.lua:25019 | fix | accepted | 是 | 独立核验通过；完整句没有其他词承接 natural；“粘液”未表达自然产生这一限定，补“天然”。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
