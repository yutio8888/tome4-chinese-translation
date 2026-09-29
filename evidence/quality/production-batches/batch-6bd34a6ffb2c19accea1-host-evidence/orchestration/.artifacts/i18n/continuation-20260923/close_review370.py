import datetime
import hashlib
import json
import pathlib
import shutil
import sqlite3
import subprocess

root = pathlib.Path.cwd()
scratch = root / '.artifacts/i18n/continuation-20260923'
batch = 'batch-6bd34a6ffb2c19accea1'
host = root / 'evidence/quality/production-batches' / f'{batch}-host-evidence'
receipt = json.loads((scratch / 'review370-finalize-timing.json').read_text())
assert receipt['exit_code'] == 0
assert not (root / '.artifacts/i18n/production-review-v2-lite/active-batch.json').exists()
commit = json.loads((scratch / 'review370-evidence-commit.json').read_text())['commit']
db = sqlite3.connect(root / '.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
assert db.execute('select evidence_head from meta').fetchone()[0] == commit
(host / 'FINALIZE-RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
runtime = root / '.artifacts/i18n/production-review-v2-lite/contextual'
assert not runtime.exists()
listing = subprocess.run(['git', 'ls-tree', '--name-only', f'{commit}:evidence/production-review-v2-lite/batches/{batch}/raw/'], text=True, capture_output=True).stdout.split()
assert 'contextual' not in listing, listing
(host / 'RUNTIME-BOUNDARY-RECEIPT.json').write_text(json.dumps(dict(
    evidence_commit=commit, verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    files=[], archived_directory=None, committed_raw_directories=listing,
    reason='Surface-only batch: no entry was deep_required, so no contextual export ran; the contextual runtime path is absent and the committed batch evidence has no raw/contextual directory.'),
    ensure_ascii=False, indent=2) + '\n')
print('FINALIZE_RECEIPT_AND_RUNTIME_BOUNDARY_VERIFIED')
