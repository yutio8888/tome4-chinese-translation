import sys,json,sqlite3,subprocess,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
n=int(sys.argv[1]);assert n in (2,3)
assert not Path('.artifacts/i18n/production-review-v2-lite/active-batch.json').exists()
timing=Path(f'.artifacts/i18n/repair-window/window7-20260922-queue-{n}-timing.json')
t=json.loads(timing.read_text());assert t['exit_code']==0
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/develop'],text=True).split()[0]
assert head==remote
c=sqlite3.connect('file:.artifacts/i18n/production-review-v2-lite/queue.sqlite3?mode=ro',uri=True);c.row_factory=sqlite3.Row
meta=dict(c.execute('select schema_version,catalog_id,evidence_head,rebuilt_at from meta').fetchone());assert meta['evidence_head']==head
catalog=Path('evidence/production-review-v2-lite/catalog');manifest=json.loads((catalog/'manifest.json').read_text())
assert manifest['catalog_id']==meta['catalog_id'];raw=(catalog/'entries.jsonl').read_bytes();assert hashlib.sha256(raw).hexdigest()==manifest['entries_sha256']
entries={r['entry_revision_identity'] for r in map(json.loads,raw.decode().splitlines())};assert len(entries)==manifest['entry_count']
states={r['entry_revision_identity']:r['state'] for r in c.execute('select entry_revision_identity,state from state_override')};assert set(states)<=entries
changes=json.loads((P/'CATALOG-CHANGE-VERIFICATION.json').read_text())['changed'];successors=[r['new_revision'] for r in changes]
assert len(successors)==8 and all(k in entries and k not in states for k in successors)
counts={r['state']:r['n'] for r in c.execute('select state,count(*) n from state_override group by state')}
assert not any(counts.get(k,0) for k in ('reserved','screened','deep_required'))
out=dict(verified=True,verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=head,remote_head=remote,sqlite_evidence_head=meta['evidence_head'],catalog_id=meta['catalog_id'],queue_receipt_path=str(timing),counts=counts,queued=len(entries)-len(states),successors_verified_queued=8,successors=successors,meta=meta,continuation_policy='pause_after_window7',next_batch_requires_new_user_authorization=True)
path=P/('PUBLICATION-CLOSURE.json' if n==2 else 'FINAL-PUSH-VERIFICATION.json');assert not path.exists();path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
