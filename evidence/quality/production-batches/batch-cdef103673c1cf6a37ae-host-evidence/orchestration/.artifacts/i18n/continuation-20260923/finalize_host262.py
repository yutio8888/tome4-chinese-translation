import pathlib,json,collections
b='batch-cdef103673c1cf6a37ae';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f15f5593':('confirmed',True,'与 surface 同向：星辰契约说明 The strength of your bond 被译成“你的力量”，丢失与恒星化身的羁绊。宿主另核 celestial/combat.lua:99–104：光辉引力以被击中目标为中心收集半径 5 内敌人并 pull(target.x,target.y,5)，即拉向被击中的目标；现译“将5格范围内的敌人拉过来”易读作拉向施法者，一并明确。Eyal=“埃亚尔大陆”为本库既有用法（23 处），不在本条改动范围。整条修复，恢复 \\t\\t 缩进。'),
'f18f9a4e':('confirmed',True,'lore/fun.lua:217–289 不死猎人指南（宿主逐句核对固定源码）：usually armed and sometimes even armoured 被夸大为“大多都是持有武器或是全副武装的”；treat them as you would a necromancer - with cold steel 增译“刺穿他们的喉咙”；Ever fought a snow giant? 增译“一向被视为力量象征的”；all screaming for your blood to be spilt 被改成因果“因为你的每滴鲜血都令其饥渴无比”；I always receive the same answer 弱化为“几乎都是同样的原因”；巫妖段“传说与之不符是因为它超越传说”被译成传说“有所失实”，与下句自相矛盾。忠实性缺陷，整条逐句对照修复（wild infusion=野性纹身保持）。'),
'f19cec26':('confirmed',True,'与 surface 同向：alchemist-last-hope.lua:405–406 往瓶里加了好料/明早宿醉难受被误译为“带来个好东西/也许明早没什么用”。整条修复。'),
'f20e44ef':('confirmed',True,'与 surface 同向：%s 为 string.his_her_self 反身代词（utils.lua:953–957），special_death_msg 再嵌入 PartyDeath.lua:123–131 以玩家名为主语的死讯；按同族“牺牲了%s，引来…”式修复。'),
'f2230567':('confirmed',True,'与 surface 同向：munitions.lua:418 damDesc(self, DamageType.NATURE, poison)，应为“自然伤害”。'),
}
raw=json.loads((A/'review262-contextual-raw/full-001.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==18
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==7,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==2,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=71,repair_required=7,blocked=2),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-001; full-000 rejected for prose prefix, archived, superseded)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest; no hand attribution in this batch.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==18
(A/'review262-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW16-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 262',window=16,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; 2 pending (user review) excluded; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第262批：80条，全部固定ToME源码（含一条 lowercased-entity-name 证据：gem.lua lapis lazuli）。四组surface（codex/gpt-6-sol）：67 OK / 13 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致；lane-000-3 经 MCP 建 Paseo 终端只读取自身信封与契约，宿主核验按键后已关闭终端。full contextual（claude/claude-opus-5-5）首次 full-000 在 JSON 前多一句英文导语被判 output_valid=False，归档确认后以 full-001（attempt 2，retry_of full-000）重派，8 OK / 5 ISSUE。6个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对18个观察裁决%s，结果71条完成、7条修复、2条pending。修复范围：50级祝贺空行、星辰契约 bond 与光辉引力拉向目标、不死猎人指南多处增译夸大、矮人加料/宿醉玩笑、虚空传送门成就 closing、牺牲死讯 %%s 反身代词、剧毒弹自然伤害。pending：神器 Exiler“放逐”、技能系 Crimson Templar“赤红守卫”。驳回：壁画/starlit 末尾空格、野性纹身。advisory：邪教徒口号、+Assail 飘字。\n\n按1:1节奏，推送后进入修复窗口16，仅处理这7条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
