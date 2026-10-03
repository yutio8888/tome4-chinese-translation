import json,pathlib,sys,hashlib,re
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
D=pathlib.Path('.ai/task/mechanics-rollback-20261003');A=pathlib.Path('.artifacts/i18n/mechanics-rollback-20261003')
inv=json.loads((D/'INVENTORY.json').read_text());rows=inv['all_changed_records'];lookup={(r['file'],r['record_index']):r for r in rows}
L=LocaleLoader(LuaRuntime(load_manifest()));proof=[];changes=[];finals=[]
def mask_targets(data):
 text=data.decode('utf-8'); spans=[]
 import contextual_anchor_preflight as lex
 for match in re.finditer(r'^t\(',text,re.M):
  i=match.end();depth=0;commas=[]
  while i<len(text):
   c=text[i]
   if c in ['"', "'"]:
    _,i=lex._decode_lua_string(text,i);continue
   lb=lex._skip_long_bracket(text,i) if c=='[' else None
   if lb is not None:i=lb;continue
   if text.startswith('--',i):
    i=lex._skip_space_and_comments(text,i);continue
   if c in '({[':depth+=1
   elif c in ')}]':
    if depth==0:
     assert c==')';end=i;break
    depth-=1
   elif c==',' and depth==0:commas.append(i)
   i+=1
  assert commas
  spans.append((commas[0]+1,commas[1] if len(commas)>1 else end))
 parts=[];last=0;targets=[]
 for a,b in spans:
  parts.extend([text[last:a],'__TARGET_EXPRESSION__']);targets.append(text[a:b]);last=b
 parts.append(text[last:])
 return ''.join(parts).encode('utf-8'),targets
for f in json.loads((D/'SCOPE.json').read_text())['allowed_files']:
 b=(D/'baseline'/f).read_bytes();n=pathlib.Path(f).read_bytes();B=L.load_bytes(b,logical_path=f);N=L.load_bytes(n,logical_path=f)
 assert len(B.records)==len(N.records),f
 count=0
 for idx,(old,new) in enumerate(zip(B.records,N.records)):
  key=(f,idx)
  if key in lookup:
   r=lookup[key];finals.append(dict(id=r['id'],file=f,record_index=idx,source=new['source'],baseline_target=r['baseline']['target'],pre_rollback_target=old['target'],final_target=new['target']))
  if {k:v for k,v in old.items() if k!='line'}=={k:v for k,v in new.items() if k!='line'}:continue
  assert key in lookup,('outside inventory',f,idx)
  assert {k:v for k,v in old.items() if k not in ['target','line']}=={k:v for k,v in new.items() if k not in ['target','line']},('nontarget',f,idx)
  assert old['kind']=='translation'
  count+=1
  changes.append(dict(id=lookup[key]['id'],file=f,line=old['line'],record_index=idx,old_target=old['target'],new_target=new['target']))
 bm,bt=mask_targets(b);nm,nt=mask_targets(n)
 assert len(bt)==len(nt),(f,len(bt),len(nt))
 import contextual_anchor_preflight as lex
 def decode_expr(expr):
  i=0;parts=[]
  while i<len(expr):
   i=lex._skip_space_and_comments(expr,i)
   if i==len(expr):break
   if expr.startswith('..',i):i+=2;continue
   if expr[i] in ['"',"'"]:part,i=lex._decode_lua_string(expr,i)
   else:part,i=lex._decode_lua_long_bracket(expr,i)
   parts.append(part)
  return ''.join(parts)
 from collections import Counter
 raw_changes=Counter((decode_expr(x),decode_expr(y)) for x,y in zip(bt,nt) if x!=y)
 semantic_changes=Counter((r['old_target'],r['new_target']) for r in changes if r['file']==f)
 assert raw_changes==semantic_changes,('raw vs executed target mismatch',f,raw_changes-semantic_changes,semantic_changes-raw_changes)
 assert bm==nm,('outside target byte drift',f)
 proof.append(dict(file=f,baseline_sha256=hashlib.sha256(b).hexdigest(),final_sha256=hashlib.sha256(n).hexdigest(),record_count=len(N.records),changed_targets=count,all_non_target_fields_equal=True,masked_outside_target_bytes_equal=True,masked_sha256=hashlib.sha256(bm).hexdigest()))
assert len(finals)==165
j=dict(status='passed',inventory_count=len(finals),changed_targets=len(changes),files=proof,changes=changes,all_final_records=sorted(finals,key=lambda x:x['id']),scope='Restoration verification only; not a new game-mechanism correctness endorsement.')
(A/'host-scope-proof.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in j.items() if k not in ['changes','all_final_records']},ensure_ascii=False))
