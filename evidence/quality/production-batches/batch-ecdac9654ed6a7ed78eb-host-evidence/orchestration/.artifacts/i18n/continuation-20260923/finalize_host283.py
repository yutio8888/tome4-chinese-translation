import collections
import json
from pathlib import Path

batch = 'batch-ecdac9654ed6a7ed78eb'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'
M_unused = '固定主游戏 624a673 engine/damage_types.lua:1188–1203 FIREBURN 先造成 50% 火焰伤害、余下作 3 回合燃烧。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    'a12d1530d5': ('advisory', False, '公开 Ashes world-artifacts.lua:105–110 Fearfire Mantle 为 BASE_CLOAK（unided_name cloak shaped flames）；现译“恐惧之焰”未体现 Mantle（斗篷），但为本库既定神器名（tome-ashes-urhrok.lua:168），单条不改名，记 advisory。' + U),
    'a598376102': ('refuted', False, '所附 observation（半径火焰波→锥形）错位：描述的是同 lane 前一条 a562167573（fearfire.lua:164 炼狱吐息），且该条 target 为 type="cone"（fearfire.lua:141），现译“锥形范围”贴合实现。本条 timed_effects.lua:198 INFERNAL_FEAR long_desc 译文“伤害减少 %d%%，速度减慢 %d%%”准确，不改。' + U),
    'a6090c7e0f': ('refuted', False, '所附 observation（fearsome to behold）错位：描述的是同 lane 前一条 a5ef7ca96f（aquatic-demon.lua:28），已记入 additional_host_observations。本条 achievements/all.lua:87 三恶魔成就说明译文准确，不改。' + U),
    'a6fd631ea2': ('confirmed', True, '公开 Ashes torture.lua:242–243 源串续行以 \\n\\t\\t 缩进（宿主实测源 1 个 LF、1 处 \\n\\t\\t），现译为 \\n\\t，一级 TAB 不变量，只恢复制表符。' + U),
    'aaaaf55ee4': ('confirmed', True, '公开 Ashes birth/corrupted.lua:117：often evil but a few have been known to use demonic powers to fight demons 是“多半用于作恶，少数用来对抗恶魔”；现译“无论善恶”抹去 often evil 倾向并使后半句转折失效，改回倾向与转折。' + U),
    'aad36f17ae': ('refuted', False, '公开 Ashes timed_effects.lua:673–690 DEMONIC_CUT：callbackOnMeleeHit 中仅当 src == eff.src（造成伤口者）近战命中时 src:heal(eff.heal)；现译“造成该伤口的来源以近战攻击命中目标时恢复”贴合实现，上游 info 的 Anytime you hit it 较宽泛。' + U),
    'ac2347dac6': ('confirmed', True, '公开 Ashes timed_effects.lua:195–201 INFERNAL_FEAR 效果名 Overwhelming Fear：有持续时间、最多叠 8 层（max_stacks=8），“无尽”误作无限；本库仅 tome-ashes-urhrok.lua:1479 一处使用，改为“压倒性恐惧”类译名（修复窗口先做双向冲突检查）。' + U),
    'ae8c122720': ('confirmed', True, '公开 Ashes demon-seeds.lua:708–709 源串两句间 \\n\\t\\t（宿主实测源 1 个 LF），现译合为一行（0 个 LF），一级换行不变量；同条“持续 %d 回合”语序随之按原文两句恢复。' + U),
    'af350d83cb': ('refuted', False, '公开 Ashes demonic-strength.lua:122 该光环以 on_melee_hit 施加火焰/枯萎伤害，只在被近战命中时反击；现译“近战反击伤害”贴合实现，上游 info 的 all attacking foes 较宽泛。' + U),
    'af918013e6': ('confirmed', True, '公开 Ashes demonic-pact.lua:855–875：range 为可选目标点的最大距离，随后 teleportRandom 以 radius 随机落点；现译“传到 %d 码外的一个位置”丢 up to/randomly，写成固定距离（删限定词类）。另源串 random demon from your seeds 与 fizzle（实现为以原地为中心在整个 range 内随机传送，:865–869）同条整句核对修复，换行保持。' + U),
    'b281c0e29d': ('confirmed', True, '公开 Ashes corruptions.lua:21：can not be learnt, they must be used from demon seeds attached to your equipment；现译“必须通过装备来展现”丢了“附着在装备上的恶魔种子”这一使用条件，“不是人能学会的”亦增译，整句修复。' + U),
    'b2c260c330': ('refuted', False, '公开 Ashes timed_effects.lua:620/812 为 Corrupted Light 与 Dark Reign 两个增益效果的 on_lose（on_gain 为 #Target# is filled with dark power!），黑暗力量是目标自身获得的增益；“#Target#的黑暗力量消退了”贴合效果结束，不改。' + U),
    'b349784043': ('pending', False, '公开 Ashes timed_effects.lua:521–530 OSMOSIS_REGEN 为持续回复生命效果（subtype heal，on_timeout 调用 self:heal），现译“渗透吸收”未表达 Regeneration，且与渗透护盾吸收易混；但同族 +/-Osmosis Regen 日志（tome-ashes-urhrok.lua:1538–1541）统一用“渗透吸收”，与第278批 3747432e7d 同属一次跨条更名决定，列入待用户集中审阅第24项。' + U),
}
contextual = {
    'a12d1530d5': ('advisory', False, decisions['a12d1530d5'][2] + ' contextual 建议“恐惧之焰斗篷”，作为改名选项记录。'),
    'aaaaf55ee4': decisions['aaaaf55ee4'],
    'ac2347dac6': decisions['ac2347dac6'],
    'af918013e6': decisions['af918013e6'],
    'b281c0e29d': decisions['b281c0e29d'],
    'b349784043': ('pending', False, decisions['b349784043'][2] + ' contextual 建议“渗透回复/渗透再生”，作为改名选项记录。'),
}
extra = [dict(revision_key='a5ef7ca96fd9cdc73c8acebfc36ba8c20a82cb91e986602e499643800710a167',
              source="Walrog, the lord of Water, is #AQUAMARINE#fearsome#LAST# to behold. ...",
              target='乌尔罗格，水之主，是水中的#AQUAMARINE#恐怖#LAST#恶魔。...',
              disposition='advisory',
              note='surface lane-000-0 的 observation 错位挂到下一条 a6090c7e0f；本条 surface 判 OK、无 accepted observation，不能加裁决键。公开 Ashes aquatic-demon.lua:28：is fearsome to behold 是“看上去令人畏惧”，现译“是水中的恐怖恶魔”改变句意。本批记 done，请后续批次或维护者重新覆盖。' + U)]
rows = []
for file in sorted((scratch / 'review283-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 13
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=dict(lane='lane-000-0', entries=['a598376102', 'a6090c7e0f'], fact='observations for lane indexes 13 and 15 (a562167573, a5ef7ca96f) were attached to indexes 14 and 16; checked entry by entry against frozen source/target'),
    additional_host_observations=extra,
    slide_check='all 13 observations checked against their own frozen source/target; two slid by one entry in lane-000-0',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review283-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 19
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 6 and len(pending) == 1
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=6, blocked=1), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (refreeze dlc-location-v1 of full-000, 13 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed.',
                 'lane-000-0 observations for a562167573 and a5ef7ca96f slid one entry onto a598376102 and a6090c7e0f; both refuted on their own revisions, a5ef7ca96f recorded as a host additional observation (a562167573 cone wording matches the implementation).',
                 'The first contextual run (full-000) ran ls /workspace and probed /workspace/tome4-dlcs to find the DLC checkout and was rejected (review283-contextual-0-rejection.json) and archived; the refreeze dlc-location-v1 run with the Ashes checkout was accepted and adjudicated here.',
                 'On aad36f17ae and af350d83cb the translations match the implementation (heal only on the wound source melee hit; on_melee_hit retaliation); upstream info text is broader.',
                 'Osmosis Regeneration (b349784043) joins pending item 23 from batch 278 as item 24; one family rename decision for the user.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Six confirmed repair revisions raise the window 29 backlog from 15 to 21, reaching the threshold of 20; repair window 29 opens after this batch closes.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review283-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=29, window_opened=True, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=15, source='batches 281 (7) and 282 (8)'),
    backlog_after_count=21, default_max_cycles=3,
    source_batches=['batch-6b0d756f5c05a40663fd', 'batch-523380060ecba03a1855', batch],
    excluded='pending named term, advisory, refuted and host additional observation entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第283批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，13个ISSUE（lane-000-0 两条 observation 错位一格，逐条比对）；contextual 首轮 Opus run 为找 DLC checkout 执行 ls /workspace 并探查 /workspace/tome4-dlcs，被拒收并归档，refreeze（dlc-location-v1）run 复核这13条，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决19个观察：{counts}；预计73条完成、6条待修复、1条 pending。'
    '修复 revision：苦痛延伸制表符、恶魔学者背景 often evil、压倒性恐惧效果名（无尽→压倒性）、盾牌附魔换行、恶魔传送 up to/随机/失控、恶魔种子技能使用条件。'
    '炼狱吐息锥形与深渊伤口、深渊气息近战反击均贴合实现 refuted，两条错位观察 refuted（乌尔罗格 fearsome to behold 记宿主补充建议）；恐惧之焰斗篷名记 advisory；渗透吸收同族更名列待用户审阅第24项。'
    '修复窗口29积压从15增至21，达到20，本批闭合后开修复窗口29。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=21), ensure_ascii=False))
