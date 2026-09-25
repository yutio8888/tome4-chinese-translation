import json,pathlib,subprocess,hashlib,datetime
R=pathlib.Path.cwd()
cp=json.loads((R/'.artifacts/i18n/production-review-v2-lite/active-batch.json').read_text())
b=cp['batch_id'];D=R/'.ai/task'/b;D.mkdir(parents=True,exist_ok=True)
w=json.loads((R/'evidence/quality/production-batches'/f'{b}-source-workset.json').read_text())
assert w['batch_id']==b
print(type(w['source_verification']).__name__)
files={};records=[];excerpts=[]
for v in w['source_verification']:
 pinned=v['source_pinning']=='pinned'
 if pinned:
  assert v['verification_status']=='confirmed' and v['fixed_source_commit'],v
 else:
  assert v['component'] in ('ashes-urhrok','cults') and v['verification_status'] is None and v['fixed_source_commit'] is None,v
 key=(v['fixed_source_commit'] if pinned else 'unpinned-public-dlc:'+v['component'],v['public_source_path'])
 if key not in files:
  if pinned:
   raw=subprocess.check_output(['git','-C','/workspace/t-engine4','show',f'{key[0]}:{key[1]}'])
  else:
   raw=(pathlib.Path('/workspace/tome4-dlcs')/v['component']/key[1]).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==v['source_file_sha256']
  files[key]=raw
 records.append(dict(entry_revision_identity=v['entry_revision_identity'],fixed_source_commit=v['fixed_source_commit'],source_pinning=v['source_pinning'],public_source_path=key[1],source_file_sha256=v['source_file_sha256'],source_bytes_match_recorded_sha256=True,source_commit_unfixed=not pinned,source_verification=v))
 lines=files[key].decode().splitlines();hits=v.get('matching_literal_lines')
 if hits is None and 'lowercased_entity_name_verification' in v:
  proof=v['lowercased_entity_name_verification'];assert proof['status']=='confirmed'
  hits=proof['argument_lines']+proof['lower_lines']
  assert v['source']==proof['resolved_argument'].lower()
 elif hits is None:
  proof=v['concatenated_entity_name_verification'];assert proof['status']=='confirmed'
  hits=proof['argument_lines']+proof['concat_lines']
  assert v['source']==proof['literal_prefix']+proof['resolved_argument'].lower()
 indexes=sorted(set(i for n in hits for i in range(max(0,n-3),min(len(lines),n+2))))
 excerpts.append(dict(entry_revision_identity=v['entry_revision_identity'],public_source_path=key[1],lines=[dict(line=i+1,text=lines[i]) for i in indexes]))
(D/'HOST-SOURCE-VERIFICATION.json').write_text(json.dumps(dict(batch_id=b,entry_count=len(records),fixed_git_files_verified=len(files),verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),entries=records),ensure_ascii=False,indent=2)+'\n')
(D/'HOST-SOURCE-EXCERPTS.json').write_text(json.dumps(excerpts,ensure_ascii=False,indent=2)+'\n')
(D/'SCOPE.json').write_text(json.dumps(dict(schema_version=1,allowed_files=[],anchor_scopes=[],review_only_files=sorted(set(e['normalized_path'] for e in cp['entry_snapshots'])),ordered_revisions=cp['selected']),ensure_ascii=False,indent=2)+'\n')
comp_label='+'.join(sorted({{'tome-ashes-urhrok.lua':'Ashes','tome-cults.lua':'Cults','tome-orcs.lua':'Orcs'}.get(e['normalized_path'],e['normalized_path']) for e in cp['entry_snapshots']}))
(D/'SPEC.md').write_text(f"审核293，修复积压重新累计（未达20条不开窗）。用户2026-09-25解除暂停，授权继续审核；既有审核外发与推送授权有效，无需逐批确认；争议条目列pending。surface codex/gpt-6-sol，contextual claude/claude-opus-5-5。基线{cp['base_commit']}，范围为SCOPE.json和checkpoint冻结的{len(cp['selected'])}个revision。只读审核；主代理按本批 SHA 核验的 {comp_label} 公开源码裁决；DLC 来源仓库和 commit 未固定，不改译文、术语、规则或旧冻结输入。确认项汇总至下一修复窗口（积压达20条后开窗）。既有Archmage策略和旧blocked保持排除，不扩大历史pending/advisory。独立reviewer仅按envelope及完整对应契约读取。\n")
(D/'PLAN.md').write_text("1. 冻结源码workset，宿主逐条核验固定源码，派发前建立SPEC/PLAN/SCOPE。\n2. 导出surface四lane并独立审核；验证strict、native来源、读取边界并归档。\n3. surface import后构建准确contextual draft，先anchor preflight再export/freeze，独立复核并归档。\n4. 宿主按源码裁决，完整门禁、构建、两任务DONE重放、证据提交、finalize、交接、队列同步和push。\n")
print(json.dumps(dict(batch_id=b,entries=len(records),files=len(files))))
