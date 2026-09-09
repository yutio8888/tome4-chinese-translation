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
  6. 动态 tag 的兄弟文件表键 dynamic_tag_sibling_key_verification（_t(<expr>, "<tag>") 的
     运行时取值来自同目录兄弟文件里的表键，字面量不在条目所属文件内）
  7. 运行期拼接实体名 concatenated_entity_name_verification（`"<前缀>"..name:lower()`
     与具名调用实参在源码里分处两地，两半都不是完整字面量）
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

STANDARD_TAGS = {'_t', 'tformat', 'log', 'logPlayer', 'logSeen', 'logCombat',
                 'entity name', 'talent name', 'entity desc', 'talent desc'}

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

def _lib():
    """按需引入生产库，复用其正典字节/哈希实现，绝不自己另写一套。"""
    sys.path.insert(0, str(ROOT / 'tools'))
    from i18nlib import production_review_v2_lite_batch as B
    from i18nlib import production_review_v2_lite as C
    return B, C


def _proven_selection_mode(B, man):
    """selection_mode 不在 manifest 里，但 batch_id = sha(mode|selected|attempt)。

    对两个合法取值各算一遍，只有一个能复现 manifest 里的 batch_id。
    这是证明不是猜测：命中唯一即确定，命中 0 或 2 个一律拒绝。
    """
    hits = [m for m in ('queued', 'retry_blocked')
            if B._batch_id(m, man['ordered_revisions'], man['attempt']) == man['batch_id']]
    if len(hits) != 1:
        raise SystemExit(f'无法由 batch_id 唯一反推 selection_mode：命中 {hits}')
    return hits[0]


def load_checkpoint(batch):
    """优先用 active checkpoint；批次已 finalize 时从受跟踪证据确定性重建。

    重建来源全部是已提交的证据，不依赖任何运行时残留：
      manifest.json -> ordered_revisions + attempt + base_commit + catalog_id + 两个摘要
      git show <base_commit>:evidence/.../catalog/entries.jsonl -> 每条的完整目录行
    checkpoint 比目录行多两个队列运行期字段，都不是猜的：
      row_sha256           = sha256(canonical_bytes(目录行))，与 batch.py:795 同一函数
      prior_effective_state= 由 batch.py:794 的规则套用反推出的 selection_mode
    重建完成后用 manifest 记录的 ordered_revisions_sha256 与 entry_snapshots_sha256
    逐一比对；两个摘要都命中，才说明重建结果与当时的 checkpoint 逐字节一致。
    """
    live = ROOT / '.artifacts/i18n/production-review-v2-lite/active-batch.json'
    if live.is_file():
        cp = json.loads(live.read_text())
        if cp.get('batch_id') == batch:
            return cp, 'active_checkpoint'

    man_path = ROOT / 'evidence/production-review-v2-lite/batches' / batch / 'manifest.json'
    if not man_path.is_file():
        raise SystemExit(f'既无 active checkpoint 也无受跟踪证据：{man_path}')
    man = json.loads(man_path.read_text())
    assert man['batch_id'] == batch, man['batch_id']

    B, C = _lib()
    canon, sha = B.wp1.canonical_bytes, B._sha
    keys = sorted(C.ENTRY_KEYS)
    mode = _proven_selection_mode(B, man)

    raw = subprocess.run(
        ['git', 'show', f"{man['base_commit']}:evidence/production-review-v2-lite/catalog/entries.jsonl"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    by_rev = {}
    for line in raw.splitlines():
        if line.strip():
            e = json.loads(line)
            by_rev[e['entry_revision_identity']] = e

    snaps, rows = [], []
    for rev in man['ordered_revisions']:
        e = by_rev.get(rev)
        if e is None:
            raise SystemExit(f'base_commit 处目录缺少 revision {rev}')
        row = {k: e[k] for k in keys}
        snap = dict(row)
        snap['prior_effective_state'] = 'blocked' if mode == 'retry_blocked' else 'queued'
        snap['row_sha256'] = sha(canon(row))
        rows.append(row)
        snaps.append(snap)

    if sha(canon(man['ordered_revisions'])) != man['ordered_revisions_sha256']:
        raise SystemExit('ordered_revisions 摘要不符，证据自身不自洽')
    if sha(canon(rows)) != man['entry_snapshots_sha256']:
        raise SystemExit('重建的 entry_snapshots 与 manifest 摘要不符，拒绝写出')

    return {'batch_id': batch, 'base_commit': man['base_commit'],
            'catalog_id': man['catalog_id'], 'selection_mode': mode,
            'entry_snapshots': snaps}, 'rebuilt_from_evidence'


def main():
    batch = sys.argv[1]
    cp, provenance = load_checkpoint(batch)
    print(f'[freeze_workset] {batch} 来源={provenance}', file=sys.stderr)
    snaps = cp['entry_snapshots']
    entries, verifs = [], []
    filecache = {}
    for snap in snaps:
        comp, pub, abspath, pinned = resolve(snap)
        if abspath not in filecache:
            data = abspath.read_bytes()
            text = data.decode('utf-8')
            # 上游有 16 个 .lua 是 CRLF。目录抽取时行尾已规范为 LF，
            # 这里若保留 \r，跨行字面量必然假性未命中（runbook §34.1）。
            # 只规范用于匹配的文本；source_file_sha256 仍是磁盘原始字节的摘要。
            crlf = '\r\n' in text
            filecache[abspath] = (hashlib.sha256(data).hexdigest(),
                                  text.replace('\r\n', '\n').split('\n'), crlf)
        fsha, lines, crlf = filecache[abspath]
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
        sibling_key = None
        if not hits and snap['source_tag'] not in STANDARD_TAGS:
            # 动态 _t(<expr>, "<自定义 tag>")：运行时值来自同目录兄弟文件里的表键，
            # 条目所在文件只出现该 tag 的调用点，字面量本身不在该文件。
            tag = snap['source_tag']
            taglines = [i for i, ln in enumerate(lines, 1)
                        if '_t(' in ln and f'"{tag}"' in ln]
            if taglines:
                keyre = re.compile(r'[{,]\s*' + re.escape(src) + r'\s*=')
                for sib in sorted(abspath.parent.glob('*.lua')):
                    if sib == abspath:
                        continue
                    sl = sib.read_bytes().decode('utf-8').split('\n')
                    klines = [i for i, ln in enumerate(sl, 1) if keyre.search(ln)]
                    if klines:
                        sibling_key = {
                            'algorithm': 'dynamic-tag-sibling-key-attribution/1',
                            'dynamic_call_lines': taglines,
                            'key_file_sha256': hashlib.sha256(sib.read_bytes()).hexdigest(),
                            'key_lines': klines,
                            'key_public_source_path': str(sib.relative_to(DLC_ROOT)) if str(sib).startswith(str(DLC_ROOT)) else str(sib.relative_to(ENGINE_ROOT)),
                            'rule': ('entry is a runtime value of a dynamic _t(<expr>, "<tag>") call; '
                                     'the literal is a table key defined in a sibling file of the same directory'),
                            'source_key': src,
                            'status': 'confirmed',
                        }
                        break
        concat = None
        if not hits and snap['source_tag'] == 'entity name':
            # `name = "alchemist "..name:lower()`：条目是运行期拼接值，
            # 前缀在拼接处，剩余部分是同文件某次具名调用的字面量实参。
            whole = '\n'.join(lines)
            for m in re.finditer(r'"([^"\\]*)"\s*\.\.\s*name:lower\(\)', whole):
                prefix = m.group(1)
                if not src.startswith(prefix):
                    continue
                rest = src[len(prefix):]
                arglines = [i for i, ln in enumerate(lines, 1)
                            for a in re.findall(r'\(\s*"([^"\\]*)"\s*,', ln)
                            if a.lower() == rest]
                if not arglines:
                    continue
                concat = {
                    'algorithm': 'concatenated-entity-name-attribution/1',
                    'argument_lines': arglines,
                    'concat_lines': [whole.count('\n', 0, m.start()) + 1],
                    'literal_prefix': prefix,
                    'resolved_argument': rest,
                    'rule': ('entity name is built at runtime by concatenating a literal prefix '
                             'with a lowercased call argument; neither half is a whole literal'),
                    'status': 'confirmed',
                }
                break
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
            'line_ending_normalization': 'crlf_to_lf' if crlf else None,
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
        if sibling_key is not None:
            row['dynamic_tag_sibling_key_verification'] = sibling_key
            row['literal_source_match'] = False
            row['matching_literal_lines'] = None
            row['verification_status'] = 'confirmed'
        if concat is not None:
            row['concatenated_entity_name_verification'] = concat
            row['literal_source_match'] = False
            row['matching_literal_lines'] = None
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
            and 'legacy_locale_entry_verification' not in v
            and 'dynamic_tag_sibling_key_verification' not in v
            and 'concatenated_entity_name_verification' not in v]
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
