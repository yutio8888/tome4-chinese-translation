# cx373.py live <k> <aid> <sid> <createdAt> <updatedAt> <lastUserMessageAt|null> <turnStartedAt>  -> write live capture + bind
# cx373.py intent <k>                -> create-intent, prints labels json + prompt
# cx373.py done <k> <updatedAt> <attentionTs> '<lastUsage json>'  -> terminal capture, harvest, archive-intent
# cx373.py conf <k> <archivedAt>     -> archive capture + archive-confirm
import json,sys,subprocess
C='.artifacts/i18n/continuation-20260923';N='373';B='batch-eb93936e38c73186d222'
mode,k=sys.argv[1],int(sys.argv[2])
TK=3 if k==4 else k
key=f'{B}-contextual-{TK:03d}|full-{k:03d}';CH=f'{C}/review{N}-contextual-children.json'
live=f'{C}/review{N}-contextual-{k}-live.json';term=f'{C}/review{N}-contextual-{k}-terminal.json';arch=f'{C}/review{N}-contextual-{k}-archive.json'
def run(*a,**kw):
    r=subprocess.run(list(a),capture_output=True,text=True,**kw);return r
if mode=='intent':
    r=run('python3','-B','tools/orchestration/review_lifecycle.py','create-intent',CH,key,'--profiles',f'{C}/profiles-live-01.json')
    assert r.returncode==0,r.stderr
    e=json.loads(r.stdout);open(f'/tmp/ci{N}-{k}.json','w').write(r.stdout)
    l=dict(e['labels']);l.pop('paseo.parent-agent-id',None);print(json.dumps(l,ensure_ascii=False));print('----');print(e['prompt'])
elif mode=='live':
    aid,sid,cr,up,lu,ts=sys.argv[3:9]
    v=json.load(open(f'{C}/review372-contextual-0-live.json'));s=v['snapshot']
    stale=[s['id'],s['persistence']['sessionId'],s['labels']['candidate_identity']]
    e=json.load(open(f'/tmp/ci{N}-{k}.json'))
    title=f'Review {N} contextual full-{k:03d}'
    s.update(id=aid,createdAt=cr,updatedAt=up,lastUserMessageAt=None if lu=='null' else lu,title=title)
    s['activeTurn']={"turnId":"foreground-turn-1","startedAt":ts}
    s['persistence']['sessionId']=s['persistence']['nativeHandle']=sid
    s['persistence']['metadata']['title']=title
    s['labels']=dict(e['labels'])
    t=json.dumps(v,ensure_ascii=False);assert not any(x in t for x in stale),'stale'
    open(live,'w').write(t)
    r=run('python3','-B','tools/orchestration/review_lifecycle.py','bind',CH,key,'--capture',live);print('bind',r.returncode,r.stderr[-400:])
elif mode=='done':
    up,at,usage=sys.argv[3:6]
    v=json.load(open(live));s=v['snapshot'];sid=s['persistence']['sessionId']
    s.update(activeTurn=None,attentionReason='finished',attentionTimestamp=at,requiresAttention=True,status='idle',updatedAt=up,lastUsage=json.loads(usage),
     runtimeInfo={"provider":"claude","sessionId":sid,"model":"claude-opus-5-5","modeId":"auto","extra":{"runtimeModel":"claude-opus-5-5"}})
    v['status']='idle';open(term,'w').write(json.dumps(v,ensure_ascii=False))
    r=run('python3','-B','tools/orchestration/review_lifecycle.py','harvest',CH,key,'--capture',term,'--native-log',f'/home/paseo/.claude/projects/-workspace-tome4-chinese-translation/{sid}.jsonl','--outdir',f'{C}/review{N}-contextual-diag','--notified')
    open(f'/tmp/h{N}c{k}.log','w').write(r.stdout+r.stderr);print('harvest',r.returncode,(r.stdout+r.stderr)[-500:])
    ch=json.load(open(CH));print('output_valid',[(c['dispatch_id'],c.get('output_valid')) for c in ch])
    if r.returncode==0:
        r=run('python3','-B','tools/orchestration/review_lifecycle.py','archive-intent',CH,key,'--capture',term);print('intent',r.returncode,r.stderr[-300:])
elif mode=='conf':
    at=sys.argv[3]
    r=run('python3','-B',f'{C}/mkarch257.py',term,arch,at,at);assert r.returncode==0,r.stderr
    r=run('python3','-B','tools/orchestration/review_lifecycle.py','archive-confirm',CH,key,'--capture',arch);print('confirm',r.returncode,r.stderr[-300:])
