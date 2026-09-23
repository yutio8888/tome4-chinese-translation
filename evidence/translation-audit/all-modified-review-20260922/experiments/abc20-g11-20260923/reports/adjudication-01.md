完成匿名归并及全 40 条独立复核：**13 条 ISSUE、8 条 PENDING、19 条 OK；归并为 15 项确认缺陷**。OK 包括仅有措辞建议的条目。

以下 `S` 指本包的技能源码目录，`A` 指清单批准的追加 Cults 源码目录，`E` 指固定 commit 的本体源码；完整路径见末尾。所有 DLC 证据均为**哈希匹配、源码 commit 未固定的快照**，不代表目标版本机制已确认。

| entry-ID | 判定 | canonical D 或 P 编号／简短依据 |
|---|---|---|
| entry-03573 | OK | 五回合、每种疾病附加伤害及参数顺序对应 |
| entry-03574 | PENDING | P01；“激励意志”仅属叙事措辞 |
| entry-03575 | ISSUE | D01；不确认“听众”造成群体目标误译 |
| entry-03576 | ISSUE | D02、D03；另有 P02 |
| entry-03577 | OK | 拉拽日志的施受关系、标记正确 |
| entry-03578 | ISSUE | D04；另有 P03 |
| entry-03579 | PENDING | P04；黑暗／暗影、非瞬间／非瞬发仅建议 |
| entry-03580 | OK | 召唤者链接说明对应 |
| entry-03581 | ISSUE | D05；复活对象由完整段落限定为蠕虫伙伴 |
| entry-03582 | PENDING | P05；双主体承接攻击谓语，不能确认“合计一次” |
| entry-03583 | PENDING | P06；按等级获得槽位已表达非临时增益 |
| entry-03584 | PENDING | P07、P08 |
| entry-03585 | OK | 三种强度降低、叠加上限及持续时间对应 |
| entry-03586 | PENDING | P19；`args_order=[2,1]` 正确 |
| entry-03587 | OK | 额外层数、幻象概率及追加时空伤害对应 |
| entry-03588 | ISSUE | D06；另有 P09 |
| entry-03589 | OK | 传送落点选择提示对应 |
| entry-03590 | OK | 传送失败分支及目标参数对应 |
| entry-03591 | OK | 传送成功日志、颜色和姓名参数对应 |
| entry-03592 | OK | 抵抗传送分支对应 |
| entry-03593 | PENDING | P10；两种伤害间缺连词仅建议 |
| entry-03594 | ISSUE | D07；另有 P11、P17 |
| entry-03595 | ISSUE | D08；另有 P18 |
| entry-03596 | ISSUE | D09，独立复核补充 |
| entry-03597 | OK | 强化后缀及姓名参数对应 |
| entry-03598 | OK | 目标选择语境可理解；表达生硬仅建议 |
| entry-03599 | OK | `args_order=[1,3,2]` 正确保留护盾量与持续时间 |
| entry-03600 | ISSUE | D10；Magic 译名一致性仅建议 |
| entry-03601 | OK | 维度迅击失败日志、技能名对应 |
| entry-03602 | ISSUE | D11；“3 个额外目标”有快照支持 |
| entry-03603 | OK | 窃取技能选择界面提示对应 |
| entry-03604 | ISSUE | D12；消化条件可由前句承接 |
| entry-03605 | ISSUE | D13、D14；另有 P12、P13、P14 |
| entry-03606 | OK | 后缀主体措辞仅建议；宿主拼接问题归入 D13 |
| entry-03607 | OK | 触手拖拽失败及两个姓名参数对应 |
| entry-03608 | OK | 敌我效果数量、正负属性及缩短回合对应 |
| entry-03609 | OK | `logSeen` 标点术语不约束本条 `logPlayer` |
| entry-03610 | PENDING | P15 |
| entry-03611 | OK | 伤害来源、承受者及转化日志对应 |
| entry-03612 | ISSUE | D15；另有 P16 |

确认缺陷如下。“翻译新增”表示相对冻结英文产生的偏差，不表示本次实验才引入。

| D-ID | entry-ID | 内容、归因及源码／语境证据 |
|---|---|---|
| D01 | entry-03575 | **翻译新增的叙事遗漏**：`Weave your chosen prophecy into your speech` 所表达的将预言融入话语的动作没有译出。“双重诅咒”与下一句附加预言的机制说明没有保留这项叙事内容。`S/doom.lua:372`；`:110–113` 支持后句机制，但不能补回遗漏的前句。 |
| D02 | entry-03576 | **翻译新增的选择范围遗漏**：`one of your talents on cooldown` 变为“你的一个技能”，遗漏当前处于冷却中的限制。`S/doom.lua:416`；`A/data/timed_effects.lua:902–911` 从施法者的 `talents_cd` 选取非固定冷却技能，再减少剩余冷却。 |
| D03 | entry-03576 | **翻译新增的单位遗漏**：`%d turns` 只剩 `%d`，缺“回合”。`S/doom.lua:389、416、422`；`A/data/timed_effects.lua:911` 消费的是冷却回合减量。与 D02 分开计。 |
| D04 | entry-03578 | **翻译新增的初始范围信息损失**：`radius 1` 变为“一格小型黑洞”，没有明确一格是半径；后文只说明半径如何增长，不能确定初始量所指。`S/entropy.lua:84、102、119–123、231` 明确区分初始半径、增长及最大半径。 |
| D05 | entry-03581 | **翻译新增的操作说明遗漏**：末句把“更改装备与技能时切换控制”缩为仅更改装备。前句说明能改技能，没有保留该操作路径。`S/friend-of-the-worm.lua:437`；`:239–241` 设置全控伙伴，`:164–167` 分配可用技能点。 |
| D06 | entry-03588 | **翻译新增的限制作用域变化**：英文限制同时发生的多次裂隙爆炸命中同一目标；“一次湮灭不能多次伤害同一目标”仅说明单次事件内部去重。`S/nether.lua:132–134、155`；`A/data/damage_types.lua:44–47` 在目标上共享 `turn_procs.rift_explosion`，不是单次爆炸私有集合。 |
| D07 | entry-03594 | **翻译新增的类别指代错误**：`next Nether spell` 写成“下一次虚空法术”，混淆本包区分的 Nether 与 Void 类别。`S/nether.lua:24、50–58、81、103–109、164、196–200`；`S/void.lua:22`。冻结语境中的三个强化技能均属彼世系；此判定不依赖把 existing 术语当成强制规范。 |
| D08 | entry-03595 | **翻译新增的触发事件信息损失**：`applied or increased` 被概括为“受到熵能反冲”，没有区分效果新增／增强与既有效果逐回合造成伤害。`S/oblivion.lua:58`；`A/data/timed_effects.lua:803–818` 在激活、合并时调用 `do_nihil`，`:827–842` 的伤害结算没有该调用。 |
| D09 | entry-03596 | **独立补充；翻译新增的范围信息遗漏**：`radius 2 explosion` 变为“2 码的虚空爆炸”，丢失半径这一度量关系。`S/oblivion.lua:311–314、337`。附加的“暗影时空各 50%”有 `E/data/damage_types.lua:2864–2869` 支持，不列缺陷。 |
| D10 | entry-03600 | **翻译新增的明确术语违规**：`global speed` 译为“整体速度”。INPUT 的 `T.GAME.STAT / tformat / preferred` 明确要求“全局速度”，排除“整体速度”。`S/rift.lua:425–426、565`；`E/data/damage_types.lua:3266–3281` 将 `slow=0.3` 传入减速效果。 |
| D11 | entry-03602 | **翻译新增的明确术语违规**：同一适用规则下，`global speed` 再次译为“整体速度”。`S/rift.lua:538–540、626` 对强化召唤物增加 `global_speed_base`。与 D10 分属不同条目。 |
| D12 | entry-03604 | **翻译新增的叙事具体化**：`something breaks inside it` 被写成“内部器官不断破损”，增加了特定器官损伤及持续发生的过程；原句随后转入侵入心智，没有给出这两项事实。`S/slow-death.lua:101–105`；`:42–67` 的窃取实现也不能证明该叙事增添。合并为一次不受支持的具体化。 |
| D13 | entry-03605 | **翻译新增的条件拼接语病**：非空后缀时，宿主和 entry-03606 拼成“你的触手当前属性为 ，由于副手非空，该技能暂时被禁用：〔属性列表〕”。`为` 后插入完整禁用分句，破坏属性引导句。`S/tentacles.lua:69–80`。空后缀时“属性为：〔列表〕”成立，不将该状态判错。 |
| D14 | entry-03605 | **翻译新增的人群限定变化**：带引号的 `civilized people` 变为“普通人”，把文明社会身份改为普通／特殊之分；后面的遮掩恐魔外貌没有补回这一限定。`S/tentacles.lua:76` 及本条完整叙事语境。 |
| D15 | entry-03612 | **翻译新增的数量上限遗漏**：恢复频率保留，但 `stacking up to 4 times` 完全缺失。`S/void.lua:139`；`:49–50` 仅在星数小于四时恢复，`:35` 显示 `/4`。 |

70 项匿名观察逐项裁决如下。状态针对观察实际提出的 claim；同条其他缺陷不会借来充当命中。

| O-ID | 状态 | 命中 D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | advisory | — | “激励意志”后明确列出抗性穿透，没有承诺增加意志属性；`S/disfigured-face.lua:190–201`。 |
| O002 | pending | — | P01：`:192–193` 连续施加恐惧及自身穿透，未以恐惧成功为条件；缺目标版本适用证据。 |
| O003 | mixed | D01 | 省略话语编织动作属 confirmed；“听众”在随后主要目标限定下仅 advisory，不能推导群体作用。 |
| O004 | mixed | D01 | 前半句遗漏 confirmed；“听众直接曲解为群体目标”的严重机制断言 refuted。`S/doom.lua:110–113、372` 与完整译文均明确主要目标。 |
| O005 | confirmed | D02 | 正在冷却中的选择范围缺失；`A/data/timed_effects.lua:902–911`。 |
| O006 | confirmed | D03 | `%d turns` 的单位未译；`S/doom.lua:416`。 |
| O007 | confirmed | D03 | 同一单位遗漏；`alterTalentCoolingdown(tid,-eff.cd)` 消费回合减量。 |
| O008 | confirmed | D03 | 同一缺陷，不按重复次数增加权重。 |
| O009 | confirmed | D02 | `talents_cd` 选择池支持范围限制；固定冷却排除是快照细节，不另冒充译文新增遗漏。 |
| O010 | pending | — | P02：`A/data/timed_effects.lua:943–944` 要求伤害来源等于预言施加者；中英文均未说明。 |
| O011 | confirmed | D04 | 不只是更自然的写法：一格大小没有保留明确的初始半径度量；`S/entropy.lua:84、102、231`。 |
| O012 | pending | — | P03：`S/entropy.lua:127–140` 排除非敌对目标；中英文概括为所有范围内生物，版本未定。 |
| O013 | advisory | — | darkness 条目为 existing；本句仍可识别暗属性伤害，无强制术语依据。 |
| O014 | advisory | — | “黑暗／暗影”“非瞬间／非瞬发”均属一致性和自然度建议；数值、伤害类型未变。 |
| O015 | pending | — | P04：`S/entropy.lua:250` 还要求主动法术和战斗状态；属上游描述疑点。 |
| O016 | confirmed | D05 | 能调整技能与如何调整技能不是同一信息；`:437` 的操作适用范围遗漏。 |
| O017 | refuted | — | 全段持续描述唯一的蠕虫伙伴；“已死亡的单位”没有在该语境引入任意尸体选择。`:347、357–374` 与此指代一致。 |
| O018 | refuted | — | 前文能力清单不能替代末句技能调整的控制步骤；遗漏成立，见 D05。 |
| O019 | confirmed | D05 | 操作说明遗漏确认；`S/friend-of-the-worm.lua:239–241、437`。 |
| O020 | confirmed | D05 | 同一操作范围遗漏。仅确认原说明缺失，不据此断言调整技能本身必需先交装备。 |
| O021 | advisory | — | 中文“你和蠕虫合体”可共同支配后续传送、造成伤害；未写合计或仅一次。`:494、507` 各有一次攻击，明确“各自”会更清楚，但现文不足以确认错误。 |
| O022 | advisory | — | `%d 内` 缺量词较生硬，仍处于明确的传送距离语境；`:513–515`。 |
| O023 | advisory | — | 同 O022，仅措辞完整度建议。 |
| O024 | pending | — | P05：显示 `getBlindside`，写入 `1+getBlindside`；`E/class/Actor.lua:6885` 直接扣除该值。 |
| O025 | mixed | — | 补“永久”属 advisory；“`no_unlearn_last` 保证所有解锁槽永久固定”的论据 refuted，该字段不等于锁定全部等级，槽数仍由当前原始等级计算。 |
| O026 | pending | — | P06：已沿 `ActorInscriptions` 核实通用槽消费，但冻结材料未说明“纹身”是否为本项目总称，不能仅凭个人译名习惯判错。 |
| O027 | pending | — | P07：`:565` 拒绝距离 `>=3`；与中英文范围边界有差异，目标版本未定。 |
| O028 | pending | — | P08：`A/data/timed_effects.lua:267` 传入持续时间二，文本写三；不能只凭实参值宣称目标版本的最终显示时长已确认。 |
| O029 | confirmed | D06 | 单次事件内部去重与跨爆炸共享限制不同；`A/data/damage_types.lua:44–47`。 |
| O030 | advisory | — | 单独看“湮灭／引爆”属于文风选择；本观察没有提出 D06 的限制作用域问题，不借用 D06。 |
| O031 | confirmed | D06 | 文本自身已改变限制作用域，快照另有支持；不因 DLC 版本未定而搁置这项文本可证偏差。 |
| O032 | pending | — | P09：`S/nether.lua:147–149` 仅战斗中添加反冲；沿袭英文。 |
| O033 | advisory | — | 两组数值和伤害类型对应，缺连词不造成参数或信息错配。 |
| O034 | advisory | — | 同 O033；`S/nether.lua:286–292` 的参数顺序正确。 |
| O035 | pending | — | P10：`S/nether.lua:277–279` 存在同样的战斗状态限制，属于另一条目的独立出现。 |
| O036 | confirmed | D07 | 本包区分 `demented/nether` 与 `demented/void`；类别指代混淆确认。 |
| O037 | confirmed | D07 | 三个彼世技能各自检查、消耗五层火花；`:50–58、103–109、196–200`。 |
| O038 | advisory | — | Magic 的冻结记录为 existing；“魔法属性”一致性较差，但不能据此强制定罪。 |
| O039 | mixed | D07 | 类别错误 confirmed；Magic 规范要求仅 advisory；所引 `^demented/nether` 匹配代码 refuted，实际 `:309` 为 `^demented/` 的生成回调，消费在三个技能各自分支。 |
| O040 | confirmed | D07 | 正确区分现有译名偏好与不同类别的指代错误。 |
| O041 | pending | — | P11：`:309–314` 同时检查战斗状态和同回合标记；中英文均概括为每次施放。 |
| O042 | confirmed | D08 | 新增／增强效果与反冲伤害结算不同；`activate/on_merge` 和 `on_timeout` 调用链支持该区分。 |
| O043 | advisory | — | `S/rift.lua:220–222` 的选点失败语境仍能表达视线不通，主要问题是中文生硬。 |
| O044 | confirmed | D10 | INPUT 的 preferred 术语精确适用于本条 `tformat` 机制说明。 |
| O045 | confirmed | D10 | 同一术语违规；半径四、`slow=0.3` 与条目对应。 |
| O046 | advisory | — | Magic 译名问题不具有本包强制规范依据。 |
| O047 | mixed | D10 | global speed 违规 confirmed；附带的 Magic “规范应为”要求仅 advisory。 |
| O048 | confirmed | D10 | source_tag、category 与技能机制语境均匹配明确规则。 |
| O049 | confirmed | D11 | `S/rift.lua:540` 增加全局速度；术语规则适用。 |
| O050 | confirmed | D11 | 同一条目的相同术语违规。 |
| O051 | confirmed | D11 | `global_speed_base` 消费与机制相符，不是其他局部速度。 |
| O052 | confirmed | D11 | 术语违规确认；附带排除“额外三目标”错误也有 `:331–337` 支持。 |
| O053 | confirmed | D12 | 原文没有明确器官，也未说持续破损；`:101–105` 的心智因果语境支持判断。 |
| O054 | advisory | — | 前句已建立正在消化的目标，后句“它”承接该条件。显式重复时机更清楚，但不能说整个条件消失。`:42–67` 支持消化时选取。 |
| O055 | confirmed | D12 | 与 O053 为同一叙事具体化，合并，不把两个修饰分别计为两个缺陷。 |
| O056 | mixed | D13 | 非空禁用后缀造成语病 confirmed；空后缀也破坏句子的断言 refuted，冒号后的属性列表可完成“属性为”的句子。 |
| O057 | confirmed | D14 | “文明人”与“普通人”不是同一人群限定；`:76`。 |
| O058 | mixed | — | 方位 claim 保留 pending，见 P12；冒号前空格仅 advisory。该观察没有识别 D13 的非空后缀句法问题，不借用 D13。 |
| O059 | confirmed | D14 | 同一人群属性变化；引号语气为辅助语境，不另计缺陷。 |
| O060 | pending | — | P12：`A/superload/mod/class/interface/Combat.lua:40–49` 只取按攻击方向计算的左右邻格；“同侧”的范围表达仍需目标版本与实际方向语境确认。 |
| O061 | pending | — | P13：`:29–37` 未检查原攻击命中，也未在此限定普通攻击；不能直接把中文去掉“命中”判错。 |
| O062 | pending | — | P14：`:52–54` 有回合标记，缠绕分支 `S/tentacles.lua:265` 也未直接发放该增益；频率描述疑点沿袭上游。 |
| O063 | mixed | — | “该技能”替代触手的主体措辞仅 advisory；“插入后正常显示”的笼统结论 refuted，非空拼接有 D13。强制触手调用确见 `S/disfigured-face.lua:39`。 |
| O064 | advisory | — | 冻结术语为 `logSeen`，本条实际 `logPlayer`；感叹号没有违反明确适用规则。 |
| O065 | pending | — | P15：`hasLightArmor()` 接受 cloth、light、mummy；缺 DLC 与固定本体组合的目标版本适用证据。 |
| O066 | confirmed | D15 | 英文上限从译文完全消失；`:35、49–50、139` 支持。观察附带的读取自述不作为我的证据。 |
| O067 | confirmed | D15 | 同一上限遗漏。反冲的 `floor(reduce/20)×8` 支持约四成的说明；不将整数取整另列问题。 |
| O068 | confirmed | D15 | 上限缺失确认，但不采纳其未经独立标定的严重程度措辞。 |
| O069 | confirmed | D15 | 文本直接可证；无需先解决 DLC 目标版本对应。 |
| O070 | pending | — | P16：独立于上限缺失的护甲适用范围疑点，与 P15 分条覆盖。 |

未决项单独列出，不计入 D。除 P06 还涉及术语语境外，下列机制判断均缺 DLC 快照与目标版本的对应证据：

- **P01｜entry-03574｜沿袭上游**：`S/disfigured-face.lua:192–193` 未检查恐惧成功即添加自身穿透；`A/data/timed_effects.lua:580` 消费穿透值。快照支持条件疑点。
- **P02｜entry-03576｜沿袭上游**：`A/data/timed_effects.lua:941–945` 只在伤害来源为预言施加者时治疗，文本没有这项限制。
- **P03｜entry-03578｜沿袭上游**：`S/entropy.lua:127–140` 只拉拽、伤害敌对目标，文本泛称范围内所有生物。
- **P04｜entry-03579｜沿袭上游**：`S/entropy.lua:250` 要求法术、非瞬发、主动模式、处于战斗；文本未交代后两项。
- **P05｜entry-03582｜沿袭上游**：`S/friend-of-the-worm.lua:272、515` 的实际减免与显示值差一；固定本体 `E/class/Actor.lua:6885` 直接扣除字段值。
- **P06｜entry-03583｜可能为翻译范围变化，归因未定**：`max_inscriptions` 是通用容量；`E/class/interface/ActorInscriptions.lua:34–69` 另行检查铭文类别限制。冻结术语没有“纹身”与 inscription／infusion 的对应约定，不能确认它在本语境排除其他铭文。
- **P07｜entry-03584｜沿袭上游**：`S/friend-of-the-worm.lua:565` 拒绝恰好距离三；相邻共享疯狂条件 `:537` 则允许距离三。
- **P08｜entry-03584｜沿袭上游**：`A/data/timed_effects.lua:267` 施加参数为二，文本写三。还未完成效果调度、持续时间修正的完整链核验，不宣称实际玩家可见时长必为二。
- **P09｜entry-03588｜沿袭上游**：`S/nether.lua:147–149` 仅在战斗中施加反冲。
- **P10｜entry-03593｜沿袭上游**：另一技能的同类限制，见 `S/nether.lua:277–279`。
- **P11｜entry-03594｜沿袭上游**：`S/nether.lua:309–314` 的火花生成受战斗状态和每回合标记限制。
- **P12｜entry-03605｜可能为翻译范围变化**：“目标同侧”不足以精确识别快照选取的左右邻格；`A/superload/mod/class/interface/Combat.lua:40–49`。不把它直接扩大解释成阵营或整片区域。
- **P13｜entry-03605｜主要沿袭上游，中文命中措辞有所变化**：通用 `attackTargetWith` 后置分支并未以原攻击命中或普通攻击为条件。完整调用覆盖尚未完成，见上述文件 `:29–37`。
- **P14｜entry-03605｜沿袭上游**：增益受 `tentacle_insanity_gain` 回合标记及攻击路径限制；上述文件 `:52–54`，以及 `S/tentacles.lua:254–265`。
- **P15｜entry-03610｜沿袭上游**：固定本体 `E/class/interface/Combat.lua:2672–2678` 接受布甲等多个子类；不能把 DLC 提示与该版本组合直接当成目标运行事实。
- **P16｜entry-03612｜沿袭上游**：同样的护甲范围疑点，入口为 `S/void.lua:43`，与 D15 分开。
- **P17｜entry-03594｜独立补充，沿袭上游**：中英文泛称暴击率；`A/data/timed_effects.lua:655–669` 实际修改 `combat_spellcrit`，效果自身说明 `:629` 也写 spell critical chance。目标版本适用性待确认。
- **P18｜entry-03595｜独立补充，沿袭上游**：文本说随机可见敌人；`S/oblivion.lua:33–52` 的选取只显式检查半径和敌对关系，未检查可见性。`A/data/timed_effects.lua:1125–1132` 是施加后的视线丢失处理，不能自动等同初始筛选；目标版本及完整可见性行为待确认。
- **P19｜entry-03586｜独立补充，沿袭上游**：中英文概括幻象被消灭即爆发；`S/madness.lua:118–136` 将爆发包在关联受害者仍存活的条件内。快照有具体条件差异，目标版本适用性待确认。

主要分歧按完整语境处理：“听众”和“已死亡的单位”没有自动变成群体施法或任意复活；双主体句也没有自动变成合计一次攻击。相反，操作步骤的适用对象、明确的数值单位与半径关系，不能仅因玩家可能猜出而豁免。触手拼接仅确认非空后缀状态，否决“两种状态都坏”的过宽断言。

实际读取范围如下：

- 冻结包根目录 **B**：[abc20-g11-20260923](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/ADJUDICATION-INPUT.md) 所在目录。读取 `ADJUDICATION-INPUT.md`、`INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。
- **S = B/sources/dlc/cults/tome-cults/data/talents/demented**。读取相关片段的十二个单文件：`disfigured-face.lua`、`doom.lua`、`entropy.lua`、`friend-of-the-worm.lua`、`madness.lua`、`nether.lua`、`oblivion.lua`、`rift.lua`、`slow-death.lua`、`tentacles.lua`、`timethief.lua`、`void.lua`。十二份文件 SHA-256 全部匹配清单。
- **A = `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults`**。只读三份明确获准、哈希匹配的追加文件：`data/timed_effects.lua`，由已读技能效果 ID 引入；`data/damage_types.lua`，由 `RIFT`、`RIFT_EXPLOSION`、`VOIDBURN` 引入；`superload/mod/class/interface/Combat.lua`，由触手战斗接口调用引入。未读取该实验目录的其他材料。
- **E = `game/modules/tome`，commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`**。仅通过 `git -C /workspace/t-engine4 show` 读取 `class/Actor.lua`、`class/interface/Combat.lua`、`data/damage_types.lua`；分别追查冷却减免、轻甲及攻击接口、VOID 和 CHRONOSLOW。再由 `Actor.lua:37` 的明确 `require` 引入 `class/interface/ActorInscriptions.lua`。
- `entries.json` SHA-256：`a1c330dc46cb4f868aac13366156944333cde688e913cfce5bac9a04cea8635f`。40 条占位符序列按冻结 `args_order` 重排后全部匹配；未发现其他需要确认的标记或换行缺陷。

未读取身份映射、原始报告、STATE 或其他轮答案；未修改仓库、创建临时文件或子 agent。上述结果为独立审核裁决，不构成生产完成判定。
