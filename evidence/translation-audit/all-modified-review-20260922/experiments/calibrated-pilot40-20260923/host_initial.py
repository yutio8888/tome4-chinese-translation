"""Record host's full40 provisional pass, before reading either arm's output."""
import json, hashlib, datetime
from pathlib import Path
R=Path(__file__).resolve().parent
es=json.loads((R/'entries.json').read_text()); ix={e['audit_id']:e for e in es}
claims=[]
def c(n,src,zh,reason,counter,proof,status='confirmed'):
    e=ix['entry-'+str(n).zfill(5)]
    assert src in e['source'],(n,src)
    assert zh in e['target'],(n,zh)
    claims.append(dict(id=f'H{len(claims)+1:02}',entry_id=e['audit_id'],source_quote=src,target_quote=zh,reason=reason,strongest_counterargument=counter,status=status,text_status=status,snapshot_fact=proof,target_applicability='DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only',impact='meaning/reader understanding',origin='translation-introduced unless explicitly noted',section=e['section']))
c(3788,'confusing nearby enemies','混乱周围生物','混乱对象从敌人扩大为周围生物。','生物可泛指敌人，但同句周围没有敌方限定；会改变对盟友的理解。','chemistry.lua:284,301-315 -> damage_types.lua:296-314 explicitly separates hostile confusion from friendly smoke cover')
c(3830,'stack of herbs (sessali)','一束植物（延龄草）','草药材料类别泛化为植物。','括注草名保留种类；但普通植物与草药的材料用途类别并不相同。','ingredients.lua:76; text-only')
c(3846,'home steam-pipes','蒸汽阀','法定检查对象由管道缩为阀门。','上句同时提到阀门和接头，但本句home steam-pipes是管路整体。','emporium.lua:77 onward, inspection paragraph')
c(3846,'over 40%','减少40%','超过40%的阈值限定消失。','括号仍说明因人而异，但未保留原文最低幅度关系。','emporium.lua, collection-suit paragraph')
c(3846,'up to four years in prison','并处四年监禁','刑期上限改成固定四年；仅文学世界内语义判断。','译文的最高只修饰3000金币罚金，后面并处四年没有上限限定。','emporium.lua, last bullet')
c(3847,'...thing on?','……什么事？','录音开场检查机器是否开着，被写成询问事情。','原文截断但同篇日志录音语境支持device on。','gem.lua:24-34; recording context')
c(3847,'journey to the Loyalist\'s last known position is underway','正在准备前往忠诚者的上一个位置','正在进行旅程改成准备出发。','前句已说准时出发，不能消除本句的准备时序矛盾。','gem.lua:34')
c(3848,'for posterity','为了繁荣','为后世留存记录误作繁荣。','下句保留子孙后代但不使开头繁荣成为等价目的。','gem.lua:39')
c(3848,'I assume','我保证','推测口气被改成保证。','两者都可为应和，但认识确定性相反。','gem.lua, splendid dialogue')
c(3848,'Gurgling.','血液流淌之声。','咕噜声被确定成血液流淌声。','暴力场景可含血，但没有确定声音来源的文字证据。','gem.lua, screams/gurgling/crashing direction')
c(3855,'my entire ass','我的屁股','反驳前述抽签解释的粗口被字面化，丢失斥为胡扯的表达功能。','下一句明确作弊能让读者推断，但本句汉语未承载反驳。','misc.lua:104; whole draw/calibration paragraph')
c(3855,'the only type of person','世界上唯一一个','唯一的一类人改成世界上唯一一个个体。','中文家伙可泛称，但世界上唯一一个直接收窄数量。','misc.lua:106')
c(3855,'rich potion-brewer living comfortably','安居乐业的普通药水贩子','富裕变成普通，去掉与疯狂炼金师相对的发财结果。','安居乐业表达舒适生活，但不等于富裕，普通是新增评价。','misc.lua:108')
c(3863,'Neither can afford direct intervention, but some form of support will assuredly be available.','不论是那种，我们都没法直接介入，不过确实可以提供某种支持。','谈外部两派无法直接干涉却可支援，被换为己方我们无法干涉并供援。','后文谈请小个子协助进一步确认原文支援方向。','palace-fumes.lua, Palaquie reply between negotiation question and tinies response')
c(3863,'filthy little greenskins','狡猾的小绿人们','肮脏的贬称改成狡猾的性格。','同为贬低但评价的具体性质不同。','palace-fumes.lua, final Tantalos speech')
c(3869,'The damage left','魔法大爆炸对那里所造成的伤害','把未限定来源的破坏明确归因于魔法大爆炸。','世界观可能相关，但本段原文及随后英雄战斗造成的损伤不能证明全由爆炸引起。','primal-forest.lua:52-54')
c(3869,'may once more tip towards ruin','世界濒临毁灭的边缘','可能再次恶化改为已经濒临毁灭。','汉语描述危险，仍将可能趋势写成当前现实。','primal-forest.lua, opening paragraph')
c(3869,'where you explored, when','记录下各种观察到的生物的分布和数量','调查记录要求的时间信息遗漏。','分布与数量涵盖地点和多少，不涵盖何时调查。','primal-forest.lua, learning/observing paragraph')
c(3869,'endangered or invasive','濒临灭绝或受到入侵','物种成为入侵种变成物种受到入侵，生态监测对象关系反转。','前面的扩散监测不能改正后面明确的受动入侵。','primal-forest.lua, same paragraph')
c(3895,'at most %d distance to return to you','最多飞行 %d 然后折回你','返程最大距离被移成折返之前飞行距离。','此前已经说明折返，但本句然后明确将数值接在折返前。','sol.lua:52,58-79,102-103; newrange passed to homing return')
c(3907,'all foes in radius %d','半径 %d 码内的所有单位','敌方范围扩大为所有单位。','首句目标没有限定扩散对象；所有单位明确包含盟友。','action-at-a-distance.lua:186-197,209-213 friendlyfire=false corroborates text')
c(4128,'Your mere presence is a blight in your foes minds.','链接目标，偷取目标一个技能。','存在本身侵蚀敌人心智的叙事前提没有表达；仅保留连接和偷技能。','机制句可以解释如何偷取，不能表达前句被删的存在影响。','Frozen entries.json and context.lua; Possessors source unavailable')
c(4133,'You may only steal the body','你可能只会偷走','许可/限制may only误作可能性，弱化可偷取类型的硬性条件。','后句可学习新类型为限制提供线索，但不消除当前限定被写成概率。','Frozen entries.json and context.lua; text claim only')
special={
'entry-03844':('OK','荒诞疾病名译法有精度疑点，仅建议；不凭常识强定虚构病症。global speed core规范不约束本DLC。'),
'entry-03880':('OK','原文件物品自身desc称bomb，detonator→炸弹有语境；爆炸前离开保留操作要求。'),
'entry-03885':('PENDING','中英文说敌人命中；快照cosmic.lua:56只排除自己与自己召唤者，可能含友军；沿袭上游范围疑点，目标版本未定。'),
'entry-03947':('OK','setTarget(self)支持嘲讽/强制转移攻击目标日志，不据一句provokes判绝对行动控制。'),
'entry-03948':('PENDING','mecharachnid.lua:760定义半径tg2，761却project(tg)，与中英文半径嘲讽可能不符；沿袭上游，DLC适用性未定。'),
'entry-03964':('OK','致痒强度可表达施加检定强度；建议明确施加判定，不确认改变概率/时长成长。'),
'entry-03988':('OK','伤害/射程/周期参数一致；air→蒸汽在蒸汽武器语境暂作风味建议，待其他证据。'),
'entry-03989':('OK','电磁炮有同文件T_TURRET_GAUSS_CANNON证据；未称为无据新增。'),
'entry-04036':('OK','裸伤害涵盖all sources，无额外类型限制，不报漏译all。'),
'entry-04120':('OK','忠实生命加值标签；组件无源码不推定上游机制错误。'),
'entry-04144':('OK','保留永久选择、身体和克隆；不把多余空格作为确认缺陷。')}
table=[]
for e in es:
    cs=[c['id'] for c in claims if c['entry_id']==e['audit_id']]
    state,reason=('ISSUE',';'.join(cs)) if cs else special.get(e['audit_id'],('OK','完整原译核对：主体、条件、数值与操作含义相符；格式以参数消费检查为准。'))
    table.append({'entry_id':e['audit_id'],'state':state,'reason':reason,'claims':cs})
d={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'host provisional full40 before reading independent arm output','not_gold':True,'entries':table,'claims':claims,'limitations':'Host knows calibration and original task; this is independent of fresh model findings, not a human gold standard. Additional observations may be accepted/rejected at adjudication with explicit crosswalk.'}
(R/'HOST-INITIAL.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(R/'HOST-INITIAL-FREEZE.json').write_text(json.dumps({'file':'HOST-INITIAL.json','sha256':hashlib.sha256((R/'HOST-INITIAL.json').read_bytes()).hexdigest()},indent=2)+'\n')
print(len(table),len(claims))
