import pathlib
p=pathlib.Path('handoff.md');s=p.read_text(encoding='utf-8')
o3='更新时间：2026-09-24（审核274已完成；修复改为攒批，积压7条，达20条后开合并修复窗口27）'
n3='更新时间：2026-09-24（审核275已完成；修复攒批中，积压13条，达20条后开合并修复窗口27）'
M='当前修复积压共 7 条（273 两条 + 274 五条）；下一步继续审核275（默认80条），积压达 20 条后开合并修复窗口27。\n'
assert s.count(o3)==1 and s.count(M)==1
ev=open('/tmp/evid275').read().strip()[:8]
new=('审核275（`batch-54d2d16b94c511082107`）已闭合，结果为 **74 done / 6 repair_required / 0 blocked**。\n'
'surface 四组 `codex/gpt-6-sol` 为 69 OK / 11 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 复核这 11 条，为 7 OK / 4 ISSUE。\n'
f'15 个观察裁决为 10 confirmed、5 refuted，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `{ev}`，\n'
'详见[275宿主证据](evidence/quality/production-batches/batch-54d2d16b94c511082107-host-evidence/summary.md)。本批在 adjudication chain 之后按用户要求暂停过一次（系统重启），恢复后从 commit_ready 继续收口。\n\n'
'275 的 6 条修复计入积压（`.ai/task/batch-54d2d16b94c511082107/REPAIR-BACKLOG-DECISION.json`）：燃烧之手补“（及武器）”并把体力回复改为“每次命中”；恶魔空间补“每回合”、持续光环与“法术结束时”；'
'黑暗者古尔莫特墓志铭拆回三行（LF 6→5 实测）；回复纹身加载提示整句修复（预判伤害、提前准备，物品名统一“回复纹身”）；任务名 From bellow, it devours 对齐“来自深渊，吞噬四方”；wispy purple cloak“脆弱的”改“缥缈的”。\n\n'
'当前修复积压共 13 条（273 两条 + 274 五条 + 275 六条）；下一步继续审核276（默认80条），积压达 20 条后开合并修复窗口27。\n')
p.write_text(s.replace(o3,n3).replace(M,new),encoding='utf-8')
print('handoff ok')
