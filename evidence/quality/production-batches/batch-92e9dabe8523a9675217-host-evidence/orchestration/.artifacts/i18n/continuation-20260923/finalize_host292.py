import collections
import json
from pathlib import Path

batch = 'batch-92e9dabe8523a9675217'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review292-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review292-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review292-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 8, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 8 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review292-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 14, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 5 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=75, repair_required=5, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes of 20, all Cults)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Cults 8 entries)'),
             notes=[
                 'Cults-only batch: surface ran as four lanes of 20; all four lanes echoed their identities exactly and no observation slid (lane-000-2 prefixed its JSON with a stray "---" line; the harvested output still validated).',
                 'The contextual run read only its own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'Cacophony (337c134819) keeps the library talent name; the Fanged Collar special_desc (39b3dcfffa) matches the desc that calls the collar a creature.',
                 'dendritic hemospinner (36a8849dbb) stays advisory: renaming the coined blob family needs a new name, not a correction.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Five confirmed repair revisions raise the window 32 backlog from 14 to 19 (batches 290-292).'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=32, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=14, source='batches 290-291 (6ec03e4e)'),
    backlog_after_count=19, default_max_cycles=5,
    source_batches=['batch-41762084bcf428db6c44', 'batch-6da096d4813ef282276a', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第292批：冻结80条（全部 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane 各20条，identity 回显全部逐位一致，8个ISSUE，无错位；'
    'contextual 一个 Opus run（8 条）只读 envelope 与契约，未越界，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决14个观察：{counts}；预计75条完成、5条待修复。'
    '修复 revision：克诺什库尔“不成型的生物”（应为畸形）、空无 info（多余换行/或增加）、'
    '菲·维莉欧斯的冒险返回符文一节（低语/缓过气/由她指导）、马虑成就描述（救免于死/逃脱/增译）、'
    '菲·维莉欧斯的冒险追击死灵法师一节（现身/其余骷髅/缺字）。'
    '心灵尖啸沿用本库技能名、利牙项环“项环上的生物”贴合 desc，refuted；树突胞递呈者记 advisory。'
    '修复窗口32积压为19（第290–292批）。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=19), ensure_ascii=False))
