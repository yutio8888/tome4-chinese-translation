import json
from pathlib import Path

batch = 'batch-a2538cac10c65873a661'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
decisions = {
    '10419e2ec3': ('confirmed', True, '公开 Ashes 源码本批 SHA 匹配，来源/commit 未固定：black flame 是黑色火焰，现译“邪恶火焰”改变颜色信息。'),
    '119af89312': ('confirmed', True, '公开 Ashes searing-halls/npcs.lua:99 的 italic 标记分别强调 extracting 与 willing；现译把标记放到“志愿者”和“获取”，对应关系颠倒。修复标记附着位置并保持原意。'),
    '120d3d48de': ('confirmed', True, '公开 Ashes 记忆对白原文要求踏上 plate、摆好手臂，以便安置 bindings；现译“站在那里别动……把它放好”遗漏板子和束缚装置。'),
    '12c3c45f81': ('confirmed', True, '公开 Ashes 源文 3 arms 是三条手臂，现译“三只手”误作手掌；本批文件 SHA 匹配，来源/commit 未固定。'),
    '1be82f2f19': ('confirmed', True, 'primary ambush 指主要/最初的伏击，现译“面前伏击”改为位置关系；应恢复伏击的阶段或主次含义。'),
    '1dafd3a728': ('pending', False, 'timed_effects.lua:1045–1052 将 Corruption of the Doomed 用作效果名及 +/- 日志，同族现译统一“腐化形态”。改为含 Doomed 的新专名须同步四处，交用户集中决定。Ashes 来源/commit 未固定。'),
    '218c180b3f': ('confirmed', True, '公开 Ashes 叙事原文是父 Urh\'Rok 直接而热情地认可 Khulmanar 的头脑，现译“精神受到父的指引”把认可改成指引。'),
    '21d89ecd3e': ('confirmed', True, '公开 Ashes 叙事原文说全副武装的堡垒停在兵工厂与人口中心上方；现译“所有武器系统都瞄准了”增添主动瞄准，改变威胁方式。'),
    '28ea98973d': ('confirmed', True, '公开 Ashes demon-seeds.lua:737 写 fiery display of speed，现译“闪电般”把火焰意象换成闪电。'),
    '295b84f066': ('confirmed', True, 'wrath.lua:186–195 源文各后续行以两个制表符缩进，译文改成一个，影响多行技能说明结构。Obliterating Smash 的 range 实际赋给圆锥 radius（wrath.lua:32–37），因此“增加半径”本身有机制依据，不作为修复原因。'),
    '296765c04d': ('refuted', False, 'timed_effects.lua:420–470 的 FIRE_SHIELD 移除时确实以 friendlyfire=false 投射 FIREBURN，dur=3、radius=eff.radius、dam=eff.power；译文补充的是实际机制，不是错误附加效果。本批文件 SHA 匹配，来源/commit 未固定。'),
}
rows = []
for file in sorted((scratch / 'review277-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        key = result['entry_revision_identity'][:10]
        assert key in decisions, key
        disposition, repair, conclusion = decisions.pop(key)
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == 11 and not decisions
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='each of 11 observations checked against its own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
print({name: sum(row['disposition'] == name for row in rows)
       for name in ('confirmed', 'refuted', 'advisory', 'pending')})
