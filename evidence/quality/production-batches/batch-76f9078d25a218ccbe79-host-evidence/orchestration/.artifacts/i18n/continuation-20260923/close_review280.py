import datetime
import hashlib
import json
import pathlib
import shutil
import sqlite3
import subprocess

root = pathlib.Path.cwd()
scratch = root / '.artifacts/i18n/continuation-20260923'
batch = 'batch-76f9078d25a218ccbe79'
host = root / 'evidence/quality/production-batches' / f'{batch}-host-evidence'
receipt = json.loads((scratch / 'review280-finalize-timing.json').read_text())
assert receipt['exit_code'] == 0
assert not (root / '.artifacts/i18n/production-review-v2-lite/active-batch.json').exists()
commit = json.loads((scratch / 'review280-evidence-commit.json').read_text())['commit']
db = sqlite3.connect(root / '.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
assert db.execute('select evidence_head from meta').fetchone()[0] == commit
(host / 'FINALIZE-RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
runtime = root / '.artifacts/i18n/production-review-v2-lite/contextual'
proof = []
for index, run in ((4, '000'),):
    for kind in ('input', 'output'):
        name = f'run-{run}-{kind}.json'
        path = runtime / name
        committed = f'evidence/production-review-v2-lite/batches/{batch}/raw/contextual/{index:03d}-{kind}_path.json'
        raw = subprocess.check_output(['git', 'show', f'{commit}:{committed}'])
        assert raw == path.read_bytes(), (run, kind)
        proof.append(dict(runtime_path=str(path.relative_to(root)), committed_path=committed,
                          sha256=hashlib.sha256(raw).hexdigest()))
archive = root / '.artifacts/i18n/production-review-v2-lite/finalized-runtime-scratch' / f'{batch}-contextual'
assert not archive.exists()
shutil.move(runtime, archive)
(host / 'RUNTIME-BOUNDARY-RECEIPT.json').write_text(json.dumps(dict(
    evidence_commit=commit, verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    files=proof, archived_directory=str(archive),
    reason='Preserve finalized runtime bytes while clearing the next contextual export path.'),
    ensure_ascii=False, indent=2) + '\n')
print('FINALIZE_RECEIPT_AND_RUNTIME_BOUNDARY_VERIFIED')
