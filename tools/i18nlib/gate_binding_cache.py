"""Disposable stat-keyed content hashes; failures only discard acceleration."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


def strict_json(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key] = value
        return out
    def invalid(value):
        raise ValueError('non-finite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def fingerprint(path):
    s = path.lstat()
    return [s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_ino, s.st_dev, s.st_mode]


class BindingCache:
    def __init__(self, root):
        self.path = Path(root) / '.artifacts/i18n/gate-binding-cache.json'
        self.entries = {}
        self.updated = {}
        try:
            data = strict_json(self.path.read_bytes())
            if type(data) is not dict or set(data) != {'version', 'entries', 'entries_sha256'} or type(data['version']) is not int or data['version'] != 1:
                raise ValueError('cache schema')
            if hashlib.sha256(json.dumps(data['entries'], sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest() != data['entries_sha256']:
                raise ValueError('cache checksum')
            for name, item in data['entries'].items():
                if (not isinstance(name, str) or not isinstance(item, list) or len(item) != 2
                        or not isinstance(item[0], list) or len(item[0]) != 6
                        or not all(type(n) is int for n in item[0])
                        or not isinstance(item[1], list) or len(item[1]) != 2
                        or type(item[1][0]) is not int or not isinstance(item[1][1], str)
                        or re.fullmatch('[0-9a-f]{64}', item[1][1]) is None):
                    raise ValueError('cache entry')
            self.entries = data['entries']
        except (OSError, ValueError, TypeError, AttributeError, RecursionError):
            pass

    def identity(self, name, path, reader):
        try:
            before = fingerprint(path)
            cached = self.entries.get(name)
            if cached is not None and cached[0] == before and stat.S_ISREG(before[-1]) and cached[1][0] == stat.S_IMODE(before[-1]):
                value = cached[1]
            else:
                value = reader(path)
            # Never persist a hash computed while its file was changing. Symlinks
            # and absent files always use the reference reader.
            if fingerprint(path) != before:
                # A hit that raced a change must not return stale bytes. One
                # reference read is bounded and retains the original semantics.
                return reader(path)
            if isinstance(value[0], int):
                self.updated[name] = [before, value]
            return value
        except OSError:
            return reader(path)

    def save(self, *, keep_existing=False):
        if keep_existing:
            self.updated = dict(self.entries, **self.updated)
        temporary = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w', dir=self.path.parent, delete=False) as stream:
                temporary = stream.name
                json.dump({'version': 1, 'entries': self.updated, 'entries_sha256': hashlib.sha256(json.dumps(self.updated, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()}, stream, sort_keys=True, separators=(',', ':'), allow_nan=False)
            os.replace(temporary, self.path)
        except (OSError, ValueError):
            pass
        finally:
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass
