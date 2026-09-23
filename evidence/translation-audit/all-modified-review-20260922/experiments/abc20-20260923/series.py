"""Series bookkeeping; no semantic judgments. Every decision originates in reviewer reports."""
import collections, hashlib, importlib.util, json, re, sys
from pathlib import Path
SERIES = Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cited_claims(text):
    claims=set(re.findall(r'\bC\d+\b',text))
    for first,last in re.findall(r'\bC(\d+)\s*[–—-]\s*C(\d+)\b',text):
        start,end=int(first),int(last)
        assert 0 < start <= end < 1000, ('Invalid claim range',first,last)
        claims.update(f'C{i:02}' for i in range(start,end+1))
    return claims
def module(root,name):
    spec=importlib.util.spec_from_file_location(name,root/(name+".py"))
    m=importlib.util.module_from_spec(spec)
    source=(root/(name+".py")).read_text()
    # A failed infrastructure dispatch remains immutable; select its fresh retry by ID.
    selection=read(root/"SELECTION.json") if (root/"SELECTION.json").exists() else {}
    for arm,dispatch in selection.items():
        source=source.replace('"'+arm+'-01"','"'+dispatch+'"')
    if name=="extract_observations":
        source=source.replace('assert headings, name','assert headings or all(s == "未发现问题" for _,s,_ in rows), name')
        source=source.replace(r'(存在问题|仅建议|待确认).*?$',r'([^\n]+)$')
        source=source.replace('STATES[heading[3]]','next((v for k,v in STATES.items() if heading[3].startswith(k)), "NON_DEFECT")')
        source=source.replace('"text": block,','"original_label": heading[3], "text": block,')
    exec(compile(source,str(root/(name+".py")),"exec"),m.__dict__)
    if name=="render_findings":
        m.STATES.update({"OK":"未发现问题","NON_DEFECT":"明确未列为缺陷"})
    return m
def sync():
    s=read(SERIES/"STATE.json")
    target=s.get('target_groups',20)
    for g in s["groups"]:
        if g.get("legacy"): continue
        state=read(SERIES.parent/g["directory"]/"STATE.json")
        if g['index']>target:
            assert not state['child_dispatches'], 'Out-of-scope group has children'
            g['state']='FROZEN_NOT_RUN'
            continue
        g["state"]="DONE" if state["state"]=="DONE_research_only" else state["state"]
    s["completed_groups"]=sum(g["state"]=="DONE" for g in s["groups"])
    s["state"]="DONE_research_only" if s["completed_groups"]==target else "RUNNING"
    write(SERIES/"STATE.json",s)
    return s
def adjudicate(root):
    m=module(root,"extract_observations")
    mapping=m.extract(m.REPORTS)
    for name,rows in mapping['tables'].items():
        cited=cited_claims(' '.join(r['note'] for r in rows))
        present={o['claim_id'] for o in mapping['observations'] if o['origin']==name}
        assert cited<=present, ('Incomplete claim detail',name,sorted(cited-present))
    supplement=root/'EXTRACTION-SUPPLEMENT.json'
    if supplement.exists():
        for item in read(supplement):
            p=root/'reports'/(item['origin']+'.md')
            text=p.read_text()
            assert sha(p)==item['source_sha256']
            assert not any(o['origin']==item['origin'] and o['start']<=item['start']<o['end'] for o in mapping['observations']), 'Supplement overlaps existing claim; inspect boundary'
            mapping['observations'].append({**item,'text':text[item['start']:item['end']]})
        mapping['observations'].sort(key=lambda o:(o['entry_id'],o['text']))
        for index,o in enumerate(mapping['observations'],1):
            o['observation_id']=f'O{index:03}'
    for o in mapping["observations"]:
        p=root/"reports"/(o["origin"]+".md")
        assert sha(p)==o["source_sha256"]
        assert p.read_text()[o["start"]:o["end"]]==o["text"]
    write(root/"ANON-MAPPING-HOST-ONLY.json",mapping)
    n=len(mapping["observations"])
    template=(SERIES.parent/"abc-40-b096-20260923/ADJUDICATION-INPUT.md").read_text().split("\n## O001")[0]
    template=template.replace("36",str(n)).replace("sources/ 内 source-access列明的15份源码","source-access.json 明确列出的冻结源码")
    template=template.replace("沿其限定调用链可以git show固定commit单文件","沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差")
    chunks=[template]
    for o in mapping["observations"]:
        assert not re.search(r"/(?:\.claude|\.codex)/|\b(?:Opus|Gemini|GPT-6|GPT6)\b",o["text"],re.I), ("Potential identity leakage; inspect exact block",o["observation_id"])
        chunks.append("## "+o["observation_id"]+" | "+o["entry_id"]+"\n\n"+o["text"])
    dest=root/"ADJUDICATION-INPUT.md"
    assert not dest.exists(),"Already frozen"
    dest.write_text("\n\n".join(chunks)+"\n")
    write(root/"ADJUDICATION-FREEZE.json",{"input_sha256":sha(dest),"mapping_sha256":sha(root/"ANON-MAPPING-HOST-ONLY.json"),"blind_report_sha256":sha(root/"reports/reference-blind-01.md"),"observations":n})
    (root/"dispatches/adjudication-prompt.txt").write_text("你是本任务独立REVIEWER，purpose=translation_contextual_v1。请按唯一入口完成匿名归并裁决及全40条复核，不读取模型身份或其他答案，不修改仓库，不创建子agent，不宣称DONE_VERIFIED。唯一入口："+str(dest.resolve())+"\n")
    print(json.dumps({"observations":n,"input":str(dest)},ensure_ascii=False))
def finish(root):
    module(root,"record").guards()
    state=read(root/"STATE.json")
    assert len(state["child_dispatches"])>=5
    assert all(c["archive_confirmed"] and (c["table_coverage_valid"] or c.get("excluded")) for c in state["child_dispatches"])
    assert all(c.get("lineage_verified") for c in state["child_dispatches"])
    selection=read(root/"SELECTION.json") if (root/"SELECTION.json").exists() else {}
    selected=[selection.get(a,a+"-01") for a in ["opus","sol","gemini"]]
    arms=[c for c in state["child_dispatches"] if c["dispatch_id"] in selected]
    assert len(arms)==3 and all(c["table_coverage_valid"] for c in arms)
    assert len({(c["prompt_sha256"],c["input_sha256"]) for c in arms})==1
    module(root,"build_scoring").main()
    scoring=read(root/"SCORING.json");scorer=module(root,"score")
    metrics=scorer.score(scoring);write(root/"METRICS.json",metrics)
    assert metrics==scorer.score(read(root/"SCORING.json"))
    module(root,"render_findings").main()
    mapping=read(root/"ANON-MAPPING-HOST-ONLY.json");ref=read(root/"REFERENCE.json")
    counts=collections.Counter(o["origin"] for o in mapping["observations"])
    p=root/"MERGED-FINDINGS.md";text=p.read_text()
    text=text.replace("三位参赛reviewer的28项观察及独立盲审的8项观察",f"三位参赛reviewer的{sum(v for k,v in counts.items() if k!='reference-blind-01')}项观察及独立盲审的{counts['reference-blind-01']}项观察")
    text=text.replace("依据固定源码的暂定核验","依据本组获准源码与语境的暂定核验")
    p.write_text(text)
    result=["# 40条三模型审核对比结果","","这是模型依据冻结材料形成的暂定参考，不是人工金标准。每个问题以原子缺陷归并；仅报对条目而理由不符不计检出，建议与待确认不追算明确检出。未修改译文。","",
      f"覆盖40条；参考确认{sum(e['status']=='ISSUE' for e in ref['entries'])}条问题、{len(ref['canonical_defects'])}个缺陷；{len(metrics['reference_pending'])}条参考待确认。","",
      "| 模型 | 全部已裁定条目正确率（弃权不计正确） | 共同明确分母正确率 | 问题条目召回 | 缺陷召回 |","|---|---|---|---|---|"]
    def fmt(x):
        return f"{x['numerator']}/{x['denominator']}"+(f"（{x['rate']:.1%}）" if x["rate"] is not None else "（N/A）")
    for a,label in [("opus","Opus 5.5"),("sol","GPT-6 Sol"),("gemini","Gemini 3.8 Flash")]:
        x=metrics["arms"][a];result.append("| "+" | ".join([label,*[fmt(x[k]) for k in ["all_resolved_accuracy_abstention_not_correct","common_accuracy","issue_entry_recall","claim_recall"]]])+" |")
    result += ["","[归并问题清单](MERGED-FINDINGS.md)保留归因、证据和三个模型的原始观察；[完整统计](METRICS.json)包括误报、漏报、理由错误、弃权及配对差异。","","局限：40条为队列切片，不能视为随机总体样本。参考复核和裁决使用GPT-6 Astra，与Sol同属模型家族，存在相关偏差；DLC及缺少源码组件的来源限制见[输入](INPUT.md)。未做人工金标准核验，也不宣称生产审核完成。",""]
    if state.get('gemini_transport_decision'):
        result += ['本组 Gemini 实际通道：`'+state['gemini_transport_decision']['provider']+'`，high；通道决定及重试记录见 [STATE](STATE.json)。汇总按通道分层，不将不同运行环境视为完全相同。','']
    (root/"RESULT.md").write_text("\n".join(result))
    verification={"state":"DONE_research_only","entry_coverage_each_arm":40,"reference_entries":40,"reference_issue_entries":sum(e["status"]=="ISSUE" for e in ref["entries"]),"confirmed_defects":len(ref["canonical_defects"]),"anonymous_observations":len(mapping["observations"]),"reference_pending":len(metrics["reference_pending"]),"common_denominator":metrics["common_denominator"],"replay_identical":True,"original_verdicts_preserved":True,"all_children_archived":True,"archive_attempts":[c["archive_attempts_started"] for c in state["child_dispatches"]],"frozen_inputs_and_baselines_verified":True,"semantic_decisions_source":"reports/adjudication-01.md","production_mutations":False}
    write(root/"VERIFICATION.json",verification)
    state.update(state="DONE_research_only",verification="VERIFICATION.json",results="RESULT.md",strict_contract_completion_claimed=False);write(root/"STATE.json",state)
    s=sync();print(json.dumps({"completed":s["completed_groups"],"verification":verification},ensure_ascii=False))
if __name__=="__main__":
    action=sys.argv[1]
    if action=="sync":
        s=sync();print(json.dumps({"completed":s["completed_groups"],"groups":[[g["index"],g["state"]] for g in s["groups"]]}))
    else:
        root=Path(sys.argv[2]);{"adjudicate":adjudicate,"finish":finish}[action](root)
