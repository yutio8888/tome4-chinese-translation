import json,pathlib,runpy,datetime
p=pathlib.Path(__file__).parent
score=runpy.run_path(str(p/'score.py'))['score'];reference=json.loads((p/'HOST-DEV-REFERENCE.json').read_text())['claims']
# Host mappings based on concrete meaning, not wording or model consensus.
mapsets={
 'dev-F01-r1':{'C01':['H06'],'C02':['H04'],'C03':['N43'],'C04':['H38'],'C05':['H01','H02'],'C06':['N05'],'C07':['H28'],'C08':['H40']},
 'dev-F11-r1':{'C01':['H06'],'C02':['H04'],'C03':['N43'],'C04':['H38'],'C05':['H02'],'C06':['N05'],'C07':['H28'],'C08':['H40'],'C09':['H43']},
 'dev-F10-r1':{'C01':['H06'],'C02':['H04'],'C03':['N43'],'C04':['H38'],'C05':['H02'],'C06':['N05'],'C07':['H40']},
}
for dispatch,match in mapsets.items():
 d=json.loads((p/f'reports/{dispatch}.md').read_text().split('```json')[1].split('```')[0]);raw=json.loads((p/f'raw/{dispatch}.json').read_text());ss=raw['status']['structuredContent']['snapshot'];mappings=[]
 for c in d['claims']:
  rr=match[c['id']];mappings.append(dict(claim_id=c['id'],atom_id=rr[0],reference_ids=rr,verdict='unresolved' if rr==['N43'] else 'supported',model_status=c['status'],reason='N43 source implementation missing and current-body context admits alternative reading.' if rr==['N43'] else 'Matches explicit semantic defect in frozen host reference.'))
  if c['id']=='C05':mappings.append(dict(claim_id='C05',atom_id='N76',reference_ids=['N76'],verdict='unsupported',model_status='confirmed',reason='Separate at-will omission assertion: acquired summoning ability permits active-use interpretation; duration omission remains supported.'))
 # Goal-to-max present in quote alone does not establish that model claimed its omission.
 seconds=(datetime.datetime.fromisoformat(ss['attentionTimestamp'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(ss['createdAt'].replace('Z','+00:00'))).total_seconds()
 data=dict(reference=reference,mappings=mappings,meta=dict(valid=True,seconds=seconds,cost=None,evidence_checks=[]),host_blinding='Notifications exposed arm IDs and outputs; mappings use frozen criteria but host adjudication is not fully blinded.',selection_status='Do not select until all eight valid development runs collected and provenance checks complete.')
 (p/f'normalized/{dispatch}-mapped.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(dispatch,score(reference,mappings,data['meta']))
