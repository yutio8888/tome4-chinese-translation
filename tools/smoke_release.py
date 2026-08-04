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
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import load_manifest  # noqa: E402

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


def run_lua(script: str, *args: str) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False) as fp:
        fp.write(script)
        tmp = fp.name
    try:
        return subprocess.run(
            ["luajit", tmp, *args], capture_output=True, text=True, timeout=300
        )
    finally:
        Path(tmp).unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--addon-root", default=None, help="release repository root")
    args = parser.parse_args(argv)

    manifest = load_manifest()
    addon_root = Path(args.addon_root) if args.addon_root else manifest.repository_path("addon")
    locale_file = addon_root / "data" / "locales" / "zh_hans.lua"
    null_file = addon_root / "data" / "null_translation.lua"
    hooks_file = addon_root / "hooks" / "load.lua"
    init_file = addon_root / "init.lua"

    failures = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
        if not ok:
            failures += 1

    check("locale file exists", locale_file.is_file())
    check("null_translation exists", null_file.is_file())
    check("hooks/load.lua exists", hooks_file.is_file())
    check("init.lua exists", init_file.is_file())

    # 1) 主覆盖层加载
    result = run_lua(_LUA_PROBE, str(locale_file))
    ok = result.returncode == 0
    entries = 0
    if ok:
        for line in result.stdout.splitlines():
            if line.startswith("entries:"):
                entries = int(line.split(":", 1)[1])
    check("zh_hans.lua loads (locale/section/t env)", ok,
          f"{entries} t() entries" if ok else result.stdout + result.stderr)
    check("zh_hans.lua has >5000 entries", entries > 5000, f"{entries}")

    # 2) null_translation 加载（hooks 显式加载的目标）
    result = run_lua(_LUA_PROBE, str(null_file))
    ok = result.returncode == 0
    null_entries = 0
    if ok:
        for line in result.stdout.splitlines():
            if line.startswith("entries:"):
                null_entries = int(line.split(":", 1)[1])
    check("null_translation.lua loads", ok,
          f"{null_entries} t() entries" if ok else result.stdout + result.stderr)
    check("null_translation entries > 400", null_entries > 400, f"{null_entries}")

    # 3) hooks/load.lua 语法 + 显式加载语句
    check(
        "hooks/load.lua loads standalone translations",
        "null_translation.lua" in hooks_file.read_text(encoding="utf-8"),
    )
    result = subprocess.run(
        ["luajit", "-e", f"assert(loadfile({str(hooks_file)!r}))"],
        capture_output=True, text=True,
    )
    check("hooks/load.lua syntax", result.returncode == 0, result.stderr.strip())

    # 4) init.lua 元数据 + GPL v3 头部
    init_text = init_file.read_text(encoding="utf-8", errors="replace")
    check("init.lua has GPL v3 header", "GNU General Public License" in init_text)
    check("init.lua locale metadata", 'for_module = "tome"' in init_text
          and "addon_version" in init_text)

    # 5) 与规范译文一致性抽查（DLC 专有条目在发布文件中）
    try:
        from i18nlib.locale_model import LocaleLoader  # noqa: PLC0415
        from i18nlib.runtime import LuaRuntime  # noqa: PLC0415

        runtime = LuaRuntime(manifest)
        runtime.doctor()
        loader = LocaleLoader(runtime)
        pub = loader.load_path(locale_file, logical_path="release")
        pub_keys = {(r.get("source"), r.get("source_tag")) for r in pub.translations}
        sampled = 0
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            component = manifest.component(component_id)
            doc = loader.load_path(manifest.root / component.translation, logical_path=component_id)
            present = sum(
                1
                for r in doc.translations
                if (r.get("source"), r.get("source_tag")) in pub_keys
            )
            sampled += present
            check(
                f"DLC {component_id} canonical entries in release file",
                present > 0,
                f"{present}/{len(doc.translations)}",
            )
        check("DLC entries sampled overall", sampled > 4000, f"{sampled}")
    except Exception as error:  # pragma: no cover
        check("canonical consistency probe", False, str(error))

    print()
    if failures:
        print(f"SMOKE FAILED: {failures} check(s) failed")
        return 1
    print("SMOKE OK: release addon is loadable and consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
