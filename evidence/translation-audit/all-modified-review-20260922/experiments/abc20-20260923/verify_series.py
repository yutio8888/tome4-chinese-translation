"""Read-only mechanical verification; --complete requires the current user-authorized scope."""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path
import series

def main():
    state = series.read(series.SERIES / 'STATE.json')
    target = state.get('target_groups',20)
    assert state['target_entries']==target*40
    identities = [e for g in state['groups'] for e in g['entry_ids']]
    assert len(identities) == len(set(identities)) == 800
    assert len(state['groups']) == 20
    results = []
    for g in state['groups']:
        root = series.SERIES.parent / g['directory']
        entries = series.read(root / 'entries.json')
        assert [e['audit_id'] for e in entries] == g['entry_ids']
        assert len(entries) == 40
        if g.get('legacy'):
            results.append({'group': g['index'], 'legacy': True, 'state': g['state']})
            continue
        series.module(root, 'record').guards()
        current = series.read(root / 'STATE.json')
        if g['index']>target:
            assert not current['child_dispatches'] and current['state']=='FROZEN'
            assert g['state']=='FROZEN_NOT_RUN'
            results.append({'group':g['index'],'state':'FROZEN_NOT_RUN'})
            continue
        if current['state'] != 'DONE_research_only':
            results.append({'group': g['index'], 'state': current['state']})
            continue
        assert all(c['archive_confirmed'] and c['lineage_verified'] for c in current['child_dispatches'])
        selection = series.read(root / 'SELECTION.json') if (root / 'SELECTION.json').exists() else {}
        selected = {selection.get(a, a + '-01') for a in ('opus', 'sol', 'gemini')}
        arms = [c for c in current['child_dispatches'] if c['dispatch_id'] in selected]
        assert len(arms) == 3
        assert len({(c['prompt_sha256'], c['input_sha256']) for c in arms}) == 1
        expected_gemini = current.get('gemini_transport_decision', {}).get('provider', 'antigravity/gemini-3.8-flash')
        assert expected_gemini in {'pi/cpa/gemini-3.8-flash-high','antigravity/gemini-3.8-flash'}
        assert {c['requested_provider'] for c in arms} == {
            'claude/claude-opus-5-5', 'codex/gpt-6-sol', expected_gemini}
        assert all(c['requested_settings']['thinkingOptionId'] == 'high' for c in arms)
        for c in current['child_dispatches']:
            report = root / 'reports' / (c['dispatch_id'] + '.md')
            assert series.sha(report) == c['report_sha256']
            if not c.get('excluded') and c['dispatch_id'] != 'adjudication-01':
                text = report.read_text()
                table = '\n'.join(l for l in text.splitlines() if re.match(r'^\|\s*entry-\d+',l))
                required = series.cited_claims(table)
                available = set(re.findall(r'^###\s+(C\d+)',text,re.M))
                assert required <= available, (report, required-available)
        mapping = series.read(root / 'ANON-MAPPING-HOST-ONLY.json')
        for o in mapping['observations']:
            p = root / 'reports' / (o['origin'] + '.md')
            assert series.sha(p) == o['source_sha256']
            assert p.read_text()[o['start']:o['end']] == o['text']
        freeze = series.read(root / 'ADJUDICATION-FREEZE.json')
        assert series.sha(root / 'ADJUDICATION-INPUT.md') == freeze['input_sha256']
        assert series.sha(root / 'ANON-MAPPING-HOST-ONLY.json') == freeze['mapping_sha256']
        assert series.sha(root / 'reports/reference-blind-01.md') == freeze['blind_report_sha256']
        metrics = series.module(root, 'score').score(series.read(root / 'SCORING.json'))
        assert metrics == series.read(root / 'METRICS.json')
        scoring = series.read(root / 'SCORING.json')
        for entry in scoring['entries']:
            for arm in entry['arms'].values():
                earned = {d for o in arm['observations'] if o['original_assertion'] == 'ISSUE'
                          for d in o['adjudication']['defects']}
                assert earned == set(arm['confirmed_defects'])
        results.append({'group': g['index'], 'state': 'DONE', 'replay_identical': True,
                        'observations': len(mapping['observations']), 'children_archived': len(current['child_dispatches'])})
    completed = sum(g['state'] == 'DONE' for g in results)
    assert completed == state['completed_groups']
    if '--complete' in sys.argv:
        assert completed == target and state['state'] == 'DONE_research_only'
        assert all(g['state']=='DONE' for g in results if g['group']<=target)
    print(json.dumps({'completed': completed, 'target_groups':target, 'reviewed_entries':completed*40, 'frozen_unique_entries':800, 'groups': results}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
