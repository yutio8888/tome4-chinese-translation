import json,sys,glob,pathlib
# usage: lane257.py precheck <i>  -> compares native-log final JSON identities to envelope
i=sys.argv[2];C=pathlib.Path('.artifacts/i18n/continuation-20260923');B='batch-54d2d16b94c511082107'
cap=json.load(open(C/f'captures275/lane{i}-terminal.json'))['snapshot'];sid=cap['persistence']['sessionId']
L=(glob.glob(f'/home/paseo/.codex/sessions/*/*/*/*{sid}.jsonl')+glob.glob(f'/home/paseo/.codex/archived_sessions/*{sid}.jsonl'))[0]
last=None
for line in open(L):
    o=json.loads(line);p=o.get('payload',{})
    if o.get('type')=='response_item' and p.get('type')=='message' and p.get('role')=='assistant':
        last=''.join(c.get('text','') for c in p.get('content',[]))
res=json.loads(last)['results']
env=[e['entry_revision_identity'] for e in json.load(open(f'.ai/task/{B}/SURFACE-SCREEN-ENVELOPE-lane-000-{i}.json'))['payload']['entries']]
got=[r['entry_revision_identity'] for r in res]
print('LOG',L);print('match',got==env,len(got),len(env))
for k,(a,b) in enumerate(zip(env,got)):
    if a!=b:print('MISMATCH',k,a,b)
print('issues',[(r['entry_revision_identity'][:10],r.get('verdict')) for r in res if r.get('verdict')!='OK'])
