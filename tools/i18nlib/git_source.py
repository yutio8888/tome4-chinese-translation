"""Immutable Git object reads used by extraction and comparison."""

from __future__ import annotations

import io
import os
import shutil
import subprocess
import tarfile
from pathlib import Path, PurePosixPath

from .errors import ConfigurationError, ExtractionError


UNSAFE_GIT_ENV = frozenset(
    {
        "BASH_ENV",
        "ENV",
        "CDPATH",
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_REPLACE_REF_BASE",
        "GIT_EXTERNAL_DIFF",
        "GIT_DIFF_OPTS",
        "LD_PRELOAD",
        "LD_LIBRARY_PATH",
        "PYTHONHOME",
        "PYTHONPATH",
    }
)


def _git_environment() -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in UNSAFE_GIT_ENV and not key.startswith("GIT_")
    }
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "LC_ALL": "C",
            "LANG": "C",
        }
    )
    return env


def _normalized_git_path(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or "\\" in value
        or "\x00" in value
    ):
        raise ConfigurationError(f"unsafe Git path: {value!r}")
    return value


class GitRepository:
    def __init__(self, path: Path) -> None:
        self.path = path.resolve()
        git = shutil.which("git")
        if not git:
            raise ConfigurationError("git executable not found")
        self.git = git

    def _run(
        self, arguments: list[str], *, text: bool = False
    ) -> subprocess.CompletedProcess[bytes] | subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                [self.git, "-C", str(self.path), *arguments],
                env=_git_environment(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=text,
                check=False,
            )
        except OSError as error:
            raise ConfigurationError(f"cannot execute git: {error}") from error

    def validate(
        self, commit: str, *, check_worktree: bool = True
    ) -> dict[str, object]:
        if not self.path.is_dir():
            raise ConfigurationError(f"repository directory not found: {self.path}")
        top = self._run(["rev-parse", "--show-toplevel"], text=True)
        if top.returncode != 0:
            raise ConfigurationError(f"not a Git worktree: {self.path}")
        actual_top = Path(top.stdout.strip()).resolve()
        if actual_top != self.path:
            raise ConfigurationError(
                f"repository path must be its Git top-level: {self.path} != {actual_top}"
            )
        resolved = self._run(
            ["rev-parse", "--verify", f"{commit}^{{commit}}"], text=True
        )
        if resolved.returncode != 0 or resolved.stdout.strip() != commit:
            detail = resolved.stderr.strip()
            raise ConfigurationError(
                f"required Git commit is unavailable in {self.path}: {commit}"
                + (f" ({detail})" if detail else "")
            )
        head = self._run(["rev-parse", "--verify", "HEAD"], text=True)
        clean: bool | None = None
        if check_worktree:
            status = self._run(
                ["status", "--porcelain", "--untracked-files=all"], text=True
            )
            clean = status.returncode == 0 and not status.stdout.strip()
        return {
            "path": str(self.path),
            "commit": commit,
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "clean": clean,
            "worktree_checked": check_worktree,
        }

    def read_blob(self, commit: str, git_path: str) -> bytes:
        normalized = _normalized_git_path(git_path)
        tree = self._run(["ls-tree", "-z", commit, "--", normalized])
        if tree.returncode != 0:
            raise ExtractionError(
                tree.stderr.decode("utf-8", errors="replace").strip()
                or f"git ls-tree failed for {normalized}"
            )
        records = [record for record in tree.stdout.split(b"\0") if record]
        if len(records) != 1:
            raise ExtractionError(
                f"Git blob is missing or ambiguous: {commit}:{normalized}"
            )
        try:
            header, listed = records[0].split(b"\t", 1)
            mode, object_type, object_id = header.decode("ascii").split(" ")
            listed_path = listed.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise ExtractionError("invalid Git tree record") from error
        if (
            listed_path != normalized
            or object_type != "blob"
            or mode not in ("100644", "100755")
        ):
            raise ExtractionError(
                f"Git path is not a regular file: {commit}:{normalized}"
            )
        blob = self._run(["cat-file", "blob", object_id])
        if blob.returncode != 0:
            raise ExtractionError(
                blob.stderr.decode("utf-8", errors="replace").strip()
                or f"cannot read Git blob {object_id}"
            )
        return blob.stdout

    def lua_files(self, commit: str, git_path: str) -> list[tuple[str, bytes]]:
        normalized = _normalized_git_path(git_path).rstrip("/")
        pathspec = f":(glob){normalized}/**/*.lua"
        archive = self._run(["archive", "--format=tar", commit, "--", pathspec])
        if archive.returncode != 0:
            detail = archive.stderr.decode("utf-8", errors="replace").strip()
            raise ExtractionError(
                f"cannot archive Lua sources at {commit}:{normalized}: {detail}"
            )
        files: list[tuple[str, bytes]] = []
        try:
            with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
                for member in tar:
                    if not member.isfile() or not member.name.endswith(".lua"):
                        continue
                    name = _normalized_git_path(member.name)
                    if not (name == normalized or name.startswith(normalized + "/")):
                        raise ExtractionError(
                            f"archive member escaped requested path: {name}"
                        )
                    handle = tar.extractfile(member)
                    if handle is None:
                        raise ExtractionError(f"cannot read archive member: {name}")
                    files.append((name, handle.read()))
        except tarfile.TarError as error:
            raise ExtractionError(f"invalid Git archive: {error}") from error
        if not files:
            raise ExtractionError(
                f"no Lua files found at {commit}:{normalized}"
            )
        files.sort(key=lambda item: item[0])
        return files

    def materialize_lua_tree(
        self,
        commit: str,
        git_path: str,
        destination: Path,
        *,
        mount: str,
    ) -> int:
        source_prefix = _normalized_git_path(git_path).rstrip("/")
        mount_prefix = PurePosixPath(_normalized_git_path(mount))
        count = 0
        for source_name, data in self.lua_files(commit, source_prefix):
            relative = PurePosixPath(source_name).relative_to(source_prefix)
            target_relative = mount_prefix / relative
            target = destination.joinpath(*target_relative.parts)
            if target.exists():
                if target.read_bytes() != data:
                    raise ExtractionError(f"conflicting staged source: {target_relative}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            count += 1
        return count
