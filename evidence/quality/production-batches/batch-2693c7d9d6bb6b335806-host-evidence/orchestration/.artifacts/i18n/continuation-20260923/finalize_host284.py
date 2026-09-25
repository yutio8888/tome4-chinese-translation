import collections
import json
from pathlib import Path

batch = 'batch-2693c7d9d6bb6b335806'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    'aa2d64b69f': ('refuted', False, '公开 Ashes heart-of-fire.lua:73 移除燃烧的投射为 {type="ball", radius = 10}（硬编码），上游 info（:95）写 radius of 5 与实现不符；现译“半径 10”贴合实现，不改。' + U),
    'b8b4a33d9a': ('advisory', False, '公开 Ashes oppression.lua:104 技能名 Mass Hysteria；现译“恐惧之潮”为本库既定技能名（tome-ashes-urhrok.lua:1279），意译未直译 hysteria，单条不改名，记 advisory。' + U),
    'ba84fb7070': ('confirmed', True, '公开 Ashes lore/demon.lua:414：reverse-engineering the Sher\'Tul portals 是“逆向研究/破解夏·图尔的传送门”；现译“反向驱动”误述所做之事，整句修复（同句 mass-producible artifact 等一并对照）。' + U),
    'bade887035': ('confirmed', True, '公开 Ashes zones/searing-halls/npcs.lua:127 Planar Controller（掌控传送门的恶魔）的 killer_message：and teleported to Mal\'Rok for more experiments；现译“被带去”丢了传送方式，且“做为”应作“作为”，修复为被传送到玛·洛克。' + U),
    'bb5638cb0c': ('refuted', False, '公开 Ashes wrath.lua:32 Obliterating Smash 的 range 为 3 + ceil(is_destroyer/4)，:37 以 radius=self:getTalentRange(t) 作半圆锥半径（info :57 亦称 radius %d semicircle）；变身（timed_effects.lua:105 is_destroyer）增加的 range 就是该半径，现译“增加半径 %d”贴合实现。' + U),
    'bc6203b66b': ('confirmed', True, '公开 Ashes lore/demon.lua:29 lore 名 history of Mal\'Rok (mistranslated)，正文为方括号标注的误译文本，同族 (1)(2)(3) 现译“玛·洛克的历史（1）”等；现译“有关玛·洛克历史的模糊印象”丢了 (mistranslated) 标记并与同族不一致，改为“玛·洛克的历史（误译）”。' + U),
    'bce9bc97c2': ('confirmed', True, '公开 Ashes lore/demon.lua:166–179：fireballs, acidic bursts 为法术，现译“近战火球”增译近战，一级 fidelity；整条对照时另有“他的能力”写死男性代词（原文 these powers，应随 player 代词或改写为中性）。占位符 :capitalize() 在中文代词上为无操作（首字节非 ASCII），去掉不改变输出，不作缺陷。' + U),
    'bee297d916': ('pending', False, '公开 Ashes timed_effects.lua:1045–1052 效果 Corruption of the Doomed 的 +日志；现译“+腐化形态”未表达 of the Doomed，但与待用户审阅第22项（1dafd3a728，同族效果名）同属一次跨条更名决定，列入待审第25项。' + U),
    'bfd436bc1b': ('refuted', False, '公开 Ashes spellblaze.lua:94 callbackOnDealDamage 以 core.fov.distance(...) > 4 硬编码触发距离，与 info 所示 getTalentRadius 无关；现译括注“实际触发范围固定为 4 格，不随该数值变化”贴合实现，不改。' + U),
    'c254cf06e2': ('confirmed', True, '公开 Ashes world-artifacts.lua:158：go out of their way to find more 是“会特意/不惜费力去寻找更多燃料”；现译“知道去哪里寻找”丢了主动寻找的动作，修复该句。' + U),
    'c348419616': ('advisory', False, '公开 Ashes world-artifacts.lua:453–455 引文署名 Cornac demonologist；Demonologist 为 Ashes 职业名，术语表 classes.tsv:37 现译“恶魔使者”（existing），本条沿用职业译名，记 advisory；引文引号缺失一并作为建议记录。' + U),
    'c6e8c8e40e': ('confirmed', True, '公开 Ashes timed_effects.lua:614 long_desc：increasing all damage done by %d%% 是目标自身造成的所有伤害提升；现译“增加 %d%% 全体伤害”易读作对全体目标，主游戏同类效果译“造成的所有伤害”（mod-tome.lua:35064），修复为“造成的所有伤害提升 %d%%”。' + U),
}
contextual = {
    'aa2d64b69f': decisions['aa2d64b69f'],
    'ba84fb7070': ('confirmed', True, decisions['ba84fb7070'][2] + ' contextual 另指 mass-producible artifact 译“工艺品”未表达魔法造物，修复时整句一并处理。'),
    'bc6203b66b': decisions['bc6203b66b'],
    'bce9bc97c2': ('confirmed', True, decisions['bce9bc97c2'][2] + ' contextual 另指 may be capable of 被译成肯定的“足以”、drain energy 增译“生命能量”、ripping away shield 增译“用缴械技能卸下”，修复时整段对照一并处理。'),
    'bfd436bc1b': ('confirmed', True, '公开 Ashes spellblaze.lua:94 以 distance > 4 硬编码触发距离，括注“实际触发范围固定为 4 格”贴合实现，保留（contextual 该点 refuted）；但第三句“离开你范围 %d 码范围”重复“范围”，原文 as long as it remains in radius %d of you，改为“只要它仍在你周围半径 %d 内”一类通顺表述，只改该句。' + U),
}
extra = []
rows = []
for file in sorted((scratch / 'review284-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 12
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 12 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review284-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 17
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 7 and len(pending) == 1
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=72, repair_required=7, blocked=1), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (full-000, 12 entries)'),
             notes=[
                 'All four surface lanes echoed their 20 identities exactly; no group retry was needed; no observation slid.',
                 'The contextual run (full-000) read only its frozen envelope and the v2 contract; no /workspace probing, so no refreeze was needed.',
                 'aa2d64b69f (radius 10 hardcoded at heart-of-fire.lua:73), bb5638cb0c (range is the cone radius) and the fixed 4-tile note on bfd436bc1b match the implementation; upstream info text differs.',
                 '+Corruption of the Doomed (bee297d916) joins pending item 22 from batch 277 as item 25; one family rename decision for the user.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Seven confirmed repair revisions start the window 30 backlog at 7 (window 29 closed with backlog 0); below the threshold of 20.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review284-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=30, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=0, source='window 29 closed (evidence 21078cae)'),
    backlog_after_count=7, default_max_cycles=3,
    source_batches=[batch],
    excluded='pending named term, advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第284批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4个 lane 审80条，identity 回显全部逐位一致，12个ISSUE，无错位；contextual Opus run 复核这12条，未越界，5个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决17个观察：{counts}；预计72条完成、7条待修复、1条 pending。'
    '修复 revision：小恶魔德瑞宝传送研究 reverse-engineering/工艺品、空间控制者击杀信息 teleported、玛·洛克历史（误译）标题、战术简报近战火球/写死“他”/增译手段、唯余灰烬末句“范围”重复、疫火权杖描述主动寻找燃料、腐化之光“全体伤害”。'
    '火焰守护半径10、歼灭挥斩半径、4格触发括注均贴合实现 refuted；恐惧之潮、恶魔使者记 advisory；+腐化形态同族更名列待用户审阅第25项。'
    '修复窗口30积压从0增至7，未达20，继续审核下一批。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=7), ensure_ascii=False))
