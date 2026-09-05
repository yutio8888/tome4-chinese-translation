#!/usr/bin/env bash
# 本地 CI 门禁：步骤见 docs/agent-workflow.md，触发条件见 AGENTS.md；任一失败即退出非零。
# 用法：tools/ci-gates.sh [--skip-build]
# 仅当任务 SPEC 证明不影响 addon 输出或构建时，才允许使用 --skip-build。
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

exec python3 -B "$ROOT/tools/ci_gates.py" "$@"
