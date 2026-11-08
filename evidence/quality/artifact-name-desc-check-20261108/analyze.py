import csv, re, json, collections, sys
csv.field_size_limit(10**9)
def unesc(s): return s.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')

arts = collections.OrderedDict()   # name -> {comp, file, fields{}}
for comp in ['tome', 'orcs', 'cults', 'ashes-urhrok']:
    for line in open(f'/tmp/artchk/{comp}.tsv', encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if len(p) < 5: continue
        _, f, field, name, text = p
        name, text = unesc(name), unesc(text)
        a = arts.setdefault(name, {'comp': comp, 'file': f.replace('/tmp/artchk/src/', '').replace('/workspace/tome4-dlcs/', 'dlc:'), 'fields': {}})
        a['fields'].setdefault(field, text)

tr = collections.defaultdict(list)  # src -> [(dst, tag, file)]
for line in open('/tmp/artchk/tr.tsv', encoding='utf-8'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 4: continue
    tr[unesc(p[0])].append((unesc(p[1]), p[2], p[3]))

def names_of(n):
    return sorted({d for d, tag, f in tr.get(n, []) if tag == 'entity name'})

out = {'name_missing': [], 'name_variants': [], 'desc_missing': [], 'desc_mention': [], 'other_mention': []}
canon = {}
for n, a in arts.items():
    v = names_of(n)
    if not v:
        anyv = sorted({d for d, tag, f in tr.get(n, [])})
        out['name_missing'].append({'name': n, 'file': a['file'], 'other_tag_targets': anyv})
    elif len(v) > 1:
        out['name_variants'].append({'name': n, 'file': a['file'], 'targets': [(d, tag, f) for d, tag, f in tr[n] if tag == 'entity name']})
    canon[n] = v or sorted({d for d, tag, f in tr.get(n, [])})

# mention patterns: full name and name without leading article
def variants(n):
    vs = {n}
    m = re.match(r'^(the|The|a|A|an|An)\s+(.*)$', n)
    if m: vs.add(m.group(2))
    return [x for x in vs if len(x) >= 4]
pat = {}
for n in arts:
    if not canon.get(n) or not variants(n): continue
    pat[n] = re.compile(r'(?<![A-Za-z\'])(' + '|'.join(re.escape(x) for x in variants(n)) + r')(?![A-Za-z])')

def tnames(n):
    s = set()
    for t in canon[n]:
        s.add(t)
        s.add(re.sub(r'^#[A-Z_]+#|#LAST#$', '', t))
    return s

for n, a in arts.items():
    d = a['fields'].get('desc')
    if not d: continue
    tds = sorted({x for x, tag, f in tr.get(d, [])})
    if not tds:
        out['desc_missing'].append({'name': n, 'file': a['file'], 'desc': d[:200]})
        continue
    for m, p in pat.items():
        if p.search(d):
            want = tnames(m)
            for td in tds:
                if not any(w and w in td for w in want):
                    out['desc_mention'].append({'artifact': n, 'artifact_zh': canon.get(n), 'mentions': m, 'mentions_zh': sorted(want), 'file': a['file'], 'desc_en': d, 'desc_zh': td, 'self': m == n})

# other library entries mentioning multi-word artifact names
artdesc = {a['fields'].get('desc') for a in arts.values()}
for m, p in pat.items():
    if len(m.split()) < 2: continue
    want = tnames(m)
    for src, lst in tr.items():
        if src == m or src in artdesc: continue
        if not p.search(src): continue
        for d, tag, f in lst:
            if tag == 'entity name': continue
            if not any(w and w in d for w in want):
                out['other_mention'].append({'mentions': m, 'mentions_zh': sorted(want), 'tag': tag, 'file': f, 'src': src[:400], 'dst': d[:400]})

json.dump(out, open('/tmp/artchk/result.json', 'w'), ensure_ascii=False, indent=1)
print('artifacts', len(arts), {k: len(v) for k, v in out.items()})
