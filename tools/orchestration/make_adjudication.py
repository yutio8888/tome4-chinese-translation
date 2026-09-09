#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由「裁决说明」生成 adjudicate --input 所需的规范 JSON。

用法：python3 -B tools/orchestration/make_adjudication.py <spec.json> <out.json>

spec.json: {"workset": "...", "decisions": {"<rev前10位>|<surface|contextual>":
            {"disposition": "...", "repair_required": bool, "conclusion": "..."}}}

自动处理三件容易出错的事（runbook §40.2）：
  - 键集合必须是精确的十个，多带 schema_version 会报 exact schema mismatch；
  - 决策数量必须与 _accepted_observations 完全相等（只有 ISSUE 才算观察）；
  - disposition=confirmed 必须附公开源码的自证快照（{content, sha256}），
    因为游戏源码不在本仓库 git 里，无法用 path+commit 形式。
"""
import hashlib, json, pathlib, sys
sys.path.insert(0, 'tools')
from i18nlib import production_review_v2_lite_batch as B
from i18nlib import production_review as wp1

CONTRACT = {'surface': 'translation_surface_screen_v1', 'contextual': 'translation_contextual_v2'}
ENGINE = pathlib.Path('/workspace/t-engine4')

spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
cp = B.preflight(pathlib.Path('.'))
obs = B._accepted_observations(cp)
paths = {v['entry_revision_identity']: v['public_source_path']
         for v in json.loads(pathlib.Path(spec['workset']).read_text())['source_verification']}

want = {}
for key, val in spec['decisions'].items():
    rev, kind = key.split('|')
    want[(rev, CONTRACT[kind])] = val

cache, out, missing = {}, [], []
for o in obs:
    k = (o['entry_revision_identity'][:10], o['contract'])
    if k not in want:
        missing.append(k); continue
    v = want.pop(k)
    snap = None
    if v['disposition'] == 'confirmed':
        rel = paths[o['entry_revision_identity']]
        if rel not in cache:
            raw = (ENGINE / rel).read_bytes()
            cache[rel] = {'content': raw.decode('utf-8'), 'sha256': hashlib.sha256(raw).hexdigest()}
        snap = cache[rel]
    out.append({'conclusion': v['conclusion'], 'disposition': v['disposition'],
                'entry_revision_identity': o['entry_revision_identity'],
                'evidence_commit': None, 'evidence_path': None, 'evidence_snapshot': snap,
                'observation_contract': o['contract'],
                'observation_identity': o['observation_identity'],
                'observation_sha256': hashlib.sha256((o['observation'] or '').encode()).hexdigest(),
                'repair_required': bool(v['repair_required'])})
if missing:
    raise SystemExit(f'spec 缺这些观察的裁决：{missing}')
if want:
    raise SystemExit(f'spec 里有多余、对不上任何观察的裁决：{sorted(want)}')
pathlib.Path(sys.argv[2]).write_bytes(wp1.canonical_bytes({'batch_id': cp['batch_id'], 'decisions': out}))
from collections import Counter
print(f'{len(out)} 条裁决', dict(Counter(d["disposition"] for d in out)),
      '| repair', sum(1 for d in out if d['repair_required']))
