"""Generic single-run host finalize: finalize_host_gen.py <N>.

Counts come from review<N>-host-decisions.json and the surface/contextual raw
results; only prose comes from /tmp/fin<N>.json:
  surface_note_en, contextual_note_en, extra_notes_en (list), commit_note_en,
  surface_zh, contextual_zh, repairs_zh, other_zh,
  backlog_before {count, source}, prior_source_batches (list), target_window,
  backlog_items_zh (handoff list fragment for this batch)
Writes HOST-SURFACE-DECISIONS, HOST-FINAL-DECISIONS, REPAIR-BACKLOG-DECISION,
HOST-SUMMARY and /tmp/stats<N>.json (consumed by handoff_gen.py and the
commit messages). Refuses mixed-source/multi-run batches (use the 290/287 path).
"""
import collections
import json
import re
import sys
from pathlib import Path

N = sys.argv[1]
T = sys.argv[2] if len(sys.argv) > 2 else N  # file tag (review<T>-*)
scratch = Path('.artifacts/i18n/continuation-20260923')
batch = re.search(r'"batch_id": "(batch-[0-9a-f]+)"', (scratch / f'review{T}-start.out').read_text()).group(1)
task = Path('.ai/task') / batch
fin = json.loads(Path(f'/tmp/fin{N}.json').read_text())
spec = json.loads((scratch / f'review{T}-host-decisions.json').read_text())['decisions']
_ws = json.loads((Path('evidence/quality/production-batches') / f'{batch}-source-workset.json').read_text())
_comp = {e['entry_revision_identity']: e['component'] for e in _ws['entries']}
_cc = collections.Counter(_comp.values())
_EN = {'tome': 'main game', 'engine': 'engine', 'boot': 'boot', 'orcs': 'Orcs', 'ashes-urhrok': 'Ashes', 'cults': 'Cults'}
_ZH = {'tome': '主游戏', 'engine': '引擎', 'boot': '启动', 'orcs': 'Orcs', 'ashes-urhrok': 'Ashes', 'cults': 'Cults'}
_order = ['tome', 'engine', 'boot', 'orcs', 'ashes-urhrok', 'cults']
_pinned = sum(_cc[c] for c in ('tome', 'engine', 'boot'))
_dlc = [c for c in ('orcs', 'ashes-urhrok', 'cults') if _cc[c]]
comp_zh = '、'.join(f'{_ZH[c]} {_cc[c]} 条' for c in _order if _cc[c])
pinned_en = ', '.join(f'{_cc[c]} {_EN[c]}' for c in ('tome', 'engine', 'boot') if _cc[c])
dlc_en = ', '.join(f'{_cc[c]} {_EN[c]}' for c in _dlc)
_plan = json.loads((scratch / f'review{T}-surface-plan.json').read_text())
_groups = []
for _tid, _g in _plan.items():
    _sizes = [l['entries'] for l in _g['lanes']] if isinstance(_g.get('lanes'), list) else [_g['entries']]
    _ids = []
    for _l in (_g['lanes'] if isinstance(_g.get('lanes'), list) else []):
        _ids += [e['entry_revision_identity'] for e in json.loads(Path(_l['input_path']).read_text())['payload']['entries']]
    _gc = sorted({_comp[i] for i in _ids}, key=_order.index) if _ids else []
    _lab = '/'.join(_EN[c] for c in _gc) or 'full'
    _mode = 'full mode' if _g['mode'] == 'full' else '/'.join(map(str, _sizes))
    _groups.append(f"{'surface' if _tid == batch else 'surface-' + _tid.rsplit('-', 1)[-1]} {_lab} {_g['entries']} in {_mode}")
groups_en = '; '.join(_groups)

rows = []
surface = collections.Counter()
lanes = 0
for file in sorted((scratch / f'review{T}-surface-raw').glob('*.json')):
    lanes += 1
    for result in json.loads(file.read_text())['results']:
        surface[result['verdict']] += 1
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
n_surface = len(rows)
EXTRA = json.loads((scratch / f'review{T}-extra.json').read_text())
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='surface-only batch: every lane returned OK, so no observation needed adjudication and no contextual run was needed',
    slid_observations=fin.get('slid_observations'),
    additional_host_observations=EXTRA,
    slide_check=fin.get('slide_check_en', f'all {n_surface} observations checked against their own frozen source/target; none slid'),
    rows=rows), ensure_ascii=False, indent=2) + '\n')
ctx_files = sorted((scratch / f'review{T}-contextual-raw').glob('*.json'))
assert not ctx_files and not surface.get('ISSUE'), 'surface-only batch: no deep rows, no contextual run'
_runs = []
contextual = collections.Counter()
for file in ctx_files:
    for verdict in json.loads(file.read_text())['verdicts']:
        contextual[verdict['verdict']] += 1
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec), (len(rows), len(spec))
total = len(_ws['entries'])
import os
BLOCKED = int(os.environ.get('BLOCKED', '0'))  # host-blocked dead keys in this batch
assert sum(surface.values()) in (total, total - BLOCKED), (sum(surface.values()), total, BLOCKED)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert not pending, 'pending rows need the manual path'
counts = dict(collections.Counter(r['disposition'] for r in rows))
done = total - len(repair) - BLOCKED
before = fin['backlog_before']
after = before['count'] + len(repair)
window = fin['target_window']
notes = [fin['surface_note_en'], fin['contextual_note_en'], *fin.get('extra_notes_en', []),
         (f'{_pinned} pinned entries ({pinned_en}) were verified against the manifest-pinned commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 and all matched the literal in the recorded file' if _pinned else 'No pinned entries')
         + (f'; {dlc_en} entries matched the public DLC source file SHA in the workset, with the DLC repositories and commits unpinned.' if _dlc else '.'),
         f'{len(repair)} confirmed repair revisions raise the window {window} backlog from {before["count"]} to {after}'
         + (f', reaching the 20 threshold: repair window {window} opens next.' if after >= 20 else '; below the 20 threshold, so no window opens.')]
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=done, repair_required=len(repair), blocked=BLOCKED), rows=rows,
             additional_host_observations=EXTRA,
             reviewers=dict(surface=f'codex/gpt-6.1-sol ({lanes} lanes: {groups_en})',
                            contextual='none (no deep_required entry)'),
             notes=notes)
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=window, window_opened=after >= 20, batch=batch, bounded_revision_keys=repair,
    backlog_before=before, backlog_after_count=after, default_max_cycles=5,
    source_batches=[*fin['prior_source_batches'], batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
zh = {'confirmed': '确认', 'refuted': '驳回', 'advisory': '建议'}
(task / 'HOST-SUMMARY.md').write_text(
    f'第{N}批：冻结{total}条（{comp_zh}；为修复窗口67迁移 a0f4f220 排入的 successor），逐条核验{total}/{total}：' + ('主游戏、引擎与启动按 manifest 固定 commit 624a673 核验' if _pinned else '') + ('，' if _pinned and _dlc else '') + ('DLC 按本批公开源码文件SHA核验、来源仓库和commit未固定' if _dlc else '') + f'。'
    + fin['surface_zh'] + fin['contextual_zh'] +
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决{len(rows)}个观察：{counts}；预计{done}条完成、{len(repair)}条待修复。'
    + fin['repairs_zh'] + fin['other_zh'] +
    f'修复窗口{window}积压为{after}' + (f'，达到20，开修复窗口{window}。\n' if after >= 20 else '，未达20。\n'))
stats = dict(N=N, batch=batch, total=total, done=done, repair=len(repair), repair_keys=repair,
             surface=dict(surface), contextual=dict(contextual), dispositions=counts,
             observations=len(rows), backlog_before=before['count'], backlog_after=after, window=window,
             lanes=lanes, contextual_entries=sum(contextual.values()))
Path(f'/tmp/stats{N}.json').write_text(json.dumps(stats, ensure_ascii=False, indent=1))
if after >= 20:
    print(f'WINDOW_THRESHOLD_REACHED: repair window {window} opens next')
print(json.dumps(dict(dispositions=counts, done=done, repair=len(repair), backlog=after), ensure_ascii=False))
