import collections
import json
from pathlib import Path

batch = 'batch-5ce6060013cbbb517e2c'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    'dcfd031f93': ('pending', False, '公开 Ashes timed_effects.lua:521–530 OSMOSIS_REGEN 的 -日志 -Osmosis Regen；现译“-渗透吸收”未表达 Regen，但与待用户审阅第23、24项同族（效果名及 +日志统一“渗透吸收”），属一次跨条更名决定，列入待审第26项。' + U),
    'de010befad': ('confirmed', True, '公开 Ashes demon-seeds.lua:56–57 Flame Bolts info：hurls up to %d flame bolts ... to foes in sight（实现 :31–50 以自身为中心 radius 5 的 ball 选取敌对目标后逐个发射 bolt）；现译漏掉目标范围 foes in sight，一级 completeness，补“视野内的敌人”。' + U),
    'de5854b649': ('confirmed', True, '公开 Ashes lore/demon.lua:316 缟玛瑙之子/夸塞魔 lore：现译漏 very much machines, made with bolstered muscles without losing the clever minds、As eager as they are brilliant，well-disciplined and capable in combat 被改成“钢铁般的纪律”，Forge-Giant-produced armor bolted onto their skin 丢了“铆在皮肤上”，towering creations 漏译；整段对照修复。' + U),
    'df20e15744': ('pending', False, '公开 Ashes demon-seeds.lua:689 技能名 Armoured Leviathan；现译“重装上阵”未表达 Leviathan 的巨兽意象，但与待用户审阅第21项（0c451e854a 同名效果）同族，更名须同步技能、效果及 +/- 日志，列入待审第27项。' + U),
    'df5ab19126': ('confirmed', True, '公开 Ashes doom-covenant.lua:146–147 源串续行以 \\n\\t\\t\\t（三个制表符）缩进，现译 \\n\\t\\t，一级 TAB 不变量，只恢复制表符。' + U),
    'e1e7560227': ('advisory', False, '公开 Ashes timed_effects.lua:148–160 RAGING_FLAMES（desc Raging flames，武器燃起火焰）的 -日志 -Revel；现译“-烈焰”与同效果 +日志（tome-ashes-urhrok.lua:1470 “+烈焰”）一致，按效果内容意译，未保留 Revel 字面，记 advisory。' + U),
    'e20983d04a': ('advisory', False, '公开 Ashes timed_effects.lua:156 RAGING_FLAMES 的 +日志 +Revel；与 -Revel 同族均译“烈焰”，按效果内容意译，记 advisory。' + U),
    'e6985dcdec': ('confirmed', True, '公开 Ashes lore/demon.lua:377 锻造巨人 lore 首句 cannot be overstated, except by claiming it to be infinite 是“怎么夸大都不为过——除非说它无限”；现译“没有什么词语比‘无穷无尽’更加合适”意思相反，整段对照修复。' + U),
    'e781f9306f': ('confirmed', True, '公开 Ashes lore/demon.lua:478 里斯丰格 lore：he recovered an intact one 是找回一座完好的传送门，现译“找到了一个未被人使用过的”误作未使用，整段对照修复。' + U),
    'e7f6cac456': ('refuted', False, '公开 Ashes wrath.lua:116–117 爆裂冲锋实现：blast 为 {type="ball", radius=3}（硬编码），t.fireRadius 作为 FIREKNOCKBACK 的 dist（击退距离）传入；info 第二个 %d 即 fireRadius。现译“半径 3 码……击退 %d 码”贴合实现，上游 info 的 radius %d 与实现不符。' + U),
    'e8b56851f1': ('refuted', False, '公开 Ashes timed_effects.lua:597–608 BURNING_PLAGUE callbackOnDeath 以 ball 投射对附近目标重新施加疫火（power×0.75，hasspread 计数上限 spreadcount），无直接爆炸伤害；现译“死亡时疫火将传播到附近的敌人，至多传播2次”贴合实现（与第285批 d4e9fc7ae6 同一机制）。' + U),
    'ea1d8fcb0b': ('confirmed', True, '公开 Ashes demonic-pact.lua:640–700：种子植入按宿主级别 rng.percent(chance) 判定（5/20/50/100%），info 写 a demonic seed tries to take hold；现译“你会将恶魔种子植入目标体内”删了 tries（删限定词类），与后文几率自相矛盾；另源串空行为 \\n\\t\\t\\n，现译为 \\n\\n，一并恢复。dazing 译“眩晕”符合本库 daze=眩晕 惯例，该点不成立。' + U),
    'eb38d586e7': ('confirmed', True, '公开 Ashes world-artifacts.lua:105–110 恐惧之焰（BASE_CLOAK）unided_name cloak shaped flames 是“斗篷状的火焰”；现译“火焰般的斗篷”主体颠倒，修复。' + U),
    'ebb709fd1b': ('confirmed', True, '公开 Ashes demonic-strength.lua:41–42 源串续行 \\n\\t\\t，现译 \\n\\t，一级 TAB 不变量，只恢复制表符。' + U),
    'ee89209326': ('confirmed', True, '公开 Ashes doom-shield.lua:79 info：infuse your shield with the energies of Urh\'Rok；现译“恶魔能量”丢了乌鲁洛克这一神名，一级 fidelity，改为“乌鲁洛克的能量”。' + U),
    'f13d578c10': ('confirmed', True, '公开 Ashes world-artifacts.lua:783–789 黑之锤（The Black Maul，BASE_GREATMAUL）描述 "A fitting weapon for the Champion."；现译“冠军之锤，举重若轻”增译“举重若轻”并丢了引号，修复为带引号的“正配得上冠军的武器”一类。' + U),
    'f3b3b2e5ab': ('confirmed', True, '公开 Ashes torture.lua:182–185 源串 3 处 \\n\\t\\t（宿主实测 3 个 LF），现译 4 处 \\n\\t（多拆一行），一级换行/TAB 不变量，按原文分行恢复。' + U),
    'f402d6591d': ('advisory', False, '公开 Ashes timed_effects.lua:74/493 on_gain 日志以“!”结尾；现译缺句末标点，同文件其余 #Target# 日志多保留“！”，属标点一致性，记 advisory。' + U),
}
contextual = {
    'de010befad': ('confirmed', True, decisions['de010befad'][2] + ' contextual 另指 flame bolts 译“火球”与 bolt 不符；技能名“近战火球”为本库既定名（第285批 advisory），info 内可随整句改为“火焰飞弹”由修复窗口按整条对照处理。'),
    'de5854b649': ('confirmed', True, decisions['de5854b649'][2] + ' contextual 另指 holding the front lines against the hordes of Eyal（抵御埃亚尔大军）、study new magical spells for our arsenal（为我们的武库研究新法术）误译；children of onyx 本条作“玛瑙色的孩子们”，本库其余 7 处统一“缟玛瑙之子”（含同批 e6985dcdec），修复时统一。'),
    'e6985dcdec': ('confirmed', True, decisions['e6985dcdec'][2] + ' contextual 另指 heating raw metal ... then pounding it into their shape 被译成“导入模具”，与后文锤头产出装备冲突；energy-efficient creation 误作“能量燃率”；“父亲大人”为增译；一并修复。'),
    'e781f9306f': ('confirmed', True, decisions['e781f9306f'][2] + ' contextual 另指 too awful to risk inflicting on other test subjects（不愿让其他受试者承担失败后果，故亲自进入）被译成“实施其他实验的失败后果太过危险”，丢了无私动机，一并修复。'),
    'e7f6cac456': ('refuted', False, decisions['e7f6cac456'][2] + ' contextual 所疑“火焰伤害”“包括目标”：DamageType.FIREKNOCKBACK 为火焰伤害，blast friendlyfire=false 且以自身为中心半径 3，目标在内（仅临时 knockback_immune），均贴合实现。'),
    'ea1d8fcb0b': ('confirmed', True, decisions['ea1d8fcb0b'][2] + ' contextual 另指 :700 Implanting a seed into unique demons ... will always try to grant 限定唯一恶魔且为“总会尝试”，现译扩为所有“史诗生物”并写成“必定会获得”；“眩晕 敌人”多一空格；一并修复。'),
    'eb38d586e7': decisions['eb38d586e7'],
    'f13d578c10': decisions['f13d578c10'],
}
extra = []
rows = []
for file in sorted((scratch / 'review286-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 18
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 18 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review286-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 26
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 11 and len(pending) == 2
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=67, repair_required=11, blocked=2), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (full-000, 18 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed; no observation slid.',
                 'The contextual run (full-000) read only its frozen envelope, the v2 contract and its own session tool-result file; no /workspace probing, so no refreeze was needed.',
                 'e7f6cac456 (Detonating Charge hardcodes blast radius 3 and passes fireRadius as knockback distance) and e8b56851f1 (Plaguefire re-spreads on death) match the implementation; upstream info text differs.',
                 '-Osmosis Regen (dcfd031f93) joins pending items 23/24 as item 26; Armoured Leviathan talent name (df20e15744) joins pending item 21 as item 27.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Eleven confirmed repair revisions raise the window 30 backlog from 12 to 23, reaching the threshold of 20; repair window 30 opens after this batch closes.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review286-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=30, window_opened=True, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=12, source='batches 284 (7) and 285 (5)'),
    backlog_after_count=23, default_max_cycles=3,
    source_batches=['batch-2693c7d9d6bb6b335806', 'batch-fa1ef950617bf0290a74', batch],
    excluded='pending named term, advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第286批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，18个ISSUE，无错位；contextual Opus run 复核这18条，未越界，8个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决26个观察：{counts}；预计67条完成、11条待修复、2条 pending。'
    '修复 revision：Flame Bolts info 漏 foes in sight、夸塞魔 lore（漏译与缟玛瑙之子统一）、doom-covenant 三制表符、锻造巨人 lore（cannot be overstated 反译、模具、能耗）、里斯丰格 lore（intact、受试者动机）、'
    '恶魔种子植入（tries/unique demons/空行制表符）、恐惧之焰 unided_name 主体颠倒、demonic-strength 制表符、doom-shield 乌鲁洛克的能量、黑之锤描述增译与引号、灼魂之罚 info 换行。'
    '爆裂冲锋半径与击退、疫火死亡传播均贴合实现 refuted；±Revel“烈焰”与缺叹号记 advisory；-Osmosis Regen 与 Armoured Leviathan 技能名分别列待用户审阅第26、27项。'
    '修复窗口30积压从12增至23，达到20，本批闭合后开修复窗口30。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=23), ensure_ascii=False))
