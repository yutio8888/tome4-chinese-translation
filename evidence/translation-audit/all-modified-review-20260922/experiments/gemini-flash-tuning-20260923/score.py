"""Score host-adjudicated atomic mappings, never infer correctness from agreement.
Input: reference claims(id,entry,status,impact), mappings(reference_ids, verdict,
atom_id, model_status), run metadata(valid, cost, seconds, evidence_checks).
Pending reference IDs are excluded from TP/FP. Nonconfirmed model candidates
are reported separately and cannot count as confirmed detection.
"""
import json,sys

def score(reference, mappings, meta):
    refs={r['id']:r for r in reference if r['status']=='confirmed'}
    pending={r['id'] for r in reference if r['status']=='pending'}
    found=set(); fp=set(); supported_new=set()
    for m in mappings:
        if m['model_status']!='confirmed': continue
        ids=set(m.get('reference_ids',[]))
        if m['verdict']=='supported':
            found |= ids & refs.keys()
            if not ids: supported_new.add(m['atom_id'])
        elif m['verdict']=='unsupported' and not ids & pending:
            fp.add(m['atom_id'])
    groups={r['entry'] for r in refs.values()}
    cov=[sum(i in found for i,r in refs.items() if r['entry']==e)/sum(r['entry']==e for r in refs.values()) for e in groups]
    mechanisms={i for i,r in refs.items() if r.get('impact') in ('mechanism','机制/操作')}
    checks=meta.get('evidence_checks',[])
    return dict(valid=meta['valid'],reference_confirmed=len(refs),detected=len(found),micro=len(found)/len(refs) if refs else None,macro=sum(cov)/len(cov) if cov else None,false_positive=len(fp),mechanism_missed=len(mechanisms-found),novel_supported=len(supported_new),candidates=len(mappings),pending=sum(m['model_status']=='pending' for m in mappings),evidence_valid_rate=sum(checks)/len(checks) if checks else None,cost=meta.get('cost'),seconds=meta.get('seconds'))

if __name__=='__main__':
    data=json.load(open(sys.argv[1]));print(json.dumps(score(data['reference'],data['mappings'],data['meta']),ensure_ascii=False,indent=2))
