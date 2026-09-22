import json,subprocess,hashlib,sys
from pathlib import Path
D=Path('.ai/task/review-input-policy-20260922')
s=json.loads((D/'STATE.json').read_text());phase=sys.argv[1];cycle=s['cycle'];allowed=json.loads((D/'SCOPE.json').read_text())['allowed_files'];base=s['baseline']['commit'];chunks=[];paths=[];hashes={}
assert all(c['archive_confirmed'] for c in s['child_dispatches'])
author=s['executor']['agent_id'];assert any(c['agent_id']==author and c.get('output_valid') is True for c in s['child_dispatches'])
for f in sorted(allowed):
 tracked=subprocess.run(['git','ls-files','--error-unmatch','--',f],capture_output=True).returncode==0
 if tracked:r=subprocess.run(['git','diff','--no-ext-diff','--binary',base,'--',f],capture_output=True);assert r.returncode==0
 elif Path(f).is_file():r=subprocess.run(['git','diff','--no-index','--no-ext-diff','--binary','--','/dev/null',f],capture_output=True);assert r.returncode in (0,1)
 else:continue
 if not r.stdout:continue
 chunks.append(r.stdout);paths.append(f);hashes[f]=hashlib.sha256(Path(f).read_bytes()).hexdigest()
assert paths
raw=b''.join(chunks);diff=D/f'CODE_DIFF-{phase}-{cycle}.patch';assert not diff.exists();diff.write_bytes(raw)
spec=Path(s.get('active_spec_path',str(D/'SPEC.md')));ci=hashlib.sha256(spec.read_bytes()+b'\0'+raw).hexdigest();locator=dict(spec_path=str(spec),diff_path=str(diff));recipe='sorted allowed paths; git diff --no-ext-diff --binary BASE -- PATH; untracked git diff --no-index --no-ext-diff --binary -- /dev/null PATH; concatenate exact bytes'
s.update(state=phase,review_phase=phase,candidate_author_agent_id=author,candidate_ref=ci,candidate_locator=locator,frozen_paths=paths,frozen_hashes=hashes,diff_recipe=recipe)
(D/f'CANDIDATE-{phase}-{cycle}.json').write_text(json.dumps(dict(candidate_ref=ci,candidate_locator=locator,paths=paths,hashes=hashes,base_commit=base,diff_recipe=recipe),indent=2)+'\n')
(D/'STATE.json').write_text(json.dumps(s,indent=2)+'\n');print(ci,len(paths))
