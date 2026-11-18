import json,re,sys
sys.path.insert(0,'tools'); import lite_review as LR
B='evidence/lite-review/batches/0521/'
E=json.load(open(B+'input.json'))['entries']
C=re.compile(r'rng\.percent|rng\.chance|checkHit|canBe\(|Save\(|removeEffect|removeEffectsFilter|cleanse|_immune|\.dur\b|alterEffectDuration|setEffect\(|callbackOn\w+|on_timeout|on_die|on_lose|on_gain|project\(|addEffect\(|^\s*if\b|\belseif\b|knowTalent|getTalentLevel')
def block(L,ln):
    s=ln-1
    while s>0 and not re.match(r'\s*(newTalent|newEffect|uberTalent)\s*\{',L[s]): s-=1
    e=ln
    while e<len(L) and not re.match(r'\s*(newTalent|newEffect|uberTalent)\s*\{',L[e]): e+=1
    return s,e
ctx={}
for x in E:
    text,loc=LR.source_text(x['section']); L=text.splitlines()
    ln=x['source_lines'][0]; s,e=block(L,ln)
    # format call: first tformat/format( at or after the string's last line within block
    fmt=None
    for i in range(ln-1,min(e,ln+60)):
        m=re.search(r'\)\s*:\s*t?format\((.*)$',L[i]) or re.search(r'\btformat\((.*)$',L[i])
        if m: fmt=f'{i+1}: '+L[i].strip()[:400]; break
    lines=[f'{i+1}: '+L[i].strip()[:200] for i in range(s,e) if C.search(L[i])][:40]
    ctx[x['id']]={'definition_lines':[s+1,e],'string_line':ln,'format_call':fmt,'args_order':x['args_order'],
                 'code_conditions_and_callbacks':lines}
json.dump({'note':'Code facts extracted from the same source files as input.json (core @624a67329fe2; DLC public checkout, fingerprints in source-provenance.json). No review history or expected verdicts.','entries':ctx},open(B+'context.json','w'),ensure_ascii=False,indent=1)
print(len(ctx),sum(1 for v in ctx.values() if v['format_call']))
