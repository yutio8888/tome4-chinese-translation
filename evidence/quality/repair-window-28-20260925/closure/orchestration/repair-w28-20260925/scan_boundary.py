import json,re,sys
from pathlib import Path
# scan_boundary.py <did>: list write-like and out-of-scope access patterns in a reviewer's native tool calls.
# /tmp scratch writes are allowed since the 2026-09-25 user authorization (USER-AUTH-TMP-WRITES.json).
P=Path(__file__).parent;did=sys.argv[1]
d=json.loads((P/f'{did}-native-tools.json').read_text());writes=[];tmp=[];paths=set()
for c in d['tool_calls']:
    s=json.dumps(c.get('input',c.get('arguments','')),ensure_ascii=False)
    for x in re.findall(r'open\([^)]{0,80}[\x27"]w[\x27"]|[^=]> *[/.\w-]+|\btee |Begin Patch|\brm |\bmv |\bcp |"file_path"',s):
        (tmp if '/tmp/' in s and ('/tmp' in x or 'open(' in x) else writes).append(x)
    paths|=set(re.findall(r'/workspace/[\w.-]+(?:/[\w.-]+)?',s))
    if re.search(r'\bls /workspace\b(?!/)|find /workspace\b(?!/tome4-dlcs/ashes-urhrok)|find / ',s): writes.append('workspace-enumeration')
w=[x for x in writes if 'file_path' not in x and '/dev/null' not in x and not x.endswith('>text')]
print(json.dumps(dict(dispatch_id=did,calls=len(d['tool_calls']),non_tmp_write_or_scan=w,tmp_writes=tmp,paths=sorted(paths)),ensure_ascii=False))
