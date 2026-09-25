import collections
import json
from pathlib import Path

batch = 'batch-6da096d4813ef282276a'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review291-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review291-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review291-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 9, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 9 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review291-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 16, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 8 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=72, repair_required=8, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes of 20, all Cults)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Cults 9 entries)'),
             notes=[
                 'Cults-only batch: surface ran as four lanes of 20; all four lanes echoed their identities exactly and no observation slid.',
                 'The contextual run read only its own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'Severed Threads (28b401e79b): surface flagged the added "attempt", but the public chronophage.lua atrophy hook gates the kill on checkHit and canBe("instakill"), so the wording is refuted; the contextual timeline/lifeline point is confirmed.',
                 '283cf77312 and 2b501aeaa3 carry leading-indentation TAB invariant faults (inner lines), not trailing whitespace.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Eight confirmed repair revisions raise the window 32 backlog from 6 to 14 (batches 290-291).'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=32, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=6, source='batch 290 (d5cfc68c)'),
    backlog_after_count=14, default_max_cycles=5,
    source_batches=['batch-41762084bcf428db6c44', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第291批：冻结80条（全部 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane 各20条，identity 回显全部逐位一致，9个ISSUE，无错位；'
    'contextual 一个 Opus run（9 条）只读 envelope 与契约，未越界，7个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决16个观察：{counts}；预计72条完成、8条待修复。'
    '修复 revision：菲·维莉欧斯的冒险埃尔瓦拉守城一节（叠字/残句/转身/涌入方向/队长称谓/备法）、'
    '腐败的浮肿恐魔 info（内部缩进/召唤物等级/单数主语）、断绝 info“时间线”、心灵尖啸 info 缩进、'
    '阿马克泰尔 lore（改变生灵/触碰/神性存在）、菲·维莉欧斯的冒险死灵法师一节（片刻/遭人非议/察觉法杖/增译/错字/斗篷）、'
    '幻象城堡舰名“无心之失”、慢性死亡技能树描述漏译“痛苦”。'
    '断绝“尝试”贴合实现（豁免与免疫判定）refuted；“递归之家”记 advisory。'
    '修复窗口32积压为14（第290–291批）。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=14), ensure_ascii=False))
