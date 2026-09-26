import datetime
import hashlib
import json
import pathlib
import re
import subprocess

batch = 'batch-fddb88b07b599a5e41c8'
scratch = pathlib.Path('.artifacts/i18n/continuation-20260923')
host = pathlib.Path('evidence/quality/production-batches') / f'{batch}-host-evidence'
paths = [f'evidence/production-review-v2-lite/batches/{batch}', str(host),
         f'evidence/quality/production-batches/{batch}-source-workset.json',
         'evidence/quality/pending-user-review.md', 'handoff.md']
prior = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
assert all(any(path == allowed or path.startswith(allowed + '/') for allowed in paths)
           for path in prior), prior
subprocess.run(['git', 'add', '-f', '--', *paths], check=True)
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
assert staged and all(any(path == allowed or path.startswith(allowed + '/') for allowed in paths)
                      for path in staged), staged
manifest = {item['path']: item for item in json.loads((host / 'snapshot-inventory.json').read_text())['files']}
for item in manifest.values():
    target = str(host / 'orchestration' / item['path'])
    assert target in staged
    assert hashlib.sha256(subprocess.check_output(['git', 'show', ':' + target])).hexdigest() == item['sha256']
result = subprocess.run(['git', 'diff', '--cached', '--check'], capture_output=True, text=True)
(scratch / 'review298-staged-whitespace.txt').write_text(result.stdout + result.stderr)
exceptions = []
for line in result.stdout.splitlines():
    match = re.match(r'(.+?):(\d+): (trailing whitespace\.|new blank line at EOF\.)$', line)
    if not match:
        continue
    path, line_number, reason = match.groups()
    prefix = str(host / 'orchestration') + '/'
    assert path.startswith(prefix), line
    original = path[len(prefix):]
    assert original in manifest
    data = subprocess.check_output(['git', 'show', ':' + path])
    sha = hashlib.sha256(data).hexdigest()
    assert sha == manifest[original]['sha256'] == hashlib.sha256(pathlib.Path(original).read_bytes()).hexdigest()
    exceptions.append(dict(path=path, line=int(line_number), reason=reason, original=original,
                           sha256=sha, disposition='preserve exact archived evidence bytes'))
if result.returncode:
    assert exceptions and len([line for line in result.stdout.splitlines()
                               if re.match(r'.+:\d+: ', line)]) == len(exceptions)
(scratch / 'review298-staging-verification.json').write_text(json.dumps(dict(
    verified=True, verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    staged_files=staged, raw_whitespace_exit_code=result.returncode,
    immutable_artifact_exceptions=exceptions, remaining_staged_whitespace_issues=0),
    ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(staged_files=len(staged), raw_whitespace_exit_code=result.returncode,
                      archival_exception_count=len(exceptions)), ensure_ascii=False))
