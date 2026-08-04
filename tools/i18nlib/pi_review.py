"""Run a no-tools Pi reviewer against a bounded review bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
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
from .proposal import decode_json_object, extract_event_stream_output
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
MODEL_OUTPUT_FIELDS = frozenset(
    {"schema_version", "review_contract", "bundle_id", "findings"}
)
MODEL_FINDING_FIELDS = frozenset(
    {
        "finding_id",
        "severity",
        "category",
        "item_id",
        "title",
        "body",
        "suggested_fix",
        "path",
    }
)
REVIEW_CACHE_SCHEMA_VERSION = 1


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


def _review_summary(findings: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "ok": True,
        "findings": len(findings),
        "blockers": sum(item.get("severity") == "blocker" for item in findings),
        "majors": sum(item.get("severity") == "major" for item in findings),
        "minors": sum(item.get("severity") == "minor" for item in findings),
        "notes": sum(item.get("severity") == "note" for item in findings),
    }


def _validate_findings(
    bundle: dict[str, Any], output: dict[str, Any], *, strict: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    if strict:
        unknown = set(output) - MODEL_OUTPUT_FIELDS
        if unknown:
            raise ValidationError(
                f"Pi review contains unknown top-level fields: {sorted(unknown)!r}"
            )
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
    source_items = (
        bundle.get("items", [])
        if bundle.get("kind") == "translations"
        else bundle.get("files", [])
    )
    allowed = {
        item.get("item_id"): item
        for item in source_items
        if isinstance(item, dict) and isinstance(item.get("item_id"), str)
    }
    seen_model_ids: set[str] = set()
    seen_finding_keys: set[str] = set()
    normalized_findings: list[dict[str, Any]] = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"Pi finding {index} is not an object")
        if strict:
            unknown = set(finding) - MODEL_FINDING_FIELDS
            if unknown:
                raise ValidationError(
                    f"Pi finding {index} contains unknown fields: {sorted(unknown)!r}"
                )
        model_finding_id = finding.get("finding_id")
        if (
            not isinstance(model_finding_id, str)
            or not model_finding_id.strip()
            or len(model_finding_id) > 128
        ):
            raise ValidationError(f"Pi finding {index} has no finding_id")
        if model_finding_id in seen_model_ids:
            raise ValidationError(
                f"Pi findings contain duplicate finding_id: {model_finding_id}"
            )
        seen_model_ids.add(model_finding_id)
        if finding.get("severity") not in SEVERITIES:
            raise ValidationError(f"Pi finding {index} has an invalid severity")
        if finding.get("category") not in CATEGORIES:
            raise ValidationError(f"Pi finding {index} has an invalid category")
        if finding.get("item_id") not in allowed:
            raise ValidationError(f"Pi finding {index} references an unknown item_id")
        for key, maximum in (("title", 500), ("body", 12000)):
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                raise ValidationError(f"Pi finding {index} has no {key}")
            if len(finding[key]) > maximum:
                raise ValidationError(f"Pi finding {index} has an oversized {key}")
        if "suggested_fix" in finding and not isinstance(
            finding.get("suggested_fix"), str
        ):
            raise ValidationError(f"Pi finding {index} has an invalid suggested_fix")
        if len(finding.get("suggested_fix", "")) > 12000:
            raise ValidationError(f"Pi finding {index} has an oversized suggested_fix")
        if "path" in finding and finding.get("path") is not None:
            path = finding.get("path")
            if (
                not isinstance(path, str)
                or Path(path).is_absolute()
                or ".." in Path(path).parts
            ):
                raise ValidationError(f"Pi finding {index} has an unsafe path")
            expected_path = (
                allowed[finding["item_id"]].get("section")
                if bundle.get("kind") == "translations"
                else allowed[finding["item_id"]].get("path")
            )
            if path != expected_path:
                raise ValidationError(
                    f"Pi finding {index} path does not match its item_id"
                )
        normalized = {
            key: finding[key]
            for key in MODEL_FINDING_FIELDS
            if key in finding and key != "finding_id"
        }
        normalized["model_finding_id"] = model_finding_id
        finding_key = _canonical_sha256(
            {
                key: normalized.get(key)
                for key in (
                    "item_id",
                    "severity",
                    "category",
                    "title",
                    "body",
                    "path",
                )
            }
        )
        if finding_key in seen_finding_keys:
            raise ValidationError(
                f"Pi review contains duplicate semantic finding: {finding_key}"
            )
        seen_finding_keys.add(finding_key)
        normalized["finding_key"] = finding_key
        normalized_findings.append(normalized)

    normalized_findings.sort(
        key=lambda item: (str(item.get("item_id")), item["finding_key"])
    )
    for ordinal, finding in enumerate(normalized_findings, start=1):
        finding_ref = f"R-{ordinal:03d}"
        finding["finding_ref"] = finding_ref
        finding["finding_id"] = finding_ref
    decision_digest = _canonical_sha256(
        [
            {
                key: finding.get(key)
                for key in (
                    "finding_key",
                    "severity",
                    "category",
                    "item_id",
                    "title",
                    "body",
                    "suggested_fix",
                    "path",
                )
                if key in finding
            }
            for finding in normalized_findings
        ]
    )
    normalized_output = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_contract": REVIEW_CONTRACT,
        "bundle_id": bundle["bundle_id"],
        "decision_digest": decision_digest,
        "findings": normalized_findings,
    }
    normalized_output["review_id"] = _canonical_sha256(normalized_output)
    return _review_summary(normalized_findings), normalized_output


def _review_cache_key(
    *,
    bundle_id: str,
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    strict: bool,
) -> str:
    return _canonical_sha256(
        {
            "cache_contract": "tome4-pi-review-cache-v1",
            "tool_version": TOOL_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle_id,
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "strict": strict,
        }
    )


def _cached_review_path(root: Path, cache_key: str) -> Path:
    return root / ".artifacts" / "i18n" / "cache" / "pi-review" / f"{cache_key}.json"


def _revalidate_normalized_review(
    bundle: dict[str, Any], review: dict[str, Any], *, strict: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    findings = review.get("findings")
    if not isinstance(findings, list):
        raise ValidationError("cached Pi review findings are invalid")
    model_findings: list[dict[str, Any]] = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"cached Pi finding {index} is invalid")
        model_finding_id = finding.get("model_finding_id")
        if not isinstance(model_finding_id, str):
            raise ValidationError(f"cached Pi finding {index} has no model id")
        model_finding = {
            key: finding[key]
            for key in MODEL_FINDING_FIELDS
            if key in finding and key != "finding_id"
        }
        model_finding["finding_id"] = model_finding_id
        model_findings.append(model_finding)
    summary, expected = _validate_findings(
        bundle,
        {
            "schema_version": review.get("schema_version"),
            "review_contract": review.get("review_contract"),
            "bundle_id": review.get("bundle_id"),
            "findings": model_findings,
        },
        strict=strict,
    )
    if expected != review:
        raise ValidationError("cached Pi review digest or normalization is invalid")
    return summary, expected


def _load_cached_review(
    *,
    path: Path,
    cache_key: str,
    bundle: dict[str, Any],
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    strict: bool,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise ValidationError("Pi review cache entry is not a regular file")
    record = _read_json(path, "Pi review cache entry")
    expected = {
        "cache_schema_version": REVIEW_CACHE_SCHEMA_VERSION,
        "cache_key": cache_key,
        "bundle_id": bundle["bundle_id"],
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "prompt_sha256": prompt_sha256,
        "strict": strict,
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise ValidationError("Pi review cache entry identity is invalid")
    review = record.get("review")
    if not isinstance(review, dict):
        raise ValidationError("Pi review cache entry has no review")
    summary, normalized = _revalidate_normalized_review(
        bundle, review, strict=strict
    )
    return summary, normalized


def _write_cached_review(
    *,
    path: Path,
    cache_key: str,
    bundle: dict[str, Any],
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    strict: bool,
    review: dict[str, Any],
) -> None:
    write_json(
        path,
        {
            "cache_schema_version": REVIEW_CACHE_SCHEMA_VERSION,
            "cache_key": cache_key,
            "bundle_id": bundle["bundle_id"],
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "strict": strict,
            "review": review,
        },
    )


def build_review_command(
    *,
    executable: str,
    provider: str,
    model: str,
    thinking: str,
    system_prompt: str,
    bundle: dict[str, Any],
    bundle_resolved: Path,
) -> list[str]:
    inventory = (
        [item.get("item_id") for item in bundle.get("items", [])]
        if bundle.get("kind") == "translations"
        else [item.get("item_id") for item in bundle.get("files", [])]
    )
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
        f"@{bundle_resolved}",
        "Review only this bundle and return the required JSON object. Do not omit the envelope. "
        "The exact allowed item_id inventory for this bundle is "
        f"{json.dumps(inventory, ensure_ascii=False)}; copy item_id values verbatim, never use paths.",
    ]


def run_pi_review(
    *,
    bundle_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    pi_executable: str | None = None,
    use_cache: bool = True,
    force: bool = False,
) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_manifest()
    bundle_resolved = bundle_path.expanduser().resolve()
    bundle = validate_review_bundle(manifest, bundle_resolved)
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")

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

    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    cache_key = _review_cache_key(
        bundle_id=bundle["bundle_id"],
        provider=provider,
        model=model,
        thinking=thinking,
        prompt_sha256=prompt_sha256,
        strict=strict,
    )
    cache_path = _cached_review_path(manifest.root, cache_key)
    cache_decision = "disabled" if not use_cache else ("bypass" if force else "miss")
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
        "mode": "findings-only-v1",
        "pi_tools": False,
        "pi_session": False,
        "candidate_execution": False,
        "concurrency": 1,
        "run_id": run_directory.name,
        "bundle": str(bundle_resolved),
        "bundle_id": bundle["bundle_id"],
        "kind": bundle["kind"],
        "prompt_sha256": prompt_sha256,
        "result_cache_key": cache_key,
        "cache_decision": cache_decision,
        "timeout_seconds": timeout,
        "attempts": 0,
        "charged_or_possible_transfers": 0,
        "provider_confirmed_requests": None,
        "validated_results": 0,
        "run_directory": str(run_directory),
        "raw_output": None,
        "report": str(report_path),
    }
    if use_cache and not force:
        try:
            cached = _load_cached_review(
                path=cache_path,
                cache_key=cache_key,
                bundle=bundle,
                provider=provider,
                model=model,
                thinking=thinking,
                prompt_sha256=prompt_sha256,
                strict=strict,
            )
        except ValidationError as error:
            report["error"] = f"Pi review cache validation failed: {error}"
            report["elapsed_seconds"] = round(time.monotonic() - started, 6)
            write_json(report_path, report)
            raise AgentError(f"{report['error']}; report: {report_path}") from error
        if cached is not None:
            summary, output = cached
            write_json(review_path, output)
            report.update(
                {
                    "ok": True,
                    "cache_decision": "hit",
                    "summary": summary,
                    "review": str(review_path),
                    "validated_results": 1,
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                }
            )
            write_json(report_path, report)
            return report

    executable = pi_executable or shutil.which("pi")
    if not executable:
        report["error"] = "pi is not available on PATH"
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"pi is not available on PATH; report: {report_path}")
    command = build_review_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        bundle=bundle,
        bundle_resolved=bundle_resolved,
    )
    report.update(
        {
            "attempts": 1,
            "charged_or_possible_transfers": 1,
            "raw_output": str(raw_output_path),
        }
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
        report["stderr"] = str(stderr_path)
        report["error"] = f"Pi timed out after {timeout} seconds"
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"Pi timed out after {timeout} seconds; report: {report_path}")
    except OSError as error:
        report["error"] = f"cannot start Pi: {error}"
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
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
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"Pi exited with status {result.returncode}; report: {report_path}")
    if not result.stdout.strip():
        report["error"] = "Pi returned an empty response"
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"Pi returned an empty response; report: {report_path}")
    try:
        model_output = decode_json_object(
            extract_event_stream_output(
                result.stdout, "Pi review output"
            ),
            "Pi review output",
        )
        summary, output = _validate_findings(bundle, model_output, strict=strict)
    except ValidationError as error:
        report["error"] = str(error)
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"Pi review validation failed: {error}; report: {report_path}") from error

    write_json(review_path, output)
    if use_cache and not force:
        _write_cached_review(
            path=cache_path,
            cache_key=cache_key,
            bundle=bundle,
            provider=provider,
            model=model,
            thinking=thinking,
            prompt_sha256=prompt_sha256,
            strict=strict,
            review=output,
        )
    report.update(
        {
            "ok": True,
            "summary": summary,
            "review": str(review_path),
            "validated_results": 1,
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    )
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
    parser.add_argument(
        "--cache",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="reuse an exact validated result before starting Pi (default: true)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="bypass cache lookup and do not replace the cached observation",
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
            use_cache=arguments.cache,
            force=arguments.force,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        return error.exit_code
    summary = report["summary"]
    print(
        f"OK  Pi review {report['bundle_id'][:16]}  "
        f"kind={report['kind']} findings={summary['findings']} "
        f"cache={report['cache_decision']} attempts={report['attempts']}"
    )
    print(f"Review: {report['review']}")
    print(f"Report: {report['report']}")
    return 0
