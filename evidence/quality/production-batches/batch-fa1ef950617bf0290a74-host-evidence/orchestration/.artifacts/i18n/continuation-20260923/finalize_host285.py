import collections
import json
from pathlib import Path

batch = 'batch-fa1ef950617bf0290a74'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    'cc71bc2cab': ('advisory', False, '公开 Ashes achievements/all.lua:21–29 成就 A Fist Full of Demons 条件为击杀 1000 个恶魔（desc Killed 1000 demons.）；现译“恶魔杀戮者”未保留 fist full 的双关，但贴合成就条件，且与上游官方 zh_hans 语言包（data/locales/zh_hans.lua:5）一致，为本库既定成就名，记 advisory。' + U),
    'cdac06c979': ('confirmed', True, '公开 Ashes world-artifacts.lua:190–198 死亡之刃（Dethblyd）描述：He wasn\'t known for his subtlety of naming 是调侃剑名 Dethblyd 起得直白，but there\'s no denying the power of his massive sword；现译“从不擅长谋略”“他的力量无以伦比”误解命名梗并丢了巨剑，整句修复。' + U),
    'ce3b54895d': ('advisory', False, '公开 Ashes lore/demon.lua:105–125 遗失的记忆（1）：四处 <?=_t(player.descriptor.subrace, ...)?> 指与玩家同种族的另一名受试者，现译以“同族”“他”指代，语义保持（the other one 在原文中亦以 he 指代），模板表达式省略不改变显示含义，记 advisory。' + U),
    'd393910508': ('advisory', False, '公开 Ashes demon-seeds.lua:23–50 Flame Bolts 为被动：callbackOnMeleeAttack 近战命中时按几率向范围内敌人发射火焰飞弹（type="bolt"）；现译“近战火球”为本库既定技能名（tome-ashes-urhrok.lua:781），“近战”对应触发条件，“球”与 bolt 不完全贴合，单条不改名，记 advisory。' + U),
    'd3c0b76c51': ('confirmed', True, '公开 Ashes fearfire.lua:121–123 源串两处分隔均为 \\n\\t\\t（宿主实测源 2 个 LF），现译为 \\n\\t 与 \\n\\n，一级换行/TAB 不变量，恢复为两处 \\n\\t\\t。' + U),
    'd3db2e0afe': ('confirmed', True, '公开 Ashes world-artifacts.lua:737–743 黑之铠（The Black Plate）描述 "Wreckage all about you. Is there anything left inside?"：残骸在“你周围”，并追问甲内是否还剩什么；现译“己身若残，何物能存？”把残骸移到自身并丢了引号，修复。' + U),
    'd3e2c5ca56': ('advisory', False, '公开 Ashes torture.lua:108 技能 Abduction（命中后把目标拉到身边再次攻击）；现译“锁魂之链”为本库既定技能名（tome-ashes-urhrok.lua:1335，同族变身加成亦用此名），意译未直译“掳走”，单条不改名，记 advisory。' + U),
    'd4e9fc7ae6': ('refuted', False, '公开 Ashes timed_effects.lua:575–608 BURNING_PLAGUE（瘟疫之焰）callbackOnDeath：以半径 range 的 ball 投射，对附近目标重新施加 BURNING_PLAGUE，power=eff.power*eff.explosion（0.75），无直接爆炸伤害；现译“以更弱的强度传播到附近目标”贴合实现，上游 info 的 explode 较笼统。' + U),
    'dac57e56ba': ('confirmed', True, '公开 Ashes lore/demon.lua:212–229 轨道基地战斗情报便条：like the pen was rapidly jerked away 是笔被猛地拽走，现译“笔从手上滑落”；double-bladed katana 漏“双刃”，giant construct labelled 漏“巨型构装体”，interrupted this demon\'s writing 被改成“吓尿了”，target\'s 写死为“他的”（应随 player 或改中性），isolating 被改成“启动最高优先级措施”，整段对照修复。' + U),
}
contextual = {
    'cdac06c979': ('confirmed', True, decisions['cdac06c979'][2] + ' contextual 另指错字“无以伦比”应为“无与伦比”，修复时一并处理。'),
    'ce3b54895d': ('confirmed', True, '公开 Ashes lore/demon.lua:114–125 遗失的记忆（1）（宿主实测源文）：两处 patch him up 是“给他疗伤”，现译“把他带走”“带下去”与后文伤口愈合矛盾；it missed your eyes（酸液没溅到眼睛，所以你还看得见）被译成“他漏看了你的眼睛”；Structural damage subpar 漏译 subpar（低于预期，正是对方失望的原因）；your skin still bubbles 被译成“仍在颤抖”。一级 fidelity，整段对照修复；subrace 模板以“同族”指代保持不变（surface 该点 advisory）。' + U),
    'd393910508': ('advisory', False, decisions['d393910508'][2] + ' contextual 依 range=5 认为是远程技能，但同文件 :32 callbackOnMeleeAttack 表明由近战攻击触发，“近战”有实现依据；bolt≠球的偏差照记 advisory。'),
    'd4e9fc7ae6': ('refuted', False, decisions['d4e9fc7ae6'][2] + ' contextual 因冻结片段未含 on-death 实现而存疑，宿主已核 callbackOnDeath（:597–608）。'),
    'dac57e56ba': ('confirmed', True, decisions['dac57e56ba'][2] + ' contextual 另指 Blow all connectors 被弱化成“关闭”，应为炸毁，一并修复。'),
}
extra = []
rows = []
for file in sorted((scratch / 'review285-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 9
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 9 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review285-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 14
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 5 and len(pending) == 0
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=75, repair_required=5), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (full-000, 9 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed; no observation slid.',
                 'The contextual run (full-000) read only its frozen envelope and the v2 contract; no /workspace probing, so no refreeze was needed.',
                 'd4e9fc7ae6 (Plaguefire on death re-applies itself at 0.75 power) matches the implementation; contextual lacked the callbackOnDeath excerpt and the host verified it.',
                 'd393910508 Flame Bolts keeps the established name 近战火球: the talent triggers from melee attacks (callbackOnMeleeAttack) even though its bolts have range 5.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Five confirmed repair revisions raise the window 30 backlog from 7 to 12; below the threshold of 20.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review285-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=30, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=7, source='batch 284 (7)'),
    backlog_after_count=12, default_max_cycles=3,
    source_batches=['batch-2693c7d9d6bb6b335806', batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第285批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，9个ISSUE，无错位；contextual Opus run 复核这9条，未越界，5个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决14个观察：{counts}；预计75条完成、5条待修复。'
    '修复 revision：死亡之刃描述命名梗与巨剑、遗失的记忆（1）patch him up/眼睛/subpar/bubbles、灵魂焚净换行制表符、黑之铠描述残骸位置与引号、轨道基地战斗情报便条（笔被拽走、双刃、巨型构装体、打断书写、炸毁连接、隔离、写死“他”）。'
    '瘟疫之焰死亡传播贴合实现 refuted；恶魔杀戮者、近战火球、锁魂之链记 advisory。'
    '修复窗口30积压从7增至12，未达20，继续审核下一批。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=12), ensure_ascii=False))
