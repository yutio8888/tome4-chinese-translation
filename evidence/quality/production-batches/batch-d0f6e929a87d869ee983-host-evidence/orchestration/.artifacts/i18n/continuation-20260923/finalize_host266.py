import pathlib,json,collections
b='batch-d0f6e929a87d869ee983';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f58a8172':('confirmed',True,'与 surface 同向：world-artifacts.lua:5002–5022 Telekinetic Core 的 wielder 无被动牵引，仅 use_talent T_PSIONIC_PULL 主动使用；现译删 appears 并增“所有”，把外观描述写成确定的被动效果。整条修复。'),
'f5928e33':('confirmed',True,'与 surface 同向：horror.lua:264 bloodshot 为“布满血丝/充血”，现译“带血的”误作沾血。整条修复。'),
'f5d4f8ef':('confirmed',True,'与 surface 同向，并补充：death.lua:229–234 callbackOnKill/callbackOnSummonKill 对任何被杀生物触发，原文为 creature，现译缩为“敌人”。整条修复：thrill of the death 译为击杀/死亡带来的快感，creature 译为“生物”。'),
'f5f90d5b':('confirmed',True,'与 surface 同向：GameOptions.lua:672 Version checks 为不再检查插件新版本，现译“无法更新插件的版本”与上一条“仍可手动安装”矛盾。整条修复（其余各条 contextual 判一致）。'),
'f603e1fb':('confirmed',True,'与 surface 同向：spells.lua:32 spell/temporal 类别说明是名词短语“操控时间的法术学派”，现译“学习操控时间。”误作动作。整条修复。'),
'f6060b57':('confirmed',True,'与 surface 同向：quests.lua:267–269 MELINDA_SAVED，damsels in distress 为“落难少女”，与迷路无关。整条修复。'),
'f62d40cf':('confirmed',True,'与 surface 同向：ardhungol/objects.lua:40–45 BASE_ROD，由巨型蜘蛛獠牙雕成；wand 本库统一“魔杖”（entity subtype wand=魔杖），现译“枝条”错。contextual 称冻结术语快照无 wand 条目，宿主以本库现行译名“魔杖”补足。整条修复。'),
}
raw=json.loads((A/'review266-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==16
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==7,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=73,repair_required=7,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all four surface lanes and the contextual child harvested via --native-log directly, no bypass and no hand attribution; all 80 surface identity echoes pre-checked exact against envelopes before harvest. lane-000-3 Paseo display showed a leading "---" line but the native final assistant message starts with "{".',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f603f432 (mindstar feeds) and f66c15e3 (another shadow), matching host refuted/advisory.','Freeze MISS 1: the lore/misc.lua text rowed under section mod-tome/load.lua is the window-19 successor (runtime-effective duplicate); surface OK this time.','Freeze MISS 2: f64b64ae (#LIGHT_BLUE#The merchant carefully hands you: %s, section last-hope-lost-merchant.lua) exists only in upstream locale files at 624a673 and is registered in evidence/production-review-v2-lite/known-dead-keys.json; the translation text is correct and surface OK, so it closes done; the dead-key source migration stays a maintainer pending item.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==16
(A/'review266-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW20-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 266',window=20,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames (sibling spell school descriptions such as Conveyance are out of scope)',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第266批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：71 OK / 9 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致，四组均直接以原生日志收取。full contextual（claude/claude-opus-5-5）full-000：2 OK / 7 ISSUE，与 surface 确认项完全同向。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对16个观察裁决%s，结果73条完成、7条修复、0条pending。修复范围：念力核心项圈外观（删“似乎”、增“所有”）、邪眼“bloodshot”误作带血、死亡盛宴技能“thrill of the death”误作渴望死亡且 creature 缩为敌人、离线模式说明“版本检查”误作无法更新、时空法术类别说明误作“学习”、梅琳达成就“落难少女”误作迷路、蛛毒魔棒未鉴定名 wand 误作枝条。驳回：心灵之星“feeds”方向。advisory：召唤“另一个”阴影。冻结 MISS 两条：窗口19后继的 load.lua 段 lore 行，以及已登记死键的失落商人日志行（译文正确，按 done 闭合，死键迁移仍待维护者）。\n\n按1:1节奏，推送后进入修复窗口20，仅处理这7条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
