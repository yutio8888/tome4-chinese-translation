"""Run a no-tools Pi reviewer against a bounded review bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .errors import AgentError, I18nToolError, ValidationError
from .pi_agent import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_THINKING,
    _pi_environment,
)
from .proposal import decode_json_object
from .report import atomic_write_bytes, create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_TIMEOUT,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    validate_review_bundle,
)
from .config import load_manifest


SEVERITIES = frozenset({"blocker", "major", "minor", "note"})
CATEGORIES = frozenset(
    {"translation", "format", "markup", "code", "security", "scope", "catalog"}
)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid {label}: {path}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def _validate_findings(bundle: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    if output.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ValidationError("Pi review has an unsupported schema")
    if output.get("review_contract") != REVIEW_CONTRACT:
        raise ValidationError("Pi review has an unsupported contract")
    if output.get("bundle_id") != bundle.get("bundle_id"):
        raise ValidationError("Pi review bundle_id does not match")
    findings = output.get("findings")
    if not isinstance(findings, list):
        raise ValidationError("Pi review findings must be an array")
    if len(findings) > 200:
        raise ValidationError("Pi review returned too many findings")
    if bundle.get("kind") == "translations":
        allowed = {
            item.get("item_id")
            for item in bundle.get("items", [])
            if isinstance(item, dict)
        }
    else:
        allowed = {
            item.get("item_id")
            for item in bundle.get("files", [])
            if isinstance(item, dict)
        }
    seen: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"Pi finding {index} is not an object")
        finding_id = finding.get("finding_id")
        if not isinstance(finding_id, str) or not finding_id:
            raise ValidationError(f"Pi finding {index} has no finding_id")
        if finding_id in seen:
            raise ValidationError(f"Pi findings contain duplicate finding_id: {finding_id}")
        seen.add(finding_id)
        if finding.get("severity") not in SEVERITIES:
            raise ValidationError(f"Pi finding {index} has an invalid severity")
        if finding.get("category") not in CATEGORIES:
            raise ValidationError(f"Pi finding {index} has an invalid category")
        if finding.get("item_id") not in allowed:
            raise ValidationError(f"Pi finding {index} references an unknown item_id")
        for key in ("title", "body"):
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                raise ValidationError(f"Pi finding {index} has no {key}")
        if "suggested_fix" in finding and not isinstance(
            finding.get("suggested_fix"), str
        ):
            raise ValidationError(f"Pi finding {index} has an invalid suggested_fix")
        if "path" in finding and finding.get("path") is not None:
            path = finding.get("path")
            if not isinstance(path, str) or Path(path).is_absolute() or ".." in Path(path).parts:
                raise ValidationError(f"Pi finding {index} has an unsafe path")
    return {
        "ok": True,
        "findings": len(findings),
        "blockers": sum(item.get("severity") == "blocker" for item in findings),
        "majors": sum(item.get("severity") == "major" for item in findings),
        "minors": sum(item.get("severity") == "minor" for item in findings),
        "notes": sum(item.get("severity") == "note" for item in findings),
    }


def run_pi_review(
    *,
    bundle_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    pi_executable: str | None = None,
) -> dict[str, Any]:
    manifest = load_manifest()
    bundle_resolved = bundle_path.expanduser().resolve()
    bundle = validate_review_bundle(manifest, bundle_resolved)
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")
    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")

    run_directory = create_run_directory(manifest.root, "pi-review")
    run_directory.chmod(0o700)
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    review_path = run_directory / "review.json"
    report_path = run_directory / "pi-review.json"
    prompt_path = manifest.root / "i18n" / "prompts" / "pi-reviewer.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi reviewer prompt: {prompt_path}") from error

    report: dict[str, Any] = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_contract": REVIEW_CONTRACT,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "bundle": str(bundle_resolved),
        "bundle_id": bundle["bundle_id"],
        "kind": bundle["kind"],
        "prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "run_directory": str(run_directory),
        "raw_output": str(raw_output_path),
        "report": str(report_path),
    }
    inventory = (
        [item.get("item_id") for item in bundle.get("items", [])]
        if bundle.get("kind") == "translations"
        else [item.get("item_id") for item in bundle.get("files", [])]
    )
    command = [
        executable,
        "--provider",
        provider,
        "--model",
        model,
        "--thinking",
        thinking,
        "--mode",
        "text",
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
        f"@{bundle_resolved}",
        "Review only this bundle and return the required JSON object. Do not omit the envelope. "
        "The exact allowed item_id inventory for this bundle is "
        f"{json.dumps(inventory, ensure_ascii=False)}; copy item_id values verbatim, never use paths.",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=run_directory,
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
        report["error"] = f"Pi timed out after {timeout} seconds"
        write_json(report_path, report)
        raise AgentError(f"Pi timed out after {timeout} seconds; report: {report_path}")
    except OSError as error:
        report["error"] = f"cannot start Pi: {error}"
        write_json(report_path, report)
        raise AgentError(f"cannot start Pi: {error}; report: {report_path}") from error

    atomic_write_bytes(raw_output_path, result.stdout)
    if result.stderr:
        atomic_write_bytes(stderr_path, result.stderr)
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = result.returncode
    report["raw_output_sha256"] = hashlib.sha256(result.stdout).hexdigest()
    if result.returncode != 0:
        report["error"] = f"Pi exited with status {result.returncode}"
        write_json(report_path, report)
        raise AgentError(f"Pi exited with status {result.returncode}; report: {report_path}")
    if not result.stdout.strip():
        report["error"] = "Pi returned an empty response"
        write_json(report_path, report)
        raise AgentError(f"Pi returned an empty response; report: {report_path}")
    try:
        output = decode_json_object(result.stdout, "Pi review output")
        summary = _validate_findings(bundle, output)
    except ValidationError as error:
        report["error"] = str(error)
        write_json(report_path, report)
        raise AgentError(f"Pi review validation failed: {error}; report: {report_path}") from error

    output["review_id"] = _canonical_sha256(output)
    write_json(review_path, output)
    report.update({"ok": True, "summary": summary, "review": str(review_path)})
    write_json(report_path, report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/pi-review",
        description="Run a no-tools Pi reviewer against a bounded review bundle",
    )
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER))
    parser.add_argument("--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING))
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_REVIEW_TIMEOUT,
        help="Pi time limit per review bundle in seconds (default: 1200 / 20 minutes)",
    )
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="reject malformed findings (default: true)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    try:
        report = run_pi_review(
            bundle_path=arguments.bundle,
            provider=arguments.provider,
            model=arguments.model,
            thinking=arguments.thinking,
            timeout=arguments.timeout,
            strict=arguments.strict,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        return error.exit_code
    summary = report["summary"]
    print(
        f"OK  Pi review {report['bundle_id'][:16]}  "
        f"kind={report['kind']} findings={summary['findings']}"
    )
    print(f"Review: {report['review']}")
    print(f"Report: {report['report']}")
    return 0
