set -euo pipefail
C=.artifacts/i18n/continuation-20260923; B=batch-54d2d16b94c511082107; H=evidence/quality/production-batches/$B-host-evidence
git commit -q -F /tmp/e275.txt
E=$(git rev-parse HEAD); echo evidence=$E; echo $E > /tmp/evid275
python3 -c "
import json,datetime;json.dump(dict(commit='$E',batch_id='$B',committed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),open('$C/review275-evidence-commit.json','w'),indent=2)"
python3 $C/timed_command.py $C/review275-finalize python3 -B tools/i18n production batch finalize --commit $E 2>&1 | tail -3
python3 -B $C/close_review275.py | tail -1
python3 /tmp/h275.py
git add -f $H/FINALIZE-RECEIPT.json $H/RUNTIME-BOUNDARY-RECEIPT.json handoff.md
git diff --cached --check
git commit -q -F /tmp/c275.txt
echo closure=$(git rev-parse HEAD)
python3 $C/timed_command.py $C/review275-post-closure-queue python3 -B tools/i18n production queue rebuild >/dev/null 2>&1
grep exit_code $C/review275-post-closure-queue-timing.json
git push -q origin develop
git fetch -q
git rev-parse HEAD origin/develop
git status --short | grep -v '^??' || true
echo ALL_OK
