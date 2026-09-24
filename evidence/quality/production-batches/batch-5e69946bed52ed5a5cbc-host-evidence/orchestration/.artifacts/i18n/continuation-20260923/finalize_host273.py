import pathlib,json,collections
b='batch-5e69946bed52ed5a5cbc';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fd267689':('confirmed',True,'与 surface 同向并补充：enforced order and discipline 被写成“执行他的命令和法律”；loyal to the crown 漏宾语；同条前称“王冠”后称“皇冠”不一致（物品名为“领袖的皇冠”，统一为“皇冠”）；Nargol lands 非“大陆”。并入同条整句修复。'),
}
raw=json.loads((A/'review273-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==10
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==2,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=78,repair_required=2,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1 and Codex function_call items since 5c2f8459; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual scope was the 9 surface-flagged revisions (envelope entries=9); the other 71 rest on the surface OK verdicts.','Contextual raised 1 ISSUE (fd267689 Crown of Command), agreeing with the host-confirmed surface row and adding detail (order/discipline, loyal to the crown, 王冠/皇冠 inconsistency).','Contextual passed fcb8219f (Antimagic User); host keeps it confirmed: source says spells and arcane equipment are impossible and class/Actor.lua:5059/5139 forbid_arcane is a hard block, while the target says 拒绝使用法术 (refuse), turning a restriction into a choice.','Contextual passed the 7 host-refuted rows (keyword family, ego-affix space, colon-label spaces, Cunning, Rime Wraith name, munitions wording).','No advisories.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==10
(A/'review273-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW27-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 273',window=27,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第273批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：71 OK / 9 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000 复核 surface 标出的 9 条：8 OK / 1 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对10个观察裁决%s，结果78条完成、2条修复、0条pending。修复范围：“反魔法”提示说明“拒绝使用法术”改为无法使用法术及奥术驱动装备（forbid_arcane 为硬限制）；领袖的皇冠描述整句修复（许多人而非大部分、秩序与纪律、效忠皇冠、称呼统一为与物品名一致的“皇冠”、纳格尔领土而非大陆）。驳回：灵晶 keyword“创造力”（同族名词化）、ego 后缀与冒号标签的空格、Cunning=灵巧、远古冰魂（本库技能名）、合金弹药措辞（贴合实现与本库写法）。\n\n按1:1节奏，推送后进入修复窗口27，仅处理这2条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
