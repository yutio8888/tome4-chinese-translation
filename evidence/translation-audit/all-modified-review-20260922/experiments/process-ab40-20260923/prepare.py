"""Prepare a bounded, paired process experiment; no production mutation."""
import csv, hashlib, json, random, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
PRIOR = ROOT.parent / 'calibrated-pilot40-20260923'
SERIES = ROOT.parent / 'abc20-20260923'
REPO = Path.cwd()

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def length(e): return 'short' if len(e['source']) <= 160 else 'medium' if len(e['source']) <= 800 else 'long'

RULES = '''# 冻结审核规则
本轮为用户授权的只读研究旁路，非正式生产审核。只返回观察，不宣称 DONE_VERIFIED。不得写文件、创建子代理、读取其他报告或遍历仓库。入口中列出的 files 是唯一文字输入；source-access.json 明列的源码和已读文件明确引用的单一额外源码可读，必须核哈希；禁止替代缺失组件。

1. 审完整句段、指代及运行消费，不逐词计漏译。每项问题给精确原译短引、具体意义变化、最强上下文反证、证据位置及影响。非直译不等于错译；reasonable equivalent readings mean no confirmed defect without further evidence.
2. 术语同时核对大小写、source_tag、category/notes、status 和 scope。existing 不强制改名。global/multi 覆盖所有；dlc=ashes-urhrok,cults,items-vault,orcs,possessors；core 排除这五个；addon=addon-dev,items-vault,possessors。词形出现不证明语境匹配。使用本包 terms.json，不追读旧规则。
3. 无类型限制的“增加伤害”或“受到额外伤害”可以表达全伤害/全来源；代码 all 不要求中文逐字出现“所有”。须有实质范围变化才判错。
4. 保持参数消费、有效标记和信息结构，不机械比较空格、空行、标点和大小写强调。动态拼接检查空/非空后缀；静态渲染不等于游戏测试。
5. 用户定标的三个边界：主句已限定造成伤害时的“攻击的第一个生物”、文明人→普通人、受到熵能反冲概括施加与增强，列 needs clarification/advisory，不计确认错译；不泛化到其他不同语境。
6. 正确性与修复优先级分开。低影响但有充分证据的语义偏差仍可 confirmed；高影响猜测仍 pending。纯措辞偏好 advisory。不得因风味文字不影响机制就自动抹去明确数值、关系或事件变化。
7. 分别说明 text_status、snapshot_fact、target_applicability、impact。纯文本偏差可确认；依赖未固定 DLC 机制或目标版本的判断保留适用性缺口。忠实沿袭上游的问题单列，不算译文新增。
8. 报告没有最低问题数。OK 不等于推荐措辞。只按本轮明确证据判断，不预测其他审核者。

输出中文：先按输入顺序给完整 entry-ID | ISSUE/PENDING/OK | claim编号或简短依据 表；再列原子 C01... 观察，每项含 entry-ID、精确短引、意义变化、最强反证及处理、confirmed/pending/advisory、证据、影响与版本限制。最后列实际读取文件。记录每项影响为机制/操作、叙事事实、表达建议之一；不要把影响标签当成正确性判定。报告尽量紧凑，但不得为凑字数漏条目或证据。
'''

PROTOCOL = '''# A/B 流程对照预注册

任务：process-ab40-20260923；模式：只读研究。授权为设计并运行一次有界 A/B 流程实验，到本轮报告和 child 归档即停止。唯一写入范围是本实验目录的输入、编排和核验记录；禁止改译文、术语、规则或旧实验。不套用生产完成谓词。

## 问题与设计
检验按风险定向补漏并分离反证核验，能否在接近资源投入下减少实质漏检及误报。40 条同样本配对，不是两组不同条目的横向比较。两臂共用一次全量独立初审 P，固定其报告同时作为 A1 与 B1；费用、token 和运行时间在每臂各计一次，真实总支出只计一次。这个设计控制共同初审的随机波动，但不测量首次审核模型的稳定性。

A：P + 一次全40条独立常规复审 A2；正式比较的输出为两路 confirmed 候选并集，去重仅按具体 claim，不多数投票。
B：P + 一次预先选定20条的独立定向补漏 B2 + fresh child 对 P/B2 全部候选观察作反证核验 B3。B2 看不到 P；B3 可看到两份已经冻结的报告，但看不到 A2 或参考结论。B3 必须保留全部输入 claim 的接受/降级/撤销映射，不能无记录删除。核验中另发现的问题标 NEW，单独报告其贡献。

两臂发现阶段使用同样规则、证据和当前术语。差异仅为第二阶段工作分配及 B 的显式反证核验。A 原始候选与 B 核验后候选用同一参考审查；另报 B 核验前结果，区分定向补漏与核验的作用。不能把共同最终裁决过滤后的结果拿来宣称两臂都没有误报。

## 样本与分流
从上次冻结的412条候选框排除 pilot40 以及后续 scope 审查接触的条目。保留无先前 spotcheck 的条件，不恢复 ABC 第15组派发。固定种子 2026092302；Orcs 短13/中15/长8，Possessors 短2/中2；长度阈值160/800字符。共40条；不是全仓代表性样本。
B2 在揭示任何结果前固定20条：全部8条长文；非长文按占位符数、动态字符串占位符、格式化机制条件词计算复杂度，取前8条；剩余24条中固定另一种子随机抽4条。词形评分只分配检查精力，不判错；所有条目至少由 P 全量初审。B2 检查全文，不只找评分触发词；长文重点为主体/集合、时间、数量、条件和因果。

## 参考与隔离
宿主在读取任何模型报告前，对40条完成独立初审并冻结；然后逐项裁决三路发现与 B3 结果，并复查全部共同未报错项。宿主参考也可能错，不是人工金标准。报告区分独立初审发现、揭示候选后修订和未决证据。用户既有语言边界定标不改。只能把参考覆盖称为“对本轮宿主裁决集的覆盖”。
子代理禁止读彼此报告；B3 是唯一允许读本臂既有观察的阶段。主代理输出冻结后才收获报告；若终态通知自动暴露结果早于冻结，记录暴露条目，不能伪称严格盲审。所有原报告原样保留。

## 资源与运行
每次实时读取 profiles，使用 Main Reviewer-GPT Sol 做 P，Cross Reviewer - Opus 做 A2/B2/B3；原样复制 profile model/mode/thinking/features。模型在两臂同一职能保持一致，profile 漂移则在派发前记录并停止混合比较；不拿本轮与旧 high 配置实验作模型优劣比较。
预算目标：P 8分钟，A2 8分钟；B2 4分钟+B3 4分钟，即两臂目标16 agent-minutes。此为目标，接口未提供跨提供商统一硬 token 限额，不凭固定分钟阈值中断运行或诊断挂起。实际时间和费用可能超标，必须如实报告。首次计划4个 child（P/A2/B2/B3），只有无效输出或基础设施失败才可每阶段 fresh retry 一次；重试支出另列，不按成绩挑选运行。
相近预算的描述性判据：可比同提供商 B2+B3 的实际费用相对 A2 在0.8–1.25之间，且把 P 加入每臂后 agent运行时间比不超过1.25。若缺费用、计量口径不一致或超界，不宣称等/近成本更优，仅报告质量与资源取舍。token按提供商原值分栏，不合并不同口径；调度等待、模型运行、工具活动及宿主阶段耗时分开；并行运行的端到端时间不可用 agent-minutes 冒充。

## 评价与决策
主指标：confirmed 原子 claim 的参考覆盖、未被支持的 confirmed 数、机制/操作类参考漏检数。同步报告条目级覆盖、pending、共同未报错漏检、B3 保留/撤销真问题数、核验候选数、可观测费用及耗时。上游问题与仅表达建议不混入译文缺陷分母；参考 pending 不记真阳或假阳。原子切分规则为独立意义变化，重复说法合并，不为一个臂额外拆分计分。
若 B 覆盖不低于 A、未支持 confirmed 不多于 A、机制/操作漏检不多于 A，并满足可比资源界限，才称为“值得扩大验证的候选”；否则说明具体交换代价。单次40条不作显著性/总体准确率/模型淘汰结论。最终报告必须列出分歧实例、参考修订、预算是否达标、无效运行和所有 child 归档证明。
'''

def main():
    assert not (ROOT/'FREEZE.json').exists()
    inv=json.loads((BASE/'inventory.json').read_text())
    frame_ids=set(json.loads((PRIOR/'SAMPLING-PREREG.json').read_text())['frame_ids'])
    excluded={e['audit_id'] for e in json.loads((PRIOR/'entries.json').read_text())}
    scoped=json.loads((REPO/'evidence/translation-audit/scope-rule-calibration-20260923/AFFECTED.json').read_text())
    excluded.update(i for e in scoped['records'] for i in e['inventory_audit_ids'])
    frame=[e for e in inv['entries'] if e['audit_id'] in frame_ids-excluded]
    allocation={'orcs/short':13,'orcs/medium':15,'orcs/long':8,'possessors/short':2,'possessors/medium':2}
    rng=random.Random(2026092302); selected=[]
    for key,n in allocation.items():
        selected.extend(rng.sample(sorted([e for e in frame if e['component']+'/'+length(e)==key],key=lambda e:e['audit_id']),n))
    selected.sort(key=lambda e:e['audit_id'])
    keys=['audit_id','source','target','section','source_tag','args_order','special','logical_path','component','line','occurrence','snapshot_sha256']
    entries=[{k:e.get(k) for k in keys} for e in selected]
    dump(ROOT/'entries.json',entries)
    def score(e):
        fmt=len(re.findall(r'%(?!%)[0-9.]*[sdf]',e['source']))
        conditions=len(re.findall(r'\b(?:if|when|each|every|only|until|chance|radius|cooldown)\b',e['source'],re.I))
        return fmt*2 + ('%s' in e['source'])*3 + min(conditions,5)
    longs=[e for e in entries if length(e)=='long']
    ranked=sorted([e for e in entries if length(e)!='long'],key=lambda e:(-score(e),e['audit_id']))
    complex_rows=ranked[:8]; random_rows=random.Random(2026092303).sample(ranked[8:],4)
    targeted=sorted(longs+complex_rows+random_rows,key=lambda e:e['audit_id'])
    assert len(targeted)==20 and len({e['audit_id'] for e in targeted})==20
    dump(ROOT/'targeted-entries.json',targeted)
    dump(ROOT/'SAMPLING.json',{'seed':2026092302,'allocation':allocation,'frame_ids':sorted(frame_ids-excluded),'frame_count':len(frame),'excluded_ids':sorted(excluded),'sample':[{'audit_id':e['audit_id'],'length':length(e),'chars':len(e['source'])} for e in entries],'routing':{'all_long':[e['audit_id'] for e in longs],'complex_nonlong':[{'audit_id':e['audit_id'],'score':score(e)} for e in complex_rows],'random_lowrisk':[e['audit_id'] for e in random_rows],'random_seed':2026092303}})
    registry=json.loads((SERIES/'DLC-SOURCE-REGISTRY.json').read_text())
    parts=[]; metas=[]; files={}
    for lp in sorted({e['logical_path'] for e in entries}):
        locale=subprocess.check_output(['git','show',inv['snapshot_commit']+':'+lp],text=True)
        sections={e['section'] for e in entries if e['logical_path']==lp}
        marks=list(re.finditer(r'^section "([^"]+)"',locale,re.M))
        for i,m in enumerate(marks):
            if m.group(1) in sections:parts.append(locale[m.start():marks[i+1].start() if i+1<len(marks) else len(locale)])
        for section in sorted(sections):
            component=next(e['component'] for e in entries if e['section']==section)
            if component=='possessors':
                metas.append({'component':component,'section':section,'source_pinning':'unavailable','source_path':None});continue
            src=SERIES/'sources'/component/section
            assert sha(src)==registry[component]['files_sha256'][section]
            rel='sources/dlc/'+component+'/'+section; dest=ROOT/rel
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes());files[rel]=sha(dest)
            metas.append({'component':component,'section':section,'source_pinning':'unpinned','source_path':rel})
    (ROOT/'context.lua').write_text('\n'.join(parts))
    dump(ROOT/'source-access.json',{'engine_repository':'/workspace/t-engine4','engine_commit':'624a67329fe2ad440c5b344785a9c73fcf22ae63','sections':metas,'files_sha256':files,'dlc_additional_sources':{'orcs':{'root':str((SERIES/'sources/orcs').resolve()),'files_sha256':registry['orcs']['files_sha256'],'source_pinning':'unpinned'}},'unavailable_components':['possessors'],'rule':'Primary listed files; additional files only via explicit symbol/call from a read file and registry hash. No other locales/reports.'})
    terms=[];text='\n'.join(e['source'].lower() for e in entries)
    for p in sorted((REPO/'terminology').glob('*.tsv')):
        for n,row in enumerate(csv.DictReader(p.open(),delimiter='\t'),2):
            if row['source'].lower() in text:terms.append(dict(row,file=str(p.relative_to(REPO)),line=n))
    dump(ROOT/'terms.json',terms)
    (ROOT/'RULES.md').write_text(RULES)
    (ROOT/'SPEC.md').write_text(PROTOCOL)
    (ROOT/'PLAN.md').write_text('# Plan\nFreeze sample/routing/rules and baseline; dispatch independent P/A2/B2; freeze host full40 pass before harvesting; harvest/archive; freeze B3 candidate packet and dispatch; host source/counterevidence and joint-negative audit; score paired workflows with actual resources; verify immutability and archive all children; report and stop.\n')
    for name,entry_file,n,special in [('P','entries.json',40,'全量独立初审。'),('A2','entries.json',40,'全量独立复审。'),('B2','targeted-entries.json',20,'独立定向补漏：长文重点核对主体/集合、数量、时间、条件和因果；机制说明重点核对作用对象、触发条件及参数消费。不能只查关键词；每条仍需完整阅读。')]:
        (ROOT/f'INPUT-{name}.md').write_text(f'# 独立只读审核 {name}\n{special}\n严格按 {entry_file} 顺序审完恰好 {n} 条。唯一允许输入：本文件、RULES.md、{entry_file}、context.lua、terms.json、source-access.json、FREEZE.json，以及 source-access 允许的源码。不得读取 entries.json 的非分配条目作为审核目标、其他阶段输入/报告、SPEC、SAMPLING、宿主记录或任何旧实验。context.lua 的邻文仅作语境，不额外报未分配条目。遵守 RULES.md 的判定口径和报告格式。最终直接返回完整报告，不写文件。\n')
    dump(ROOT/'SCOPE.json',{'task_id':ROOT.name,'mode':'review_only_research','write_allowed':[str(ROOT.relative_to(REPO))+'/**'],'max_entries':40,'planned_dispatches':['P','A2','B2','B3'],'max_fresh_retry_per_phase':1,'no_production_mutation':True})
    protected={str(p.relative_to(REPO)):sha(p) for p in BASE.rglob('*') if p.is_file() and ROOT not in p.parents and '__pycache__' not in p.parts}
    protected.update({str(p.relative_to(REPO)):sha(p) for p in [REPO/'AGENTS.md',REPO/'TERMINOLOGY.md',REPO/'docs/agent-workflow.md',*REPO.glob('terminology/*.tsv'),*[REPO/p for p in sorted({e['logical_path'] for e in inv['entries']})]]})
    dump(ROOT/'BASELINE.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'hashes':protected,'git_status':subprocess.check_output(['git','status','--short'],text=True)})
    dump(ROOT/'STATE.json',{'task_id':ROOT.name,'state':'FROZEN','mode':'review_only_research','orchestration_transport':'mcp','workspace_id':'wks_ac28b30c4bf45d5b','orchestrator_agent_id':'3a99ff56-6868-4533-b3d5-755e411f9159','candidate_author_agent_id':None,'strict_contract_completion_claimed':False,'child_dispatches':[]})
    frozen=['prepare.py','SPEC.md','PLAN.md','SCOPE.json','RULES.md','INPUT-P.md','INPUT-A2.md','INPUT-B2.md','entries.json','targeted-entries.json','SAMPLING.json','context.lua','terms.json','source-access.json']+list(files)
    dump(ROOT/'FREEZE.json',{'count':40,'snapshot_commit':inv['snapshot_commit'],'files_sha256':{p:sha(ROOT/p) for p in frozen}})
    for d in ['dispatches','raw','reports']:(ROOT/d).mkdir(exist_ok=True)
    print('Frozen40, source chars',sum(len(e['source']) for e in entries),'targeted20 chars',sum(len(e['source']) for e in targeted),'of eligible',len(frame))
    print('IDs',[e['audit_id'] for e in entries])

if __name__=='__main__': main()
