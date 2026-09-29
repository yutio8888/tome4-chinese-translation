"""Aggregate completed groups without conflating unavailable evidence or eligibility."""
import collections, json
from pathlib import Path
from series import SERIES, read, write, sync, module
ARMS=("opus","sol","gemini")
def stats(rows,correct):
    resolved=[r for r in rows if r["reference_status"]!="PENDING"]
    common=[r for r in resolved if all(r["arms"][a]["verdict"] in {"ISSUE","OK","ADVISORY"} for a in ARMS)]
    result={"entries":len(rows),"resolved":len(resolved),"reference_pending":len(rows)-len(resolved),"common":len(common),"issue_entries":sum(r["reference_status"]=="ISSUE" for r in resolved),"arms":{}}
    def ratio(n,d): return {"numerator":n,"denominator":d,"rate":n/d if d else None}
    for a in ARMS:
        matched=sum(r["reference_status"]=="ISSUE" and correct(r,a) for r in resolved)
        reported=sum(r["arms"][a]["verdict"]=="ISSUE" for r in resolved)
        tp=sum(len(set(r["arms"][a]["confirmed_defects"])) for r in resolved if r["arms"][a]["verdict"]=="ISSUE")
        fp=sum(len(r["arms"][a]["refuted_claims"]) for r in resolved if r["arms"][a]["verdict"]=="ISSUE")
        result["arms"][a]={"all_resolved_accuracy":ratio(sum(correct(r,a) for r in resolved),len(resolved)),"common_accuracy":ratio(sum(correct(r,a) for r in common),len(common)),"issue_precision":ratio(matched,reported),"issue_recall":ratio(matched,result["issue_entries"]),"claim_precision":ratio(tp,tp+fp),"claim_recall":ratio(tp,sum(len(r["reference_defects"]) for r in resolved)),"abstentions":sum(r["arms"][a]["verdict"]=="PENDING" for r in rows)}
        result["arms"][a]["label_only_accuracy_diagnostic"]=ratio(sum((r["reference_status"]=="ISSUE" and r["arms"][a]["verdict"]=="ISSUE") or (r["reference_status"]=="OK" and r["arms"][a]["verdict"] in {"OK","ADVISORY"}) for r in resolved),len(resolved))
    return result
def main():
    state=sync();rows=[];by_group=[];ledger=[];failures=[];incomplete=[]
    scorer=module(SERIES.parent/"abc-40-b096-20260923","score")
    for g in state["groups"]:
        if not g.get("legacy"):
            gs=read(SERIES.parent/g["directory"]/"STATE.json")
            for c in gs["child_dispatches"]:
                terminal=c.get("terminal_observation",{})
                if terminal.get("status")=="error":
                    failures.append({"group":g["index"],"dispatch":c["dispatch_id"],"provider":c["requested_provider"],"error":terminal.get("lastError"),"archived":c["archive_confirmed"],"replacement":c.get("replacement_dispatch")})
                elif c.get('output_integrity_valid') is False:
                    incomplete.append({'group':g['index'],'dispatch':c['dispatch_id'],'reason':c['exclusion_reason'],'archived':c['archive_confirmed'],'replacement':c.get('replacement_dispatch')})
        if g["state"]!="DONE": continue
        root=SERIES.parent/g["directory"];scoring=read(root/"SCORING.json")
        entries={e["audit_id"]:e for e in read(root/"entries.json")}
        eligible=all(scoring["primary_eligibility"].values())
        transports={}
        if not g.get('legacy'):
            selection=read(root/'SELECTION.json') if (root/'SELECTION.json').exists() else {}
            for a in ARMS:
                dispatch=selection.get(a,a+'-01')
                transports[a]=next(c['requested_provider'] for c in gs['child_dispatches'] if c['dispatch_id']==dispatch)
        else:
            transports={a:'legacy-preserved-see-group-record' for a in ARMS}
        for r in scoring["entries"]:
            r.update(group=g["index"],component=entries[r["entry_id"]]["component"],three_arm_eligible=eligible)
            r["protocol_family"]="v2" if g["index"]==1 else "v3-temp" if g["index"]<=3 else "v3-source"
            r["source_pinning"]="engine_commit_pinned" if r["component"]=="tome" else "public_snapshot_commit_unpinned" if r["component"] in {"ashes-urhrok","cults","orcs"} else "source_unavailable"
            r['gemini_transport']=transports['gemini']
            rows.append(r)
        by_group.append({"group":g["index"],"directory":g["directory"],"three_arm_eligible":eligible,"transports":transports,"metrics":stats(scoring["entries"],scorer.correct)})
        reference=read(root/"REFERENCE.json")
        for did,d in reference.get("canonical_defects",{}).items():
            ledger.append({"group":g["index"],"canonical_id":f"g{g['index']:02}-{did}",**d,"reference":str(root/"REFERENCE.json")})
    eligible=[r for r in rows if r["three_arm_eligible"]]
    components=sorted(set(r["component"] for r in eligible))
    target=state.get('target_groups',20)
    result={"status":state["state"],"completed_groups":state["completed_groups"],"target_groups":target,"reference":"provisional model adjudication, not human gold","eligible_three_arm":stats(eligible,scorer.correct),"all_content_diagnostic":stats(rows,scorer.correct),"by_component":{c:stats([r for r in eligible if r["component"]==c],scorer.correct) for c in components},"groups":by_group}
    result['scope_change']=state.get('scope_change')
    result["infrastructure_failures_group3_onward"]=failures
    result['incomplete_outputs_group3_onward']=incomplete
    result["by_protocol"]={p:stats([r for r in eligible if r["protocol_family"]==p],scorer.correct) for p in sorted(set(r["protocol_family"] for r in eligible))}
    result["by_source_pinning"]={p:stats([r for r in eligible if r["source_pinning"]==p],scorer.correct) for p in sorted(set(r["source_pinning"] for r in eligible))}
    result['by_gemini_transport']={p:stats([r for r in eligible if r['gemini_transport']==p],scorer.correct) for p in sorted(set(r['gemini_transport'] for r in eligible))}
    write(SERIES/"AGGREGATE.json",result)
    write(SERIES/"MERGED-FINDINGS.json",{"reference":result["reference"],"completed_groups":state["completed_groups"],"defects":ledger,"note":"Canonical IDs are local to a group and prefixed here; recurring semantics across distinct entries are not silently collapsed."})
    lines=[f"# {target}组审核对比实验"+('报告' if state['state']=='DONE_research_only' else '进度'),"",f"已闭合 {state['completed_groups']}/{target} 组；累计 {len(rows)}/{target*40} 条。暂定模型参考，不是人工金标准。","",
        "| 组 | 范围与结果 | Opus 条目正确 | Sol 条目正确 | Gemini 条目正确 | 合规三方比较 |","|---|---|---|---|---|---|"]
    def f(x):return f"{x['numerator']}/{x['denominator']}"
    for g in by_group:
        m=g["metrics"];lines.append("| "+" | ".join([str(g["group"]),f"[结果](../{g['directory']}/RESULT.md)",*[f(m["arms"][a]["all_resolved_accuracy"]) for a in ARMS],"是" if g["three_arm_eligible"] else "否，仅诊断"])+" |")
    pooled=result['eligible_three_arm']
    lines += ['', f"合规三方配对汇总覆盖 {pooled['entries']} 条，其中 {pooled['resolved']} 条已裁定、{pooled['reference_pending']} 条参考待确认。正确率要求判定及问题理由匹配；待确认不进入已裁定分母。", '',
        '| 模型 | 已裁定条目正确率 | 问题条目精确率 | 问题条目召回率 | 原子缺陷召回率 |',
        '|---|---|---|---|---|']
    def percentage(x):
        return f(x)+(f"（{x['rate']:.1%}）" if x['rate'] is not None else '（N/A）')
    for a,label in [('opus','Opus 5.5'),('sol','GPT-6 Sol'),('gemini','Gemini 3.8 Flash')]:
        lines.append('| '+' | '.join([label,*[percentage(pooled['arms'][a][k]) for k in ['all_resolved_accuracy','issue_precision','issue_recall','claim_recall']]])+' |')
    lines+=["","合规汇总排除首组旧流程违规臂所处的三方配对组；原内容成绩保留于诊断汇总。参考裁决与Sol属同一模型家族；队列不是随机抽样。DLC使用获准公开快照，目标版本来源限制与pending不可当作已核实真值。共同输入含原库存元数据，不能宣称完全无历史字段暴露的严格盲测。",'',f"第3组起记录 {len(failures)} 次基础设施失败、{len(incomplete)} 次最终交付不完整；原运行与替代dispatch均保留，不计为内容错误。不完整输出的底层原因未经证实。", "","[分层统计](AGGREGATE.json) · [跨组问题台账](MERGED-FINDINGS.json)",""]
    (SERIES/"RESULT.md").write_text("\n".join(lines))
    if state.get('scope_change'):
        with (SERIES/'RESULT.md').open('a') as output:
            output.write('\n用户将范围由20组收束至第14组；第15–20组仅保留预先冻结的材料，未派发、未计分，不计为已完成审核。\n')
    if any(r['gemini_transport']=='pi/cpa/gemini-3.8-flash-high' for r in rows):
        with (SERIES/'RESULT.md').open('a') as output:
            output.write('\n部分 Gemini 运行使用 CPA 同名模型通道，各组实际通道见记录。通道差异及分层成绩见 AGGREGATE.json 的 by_gemini_transport，不能据此声称所有运行环境完全一致。\n')
    print(json.dumps({"completed":state["completed_groups"],"entries":len(rows),"eligible":len(eligible),"defects":len(ledger)}))
if __name__=="__main__":main()
