import datetime
import hashlib
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

root = Path.cwd()
batch = 'batch-fddb88b07b599a5e41c8'
tasks = [batch, f'{batch}-contextual-000']
cp = json.loads((root / '.artifacts/i18n/production-review-v2-lite/active-batch.json').read_text())
assert cp['batch_id'] == batch and cp['phase'] == 'commit_ready'
checks = cp['gates']['commands']
assert len(checks) == 17 and all(c['exit_code'] == 0 for c in checks)
for check in checks:
    assert hashlib.sha256((root / check['log_path']).read_bytes()).hexdigest() == check['output_sha256']

host = root / 'evidence/quality/production-batches' / f'{batch}-host-evidence'
assert not host.exists()
snapshot = host / 'orchestration'
files = set()
for task in [batch, *tasks]:
    for section in ('.ai/task', '.ai/reviews'):
        directory = root / section / task
        if directory.exists():
            files.update(p for p in directory.rglob('*') if p.is_file())
prefix = root / '.artifacts/i18n/continuation-20260923'
keep = {'timed_command.py', 'audit_native_tools.py', 'prepare_review298.py',
        'prepare_contextual298.py', 'finalize_host298.py', 'snapshot_review298_current.py',
        'stage_review298_current.py', 'close_review298.py'}
for path in prefix.rglob('*'):
    rel = str(path.relative_to(prefix))
    if (path.is_file() and not path.name.endswith('.pyc') and
            (rel.startswith(('review298', 'captures298/')) or rel in keep) and
            not rel.startswith(('review298-stag', 'review298-evidence-commit',
                                'review298-finalize', 'review298-post-closure',
                                'review298-source-root/'))):
        files.add(path)
files.add(root / 'evidence/quality/production-batches' / f'{batch}-source-workset.json')

for name in ('review298-surface', 'review298-contextual'):
    rows = json.loads((prefix / f'{name}-children.json').read_text())
    for row in rows:
        if row['agent_id'] is None:
            assert row['archive_confirmed'] is False and row.get('output_valid') is None
            continue
        assert row['archive_confirmed'] is True
        assert row['output_valid'] in (True, False)
        for attempt in row['create_attempts']:
            path = root / attempt['profiles_path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == attempt['profiles_sha256']
            files.add(path)

manifest = []
for path in sorted(files):
    assert not path.is_symlink()
    rel = path.relative_to(root)
    data = path.read_bytes()
    target = snapshot / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    assert target.read_bytes() == data
    manifest.append(dict(path=str(rel), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
(host / 'snapshot-inventory.json').write_text(json.dumps(dict(files=manifest), ensure_ascii=False, indent=2) + '\n')

replay = []
for task in tasks:
    result = subprocess.run(['python3', '-B', 'tools/ai_state_check.py',
                             str(snapshot / '.ai/task' / task / 'STATE.json'),
                             '--target', 'DONE', '--workspace-root', str(snapshot)],
                            text=True, capture_output=True)
    replay.append(dict(task=task, exit_code=result.returncode, output=result.stdout + result.stderr))
    assert result.returncode == 0, (task, result.stdout, result.stderr)
(host / 'SNAPSHOT-REPLAY.json').write_text(json.dumps(replay, ensure_ascii=False, indent=2) + '\n')

src = root / '.artifacts/i18n/production-review-v2-lite/prospective/evidence/production-review-v2-lite/batches' / batch
dst = root / 'evidence/production-review-v2-lite/batches' / batch
assert src.is_dir() and not dst.exists()
items = []
for path in sorted(src.rglob('*')):
    if path.is_file():
        assert not path.is_symlink()
        rel = path.relative_to(src)
        data = path.read_bytes()
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        assert target.read_bytes() == data
        items.append(dict(path=str(target.relative_to(root)), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
counts = Counter(json.loads(line)['final_state'] for line in (dst / 'results.jsonl').read_text().splitlines())
expected = json.loads((root / '.ai/task' / batch / 'HOST-FINAL-DECISIONS.json').read_text())['expected_final_states']
assert counts == {key: value for key, value in expected.items() if value}, counts
(host / 'PRODUCTION-COMMIT-READY.json').write_text(json.dumps(dict(
    batch_id=batch, base_commit=cp['base_commit'], phase=cp['phase'], checks=checks,
    production_files=items, installed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    selected=80, final_states=dict(counts), supplemental_repair_revisions=0),
    ensure_ascii=False, indent=2) + '\n')
shutil.copyfile(root / '.artifacts/i18n/adjudication-chain/review298-20260926-attempt01.json',
                host / 'PRODUCTION-CHAIN.json')
shutil.copyfile(root / '.ai/task' / batch / 'HOST-SUMMARY.md', host / 'summary.md')
for item in manifest:
    assert hashlib.sha256((snapshot / item['path']).read_bytes()).hexdigest() == item['sha256']
print(json.dumps(dict(snapshot_files=len(manifest), snapshot_bytes=sum(i['bytes'] for i in manifest),
                      production_files=len(items), gates=len(checks), results=dict(counts),
                      replay=[(r['task'], r['exit_code']) for r in replay]), ensure_ascii=False))
