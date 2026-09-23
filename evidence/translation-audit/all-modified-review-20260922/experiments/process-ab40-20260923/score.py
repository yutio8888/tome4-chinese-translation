"""Score frozen observations against a provisional host reference, not human gold."""
import json
from pathlib import Path

P=Path(__file__).resolve().parent

def main():
    data=json.loads((P/'ADJUDICATION.json').read_text())
    reference={c['id']:c for c in data['canonical']}
    confirmed={k for k,c in reference.items() if c['status']=='confirmed'}
    impact={k for k in confirmed if reference[k]['impact']=='机制/操作'}
    observations=data['observations']
    seen=set()
    for o in observations:
        key=(o['stage'],o['id']);assert key not in seen,key;seen.add(key)
        assert o['source_status'] in {'confirmed','pending','advisory','refuted'}
        assert o['host_decision'] in {'accepted','pending','refuted','advisory'}
        assert all(k in reference for k in o['canonical'])
    def score(stages):
        candidates=[o for o in observations if o['stage'] in stages and o['source_status']=='confirmed']
        covered={k for o in candidates for k in o['canonical'] if k in confirmed}
        unsupported=[o for o in candidates if o['host_decision']=='refuted']
        unresolved=[o for o in candidates if o['host_decision']=='pending']
        missed=confirmed-covered
        return {'stages':stages,'confirmed_observation_units':len(candidates),'supported_reference_claims':sorted(covered),'coverage_count':len(covered),'reference_confirmed_count':len(confirmed),'reference_coverage':len(covered)/len(confirmed) if confirmed else None,'unsupported_confirmed_units':[o['stage']+':'+o['id'] for o in unsupported],'unsupported_distinct_clusters':sorted({o['false_cluster'] for o in unsupported}),'pending_confirmed_units':[o['stage']+':'+o['id'] for o in unresolved],'missed_reference_claims':sorted(missed),'missed_mechanism_operation_claims':sorted(missed & impact),'issue_entries_found':sorted({reference[k]['entry'] for k in covered})}
    results={name:score(stages) for name,stages in [('shared_primary',['P']),('A',['P','A2']),('B_before_verification',['P','B2']),('B',['B3'])]}
    assert set(data['entries'])=={e['audit_id'] for e in json.loads((P/'entries.json').read_text())}
    a=results['A'];b=results['B']
    result={'reference_status':'provisional host-adjudicated set, not human gold','atomic_unit_rule':'Independent meaning changes; related duplicates and repeated conditional-branch instances are merged consistently for every stage. Compound source claims may be split into explicit subunits retaining original IDs.','results':results,'paired_differences':{'B_only':sorted(set(b['supported_reference_claims'])-set(a['supported_reference_claims'])),'A_only':sorted(set(a['supported_reference_claims'])-set(b['supported_reference_claims']))},'quality_candidate_conditions':{'coverage_not_lower':b['coverage_count']>=a['coverage_count'],'unsupported_not_more':len(b['unsupported_distinct_clusters'])<=len(a['unsupported_distinct_clusters']),'mechanism_misses_not_more':len(b['missed_mechanism_operation_claims'])<=len(a['missed_mechanism_operation_claims'])},'resource_condition':'See resource report; missing cost or unmatched usage prevents a near-cost superiority claim.'}
    (P/'SCORES.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({k:(v['coverage_count'],len(v['unsupported_distinct_clusters'])) for k,v in results.items()})

if __name__=='__main__':main()
