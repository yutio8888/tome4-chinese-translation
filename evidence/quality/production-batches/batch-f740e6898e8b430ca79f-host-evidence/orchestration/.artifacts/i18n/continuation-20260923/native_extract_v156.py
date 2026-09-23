"""Host extraction for Codex 0.156.0 / Claude 2.1.280 native logs.
Runs the repository's exact _parse_native_final from a temp copy where ONLY the pinned
version literals are substituted; repo tools stay unmodified. Writes raw bytes + proof."""
import sys, json, hashlib, importlib.util, pathlib, tempfile, shutil
R = pathlib.Path.cwd()
children, key, native_log, out = sys.argv[1:5]
src = (R/'tools/orchestration/review_lifecycle.py').read_text()
assert src.count("version = '0.153.0'") == 1 and src.count("version = '2.1.259'") == 1
patched = src.replace("version = '0.153.0'", "version = '0.156.0'").replace("version = '2.1.259'", "version = '2.1.280'")
tmp = pathlib.Path(tempfile.mkdtemp())
shutil.copytree(R/'tools', tmp/'tools', ignore=shutil.ignore_patterns('__pycache__'))
(tmp/'tools/orchestration/review_lifecycle.py').write_text(patched)
sys.path.insert(0, str(tmp/'tools/orchestration')); sys.path.insert(0, str(tmp/'tools'))
spec = importlib.util.spec_from_file_location('rl_v156', tmp/'tools/orchestration/review_lifecycle.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = json.load(open(children)); row, = [r for r in rows if r['task_id']+'|'+r['dispatch_id'] == key]
s = row['first_live_capture']['snapshot']
provider = s['provider']; session = s['persistence']['sessionId'] if s.get('persistence', {}).get('sessionId') else None
if session is None:
    session = json.load(open(sys.argv[5]))['snapshot']['persistence']['sessionId']
prompt = row['create_parameters']['prompt']
assert hashlib.sha256(prompt.encode()).hexdigest() == row['create_prompt_sha256']
data = pathlib.Path(native_log).read_bytes()
raw, proof = m._parse_native_final(data, provider=provider, session_id=session, cwd=row['cwd'], prompt=prompt, natural_success=True)
o = pathlib.Path(out); o.parent.mkdir(parents=True, exist_ok=True); assert not o.exists()
o.write_bytes(raw)
proof.update(key=key, agent_id=row['agent_id'], native_log=str(native_log), native_log_sha256=hashlib.sha256(data).hexdigest(),
             raw_sha256=hashlib.sha256(raw).hexdigest(), parser='repo _parse_native_final with version literal substitution only',
             substitution={'0.153.0': '0.156.0', '2.1.259': '2.1.280'}, repo_parser_sha256=hashlib.sha256(src.encode()).hexdigest())
pathlib.Path(str(o)+'.proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
shutil.rmtree(tmp); print(json.dumps(proof, ensure_ascii=False))
