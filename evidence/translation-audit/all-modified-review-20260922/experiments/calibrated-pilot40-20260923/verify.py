"""Bounded research integrity checks, not production DONE_VERIFIED."""
import hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    guard=read(R/'BASELINE-GUARD.json')
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==guard['head']
    for p,h in guard['prior_files_sha256'].items(): assert sha(R.parent.parent/p)==h,p
    for p,h in guard['production_sha256'].items(): assert sha(Path(p))==h,p
    freeze=read(R/'FREEZE.json')
    for p,h in freeze['files_sha256'].items(): assert sha(R/p)==h,p
    h=read(R/'HOST-INITIAL-FREEZE.json');assert sha(R/h['file'])==h['sha256']
    entries=read(R/'entries.json');ids=[e['audit_id'] for e in entries]
    assert len(ids)==len(set(ids))==40
    assert all(i in read(R/'SAMPLING-PREREG.json')['frame_ids'] for i in ids)
    final=R/'RESULT.json'
    if final.exists():
        result=read(final);assert [e['entry_id'] for e in result['entries']]==ids
        assert set(c['entry_id'] for c in result['confirmed_claims']).issubset(ids)
        state=read(R/'STATE.json');assert len(state['child_dispatches'])==2
        for child in state['child_dispatches']:
            assert child['archive_confirmed']
            assert child['table_coverage_valid']
    print(json.dumps({'integrity':'pass','frozen_entries':40,'prior_files_unchanged':len(guard['prior_files_sha256']),'production_files_unchanged':len(guard['production_sha256']),'production_completion_claimed':False}))
if __name__=='__main__':main()
