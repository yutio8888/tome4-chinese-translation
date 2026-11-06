# Build lore-screen batches: lore sections (data/lore/), English source >= 300 chars, ~60K source chars per batch, file order.
import sys, json
from pathlib import Path
sys.path.insert(0, 'tools'); sys.argv = ['x']
import lite_review as L
OUT = Path('evidence/quality/lore-screen-20261105')
us = sorted((u for u in L.units() if '/lore/' in u['occurrence']['section'] and len(u['occurrence']['source']) >= 300), key=L.order_key)
batches, cur, size = [], [], 0
for u in us:
    n = len(u['occurrence']['source'])
    if cur and size + n > 60000:
        batches.append(cur); cur, size = [], 0
    cur.append(u); size += n
if cur: batches.append(cur)
for i, b in enumerate(batches, 1):
    entries = []
    for u in b:
        e = L.entry(u)
        entries.append({k: e[k] for k in ('id', 'section', 'translation_file', 'translation_line', 'source', 'target')})
    (OUT / f'batch-{i:02d}.json').write_text(json.dumps({'batch': f'{i:02d}', 'count': len(entries), 'entries': entries}, ensure_ascii=False, indent=1) + '\n')
print(len(us), 'entries', len(batches), 'batches', [len(b) for b in batches])
