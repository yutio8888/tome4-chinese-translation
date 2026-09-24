import collections
import json
from pathlib import Path

batch = 'batch-f8d6c02a3294c168f104'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
surface = json.loads((task / 'HOST-SURFACE-DECISIONS.json').read_text())['rows']
contextual = {
    'ff891672cb': ('pending', False, '与 surface 同向：固定主游戏 world-artifacts.lua:2637 的神器名含 Archlich，现译未明确表达；神器专名口径仍需集中决定，本批不单改。'),
    'ffb21dd4cc': ('confirmed', True, '与 surface 同向：固定主游戏 magical.lua:600–618 的增伤效果结束，less dangerous 表威胁降低而非情绪平静；并入同条修复。'),
    'ffe80f4c81': ('confirmed', True, '与 surface 同向：固定主游戏 portal-vault.lua:133 的 strange 被省略；并入同条修复。'),
    'fff8487389': ('confirmed', True, '与 surface 同向：固定主游戏 summon-melee.lua:500–538 赋予 T_UNSTOPPABLE 技能，can become 为可触发状态；并入同条修复。'),
    '0c22616dae': ('confirmed', True, '与 surface 同向：公开 DLC world-artifacts.lua:691 的 treacherous road 是险途，且原文有引号；本批 SHA 匹配，来源和 commit 未固定；并入同条修复。'),
}
rows = list(surface)
for name in ('full-000.json', 'full-001.json'):
    raw = json.loads((scratch / 'review276-contextual-refreeze-raw' / name).read_text())
    for verdict in raw['verdicts']:
        if verdict['verdict'] == 'OK':
            continue
        key = verdict['revision_key'][:10]
        assert key in contextual, key
        status, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=status,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 16
repair = sorted({row['revision_key'] for row in rows if row['repair_required']})
pending = sorted({row['revision_key'] for row in rows if row['disposition'] == 'pending'})
assert len(repair) == 6 and len(pending) == 2
counts = dict(collections.Counter(row['disposition'] for row in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=72, repair_required=6, blocked=2), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (8 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (2 refrozen source-component runs, 11 entries)',
                            selection='user instruction 2026-09-23; refreeze repair authorized 2026-09-24'),
             notes=[
                 'Surface and contextual observations adjudicated independently against their own frozen revision.',
                 'No slid surface observations; all 11 surface observations were host checked before contextual dispatch.',
                 'The contextual scope is the 11 surface ISSUE revisions; the other 69 rest on surface OK.',
                 'Refrozen contextual outputs contain 5 ISSUE, all on already flagged surface revisions; no new repair revision.',
                 'Contextual OK on 0523b49940 and 0ed5688129 does not erase independently confirmed surface findings: source text directly shows the omitted timing/imagery and run/destruction meaning.',
                 'Two named-term observations remain pending for a cross-entry naming decision; they are blocked in this batch, without changing terminology or translation.',
                 'Ashes public source files match this batch workset SHA; source repository/commit remain unpinned.',
                 'Repair backlog rises from 13 to 19. Accumulate-then-repair cadence keeps window 27 closed until at least 20 confirmed repairs.',
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
decisions = {row['revision_key'][:10] + '|' + row['stage']:
             {key: row[key] for key in ('disposition', 'repair_required', 'conclusion')}
             for row in rows}
assert len(decisions) == len(rows)
(scratch / 'review276-host-decisions.json').write_text(json.dumps({
    'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
    'decisions': decisions}, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='accumulate-then-repair cadence (user instruction 2026-09-24: open one combined window at >=20 confirmed repairs)',
    target_window=27, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=13, source='batch-54d2d16b94c511082107 REPAIR-BACKLOG-DECISION.json'),
    backlog_after_count=19, default_max_cycles=3,
    excluded='pending named terms, advisory, unrelated existing blocked/repair records, and global terminology renames',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第276批：冻结80条，源码逐条核验80/80；主游戏32条对应固定commit 624a673，Ashes DLC 48条按本批公开源码文件SHA核对，来源仓库和commit未固定。'
    'surface 8个Codex lane审80条，11个ISSUE；contextual按组件拆成2个Opus run，复核11条，5个ISSUE。'
    '两路重冻reviewer的原生读取边界由宿主核对，均未从根目录扫描，输出严格收录并确认归档；旧DLC越界输出不参与结果。\n\n'
    '宿主裁决16个观察：%s；结果72条完成、6条待修复、2条因专名策略待定而阻塞。'
    '修复项：威胁降低误作平静、奇异传送门漏译、石傀儡技能可能性误作常态、DLC灼热平台时序与意象、险途误作背叛、逃跑/毁灭工具误译。'
    'Archlich权杖与Armoured Leviathan的跨条命名暂留pending。已确认修复积压从13增至19，未达20，不开启窗口27。\n' % counts)
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=19), ensure_ascii=False))
