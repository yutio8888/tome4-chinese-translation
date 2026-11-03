#!/usr/bin/env bash
# Lightweight review dispatch for one batch: create A (Opus 5.5) and B (GPT 6.1 Sol), wait, collect, archive.
# usage: tools/lite_dispatch.sh BATCH            (needs PASEO_AGENT_ID and TOME_PASEO_WORKSPACE in the environment)
# LITE_LANE=B dispatches only B (B backfill batches, 2026-11-02; also used to re-dispatch one failed lane after
# moving its /tmp/lite-review/BATCH/*-LANE files aside).
set -u -o pipefail
cd "$(dirname "$0")/.."
B=$1; D=evidence/lite-review/batches/$B
LN=${LITE_LANE:-A B}
M=.ai/task/full-review-20261013-takeover-runtime/mcpcall.py
W=${TOME_PASEO_WORKSPACE:?}
[ -f $D/input.json ] || { echo "no input for $B"; exit 1; }
mkdir -p /tmp/lite-review/$B
create(){ # lane provider mode
  python3 - "$1" "$2" "$3" > /tmp/lite-review/$B/create-$1.args <<PY
import json,sys
lane,prov,mode=sys.argv[1:4]
print(json.dumps({"provider":prov,"title":"lite-$B-"+lane,"workspaceId":"$W","notifyOnFinish":True,
 "initialPrompt":open("$D/prompt-"+lane+".txt").read(),
 "settings":{"modeId":mode,"thinkingOptionId":"medium"},
 "labels":{"role":"reviewer","purpose":"lite-review","batch":"$B","lane":lane,"paseo.parent-agent-id":"$PASEO_AGENT_ID"}}))
PY
  /usr/bin/python3 -B $M create_agent "$(cat /tmp/lite-review/$B/create-$1.args)" /tmp/lite-review/$B/create-$1.json | cut -c1-160 || return 1
  python3 -c "import json;print(json.load(open('/tmp/lite-review/$B/create-$1.json'))['structuredContent']['agentId'])" > /tmp/lite-review/$B/agent-$1
}
for lane in $LN; do
  [ -s /tmp/lite-review/$B/agent-$lane ] && continue
  if [ $lane = A ]; then create A claude/claude-opus-5-5 auto || exit 1; else create B codex/gpt-6.1-sol auto-review || exit 1; fi
done
echo "agents $(for l in $LN; do printf '%s=%s ' $l $(cat /tmp/lite-review/$B/agent-$l); done)"
for lane in $LN; do
  id=$(cat /tmp/lite-review/$B/agent-$lane)
  for i in $(seq 1 120); do
    /usr/bin/python3 -B $M get_agent_status "{\"agentId\":\"$id\"}" /tmp/lite-review/$B/status-$lane.json >/dev/null 2>&1
    st=$(python3 -c "import json;d=json.loads(json.load(open('/tmp/lite-review/$B/status-$lane.json'))['content'][0]['text']);print(d['status'])" 2>/dev/null)
    case "$st" in idle|error|closed) break;; esac
    sleep 30
  done
  echo "$lane $st"
  raw=/tmp/lite-review/$B-$lane.json
  if [ ! -s $raw ]; then
    /usr/bin/python3 -B $M get_agent_activity "{\"agentId\":\"$id\",\"limit\":1}" /tmp/lite-review/$B/activity-$lane.json >/dev/null
    python3 -c "import json;print(json.load(open('/tmp/lite-review/$B/activity-$lane.json'))['structuredContent']['content'])" > /tmp/lite-review/$B/final-$lane.txt
    raw=/tmp/lite-review/$B/final-$lane.txt
  fi
  python3 -B tools/lite_review.py collect $B $lane $raw || echo "COLLECT-$lane-FAIL"
done
for lane in $LN; do
  /usr/bin/python3 -B $M archive_agent "{\"agentId\":\"$(cat /tmp/lite-review/$B/agent-$lane)\"}" /tmp/lite-review/$B/archive-$lane.json | cut -c1-100
done
echo DISPATCH-DONE
