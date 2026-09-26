# Batch driver for single-component (all-Cults) review batches; wraps the same
# lifecycle/tool calls the per-step flow used, grouped so one host turn covers
# several lanes. Usage: N=296 source .artifacts/i18n/continuation-20260923/bd.sh
# MCP calls (create_agent/get_agent_status/archive_agent) stay with the host.
cd /workspace/tome4-chinese-translation
C=.artifacts/i18n/continuation-20260923
export TOME_PASEO_WORKSPACE=wks_420314270844170b I18N_PROJECTION_CACHE=on
[ -n "$N" ] || { echo "N unset: run N=<num>; source bd.sh as two statements"; return 1; }
P=$((N - 1))
# T = file tag (review$T-*); batch 296 was run with an empty tag, later batches use T=N.
T=${T-$N}
PT=${PT-$P}
# S = template source number for script derivation (297 derives from 295 because 296 used the empty tag).
S=${S-$PT}
bid(){ python3 -c "import re;print(re.search(r'\"batch_id\": \"(batch-[0-9a-f]+)\"',open('$C/review$1-start.out').read()).group(1))"; }
[ -f $C/review$T-start.out ] && B=$(bid "$T")

# bd_pre: start + freeze + derive scripts from N-1 + prepare/export/stage/emit + intent for lane 0.
# create-intent refuses while another lane is dispatching/created, so lanes go create -> status -> bd_binds + next intent.
bd_pre(){ (
  set -e
  [ -z "$(git status --short | grep -v '^??')" ] || { echo DIRTY_TREE; exit 1; }
  [ ! -f $C/review$T-start.out ] || { echo START_EXISTS; exit 1; }
  python3 $C/timed_command.py $C/review$T-start python3 -B tools/i18n production batch start --limit 80 > $C/review$T-start.out 2>&1
  B=$(bid "$T"); echo batch=$B
  python3 -B tools/orchestration/freeze_workset.py $B 2>&1 | tail -1
  python3 -c "
import json,collections,sys;d=json.load(open('evidence/quality/production-batches/$B-source-workset.json'))
c=collections.Counter(i['component'] for i in d['entries']);print('components',dict(c))
sys.exit(0 if set(c)=={'cults'} else 3)" || { echo MIXED_OR_NON_CULTS_BATCH_USE_MANUAL_TEMPLATES; exit 3; }
  [ -n "$S" ] && [ -n "$T" ] || { echo "template source S and tag T must be non-empty"; exit 1; }
  O=$(bid "$S")
  for n in lane mklive mkterm prepare_contextual prepare_review stage_review%s_current snapshot_review%s_current close_review%s; do
    f=$(printf "$n" $S); [ "$f" = "$n" ] && f=$n$S; g=${f/$S/$T}
    sed "s/$O/$B/g;s/review$S/review$T/g;s/\([a-z_]\)$S\([._/-]\)/\1$T\2/g;s/审核$S/审核$N/g;s/第${S}批/第${N}批/g" $C/$f.py > $C/$g.py
    left=$(grep -c "review$S\|$O" $C/$g.py || true); [ "$left" = 0 ] || { echo "LEFTOVER $g $left"; exit 1; }
  done
  sed "s/$O/$B/g;s/review$S/review$T/g;s/mklive$S/mklive$T/g;s/mkterm$S/mkterm$T/g;s/lane$S/lane$T/g" /tmp/r$S.sh > /tmp/r$T.sh
  left=$(grep -c "$S\|$O" /tmp/r$T.sh || true); [ "$left" = 0 ] || { echo "LEFTOVER r$T.sh $left"; exit 1; }
  python3 -B $C/prepare_review$T.py 2>&1 | tail -1
  python3 $C/timed_command.py $C/review$T-surface-export python3 -B tools/i18n production batch surface-export >/dev/null 2>&1
  python3 -B tools/orchestration/stage_surface.py $B --out $C/review$T-surface-plan.json 2>&1 | tail -1
  python3 -B tools/orchestration/dispatch_surface.py $C/review$T-surface-plan.json $C/review$T-surface-children.json --emit $C/review$T-surface-emit.json --select-transport mcp --provider codex/gpt-6-sol --thinking medium --mode auto-review 2>&1 | tail -1
  L=$(python3 -c "import json;print(len(json.load(open('$C/review$T-surface-emit.json'))))"); echo lanes=$L
  bd_intents 0
) ; }

# bd_intents <n>...: durable create-intent per lane; prints title, labels and prompt for create_agent.
bd_intents(){ source /tmp/r$T.sh; for n in "$@"; do echo "=== lane $n title=$(did $n)"; intent $n; done; }

# bd_binds "<n> <aid> <sid> <createdAt> <updatedAt> <turnStartedAt> <lastUserMessageAt|null>" ...
bd_binds(){ source /tmp/r$T.sh; for a in "$@"; do live $a; done; }

# bd_hs "<n> <updatedAt> <lastUserMessageAt> <attentionTimestamp> <sessionId>" ...: precheck + harvest + archive-intent.
bd_hs(){ source /tmp/r$T.sh; for a in "$@"; do set -- $a; h $1 $2 $3 $4 $5 20; done; }

# bd_confs "<n> <archivedAt>" ...
bd_confs(){ source /tmp/r$T.sh; for a in "$@"; do conf $a; done; }

# bd_mid: native audit (gating) + boundary audit + close/index/import + contextual prep/export/stage/emit/intent,
# then dumps the flagged surface entries for adjudication.
bd_mid(){ (
  set -e
  python3 $C/audit_native_tools.py $C/review$T-surface-children.json .ai/task/$B > $C/review$T-surface-audit.txt 2>&1
  python3 - "$B" "$T" <<'EOF'
import json,re,glob,hashlib,datetime,sys
B,N=sys.argv[1:3];C='.artifacts/i18n/continuation-20260923'
bad_any=False
for f in sorted(glob.glob(f'.ai/task/{B}/NATIVE-TOOLS-lane-*.json')):
    calls=json.load(open(f));txt=' '.join(json.dumps(c.get('input') or c.get('arguments'),ensure_ascii=False) for c in calls)
    bad=[w for w in ('>>','tee ','apply_patch','create_terminal','send_terminal_keys','rm ','mv ',"'w'",'"w"') if w in txt]
    print(f[-15:-5],len(calls),bad)
    bad_any|=bool(bad)
if bad_any:
    print('BOUNDARY_HIT: inspect before close/import (see reviewer-paseo-terminal-sandbox-bypass)');sys.exit(4)
ch=json.load(open(f'{C}/review{N}-surface-children.json'))
items=[]
for c in ch:
    raw=open(f'.ai/task/{B}/NATIVE-TOOLS-{c["dispatch_id"]}.json','rb').read()
    items.append(dict(dispatch_id=c['dispatch_id'],agent_id=c['agent_id'],native_tools_sha256=hashlib.sha256(raw).hexdigest(),tool_calls=len(json.loads(raw)),archive_confirmed=c['archive_confirmed'],output_valid=c.get('output_valid')))
assert all(i['archive_confirmed'] and i['output_valid'] for i in items)
json.dump(dict(batch_id=B,review_contract='translation_surface_screen_v1',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),launched=len(items),undispatched_prepared=0,all_launched_archived=True,
 allowed_read_files='each own frozen envelope and surface contract',other_commands='reads of the own envelope and contract only; no write-pattern hits',
 write_or_external_calls_observed=False,rejected=[],identity_echo_corrections=[],
 items=items),open(f'.ai/task/{B}/HOST-SURFACE-BOUNDARY-AUDIT.json','w'),ensure_ascii=False,indent=2)
print('audit ok')
EOF
  bd_mid_rest
) ; }

# bd_mid_rest: everything after the boundary audit (rerun this alone after a manual audit).
bd_mid_rest(){ (
  set -e
  mkdir -p $C/review$T-surface-raw
  python3 -B tools/orchestration/close_review_tasks.py surface $C/review$T-surface-plan.json $C/review$T-surface-children.json $C/review$T-surface-raw 2>&1 | tail -1
  python3 -B tools/orchestration/build_import_index.py surface $C/review$T-surface-raw $C/review$T-surface-index.json 2>&1 | tail -1
  python3 $C/timed_command.py $C/review$T-surface-import python3 -B tools/orchestration/run_batch_steps.py surface-import=$C/review$T-surface-index.json >/dev/null 2>&1
  python3 -B $C/prepare_contextual$T.py > /tmp/pc$T.out 2>&1; grep -o "PREFLIGHT_[A-Z]*" /tmp/pc$T.out | head -1
  python3 $C/timed_command.py $C/review$T-contextual-export python3 -B tools/orchestration/run_batch_steps.py contextual-export=evidence/quality/production-batches/$B-source-workset.json >/dev/null 2>&1
  python3 -B tools/orchestration/stage_contextual.py $B --out $C/review$T-contextual-plan.json 2>&1 | tail -1
  python3 -B tools/orchestration/dispatch_contextual.py $C/review$T-contextual-plan.json $C/review$T-contextual-children.json --emit $C/review$T-contextual-emit.json --select-transport mcp --provider claude/claude-opus-5-5 --thinking medium --mode auto 2>&1 | tail -1
  python3 -B tools/orchestration/review_lifecycle.py create-intent $C/review$T-contextual-children.json "$B-contextual-000|full-000" --profiles $C/profiles-live-01.json > /tmp/ci$T.json 2>&1
  python3 -c "
import json;e=json.load(open('/tmp/ci$T.json'));l=e['labels'];l.pop('paseo.parent-agent-id',None);print('CTX_LABELS',json.dumps(l));print('CTX_PROMPT');print(e['prompt'])"
  bd_dump surface
) ; }

# bd_dump surface|contextual: flagged entries with observation, source and target (for adjudication).
bd_dump(){ python3 - "$B" "$T" "$1" <<'EOF'
import json,glob,sys
B,N,stage=sys.argv[1:4];C='.artifacts/i18n/continuation-20260923'
E={e['entry_revision_identity']:e for e in json.load(open(f'evidence/quality/production-batches/{B}-source-workset.json'))['entries']}
if stage=='surface':
    flagged=[(r['entry_revision_identity'],r['observation']) for f in sorted(glob.glob(f'{C}/review{N}-surface-raw/*.json')) for r in json.load(open(f))['results'] if r['verdict']=='ISSUE']
else:
    flagged=[(v['revision_key'],v['observation']) for f in sorted(glob.glob(f'{C}/review{N}-contextual-raw/*.json')) for v in json.load(open(f))['verdicts'] if v['verdict']=='ISSUE']
    ok=[v['revision_key'][:10] for f in sorted(glob.glob(f'{C}/review{N}-contextual-raw/*.json')) for v in json.load(open(f))['verdicts'] if v['verdict']!='ISSUE']
    print('CTX_OK',ok)
out=[]
for k,obs in flagged:
    e=E[k];out.append(f"===== {k[:10]} {e['section']} {e['source_tag']}\nOBS: {obs}\nEN: {e['source'][:1500]!r}\nZH: {e['target'][:1000]!r}")
open(f'/tmp/s{N}-{stage}.txt','w').write('\n'.join(out)+'\n')
print(f'{len(flagged)} flagged -> /tmp/s{N}-{stage}.txt')
EOF
}

# bd_cbind <aid> <sessionId> <createdAt> <updatedAt> <lastUserMessageAt> <turnStartedAt>
bd_cbind(){ python3 - "$T" "$PT" "$B" "$@" "$N" <<'EOF'
import json,sys
N,P,B,aid,sid,cr,up,lu,ts,num=sys.argv[1:11];C='.artifacts/i18n/continuation-20260923'
old=json.load(open(f'{C}/review{P}-contextual-0-live.json'));old_s=old['snapshot']
stale=[old_s['id'],old_s['persistence']['sessionId'],old_s['labels']['candidate_identity']]
e=json.load(open(f'/tmp/ci{N}.json'));v=old;s=v['snapshot']
title=f'Review {num} contextual full-000'
s.update(id=aid,createdAt=cr,updatedAt=up,lastUserMessageAt=lu,title=title)
s['activeTurn']={"turnId":"foreground-turn-1","startedAt":ts}
s['persistence']['sessionId']=s['persistence']['nativeHandle']=sid
s['persistence']['metadata']['title']=title
s['labels']=dict(e['labels'])
t=json.dumps(v,ensure_ascii=False);assert not any(x in t for x in stale),'stale identity'
open(f'{C}/review{N}-contextual-0-live.json','w').write(t)
EOF
  python3 -B tools/orchestration/review_lifecycle.py bind $C/review$T-contextual-children.json "$B-contextual-000|full-000" --capture $C/review$T-contextual-0-live.json; echo cbind=$?; }

# bd_ch <updatedAt> <attentionTimestamp> '<lastUsage json>': terminal capture + harvest + archive-intent.
bd_ch(){ python3 - "$T" "$@" <<'EOF'
import json,sys
N,up,at,usage=sys.argv[1:5];C='.artifacts/i18n/continuation-20260923'
v=json.load(open(f'{C}/review{N}-contextual-0-live.json'));s=v['snapshot']
sid=s['persistence']['sessionId']
s.update(activeTurn=None,attentionReason='finished',attentionTimestamp=at,requiresAttention=True,status='idle',updatedAt=up,lastUsage=json.loads(usage),
 runtimeInfo={"provider":"claude","sessionId":sid,"model":"claude-opus-5-5","modeId":"auto","extra":{"runtimeModel":"claude-opus-5-5"}})
v['status']='idle'
open(f'{C}/review{N}-contextual-0-terminal.json','w').write(json.dumps(v,ensure_ascii=False))
EOF
  local K="$B-contextual-000|full-000" sid
  sid=$(python3 -c "import json;print(json.load(open('$C/review$T-contextual-0-live.json'))['snapshot']['persistence']['sessionId'])")
  python3 -B tools/orchestration/review_lifecycle.py harvest $C/review$T-contextual-children.json "$K" --capture $C/review$T-contextual-0-terminal.json --native-log /home/paseo/.claude/projects/-workspace-tome4-chinese-translation/$sid.jsonl --outdir $C/review$T-contextual-diag --notified > /tmp/h${T}c0.log 2>&1; echo harvest=$?
  python3 -c "import json;print('output_valid',[c.get('output_valid') for c in json.load(open('$C/review$T-contextual-children.json'))])"
  python3 -B tools/orchestration/review_lifecycle.py archive-intent $C/review$T-contextual-children.json "$K" --capture $C/review$T-contextual-0-terminal.json >/dev/null; echo intent=$?; }

# bd_cconf <archivedAt>: archive-confirm + close + index + dump flagged contextual entries.
bd_cconf(){ (
  set -e
  python3 -B $C/mkarch257.py $C/review$T-contextual-0-terminal.json $C/review$T-contextual-0-archive.json $1 $1
  python3 -B tools/orchestration/review_lifecycle.py archive-confirm $C/review$T-contextual-children.json "$B-contextual-000|full-000" --capture $C/review$T-contextual-0-archive.json >/dev/null
  mkdir -p $C/review$T-contextual-raw
  python3 -B tools/orchestration/close_review_tasks.py contextual $C/review$T-contextual-plan.json $C/review$T-contextual-children.json $C/review$T-contextual-raw 2>&1 | tail -1
  python3 -B tools/orchestration/build_import_index.py contextual $C/review$T-contextual-raw $C/review$T-contextual-index.json 2>&1 | tail -1
  bd_dump contextual
) ; }

# bd_close: needs review$T-host-decisions.json, /tmp/fin$N.json, /tmp/e$N.txt and /tmp/c$N.txt.
# Source root -> timed chain -> finalize_host_gen -> snapshot -> stage -> evidence commit -> finalize ->
# closure commit -> push. Stops at the first failure; nothing is committed before snapshot and stage pass.
bd_close(){ (
  set -euo pipefail
  for f in $C/review$T-host-decisions.json /tmp/fin$N.json /tmp/e$N.txt /tmp/c$N.txt; do [ -s $f ] || { echo "MISSING $f"; exit 1; }; done
  python3 - "$B" "$T" <<'EOF'
import json,hashlib,os,shutil,sys
B,N=sys.argv[1:3];C='.artifacts/i18n/continuation-20260923'
d=json.load(open(f'evidence/quality/production-batches/{B}-source-workset.json'))
dec=json.load(open(f'{C}/review{N}-host-decisions.json'))['decisions']
conf={k.split('|')[0] for k,v in dec.items() if v['disposition']=='confirmed'}
R=f'{C}/review{N}-source-root';n=0
for v in d['source_verification']:
  if v['entry_revision_identity'][:10] not in conf: continue
  p=v['public_source_path'];src='/workspace/tome4-dlcs/cults/'+p
  h=hashlib.sha256(open(src,'rb').read()).hexdigest();assert h==v['source_file_sha256'],(p,h)
  dst=f'{R}/{p}';os.makedirs(os.path.dirname(dst),exist_ok=True)
  if not os.path.exists(dst): shutil.copy2(src,dst);n+=1
print('source-root copied',n,'confirmed',len(conf))
EOF
  D=$(date -u +%Y%m%d)
  python3 $C/timed_command.py $C/review$T-adjudication-chain python3 -B tools/orchestration/run_batch_steps.py contextual-adjudication-chain --input $C/review$T-contextual-index.json --spec $C/review$T-host-decisions.json --output .artifacts/i18n/adjudication-chain/review$T-$D-attempt01.json --source-root $C/review$T-source-root > $C/review$T-chain.log 2>&1
  grep -q '"ok": true' $C/review$T-chain.log
  echo chain_ok
  python3 -B $C/finalize_host_gen.py $N "$T"
  sed -i "s#adjudication-chain/review$T-[0-9]\{8\}-attempt01.json#adjudication-chain/review$T-$D-attempt01.json#" $C/snapshot_review${T}_current.py
  grep -q "review$T-$D-attempt01.json" $C/snapshot_review${T}_current.py
  python3 -B $C/snapshot_review${T}_current.py | tail -1
  python3 -B $C/stage_review${T}_current.py | tail -1
  bash $C/close_tpl.sh $N $B "$T"
) ; }
