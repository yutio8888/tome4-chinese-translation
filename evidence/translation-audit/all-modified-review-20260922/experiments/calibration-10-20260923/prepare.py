"""Build clean calibration inputs from existing frozen evidence; no original writes."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
EXP = HERE.parent
B = HERE / 'blind'
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def put(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

chosen = [(12, '03620'), (14, '03714'), (12, '03627'), (14, '03729'),
          (11, '03605'), (13, '03689'), (13, '03692'), (11, '03595'),
          (11, '03596'), (12, '03646')]
entries, mapping, terms, access = [], [], set(), {}
keep = ['source', 'target', 'section', 'source_tag', 'args_order', 'special', 'component', 'occurrence']
groups = sorted({g for g, _ in chosen})
for g in groups:
    p = EXP / f'abc20-g{g:02}-20260923'
    a = json.loads((p / 'source-access.json').read_text())
    for rel, h in a['files_sha256'].items():
        src = p / 'sources' / rel
        assert digest(src) == h, src
        access[str(src)] = h
    for c in a.get('dlc_additional_sources', {}).values():
        for rel, h in c['files_sha256'].items():
            access[str(Path(c['root']) / rel)] = h
    # Translation context contains no old findings or reviewer identity.
    (B / f'context-{g}.lua').write_bytes((p / 'context.lua').read_bytes())
    inp = (p / 'INPUT.md').read_text()
    table = inp[inp.index('source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes'):]
    terms.update(line for line in table.splitlines()[1:] if line.count('\t') == 7)
for n, (g, ident) in enumerate(chosen, 1):
    p = EXP / f'abc20-g{g:02}-20260923'
    item = next(x for x in json.loads((p / 'entries.json').read_text()) if x['audit_id'] == 'entry-' + ident)
    clean = {k: item.get(k) for k in keep}
    clean['id'] = f'K{n:02}'
    clean['context_file'] = f'context-{g}.lua'
    clean['source_file'] = str(p / 'sources' / 'dlc' / item['component'] / item['section'])
    entries.append(clean)
    mapping.append({'id': clean['id'], 'entry_id': item['audit_id'], 'group': g,
                    'original_entries_sha256': digest(p / 'entries.json')})
put(B / 'entries.json', entries)
put(HERE / 'HOST-MAPPING.json', mapping)
put(B / 'source-access.json', {'engine_repository': '/workspace/t-engine4',
    'engine_commit': '624a67329fe2ad440c5b344785a9c73fcf22ae63',
    'dlc_source_pinning': 'hash fixed; repository, commit and target version unpinned',
    'allowed_dlc_files_sha256': access})
(B / 'terms.tsv').write_text('source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n' + '\n'.join(sorted(terms)) + '\n')
(B / 'TERMINOLOGY.md').write_bytes((ROOT / 'TERMINOLOGY.md').read_bytes())
head_rules = subprocess.check_output(['git', 'show', 'HEAD:TERMINOLOGY.md'])
assert head_rules == (B / 'TERMINOLOGY.md').read_bytes()
put(HERE / 'PROVENANCE.json', {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'terminology_rules_equal_HEAD': True,
    'rule_note': 'Current HEAD scope rules supplied explicitly for calibration; original reviewer package did not include full scope definition. Do not retroactively overwrite original scores.',
    'selected_entries': mapping,
    'blind_file_hashes': {p.name: digest(p) for p in B.iterdir() if p.is_file()}})
# Guard all previous experiment reports, metrics, inputs and tracked worktree files.
guard = {str(p.relative_to(ROOT)): digest(p) for p in EXP.rglob('*')
         if p.is_file() and HERE not in p.parents and 'sources' not in p.parts}
for rel in subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0'):
    if rel and (ROOT / rel).is_file():
        guard[rel] = digest(ROOT / rel)
put(HERE / 'BASELINE-GUARD.json', guard)
print(f'Built {len(entries)} clean entries, {len(terms)} frozen term rows, {len(access)} permitted source files, {len(guard)} protected files.')
