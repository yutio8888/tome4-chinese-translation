import pathlib,json,hashlib,sys,collections
sys.path.insert(0,'tools');from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
from i18nlib.lint import extract_format_tokens,MARKUP_RE
D=pathlib.Path('.ai/task/awkward-explanations-adjust-20261003');A=pathlib.Path('.artifacts/i18n/awkward-explanations-adjust-20261003');xs=json.load(open(D/'CHANGES.json'));L=LocaleLoader(LuaRuntime(load_manifest()));proof=[];records=[]
for f in json.load(open(D/'SCOPE.json'))['allowed_files']:
 b=(D/'baseline'/f).read_bytes();n=pathlib.Path(f).read_bytes();expected=b;B=L.load_bytes(b,logical_path=f).records;N=L.load_bytes(n,logical_path=f).records;allowed={x['record_index']:x for x in xs if x['file']==f};assert len(B)==len(N)
 for idx,(o,z) in enumerate(zip(B,N)):
  assert {k:v for k,v in o.items() if k not in ['line','target']}=={k:v for k,v in z.items() if k not in ['line','target']}
  if idx not in allowed:assert o.get('target')==z.get('target');continue
  x=allowed[idx];assert o['target']==x['old_target'] and z['target']==x['new_target'],x['id'];assert expected.count(x['old_target'].encode())==1;expected=expected.replace(x['old_target'].encode(),x['new_target'].encode(),1)
  assert [t.raw for t in extract_format_tokens(o['target'])]==[t.raw for t in extract_format_tokens(z['target'])];assert MARKUP_RE.findall(o['target'])==MARKUP_RE.findall(z['target']);assert o['target'].count('\n')==z['target'].count('\n');records.append(dict(**x,final_target=z['target'],line=z['line'],args_order=z.get('args_order'),special=z.get('special')))
 assert expected==n,(f,'outside exact changes drift');proof.append(dict(file=f,baseline_sha256=hashlib.sha256(b).hexdigest(),final_sha256=hashlib.sha256(n).hexdigest(),record_count=len(N),changed_targets=len(allowed),all_non_target_fields_equal=True,exact_raw_replacement_only=True))
j={'status':'passed','changed_targets':len(records),'files':proof,'records':records};(A/'host-proof.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');print('verified',len(records),'exact target changes; raw bytes, LuaJIT fields and formats pass')
