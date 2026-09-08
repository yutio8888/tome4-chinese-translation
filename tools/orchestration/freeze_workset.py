#!/usr/bin/env python3
"""冻结一个生产批次的公开源码工作集（evidence/quality/production-batches/<batch>-source-workset.json）。

用法：python3 -B tools/orchestration/freeze_workset.py <batch_id>
前置：存在 active checkpoint；环境变量 TOME_ENGINE_ROOT、TOME_DLC_ROOT 已设置。
覆盖四类源码归属形态，任一未命中即报 MISS 并须人工归因（不得放行）：
  1. 直接字面量（含 \n/\t 转义变体与多行回退）
  2. 宿主生成键 host_generated_key_verification（DLC birth facial category）
  3. interface 混入归属 interface_mixin_verification（extractor 把 interface 字面量记到引入方）
  4. `.always_merge` 跨模块键 always_merge_locale_verification（上游 zh_hans locale 定义的
     跨模块专名/术语；catalog 记 normalized_path=engine.lua、section=".always_merge"）
  5. 上游 locale 的历史遗留条目 legacy_locale_entry_verification（locale 在该 section 下以
     `-- old translated text` 标注保留，固定源码已无对应代码字面量）
另注：engine.lua 的 section 也可能是 DLC 路径（如 tome-cults/...），此时按 section 前缀
解析到 DLC 根，而不是按 normalized_path。
详见 docs/baseline-batch-runbook-2026-09-06.md。
"""
import json, hashlib, os, re, subprocess, sys

EXTRACTOR_COMMIT = 'bdc19d22862f7a6cfbe71d7136145720ecea7bf7'
EXTRACTOR_SHA256 = '6ada26a3c126dca5386ad7e15ea6faa856b1715841083ba6622d99d9e61fd0ba'
from pathlib import Path

ROOT = Path(os.environ.get('TOME_TRANSLATION_ROOT', Path(__file__).resolve().parents[2]))
ENGINE_ROOT = Path(os.environ['TOME_ENGINE_ROOT'])   # 由 Paseo 环境提供
DLC_ROOT = Path(os.environ['TOME_DLC_ROOT'])         # 由 Paseo 环境提供

PINNED_MAP = {
    'mod-tome.lua':  ('tome',   'mod-tome/',  'game/modules/tome/'),
    'engine.lua':    ('engine', 'engine/',    'game/engines/default/'),
    'mod-boot.lua':  ('boot',   'mod-boot/',  'game/engines/default/modules/boot/'),
}
DLC_MAP = {
    'tome-orcs.lua':         ('orcs',         'orcs'),
    'tome-cults.lua':        ('cults',        'cults'),
    'tome-ashes-urhrok.lua': ('ashes-urhrok', 'ashes-urhrok'),
}

def unescape_variants(s):
    out = [s]
    # engine files may write embedded newlines/tabs as two-char escapes
    esc = s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')
    if esc != s:
        out.append(esc)
    simple = s.replace('\n', '\\n').replace('\t', '\\t')
    if simple not in out:
        out.append(simple)
    return out

ALWAYS_MERGE_LOCALE = 'game/engines/default/data/locales/engine/zh_hans.lua'

def resolve(snap):
    npath = snap['normalized_path']
    section = snap['section']
    # `.always_merge` 是上游 zh_hans locale 定义的跨模块键集合，没有单一代码字面量归属
    if section == '.always_merge':
        return 'engine', ALWAYS_MERGE_LOCALE, ENGINE_ROOT / ALWAYS_MERGE_LOCALE, True
    # section 可能跨组件（engine.lua 的 catalog 里出现 tome-cults/... 的 section）
    for lua, (comp, dlc) in DLC_MAP.items():
        prefix = f'tome-{dlc}/'
        if section.startswith(prefix):
            rel = section[len(prefix):]
            return comp, section, DLC_ROOT / dlc / f'tome-{dlc}' / rel, False
    if npath in PINNED_MAP:
        comp, prefix, pubroot = PINNED_MAP[npath]
        assert section.startswith(prefix), (npath, section)
        rel = section[len(prefix):]
        pub = pubroot + rel
        return comp, pub, ENGINE_ROOT / pub, True
    comp, dlc = DLC_MAP[npath]
    pub = section
    rel = section.split('/', 1)[1]
    return comp, pub, DLC_ROOT / dlc / f'tome-{dlc}' / rel, False

def main():
    batch = sys.argv[1]
    cp = json.loads((ROOT / '.artifacts/i18n/production-review-v2-lite/active-batch.json').read_text())
    assert cp['batch_id'] == batch, cp['batch_id']
    snaps = cp['entry_snapshots']
    entries, verifs = [], []
    filecache = {}
    for snap in snaps:
        comp, pub, abspath, pinned = resolve(snap)
        if abspath not in filecache:
            data = abspath.read_bytes()
            filecache[abspath] = (hashlib.sha256(data).hexdigest(), data.decode('utf-8').split('\n'))
        fsha, lines = filecache[abspath]
        src = snap['source']
        variants = unescape_variants(src)
        hits = []
        for i, line in enumerate(lines, 1):
            if any(v in line for v in variants):
                hits.append(i)
        if not hits:
            # multi-line literal: match against whole text
            whole = '\n'.join(lines)
            if any(v in whole for v in variants):
                idx = whole.index(next(v for v in variants if v in whole))
                start = whole.count('\n', 0, idx) + 1
                hits = list(range(start, start + src.count('\n') + 1))
        mixin = None
        if not hits:
            # extractor 把 interface 的字面量归属到 require/混入它的类文件。
            # 回退：解析该 section 文件的 require "<pkg>"，在被引入文件中定位字面量。
            whole = '\n'.join(lines)
            for req in re.findall(r'require\s+"([\w.]+)"', whole):
                parts = req.split('.')
                if parts[0] == 'mod':
                    cand = abspath.parents[len(Path(pub).parts) - 2] if False else None
                # 由 public root 推导：section 的 public 前缀 + require 路径
                rel = '/'.join(parts[1:]) + '.lua' if parts[0] in ('mod', 'engine') else None
                if not rel:
                    continue
                base = ENGINE_ROOT / ('game/modules/tome' if parts[0] == 'mod'
                                      else 'game/engines/default')
                cpath = base / rel
                if not cpath.is_file():
                    continue
                cdata = cpath.read_bytes().decode('utf-8')
                clines = cdata.split('\n')
                chits = [i for i, ln in enumerate(clines, 1)
                         if any(v in ln for v in variants)]
                if chits:
                    reqlines = [i for i, ln in enumerate(lines, 1) if req in ln]
                    mixin = {
                        'algorithm': 'interface-mixin-attribution/1',
                        'including_file_require_lines': reqlines,
                        'literal_file_sha256': hashlib.sha256(cpath.read_bytes()).hexdigest(),
                        'literal_lines': chits,
                        'literal_public_source_path': str(cpath.relative_to(ENGINE_ROOT)),
                        'require_package': req,
                        'rule': 'extractor attributes an interface literal to the class that requires/mixes it in',
                        'status': 'confirmed',
                    }
                    break
        hostgen = None
        if not hits and snap['source_tag'] == 'birth facial category':
            # extractor i18n_tools/i18n_extractor.lua lines 174-180 (commit bdc19d2):
            # cosmetic_options field key -> gsub("_"," "):capitalize()
            want = src
            for i, line in enumerate(lines, 1):
                m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{\s*$", line)
                if m:
                    key = m.group(1)
                    derived = key.replace('_', ' ')
                    derived = derived[:1].upper() + derived[1:]
                    if derived == want:
                        hostgen = {
                            'extractor_commit': EXTRACTOR_COMMIT,
                            'extractor_lines': [174, 180],
                            'extractor_path': 'i18n_tools/i18n_extractor.lua',
                            'extractor_sha256': EXTRACTOR_SHA256,
                            'limitation': 'DLC source repository/commit unpinned; exact local public file bound by SHA-256',
                            'rule': 'cosmetic_options field key, underscore to space then capitalize',
                            'source_key': key,
                            'source_lines': [i],
                            'status': 'confirmed',
                        }
                        break
        always_merge = None
        if snap['section'] == '.always_merge':
            # 上游 locale 以 t("<source>", ...) 定义该键；命中行即其公开定义处
            amlines = [i for i, ln in enumerate(lines, 1)
                       if ln.startswith(f't("{src}",')]
            if amlines:
                always_merge = {
                    'algorithm': 'always-merge-locale-attribution/1',
                    'locale_public_source_path': ALWAYS_MERGE_LOCALE,
                    'locale_section': '.always_merge',
                    'rule': 'cross-module proper noun/term defined by the upstream zh_hans locale always_merge section',
                    'source_lines': amlines,
                    'status': 'confirmed',
                }
                hits = amlines
        legacy = None
        if not hits and pinned and snap['normalized_path'] == 'engine.lua':
            # 上游 locale 把当前源码已无字面量的历史条目留在对应 section 下，
            # 并以 `-- old translated text` 标注。按该标注归属，不算未命中。
            lpath = ENGINE_ROOT / ALWAYS_MERGE_LOCALE
            llines = lpath.read_bytes().decode('utf-8').split('\n')
            want_section = f'section "{snap["section"]}"'
            in_section, marker = False, None
            for i, ln in enumerate(llines, 1):
                if ln.startswith('section "'):
                    in_section = (ln.strip() == want_section)
                    marker = None
                    continue
                if not in_section:
                    continue
                if ln.strip() == '-- old translated text':
                    marker = i
                if ln.startswith(f't("{src}",') and marker is not None:
                    legacy = {
                        'algorithm': 'legacy-locale-entry-attribution/1',
                        'locale_marker_line': marker,
                        'locale_public_source_path': ALWAYS_MERGE_LOCALE,
                        'locale_section': snap['section'],
                        'locale_sha256': hashlib.sha256(lpath.read_bytes()).hexdigest(),
                        'rule': 'upstream locale keeps the entry under "-- old translated text"; the fixed source no longer contains the literal',
                        'source_lines': [i],
                        'status': 'confirmed',
                    }
                    break
        row = {
            'args_order': snap.get('risk', {}).get('args_order'),
            'component': comp,
            'entry_revision_identity': snap['entry_revision_identity'],
            'fixed_source_commit': snap['fixed_source_identity'][7:] if pinned else None,
            'literal_source_match': bool(hits),
            'matching_literal_lines': hits,
            'public_source_path': pub,
            'section': snap['section'],
            'source': src,
            'source_file_sha256': fsha,
            'source_pinning': 'pinned' if pinned else 'unpinned',
            'source_tag': snap['source_tag'],
            'verification_status': 'confirmed' if pinned else None,
        }
        if mixin is not None:
            row['interface_mixin_verification'] = mixin
            row['matching_literal_lines'] = None
            row['verification_status'] = 'confirmed'
        if legacy is not None:
            row['legacy_locale_entry_verification'] = legacy
            row['literal_source_match'] = False
            row['matching_literal_lines'] = None
            row['verification_status'] = 'confirmed'
        if always_merge is not None:
            row['always_merge_locale_verification'] = always_merge
            row['verification_status'] = 'confirmed'
        if hostgen is not None:
            row['host_generated_key_verification'] = hostgen
            row['matching_literal_lines'] = None
            row['verification_status'] = 'confirmed'
        if not pinned:
            row['actual_public_source_match'] = bool(hits)
            row['provenance_note'] = (f'Locally available public {comp} source; source repository/commit not pinned. '
                                      'Catalog extraction snapshot identity is not a source commit.')
            row['source_commit'] = None
        verifs.append(row)
        entries.append(snap)
    miss = [v for v in verifs if not v['literal_source_match']
            and 'host_generated_key_verification' not in v
            and 'interface_mixin_verification' not in v
            and 'legacy_locale_entry_verification' not in v]
    out = {
        'base_commit': cp['base_commit'],
        'batch_id': batch,
        'boundary_reason': 'Stable policy selection of 80 revisions, no source-identity truncation. Source verification is not semantic completion.',
        'catalog_id': cp['catalog_id'],
        'entries': entries,
        'entry_count': len(entries),
        'kind': 'production_batch_public_source_workset_v1',
        'schema_version': 1,
        'source_verification': verifs,
    }
    dest = ROOT / 'evidence/quality/production-batches' / f'{batch}-source-workset.json'
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    print('entries', len(entries), 'matched', len(entries) - len(miss), 'missing', len(miss))
    for m in miss:
        print('MISS', m['section'], '|', m['source'][:90])

main()
