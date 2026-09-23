import pathlib,json,collections
b='batch-f740e6898e8b430ca79f';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
for r in rows:
    if r['revision_key'].startswith('e90949f9'):
        r.update(disposition='confirmed',repair_required=True,conclusion='quests.lua:337–340 ALL_DREAMS 成就名 Dreaming my dreams，desc 为体验并完成 Dogroth Caldera 全部梦境。译文我的梦就是你的梦新增第二人称并改成两人梦境等同的断言，偏离原名含义；surface 与独立 contextual 均指出，宿主据源码确认，应恢复为做着我的梦类表述。')
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(S,ensure_ascii=False,indent=2)+'\n')
C={
'e8fc5b0a':('confirmed',True,'与 surface 键同一缺陷的独立语境复核：cursed.lua:22 weary 被反转为不知疲倦，丢失 each day 与起身意象并新增下一个目标；确认修复整句。'),
'e90949f9':('confirmed',True,'独立语境复核与 surface 一致：成就名新增你的梦、改变含义；确认有界修复标题。'),
'e92433bc':('confirmed',True,'unlock-yeek.lua:22–34 原文 12 个换行，译文 13 个：原第 23 行一句被拆成“……有点滑稽。\\n不过他们是……”两行，违反 newline 不变量，确认修复（合并为一行）。cunning 译灵巧与术语库 Cunning=灵巧（stat name）一致，不作修复。'),
'e9253668':('confirmed',True,'misc.lua:530–545 诗句 Once flowers rose to reach the sky 被虚构为复仇火焰，Now all lost, now all fled 被复写成首节的尘土/虚无；确认修复该两行。blossoms/beech 细节属建议，可在修复同句时顺带贴合但不扩大范围。'),
'e9517394':('confirmed',True,'magical.lua:4259–4261 NUMBING_BLIGHT long_desc: All damage it does is reduced by %d%%；blight.lua:212 reduces all damage dealt。译文降低 %d%% 伤害未说明是目标造成的全部伤害，可被读为受到伤害降低，方向歧义属机制描述缺陷，确认修复该行。'),
'e9884825':('confirmed',True,'misc.lua:509–519 races-10：may be borne purely from the fanatical delusions 被改为只有信徒才会相信（删 may 并改变主张）；The Daikara Pass and surrounding mountain chains 被缩为岱卡拉山脉；over 40\' 丢失 over；newly matured drakes 丢失 newly。确认有界修复这四处；surface 所提第一人称增译仍只记建议。'),
}
raw=json.loads((A/'review254-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==18
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==6,rep
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,expected_final_states=dict(done=74,repair_required=6),rows=rows,additional_host_observations=S['additional_host_observations'],
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser_deviation='Codex CLI 0.156.0 and Claude Code 2.1.280 are newer than the repo native parser pins (0.153.0 / 2.1.259). Raw bytes were extracted by running the repo _parse_native_final from a temp copy with only the version literals substituted, then harvested via the strict --raw path; proofs in review254-*-native/*.proof.json. Repo tools unmodified.',
  notes=['Surface and contextual observations adjudicated independently.','lane-000-1 observations slid by one entry for three rows; handled per slid-observation procedure.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==18
(A/'review254-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW8-EARLY-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='confirmed newline invariant in e92433bcba (unlock-yeek) plus mechanism-direction ambiguity in e951739433; finish and push current formal review batch before repair',window=8,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; e923d2b8 host additional observation; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第254批：80条，全部固定ToME源码，65文件逐字节核验，80条原文字面命中。含窗口7的8个successor（均判OK或所附观察被驳回）。\n\n审核模型按用户2026-09-23指示改为surface codex/gpt-6-sol、contextual claude/claude-opus-5-5。四组surface：68 OK / 12 ISSUE（lane-000-1有3条observation错位一格，已逐条比对）；一组full contextual：6 OK / 6 ISSUE。5个独立reviewer已严格校验并归档，原生读取边界已人工审计。Codex 0.156.0/Claude Code 2.1.280 高于仓库原生parser固定版本，原文bytes以仅替换版本字面量的同一parser提取并走严格--raw收取，仓库工具未改。\n\n宿主对18个观察裁决%s，合并为6条修复、74条完成。修复范围：诅咒无尽狩猎技能树描述（疲惫被反转）、ALL_DREAMS成就名、unlock-yeek多余换行、自然精灵诗句花朵/逃散两行、麻痹毒素伤害方向、龙族传说四处限定词与地名。Overcharge飞弹每目标一枚、挽歌触发条件、毒素风暴等概率均与实现一致而驳回；e923d2b8 资源→能量为错位漏报，记宿主补充建议。\n\n批次提交、finalize和推送闭合后提前进入窗口8，仅处理这6条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
