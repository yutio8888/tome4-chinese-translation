#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布仓库冒烟验证：模拟 addon 运行时加载链。

验证发布仓库（tome-chn-mod）的：
1. data/locales/zh_hans.lua —— 引擎自动加载的主覆盖层（tome delta + DLC sections）
2. data/null_translation.lua —— hooks/load.lua 显式加载的 Nullpack 译文
3. hooks/load.lua —— 语法与加载语句存在性
4. init.lua —— 元数据与 GPL v3 声明头部

用法：python3 -B tools/smoke_release.py [--addon-root /path/to/tome-chn-mod]
退出码：0 = 全部通过；非 0 = 失败。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import Manifest, load_manifest  # noqa: E402
from i18nlib.locale_model import (  # noqa: E402
    LocaleDocument,
    LocaleLoader,
    runtime_map,
)
from i18nlib.publish import (  # noqa: E402
    _dlc_overlay_entries,
    _official_locale_keys,
)
from i18nlib.runtime import LuaRuntime  # noqa: E402

_LUA_TIMEOUT_SECONDS = 300
_DLC_COMPONENTS = ("ashes-urhrok", "cults", "orcs")
_SEMANTIC_FIELDS = ("target", "args_order", "special")

_LUA_PROBE = r"""
-- probe: load a locale file under an I18N-like environment
local file = arg[1]
local n = 0
local lc = nil
local env = {
    locale = function(s) lc = s end,
    section = function(s) end,
    t = function(src, dst, tag) n = n + 1 end,
    tc = function(src, dst, tag) n = n + 1 end,
}
setmetatable(env, { __index = _G })
local f, err = loadfile(file)
if not f then io.write("LOADFAIL:", err, "\n"); os.exit(2) end
setfenv(f, env)
local ok, load_err = pcall(f)
if not ok then io.write("RUNFAIL:", load_err, "\n"); os.exit(3) end
io.write("entries:", n, "\n")
if lc and lc ~= "zh_hans" then io.write("LOCALEMISMATCH:", lc, "\n"); os.exit(4) end
os.exit(0)
"""

_LUA_SYNTAX_PROBE = r"""
local file = arg[1]
local chunk, err = loadfile(file)
if not chunk then io.write("LOADFAIL:", err, "\n"); os.exit(2) end
os.exit(0)
"""

RuntimeKey = tuple[str, str | None]
RuntimeEntryMap = dict[RuntimeKey, dict[str, Any]]


@dataclass(frozen=True)
class ReleaseLayout:
    locale: Path
    null_translation: Path
    hooks: Path
    init: Path

    def required_files(self) -> tuple[tuple[str, Path], ...]:
        return (
            ("locale file exists", self.locale),
            ("null_translation exists", self.null_translation),
            ("hooks/load.lua exists", self.hooks),
            ("init.lua exists", self.init),
        )


@dataclass(frozen=True)
class DlcComparison:
    expected: int
    actual: int
    missing: tuple[RuntimeKey, ...]
    unexpected: tuple[RuntimeKey, ...]
    mismatched: tuple[RuntimeKey, ...]

    @property
    def ok(self) -> bool:
        return not (self.missing or self.unexpected or self.mismatched)

    @property
    def detail(self) -> str:
        return (
            f"expected={self.expected}, actual={self.actual}, "
            f"missing={len(self.missing)}, "
            f"unexpected={len(self.unexpected)}, "
            f"mismatched={len(self.mismatched)}"
        )


class CheckReporter:
    def __init__(self) -> None:
        self.failures = 0

    def check(self, label: str, ok: bool, detail: str = "") -> None:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
        if not ok:
            self.failures += 1

    def finish(self) -> int:
        print()
        if self.failures:
            print(f"SMOKE FAILED: {self.failures} check(s) failed")
            return 1
        print("SMOKE OK: release addon is loadable and consistent")
        return 0


def _release_layout(addon_root: Path) -> ReleaseLayout:
    return ReleaseLayout(
        locale=addon_root / "data" / "locales" / "zh_hans.lua",
        null_translation=addon_root / "data" / "null_translation.lua",
        hooks=addon_root / "hooks" / "load.lua",
        init=addon_root / "init.lua",
    )


def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _error_detail(error: BaseException) -> str:
    return str(error).strip() or type(error).__name__


def _process_detail(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stderr.strip() or result.stdout.strip() or "no diagnostic output")


def run_lua(
    runtime: LuaRuntime,
    script: str,
    *args: str,
    timeout: int = _LUA_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    """Run a temporary Lua probe through the manifest-configured runtime."""
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", suffix=".lua", delete=False
    ) as fp:
        fp.write(script)
        temporary_path = Path(fp.name)
    try:
        return runtime.run(
            [temporary_path, *args],
            cwd=runtime.manifest.root,
            timeout=timeout,
        )
    finally:
        temporary_path.unlink(missing_ok=True)


def _translation_probe(
    runtime: LuaRuntime, path: Path
) -> tuple[bool, int, str]:
    try:
        result = run_lua(runtime, _LUA_PROBE, str(path))
    except Exception as error:
        return False, 0, _error_detail(error)
    if result.returncode != 0:
        return False, 0, _process_detail(result)
    entry_lines = [
        line for line in result.stdout.splitlines() if line.startswith("entries:")
    ]
    if len(entry_lines) != 1:
        return False, 0, f"unexpected probe output: {result.stdout!r}"
    try:
        entries = int(entry_lines[0].split(":", 1)[1])
    except ValueError:
        return False, 0, f"invalid entry count: {entry_lines[0]!r}"
    return True, entries, f"{entries} t() entries"


def _syntax_probe(runtime: LuaRuntime, path: Path) -> tuple[bool, str]:
    try:
        result = run_lua(runtime, _LUA_SYNTAX_PROBE, str(path))
    except Exception as error:
        return False, _error_detail(error)
    if result.returncode != 0:
        return False, _process_detail(result)
    return True, ""


def _translation_signature(entry: Mapping[str, Any]) -> str:
    """Return a deterministic, type-sensitive signature of runtime semantics."""
    return json.dumps(
        {field: entry.get(field) for field in _SEMANTIC_FIELDS},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _runtime_key_sort_key(key: RuntimeKey) -> str:
    return json.dumps(key, ensure_ascii=False, separators=(",", ":"))


def compare_dlc_runtime_maps(
    expected: Mapping[RuntimeKey, Mapping[str, Any]],
    actual: Mapping[RuntimeKey, Mapping[str, Any]],
) -> DlcComparison:
    """Compare exact runtime keys and t() semantics for one DLC section."""
    expected_keys = set(expected)
    actual_keys = set(actual)
    missing = tuple(
        sorted(expected_keys - actual_keys, key=_runtime_key_sort_key)
    )
    unexpected = tuple(
        sorted(actual_keys - expected_keys, key=_runtime_key_sort_key)
    )
    mismatched = tuple(
        sorted(
            (
                key
                for key in expected_keys & actual_keys
                if _translation_signature(expected[key])
                != _translation_signature(actual[key])
            ),
            key=_runtime_key_sort_key,
        )
    )
    return DlcComparison(
        expected=len(expected_keys),
        actual=len(actual_keys),
        missing=missing,
        unexpected=unexpected,
        mismatched=mismatched,
    )


def _entries_runtime_map(
    entries: Iterable[dict[str, Any]], *, logical_path: str
) -> RuntimeEntryMap:
    document = LocaleDocument(
        logical_path=logical_path,
        sha256="",
        records=tuple(entries),
    )
    return runtime_map((document,))


def expected_dlc_runtime_maps(
    manifest: Manifest,
    loader: LocaleLoader,
    *,
    official_keys_loader: Callable[
        [Manifest, LocaleLoader], set[RuntimeKey]
    ] = _official_locale_keys,
    overlay_entries_loader: Callable[
        [Manifest, LocaleLoader, set[RuntimeKey]], list[dict[str, Any]]
    ] = _dlc_overlay_entries,
) -> dict[str, RuntimeEntryMap]:
    """Build the same canonical DLC overlay maps used by publish."""
    official_keys = official_keys_loader(manifest, loader)
    overlay_entries = overlay_entries_loader(manifest, loader, official_keys)
    return {
        component_id: _entries_runtime_map(
            (
                entry
                for entry in overlay_entries
                if entry.get("section") == component_id
            ),
            logical_path=f"expected:{component_id}",
        )
        for component_id in _DLC_COMPONENTS
    }


def release_dlc_runtime_maps(document: LocaleDocument) -> dict[str, RuntimeEntryMap]:
    """Select the runtime map belonging to each DLC section in a release file."""
    return {
        component_id: _entries_runtime_map(
            (
                entry
                for entry in document.translations
                if entry.get("section") == component_id
            ),
            logical_path=f"release:{component_id}",
        )
        for component_id in _DLC_COMPONENTS
    }


def run_release_smoke(
    manifest: Manifest,
    addon_root: Path,
    *,
    runtime_factory: Callable[[Manifest], LuaRuntime] | None = None,
    loader_factory: Callable[[LuaRuntime], LocaleLoader] | None = None,
    official_keys_loader: Callable[
        [Manifest, LocaleLoader], set[RuntimeKey]
    ] | None = None,
    overlay_entries_loader: Callable[
        [Manifest, LocaleLoader, set[RuntimeKey]], list[dict[str, Any]]
    ] | None = None,
    text_reader: Callable[[Path], str] = _read_utf8,
) -> int:
    """Run smoke checks with injectable runtime, loader, and canonical sources."""
    runtime_factory = runtime_factory or LuaRuntime
    loader_factory = loader_factory or LocaleLoader
    official_keys_loader = official_keys_loader or _official_locale_keys
    overlay_entries_loader = overlay_entries_loader or _dlc_overlay_entries

    reporter = CheckReporter()
    layout = _release_layout(addon_root)
    layout_valid = True
    for label, path in layout.required_files():
        exists = path.is_file()
        reporter.check(label, exists, "" if exists else str(path))
        layout_valid = layout_valid and exists
    if not layout_valid:
        return reporter.finish()

    try:
        runtime = runtime_factory(manifest)
        runtime.doctor()
    except Exception as error:
        reporter.check("manifest Lua runtime doctor", False, _error_detail(error))
        return reporter.finish()
    reporter.check("manifest Lua runtime doctor", True)

    locale_ok, entries, locale_detail = _translation_probe(runtime, layout.locale)
    reporter.check(
        "zh_hans.lua loads (locale/section/t env)", locale_ok, locale_detail
    )
    reporter.check("zh_hans.lua has >5000 entries", entries > 5000, str(entries))

    null_ok, null_entries, null_detail = _translation_probe(
        runtime, layout.null_translation
    )
    reporter.check("null_translation.lua loads", null_ok, null_detail)
    reporter.check(
        "null_translation entries > 400", null_entries > 400, str(null_entries)
    )

    try:
        hooks_text = text_reader(layout.hooks)
    except Exception as error:
        reporter.check(
            "hooks/load.lua loads standalone translations",
            False,
            _error_detail(error),
        )
    else:
        reporter.check(
            "hooks/load.lua loads standalone translations",
            "null_translation.lua" in hooks_text,
        )
    hooks_syntax_ok, hooks_syntax_detail = _syntax_probe(runtime, layout.hooks)
    reporter.check("hooks/load.lua syntax", hooks_syntax_ok, hooks_syntax_detail)

    try:
        init_text = text_reader(layout.init)
    except Exception as error:
        reporter.check("init.lua readable", False, _error_detail(error))
    else:
        reporter.check(
            "init.lua has GPL v3 header",
            "GNU General Public License" in init_text,
        )
        reporter.check(
            "init.lua locale metadata",
            'for_module = "tome"' in init_text and "addon_version" in init_text,
        )

    try:
        loader = loader_factory(runtime)
        release_document = loader.load_path(layout.locale, logical_path="release")
        expected_maps = expected_dlc_runtime_maps(
            manifest,
            loader,
            official_keys_loader=official_keys_loader,
            overlay_entries_loader=overlay_entries_loader,
        )
        actual_maps = release_dlc_runtime_maps(release_document)
    except Exception as error:
        reporter.check("canonical DLC consistency", False, _error_detail(error))
    else:
        for component_id in _DLC_COMPONENTS:
            comparison = compare_dlc_runtime_maps(
                expected_maps[component_id], actual_maps[component_id]
            )
            reporter.check(
                f"DLC {component_id} exact runtime overlay",
                comparison.ok,
                comparison.detail,
            )

    return reporter.finish()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--addon-root", default=None, help="release repository root")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest()
        addon_root = (
            Path(args.addon_root)
            if args.addon_root
            else manifest.repository_path("addon")
        )
        return run_release_smoke(manifest, addon_root)
    except Exception as error:
        print(f"[FAIL] smoke release setup — {_error_detail(error)}")
        print()
        print("SMOKE FAILED: 1 check(s) failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
