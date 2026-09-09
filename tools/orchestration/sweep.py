#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库批量改译文：文本改写，语义校验，全过才落盘。

用法：
  python3 -B tools/orchestration/sweep.py plan  <rules.json>
  python3 -B tools/orchestration/sweep.py apply <rules.json>

rules.json：
  {"name": "...", "replacements": [{"pattern": "...", "replacement": "...", "flags": "M"}],
   "components": [...可选，缺省即全部 11 个...], "max_entries": 400}

做法：对整份文件做正则替换（文本），再用 LuaJIT 桥**重新语义解析**改后的字节，
逐条与改前比对。写盘前任何一条不符即整轮放弃——不写半个文件（runbook §31.3）。

替换只允许落在译文里。判据是一条可检验的等式：
    文件里实际发生的替换次数 == 各条译文里匹配次数之和
不相等就说明有匹配落在注释、源文或代码上（§30.6 曾因此改到被注释掉的条目）。

逐条守卫，每条都是踩过的坑：
  - 源文、source_tag、args_order、special 一律不得变化
  - 译文首尾空白不得变化（§27：删掉行首空格会破坏运行期字符串拼接）
  - 占位符转换序列不得变化（顺序变了实参就错绑）
  - 颜色/样式标记 #...# 序列不得变化
  - 条目数与顺序不得变化（注释掉或新增条目都会被发现）

文件集合默认是**六个目录内组件 + 五个 addon/example 组件**，共 11 个。
只遍历权威目录的 6 个会漏改，`06-runtime-collision-scan` 会挂（§27）。
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import _orch
from i18nlib.config import load_manifest
from i18nlib.locale_model import LocaleLoader
from i18nlib.runtime import LuaRuntime

ROOT = _orch.ROOT
CATALOG_COMPONENTS = ['engine.lua', 'mod-boot.lua', 'mod-tome.lua',
                      'tome-ashes-urhrok.lua', 'tome-cults.lua', 'tome-orcs.lua']
EXTRA_COMPONENTS = ['mod-example.lua', 'mod-example_realtime.lua', 'tome-addon-dev.lua',
                    'tome-items-vault.lua', 'tome-possessors.lua']
ALL_COMPONENTS = CATALOG_COMPONENTS + EXTRA_COMPONENTS

_CONV = r'%[-+#0]*[0-9]*(?:\.[0-9]+)?[diouxXeEfFgGcsq]'
SPEC_RE = re.compile(rf'(?:{_CONV}%%)|(?:{_CONV})|%%')
MARKER_RE = re.compile(r'#\{[a-z]+\}#|#[A-Z_]+#')


def compile_rules(rules):
    out = []
    for r in rules['replacements']:
        flags = 0
        for ch in r.get('flags', ''):
            flags |= {'M': re.M, 'S': re.S, 'I': re.I, 'X': re.X}[ch]
        out.append((re.compile(r['pattern'], flags), r['replacement']))
    return out


def apply_rules(text, compiled):
    """返回 (新文本, 替换次数)。"""
    n = 0
    for rx, rep in compiled:
        text, k = rx.subn(rep, text)
        n += k
    return text, n


def shape(s):
    """一条译文的不变量指纹：首尾空白、占位符序列、标记序列。"""
    lead = len(s) - len(s.lstrip())
    trail = len(s) - len(s.rstrip())
    return (s[:lead], s[len(s) - trail:] if trail else '',
            tuple(m.group(0) for m in SPEC_RE.finditer(s)),
            tuple(m.group(0) for m in MARKER_RE.finditer(s)))


def main():
    mode, rules_path = sys.argv[1], sys.argv[2]
    if mode not in ('plan', 'apply'):
        raise SystemExit('用法：sweep.py plan|apply <rules.json>')
    rules = json.loads(pathlib.Path(rules_path).read_text())
    compiled = compile_rules(rules)
    components = rules.get('components') or ALL_COMPONENTS
    missing = [c for c in ALL_COMPONENTS if c not in components]
    if missing:
        print(f'⚠ 未覆盖 {len(missing)} 个组件：{missing}')
        print('  只遍历部分组件会漏改同一 runtime key，06-runtime-collision-scan 会挂。')

    runtime = LuaRuntime(load_manifest(version=rules.get('version_manifest', 'tome-1.7.6'),
                                       manifest_path=None))
    loader = LocaleLoader(runtime)

    pending, problems, total_changed, key_index = [], [], 0, {}
    for name in components:
        p = ROOT / name
        if not p.is_file():
            problems.append(f'{name}: 文件不存在'); continue
        raw = p.read_bytes()
        text = raw.decode('utf-8')
        new_text, textual_hits = apply_rules(text, compiled)
        before = loader.load_bytes(raw, logical_path=name).translations
        if new_text == text:
            print(f'{name:26} 无匹配')
            continue
        after = loader.load_bytes(new_text.encode('utf-8'), logical_path=name).translations

        if len(before) != len(after):
            problems.append(f'{name}: 条目数从 {len(before)} 变成 {len(after)}')
            continue

        semantic_hits, changed = 0, []
        for i, (b, af) in enumerate(zip(before, after)):
            for key in ('source', 'source_tag', 'args_order', 'special'):
                if b.get(key) != af.get(key):
                    problems.append(f'{name}#{i}: {key} 被改动（只允许改译文）')
            want, k = apply_rules(b['target'], compiled)
            semantic_hits += k
            if af['target'] != want:
                problems.append(f'{name}#{i}: 译文结果与按规则推算的不一致')
            if k:
                if shape(b['target']) != shape(af['target']):
                    problems.append(f'{name}#{i}: 首尾空白/占位符/标记 序列被改变 —— {b["source"][:50]!r}')
                changed.append((b['source'], b['target'], af['target']))
                key_index.setdefault(b['source'], []).append(name)

        if textual_hits != semantic_hits:
            problems.append(f'{name}: 文本替换 {textual_hits} 次，但译文内只应有 {semantic_hits} 次'
                            f'——有匹配落在注释/源文/代码上')
        total_changed += len(changed)
        print(f'{name:26} 改 {len(changed):4d} 条（文本 {textual_hits} 次 / 语义 {semantic_hits} 次）')
        pending.append((p, new_text, changed))

    cap = rules.get('max_entries')
    if cap and total_changed > cap:
        problems.append(f'共 {total_changed} 条超过 max_entries={cap}，拒绝执行')

    cross = {k: v for k, v in key_index.items() if len(set(v)) > 1}
    if cross:
        print(f'\n跨组件 runtime key {len(cross)} 个（必须各组件一致，否则挂 runtime-collision）：')
        for k, v in list(cross.items())[:8]:
            print(f'   {k[:60]!r} -> {sorted(set(v))}')

    print(f'\n合计 {total_changed} 条译文')
    if problems:
        print(f'\n❌ {len(problems)} 项校验未过，不写任何文件：')
        for m in problems[:25]:
            print('  ', m)
        sys.exit(1)
    if mode == 'plan':
        print('✅ 全部校验通过（plan 模式，未写盘）')
        return
    for p, new_text, _ in pending:
        _orch.write_atomic(p, new_text)
    print(f'✅ 已写入 {len(pending)} 个文件；接下来：strict lint → catalog build → migration → 门禁')


main()
