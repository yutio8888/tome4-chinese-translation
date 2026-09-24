import pathlib,json,collections
b='batch-54be748f9582a3f09434';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fc0f5daa':('confirmed',True,'与 surface 同向：psionic/thought-forms 技能系召唤思维形态实体，psionic summons 是召唤物而非召唤术。并入同条修复。'),
'fc3dc9f6':('confirmed',True,'与 surface 同向并补充：还漏 with a good amount of scorn；revealed to you your folly 被改写为“世界如此巨大，你又如此渺小”，trials 被改写为“可怕梦魇”；署名前应为空行。并入同条逐段重译。'),
'fc5311ff':('confirmed',True,'与 surface 同向并补充：than any arrow you\'ve ever seen 也被省略。并入同条修复。'),
'fc60ee27':('confirmed',True,'与 surface 同向：多出的换行与 crippling blow 缺失。并入同条修复。'),
'fc753883':('confirmed',True,'与 surface 同向：raiding party 缺失。reviewer 对 Yaech 译名证据不足的保留由宿主核实：本库 mod-tome.lua:9037（Yaeches 条目）与 39138（Murgol, the Yaech Lord）均译“夺魂魔”，保持。并入同条修复。'),
}
raw=json.loads((A/'review272-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==10
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=75,repair_required=5,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1 and Codex function_call items since 5c2f8459; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual raised 5 ISSUEs, all on the 5 host-confirmed surface rows, adding detail (scorn/folly/trials rewrites in the Weisman letter, the Titan arrows comparison clause).','Contextual scope was the 5 surface-flagged revisions only (envelope entries=5); the other 75 rest on the surface OK verdicts.','No advisories.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==10
(A/'review272-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW26-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 272',window=26,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第272批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：75 OK / 5 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000：0 OK / 5 ISSUE（仅含 surface 标出的 5 条）。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对10个观察裁决%s，结果75条完成、5条修复、0条pending。修复范围：思维形态技能系说明“灵能召唤术”改“灵能召唤物”；罗尔夫致威斯曼信（巨蚁母体、嘲讽、勇气、段落与空行）逐段重译；泰坦的箭袋描述补“锋利”“几乎无法折断”等分句；阿塔玛森红宝石眼睛描述删多余换行并补“重创”；梅琳达任务日志补“袭击队”。\n\n按1:1节奏，推送后进入修复窗口26，仅处理这5条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
