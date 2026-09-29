# 批阅裁决台账 — batch-04

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`010c29cfd33bc8ac8b9b5c12781a88b2cff99bd11249c00af6765101aacfc8c1`
- 决策行：40；冻结修订（含孪生载体）：33
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 33 |

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
| hrq-00132 | entry-01127 | mod-tome.lua:13176 | fix | accepted | 是 | 独立核验通过；反证：「迅速干掉敌人」可视为泛指，但 most foes 是明确范围限定，省略后把「大多数」说成「全部」，属删限定词；补「大多数」。 |
| hrq-00133 | entry-01132 | mod-tome.lua:13192 | fix | accepted | 是 | 独立核验通过；反证：无。源码 logSeen 参数依次为使用者名、his_her、物品名；原文是「通过自己的某物聚焦时间流」，现译把 time flows 写成「时间线」、把 through 的媒介物品写成聚焦位置。改为以物品为媒介；占位符顺序不变。 |
| hrq-00134 | entry-01137 | mod-tome.lua:13200 | fix | accepted | 是 | 独立核验通过；反证：「环绕有强大的风暴」传达了风暴主题；但 crackles（噼啪作响的电气动态）完全漏译，vicious 被弱化为「强大」，且把 with the intensity of（比喻）写成实际环绕风暴。补译 crackles 与比喻关系。 |
| hrq-00135 | entry-01145 | mod-tome.lua:13224 | no_change | accepted | 否 | 无需修改；advisory 且模型自承需维护者定统一译法。源码为给物品镶入宝石后的日志（gem:getName），「安装」虽偏机械但未改变机制含义；imbue 统一为「镶嵌」或「灌注」属跨条目用词策略，不在本条单独改。 |
| hrq-00136 | entry-01149 | mod-tome.lua:13243 | fix | accepted | 是 | 独立核验通过；标点错误：中文句中混入半角分号，按用户「标点错误修正」策略改为全角分号。其余语义（取较低者、消耗被抵消伤害 5% 的活力）核对无误，%d/%%/换行不变。 |
| hrq-00137 | entry-01155 | mod-tome.lua:13277 | fix | accepted | 是 | 独立核验通过；「自命不凡的认为」状语应用「地」，确认修正。增饰：the fire followed his footsteps 只说「火焰」，「地狱之焰」为增饰，改回「火焰」；「恶魔的老巢高达勒斯」对 Goedalath（恶魔母星）为事实性同位说明，不改变语义，保留（hint 所问的整体意译风格不作重写）。 |
| hrq-00138 | entry-01156 | mod-tome.lua:13278 | fix | accepted | 是 | 独立核验通过；机制核验：act() 中 game.level.map:addEffect(who, x, y, 6, FIRE, dam, 0, 5, nil, {type="inferno"}, nil, false, false)，末两参 selffire=false、friendlyfire=false，只伤敌人。现译「所有经过的生物」暗示伤及自身与友方，属一级机制误导；改为「进入其中的敌人」。 |
| hrq-00139 | entry-01160 | mod-tome.lua:13294 | fix | accepted | 是 | 独立核验通过；biting colds 指刺骨寒冷，「呼啸的寒风」把寒冷换成风声意象；物品描述称谓全库以「你」为主（「您」仅 20 处），统一为「你」。 |
| hrq-00140 | entry-01161 | mod-tome.lua:13298 | no_change | accepted | 否 | 无需修改；advisory：tingly 译「刺痛」略重、「增强了你的思考」略生硬，但未改变含义，属二级文风偏好，不改。 |
| hrq-00141 | entry-01162 | mod-tome.lua:13310 | fix | accepted | 是 | 独立核验通过；源码：该 desc 属 Stormfront，base = "BASE_BATTLEAXE"（战斧），blade 指斧刃；「剑身」错指武器类型，改「斧刃」。 |
| hrq-00142 | entry-01163 | mod-tome.lua:13314 | fix | accepted | 是 | 独立核验通过；bright warm light 译「微光」亮度方向相反；且与姊妹灵晶 dim cool light（「寒冷的微光」，world-artifacts.lua:8124）的明暗对照被抹平。改「明亮而温暖的光芒」。 |
| hrq-00143 | entry-01183 | mod-tome.lua:13524 | no_change | accepted | 否 | 无需修改；「%s 抵抗传送！」中占位符后的半角空格属纯静态排版差异，按用户策略（空格差异不处理）不改；语义与占位符正确。Gemini 行号主张 refuted，不影响结论（实际源码 teleport.lua:43）。 |
| hrq-00144 | entry-01193 | mod-tome.lua:13635 | fix | accepted | 是 | 独立核验通过；「牢牢的抓住」状语应为「地」，确认修正。advisory：两句并为逗号句、「挖地逃走」对 dig themselves back into the ground 的处理均未改变含义，不改。行号主张 refuted（实际 ingredients.lua:138）。 |
| hrq-00145 | entry-01194 | mod-tome.lua:13641 | fix | accepted | 是 | 独立核验通过；It doesn't much matter 是「无所谓」，现译「没有确切的答案」改写了语义；恢复原意。advisory（对任务指引无影响）不影响结论；行号 refuted（实际 ingredients.lua:156）。 |
| hrq-00146 | entry-01196 | mod-tome.lua:13650 | fix | accepted | 是 | 独立核验通过；「穿的暖和点」补语应为「得」；原文为句号，现译改省略号，恢复句号；But 转折一并补出。「冰龙常换牙完全准确」的模型主张 refuted，不作依据；行号 refuted（实际 ingredients.lua:183）。 |
| hrq-00147 | entry-01198 | mod-tome.lua:13656 | fix | accepted | 是 | 独立核验通过；「把这个瓶子离……远一些」把字句杂糅；「明天」无原文依据；unless 条件关系被改成「我可不想」。重写为条件句。advisory：stuff 译「瓶子」——物品为 vial，改「这瓶东西」兼顾两者。行号 refuted（实际 ingredients.lua:201）。 |
| hrq-00148 | entry-01201 | mod-tome.lua:13665 | fix | accepted | 是 | 独立核验通过；后半句「把头伸进去找它」为无据扩写；原文是「位置远在你能看见它们并活下来的地方之后」。收束到原信息量，并修正「它们/它」混用。advisory（Gemini 称生动）不影响结论；行号 refuted（实际 ingredients.lua:228）。 |
| hrq-00149 | entry-01205 | mod-tome.lua:13677 | fix | accepted | 是 | 独立核验通过；「其他蠕虫」为增译；get any knots out 只说解开缠结，不锁定是自身打结还是与同伴缠结（pending 主张不作依据）。按 hint 改为不锁定意象的「把缠结都解开」，与物品 desc「从一团同伴中分离出的单条蠕虫」兼容；refuted 的「矛盾」主张不采纳。 |
| hrq-00150 | entry-01210 | mod-tome.lua:13785 | fix | accepted | 是 | 独立核验通过；同一测试列表首项「实验品」与其余「试验品」不一致，统一为「试验品」。另一条 confirmed（格式标签与语义完整）为正面结论，无需修改。 |
| hrq-00151 | entry-01211 | mod-tome.lua:13840 | no_change | accepted | 否 | 无需修改；refuted：X 条「传送回来时」已表达第二次（返程）传送，second 未漏译。confirmed 与 advisory 均为正面评价。无需修改。 |
| hrq-00152 | entry-01214 | mod-tome.lua:14196 | fix | accepted | 是 | 独立核验通过；(1)「截然而止」误字，改「戛然而止」。(2) sullied by 是「被……玷污」，现译「厌倦了」语义偏移，改正。(3) 全文听众为复数 young acolytes（前文已用「你们」），末段改单数「你」，统一为「你们」。(4) 专名（安格利文、夏·图尔、永恒精灵、魔法大爆炸、埃亚尔）与术语库一致，正面结论，不改。 |
| hrq-00153 | entry-01215 | mod-tome.lua:14230 | fix | accepted | 是 | 独立核验通过；(1) base materials/components 译「基本元素」，与后文「埃亚尔元素」（Elements of Eyal）混淆，且以「他们」指无生命组分；改「基本成分」「它们」。(2)「明智的使用」应为「地」。(3)「作为……学生我假定」缺停顿，补逗号并还原原文感叹语气。(4) advisory「双刃剑」替换 good or ill：意义等价，不改。(5) pending：控制码 #{b |
| hrq-00154 | entry-01216 | mod-tome.lua:14450 | fix | accepted | 是 | 独立核验通过；开引号误用右双引号 U+201D，改为左双引号。另一 confirmed（解锁龙火陷阱，叙事与机制相符）为正面结论。 |
| hrq-00155 | entry-01218 | mod-tome.lua:14722 | fix | accepted | 是 | 独立核验通过；(1) 四处对话以右双引号 ” 开引（还是说你不够男人／快来吧／别抢了我的乐子／我已经记不清了），全部改为左引号 “。(2) 引号外重复标点：「？”，」「。”，」「”，」「？”。」「…”。」等共 6 处删去引号外多余逗号／句号，缺句末标点的引语补标点并改为规范的「引语＋说明」结构；顺带「杀的更多」→「杀得更多」、单个「…」→「……」。(3)「舞会开始了」缺句末标点，补句号。另拆成段一项成立（原文  |
| hrq-00156 | entry-01220 | mod-tome.lua:14814 | fix | accepted | 是 | 独立核验通过；逐条：(1) be no match to this 是「无法与之相比」，现译「宝剑干不了这种事情」曲解，改正并去掉原文无的「先生」。(2) Expecting someone else? 是「在等别人吗」（承接他误以为是莱娜尼尔），改正，并补 seeing the surprised look。(3) I wonder 在此表怀疑保留（后句说记录并不像神话那样结论分明），改「那可不好说」；「反转 |
| hrq-00157 | entry-01221 | mod-tome.lua:14988 | fix | accepted | 是 | 独立核验通过；逐条：(1) no normal day 被译反为「没有一天不处在危险之中」，并漏 day of reckoning，改为「绝非寻常的一天……清算之日」。(2)「希望的缰绳／扼住命运的咽喉／真正的和平」均无原文依据，收束为 hold the reins of fate in our palms 与 steady hand；同时补回被替换的 Our actions today will decide |
| hrq-00158 | entry-01222 | mod-tome.lua:15094 | fix | accepted | 是 | 独立核验通过；逐条：(1) 格式与控制字符配对正确，正面结论。(2)「已知依赖着」错别字，改「一直依赖着」。(3) 两处「！”，」冗余引号外逗号，删去。(4) head in my lap 译「抱着……脸庞」，改「把垂死爱人的头捧在膝上」。(5) crisis 译「毁灭」并加「瞬间」，改「希望已化为危机」。(6) burns 泛化为「创口」，改「烧伤处」；seeping freely 的「反向表达」refute |
| hrq-00159 | entry-01223 | mod-tome.lua:15168 | fix | accepted | 是 | 独立核验通过；逐条：(1) 格式控制符与段落结构正确，正面结论，换行数 65 未变。(2) this human 指 Cuilan 本人（If this human's tale / From what this human says），现译成「有关人类的事情」「那些人类说」，两处指代均改为「这个人类」。(3) none of this I knew 指当时对上述后续浩劫一无所知，现译「还不知道之后所发生的那些 |
| hrq-00160 | entry-01224 | mod-tome.lua:15300 | fix | accepted | 是 | 独立核验通过；本修订由 hrq-00160／hrq-00161／hrq-00162 三行共同引用，三行 claim 集合相同，逐条回应：(a)「床位」应为「床尾」——confirmed，源码 near the end of my bed，同回忆录第二章亦用 at the foot of my bed，改「床尾附近」（hrq-00162 主张，hrq-00160／00161 同列）。(b) 眼周皱纹特写被泛化且「 |
| hrq-00163 | entry-01225 | mod-tome.lua:15366 | fix | accepted | 是 | 独立核验通过；逐条：(1)「长着六肢的长而厚的身体之上」断裂病句，补出「头部连着一具……身体」。(2)「我面对着背后的怪物」方位矛盾、(3)「顺便跳进了我背后的门中」动作失真：原文 With my back to the opening... as I leapt backwards through the door，重写为背对门口、向后跃过门。(4) blade 译「刀片」，改「挥剑」。(5)「她冲破了她分开 |
| hrq-00164 | entry-01228 | mod-tome.lua:15875 | fix | accepted | 是 | 独立核验通过；本修订由 hrq-00164–hrq-00169 六行共同引用，六行 claim 集合相同，逐条回应：(a) 吸血鬼段增译与因果改写（hrq-00167 主线）——confirmed：It is for this reason 承接前文的氏族网络，「借助团体的力量」「自己的奴隶」「用钢剑刺穿喉咙」均为改写，按 hint 改为「正因如此……统治者……以冰冷的钢铁相待」，并补 in turn。(b)  |
| hrq-00170 | entry-01230 | mod-tome.lua:16072 | no_change | accepted | 否 | 无需修改；(1) 对应 elandar-1，正文与专名（生命之血、夏·图尔、安格利文、泰恩、盖里克）含义相符，正面结论。(2) 控制标签闭合、标点合理，正面结论。(3) advisory：#{italic}# 范围由 too 扩大到「理智得过了头」——中文无法只给「过」加斜体而不割裂词语，属排版取舍；调整标记范围亦触及 markup，本批不改。 |
| hrq-00171 | entry-01245 | mod-tome.lua:16538 | no_change | accepted | 否 | 无需修改；(1) 对应 keepsake-kyless-journal-2，正文、标签与心灵操控叙事准确，正面结论。(2) advisory：「发现了什么——」有不定代词直译痕迹，但 something...a dead man 的悬念语气由破折号保留，属二级文风偏好，不改。凯勒斯（Kyless）译名本身另有术语讨论，本条不涉。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
