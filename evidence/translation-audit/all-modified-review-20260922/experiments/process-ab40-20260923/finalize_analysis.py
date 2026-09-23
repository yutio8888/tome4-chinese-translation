"""Validate the bounded research run and prepare transparent comparison details."""
import ast, collections, datetime, hashlib, json, re
from pathlib import Path

P = Path(__file__).resolve().parent
ROOT = next(q for q in P.parents if (q / 'AGENTS.md').exists())

def read(name):
    return json.loads((P / name).read_text())

def write(name, data):
    (P / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def main():
    d, scores, state = read('ADJUDICATION.json'), read('SCORES.json'), read('STATE.json')
    refs = {c['id']: c for c in d['canonical']}
    old = read('HOST-DISCOVERY-REFERENCE.json')
    old_refs = {c['id']: c for c in old['canonical']}
    changes = [{ 'id': k, 'before': old_refs[k]['status'], 'after': c['status'] }
               for k,c in refs.items() if k in old_refs and old_refs[k]['status'] != c['status']]
    write('POST-B3-REFERENCE-CHANGES.json', {
        'existing_status_changes': changes,
        'new_confirmed': [k for k,c in refs.items() if k not in old_refs and c['status']=='confirmed'],
        'new_nonconfirmed': [k for k,c in refs.items() if k not in old_refs and c['status']!='confirmed'],
        'reason': 'N88 is the specific 的/得 typo already mentioned as B2 advisory and promoted by B3. Other additions document rebutted layout/wording assertions. No previous confirmed/pending/advisory status changed after B3.',
        'normalization': 'B2 C33 and C63 side assertions are split identically to B3 K37 and K66. Additional B2 unnumbered advisory observations receive U20–U43; this changes traceability, not B2 confirmed coverage.'
    })
    expected = [x['audit_id'] for x in read('entries.json')]
    checks = {}
    for stage in ['P','A2','B2','B3']:
        text = (P / f'reports/{stage}.md').read_text()
        actual = re.findall(r'^\|\s*(?:\d+\s*\|\s*)?(entry-\d+)\s*\|', text, re.M)
        wanted = [x['audit_id'] for x in read('targeted-entries.json')] if stage=='B2' else expected
        assert actual == wanted, (stage, actual)
        checks[stage] = {'entry_table_count': len(actual), 'order_matches': True}
    for stage,n in [('P',18),('A2',57),('B2',80)]:
        mapped = {o['id'].split('.')[0] for o in d['observations'] if o['stage']==stage}
        missing = sorted({f'C{i:02d}' for i in range(1,n+1)} - mapped)
        assert not missing, (stage, missing)
        checks[stage]['numbered_claims_mapped'] = n
    for prefix,n in [('K',83),('U',38),('NEW',7)]:
        mapped={o['id'].split('.')[0] for o in d['observations'] if o['stage']=='B3'}
        assert {f'{prefix}{i:02d}' for i in range(1,n+1)} <= mapped
        checks['B3'][prefix+'_mapped'] = n
    text=(P/'reports/B3.md').read_text()
    incoming=re.findall(r'^\| (P:C\d+(?:\.\d+)?|B2:C\d+(?:\.\d+)?) \|',text,re.M)
    assert {x.split('.')[0] for x in incoming} == {f'P:C{i:02d}' for i in range(1,19)} | {f'B2:C{i:02d}' for i in range(1,81)}
    write('B3-INCOMING-MAPPING.json', {
        'rows': [line for line in text.splitlines() if re.match(r'^\| (P:C|B2:C)',line)],
        'complete_numbered_parent_ids': 98,
        'issues': [
            'B3 P:C06.2 refutes a supposed smoke-palace allegation that is not an actual P:C06 claim; not credited as removal of a real P false positive.',
            'K11 is advisory in part of the incoming table but confirmed in the deduplicated table and B2:C24 mapping; final deduplicated confirmed status used. Advisory treatment would reduce B false clusters by one and not change the decision.',
            'K55 has advisory/pending mixed labels; use pending and do not count a confirmed finding.',
            'B3 says eight source files but its final list contains sixteen; the self-reported count is inconsistent.',
            'B3 interpreted the other-experiment prohibition as excluding source-access-authorized extra source snapshots. This limits evidentiary closure; do not claim exhaustive source verification.'
        ]
    })
    pre,post=scores['results']['B_before_verification'],scores['results']['B']
    tp0,tp1=set(pre['supported_reference_claims']),set(post['supported_reference_claims'])
    fp0,fp1=set(pre['unsupported_distinct_clusters']),set(post['unsupported_distinct_clusters'])
    write('VERIFIER-EFFECT.json',{
        'supported_retained':sorted(tp0 & tp1), 'supported_removed':sorted(tp0-tp1),
        'supported_promoted_or_new':sorted(tp1-tp0),
        'unsupported_removed':sorted(fp0-fp1), 'unsupported_added':sorted(fp1-fp0),
        'NEW_accepted_reference':['H01'],
        'NEW_note':'NEW01 recovers an existing host/A2 reference, not a new gold defect. NEW02/03/04/06/07 are unsupported confirmed; NEW05 remains advisory/pending.',
        'entry_level_note':'A and B both cover the same twelve reference ISSUE entries; atomic coverage differences concentrate within long narratives.'
    })
    before=read('DISCOVERY-NEGATIVE-AUDIT.json')
    final_entries=[]
    for e in expected:
        items=[x for x in refs.values() if x['entry']==e]
        cs=[x['id'] for x in items if x['status']=='confirmed']
        ps=[x['id'] for x in items if x['status']=='pending']
        final_entries.append({'entry':e,'status':'ISSUE' if cs else 'PENDING' if ps else 'OK', 'confirmed':cs,'pending':ps})
    write('FINAL-ENTRY-RESULTS.json',final_entries)
    neg=set(expected)-set(scores['results']['A']['issue_entries_found'])-set(post['issue_entries_found'])
    write('FINAL-NEGATIVE-AUDIT.json',{
        'final_neither_arm_supported_issue_entries':sorted(neg),
        'method':'All forty pairs were independently read before report revelation. Seventeen all-discovery-negative entries were reread (DISCOVERY-NEGATIVE-AUDIT.json). Other final negative entries arose from adjudicating reported candidates against full context; no negative entry was inferred merely from a model OK label.',
        'new_confirmed_after_B3':'N88 is inside an already positive long narrative; none in final joint negatives.',
        'pending_preserved':[e for e in final_entries if e['status']=='PENDING'],
        'discovery_audit_artifact':'DISCOVERY-NEGATIVE-AUDIT.json'
    })
    integrity={}
    for name,key,root in [('BASELINE.json','hashes',ROOT),('FREEZE.json','files_sha256',P),('B3-FREEZE.json','files_sha256',P)]:
        vals=read(name)[key];bad=[f for f,h in vals.items() if not (root/f).exists() or hashlib.sha256((root/f).read_bytes()).hexdigest()!=h]
        assert not bad,(name,bad)
        integrity[name]={'count':len(vals),'mismatch':bad}
    for name in ['SCORING-FREEZE.json','HOST-DISCOVERY-FREEZE.json']:
        f=read(name);assert hashlib.sha256((P/f['file']).read_bytes()).hexdigest()==f['sha256'];integrity[name]=True
    initial=read('HOST-INITIAL-FREEZE.json')
    assert hashlib.sha256((P/'HOST-INITIAL.json').read_bytes()).hexdigest()==initial['sha256']
    assert hashlib.sha256((P/'host_initial.py').read_bytes()).hexdigest()==initial['script_sha256']
    integrity['HOST-INITIAL-FREEZE.json']=True
    for f in P.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
    for child in state['child_dispatches']:
        stage=child['stage'];a=read(f'dispatches/archived-status-{stage}.json')['structuredContent']['snapshot']
        t=read(f'dispatches/terminal-{stage}.json')['structuredContent']['snapshot']
        assert child['archive_confirmed'] and a['archivedAt'] and t['activeTurn'] is None
        assert t['runtimeInfo']['model'] == ('gpt-5.6-sol' if stage=='P' else 'claude-opus-5')
    write('FINAL-VALIDATION.json',{
        'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'report_coverage':checks,'integrity':integrity,'scripts_ast_parse':True,
        'all_four_children_archived':True,'production_files_changed_by_experiment':False,
        'validation_scope':'Research artifacts, immutable baseline/input/reference/scorer hashes, report coverage and lifecycle. No translation changes; production Lua lint/build/contract DONE gates are not applicable.'
    })
    print({'reference':collections.Counter(x['status'] for x in refs.values()),'validation':'passed'})

if __name__=='__main__':main()
