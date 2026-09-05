#!/usr/bin/env bash
set -uo pipefail

system_tmp=/tmp
suite_tmp=$(mktemp -d "$system_tmp/gemini-evaluator-contract-effectiveness-holdout-v2-tests.XXXXXX") || exit 1
chmod 700 "$suite_tmp"
cleanup() {
  rm -rf -- "$suite_tmp"
}
trap cleanup EXIT HUP INT TERM

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
TMPDIR="$suite_tmp" HOLDOUT_PRIVATE_TEST_TMPDIR="$suite_tmp" node "$script_dir/test-package.mjs"
status=$?
cleanup
trap - EXIT HUP INT TERM

residue=()
for candidate in \
  "$system_tmp"/holdout-test-* \
  "$system_tmp"/holdout-terminal-* \
  "$system_tmp"/gemini-holdout-* \
  "$system_tmp"/gemini-evaluator-contract-effectiveness-holdout-v2-tests.* \
  "$system_tmp"/gen_holdout.py \
  "$system_tmp"/holdout-preflight.json \
  "$system_tmp"/holdout-tests.log
do
  [[ -e "$candidate" ]] && residue+=("$candidate")
done
if ((${#residue[@]})); then
  printf 'registered temporary residue remains\n' >&2
  status=1
fi
exit "$status"
