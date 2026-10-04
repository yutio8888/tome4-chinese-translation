import os
from pathlib import Path
def native_log(provider, session, cwd):
    if provider == 'claude':
        return Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home()/'.claude')))/'projects'/cwd.replace('/', '-')/(session+'.jsonl')
    if provider == 'codex':
        root = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))
        paths = list(root.glob(f'sessions/*/*/*/*{session}.jsonl')) + list(root.glob(f'archived_sessions/*{session}.jsonl'))
        assert len(paths) == 1, paths
        return paths[0]
    raise ValueError(provider)
