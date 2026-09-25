import collections
import json
from pathlib import Path

batch = 'batch-fbefc4aef1a281aee013'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review288-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review288-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review288-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 10, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 10 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review288-contextual-raw').glob('*.json')):
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
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, Cults 80)',
                            contextual='claude/claude-opus-5-5 (full-000, Cults 10 entries)'),
             notes=[
                 'Lane 1 echoed result 10 identity with a typo; the host saved the original raw, corrected only that identity by full-set positional comparison and harvested the corrected raw (recorded in HOST-SURFACE-BOUNDARY-AUDIT identity_echo_corrections). No observation slid.',
                 'The contextual run read only its frozen envelope and the v2 contract; no /workspace probing, so no refreeze was needed.',
                 '043e30bf48 (entropic feedback damage equals power% of healing) and 0f553f817a (Writhing Hairs: dam * brittle/100 with brittle 30-60 reduces damage, contrary to the English) match the implementation; 1070f364a9 plural is not a Chinese defect.',
                 '0b62ca8ba3 is advisory: the confirm button is Read Tome but confirming does transition into the tome plane.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Six confirmed repair revisions raise the window 31 backlog to 14, below the threshold of 20; review continues with batch 289.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=31, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=8, source='batch-de7c2c3d32f752f42784 (batch 287)'),
    backlog_after_count=14, default_max_cycles=5,
    source_batches=['batch-de7c2c3d32f752f42784', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第288批：冻结80条（全为 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane，lane 1 一处 identity 回显错字经宿主保存原件、逐位更正后收取，10个ISSUE，无错位；contextual Opus 单 run 复核 10 条，未越界，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决16个观察：{counts}；预计74条完成、6条待修复。'
    '修复 revision：熵之化身 lore（manifestation、towering、多余视角）、撕裂目标的本质、霾洞开场（sometimes/to look at you、增译整天）、'
    'Additionally 段前空行、野心误作骄傲自满与增译撕裂的空间、熵能反冲 info 两处空行。'
    '熵能反馈等量伤害、蜿蜒之发伤害降至 brittle%（实现与英文相反，译文贴合实现）、阵营名复数均 refuted；禁书确认弹窗“进入”记 advisory。'
    '修复窗口31积压为14，未达20，继续审核第289批。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=14), ensure_ascii=False))
