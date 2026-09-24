import pathlib,json,collections
b='batch-c03b7552b4059d697ec0';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fd89fad0':('confirmed',True,'与 surface 同向并补充：While active 与 temporary 限定亦应保留；按 doStrip 实现整句修复（物理伤害除去物理增益、时空伤害除去魔法增益；每目标每回合各至多一项）。'),
'fd9c72bf':('confirmed',True,'与 surface 同向：自然世界 与英文名及机制（无视自然抗性、软泥免费吐射）均不符；本库 Unstoppable=势不可挡，改“势不可挡的自然”一类。'),
'fe42c359':('confirmed',True,'与 surface 同向：越晚回来越可能见到冒烟的弹坑和暴怒的半身人；现译改成“在这儿待太久”并丢失弹坑。整句修复末两句。'),
}
raw=json.loads((A/'review274-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==14
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=75,repair_required=5,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1 and Codex function_call items since 5c2f8459; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual scope was the 11 surface-flagged revisions (envelope entries=11); the other 69 rest on the surface OK verdicts.','Contextual raised 3 ISSUE (fd89fad0 Disintegration, fd9c72bf Unstoppable Nature, fe42c359 alchemist chat), each agreeing with a host-confirmed surface row.','Contextual passed fda88c96 (Reflex Defense); host keeps it confirmed: unarmed-training.lua:128 is flat damage reduction plus lower incoming critical multiplier, not evasion, while 闪避神经 names dodging and collides with Reflexive Dodging=闪避反射.','Contextual passed fdff442a (Mucus); host keeps it confirmed: damage_types.lua MUCUS acts on actors standing on the mucus grid (friendly creatures in your mucus), while the target says 经过 (passing through).','Contextual passed the 6 host-refuted rows (colon-label space, Lightning Speed self-reference, Bash and Smash name, Mercy lore vs implementation, blind_immune convention, butler pronoun).','No advisories.','No pending, no glossary/global rename; old pending/blocked unchanged.','Repair cadence changed by user on 2026-09-24: the 5 repairs join the backlog (now 7) and no window is opened until it reaches >=20.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==14
(A/'review274-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(trigger='accumulate-then-repair cadence (user instruction 2026-09-24: record repairs, open one combined window once the backlog reaches >=20)',target_window=27,window_opened=False,batch=b,bounded_revision_keys=rep,backlog_before=dict(count=2,source='batch-5e69946bed52ed5a5cbc WINDOW27-REPAIR-DECISION.json (fcb8219f, fd267689)'),backlog_after_count=2+len(rep),default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第274批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：69 OK / 11 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000 复核 surface 标出的 11 条：8 OK / 3 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对14个观察裁决%s，结果75条完成、5条修复、0条pending。修复项：“裂解”（Disintegration）每目标每回合可各除去一项物理和一项魔法增益（并补回“分别”对应关系）；技能名 Unstoppable Nature“自然世界”改“势不可挡的自然”一类；技能名 Reflex Defense“闪避神经”改“反射防御”一类（机制为减伤与降低受暴击倍率）；粘液说明中友方单位条件“经过”改为“处在粘液中”；半身人炼金术士对话（alchemist-hermit）末句恢复“冒烟的弹坑”与“越晚回来”。驳回：冒号标签尾空格、闪电加速自指、击退射击（意译贴合机制且同族一致）、“慈悲”描述（贴合实现）、致盲免疫惯例、堡垒之影称“它”。\n\n按用户 2026-09-24 新节奏，修复项计入积压（累计 7 条），不开窗；积压达 20 条后开合并修复窗口27。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
