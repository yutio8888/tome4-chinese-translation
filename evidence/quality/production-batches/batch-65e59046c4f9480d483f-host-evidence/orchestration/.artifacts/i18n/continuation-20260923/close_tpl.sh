set -euo pipefail
cd /workspace/tome4-chinese-translation
export TOME_PASEO_WORKSPACE=wks_420314270844170b
C=.artifacts/i18n/continuation-20260923; N=$1; B=$2; T=${3-$1}; H=evidence/quality/production-batches/$B-host-evidence
git commit -q -F /tmp/e$N.txt
E=$(git rev-parse HEAD); echo evidence=$E; echo $E > /tmp/evid$N
python3 -c "
import json,datetime;json.dump(dict(commit='$E',batch_id='$B',committed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),open('$C/review$T-evidence-commit.json','w'),indent=2)"
python3 $C/timed_command.py $C/review$T-finalize python3 -B tools/i18n production batch finalize --commit $E 2>&1 | tail -3
python3 -B $C/close_review$T.py | tail -1
python3 -B $C/handoff_gen.py $N "$T"
git add -f $H/FINALIZE-RECEIPT.json $H/RUNTIME-BOUNDARY-RECEIPT.json handoff.md
git diff --cached --check
git commit -q -F /tmp/c$N.txt
echo closure=$(git rev-parse HEAD)
I18N_PROJECTION_CACHE=on python3 $C/timed_command.py $C/review$T-post-closure-queue python3 -B tools/i18n production queue rebuild >/dev/null 2>&1
grep exit_code $C/review$T-post-closure-queue-timing.json
git push -q origin develop
git fetch -q
git rev-parse HEAD origin/develop
git status --short | grep -v '^??' || true
echo ALL_OK
