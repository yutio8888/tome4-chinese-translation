#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库死键扫描（v2）：找出「英文原文在 pinned 游戏树中已不存在」的目录条目。

判据：source 文本能否在该组件对应的公开源码里找到。**不按 tag 或 section 判**
——engine/I18N.lua 的 set() 会把译文同时写进 table[tag][key] 与 table["nil"][key]，
get() 先试带 tag 的桶再回落 nil 桶，所以 tag 对不上、归属文件过期都不影响
运行时可达性；只有原文本身不存在（key 不同）才真正失效。

v1 的三处假阳性来源已修正：
  1. 文本不只在 .lua —— 还有 .chat（对话树）；
  2. `.always_merge` 条目由上游 zh_hans locale 定义，不在代码里；
  3. 运行期拼接名（如 "alchemist "..name:lower()）两半分处两地。
前两类直接纳入语料；第三类改为「命中失败后再试后缀」并单独归类，
不与真死键混在一起。

输出 JSON 清单，只读，不修改任何文件。
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path('/workspace/tome4-chinese-translation')
ENGINE = Path(os.environ['TOME_ENGINE_ROOT'])
DLC = Path(os.environ['TOME_DLC_ROOT'])
ALWAYS_MERGE = ENGINE / 'game/engines/default/data/locales/engine/zh_hans.lua'

SEARCH_ROOTS = {
    'mod-tome.lua':          [ENGINE / 'game/modules/tome'],
    'engine.lua':            [ENGINE / 'game/engines/default'],
    'mod-boot.lua':          [ENGINE / 'game/engines/default/modules/boot',
                              ENGINE / 'game/engines/default'],
    'tome-orcs.lua':         [DLC / 'orcs'],
    'tome-cults.lua':        [DLC / 'cults'],
    'tome-ashes-urhrok.lua': [DLC / 'ashes-urhrok'],
}
EXTS = ('*.lua', '*.chat')
SKIP_DIRS = {'locales'}


def load_corpus(roots):
    parts, seen = [], set()
    for r in roots:
        if not r.is_dir():
            continue
        for pat in EXTS:
            for p in sorted(r.rglob(pat)):
                if any(d in SKIP_DIRS for d in p.parts):
                    continue
                rp = str(p.resolve())
                if rp in seen:
                    continue
                seen.add(rp)
                try:
                    parts.append(p.read_bytes().decode('utf-8').replace('\r\n', '\n'))
                except UnicodeDecodeError:
                    continue
    return '\n'.join(parts)


def variants(s):
    out = [s]
    esc = s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')
    if esc != s:
        out.append(esc)
    simple = s.replace('\n', '\\n').replace('\t', '\\t')
    if simple not in out:
        out.append(simple)
    return out


def main():
    corpora = {c: load_corpus(r) for c, r in SEARCH_ROOTS.items()}
    for c, t in corpora.items():
        print(f'[corpus] {c}: {len(t)/1e6:.1f} MB', file=sys.stderr)
    am = ALWAYS_MERGE.read_text(encoding='utf-8') if ALWAYS_MERGE.is_file() else ''
    print(f'[corpus] .always_merge locale: {len(am)/1e6:.1f} MB', file=sys.stderr)

    dead, concat, amerge, hostgen, total = [], [], [], [], 0
    cat = ROOT / 'evidence/production-review-v2-lite/catalog/entries.jsonl'
    for line in cat.open(encoding='utf-8'):
        if not line.strip():
            continue
        e = json.loads(line)
        total += 1
        # section 可能跨组件（engine.lua 的条目带 tome-cults/... 的 section），
        # 必须按 section 前缀选语料，否则会在错误的树里搜索而假报缺失。
        comp = e['normalized_path']
        sec = e.get('section') or ''
        for lua, pref in (('tome-orcs.lua', 'tome-orcs/'), ('tome-cults.lua', 'tome-cults/'),
                          ('tome-ashes-urhrok.lua', 'tome-ashes-urhrok/')):
            if sec.startswith(pref):
                comp = lua
                break
        corpus = corpora.get(comp)
        if corpus is None:
            continue
        src, vs = e['source'], variants(e['source'])
        if any(v in corpus for v in vs):
            continue

        # birth facial category 是宿主生成键：extractor 由 cosmetic_options 的
        # 字段名 gsub("_"," "):capitalize() 派生，字面量本身不在源码里。
        if e.get('source_tag') == 'birth facial category':
            key = src[0].lower() + src[1:]
            key = key.replace(' ', '_')
            if re.search(r'\b' + re.escape(key) + r'\s*=\s*\{', corpus):
                hostgen.append({k: e.get(k) for k in
                                ('entry_revision_identity', 'normalized_path',
                                 'section', 'source_tag', 'source', 'target')})
                continue

        rec = {k: e.get(k) for k in
               ('entry_revision_identity', 'normalized_path', 'section',
                'source_tag', 'source', 'target')}

        # `.always_merge`：上游 locale 以 t("<source>", ...) 定义该键
        if e.get('section') == '.always_merge':
            if f't("{src}",' in am or f't([[{src}]],' in am:
                amerge.append(rec); continue

        # 运行期拼接：整串不在，但去掉首词后的余下部分作为独立字面量存在
        words = src.split(' ')
        if len(words) > 1:
            tail = ' '.join(words[1:])
            cands = {tail, tail.capitalize(), tail.title()}
            if len(tail) >= 3 and any(f'"{t}"' in corpus for t in cands):
                rec['concat_tail'] = tail
                concat.append(rec); continue

        dead.append(rec)

    from collections import Counter
    out = ROOT / '.artifacts/i18n/dead-key-scan.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'total_entries': total,
        'dead_candidates': len(dead),
        'excluded_always_merge': len(amerge),
        'excluded_runtime_concat': len(concat),
        'excluded_host_generated': len(hostgen),
        'dead_by_component': dict(Counter(x['normalized_path'] for x in dead)),
        'dead_by_section': dict(Counter(x['section'] for x in dead).most_common()),
        'dead': dead, 'always_merge': amerge, 'runtime_concat': concat,
        'host_generated': hostgen,
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f'\n扫描 {total} 条')
    print(f'  真死键候选        {len(dead)}')
    print(f'  排除 .always_merge {len(amerge)}（由上游 locale 定义，非代码字面量）')
    print(f'  排除 运行期拼接    {len(concat)}')
    print(f'  排除 宿主生成键    {len(hostgen)}（cosmetic_options 字段名派生）')
    print('候选按组件：', dict(Counter(x['normalized_path'] for x in dead)))
    print('候选按 section：')
    for s, n in Counter(x['section'] for x in dead).most_common(20):
        print(f'   {str(s):58} {n}')
    print('清单：', out)


main()
