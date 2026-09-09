#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""编排脚本共用件：环境配置、带返回码检查的 paseo 调用、原子写。

三条规矩，都是被真实事故换来的（runbook §35）：
  1. 身份（parent agent、workspace）一律运行时发现，不写死在脚本里；
  2. 外部命令必须查返回码，绝不让调用方拿着空串继续往下走；
  3. 落盘一律「同目录临时文件 + rename」，中途崩溃不留半个文件。
"""
import json, os, pathlib, subprocess, tempfile

ROOT = pathlib.Path(os.environ.get('TOME_TRANSLATION_ROOT',
                                   pathlib.Path(__file__).resolve().parents[2]))


def env(name, hint):
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f'缺少环境变量 {name}（{hint}）')
    return v


def parent_agent_id():
    """当前 ORCHESTRATOR 自己。抄用别的 agent 的 id 会写错 lineage，DONE 校验必败。"""
    return env('PASEO_AGENT_ID', '由 Paseo 自动注入；不在 Paseo 里跑就得手工导出')


_WS_CACHE = {}


def workspace_id():
    """按 cwd 运行时发现，不硬编码（README「身份与路径」一节）。

    CLI 返回裸数组，MCP 返回 {"workspaces":[...]}，两种都兼容。
    允许 TOME_PASEO_WORKSPACE 覆盖，供非标准环境使用。
    """
    override = os.environ.get('TOME_PASEO_WORKSPACE')
    if override:
        return override
    cwd = str(ROOT)
    if cwd not in _WS_CACHE:
        d = paseo_json(['workspace', 'ls', '--json'])
        ws = d.get('workspaces', []) if isinstance(d, dict) else d
        hit = [w['workspaceId'] for w in ws if w.get('cwd') == cwd]
        if len(hit) != 1:
            raise SystemExit(f'按 cwd={cwd} 匹配到 {len(hit)} 个 workspace，无法确定；'
                             '必要时用 TOME_PASEO_WORKSPACE 指定')
        _WS_CACHE[cwd] = hit[0]
    return _WS_CACHE[cwd]


def paseo(args, *, timeout=600):
    """返回 stdout。非零返回码立即失败——空 stdout 曾被当成「没有输出」继续走。"""
    r = subprocess.run(['paseo', *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        head = ' '.join(args[:3])
        raise SystemExit(f'paseo {head} 失败（rc={r.returncode}）：{(r.stderr or r.stdout).strip()[:400]}')
    return r.stdout


def paseo_json(args, **kw):
    out = paseo(args, **kw)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        head = ' '.join(args[:3])
        raise SystemExit(f'paseo {head} 输出不是合法 JSON：{e}；前 200 字节 {out[:200]!r}')


def write_atomic(path, text):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=p.name + '.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


def write_json_atomic(path, obj):
    write_atomic(path, json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')


def expected_coverage(envelope):
    """从冻结输入取出「本 lane 应当恰好覆盖哪些 revision、按什么顺序」。

    surface   信封：payload.entries[].entry_revision_identity
    contextual信封：payload.ordered_revision_keys
    两种形态都没有就报错——宁可拒绝收割，也不放行一个无法校验覆盖的产物。
    """
    p = envelope['payload']
    if isinstance(p.get('entries'), list) and p['entries']:
        return [e['entry_revision_identity'] for e in p['entries']]
    if isinstance(p.get('ordered_revision_keys'), list) and p['ordered_revision_keys']:
        return list(p['ordered_revision_keys'])
    raise SystemExit('信封里既无 payload.entries 也无 payload.ordered_revision_keys，无法校验覆盖')
