"""Verify calibration inputs and preservation of previous evidence."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):
    return json.loads((HERE / name).read_text())

provenance = read('PROVENANCE.json')
baseline = read('BASELINE-GUARD.json')
changed = [p for p, h in baseline.items() if not (ROOT / p).is_file() or sha(ROOT / p) != h]
assert not changed, changed
for name, h in provenance['blind_file_hashes'].items():
    assert sha(HERE / 'blind' / name) == h, name
entries = read('blind/entries.json')
mapping = read('HOST-MAPPING.json')
assert len(entries) == len(mapping) == 10
assert {e['id'] for e in entries} == {f'K{i:02}' for i in range(1, 11)}
allowed = {'source', 'target', 'section', 'source_tag', 'args_order', 'special', 'component', 'occurrence', 'id', 'context_file', 'source_file'}
for e, m in zip(entries, mapping):
    assert set(e) == allowed
    assert e['id'] == m['id']
    p = HERE.parent / f"abc20-g{m['group']:02}-20260923" / 'entries.json'
    old = next(x for x in json.loads(p.read_text()) if x['audit_id'] == m['entry_id'])
    for key in allowed - {'id', 'context_file', 'source_file'}:
        assert e[key] == old.get(key), (e['id'], key)
result = {'entries': 10, 'input_identity_matches': True, 'blind_hashes_match': True,
          'protected_files': len(baseline), 'protected_files_changed': changed,
          'scope': '10-entry calibration only; previous reports, production files and rules preserved'}
(HERE / 'VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
