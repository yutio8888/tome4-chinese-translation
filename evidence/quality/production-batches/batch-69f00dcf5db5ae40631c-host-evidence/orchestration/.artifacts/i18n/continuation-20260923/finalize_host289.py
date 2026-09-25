import collections
import json
from pathlib import Path

batch = 'batch-69f00dcf5db5ae40631c'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review289-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review289-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review289-surface-raw').glob('*.json')):
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
    slide_check='all 11 observations checked against their own frozen source/target; 1a5b7fe508 carries the observation of the preceding lane-000-2 entry 1a38e54fe5 (which matches the implementation); 1a5b7fe508 is confirmed on its own TAB defect',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review289-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 19, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 9 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=71, repair_required=9, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, Cults 80)',
                            contextual='claude/claude-opus-5-5 (refreeze dlc-location-v1 of full-000, Cults 11 entries)'),
             notes=[
                 'All four surface lanes echoed their identities exactly; one observation slid by one entry (1a5b7fe508 carries the text for 1a38e54fe5), rescued by confirming 1a5b7fe508 on its own TAB defect; 1a38e54fe5 itself matches the PROPHECY_OF_TREASON timer implementation.',
                 'The first contextual run (full-000) ran `ls tome-cults; ls ../t-engine4` to look for a source checkout and was rejected (review289-contextual-0-rejection.json) and archived; its findings are not used. The refreeze dlc-location-v1 run read only its envelope and the contract and was accepted.',
                 'stage_contextual/contextual_export only write source_checkout for Ashes facts, so the all-Cults refreeze envelope is byte-identical to the rejected one (same candidate identity) and still names no checkout; --ashes-checkout was given the Cults checkout, which the validator does not consult for Cults facts. Supporting a Cults checkout location is a tooling follow-up.',
                 'The contextual anchor preflight required explicit chapter-title anchors for tome-cults/data/lore/fay-willows.lua (32 titles); prepare_contextual289.py now derives ordered_titles from the actual title calls.',
                 'SPEC.md of this batch (like 287 and 288) says the adjudication uses Ashes public source; the batch is all Cults and was adjudicated against SHA-verified Cults source. The SPEC bytes are part of the frozen candidate, so the wording is left as is and the template is fixed from batch 290.',
                 '18b675d3dc keeps the library term 混沌效果 (sibling Chaos Orbs info maps insanity chaotic effect to it); 1a72cc2056 matches FORTUNE activate/on_merge.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Nine confirmed repair revisions raise the window 31 backlog to 23 (batches 287-289), reaching the threshold of 20; repair window 31 opens next.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=31, window_opened=True, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=14, source='batches 287 (8) and 288 (6)'),
    backlog_after_count=23, default_max_cycles=5,
    source_batches=['batch-de7c2c3d32f752f42784', 'batch-fbefc4aef1a281aee013', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第289批：冻结80条（全为 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane，identity 回显全部逐位一致，11个ISSUE（lane-000-2 一条 observation 错位一格，逐条比对后以本条自身制表符缺陷确认）；'
    'contextual 首轮 Opus run 为找源码 checkout 执行 ls ../t-engine4，被拒收并归档，refreeze（dlc-location-v1）run 复核这11条，8个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决19个观察：{counts}；预计71条完成、9条待修复。'
    '修复 revision：触手 info 两处空行、菲·维莉欧斯的冒险两条（话音渐弱/魔法大爆炸/解救者颠倒/转身/待在家里/夫妇/伸出；plans/问句变陈述/惊讶对象/漏译一句）、'
    '部落几天的食物、德瑞姆 lore（进食/无法讲理/野生德瑞姆/德瑞莫）、菲·维莉欧斯的冒险纳格尔王国一节（领袖复数/被迫/地震增译）、ever ceasing 反译、阿马克泰尔 info 制表符、德瑞姆出生描述“出现”。'
    '混沌效果术语与幸运叠层括注贴合本库与实现 refuted。'
    '修复窗口31积压为23（第287–289批），达到20，开修复窗口31。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=23), ensure_ascii=False))
