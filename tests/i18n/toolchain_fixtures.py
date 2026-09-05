"""Shared toolchain fixtures; no TestCase classes or aggregate discovery."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
TEST_FIXTURE_BASE = ROOT / ".artifacts" / "i18n" / "test-fixtures"
TEST_FIXTURE_BASE.mkdir(parents=True, exist_ok=True)
_TEST_FIXTURE_DIRECTORY = tempfile.TemporaryDirectory(
    prefix="toolchain-", dir=TEST_FIXTURE_BASE
)
TEST_FIXTURE_ROOT = Path(_TEST_FIXTURE_DIRECTORY.name)
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.lint import Policy, stable_entry_id
from i18nlib.locale_model import LocaleDocument
from i18nlib.workset import create_workset


EMPTY_POLICY = Policy(frozenset(), frozenset(), frozenset())
_UNSET = object()


def create_workset_fixture(
    manifest: object,
    directory: Path,
    *,
    previous_special: object = _UNSET,
) -> tuple[dict[str, object], Path, Path]:
    component = "boot"
    section = "fixture/dialog.lua"
    source = "%s has %d"
    source_tag = "tformat"
    item = {
        "entry_id": stable_entry_id(component, section, source, source_tag),
        "component": component,
        "section": section,
        "source": source,
        "source_tag": source_tag,
        "classification": "added",
        "origins": [
            {"document": "generated:fixture", "kind": "extracted", "line": 1}
        ],
    }
    if previous_special is not _UNSET:
        item["previous_special"] = previous_special
    fixture_root = TEST_FIXTURE_ROOT / directory.name
    fixture_root.mkdir(parents=True, exist_ok=True)
    merge_path = fixture_root / "merge.json"
    merge_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "merge_id": "a" * 64,
                "component": component,
                "untranslated": [item],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    workset = create_workset(
        manifest,
        merge_report_path=merge_path,
        limit=10,
        section_prefix=None,
        classification="all",
    )
    workset_path = Path(str(workset["output"]))
    proposal_path = directory / "proposal.json"
    proposal = json.loads(Path(str(workset["proposal_template"])).read_text())
    proposal["proposals"][0]["target"] = "%d 属于 %s"
    proposal["proposals"][0]["args_order"] = [2, 1]
    proposal_path.write_text(
        json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
    )
    return workset, workset_path, proposal_path


def _component_selection_document(
    logical_path: str, source: str | None = None
) -> LocaleDocument:
    records: tuple[dict[str, object], ...] = ()
    if source is not None:
        records = (
            {
                "kind": "translation",
                "section": logical_path,
                "source": source,
                "target": f"translated {source}",
                "source_tag": None,
                "args_order": None,
                "special": None,
            },
        )
    return LocaleDocument(
        logical_path=logical_path,
        sha256="0" * 64,
        records=records,
    )
