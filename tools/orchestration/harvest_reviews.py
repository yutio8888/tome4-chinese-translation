#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收割 reviewer 输出：取 paseo logs 里最后一个合法 JSON，落盘并**当场校验**。

用法：python3 -B tools/orchestration/harvest_reviews.py <children.json> <outdir> [--key results|verdicts]

原实现只检查 `candidate_identity` 非空，等于没查（runbook §35.2）：
identity 写错、少答几条、多答几条、顺序错位，全都能过。
现在逐条对着**冻结输入信封**校验三件事，任一不符即整批失败：
  1. candidate_identity 必须与信封**相等**（不是「非空」）；
  2. 逐条 revision 必须与信封的冻结顺序**完全一致**（顺序即覆盖，多答少答错序一起管）；
  3. 每条必须有 verdict。
surface 输出用 entry_revision_identity，contextual 用 revision_key，两种都认。
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _orch

REV_KEYS = ('entry_revision_identity', 'revision_key')


def row_revision(r):
    for k in REV_KEYS:
        if r.get(k):
            return r[k]
    return None


def check(k, o, key):
    """返回问题描述列表；空列表表示这条 lane 干净。"""
    env = json.load(open(k['input_path']))
    problems = []

    want_id = env['candidate_identity']
    got_id = o.get('candidate_identity')
    if got_id != want_id:
        problems.append(f'identity 不符：期望 {want_id[:12]}… 实得 {str(got_id)[:12]}…')

    want = _orch.expected_coverage(env)
    rows = o.get(key)
    if not isinstance(rows, list):
        problems.append(f'缺少 {key} 数组')
        return problems
    got = [row_revision(r) for r in rows]
    if got != want:
        ws, gs = set(want), set(x for x in got if x)
        missing, extra = ws - gs, gs - ws
        if missing:
            problems.append(f'漏答 {len(missing)} 条，例如 {sorted(missing)[0][:12]}…')
        if extra:
            problems.append(f'多答 {len(extra)} 条，例如 {sorted(extra)[0][:12]}…')
        if None in got:
            problems.append(f'{got.count(None)} 条没有 revision 标识')
        if not missing and not extra and None not in got:
            problems.append(f'覆盖齐全但顺序与冻结顺序不一致（共 {len(want)} 条）')
    if any(r.get('verdict') is None for r in rows):
        problems.append('存在没有 verdict 的条目')
    return problems


def main():
    kids = json.load(open(sys.argv[1]))
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    key = sys.argv[sys.argv.index('--key') + 1] if '--key' in sys.argv else 'results'
    idx, bad = {}, []

    for k in kids:
        did = k['dispatch_id']
        if k.get('status') not in (None, 'dispatched'):
            bad.append((did, f'派发未完成（status={k.get("status")}）'))
            continue
        if not k.get('input_path'):
            bad.append((did, 'children.json 缺 input_path，无法校验覆盖；请用新版 dispatch 重新派发'))
            continue

        log = _orch.paseo(['agent', 'logs', k['agent_id']])
        cands = [l.strip() for l in log.split('\n')
                 if l.strip().startswith('{') and l.strip().endswith('}')]
        if not cands:
            bad.append((did, '无 JSON 输出'))
            continue
        raw = cands[-1]
        try:
            o = json.loads(raw)
        except Exception as e:
            bad.append((did, f'非法 JSON: {e}'))
            continue

        problems = check(k, o, key)
        if problems:
            bad.append((did, '；'.join(problems)))
            continue

        p = out / f'{did}.json'
        _orch.write_atomic(p, raw)
        rows = o[key]
        iss = [x for x in rows if x.get('verdict') not in (None, 'OK')]
        print(f'{did:14} entries={len(rows):3} ISSUE={len(iss)} 覆盖/身份 已核')
        idx[did] = str(p)

    if bad:
        print('失败：')
        for d, m in bad:
            print('  ', d, m)
        sys.exit(1)
    _orch.write_json_atomic(out / 'index.json', idx)
    print(f'收割 {len(idx)} 个 lane，全部通过身份与覆盖校验')


main()
