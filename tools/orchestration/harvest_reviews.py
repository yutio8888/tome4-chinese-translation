#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收割 reviewer 输出：取 paseo logs 里最后一个合法 JSON，落盘并校验覆盖。

用法：python3 -B tools/orchestration/harvest_reviews.py <children.json> <outdir> [--key results|verdicts]
"""
import json, sys, subprocess, pathlib


def main():
    kids = json.load(open(sys.argv[1]))
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    key = sys.argv[sys.argv.index('--key') + 1] if '--key' in sys.argv else 'results'
    idx, bad = {}, []
    for k in kids:
        log = subprocess.run(['paseo', 'agent', 'logs', k['agent_id']],
                             capture_output=True, text=True).stdout
        cands = [l.strip() for l in log.split('\n')
                 if l.strip().startswith('{') and l.strip().endswith('}')]
        if not cands:
            bad.append((k['dispatch_id'], '无 JSON 输出')); continue
        raw = cands[-1]
        try:
            o = json.loads(raw)
        except Exception as e:
            bad.append((k['dispatch_id'], f'非法 JSON: {e}')); continue
        if not o.get('candidate_identity'):
            bad.append((k['dispatch_id'], 'identity 未回显')); continue
        p = out / f"{k['dispatch_id']}.json"; p.write_text(raw)
        rows = o.get(key) or []
        iss = [x for x in rows if x.get('verdict') not in (None, 'OK')]
        print(f"{k['dispatch_id']:14} entries={len(rows):3} ISSUE={len(iss)}")
        idx[k['dispatch_id']] = str(p)
    if bad:
        print('失败：'); [print('  ', d, m) for d, m in bad]; sys.exit(1)
    json.dump(idx, open(sys.argv[2].rstrip('/') + '/index.json', 'w'), indent=1)


main()
