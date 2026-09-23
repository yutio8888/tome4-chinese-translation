"""Render the final audit trail; no judgments are computed by this formatter."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
def esc(x):return str(x).replace('|','\\|').replace('\n',' ')
def main():
    d=json.loads((P/'ADJUDICATION.json').read_text())
    lines=['# 宿主逐项裁决记录','',
    '这是本轮研究参考集，不是人工金标准或生产验收。H 编号源于报告揭示前的独立初审，N 编号为揭示候选后补充。原始意见、初判与修订均另行保留；候选低影响并不自动撤销，合理等价读法也不自动确认为错译。', '',
    '所有文本判断以冻结 entries.json 的完整原译为依据。Orcs 源码仅固定文件哈希，目标发布版本未固定；Possessors 源码不可用。表内 section 是冻结快照路径，不能称为固定 DLC commit。', '',
    '| 编号 | entry-ID | 最终状态 | 影响 | 原译锚点与结论 | 最强反证／处理 | 证据 |','|---|---|---|---|---|---|---|']
    for c in d['canonical']:
        e=c.get('evidence',{});ev=e.get('file') or e.get('section') or '冻结原译；实现缺失'
        if e.get('line'):ev+=':'+str(e['line'])
        reason=c.get('revision_reason',c['reason'])
        lines.append('| '+' | '.join(map(esc,[c['id'],c['entry'],c['status'],c['impact'],c['source_quote']+' → '+c['target_quote']+'；'+reason,c['strongest_counterevidence'],ev]))+' |')
    lines+=['','## 原始候选到参考项的映射','','confirmed 候选降为表达建议时，host_decision=refuted 表示其“确认错译”主张不成立，并非否认它可以润色。pending 不计入真阳或假阳。复合候选按独立意义变化拆子编号；重复分支和重复措辞统一合并。','',
    '| 阶段与原编号 | 原状态 | 宿主裁决 | 参考编号 | 备注 |','|---|---|---|---|---|']
    for o in d['observations']:
        lines.append('| '+' | '.join(map(esc,[o['stage']+':'+o['id'],o['source_status'],o['host_decision'],', '.join(o['canonical']),o.get('reason','见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。')]))+' |')
    (P/'ADJUDICATION.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
