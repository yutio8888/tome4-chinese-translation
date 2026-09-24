# 批阅裁决台账 — batch-05

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`e9548f9d181540946c930fac5d11a2cd4d97e82b07ced6b52dc1c13e1bf55f70`
- 决策行：40；冻结修订（含孪生载体）：40
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 38 |
| deferred | 2 |

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
| hrq-00172 | entry-01247 | mod-tome.lua:16562 | fix | accepted | 是 | 独立核验通过；整段确实交代凯勒斯抢强盗黄金并藏入洞穴；priceless 在他享受袭击的语境中译作“无比快意”成立，误译指控被反证推翻。“呆在一起”此处指停留，应写“待在一起”。 |
| hrq-00173 | entry-01252 | mod-tome.lua:16622 | no_change | accepted | 否 | 无需修改；全段人物、空气变化与攻击动作均已表达；末句原文虽用句号，译文省略号仅营造悬念，尚不足以证明情节或动作被改变。 |
| hrq-00174 | entry-01256 | mod-tome.lua:16683 | fix | accepted | 是 | 独立核验通过；第二段增加的单换行是纯静态分段，而且本批禁止改换行序列；末句“～。”叠用标点不合中文句末写法，删去波浪号。 |
| hrq-00175 | entry-01259 | mod-tome.lua:16826 | fix | accepted | 是 | 独立核验通过；前文已经写明半身人撤军，所以“欢庆胜利”有语境依据，但 peace 所指的和平状态仍未表达；“新建的游击力量”缩窄 military might。Army of Rogues 是引号中的军队名，“游击军”只说明战术，未传达 rogues；改其两次出现。职业双关没有固定源码证据，不以此定案；序号与二十／30 是纯格式差异。 |
| hrq-00176 | entry-01262 | mod-tome.lua:17299 | defer | deferred | 否 | Gaustadnes 现译“加斯塔德”没有译出末尾音节，但术语库与本仓均无该人名的既定完整译法；是否致敬像素画师也没有固定文本证据。专名须先确定读音及跨条目用法，不能凭模型推测补名。 |
| hrq-00177 | entry-01263 | mod-tome.lua:17473 | no_change | accepted | 否 | 无需修改；年份、样式和行序与原文相符；“先觉／察觉”保存 Foursaw／saw 的双关，不需修改。 |
| hrq-00178 | entry-01267 | mod-tome.lua:17570 | fix | accepted | 是 | 独立核验通过；条目名已译“无序之卷”，正文标题却用“无序之治”；tract 为篇章或小册，“治”既失词义也造成同一文本内不一致。“拾取变标题”的说法没有源码消费证据，但本条标题与条目名本身足以确认修复。 |
| hrq-00179 | entry-01270 | mod-tome.lua:17594 | fix | accepted | 是 | 独立核验通过；原文 nature could not have hoped to create such a race 是赞叹而非反问；现译“大自然怎么会创造”反转语气。Temple of Creation 在本仓同族译作“造物主神庙”，术语记录为 existing 而非 preferred，现译保持族内一致；“变的”应为“变得”。 |
| hrq-00180 | entry-01271 | mod-tome.lua:17598 | fix | accepted | 是 | 独立核验通过；德斯镇在后段狼毛句已经出现，不能说整篇完全漏译；但遭遇地点“德斯周围”在前段确实缺失。现译另加赤眼、吞噬生命和挥舞獠牙，删改了由普通狼、座狼到熊般巨狼的递进；末段 legends 指故事而非让野兽繁衍。 |
| hrq-00181 | entry-01272 | mod-tome.lua:17618 | fix | accepted | 是 | 独立核验通过；本仓 old forest 有 existing“古老森林”，现译“远古丛林”并非必改术语但本条可与同族对齐。原文是巨蚁始祖指挥甲壳幼虫，现译变成史前白蚁与蚁王，并臆造前颚碎尸；外观的臃肿、渗液与啁叫也失去。Such pluck and derring-do 漏了果敢讽刺。分段本身仅排版且换行受冻结保护。 |
| hrq-00182 | entry-01273 | mod-tome.lua:17637 | fix | accepted | 是 | 独立核验通过；“尽快告知最后的希望”已有加急之意，“加急快递”只是现代口吻，单独不构成一级缺陷；但原文没有粗口，也没有指明巨鸟，且“煽动”误用为动作词。两处段落拆分属纯排版。 |
| hrq-00183 | entry-01275 | mod-tome.lua:17677 | fix | accepted | 是 | 独立核验通过；nice and big 修饰下封信的字是否足够大，不表示字美；触手非人，用“他们”错误，lashed 指鞭打而非插入。独白拆段不改变内容且换行冻结。 |
| hrq-00184 | entry-01277 | mod-tome.lua:17714 | fix | accepted | 是 | 独立核验通过；profits 确是“收益／利润”的意象，单译“祖先保佑”抹掉了财运口吻；与 prophets 是否双关、罗尔夫是否矮人都缺固定证据，不作为修复依据。 |
| hrq-00185 | entry-01278 | mod-tome.lua:17728 | fix | accepted | 是 | 独立核验通过；正文已写威斯曼被腐化为怪物，因此“完全抹掉怪物”不是事实；但旁注 one-half of that abomination 明说老友成了怪物的另一半，现译“永远团聚”确实抹掉这一关键信息。“神智尽失”比 half-gone 更绝对。 |
| hrq-00186 | entry-01280 | mod-tome.lua:17737 | fix | accepted | 是 | 独立核验通过；“一瞬”是原译的主观时间停滞，并未断言真实时间极短，因此“极长反转为极短”说法过强；但 a century 的具体意象确实消失。后文“没有其它的人像你一样”保留了独一无二的解释，却未保留 Am I alone 的独处发问；改为“只有我一个人吗”。Alor? 无既定官方读音，保留既有阿洛。两处状语“温情的／大声的”改“地”。 |
| hrq-00187 | entry-01282 | mod-tome.lua:17791 | fix | accepted | 是 | 独立核验通过；叙述者前文已经表明是半身人，“我们”可由语境承接，故并非种族彻底失踪；仍可明确主体。same god 的“同一个上帝”引入特定宗教语感；other gods were responsible 指别的神创造其他种族，不是“其他创造者也很负责”。 |
| hrq-00188 | entry-01283 | mod-tome.lua:17826 | fix | accepted | 是 | 独立核验通过；“在埃亚尔两端”已保留位置，却未写姐妹仅隐约可见的月相；walk abroad 的外出禁令与盖里克外出动作大体承接前文，非核心完全漏译。两处 Aye 是叙事叹词，可补入以保留吟诵口吻；moonsister 只说明月亮姐妹而非女神，现译增设神格。 |
| hrq-00189 | entry-01286 | mod-tome.lua:17921 | fix | accepted | 是 | 独立核验通过；梦境确实清晰，但“刚睡醒脑袋一团浆糊”无原文依据；beyond 是在红星更远处，不是上方。held together 指维系这个世界，非“他们”。moonstone 单数且无“该死的”；shall wake up from 表未来醒来，非“早该”；lava spilled up 是岩浆向上涌出，非浮沉。 |
| hrq-00190 | entry-01290 | mod-tome.lua:17978 | defer | deferred | 否 | Cataclysm 的“大爆炸”与 Spellblaze 混淆；spellhunters 也已有本仓“魔法猎手”的明晰同族用法。但 mod-tome.lua:43240 起另有同源活跃孪生载体，仍译“大爆炸／猎魔者”；本批未冻结该 target，只改本条会制造族内不一致，须把两条一同纳入后续冻结。 |
| hrq-00191 | entry-01292 | mod-tome.lua:18000 | fix | accepted | 是 | 独立核验通过；段落与末尾换行、占位符均完整；图库纳／托拉克称号有本仓现译支持，术语 claim 仅有部分可核。“雇佣”擅自加入付款关系，enlisted the aid of 只说请求协助；改成“请来”。与第一章完全一致的主张缺逐项证据，不据此裁断。 |
| hrq-00192 | entry-01294 | mod-tome.lua:18019 | fix | accepted | 是 | 独立核验通过；钢铁王座、斯莱特和沃瑞钽已符合既有用法，段落引号完整；physical suffering 是肉体苦痛的承受，不是游戏机制的“物理抵抗能力”。halls of stone 是石造厅堂，“石头洞穴”改掉意象。 |
| hrq-00193 | entry-01296 | mod-tome.lua:18037 | fix | accepted | 是 | 独立核验通过；同段已用“永恒精灵”指 Shaloren，Shalore 原名写在括号里并不凭空丢掉种族信息；但 or 的“又称”关系未译，可直接补出。arcane arts 在长生研究语境中“魔法造诣”已含秘法，不判失义；引号体例差异仅风格。主要事件与段落完整，不等于不存在上述小遗漏。 |
| hrq-00194 | entry-01298 | mod-tome.lua:18055 | no_change | accepted | 否 | 无需修改；原文明确把 Thaloren 与 Thalore 放在同一括号作别称，现译“自然精灵（或木精灵）”仍清楚指同一种族；“木精灵”是否全库仅一处不足以证明读者会误认第二分支。术语表将 Thalore 记为 existing 而非 preferred，不强制改名；其余专名与段落无明确缺陷。 |
| hrq-00195 | entry-01302 | mod-tome.lua:18083 | fix | accepted | 是 | 独立核验通过；原文指精细铭刻促成手指灵巧，非“管理符文”；patient study 的耐心研习与 if properly motivated 的“有足够动机”都被泛化成技术水平和需要。“长老会”不是 Overseers 的监督职称；grain shipment 未说货船。段落和占位符完整；埃尔瓦拉无本批强制 preferred，不能以“全部专名合规”概括。 |
| hrq-00196 | entry-01306 | mod-tome.lua:18119 | fix | accepted | 是 | 独立核验通过；“其他理论——”已经引出后续说法，但未交代这些理论也有一定说服力；academic circles 泛指学界，非仅考古界。crucible race 的修饰在现译确未体现，但词义依上下文可能是关键历史种族，缺可核的专指依据，不猜定某种熔炉含义；先改前两项。 |
| hrq-00197 | entry-01308 | mod-tome.lua:18137 | fix | accepted | 是 | 独立核验通过；“攻击市民”把 communities 的聚居群体缩为城市居民；“更为敏捷的速度”与后文“移动迅速”重复 move faster，只留后者。towards the end of 是烈火纪末期，现译少时间限定；swinging limbs 失去摆动特征。 |
| hrq-00198 | entry-01310 | mod-tome.lua:18155 | fix | accepted | 是 | 独立核验通过；“另人”确是“令人”的错字。原文 those 指部分研究过久的龙战士，现译“那些……信徒”大体可追溯，但“只有……才会相信”把理论成因改成排他性信念；borne purely from 指理论可能纯由狂热妄想产生，需改回不确定语气。 |
| hrq-00199 | entry-01312 | mod-tome.lua:18235 | fix | accepted | 是 | 独立核验通过；原诗说孩童染病，不是患病孩童数量增长；renowned 是著名而非臭名昭著；zeal 指热忱，非问心无愧；末句 to Nature 指归于自然，现译只剩尘土。诗行和段序保持不变。 |
| hrq-00200 | entry-01313 | mod-tome.lua:18334 | fix | accepted | 是 | 独立核验通过；原文完整场景并未在别处补出异界色彩、余光边缘、阴影忽隐忽现、清醒梦中的清醒意识和心血来潮；“飞舞”只写运动不写隐现。省略号是修辞，不单列缺陷；Lucid Dreamer 是否被动天赋不能从此文推出，拒用该机制主张。 |
| hrq-00201 | entry-01314 | mod-tome.lua:18345 | fix | accepted | 是 | 独立核验通过；样式标签与三行换行均完整；Love, Eden 是艾登在信尾向收信人致意，现译“你钟爱的艾登”把爱慕方向改成收信人钟爱艾登。 |
| hrq-00202 | entry-01315 | mod-tome.lua:18375 | fix | accepted | 是 | 独立核验通过；flame secure bindings 只要求耐火的束缚物，没有指定胶布；删去臆造材质。破折号截断在原文中已表示未完成句，双侧包裹是排版建议；luminous horror 已按 preferred 译金色恐魔；“法罗”无固定术语或读音证据，保留待专名核定；清单缩进与样式未见破坏。 |
| hrq-00203 | entry-01316 | mod-tome.lua:18410 | fix | accepted | 是 | 独立核验通过；其余句子对反魔自然能量及警告的主要含义与排版均吻合；标题的 arcane abilities 指施法能力，现译“奥术能量”变成资源或能量，客观改变对象。 |
| hrq-00204 | entry-01317 | mod-tome.lua:18417 | fix | accepted | 是 | 独立核验通过；“他的主人”承接英雄装备所有者，未凭空引入另一主人；“亲眼所见的大半都当作神话”也保留了主观怀疑。其余有客观偏差：原文并列列举地宫、邪教与恶魔、饥饿森林和超时空力量，现译加具体剧情；most 被缩为年轻人，before all 是首要危险，too many 是泛指太多人而非直接指责读者。 |
| hrq-00205 | entry-01318 | mod-tome.lua:18444 | fix | accepted | 是 | 独立核验通过；现译整段已保留违规可获自由裁量的语境，但 fair game 不是“公平竞赛”，是可随意作为试验场的时段；a few decades 为几十年，once in a while 为偶尔。餐厅句“只有我们”增排他义；benefactor 单数；“被限制在于”句法杂糅。“一会儿谢”仅口吻生硬，非一级错误。 |
| hrq-00206 | entry-01319 | mod-tome.lua:18474 | fix | accepted | 是 | 独立核验通过；粗体句点位置与诗歌标点体例只是排版风格，斯派德与同 section 的装备译名相符，但全库完整一致性未核定。won’t claim me today 是说今天陷阱休想夺命，现译“仍未能”变成事后结果，丢掉决意。 |
| hrq-00207 | entry-01320 | mod-tome.lua:18509 | fix | accepted | 是 | 独立核验通过；前文确写它试图施法，但没有说“只能发出名字的声音”，不采这种额外剧情解释。末句 all he can manage is a corruption of his own name 指他施出的结果只是名字的扭曲，非“拥有堕落名字”；同一句“它／他”指代不统一。trivial 指其余材料容易取得而非品质太次；与红宝石价值的直接矛盾缺证据，不作理由。 原文明确称 Ruby of Eldoral，现译“艾德瑞尔之石”漏了红宝石材质，也一并补正； |
| hrq-00208 | entry-01321 | mod-tome.lua:18529 | no_change | accepted | 否 | 无需修改；前文明确 Shellsea 是村庄，现译“贝壳之海”是该村专名的语义译法；诗中“记住她”“将她淹没”承接村庄拟人，未误认普通海域。无官方读音或术语 preferred，不凭模型改名；诗句标点不齐属风格。 |
| hrq-00209 | entry-01326 | mod-tome.lua:19079 | no_change | accepted | 否 | 无需修改；两处省略号后确比第三处多一个静态空行，原文段落相同结构；但这是纯静态排版差异，本批又禁止改变换行序列，不据此改 target。 |
| hrq-00210 | entry-01328 | mod-tome.lua:19211 | fix | accepted | 是 | 独立核验通过；诗中前半写 wyrms 与 drakes，后半改说在沙下隧道循 giant worms；把虫译成“沙龙”混同龙类，破坏两组意象对照。即使不采同节另两处的未经冻结引文，词义和本诗上下文已足够判定。 |
| hrq-00211 | entry-01331 | mod-tome.lua:19358 | no_change | accepted | 否 | 无需修改；外层直单引号换中文双引号只改变引文呈现，异语音节、内部直单引号和样式标签均保留；本 section 引号体例混杂，单行不能建立必须统一的规范。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
