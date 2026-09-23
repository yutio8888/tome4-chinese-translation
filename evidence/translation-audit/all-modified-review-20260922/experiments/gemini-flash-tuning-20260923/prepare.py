"""Freeze factorial prompt packets; quote selection never consumes audit labels."""
import csv, hashlib, json, random, re, subprocess, time
from pathlib import Path

P=Path(__file__).resolve().parent
BASE=P.parent.parent
REPO=next(q for q in P.parents if (q/'AGENTS.md').exists())
AB=P.parent/'process-ab40-20260923'
PILOT=P.parent/'calibrated-pilot40-20260923'
SERIES=P.parent/'abc20-20260923'
def read(p):return json.loads(p.read_text())
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def size(e):return 'short' if len(e['source'])<=160 else 'medium' if len(e['source'])<=800 else 'long'
def block(text,line):
    lines=text.splitlines();starts=[i for i,l in enumerate(lines) if re.match(r'^\s*new(?:Talent|Effect|Lore|Chat|Entity)\s*\{',l)]
    before=[i for i in starts if i<=line-1];after=[i for i in starts if i>line-1]
    a=before[-1] if before else max(0,line-61)
    b=after[0] if before and after else len(lines) if before else min(len(lines),line+60)
    # A declaration can contain long narrative text. Preserve the whole block.
    return a+1,b,'\n'.join(f'{i+1}: {lines[i]}' for i in range(a,b))
def locate(text,e,known):
    if e['audit_id'] in known:return known[e['audit_id']]
    src=e['source'];candidates=[src,src.splitlines()[0],src[:70],src[:35]]
    for q in candidates:
        if not q:continue
        for variant in [q,q.replace('"','\\"'),q.replace("'","\\'")]:
            i=text.find(variant)
            if i>=0:return text[:i].count('\n')+1
    return None

def main():
    assert not (P/'FREEZE.json').exists()
    started=time.monotonic();inv=read(BASE/'inventory.json');ab=read(AB/'entries.json');pilot=read(PILOT/'entries.json')
    dev_ids={'03740','03857','03858','03862','03868','03891','03915','03923','03932','03995','04039','04078','04119','04121','04126','04127'}
    dev=[e for e in ab if e['audit_id'][-5:] in dev_ids];assert len(dev)==16
    prior=ab+pilot;ex_ids={e['audit_id'] for e in prior};ex_sections={e['section'] for e in prior}
    frame=set(read(AB/'SAMPLING.json')['frame_ids'])
    eligible=[e for e in inv['entries'] if e['audit_id'] in frame-ex_ids and e['section'] not in ex_sections]
    allocation={'orcs/long':4,'orcs/medium':8,'orcs/short':10,'possessors/medium':1,'possessors/short':1}
    rng=random.Random(2026092305);hold=[]
    for key,n in allocation.items():hold+=rng.sample(sorted([e for e in eligible if e['component']+'/'+size(e)==key],key=lambda e:e['audit_id']),n)
    keys=['audit_id','source','target','section','source_tag','args_order','special','logical_path','component','line','occurrence','snapshot_sha256']
    hold=[{k:e.get(k) for k in keys} for e in sorted(hold,key=lambda e:e['audit_id'])]
    dump(P/'dev/entries.json',dev);dump(P/'holdout/entries.json',hold)
    dump(P/'SAMPLING.json',{'dev_choice':'predeclared diagnostic cases from AB40, not random prevalence sample','dev_ids':[e['audit_id'] for e in dev],'holdout_seed':2026092305,'holdout_allocation':allocation,'eligible_holdout_ids':[e['audit_id'] for e in eligible],'holdout_ids':[e['audit_id'] for e in hold],'excluded_ids':sorted(ex_ids),'excluded_primary_sections':sorted(ex_sections)})
    registry=read(SERIES/'DLC-SOURCE-REGISTRY.json')['orcs']['files_sha256']
    srcroot=SERIES/'sources/orcs';known={x['entry']:x['line'] for x in read(AB/'HOST-ANCHORS.json') if x.get('line')}
    # Text-only effect index: no model opinions, no reference labels.
    effects={}
    for f,h in registry.items():
        if '/timed_effects' not in f:continue
        q=srcroot/f;assert sha(q)==h;text=q.read_text()
        for m in re.finditer(r'newEffect\s*\{\s*name\s*=\s*"([A-Z0-9_]+)"',text):
            line=text[:m.start()].count('\n')+1;effects[m.group(1)]=(f,line)
    all_source_hashes={}
    for phase,entries in [('dev',dev),('holdout',hold)]:
        out=P/phase;snips=[];access=[];texts={};allowed={};context=[]
        for lp in sorted({e['logical_path'] for e in entries}):
            locale=subprocess.check_output(['git','show',inv['snapshot_commit']+':'+lp],cwd=REPO,text=True)
            sections={e['section'] for e in entries if e['logical_path']==lp};marks=list(re.finditer(r'^section "([^"]+)"',locale,re.M))
            for i,m in enumerate(marks):
                if m.group(1) in sections:context.append(locale[m.start():marks[i+1].start() if i+1<len(marks) else len(locale)])
        (out/'context.lua').write_text('\n'.join(context))
        def materialize(section):
            src=srcroot/section;assert sha(src)==registry[section]
            rel='sources/orcs/'+section;dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes());all_source_hashes[rel]=sha(dest);allowed[rel]=sha(dest);return rel,src.read_text()
        terms=[];source_text='\n'.join(e['source'].lower() for e in entries)
        for f in sorted((REPO/'terminology').glob('*.tsv')):
            for n,row in enumerate(csv.DictReader(f.open(),delimiter='\t'),2):
                if row['source'].lower() in source_text:terms.append(dict(row,file=str(f.relative_to(REPO)),line=n))
        dump(out/'terms.json',terms)
        for e in entries:
            component=e['component'];section=e['section'];rec={'entry':e['audit_id'],'component':component,'section':section,'source_tag':e['source_tag'],'args_order':e['args_order'],'primary':None,'direct_effects':[]}
            rec['term_candidates']=[dict(t,lexical_candidate_only=True,tag_equal=t['source_tag']==e['source_tag']) for t in terms if t['source'].lower() in e['source'].lower()]
            if component=='possessors':
                rec['source_status']='unavailable';access.append({'entry':e['audit_id'],'section':section,'source_pinning':'unavailable'});snips.append(rec);continue
            rel,text=materialize(section);anchor=locate(text,e,known)
            access.append({'entry':e['audit_id'],'section':section,'source_pinning':'unpinned','path':rel,'anchor_line':anchor})
            rec['source_status']='hash-fixed, DLC repository/commit/target-release unpinned'
            if anchor:
                a,b,quote=block(text,anchor);rec['primary']={'path':rel,'sha256':allowed[rel],'start_line':a,'end_line':b,'quote':quote}
                refs=sorted(set(re.findall(r'\bEFF_([A-Z0-9_]+)',quote)))
                found=[r for r in refs if r in effects]
                for symbol in found[:4]:
                    f,line=effects[symbol];r,t=materialize(f);aa,bb,q=block(t,line);rec['direct_effects'].append({'symbol':symbol,'path':r,'sha256':allowed[r],'start_line':aa,'end_line':bb,'quote':q})
                rec['additional_effect_symbols_not_in_card']=found[4:]
            else:rec['note']='Exact anchor not found mechanically; inspect the full allowed primary source, not an invented line.'
            snips.append(rec)
        dump(out/'evidence-cards.json',{'generation':'same full declaration block for every located source; first four directly named effects sorted lexically; no judgments or selected error phrases','cards':snips})
        dump(out/'source-access.json',{'engine_repository':'/workspace/t-engine4','engine_commit':'624a67329fe2ad440c5b344785a9c73fcf22ae63','sections':access,'files_sha256':allowed,'additional_orcs':{'root':str(srcroot),'files_sha256':registry,'condition':'Only explicit symbol/call references from a read allowed file; hash verify. This source directory is allowed even though its parent has another experiment name.'},'unavailable_components':['possessors'],'path_base':str(P)})
        for rep in [1,2]:
            ordered=list(entries);random.Random(2026092310+rep).shuffle(ordered);dump(out/f'entries-r{rep}.json',ordered)
            for arm in ['F00','F10','F01','F11']:
                ptype='P1.md' if arm[1]=='1' else 'P0.md';ev=arm[2]=='1'
                content=f'''# {phase} {arm} repeat {rep}\n\n只读REVIEWER，purpose=translation_contextual_v1，自然语言研究旁路。\n实验根目录：{P}\n先读COMMON.md与{ptype}，然后读{phase}/entries-r{rep}.json，共{len(entries)}条，严格按其顺序输出。\n允许输入仅本入口、COMMON.md、{ptype}、FREEZE.json、{phase}/entries-r{rep}.json、{phase}/context.lua、{phase}/terms.json、{phase}/source-access.json及其源码白名单。context只作分配条目的语境，不额外审核邻文。\n'''
                if ev:content+=f'先读取{phase}/evidence-cards.json：机械生成的原始源码引用卡，不是裁决。卡片的术语词形命中不是适用性判定；有缺失可继续读取同一白名单源码。该卡也是允许输入。\n'
                else:content+='按需自行定位源码与术语；不得读取任何evidence-cards.json或其他组入口。\n'
                content+='禁止读取SPEC、SAMPLING、HOST、REFERENCE、STATE、其他阶段或组的输入／结果、以往审核报告。不要回读仓库全局说明来扩大范围。勿将只读权限因工具自动批准而改变。统一JSON格式一次返回；不要只给计划。\n'
                (out/f'INPUT-{arm}-r{rep}.md').write_text(content)
    # The old host reference is private evaluation data, never an evidence card.
    old=read(AB/'ADJUDICATION.json');devset={e['audit_id'] for e in dev}
    dump(P/'HOST-DEV-REFERENCE.json',{'claims':[c for c in old['canonical'] if c['entry'] in devset],'provenance':str(AB/'ADJUDICATION.json'),'sha256':sha(AB/'ADJUDICATION.json'),'status':'existing provisional host reference; not human gold'})
    dump(P/'SCOPE.json',{'task_id':P.name,'write_allowed':[str(P.relative_to(REPO))+'/**'],'mode':'review_only_research','planned_dev_runs':8,'max_holdout_runs':4,'max_infrastructure_retries_total':2,'max_parallel_children':3,'no_production_mutation':True})
    order=['F00','F11','F10','F01'];random.Random(2026092316).shuffle(order)
    dump(P/'RUN-PLAN.json',{'dev':[(a,r) for r,seq in [(1,order),(2,list(reversed(order)))] for a in seq],'holdout':'F00 and frozen selected challenger, two repeats each; no prompt edits'})
    dump(P/'STATE.json',{'task_id':P.name,'state':'FROZEN','mode':'review_only_research','orchestration_transport':'mcp','workspace_id':'wks_ac28b30c4bf45d5b','orchestrator_agent_id':'3a99ff56-6868-4533-b3d5-755e411f9159','child_dispatches':[],'research_contract_only':True,'strict_contract_completion_claimed':False,'selected_holdout_challenger':None})
    protected={str(q.relative_to(REPO)):sha(q) for q in BASE.rglob('*') if q.is_file() and P not in q.parents and '__pycache__' not in q.parts}
    for q in [REPO/'AGENTS.md',REPO/'TERMINOLOGY.md',REPO/'docs/agent-workflow.md',*REPO.glob('terminology/*.tsv'),*[REPO/s for s in {e['logical_path'] for e in inv['entries']}]]:protected[str(q.relative_to(REPO))]=sha(q)
    dump(P/'BASELINE.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'hashes':protected})
    frozen=[q for q in P.rglob('*') if q.is_file() and q.name not in ['STATE.json','BASELINE.json']]
    dump(P/'FREEZE.json',{'at':'2026-09-23','snapshot_commit':inv['snapshot_commit'],'files_sha256':{str(q.relative_to(P)):sha(q) for q in frozen}})
    dump(P/'PREPARATION-COST.json',{'wall_seconds':time.monotonic()-started,'characters':{phase:{'entries_source':sum(len(e['source']) for e in es),'entries_target':sum(len(e['target']) for e in es),'cards':len((P/phase/'evidence-cards.json').read_text()),'context':len((P/phase/'context.lua').read_text())} for phase,es in [('dev',dev),('holdout',hold)]},'note':'One-time packet generation wall time only; host design time is not included; byte/character counts are not token counts.'})
    for name in ['dispatches','reports','raw','normalized']:(P/name).mkdir(exist_ok=True)
    print({'dev':len(dev),'holdout':len(hold),'sources':len(all_source_hashes),'dev_order':order,'holdout_ids':[e['audit_id'] for e in hold]})

if __name__=='__main__':main()
