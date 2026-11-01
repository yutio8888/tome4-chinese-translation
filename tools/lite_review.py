"""Lightweight full-translation review ledger (2026-11-01, docs/lite-review-workflow-20261101.md).

Subcommands:
  status                      progress against the current translation files
  next [--max N] [--path P]   print the next unreviewed slice (release-required units, file order)
  prepare BATCH [--max N] [--path P] [--units FILE]
                              freeze batches/BATCH/input.json and the A/B prompts
  collect BATCH LANE RAW      extract the lane JSON (first JSON object in RAW) into batches/BATCH/LANE.json
  strict BATCH                validate the confirmed edits of batches/BATCH/decision.json with `tools/i18n proposal --strict`
  record BATCH                append reviewed units to ledger.jsonl from batches/BATCH/decision.json

A unit is reviewed for a lane when (unit_id, revision_key) is in the R296 seed or the ledger for that lane.
Changing a target changes its revision, so the unit returns to the queue and is re-reviewed.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from i18nlib import full_review as fr  # noqa: E402
from i18nlib.config import load_manifest  # noqa: E402
from i18nlib.cli_common import _inject_public_dlc_env  # noqa: E402

LITE = ROOT / 'evidence/lite-review'
SEED = LITE / 'seed-R296.json'
LEDGER = LITE / 'ledger.jsonl'
CORE = '624a67329fe2ad440c5b344785a9c73fcf22ae63'
ENGINE_REPO = Path('/workspace/t-engine4')
DLC = {'tome-cults': Path('/workspace/tome4-dlcs/cults'), 'tome-orcs': Path('/workspace/tome4-dlcs/orcs'),
       'tome-ashes-urhrok': Path('/workspace/tome4-dlcs/ashes-urhrok')}
MAX = 80


def units():
    _inject_public_dlc_env()
    rows, _ = fr.current_units(load_manifest())
    return [u for u in rows if u['disposition'] == 'release-required']


def reviewed():
    done = {'A': set(), 'B': set()}
    seed = json.loads(SEED.read_text())
    for r in seed['units']:
        for lane in ('A', 'B'):
            if r[lane]:
                done[lane].add((r['unit_id'], r['revision_key']))
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            r = json.loads(line)
            for lane in r['lanes']:
                done[lane].add((r['unit_id'], r['revision_key']))
    return done


def order_key(u):
    o = u['occurrence']
    return (o['translation_path'], o['document_ordinal'])


def pending(us, done):
    return sorted((u for u in us if (u['unit_id'], u['revision_key']) not in done['A']), key=order_key)


def select(us, done, max_n, path=None):
    rest = [u for u in pending(us, done) if path is None or u['occurrence']['section'] == path
            or u['occurrence']['section'].startswith(path)]
    if not rest:
        return []
    # group by section in file order; take whole sections while they fit, split a section only if it alone exceeds max
    groups, seen = [], {}
    for u in rest:
        s = u['occurrence']['section']
        if s not in seen:
            seen[s] = len(groups); groups.append([])
        groups[seen[s]].append(u)
    out = []
    for g in groups:
        if not out and len(g) > max_n:
            return g[:max_n]
        if len(out) + len(g) > max_n:
            break
        out += g
    return out


_src_cache = {}


def source_text(section):
    head, _, rest = section.partition('/')
    if head == 'mod-tome':
        key = ('core', 'game/modules/tome/' + rest)
    elif head == 'engine':
        key = ('core', 'game/engines/default/engine/' + rest)
    elif head in DLC:
        key = ('dlc', str(DLC[head] / head / rest))
    else:
        return None, None
    if key not in _src_cache:
        if key[0] == 'core':
            r = subprocess.run(['git', '-C', str(ENGINE_REPO), 'show', f'{CORE}:{key[1]}'], capture_output=True)
            _src_cache[key] = r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None
        else:
            p = Path(key[1])
            _src_cache[key] = p.read_text('utf-8', 'replace') if p.exists() else None
    loc = (f'{key[1]} @ {CORE[:12]} (pinned core)' if key[0] == 'core'
           else f'{key[1]} (unpinned public DLC checkout)')
    return _src_cache[key], loc


def locate(text, source):
    if text is None:
        return []
    lines = text.splitlines()
    first = source.split('\n')[0]
    needles = [json.dumps(first, ensure_ascii=False)[1:-1], first]
    hits = []
    for n in needles:
        if not n.strip():
            continue
        hits = [i + 1 for i, l in enumerate(lines) if n in l]
        if hits:
            break
    return hits[:5]


def grep_core(source):
    """Hints for sections with no single source file (.always_merge etc.): quoted literal hits at the pinned core."""
    first = source.split('\n')[0]
    if len(first.strip()) < 3:
        return []
    r = subprocess.run(['git', '-C', str(ENGINE_REPO), 'grep', '-n', '-F', '-e', f'"{first}"', '-e', f"'{first}'",
                        CORE, '--', 'game/', ':(exclude,glob)**/locales/**'], capture_output=True)
    hits = []
    for line in r.stdout.decode('utf-8', 'replace').splitlines()[:5]:
        _, path, number, _ = line.split(':', 3)     # <commit>:<path>:<line>:<text>
        hits.append(f'{path}:{number}')
    return hits


def entry(u):
    o = u['occurrence']
    text, loc = source_text(o['section'])
    if loc is None:
        hits = grep_core(o['source'])
        return {'id': u['unit_id'][:12], 'unit_id': u['unit_id'], 'revision_key': u['revision_key'],
                'translation_file': o['translation_path'], 'translation_line': u['line'],
                'section': o['section'], 'source_tag': o['source_tag'], 'args_order': o['args_order'],
                'source': o['source'], 'target': o['target'],
                'source_file': f'git grep @ {CORE[:12]} (pinned core; no single source file)' if hits else None,
                'source_lines': hits}
    return {'id': u['unit_id'][:12], 'unit_id': u['unit_id'], 'revision_key': u['revision_key'],
            'translation_file': o['translation_path'], 'translation_line': u['line'],
            'section': o['section'], 'source_tag': o['source_tag'], 'args_order': o['args_order'],
            'source': o['source'], 'target': o['target'], 'source_file': loc,
            'source_lines': locate(text, o['source'])}


PROMPT = """轻量审核 {lane}（{batch}）。逐条审 {path} 中的译文，有源码或语境证据的问题报 ISSUE，否则 OK。
读完 docs/lite-review-reviewer.md 的规则后开始。核心源码只用固定提交（git -C /workspace/t-engine4 show {core}:<path>），DLC 读 /workspace/tome4-dlcs 下公开检出。
仓库只读；把结果 JSON 写到 {out}，并把同一 JSON 作为最终回复（不加其他文字）。"""


def prepare(batch, max_n, path, units_file):
    us = units()
    done = reviewed()
    if units_file:
        want = set(json.loads(Path(units_file).read_text()))
        chosen = sorted((u for u in us if u['unit_id'] in want or u['unit_id'][:12] in want), key=order_key)
    else:
        chosen = select(us, done, max_n, path)
    if not chosen:
        raise SystemExit('nothing pending')
    d = LITE / 'batches' / batch
    if (d / 'input.json').exists():
        raise SystemExit('batch exists: ' + batch)
    d.mkdir(parents=True, exist_ok=True)
    entries = [entry(u) for u in chosen]
    for e in entries:
        e['previously_reviewed'] = {lane: any(k[0] == e['unit_id'] for k in done[lane]) for lane in ('A', 'B')}
    data = {'batch': batch, 'core_commit': CORE, 'count': len(entries),
            'sections': sorted({e['section'] for e in entries}), 'entries': entries}
    (d / 'input.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    for lane in ('A', 'B'):
        out = f'/tmp/lite-review/{batch}-{lane}.json'
        (d / f'prompt-{lane}.txt').write_text(PROMPT.format(lane=lane, batch=batch, path=str(d / 'input.json').replace(str(ROOT) + '/', ''),
                                                            core=CORE, out=out))
    Path('/tmp/lite-review').mkdir(exist_ok=True)
    print(json.dumps({'batch': batch, 'count': len(entries), 'sections': data['sections']}, ensure_ascii=False))


def first_json(raw):
    i = raw.find('{')
    while i >= 0:
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw[i:])
            if isinstance(obj, dict) and 'verdicts' in obj:
                return obj
        except json.JSONDecodeError:
            pass
        i = raw.find('{', i + 1)
    raise SystemExit('no verdict JSON found')


def collect(batch, lane, raw_path):
    d = LITE / 'batches' / batch
    inp = json.loads((d / 'input.json').read_text())
    raw = Path(raw_path).read_text()
    obj = first_json(raw)
    ids = [e['id'] for e in inp['entries']]
    got = {}
    for v in obj['verdicts']:
        k = str(v.get('id', ''))[:12]
        if k not in ids or v.get('verdict') not in ('OK', 'ISSUE'):
            raise SystemExit(f'bad verdict row: {v}')
        got[k] = v
    missing = [k for k in ids if k not in got]
    if missing:
        raise SystemExit(f'missing {len(missing)} verdicts: {missing[:5]}')
    (d / f'{lane}.raw.txt').write_text(raw)
    (d / f'{lane}.json').write_text(json.dumps({'lane': lane, 'verdicts': [got[k] for k in ids]}, ensure_ascii=False, indent=1) + '\n')
    iss = [k for k in ids if got[k]['verdict'] == 'ISSUE']
    print(f'{lane} {len(ids)} verdicts; ISSUE {len(iss)}: {iss}')
    for k in iss:
        e = next(x for x in inp['entries'] if x['id'] == k)
        print(f'--- {k} [{e["section"]}] {e["source"][:120]!r}\n    T: {e["target"][:120]!r}\n    O: {got[k].get("observation", "")[:600]}')


def record(batch):
    """decision.json: {"confirmed":[{"id","edit":[old,new],"evidence"}], "advisory":[{"id","note"}], "notes": str}.
    Units whose current revision still equals the frozen input revision are recorded as reviewed by A and B;
    confirmed units are recorded with their decision and return to the queue after the edit (new revision)."""
    d = LITE / 'batches' / batch
    inp = json.loads((d / 'input.json').read_text())
    dec = json.loads((d / 'decision.json').read_text())
    lanes = {lane: json.loads((d / f'{lane}.json').read_text()) for lane in ('A', 'B')}
    conf = {c['id'] for c in dec.get('confirmed', [])}
    adv = {c['id'] for c in dec.get('advisory', [])}
    rej = {c['id'] if isinstance(c, dict) else c for c in dec.get('rejected', [])}   # {"id","reason"} or a bare id
    issues = {k for lane in lanes.values() for v in lane['verdicts'] if v['verdict'] == 'ISSUE' for k in [v['id']]}
    if not issues <= conf | adv | rej:
        raise SystemExit(f'unadjudicated ISSUE: {sorted(issues - conf - adv - rej)}')
    if conf and not (d / 'strict-result.json').exists():
        raise SystemExit('confirmed edits need `lite_review.py strict BATCH` first')
    already = set()
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            r = json.loads(line)
            if r['batch'] == batch:
                already.add(r['unit_id'])
    n = 0
    with LEDGER.open('a') as fh:
        for e in inp['entries']:
            if e['unit_id'] in already:
                continue
            v = {lane: next(x for x in lanes[lane]['verdicts'] if x['id'] == e['id'])['verdict'] for lane in lanes}
            status = ('confirmed' if e['id'] in conf else 'advisory' if e['id'] in adv
                      else 'rejected' if e['id'] in rej else 'ok')
            fh.write(json.dumps({'batch': batch, 'unit_id': e['unit_id'], 'revision_key': e['revision_key'],
                                 'section': e['section'], 'lanes': ['A', 'B'], 'verdicts': v, 'host': status},
                                ensure_ascii=False, sort_keys=True) + '\n')
            n += 1
    print(f'recorded {n} units ({len(conf)} confirmed, {len(adv)} advisory)')


def strict(batch):
    """Strict proposal validation of the confirmed edits, in the validator shape used by the W63 repairs."""
    from i18nlib import full_review as f
    from i18nlib.workset import create_workset, proposal_template_for
    from i18nlib.lint import stable_entry_id
    d = LITE / 'batches' / batch
    inp = {e['id']: e for e in json.loads((d / 'input.json').read_text())['entries']}
    dec = json.loads((d / 'decision.json').read_text())
    m = load_manifest()
    comp = {c.translation: c.id for c in m.components}
    live = {u['unit_id']: u for u in units()}
    groups = {}
    for c in dec.get('confirmed', []):
        e = inp[c['id']]
        o = live[e['unit_id']]['occurrence']
        if o['target'] == e['target']:
            raise SystemExit(f'{c["id"]}: target not edited yet')
        groups.setdefault(comp[e['translation_file']], []).append((c, e, o))
    results = []
    for component, rows in groups.items():
        items, targets = [], {}
        for c, e, o in rows:
            eid = stable_entry_id(component, e['section'], e['source'], e['source_tag'])
            targets[eid] = o['target']
            items.append({'entry_id': eid, 'component': component, 'section': e['section'], 'source': e['source'],
                          'source_tag': e['source_tag'], 'previous_target': e['target'],
                          'previous_args_order': e['args_order'], 'previous_special': o.get('special'),
                          'host_repair_unit_id': e['unit_id']})
        out = ROOT / '.artifacts/i18n/lite-review' / batch / component
        out.mkdir(parents=True, exist_ok=True)
        report = {'schema_version': 1, 'component': component, 'untranslated': items,
                  'derivation_kind': 'host-confirmed-target-repair-selection in merge-report-compatible validator shape',
                  'meaning': 'untranslated is the required validator container name only: these items already have '
                             'translations. Lite review batch ' + batch + ' confirmed edits.',
                  'provenance': [{'host_record': str((d / 'decision.json').relative_to(ROOT))}]}
        report['merge_id'] = f.sha(f.canonical(report))
        rp = out / 'confirmed-repair-selection.json'
        rp.write_bytes(f.canonical(report))
        w = create_workset(m, merge_report_path=rp, limit=len(items), section_prefix=None, classification='all')
        proposal = proposal_template_for(w)
        for p in proposal['proposals']:
            p['target'] = targets[p['entry_id']]
            p['notes'] = f'Lite review batch {batch} host-confirmed edit'
        pp = out / 'proposal.json'
        pp.write_bytes(f.canonical(proposal))
        r = subprocess.run(['python3', '-B', 'tools/i18n', 'proposal', '--workset', str(w['output']), '--proposal', str(pp),
                            '--strict', '--json'], capture_output=True, text=True, cwd=ROOT)
        results.append({'component': component, 'units': [e['unit_id'] for _, e, _ in rows], 'exit_code': r.returncode,
                        'stdout': r.stdout[-4000:], 'stderr': r.stderr[-4000:]})
        if r.returncode:
            print(r.stdout[-3000:], r.stderr[-3000:])
            raise SystemExit(f'strict proposal failed for {component}')
    (d / 'strict-result.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    print('strict ok:', {g: len(v) for g, v in groups.items()})


def status():
    us = units()
    done = reviewed()
    a = sum((u['unit_id'], u['revision_key']) in done['A'] for u in us)
    b = sum((u['unit_id'], u['revision_key']) in done['B'] for u in us)
    p = pending(us, done)
    by = {}
    for u in p:
        by[u['occurrence']['translation_path']] = by.get(u['occurrence']['translation_path'], 0) + 1
    print(json.dumps({'release_required_units': len(us), 'reviewed_A': a, 'reviewed_B': b, 'pending_A': len(p),
                      'pending_by_file': by, 'next_sections': list(dict.fromkeys(u['occurrence']['section'] for u in p))[:8]},
                     ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('status')
    n = sp.add_parser('next'); n.add_argument('--max', type=int, default=MAX); n.add_argument('--path')
    p = sp.add_parser('prepare'); p.add_argument('batch'); p.add_argument('--max', type=int, default=MAX); p.add_argument('--path'); p.add_argument('--units')
    c = sp.add_parser('collect'); c.add_argument('batch'); c.add_argument('lane', choices=['A', 'B']); c.add_argument('raw')
    r = sp.add_parser('record'); r.add_argument('batch')
    s = sp.add_parser('strict'); s.add_argument('batch')
    a = ap.parse_args()
    if a.cmd == 'status':
        status()
    elif a.cmd == 'next':
        for u in select(units(), reviewed(), a.max, a.path):
            o = u['occurrence']; print(u['unit_id'][:12], o['section'], o['source_tag'], repr(o['source'][:60]))
    elif a.cmd == 'prepare':
        if not re.fullmatch(r'\d{4}', a.batch):
            raise SystemExit('batch must be 4 digits')
        prepare(a.batch, a.max, a.path, a.units)
    elif a.cmd == 'collect':
        collect(a.batch, a.lane, a.raw)
    elif a.cmd == 'strict':
        strict(a.batch)
    elif a.cmd == 'record':
        record(a.batch)


if __name__ == '__main__':
    main()
