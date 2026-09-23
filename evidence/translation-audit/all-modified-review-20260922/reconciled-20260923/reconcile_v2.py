#!/usr/bin/env python3
"""Exact, deterministic evidence reconciliation (no semantic review)."""
from __future__ import annotations
import csv, hashlib, io, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

OUT=Path(__file__).resolve().parent; CAM=OUT.parent; ROOT=CAM.parents[2]; EXP=CAM/'experiments'
SCOPE=ROOT/'evidence/translation-audit/scope-rule-calibration-20260923'
EID=re.compile(r'entry-\d{5}')
MARK=re.compile(r'(?mi)^(?:#{1,6}\s+[^\n]{0,40}?|\d+[.)]\s+|[-*]\s+|\|\s*)(?:`|\*\*)?(entry-\d{5})(?:`|\*\*)?\b')
used=set()
def use(p):
 p=Path(p).resolve()
 if not p.is_file(): raise FileNotFoundError(p)
 used.add(p); return p
def load(p): return json.loads(use(p).read_text(encoding='utf-8'))
def rel(p): return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def loc(p,local=None,line=None):
 d={'path':rel(p)}
 if local is not None:d['local_id']=local
 if line is not None:d['line']=line
 return d
def status(line):
 s=line.lower()
 if re.search(r'\brefuted\b|撤销|驳回|不成立',s):return 'refuted'
 if re.search(r'\bpending\b|待确认|待决',s):return 'pending'
 if re.search(r'\badvisory\b|细微观察|仅建议|建议项',s):return 'advisory'
 if re.search(r'\bconfirmed(?:_provisional)?\b|存在问题|已确认|确认错译',s):return 'confirmed'
 if '存在疑点' in s:return 'pending_candidate'
 if re.search(r'未发现问题|\bOK\b',line):return 'ok'
 return 'unknown'
def blocks(p):
 t=use(p).read_text(encoding='utf-8'); ms=list(MARK.finditer(t)); starts=[0]+[m.end() for m in re.finditer('\n',t)]
 import bisect
 out=[]
 for i,m in enumerate(ms):
  end=ms[i+1].start() if i+1<len(ms) else len(t); b=t[m.start():end].rstrip(); st=status(b.splitlines()[0])
  if st=='unknown':
   for line in b.splitlines()[1:]:
    if re.match(r'^\s*(?:[-*]\s*)?(?:\*\*)?(?:复核结论|结论|状态|判断)(?:\*\*)?\s*[：:]',line):
     st=status(line)
     if st!='unknown':break
  out.append({'eid':m.group(1).lower(),'text':b,'line':bisect.bisect_right(starts,m.start()),'status':st})
 return out
def markdown_claims(p):
 """Index explicit non-OK conclusions, status headings, and observation fields."""
 t=use(p).read_text(encoding='utf-8'); ms=list(MARK.finditer(t)); out=[]
 cre=re.compile(r'(?mi)^\s*(?:[-*]\s*)?(?:\*\*)?(?:复核结论|结论|状态|判断)(?:\*\*)?\s*[：:]\s*(?:\*\*)?([^*\n]+)')
 ore=re.compile(r'(?mi)^\s*[-*]\s*(?:\*\*)?(细微观察|advisory|建议项|存在疑点|疑点|观察)(?:\*\*)?\s*[：:]\s*([^\n]*)')
 ire=re.compile(r'(?mi)^([^\n]{0,240}?状态为\s*(?:\*\*)?(pending|advisory|confirmed|refuted)(?:\*\*)?[^\n]*)$')
 import bisect
 starts=[0]+[m.end() for m in re.finditer('\n',t)]
 for i,m in enumerate(ms):
  end=ms[i+1].start() if i+1<len(ms) else len(t); section=t[m.start():end]
  cms=list(cre.finditer(section))
  for j,c in enumerate(cms,1):
   literal=c.group(1).strip(); st=status(literal)
   if st=='ok':continue
   before=section[:c.start()]
   hs=list(re.finditer(r'(?m)^#{2,6}\s+([^\n]+)',before)); start=hs[-1].start() if hs else 0
   stop=len(section)
   nh=re.search(r'(?m)^#{2,6}\s+',section[c.end():])
   if nh:stop=c.end()+nh.start()
   raw_block=section[start:stop].rstrip()
   label=(hs[-1].group(1).strip() if hs else f'conclusion-{j}')
   local=f"{m.group(1).lower()}:{re.sub(r'[^A-Za-z0-9_.-]+','-',label).strip('-') or j}"
   out.append({'eid':m.group(1).lower(),'local_id':local,'literal_status':literal,'status':st,'text':raw_block,'line':bisect.bisect_right(starts,m.start()+start)})
  # Some frozen primary reports put the only status in the entry heading.
  heading=section.splitlines()[0] if section.splitlines() else ''
  hst=status(heading)
  if hst not in ('ok','unknown') and not cms:
   out.append({'eid':m.group(1).lower(),'local_id':f"{m.group(1).lower()}:heading-status",'literal_status':heading.strip(),'status':hst,'text':section.rstrip(),'line':bisect.bisect_right(starts,m.start())})
  # An explicit observation/advisory field remains a separate record even when
  # the entry-level conclusion is OK (for example gemini-024 entry-00948).
  for o in ore.finditer(section):
   label=o.group(1).strip(); st=status(label); st=st if st!='unknown' else 'unknown'
   line=bisect.bisect_right(starts,m.start()+o.start())
   out.append({'eid':m.group(1).lower(),'local_id':f"{m.group(1).lower()}:observation-L{line}",'literal_status':label,'status':st,'text':o.group(0).rstrip(),'line':line})
  for o in ire.finditer(section):
   literal=o.group(2);line=bisect.bisect_right(starts,m.start()+o.start())
   out.append({'eid':m.group(1).lower(),'local_id':f"{m.group(1).lower()}:inline-status-L{line}",'literal_status':literal,'status':status(literal),'text':o.group(1).rstrip(),'line':line})
 return out
def singleton_cross_claims(p,eid):
 """Bounded adapter for a one-entry cross report whose Claim headings omit ID."""
 t=use(p).read_text(encoding='utf-8'); heads=list(re.finditer(r'(?mi)^#{2,6}\s+(Claim\s*\d+)[^\n]*',t));out=[]
 for i,m in enumerate(heads):
  end=heads[i+1].start() if i+1<len(heads) else len(t);block=t[m.start():end].rstrip()
  cm=re.search(r'(?mi)^\s*(?:\*\*)?结论(?:\*\*)?\s*[：:]\s*(?:\*\*)?([^*\n]+)',block)
  literal=cm.group(1).strip() if cm else 'unknown';st=status(literal)
  out.append({'eid':eid,'local_id':re.sub(r'\s+','-',m.group(1).lower()),'literal_status':literal,'status':st,'text':block,'line':t.count('\n',0,m.start())+1})
 return out
def preserve_entry_gaps(p, entry_blocks, parsed, author, validity='valid'):
 """Keep unparsed source blocks; coverage is never evidence of claim ingestion.

 This fallback makes no translation or status judgment. A known-clear OK block
 needs no finding; an unrecognized block or omitted observation marker remains
 an explicit source-local parsing task with its complete original text.
 """
 links=[]
 marker=re.compile(r'细微观察|存在疑点|待确认|\b(?:pending|advisory|confirmed|refuted)\b',re.I)
 for b in entry_blocks:
  owned=[x for x in parsed if x['eid']==b['eid']]
  retained='\n'.join(x['text'] for x in owned)
  omitted=[line for line in b['text'].splitlines() if marker.search(line) and line.strip() not in retained]
  if owned and not omitted:continue
  if not owned and b['status']=='ok' and not omitted:continue
  lid=f"{b['eid']}:unparsed-entry-L{b['line']}"
  reason='Original entry block preserved; claim/status extraction is unresolved. Coverage and STATE summaries do not resolve this gap.'
  rid=addraw(p.stem,lid,b['eid'],'unknown',b['text'],p,author,validity,
             reason=reason if validity!='valid' else None,line=b['line'],
             kind='unparsed_source_entry',literal_status='unparsed; consult original_text')
  links.append({'local_id':lid,'line':b['line'],'entry_id':b['eid'],
                'disposition':'unresolved' if validity=='valid' else 'excluded_invalid',
                'output_refs':[rid],'raw_text':b['text'],'reason':reason})
 return links
def jb(x):return (json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
def cb(rows,fields):
 s=io.StringIO(newline=''); w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n'); w.writeheader();w.writerows(rows);return s.getvalue().encode()

invp=use(CAM/'inventory.json'); statep=use(CAM/'STATE.json'); inv=load(invp)['entries']; state=load(statep)
ids=[x['audit_id'] for x in inv]; idset=set(ids)
if len(ids)!=4144 or len(idset)!=4144:raise SystemExit('bad inventory identity')
rows={}
for x in inv:
 e=x['audit_id']; rows[e]={'entry_id':e,'component':x['component'],'logical_path':x['logical_path'],'line':x['line'],'section':x['section'],'source_tag':x['source_tag'],'snapshot_sha256':x['snapshot_sha256'],'original_batch':None,'events':[],'coverage':{'initial_full_entry_review':False,'cross_review':False,'experiment_full_entry_review':False,'bounded_calibration':False,'adjudication':False},'todo_status':[]}
unknown=set(); ekeys=set(); accounting=[]; raw=[]; rawkeys=set(); claims={}; unresolved=[]
def account(p,adapter,expected,included,excluded=0,unresolved_count=0,note=None,records=None):
 use(p); accounting.append({'path':rel(p),'sha256':sha(p),'adapter':adapter,'expected_records':expected,'included_records':included,'excluded_records':excluded,'unresolved_records':unresolved_count,'note':note,'records':records or []})
 if adapter=='campaign_cross_report_local':
  rs=records or []
  accounting[-1]['record_counts_by_kind']={
   'coverage':sum(bool(r.get('output_refs')) and all(z.startswith('coverage:') for z in r['output_refs']) for r in rs),
   'parsed_source_claim':sum(r['disposition']=='included' and any(not z.startswith('coverage:') for z in r.get('output_refs',[])) for r in rs),
   'unresolved_source_block':sum(r['disposition']=='unresolved' for r in rs)}
def event(e,layer,out,inp,valid,kind,qual,identity):
 if e not in idset:unknown.add(e);return
 use(out);use(inp); k=(e,layer,rel(out),rel(inp),valid,kind)
 if k in ekeys:return
 ekeys.add(k); rows[e]['events'].append({'layer':layer,'kind':kind,'valid':valid,'qualification':qual,'identity_check':identity,'output':rel(out),'output_sha256':sha(out),'input':rel(inp),'input_sha256':sha(inp)})
 if valid:rows[e]['coverage'][layer]=True
def addraw(ns,lid,e,st,text,src,author,valid='valid',mapped=None,reason=None,line=None,kind='observation',literal_status=None,adjudications=None,atom_mappings=None):
 es=[e] if isinstance(e,str) else list(e)
 for z in es:
  if z not in idset:unknown.add(z)
 if not es or any(z not in idset for z in es):return
 rid=f'{ns}:{lid}'; k=(rid,rel(src))
 if k in rawkeys:
  rec=next(x for x in raw if x['observation_id']==rid and x['source']['path']==rel(src))
  rec['entry_ids']=sorted(set(rec['entry_ids']+es));rec['entry_id']=rec['entry_ids'][0]
  rec['mapped_claims']=sorted(set(rec['mapped_claims']+(mapped or [])))
  rec['adjudications']+= [x for x in (adjudications or []) if x not in rec['adjudications']]
  rec['atom_mappings']+= [x for x in (atom_mappings or []) if x not in rec['atom_mappings']]
  return rid
 rawkeys.add(k);use(src); rec={'observation_id':rid,'entry_id':e,'historical_status':st,'original_text':text,'author':author,'validity':valid,'source':loc(src,lid,line),'source_sha256':sha(src),'record_kind':kind,'mapped_claims':mapped or [],'exclusion_reason':reason};raw.append(rec)
 rec['entry_ids']=sorted(set(es));rec['entry_id']=rec['entry_ids'][0];rec['literal_status']=literal_status if literal_status is not None else st;rec['adjudications']=adjudications or [];rec['atom_mappings']=atom_mappings or []
 if valid=='valid' and st!='ok' and not mapped:unresolved.append({'observation_id':rid,'entry_id':rec['entry_id'],'entry_ids':rec['entry_ids'],'status':st,'reason':'no explicit canonical mapping in existing evidence','source':rec['source']})
 return rid
def addclaim(cid,e,st,text,src,lid,authority,qual,mapped=None):
 if e not in idset:unknown.add(e);return
 use(src); hist={'status':st,'source':loc(src,lid),'source_sha256':sha(src),'authority':authority,'qualification':qual}
 if cid in claims:
  if claims[cid]['entry_id']!=e:raise SystemExit('claim collision '+cid)
  if hist not in claims[cid]['status_history']:claims[cid]['status_history'].append(hist)
  claims[cid]['mapped_observations']=sorted(set(claims[cid]['mapped_observations']+(mapped or [])));return
 claims[cid]={'claim_id':cid,'entry_id':e,'claim_text':text,'status_history':[hist],'effective_status':st,'effective_source':hist['source'],'mapped_observations':sorted(set(mapped or [])),'calibration':[]}
def calibrate(cid,st,src,lid,reason,authority):
 if cid not in claims:raise SystemExit('missing calibration target '+cid)
 use(src); x={'status':st,'source':loc(src,lid),'source_sha256':sha(src),'reason':reason,'authority':authority};claims[cid]['calibration'].append(x);claims[cid]['effective_status']=st;claims[cid]['effective_source']=x['source']
def abc_original_status(a):
 """Recover only an explicitly labelled original status; never use host status."""
 if not a:return ('unknown','unknown')
 candidates=[]
 for key in ('original_label','original_assertion'):
  if a.get(key):candidates.append(str(a[key]).strip())
 text=str(a.get('text') or '')
 for m in re.finditer(r'(?mi)^\s*(?:[-*]\s*)?(?:\*\*)?(?:复核结论|结论|状态|判断)(?:\*\*)?\s*[：:]\s*(?:\*\*)?([^*\n]+)',text):
  candidates.append(m.group(1).strip())
 first=text.splitlines()[0].strip() if text.splitlines() else ''
 if first:candidates.append(first)
 for literal in candidates:
  st=status(literal)
  if st!='unknown':return (st,literal)
 return ('unknown',candidates[0] if candidates else 'unknown')

# Campaign primary: selected output paths/dispatches only; entry markers prove coverage.
batch_mismatch=[]; selected_primary=set()
for b in state['batches']:
 inp=use(ROOT/b['input_path'])
 if b.get('input_sha256') and sha(inp)!=b['input_sha256']:batch_mismatch.append(b['batch_id'])
 allowed=set(b['entry_ids'])
 for e in allowed:rows[e]['original_batch']=b['batch_id']
 paths=[]
 for k in ('raw_output_path','supplement_raw_output_path'):
  if b.get(k) and (ROOT/b[k]).is_file():paths.append((ROOT/b[k]).resolve())
 for d in b.get('dispatches',[]):
  p=CAM/'reports'/f'{d}.md'
  if p.is_file():paths.append(p.resolve())
 for p in sorted(set(paths)):
  selected_primary.add(p); bs=[x for x in blocks(p) if x['eid'] in allowed]
  for x in bs:
   event(x['eid'],'initial_full_entry_review',p,inp,True,'campaign_primary','selected output','report entry ID in frozen batch')
  cs=[x for x in markdown_claims(p) if x['eid'] in allowed]
  links=[]
  for x in cs:
   rid=addraw(p.stem,x['local_id'],x['eid'],x['status'],x['text'],p,p.stem.split('-')[0],line=x['line'],kind='campaign_primary_claim',literal_status=x['literal_status'])
   links.append({'local_id':x['local_id'],'disposition':'included','output_refs':[rid]})
  gaps=preserve_entry_gaps(p,bs,cs,p.stem.split('-')[0]);links+=gaps
  account(p,'campaign_primary_markdown_claims',len(links),len(cs),unresolved_count=len(gaps),note=rel(inp),records=links)
for p in sorted((CAM/'reports').glob('gemini-*.md')):
 if p.resolve() in selected_primary:continue
 bs=blocks(p)
 cs=markdown_claims(p);links=[]
 for x in cs:
  rid=addraw(p.stem,x['local_id'],x['eid'],x['status'],x['text'],p,'gemini','invalid',reason='not selected by explicit batch mapping',line=x['line'],kind='campaign_primary_claim',literal_status=x['literal_status'])
  links.append({'local_id':x['local_id'],'disposition':'excluded_invalid','output_refs':[rid],'reason':'not selected by explicit batch mapping'})
 links+=preserve_entry_gaps(p,bs,cs,'gemini','invalid')
 account(p,'campaign_primary_unselected_claims',len(links),0,excluded=len(links),note='invalid historical output',records=links)

# Ten prior checks use exact frozen identity.
spot=use(ROOT/'evidence/spotchecks/modified-translation-spotcheck-20260921/reviewer-full-02.md'); wsp=use(ROOT/'evidence/spotchecks/modified-translation-spotcheck-20260921/workset.json'); wt={x['revision_key']:x for x in load(wsp)['entries']}; txt=spot.read_text(encoding='utf-8');pf=[]
for x in inv:
 if not x.get('prior_spotcheck'):continue
 f=wt.get(x['prior_spotcheck']);ok=bool(f and x['prior_spotcheck'] in txt and f['source']==x['source'] and f['target']==x['target'] and f['section']==x['section'] and f['line']==x['line'])
 if not ok:pf.append(x['audit_id'])
 event(x['audit_id'],'initial_full_entry_review',spot,wsp,ok,'prior_spotcheck',x['prior_spotcheck'],'revision key + exact source/target/section/line')
account(spot,'prior_spotcheck_exact_identity',10,10-len(pf),unresolved_count=len(pf))

# Cross mapping follows raw/result dispatch, never cross number.
selected_cross=set();cross_state_records=[]
for c in state['cross_reviews']:
 inp=ROOT/c['input_path']; p=None
 if c.get('raw_output_path') and (ROOT/c['raw_output_path']).is_file():p=(ROOT/c['raw_output_path']).resolve()
 for k in ('replacement_dispatch_id','result_dispatch_id'):
  q=CAM/'reports'/f"{c.get(k,'')}.md"
  if c.get(k) and q.is_file():p=q.resolve()
 if p is None:
  for d in reversed(c.get('dispatches',[])):
   q=CAM/'reports'/f'{d}.md'
   if q.is_file() and d!='sol-091-01':p=q.resolve();break
 if p is None:continue
 selected_cross.add(p); allowed=set(c['entry_ids']);bs=blocks(p);present={x['eid'] for x in bs}&allowed
 source_claims=[x for x in markdown_claims(p) if x['eid'] in allowed]
 if not source_claims and not present and len(allowed)==1:
  source_claims=singleton_cross_claims(p,next(iter(allowed)))
  if source_claims:present=set(allowed)
 coverage_records=[]
 for e in sorted(present):
  event(e,'cross_review',p,inp,True,'campaign_cross','selected cross output','STATE output/dispatch + report ID in frozen input')
  b=next((x for x in bs if x['eid']==e),None);line=b['line'] if b else source_claims[0]['line']
  coverage_records.append({'local_id':f'{e}@L{line}','disposition':'included','output_refs':[f'coverage:{e}:campaign_cross:{p.name}']})
 rec=c.get('recorded_cross_verdicts',[]);inc=0
 for i,x in enumerate(rec,1):
  e=x.get('entry_id') or (next(iter(allowed)) if len(allowed)==1 else None)
  sid=f"{c['cross_id']}:state-{i}"
  if not e:
   unresolved.append({'observation_id':sid,'entry_id':None,'status':x.get('verdict','unknown'),'reason':'multi-entry STATE claim lacks entry mapping','source':loc(statep,f"{c['cross_id']}[{i-1}]")})
   cross_state_records.append({'local_id':f"{c['cross_id']}[{i-1}]",'disposition':'unresolved','output_refs':[],'reason':'summary-only STATE claim lacks exact entry mapping'});continue
  rid=addraw(c['cross_id'],f'state-{i}',e,x.get('verdict','unknown'),x.get('claim',''),statep,c.get('verdict_author','cross reviewer'),kind='state_recorded_cross_verdict');inc+=1
  cross_state_records.append({'local_id':f"{c['cross_id']}[{i-1}]",'disposition':'included','output_refs':[rid],'reason':'STATE summary retained separately; not credited as report-local consumption'})
 claim_records=[]
 for x in source_claims:
  rid=addraw(p.stem,x['local_id'],x['eid'],x['status'],x['text'],p,'cross reviewer',line=x['line'],kind='campaign_cross_claim',literal_status=x['literal_status'])
  claim_records.append({'local_id':f"{x['local_id']}@L{x['line']}",'disposition':'included','output_refs':[rid]})
 gap_records=preserve_entry_gaps(p,[x for x in bs if x['eid'] in allowed],source_claims,'cross reviewer')
 report_records=coverage_records+claim_records+gap_records
 if not report_records:
  report_records=[{'local_id':'raw-report@L1','disposition':'unresolved','output_refs':[],'reason':'report has no exact entry/claim locator in supported frozen formats; preserved without semantic mapping','line':1,'raw_text':use(p).read_text(encoding='utf-8')}]
 account(p,'campaign_cross_report_local',len(report_records),sum(x['disposition']=='included' for x in report_records),unresolved_count=sum(x['disposition']=='unresolved' for x in report_records),note=f"{c['cross_id']} -> {p.name}; STATE summaries accounted separately",records=report_records)
if cross_state_records:
 account(statep,'campaign_cross_state_summaries',len(cross_state_records),sum(x['disposition']=='included' for x in cross_state_records),unresolved_count=sum(x['disposition']=='unresolved' for x in cross_state_records),records=cross_state_records,note='summary-only records; never credited as report-local claims')
for p in sorted((CAM/'reports').glob('sol-*.md')):
 if p.resolve() in selected_cross:continue
 cs=markdown_claims(p);reason='wrong frozen input; replaced by sol-091-02' if p.name=='sol-091-01.md' else 'not selected by explicit cross mapping';links=[]
 for x in cs:
  rid=addraw(p.stem,x['local_id'],x['eid'],x['status'],x['text'],p,'cross reviewer','invalid',reason=reason,line=x['line'],kind='campaign_cross_claim',literal_status=x['literal_status'])
  links.append({'local_id':x['local_id'],'disposition':'excluded_invalid','output_refs':[rid],'reason':reason})
 account(p,'campaign_cross_unselected_claims',len(cs),0,excluded=len(cs),note=reason,records=links)

# ABC cumulative canonical D plus group D/P/O mappings.
abcs=use(EXP/'abc20-20260923/STATE.json'); ast=load(abcs); acp=use(EXP/'abc20-20260923/MERGED-FINDINGS.json'); ac=load(acp)
abc_pending_expected=set();abc_original_expected={}
for d in ac['defects']:
 cid=f"abc:g{int(d['group']):02d}:{d['canonical_id'].split('-',1)[-1]}";addclaim(cid,d['entry_id'],'confirmed_provisional',d['evidence'],acp,d['canonical_id'],'ABC host adjudication','provisional; not human gold')
account(acp,'abc_cumulative_canonical_defects',len(ac['defects']),len(ac['defects']))
for g in ast['groups']:
 n=int(g['index']); dr=EXP/g['directory']
 if n>14 or g.get('state')!='DONE':continue
 ep=dr/'entries.json';rp=dr/'REFERENCE.json';mp=dr/'MERGED-FINDINGS.json';out=mp if mp.is_file() else rp
 for e in g['entry_ids']:
  event(e,'experiment_full_entry_review',out,ep,True,'abc_group','group1 protocol anomaly' if n==1 else 'completed group','STATE directory + explicit group IDs');event(e,'adjudication',out,ep,True,'abc_reference','provisional; not human gold','REFERENCE/MERGED mapped to entries')
 if not rp.is_file():continue
 r=load(rp);prefix=f'abc:g{n:02d}'; merged=load(mp) if mp.is_file() else {};oi=0
 anonp=dr/'ANON-MAPPING-HOST-ONLY.json';anon_by_id={}
 if anonp.is_file():anon_by_id={x['observation_id']:x for x in load(anonp)['observations']}
 adjudp=dr/r.get('report','reports/adjudication-01.md');pdefs={}
 if adjudp.is_file():
  at=use(adjudp).read_text(encoding='utf-8')
  for m in re.finditer(r'(?m)^- \*\*[^\n]+',at):
   for pid,e in re.findall(r'(P\d+)｜(entry-\d{5})',m.group(0)):
    pdefs[pid]={'entry_id':e,'text':m.group(0),'line':at.count('\n',0,m.start())+1,'label':'report pending'}
  # Some reports put the status in a compact entry table and explain it later.
  for m in re.finditer(r'(?m)^\|\s*(entry-\d{5})\s*\|\s*PENDING\s*\|\s*(P\d+)[^|]*\|',at):
   pdefs.setdefault(m.group(2),{'entry_id':m.group(1),'text':m.group(0),'line':at.count('\n',0,m.start())+1,'label':'report pending'})
 for pid,pd in sorted(pdefs.items()):
  addclaim(f'{prefix}:{pid}',pd['entry_id'],'pending',pd['text'],adjudp,pid,'ABC host adjudication','pending; provisional')
 for did,d in r.get('canonical_defects',{}).items():
  if f'{prefix}:{did}' not in claims:addclaim(f'{prefix}:{did}',d['entry_id'],'confirmed_provisional',d.get('evidence',''),rp,did,'ABC group reference','provisional; not human gold')
 pending_ids=set(r.get('pending_observations',[]));abc_pending_expected.update(f'{prefix}:{x}' for x in pending_ids);pend=r.get('pending',[]);pend=list(pend.values()) if isinstance(pend,dict) else pend
 for p in pend:
  pid=p.get('id','P?');addclaim(f'{prefix}:{pid}',p['entry_id'],'pending',p.get('reason',''),rp,pid,'ABC group adjudication','pending; provisional',[f"{prefix}:{p['observation']}"] if p.get('observation') else [])
 for oid,o in r.get('observations',{}).items():
  mapped=[f'{prefix}:{d}' for d in o.get('defects',[])];a=anon_by_id.get(oid);e=a and a.get('entry_id')
  for pid in re.findall(r'\bP\d+\b',o.get('rationale','')):
   cid=f'{prefix}:{pid}'
   if cid in claims:mapped.append(cid);e=e or claims[cid]['entry_id']
  e=e or next((claims[c]['entry_id'] for c in mapped if c in claims),None)
  if e is None:
   for d in merged.get('confirmed_defects',[]):
    if any(s.get('observation_id')==oid for s in d.get('sources',[])):e=d['entry_id'];mapped.append(f"{prefix}:{d['defect_id']}");break
  if e is None:
   q=next((p for p in pend if p.get('observation')==oid),None);e=q and q['entry_id']
  if e is None:unresolved.append({'observation_id':f'{prefix}:{oid}','entry_id':None,'status':o.get('status','unknown'),'reason':'ABC observation lacks explicit entry mapping','source':loc(rp,oid)});continue
  src=rp;text=o.get('rationale','');author='ABC reviewer/adjudicator';line=None
  if a:
   report=dr/'reports'/f"{a['origin']}.md"
   if report.is_file():src=report;line=use(report).read_text(encoding='utf-8').count('\n',0,a.get('start',0))+1
   else:src=anonp
   text=a.get('text') or a.get('original_assertion') or text;author=a.get('origin') or author
  original_st,literal=abc_original_status(a)
  rid=f'{prefix}:{oid}';abc_original_expected[rid]=(original_st,literal)
  addraw(prefix,oid,e,original_st,text,src,author,mapped=sorted(set(mapped)),line=line,kind='abc_observation',literal_status=literal,adjudications=[{'status':o.get('status','unknown'),'authority':'ABC host adjudication','source':loc(rp,oid),'text':o.get('rationale','')}])
  for cid in mapped:
   if cid in claims:claims[cid]['mapped_observations']=sorted(set(claims[cid]['mapped_observations']+[f'{prefix}:{oid}']))
  oi+=1
 pcount=len({c for c in claims if c.startswith(prefix+':P')})
 account(rp,'abc_group_D_P_O',len(r.get('canonical_defects',{}))+len(r.get('observations',{}))+pcount,len(r.get('canonical_defects',{}))+oi+pcount,unresolved_count=len(r.get('observations',{}))-oi,note=f"pending_observation_ids={len(pending_ids)}; exact_anon_links={sum(x in anon_by_id for x in r.get('observations',{}))}")
 if mp.is_file():account(mp,'abc_merged_mapping_crosscheck',len(merged.get('confirmed_defects',[]))+len(merged.get('observation_decisions',{})),len(merged.get('confirmed_defects',[]))+len(merged.get('observation_decisions',{})))

# Pilot structured claims and crosswalk.
pd=EXP/'calibrated-pilot40-20260923';pep=use(pd/'entries.json');prp=use(pd/'RESULT.json');pcp=use(pd/'CLAIM-CROSSWALK.json');pr=load(prp);pc=load(pcp);pe=load(pep)
for x in (pe.get('entries',[]) if isinstance(pe,dict) else pe):event(x['audit_id'],'experiment_full_entry_review',prp,pep,True,'calibrated_pilot','full entry review in bounded research sample','explicit membership')
for key,st in [('confirmed_claims','confirmed'),('pending_claims','pending')]:
 for c in pr[key]:addclaim(f"pilot:{c['id']}",c['entry_id'],st,c['reason'],prp,c['id'],'pilot host adjudication','not human gold')
for x in pc:
 addraw(f"pilot:{x['arm']}",x['observation_id'],x['entry_ids'],x['reported_status'],x['reason'],pcp,x['arm'],mapped=[f'pilot:{z}' for z in x.get('canonical_ids',[])],kind='pilot_crosswalk',literal_status=x['reported_status'],adjudications=[{'status':x['host_status'],'authority':'pilot host','source':loc(pcp,f"{x['arm']}:{x['observation_id']}")}])
account(prp,'pilot_result_claims',len(pr['confirmed_claims'])+len(pr['pending_claims']),len(pr['confirmed_claims'])+len(pr['pending_claims']));account(pcp,'pilot_claim_crosswalk',len(pc),len(pc))

# AB canonical claims and exact observation mappings, including split A2/C02.*.
ad=EXP/'process-ab40-20260923';aep=use(ad/'entries.json');aap=use(ad/'ADJUDICATION.json');aa=load(aap);ae=load(aep)
for x in (ae.get('entries',[]) if isinstance(ae,dict) else ae):event(x['audit_id'],'experiment_full_entry_review',aap,aep,True,'process_ab','full entry review in bounded experiment','explicit membership')
for c in aa['canonical']:addclaim(f"ab:{c['id']}",c['entry'],c['status'],c['reason'],aap,c['id'],'AB host adjudication','not human gold')
def report_claim(path,cid):
 if not path.is_file():return None
 t=use(path).read_text(encoding='utf-8');ids=[cid]
 if '.' in cid:ids.append(cid.split('.')[0])
 def mentions(line,z):
  if re.search(rf'(?<![A-Z0-9.]){re.escape(z)}(?![0-9.])',line):return True
  if z.startswith('C') and z[1:].isdigit():
   n=int(z[1:])
   for a,b in re.findall(r'\bC(\d+)[–-](?:C)?(\d+)\b',line):
    if int(a)<=n<=int(b):return True
  return False
 m=None
 for z in ids:
  pat=re.compile(rf'(?mi)^(?:#{{2,6}}\s+|\*\*){re.escape(z)}(?![0-9.])[^\n]*')
  m=pat.search(t)
  if m:break
 if m:
  heading=m.group(0);n=re.search(r'(?m)^(?:#{2,6}\s+|\*\*[A-Z]\d)',t[m.end():]);end=m.end()+n.start() if n else len(t);b=t[m.start():end].rstrip();line=t.count('\n',0,m.start())+1
  entry_ids=EID.findall(heading)
 else:
  found=next(((i,x) for i,x in enumerate(t.splitlines(),1) if any(mentions(x,z) for z in ids)),None)
  if not found:return None
  line,b=found;entry_ids=EID.findall(b)
 if not entry_ids:
  # Exact table association: same row may use entry-03862 or the bare 03862.
  assoc=next((x for x in t.splitlines() if any(mentions(x,z) for z in ids) and (EID.search(x) or re.search(r'\|\s*(\d{5})\s*\|',x))),None)
  if assoc:
   entry_ids=EID.findall(assoc)
   if not entry_ids:
    entry_ids=['entry-'+x for x in re.findall(r'(?:^|\|)\s*(\d{5})\s*(?=\|)',assoc)]
 return {'text':b,'entry_ids':list(dict.fromkeys(entry_ids)),'line':line,'path':path}
aoi=0;ab_explicit_multi={};ab_records=[{'local_id':c['id'],'disposition':'included','output_refs':[f"ab:{c['id']}"]} for c in aa['canonical']]
for o in aa['observations']:
 mapped=[f'ab:{x}' for x in o.get('canonical',[])];stagep=ad/'reports'/f"{o['stage']}.md";src=report_claim(stagep,o['id'])
 if not src and o['stage']=='B2':src=report_claim(ad/'reports/B3.md',o['id'])
 es=(src and src['entry_ids']) or []
 if not es:
  mapped_entry=next((claims[c]['entry_id'] for c in mapped if c in claims),None);es=[mapped_entry] if mapped_entry else []
 if not es:
  unresolved.append({'observation_id':f"ab:{o['stage']}:{o['id']}",'entry_id':None,'status':o.get('source_status','unknown'),'reason':'AB report and canonical mapping have no explicit entry association','source':loc(stagep if stagep.is_file() else aap,f"{o['stage']}/{o['id']}")});ab_records.append({'local_id':f"{o['stage']}:{o['id']}",'disposition':'unresolved','output_refs':[],'reason':'no explicit entry association in bounded AB sources'});continue
 rid=f"ab:{o['stage']}:{o['id']}"
 if src and len(es)>1:ab_explicit_multi[rid]=sorted(es)
 addraw(f"ab:{o['stage']}",o['id'],es,o.get('source_status','unknown'),src['text'] if src else json.dumps(o,ensure_ascii=False,sort_keys=True),src['path'] if src else aap,o['stage'],mapped=mapped,line=src and src['line'],kind='ab_observation',literal_status=o.get('source_status','unknown'),adjudications=[{'status':o.get('host_decision','unknown'),'authority':'AB host adjudication','source':loc(aap,f"{o['stage']}/{o['id']}"),'text':o.get('reason','')}])
 for cid in mapped:claims[cid]['mapped_observations']=sorted(set(claims[cid]['mapped_observations']+[rid]))
 ab_records.append({'local_id':f"{o['stage']}:{o['id']}",'disposition':'included','output_refs':[rid]});aoi+=1
account(aap,'process_ab_canonical_and_observation_mapping',len(aa['canonical'])+len(aa['observations']),len(aa['canonical'])+aoi,unresolved_count=len(aa['observations'])-aoi,records=ab_records)

# Calibration-10 and exact later user boundaries.
cd=EXP/'calibration-10-20260923';cmp=use(cd/'CLAIM-CROSSWALK.json');crp=use(cd/'RESULT.json');cm=load(cmp);cr=load(crp);hmp=use(cd/'HOST-MAPPING.json')
creport=use(cd/'REPORT.md');ct=creport.read_text(encoding='utf-8');cal_pending_entry={pid:x['entry_id'] for x in cr['entries'] for pid in x.get('pending',[])};cal_pending={}
for m in re.finditer(r'(?m)^\|\s*(P\d+)\s*\|\s*(K\d+)\s*\|\s*([^\n]+?)\s*\|$',ct):
 pid,kid,body=m.groups();e=cal_pending_entry.get(pid);cal_pending[pid]={'entry_id':e,'text':m.group(0),'line':ct.count('\n',0,m.start())+1,'k_id':kid,'body':body}
for pid,x in sorted(cal_pending.items()):
 if not x['entry_id']:raise SystemExit('calibration pending lacks RESULT entry '+pid)
 addclaim(f'cal10:{pid}',x['entry_id'],'pending',x['text'],creport,pid,'calibration-10 host','pending; provisional')
for e in sorted({x['entry_id'] for x in cr['entries']}):event(e,'bounded_calibration',crp,hmp,True,'calibration10','duplicate provisional sample','HOST-MAPPING exact ID')
for x in cm['old_canonical_claims']:
 g,d=x['old_id'].split('-');calibrate(f"abc:g{int(g[1:]):02d}:{d}",x['new_status'],cmp,x['id'],x['reason'],'calibration-10 explicit crosswalk')
for x in cm['new_claims']:addclaim(f"cal10:{x['id']}",x['entry_id'],x['text_status'],x['note'],cmp,x['id'],'calibration-10 host','provisional; not human gold')
account(cmp,'calibration10_explicit_crosswalk',len(cm['old_canonical_claims'])+len(cm['new_claims']),len(cm['old_canonical_claims'])+len(cm['new_claims']));account(crp,'calibration10_entry_results',len(cr['entries']),len(cr['entries']));account(creport,'calibration10_pending_claims',len(cal_pending),len(cal_pending),records=[{'local_id':pid,'disposition':'included','output_refs':[f'cal10:{pid}']} for pid in sorted(cal_pending)])
usercal={'abc:g12:D08':'first attacked/first hit 仅需澄清，不计确认错译','abc:g11:D14':'文明人/普通人仅需澄清，不计确认错译','abc:g11:D08':'施加/增强的概括仅需澄清，不计确认错译'}
for cid,why in usercal.items():calibrate(cid,'advisory',cmp,'user-boundary:'+cid,why,'later explicit user calibration')
for pid,cid in {'P01':'abc:g12:D08','P05':'abc:g11:D14','P09':'abc:g11:D08'}.items():
 calibrate(f'cal10:{pid}','advisory',cmp,'user-boundary:'+pid,usercal[cid],'later explicit user calibration')

# Flash: actual references, frozen input and fenced-JSON run outputs.
fd=EXP/'gemini-flash-tuning-20260923';lp=use(fd/'RUN-LEDGER.json');ledger={x['dispatch']:x for x in load(lp)};drp=use(fd/'HOST-DEV-REFERENCE.json');hrp=use(fd/'HOST-HOLDOUT-INITIAL.json');hfp=use(fd/'HOLDOUT-FINAL-ADJUDICATION.json');dv=load(drp);ho=load(hrp);hf=load(hfp)
for c in dv['claims']:
 if f"ab:{c['id']}" not in claims:addclaim(f"ab:{c['id']}",c['entry'],c['status'],c['reason'],drp,c['id'],'Flash copied AB reference','derived, not independent truth')
for c in ho['claims']:addclaim(f"flash-holdout:{c['id']}",c['entry'],c['status'],c['reason'],hrp,c['id'],'host holdout initial','provisional; not human gold')
for x in ho['coverage']:event(x['entry'],'experiment_full_entry_review',hrp,fd/'holdout/entries.json',True,'flash_holdout_reference','host provisional full entry review','explicit coverage row')
account(drp,'flash_dev_reference_alias_to_ab',len(dv['claims']),len(dv['claims']),note='aliases ab:*');account(hrp,'flash_holdout_initial',len(ho['claims'])+len(ho['coverage']),len(ho['claims'])+len(ho['coverage']))
norm={}
for np in sorted((fd/'normalized').glob('*-mapped.json')):
 dispatch=np.stem.removesuffix('-mapped');nd=load(np);norm[dispatch]={}
 for m in nd.get('mappings',[]):norm[dispatch].setdefault(m['claim_id'],[]).append({**m,'source':loc(np,m['claim_id'])})
 account(np,'flash_normalized_exact_mapping',len(nd.get('mappings',[])),len(nd.get('mappings',[])),records=[{'local_id':f"{dispatch}:{m['claim_id']}:{m.get('atom_id','')}",'disposition':'included','output_refs':[f"flash:{dispatch}:{m['claim_id']}"]} for m in nd.get('mappings',[])])
finalmap={x['claim']:x for x in hf['final_pair'].get('F00-r2',[])}
def fence(p):
 t=use(p).read_text(encoding='utf-8');m=re.search(r'```json\s*(\{.*\})\s*```',t,re.S)
 if not m:raise ValueError('no fenced JSON '+str(p))
 return json.loads(m.group(1))
for p in sorted((fd/'reports').glob('*.md')):
 dispatch=p.stem.removesuffix('-full')
 if p.stem.endswith('-full'):account(p,'flash_duplicate_full_copy',1,0,excluded=1,note='duplicate excluded');continue
 doc=fence(p);claimsrc=p;recovered=fd/'normalized'/f'{dispatch}-recovered.json'
 if recovered.is_file():
  rd=load(recovered);doc=rd['data'];claimsrc=recovered
  account(recovered,'flash_recovered_claim_ids',len(doc.get('claims',[])),len(doc.get('claims',[])),note='host recovery artifact; not model-original JSON, selected by matching valid dispatch')
 bad=bool(ledger.get(dispatch,{}).get('excluded_assignment'));subset='dev' if dispatch.startswith('dev-') else 'holdout';inp=fd/subset/'entries.json'
 for x in doc.get('entries',[]):event(x['id'],'experiment_full_entry_review',p,inp,not bad,f'flash_{subset}_run','excluded wrong input' if bad else 'actual fenced JSON full entry review','RUN-LEDGER + frozen subset ID')
 for c in doc.get('claims',[]):
  e=c.get('entry_id') or c.get('entry');e=e if isinstance(e,str) and EID.fullmatch(e) else next((x['id'] for x in doc.get('entries',[]) if c.get('id') in x.get('claim_ids',[])),None)
  if not e:continue
  atoms=norm.get(dispatch,{}).get(str(c.get('id','claim')),[]);refs=[]
  for a in atoms:refs.extend(a.get('reference_ids',[]))
  refs=refs or c.get('reference_ids') or ([c['reference_id']] if c.get('reference_id') else []);mapped=[]
  for z in refs:
   cid=f'ab:{z}' if subset=='dev' else f'flash-holdout:{z}'
   if cid in claims:mapped.append(cid)
  adjs=[{'status':a.get('verdict','unknown'),'authority':'Flash normalized host mapping','source':a['source'],'text':a.get('reason','')} for a in atoms]
  if dispatch=='holdout-F00-r2' and str(c.get('id')) in finalmap:
   f=finalmap[str(c['id'])];zs=f['reference'] if isinstance(f['reference'],list) else [f['reference']];mapped=sorted(set(mapped+[f'flash-holdout:{z}' for z in zs if f'flash-holdout:{z}' in claims]));adjs.append({'status':f['decision'],'authority':'Flash holdout final host adjudication','source':loc(hfp,f"F00-r2:{c['id']}"),'text':f['reason']})
  addraw(f'flash:{dispatch}',str(c.get('id','claim')),e,str(c.get('status','unknown')).lower(),json.dumps(c,ensure_ascii=False,sort_keys=True),claimsrc,'gemini-flash','invalid' if bad else 'valid',sorted(set(mapped)),'RUN-LEDGER excluded assignment' if bad else None,kind='flash_recovered_claim' if claimsrc!=p else 'flash_fenced_json_claim',literal_status=str(c.get('status','unknown')),adjudications=adjs,atom_mappings=atoms)
 account(p,'flash_fenced_json_run',len(doc.get('entries',[]))+len(doc.get('claims',[])),len(doc.get('entries',[]))+len(doc.get('claims',[])),note='invalid by ledger' if bad else 'valid run')
account(hfp,'flash_holdout_final_mapping',len(finalmap),sum(any(r['observation_id']==f'flash:holdout-F00-r2:{cid}' and r['mapped_claims'] for r in raw) for cid in finalmap),unresolved_count=sum(not any(r['observation_id']==f'flash:holdout-F00-r2:{cid}' and r['mapped_claims'] for r in raw) for cid in finalmap),records=[{'local_id':f'F00-r2:{cid}','disposition':'included' if any(r['observation_id']==f'flash:holdout-F00-r2:{cid}' and r['mapped_claims'] for r in raw) else 'unresolved','output_refs':[f'flash:holdout-F00-r2:{cid}'] if any(r['observation_id']==f'flash:holdout-F00-r2:{cid}' and r['mapped_claims'] for r in raw) else [],'reason':None if any(r['observation_id']==f'flash:holdout-F00-r2:{cid}' and r['mapped_claims'] for r in raw) else 'matching valid report claim not recovered'} for cid in sorted(finalmap)])

# Scope calibration is bounded, never full review.
sp=use(SCOPE/'AFFECTED.json');sd=load(sp)
for x in sd['records']:
 for e in x.get('inventory_audit_ids',[]):event(e,'bounded_calibration',sp,sp,True,'scope_rule_calibration','bounded terminology scope only','explicit inventory IDs')
account(sp,'scope_rule_calibration',len(sd['records']),len(sd['records']))

# Human-readable experiment reports are accounted claim by claim.  A hash alone
# is never treated as content consumption: every local heading either links to
# an emitted observation or remains an explicit unresolved source record.
already={x['path'] for x in accounting}
report_paths=set(EXP.glob('*/reports/*.md'))
raw_by_source=defaultdict(list)
for r in raw:raw_by_source[r['source']['path']].append(r)
for pattern in ('*/FINDINGS.md','*/ADJUDICATION.md','*/MERGED-FINDINGS.md','*/REPORT.md'):
 report_paths.update(EXP.glob(pattern))
for p in sorted(report_paths):
 if rel(p) in already:continue
 text=use(p).read_text(encoding='utf-8')
 marks=[]
 for m in re.finditer(r'(?m)^(?:#{2,6}\s+(?:\[[^]]+\]\s*)?|\*\*)((?:C|P)\d+(?:\.\d+)?)\b',text):
  lid=m.group(1);line=text.count('\n',0,m.start())+1
  refs=[r['observation_id'] for r in raw_by_source[rel(p)] if r['source'].get('local_id')==lid or re.search(rf'(?m)^(?:#{{2,6}}\s+|\*\*)[^\n]*\b{re.escape(lid)}\b',r['original_text'])]
  marks.append({'local_id':f'{lid}@L{line}','disposition':'included' if refs else 'unresolved','output_refs':sorted(set(refs)),'reason':None if refs else 'claim-bearing report block has no exact emitted observation link'})
 inc=sum(x['disposition']=='included' for x in marks);unr=len(marks)-inc
 account(p,'experiment_report_claim_accounting',len(marks),inc,unresolved_count=unr,records=marks,note='included count derived only from explicit output_refs')
source_unresolved=[{'path':x['path'],'adapter':x['adapter'],'local_id':r['local_id'],'entry_id':r.get('entry_id'),'line':r.get('line'),'reason':r.get('reason'),'output_refs':r.get('output_refs',[])} for x in accounting for r in x['records'] if r.get('disposition')=='unresolved']

# Derive coverage/backlog without entry-level status unions.
cbe=defaultdict(list);rbe=defaultdict(list);ube=defaultdict(list)
for c in claims.values():cbe[c['entry_id']].append(c['claim_id'])
for r in raw:
 for e in r['entry_ids']:rbe[e].append(r['observation_id'])
for u in unresolved:
 for e in u.get('entry_ids') or ([u['entry_id']] if u.get('entry_id') else []):ube[e].append(u['observation_id'])
for e,x in rows.items():
 full=x['coverage']['initial_full_entry_review'] or x['coverage']['experiment_full_entry_review']
 if not full:x['todo_status'].append('no_valid_full_entry_review')
 if ube[e]:x['todo_status'].append('unmapped_observation')
 if any(u.get('entry_id')==e for u in source_unresolved):x['todo_status'].append('source_local_parsing_pending')
 pending_raw=any(e in r['entry_ids'] and r['validity']=='valid' and (r['historical_status'] in ('pending','pending_candidate') or any(str(a.get('status','')).startswith(('pending','unresolved')) for a in r['adjudications'])) for r in raw)
 if any(claims[c]['effective_status']=='pending' for c in cbe[e]) or pending_raw:x['todo_status'].append('pending_fact_or_source')
 if any(claims[c]['calibration'] for c in cbe[e]):x['todo_status'].append('later_claim_calibration_present')
 if any(e in r['entry_ids'] and r['validity']=='valid' and r['historical_status'] not in ('ok','unknown') and not r['mapped_claims'] for r in raw):x['todo_status'].append('reported_observation_not_claim_mapped')
 if any(e in r['entry_ids'] and r['validity']=='valid' and r['record_kind'] in ('campaign_primary_claim','campaign_cross_claim') for r in raw) and not x['coverage']['cross_review']:x['todo_status'].append('reported_suspicion_not_cross_reviewed')
cov=[rows[e] for e in ids];fullids={e for e in ids if rows[e]['coverage']['initial_full_entry_review'] or rows[e]['coverage']['experiment_full_entry_review']}
cc=[]
for x in cov:cc.append({'entry_id':x['entry_id'],'component':x['component'],'logical_path':x['logical_path'],'line':x['line'],'section':x['section'],'original_batch':x['original_batch'] or '',**{k:str(v).lower() for k,v in x['coverage'].items()},'todo_status':';'.join(x['todo_status']),'valid_outputs':';'.join(sorted({e['output'] for e in x['events'] if e['valid']})),'invalid_outputs':';'.join(sorted({e['output'] for e in x['events'] if not e['valid']}))})
cats=defaultdict(list)
for e in ids:
 for k in rows[e]['todo_status']:cats[k].append(e)
back={'schema_version':2,'categories':[{'category':k,'count':len(v),'entry_ids':v} for k,v in sorted(cats.items())],'unresolved_unmapped_records':sorted(unresolved,key=lambda x:(str(x.get('entry_id')),x['observation_id'])),'unresolved_source_local_records':sorted(source_unresolved,key=lambda x:(x['path'],x['local_id'])),'formal_completion_rule':'Model reports and bounded calibration do not imply production completion.'}
bc=[{'category':k,'entry_id':e,'component':rows[e]['component'],'original_batch':rows[e]['original_batch'] or ''} for k,v in sorted(cats.items()) for e in v]
cr=sorted(claims.values(),key=lambda x:x['claim_id']);rr=sorted(raw,key=lambda x:(x['entry_id'],x['observation_id'],x['source']['path']));eff=Counter(x['effective_status'] for x in cr);hist=Counter(h['status'] for x in cr for h in x['status_history']);rstat=Counter(x['historical_status'] for x in rr if x['validity']=='valid')

# Baseline and concrete regressions.
bp=use(ROOT/'.ai/task/modified-review-reconcile-20260923/BASELINE.json');base=load(bp)['sha256'];missing=[];mismatch=[]
for n,want in base.items():
 p=ROOT/n
 if not p.is_file():missing.append(n)
 elif sha(p)!=want:mismatch.append({'path':n,'expected':want,'actual':sha(p)})
def ev(e,suf,layer=None):return any(x['valid'] and x['output'].endswith(suf) and (layer is None or x['layer']==layer) for x in rows[e]['events'])
checks={'inventory_count_4144':len(cov)==4144,'inventory_ids_unique':len({x['entry_id'] for x in cov})==4144,'unknown_ids_empty':not unknown,'full_review_union_3836':len(fullids)==3836,'no_full_review_308':len(idset-fullids)==308,'bounded_calibration_not_full_review':all('no_valid_full_entry_review' in rows[e]['todo_status'] for e in ['entry-03927','entry-03930','entry-03973']),'sol_007_exact_mapping':all(ev(e,'sol-007-01.md','cross_review') for e in ['entry-00244','entry-00247','entry-00254']),'sol_025_raw_pointer':all(ev(e,'sol-024-01.md','cross_review') for e in ['entry-00972','entry-00980']),'sol_prior_mapping':ev('entry-01917','sol-prior-01.md','cross_review'),'entry_00075_no_fake_union':not any(x['entry_id']=='entry-00075' and x['historical_status'] in ('confirmed','pending','refuted') and x['validity']=='valid' for x in rr),'ab_A2_C02_split':all(any(x['observation_id']==f'ab:A2:{a}' and x['mapped_claims']==[b] for x in rr) for a,b in [('C02.1','ab:H01'),('C02.2','ab:H02'),('C02.3','ab:N76')]),'abc_canonical_431':sum(x['claim_id'].startswith('abc:') and x['claim_id'].split(':')[-1].startswith('D') for x in cr)==431,'abc_g01_P01':'abc:g01:P01' in claims,'abc_g11_reference_accounted':any(x['path'].endswith('abc20-g11-20260923/REFERENCE.json') for x in accounting),'flash_holdout_actual_reference':all(x in claims for x in ['flash-holdout:Q01','flash-holdout:Q02','flash-holdout:Q06']),'flash_Q06_pending':claims['flash-holdout:Q06']['effective_status']=='pending','cal10_refutations':all(claims[x]['effective_status']=='refuted' for x in ['abc:g12:D03','abc:g14:D07','abc:g14:D11']),'user_boundaries_exact':all(claims[x]['effective_status']=='advisory' for x in usercal),'calibrated_D13_remains_confirmed':claims['abc:g11:D13']['effective_status']=='confirmed','source_accounting_balanced':all(x['expected_records']==x['included_records']+x['excluded_records']+x['unresolved_records'] for x in accounting),'valid_events_have_real_io':all(x['output_sha256'] and x['input_sha256'] for r in cov for x in r['events'] if x['valid']),'batch_input_hashes':not batch_mismatch,'prior_ten_identity':not pf,'baseline_11190_unchanged':len(base)==11190 and not missing and not mismatch}
checks.update({
 'abc_pending_105_exact_entry_and_P_links':len(abc_pending_expected)==105 and all(any(r['observation_id']==oid and r['entry_ids'] and any(a['status']=='pending' for a in r['adjudications']) and any(':P' in c for c in r['mapped_claims']) for r in rr) for oid in abc_pending_expected),
 'calibration11P_complete':all(f'cal10:P{i:02d}' in claims for i in range(1,12)),
 'calibration_user_boundary_P_exact':all(claims[f'cal10:{p}']['effective_status']=='advisory' for p in ('P01','P05','P09')) and all(claims[f'cal10:P{i:02d}']['effective_status']=='pending' for i in (2,3,4,6,7,8,10,11)),
 'sol092_two_claims':sum(r['source']['path'].endswith('/sol-092-01.md') and r['validity']=='valid' for r in rr)==2,
 'gemini094_advisories_and_pending':all(any(e in r['entry_ids'] and r['source']['path'].endswith('/gemini-094-01.md') for r in rr) for e in ('entry-03137','entry-03139')),
 'ab_A2_C05_entry_and_text':any(r['observation_id']=='ab:A2:C05' and 'entry-03841' in r['entry_ids'] and r['source']['path'].endswith('/reports/A2.md') for r in rr),
 'pilot_multi_entry_and_status_layers':any(r['observation_id']=='pilot:opus:C03' and r['entry_ids']==['entry-03844','entry-03846'] and r['historical_status']=='pending' and any(a['status']=='advisory' for a in r['adjudications']) for r in rr),
 'flash_dev_normalized_mapped':any(r['observation_id']=='flash:dev-F01-r1:C05' and set(r['mapped_claims'])>={'ab:H01','ab:H02','ab:N76'} and len(r['atom_mappings'])>=2 for r in rr),
 'flash_holdout_final_exact':all(any(r['observation_id']==f'flash:holdout-F00-r2:{c}' and r['mapped_claims'] and any(a['authority']=='Flash holdout final host adjudication' for a in r['adjudications']) for r in rr) for c in ('C01','C02','C03','C04')),
 'entry_00094_pending_backlog':'pending_fact_or_source' in rows['entry-00094']['todo_status'],
 'source_claim_records_derived':all(not x['records'] or (x['included_records']==sum(r['disposition']=='included' for r in x['records']) and x['unresolved_records']==sum(r['disposition']=='unresolved' for r in x['records']) and x['excluded_records']==sum(r['disposition'].startswith('excluded') for r in x['records'])) for x in accounting),
 'r03_primary_heading_and_advisory_fields':all(any(r['source']['path'].endswith('/gemini-014-01.md') and e in r['entry_ids'] and r['historical_status']==st for r in rr) for e,st in [('entry-00522','advisory'),('entry-00527','advisory'),('entry-00553','pending_candidate'),('entry-00560','advisory')]) and any(r['source']['path'].endswith('/gemini-024-01.md') and r['entry_ids']==['entry-00948'] and r['historical_status']=='advisory' for r in rr),
 'r03_abc_original_status_separate':any(r['observation_id']=='abc:g01:O001' and r['historical_status']=='advisory' and any(a['status']=='mixed' for a in r['adjudications']) for r in rr) and any(r['observation_id']=='abc:g04:O018' and r['historical_status']=='pending' and any(a['status']=='refuted' for a in r['adjudications']) for r in rr),
 'r03_ab_C56_multi_entry_direct':any(r['observation_id']=='ab:A2:C56' and r['entry_ids']==['entry-03867','entry-03868'] and r['mapped_claims'] for r in rr) and 'ab:A2:C56' in rbe['entry-03868'],
 'r03_cross_report_source_local_accounting':len([x for x in accounting if x['adapter']=='campaign_cross_report_local'])==len(selected_cross) and all(x['records'] and all((r['disposition']=='included' and r['output_refs']) or (r['disposition']=='unresolved' and r.get('raw_text') and r.get('line')) for r in x['records']) for x in accounting if x['adapter']=='campaign_cross_report_local') and any(r['source']['path'].endswith('/sol-014-01.md') and r['source'].get('line')==80 and r['historical_status']=='pending' for r in rr),
 'r03_primary_same_format_accounted':all(x['expected_records']==len(x['records']) and x['included_records']+x['unresolved_records']==len(x['records']) for x in accounting if x['adapter']=='campaign_primary_markdown_claims'),
 'r03_abc_original_status_same_format':all(any(r['observation_id']==oid and (r['historical_status'],r['literal_status'])==expected for r in rr) for oid,expected in abc_original_expected.items()),
 'r03_ab_explicit_multi_entry_same_format':all(any(r['observation_id']==oid and r['entry_ids']==expected for r in rr) for oid,expected in ab_explicit_multi.items()),
 'r04_unrecognized_primary_preserved':all(any(r['source']['path'].endswith('/'+name) and e in r['entry_ids'] and marker in r['original_text'] and r['record_kind']=='unparsed_source_entry' and r['historical_status']=='unknown' for r in rr) for name,e,marker in [('gemini-030-01.md','entry-01183','细微观察'),('gemini-032-01.md','entry-01215','存在疑点')]),
 'r04_sol012_pending_block_preserved':any(r['source']['path'].endswith('/sol-012-01.md') and '**pending**' in r['original_text'] and r['record_kind']=='unparsed_source_entry' for r in rr),
 'r04_fallback_raw_exact_and_backlogged':all(r['original_text']== '\n'.join((ROOT/r['source']['path']).read_text(encoding='utf-8').splitlines()[r['source']['line']-1:r['source']['line']-1+len(r['original_text'].splitlines())]).strip() and all('source_local_parsing_pending' in rows[e]['todo_status'] for e in r['entry_ids']) for r in rr if r['record_kind']=='unparsed_source_entry' and r['validity']=='valid'),
})
counts={'entries':4144,'full_entry_review_union':len(fullids),'no_full_entry_review':len(idset-fullids),'coverage_layers':{k:sum(x['coverage'][k] for x in cov) for k in rows[ids[0]]['coverage']},'canonical_claims':len(cr),'effective_claim_statuses':dict(sorted(eff.items())),'historical_claim_statuses':dict(sorted(hist.items())),'raw_observations':len(rr),'valid_raw_statuses':dict(sorted(rstat.items())),'unresolved_unmapped_records':len(unresolved),'unresolved_source_local_records':len(source_unresolved),'source_accounting_rows':len(accounting),'backlog':{k:len(v) for k,v in sorted(cats.items())}}
val={'schema_version':2,'checks':checks,'counts':counts,'unknown_ids':sorted(unknown),'batch_input_mismatches':batch_mismatch,'prior_identity_failures':pf,'baseline':{'checked_files':len(base),'missing':missing,'mismatches':mismatch},'replay':{'mode':'python3 generate.py --check','determinism':'sorted JSON/stable traversal/LF'},'anomalies':[{'code':'OLD_STATE_STALE','detail':'gemini-094-01 and sol-092-01 recovered from explicit dispatch/output files.'},{'code':'SOL_091_WRONG_INPUT','detail':'sol-091-01 invalid; sol-091-02 effective.'},{'code':'ABC_GROUP1_PROTOCOL','detail':'Read-only coverage retained with qualification.'},{'code':'ABC_15_20_NOT_RUN','detail':'Frozen groups do not count.'},{'code':'REFERENCE_NOT_HUMAN_GOLD','detail':'Experimental references retain qualification.'}]}
if not all(checks.values()):raise SystemExit(f"validation failed: {', '.join(k for k,v in checks.items() if not v)}; full={len(fullids)} nofull={len(idset-fullids)} D13={claims['abc:g11:D13']['effective_status']}")
for n in ('PROGRESS.md','HUMAN-REVIEW.md','CHECKS.md','INVENTORY-CORRECTIONS.md','PLAN.md'):
 if (CAM/n).is_file():use(CAM/n)
for p in (SCOPE/'REPORT.md',SCOPE/'VERIFICATION.json'):
 if p.is_file():use(p)
manifest={'schema_version':2,'root':'.','inputs':[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(used,key=rel)],'policy':'All evidence/history actually read is hashed; generated files excluded.'}
findings={'schema_version':2,'canonical_claims':cr,'raw_observations':rr,'unresolved_unmapped_records':sorted(unresolved,key=lambda x:(str(x.get('entry_id')),x['observation_id'])),'entries':[{'entry_id':e,'canonical_claim_ids':sorted(cbe[e]),'raw_observation_ids':sorted(rbe[e]),'unresolved_observation_ids':sorted(ube[e])} for e in ids if cbe[e] or rbe[e] or ube[e]]}
fl=['# 问题、待确认与未归并入口','','由 `generate.py` 归并既有记录，不新增语义裁决。claim、raw observation、历史/有效状态和来源见 `FINDINGS.json`。','',f"- canonical claims：{len(cr)}；有效状态："+'，'.join(f'{k}={v}' for k,v in sorted(eff.items()))+'。',f'- raw observations：{len(rr)}；无显式 claim 映射：{len(unresolved)}。','','后续处理必须按 `claim_id`；同 entry 的不同 claim 不作状态并集。','']
def cell(v,limit=180):
 s=v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,sort_keys=True)
 s=' '.join(s.split())
 return (s[:limit]+'…' if len(s)>limit else s).replace('|','\\|').replace('<','&lt;').replace('>','&gt;')
def sourcelink(s):
 p=ROOT/s['path']; suffix=f":{s['line']}" if s.get('line') else ''
 return f"[{p.name} · {cell(s.get('local_id',''),60)}]({p}{suffix})"
fl+=['## 已有明确归并的 claim','','`confirmed_provisional` 保留实验暂定资格；`confirmed` 也不代表本次已重新核验。摘要为既有记录节选，完整内容及历史状态见 [FINDINGS.json](FINDINGS.json)。','', '| Claim | Entry | 当前记录状态 | 原记录节选 | 有效状态来源 |','|---|---|---|---|---|']
for c in cr:fl.append(f"| {c['claim_id']} | {c['entry_id']} | {c['effective_status']} | {cell(c['claim_text'])} | {sourcelink(c['effective_source'])} |")
fl+=['','## 未映射观察与来源待解析索引','','以下是记录整理待办，**不等同于确认错译**。同一原文可能同时存在于已解析观察和保底原文块中，不能将数量相加作为缺陷数。按 entry 查询完整记录请使用 [FINDINGS.json](FINDINGS.json)；具体缺口见 [BACKLOG.json](BACKLOG.json)。','','| Entry | 未映射观察数 | 来源待解析块数 | 原始来源示例 |','|---|---:|---:|---|']
for e in ids:
 us=[u for u in source_unresolved if u.get('entry_id')==e]
 if not ube[e] and not us:continue
 samples=[r['source'] for r in rr if e in r['entry_ids'] and r['observation_id'] in ube[e]]
 fl.append(f"| {e} | {len(ube[e])} | {len(us)} | "+'；'.join(sourcelink(s) for s in samples[:2])+' |')
readme=f'''# 已修改译文审核统一台账（2026-09-23）

本台账以 4144 个 inventory entry-ID 为母表，只归并已有覆盖、claim、观察和待确认，不新增语义裁决，不表示生产 `DONE_VERIFIED`。

## 统计

- 完整逐条审核并集：{len(fullids)}/4144；尚无完整逐条审核：{len(idset-fullids)}。局部术语/实验校准单列，不冒充完整审核。
- canonical claims：{len(cr)}；有效状态：{', '.join(f'{k}={v}' for k,v in sorted(eff.items()))}。
- raw observations：{len(rr)}；未显式映射：{len(unresolved)}。不以关键词或同 entry 状态并集强行归并。
- ABC groups 1–14：560 条逐条覆盖、431 个累计 canonical defects；groups 15–20 未运行。
- ABC G04–G14 的 {len(abc_pending_expected)} 个 pending O 均按 ANON 映射恢复 entry/作者原文并连到显式 P；calibration P01–P11 全部单列，用户口径仅作用于 P01/P05/P09 及已明确映射的旧 D。
- 来源 local-ID 未闭合：{len(source_unresolved)} 条，均在 `SOURCE-ACCOUNTING.json` 与 `BACKLOG.json` 保留具体路径、local-ID 和原因；另有 {sum(1 for u in unresolved if not u.get('entry_id'))} 条结构化观察缺明确 entry 关联，未作语义猜配。
- 92 份有效 cross 报告均建立了 source-local accounting；其中 {sum(r['disposition']=='unresolved' for x in accounting if x['adapter']=='campaign_cross_report_local' for r in x['records'])} 个来源块以原文保留为 `unresolved`，不用 coverage 或 STATE summary 代填。覆盖引用、已解析 claim 与待解析块分别计数。
- 未识别格式采用原文保底，状态为 `unknown`，并单列 `source_local_parsing_pending`。这会增加待整理记录数，不代表新发现同等数量的译文问题，也不影响已完成逐条审核的覆盖数。

## 文件与恢复

`COVERAGE.json/.csv` 保存真实 input/output 和分层覆盖；`FINDINGS.json` 分开 canonical claims、raw observations 与 unmapped records；`SOURCE-ACCOUNTING.json` 的 included 只由具体 output refs 计算，哈希本身不算消费内容；`BACKLOG.json/.csv` 分列未覆盖、pending、未交叉疑点、未映射及 source-local 缺口；`SOURCE-MANIFEST.json` 保存所有输入哈希；`VALIDATION.json` 保存反例和 11190 文件基线检查。

运行 `python3 evidence/translation-audit/all-modified-review-20260922/reconciled-20260923/generate.py` 重放；追加 `--check` 做无写比较。

旧 `STATE.json`、`PROGRESS.md`、`HUMAN-REVIEW.md`、报告和实验均为历史快照。交叉报告按 `raw_output_path`/result dispatch/frozen input 连接，不猜编号；`sol-091-01` 无效，`sol-091-02` 生效。Flash 开发参考沿 AB claim，留出读取实际 `HOST-HOLDOUT-INITIAL.json`，run 按围栏 JSON 与 RUN-LEDGER。用户三边界只校准 `abc:g12:D08`、`abc:g11:D14`、`abc:g11:D08`，不改历史状态或同 entry 其他 claim。
'''
outputs={'SOURCE-MANIFEST.json':jb(manifest),'SOURCE-ACCOUNTING.json':jb({'schema_version':1,'sources':sorted(accounting,key=lambda x:(x['path'],x['adapter']))}),'COVERAGE.json':jb({'schema_version':2,'inventory_sha256':sha(invp),'entries':cov}),'COVERAGE.csv':cb(cc,list(cc[0])),'FINDINGS.json':jb(findings),'FINDINGS.md':('\n'.join(fl)+'\n').encode(),'BACKLOG.json':jb(back),'BACKLOG.csv':cb(bc,['category','entry_id','component','original_batch']),'VALIDATION.json':jb(val),'README.md':readme.encode()}
if '--check' in sys.argv:
 bad=[n for n,b in outputs.items() if not (OUT/n).is_file() or (OUT/n).read_bytes()!=b]
 if bad:raise SystemExit('replay mismatch: '+', '.join(bad))
 print(json.dumps({'replay':'stable',**counts},ensure_ascii=False,sort_keys=True))
else:
 for n,b in outputs.items():(OUT/n).write_bytes(b)
 print(json.dumps(counts,ensure_ascii=False,sort_keys=True))
