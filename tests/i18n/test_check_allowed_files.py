from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check_allowed_files as caf


class LoadAllowedFilesTests(unittest.TestCase):
    def test_missing_scope_file_fails_closed(self) -> None:
        with patch.object(caf, "ROOT", Path(tempfile.mkdtemp())):
            with self.assertRaises(FileNotFoundError):
                caf.load_allowed_files("no-such-task")

    def test_empty_allowed_files_rejected(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        task_dir = tmp / ".ai" / "task" / "t1"
        task_dir.mkdir(parents=True)
        (task_dir / "SCOPE.json").write_text(json.dumps({"allowed_files": []}))
        with patch.object(caf, "ROOT", tmp):
            with self.assertRaises(ValueError):
                caf.load_allowed_files("t1")

    def test_valid_scope_file_loads(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        task_dir = tmp / ".ai" / "task" / "t1"
        task_dir.mkdir(parents=True)
        (task_dir / "SCOPE.json").write_text(
            json.dumps({"allowed_files": ["tome-cults.lua", "docs/foo.md"]})
        )
        with patch.object(caf, "ROOT", tmp):
            self.assertEqual(
                caf.load_allowed_files("t1"), ["tome-cults.lua", "docs/foo.md"]
            )


class MainTests(unittest.TestCase):
    def _make_task(self, tmp: Path, task_id: str, allowed: list[str]) -> None:
        task_dir = tmp / ".ai" / "task" / task_id
        task_dir.mkdir(parents=True)
        (task_dir / "SCOPE.json").write_text(json.dumps({"allowed_files": allowed}))

    def test_in_scope_paths_pass(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self._make_task(tmp, "t1", ["tome-cults.lua"])
        with patch.object(caf, "ROOT", tmp):
            with patch.object(sys, "argv", ["check_allowed_files.py", "--task-id", "t1", "--paths", "tome-cults.lua"]):
                self.assertEqual(caf.main(), 0)

    def test_out_of_scope_path_fails(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self._make_task(tmp, "t1", ["tome-cults.lua"])
        with patch.object(caf, "ROOT", tmp):
            with patch.object(
                sys, "argv",
                ["check_allowed_files.py", "--task-id", "t1", "--paths", "tome-cults.lua", "tome-orcs.lua"],
            ):
                self.assertEqual(caf.main(), 1)

    def test_no_scope_file_fails_closed_via_main(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        (tmp / ".ai" / "task").mkdir(parents=True)
        with patch.object(caf, "ROOT", tmp):
            with patch.object(sys, "argv", ["check_allowed_files.py", "--task-id", "missing", "--paths", "x.lua"]):
                self.assertEqual(caf.main(), 1)

    def test_no_changed_paths_is_ok(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self._make_task(tmp, "t1", ["tome-cults.lua"])
        with patch.object(caf, "ROOT", tmp):
            with patch.object(sys, "argv", ["check_allowed_files.py", "--task-id", "t1", "--paths"]):
                self.assertEqual(caf.main(), 0)


if __name__ == "__main__":
    unittest.main()
