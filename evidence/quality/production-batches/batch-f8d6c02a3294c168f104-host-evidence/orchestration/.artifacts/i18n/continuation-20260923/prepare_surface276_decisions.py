import json
import pathlib

B = 'batch-f8d6c02a3294c168f104'
P = pathlib.Path('.ai/task') / B
C = pathlib.Path('.artifacts/i18n/continuation-20260923')
D = {
    'ff891672cb': ('pending', False, 'Sceptre of the Archlich 的 Archlich 限定在“死灵权杖”中未明确表达；world-artifacts.lua:2637（固定 624a673）确为神器名。改名涉及神器专名口径，列入用户集中审阅；本批不单改。'),
    'ffa77aef82': ('refuted', False, 'The Master 在本库已有固定称谓“领主”（mod-tome.lua:38309 entity name，另有同族信件 14592、14610）；此处沿用，不是无依据改名。'),
    'ffb21dd4cc': ('confirmed', True, '固定主游戏 magical.lua:600–618：SUPERCHARGE_GOLEM 结束移除伤害和生命回复增益；“seems less dangerous”是威胁降低，现译“平静了下来”误述情绪。修复为“#Target#看起来没那么危险了。”一类，保留 #Target#。'),
    'ffd4751c6b': ('refuted', False, 'Maximum encumbrance: 是属性标签；中文全角冒号后不保留英文尾随空格，符合本库已裁定的标签拼接惯例。'),
    'ffe80f4c81': ('confirmed', True, '固定主游戏 portal-vault.lua:133 原文 A strange portal to some place else，现译遗漏 strange 的“奇异”信息。补回该限定，不改运行键。'),
    'fff8487389': ('confirmed', True, '固定主游戏 summon-melee.lua:500–538：岩石傀儡获 T_UNSTOPPABLE 技能，可进入不可阻挡状态；原文 can become，现译“并且不可阻挡”误作恒定状态。修复为“有可能变得不可阻挡”。damage%% 已由“百分比伤害”表达，resistance penetration %% 为百分比属性，不把字面 %% 当运行时 placeholder 要求。'),
    '0523b49940': ('confirmed', True, '公开 DLC start-ashes.lua:23–28（本批文件 SHA 匹配，仓库/commit 未固定）：原文恢复意识时灼热土地构成的平台正在从主大陆分裂；现译写成醒后发现已分离，并漏掉 searing earth。只修这一时序与土地意象；Eyal 的全局译名另在既有 pending。'),
    '0c22616dae': ('confirmed', True, '公开 DLC world-artifacts.lua:691（本批文件 SHA 匹配，commit 未固定）：treacherous road to the top of the world 指通往世界之巅的险途；“背叛之路，直通天际”改动道路性质和终点。修复为保留引号的险途/世界之巅表达。'),
    '0c451e854a': ('pending', False, 'Armoured Leviathan 在同 DLC 中是技能名、效果名及 +/- 日志的同族称谓（tome-ashes-urhrok.lua:864,1567,1570,1572）；“重装上阵”是既有统一意译。改为含巨兽的新名需跨条命名决定，交用户集中审阅。'),
    '0ed5688129': ('confirmed', True, '公开 DLC corrupted.lua:114（本批文件 SHA 匹配，commit 未固定）：Most simply run 是多数人逃跑，现译“人们常畏惧”改变行动；destruction\'s engines 是毁灭的工具/引擎，现译添“战争机器”。修复该两处并保持原文的抒情节奏。'),
    '100cec57ae': ('refuted', False, 'Empathic Hex 本库技能名与同族引用统一为“转移邪术”（mod-tome.lua:22802,35669–35673）；固定主游戏 hexes.lua:99–129 显示目标造成伤害时自身承受部分同量伤害，现行意译有机制依据。'),
}
rows = []
for f in sorted((C / 'review276-surface-raw').glob('*.json')):
    for r in json.loads(f.read_text())['results']:
        if r['verdict'] != 'ISSUE':
            continue
        matches = [v for k, v in D.items() if r['entry_revision_identity'].startswith(k)]
        assert len(matches) == 1, r['entry_revision_identity']
        disposition, repair, conclusion = matches[0]
        rows.append(dict(revision_key=r['entry_revision_identity'], stage='surface',
                         observation=r['observation'], disposition=disposition,
                         repair_required=repair, conclusion=conclusion))
assert len(rows) == 11, len(rows)
(P / 'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(
    status='host adjudicated surface observations; contextual observations adjudicated separately',
    slid_observations=None,
    slide_check='each of 11 observations compared against its own frozen source/target; none slid',
    rows=rows), ensure_ascii=False, indent=2) + '\n')
(P / 'HOST-INDEPENDENT-FINDINGS.json').write_text(json.dumps(dict(
    batch_id=B,
    rows=[dict(revision_key='ff98c01bb52807ecc4542900c938966404ef8dbbbe2eb850ad69c3cc39b42330',
               disposition='confirmed', repair_queued=False,
               observation='Clinch 说明将 attempt to grapple 译成“并抓取”，省略了可失败的尝试条件。',
               evidence='固定主游戏 624a673：game/modules/tome/data/talents/techniques/grappling.lua:104；class/interface/Combat.lua:2790–2833 的 startGrapple 在目标不能被定身时返回 false。',
               workflow_limit='surface reviewer returned OK; production adjudication accepts only reviewer ISSUE observations. Retain as host-confirmed finding outside the formal repair_required queue until a separately authorized repair route is selected.')]),
    ensure_ascii=False, indent=2) + '\n')
print({d: sum(r['disposition'] == d for r in rows) for d in ('confirmed', 'refuted', 'advisory', 'pending')})
