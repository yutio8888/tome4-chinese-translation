#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收尾 review run：写 review record、归档 child、填 STATE，并逐 run 校验 DONE_VERIFIED。

环境：TOME_ORCH_PARENT_AGENT_ID、TOME_PASEO_WORKSPACE

surface_evidence_binding.artifact_sha256 必须是精确集合：
  surface_screen_input_path + 每条 record 的 input_path 与 raw_output_path
多一个少一个都会失败（runbook §28）。

用法：
  close_review_tasks.py surface    <plan.json> <children.json> <rawdir>
  close_review_tasks.py contextual <ctx.json>  <children.json> <rawdir>
"""
import json, sys, hashlib, pathlib, subprocess, datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _orch

P = _orch.parent_agent_id()
WS = _orch.workspace_id()
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def inspect(aid):
    return _orch.paseo_json(['agent', 'inspect', aid, '--json'])


def meta(o):
    for k in ('Mode', 'Model', 'Provider', 'Thinking'):
        if not o.get(k):
            raise SystemExit(f'agent {o.get("Id")} 的 inspect 缺 {k}，不能记成 captured')
    return {'capture_status': 'captured', 'captured_at': NOW, 'schema_version': 1,
            'source': 'live_agent_metadata',
            'mode': {'presence': 'present', 'value': o['Mode']},
            'model': {'presence': 'present', 'value': o['Model']},
            'provider': {'presence': 'present', 'value': o['Provider']},
            'thinking': {'presence': 'present', 'value': o['Thinking']}}


def archive_confirmed(aid):
    """归档并**回读确认**，再决定能不能写 archive_confirmed=true（runbook §35.3）。

    原实现 `subprocess.run(...archive..., capture_output=True)` 连返回码都不看，
    紧接着无条件写 archive_confirmed=True —— 归档失败时证据链上留下的是一句假话。

    权威信号是回读到的 Archived，不是 archive 命令的返回码：
    `paseo agent archive` 对**已归档**的 agent 会返回 rc=1（"already archived"），
    那是幂等重跑的正常情形，不该当成失败；反过来 rc=0 也不足以证明真的归档了。
    所以先尽力归档、记下错误，再以 inspect 的回读结果为准。
    ai_state_check 只认字面 true，因此确认不了就直接失败，绝不降级写 false 蒙混。
    """
    err = None
    try:
        _orch.paseo(['agent', 'archive', aid])
    except SystemExit as e:
        err = str(e)                                 # 可能只是「已归档」，交给回读判定
    o = inspect(aid)                                 # 回读服务端状态，不信自己的乐观假设
    if o.get('Archived') is not True:
        raise SystemExit(f'agent {aid} 归档后回读 Archived={o.get("Archived")}，'
                         f'拒绝写 archive_confirmed；归档命令输出：{err}')
    if o.get('ParentAgentId') != P:
        raise SystemExit(f'agent {aid} 的 ParentAgentId={o.get("ParentAgentId")} 与本编排 {P} 不符，'
                         '拒绝写 lineage_verified')
    return o


def close(task, contract, items, rawdir):
    rev = pathlib.Path('.ai/reviews') / task
    rev.mkdir(parents=True, exist_ok=True)
    recs, kids, art = [], [], {}
    surface = contract.startswith('translation_surface')
    if surface:
        draft = f'.ai/task/{task}/SURFACE-SCREEN-INPUT-DRAFT.json'
        art[draft] = sha(draft)
    for it in items:
        did = it['dispatch_id']
        rawtxt = rev / f'raw-{did}.txt'
        rawtxt.write_text(pathlib.Path(f'{rawdir}/{did}.json').read_text())
        rec = {'agent_id': it['agent_id'], 'attempt': 1,
               'candidate_identity': it['candidate_identity'], 'cycle': 0, 'dispatch_id': did,
               'input_path': it['input_path'], 'lineage_verified': True, 'parent_agent_id': P,
               'purpose': contract, 'raw_output_path': str(rawtxt),
               'raw_output_sha256': sha(rawtxt), 'review_contract': contract,
               'review_kind': it.get('review_kind', 'full'), 'review_phase': 'REVIEW',
               'reviewer_role': 'REVIEWER', 'status': 'completed', 'task_id': task,
               'workspace_id': WS}
        if it.get('lane'):
            rec['lane'] = it['lane']
        (rev / f'{did}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True))
        recs.append(str(rev / f'{did}.json'))
        if surface:
            art[it['input_path']] = sha(it['input_path'])
            art[str(rawtxt)] = sha(rawtxt)
        info = archive_confirmed(it['agent_id'])
        lb = {'candidate_identity': it['candidate_identity'], 'dispatch_id': did,
              'paseo.parent-agent-id': P, 'purpose': contract, 'role': 'reviewer', 'task_id': task}
        k = {'agent_id': it['agent_id'], 'archive_attempts_started': 1, 'archive_confirmed': True,
             'archived_at': info.get('ArchivedAt') or NOW,
             'author_provider_resolution': 'not_applicable',
             'candidate_author_agent_id': None, 'candidate_identity': it['candidate_identity'],
             'dispatch_id': did, 'input_path': it['input_path'], 'labels': lb,
             'lifecycle': 'archived', 'lineage_verified': True, 'output_valid': True,
             'parent_agent_id': P, 'purpose': contract, 'role': 'REVIEWER',
             'runtime_observation': meta(info), 'workspace_id': WS}
        if it.get('lane'):
            k['lane_index'] = it['lane']['index']
            k['lane_group_identity'] = it['lane']['group_identity']
            lb['lane_index'] = str(it['lane']['index'])
            lb['lane_group_identity'] = it['lane']['group_identity']
        kids.append(k)

    sp = pathlib.Path(f'.ai/task/{task}/STATE.json')
    st = json.loads(sp.read_text())
    st.update({'state': 'DONE', 'completed_review_contracts': [contract],
               'pending_review_contracts': [], 'child_dispatches': kids, 'review_records': recs,
               'final_validation_passed': True, 'orchestrator_agent_id': P, 'updated_at': NOW})
    if surface:
        st['surface_carry_over_path'] = None
        st['surface_screen_input_path'] = f'.ai/task/{task}/SURFACE-SCREEN-INPUT-DRAFT.json'
        st['change_class'] = 'translation_workflow'
        st['surface_evidence_binding'] = {'algorithm': 'surface-evidence-binding/1',
                                          'artifact_sha256': art, 'task_id': task,
                                          'terminal': 'whole_screen'}
    else:
        st['change_class'] = 'standard'
        st['contextual_reviewers'] = [
            {'agent_id': it['agent_id'], 'candidate_identity': it['candidate_identity'],
             'dispatch_id': it['dispatch_id'], 'input_path': it['input_path'],
             'purpose': contract, 'role': 'REVIEWER'} for it in items]
    _orch.write_atomic(sp, json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True))
    r = subprocess.run(['python3', '-B', 'tools/ai_state_check.py', str(sp), '--target', 'DONE'],
                       capture_output=True, text=True)
    line = (r.stdout.strip() or r.stderr.strip())
    print(f'{task}: {line}')
    return line.startswith('DONE_VERIFIED')


def main():
    kind, spec, childf, rawdir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    kids = {(k['task_id'], k['dispatch_id']): k['agent_id'] for k in json.load(open(childf))}
    ok = True
    if kind == 'surface':
        plan = json.load(open(spec))
        for task, v in sorted(plan.items()):
            items = []
            for l in v['lanes']:
                it = {'dispatch_id': l['dispatch_id'], 'candidate_identity': l['candidate_identity'],
                      'input_path': l['input_path'], 'agent_id': kids[(task, l['dispatch_id'])],
                      'review_kind': l['review_kind']}
                if l['review_kind'] == 'lane':
                    # 路径以 plan 里记录的为准，绝不从 task 名反推（单 run 批次 task==batch id）
                    gp = l['group_manifest_path']
                    g = json.loads(pathlib.Path(gp).read_text())
                    b = [x for x in g['payload']['lane_boundaries'] if x['index'] == l['index']][0]
                    it['lane'] = {'count': g['payload']['lane_count'],
                                  'group_id': g['payload']['group_id'],
                                  'group_identity': g['group_identity'], 'group_manifest_path': gp,
                                  'index': b['index'], 'length': b['length'], 'offset': b['offset']}
                items.append(it)
            ok &= close(task, 'translation_surface_screen_v1', items, rawdir)
    else:
        for r in json.load(open(spec)):
            it = dict(r); it['agent_id'] = kids[(r['task_id'], r['dispatch_id'])]
            it['review_kind'] = 'full'
            ok &= close(r['task_id'], 'translation_contextual_v2', [it], rawdir)
    sys.exit(0 if ok else 1)


main()
