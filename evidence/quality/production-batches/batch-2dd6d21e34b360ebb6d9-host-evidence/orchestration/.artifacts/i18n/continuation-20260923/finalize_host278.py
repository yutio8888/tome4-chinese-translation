import collections
import json
from pathlib import Path

batch = 'batch-2dd6d21e34b360ebb6d9'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')

# Each observation is decided against its own frozen revision and source file.
decisions = {
    '2d35d939ad': ('refuted', False, '固定主游戏 TooltipsData.lua:533–536 将 Antimagic User 用作特性标题；“反魔法”作为 UI 标题可表达该特性，正文已说明使用者的行为，省略 User 不造成事实缺失。'),
    '87b94dc2bb': ('refuted', False, '固定主游戏 summon-melee.lua 的 damage%% 已译作“百分比伤害”；resistance penetration %% 是百分比属性而非必须逐字保留的运行时占位符。与第276批同一源串的已记录裁决一致。'),
    '2b3e15fe6a': ('confirmed', True, '公开 Ashes world-artifacts.lua:716 的物品描述是“看似无害的饰物，直到透过孔洞观看”；现译改为劝诫，漏掉饰物、孔洞与转折。本批文件 SHA 匹配，来源仓库/commit 未固定。'),
    '2f11be502c': ('confirmed', True, '公开 Ashes world-artifacts.lua:742 的 pitch black 只表示漆黑，现译“黑曜石”增添材质；同文件:715 另有 obsidian ring，二者不可混同。本批文件 SHA 匹配，来源仓库/commit 未固定。'),
    '318a0c4d70': ('confirmed', True, '公开 Ashes lore/demon.lua:342 的 no less aggressive 是攻击性不逊于年轻同类，few Eyalites would stand and fight 是少有埃亚尔人愿意迎战；现译误作杀伤力及几乎无人能近战，并漏掉改造后代。文件 SHA 匹配，来源仓库/commit 未固定。'),
    '31eda85aa9': ('refuted', False, '公开 Ashes overload/data/chats/ashes-urhrok-walrog-pop.lua:50–54 用 Murderer 代入“%s to the Naloren”句中；中文完整句以“屠戮纳鲁精灵”表达动作，不能孤立按名词判断。文件 SHA 匹配，来源仓库/commit 未固定。'),
    '368ba81f97': ('confirmed', True, '公开 Ashes data/timed_effects.lua:51–52 的 Demon Blade 消失消息主语是 #Target# 的武器；现译写成角色本人威胁降低。文件 SHA 匹配，来源仓库/commit 未固定。'),
    '36a250255f': ('refuted', False, '公开 Ashes overload/data/chats/ashes-urhrok-walrog-pop.lua:50–54 用 Traitor 代入“%s to the Naloren”句中；中文完整句以“背叛乌克姆斯维克”表达动作，不能孤立按名词判断。文件 SHA 匹配，来源仓库/commit 未固定。'),
    '3703023121': ('confirmed', True, '公开 Ashes unlock-corrupter_demonologist.lua:21–36 的 created many dark cults 被误作“通过黑暗仪式”；ranged attackers 遗漏，原文单换行被加空行，恶魔之种/恶魔种子与堕落系/堕落者在同条不一致。文件 SHA 匹配，来源仓库/commit 未固定。'),
    '3747432e7d': ('pending', False, '公开 Ashes timed_effects.lua:523–530 的 Osmosis Regeneration、+/- Osmosis Regen 描述生命再生，现有同族译名统一为“渗透吸收”；是否更名须同步效果及日志，列为跨条名称决定。本批文件 SHA 匹配，来源仓库/commit 未固定。'),
    '39754d3147': ('confirmed', True, '公开 Ashes corruptions.lua:22 明写 Bind and use demons to do your bidding；现译只说驱使恶魔作战，漏掉束缚并把服从命令缩成作战。文件 SHA 匹配，来源仓库/commit 未固定。'),
}
rows = []
for file in sorted((scratch / 'review278-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 11
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='all 11 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

contextual = {
    '2f11be502c': decisions['2f11be502c'],
    '318a0c4d70': decisions['318a0c4d70'],
    '368ba81f97': decisions['368ba81f97'],
    '3703023121': decisions['3703023121'],
}
for file in sorted((scratch / 'review278-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 15
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 6 and len(pending) == 1
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=6, blocked=1), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (8 accepted lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (2 component runs, 11 entries)'),
             notes=[
                 'Surface and contextual observations independently adjudicated against their own frozen revisions.',
                 'The contextual scope was the 11 surface ISSUE revisions; its four ISSUE observations are on existing surface findings.',
                 'Contextual OK does not erase confirmed surface findings on 2b3e15fe6a and 39754d3147, where the source directly supports the omission.',
                 'Two initially invalid surface outputs were rejected, archived and superseded by a fully valid fresh run; only accepted run results count.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Six confirmed repair revisions start a new three-batch window after repair window 27; threshold 20 is not reached.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review278-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='three finalized batches or >=20 unique confirmed executable revisions, whichever comes first',
    target_window=28, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=0, source='repair-window-27-20260924 closed'),
    backlog_after_count=6, default_max_cycles=3,
    excluded='pending named term, advisory and historical blocked entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第278批：冻结80条，逐条源码核验80/80；主游戏16条对应固定commit 624a673，Ashes DLC 64条按本批公开源码文件SHA核对，来源仓库和commit未固定。'
    'surface 8个有效lane审80条，11个ISSUE；contextual按组件拆为2个Opus run复核11条，4个ISSUE。'
    '另有两次surface无效输出已拒收归档，不计入结果。全部有效child的原生读取边界已核对并确认归档。\n\n'
    f'宿主裁决15个观察：{counts}；预计73条完成、6条待修复、1条因同族名称策略待定而阻塞。'
    '六个修复revision为：饰物描述遗漏、漆黑胸甲误作黑曜石、腐化泰坦叙事误译、武器效果对象误译、恶魔使者解锁文案误译、束缚恶魔遗漏。'
    'Osmosis Regen 同族命名暂留pending。修复窗口28积压从0增至6，未达20，继续审核。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=6), ensure_ascii=False))
