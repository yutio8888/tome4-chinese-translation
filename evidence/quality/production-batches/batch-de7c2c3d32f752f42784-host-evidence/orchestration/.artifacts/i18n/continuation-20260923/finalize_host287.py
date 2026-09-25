import collections
import json
from pathlib import Path

batch = 'batch-de7c2c3d32f752f42784'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    'dff6969913': ('refuted', False, '公开 Ashes spellblaze.lua:92 唯余灰烬触发判定 core.fov.distance(...) > 4 then return（硬编码 4 格），info 的半径 %d 与实现不符；现译括注“实际触发范围固定为 4 格”贴合实现，与第284批裁决一致，保留。' + U),
    'f684bba995': ('advisory', False, '公开 Ashes lore/demon.lua:492 达莱奇 lore 末句 it will prove effective on the surface of Eyal；现译“它会前往埃亚尔大陆证明他的实际效果”略有增译（前往/证明）且以“他”指代样本，但未改变“将在埃亚尔地表发挥作用”的要义，记 advisory。' + U),
    'f6eee01b5c': ('confirmed', True, '公开 Ashes infernal-combat.lua:171–184 恶魔之角：DEMONIC_CUT 每回合伤害 dam*0.5/5（即所造成伤害的 50%% 分 5 回合，DamageType.DARKNESS），治疗在 timed_effects.lua:683 callbackOnMeleeHit（近战命中流血中的目标）。现译“每次你攻击被恶魔角刺穿的目标时”丢近战与“流血期间”限定，“合计受到额外 50%% 黑暗伤害”丢“所造成伤害的”比例基准，且 darkness 应为本库伤害类型名“暗影”（mod-tome.lua:6894）。整句按原文修复，\\n\\t\\t 结构保持；此即窗口30 记下的 1240 行同条。' + U),
    'f746ce383c': ('confirmed', True, '公开 Ashes lore/demon.lua:187–197 战术简报（template）：源文 10 个 LF、以 \\n\\n 结尾，现译 9 个 LF 缺末尾空行（一级 LF 不变量）；“他的隐身和暗影爆炸”写死“他”而本条其余均用 player 代词；Our standard alterations have synergized with this Shalore\'s natural reactive magic 误作“调整了永恒精灵天赋的加速能力…并在传送后大幅提升闪避能力”；the resilience alterations we gave him 误作“在恶魔空间的试炼增强了…韧性”；poisons, flames, and the like 泛化为“异常状态”；beat him until he stops moving 弱化为“直到其放弃移动”；末句 it is unlikely we will see any casualties 删限定作“不会受到什么损失”。整段对照修复。' + U),
    'f985ec15c0': ('confirmed', True, '公开 Ashes black-magic.lua:96 无情未来 remove = math.min(eff.stacks, t:_getStack(self))，info consume up to %s stacks 为上限；现译“消耗 %s 层叠加效果”删“至多”，把上限写成定额（删限定词缺陷类），改“至多消耗 %s 层”。' + U),
    'f9e45b5a07': ('confirmed', True, '公开 Ashes heart-of-fire.lua:56–58 燃烧献祭源串续行 \\n\\t\\t（两处），现译 \\n\\t，一级 TAB 不变量，只恢复制表符。' + U),
    'fb23faa260': ('pending', False, '公开 Ashes timed_effects.lua:638 ARMOURED_LEVIATHAN 的 -日志 -Armoured Leviathan；现译“-重装上阵”与待用户审阅第21、27项同族（技能/效果/±日志统一“重装上阵”），更名属跨条决定，列入待审第28项。' + U),
    'fb28924d4a': ('refuted', False, '公开 Ashes timed_effects.lua:861 BLACKICE long_desc You have %d charges. 以 eff.stacks 填充（charges = eff.stacks，on_merge 叠加至 max_stacks 3），charges 即叠加层数；现译“叠加次数：%d。”贴合实现。' + U),
    'fc65680ae7': ('confirmed', True, '公开 Ashes lore/demon.lua:309 小水怪 lore：a prime location for carrying out covert operations 被译成“我们的藏身的主要根据地”（丢秘密行动且不通），experiments too dangerous to perform on our own soil 误作“对于我们的土壤来说过于危险”，As our scouts and servants beneath the seas 只剩“使者”，pay tribute 误作“奉上礼物”（应为致敬/铭记）。整段对照修复。' + U),
    'fc8cdfb222': ('confirmed', True, '公开 Ashes brutality.lua:120–122 炙炎之牢源串续行 \\n\\t\\t（两处），现译 \\n\\t，一级 TAB 不变量，只恢复制表符。' + U),
    'fc9cbd5243': ('pending', False, '公开 Ashes timed_effects.lua:1042 CORRUPTION_OF_THE_DOOMED 效果名 Corruption of the Doomed；现译“腐化形态”未表达 Doomed，但与待用户审阅第22、25项同族（效果名及 ±日志统一“腐化形态”），更名属跨条决定，列入待审第29项。' + U),
    'fdf0fd6913': ('refuted', False, '公开 Ashes spellblaze.lua:21–58 Rain of Fire 实现以 "meteor" 粒子与 DamageType.METEOR 在周围随机落点投射（info：at most two meteors will fall near you per turn），“陨星火雨”贴合实现且为本库既定技能名。' + U),
    '00b0f993a3': ('confirmed', True, '公开 Cults init.lua:28–31 插件描述三行，源文 3 个 LF（首句后换行），现译 2 个 LF 把前两段并成一行（一级 LF 不变量）；horribly mutated and partly insane 的 partly 被删成“进入了疯狂之中”（删限定词缺陷类）。恢复首处换行并译出“半疯/神志部分失常”。' + U),
    '00d110ae42': ('refuted', False, '公开 Cults timed_effects.lua:1063–1072 Mark of Treason callbackOnHit：linked_damage = cb.value*eff.power/100 由链接源承受，日志 (%d linked) 的 %d 即经链接转移的伤害；现译“(%d 伤害链接)”点明伤害，贴合实现。' + U),
    '01bdde5133': ('confirmed', True, '公开 Cults timed_effects.lua:2330 on_gain #Target# is bolstered at the sight of the horror!：该效果 beneficial（护甲加成），看见恐魔的是 #Target#；现译“在恐魔的视线中被强化了”把观看者颠倒成恐魔，一级 fidelity，改“#Target#目睹恐魔，士气大振！”一类。' + U),
}
contextual = {
    'f6eee01b5c': ('confirmed', True, decisions['f6eee01b5c'][2] + ' contextual 同指跨条“黑暗伤害”与同批“暗影伤害”不一致、近战与流血期间条件及“所造成伤害的 50%”比例丢失。'),
    'f746ce383c': ('confirmed', True, decisions['f746ce383c'][2] + ' contextual 同指写死“他”、加速/传送后增译、试炼改变施加者、异常状态泛化与“放弃移动”弱化。'),
    'f985ec15c0': ('confirmed', True, decisions['f985ec15c0'][2] + ' contextual 同指 t.getStack 为上限。'),
    'fc65680ae7': ('confirmed', True, decisions['fc65680ae7'][2] + ' contextual 同指 pay tribute、斥候与秘密行动。'),
    '00b0f993a3': ('confirmed', True, decisions['00b0f993a3'][2] + ' contextual 同指首处换行与 partly。'),
    '01bdde5133': ('confirmed', True, decisions['01bdde5133'][2] + ' contextual 同指观看者颠倒，且效果 subtype horror/armor 提供 flat_damage_armor。'),
}
extra = []
rows = []
for file in sorted((scratch / 'review287-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 15, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 15 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review287-contextual-raw').glob('*.json')):
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
assert len(repair) == 8 and len(pending) == 2
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=70, repair_required=8, blocked=2), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (8 lanes in 2 groups: Ashes 61 + Cults 19)',
                            contextual='claude/claude-opus-5-5 (full-000 Ashes 12 entries, full-001 Cults 3 entries)'),
             notes=[
                 'First mixed Ashes+Cults batch: surface split into groups surface-000 (4 lanes, 61) and surface-001 (4 lanes, 19); every lane echoed its identities exactly; no group retry; no observation slid.',
                 'Both contextual runs read only their frozen envelope and the v2 contract (full-000 also grepped its own envelope for a checkout field); no /workspace probing, so no refreeze was needed.',
                 'dff6969913 (Only Ashes Left 4-tile check), fb28924d4a (Blackice charges = stacks), fdf0fd6913 (Rain of Fire drops meteors) and 00d110ae42 (linked damage) match the implementation.',
                 '-Armoured Leviathan (fb23faa260) joins pending items 21/27 as item 28; Corruption of the Doomed (fc9cbd5243) joins items 22/25 as item 29.',
                 'f6eee01b5c is the demon-horns entry noted during repair window 30 (tome-ashes-urhrok.lua:1240); it is now batch-adjudicated and counted once.',
                 'Ashes and Cults public source file SHA matched this batch workset; source repositories and commits remain unpinned.',
                 'Eight confirmed repair revisions make the window 31 backlog 8 (the host-noted 1240 entry is the same revision), below the threshold of 20; review continues with batch 288.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review287-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=31, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=1, source='host note from repair window 30 FINAL(3): tome-ashes-urhrok.lua:1240 demon horns (same revision as f6eee01b5c)'),
    backlog_after_count=8, default_max_cycles=5,
    source_batches=[batch],
    excluded='pending named term, advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第287批：冻结80条（Ashes 61、Cults 19），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 分两组共 8 个 lane，identity 回显全部逐位一致，15个ISSUE，无错位；contextual Opus 两个 run（Ashes 12、Cults 3）复核，未越界，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决21个观察：{counts}；预计70条完成、8条待修复、2条 pending。'
    '修复 revision：恶魔之角（近战/流血期间条件、伤害比例、暗影伤害）、战术简报（末尾空行、写死“他”、改造与韧性来源误译、unlikely 删限定）、'
    '无情未来 up to、燃烧献祭与炙炎之牢制表符、小水怪 lore（秘密行动、己方土地、斥候、致敬）、Cults 插件描述（首处换行、partly）、Cults 恐魔鼓舞日志观看者颠倒。'
    '唯余灰烬 4 格括注、Blackice charges、陨星火雨、链接伤害均贴合实现 refuted；达莱奇 lore 末句记 advisory；-Armoured Leviathan 与 Corruption of the Doomed 分别列待用户审阅第28、29项。'
    '修复窗口31积压为8（窗口30 记下的 1240 行即 f6eee01b，同一 revision 只计一次），未达20，继续审核第288批。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=8), ensure_ascii=False))
