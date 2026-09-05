"""Toolchain tests: contracts."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT, TOOLS
import contextlib
import hashlib
import io
import sys
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml
import paseo_contract_check


class CiGatesScriptTests(unittest.TestCase):
    def test_public_shell_delegates_and_propagates_failure(self):
        # Only intercept the shell's interpreter launch. Runner behavior and
        # command/log coverage are tested through its Python execution seam.
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "python3"
            fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\nexit 17\n')
            fake.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"])
            for arguments in ([], ["--skip-build"]):
                result = subprocess.run([str(TOOLS / "ci-gates.sh"), *arguments],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 17)
                self.assertEqual(result.stdout.splitlines(),
                                 ["-B", str(TOOLS / "ci_gates.py"), *arguments])
            for arguments in (["--unknown"], ["--skip-build", "extra"]):
                result = subprocess.run([str(TOOLS / "ci-gates.sh"), *arguments],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("Usage:", result.stderr)


class ProjectSubagentDefinitionTests(unittest.TestCase):
    """Validate project role definitions and the role-only Paseo routing contract."""

    ARCHIVE_AGENTS_DIR = ROOT / "archive" / ".pi" / "agents"
    ARCHIVE_EXTENSION_DIR = ROOT / "archive" / ".pi" / "extensions" / "subagent"
    ARCHIVE_SKILLS_DIR = ROOT / "archive" / ".agents" / "skills"
    ARCHIVE_SKILL_DIR = ROOT / "archive" / ".agents" / "skills" / "tome4-pi-subagent"
    CONTRACT_DOC = ROOT / "archive" / "docs" / "pi-review-v2-contract.md"
    def _frontmatter(self, path: Path) -> dict:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            self.fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")
        end = text.index("\n---", 4)
        return yaml.safe_load(text[4:end])

    def _normative_texts(self) -> dict[str, str]:
        return {
            "agents": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "orchestrator": (ROOT / ".ai" / "roles" / "orchestrator.md").read_text(
                encoding="utf-8"
            ),
            "executor": (ROOT / ".ai" / "roles" / "executor.md").read_text(
                encoding="utf-8"
            ),
            "reviewer": (ROOT / ".ai" / "roles" / "reviewer.md").read_text(
                encoding="utf-8"
            ),
            "senior": (ROOT / ".ai" / "roles" / "senior-reviewer.md").read_text(
                encoding="utf-8"
            ),
            "scout": (ROOT / ".ai" / "roles" / "scout.md").read_text(
                encoding="utf-8"
            ),
            "contract": (
                ROOT / "docs" / "paseo-orchestration-v2-contract.md"
            ).read_text(encoding="utf-8"),
        }

    def test_archived_agents_exist_with_required_frontmatter(self) -> None:
        expected = {"scout", "plan-reviewer"}
        found = {path.stem for path in self.ARCHIVE_AGENTS_DIR.glob("*.md")}
        self.assertEqual(found, expected)
        for path in sorted(self.ARCHIVE_AGENTS_DIR.glob("*.md")):
            with self.subTest(agent=path.stem):
                meta = self._frontmatter(path)
                self.assertIsInstance(meta.get("name"), str)
                self.assertIsInstance(meta.get("description"), str)
                tools = meta.get("tools")
                self.assertIsInstance(tools, str)
                allowed = {tool.strip() for tool in tools.split(",")}
                self.assertLessEqual(allowed, {"read", "grep", "find", "ls", "bash"})
                self.assertEqual(meta.get("systemPromptMode"), "replace")
                self.assertFalse(meta.get("inheritProjectContext"))
                self.assertFalse(meta.get("inheritSkills"))

    def test_archived_extension_files_exist(self) -> None:
        for name in ("agents.ts", "index.ts", "live-output.mjs"):
            self.assertTrue((self.ARCHIVE_EXTENSION_DIR / name).is_file(), name)
        index = (self.ARCHIVE_EXTENSION_DIR / "index.ts").read_text(encoding="utf-8")
        self.assertIn("--no-approve", index)
        self.assertIn("--no-context-files", index)
        self.assertIn("--no-skills", index)
        self.assertNotIn("--approve", index.replace("--no-approve", ""))

    def test_archived_skill_and_contract_doc_exist(self) -> None:
        self.assertTrue((self.ARCHIVE_SKILL_DIR / "SKILL.md").is_file())
        skill = (self.ARCHIVE_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("scout", skill)
        self.assertIn("plan-reviewer", skill)
        self.assertTrue(self.CONTRACT_DOC.is_file())
        contract = self.CONTRACT_DOC.read_text(encoding="utf-8")
        self.assertIn("selection_sha256", contract)
        self.assertIn("/private/tmp", contract)
        self.assertIn("/tmp", contract)

    def test_project_skills_are_archived(self) -> None:
        skill_names = ("tome4-pi-review", "tome4-pi-file-review", "tome4-pi-subagent")
        for name in skill_names:
            with self.subTest(skill=name):
                path = self.ARCHIVE_SKILLS_DIR / name / "SKILL.md"
                meta = self._frontmatter(path)
                self.assertIn("Paseo 未激活", meta["description"])
                self.assertIn("Paseo 激活后不得使用", meta["description"])

        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        orchestrator = (ROOT / ".ai" / "roles" / "orchestrator.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("已归档", agents)
        self.assertIn("角色独占路由", orchestrator)
        for name in skill_names:
            self.assertIn("$" + name, agents)
            self.assertIn("$" + name, orchestrator)


    @staticmethod
    def _normalized_markdown(text: str) -> str:
        return " ".join(text.split())


    def test_plan_state_starts_with_empty_dispatch_history(self) -> None:
        contract = self._normative_texts()["contract"]
        state_section = contract[contract.index("### 最小 STATE") :]
        json_start = state_section.index("```json") + len("```json\n")
        json_end = state_section.index("\n```", json_start)
        state = json.loads(state_section[json_start:json_end])
        self.assertEqual(state["state"], "PLAN")
        self.assertEqual(state["child_dispatches"], [])


class PaseoTranslationContextReviewTests(unittest.TestCase):
    """Validate the role-only translation_contextual_v1 contract."""

    CONTEXTUAL_DOC = ROOT / "docs" / "paseo-translation-context-review-v1-contract.md"

    def _texts(self) -> dict[str, str]:
        return {
            "agents": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "orchestrator": (ROOT / ".ai" / "roles" / "orchestrator.md").read_text(
                encoding="utf-8"
            ),
            "reviewer": (ROOT / ".ai" / "roles" / "reviewer.md").read_text(
                encoding="utf-8"
            ),
            "contract": (
                ROOT / "docs" / "paseo-orchestration-v2-contract.md"
            ).read_text(encoding="utf-8"),
            "contextual": self.CONTEXTUAL_DOC.read_text(encoding="utf-8"),
        }

    @staticmethod
    def _canonical_bytes(payload: dict[str, object]) -> bytes:
        return json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

    @staticmethod
    def _minimal_payload() -> dict[str, object]:
        return {
            "contract": "translation_contextual_v1",
            "ordered_revision_keys": ["r1"],
            "translation_snapshot": [
                {"revision_key": "r1", "source": "Hello world", "target": "你好，世界"}
            ],
            "fixed_source_identity": "commit:61bb370c33e46c4df4b2bbfd56113a0de1822300",
            "terminology_snapshot": "术语：zone=区域",
            "bounded_context": [
                {"revision_key": "r1", "context": "tag=talents/foo; nearby: A, B"}
            ],
            "rendered_briefing": "有界语境审核 briefing：revision r1",
        }


    def test_contextual_payload_has_no_runtime_component(self) -> None:
        payload = self._minimal_payload()
        encoded = self._canonical_bytes(payload)
        self.assertEqual(
            hashlib.sha256(encoded).hexdigest(),
            "65f5ea8778a47fa96537d72de55f28b899e7f6ad1df9d2ac3c71772d4d71b8d9",
        )

    def test_contextual_payload_identity_changes_with_content(self) -> None:
        payload = self._minimal_payload()
        base = self._canonical_bytes(payload)
        changed = dict(payload, fixed_source_identity="commit:" + "0" * 40)
        self.assertNotEqual(self._canonical_bytes(changed), base)
        changed = dict(payload, ordered_revision_keys=["r2"])
        self.assertNotEqual(self._canonical_bytes(changed), base)
        changed = dict(payload, rendered_briefing="changed")
        self.assertNotEqual(self._canonical_bytes(changed), base)


    def test_contextual_short_prompt_is_three_lines_and_bounded(self) -> None:
        contextual = self._texts()["contextual"]
        match = re.search(r"## 四、短派发 prompt.*?~~~text\n(.*?)\n~~~", contextual, re.S)
        self.assertIsNotNone(match)
        prompt = match.group(1)
        lines = prompt.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("任务："))
        self.assertTrue(lines[1].startswith("输入："))
        self.assertTrue(lines[2].startswith("输出："))
        self.assertLessEqual(len(prompt.encode("utf-8")), 800)
        self.assertEqual(
            re.findall(r"<[^>]+>", prompt),
            ["<candidate_identity>", "<input_path>", "<candidate_identity>"],
        )
        self.assertIn("全程只读", prompt)
        self.assertIn("冻结顺序全量覆盖", prompt)
        self.assertNotIn("runtime_tuple", prompt)
        self.assertNotIn("source/target", prompt)


class PaseoRuntimeNeutralContractTests(unittest.TestCase):
    """Ensure the old mode-specific contract has no active assertions left."""


    def test_quality_and_archive_surfaces_are_not_moved(self) -> None:
        quality = (ROOT / "docs" / "translation-quality-evaluator-v3.md").read_text(
            encoding="utf-8"
        )
        archive = (
            ROOT / "archive" / "docs" / "pi-review-v2-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("provider", quality)
        self.assertIn("model", quality)
        self.assertIn("selection_sha256", archive)


class PaseoClauseIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="paseo-clause-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for relative in paseo_contract_check.ACTIVE_FILES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())

    def check(self):
        with patch.object(paseo_contract_check, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return paseo_contract_check.main()

    def test_active_declarations_and_versions_pass(self):
        self.assertEqual(self.check(), 0)
        text = (self.root / paseo_contract_check.ROLE_CONTRACT_PATH).read_text()
        self.assertEqual(len(paseo_contract_check.declarations(text)), 16)

    def test_each_canonical_declaration_removal_fails_despite_references(self):
        path = self.root / paseo_contract_check.ROLE_CONTRACT_PATH
        source = path.read_text()
        for clause in sorted(paseo_contract_check.EXPECTED_CLAUSES):
            with self.subTest(clause=clause):
                mutated, count = re.subn(r"^\| `" + re.escape(clause) + r"` \|[^\n]+\n", "", source, flags=re.M)
                self.assertEqual(count, 1)
                path.write_text(mutated + "\nReference: `" + clause + "`\n")
                self.assertEqual(self.check(), 1)
        path.write_text(source)

    def test_duplicate_unknown_and_malformed_declarations_fail(self):
        path = self.root / paseo_contract_check.ROLE_CONTRACT_PATH
        source = path.read_text()
        row = paseo_contract_check.DECLARATION_ROW.search(source).group()
        for replacement in (row + "\n" + row, row.replace("P2-SINGLE-WRITER", "P2-UNKNOWN"), row.replace("` |", " |", 1)):
            with self.subTest(replacement=replacement):
                path.write_text(source.replace(row, replacement, 1))
                self.assertEqual(self.check(), 1)

    def test_prose_changes_in_every_active_document_pass(self):
        for relative in paseo_contract_check.ACTIVE_FILES:
            path = self.root / relative
            source = path.read_text()
            # Rewrite prose punctuation throughout, keeping declaration syntax
            # and the live version header intact.
            changed = []
            for line in source.splitlines(True):
                if '契约版本：' in line or line.startswith('版本 `'):
                    changed.append(line)
                else:
                    changed.append(line.replace('。', '！').replace('必须', '须'))
            with self.subTest(document=relative):
                path.write_text(''.join(changed))
                self.assertEqual(self.check(), 0)
            path.write_text(source)

    def test_each_live_version_missing_malformed_mismatched_or_duplicate_fails(self):
        for relative, version in paseo_contract_check.CONTRACT_VERSIONS.items():
            path = self.root / relative
            source = path.read_text()
            line = next(line for line in source.splitlines(True) if '契约版本：' in line or line.startswith('版本 `'))
            variants = ('', line.replace(version, 'malformed'), line.replace(version, version + '-wrong'), line + line, line.replace('版本', '历史版本', 1), line.replace(version, '`' + version), line.replace(version, version + '`'))
            for replacement in variants:
                with self.subTest(document=relative, replacement=replacement):
                    path.write_text(source.replace(line, replacement, 1) + '\n## History\n' + line)
                    self.assertEqual(self.check(), 1)
            path.write_text(source)

    def test_role_references_missing_unknown_or_unlinked_fail(self):
        for relative, clauses in paseo_contract_check.ROLE_CLAUSE_REFERENCES.items():
            path = self.root / relative
            source = path.read_text()
            for mutated in (source.replace(clauses[0], ''), source + '\nP2-UNDECLARED\n', source.replace(paseo_contract_check.ROLE_CONTRACT_PATH, 'missing.md')):
                with self.subTest(role=relative):
                    path.write_text(mutated)
                    self.assertEqual(self.check(), 1)
            path.write_text(source)

    def test_missing_or_invalid_utf8_active_document_fails(self):
        for relative in paseo_contract_check.ACTIVE_FILES:
            path = self.root / relative
            source = path.read_bytes()
            with self.subTest(document=relative):
                path.unlink()
                self.assertEqual(self.check(), 1)
                path.write_bytes(b'\xff')
                self.assertEqual(self.check(), 1)
            path.write_bytes(source)


if __name__ == "__main__":
    unittest.main()
