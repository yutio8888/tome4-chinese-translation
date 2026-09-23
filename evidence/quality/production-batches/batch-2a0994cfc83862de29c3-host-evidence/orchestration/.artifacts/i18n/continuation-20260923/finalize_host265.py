import pathlib,json,collections
b='batch-2a0994cfc83862de29c3';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f4754d3c':('confirmed',True,'与 surface 同向：psi-archery.lua:238–245 attack a target each turn for %d turns 与 to determine attack and damage；现译漏“每回合”（读作整个持续期只攻击一次）与“伤害”，并少一个行首 TAB。整条修复。'),
'f5651a16':('confirmed',True,'与 surface 同向：traps.lua:2188–2193 分别施加 EFF_STUNNED 与 EFF_POISONED（各 4 回合，各自受 canBe 判定）；现译漏“中毒”，“持续4回合”也只修饰伤害。整条修复，写明震慑与中毒均持续 4 回合。'),
'f56e57b6':('confirmed',True,'与 surface 同向，并补充：towards the end of the Age of Pyre 现译“在烈火纪时”漏“末期”。连同首句、speech、few hundred years、demons release acids/darkness 一并整条逐句修复。'),
}
raw=json.loads((A/'review265-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==11
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==4,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=76,repair_required=4,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest; lane-000-0 results[3] (truncated, mixed with results[5] tail) and results[15] (one b dropped) identity echoes were wrong at OK positions; host hand-attributed and harvested via --raw with the corrected identities, original bytes kept (captures265/lane0-original.raw, lane0-attribution.md).',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f4d315f2 (Burrow); host keeps it confirmed on objective evidence: the frozen target replaces the third line\'s \\n\\t\\t indent with \\n plus five spaces (TAB invariant), and burrow into earthen walls drops earthen.','Freeze MISS: f56e57b6 is a lore/misc.lua text rowed under section mod-tome/load.lua (mod-tome.lua:43247); section() is a no-op in game and t() is last-write-wins per src+tag (I18N.lua:100-101,141-143), so this later row overrides the lore/misc row at 18126 and is the effective translation. Repair targets this row only; the 18126 row keeps its own separate revision.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==11
(A/'review265-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW19-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 265',window=19,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第265批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：72 OK / 8 ISSUE；harvest 前逐位比对 80 个回显 identity，lane-000-0 两处判 OK 的 identity 回显错误（第4条截断混入他条尾部、第16条少一个 b），宿主手工归因并以更正 raw 收取，原字节留档。full contextual（claude/claude-opus-5-5）full-000：5 OK / 3 ISSUE，与 surface 确认项同向。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对11个观察裁决%s，结果76条完成、4条修复、0条pending。修复范围：念动弓说明（漏“每回合”与“伤害”、行首 TAB 数）、Burrow 说明（第三行用空格代替 TAB、漏“土质”）、Nightshade 陷阱（漏“中毒”）、野蛮种族记载（位于 load.lua 段但实际生效的重复行：首句、speech、几百年、烈火纪末期、恶魔释放酸液/黑暗之云）。contextual 对 Burrow 判 OK，宿主据 TAB 不变量维持确认。驳回：murderer’s 前缀空格、Antimagic! 成就名。advisory：龙系类别说明族内意译、森林巨魔巫师外貌描述。\n\n按1:1节奏，推送后进入修复窗口19，仅处理这4条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
