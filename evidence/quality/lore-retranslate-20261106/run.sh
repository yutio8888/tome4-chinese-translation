#!/bin/bash
set -u -o pipefail
cd /tmp/gem-lore
for k in ${RUN_IDS}; do
  [ -s $k/out.txt ] && { echo "SKIP $k"; continue; }
  id=$(paseo run -d --title gem-lore-$k --provider antigravity --model gemini-4-argon --mode dangerously-skip-permissions --new-workspace local --cwd /tmp/gem-lore/$k "请完整阅读 /tmp/gem-lore/$k/prompt.md 并按其执行。" 2>&1 | grep -v -e UNDICI -e trace | tail -1 | awk '{print $1}')
  echo "$(date +%T) START $k $id"
  paseo wait $id --timeout 3600 >/dev/null 2>&1; echo "$(date +%T) WAIT-RC $? $k"
  if [ -s $k/out.txt ]; then echo "OUT $k nl=$(grep -c '' $k/out.txt) src_nl=$(grep -c '' $k/source.txt)"; else echo "NO-OUT $k"; fi
  echo $id > $k/agent.id
done
echo ALL-DONE
