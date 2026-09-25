import collections
import json
from pathlib import Path

batch = 'batch-99f8a711d02012a6de19'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    '3bd78dce70': ('confirmed', True, '公开 Ashes talents/corruptions/wrath.lua:132–134 爆裂冲锋说明的两个后续行均以 \\n\\t\\t 缩进，现译两处改为 \\n\\t（一级 TAB 不变量，与窗口27 wrath.lua 同类修复一致）；文字内容本身无误，只恢复两个制表符。' + U),
    '3c496fb546': ('confirmed', True, '公开 Ashes world-artifacts.lua:178–188 疫火权杖的使用效果是 type="bolt"、range=5 的指向性弹道，命中后施加 BURNING_PLAGUE；现译“召唤出一团疫火”把发射弹道改成召唤，误导使用方式。本库同类 fire a bolt 均译“发射”。' + U),
    '3d80f4a586': ('confirmed', True, '公开 Ashes achievements/all.lua:59–66 的 can_gain 统计 game.party.m_list 中 type/subtype 为 demon 的成员不少于 5 个；条件是队伍组成，现译“同时召唤至少5个恶魔”改成一次召唤动作。' + U),
    '3ddfbf1e99': ('refuted', False, '公开 Ashes doom-covenant.lua:67 getDieAt 为正值，timed_effects.lua:805、822 以 -(stacks*die_at) 写入 die_at，效果说明亦显示为负生命；现译“-%d 生命底限”与实现一致，负号不是增译。两处 \\n\\t\\t 均保留。' + U),
    '4130b80959': ('confirmed', True, '公开 Ashes zones/searing-halls/npcs.lua:126 空间控制者描述：towers above you 是高耸于你面前，现译“朝你走来”增添动作；in the nearby Fearscape area 被删，只剩“附近所有的传送门”。' + U),
    '43134b3dae': ('confirmed', True, '公开 Ashes lore/demon.lua:404（毁灭女妖雕像）：portals ... will occasionally emit a shade 是传送门偶尔放出亡魂，现译“附近经常徘徊着灵魂”把偶尔改成经常、把放出改成徘徊（删限定词缺陷类）；our scouting parties 亦被写成“埃亚尔探险队”。' + U),
    '435ca9b749': ('confirmed', True, '公开 Ashes heart-of-fire.lua:143–144 吞噬之焰说明第二行以 \\n\\t\\t 缩进，现译为 \\n\\t（一级 TAB 不变量），只恢复制表符。observation 的机制部分不成立：heart-of-fire.lua:116–137 实为 rng.percent(50)、跳过已受诅咒者、is_burning 计算后未使用，伤害走 FIREBURN（固定主游戏 624a673 damage_types.lua:1187–1201 首发 50%、余量 3 回合燃烧），现译贴合实现，保留。' + U),
    '46fd21dfbe': ('advisory', False, '公开 Ashes world-artifacts.lua:621 黑之核 desc 为带引号的格言；现译“锁住灵魂，死亡莫及。”语义完整。同文件同族格言（tome-ashes-urhrok.lua:213–241）八条中七条现译均不带引号，引号不是运行时标记；是否全族统一加引号属风格，不单条修复。' + U),
    '4b928dc676': ('advisory', False, '公开 Ashes world-artifacts.lua:825 黑之墙 desc 为带引号的格言；现译“披坚持盾，众莫能伤”语义与盾牌物品相符。引号与句号的省略沿用同族格言惯例，不单条修复。' + U),
    '4dd916e4cb': ('refuted', False, '公开 Ashes lore/demon.lua:52 的 convert ambient magic into caloric energy；“热量”在中文本就兼指食物热量，现译“把环境中的魔力转化为热量能量”不构成误译，属措辞偏好。' + U),
}
contextual = {
    '3c496fb546': decisions['3c496fb546'],
    '3d80f4a586': decisions['3d80f4a586'],
    '4130b80959': decisions['4130b80959'],
    '43134b3dae': decisions['43134b3dae'],
    '435ca9b749': ('refuted', False, '公开 Ashes heart-of-fire.lua:116–137 的实现：每回合对半径 10 内带诅咒之焰的敌人 rng.percent(50) 判定，向半径 1 内尚未受诅咒者传播（is_burning 计算后未被读取，燃烧与否不影响），伤害经 FIREBURN 结算（固定主游戏 624a673 damage_types.lua:1187–1201：首发 50%，余量 3 回合燃烧）。现译贴合实现而非上游英文，按实现为准不修；制表符问题由 surface 行单独确认。' + U),
    '4dd916e4cb': ('confirmed', True, '公开 Ashes lore/demon.lua:30–61 的 lore 在最后一段后以换行结束（源文 31 个 LF，实测），现译缺末尾 LF（30 个，实测）；一级换行不变量，与既有 Exploit Weakness 结尾换行修复同类。其余空行下标与 187 对标记一致。' + U),
}
rows = []
for file in sorted((scratch / 'review279-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 10
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='all 10 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review279-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 16
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 7 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=7), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (1 run, 10 entries)'),
             notes=[
                 'Surface and contextual observations independently adjudicated against their own frozen revisions.',
                 'The contextual scope was the 10 surface ISSUE revisions; it added one new objective finding (4dd916e4cb trailing LF) on a revision whose surface observation was refuted.',
                 'Contextual OK does not erase the confirmed surface TAB finding on 3bd78dce70.',
                 'On 435ca9b749 the translation follows the implementation rather than the upstream English; only the tab indentation is repaired.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Seven confirmed repair revisions raise the window 28 backlog from 6 to 13; threshold 20 is not reached.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review279-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=28, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=6, source='batch-2dd6d21e34b360ebb6d9 (278)'),
    backlog_after_count=13, default_max_cycles=3,
    excluded='pending named term, advisory and historical blocked entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第279批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个lane审80条，10个ISSUE；contextual 1个Opus run复核10条，6个ISSUE。'
    '全部5个child的原生读取边界已核对并确认归档；Opus 有两次仅元数据探测（行数、路径列表），已如实记录。\n\n'
    f'宿主裁决16个观察：{counts}；预计73条完成、7条待修复。'
    '七个修复revision为：爆裂冲锋说明制表符、疫火权杖“召唤”应为发射、恶魔狂欢！成就条件、空间控制者描述、毁灭女妖雕像传说频率与动作、吞噬之焰说明制表符（机制译文贴合实现，保留）、玛·洛克历史传说末尾换行。'
    '黑之核、黑之墙格言引号记 advisory。修复窗口28积压从6增至13，未达20，继续审核。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=13), ensure_ascii=False))
