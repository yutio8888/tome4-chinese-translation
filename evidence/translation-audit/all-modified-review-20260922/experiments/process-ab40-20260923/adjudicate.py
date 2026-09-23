"""Host judgments, separate from immutable participant reports and preregistered scorer."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
entries=json.loads((P/'entries.json').read_text()); E={x['audit_id']:x for x in entries}
canonical=json.loads((P/'HOST-INITIAL.json').read_text())['claims']
R={c['id']:c for c in canonical}
revisions={
'H05':('advisory','整段仍在否定祖先明确告诫兽人的危险；原判把否定作用域中的比喻当独立肯定事实。该转述可保留未作警示的意思，不确认主体反转。'),
'H14':('pending','battleaxe 在游戏中可能对应具体双手武器类别；没有获准对应实体证据，不仅按一般词义判错。'),
'H16':('advisory','后句为倒在烈火之刃下，近身战斗可承接当前情景；不足以确认对远程战斗另作错误声明。'),
'H23':('advisory','废墟也可作荒废地域描写；初判将其严格等同建筑残骸过强，尚无地貌冲突证据。'),
'H44':('advisory','在任何报告返回之前已撤销：同一护符名为 Gardanion, the Light of God；穿戴语境可用名称呼应其光辉。')}
for key,(status,why) in revisions.items():R[key].update(status=status,text_status=status,revision_reason=why)
def new(id,entry,status,source,target,reason,counter,impact='叙事事实'):
    e=E['entry-'+str(entry)]; c=dict(id=id,entry=e['audit_id'],status=status,source_quote=source,target_quote=target,reason=reason,strongest_counterevidence=counter,impact=impact,evidence={'section':e['section'],'frozen_pair':'entries.json#'+e['audit_id']},text_status=status,target_applicability='Frozen text/context only; unpinned Orcs or unavailable Possessors implementation does not establish a target release.')
    canonical.append(c);R[id]=c

# Non-H claims below retain exact candidate anchors and explicit host counterarguments.
new('N01','03841','advisory','entity it detonates against','引爆所波及','报告推定 against 只指碰撞命中，证据不足。','爆炸对目标引爆与波及目标有可接受交集；原广告没有 direct hit 或碰撞/范围对立。')
new('N02','03857','confirmed','Assessment of the Species','关于人种的调查','物种调查被收窄成人种。','同文件 misc.lua:136 系列另一章是 Steam Giants，支持跨物种分类。')
new('N03','03862','advisory','shards of your ruined cities','文明的废墟','整个人群覆灭的威胁中，文明废墟可作城市废墟的借代。','不据比喻转述推断实际搜寻范围扩大。')
new('N04','03867','confirmed','Aeryn relented','艾琳被击败了','罢手行为未表达；不确认胜负对象反转。','英文 winner 代词存在上游歧义；被打败本身不表达罢手，故仅保留遗漏这一子项。')
new('N05','03868','confirmed','Scourge from the West','西方灾星','违反本包明确适用的 preferred 称号。','terms.json society.tsv:34，_t/preferred/dlc，与本条完全匹配并明确排除灾星。')
new('N06','03893','advisory','wall %d units long','一堵墙长 %d','补单位和调整语序可改善清楚度。','已给墙长与持续时间两个独立参数，无证据表明读数被当成其他物理量。','表达建议')
new('N07','03734','advisory','WASTE YOUR SHOT','浪费子弹','确认提示中的惯用语成立。','子弹一词不承诺能补充弹药；一次性源码不能证明中文新增可重复使用。')
new('N08','03770','advisory','corrupted cave door','被污染的山洞门','术语候选不是此 tag 的强制要求。','entity subtype 与 entity name 不同；污染与腐化在此门名可作一致性建议。','表达建议')
new('N09','03862','confirmed','relations with our now-distant kin','谈论过与我们今日的远亲风暴部族','与字结构缺中心语关系，语法残缺。','不是单纯省略连词；谈论过与某部族不能独立完成宾语。','表达建议')
new('N10','03862','confirmed','recorded in a matter-of-fact nature','确实完全实事求是的','缺判断词是，句尾的悬空。','可改为确实完全实事求是或确实是…的；现句不成立。','表达建议')
new('N11','03862','confirmed','yearly messages','在于在一条在','重复介词导致句法断裂。','该句同时存在年度信息内容问题，语法另计，未以标点风格判错。','表达建议')
new('N12','03862','advisory','yearly messages','一条…年度总结信息','周期性仍由年度保留，不独立确认从每年变成一次。','具体化为总结已归 H08；不重复计入数量丢失。')
new('N13','03866','confirmed','when a skeletal warrior struck her','这是，一个骷髅战士','这是应为这时，明确错字。','读者可猜到不等于文字无错。','表达建议')
new('N14','03866','confirmed','lost his bearings','失去平衡','失去方向感改成失衡。','抛掷可能同时造成失衡，但不能替代踩错方向的叙述。')
new('N15','03867','confirmed','on … way to challenge the grand magus Vor','与大魔导师沃尔的战斗','途中风暴被放进与沃尔的战斗。','都在部落内不消除事件阶段差别。')
new('N16','03867','confirmed','danger they were in','出于怎样的危机','出于误作处于，明确错字。','不按专名间隔点另计缺陷。','表达建议')
new('N17','03867','advisory','Maj\'Eyal','马基埃亚尔／马基·埃亚尔','同名间隔点一致性建议。','两种字形都明确指同地；scope=core不绑定DLC，不能改称内部一致性后变相强制。','表达建议')
new('N18','03867','confirmed','corrupted horrors of Yiikgur','占据伊克格的恐魔','遗漏恐魔受到腐化的限定。','占据地点未表达腐化状态。')
new('N19','03867','confirmed','dragon-tamers … master wyrmics','驯龙师和高阶龙战士','同位身份被拆成两类并列人物。','和在此没有即的同位释义。')
new('N20','03867','confirmed','without a thought to where it led','没有任何犹豫','未考虑目的地被泛化为不犹豫。','不犹豫也可能已知目的地；紧接未知传送场景不能自动补回该心理信息。')
new('N21','03867','confirmed','at her orders','冲进了传送门中','奉艾琳命令这一行动来源遗漏。','前文艾琳在场不等于她下令。')
new('N22','03868','confirmed','<? if Lore.pocket_time_winner.sacrifice then ?>','站在了巅峰之上，，从而','非牺牲分支产生双逗号，静态展开可重现。','这是实际重复字形而非要求原译标点一一相同；低影响显示文字错误，不称游戏崩溃。','表达建议')
new('N23','03868','advisory','it / its','他／它','对拟人神灵的代词一致性建议。','指代仍唯一；他/它切换不证明性别、身份或作用主体改变。','表达建议')
new('N24','03868','confirmed','whenever it found or created a threat','直到它找到或者创造了','再次遇到威胁时想起他，被写成只记到某个终点。','愿意牢记直到找到虽保留承诺，但未保留原来的条件关系。')
new('N25','03870','confirmed','also happen to be decent people','碰巧上是好人','碰巧上是含衍字。','不影响大意仍属明确文字错误。','表达建议')
new('N26','03870','confirmed','significantly more credibility','更加可信地多','地应为程度补语的得。','不是措辞偏好。','表达建议')
new('N27','03870','confirmed','rogue mages','游荡法师','失控或脱离约束的法师被改为移动状态。','反魔训练语境关注行为约束，不是法师是否游历。')
new('N28','03870','confirmed','attacks on Ziguranth patrols','对伊格兰斯巡逻队的搜捕','袭击变为搜捕。','两者受事相同，否决报告所谓施受反转，仅确认行动性质差别。')
new('N29','03870','confirmed','the old guard','过去的守护者','守旧派/元老派被当成昔日守护者。','与年轻自然精灵涌入并列构成派系代际对照。')
new('N30','03870','confirmed','alongside widespread acceptance of runes','而没有意识到早在更早之前','并列原因被添加为未察觉的认知状态。','前文忽视政治趋势不等于此处已有认知失败。')
new('N31','03870','confirmed','mumbo-jumbo about the heavens','有关天空的一系列繁文缛节','胡言说辞变成繁琐礼节。','包装奥术的论说不等于进行仪式；同句没有礼节证据。')
new('N32','03870','advisory','the raid on Zigur','伊格被摧毁／对伊格的袭击','袭击及破坏结果的转述需一致性改善。','不凭孤立词推翻事件中已可能包含的摧毁结果；缺固定事件范围证据。')
new('N33','03870','advisory','CAN','[b]真的可以[/b]','大小写强调转为有效粗体，未破坏信息结构。','不按标记集合机械相等判错。','表达建议')
new('N34','03877','advisory','entire recorded history','整个历史','历史记录语境可概括为整个历史。','无证据引入未记载时代，补有记载以来仅提高清楚度。')
new('N35','03915','confirmed','The wheels of death! Amazing!','冲锋！死亡之轮！！','赞叹真棒被改为冲锋命令。','不是感叹号数量问题；不同话语行为，低影响风味偏差。')
new('N36','03923','advisory','superheated steam','蒸汽冲击波…火焰伤害','过热可由火焰伤害及后句更高温语境承接。','未额外指控基础波是冷蒸汽；可补词但不足确认错误。')
new('N37','03955','pending','last 5 turns','持续5回合','上游时长与快照 summon_time=8 不符。','忠实沿袭，不进入译文缺陷分母；目标版本未固定。','机制/操作')
new('N38','03962','pending','cannot be used on rares','稀有…无效','报告指出上游等级过滤疑点，需目标版本及rank语义核实。','即使成立也非中文新增；不以模型声称rank=3直接判定。','机制/操作')
new('N39','04078','confirmed','several vital spots','重要部分都','若干要害扩大为全部要害。','都的全称在此明确；非一般无类型限定伤害的既有豁免。')
new('N40','04078','advisory','its','它／他','雪人代词一致性建议。','角色身份未变，不确认另一个对象。','表达建议')
new('N41','04121','advisory','mainhand weapon and an offhand mindstar','主手武器副手灵晶','可补和或顿号，现有并列可读。','主手/副手明确分隔，两项需求均在，不能凭缺连词判语法不成立。','表达建议')
new('N42','04119','advisory','strange and may be confusing to play for beginners','机制相当奇怪，可能不适合新手使用','警告语境中的合理意译。','奇怪机制与可能不适合的完整句保留新手难掌握的警示；不等于禁止新手。')
new('N43','04127','pending','When you assume a form','吞噬一具储备的身体，用来补充现在的身体','使用附身形态的限定明确度不足，原有当前身体也可承接。','无源码不能把 when assume 锁定为换身瞬间的唯一触发；先待确认，否决必然自动吞噬推断。','机制/操作')
new('N44','04127','pending','As such may things that prevent healing','阻止治疗的效果无法阻止吞噬生效','may疑为many，范围及实际豁免待核。','源句有误且缺组件源码；不将 many 推断直接升格为目标版本错误。','机制/操作')
new('N45','03866','advisory','Dazed and stumbling','因震慑而失去平衡','叙事一般形容词不足以证明两种游戏效果混淆。','effect subtype术语不匹配_t叙事，global不是所有语义和tag均强制。','表达建议')
new('N46','03866','advisory','a couple of them / as his friend was cut down','几个兽人／在朋友被砍倒后','couple可作少数；as在紧接事件中可译随着/当…，未证严格同时性。','不把一般事件连接硬解为可测时间并发。')
new('N47','03866','advisory','The Master','吸血鬼领主／领主','增补身份与简称共存可接受。','报告自身认可身份正确；不以两个长度不同的称谓强迫同名。','表达建议')
new('N48','03866','confirmed','battling waves of shambling undead','与一波波蹒跚的不死生物而战','与…而战搭配不成立。','可作与…战斗或为…而战；当前混合结构有误。','表达建议')
new('N49','03866','advisory','multi-hued wyrms','七彩龙','七彩可作多色惯用语，不承诺恰有七色。','entity subtype候选不得强加于_t叙事；不绕过tag限制。','表达建议')
new('N50','03868','advisory','in <?=Lore.pocket_time_winner.hisher?> legend','传说中的西方灾星','完整末段明确是同一传奇人物，省略所有格不改变所指。','模板代词可按中文省略；不是位置格式参数错位，不按变量个数判错。','表达建议')
new('N51','03867','confirmed','awaited … in the tower of High Peak','在那里等待着的','牺牲分支首次地点高塔名称遗漏，那里缺先行词。','未显示另一非牺牲分支的准备进攻高塔段；后句高塔只给类型，未给专名。')
new('N52','03867','confirmed','what orcs are best known for','以兽人中最强大的力量著称','兽人整体以蛮力著称改成该部落在兽人中最强。','强度的比较群体改变，不是主语省略。')
new('N53','03867','confirmed','orcs stood … at Grushnak Pride','格鲁希纳克部落的精英部队','增加精英部队身份。','部落强大不等于原句确认精英身份；只确认文本新增。')
new('N54','03868','advisory','reclaimed Sher\'Tul fortress','夏·图尔要塞','全文前段已说明主角夺回要塞。','所属对象已明确，同篇回指可压缩修饰；不单独计遗漏。')
new('N55','03868','confirmed','citizens of Eyal','埃亚尔的世界','受害对象居民泛化为世界。','可能伤害世界也影响居民，不代表同一断言。')
new('N56','03868','confirmed','often with difficulty','有时艰难取胜','经常艰难的频度被降为有时。','与sometimes/occasionally形成明确频度对照；低影响仍有可证区别。')
new('N57','03868','confirmed','room left for the rest of … life','故事就此走到了尽头','故事不给人物余生留空间的信息未保留。','前句故事结束被重复，未保留人仍有余生的对照。')
new('N58','03870','confirmed','intimidation can get us anywhere','暴力威慑是不能解决一切问题的','恐吓已无进展改成不能解决所有问题。','不能解决一切允许部分有效，与原文的阶段判断不同。')
new('N59','03870','confirmed','allowed the idea … to survive','我们高举着…旗号…幸存下来','存活的对象由理念变成组织成员。','高举理念不表达使理念免于消失，组织生存是另一个命题。')
new('N60','03870','advisory','further refine our techniques','进一步锤炼自己…能力','教授我们的技法与精进学习者能力在课程语境可等价。','不足据所有格不同确认受益对象错误。')
new('N61','03870','advisory','old guard has been overrun with','被…所代替','新人占主导可概括为旧派被替代。','未必断言每个旧成员离开；旧派译词问题已单列N29。')
new('N62','03870','advisory','damage magic may inflict','魔法所造成的伤害','中文所造成可泛指潜在/一般结果。','没有时间词表明已经发生；不能仅因无may判事实化。')
new('N63','03870','confirmed','will make it more capable of resisting','更加强大，才能抵挡','提升抵抗能力被改成必要条件。','才能比更能的逻辑强度更高；仅文本设定，不夸为游戏机制。')
new('N64','03874','advisory','no one of them','没人','上句众神提供了量词范围。','不合理地把中文没人脱离紧邻主语扩大到整个宇宙。')
new('N65','03874','advisory','ire of the universe, of fate itself','天怒人怨，被命运所诅咒','拟人化厄运的意译成立。','命运诅咒可作比喻；不必等于下段特定时空法术的实然断言。')
new('N66','03874','advisory','Or maybe … powerful enough to put','或者我们只是激怒了…给我们施加了','或许假说仍统摄全句，未变为确定事实。','不能将局部给…施加从或许作用域中割离。')
new('N67','03874','advisory','carry it deep within ourselves','在自身的存在中也一直传承下来','种族承载创造者情绪的完整段允许传承意象。','宾语可以承上文憎恨等，不证明新增特定代际事件。')
new('N68','03915','advisory','two sentences / line breaks','合并两句','换行/并句不构成独立缺陷。','主动取消信息遗漏已H40计，不重复把同一问题按换行计数。','表达建议')
new('N69','03923','advisory','(current factor %d%%)','当前强度系数 %d%%。','括注另起一行仍明确补充前句。','未丢参数、范围或层级，规则禁止按换行数判错。','表达建议')
new('N70','03923','advisory','radius %d','半径 %d','原文也没有单位，参数语义相同。','不能以另一条有单位强判本条漏译。','表达建议')
new('N71','03932','advisory','evade/are missed by','闪避或躲闪','攻击未命中在中文可说被躲闪。','报告未查callback且主动/被动语言不等于两种互斥机制；没有证据证明排除miss路径。','机制/操作')
new('N72','04078','advisory','reinforced with stralite plating','被斯莱特装甲所覆盖','装甲覆盖表达防护加强，可接受。','若干→全部另计N39；不将防护同义描写另拆。')
new('N73','04119','advisory','BEWARE: This class is very strange','注意: 该职业机制相当奇怪','注意及机制是警告语境合理表达，半角冒号不构成缺陷。','不以强度感受或标点风格自动确认。','表达建议')
new('N74','04127','advisory','you may cannibalize','吞噬一具储备的身体','技能说明动词直陈不等于必然自动触发。','may为可选操作，标题/技能说明语境允许此语法，不额外确认意愿变化。','机制/操作')
new('N75','04127','advisory','separate final sentence','吞噬是治疗身体的唯一方法。','合段仍保留唯一方法的独立完整句。','不按换行行数推断信息损失。','表达建议')

observations=[]
def add(stage,id,status,refs,reason=None):
    ids=refs.split() if isinstance(refs,str) else refs
    states={R[k]['status'] for k in ids}
    decision='accepted' if 'confirmed' in states else 'pending' if 'pending' in states else ('refuted' if status=='confirmed' else 'advisory')
    o=dict(stage=stage,id=id,source_status=status,host_decision=decision,canonical=ids)
    if decision=='refuted':o['false_cluster']='F-'+('+'.join(sorted(ids)) or stage+'-'+id)
    if reason:o['reason']=reason
    observations.append(o)

def table(stage,text):
    for line in text.strip().splitlines():
        id,status,refs=line.split('|');add(stage,id,{'c':'confirmed','p':'pending','a':'advisory','r':'refuted'}[status],refs)

new('N76','03740','advisory','at will','具有召唤他的能力','玩家得到可发动的召唤能力允许主动使用的读法。','不另确认无限次或强制触发；持续数回合和永久绑定分别单列。','机制/操作')
new('N77','03866','pending','bone armor','骨盾','骨甲与骨盾是否对应既有技能名待核。','未获准对应定义，不能以武器/护甲一般词典义覆盖游戏命名。')
new('N78','03866','confirmed','while leaving his hands free','灵能的潜力来在空中挥舞法杖','悬空操杖同时解放双手的信息遗漏。','前文徒手格斗能力不等于本动作仍保持双手空闲。')
new('N79','03866','confirmed','master a few of these','在这些方面都有了一些实战经验','掌握其中几项被改成各方面只有一些经验。','不是只删程度副词，熟练程度和涉及能力集合均改变，合计为能力状态一项。')
new('N80','03866','advisory','a pair of earthen missiles','一双石弹','量词生硬，但两枚含义仍在。','可改两发；不指控数值或对象错误。','表达建议')
new('N81','03867','pending','fight by hisher side','与<?=Lore.pocket_time_winner.hisher?>并肩作战','所有格模板值是否自带的需核对中文取值。','缺本地化短串，不能断言实际渲染一定语病；变量个数不单独判错。','机制/操作')
new('N82','03870','confirmed','they found themselves sliding into irrelevance','不知道自己已经变成了无关紧要的局外人','落入边缘状态被增写成不知道该状态。','found themselves 不必强调主动察觉，但也不表达不知道；具体认知否定是新增信息。')
new('N83','03870','advisory','If … then …','既然…淡忘。…那么，','跨句条件结构略拗口但完整逻辑仍在。','不按句号位置机械判残句。','表达建议')
new('N84','03870','confirmed','These allies will help us support Nature','这些盟友对我们在保护自然事业上的支持达到了','未来预期帮助被写成已达到的支持。','已拥有盟友不等于原文承诺的帮助已实现。')
new('N85','03976','advisory','it will vaporize','子弹…将气化','it所指有歧义，湿润被移除的实现不能证明作者只指水。','译文动作与爆炸关系成立，未固定实现也不决定叙述主语唯一读法。','机制/操作')
new('N86','03932','advisory','Using small engines','开启引擎','反射强化语境保留引擎作用，尺寸小可补充。','不按每个修饰词机械计遗漏。')
new('N87','03866','advisory','as his friend was cut down','在他的朋友被兽人战士砍倒后','as 在紧接的逃亡事件中可承接当时/随着，不足以确认可测的严格同时关系。','报告把一般事件连接词硬解为同时触发；这是时序明确度建议。')
R['N46'].update(source_quote='a couple of them',target_quote='几个兽人',reason='couple 可在非计量叙事里泛指少数，几个是合理读法。',strongest_counterevidence='没有场景人数判定或后续数量对照锁定恰为二。')

table('P','''C01.1|c|H02
C01.2|c|N76
C02|c|N01
C03|c|N02
C04|c|H04
C05|c|H06
C06|c|H08
C07|c|N03
C08|c|H15
C09|c|H27
C10|c|N04
C11|c|N05
C12|c|H33
C13|a|H36
C14|c|H38
C15|a|N06
C16|c|H40
C17|c|H42
C18|c|H43''')


table('A2','''C01|c|N07
C02.1|c|H01
C02.2|c|H02
C02.3|c|N76
C03|c|H03
C04|p|N08
C05|a|
C06|c|N02
C07|c|H04
C08|c|H06
C09|c|H07
C10.1|c|N09
C10.2|c|N10
C10.3|c|N11
C10.4|c|H08
C10.5|c|N12
C11|c|H09
C12|a|N17
C13|c|H13
C14|c|H15
C15|c|N13
C16.1|a|H11
C16.2|a|N14
C17|a|N49
C18.1|c|H21
C18.2|c|H22
C19|c|N15
C20|c|H27
C21.1|c|N16
C21.2|c|N17
C22.1|c|H20
C22.2|c|N18
C23.1|a|N19
C23.2|a|H23
C23.3|a|N20
C23.4|a|N21
C23.5|a|H26
C24|c|N22
C25|c|N05
C26|c|H28
C27|c|N23
C28.1|a|H30
C28.2|a|N24
C29|c|H32
C30.1|c|N25
C30.2|c|N26
C31.1|c|N27
C31.2|c|N28
C31.3|c|N29
C32.1|c|H34
C32.2|c|N30
C33.1|a|N31
C33.2|a|N32
C33.3|a|N33
C33.4|a|N83
C34|a|
C35.1|c|H37
C35.2|c|H36
C36|a|N34
C37.1|c|H38
C37.2|c|
C38|a|N06
C39|a|
C40|c|H40
C41.1|a|N35
C41.2|a|
C42|a|N36 N69
C43|a|N37
C44.1|a|
C44.2|a|N38
C45|a|H41
C46|c|H42
C47.1|c|H43
C47.2|c|N39
C48|a|N40
C49|c|H44
C50|a|
C51|c|N41
C52|c|N42
C53|p|H45
C54.1|c|N43
C54.2|c|N74
C55|p|N44
C56|a|N50 N81
C57|a|''')

table('B2','''C01|c|N01
C02|a|
C03|c|H06
C04|c|H07
C05.1|c|N12
C05.2|c|H08
C05.3|c|N11
C06.1|c|H09
C06.2|c|
C07|c|N17
C08|c|N09
C09.1|c|N10
C09.2|c|
C10|c|N45
C11|c|H13
C12.1|c|H10
C12.2|c|N46
C13|c|N87
C14.1|c|H11
C14.2|c|N14
C15|c|N47
C16.1|c|N13
C16.2|c|N48
C17|c|N49
C18|c|H15
C19|c|N50
C20|c|N05
C21|c|H21
C22|c|N51
C23.1|c|H27
C23.2|c|
C24|c|N17
C25|c|H20
C26|c|N15
C27|c|N19
C28.1|c|N52
C28.2|c|N53
C29|c|H23
C30.1|c|N20
C30.2|c|N21
C31|c|H24
C32|c|N22
C33|c|H28
C34|c|N24
C35.1|c|H30
C35.2|c|N54
C36.1|c|H29
C36.2|c|N55
C37|c|N56
C38|c|N57
C39|c|N23
C40|c|H32
C41|c|N58
C42|c|H34
C43.1|c|N59
C43.2|c|N28
C44.1|c|N60
C44.2|c|N27
C45.1|c|N29
C45.2|c|N61
C46.1|c|N62
C46.2|c|N63
C47.1|c|N25
C47.2|c|N26
C48|a|N33
C49|a|
C50|a|
C51|c|H36
C52.1|c|H37
C52.2|c|N64
C53|c|N65
C54|c|N66
C55|c|N67
C56.1|c|H38
C56.2|c|H39
C57|c|N06
C58|a|N06
C59|a|
C60|a|
C61|c|H40
C62|c|N68
C63|c|N35
C64|a|
C65|c|N69
C66.1|c|N70
C66.2|c|N36
C67|a|
C68|c|N71
C69|a|N86
C70|a|N85
C71|c|H42
C72|c|H43
C73.1|c|N39
C73.2|c|N72
C74|c|N40
C75|c|N42
C76|c|N73
C77|a|
C78.1|c|N43
C78.2|c|N74
C79|c|N44
C80|c|N75
U01|a|N03
U02|a|N77
U03|a|H17
U04|a|N78
U05|a|N79
U06|a|N80
U07|p|N81
U08|p|N04
U09|a|H26
U10|a|H22
U11|a|H25
U12|a|N16
U13|a|N31
U14|a|H33
U15|a|N82
U16|a|N30
U17|a|N32
U18|a|N83
U19|a|N84''')

for o in observations:
    if o['stage']=='A2' and o['id']=='C37.2':o.update(host_decision='refuted',false_cluster='F-A2-C37.2',reason='括注紧接正常的休息值，其参数归属可由原译相同结构承接。')
    if o['stage']=='B2' and o['id']=='C06.2':o.update(host_decision='refuted',false_cluster='F-B2-C06.2',reason='抱着意图虽生硬，但宾语与承接主语都在，未证句法残缺。')
    if o['stage']=='B2' and o['id']=='C09.2':o.update(host_decision='refuted',false_cluster='F-B2-C09.2',reason='their boorish behavior 在本段讨论true nature语境下可作本性中的粗野举动；不独立确认新增人格本质判断。')
    if o['stage']=='B2' and o['id']=='C23.2':o.update(host_decision='refuted',false_cluster='F-B2-C23.2',reason='完整条目已明确两位法师要举行仪式，补法师们有同文依据。')

from b3_adjudication import extend
extend(globals())

def save():
    # Replace abbreviated draft anchors with byte-exact frozen excerpts; judgments unchanged.
    exact={
      'N15':{'source_quote':'way to challenge the grand magus Vor'},
      'N16':{'source_quote':'they were ever in danger'},
      'N19':{'source_quote':'the dragon-tamers of Gorbat Pride, master wyrmics'},
      'N20':{'source_quote':'Without a thought to where it led'},
      'N22':{'target_quote':'站在了巅峰之上，<? if Lore.pocket_time_winner.sacrifice then ?>通过牺牲<?=Lore.pocket_time_winner.himher?>的生命来关闭了法师的远行传送门<? end ?>，从而'},
      'N48':{'source_quote':'Climbing through the waves of shambling undead'},
      'N51':{'source_quote':'in the tower of High Peak'},
      'N53':{'source_quote':'orcs stood in'},
      'N57':{'source_quote':"room left for the rest of <?=Lore.pocket_time_winner.name?>'s life"},
      'N59':{'source_quote':'allowed the idea of supporting Nature over magic to survive','target_quote':'我们高举着“自然胜过魔法”的旗号，从联合王国与晨曦之门的条约、对伊格的袭击，以及对伊格兰斯巡逻队的搜捕中幸存下来'},
      'N78':{'target_quote':'一种在空中挥动法杖的心灵潜能'},
    }
    for id,fields in exact.items():R[id].update(fields)
    for c in canonical:
        if c['status']=='confirmed':
            assert c['source_quote'] in E[c['entry']]['source'],c['id']
            assert c['target_quote'] in E[c['entry']]['target'],c['id']
    result={'entries':list(E),'canonical':canonical,'observations':observations,'reference_limit':'Host-adjudicated comparison, not human gold; all initial and participant files immutable.','host_revisions':revisions}
    (P/'ADJUDICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':save()
