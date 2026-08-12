"""LuaJIT 5.1 runtime discovery and invocation."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

from .config import Manifest
from .errors import RuntimeCheckError


class LuaRuntime:
    def __init__(self, manifest: Manifest) -> None:
        self.manifest = manifest
        self.spec = manifest.runtime
        configured_luajit = os.environ.get(self.spec.luajit_env)
        if configured_luajit:
            candidate = Path(configured_luajit).expanduser()
            if not candidate.is_absolute():
                raise RuntimeCheckError(
                    f"{self.spec.luajit_env} must be an absolute path"
                )
            self.luajit = candidate
        else:
            discovered = shutil.which("luajit")
            self.luajit = (
                Path(discovered).resolve() if discovered else Path("luajit")
            )

        configured_rocks = os.environ.get(self.spec.luarocks_root_env)
        self.rocks_root = Path(
            configured_rocks or self.spec.luarocks_root_default
        ).expanduser()
        if configured_rocks and not self.rocks_root.is_absolute():
            raise RuntimeCheckError(
                f"{self.spec.luarocks_root_env} must be an absolute path"
            )
        self.rocks_root = self.rocks_root.resolve()

    @property
    def lua_share(self) -> Path:
        return self.rocks_root / "share" / "lua" / "5.1"

    @property
    def lua_lib(self) -> Path:
        return self.rocks_root / "lib" / "lua" / "5.1"

    def environment(
        self,
        lua_paths: Iterable[Path] = (),
        *,
        cwd: Path,
    ) -> dict[str, str]:
        env = os.environ.copy()
        prefixes: list[str] = []
        for path in lua_paths:
            resolved = (path if path.is_absolute() else cwd / path).resolve()
            prefixes.extend(
                [str(resolved / "?.lua"), str(resolved / "?" / "init.lua")]
            )
        prefixes.extend(
            [
                str(self.lua_share / "?.lua"),
                str(self.lua_share / "?" / "init.lua"),
                "",
                "",
            ]
        )
        env["LUA_PATH"] = ";".join(prefixes)
        env["LUA_CPATH"] = ";".join(
            [str(self.lua_lib / "?.so"), "", ""]
        )
        env["LC_ALL"] = "C"
        env["LANG"] = "C"
        env["LUA_INIT"] = ""
        env["LUA_INIT_5_1"] = ""
        return env

    def run(
        self,
        arguments: Sequence[str | Path],
        *,
        cwd: Path,
        lua_paths: Iterable[Path] = (),
        timeout: int | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [str(self.luajit), *(str(argument) for argument in arguments)]
        env = self.environment(lua_paths, cwd=cwd)
        if extra_env:
            env.update(extra_env)
        try:
            return subprocess.run(
                command,
                cwd=cwd,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as error:
            raise RuntimeCheckError(f"luajit not found: {self.luajit}") from error
        except OSError as error:
            raise RuntimeCheckError(f"cannot execute luajit: {error}") from error
        except subprocess.TimeoutExpired as error:
            raise RuntimeCheckError(
                f"luajit command timed out after {timeout} seconds"
            ) from error

    def run_protected(
        self,
        arguments: Sequence[str | Path],
        *,
        cwd: Path,
        lua_paths: Iterable[Path] = (),
        timeout: int | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[None]:
        """Run an audited Lua broker without exposing either output stream."""
        command = [str(self.luajit), *(str(argument) for argument in arguments)]
        env = self.environment(lua_paths, cwd=cwd)
        if extra_env:
            env.update(extra_env)
        try:
            return subprocess.run(
                command,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as error:
            raise RuntimeCheckError(f"luajit not found: {self.luajit}") from error
        except OSError as error:
            raise RuntimeCheckError("cannot execute protected Lua broker") from error
        except subprocess.TimeoutExpired as error:
            raise RuntimeCheckError(
                f"protected Lua broker timed out after {timeout} seconds"
            ) from error

    def doctor(self) -> dict[str, object]:
        if not self.luajit.is_absolute():
            if shutil.which(str(self.luajit)) is None:
                raise RuntimeCheckError(f"luajit not found: {self.luajit}")
        elif not self.luajit.is_file():
            raise RuntimeCheckError(f"luajit not found: {self.luajit}")
        if not self.rocks_root.is_dir():
            raise RuntimeCheckError(
                f"project LuaRocks tree not found: {self.rocks_root}"
            )

        invalid_modules = [
            module
            for module in self.spec.required_modules
            if not isinstance(module, str)
            or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*([.][A-Za-z_][A-Za-z0-9_]*)*", module
            )
        ]
        if invalid_modules:
            raise RuntimeCheckError(
                "required module names must be simple Lua identifiers: "
                + ", ".join(str(module) for module in invalid_modules)
            )
        require_lines = [
            f'local m_{index} = require("{module}")'
            for index, module in enumerate(self.spec.required_modules)
        ]
        probe = "; ".join(
            [
                *require_lines,
                'local lpeg = require("lpeg")',
                'print(_VERSION)',
                'print(jit.version)',
                'print(lpeg.version and lpeg.version() or "unknown")',
            ]
        )
        result = self.run(["-e", probe], cwd=self.manifest.root)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeCheckError(f"LuaJIT dependency probe failed: {detail}")
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) < 3:
            raise RuntimeCheckError(
                f"unexpected LuaJIT dependency probe output: {result.stdout!r}"
            )
        lua_version, luajit_version, lpeg_version = lines[-3:]
        if lua_version != self.spec.lua_version:
            raise RuntimeCheckError(
                f"expected {self.spec.lua_version}, got {lua_version}"
            )
        if lpeg_version != self.spec.lpeg_runtime_version:
            raise RuntimeCheckError(
                "incompatible LPeg runtime: "
                f"expected {self.spec.lpeg_runtime_version}, got {lpeg_version}"
            )
        rock_dir = (
            self.rocks_root
            / "lib"
            / "luarocks"
            / "rocks-5.1"
            / "lpeg"
            / self.spec.lpeg_rock_version
        )
        if not rock_dir.is_dir():
            raise RuntimeCheckError(
                "verified LPeg rock is missing: "
                f"expected {self.spec.lpeg_rock_version} under {rock_dir.parent}"
            )
        return {
            "ok": True,
            "luajit": str(self.luajit.resolve()),
            "lua_version": lua_version,
            "luajit_version": luajit_version,
            "lpeg_runtime_version": lpeg_version,
            "lpeg_rock_version": self.spec.lpeg_rock_version,
            "luarocks_root": str(self.rocks_root),
            "modules": list(self.spec.required_modules),
        }
