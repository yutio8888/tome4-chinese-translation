import json,pathlib,runpy,datetime,statistics
p=pathlib.Path(__file__).parent;score=runpy.run_path(str(p/'score.py'))['score']
names={'F00':['dev-F00-r1-retry1','dev-F00-r2'],'F10':['dev-F10-r1','dev-F10-r2-retry2'],'F01':['dev-F01-r1','dev-F01-r2'],'F11':['dev-F11-r1','dev-F11-r2']}
results={}
for arm,runs in names.items():
 metrics=[]
 for run in runs:
  d=json.loads((p/f'normalized/{run}-mapped.json').read_text());x=score(d['reference'],d['mappings'],d['meta']);x['run']=run;metrics.append(x)
 results[arm]={'runs':metrics,'both_raw_valid':all(x['valid'] for x in metrics)}
 for key in ['macro','micro','false_positive','mechanism_missed','seconds']:
  results[arm][key]=round(statistics.mean(x[key] for x in metrics),12)
 results[arm]['cost']=statistics.mean(x['cost'] for x in metrics) if all(x['cost'] is not None for x in metrics) else None
b=results['F00'];eligible=[]
for a,x in results.items():
 if a=='F00':continue
 x['quality_eligible']=x['both_raw_valid'] and x['false_positive']<=b['false_positive'] and x['macro']>=b['macro']-.05 and x['mechanism_missed']<=b['mechanism_missed']
 x['strict_improvement']=any(x[k]<b[k] for k in ['false_positive','mechanism_missed','seconds']) or x['macro']>b['macro']
 if x['quality_eligible'] and x['strict_improvement']:eligible.append(a)
def resource(a):return results[a]['cost'] if results[a]['cost'] is not None else results[a]['seconds']
selected=min(eligible,key=lambda a:(-results[a]['macro'],results[a]['false_positive'],resource(a),a)) if eligible else min((a for a in results if a!='F00'),key=lambda a:(results[a]['false_positive'],-results[a]['macro'],results[a]['seconds'],a))
out=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),selected=selected,diagnostic_only=not bool(eligible),results=results,holdout_order=[['F00',1],[selected,1],[selected,2],['F00',2]],limitations=['Reference is provisional host judgment, not human gold.','One baseline raw-schema failure scored semantically using documented derived IDs; strict format failure retained.','Some development runs overlapped before serial amendment; timing is observational, not controlled concurrency evidence.','No measured fees/tokens available; no cost winner claim.'])
(p/'SELECTION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
