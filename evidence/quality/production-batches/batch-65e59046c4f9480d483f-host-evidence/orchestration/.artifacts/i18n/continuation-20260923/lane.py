import json,sys,glob,pathlib
# usage: lane257.py precheck <i>  -> compares native-log final JSON identities to envelope
i=int(sys.argv[2]);C=pathlib.Path('.artifacts/i18n/continuation-20260923')
e=json.load(open(C/'review-surface-emit.json'))[i]
cap=json.load(open(C/f'review-{e["dispatch_id"]}-terminal.json'))['snapshot'];sid=cap['persistence']['sessionId']
L=(glob.glob(f'/home/paseo/.codex/sessions/*/*/*/*{sid}.jsonl')+glob.glob(f'/home/paseo/.codex/archived_sessions/*{sid}.jsonl'))[0]
last=None
for line in open(L):
    o=json.loads(line);p=o.get('payload',{})
    if o.get('type')=='response_item' and p.get('type')=='message' and p.get('role')=='assistant':
        last=''.join(c.get('text','') for c in p.get('content',[]))
res=json.loads(last)['results']
input_path=f'.ai/task/{e["task_id"]}/SURFACE-SCREEN-ENVELOPE-{e["dispatch_id"]}.json'
env=[v['entry_revision_identity'] for v in json.load(open(input_path))['payload']['entries']]
got=[r['entry_revision_identity'] for r in res]
print('LOG',L);print('match',got==env,len(got),len(env))
for k,(a,b) in enumerate(zip(env,got)):
    if a!=b:print('MISMATCH',k,a,b)
print('issues',[(r['entry_revision_identity'][:10],r.get('verdict')) for r in res if r.get('verdict')!='OK'])
