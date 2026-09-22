import json,re
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
E=Path('evidence/quality/repair-window-7-20260922')
proof=json.loads((P/'PUBLICATION-CLOSURE.json').read_text())
replay=json.loads((E/'closure/replay-verification.json').read_text())
assert proof['verified'] and replay['verified'] and replay['children']==23
head=proof['head'];counts=proof['counts']
status=f"{counts['done']} done / {counts['repair_required']} repair_required / {counts['blocked']} blocked / {proof['queued']} queued"
h=Path('handoff.md');t=h.read_text()
t=t.replace('修复窗口7证据已发布；按用户要求暂停，宿主待完成最终收尾','修复窗口7已闭合并推送；按用户要求暂停')
t=t.replace('修复窗口7闭合后进入','修复窗口7已闭合，当前进入')
t=t.replace('实施/复审child共22个已确认归档；本publication child仍待宿主\n收获归档，不提前宣称。','实施/复审22个child及publication child共23个均已确认归档；最终状态检查通过。\n')
t=t.replace('当前候选catalog为','当前catalog为')
start=t.index('### 宿主待完成的最终收尾');end=t.index('\n旧Archmage',start)
closure=f'''### 已完成的收尾与暂停边界

证据/catalog/migration提交为`{head}`，提交后的第二次queue rebuild、push与远端核验
均已于`{proof['verified_at']}`完成；本地HEAD、origin/develop与SQLite evidence head一致。
队列实测 **{status}**；本轮8个新revision逐条确认queued，须重新审核。
详见[收尾核验](evidence/quality/repair-window-7-20260922/closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-CLOSURE.json)。

原452项immutable快照保持原字节；收尾增量共{replay['delta_files']}项，包含publication生命周期、
提交/队列/push证明，与基础快照合并后独立重放为`DONE_VERIFIED`。
见[增量重放结果](evidence/quality/repair-window-7-20260922/closure/replay-verification.json)。
本交接和收尾证明随最终文档提交保存，提交后仅同步queue并push，不再产生译文或新批次。
**当前STOP；审核254未启动，只有新的用户授权才能继续。**
'''
t=t[:start]+closure+t[end:]
t=t.replace('当前catalog为`6f08','窗口6闭合时catalog为`6f08').replace('当前 catalog 为 `c267','窗口5闭合时 catalog 为 `c267')
t=t.replace('用户持续授权连续审核和每批 push。审核 250、251 均已完成；','窗口5执行时用户授权连续审核和每批 push；现以顶部暂停指令为准。审核 250、251 均已完成；')
h.write_text(t)
f=E/'PUBLICATION.md';t=f.read_text()
t=t.replace('本出版阶段没有修改 Lua','publication EXECUTOR 没有修改 Lua')
t=t.replace('本\npublication child 尚待宿主收获并确认归档，本文不提前宣称。','publication child 也已由宿主收获并确认归档，合计23个。\n最终生命周期与状态见[收尾增量](closure/snapshot-delta.json)。')
t=t.replace('## 暂停状态与宿主待办','## 已完成的宿主收尾与暂停状态')
start=t.index('本文件生成时，窗口 7');end=t.index('\n旧 Archmage',start)
t=t[:start]+f'''证据/catalog/migration提交`{head}`，提交后的第二次queue rebuild、push、
本地/远端/SQLite三方核验均已于`{proof['verified_at']}`完成。
队列为 **{status}**，8个successor逐条验证queued。
23个child全部确认归档，最终STATE为`DONE_VERIFIED`。

原452项包保持不变；{replay['delta_files']}项收尾增量与基础包合并独立重放通过。
见[实测收尾证明](closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-CLOSURE.json)、
[增量清单](closure/snapshot-delta.json)及[重放结果](closure/replay-verification.json)。
提交检查发现12处冻结历史空白，均以来源和Git索引SHA绑定记录例外，原字节未修改。
首次收尾脚本遗漏补丁中的space-before-tab诊断，经一次有界诊断完成独立核验；
详见[提交核验](closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-STAGING-VERIFICATION.json)。
最终handoff与本收尾证明随文档提交保存；此后仅同步queue/push，当前STOP，未启动254。
''' +t[end:]
f.write_text(t)
for doc in [h,f]:
 text=doc.read_text();assert all(l==l.rstrip() for l in text.splitlines())
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
  if '://' not in target and not target.startswith('#'):assert (doc.parent/target).exists(),(doc,target)
print('Handoff and publication closure updated; UTF-8, links and whitespace verified')
