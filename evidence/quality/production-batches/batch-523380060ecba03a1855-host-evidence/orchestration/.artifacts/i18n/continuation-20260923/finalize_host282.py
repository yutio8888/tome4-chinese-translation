import collections
import json
from pathlib import Path

batch = 'batch-523380060ecba03a1855'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'
M_unused = '固定主游戏 624a673 engine/damage_types.lua:1188–1203 FIREBURN 先造成 50% 火焰伤害、余下作 3 回合燃烧。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    '880a05d14d': ('confirmed', True, '公开 Ashes oppression.lua:72–81 骇人打击仅在 callbackOnMeleeAttack 且 hitted 时施加 EFF_INFERNAL_FEAR；现译“你的攻击能够惊吓目标”丢了“近战命中”限定。另宿主实测源 5 个 LF、5 处 \\n\\t\\t（含末尾 \\n\\t\\t），译 4 个 LF、均为 \\n\\t 且无末尾缩进，一级换行/TAB 不变量。同条整句修复。' + U),
    '886c20b244': ('refuted', False, '公开 Ashes timed_effects.lua:288–295 PURIFIED_BY_FIRE，desc 为 Cleansing flames、subtype fire，on_lose 即本串；“火焰净化结束了”贴合效果本身，不改。' + U),
    '89a4d5c92f': ('confirmed', True, '公开 Ashes world-artifacts.lua:589 黑之冠 desc 为带引号的俏皮话 "For the demon who has everything."（送给应有尽有的恶魔），现译另起口号“魔中之魔，加冕为王”且丢引号，含义不符。' + U),
    '8c1bab1ad2': ('advisory', False, '公开 Ashes races.lua:100 魔化精灵种族技能；本库 tome-ashes-urhrok.lua:1412 既定名“强韧”，单条不改名，记 advisory。' + U),
    '8cc43b0e6e': ('advisory', False, '公开 Ashes world-artifacts.lua:555 实验头盔说明：“提高魔化精灵的能力”对 enhance the effects of the Doomelf corruption 概括偏松但不改变含义，记 advisory。' + U),
    '8d7b289755': ('confirmed', True, '公开 Ashes torture.lua:146 源串为单行（宿主实测 0 个 LF），现译在两句间插入 \\n\\t，一级换行不变量，只删多余换行。' + U),
    '8dcc6c29ec': ('refuted', False, '公开 Ashes demon-seeds.lua:666 腐蚀锥 tg 未设 friendlyfire=false，固定主游戏 624a673 engine/Target.lua:682 默认 friendlyfire=true，锥形会波及友方；上游 info 的 all enemies 与实现不符，现译不写“所有敌人”反而贴合实现，不改。' + U),
    '8ead585688': ('confirmed', True, '公开 Ashes unlock-race_doomelf.lua:21–31：“烈火”为增译（honed by their rigorous training on the Fearscape）；the truth 被具体化为“有关埃亚尔大陆的真相”；have earned the right to make Doomelf characters 被改成“应运而生”丢了解锁含义；Instant cast phase door 被改成“使用加速技能，瞬间穿梭空间”。同条整句修复，换行与颜色标记保持。' + U),
    '90ae8f40d2': ('confirmed', True, '公开 Ashes world-artifacts.lua:430–435 小鬼之爪 unided_name “red, mottled claw”，现译“红色的爪子”丢 mottled（斑驳），补“斑驳”。' + U),
    '919188331c': ('advisory', False, '公开 Ashes world-artifacts.lua:80；“歼灭挥斩”为本库既定技能名（tome-ashes-urhrok.lua:1355），记 advisory 不改名。' + U),
    '952fa9c1b8': ('advisory', False, '公开 Ashes wrath.lua:23/191；本库 tome-ashes-urhrok.lua:1355 既定名“歼灭挥斩”，单条不改名，记 advisory。' + U),
    '958319eb5e': ('advisory', False, '公开 Ashes races.lua:119；本库 tome-ashes-urhrok.lua:1416/1644 既定名“腐化形态”，单条不改名，记 advisory。' + U),
    '9ac85a7a89': ('confirmed', True, '公开 Ashes ashes-urhrok-walrog-pop.lua:49–53：%s 由 _t"Traitor"/_t"Murderer" 填入，“%s to the Naloren”应为“纳鲁精灵的%s”，现译“%s纳鲁精灵”缺“的”；Your \'loyalty...\' would give me their fate 意为信你的“忠诚”只会落得他们的下场，现译“还能骗得了谁？”不符；“巨大的身形”为增译。另宿主实测源 4 个 LF、译 3 个 LF，scowl. 后换行被并掉，一级换行不变量。同条整句修复。' + U),
    '9d7afbedda': ('confirmed', True, '公开 Ashes world-artifacts.lua:780–788 黑色巨锤 color=colors.BLACK，unided_name “massive black hammer” 无材质；“黑曜石”为增译（黑曜石属黑之冠 cracked obsidian crown），改回“黑色”。' + U),
    '9e25a17b1f': ('confirmed', True, '公开 Ashes ashes-urhrok-walrog-pop.lua:33 回答选项 The chaos and death ends now!，现译“邪恶与混沌”把 death 换成“邪恶”，改为“混沌与死亡”。' + U),
    '9e32f9dfdf': ('refuted', False, '公开 Ashes world-artifacts.lua:450–492 命运之轮 base 为 BASE_RING，“重置戒指属性”中 item 具体化为戒指贴合实体，不改。' + U),
}
contextual = {k: decisions[k] for k in ('880a05d14d', '89a4d5c92f', '8ead585688', '9ac85a7a89', '9d7afbedda')}
rows = []
for file in sorted((scratch / 'review282-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 16
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='all 16 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review282-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 21
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 8 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=72, repair_required=8), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (refreeze dlc-location-v1 of full-000, 16 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed.',
                 'The first contextual run (full-000) enumerated /workspace outside its boundary and was rejected (review282-contextual-0-rejection.json) and archived; the refreeze dlc-location-v1 run with the Ashes checkout was accepted and adjudicated here.',
                 'Surface and contextual observations independently adjudicated against their own frozen revisions.',
                 'On 8dcc6c29ec the translation matches the implementation (cone tg has no friendlyfire=false, so it can hit allies); upstream info text says all enemies.',
                 'Talent names 8c1bab1ad2, 952fa9c1b8, 958319eb5e and the 919188331c reference are established library names; advisory only.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Eight confirmed repair revisions raise the window 29 backlog from 7 to 15; threshold 20 not reached.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review282-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=29, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=7, source='batch 281 (c5035e03)'),
    backlog_after_count=15, default_max_cycles=3,
    source_batches=['batch-6b0d756f5c05a40663fd', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第282批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，16个ISSUE；contextual 首轮 Opus run 越界枚举 /workspace 被拒收并归档，refreeze（dlc-location-v1）run 复核这16条，5个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决21个观察：{counts}；预计72条完成、8条待修复。'
    '修复 revision：骇人打击（近战命中限定、换行/制表符）、黑之冠 desc、折磨类技能多余换行、魔化精灵解锁文本（真相/资格/瞬发相位门/烈火）、小鬼之爪 mottled、沃尔罗格对话（叛徒的、忠诚句、换行）、黑色巨锤材质、混沌与死亡。'
    '火焰净化、腐蚀锥（实现会波及友方）、命运之轮（戒指）refuted；强韧、歼灭挥斩、腐化形态等既定名与实验头盔说明记 advisory。修复窗口29积压从7增至15，未达20。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=15), ensure_ascii=False))
