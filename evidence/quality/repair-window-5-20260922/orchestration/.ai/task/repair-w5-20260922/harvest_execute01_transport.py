import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools/orchestration')
from review_lifecycle import read_native_final
P=Path(__file__).parent;did='execute-01';s=json.loads((P/'STATE.json').read_text());v=json.loads((P/f'{did}-terminal.json').read_text())['snapshot'];d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
assert v['id']==d['agent_id'] and v['activeTurn'] is None and v['status']=='idle' and v['attentionReason']=='finished'
assert v['workspaceId']==s['workspace_id'] and v['labels']==d['labels'] and v['provider']=='codex'
submitted=json.loads((P/f'{did}-create.json').read_text())['parameters']['initialPrompt'];assert submitted==(P/f'{did}-prompt.txt').read_text()
session=v['persistence']['sessionId'];paths=list(Path('/home/paseo/.codex/sessions/2026/09/22').glob('*'+session+'.jsonl'));assert len(paths)==1
matches=[]
for line in paths[0].read_text().splitlines():
 j=json.loads(line);x=j.get('payload',{})
 if j.get('type')=='response_item' and x.get('role')=='user':
  t=''.join(y.get('text','') for y in x.get('content',[]) if y.get('type')=='input_text')
  if t.startswith('你是唯一EXECUTOR，实际实施修复窗口5'):matches.append(t)
assert len(matches)==1;effective=matches[0];assert submitted==effective+'\n'
receipt=dict(kind='executor_creation_terminal_lf_transport_difference',submitted_prompt_path=str(P/f'{did}-prompt.txt'),submitted_sha256=hashlib.sha256(submitted.encode()).hexdigest(),native_sha256=hashlib.sha256(effective.encode()).hexdigest(),difference='Native initial user message equals submitted creation prompt with exactly one terminal LF removed; all other bytes identical.',initial_strict_harvest_error='frozen creation prompt mismatch',original_records_preserved=True,scope='EXECUTOR instruction transport only; no reviewer result or frozen review envelope normalization')
(P/f'{did}-transport-difference.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(P/f'{did}-native-prompt.txt').write_text(effective)
raw,proof=read_native_final(paths[0],provider='codex',session_id=session,cwd=str(Path.cwd()),prompt=effective,natural_success=True)
dest=P/f'{did}-report.raw';assert not dest.exists();dest.write_bytes(raw);proof['submitted_prompt_transport_receipt']=str(P/f'{did}-transport-difference.json');(P/f'{did}-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
d.update(output_valid=True,raw_output_path=str(dest),raw_output_sha256=hashlib.sha256(raw).hexdigest(),executor_prompt_transport_receipt=str(P/f'{did}-transport-difference.json'))
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(raw.decode())
