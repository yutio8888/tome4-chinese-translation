import pathlib,json,hashlib,subprocess,collections
b='batch-ba766c90924912867b02';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260922');rows=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text())['rows'];s={r['revision_key']:r for r in rows};ctx=json.loads((A/'review253-contextual-raw/full-000.json').read_text());out=[]
for r in ctx['verdicts']:
 if r['verdict']=='OK':continue
 key=r['revision_key'];base=s[key];d=base['disposition'];repair=base['repair_required'];reason=base['conclusion']
 if key.startswith('e85e4d'):
  d='confirmed';repair=True;reason='本观察并非surface的Daze状态名争议。agility.lua:130–136 将 shield_combat.dammod.str 转入 dex，只替换属性伤害加成；源文明确 bonus damage。译文省略加成而称决定盾牌伤害，未保留适用部分，确认有界补回属性加成。保留既定Daze=眩晕术语。'
 if key.startswith('e8959a'):
  reason+=' 同时确认首句defiance为抗争/不屈而非暴乱；sustain yourself through spite为以怨恨支撑自身，不是支持仇恨中的你。依据源文语义恢复首句，不更名技能或全局术语。'
 out.append(dict(revision_key=key,stage='contextual',observation=r['observation'],disposition=d,repair_required=repair,conclusion=reason))
rows+=out;assert len(rows)==25
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==8
p=P/'HOST-SOURCE-SUPPLEMENTAL.json';a=json.loads(p.read_text());c='624a67329fe2ad440c5b344785a9c73fcf22ae63';f='game/modules/tome/data/talents/techniques/agility.lua';raw=subprocess.check_output(['git','-C','/workspace/t-engine4','show',c+':'+f]);ls=raw.decode().splitlines();key=next(k for k in rep if k.startswith('e85e4d'));a['queries'].append(dict(revision_key=key,component='tome',public_source_path=f,fixed_source_commit=c,file_sha256=hashlib.sha256(raw).hexdigest(),start_line=130,end_line=169,excerpt='\n'.join(f'{i+1}: {ls[i]}' for i in range(129,169))));p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
counts=dict(collections.Counter(r['disposition'] for r in rows));final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,expected_final_states=dict(done=72,repair_required=8),rows=rows,notes=['Surface and contextual observations adjudicated independently; no verdict laundering.','Full contextual OK does not erase source-confirmed surface detail/format defects.','Surface Daze issue refuted; distinct contextual bonus-damage issue confirmed.','Fullscreen-notification objections refuted via actual Player.lua blur-shader behavior.','No glossary/global rename or excluded old repair expansion.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n');dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==25
(A/'review253-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
w=P/'WINDOW7-EARLY-REPAIR-DECISION.json';v=json.loads(w.read_text());v.update(bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,revision_count=8);w.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第253批：80条，全部固定ToME源码，63文件逐字节核验；79条原文字面命中，1条alchemist pearl为已核验拼接键。\n\n四组surface：61 OK / 19 ISSUE；一组full contextual：13 OK / 6 ISSUE。5个独立reviewer已严格校验并归档，全部原生读取边界已人工审计。宿主对25个观察裁决12 confirmed / 9 refuted / 4 advisory，合并为8条修复、72条完成。\n\n修复范围：疾病传播范围、法杖粗大尖端遗漏、抹除过去的日志、盾牌属性加成限定、弹体含义及LF/TAB、护盾延时及不屈首句、spinneret器官、剖腹死亡描述。Daze和Probability Travel遵照既有术语；全屏混乱设置以Player blur shader实际行为裁决，不是通知消息流。\n\n批次提交、finalize和推送闭合后提前进入窗口7，仅处理这8条；不扩展旧pending、blocked、其他repair或全局术语。\n')
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
