#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为审核者生成「冻结证据包」：只有客观事实，不含结论。

用法：
  python3 -B tools/orchestration/build_evidence_pack.py <batch_id> [--context 3] [--siblings 4]
环境：TOME_ENGINE_ROOT、TOME_DLC_ROOT（与 freeze_workset.py 相同）

产出 evidence/quality/production-batches/<batch>-evidence-pack.json，逐条包含：
  - 固定源码版本与归属（pinned 的记 commit；DLC 未固定的**显式声明**并只以文件 SHA-256 绑定）
  - 调用点原文片段（带行号，含上下文），文件 SHA-256
  - 占位符清单与其取值来源，含伤害格式的领域约定（runbook §33.1）
  - 命中的术语表词条：category/domain/source_tag/status/scope 与**已批准译法**
  - 同术语在库内其它条目的现有写法（标注为「现状」，不是标准）
  - 运行期拼接／宿主生成键等非字面量归属关系

**刻意不放进去的东西**（这是本工具的要点，不是疏漏）：
  上一轮的 finding、裁决结论、期待答案、任何 .ai/reviews 或 adjudications 内容。
  审核者要独立得出结论；把上一轮结论塞进上下文，两轮就不再是独立观察，
  §23 的「两轮各自复现同一主张才算 confirmed」也就失去意义。
  裁决索引由编排者在自己的上下文里维护，不下发。
"""
import argparse, hashlib, json, os, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import _orch

ROOT = _orch.ROOT
ENGINE_ROOT = pathlib.Path(os.environ.get('TOME_ENGINE_ROOT', '/workspace/t-engine4'))
DLC_ROOT = pathlib.Path(os.environ.get('TOME_DLC_ROOT', '/workspace/tome4-dlcs'))

# 伤害格式是维护者确认的领域约定（runbook §33.1），属于客观事实而非对本条的结论。
FORMAT_NOTES = {
    '%d%%': '百分比伤害：基于武器基础伤害的百分比（ToME4 约定）',
    '%0.2f': '点数伤害：固定点数，与武器基础伤害无关（ToME4 约定）',
}
# 转换说明符：% + 标志 + 宽度 + .精度 + 转换字符；`%d%%` 这种「百分比」整体视为一个单位。
# 单独的 `%%` 是字面百分号，不是占位符——旧写法把它算成占位符，
# 又因为标志类里含空格而把 "50%%, putting" 误配成 "%.  W"，产生假的顺序不一致。
_CONV = r'%[-+#0]*[0-9]*(?:\.[0-9]+)?[diouxXeEfFgGcsq]'
PLACEHOLDER_RE = re.compile(rf'(?:{_CONV}%%)|(?:{_CONV})|%%')


def load_terminology():
    rows = []
    for tsv in sorted((ROOT / 'terminology').glob('*.tsv')):
        lines = tsv.read_text(encoding='utf-8').splitlines()
        head = lines[0].split('\t')
        for line in lines[1:]:
            if not line.strip():
                continue
            cells = line.split('\t')
            row = dict(zip(head, cells + [''] * (len(head) - len(cells))))
            row['_file'] = tsv.name
            rows.append(row)
    return rows


def order_ok(src_specs, tgt_specs, args_order):
    """占位符顺序是否成立——必须考虑 args_order，否则合法重排会被报成不一致。

    args_order[i] = 译文第 i 个占位符取源文第几个实参（1 起）。
    未声明时才要求两边序列逐一相等。
    """
    if not args_order:
        return src_specs == tgt_specs
    if len(args_order) != len(tgt_specs) or sorted(args_order) != list(range(1, len(src_specs) + 1)):
        return False
    return [src_specs[i - 1] for i in args_order] == tgt_specs


def snippet(path, lines, want, context):
    """返回带行号的原文片段。行号是 1 起，与编辑器一致。"""
    if not want:
        return []
    out, seen = [], set()
    for n in want:
        for i in range(max(1, n - context), min(len(lines), n + context) + 1):
            if i not in seen:
                seen.add(i)
                out.append({'line': i, 'text': lines[i - 1], 'is_match': i in set(want)})
    out.sort(key=lambda r: r['line'])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch')
    ap.add_argument('--context', type=int, default=3)
    ap.add_argument('--siblings', type=int, default=4)
    args = ap.parse_args()
    batch = args.batch

    wsp = ROOT / 'evidence/quality/production-batches' / f'{batch}-source-workset.json'
    if not wsp.is_file():
        raise SystemExit(f'先跑 freeze_workset.py：缺少 {wsp}')
    ws = json.loads(wsp.read_text())
    snaps = {e['entry_revision_identity']: e for e in ws['entries']}

    terms = load_terminology()
    # 全库现有写法索引：源文里出现某术语的条目，用于「现状」佐证
    catalog = [json.loads(l) for l in
               (ROOT / 'evidence/production-review-v2-lite/catalog/entries.jsonl'
                ).read_text().splitlines() if l.strip()]

    filecache = {}
    packs = []
    for ver in ws['source_verification']:
        rev = ver['entry_revision_identity']
        snap = snaps[rev]
        src, tgt = snap['source'], snap['target']

        # --- 调用点原文 ---
        call = {'public_source_path': ver['public_source_path'],
                'source_file_sha256': ver['source_file_sha256'],
                'matching_lines': ver['matching_literal_lines'],
                'snippet': []}
        if ver['matching_literal_lines']:
            base = ENGINE_ROOT if ver['source_pinning'] == 'pinned' else DLC_ROOT
            p = base / ver['public_source_path']
            if not p.is_file() and ver['source_pinning'] != 'pinned':
                comp = ver['component']
                p = DLC_ROOT / comp / ver['public_source_path']
            if p.is_file():
                if p not in filecache:
                    filecache[p] = p.read_bytes().decode('utf-8').replace('\r\n', '\n').split('\n')
                call['snippet'] = snippet(p, filecache[p], ver['matching_literal_lines'], args.context)

        # --- 占位符 ---
        placeholders = []
        for m in PLACEHOLDER_RE.finditer(src):
            spec = m.group(0)
            note = FORMAT_NOTES.get(spec)
            placeholders.append({'spec': spec, 'offset': m.start(),
                                 'convention': note} if note else
                                {'spec': spec, 'offset': m.start()})
        src_specs = [p['spec'] for p in placeholders if p['spec'] != '%%']
        tgt_specs = [m.group(0) for m in PLACEHOLDER_RE.finditer(tgt) if m.group(0) != '%%']

        # --- 术语 ---
        low = src.lower()
        hits = []
        for t in terms:
            s = t.get('source', '')
            if s and re.search(r'\b' + re.escape(s.lower()) + r'\b', low):
                hits.append({'source': s, 'approved_target': t.get('target', ''),
                             'category': t.get('category', ''), 'domain': t.get('domain', ''),
                             'source_tag': t.get('source_tag', ''), 'status': t.get('status', ''),
                             'scope': t.get('scope', ''), 'table': t['_file']})
        hits.sort(key=lambda h: (-len(h['source']), h['source']))

        # --- 同术语的库内现状（不是标准，仅供一致性比对）---
        siblings = []
        for h in hits[:3]:
            pat = re.compile(r'\b' + re.escape(h['source'].lower()) + r'\b')
            found = []
            for e in catalog:
                if e['entry_revision_identity'] == rev:
                    continue
                if pat.search(e['source'].lower()):
                    found.append({'section': e['section'], 'source_tag': e['source_tag'],
                                  'source': e['source'][:120], 'current_target': e['target'][:120]})
                if len(found) >= args.siblings:
                    break
            if found:
                siblings.append({'term': h['source'], 'existing_usages': found})

        row = {
            'entry_revision_identity': rev,
            'component': ver['component'],
            'section': ver['section'],
            'source_tag': ver['source_tag'],
            'source': src,
            'current_target': tgt,
            'source_pinning': ver['source_pinning'],
            'fixed_source_commit': ver.get('fixed_source_commit'),
            'call_site': call,
            'placeholders': placeholders,
            'placeholder_order_matches': order_ok(src_specs, tgt_specs, ver.get('args_order')),
            'placeholders_in_target': tgt_specs,
            'args_order': ver.get('args_order'),
            'terminology': hits,
            'existing_library_usage': siblings,
        }
        if ver['source_pinning'] != 'pinned':
            row['unpinned_source_disclosure'] = ver.get('provenance_note')
        for key in ('concatenated_entity_name_verification', 'host_generated_key_verification',
                    'interface_mixin_verification', 'dynamic_tag_sibling_key_verification',
                    'always_merge_locale_verification', 'legacy_locale_entry_verification'):
            if key in ver:
                row['non_literal_attribution'] = {'kind': key, **ver[key]}
        packs.append(row)

    out = {
        'batch_id': batch,
        'base_commit': ws['base_commit'],
        'catalog_id': ws['catalog_id'],
        'kind': 'production_batch_reviewer_evidence_pack_v1',
        'schema_version': 1,
        'entry_count': len(packs),
        'excluded_by_design': ('prior findings, adjudication conclusions, expected answers, '
                               'and any .ai/reviews or adjudications content are deliberately absent'),
        'entries': packs,
    }
    body = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n'
    dest = ROOT / 'evidence/quality/production-batches' / f'{batch}-evidence-pack.json'
    _orch.write_atomic(dest, body)
    print(f'{dest.name}  {len(packs)} 条  sha256={hashlib.sha256(body.encode()).hexdigest()[:16]}')
    print(f'  有调用点片段 {sum(1 for r in packs if r["call_site"]["snippet"])} 条')
    print(f'  命中术语     {sum(1 for r in packs if r["terminology"])} 条')
    print(f'  含占位符     {sum(1 for r in packs if r["placeholders"])} 条'
          f'（顺序与源文不一致 {sum(1 for r in packs if not r["placeholder_order_matches"])} 条）')
    print(f'  非字面量归属 {sum(1 for r in packs if "non_literal_attribution" in r)} 条')
    print(f'  未固定来源   {sum(1 for r in packs if r["source_pinning"] != "pinned")} 条')


main()
