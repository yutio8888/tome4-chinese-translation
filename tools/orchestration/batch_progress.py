#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐批的「净进展」报表：把批次规模换算成真正新增的覆盖与返工。

用法：
  python3 -B tools/orchestration/batch_progress.py            # 最近 10 批
  python3 -B tools/orchestration/batch_progress.py --all
  python3 -B tools/orchestration/batch_progress.py --json

「审了 80 条」不等于「前进了 80 条」：同一逻辑条目可能因为改译产生新 revision
而被再次审到。这里按 logical_entry_identity 算首次覆盖，把重复审到的单列出来。

只读受跟踪证据（evidence/production-review-v2-lite/batches/*），不碰队列，
因此可以在批次进行期间安全运行。

派发耗时、各阶段墙钟、白跑的派发次数不在受跟踪证据里——那要由编排脚本另行记录，
本工具不猜（宁可不报，也不给一个看着像测量结果的估计值）。
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BATCHES = ROOT / 'evidence/production-review-v2-lite/batches'
MIGRATIONS = ROOT / 'evidence/production-review-v2-lite/migrations'


def rework_sources():
    """改译会让条目产生新 revision 并重新入队——这是未来返工的来源。

    每次迁移的 rows 就是被改动的条目。首次全量发布（一次性改掉全部条目）
    不是返工，单独剔除，否则会把基线当成返工淹没真实信号。
    """
    rows = []
    for f in sorted(MIGRATIONS.glob('*.json')):
        d = json.loads(f.read_text())
        n = sum(1 for r in d['rows'] if r['disposition'] == 'revision_changed')
        if n:
            rows.append((n, f.name[:12], d.get('recorded_by', '')))
    baseline = [r for r in rows if r[0] > 20000]
    repairs = [r for r in rows if r[0] <= 20000]
    return baseline, sorted(repairs, reverse=True)


def load(bdir):
    man = json.loads((bdir / 'manifest.json').read_text())
    rows = [json.loads(l) for l in (bdir / 'results.jsonl').read_text().splitlines() if l.strip()]
    adj = [json.loads(l) for l in (bdir / 'adjudications.jsonl').read_text().splitlines() if l.strip()]
    return man, rows, adj


def main():
    dirs = sorted(d for d in BATCHES.iterdir() if (d / 'manifest.json').is_file())
    batches = []
    for d in dirs:
        man, rows, adj = load(d)
        batches.append((man['recorded_at'], d.name, man, rows, adj))
    batches.sort()

    seen = set()
    report = []
    for recorded_at, name, man, rows, adj in batches:
        logical = [r['logical_entry_identity'] for r in rows]
        fresh = [x for x in logical if x not in seen]
        again = len(logical) - len(fresh)
        seen.update(logical)
        deep = sum(1 for r in rows if r.get('completion_level') != 'surface_only')
        disp = {}
        for a in adj:
            disp[a['disposition']] = disp.get(a['disposition'], 0) + 1
        report.append({
            'batch': name,
            'recorded_at': recorded_at,
            'entries': len(rows),
            'distinct_logical': len(set(logical)),
            'newly_covered': len(set(fresh)),
            're_reviewed': again,
            'deep_reviewed': deep,
            'surface_only': len(rows) - deep,
            'surface_issue': sum(1 for r in rows if r.get('surface_verdict') not in (None, 'OK')),
            'deep_issue': sum(1 for r in rows if r.get('deep_verdict') not in (None, 'OK')),
            'adjudications': len(adj),
            'dispositions': disp,
            'repair_required': sum(1 for a in adj if a.get('repair_required')),
            'not_done': sum(1 for r in rows if r.get('final_state') != 'done'),
        })

    if '--json' in sys.argv:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return

    shown = report if '--all' in sys.argv else report[-10:]
    print(f'{"批次":26} {"条数":>4} {"净新增":>6} {"重复":>4} {"深审":>4} '
          f'{"表层ISSUE":>8} {"深层ISSUE":>8} {"confirmed":>9} {"待修":>4}')
    for r in shown:
        c = r['dispositions'].get('confirmed', 0)
        print(f'{r["batch"]:26} {r["entries"]:4d} {r["newly_covered"]:6d} {r["re_reviewed"]:4d} '
              f'{r["deep_reviewed"]:4d} {r["surface_issue"]:8d} {r["deep_issue"]:8d} '
              f'{c:9d} {r["repair_required"]:4d}')
    tot_e = sum(r['entries'] for r in report)
    tot_n = sum(r['newly_covered'] for r in report)
    tot_r = sum(r['re_reviewed'] for r in report)
    print(f'\n全部 {len(report)} 批：审 {tot_e} 条 revision，净新增覆盖 {len(seen)} 个逻辑条目，'
          f'重复审到 {tot_r} 条（{100*tot_r/tot_e:.1f}%）')
    print(f'累计 confirmed {sum(r["dispositions"].get("confirmed",0) for r in report)}、'
          f'pending {sum(r["dispositions"].get("pending",0) for r in report)}、'
          f'advisory {sum(r["dispositions"].get("advisory",0) for r in report)}、'
          f'refuted {sum(r["dispositions"].get("refuted",0) for r in report)}；'
          f'待修 {sum(r["repair_required"] for r in report)}')
    deep = sum(r['deep_reviewed'] for r in report)
    print(f'深审覆盖 {deep}/{tot_e}（{100*deep/tot_e:.1f}%）——'
          f'其余只过表层一轮，漏报率无法由此估计')

    baseline, repairs = rework_sources()
    changed = sum(n for n, _, _ in repairs)
    print(f'\n=== 返工来源：改译产生新 revision，重新入队 ===')
    print(f'{len(repairs)} 次修复/清扫共改动 {changed} 条'
          f'（另有首次全量发布 {sum(n for n,_,_ in baseline)} 条，不计为返工）')
    for n, mid, by in repairs[:5]:
        print(f'   {mid} 改 {n:4d} 条 ≈ {n/80:.1f} 个批次的返工   {by[:38]}')
    print(f'其中已被重审 {tot_r} 条，尚有约 {changed - tot_r} 条待重审——'
          f'全库清扫的代价要按「它会占掉多少个后续批次」来算')


main()
