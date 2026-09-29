"""Host observations recorded before reading participant reports; immutable after freeze."""
import datetime, hashlib, json
from pathlib import Path
P=Path(__file__).resolve().parent
entries=json.loads((P/'entries.json').read_text());byid={e['audit_id']:e for e in entries}
anchors={e['entry']:e for e in json.loads((P/'HOST-ANCHORS.json').read_text())}
rows=[]
def add(n,en,zh,reason,counter,status='confirmed',impact='叙事事实'):
    key='entry-'+str(n).zfill(5);e=byid[key]
    assert en in e['source'],(key,en,'source')
    assert zh in e['target'],(key,zh,'target')
    rows.append({'id':f'H{len(rows)+1:02d}','entry':key,'source_quote':en,'target_quote':zh,'reason':reason,'strongest_counterevidence':counter,'status':status,'impact':impact,'evidence':anchors[key],'text_status':status,'target_applicability':'Textual comparison of frozen input; implementation-dependent applicability remains unpinned/unavailable.'})

add(3740,'binding John to it forever','将约翰绑定到戒指上','永久绑定的时间限定遗漏。','绑定可以暗示持续，但未明确永久；后句只涉及召唤。')
add(3740,'summon him for a few turns at will','戒指现在具有召唤他的能力','召唤仅持续数回合的限制遗漏。','仍有召唤能力不等于保留持续时限；不另外指控无限次或随意使用。',impact='机制/操作')
add(3744,'consider you a customer for now','将你视为顾客','暂时视为顾客的限定未直接保留。','后句违法即受攻击表达条件性接待；宜澄清，不必确认永久接待误述。','advisory','表达建议')
add(3858,'had already caught fire','突然着火了','被拉入之前已着火，改成拉入时突然着火。','读不完标题的结果保留，不消除火起时序变化。')
add(3862,'a pitiful, fallen reminder','也没有留下一个可悲的警示','原文说兽人本身是堕落的警示；中文说祖先没有留下警示，改变对象关系。','段落仍说未直接劝告，但没有保留对兽人这一对象的评价。')
add(3862,'mercifully brief reign','短暂的仁政','庆幸统治短暂误成仁慈的统治。','不是仁慈君主的独立设定，mercifully修饰brief。')
add(3862,'After a brief description of the events of the meeting','简短地讨论了几件事后','正史简述会面变成会面前讨论事件。','后句仍讲会面，却不能把记录层的description变成场景里的discussion。')
add(3862,'yearly messages','年度总结信息','每年来信被具体化成年度总结。','年度保留频率，但总结额外限定了消息内容。')
add(3862,'least of all ourselves','这不可能对任何人有好处','尤其不利于自己的比较限定遗漏。','任何人包含自己，但不表达自身最受害的程度比较。')
add(3866,'ran face-first into a couple of them','直接向几个兽人正面冲去','逃跑时迎面撞上兽人改成朝兽人冲去。','正在逃跑的前句使主动冲锋读法可疑，但中文朝目标冲去仍改变碰上事件。')
add(3866,'tossed him around his lair','在他的巢穴里把他扔了出去','在巢穴内反复抛掷改成扔出去。','扔的动作保留，空间方向和活动方式未保留。')
add(3866,'swearing incomprehensibly about unfairness','发表了一番关于不公平的费解的话','骂骂咧咧的说话方式未保留。','费解保留难懂，不保留swearing的辱骂语气。')
add(3866,"right where she'd applied a wild infusion",'当她想用她仅有的那一个狂暴纹身时','击中纹身所在部位改成在尝试使用纹身时击中。','后句也尝试使用纹身，但不能代替原句的具体命中部位。')
add(3866,'battleaxe','双手斧','不限定握持方式的战斧被指定为双手斧。','角色还使用长剑；battleaxe词本身不能证明双手武器。')
add(3866,'salivated at the prospect of traveling','他旅行到远东','对未来赴远东残害兽人的期待变成已经赴远东并看到的事件。','后文确实到达远东，但不能反向抹掉此句当时的期待视角。')
add(3866,'direct combat','近身战斗','正面战斗缩为近身战斗。','烈火之刃提示近战场景，但原文比较的是直接作战适应性。')
add(3866,'a demonic statue called out to her','当她看到一个恶魔雕像时','雕像主动呼唤的事件被看到雕像取代。','看到可以与呼唤并存，但中文没有表达雕像发出呼唤。')
add(3866,'effortlessly destroying any foe','秒杀所有遇到的敌人','轻松消灭被限定为瞬间击杀。','秒杀可以夸张表达强大；是否构成实质时序限定宜保守，先记表达建议。','advisory','表达建议')
add(3866,'wild infusion','狂暴纹身','术语候选野性纹身为core/entity name，本条DLC/_t不直接匹配；语义指称仍需中文映射。','不能凭该不适用术语行强制改名；缺可适用的同一技能中文映射。','pending')
add(3867,'a mere stepping stone on the way','作为下一步攻入恐惧王座的据点','旅程中的过渡成就被具体化为攻城据点用途。','获得堡垒确实先于攻塔，但未证明把它作为军事据点。')
add(3867,'in centuries','那是和马基·埃亚尔分割了几个世纪的远东大陆','几个世纪以来首位跨大陆者，改成大陆隔绝几个世纪；首位的时间范围也失去。','历史隔绝可以解释无人来往，但不是本句原定量范围；按同一修饰归属变化计一项。')
add(3867,'closed <?=Lore.pocket_time_winner.hisher?> eyes','深吸一口气，穿过','穿越前闭眼的动作遗漏。','深呼吸和穿越保留，未包含闭眼。')
add(3867,'the wastes of Eruan','艾露安的废墟','荒地被指定为建筑废墟。','地名相同不能证明两类地貌等价。')
add(3867,'Gerlyk, a god driven mad from isolation','盖里克，在长期的隔绝之中陷入了无尽的疯狂','两个分支都未保留Gerlyk的神明身份。','远古威胁只说明危险性，不说明神明类别；重复分支合并一项。')
add(3867,'what our champion did after that','我们的英雄在之后去了哪里','不知后来做了什么缩为不知去了哪里。','后句不论如何是笼统承接，未补回活动范围。')
add(3867,'the most trying challenge','挑战者是出人意料的','最艰难的挑战改成出乎意料的挑战者。','艾琳是盟友使意外合理，但不能代替挑战难度评价。')
add(3867,'despite the calls to help','未能阻止法师们在灼烧之痕举行的仪式','听到求援仍未阻止仪式的让步信息遗漏。','前分支收到急报不属于此条件分支的必经文字；应按当前分支判断。')
add(3868,'deeming many failures','面对无数的困难','评估许多候选为失败改成讲故事者面对困难。','各种可能性保留选择背景，不能恢复失败评价的对象。')
add(3868,'would be likely to find','很快发现自己面对的东西','假设未来可能找到的敌人改成已发现的经历。','前句本可以保留一种假设，却被后句很快发现转成事实叙述。')
add(3868,'inevitable doom in the Infinite Dungeon','前往无尽地下城寻求无穷无尽的挑战','前往必然毁灭的结局改成寻求不断挑战。','无穷挑战并不必然表达角色死亡或毁灭。')
add(3868,'to you in life','我此生欠你这个机会','在现实生命中的你与传说人物的对照改为叙述者此生。','下一分句传说中的西方灾星支持现实/传说对照；不是叙述者寿命说明。')
add(3870,'leaf-bound journal','被书页包裹的笔记','树叶装订/包裹的笔记改成书页包裹。','leaf可指书页，但随即枯萎及自然施法者日记语境支持植物叶；待核是否有更直接实体证据。','pending')
add(3870,'risk of mutating into something','被人扭曲','奥术力量变异的风险加上人为施动者限制。','魔法有使用者，但原文没有把变异必然归于人。')
add(3870,"support we'd otherwise lack",'我们过去所忽视的支持者','不用这种策略便得不到的支持，改成过去忽视的支持者。','新策略招募仍在，原文未说过去故意或无意忽视他们。')
add(3870,'there were Ziguranth in the last century','伊格兰斯一个世纪里招募的成员的数量','现有成员/上世纪成员的比较变成招募累计人数比较。','招募产生成员但不等于同一时点现有量；按比较对象一项计。')
add(3874,'only allowed to live','才被创造了出来','获准存活改成被创造的时点。','前段已说他们被造出，不能把允许生存等同首次创造。')
add(3874,'I doubt any of them','我们不认为众神中有人','叙述者个人看法变成群体共同看法。','全文多用我们描述种族，不自动把此处I的意见归给全体。')
add(3891,'Whichever of your positive and negative energies is a higher percentage','无论是你的正能量还是负能量都将用更高百分比的恢复','择占比更高的一种能量，改成正负能量均以更高百分比恢复。','后句两种速率都提高不等于前句两者都朝满值恢复；energies.lua:64–81分支支持。',impact='机制/操作')
add(3891,'regenerates towards its max','替代正常的休息值','朝最大值恢复的终点遗漏。','更高百分比不是最大值；正常静止值与最大值是不同概念。',impact='机制/操作')
add(3915,'broken or cancelled','攻击或者使用其他技能的动作都会中断效果，同时','主动取消时同样造成伤害的触发范围没有表达。','同时只承接攻击/使用技能中断；源码deactivate支持独立取消路径，目标版本另有限制。',impact='机制/操作')
add(3994,'ripples in radius 4','对半径 4 内的所有目标','中文全目标可能包含自身与召唤者，而快照明确排除二者。','英文也仅简述范围；这是中文新增全称与未固定实现之间的疑点，不能确认目标版本误述。','pending','机制/操作')
add(4039,'fully absorb any damaging actions','几率吸收伤害','是否缺少完全吸收量的明确度。','吸收伤害可泛指整次拦截，未出现部分吸收限定；先作表达澄清。','advisory','表达建议')
add(4078,'did an amazing job of pain and destruction','变成了一个恐怖的杀戮机器','对折磨者残害行为的评价改成雪人变成杀戮机器的结果。','装甲与链锯支持武器化外观，但不能代替原句对疼痛/摧残的评价。')
add(4087,'The light of the Amulet','神的光辉','护符发出的光被改为神的光辉。','护符可能带有神力，但原句的具体来源物品未保留。')
add(4126,'a third of the uses','复制的数量除以 3','可用次数与额外复制数的分母是否相同。','更名为获得身体可承接收存机制；Possessors无源码，不能确认是总次数还是额外副本。','pending','机制/操作')

verdicts=[]
for e in entries:
    claims=[c for c in rows if c['entry']==e['audit_id']]
    status='ISSUE' if any(c['status']=='confirmed' for c in claims) else 'PENDING' if any(c['status']=='pending' for c in claims) else 'OK'
    verdicts.append({'entry':e['audit_id'],'verdict':status,'claims':[c['id'] for c in claims],'note':'Full source and target read; no additional confirmed discrepancy in this initial pass.'})
out={'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independence':'Host has read all40 exact source/target and listed local evidence; no participant reports or terminal notifications seen before this write. Not human gold.','verdicts':verdicts,'claims':rows,'source_limits':'Orcs source files hash checked; unpinned DLC target mapping; Possessors source unavailable.'}
assert not (P/'HOST-INITIAL-FREEZE.json').exists()
(P/'HOST-INITIAL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'HOST-INITIAL-FREEZE.json').write_text(json.dumps({'at':out['completed_at'],'sha256':hashlib.sha256((P/'HOST-INITIAL.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
print('host frozen',len(verdicts),len(rows),{s:sum(c['status']==s for c in rows) for s in ['confirmed','pending','advisory']})
