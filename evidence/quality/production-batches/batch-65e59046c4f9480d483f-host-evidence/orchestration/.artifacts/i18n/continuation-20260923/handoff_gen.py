"""handoff_gen.py <N>: update handoff.md after finalize (reads /tmp/stats<N>.json, /tmp/fin<N>.json, /tmp/evid<N>)."""
import json
import sys
from pathlib import Path

N = sys.argv[1]
T = sys.argv[2] if len(sys.argv) > 2 else N
C = Path('.artifacts/i18n/continuation-20260923')
st = json.loads(Path(f'/tmp/stats{N}.json').read_text())
fin = json.loads(Path(f'/tmp/fin{N}.json').read_text())
E = Path(f'/tmp/evid{N}').read_text().strip()
import os
p = Path(os.environ.get('HANDOFF', 'handoff.md'))
s = p.read_text()
P = str(int(N) - 1)
W = st['window']
B = st['batch']


def timing(name):
    f = C / f'review{T}-{name}-timing.json'
    return f'{json.loads(f.read_text())["wall_seconds"]:.1f} s' if f.exists() else '未计时'


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)


line = s.index('更新时间：')
s = s[:line] + (f'更新时间：{fin["date"]}（第{N}批已 finalize，窗口{W}积压 {st["backlog_after"]} 条，继续审核第{int(N) + 1}批）'
                ) + s[s.index('\n', line):]

start = s.index(f'- 审核已闭合至第 **{P}** 批')
end = s.index('- 修复窗口已闭合至 **')
s = s[:start] + (
    f'- 审核已闭合至第 **{N}** 批（`{B}`）：{st["total"]} 条（全部 Cults），{st["done"]} done / {st["repair"]} repair_required。\n'
    f'  {fin["handoff_scope_zh"]}\n'
    f'  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `{E}` 已 finalize。当前无 active batch。\n'
) + s[end:]

k = s.index(f'窗口 {W} 积压 ', s.index('- 修复窗口已闭合至 **'))
e = s.index('\n', k) + 1
s = s[:k] + f'窗口 {W} 积压 {st["backlog_after"]} 条（{fin["backlog_span_zh"]}）。\n' + s[e:]

row_start = s.index(f'| {P} | `')
row_end = s.index('\n', row_start) + 1
sv, cv, dv = st['surface'], st['contextual'], st['dispositions']
s = s[:row_end] + (
    f'| {N} | `{B}` | {st["done"]} done / {st["repair"]} repair | {sv.get("OK", 0)} OK / {sv.get("ISSUE", 0)} ISSUE | '
    f'{cv.get("OK", 0)} OK / {cv.get("ISSUE", 0)} ISSUE | '
    + ' / '.join(f'{dv[k]} {k}' for k in ('confirmed', 'refuted', 'advisory', 'pending') if dv.get(k)) + ' |\n') + s[row_end:]

sub(f'1. 继续审核第 **{N}** 批', f'1. 继续审核第 **{int(N) + 1}** 批')
s = s.replace(f'脚本从 `*{P}.py` 派生', '用 `.artifacts/i18n/continuation-20260923/bd.sh` 驱动（`N=<批号>; source bd.sh` 须分两句；第297批加 `S=295`，因第296批脚本无批号）', 1)
k = s.index(f'窗口 {W} 积压 **')
e = s.index('条', k)
s = s[:k] + f'窗口 {W} 积压 **{st["backlog_after"]}** ' + s[e:]
k2 = s.index('（第', k)
e2 = s.index('）：', k2)
s = s[:k2] + f'（{fin["backlog_span_zh"]}，Cults' + s[e2:]
k3 = s.index('；依据见', k)
e3 = s.index('HOST-FINAL-DECISIONS.json`。', k3) + len('HOST-FINAL-DECISIONS.json`。')
s = s[:k3] + f'；第{N}批 ' + fin['backlog_items_zh'] + '；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。' + s[e3:]

k = s.index(f'   第{P}批计时（实测')
e = s.index('\n', k) + 1
s = s[:k] + (f'   第{N}批计时（实测，投影缓存 on）：start {timing("start")}；adjudication chain（含 17 项门禁）'
             f'{timing("adjudication-chain")}；finalize {timing("finalize")}。\n') + s[e:]
p.write_text(s)
print('HANDOFF_UPDATED')
