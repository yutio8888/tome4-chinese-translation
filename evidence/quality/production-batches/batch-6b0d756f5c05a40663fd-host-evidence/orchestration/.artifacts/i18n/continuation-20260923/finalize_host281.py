import collections
import json
from pathlib import Path

batch = 'batch-6b0d756f5c05a40663fd'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'
M = '固定主游戏 624a673 engine/damage_types.lua:1188–1203 FIREBURN 先造成 50% 火焰伤害、余下作 3 回合燃烧。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    '086556871c': ('refuted', False, '公开 Ashes fearfire.lua:75–78 炼狱之门 setEffect(EFF_SENSE, 4)，觉察实际持续 4 回合；现译“4 回合”贴合实现，上游 info 的 3 回合与实现不符。宿主实测换行结构源/译均为 2 个 LF、2 处 \\n\\t\\t。' + U),
    '3f0c3f1b93': ('refuted', False, '公开 Ashes heart-of-fire.lua:113–138 吞噬之焰：扩散前 rng.percent(50)；is_burning 在循环中计算但从未被读取，故不论后者是否燃烧都会扩散；扩散伤害走 FIREBURN。' + M + '现译“50% 几率”“无论后者此前是否在燃烧”“一半立即、另一半 3 回合”均贴合实现，上游 info 与实现不符。' + U),
    '4e2414c680': ('refuted', False, '公开 Ashes lore/demon.lua 的 Champions of Urh\'Rok；本库同族 tome-ashes-urhrok.lua:110（一位乌鲁洛克的精英卫兵）、548（恶魔雕像：乌鲁洛克的精英卫兵）一致作“乌鲁洛克的精英卫兵”，属既定专名，单条不改（同第280批 61c813b980）。' + U),
    '6b24dee87b': ('confirmed', True, '公开 Ashes lore/demon.lua（哈卡祖雕像）：we had designed him to survive this, the fragments merging back … once he reached the surface 是设计意图；现译断言碎片“在到达埃亚尔之后重新融合……组成完整形态”，与下句“无法进行第二阶段——将碎片重组”矛盾。另 reverse-engineer these spells 误作“反制这些咒语”、standard troops 的 standard 被删、too sturdy 误作“太过顽固”，同条整句修复。' + U),
    '72a3b33315': ('confirmed', True, '观察所称“半径 5”不成立：公开 Ashes heart-of-fire.lua:73 火焰守护 project 半径硬编码 10，现译“半径 10”贴合实现须保留。但换行结构被改（宿主实测：源 1 个 LF、1 处 \\n\\t\\t，位于护盾结束句前；译 2 个 LF，在首句后多拆一行），一级换行不变量；同条护盾持续时间“轮”与后文“回合”不一致，一并改为“回合”。' + U),
    '747d29c924': ('confirmed', True, '公开 Ashes 欢迎提示（tformat）：Have fun crushing your foes! 被替换为另一句口号“恶魔之力，毁灭一切！”；a fiery bringer of doom 被改写为“与恶魔共舞的毁灭旅程”，且同条“你/您”混用。按原文恢复“尽情碾碎你的敌人吧！”等并统一称谓，标记与 %s 保持。' + U),
    '78452093a6': ('confirmed', True, '公开 Ashes torture.lua:90–95 焚尽强击说明续行以 \\n\\t\\t 缩进（宿主实测源 4 处 \\n\\t\\t），现译 4 处均为 \\n\\t（一级 TAB 不变量，同第279/280批同类修复），只恢复制表符。' + U),
    '791ae3630d': ('advisory', False, '公开 Ashes 聊天：gave up sea travel ages ago 作“早就放弃海洋了”，语义接近（放弃出海），属措辞取舍，记 advisory。' + U),
    '7975a16239': ('confirmed', True, '公开 Ashes lore/demon.lua（火魔婴雕像）：fuses some of the Eyal-scarred earth … to her hands 是把土壤熔合到双手上，现译“拿在手里”使后文“没有手的话”失去依据；Although the bulk of the ruby species do not pursue this path, instead focusing on magical research and furthering our alteration projects 被改成整族“没有沿着近身厮杀的道路走下去”，丢 bulk 与 alteration projects 并错误概括。同条整句修复。' + U),
    '80546ccc12': ('refuted', False, '公开 Ashes demon-seeds.lua:1011 恶臭吐息 info 的 darkness and flight 为上游笔误，同句伤害为 darkness/blight；现译“黑暗的疫气”按实际伤害类型表达，不改。' + U),
    '80f8794107': ('confirmed', True, '公开 Ashes wrath.lua:160–162 饕餮之刃说明：宿主实测源 1 个 LF、1 处 \\n\\t\\t（位于 Additionally 前）；译 2 个 LF、均为 \\n\\t，并在首句后多拆一行。一级换行/TAB 不变量，只恢复换行与制表符。' + U),
    '84ca86e56a': ('confirmed', True, '公开 Ashes lore/demon.lua:68–74（乌鲁洛克创世史）：then because we could 被译“只能战斗”意思相反；kept the storms entertained 被改成“风暴间唯一的娱乐活动”并增译“神经已经麻木”；Their cities lay hidden among us 被改写并增译“阴毒地对我们偷偷发动袭击”。同条整句修复。' + U),
    '85af2f1f5d': ('advisory', False, '公开 Ashes lore/demon.lua（火焰风暴雕像）：after some controversy 作“在矛盾的抉择后”、Once the portals were unleashed on us 作“当传送门解开后”，语义偏松但不改变所述事件，记 advisory。' + U),
}
contextual = {
    '086556871c': ('refuted', False, decisions['086556871c'][2]),
    '3f0c3f1b93': ('refuted', False, decisions['3f0c3f1b93'][2] + ' observation 自述冻结输入未含实现，宿主已核实现。'),
    '6b24dee87b': decisions['6b24dee87b'],
    '72a3b33315': ('confirmed', True, '观察所称“半径 5”不成立（heart-of-fire.lua:73 硬编码 radius=10，现译贴合实现）；“轮/回合”不一致成立，并入该条换行修复一起改。' + U),
    '7975a16239': decisions['7975a16239'],
    '84ca86e56a': ('confirmed', True, decisions['84ca86e56a'][2] + '另 he had been sealed away, prevented from helping us by people who had been creating the dust storms 的施动关系（制造风暴的人封印了他）被丢失，同条一并修正。'),
}
rows = []
for file in sorted((scratch / 'review281-surface-raw').glob('*.json')):
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
    slid_observations=None,
    slide_check='all 13 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review281-contextual-raw').glob('*.json')):
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
assert len(repair) == 7 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=7), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (full-000, 13 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed.',
                 'The contextual run stayed inside the repo (contract, own envelope, batch source workset); it did not search for the DLC checkout, so no refreeze was needed.',
                 'Surface and contextual observations independently adjudicated against their own frozen revisions.',
                 'On 086556871c, 3f0c3f1b93 and 72a3b33315 the translations match the implementation (EFF_SENSE 4 turns; 50% spread chance with unused is_burning and FIREBURN 50/50 split; radius 10); upstream info text disagrees with code. 72a3b33315 is confirmed only for host-measured newline structure plus the 轮/回合 unit.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Seven confirmed repair revisions start the window 29 backlog at 7 (window 28 closed at 0883a3f8); threshold 20 not reached.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review281-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=29, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=0, source='window 28 closed (evidence 0883a3f8)'),
    backlog_after_count=7, default_max_cycles=3,
    source_batches=[batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第281批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，13个ISSUE；contextual Opus run 复核这13条，未越界，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决19个观察：{counts}；预计73条完成、7条待修复。'
    '修复 revision：哈卡祖雕像传说（设计意图写成事实等）、火焰守护换行与“轮/回合”（半径 10 贴合实现须保留）、欢迎提示末句与称谓、焚尽强击与饕餮之刃制表符/换行、火魔婴雕像传说（熔手、bulk）、乌鲁洛克创世史（because we could 等）。'
    '炼狱之门 4 回合、吞噬之焰扩散机制、恶臭吐息笔误、乌鲁洛克的精英卫兵专名 refuted（译文贴合实现或既定专名）；出海、火焰风暴雕像两条记 advisory。修复窗口29积压从0增至7，未达20。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=7), ensure_ascii=False))
