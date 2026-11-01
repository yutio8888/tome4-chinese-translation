#!/usr/bin/env bash
# Push the local develop branch to GitHub through a filtered mirror without evidence/full-review (2026-11-01 user decision:
# GitHub keeps tools and texts only; the local repository keeps the complete evidence history).
#   tools/push_github.sh init   build ~/tome4-github-mirror by filtering all local commits after the last pushed remote commit
#   tools/push_github.sh        cherry-pick new local develop commits onto the mirror and push them
set -u -o pipefail
SRC=$(cd "$(dirname "$0")/.." && pwd)
MIR=${TOME_GITHUB_MIRROR:-$HOME/tome4-github-mirror}   # bare repository (filtered history)
WT=$MIR-worktree                                        # light worktree of the filtered develop for cherry-picks
URL=$(git -C "$SRC" remote get-url origin)
MAP=$MIR/lite-sync-last                                 # last local develop commit already mirrored
if [ "${1:-}" = init ]; then
  [ -e "$MIR" ] && { echo "mirror exists: $MIR"; exit 1; }
  BASE=$(git -C "$SRC" rev-parse origin/develop)
  git clone -q --bare "$SRC" "$MIR" && cd "$MIR" || exit 1
  git remote set-url origin "$URL"
  FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --prune-empty \
    --index-filter 'git rm -r -q --cached --ignore-unmatch evidence/full-review' -- "$BASE..develop" || exit 1
  git -C "$SRC" rev-parse develop > "$MAP"
  git log --oneline -1 develop
  echo "mirror ready at $MIR; base $BASE"
  exit 0
fi
cd "$MIR" || { echo "no mirror; run: tools/push_github.sh init"; exit 1; }
[ -d "$WT" ] || git worktree add -q "$WT" develop || exit 1
cd "$WT" || exit 1
git fetch -q "$SRC" develop || exit 1
LAST=$(cat "$MAP")
for c in $(git rev-list --reverse "$LAST..FETCH_HEAD"); do
  if git -C "$SRC" diff-tree --no-commit-id --name-only -r "$c" | grep -q '^evidence/full-review/'; then
    echo "commit $c touches evidence/full-review; refusing (untrack it locally first)"; exit 1
  fi
  git cherry-pick --allow-empty -x "$c" >/dev/null || { echo "cherry-pick failed at $c"; exit 1; }
  echo "$c" > "$MAP"
done
git push origin develop 2>&1 | tail -3
