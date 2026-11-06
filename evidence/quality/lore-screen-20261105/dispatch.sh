# usage: dispatch.sh BATCH  -> runs lane A (Opus 5.5) and B (GPT 6.1 Sol) for one lore-screen batch, waits, validates
set -u -o pipefail
cd /workspace/tome4-chinese-translation
B=$1; D=evidence/quality/lore-screen-20261105
for L in A B; do
  P="长篇 Lore 整体评估 $L（批次 $B）。先完整阅读 $D/reviewer-rules.md，再评估 $D/batch-$B.json 中的全部条目。仓库只读；把结果 JSON 写到 /tmp/lore-screen/$B-$L.json。最终回复只写一行摘要。"
  if [ $L = A ]; then prov=claude/claude-opus-5-5; mode=auto; else prov=codex/gpt-6.1-sol; mode=auto-review; fi
  paseo run -d --title lore-screen-$B-$L --provider $prov --mode $mode --thinking medium "$P" 2>&1 | tail -1 | awk '{print $1}' > /tmp/lore-screen/$B-$L.agent
done
for L in A B; do paseo wait $(cat /tmp/lore-screen/$B-$L.agent) --timeout 5400 >/dev/null 2>&1; done
for L in A B; do
  python3 - $B $L <<'PY'
import json,sys
B,L=sys.argv[1:3]
inp=json.load(open(f'evidence/quality/lore-screen-20261105/batch-{B}.json'))
ids=[e['id'] for e in inp['entries']]
try:
    d=json.load(open(f'/tmp/lore-screen/{B}-{L}.json'))
    got={v['id'][:12]:v for v in d['verdicts']}
    miss=[i for i in ids if i not in got]; bad=[v for v in got.values() if v.get('rating') not in ('OK','LOCAL','RETRANSLATE')]
    if miss or bad: print(f'{B}-{L} INVALID missing={len(miss)} bad={len(bad)}')
    else:
        json.dump({'batch':B,'lane':L,'verdicts':[got[i] for i in ids]},open(f'evidence/quality/lore-screen-20261105/result-{B}-{L}.json','w'),ensure_ascii=False,indent=1)
        import collections; print(f'{B}-{L} OK', dict(collections.Counter(got[i]['rating'] for i in ids)))
except Exception as e: print(f'{B}-{L} INVALID {e}')
PY
done
for L in A B; do paseo archive $(cat /tmp/lore-screen/$B-$L.agent) >/dev/null 2>&1; done
echo DONE-$B
