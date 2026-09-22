import json,sys,hashlib,os
from pathlib import Path
sys.path.insert(0,'tools/orchestration')
from review_lifecycle import read_native_final
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
did=sys.argv[1]
s=json.loads((P/'STATE.json').read_text())
d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
v=json.loads((P/f'{did}-terminal.json').read_text())['snapshot']
assert v['id']==d['agent_id'] and v['activeTurn'] is None and v['status']=='idle' and v['attentionReason']=='finished'
assert v['workspaceId']==s['workspace_id'] and v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id']
assert d['role']=='SENIOR_REVIEWER' and d['purpose']=='scope_audit' and v['provider']=='codex'
a=json.loads((P/'SCOPE-AUDIT-R2.json').read_text())
loc=a['candidate_locator']
assert hashlib.sha256(Path(loc['spec_path']).read_bytes()+b'\0'+Path(loc['diff_path']).read_bytes()).hexdigest()==a['candidate_ref']==d['candidate_ref']
assert hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest()==s['current_translation_sha256']
session=v['persistence']['sessionId']
paths=list((Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions/2026/09/22').glob('*'+session+'.jsonl'))
assert len(paths)==1
prompt=(P/f'{did}-prompt.txt').read_text()
assert prompt==json.loads((P/f'{did}-create.json').read_text())['parameters']['initialPrompt']
raw,proof=read_native_final(paths[0],provider='codex',session_id=session,cwd=str(Path.cwd()),prompt=prompt,natural_success=True)
rp=Path('.ai/reviews')/P.name/f'raw-{did}.txt'
assert not rp.exists()
rp.write_bytes(raw)
(P/f'{did}-raw-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
def unique(pairs):
    result={}
    for k,v in pairs:
        assert k not in result,'duplicate key'
        result[k]=v
    return result
rows=json.loads(raw,object_pairs_hook=unique)
expected=[f'.ai/reviews/{P.name}/host-findings-r2.json / '+x['id'] for x in a['findings']]
assert isinstance(rows,list) and len(rows)==len(expected)
assert [x['finding_ref'] for x in rows]==expected
keys={'finding_ref','assessment','design_ac_basis','observable_impact','personal_project_proportionality','minimum_sufficient_action','rationale'}
for row in rows:
    assert set(row)==keys and all(isinstance(v,str) and v for v in row.values())
    assert row['assessment'] in {'keep','narrow','downgrade','reject','defer_to_user'}
d.update(output_valid=True,raw_output_path=str(rp),raw_output_sha256=hashlib.sha256(raw).hexdigest())
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(raw.decode())
