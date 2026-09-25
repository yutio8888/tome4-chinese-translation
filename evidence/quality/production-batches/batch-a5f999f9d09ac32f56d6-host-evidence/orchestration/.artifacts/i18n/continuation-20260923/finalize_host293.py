import collections
import json
from pathlib import Path

batch = 'batch-a5f999f9d09ac32f56d6'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review293-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review293-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review293-surface-raw').glob('*.json')):
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
for file in sorted((scratch / 'review293-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 15, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 7 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=7, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes of 20, all Cults)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Cults 10 entries)'),
             notes=[
                 'Attempts 1-3 of this batch were abandoned for Codex authentication failures (refresh-token reuse, then 401 with a service-account key) before any lane produced output; artifacts and host notes are in review293-attempt-{1,2,3}. Attempt 4 reused the identical frozen workset and candidate identities.',
                 'Cults-only batch: surface ran as four lanes of 20; all four lanes echoed their identities exactly and no observation slid (lane-000-3 prefixed its JSON with a stray "---" line; the harvested output still validated).',
                 'The contextual run read only its own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'Nihil (3de06b73a0) keeps the "other"-type exclusion: the Cults Actor superload skips e.type == "other" for both duration modifiers. natural infusions (3ecc90f60d) keeps the library term 纹身.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Seven confirmed repair revisions raise the window 32 backlog from 19 to 26 (batches 290-293), reaching the 20 threshold: repair window 32 opens next.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=32, window_opened=True, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=19, source='batches 290-292 (afee774a)'),
    backlog_after_count=26, default_max_cycles=5,
    source_batches=['batch-41762084bcf428db6c44', 'batch-6da096d4813ef282276a', 'batch-92e9dabe8523a9675217', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第293批：冻结80条（全部 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    '前三次尝试因 Codex 认证失败（刷新令牌复用、401）在任何输出之前放弃，第四次沿用同一冻结 workset。'
    'surface 4 个 lane 各20条，identity 回显全部逐位一致，10个ISSUE，无错位；'
    'contextual 一个 Opus run（10 条）只读 envelope 与契约，未越界，5个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决15个观察：{counts}；预计73条完成、7条待修复。'
    '修复 revision：坚定意志描述漏译“污秽”、黑色巨石 info 删“尝试”、厄运之触 info（缩进/脱离视线条件）、污秽夹击 info 缩进、'
    '克罗格开场文本（段落空行/伊格兰斯改造）、天谴之龙解锁文本（无可救药/空行）、菲·维莉欧斯的冒险废弃定居点一节（吃蜘蛛网/昏迷多久/指挥官称谓）。'
    '空无括注贴合 superload、natural infusions 沿用本库“纹身”，refuted；属性重铸确认框记 advisory。'
    '修复窗口32积压为26（第290–293批），达到20，开修复窗口32。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=26), ensure_ascii=False))
