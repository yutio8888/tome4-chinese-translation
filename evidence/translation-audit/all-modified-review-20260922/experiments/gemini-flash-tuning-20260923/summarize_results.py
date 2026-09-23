"""Summarize frozen scoring outputs without changing references or selection."""
import json
import pathlib
import runpy
import statistics

p = pathlib.Path(__file__).parent
score = runpy.run_path(str(p / 'score.py'))['score']
selection = json.loads((p / 'SELECTION.json').read_text())
holdout = {}
for arm in ['F00', 'F11']:
    runs = []
    for rep in [1, 2]:
        name = f'holdout-{arm}-r{rep}'
        d = json.loads((p / f'normalized/{name}-mapped.json').read_text())
        s = score(d['reference'], d['mappings'], d['meta'])
        confirmed = {r['id'] for r in d['reference'] if r['status'] == 'confirmed'}
        noticed = set()
        for m in d['mappings']:
            if m['verdict'] == 'supported':
                noticed.update(set(m.get('reference_ids', [])) & confirmed)
        s.update(run=name, candidate_detected_including_advisory=len(noticed))
        runs.append(s)
    mean = {k: statistics.mean(r[k] for r in runs) for k in
            ['macro', 'micro', 'false_positive', 'mechanism_missed', 'seconds',
             'candidates', 'candidate_detected_including_advisory']}
    holdout[arm] = dict(runs=runs, mean=mean, both_raw_valid=all(r['valid'] for r in runs))
b, c = holdout['F00']['mean'], holdout['F11']['mean']
gates = dict(
    both_raw_valid=holdout['F11']['both_raw_valid'],
    false_positive_not_worse=c['false_positive'] <= b['false_positive'],
    false_positive_density=c['false_positive'] <= 2.4,
    macro_within_margin=c['macro'] >= b['macro'] - .05,
    mechanism_misses_not_worse=c['mechanism_missed'] <= b['mechanism_missed'],
    any_strict_improvement=(c['macro'] > b['macro'] or any(
        c[k] < b[k] for k in ['false_positive', 'mechanism_missed', 'seconds'])),
)
result = dict(development=selection['results'], selected='F11', holdout=holdout,
              relative_gates=gates, relative_gate_pass=all(gates.values()),
              cost_winner=None, token_usage=None,
              reference_status='Provisional host-adjudicated reference, not human gold.',
              promotion='No demonstrated holdout detection gain; do not use OK as acceptance.',
              warning='Relative noninferiority can pass with zero absolute coverage. No population accuracy inference.')
(p / 'RESULTS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(holdout=holdout, relative_gates=gates), ensure_ascii=False, indent=2))
