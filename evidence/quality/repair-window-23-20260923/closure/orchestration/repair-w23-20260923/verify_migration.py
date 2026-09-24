import json,sqlite3
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());base=Path('.artifacts/i18n/repair-window');m=json.loads((base/'window23-20260923-migration.json').read_text());timing=json.loads((base/'window23-20260923-migration-timing.json').read_text());assert timing['success'] and timing['projection_calls']==1
changes=json.loads((P/'CATALOG-CHANGE-VERIFICATION.json').read_text());expected={(r['old_revision'],r['new_revision']) for r in changes['changed']};assert len(m['rows'])==3
assert {(r['old_entry_revision_identity'],r['new_entry_revision_identity']) for r in m['rows']}==expected
assert all(r['disposition']=='revision_changed' and r['reason']=='target_changed' for r in m['rows'])
c=sqlite3.connect('file:.artifacts/i18n/production-review-v2-lite/queue.sqlite3?mode=ro',uri=True);c.row_factory=sqlite3.Row;meta=dict(c.execute('select schema_version,catalog_id,evidence_head,rebuilt_at from meta').fetchone());assert meta['catalog_id']==m['new_catalog_id'];assert meta['evidence_head']==json.loads((P/'TRANSLATION-COMMIT.json').read_text())['translation_commit']
for old,new in expected:assert c.execute('select state from state_override where entry_revision_identity=?',(new,)).fetchone() is None
receipt=dict(verified=True,migration_id=m['migration_id'],revision_changed=3,unchanged=changes['unchanged'],queued_successors=3,ambiguous=0,unmapped=0,projection_calls=1,meta=meta,timing=timing)
(P/'MIGRATION-HOST-VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
