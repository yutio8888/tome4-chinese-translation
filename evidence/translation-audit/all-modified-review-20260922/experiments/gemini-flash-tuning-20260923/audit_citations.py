"""Mechanical quotation/location checks; semantic warrant is adjudicated separately."""
import json,pathlib,re
p=pathlib.Path(__file__).parent
out=[]
for mapping in sorted((p/'normalized').glob('*-mapped.json')):
 run=mapping.name.removesuffix('-mapped.json');phase=run.split('-')[0];text=(p/f'reports/{run}.md').read_text();d=json.loads(text.split('```json')[1].split('```')[0]);terms=json.loads((p/f'{phase}/terms.json').read_text());rows=terms if isinstance(terms,list) else terms.get('terms',[])
 for i,c in enumerate(d['claims'],1):
  for ev in c['evidence']:
   path=ev['path'];q=ev['quote'];line=ev.get('line');f=pathlib.Path(path)
   if not f.is_absolute():f=p/f
   result=dict(run=run,claim=c.get('id',f'position-{i}'),path=path,line=line,literal_in_file=False,line_accurate=False,term_origin_supported=False)
   if f.exists() and (p.resolve() in f.resolve().parents):
    t=f.read_text();result['literal_in_file']=q in t
    if isinstance(line,int):result['line_accurate']=q in '\n'.join(t.splitlines()[max(0,line-1):line+max(1,len(q.splitlines()))])
   # Citing original term provenance is permitted only if represented in frozen rows.
   if path.startswith('terminology/'):
    candidates=[r for r in rows if r.get('file')==path and r.get('line')==line]
    result['term_origin_supported']=any(r['source'] in q and r['target'] in q and all(str(r.get(k,'')) in q for k in ['status','scope']) for r in candidates)
   result['retrievable']=result['literal_in_file'] or result['term_origin_supported'];out.append(result)
(p/'CITATION-CHECKS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for run in sorted({r['run'] for r in out}):
 rs=[r for r in out if r['run']==run];print(run,len(rs),sum(r['retrievable'] for r in rs),sum(r['line_accurate'] or r['term_origin_supported'] for r in rs))
