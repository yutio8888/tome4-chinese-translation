#!/usr/bin/env bash
# 本地 CI 门禁：与 AGENTS.md「门禁检查」段落一致，任一失败即退出非零。
# 用法：tools/ci-gates.sh [--skip-build]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1
FAILED=0

step() { printf '\n== [%02d] %s ==\n' "$1" "$2"; }
check() { # check <描述> <命令...>
    local desc="$1"; shift
    if "$@" >/tmp/ci-gates-$1.log 2>&1; then
        echo "PASS  $desc"
    else
        echo "FAIL  $desc (log: /tmp/ci-gates-$1.log)"
        FAILED=1
    fi
}

step 1 "doctor"
check "doctor" python3 -B tools/i18n doctor

step 2 "strict lint"
check "lint --strict" python3 -B tools/i18n lint --strict

step 3 "toolchain unit tests"
check "unittest" python3 -m unittest -q tests/i18n/test_toolchain.py

step 4 "cross-component same-tag collision scan"
check "scan_runtime_collisions" python3 -B tools/scan_runtime_collisions.py

step 5 "runtime key classification"
check "classify_runtime_keys" python3 -B tools/classify_runtime_keys.py

step 6 "terminology static audit"
check "audit_static" python3 -B tools/audit_static.py

step 7 "terminology dynamic audit"
check "audit_dynamic" python3 -B tools/audit_dynamic.py

step 8 "domain annotation"
check "annotate_domains" python3 -B tools/annotate_domains.py

step 9 "worktree whitespace"
if git diff --check >/tmp/ci-gates-diffcheck.log 2>&1; then
    echo "PASS  git diff --check"
else
    echo "FAIL  git diff --check (log: /tmp/ci-gates-diffcheck.log)"
    FAILED=1
fi

if [[ "${1:-}" != "--skip-build" ]]; then
    step 10 "core addon strict build"
    check "core addon build" python3 -B tools/i18n build --profile addon --component tome --require-complete
fi

if [[ $FAILED -eq 0 ]]; then
    echo; echo "ALL GATES PASSED"
else
    echo; echo "GATES FAILED"
fi
exit $FAILED
