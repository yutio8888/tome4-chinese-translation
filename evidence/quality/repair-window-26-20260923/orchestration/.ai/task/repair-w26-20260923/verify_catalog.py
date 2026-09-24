import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());base=Path('.artifacts/i18n/repair-window/window26-20260923-candidate-catalog');rel=Path('evidence/production-review-v2-lite/catalog/entries.jsonl')
def load(path):return {r['logical_entry_identity']:r for r in map(json.loads,path.read_text().splitlines())}
a=load(rel);b=load(base/rel);assert a.keys()==b.keys();work=json.loads((P/'WORKSET.json').read_text())['items'];allowed={i['entry_revision_identity'] for i in work};changed=[]
for key,x in a.items():
 y=b[key]
 if x['entry_revision_identity']==y['entry_revision_identity']:continue
 assert x['entry_revision_identity'] in allowed
 for field in ('source','section','source_tag','args_order','fixed_source_identity','call_locator','rules_version'):assert x.get(field)==y.get(field),field
 assert x['target']!=y['target']
 changed.append(dict(logical_entry_identity=key,old_revision=x['entry_revision_identity'],new_revision=y['entry_revision_identity'],old_target_sha256=x['target_sha256'],new_target_sha256=y['target_sha256']))
assert {r['old_revision'] for r in changed}==allowed and len(changed)==5
receipt=dict(verified=True,entries=len(a),revision_changed=5,unchanged=len(a)-5,workset_exact_match=True,changed=changed)
(P/'CATALOG-CHANGE-VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
