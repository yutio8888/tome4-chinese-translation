# usage: bash tools/lite_queue_names.sh BATCH   (B-only backfill batches; LITE_LANE defaults to B)
# Every B ISSUE of BATCH was host-checked and is a coined name (artifact/talent/effect name): append it to the naming
# queue for the next Gemini 4 Argon round, record it advisory, close the batch and continue the loop.
# The queue lives in /tmp/bfill-naming-queue.json; copy it into the maintenance batch that applies the names.
set -u -o pipefail
cd "$(dirname "$0")/.."
: "${PASEO_AGENT_ID:?set PASEO_AGENT_ID to the orchestrator agent id}" "${TOME_PASEO_WORKSPACE:?set TOME_PASEO_WORKSPACE}"
export LITE_LANE=${LITE_LANE:-B} PATH=/usr/local/bin:$(echo $PATH | tr ':' '\n' | grep -v '^/opt/agents/bin$\|^/usr/local/bin$' | paste -sd:) TOME_LUAJIT=${TOME_LUAJIT:-/usr/bin/luajit} TOME_LUAROCKS_ROOT=${TOME_LUAROCKS_ROOT:-/opt/tome4-luarocks}
unset I18N_FULL_REVIEW_CACHE OLDPWD LANES
B=$1; NB=$(printf '%04d' $((10#$B+1)))
python3 - "$B" <<'EOF' || exit 1
import json,os,sys
B=sys.argv[1]; b=f'evidence/lite-review/batches/{B}/'
inp={e['id']:e for e in json.load(open(b+'input.json'))['entries']}
V={v['id']:v for v in json.load(open(b+'B.json'))['verdicts'] if v['verdict']=='ISSUE'}
Q='/tmp/bfill-naming-queue.json'; q=json.load(open(Q)) if os.path.exists(Q) else []
have={x['id'] for x in q}
for k,v in V.items():
    if k in have: continue
    e=inp[k]; q.append({"batch":B,"id":k,"unit_id":e['unit_id'],"file":e['translation_file'],"line":e['translation_line'],"section":e['section'],"source":e['source'],"target":e['target'],"observation":v['observation'],"suggestion":v.get('suggestion')})
json.dump(q,open(Q,'w'),ensure_ascii=False,indent=1)
json.dump({"confirmed":[],"advisory":[{"id":k,"reason":"Coined name; host checked the B observation against the cited source; queued for the Gemini 4 Argon naming round of the B backfill."} for k in V],"rejected":[],"notes":"B backfill batch."},open(b+'decision.json','w'),ensure_ascii=False,indent=1)
print('queue',len(q))
EOF
python3 -B tools/lite_review.py record $B | tail -1 || exit 1
bash tools/lite_close.sh $B $NB "review: lite batch $B (B backfill), names queued for Gemini" "Coined names reported by B are queued for the Gemini naming round." || exit 1
bash tools/lite_loop.sh $NB 60
