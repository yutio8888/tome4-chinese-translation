"""Run an isolated Pi remediation pass over validated review findings."""

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
from .config import load_manifest
from .errors import AgentError, I18nToolError, ValidationError
from .pi_agent import DEFAULT_MODEL, DEFAULT_PROVIDER, DEFAULT_THINKING, _pi_environment
from .proposal import decode_json_object, extract_event_stream_output
from .report import atomic_write_bytes, create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_TIMEOUT,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    _read_bundle,
    _validate_findings_for_remediation,
    validate_review_bundle,
)


REMEDIATION_CONTRACT = "tome4-review-remediation-v1"
REMEDIATION_ACTIONS = frozenset(
    {"replace-translation", "patch-code", "no-change"}
)


def _read_review(path: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read validated review: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid validated review: {path}") from error
    if not isinstance(value, dict):
        raise ValidationError("validated review must be an object")
    if value.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ValidationError("validated review has an unsupported schema")
    if value.get("review_contract") != REVIEW_CONTRACT:
        raise ValidationError("validated review has an unsupported contract")
    if value.get("bundle_id") != bundle.get("bundle_id"):
        raise ValidationError("validated review bundle_id does not match")
    _validate_findings_for_remediation(bundle, value)
    return value


def _validate_remediation(
    bundle: dict[str, Any], review: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    if output.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ValidationError("Pi remediation has an unsupported schema")
    if output.get("remediation_contract") != REMEDIATION_CONTRACT:
        raise ValidationError("Pi remediation has an unsupported contract")
    if output.get("bundle_id") != bundle.get("bundle_id"):
        raise ValidationError("Pi remediation bundle_id does not match")
    if output.get("review_id") != review.get("review_id"):
        raise ValidationError("Pi remediation review_id does not match")
    proposals = output.get("proposals")
    if not isinstance(proposals, list):
        raise ValidationError("Pi remediation proposals must be an array")

    if bundle.get("kind") == "translations":
        items = {
            item.get("item_id"): item
            for item in bundle.get("items", [])
            if isinstance(item, dict)
        }
    else:
        items = {
            item.get("item_id"): item
            for item in bundle.get("files", [])
            if isinstance(item, dict)
        }
    findings = {
        item.get("finding_id"): item
        for item in review.get("findings", [])
        if isinstance(item, dict)
    }
    seen: set[str] = set()
    for index, proposal in enumerate(proposals):
        if not isinstance(proposal, dict):
            raise ValidationError(f"Pi remediation proposal {index} is not an object")
        finding_id = proposal.get("finding_id")
        item_id = proposal.get("item_id")
        action = proposal.get("action")
        if finding_id not in findings or item_id not in items:
            raise ValidationError(f"Pi remediation proposal {index} references unknown finding/item")
        if finding_id in seen:
            raise ValidationError(f"Pi remediation contains duplicate finding_id: {finding_id}")
        if findings[finding_id].get("item_id") != item_id:
            raise ValidationError(f"Pi remediation proposal {index} mismatches finding item_id")
        if action not in REMEDIATION_ACTIONS:
            raise ValidationError(f"Pi remediation proposal {index} has invalid action")
        rationale = proposal.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValidationError(f"Pi remediation proposal {index} has no rationale")
        seen.add(finding_id)
        if bundle.get("kind") == "translations" and action == "replace-translation":
            item = items[item_id]
            for key in ("source", "source_tag", "original_target"):
                expected = item.get("target") if key == "original_target" else item.get(key)
                if proposal.get(key) != expected:
                    raise ValidationError(
                        f"Pi remediation proposal {index} does not preserve {key}"
                    )
            if not isinstance(proposal.get("target"), str) or not proposal["target"].strip():
                raise ValidationError(f"Pi remediation proposal {index} has no target")
            args_order = proposal.get("args_order")
            if args_order is not None and (
                not isinstance(args_order, list)
                or not all(isinstance(value, int) and not isinstance(value, bool) for value in args_order)
            ):
                raise ValidationError(f"Pi remediation proposal {index} has invalid args_order")
        if bundle.get("kind") == "code" and action == "patch-code":
            path = proposal.get("path")
            patch = proposal.get("patch")
            if not isinstance(path, str) or Path(path).is_absolute() or ".." in Path(path).parts:
                raise ValidationError(f"Pi remediation proposal {index} has an unsafe path")
            if path != items[item_id].get("path") or not isinstance(patch, str) or not patch.strip():
                raise ValidationError(f"Pi remediation proposal {index} has an invalid code patch")
    missing = set(findings) - seen
    if missing:
        raise ValidationError(f"Pi remediation omitted findings: {sorted(missing)!r}")
    return {
        "ok": True,
        "proposals": len(proposals),
        "replace_translation": sum(item.get("action") == "replace-translation" for item in proposals),
        "patch_code": sum(item.get("action") == "patch-code" for item in proposals),
        "no_change": sum(item.get("action") == "no-change" for item in proposals),
    }


def build_remediation_command(
    *,
    executable: str,
    provider: str,
    model: str,
    thinking: str,
    system_prompt: str,
    bundle: dict[str, Any],
    bundle_resolved: Path,
    review_resolved: Path,
    review_id: str,
) -> list[str]:
    inventory = [
        {"item_id": item.get("item_id"), "path": item.get("path")}
        for item in bundle.get("files", [])
    ] if bundle.get("kind") == "code" else [
        {"item_id": item.get("item_id")}
        for item in bundle.get("items", [])
    ]
    return [
        executable,
        "--provider", provider,
        "--model", model,
        "--thinking", thinking,
        "--mode", "json",
        "--no-session", "--no-approve", "--no-context-files", "--no-skills",
        "--no-prompt-templates", "--no-themes", "--no-extensions", "--no-tools",
        "--system-prompt", system_prompt,
        "--print", f"@{bundle_resolved}", f"@{review_resolved}",
        (
            "Process every supplied finding and return only one JSON object. "
            "Use schema_version=1, remediation_contract='tome4-review-remediation-v1', "
            f"bundle_id='{bundle['bundle_id']}', review_id='{review_id}'. "
            "Do not use review_contract and do not return Markdown. "
            "For patch-code, copy an exact item_id/path pair from this inventory: "
            f"{json.dumps(inventory, ensure_ascii=False)}."
        ),
    ]


def run_pi_remediation(
    *,
    bundle_path: Path,
    review_path: Path,
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
    review_resolved = review_path.expanduser().resolve()
    review = _read_review(review_resolved, bundle)
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")
    prompt_path = manifest.root / "i18n" / "prompts" / "pi-remediator.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi remediator prompt: {prompt_path}") from error
    run_directory = create_run_directory(manifest.root, "pi-remediate")
    run_directory.chmod(0o700)
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    remediation_path = run_directory / "remediation.json"
    report_path = run_directory / "pi-remediation.json"
    report: dict[str, Any] = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "remediation_contract": REMEDIATION_CONTRACT,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "bundle": str(bundle_resolved),
        "bundle_id": bundle["bundle_id"],
        "review": str(review_resolved),
        "review_id": review["review_id"],
        "kind": bundle["kind"],
        "prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "run_directory": str(run_directory),
        "raw_output": str(raw_output_path),
        "report": str(report_path),
    }
    command = build_remediation_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        bundle=bundle,
        bundle_resolved=bundle_resolved,
        review_resolved=review_resolved,
        review_id=review["review_id"],
    )
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
        report.update({"stderr": str(stderr_path), "error": f"Pi timed out after {timeout} seconds"})
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
    try:
        output = decode_json_object(
            extract_event_stream_output(
                result.stdout, "Pi remediation output"
            ),
            "Pi remediation output",
        )
        summary = _validate_remediation(bundle, review, output)
    except ValidationError as error:
        report["error"] = str(error)
        write_json(report_path, report)
        raise AgentError(f"Pi remediation validation failed: {error}; report: {report_path}") from error
    output["remediation_id"] = hashlib.sha256(
        json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    write_json(remediation_path, output)
    report.update({"ok": True, "summary": summary, "remediation": str(remediation_path)})
    write_json(report_path, report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tools/pi-remediate")
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER))
    parser.add_argument("--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING))
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_REVIEW_TIMEOUT,
        help="Pi time limit per remediation bundle in seconds (default: 1200 / 20 minutes)",
    )
    parser.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    try:
        report = run_pi_remediation(
            bundle_path=arguments.bundle,
            review_path=arguments.review,
            provider=arguments.provider,
            model=arguments.model,
            thinking=arguments.thinking,
            timeout=arguments.timeout,
            strict=arguments.strict,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        return error.exit_code
    print(
        f"OK  Pi remediation {report['bundle_id'][:16]}  "
        f"proposals={report['summary']['proposals']}"
    )
    print(f"Remediation: {report['remediation']}")
    print(f"Report: {report['report']}")
    return 0
