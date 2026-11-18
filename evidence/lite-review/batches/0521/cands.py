import json,re,sys,subprocess,collections
sys.path.insert(0,'/workspace/tome4-chinese-translation/tools')
R='/workspace/tome4-chinese-translation/'
import lite_review as LR
U=json.load(open('/tmp/r4/units.json'))   # current_units at b46edd0f8; targets refreshed below from HEAD units
live=[u for u in U if u['disposition']=='release-required']
dead=set((p['dead']['file'],p['dead']['en'],p['dead']['tag']) for p in json.load(open(R+'evidence/quality/dead-key-scan-20261111/pairs.json')))
recent=set(); recent_secs=set()
for b in range(480,521):
    try:
        for e in json.load(open(R+f'evidence/lite-review/batches/{b:04d}/input.json'))['entries']:
            recent.add(e['unit_id'])
            if b>=511: recent_secs.add(e['section'])
    except FileNotFoundError: pass
SEC=re.compile(r'^(mod-tome/data/(talents/(techniques|cunning|cursed)/|timed_effects/)|tome-(cults|orcs|ashes-urhrok)/data/(talents|timed_effects))')
EN={'C1':r'\bchance\b|\bif (it|the|this|you|they|target)\b.*\b(hit|succeed|fail|resist|save)|\bon (a )?(hit|crit)|whenever .* (hit|crit)|\bresist',
    'C2':r'\b(remove|removes|removing|cleanse|cleanses|cure|cures|purge|neutraliz|clear|immun|prevent)',
    'C3':r'\b(duration|extend|prolong|increas\w* .* by \d? ?turns?|turns? longer|lasts?|\+%d turns)',
    'C4':r'\b(when|whenever|each time|after|upon|at the end|expires?|on death|dies|where|lands?|at the target|around (the|it|them))\b'}
CODE={'C1':r'rng\.percent|checkHit|canBe\(|checkEvasion|combat\w*Save|rng\.chance',
      'C2':r'removeEffect|removeEffectsFilter|cleanse|cureEffect|_immune|canBe\(',
      'C3':r'eff\.dur\s*=|\.dur\s*=\s*.*\+|alterEffectDuration|setEffect\([^)]*dur',
      'C4':r'callbackOn\w+|on_timeout|on_die|on_lose|doDig|project\(|addEffect\('}
def block(text,lineno):
    L=text.splitlines(); s=lineno-1
    while s>0 and not re.match(r'\s*(newTalent|newEffect|uberTalent)\s*\{',L[s]): s-=1
    e=lineno
    while e<len(L) and not re.match(r'\s*(newTalent|newEffect|uberTalent)\s*\{',L[e]): e+=1
    return '\n'.join(L[s:e]),s+1,e
rows=[];stat=collections.Counter()
for u in live:
    o=u['occurrence']
    if not SEC.match(o['section']) or o['source_tag'] not in ('tformat','_t'): continue
    stat['in_sections']+=1
    if (o['translation_path'],o['source'],str(o['source_tag'])) in dead: stat['dead']+=1; continue
    if u['unit_id'] in recent: stat['recent']+=1; continue
    src=o['source']; hitsEN=[k for k,p in EN.items() if re.search(p,src,re.I)]
    if not hitsEN or len(src)<50: continue
    stat['en_hit']+=1
    text,loc=LR.source_text(o['section']);
    if text is None: stat['no_source']+=1; continue
    ln=LR.locate(text,src)
    if not ln: stat['unlocated']+=1; continue
    blk,b0,b1=block(text,ln[0])
    cats=[k for k in hitsEN if re.search(CODE[k],blk)]
    if not cats: continue
    stat['effective']+=1
    rows.append(dict(uid=u['unit_id'],comp=o['component'],section=o['section'],cats=cats,line=ln[0],block=[b0,b1],same_recent_section=o['section'] in recent_secs,loc=loc))
print(dict(stat)); print(collections.Counter(r['comp'] for r in rows)); print(collections.Counter(c for r in rows for c in r['cats']))
print('in recent sections',sum(r['same_recent_section'] for r in rows))
json.dump(rows,open('/tmp/r5/candidates.json','w'),ensure_ascii=False,indent=0)
