"""Render the bounded experiment report from preserved adjudication and scores."""
import itertools
from collections import Counter
from series import SERIES, read, write, module

ARMS = ('opus', 'sol', 'gemini')
NAMES = {'opus': 'Opus 5.5', 'sol': 'GPT-6 Sol', 'gemini': 'Gemini 3.8 Flash High'}

def pct(r):
    return f"{r['numerator']}/{r['denominator']}（{r['rate']:.1%}）" if r['rate'] is not None else 'N/A'

def main():
    state, aggregate = read(SERIES/'STATE.json'), read(SERIES/'AGGREGATE.json')
    assert state['state'] == aggregate['status'] == 'DONE_research_only'
    assert state['completed_groups'] == state['target_groups'] == aggregate['completed_groups']
    rows, all_rows, pending = [], [], []
    for g in state['groups']:
        if g['state'] != 'DONE':
            continue
        root = SERIES.parent/g['directory']
        scoring, reference = read(root/'SCORING.json'), read(root/'REFERENCE.json')
        for row in scoring['entries']:
            copied = {**row, 'group': g['index']}
            all_rows.append(copied)
            if all(scoring['primary_eligibility'].values()):
                rows.append(copied)
        for row in reference['entries']:
            if row['status'] == 'PENDING':
                pending.append({'group':g['index'], **row,
                                'report':f"../{g['directory']}/reports/adjudication-01.md"})
    assert len(all_rows) == state['target_groups']*40
    scorer = module(SERIES.parent/'abc-40-b096-20260923','score')
    resolved = [r for r in rows if r['reference_status'] != 'PENDING']
    total_defects = sum(len(r['reference_defects']) for r in resolved)
    combinations = []
    for n in (1,2,3):
        for arms in itertools.combinations(ARMS,n):
            detected = sum(len(set().union(*(set(r['arms'][a]['confirmed_defects'])
                       if r['arms'][a]['verdict']=='ISSUE' else set() for a in arms))) for r in resolved)
            combinations.append({'arms':list(arms),'matched_defects':detected,
                                 'reference_defects':total_defects})
    paired = []
    for a,b in itertools.combinations(ARMS,2):
        paired.append({'left':a,'right':b,
            'left_only_correct':sum(scorer.correct(r,a) and not scorer.correct(r,b) for r in resolved),
            'right_only_correct':sum(scorer.correct(r,b) and not scorer.correct(r,a) for r in resolved)})
    counts = Counter(r['reference_status'] for r in all_rows)
    write(SERIES/'REPORT-DATA.json',{'target_groups':state['target_groups'],
        'reference_status_counts_all_groups':dict(counts), 'paired_all_resolved':paired,
        'confirmed_defect_unions':combinations,'pending_entries':pending,
        'pending_note':'Only entry-level PENDING is indexed here; ISSUE entries can contain further pending claims. See full adjudication reports.'})
    pooled = aggregate['eligible_three_arm']
    lines = [f"# {state['target_groups']}组译文审核对比报告",'',
        f"按用户最新指令，实验在第14组完成后停止。累计审核560条；第15–20组没有派发。原始报告、匿名观察映射、裁决、计分和归档证据均保留。译文、术语库及生产审核状态未修改。",'',
        f"14组暂定参考共判定{counts['ISSUE']}条存在问题、{counts['PENDING']}条待确认、{counts['OK']}条未发现确认缺陷（含仅建议）。共归并{len(read(SERIES/'MERGED-FINDINGS.json')['defects'])}项确认缺陷。这里的“确认”是模型依据冻结材料的裁决状态，不是人工金标准。",'',
        '## 三模型表现','',
        f"主比较覆盖第2–14组的{pooled['entries']}条：{pooled['resolved']}条已有明确参考判定，{pooled['reference_pending']}条参考待确认排除在分母外。首组流程不合规的三方配对结果只作诊断保留。",'',
        '| 模型 | 条目正确率 | 问题条目精确率 | 问题条目召回率 | 原子缺陷召回率 |',
        '|---|---|---|---|---|']
    for a in ARMS:
        lines.append('| '+' | '.join([NAMES[a],*[pct(pooled['arms'][a][k]) for k in
            ('all_resolved_accuracy','issue_precision','issue_recall','claim_recall')]])+' |')
    leaders = {k:max(ARMS,key=lambda a:pooled['arms'][a][k]['rate']) for k in
               ('all_resolved_accuracy','issue_precision','issue_recall','claim_recall')}
    lines += ['', f"在本次主比较中，{NAMES[leaders['all_resolved_accuracy']]}的条目正确率最高；"
              f"{NAMES[leaders['issue_recall']]}检出的确认问题条目比例最高；"
              f"{NAMES[leaders['issue_precision']]}的报错条目精确率最高，"
              f"{NAMES[leaders['claim_recall']]}覆盖的具体缺陷最多。这些指标衡量不同取舍，不能合并成一个不加限定的“最好模型”。"]
    for x in paired:
        if {x['left'],x['right']} == {'opus','sol'}:
            lines += ['', f"Opus与Sol在同一已裁定分母上的配对差异：仅Opus正确{x['left_only_correct']}条，仅Sol正确{x['right_only_correct']}条；"
                      '这比只看四舍五入的百分比更直观。本报告不检验统计显著性，也不估计多次运行稳定性。']
    lines += ['', '条目正确率要求判定和理由匹配：对问题条目至少指出一项被裁决支持的具体缺陷才算正确。问题条目精确率衡量报出的“有问题”中有多少理由成立；召回率衡量参考问题条目被找出的比例。原子缺陷召回率按每项具体错误计数。模型仅建议或待确认的观察不追算为明确检出；参考已裁定时，模型弃权也不计正确。', '',
        f"主比较中，全部判为无问题也能获得{(pooled['resolved']-pooled['issue_entries'])/pooled['resolved']:.1%}的条目正确率，因此应同时看召回率。单条找到一项缺陷即可算条目正确，而长条目可能包含多项缺陷，两个指标不应混为一谈。", '',
        '按组件分层的条目正确率如下，所有分母均排除参考待确认；分层样本量小，不作总体能力排名。', '',
        '| 组件 | 覆盖条目 | 已裁定条目 | Opus | Sol | Gemini |', '|---|---|---|---|---|---|']
    for component,x in aggregate['by_component'].items():
        lines.append('| '+' | '.join([component,str(x['entries']),str(x['resolved']),
            *[pct(x['arms'][a]['all_resolved_accuracy']) for a in ARMS]])+' |')
    lines += ['',
        '## 多模型互补','',
        '| 审核组合 | 覆盖的确认缺陷 |', '|---|---|']
    for x in combinations:
        lines.append('| '+' + '.join(NAMES[a] for a in x['arms'])+f" | {x['matched_defects']}/{x['reference_defects']}（{x['matched_defects']/x['reference_defects']:.1%}） |")
    lines += ['', '组合表只计算经过裁决支持的缺陷并集，用来观察互补性；它没有把未经裁决的多模型意见自动当成事实，也未计入组合带来的额外误报审核成本。各组样本和运行时间不同，本实验不能据此评价单位成本或速度。', '',
        '## 来源与运行限制','',
        '- 每组40条，三臂使用相同冻结输入和提示；另有独立全量盲审，再由新会话匿名归并全部观察并复核全40条。参考与Sol同属模型家族，可能存在相关偏差。',
        '- 样本按队列有界切片取得，未随机抽样；长篇叙事和短日志的缺陷数量不同。总体准确率也受大量无问题条目影响，不能单独作为优劣结论。',
        '- 本体使用固定commit；DLC仅固定公开快照哈希，仓库、commit及目标版本对应关系未固定；addon-dev及items-vault无可用源码。机制疑点与文本确认缺陷分开处理。',
        '- “独立盲审”指不读取参赛答案；共同冻结材料仍含原库存元数据，不能称为完全无历史字段暴露的严格盲测。匿名归并隐去模型身份，但文字风格仍可能被辨认。',
        '- 第10、11组Gemini由AGY失败后转CPA，第12–14组预先选用CPA同名High通道。身份和重试均有记录；通道及样本同时变化，不能将分层差异解释为单纯通道效果。',
        '- 三臂均请求High，但不同提供方的思考档位、客户端和工具权限并不等价。本次未取得可靠可比的费用、token或端到端耗时，不比较成本和速度。',
        f"- 第3组起记录{len(aggregate['infrastructure_failures_group3_onward'])}次终态基础设施失败、{len(aggregate['incomplete_outputs_group3_onward'])}次最终交付不完整。失败运行不计为内容错误，替代运行不按语义成绩挑选；原证据保留。", '',
        '发现一处跨组裁决尺度差异：第12组O013将“all damage→伤害”列为建议，第14组D07却将同类省略列为缺陷。原报告及正式计分保持不变；若人工将第14组entry-03714改判为建议，三臂正确数都会增加1，缺陷分母减少1，相对正确数差不变。这是明确的参考校准局限，详见[宿主核查记录](HOST-CHECKS.md)。', '',
        '## 可复查材料','',
        '- [逐组结果与总表](RESULT.md)',
        '- [完整分层统计](AGGREGATE.json)：组件、来源固定程度、协议及Gemini通道。',
        '- [跨组确认缺陷台账](MERGED-FINDINGS.json)：按组加前缀，避免局部D编号碰撞。',
        '- [配对差异、缺陷并集与待确认条目索引](REPORT-DATA.json)：ISSUE条目内的其他待确认claim请查原裁决。',
        '- [最终机械验证](FINAL-VERIFICATION.json)：输入哈希、覆盖、原始观察映射、计分重放、模型身份及子agent归档。', '',
        '- [生命周期闭合记录](FINAL-LIFECYCLE.json)：本实验83个子任务均已确认归档，第15–20组派发数为0。', '',
        '本报告交付的是只读研究结果。未将任何条目标记为生产DONE_VERIFIED，也未应用修复或提交仓库。','']
    (SERIES/'REPORT.md').write_text('\n'.join(lines))

if __name__ == '__main__':
    main()
