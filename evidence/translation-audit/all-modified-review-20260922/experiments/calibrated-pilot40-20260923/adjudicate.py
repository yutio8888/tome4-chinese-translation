"""Host adjudication of both immutable reports; manual decisions, not model gold."""
import json,re,copy,collections,datetime,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
def read(name):return json.loads((R/name).read_text())
def dump(name,d):(R/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
host=read('HOST-INITIAL.json');es=read('entries.json');index={e['audit_id']:e for e in es}
claims=[];hmap={}
for c in host['claims']:
    if c['id'] in ['H02','H11']:continue
    d=copy.deepcopy(c);d['id']=f'D{len(claims)+1:02}';hmap[c['id']]=d['id'];d['host_initial_id']=c['id'];claims.append(d)
tea=dict(id=f'D{len(claims)+1:02}',entry_id='entry-03847',source_quote='as soon as he can un-kick the hornet\'s nest',target_quote='要不是他刚刚给我们捅了个大马蜂窝',reason='先解决自己制造的混乱才给茶的条件，被替换为只责备此前制造混乱。',strongest_counterargument='讽刺与不给茶的态度仍可从语境读出，但先解决麻烦的条件没有保留。',status='confirmed',text_status='confirmed',snapshot_fact='gem.lua:32, whole reply to tea-maker demand',target_applicability='pure text; DLC target version unpinned',impact='叙事条件关系',origin='translation-introduced',section=index['entry-03847']['section'])
assert tea['source_quote'] in index['entry-03847']['source'];assert tea['target_quote'] in index['entry-03847']['target'];claims.append(tea);hmap['H24']=tea['id']
pending=[
dict(id='P01',entry_id='entry-03844',reason='pinaciphobia 的罕见词义与笑点需要可靠词源/作者语境证据。Opus 未给词义来源，宿主不能仅凭其自信确认。',evidence='Opus C02; emporium.lua:40; host supplementary lexical search found popular lists but not a decisive lexicographic entry in checked AlphaDictionary page.',text_status='pending',target_applicability='lexical meaning gap, not DLC version gap'),
dict(id='P02',entry_id='entry-03824',reason='中英文都称附近所有生物，快照只收集hostile并检查teleport。属于上游范围概括，目标版本适用性未定。',evidence='world-artifacts.lua:2245–2255',text_status='translation faithful; upstream discrepancy',target_applicability='DLC unpinned'),
dict(id='P03',entry_id='entry-03885',reason='中英文限定敌人命中，快照负能量回复分支只排除自身与自身召唤物；是否包含其他友军需目标版本链路。',evidence='cosmic.lua:50–61; host pre-reveal finding',text_status='translation faithful; upstream discrepancy',target_applicability='DLC unpinned; local callback evidence only'),
dict(id='P04',entry_id='entry-03948',reason='中英文半径嘲讽与快照定义tg2但project(tg)不符；本体投射语义及DLC目标版本适用性仍有限定。',evidence='mecharachnid.lua:760–770; host initial and Opus C18',text_status='translation faithful; upstream discrepancy',target_applicability='DLC unpinned')]
cross=[]
def x(arm,cid,entries,verdict,targets,reason,claimed):
    cross.append(dict(arm=arm,observation_id=cid,entry_ids=['entry-'+str(e).zfill(5) for e in entries],reported_status=claimed,host_status=verdict,canonical_ids=[hmap.get(t,t) for t in targets],reason=reason))
for cid,h in [('C01','H01'),('C04','H06'),('C05','H08'),('C06','H14'),('C07','H16'),('C08','H19'),('C10','H20'),('C11','H21'),('C13','H22'),('C14','H23')]:
    d=next(c for c in claims if c['id']==hmap[h]);x('opus',cid,[int(d['entry_id'][6:])],'confirmed',[h],'核对完整原译及宿主证据后确认主张；不自动确认同claim其他附带理由。','confirmed')
x('opus','C02',[3844],'pending',['P01'],'罕见词义证据不足，外部补查与冻结reviewer证据分开，不计确认命中或误报。','confirmed')
x('opus','C03',[3844,3846],'advisory',[],'preferred entity name行不直接约束_t；既定规则已确定适用边界，无须把明确不适用升级为pending。可提跨标签专名一致性建议。','pending')
x('opus','C09',[3869],'confirmed',['H17'],'宣传语气不消除may的现实/可能区别；低影响与正确性分开。','advisory')
x('opus','C12',[3964],'advisory',[],'施加强度的等价解释和同族说明成立，不能据可能误读确认改变失败概率。','advisory')
x('opus','C15',[4133],'advisory',[],'may learn可表达获得许可，无额外概率证据。源码缺失不使每个may自动成为pending缺陷。','pending')
x('opus','C16',[3846],'confirmed',['H04','H05'],'数值阈值确实变化；纯风味只影响优先级，不足以撤销语义事实。','advisory')
x('opus','C17',[3824],'pending',['P02'],'忠实于英文的上游问题，当前条目不计新增错译；目标版本机制未固定。','upstream')
x('opus','C18',[3948],'pending',['P04'],'快照疑点成立，不能称目标版本已确认。','upstream')
for cid,h in [('C01','H01'),('C03','H04'),('C04','H05'),('C05','H06'),('C06','H24'),('C07','H07'),('C08','H08'),('C09','H10'),('C10','H14'),('C11','H16'),('C12','H18'),('C13','H19'),('C15','H20'),('C16','H21'),('C17','H22')]:
    d=next(c for c in claims if c['id']==hmap[h]);x('sol',cid,[int(d['entry_id'][6:])],'confirmed',[h],'原译短引及完整上下文支持；低影响照实记录，不推断实现缺陷。','confirmed')
x('sol','C02',[3830],'advisory',[],'无适用强制专名，也无sessali必属另一植物的积极证据；游戏虚构名称本地化不能仅因缺植物学身份就挂pending。','pending')
x('sol','C14',[3880],'refuted',[],'同文件:59 subtype=bomb、:62 desc称This bomb；具体对象本就被原文称炸弹。只看弹窗标题不足。','confirmed')
x('sol','C18',[3824],'pending',['P02'],'快照反证成立；作为上游缺口与翻译新增分开。','advisory/upstream')
x('sol','C19',[3929],'advisory',[],'宿主沿LIGHTNING_DAZE追固定本体damage_types.lua:1567，默认daze_duration为3；本条3回合吻合。另一个状态说明2回合的上游问题不使本条有错。','advisory/upstream')
# Additional observations explicitly present outside numbered blocks are preserved separately.
for cid,nums,verdict,targets,reason in [
('A01',[3814],'advisory',[],'向外割去生硬，施受关系保留。'),
('A02',[3830],'advisory',[],'材料type和desc分别明示草药，名称的植物+延龄草不单独造成已证实类别误识；宿主H02撤回确认。'),
('A03',[3855],'advisory',[],'my entire ass的字面译法生硬，但后句作弊已补足拒斥意图；宿主H11撤回确认。'),
('A04',[3880],'advisory',[],'爆炸前必须离开已保留危险应对，不必逐字补炸死。'),
('A05',[3885],'advisory',[],'省略投射物主语仍可从前句承接。'),
('A06',[3928],'advisory',[],'他/它书写建议，实体对象不歧义。'),
('A07',[3988],'advisory',[],'升级语境可承载增加最大生命值；targets是否仅敌人需完整炮台调用，现不足另判新增范围错误。'),
('A08',[3989],'advisory',[],'技能等级与下一从句连读，缺级不导致参数归属失真。'),
('A09',[4113],'advisory',[],'回归之杖为任务提示的可操作具体化；世界传送能力是否存在其他可用手段需实际可达性，不凭canBe名称判缩窄。'),
('A10',[4144],'advisory',[],'多余空格未损坏变量/信息结构。'),
('A11',[3847],'advisory',[],'his previous terms与我们协议中承诺是否实质改变需更多合同背景，不强定一方开价。'),
('A12',[3847],'confirmed',['H24'],'喝茶条件关系丢失，与Sol C06同一项。'),
('A13',[3847],'confirmed',['H07'],'准备与进行中的时序改变，与Sol C07同一项。'),
('A14',[3847],'advisory',[],'这篇混乱的量词建议；无独立事件信息改变，低影响不扩展本轮评分。'),
('A15',[3848],'confirmed',['H09'],'I assume与我保证的确定性变化。'),
('A16',[3848],'advisory',[],'大小写无法机械映射中文强调；纪录/记录无关机制与事实。'),
('A17',[3869],'advisory',[],'末句我们向你介绍语法可改，但不缺谓词意义。')]:x('opus',cid,nums,verdict,targets,reason,'unnumbered advisory')
cross.sort(key=lambda x:(x['arm'],x['observation_id']))
dump('CLAIM-CROSSWALK.json',cross)
tables={}
for arm in ['opus','sol']:
    s=(R/f'reports/{arm}.md').read_text()
    tables[arm]=dict(re.findall(r'^\|\s*\d+\s*\|\s*(entry-\d+)\s*\|\s*\*?\*?(ISSUE|PENDING|OK)',s,re.M))
result_entries=[]
for e in es:
    ds=[c['id'] for c in claims if c['entry_id']==e['audit_id']];ps=[p['id'] for p in pending if p['entry_id']==e['audit_id']]
    result_entries.append(dict(entry_id=e['audit_id'],state='ISSUE' if ds else 'PENDING' if ps else 'OK',confirmed=ds,pending=ps,opus=tables['opus'][e['audit_id']],sol=tables['sol'][e['audit_id']]))
joint=[e for e in result_entries if e['opus']==e['sol']=='OK']
metrics={}
for arm in ['opus','sol']:
    obs=[x for x in cross if x['arm']==arm and x['reported_status']=='confirmed']
    hit={d for x in obs if x['host_status']=='confirmed' for d in x['canonical_ids'] if d.startswith('D')}
    allhit={d for x in cross if x['arm']==arm and x['host_status']=='confirmed' for d in x['canonical_ids'] if d.startswith('D')}
    term=read(f'dispatches/terminal-{arm}.json')['structuredContent']['snapshot']
    start=read(f'dispatches/runtime-initial-{arm}.json')['structuredContent']['snapshot']['activeTurn']['startedAt']
    end=term['attentionTimestamp'];seconds=(datetime.datetime.fromisoformat(end.replace('Z','+00:00'))-datetime.datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds()
    metrics[arm]={'entry_counts':dict(collections.Counter(tables[arm].values())),'numbered_confirmed_claims':len(obs),'accepted':sum(x['host_status']=='confirmed' for x in obs),'refuted':sum(x['host_status']=='refuted' for x in obs),'pending':sum(x['host_status']=='pending' for x in obs),'confirmed_hit_ids':sorted(hit),'any_status_observation_hit_ids':sorted(allhit),'wall_seconds':seconds,'runtime_model':term['runtimeInfo']['model'],'configured_thinking':term['thinkingOptionId'],'runtime_thinking':term['runtimeInfo'].get('thinkingOptionId'),'reported_lastUsage':term.get('lastUsage'),'cost_usd':term.get('lastUsage',{}).get('totalCostUsd'),'cost_note':'Provider field only; missing cost is unknown, not zero; token accounting differs by provider and is not normalized.'}
union=set(metrics['opus']['confirmed_hit_ids'])|set(metrics['sol']['confirmed_hit_ids'])
result={'not_gold':True,'reference':'host evidence adjudication, not human truth or production acceptance','entries':result_entries,'counts':dict(collections.Counter(e['state'] for e in result_entries)),'confirmed_claims':claims,'pending_claims':pending,'metrics':metrics,'confirmed_union_hit_ids':sorted(union),'confirmed_union_missed_ids':sorted({c['id'] for c in claims}-union),'joint_negative_count':len(joint),'joint_negative_confirmed_entries':[e['entry_id'] for e in joint if e['confirmed']],'joint_negative_pending_entries':[e['entry_id'] for e in joint if e['pending']],'user_calibration':'三类边界列需澄清，不计确认错译；原校准文件不追溯改写。'}
dump('RESULT.json',result)
dump('JOINT-NEGATIVE-AUDIT.json',{'method':'all joint OK entries checked, not sampled; host full40 pass frozen before arm reveal, new upstream claims then verified','entries':joint})
dump('HOST-REVISIONS.json',{'H02':{'to':'advisory','reason':'同实体type与desc在context.lua明确草药，名称并未造成已证实分类误识。'},'H11':{'to':'advisory','reason':'粗口字面译法的语感不佳，但全文作弊句保留拒斥功能；不再确认独立失义。'},'new_D':{'id':tea['id'],'from':'Sol C06 / Opus unnumbered advisory','reason':tea['reason']},'new_pending':['P01','P02'],'no_prior_records_changed':True})
print(json.dumps({'counts':result['counts'],'D':len(claims),'P':len(pending),'union_hits':len(union),'jointOK':len(joint),'metrics':{a:{k:v for k,v in m.items() if k in ['accepted','refuted','pending','wall_seconds','cost_usd']} for a,m in metrics.items()}},ensure_ascii=False))
