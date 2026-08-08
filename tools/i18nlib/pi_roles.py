"""Isolated curation-role runner (Facts author / curator / Gold A/B / adjudicator).

Each role is a fresh, context-free Pi subprocess that only receives its
bounded bundle and role prompt: no session, no skills, no project context.
The Facts author additionally receives an isolated working directory holding
terminology.tsv and the manifest-pinned public sources (read/bash tools only,
write tools never enabled); every other role runs with ``--no-tools``.

The runner persists the raw model output, the parsed JSON, and the session
artifacts under a per-role run directory, then the main agent validates and
recomputes every hash.  ``isolation_mode=auditable-soft`` is recorded in the
report: the runner never claims system-level isolation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .config import load_manifest
from .errors import AgentError, ValidationError
from .pi_agent import _pi_environment, _write_failure
from .pi_run_options import validate_pi_run_options
from .proposal import decode_json_object, extract_event_stream_output
from .quality import create_quality_run_directory
from .report import atomic_write_bytes, write_json


ROLE_CONTRACTS = {
    "facts-author": "tome4-quality-role-facts-author-v1",
    "curator": "tome4-quality-role-curator-v1",
    "gold-review": "tome4-quality-role-gold-review-v1",
    "adjudicator": "tome4-quality-role-adjudicator-v1",
}

DEFAULT_PROVIDER = "opencode-go"
DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_THINKING = "max"
DEFAULT_TIMEOUT = 3600

#: facts-author may read only this isolated directory (plus terminology/sources
#: symlinked inside it); the host audits the session log afterwards.
AUTHOR_ROLE = "facts-author"
NO_TOOLS_ROLES = ("curator", "gold-review", "adjudicator")


def build_role_command(
    *,
    executable: str,
    provider: str,
    model: str,
    thinking: str,
    system_prompt: str,
    bundle_path: Path,
    role: str,
    instruction: str,
) -> list[str]:
    command = [
        executable,
        "--provider", provider,
        "--model", model,
        "--thinking", thinking,
        "--mode", "json",
        "--no-session",
        "--no-approve",
        "--no-context-files",
        "--no-skills",
        "--no-prompt-templates",
        "--no-themes",
        "--no-extensions",
        "--system-prompt", system_prompt,
        "--print", f"@{bundle_path}",
        instruction,
    ]
    if role == AUTHOR_ROLE:
        command += ["--tools", "read,bash"]
    else:
        command += ["--no-tools"]
    return command


def _extract_output(raw: bytes, label: str) -> dict[str, Any]:
    extracted = extract_event_stream_output(raw, label)
    text = extracted.decode("utf-8").strip()
    # Some models wrap the JSON object in a markdown code fence; strip exactly
    # one leading/trailing fence before strict parsing.
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return decode_json_object(text.encode("utf-8"), label)


def prepare_author_workdir(manifest: Any, run: Path, study_id: str) -> Path:
    """Isolated directory for the Facts author: bundle, terminology, sources."""
    workdir = run / "author-workdir"
    workdir.mkdir(mode=0o700)
    (workdir / "sources").mkdir(mode=0o700)
    terminology = manifest.root / "terminology.tsv"
    if not terminology.is_file():
        raise ValidationError(f"cannot locate terminology.tsv: {terminology}")
    shutil.copy2(terminology, workdir / "terminology.tsv")
    engine_default = manifest.root.parent / "t-engine4"
    engine_root = Path(
        os.environ.get("TOME_ENGINE_ROOT", str(engine_default))
    ).expanduser()
    dlc_root = Path(
        os.environ.get("TOME_DLC_ROOT", str(manifest.root.parent / "tome4-dlcs"))
    ).expanduser()
    links = {
        "engine": engine_root,
        "dlc-ashes-urhrok": dlc_root / "ashes-urhrok",
        "dlc-cults": dlc_root / "cults",
        "dlc-orcs": dlc_root / "orcs",
    }
    readme_lines = [
        f"# Facts-author isolated inputs (study {study_id})",
        "",
        "Allowed inputs: this directory only. terminology.tsv and the public",
        "source trees under sources/ (engine + three official DLCs, GPL v3).",
        "Canonical translations, targets, gold and other artifacts are forbidden.",
        "",
        "Pinned revisions for provenance resources:",
        "- engine: repository=tome4-engine revision=624a67329fe2ad440c5b344785a9c73fcf22ae63",
        "- dlc-ashes-urhrok: repository=tome4-dlc-ashes-urhrok revision=1.7.4",
        "- dlc-cults: repository=tome4-dlc-cults revision=1.7.4",
        "- dlc-orcs: repository=tome4-dlc-orcs revision=1.7.4",
        "- terminology: repository=terminology revision=HEAD logical_path=terminology.tsv",
        "",
        "public-source provenance file_sha256 is the SHA-256 of the file bytes",
        "read from sources/; terminology provenance rows are 1-based TSV rows.",
    ]
    (workdir / "README.txt").write_text("\n".join(readme_lines), encoding="utf-8")
    for name, target in links.items():
        if not target.is_dir():
            raise ValidationError(f"author workdir source missing: {target}")
        link = workdir / "sources" / name
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as error:
            raise ValidationError(f"cannot link author source {name}: {error}") from error
    return workdir


def audit_author_reads(workdir: Path, session_log: Path) -> list[str]:
    """Audit the Facts-author tool calls for reads outside the workdir."""
    if not session_log.is_file():
        return ["no session log available; audit inconclusive"]
    violations: list[str] = []
    workdir_resolved = workdir.resolve()
    try:
        lines = session_log.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ["cannot read session log; audit inconclusive"]
    for line in lines:
        if '"read"' not in line and "tool_use" not in line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        message = event.get("message") if isinstance(event.get("message"), dict) else {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            name = block.get("name")
            tool_input = block.get("input")
            if name not in ("read", "bash") or not isinstance(tool_input, dict):
                continue
            text = str(tool_input.get("path") or tool_input.get("command") or "")
            if name == "read":
                path = Path(text).expanduser()
                if not path.is_absolute():
                    path = (workdir / path).resolve()
                try:
                    in_workdir = path == workdir_resolved or workdir_resolved in path.parents
                except OSError:
                    in_workdir = False
                if not in_workdir:
                    violations.append(f"read outside workdir: {text}")
            elif name == "bash":
                command = text
                if "cd " in command:
                    prefix = command.split("&&", 1)[0].strip()
                    if prefix.startswith("cd "):
                        target = prefix[3:].strip().strip('"').strip("'")
                        if target.startswith("/"):
                            path = Path(target).expanduser()
                            try:
                                if path == workdir_resolved or workdir_resolved in path.parents:
                                    continue
                            except OSError:
                                pass
                for marker in ("~/.pi", "auth.json"):
                    if marker in command:
                        violations.append(f"bash outside workdir: {command[:120]}")
                        break
    return violations


def run_role(
    *,
    role: str,
    bundle_path: Path,
    prompt_path: Path,
    instruction: str,
    output_path: Path,
    study_id: str = "",
    provider: str = DEFAULT_PROVIDER,
    model: str = DEFAULT_MODEL,
    thinking: str = DEFAULT_THINKING,
    timeout: int = DEFAULT_TIMEOUT,
    strict: bool = True,
    pi_executable: str | None = None,
    run_dir: Path | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    validate_pi_run_options(
        provider=provider, model=model, thinking=thinking,
        timeout=timeout, strict=strict,
    )
    if role not in ROLE_CONTRACTS:
        raise ValidationError(f"unknown curation role: {role}")
    manifest = load_manifest()
    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise ValidationError("pi executable is required for curation roles")
    bundle_resolved = bundle_path.expanduser().resolve()
    prompt_resolved = prompt_path.expanduser().resolve()
    bundle = json.loads(bundle_resolved.read_bytes())
    prompt_text = prompt_resolved.read_text(encoding="utf-8")
    system_prompt_path = run_dir / "system-prompt.md" if run_dir else None
    environment = _pi_environment(manifest.root, provider)
    bundle_sha256 = hashlib.sha256(bundle_resolved.read_bytes()).hexdigest()
    prompt_sha256 = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    role_run = run_dir or create_quality_run_directory(
        manifest.root, f"pi-role-{role}"
    )
    role_run.mkdir(parents=True, exist_ok=True)
    role_run.chmod(0o700)
    local_bundle = role_run / "bundle.json"
    write_json(local_bundle, bundle)
    system_prompt_file = role_run / "system-prompt.md"
    system_prompt_file.write_text(prompt_text, encoding="utf-8")
    workdir = None
    if role == AUTHOR_ROLE:
        workdir = prepare_author_workdir(manifest, role_run, study_id)
        shutil.copy2(bundle_resolved, workdir / "bundle.json")
    command = build_role_command(
        executable=executable, provider=provider, model=model, thinking=thinking,
        system_prompt=str(system_prompt_file.resolve()), bundle_path=local_bundle.resolve(),
        role=role, instruction=instruction,
    )
    raw_path = role_run / "raw-output.txt"
    stderr_path = role_run / "pi-stderr.txt"
    report: dict[str, Any] = {
        "contract": ROLE_CONTRACTS[role],
        "schema_version": 1,
        "role": role, "study_id": study_id,
        "provider": provider, "model": model, "thinking": thinking,
        "bundle_sha256": bundle_sha256, "prompt_sha256": prompt_sha256,
        "isolation_mode": "auditable-soft",
        "tools": "read,bash" if role == AUTHOR_ROLE else "none",
        "output": str(output_path), "raw_output": str(raw_path),
        "run_directory": str(role_run),
        "ok": False, "elapsed_seconds": None, "role_report_id": "",
    }
    try:
        if workdir is not None:
            environment["PI_CODING_AGENT_DIR"] = str(role_run / "pi-agent-state")
        result = subprocess.run(
            command, capture_output=True, timeout=timeout, env=environment,
            cwd=str(workdir or role_run),
        )
        atomic_write_bytes(raw_path, result.stdout)
        atomic_write_bytes(stderr_path, result.stderr)
        if result.returncode != 0 or not result.stdout.strip():
            _write_failure(
                report, role_run / "role-report.json",
                f"pi exited with status {result.returncode}: "
                f"{result.stderr.decode('utf-8', errors='replace')[:500]}",
            )
            raise AgentError(report["error"])
        output = _extract_output(result.stdout, f"{role} role output")
        if strict:
            serialized = json.dumps(output, ensure_ascii=False, sort_keys=True)
            json.loads(serialized)
        write_json(output_path, output)
        report.update(
            {
                "ok": True,
                "output_sha256": hashlib.sha256(
                    output_path.read_bytes()
                ).hexdigest(),
                "elapsed_seconds": round(time.monotonic() - started, 6),
            }
        )
    except (subprocess.TimeoutExpired, AgentError, ValidationError) as error:
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        report["error"] = str(error)
        if isinstance(error, subprocess.TimeoutExpired):
            report["error"] = f"role timed out after {timeout}s"
        _write_failure(report, role_run / "role-report.json", report["error"])
        raise
    if role == AUTHOR_ROLE:
        session_log = role_run / "pi-agent-state"
        if session_log.is_dir():
            candidates = sorted(session_log.rglob("*.jsonl"))
            audit = [str(path) for path in candidates]
            violations: list[str] = []
            for path in candidates:
                violations.extend(audit_author_reads(workdir, path))
            report["author_audit"] = {
                "session_logs": audit, "violations": violations,
            }
        else:
            report["author_audit"] = {"session_logs": [], "violations": ["no session log"]}
    report["role_report_id"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in report.items() if key != "role_report_id"},
            ensure_ascii=False, sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    write_json(role_run / "role-report.json", report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tools/pi-quality-role",
        description="Run one isolated curation role (facts-author/curator/gold-review/adjudicator)",
    )
    parser.add_argument("--role", required=True, choices=sorted(ROLE_CONTRACTS))
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--study-id", default="")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--thinking", default=DEFAULT_THINKING)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--pi-executable")
    parser.add_argument("--run-dir", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = run_role(
            role=arguments.role, bundle_path=arguments.bundle,
            prompt_path=arguments.prompt, instruction=arguments.instruction,
            output_path=arguments.output, study_id=arguments.study_id,
            provider=arguments.provider, model=arguments.model,
            thinking=arguments.thinking, timeout=arguments.timeout,
            pi_executable=arguments.pi_executable, run_dir=arguments.run_dir,
        )
    except (AgentError, ValidationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 6 if isinstance(error, AgentError) else 5
    print(f"OK  role={report['role']} model={report['model']} ok={report['ok']}")
    print(f"Output: {report['output']}")
    print(f"Role report: {report['run_directory']}/role-report.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
