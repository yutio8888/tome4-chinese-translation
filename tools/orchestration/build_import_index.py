#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 candidate_identity（不是 run/lane 编号）建 surface/contextual import index。

用法：python3 -B tools/orchestration/build_import_index.py <surface|contextual> <rawdir> <out.json>
"""
import json, sys, glob, pathlib

CKPT = '.artifacts/i18n/production-review-v2-lite/active-batch.json'


def main():
    kind, rawdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    cp = json.loads(pathlib.Path(CKPT).read_text())
    raw = {}
    for f in glob.glob(f'{rawdir}/*.json'):
        if f.endswith('index.json'):
            continue
        raw[json.loads(pathlib.Path(f).read_text())['candidate_identity']] = f
    idx = {}
    for i, r in enumerate(cp[kind]):
        ci = r['candidate_identity']
        assert ci in raw, (f'ref {i} 的 candidate_identity 无对应 raw', ci[:12])
        idx[str(i)] = raw[ci]
    assert len(idx) == len(cp[kind]), (len(idx), len(cp[kind]))
    json.dump(idx, open(out, 'w'), indent=1)
    for k, v in idx.items():
        print(' ', k, v.split('/')[-1])
    print(f'{kind} index {len(idx)} 项')


main()
