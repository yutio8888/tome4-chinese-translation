# usage: bash tools/lite_loop.sh START_BATCH [MAX_BATCHES]
# START_BATCH must already be dispatched (DISPATCH-DONE in /tmp/lite-review-START-dispatch.log).
# Clean batches (0 ISSUE in every lane of the batch) are recorded, committed, pushed, and the next batch is dispatched.
# Stops with NEEDS-ADJUDICATION when a batch has ISSUEs, or on any failure.
set -u -o pipefail
cd "$(dirname "$0")/.."
: "${PASEO_AGENT_ID:?set PASEO_AGENT_ID to the orchestrator agent id}" "${TOME_PASEO_WORKSPACE:?set TOME_PASEO_WORKSPACE}"
export PATH=/usr/local/bin:$(echo $PATH | tr ':' '\n' | grep -v '^/opt/agents/bin$\|^/usr/local/bin$' | paste -sd:) TOME_LUAJIT=${TOME_LUAJIT:-/usr/bin/luajit} TOME_LUAROCKS_ROOT=${TOME_LUAROCKS_ROOT:-/opt/tome4-luarocks}
B=$1; LEFT=${2:-20}
while :; do
  L=/tmp/lite-review-$B-dispatch.log
  grep -qx 'DISPATCH-DONE' $L || { echo "NOT-DONE $B"; exit 1; }
  grep -q 'COLLECT-.*-FAIL' $L && { echo "COLLECT-FAIL $B"; grep -v '^{"tool"' $L | tail -5; exit 1; }
  na=$(grep -c '^[AB] [0-9]* verdicts; ISSUE 0:' $L)
  nl=$(python3 -c "import json;print(len(json.load(open('evidence/lite-review/batches/$B/input.json')).get('lanes','AB')))")
  [ "$na" = "$nl" ] || { echo "NEEDS-ADJUDICATION $B"; grep -v '^{"tool"' $L | cut -c1-1500 | tail -8; exit 2; }
  D=evidence/lite-review/batches/$B
  n=$(python3 -c "import json;print(len(json.load(open('$D/input.json'))['entries']))")
  secs=$(python3 -c "import json;print(', '.join(json.load(open('$D/input.json'))['sections']))" 2>/dev/null || true)
  echo '{"confirmed": [], "advisory": [], "rejected": [], "notes": "A and B returned no ISSUE."}' > $D/decision.json
  python3 -B tools/lite_review.py record $B || exit 1
  LEFT=$((LEFT-1)); NB=$(printf '%04d' $((10#$B+1)))
  [ $LEFT -gt 0 ] && NEXT=$NB || NEXT=
  bash tools/lite_close.sh $B "$NEXT" "review: lite batch $B ($n units, no issues)" "A and B returned OK for all $n units. Sections: ${secs:-see input.json}." | grep -v '^\s*$' | tail -6
  [ ${PIPESTATUS[0]} = 0 ] || { echo "CLOSE-FAIL $B"; exit 1; }
  [ -n "$NEXT" ] || { echo "LOOP-BUDGET-END after $B"; exit 0; }
  B=$NEXT
done
