# Close one lite batch: gates (if translation/tools changed), commit, mark full gates, push via tools/push_github.sh,
# then prepare and dispatch NEXT (empty NEXT = stop). LITE_LANE=B prepares/dispatches B-only backfill batches.
# usage: bash tools/lite_close.sh BATCH NEXT "commit subject" "commit body"
set -u -o pipefail
cd "$(dirname "$0")/.."
unset I18N_FULL_REVIEW_CACHE OLDPWD LANES
: "${PASEO_AGENT_ID:?set PASEO_AGENT_ID to the orchestrator agent id}" "${TOME_PASEO_WORKSPACE:?set TOME_PASEO_WORKSPACE}"
export PATH=/usr/local/bin:$(echo $PATH | tr ':' '\n' | grep -v '^/opt/agents/bin$\|^/usr/local/bin$' | paste -sd:) TOME_LUAJIT=${TOME_LUAJIT:-/usr/bin/luajit} TOME_LUAROCKS_ROOT=${TOME_LUAROCKS_ROOT:-/opt/tome4-luarocks}
B=$1; N=$2; D=evidence/lite-review/batches/$B
if [ -n "$(git status --porcelain -- '*.lua' terminology tools tests i18n docs)" ]; then
  python3 -B tools/lite_gates.py $B > /tmp/lite-$B-gates.log 2>&1; rc=$?
  tail -3 /tmp/lite-$B-gates.log
  [ $rc = 0 ] || { echo "GATES-FAIL $B"; grep FAIL /tmp/lite-$B-gates.log; exit 1; }
fi
git add -A -- '*.lua' terminology tools/lite_review.py tools/lite_gates.py tools/lite_dispatch.sh tools/lite_close.sh tools/lite_loop.sh tools/lite_queue_names.sh docs/lite-review-workflow-20261101.md docs/README.md handoff.md evidence/lite-review || exit 1
printf '%s\n\n%s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n' "$3" "$4" | git commit -q -F - || exit 1
if [ -f $D/gates.json ] && python3 -c "import json,sys;d=json.load(open('$D/gates.json'));sys.exit(0 if d['mode']=='full' and d['passed'] else 1)"; then
  python3 -B tools/lite_gates.py $B --mark || exit 1
fi
echo "COMMITTED $(git log --oneline -1)"
bash tools/push_github.sh 2>&1 | tail -2 || { echo PUSH-FAIL; exit 1; }
[ -n "$N" ] || exit 0
python3 -B tools/lite_review.py prepare $N ${LITE_LANE:+--lane $LITE_LANE} | cut -c1-300 || exit 1
sleep ${LITE_DISPATCH_GAP:-0}   # 2026-11-01 user added a 3-minute gap; 2026-11-02 user removed it (quota normal), set LITE_DISPATCH_GAP to restore
bash tools/lite_dispatch.sh $N > /tmp/lite-review-$N-dispatch.log 2>&1; echo "DISPATCH rc=$?"
grep -v '^{"tool"' /tmp/lite-review-$N-dispatch.log | cut -c1-600 | tail -30
