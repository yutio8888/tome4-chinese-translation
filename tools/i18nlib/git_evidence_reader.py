"""Immutable Git bytes cached only inside one synchronous projection call.

Also caches objects *derived* from those bytes, keyed by the same immutable
content identity.  A projection revisits the same catalog blobs dozens of
times (97 batch base commits resolve to 43 distinct catalog contents), and
re-parsing identical bytes cannot produce a different answer.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import re
from typing import Callable, Iterator


class GitEvidenceReader:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.blobs: dict[str, bytes] = {}
        self.trees: dict[str, bytes] = {}
        self.derived: dict[tuple[str, str], object] = {}

    def read(self, kind: str, object_id: str, load: Callable[[], bytes]) -> bytes:
        cache = self.blobs if kind == "blob" else self.trees
        if object_id not in cache:
            cache[object_id] = load()
        return cache[object_id]

    def derive(self, kind: str, identity: str, load: Callable[[], object]) -> object:
        key = (kind, identity)
        if key not in self.derived:
            self.derived[key] = load()
        return self.derived[key]


_active: ContextVar[GitEvidenceReader | None] = ContextVar("git_evidence_reader", default=None)


@contextmanager
def projection_scope(root: Path) -> Iterator[None]:
    # Always create a fresh scope, including nested projections. Reset on errors
    # restores the enclosing reader; clearing also releases any retained context.
    reader = GitEvidenceReader(root)
    token = _active.set(reader)
    try:
        yield
    finally:
        _active.reset(token)
        reader.blobs.clear()
        reader.trees.clear()
        reader.derived.clear()


def read(root: Path, kind: str, object_id: str, git: Callable[..., bytes],
         *args: str) -> bytes:
    reader = _active.get()
    if reader is None or reader.root != root.resolve():
        return git(root, *args, object_id)
    if re.fullmatch(r"[0-9a-f]{40}", object_id) is None:
        # Resolve the expression BEFORE peeling: in HEAD:path^{blob}, Git
        # interprets the suffix as part of the path, not a type assertion.
        # Aliases are resolved every time, never stored as cache keys.
        resolved = git(root, "rev-parse", "--verify", object_id).decode("ascii").strip()
        if re.fullmatch(r"[0-9a-f]{40}", resolved) is None:
            return git(root, *args, object_id)
        object_id = git(root, "rev-parse", "--verify", f"{resolved}^{{{kind}}}").decode("ascii").strip()
    if re.fullmatch(r"[0-9a-f]{40}", object_id) is None:
        # Preserve the underlying Git/error contract for non-SHA1 repositories.
        return git(root, *args, object_id)
    return reader.read(kind, object_id, lambda: git(root, *args, object_id))


def derive(root: Path, kind: str, identity: str, load: Callable[[], object]) -> object:
    """Reuse an object derived from immutable Git content within one projection.

    Outside a projection scope this is a plain call, so behaviour is unchanged.
    """
    reader = _active.get()
    if reader is None or reader.root != root.resolve():
        return load()
    return reader.derive(kind, identity, load)
