"""Constrained Pi translator that can only return a validated proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .config import load_manifest
from .errors import AgentError, I18nToolError, ValidationError
from .proposal import decode_json_object, extract_event_stream_output, read_json_object, validate_proposal
from .report import atomic_write_bytes, create_run_directory, write_json
from .workset import proposal_template_for, validate_workset


DEFAULT_PROVIDER = "opencode-go"
DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_THINKING = "high"
MAX_WORKSET_ITEMS = 50


def _credential_from_pi_auth(path: Path, provider: str = "opencode-go") -> str | None:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict):
        return None
    credential = value.get(provider)
    if not isinstance(credential, dict) or credential.get("type") != "api_key":
        return None
    key = credential.get("key")
    if not isinstance(key, str) or not key or key.startswith("!") or "$" in key:
        return None
    return key


def _credential_from_keychain() -> str | None:
    security = Path("/usr/bin/security")
    if not security.is_file():
        return None
    try:
        result = subprocess.run(
            [
                str(security),
                "find-generic-password",
                "-s",
                "codex-pi-opencode-go",
                "-w",
            ],
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    try:
        key = result.stdout.decode("utf-8").strip()
    except UnicodeDecodeError:
        return None
    return key or None


def _pi_environment(root: Path, provider: str) -> dict[str, str]:
    environment = os.environ.copy()
    if provider == "opencode-go" and not environment.get("OPENCODE_API_KEY"):
        auth_path = Path(
            environment.get(
                "PI_SUBAGENT_PI_AUTH_FILE",
                str(Path.home() / ".pi" / "agent" / "auth.json"),
            )
        ).expanduser()
        key = _credential_from_pi_auth(auth_path) or _credential_from_keychain()
        if key is None:
            raise AgentError(
                "no OpenCode Go credential is available; configure Pi, "
                "OPENCODE_API_KEY, or the codex-pi-opencode-go Keychain item"
            )
        environment["OPENCODE_API_KEY"] = key
    if provider == "deepseek" and not environment.get("DEEPSEEK_API_KEY"):
        auth_path = Path(
            environment.get(
                "PI_SUBAGENT_PI_AUTH_FILE",
                str(Path.home() / ".pi" / "agent" / "auth.json"),
            )
        ).expanduser()
        key = _credential_from_pi_auth(auth_path, provider="deepseek")
        if key is None:
            raise AgentError(
                "no DeepSeek credential is available; configure Pi "
                "(login with provider deepseek) or set DEEPSEEK_API_KEY"
            )
        environment["DEEPSEEK_API_KEY"] = key
    agent_directory = root / ".artifacts" / "i18n" / "pi-agent"
    agent_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    agent_directory.chmod(0o700)
    environment.update(
        {
            "PI_CODING_AGENT_DIR": str(agent_directory),
            "PI_SKIP_VERSION_CHECK": "1",
            "PI_TELEMETRY": "0",
        }
    )
    return environment


def _write_failure(
    report: dict[str, Any], report_path: Path, message: str
) -> None:
    report.update({"ok": False, "error": message})
    write_json(report_path, report)


def build_translation_command(
    *,
    executable: str,
    provider: str,
    model: str,
    thinking: str,
    system_prompt: str,
    workset_resolved: Path,
    template_path: Path,
) -> list[str]:
    return [
        executable,
        "--provider",
        provider,
        "--model",
        model,
        "--thinking",
        thinking,
        "--mode",
        "json",
        "--no-session",
        "--no-approve",
        "--no-context-files",
        "--no-skills",
        "--no-prompt-templates",
        "--no-themes",
        "--no-extensions",
        "--no-tools",
        "--system-prompt",
        system_prompt,
        "--print",
        f"@{workset_resolved}",
        f"@{template_path}",
        (
            "Translate every workset item and return only the completed proposal "
            "JSON object. Do not omit entries."
        ),
    ]


def run_pi_translation(
    *,
    workset_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    pi_executable: str | None = None,
) -> dict[str, Any]:
    manifest = load_manifest()
    workset_resolved, workset, _ = read_json_object(workset_path, "workset")
    validate_workset(manifest, workset)
    items = workset["items"]
    if len(items) > MAX_WORKSET_ITEMS:
        raise ValidationError(
            f"Pi worksets are limited to {MAX_WORKSET_ITEMS} items; split this workset"
        )

    template_value = proposal_template_for(workset)
    template_raw_path = workset.get("proposal_template")
    if not isinstance(template_raw_path, str):
        raise ValidationError("workset has no proposal_template path")
    template_path, on_disk_template, _ = read_json_object(
        Path(template_raw_path), "proposal template"
    )
    if on_disk_template != template_value:
        raise ValidationError("proposal template is stale or does not match the workset")

    prompt_path = manifest.root / "i18n" / "prompts" / "pi-translator.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi translator prompt: {prompt_path}") from error
    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")

    run_directory = create_run_directory(manifest.root, "pi-translate")
    run_directory.chmod(0o700)
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    proposal_path = run_directory / "proposal.json"
    report_path = run_directory / "pi-translation.json"
    report: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "workset": str(workset_resolved),
        "workset_id": workset["workset_id"],
        "component": workset["component"],
        "items": len(items),
        "prompt": str(prompt_path),
        "prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "run_directory": str(run_directory),
        "raw_output": str(raw_output_path),
        "report": str(report_path),
    }
    command = build_translation_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        workset_resolved=workset_resolved,
        template_path=template_path,
    )
    try:
        result = subprocess.run(
            command,
            cwd=manifest.root,
            env=_pi_environment(manifest.root, provider),
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        atomic_write_bytes(raw_output_path, stdout)
        atomic_write_bytes(stderr_path, stderr)
        report["stderr"] = str(stderr_path)
        _write_failure(report, report_path, f"Pi timed out after {timeout} seconds")
        raise AgentError(f"Pi timed out after {timeout} seconds; report: {report_path}")
    except OSError as error:
        _write_failure(report, report_path, f"cannot start Pi: {error}")
        raise AgentError(f"cannot start Pi: {error}; report: {report_path}") from error

    atomic_write_bytes(raw_output_path, result.stdout)
    if result.stderr:
        atomic_write_bytes(stderr_path, result.stderr)
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = result.returncode
    report["raw_output_sha256"] = hashlib.sha256(result.stdout).hexdigest()
    if result.returncode != 0:
        _write_failure(report, report_path, f"Pi exited with status {result.returncode}")
        raise AgentError(
            f"Pi exited with status {result.returncode}; report: {report_path}"
        )
    if not result.stdout.strip():
        _write_failure(report, report_path, "Pi returned an empty response")
        raise AgentError(f"Pi returned an empty response; report: {report_path}")
    try:
        output_value = decode_json_object(
            extract_event_stream_output(result.stdout, "Pi output"),
            "Pi output",
        )
    except ValidationError as error:
        _write_failure(report, report_path, str(error))
        raise AgentError(f"{error}; Pi report: {report_path}") from error
    if set(output_value) == {"proposals"}:
        output_value = {
            "schema_version": 1,
            "workset_id": workset["workset_id"],
            "proposals": output_value["proposals"],
        }
        report["normalization"] = "added-deterministic-envelope"
    else:
        report["normalization"] = "none"
    write_json(proposal_path, output_value)
    report["proposal"] = str(proposal_path)

    try:
        validation = validate_proposal(
            manifest,
            workset_path=workset_resolved,
            proposal_path=proposal_path,
            allow_partial=False,
            strict=strict,
        )
    except I18nToolError as error:
        _write_failure(report, report_path, str(error))
        raise type(error)(f"{error}; Pi report: {report_path}") from error
    report["proposal_validation"] = validation["report"]
    report["proposal_id"] = validation["proposal_id"]
    report["errors"] = validation["errors"]
    report["warnings"] = validation["warnings"]
    if not validation["ok"]:
        _write_failure(
            report,
            report_path,
            f"proposal validation failed with {validation['errors']} errors and "
            f"{validation['warnings']} warnings",
        )
        raise ValidationError(
            f"Pi proposal failed validation; report: {report_path}"
        )
    report["ok"] = True
    report["validated_proposal"] = validation["validated_proposal"]
    write_json(report_path, report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/pi-subagent",
        description="Run a no-tools Pi translator and validate its structured proposal",
    )
    parser.add_argument("--workset", required=True, type=Path)
    parser.add_argument(
        "--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER)
    )
    parser.add_argument("--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL))
    parser.add_argument(
        "--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING)
    )
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="block proposal warnings (default: true)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    try:
        report = run_pi_translation(
            workset_path=arguments.workset,
            provider=arguments.provider,
            model=arguments.model,
            thinking=arguments.thinking,
            timeout=arguments.timeout,
            strict=arguments.strict,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    print(
        f"OK  Pi proposal {report['proposal_id'][:16]}  "
        f"items={report['items']} errors={report['errors']} warnings={report['warnings']}"
    )
    print(f"Validated: {report['validated_proposal']}")
    print(f"Report: {report['report']}")
    return 0
