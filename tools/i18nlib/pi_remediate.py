"""Run an isolated Pi remediation pass over validated review findings."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path, PureWindowsPath
from typing import Any

from . import TOOL_VERSION
from .build import _lua_value
from .config import Manifest, load_manifest
from .errors import AgentError, I18nToolError, ValidationError
from .lint import Policy, lint_documents, load_policy
from .locale_model import LocaleDocument
from .pi_agent import DEFAULT_MODEL, DEFAULT_PROVIDER, DEFAULT_THINKING, _pi_environment
from .pi_run_options import validate_pi_run_options as _validate_run_options
from .pi_review import _stage_validated_json
from .proposal import decode_json_object, extract_event_stream_output
from .report import atomic_write_bytes, create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_TIMEOUT,
    _validate_findings_for_remediation,
    validate_review_bundle,
)
from .semantics import json_value_signature


REMEDIATION_CONTRACT = "tome4-review-remediation-v1"
REMEDIATION_SCHEMA_VERSION = 1
REMEDIATION_ACTIONS = frozenset(
    {"replace-translation", "patch-code", "no-change"}
)
REMEDIATION_ROOT_FIELDS = frozenset(
    {"schema_version", "remediation_contract", "bundle_id", "review_id", "proposals"}
)
REMEDIATION_PROPOSAL_FIELDS = frozenset(
    {"finding_id", "item_id", "action", "rationale"}
)
TRANSLATION_PROPOSAL_FIELDS = frozenset(
    {"source", "source_tag", "original_target", "target", "args_order", "special"}
)
CODE_PROPOSAL_FIELDS = frozenset({"path", "patch"})


def _validate_json_lua_value(value: Any, *, label: str) -> None:
    try:
        json_value_signature(value, label=label)
        _lua_value(value)
    except ValidationError as error:
        raise ValidationError(f"{label} is not a finite renderable JSON/Lua value") from error


def _same_json_value(actual: Any, expected: Any, *, label: str) -> bool:
    return json_value_signature(actual, label=label) == json_value_signature(
        expected, label=f"expected {label}"
    )


def _is_safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return (
        not path.is_absolute()
        and not windows_path.is_absolute()
        and not windows_path.drive
        and ".." not in path.parts
        and ".." not in windows_path.parts
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
    if value.get("bundle_id") != bundle.get("bundle_id"):
        raise ValidationError("validated review bundle_id does not match")
    _validate_findings_for_remediation(bundle, value)
    return value


def _validate_remediation(
    bundle: dict[str, Any],
    review: dict[str, Any],
    output: dict[str, Any],
    *,
    manifest: Manifest | None = None,
    policy: Policy | None = None,
    strict: bool = True,
) -> dict[str, Any]:
    if type(strict) is not bool:
        raise ValidationError("Pi remediation strict mode must be a boolean")
    if not isinstance(output, dict):
        raise ValidationError("Pi remediation must be an object")
    if strict:
        unknown = set(output) - REMEDIATION_ROOT_FIELDS
        if unknown:
            raise ValidationError(
                "Pi remediation contains unknown top-level fields: "
                f"{sorted(unknown)!r}"
            )
    if (
        type(output.get("schema_version")) is not int
        or output["schema_version"] != REMEDIATION_SCHEMA_VERSION
    ):
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

    kind = bundle.get("kind")
    if kind == "translations":
        items = {
            item.get("item_id"): item
            for item in bundle.get("items", [])
            if isinstance(item, dict) and isinstance(item.get("item_id"), str)
        }
        allowed_actions = frozenset({"replace-translation", "no-change"})
    elif kind == "code":
        items = {
            item.get("item_id"): item
            for item in bundle.get("files", [])
            if isinstance(item, dict) and isinstance(item.get("item_id"), str)
        }
        allowed_actions = frozenset({"patch-code", "no-change"})
    else:
        raise ValidationError("Pi remediation bundle has an unsupported kind")
    review_findings = review.get("findings")
    if not isinstance(review_findings, list):
        raise ValidationError("Pi remediation review findings are invalid")
    findings = {
        item.get("finding_id"): item
        for item in review_findings
        if isinstance(item, dict) and isinstance(item.get("finding_id"), str)
    }
    seen: set[str] = set()
    lint_warnings = 0
    for index, proposal in enumerate(proposals):
        if not isinstance(proposal, dict):
            raise ValidationError(f"Pi remediation proposal {index} is not an object")
        missing_common = REMEDIATION_PROPOSAL_FIELDS - set(proposal)
        if missing_common:
            raise ValidationError(
                f"Pi remediation proposal {index} is missing fields: "
                f"{sorted(missing_common)!r}"
            )
        finding_id = proposal.get("finding_id")
        item_id = proposal.get("item_id")
        action = proposal.get("action")
        if action not in REMEDIATION_ACTIONS:
            raise ValidationError(f"Pi remediation proposal {index} has invalid action")
        if action not in allowed_actions:
            raise ValidationError(
                f"Pi remediation proposal {index} action {action!r} is incompatible "
                f"with {kind!r} bundles"
            )
        action_fields = (
            TRANSLATION_PROPOSAL_FIELDS
            if action == "replace-translation"
            else CODE_PROPOSAL_FIELDS
            if action == "patch-code"
            else frozenset()
        )
        if strict:
            unknown = set(proposal) - REMEDIATION_PROPOSAL_FIELDS - action_fields
            if unknown:
                raise ValidationError(
                    f"Pi remediation proposal {index} contains fields not allowed "
                    f"for {action!r}: {sorted(unknown)!r}"
                )
        if finding_id not in findings or item_id not in items:
            raise ValidationError(
                f"Pi remediation proposal {index} references unknown finding/item"
            )
        if finding_id in seen:
            raise ValidationError(
                f"Pi remediation contains duplicate finding_id: {finding_id}"
            )
        if findings[finding_id].get("item_id") != item_id:
            raise ValidationError(
                f"Pi remediation proposal {index} mismatches finding item_id"
            )
        rationale = proposal.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValidationError(f"Pi remediation proposal {index} has no rationale")
        seen.add(finding_id)
        if action == "replace-translation":
            missing = TRANSLATION_PROPOSAL_FIELDS - set(proposal)
            if missing:
                raise ValidationError(
                    f"Pi remediation proposal {index} is missing translation fields: "
                    f"{sorted(missing)!r}"
                )
            item = items[item_id]
            for key in ("source", "source_tag", "original_target"):
                expected = item.get("target") if key == "original_target" else item.get(key)
                if not _same_json_value(
                    proposal.get(key), expected, label=f"proposal {index} {key}"
                ):
                    raise ValidationError(
                        f"Pi remediation proposal {index} does not preserve {key}"
                    )
            if (
                not isinstance(proposal.get("target"), str)
                or not proposal["target"].strip()
            ):
                raise ValidationError(f"Pi remediation proposal {index} has no target")
            args_order = proposal.get("args_order")
            if args_order is not None and (
                not isinstance(args_order, list)
                or not all(type(value) is int for value in args_order)
            ):
                raise ValidationError(
                    f"Pi remediation proposal {index} has invalid args_order"
                )
            _validate_json_lua_value(
                proposal.get("special"), label=f"proposal {index} special"
            )

            component = item.get("component", bundle.get("component"))
            section = item.get("section")
            if not isinstance(component, str) or not isinstance(section, str):
                raise ValidationError(
                    f"Pi remediation proposal {index} has invalid translation context"
                )
            if policy is None:
                if manifest is None:
                    manifest = load_manifest()
                policy = load_policy(manifest)
            logical_path = f"remediation:{bundle.get('bundle_id')}:{finding_id}"
            record = {
                "kind": "translation",
                "function_name": "t",
                "section": section,
                "source": proposal["source"],
                "target": proposal["target"],
                "source_tag": proposal["source_tag"],
                "args_order": args_order,
                "special": proposal["special"],
                "line": None,
                "logical_path": logical_path,
            }
            synthetic = LocaleDocument(
                logical_path=logical_path,
                sha256=hashlib.sha256(
                    json_value_signature(
                        record, label=f"proposal {index} translation"
                    ).encode("utf-8")
                ).hexdigest(),
                records=(record,),
            )
            lint_issues, _lint_metrics = lint_documents(
                [(component, synthetic)], policy
            )
            errors = [issue for issue in lint_issues if issue.severity == "error"]
            warnings = [
                issue for issue in lint_issues if issue.severity == "warning"
            ]
            if errors:
                detail = "; ".join(
                    f"{issue.code}: {issue.message}" for issue in errors
                )
                raise ValidationError(
                    f"Pi remediation proposal {index} failed translation lint: {detail}"
                )
            if strict and warnings:
                detail = "; ".join(
                    f"{issue.code}: {issue.message}" for issue in warnings
                )
                raise ValidationError(
                    f"Pi remediation proposal {index} has strict lint warnings: {detail}"
                )
            lint_warnings += len(warnings)
        elif action == "patch-code":
            missing = CODE_PROPOSAL_FIELDS - set(proposal)
            if missing:
                raise ValidationError(
                    f"Pi remediation proposal {index} is missing code fields: "
                    f"{sorted(missing)!r}"
                )
            path = proposal.get("path")
            patch = proposal.get("patch")
            if not _is_safe_relative_path(path):
                raise ValidationError(
                    f"Pi remediation proposal {index} has an unsafe path"
                )
            if path != items[item_id].get("path"):
                raise ValidationError(
                    f"Pi remediation proposal {index} path does not match its item_id"
                )
            if not isinstance(patch, str) or not patch.strip():
                raise ValidationError(
                    f"Pi remediation proposal {index} has an invalid code patch"
                )
    missing = set(findings) - seen
    if missing:
        raise ValidationError(f"Pi remediation omitted findings: {sorted(missing)!r}")
    return {
        "ok": True,
        "proposals": len(proposals),
        "replace_translation": sum(
            item.get("action") == "replace-translation" for item in proposals
        ),
        "patch_code": sum(
            item.get("action") == "patch-code" for item in proposals
        ),
        "no_change": sum(item.get("action") == "no-change" for item in proposals),
        "lint_errors": 0,
        "lint_warnings": lint_warnings,
        "warnings": lint_warnings,
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
    _validate_run_options(
        provider=provider,
        model=model,
        thinking=thinking,
        timeout=timeout,
        strict=strict,
    )
    manifest = load_manifest()
    bundle_resolved = bundle_path.expanduser().resolve()
    bundle = validate_review_bundle(
        manifest, bundle_resolved, allow_legacy_translations=True
    )
    review_resolved = review_path.expanduser().resolve()
    review = _read_review(review_resolved, bundle)
    policy = load_policy(manifest)
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
    validated_bundle_path, bundle_payload_sha256, bundle_payload_bytes = (
        _stage_validated_json(run_directory, "validated-bundle.json", bundle)
    )
    validated_review_path, review_payload_sha256, review_payload_bytes = (
        _stage_validated_json(run_directory, "validated-review.json", review)
    )
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    remediation_path = run_directory / "remediation.json"
    report_path = run_directory / "pi-remediation.json"
    report: dict[str, Any] = {
        "schema_version": REMEDIATION_SCHEMA_VERSION,
        "remediation_contract": REMEDIATION_CONTRACT,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "bundle": str(bundle_resolved),
        "validated_bundle": str(validated_bundle_path),
        "bundle_payload_sha256": bundle_payload_sha256,
        "bundle_payload_bytes": bundle_payload_bytes,
        "bundle_id": bundle["bundle_id"],
        "review": str(review_resolved),
        "validated_review": str(validated_review_path),
        "review_payload_sha256": review_payload_sha256,
        "review_payload_bytes": review_payload_bytes,
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
        bundle_resolved=validated_bundle_path,
        review_resolved=validated_review_path,
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
        summary = _validate_remediation(
            bundle,
            review,
            output,
            manifest=manifest,
            policy=policy,
            strict=strict,
        )
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
