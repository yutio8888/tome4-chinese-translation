import json,re,collections,sys
sys.path.insert(0,'/workspace/tome4-chinese-translation/tools')
from i18nlib.lint import placeholder_spacing_offsets
E=json.load(open('/tmp/ft/live.json'))
cat=collections.Counter(); ex=collections.defaultdict(list)
for e in E:
    t=e['target']
    for m in re.finditer(r'：[ ]',t):
        i=m.end(); rest=t[i:]
        if rest=='' : k='end-of-string'
        elif re.match(r'%',rest): k='before-placeholder'
        elif re.match(r'#[A-Za-z_]+#|#\{',rest): k='before-colorcode'
        elif re.match(r'[\n]',rest): k='before-newline'
        elif re.match(r'[0-9+\-]',rest): k='before-number'
        else: k='before-text'
        req = ('/talents/' in e['section'] and e['tag']=='tformat' and (i-1) in placeholder_spacing_offsets(t[:i-1]+t[i:]))
        if req: k+='(lint-required)'
        cat[k]+=1; ex[k].append(e)
print(cat)
for k in ['end-of-string','before-text']:
    for e in ex[k][:60]:
        print(k,'|',e['file'],e['line'],e['tag'],'|',repr(e['source'][:50]),'|',repr(e['target'][:60]))
json.dump({k:[(e['file'],e['line'],e['tag'],e['source'],e['target']) for e in v] for k,v in ex.items()},open('/tmp/ft/p3-colon.json','w'),ensure_ascii=False)
