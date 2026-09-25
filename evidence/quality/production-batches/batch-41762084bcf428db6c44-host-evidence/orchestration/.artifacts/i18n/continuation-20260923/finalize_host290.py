import collections
import json
from pathlib import Path

batch = 'batch-41762084bcf428db6c44'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review290-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review290-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review290-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 12, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 12 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review290-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 16, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 6 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=74, repair_required=6, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (8 lanes: surface-000 Ashes 6, surface-001 Cults 74)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Ashes 2 entries, contextual-001 Cults 10 entries)'),
             notes=[
                 'Mixed Ashes+Cults batch: surface ran as two lane groups (4 Ashes lanes of 2/2/1/1, 4 Cults lanes of 19/19/18/18); all eight lanes echoed their identities exactly and no observation slid.',
                 'Both contextual runs read only their own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'contextual-001 flagged KROG_WRATH (21736923b6) and TOTAL_COLLAPSE (274f704d64) only because the envelope lacked the callbacks; the host checked the public Cults callbacks and both translations match the implementation.',
                 '023ddaba77 is the window 31 successor of the Slimy Tendril info; its numbed wording stays with pending-user-review item 30.',
                 'prepare_contextual290.py now labels each run SPEC by its own component (Ashes / Cults).',
                 'Ashes and Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Six confirmed repair revisions start the window 32 backlog at 6 (from batch 290).'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=32, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=0, source='window 31 closed and pushed (6782ea15)'),
    backlog_after_count=6, default_max_cycles=5,
    source_batches=[batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第290批：冻结80条（Cults 74、Ashes 6，混合批），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 分两组 8 个 lane，identity 回显全部逐位一致，12个ISSUE，无错位；'
    'contextual 两个 Opus run（Ashes 2 条、Cults 10 条）只读 envelope 与契约，未越界，4个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决16个观察：{counts}；预计74条完成、6条待修复。'
    '修复 revision：被诅咒城堡手记（书的容量/牺牲宝物/变化逻辑）、德瑞姆探险笔记（玻璃管容量/黑色增生物/感染范围/野生德瑞姆/残句）、'
    '瓦解 info 换行、克诺什库尔 lore“别无归处”、蛆虫吐息 info 多余换行、城堡手记“整理内部”。'
    '震慑几率与全面崩溃括注贴合实现 refuted；熵能力量为本库通用词；numbed 仍按待审第30项。'
    '修复窗口32积压为6（第290批）。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=6), ensure_ascii=False))
