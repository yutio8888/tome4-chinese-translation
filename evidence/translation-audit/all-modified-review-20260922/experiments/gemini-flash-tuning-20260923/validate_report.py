"""Validate output structurally; do not mistake valid JSON for a correct audit."""
import json,re,sys
from pathlib import Path

def validate(text, expected):
    blocks=re.findall(r'```(?:json)?\s*\n(.*?)```',text,re.S)
    candidates=blocks or [text]
    objects=[]
    for c in candidates:
        try: objects.append(json.loads(c))
        except (ValueError,TypeError): pass
    if len(objects)!=1: return None,['Expected one parseable JSON object']
    d=objects[0];errors=[]
    if not isinstance(d,dict):return d,['Top level must be object']
    if any(k not in d for k in ['entries','claims','read_files','limitations']):errors.append('Missing top-level fields')
    es=d.get('entries',[]);cs=d.get('claims',[])
    if [e.get('id') for e in es]!=expected:errors.append('Entry coverage/order mismatch')
    ids=[c.get('id') for c in cs]
    if len(set(ids))!=len(ids) or any(not x for x in ids):errors.append('Duplicate/missing claim IDs')
    for c in cs:
        required=['id','entry','status','source_quote','target_quote','change','context_counter','evidence','text_status','snapshot_fact','target_applicability','impact']
        if any(k not in c for k in required):errors.append(f"{c.get('id')}: missing field")
        if c.get('entry') not in expected or c.get('status') not in ['confirmed','pending','advisory']:errors.append(f"{c.get('id')}: invalid entry/status")
        if c.get('impact') not in ['mechanism','narrative','expression']:errors.append(f"{c.get('id')}: invalid impact")
    for e in es:
        actual=[c for c in cs if c.get('entry')==e.get('id')]
        expected_status='ISSUE' if any(c.get('status')=='confirmed' for c in actual) else 'PENDING' if any(c.get('status')=='pending' for c in actual) else 'OK'
        if e.get('status')!=expected_status:errors.append(f"{e.get('id')}: status inconsistency")
        if set(e.get('claim_ids',[]))!={c.get('id') for c in actual}:errors.append(f"{e.get('id')}: claim mapping inconsistency")
    return d,errors

if __name__=='__main__':
    text=Path(sys.argv[1]).read_text();entries=json.loads(Path(sys.argv[2]).read_text())
    data,errors=validate(text,[e['audit_id'] for e in entries]);print(json.dumps(dict(valid=not errors,errors=errors,entries=len(data.get('entries',[])) if isinstance(data,dict) else 0,claims=len(data.get('claims',[])) if isinstance(data,dict) else 0),ensure_ascii=False,indent=2))
