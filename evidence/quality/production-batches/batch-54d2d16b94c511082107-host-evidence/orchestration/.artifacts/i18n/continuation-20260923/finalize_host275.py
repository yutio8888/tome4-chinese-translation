import pathlib,json,collections
b='batch-54d2d16b94c511082107';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fe5a84a1':('confirmed',True,'与 surface 同向：首句漏“（及武器）”，并入同条修复（另含 surface 指出的“每次命中”）。'),
'fe90619e':('confirmed',True,'与 surface 同向并补充：constant aura 译“永恒之焰”未表达持续光环，并入同条整句修复（每回合、法术结束时、持续火焰光环）。'),
'ff47fb86':('confirmed',True,'与 surface 同向并补充：“开启后”暗示可开关技能，纹身为一次性使用物品；并入同条整句修复。'),
'ff658fab':('confirmed',True,'与 surface 同向：该物品为 Ethereal Embrace，描述 waves and bends with shimmering light，wispy 应作缥缈/轻纱感。'),
}
raw=json.loads((A/'review275-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==15
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==6,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=74,repair_required=6,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1 and Codex function_call items since 5c2f8459; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual scope was the 11 surface-flagged revisions (envelope entries=11); the other 69 rest on the surface OK verdicts.','Contextual raised 4 ISSUE (fe5a84a1 Fiery Hands, fe90619e Fearscape, ff47fb86 regeneration-infusion tip, ff658fab wispy cloak), each agreeing with a host-confirmed surface row.','Contextual passed fec0939b (Ghormot epitaph); host keeps it confirmed: the source italic verse has three lines and the target merges two (measured LF 6 -> 5), a newline-invariant defect.','Contextual passed ff585d0b (quest name From bellow, it devours); host keeps it confirmed: the same English sentence is rendered 来自深渊，吞噬四方 at mod-tome.lua:38225 but 地下吞噬者 here, two incompatible renderings of one line.','Contextual passed the 5 host-refuted rows (two ego-prefix spaces, colon-label space, orc-pride destroyed family, crimson-templar crit duration).','No advisories.','No pending, no glossary/global rename; old pending/blocked unchanged.','Accumulate-then-repair cadence (user 2026-09-24): the 6 repairs join the backlog (now 13); no window is opened until it reaches >=20.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==15
(A/'review275-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'REPAIR-BACKLOG-DECISION.json').write_text(json.dumps(dict(trigger='accumulate-then-repair cadence (user instruction 2026-09-24: record repairs, open one combined window once the backlog reaches >=20)',target_window=27,window_opened=False,batch=b,bounded_revision_keys=rep,backlog_before=dict(count=7,source='batch-5e69946bed52ed5a5cbc WINDOW27-REPAIR-DECISION.json (2) + batch-c03b7552b4059d697ec0 REPAIR-BACKLOG-DECISION.json (5)'),backlog_after_count=7+len(rep),default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第275批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：69 OK / 11 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000 复核 surface 标出的 11 条：7 OK / 4 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对15个观察裁决%s，结果74条完成、6条修复、0条pending。修复项：燃烧之手补“（及武器）”并把体力回复改为“每次命中”（stamina_regen_on_hit）；恶魔空间补“每回合”、持续光环与“法术结束时”；黑暗者古尔莫特墓志铭拆回三行（LF 6→5 实测）；回复纹身加载提示整句修复（预判伤害、提前准备，物品名统一“回复纹身”）；任务名 From bellow, it devours 与本库 38225 行对齐为“来自深渊，吞噬四方”；wispy purple cloak“脆弱的”改“缥缈的”。驳回：两处 ego 前缀空格、冒号标签尾空格、兽人部落“击败”同族一致、赤红守卫持续时间暴击（贴合 spellCrit 实现）。\n\n攒批节奏：修复项计入积压（累计 13 条），未达 20 条不开窗。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
