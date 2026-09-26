import collections
import json
from pathlib import Path

batch = 'batch-9af99942882ed4c5cb18'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review295-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review295-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review295-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 11, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 11 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review295-contextual-raw').glob('*.json')):
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
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes of 20, all Cults)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Cults 11 entries)'),
             notes=[
                 'Cults-only batch: surface ran as four lanes of 20; all identities echoed correctly and no observation slid.',
                 'lane-000-0 used the injected Paseo MCP terminal tools (create_terminal/send_terminal_keys/capture_terminal) to read its own envelope and the surface contract; every key sequence was read-only, the host captured and killed terminal 7ab023e4 after harvest (recorded as side_effects in HOST-SURFACE-BOUNDARY-AUDIT). The audit script asserted after close/import had already run in the same command; the audit was completed by manual inspection before the contextual child was created.',
                 'The contextual run read only its own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'Two surface observations are refuted because the targets use the library names: Accelerate = 窃速 and Drake Aspect = 龙血类型. Three are advisory: a missing exclamation mark, the Spinal Cord wording, and CARRION_FEET gore imagery.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Six confirmed repair revisions raise the window 33 backlog from 7 to 13 (batches 294-295); below the 20 threshold, so no window opens.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=33, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=7, source='batch 294 (9a6883bb)'),
    backlog_after_count=13, default_max_cycles=5,
    source_batches=['batch-37852a9bef8a75bb4c44', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第295批：冻结80条（全部 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane 各20条，11个ISSUE，无错位、identity 回显无误；lane-000-0 经注入的 Paseo 终端工具只读自身 envelope 与契约，宿主抓取留证后关闭终端，记入 side_effects；'
    'contextual 一个 Opus run（11 条）只读 envelope 与契约，未越界，5个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决16个观察：{counts}；预计74条完成、6条待修复。'
    '修复 revision：菲·维莉欧斯的冒险食人魔突围一节（践踏/许多/挫败狂热者/冲过去/看向前方）、清理垃圾任务描述（作恶者与击杀义、我们的人民）、惊骇幻象减伤限定对其他目标、菲·维莉欧斯的冒险食尸鬼一节（主语、混沌能量、独自思绪、穿过帷幕游荡进城、相撞、连击、视如家人、重字）、德瑞姆知识探求者（自顾自的习语与性别）、龙卷风鞋描述（鞋、旋转）。'
    '窃速、龙血类型为本库译名，refuted；虚空之火感叹号、脊髓措辞、蠕动之足脓液意象记 advisory。'
    '修复窗口33积压为13（第294–295批），未达20。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=13), ensure_ascii=False))
