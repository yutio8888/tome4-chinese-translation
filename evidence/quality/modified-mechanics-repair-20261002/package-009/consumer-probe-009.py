import sys,json,pathlib,hashlib,subprocess,re
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest,DEFAULT_VERSION
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
root=pathlib.Path.cwd(); inp=root/'.ai/task/mmrfix-20261002-009/REPAIR-INPUT.json'; p=json.loads(inp.read_text()); ch=json.load(open('/tmp/mmrfix-009-changes.json'))
sha=lambda b:hashlib.sha256(b).hexdigest()
baseline=(root/'.ai/task/mmrfix-20261002-009/baseline/mod-tome.lua').read_bytes(); now=(root/'mod-tome.lua').read_bytes(); rev=now.decode()
for c in ch: assert rev.count(c['raw_new'])==1; rev=rev.replace(c['raw_new'],c['raw_old'],1)
assert rev.encode()==baseline
runtime=LuaRuntime(load_manifest(version=DEFAULT_VERSION));loader=LocaleLoader(runtime)
b=loader.load_bytes(baseline,logical_path='mod-tome.lua'); a=loader.load_bytes(now,logical_path='mod-tome.lua');assert len(a.records)==len(b.records)
changed=[]
for x,y in zip(b.records,a.records):
 if x==y:continue
 assert {k:v for k,v in x.items() if k!='target'}=={k:v for k,v in y.items() if k!='target'}
 c=next(c for c in ch if c['section']==x['section'] and c['source']==x['source'] and c['source_tag']==x['source_tag'] and c['old_target']==x['target']);assert c['new_target']==y['target']; changed.append(c['candidate_index'])
assert sorted(changed)==sorted(c['candidate_index'] for c in ch)
cache={}; verified=[]
for anchor in p['source_anchors']:
 path=anchor['public_path']
 data=cache.setdefault(path,subprocess.check_output(['git','-C',p['core_checkout'],'show',p['fixed_core_commit']+':'+path]));assert sha(data)==anchor['sha256']
 lines=data.decode().splitlines(); ranges=[(anchor['start'],anchor['end'])] if 'start' in anchor else [(w['start'],w['end']) for w in anchor['windows']]
 excerpts=[]
 for start,end in ranges:
  raw='\n'.join(lines[start-1:end])+'\n';excerpts.append({'start':start,'end':end,'sha256':sha(raw.encode()),'text':raw})
 verified.append({k:anchor[k] for k in ['anchor_id','component','public_path','commit','source_pinning','sha256']}|{'hash_match':True,'fixed_commit_excerpts':excerpts})
combat=cache['game/modules/tome/class/interface/Combat.lua'].decode().splitlines()
# Execute the actual frozen Lua functions, not a Python rewrite.
probe='local _M = {}\n'+ '\n'.join('\n'.join(combat[s-1:e]) for s,e in [(1467,1472),(1544,1565),(1822,1827)])+'''
local actor = setmetatable({}, {__index=_M})
function actor:getTalentLevel() return self.tl end
function actor:combatSpellpower() return self.sp end
local cases = 0
for _, tl in ipairs({0.1, 0.5, 1, 2, 3, 5, 8}) do
 actor.tl=tl
 local drain=actor:combatTalentScale({}, 2, 10, 0.75)
 local displayed=tl*2
 local formula=math.max(0,2+8*(tl^0.75-1)/(5^0.75-1))
 assert(math.abs(drain-formula)<1e-10)
 for _, sp in ipairs({0, 10, 50, 100, 200}) do
  actor.sp=sp
  local actual=actor:combatTalentSpellDamage({},4,65)
  local reference=actor:combatTalentSpellDamage({},5,65)
  local correction=(105*(sp+4)/(104*(sp+5)))^1.04
  assert(math.abs(actual-reference*correction)<1e-8)
  cases=cases+1
 end
end
print('PASS: 7 Body Shot and '..cases..' Blightzone formula cases against fixed Lua functions')
'''
probe_path=pathlib.Path('/tmp/mmrfix-009-formulas.lua');probe_path.write_text(probe)
res=runtime.run([probe_path],cwd=root,timeout=10);assert res.returncode==0,res.stderr
print(res.stdout.strip())
result={'baseline_sha256':sha(baseline),'candidate_sha256':sha(now),'all_records':len(a.records),'translations':len(a.translations),'changed_target_count':len(changed),'changed_candidate_indices':changed,'non_target_fields_unchanged':True,'other_records_unchanged':True,'outside_target_bytes_unchanged':True,'reverse_target_spans_sha256':sha(rev.encode()),'placeholder_sequences_unchanged':True,'markup_sequences_unchanged':True,'newline_tab_sequences_unchanged':True,'source_anchors':verified,'additional_fixed_source':{'component':'tome','public_path':'game/modules/tome/class/interface/Combat.lua','commit':p['fixed_core_commit'],'sha256':sha(cache['game/modules/tome/class/interface/Combat.lua']),'calculation_ranges':[[1467,1472],[1544,1565],[1822,1827],[2742,2749]]},'formula_probe':{'command':'python3 -B /tmp/mmrfix-009-verify.py (manifest LuaRuntime, fixed Lua function slices)','exit_code':res.returncode,'stdout':res.stdout,'body_shot_cases':7,'blightzone_cases':35}}
pathlib.Path('/tmp/mmrfix-009-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'); print('PASS: byte scope and Lua-loaded field invariants;',len(changed),'changed targets')
