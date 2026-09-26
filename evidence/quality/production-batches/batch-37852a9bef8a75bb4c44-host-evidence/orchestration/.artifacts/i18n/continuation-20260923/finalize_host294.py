import collections
import json
from pathlib import Path

batch = 'batch-37852a9bef8a75bb4c44'
task = Path('.ai/task') / batch
scratch = Path('.artifacts/i18n/continuation-20260923')
# The adjudication chain already consumed review294-host-decisions.json; derive task records from it verbatim.
spec = json.loads((scratch / 'review294-host-decisions.json').read_text())['decisions']
extra = []
rows = []
for file in sorted((scratch / 'review294-surface-raw').glob('*.json')):
    for result in json.loads(file.read_text())['results']:
        if result['verdict'] != 'ISSUE':
            continue
        d = spec[result['entry_revision_identity'][:10] + '|surface']
        rows.append(dict(revision_key=result['entry_revision_identity'], stage='surface',
                         observation=result['observation'], **d))
assert len(rows) == 13, len(rows)
(task / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    additional_host_observations=extra,
    slide_check='all 13 observations checked against their own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
for file in sorted((scratch / 'review294-contextual-raw').glob('*.json')):
    for verdict in json.loads(file.read_text())['verdicts']:
        if verdict['verdict'] != 'ISSUE':
            continue
        d = spec[verdict['revision_key'][:10] + '|contextual']
        rows.append(dict(revision_key=verdict['revision_key'], stage='contextual',
                         observation=verdict['observation'], **d))
assert len(rows) == len(spec) == 20, len(rows)
repair = sorted({r['revision_key'] for r in rows if r['repair_required']})
pending = sorted({r['revision_key'] for r in rows if r['disposition'] == 'pending'})
assert len(repair) == 7 and not pending
counts = dict(collections.Counter(r['disposition'] for r in rows))
final = dict(batch_id=batch, observations=len(rows), observation_dispositions=counts,
             repair_revision_keys=repair, pending_revision_keys=pending,
             expected_final_states=dict(done=73, repair_required=7, blocked=0), rows=rows, additional_host_observations=extra,
             reviewers=dict(surface='codex/gpt-6-sol (4 lanes of 20, all Cults)',
                            contextual='claude/claude-opus-5-5 (contextual-000 Cults 13 entries)'),
             notes=[
                 'Cults-only batch: surface ran as four lanes of 20; lane-000-2 dropped five hex characters from one echoed identity (result 4, verdict OK). The provider-native log shows the agent wrote it wrong; the host hand-attributed the identity before the first harvest (captures294/lane2-original.raw and lane2-attributed.raw, recorded in HOST-SURFACE-BOUNDARY-AUDIT). No observation slid.',
                 'The contextual run read only its own envelope and the contract (no checkout probing), so no refreeze was needed.',
                 'Five surface observations are refuted because the translation matches the implementation where the English text is looser: bone staff cond unused_talents < 1, UNRAVEL_EXISTENCE counts only detrimental magical effects, the ft-horrors guardian gains +0.5 movement speed, DISOLVED_FACE deals damage on_timeout each turn, and the revelation log follows alterTalentCoolingdown.',
                 'Cults public source file SHA matched this batch workset; source repository and commit remain unpinned.',
                 'Seven confirmed repair revisions start the window 33 backlog at 7 (batch 294).'
             ])
(task / 'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')
(task / 'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(
    trigger='>=20 unique confirmed executable revisions (user instruction 2026-09-24)',
    target_window=33, window_opened=False, batch=batch, bounded_revision_keys=repair,
    backlog_before=dict(count=0, source='window 32 closed (d6ecacc5)'),
    backlog_after_count=7, default_max_cycles=5,
    source_batches=[batch],
    excluded='advisory and refuted entries',
    revision_count=len(repair)), ensure_ascii=False, indent=2) + '\n')
(task / 'HOST-SUMMARY.md').write_text(
    '第294批：冻结80条（全部 Cults），逐条按本批公开源码文件SHA核验80/80，来源仓库和commit未固定。'
    'surface 4 个 lane 各20条，13个ISSUE，无错位；lane-000-2 一条判 OK 的 identity 回显漏 5 个字符，原生日志确认为 agent 所写，宿主在首次 harvest 前按归因更正；'
    'contextual 一个 Opus run（13 条）只读 envelope 与契约，未越界，7个ISSUE。'
    '全部 child 已确认归档，原生读取边界已逐条核对。\n\n'
    f'宿主裁决20个观察：{counts}；预计73条完成、7条待修复。'
    '修复 revision：菲·维莉欧斯的冒险南部海岸一节（岩石取代平原的死亡句/提醒永恒精灵）、克罗格燃烧痛苦（纹身饱和）、舔舐 info 两处空行、'
    '消化袋对白（void 为失效）、第4卷第1章标题（精疲力竭的旅途）、纳格尔王国帐篷一节（信使/受不了/话音渐弱/随便抓人/随心所欲）、购买感谢文本（抽打）。'
    '骨杖职业点条件、抹除存在只计负面魔法效果、守护者移动速度、溶解之脸每回合伤害、启示缩短冷却均贴合实现，refuted；worms→害虫记 advisory。'
    '修复窗口33积压为7（第294批）。\n')
print(json.dumps(dict(dispositions=counts, final_states=final['expected_final_states'], repair_backlog=7), ensure_ascii=False))
