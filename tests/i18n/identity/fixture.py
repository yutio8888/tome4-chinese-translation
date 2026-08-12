"""Shared mini-tome fixture helpers for identity contract tests (G2-G12).

Stages the pinned official extractor once per process, applies the contract
patches, and runs the real Luafish traversal over a synthetic component tree
so tests exercise the actual enrichment sidecar pipeline.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import ExtractorSpec, load_manifest  # noqa: E402
from i18nlib.extract import (  # noqa: E402
    _minimal_mounts,
    _normalized_definitions,
    _patch_extractor,
    parse_enrichment_records,
)
from i18nlib.git_source import GitRepository  # noqa: E402
from i18nlib.identity import (  # noqa: E402
    SLOT_REGISTRY_RELATIVE_PATH,
    ComponentIndex,
    SlotRegistry,
    build_component_index,
)
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.snapshot import read_snapshot  # noqa: E402

_MANIFEST = load_manifest()
_RUNTIME = LuaRuntime(_MANIFEST)
_RUNTIME.doctor()
_LOADER = LocaleLoader(_RUNTIME)
_EXTRACTOR_STAGE: Path | None = None
_EXTRACTOR_STAGE_TEMP: Any = None

FIXTURE_TALENTS = """newTalent{
\tname = "Flame",
\tshort_name = "FLAME",
\ttype = {"spell/fire", 1},
\tpoints = 5,
\tinfo = function(self, t) return ([[Deals %d fire damage.]]):tformat(10) end,
}
newTalent{
\tname = "Burning Shock",
\tshort_name = "BURNING_SHOCK",
\ttype = {"spell/fire", 1},
}
newTalent{
\tname = "Flame Bolt",
\tshort_name = "FLAME_BOLT",
\ttype = {"spell/fire", 2},
}
"""

FIXTURE_EFFECTS = """newEffect{
\tname = "BURNING",
\tdesc = _t"Burning",
\ttype = "physical",
\tsubtype = { burning=true, fire=true },
}
newEffect{
\tname = "RELENTLESS_TEMPO",
\tdesc = _t"Relentless Tempo",
\ttype = "physical",
\tsubtype = { tempo=true },
}
"""

FIXTURE_ENTITIES = """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tname = "ant",
\ttype = "insect", subtype = "ant",
\tkeywords = { ["insect"] = true },
}
newEntity{
\tname = "huge ant",
\ttype = "insect", subtype = "huge",
}
newEntity{
\tbase = "BASE_NPC_ANT",
\tname = "giant ant",
\ttype = "insect", subtype = "giant",
}
"""

FIXTURE_MISC = """ActorStats:defineStat("Strength", "str")
local x = _t("physical", "damage type")
game.logPlayer(self, "You hit %s for %d damage.", target.name, 42)
"""


def manifest() -> Any:
    return _MANIFEST


def runtime() -> LuaRuntime:
    return _RUNTIME


def loader() -> LocaleLoader:
    return _LOADER


def _stage_extractor() -> Path:
    global _EXTRACTOR_STAGE, _EXTRACTOR_STAGE_TEMP
    if _EXTRACTOR_STAGE is None:
        extractor_repository = GitRepository(
            _MANIFEST.repository_path(_MANIFEST.extractor.repository)
        )
        extractor_repository.validate(_MANIFEST.extractor.commit, check_worktree=False)
        _EXTRACTOR_STAGE_TEMP = tempfile.TemporaryDirectory(
            prefix="tome4-i18n-test-extractor-"
        )
        tool_stage = Path(_EXTRACTOR_STAGE_TEMP.name) / "tool"
        extractor_repository.materialize_lua_tree(
            _MANIFEST.extractor.commit,
            _MANIFEST.extractor.git_path,
            tool_stage,
            mount="i18n_tools",
        )
        extractor_root = tool_stage / "i18n_tools"
        spec = ExtractorSpec(
            repository=_MANIFEST.extractor.repository,
            commit=_MANIFEST.extractor.commit,
            git_path=_MANIFEST.extractor.git_path,
            max_stack=_MANIFEST.extractor.max_stack,
            preserve_duplicate_occurrences=True,
        )
        _patch_extractor(extractor_root, spec, enrich=True)
        _EXTRACTOR_STAGE = extractor_root
    return _EXTRACTOR_STAGE


def write_fixture_tree(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def run_extractor(tree_root: Path) -> tuple[Path, Path]:
    """Run the patched extractor over tree_root; returns (i18n_list, sidecar)."""
    extractor_root = _stage_extractor()
    result = _RUNTIME.run(
        [extractor_root / "i18n_extractor.lua", *["mod-test"]],
        cwd=tree_root,
        lua_paths=[extractor_root],
        extra_env={"I18N_ENRICHMENT": "i18n_enrichment.jsonl"},
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert (tree_root / "i18n_list.lua").is_file()
    assert (tree_root / "i18n_enrichment.jsonl").is_file()
    return tree_root / "i18n_list.lua", tree_root / "i18n_enrichment.jsonl"


def build_fixture_index(
    tree_root: Path, *, component: str = "test-component"
) -> ComponentIndex:
    """Full index build for a fixture tree (snapshot + sidecar + registry)."""
    list_path, sidecar_path = run_extractor(tree_root)
    extracted = _LOADER.load_path(
        list_path, logical_path=f"generated:test/{component}/i18n_list.lua"
    )
    definitions = _normalized_definitions(
        component=component,
        records=extracted.records,
        origin_kind="extracted",
    )
    snapshot_data = b"".join(
        (
            json.dumps(
                definition, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
            + b"\n"
        )
        for definition in definitions
    )
    snapshot_path = tree_root / "snapshot.jsonl"
    snapshot_path.write_bytes(snapshot_data)
    snapshot = read_snapshot(snapshot_path, expected_component=component)
    sidecar = [
        json.loads(line)
        for line in sidecar_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    return build_component_index(
        component=component,
        snapshot=snapshot,
        enrichment_records=parse_enrichment_records(
            sidecar, source_label=f"test:{component}"
        ),
        slot_registry=SlotRegistry.load(
            _MANIFEST.root / SLOT_REGISTRY_RELATIVE_PATH
        ),
    )


def make_tree(files: dict[str, str] | None = None) -> Any:
    """Create a temporary mini-tome tree; returns (root, tempdir)."""
    temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-mini-tome-")
    root = Path(temporary.name)
    default_files = {
        "mod-test/data/talents.lua": FIXTURE_TALENTS,
        "mod-test/data/effects.lua": FIXTURE_EFFECTS,
        "mod-test/data/entities.lua": FIXTURE_ENTITIES,
        "mod-test/data/misc.lua": FIXTURE_MISC,
    }
    write_fixture_tree(root, files if files is not None else default_files)
    return root, temporary


def tu_uids(index: ComponentIndex, *, binding: str | None = None) -> set[str]:
    return {
        tu.tu_uid
        for tu in index.tus.values()
        if binding is None or tu.identity_binding == binding
    }


def entity_uids(index: ComponentIndex) -> set[str]:
    return set(index.entities)
