import re, json, collections
exec(open('/tmp/artchk/analyze.py').read().split("out = {")[0])  # reuse arts, tr, unesc, names_of

# proper-noun dictionary: capitalized words / phrases that never occur lowercase in any source string
lower_words = collections.Counter()
for src in tr:
    for w in re.findall(r"\b[a-z][a-z']+\b", src):
        lower_words[w] += 1
dict_ = {}
for src, lst in tr.items():
    if not re.fullmatch(r"[A-Z][a-z]+(?:[-'][A-Za-z]+)?", src): continue
    if len(src) < 4 or lower_words[src.lower()] > 0: continue
    ts = {d for d, tag, f in lst if re.search(r'[一-鿿]', d) and len(d) <= 12}
    if ts: dict_[src] = ts
STOP = set()
print('dict size', len(dict_))

res = []
for n, a in arts.items():
    zn = names_of(n) or sorted({d for d, tag, f in tr.get(n, [])})
    d = a['fields'].get('desc') or ''
    zd = sorted({x for x, tag, f in tr.get(d, [])}) if d else []
    for field, en, zhs in (('name', n, zn), ('desc', d, zd)):
        if not en or not zhs: continue
        for w in set(re.findall(r"[A-Z][a-z]+(?:[-'][A-Za-z]+)?", en)):
            if w not in dict_: continue
            # possessive "Garkul's" counted via base word
            for zh in zhs:
                if not any(t in zh for t in dict_[w]):
                    res.append({'artifact': n, 'zh_name': zn, 'field': field, 'noun': w, 'dict': sorted(dict_[w]), 'en': en[:500], 'zh': zh[:500], 'file': a['file']})
json.dump(res, open('/tmp/artchk/propn.json', 'w'), ensure_ascii=False, indent=1)
print(len(res))
