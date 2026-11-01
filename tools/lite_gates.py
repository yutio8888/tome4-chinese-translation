"""Gate selection for lightweight review commits (2026-11-01 user approval; docs/lite-review-workflow-20261101.md).

A commit that changes only translation data runs the translation checks of the verification matrix
(docs/agent-workflow.md "有界译文修改"): doctor, strict lint, semantic-claims registry, runtime-key scan and
classification, terminology audits, domain annotation, whitespace and the strict core addon build (about 5 s).
The full tools/ci-gates.sh (tool unit tests included, about 170 s) runs instead when
  - a pending change touches anything outside TRANSLATION_PATHS, or
  - tools/, tests/ or i18n/ differ from the tree recorded at the last full PASS, or
  - FULL_EVERY batches have passed since the last full PASS, or --full is given.

usage: tools/lite_gates.py BATCH [--full]      writes evidence/lite-review/batches/BATCH/gates.json
       tools/lite_gates.py BATCH --mark        after committing a batch whose full run passed, record HEAD's
                                               tools/tests/i18n trees in full-gates.json
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LITE = ROOT / 'evidence/lite-review'
STATE = LITE / 'full-gates.json'          # last full PASS: batch, commit, trees
FULL_EVERY = 10
TRANSLATION_PATHS = (re.compile(r'[^/]+\.lua'), re.compile(r'terminology/[^/]+\.tsv'), re.compile(r'evidence/lite-review/.+'))
TOOL_TREES = ('tools', 'tests', 'i18n')
PY = ['python3', '-B']
SUBSET = [
    ('01-doctor', PY + ['tools/i18n', 'doctor']),
    ('02-strict-lint', PY + ['tools/i18n', 'lint', '--strict']),
    ('04-semantic-claims-strict-registry', PY + ['tools/i18n', 'claims', 'check', '--registry',
                                                 'evidence/quality/semantic-claim-regressions-v1.json', '--strict']),
    ('06-runtime-collision-scan', PY + ['tools/scan_runtime_collisions.py']),
    ('07-runtime-key-classification', PY + ['tools/classify_runtime_keys.py']),
    ('08-terminology-static-audit', PY + ['tools/audit_static.py']),
    ('09-terminology-dynamic-audit', PY + ['tools/audit_dynamic.py']),
    ('10-domain-annotation', PY + ['tools/annotate_domains.py']),
    ('11-worktree-whitespace', ['git', 'diff', '--check']),
    ('11-staged-whitespace', ['git', 'diff', '--cached', '--check']),
    ('12-core-addon-build', PY + ['tools/i18n', 'build', '--profile', 'addon', '--component', 'tome', '--require-complete']),
]


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_paths():
    out = git('status', '--porcelain', '--untracked-files=all', '-z')
    paths, items = [], out.split('\0')
    i = 0
    while i < len(items):
        rec = items[i]
        if not rec:
            i += 1
            continue
        status, path = rec[:2], rec[3:]
        paths.append(path)
        if 'R' in status or 'C' in status:      # rename/copy: the next field is the source path
            i += 1
            paths.append(items[i])
        i += 1
    # untracked .adapter.lock files of the frozen full-review rounds are not part of any commit
    return [p for p in paths if not p.endswith('/.adapter.lock')]


def trees():
    return {t: git('rev-parse', f'HEAD:{t}').strip() for t in TOOL_TREES}


def decide(batch, force):
    reasons = []
    if force:
        reasons.append('--full requested')
    other = [p for p in changed_paths() if not any(r.fullmatch(p) for r in TRANSLATION_PATHS)]
    if other:
        reasons.append(f'non-translation changes: {other[:8]}')
    state = json.loads(STATE.read_text()) if STATE.exists() else None
    if state is None:
        reasons.append('no recorded full PASS')
    else:
        if state['trees'] != trees():
            reasons.append('tools/tests/i18n changed since the last full PASS')
        if int(batch) - int(state['batch']) >= FULL_EVERY:
            reasons.append(f'{FULL_EVERY} batches since the last full PASS ({state["batch"]})')
    return reasons


def run_subset():
    results, ok = [], True
    for name, argv in SUBSET:
        t = time.time()
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        results.append({'check': name, 'argv': argv, 'exit_code': r.returncode, 'seconds': round(time.time() - t, 2),
                        'tail': (r.stdout + r.stderr)[-600:] if r.returncode else ''})
        print(f"{'PASS' if r.returncode == 0 else 'FAIL'}  {name} ({results[-1]['seconds']} s)")
        ok = ok and r.returncode == 0
    return ok, results


def run_full():
    t = time.time()
    r = subprocess.run(['bash', 'tools/ci-gates.sh'], cwd=ROOT, capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if re.match(r'(PASS|FAIL)\s|ALL GATES', l)]
    print('\n'.join(lines))
    return r.returncode == 0, {'argv': ['bash', 'tools/ci-gates.sh'], 'exit_code': r.returncode,
                               'seconds': round(time.time() - t, 1), 'summary': lines,
                               'tail': '' if r.returncode == 0 else (r.stdout + r.stderr)[-2000:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--mark', action='store_true')
    a = ap.parse_args()
    if not re.fullmatch(r'\d{4}', a.batch):
        raise SystemExit('batch must be 4 digits')
    out = LITE / 'batches' / a.batch / 'gates.json'
    if a.mark:
        rec = json.loads(git('show', f'HEAD:{out.relative_to(ROOT)}'))   # the committed gate record
        if rec['mode'] != 'full' or not rec['passed']:
            raise SystemExit('committed gates.json is not a passed full run')
        if any(not any(r.fullmatch(p) for r in TRANSLATION_PATHS) for p in changed_paths()):
            raise SystemExit('uncommitted non-translation changes: the tested tree is not HEAD')
        STATE.write_text(json.dumps({'batch': a.batch, 'commit': git('rev-parse', 'HEAD').strip(), 'trees': trees()},
                                    indent=1) + '\n')
        print('marked full PASS at', a.batch)
        return
    reasons = decide(a.batch, a.full)
    if reasons:
        print('mode: full ci-gates;', '; '.join(reasons))
        ok, detail = run_full()
        record = {'batch': a.batch, 'mode': 'full', 'reasons': reasons, 'passed': ok, **detail}
    else:
        print('mode: translation subset (translation-only changes, tools unchanged since the last full PASS)')
        ok, results = run_subset()
        record = {'batch': a.batch, 'mode': 'subset', 'passed': ok, 'checks': results,
                  'skipped': ['03-test-group-registration', '03-toolchain-unit-tests', '04-quality-facts-unit-tests',
                              '04-semantic-claim-unit-tests', '05-contract-suite-unit-tests',
                              '05-production-shadow-surface-ledger-tests'],
                  'skip_basis': 'tool unit-test groups test tools/ and tests/ code with fixtures; unchanged since the '
                                'last full PASS recorded in full-gates.json'}
    out.write_text(json.dumps(record, ensure_ascii=False, indent=1) + '\n')
    print('GATES', 'PASS' if ok else 'FAIL', record['mode'])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
