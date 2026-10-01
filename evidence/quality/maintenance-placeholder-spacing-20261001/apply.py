#!/usr/bin/env python3
"""Talent-description placeholder spacing sweep (2026-10-01, user rule "minimal necessary").

Level-up preview tokenizes t.info() with tokenize(" ()[],") (tome Actor.lua:6851) and diffs token by
token (engine utils.lua:1969); a placeholder whose token also holds CJK text highlights the whole run.
Scope: records in */talents/* sections with source_tag tformat, across the 11 sweep components.
Guards mirror tools/orchestration/sweep.py and add: only planned ASCII spaces may be inserted;
records outside the plan must be byte-identical after reparse. Usage: apply.py plan|apply
"""
import json,sys,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'tools/orchestration'));sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import _orch
from i18nlib.config import load_manifest
from i18nlib.locale_model import LocaleLoader
from i18nlib.runtime import LuaRuntime
from ph_rule import plan
import re
COMPONENTS=['engine.lua','mod-boot.lua','mod-tome.lua','tome-ashes-urhrok.lua','tome-cults.lua','tome-orcs.lua','mod-example.lua','mod-example_realtime.lua','tome-addon-dev.lua','tome-items-vault.lua','tome-possessors.lua']
_CONV=r'%[-+#0]*[0-9]*(?:\.[0-9]+)?[diouxXeEfFgGcsq]'
SPEC_RE=re.compile(rf'(?:{_CONV}%%)|(?:{_CONV})|%%');MARKER_RE=re.compile(r'#\{[a-z]+\}#|#[A-Z_]+#')
def shape(s):
    lead=len(s)-len(s.lstrip());trail=len(s)-len(s.rstrip())
    return (s[:lead],s[len(s)-trail:] if trail else '',tuple(m.group(0) for m in SPEC_RE.finditer(s)),tuple(m.group(0) for m in MARKER_RE.finditer(s)))
def in_scope(r): return '/talents/' in (r.get('section') or '') and r.get('source_tag')=='tformat'
def quote(t,nl='\\n'): return '"'+t.replace('\\','\\\\').replace('"','\\"').replace('\n',nl).replace('\t','\\t').replace('\r','\\r')+'"'
def literals(t):
    yield quote(t); yield quote(t,'\\\n')
    for eq in range(0,4):
        o='['+'='*eq+'[';c=']'+'='*eq+']'
        if c not in t: yield o+t+c; yield o+'\n'+t+c
def insert(t,ins): return ''.join(((' ' if k in ins else '')+ch) for k,ch in enumerate(t))
mode=sys.argv[1];assert mode in ('plan','apply')
loader=LocaleLoader(LuaRuntime(load_manifest()))
problems=[];pending=[];report=[];total=0;inserts=0
for name in COMPONENTS:
    p=ROOT/name
    if not p.is_file(): problems.append(f'{name}: missing');continue
    raw=p.read_bytes();text=raw.decode('utf-8');lines=text.split('\n')
    before=loader.load_bytes(raw,logical_path=name).records
    want={};new_text=text
    # line-anchored literal replacement, applied bottom-up so earlier offsets stay valid
    starts=[0]
    for l in lines[:-1]: starts.append(starts[-1]+len(l)+1)
    edits=[]
    for i,r in enumerate(before):
        if not in_scope(r): continue
        ins=plan(r['target'])
        if not ins: continue
        new=insert(r['target'],ins);want[i]=(new,len(ins))
        lo=starts[r['line']-1];hi=text.find('\nt(',lo+1);hi=len(text) if hi<0 else hi
        seg=text[lo:hi];hit=None
        for lit in literals(r['target']):
            k=seg.find(lit)
            if k>=0 and seg.find(lit,k+1)<0 and (hit is None): hit=(lit,k)
        if hit is None: problems.append(f'{name}:{r["line"]}: target literal not located');continue
        lit,k=hit;newlit=lit.replace(r['target'],new,1) if lit.startswith('[') else (quote(new) if lit==quote(r['target']) else quote(new,'\\\n'))
        assert newlit!=lit
        edits.append((lo+k,lo+k+len(lit),newlit))
    for a,b,nl in sorted(edits,reverse=True): new_text=new_text[:a]+nl+new_text[b:]
    if not want: print(f'{name:26} 无匹配');continue
    after=loader.load_bytes(new_text.encode('utf-8'),logical_path=name).records
    if len(after)!=len(before): problems.append(f'{name}: record count {len(before)}->{len(after)}');continue
    changed=0
    for i,(b,a) in enumerate(zip(before,after)):
        for key in ('source','source_tag','args_order','special','section','function_name','kind'):
            if b.get(key)!=a.get(key): problems.append(f'{name}#{i}: {key} changed')
        if i in want:
            new,k=want[i]
            if a['target']!=new: problems.append(f'{name}#{i}: target != planned')
            if a['target'].replace(' ','')!=b['target'].replace(' ','') or len(a['target'])-len(b['target'])!=k: problems.append(f'{name}#{i}: more than planned spaces')
            if shape(a['target'])!=shape(b['target']): problems.append(f'{name}#{i}: shape changed')
            if plan(a['target']) and in_scope(a): problems.append(f'{name}#{i}: residual after fix')
            changed+=1;inserts+=k
            report.append(dict(component=name,line=b['line'],section=b['section'],source=b['source'],source_tag=b['source_tag'],target_before=b['target'],target_after=a['target'],inserted_spaces=k))
        elif a.get('target')!=b.get('target'): problems.append(f'{name}#{i}: unplanned target change')
    total+=changed;print(f'{name:26} 改 {changed:4d} 条，插入 {sum(want[i][1] for i in want)} 个空格')
    pending.append((p,new_text,hashlib.sha256(raw).hexdigest()))
# cross-component / out-of-scope runtime keys sharing a changed source
keys={(x['source'],x['source_tag']) for x in report};others=[]
for name in COMPONENTS:
    if not (ROOT/name).is_file(): continue
    for r in loader.load_path(ROOT/name,logical_path=name).records:
        if (r.get('source'),r.get('source_tag')) in keys and not in_scope(r): others.append((name,r['line'],r['section']))
print(f'\n合计 {total} 条，{inserts} 个空格；与改动条目同 runtime key 但不在范围内的记录 {len(others)} 条')
for o in others[:10]: print('  ',o)
if problems:
    print(f'\n❌ {len(problems)} 项校验未过，不写任何文件：');[print('  ',m) for m in problems[:30]];sys.exit(1)
out=pathlib.Path(__file__).resolve().parent
(out/f'{mode}-report.json').write_text(json.dumps(dict(rule='minimal-necessary',scope='*/talents/* sections, source_tag tformat, 11 components',records=total,inserted_spaces=inserts,out_of_scope_same_key=others,entries=report),ensure_ascii=False,indent=1)+'\n')
if mode=='plan': print('✅ 全部校验通过（plan，未写盘）');sys.exit(0)
for p,nt,sha in pending:
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,p
    _orch.write_atomic(p,nt)
print(f'✅ 已写入 {len(pending)} 个文件')
