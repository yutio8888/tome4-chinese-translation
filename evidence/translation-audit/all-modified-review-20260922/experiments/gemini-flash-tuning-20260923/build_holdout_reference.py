import json,pathlib,hashlib,datetime
p=pathlib.Path(__file__).parent
entries=json.loads((p/'holdout/entries.json').read_text());cards={c['entry']:c for c in json.loads((p/'holdout/evidence-cards.json').read_text())['cards']}
rows=[
('03746','confirmed','He directs his glare toward','他指向','目光投向守卫被改成指向动作。','用指向提示危险同样合理，但不是原叙述的凝视动作。','narrative'),
('03746','confirmed','guards staring at you and standing still on the sides of the room','周围和房间里那些装备良好的警卫','守卫盯着玩家、静立两侧的信息没有保留。','装备良好保留了威胁，未表达具体监视姿态；这些同一姿态合为一项。','narrative'),
('03746','advisory','exotic weaponry','异种武器','异种搭配可读性较差。','可以理解为异域奇特装备，不能必然解读成武器属于异种族。','expression'),
('03746','advisory','leans down over the counter','从柜台往下看','探身俯视被压缩。','后文靠近及俯视仍提供姿态线索，不按每次重复动作逐词追责。','expression'),
('03842','confirmed','Our contacts with the black market','黑市的那些合约','contacts联系误作合约。','上下文涉及贸易，并未说明联系就是签订的契约。','narrative'),
('03842','pending','received as payment for a product received via Iron Throne smugglers','作为从钢铁王座的走私者那里以货物形式支付的报酬','货物和报酬的流向句法含混。','英文两个received及交易对象本身难唯一确定；先不确认方向反转。','narrative'),
('03842','advisory','bi-monthly','每两个月','频率可有两种英文读法。','bi-monthly本身有歧义，不凭另一种可能词义判译错。','expression'),
('03842','advisory',"Maj'Eyal",'马基亚埃尔','专名音译与现有常用译名差异。','preferred行scope=core不约束Orcs；不借音译偏好绕过适用域。','expression'),
('03899','confirmed','other creatures','生物','其他生物的排除自身限定丢失。','中文未写所有生物，但施法者也属于生物；原文的自他区别未由其他句补回。','mechanism'),
('03899','advisory','in a radius of %d','在 %d 范围内','半径可更明确。','游戏技能范围语境可按施法者向外距离理解，不将范围一律判错。','expression'),
('03908','advisory','even through walls','超脱视线的感知','穿墙感知可明说。','超脱视线已能涵盖视线被墙阻挡，不能确认机制范围实质丢失。','expression'),
('03935','confirmed','in a frontal arc','在前方','扇形范围简化成只有前方方向。','前方可以是直线、单点或扇形，几何形态影响目标选择。','mechanism'),
('03935','confirmed','to enemies','在前方造成','伤害目标的敌方限定未译。','后面的他们无明确先行词，不能恢复敌我限定。','mechanism'),
('03935','advisory','All shockstaff attacks','所有电击棒伤害','攻击写成伤害。','本段完整近战命中伤害语境下不能仅凭词形断言新触发限制。','expression'),
('03936','confirmed','flechettes','子弹','箭形细镖弹体特征泛化为子弹。','广义子弹可含镖形弹，但原文明确的构造特征不再表达；不是判断实际攻击机制。','narrative'),
('03936','advisory','multi-barreled bolt launcher','多管重型枪械','发射器改作重型枪械。','同技能名Boltgun及重武器树允许枪械概称，不另外重复计弹体遗漏。','expression'),
('04138','pending','prevents you from ever taking blows that deal more than','每次受到伤害时，伤害不会超过','免受超阈值打击还是伤害封顶，英文说明有两种读法。','无Possessors源码，译文封顶是合理可能，不能确认机制错译。','mechanism'),
]
claims=[]
for i,(suffix,status,src,tgt,reason,counter,impact) in enumerate(rows,1):
 eid='entry-'+suffix;e=next(e for e in entries if e['audit_id']==eid);assert src in e['source'] and tgt in e['target'],(eid,src,tgt)
 primary=cards[eid].get('primary') or {};line=primary.get('start_line');path=primary.get('path','holdout/entries.json')
 if primary.get('quote'):
  for l in primary['quote'].splitlines():
   if src in l:line=int(l.split(':',1)[0]);break
 claims.append(dict(id=f'Q{i:02}',entry=eid,status=status,source_quote=src,target_quote=tgt,reason=reason,strongest_counterevidence=counter,impact=impact,evidence=dict(path=path,line=line),text_status=status,target_applicability='Frozen textual comparison; Orcs snapshot unpinned, Possessors unavailable.'))
coverage=[]
for e in entries:
 cs=[c for c in claims if c['entry']==e['audit_id']];st='ISSUE' if any(c['status']=='confirmed' for c in cs) else 'PENDING' if any(c['status']=='pending' for c in cs) else 'OK'
 coverage.append(dict(entry=e['audit_id'],status=st,claim_ids=[c['id'] for c in cs],note='Full source/target read before any holdout reports; parameters, condition scope and paragraph equivalence checked. This is provisional host reference, not human gold.'))
r=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),claims=claims,coverage=coverage,method='Independent host first pass; no holdout model has been dispatched. Later novel findings retained separately and sensitivity-scored uniformly.',limitations=['Unpinned Orcs mechanism applicability; missing Possessors source.','Small section-clustered sample, no prevalence or statistical superiority claim.'])
f=p/'HOST-HOLDOUT-INITIAL.json';f.write_text(json.dumps(r,ensure_ascii=False,indent=2));(p/'HOLDOUT-REFERENCE-FREEZE.json').write_text(json.dumps(dict(at=r['at'],sha256=hashlib.sha256(f.read_bytes()).hexdigest(),count=len(coverage),confirmed=sum(c['status']=='confirmed' for c in claims)),indent=2));print('frozen',len(coverage),'entries',sum(c['status']=='confirmed' for c in claims),'confirmed')
