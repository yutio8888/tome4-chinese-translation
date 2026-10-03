import pathlib,json,sys,hashlib,subprocess
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
from i18nlib.lint import stable_entry_id
from i18nlib.workset import create_workset,proposal_template_for
D=pathlib.Path('.ai/task/awkward-explanations-adjust-20261003');A=pathlib.Path('.artifacts/i18n/awkward-explanations-adjust-20261003');m=load_manifest();L=LocaleLoader(LuaRuntime(m));xs=json.load(open(D/'CHANGES.json'));comps={c.translation:c.id for c in m.components};results=[]
for f in sorted({x['file'] for x in xs}):
 c=comps[f];rs=L.load_bytes((D/'baseline'/f).read_bytes(),logical_path=f).records;items=[];targets={}
 for x in xs:
  if x['file']!=f:continue
  o=rs[x['record_index']];eid=stable_entry_id(c,o['section'],o['source'],o['source_tag']);items.append({'entry_id':eid,'component':c,'section':o['section'],'source':o['source'],'source_tag':o['source_tag'],'previous_target':o['target'],'previous_args_order':o.get('args_order'),'previous_special':o.get('special'),'classification':'manual-bounded-restoration'});targets[eid]=x['new_target']
 p=A/f'{c}-manual-workset-input.json';p.write_text(json.dumps({'schema_version':1,'merge_id':'manual-restoration-'+hashlib.sha256(json.dumps(items,ensure_ascii=False).encode()).hexdigest(),'component':c,'origin':'Manual bounded restoration input adapter for proposal validation, not an extractor/merge run or source-correctness claim.','untranslated':items},ensure_ascii=False,indent=2)+'\n');w=create_workset(m,merge_report_path=p,limit=16,section_prefix=None,classification='all');proposal=proposal_template_for(w)
 for it in proposal['proposals']:it['target']=targets[it['entry_id']];it['notes']='User-authorized removal of unadopted mechanism expansions / concise wording.'
 pp=A/f'{c}-proposal.json';pp.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n');cmd=['python3','-B','tools/i18n','proposal','--workset',w['output'],'--proposal',str(pp),'--strict','--json'];r=subprocess.run(cmd,capture_output=True,text=True);results.append({'component':c,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});print(c,r.returncode,flush=True)
(A/'proposal-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');assert all(r['exit_code']==0 for r in results)
