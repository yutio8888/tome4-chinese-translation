import json,hashlib,sys,datetime,os
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_lane_manifest import canonical_bytes,validate_manifest
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());phase=sys.argv[1];cycle=int(sys.argv[2]);attempt=int(sys.argv[3]);mp=P/f'CONTEXTUAL-LANE-GROUP-r{cycle}a{attempt}.json';m=json.loads(mp.read_text());validate_manifest(m,manifest_path=str(mp));s=json.loads((P/'STATE.json').read_text());assert s['review_phase']==phase and s['cycle']==cycle
spec=json.loads((P/f'REVIEW-READY-SPEC-{phase}-{cycle}-{attempt}.json').read_text());dest=Path(spec['path']);assert not dest.exists();assert dest==P/f'REVIEW-READY-{phase}-{cycle}-{attempt}.json';proof=[]
lanes=m['payload']['lanes'];assert len(lanes)==4
for lane in lanes:
 d=next(d for d in s['child_dispatches'] if d['dispatch_id']==lane['dispatch_id']);assert d['lifecycle']=='active' and d['lineage_verified'] and not d['archive_confirmed'];assert d['candidate_identity']==lane['candidate_identity'] and d['input_path']==lane['input_path'];assert d['author_provider_resolution']=='verified'
 f=Path(d['first_live_capture_path']);raw=f.read_bytes();v=json.loads(raw)['snapshot'];assert v['id']==d['agent_id'] and v['workspaceId']==s['workspace_id'] and v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id'];assert v['labels']['candidate_identity']==d['candidate_identity'];assert v['labels']['lane_group_identity']==m['group_identity'];assert int(v['labels']['lane_index'])==d['lane_index'];assert v['status']=='running' and v.get('attentionReason') not in ('finished','error')
 proof.append(dict(dispatch_id=d['dispatch_id'],agent_id=d['agent_id'],first_live_capture=str(f),sha256=hashlib.sha256(raw).hexdigest(),lane_index=d['lane_index'],candidate_identity=d['candidate_identity']))
assert len({r['agent_id'] for r in proof})==4 and {r['lane_index'] for r in proof}=={1,2,3,4};data=canonical_bytes(spec['payload']);assert hashlib.sha256(data).hexdigest()==spec['sha256']
audit=dict(verified=True,phase=phase,cycle=cycle,attempt=attempt,all_four_live_bindings=proof,release_path=str(dest),release_sha256=spec['sha256'],verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),meaning='MCP initial turn limited to frozen readiness check. This one-time token authorizes substantive four-lane review only after all live bindings verified; no extra run or follow-up.')
(P/f'REVIEW-RELEASE-AUDIT-{phase}-{cycle}-{attempt}.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
with dest.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(json.dumps(audit,ensure_ascii=False))
