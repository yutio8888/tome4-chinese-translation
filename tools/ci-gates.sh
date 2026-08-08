#!/usr/bin/env bash
# 本地 CI 门禁：与 AGENTS.md「门禁检查」段落一致，任一失败即退出非零。
# 用法：tools/ci-gates.sh [--skip-build]
set -u

usage() {
    printf 'Usage: %s [--skip-build]\n' "$0" >&2
}

SKIP_BUILD=0
case "$#" in
    0)
        ;;
    1)
        if [[ "$1" == "--skip-build" ]]; then
            SKIP_BUILD=1
        else
            printf 'ERROR: unknown argument: %s\n' "$1" >&2
            usage
            exit 2
        fi
        ;;
    *)
        printf \
            'ERROR: expected no arguments or exactly --skip-build; received %d arguments.\n' \
            "$#" >&2
        usage
        exit 2
        ;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

LOG_ROOT="$ROOT/.artifacts/i18n/ci-gates"
if ! mkdir -p "$LOG_ROOT"; then
    printf 'ERROR: unable to create CI gate log root: %s\n' "$LOG_ROOT" >&2
    exit 1
fi
if ! LOG_DIR="$(mktemp -d "$LOG_ROOT/run.XXXXXX")"; then
    printf 'ERROR: unable to create a unique CI gate log directory under: %s\n' "$LOG_ROOT" >&2
    exit 1
fi
printf 'CI gate log directory: %s\n' "$LOG_DIR"

FAILED=0

step() { printf '\n== [%02d] %s ==\n' "$1" "$2"; }
check() { # check <日志 slug> <描述> <命令...>
    local slug="$1"
    local desc="$2"
    local log_path="$LOG_DIR/$slug.log"
    shift 2
    if "$@" >"$log_path" 2>&1; then
        echo "PASS  $desc"
    else
        echo "FAIL  $desc (log: $log_path)"
        FAILED=1
    fi
}

step 1 "doctor"
check "01-doctor" "doctor" python3 -B tools/i18n doctor

step 2 "strict lint"
check "02-strict-lint" "lint --strict" python3 -B tools/i18n lint --strict

step 3 "toolchain unit tests"
check "03-toolchain-unit-tests" "unittest" python3 -m unittest -q tests/i18n/test_toolchain.py

step 4 "quality and Facts unit tests"
check \
    "04-quality-facts-unit-tests" \
    "quality/Facts unittest" \
    python3 -m unittest -q \
    tests/i18n/test_quality_contracts.py \
    tests/i18n/test_quality_claims.py \
    tests/i18n/test_dataset_registry.py \
    tests/i18n/test_quality_v2.py \
    tests/i18n/test_quality_v3.py \
    tests/i18n/test_facts_study.py \
    tests/i18n/test_facts_curation.py

step 5 "cross-component same-tag collision scan"
check \
    "05-runtime-collision-scan" \
    "scan_runtime_collisions" \
    python3 -B tools/scan_runtime_collisions.py

step 6 "runtime key classification"
check \
    "06-runtime-key-classification" \
    "classify_runtime_keys" \
    python3 -B tools/classify_runtime_keys.py

step 7 "terminology static audit"
check "07-terminology-static-audit" "audit_static" python3 -B tools/audit_static.py

step 8 "terminology dynamic audit"
check "08-terminology-dynamic-audit" "audit_dynamic" python3 -B tools/audit_dynamic.py

step 9 "domain annotation"
check "09-domain-annotation" "annotate_domains" python3 -B tools/annotate_domains.py

step 10 "worktree whitespace"
check "10-worktree-whitespace" "git diff --check" git diff --check

if [[ $SKIP_BUILD -eq 0 ]]; then
    step 11 "core addon strict build"
    check \
        "11-core-addon-build" \
        "core addon build" \
        python3 -B tools/i18n build --profile addon --component tome --require-complete
fi

if [[ $FAILED -eq 0 ]]; then
    echo; echo "ALL GATES PASSED"
else
    echo; echo "GATES FAILED"
fi
exit $FAILED
