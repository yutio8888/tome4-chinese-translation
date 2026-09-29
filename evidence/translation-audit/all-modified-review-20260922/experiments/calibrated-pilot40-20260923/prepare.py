"""One-shot bounded research input preparation; never mutates prior records."""
import csv, hashlib, json, random, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
SERIES = ROOT.parent / 'abc20-20260923'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
def git(*args): return subprocess.check_output(['git', *args]).decode()
def main():
    assert not (ROOT/'FREEZE.json').exists(), 'Already frozen'
    inv=json.loads((BASE/'inventory.json').read_text())
    series=json.loads((SERIES/'STATE.json').read_text())
    campaign=json.loads((BASE/'STATE.json').read_text())
    registry=json.loads((SERIES/'DLC-SOURCE-REGISTRY.json').read_text())
    excluded=set()
    for b in campaign['batches']:
        if b.get('dispatches') or b.get('covered_entry_ids'): excluded.update(b['entry_ids'])
    for g in series['groups']:
        if g['index']<=14: excluded.update(g['entry_ids'])
        else:
            state=json.loads((ROOT.parent/g['directory']/'STATE.json').read_text())
            assert not state['child_dispatches']
    frame=[e for e in inv['entries'] if int(e['audit_id'][6:])>=3733 and e['audit_id'] not in excluded and e['prior_spotcheck'] is None]
    def length(e): return 'short' if len(e['source'])<=160 else 'medium' if len(e['source'])<=800 else 'long'
    allocations={'orcs/short':14,'orcs/medium':15,'orcs/long':7,'possessors/short':1,'possessors/medium':2,'possessors/long':1}
    spec={'seed':2026092301,'algorithm':'Python random.Random(seed).sample within sorted component/length strata; strata order as listed', 'thresholds':{'short_max':160,'medium_max':800},'allocation':allocations,'frame_ids':[e['audit_id'] for e in frame], 'frame_count':len(frame), 'selection_before_reading_findings':True, 'eligibility':'inventory >= entry-03733, no campaign dispatch/coverage, no prior spotcheck, outside completed ABC groups1-14; frozen groups15-20 have zero children', 'limitations':'Only remaining modified Orcs and Possessors entries; oversamples long strings, not representative of full repository. Original group15 not resumed.'}
    dump(ROOT/'SAMPLING-PREREG.json',spec)
    rng=random.Random(spec['seed']); selected=[]
    for key,n in allocations.items():
        pool=sorted([e for e in frame if e['component']+'/'+length(e)==key],key=lambda e:e['audit_id'])
        selected.extend(rng.sample(pool,n))
    selected.sort(key=lambda e:e['audit_id'])
    columns=['audit_id','source','target','section','source_tag','args_order','special','logical_path','component','line','occurrence','snapshot_sha256']
    rows=[{k:e.get(k) for k in columns} for e in selected]
    dump(ROOT/'entries.json',rows)
    dump(ROOT/'SAMPLE.json',{'entries':[{'entry_id':e['audit_id'],'component':e['component'],'length':length(e),'characters':len(e['source'])} for e in selected]})
    prior={str(p.relative_to(BASE)):sha(p) for p in BASE.rglob('*') if p.is_file() and ROOT not in p.parents and '__pycache__' not in p.parts}
    production={str(p):sha(p) for p in [Path('TERMINOLOGY.md'),*Path('terminology').glob('*.tsv'), *[Path(s) for s in sorted({e['logical_path'] for e in inv['entries']})]]}
    dump(ROOT/'BASELINE-GUARD.json',{'prior_files_sha256':prior,'production_sha256':production,'head':git('rev-parse','HEAD').strip()})
    parts=[]; metas=[]; sources={}
    for lp in sorted({e['logical_path'] for e in rows}):
        locale=git('show',inv['snapshot_commit']+':'+lp)
        sections={e['section'] for e in rows if e['logical_path']==lp}
        marks=list(re.finditer(r'^section "([^"]+)"',locale,re.M))
        for i,m in enumerate(marks):
            if m.group(1) in sections: parts.append(locale[m.start():marks[i+1].start() if i+1<len(marks) else len(locale)])
        for section in sorted(sections):
            component=next(e['component'] for e in rows if e['section']==section)
            if component=='possessors':
                metas.append({'component':component,'section':section,'source_pinning':'unavailable','source_path':None}); continue
            src=SERIES/'sources'/component/section
            assert sha(src)==registry[component]['files_sha256'][section]
            rel='sources/dlc/'+component+'/'+section
            dest=ROOT/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(src.read_bytes())
            sources[rel]=sha(dest)
            metas.append({'component':component,'section':section,'source_pinning':'unpinned','source_path':rel})
    (ROOT/'context.lua').write_text('\n'.join(parts))
    dump(ROOT/'source-access.json',{'engine_repository':'/workspace/t-engine4','engine_commit':'624a67329fe2ad440c5b344785a9c73fcf22ae63','sections':metas,'files_sha256':sources,'dlc_additional_sources':{'orcs':{'root':str((SERIES/'sources/orcs').resolve()),'files_sha256':registry['orcs']['files_sha256'],'source_pinning':'unpinned'}},'unavailable_components':['possessors'],'rule':'Only listed primary files and explicit symbol/call-linked single additional files; hash verify. No locale answers or historic reports.'})
    terms=[]
    for p in sorted(Path('terminology').glob('*.tsv')):
        for line,t in enumerate(csv.DictReader(p.open(),delimiter='\t'),2): terms.append(dict(t,file=str(p),line=line))
    text='\n'.join(e['source'].lower() for e in rows)
    relevant=[t for t in terms if t['source'].lower() in text]
    dump(ROOT/'terms.json',relevant)
    rules='''# Calibrated pilot40 — frozen reviewer input v1

This is bounded read-only research, not production verification. Review exactly the 40 entries in entries.json, in frozen order. Return a complete table plus atomic observations; do not edit any file or spawn children. Do not read prior reports, scope proposals, host findings, or the other arm. Only INPUT.md, entries.json, context.lua, terms.json, source-access.json, FREEZE.json and expressly allowed source files may be read. No repository-wide search. Primary files may be searched locally; additional single files require an explicit symbol/call from a read file. Missing Possessors source cannot be replaced with similarly named code from another component. Source hashes must match. Engine commit is separate from unpinned DLC snapshots.

Task-specific rules below prevail over generic formatting guidance. Do not import full terminology writing guidance as extra defect criteria.

1. Judge full paragraph and runtime consumption, not word-by-word omission. For every claim quote exact frozen source and target, identify meaning change, strongest equivalent interpretation or contextual repair, evidence path/line, impact. Simple nonliteral translation is not a defect.
2. Check terminology status AND scope AND source_tag AND category/context. existing does not force rename. global/multi apply all components; dlc applies ashes-urhrok,cults,items-vault,orcs,possessors; core excludes those five; addon applies addon-dev,items-vault,possessors. No scope changes in this pilot. Shared mechanism alone does not override current scope. Inapplicable glossary does not prove semantic correctness.
3. Bare Chinese 增加伤害 can express all-damage increase. inc_damage.all proves implementation, not translation error. Confirm lost scope only with a substantive restriction or contrast lost in context.
4. Formatting: preserve argument consumption, valid markup and information structure. Do not mechanically count whitespace, blank lines or punctuation. Dynamic suffix claims must consider empty and nonempty alternatives. Static rendering is not a game test.
5. User calibration: ambiguity of first attacked vs first hit when main sentence already requires damage; 文明人→普通人; and 受到熵能反冲 covering application/increase: list as needs clarification/advisory, NOT confirmed mistranslation. This does not remove separate objectively supported defects in the same entry.
6. Distinguish text_status, snapshot_fact, target_applicability, impact. Pure text defects need not become pending just because DLC commit is unpinned. A conclusion depending on implementation/target identity keeps target applicability pending. Record upstream inherited error separately from translation-introduced error. Code/translation/English discrepancies require actual call-chain evidence, not guessed variables.
7. Merely possible wrong interpretation is insufficient for confirmed. Reasonable unresolved alternatives => PENDING; preference without substantive unresolved fact => ADVISORY. No quotas or pressure to find issues.

Output in Chinese: all40 entry table with ISSUE/PENDING/OK (OK may include advisory), then C01... atomic claims. Each claim: entry, exact quotes, strongest counterargument, conclusion confirmed/pending/advisory, text_status, snapshot_fact, target_applicability, impact, source proof. Finish actual files read and source/version limits. Do not claim DONE_VERIFIED. Return report in final answer, no files.

The two arms use identical input. Review findings are observations, not gold truth. Host adjudication and all joint-negative audit occur after each independent observation is frozen.
'''
    (ROOT/'INPUT.md').write_text(rules+'\nEntries and exact texts: entries.json. Full adjacent section translations: context.lua. Applicable term candidates: terms.json. Source paths/hashes: source-access.json.\n')
    (ROOT/'SPEC.md').write_text('# Scope\n40 new entries only, two independent arms Opus5.5 and GPT6Sol, high reasoning. Host makes a provisional full40 pass before reading model findings, then adjudicates claim union and checks every joint negative. No production translation or term mutation; no group15 continuation. Stop after report and confirmed child archival. No claim of accuracy improvement from different samples or model consensus as human gold.\n')
    (ROOT/'PLAN.md').write_text('# Plan\n1. Scope audit with row-specific proposal. 2. User calibration recorded as clarification, not confirmed. 3. Freeze rules and seed-stratified sample. 4. Two independent read-only reviews. 5. Host full40 evidence and claim/negative audit. 6. Runtime identity, timing, available usage, lifecycle and immutable-baseline verification; report and stop.\n')
    dump(ROOT/'SCOPE.json',{'mode':'read_only_research','write_allowed':[str(ROOT)+'/**'],'production_writes':False,'entries':[e['audit_id'] for e in rows],'max_entries':40,'max_arms':2,'old_groups_15_20':'remain undispatched'})
    dump(ROOT/'STATE.json',{'task_id':ROOT.name,'state':'FROZEN','mode':'review_only_research','orchestration_transport':'mcp','workspace_id':series['workspace_id'],'orchestrator_agent_id':series['orchestrator_agent_id'],'strict_contract_completion_claimed':False,'child_dispatches':[],'user_calibration':'列为需要澄清的表达，但不计确认错译','term_changes':'proposal only; frozen actual scope remains in force'})
    frozen=['INPUT.md','entries.json','context.lua','terms.json','source-access.json','SAMPLING-PREREG.json','SAMPLE.json','SPEC.md','PLAN.md','SCOPE.json']+list(sources)
    dump(ROOT/'FREEZE.json',{'count':40,'files_sha256':{p:sha(ROOT/p) for p in frozen},'snapshot_commit':inv['snapshot_commit']})
    for d in ['dispatches','raw','reports']: (ROOT/d).mkdir(exist_ok=True)
    (ROOT/'dispatches/common-prompt.txt').write_text('你是只读 REVIEWER，purpose=translation_contextual_v1。本轮用户授权研究旁路，非正式生产批次。独立复核全部40条，不写文件、不创建子agent、不读取其他报告。唯一入口：'+str(ROOT/'INPUT.md')+'。严格遵守其中冻结的校准规则与访问边界；最终返回完整自然语言报告。')
    print('Frozen',len(rows),'of frame',len(frame),[e['audit_id'] for e in rows])

if __name__=='__main__': main()
