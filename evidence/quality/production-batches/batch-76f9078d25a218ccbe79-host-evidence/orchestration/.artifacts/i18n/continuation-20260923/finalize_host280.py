import collections
import json
from pathlib import Path

batch = 'batch-76f9078d25a218ccbe79'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
U = '本批文件 SHA 匹配，来源仓库/commit 未固定。'

# Each observation is decided against its own frozen revision and source file.
decisions = {
    '54a6a1b06c': ('confirmed', True, '公开 Ashes overload/data/chats/ashes-urhrok-walrog-pop.lua:39–42：乌尔罗格的理由是迟早要上到地面、那时你可能更强，所以不必再等；现译“与其到时候再打败你”丢掉 you may be stronger then 这一理由并改写因果，come to the surface 夸大为“君临大地”。' + U),
    '54ef1fbfc9': ('confirmed', True, '公开 Ashes demonic-strength.lua:94–95 恶魔之血说明第二行以 \\n\\t\\t 缩进，现译为 \\n\\t（一级 TAB 不变量，同第279批同类修复），只恢复制表符。' + U),
    '55bb0228d5': ('confirmed', True, '公开 Ashes demon-seeds.lua:1144–1175 烈焰突袭的 target 为 beam、只设 selffire=false；固定主游戏 624a673 engine/Target.lua:649–682 friendlyfire 默认 true，ActorProject.lua:255 仅在其为假时跳过友方，故路径上友方也受火焰伤害并计入活力回复。现译“任何路径上的敌人”把 Any creature 收窄为敌人。' + U),
    '55dedd2404': ('confirmed', True, '公开 Ashes lore/demon.lua:151–157 全文以性别宏指代玩家；现译两处写死“他”：“阻止他冲破重围”（源为 <?=player:he_she()?>）、“将他打成马蜂窝”（源为 <?=player:him_her()?>），女性角色显示错误（一级占位符不变量；实测源 27 个宏、译 24 个）。he_she():capitalize() 在中文无大小写意义，不单独计。' + U),
    '5666e9d827': ('confirmed', True, '公开 Ashes lore/demon.lua:370（乌鲁洛克的精英卫兵雕像）：forest of pillars 被写成“复杂迷宫”；not born in the conventional manner 增译“天才”；performing adequately 被拔高为“相当出色”。' + U),
    '59e30b6e11': ('refuted', False, '公开 Ashes world-artifacts.lua:299–345 以 confusion_immune/stun_immune/pin_immune/silence_immune 部分值实现“状态抗性”；本库既定惯例把 *_immune 百分比作“免疫”（指南 6.3），现译“状态免疫”与同族一致。' + U),
    '5b6924a79d': ('confirmed', True, '公开 Ashes oppression.lua:247–248 绝望碾压说明第二行以 \\n\\t\\t 缩进，现译为 \\n\\t（一级 TAB 不变量），只恢复制表符。' + U),
    '5de8bdb19c': ('advisory', False, '公开 Ashes birth/doomelf.lua:27–32 魔化精灵锁定提示为谜语诗；解锁实为击杀三名古老恶魔（achievements/all.lua:84–107）。“为复活另一者而战”与 lore/demon.lua 中莎西·凯希设法复原克里尔·费扬的叙述相符；deception→“踪影”、taught 未译属诗体取舍，不影响解锁提示，记 advisory。' + U),
    '5e4738cdc1': ('confirmed', True, '公开 Ashes lore/demon.lua:444–464（克里尔·费扬雕像）：peasants 误作“难民”；lash out once I was sure my life was in danger 是“确认性命受威胁才反击”，现译“抽身逃走”意思相反；growing them back with more nerve endings 误作“放回神经更加密集的地方”。' + U),
    '614e152463': ('confirmed', True, '公开 Ashes walrog-pop.lua:59–62 chat c：源文无“无耻的背叛者”（Traitor 只在 chat b 按 naga 条件代入），属增译且对非 naga 角色错误；were their deaths just indecision? 被改成“他们的尸体又是怎么回事”。' + U),
    '61c813b980': ('refuted', False, '公开 Ashes demon_statues.lua:24 的 champion of Urh\'Rok；本库同族 tome-ashes-urhrok.lua:110、445、547、548、550 一致作“乌鲁洛克的精英卫兵”，属既定专名，单条不改。' + U),
    '61ee07b50f': ('refuted', False, '公开 Ashes doom-shield.lua:120–165 Demonic Madness 为以盾旋转、攻击周围并致混乱的技能（info：You spin around madly with your shield）；“疯狂旋转”概括机制且同族 info 一致（指南 6.3 意译专名）。' + U),
    '620e36d284': ('confirmed', True, '观察所称“锥形”不成立：公开 Ashes fearfire.lua:142 地狱吐息 target 为 type="cone"，现译贴合实现。但同条换行结构被拆散（宿主实测：源 1 个 LF、1 处 \\n\\t\\t；译 4 个 LF、含 1 个空行、无 \\n\\t\\t），一级换行不变量，修复只恢复换行与制表符、保留“锥形”。' + U),
    '633ee7605b': ('advisory', False, '公开 Ashes npcs/major-demon.lua:52 腐化泰坦描述 Swarming, gnashing, burning；现译以“灼烧腐蚀”概括，丢 gnashing、以本库酸液树魔的酸蚀意象代之，属措辞取舍，记 advisory。' + U),
    '641933080c': ('confirmed', True, '公开 Ashes lore/demon.lua:485（罗格洛斯雕像）：Rogroth generates countless essence-less seeds from within its frame 是其自身躯体不断产生种子；现译“在这个构造中留下了无数种子”把产生改成留下、把自身躯体改成泛指构造。' + U),
    '65e5cc8228': ('refuted', False, '公开 Ashes timed_effects.lua:473 力量之潮；固定主游戏 624a673 engine/interface/ActorLife.lua:75 以 life <= die_at 判死，即生命到达 -X 即死；现译“直到 -%d 生命才会死去”与实现一致，上游 less than 与实现不符。' + U),
    '676590b08f': ('refuted', False, '公开 Ashes timed_effects.lua:629–638 DEMON_SEED_ARMOURED_LEVIATHAN 效果名与同名恶魔种子技能一致；本库 tome-ashes-urhrok.lua:864、1566、1569、1571 同族统一作“重装上阵”，单条不改。' + U),
    '6815f464b0': ('advisory', False, '公开 Ashes lore/demon.lua:212：The last O 指英文 befo-- 的末字母，中文无法保留，改作“最后一个字”属必要适配；pen was rapidly jerked away 与“笔从手上滑落”都导向“书写被打断”，记 advisory。' + U),
    '69b3689067': ('confirmed', True, '观察所称“3 回合”不成立：公开 Ashes fearfire.lua:75–76 setEffect(EFF_SENSE, 4)，现译“4 回合”贴合实现。但同条换行结构被拆散（宿主实测：源 2 个 LF、2 处 \\n\\t\\t；译 5 个 LF、含 2 个空行、无 \\n\\t\\t），一级换行不变量，修复只恢复换行与制表符、保留“4 回合”。' + U),
}
contextual = {
    '54a6a1b06c': decisions['54a6a1b06c'],
    '55dedd2404': ('confirmed', True, decisions['55dedd2404'][2] + '另 familiarity 被译“团结精神”、furthermore 被译“也就是说”，同条一并修正。'),
    '5666e9d827': ('confirmed', True, decisions['5666e9d827'][2] + '另 sustainable amount of energy-input 被写成“很少的能量”、省略 once mass-production is in order 条件、most straightforward for the spectator 作“最为熟悉”，同条一并修正。'),
    '5e4738cdc1': ('confirmed', True, decisions['5e4738cdc1'][2] + '另 even the armies of Mal\'Rok 被写成“乌鲁洛克的军队”（同条其余处作“玛·洛克”），同条一并修正；本条 Fearscape 作“恐惧空间”，按术语库 fearscape=恶魔空间 与本库主流用法对齐。'),
    '614e152463': decisions['614e152463'],
    '69b3689067': ('refuted', False, '本条 Fearscape 作“恶魔空间”，与术语库 terminology/narrative.tsv:12 及本库主流用法一致；不一致的是 5e4738cdc1 的“恐惧空间”，已并入该条修复。observation 自述 4 回合贴合实现。' + U),
}
rows = []
for file in sorted((scratch / 'review280-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        disposition, repair, conclusion = decisions[key]
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == len(decisions) == 19
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='all 19 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')

for file in sorted((scratch / 'review280-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        key = verdict['revision_key'][:10]
        disposition, repair, conclusion = contextual.pop(key)
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert not contextual and len(rows) == 25
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 11 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=69, repair_required=11), rows=rows,
             reviewers=dict(surface='codex/gpt-6-sol (group attempt 2: 4 lanes, 80 entries)',
                            contextual='claude/claude-opus-5-5 (refreeze dlc-location-v1, 19 entries)'),
             notes=[
                 'Surface group attempt 1 was invalid: lane-000-0 echoed one wrong entry_revision_identity; it was rejected, lanes 1-2 archived, lane 3 never dispatched, and the whole four-lane group was rebuilt as group-000-retry-02 with byte-identical envelopes.',
                 'The first contextual run enumerated /workspace to find the DLC checkout and wrote /tmp/rv76.txt; its harvested output was rejected (raw preserved) and archived. A refreeze event with an explicit --ashes-checkout produced the accepted run; the rejected output was not used.',
                 'Surface and contextual observations independently adjudicated against their own frozen revisions.',
                 'On 620e36d284 and 69b3689067 the observed claims match the implementation; the revisions are confirmed only for host-measured newline/tab structure.',
                 'Ashes public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Eleven confirmed repair revisions raise the window 28 backlog from 13 to 24; threshold 20 is reached, so repair window 28 opens after this batch closes.'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
spec = {'workset': f'evidence/quality/production-batches/{batch}-source-workset.json',
        'decisions': {r['revision_key'][:10] + '|' + r['stage']:
                      {k: r[k] for k in ('disposition', 'repair_required', 'conclusion')}
                      for r in rows}}
assert len(spec['decisions']) == len(rows)
(scratch / 'review280-host-decisions.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=28, window_opened=True, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=13, source='batches 278 (6) and 279 (7)'),
    backlog_after_count=24, default_max_cycles=3,
    source_batches=['batch-2dd6d21e34b360ebb6d9', 'batch-99f8a711d02012a6de19', batch],
    excluded='pending named term, advisory and historical blocked entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第280批：冻结80条，全部为 Ashes DLC，逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 首组因 lane-000-0 回显 identity 错字判废，整组以 group-000-retry-02 重派，4个有效lane审80条，19个ISSUE；'
    'contextual 首个 Opus run 为找 DLC checkout 枚举 /workspace 并写 /tmp 文件，输出拒收并归档，按 refreeze 事件显式给出 checkout 后重派，有效 run 复核19条，6个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决25个观察：{counts}；预计69条完成、11条待修复。'
    '修复 revision：乌尔罗格对白两条（理由丢失；增译“背叛者”）、恶魔之血与绝望碾压制表符、烈焰突袭“任何生物”被收窄为敌人、战术简报两处写死“他”、精英卫兵雕像传说、克里尔·费扬雕像传说（反击误作逃走等）、罗格洛斯雕像种子来源、地狱吐息与炼狱之门换行结构（机制译文贴合实现须保留）。'
    '魔化精灵谜语、腐化泰坦描述、血迹便条记 advisory。修复窗口28积压从13增至24，达到20，本批闭合后开窗。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=24), ensure_ascii=False))
