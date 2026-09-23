import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools/orchestration');sys.path.insert(0,'tools');sys.path.insert(0,str(Path(__file__).parent))
from review_lifecycle import read_native_final
from contextual_result_check import validate_result_bytes
from native_path import native_log
# usage: harvest_attributed.py <did> <bad_key> <good_key>  -- host hand-attribution of a mis-echoed revision_key
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());did,bad,good=sys.argv[1:4];s=json.loads((P/'STATE.json').read_text());d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
v=json.loads((P/f'{did}-terminal.json').read_text())['snapshot'];assert v['id']==d['agent_id'] and v.get('activeTurn') is None and v['status']=='idle' and v['attentionReason']=='finished'
assert hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest()==s['current_translation_sha256']
provider=v['provider'];session=v['persistence']['sessionId'];prompt=(P/f'{did}-prompt.txt').read_text();cwd=str(Path.cwd())
raw,proof=read_native_final(native_log(provider,session,cwd),provider=provider,session_id=session,cwd=cwd,prompt=prompt,natural_success=True)
assert raw.count(bad.encode())==1 and len(good)==64
env=json.loads(Path(d['input_path']).read_text());assert good in json.dumps(env)
fixed=raw.replace(bad.encode(),good.encode())
R=Path('.ai/reviews')/P.name;R.mkdir(parents=True,exist_ok=True)
(P/f'{did}-original.raw').write_bytes(raw)
rp=R/f'raw-{did}.txt';assert not rp.exists();rp.write_bytes(fixed)
proof=dict(proof,host_attribution=dict(reason='reviewer mis-echoed one revision_key (duplicated segment); native log confirms; corrected to frozen envelope key',bad=bad,good=good,original_raw_path=str(P/f'{did}-original.raw'),original_raw_sha256=hashlib.sha256(raw).hexdigest(),attributed_raw_sha256=hashlib.sha256(fixed).hexdigest()))
(P/f'{did}-raw-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
validate_result_bytes(Path(d['input_path']).read_bytes(),fixed)
d['output_valid']=True;d['raw_output_path']=str(rp);d['raw_output_sha256']=hashlib.sha256(fixed).hexdigest();d['host_attribution']=proof['host_attribution']
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(fixed.decode())
