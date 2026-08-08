"""Run an isolated Pi model as a blind translation-quality evaluator."""

from __future__ import annotations

import argparse
import fcntl
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
from .errors import AgentError, ConfigurationError, I18nToolError, ValidationError
from .pi_agent import DEFAULT_MODEL, DEFAULT_PROVIDER, DEFAULT_THINKING, _pi_environment
from .pi_file_review import _run_file_review_process
from .pi_review import _canonical_sha256
from .pi_run_options import validate_pi_run_options
from .proposal import decode_json_object, extract_event_stream_output
from .quality import (
    ASSESSMENT_CONTRACT,
    DRY_RUN_CONTRACT,
    SAMPLE_CONTRACT,
    _load_sample_file,
    load_quality_policy,
    load_taxonomy,
    validate_quality_run,
)
from .quality_v2 import (
    CALIBRATION_CONTRACT,
    HOLDOUT_CONTRACT,
    build_assessment_v2,
    build_evaluator_bundles_v2,
    canonical_sha256 as canonical_sha256_v2,
    load_anchors,
    load_evaluator_prompt_v2,
    load_impact_rules,
    load_policy_v2,
    validate_assessment_v2,
    validate_sample_v2,
)
from .quality_v3 import (
    CALIBRATION_V3_CONTRACT,
    HOLDOUT_V3_CONTRACT,
    build_assessment_v3,
    build_evaluator_bundles_v3,
    canonical_sha256,
    load_anchors_v2,
    load_evaluator_prompt_v3,
    load_policy_v3,
    load_severity_matrix,
    validate_assessment_v3,
    validate_campaign_ledger_v3,
    validate_holdout_clearance_v3,
    validate_sample_v3,
    validate_stability_preregistration_v3,
    validate_stability_report_v3,
    runner_report_semantic_identity_v3,
)
from .report import atomic_write_bytes, create_run_directory, write_json

QUALITY_EVALUATOR_BUNDLE_CONTRACT = "tome4-quality-evaluator-bundle-v1"
QUALITY_EVALUATOR_CACHE_CONTRACT = "tome4-pi-quality-evaluator-cache-v1"
QUALITY_EVALUATOR_CACHE_V2_CONTRACT = "tome4-pi-quality-evaluator-cache-v2"
QUALITY_EVALUATOR_CACHE_V3_CONTRACT = "tome4-pi-quality-evaluator-cache-v3"
MAX_EVALUATOR_ITEMS = 120
DEFAULT_TIMEOUT = 1200


def _campaign_ledger_path(root: Path, preregistration_id: str) -> Path:
    return root / ".artifacts" / "i18n" / "quality" / "calibration-campaigns" / f"{preregistration_id}.json"


def _load_campaign_ledger(root: Path, preregistration_id: str) -> dict[str, Any]:
    return _read_json(
        _campaign_ledger_path(root, preregistration_id),
        "quality v3 calibration campaign ledger",
    )


def _register_campaign_stability_report(
    *, root: Path, preregistration: dict[str, Any], report: dict[str, Any],
) -> dict[str, Any]:
    preregistration_id = preregistration["preregistration_id"]
    path = _campaign_ledger_path(root, preregistration_id)
    lock_path = path.with_suffix(".lock")
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        ledger = _load_campaign_ledger(root, preregistration_id)
        validate_campaign_ledger_v3(ledger, preregistration=preregistration)
        validate_stability_report_v3(report, preregistration=preregistration)
        if report["passed"] is not True:
            raise ValidationError(
                "quality v3 campaign registration requires passed=true"
            )
        evaluator_id = report["evaluator"]["id"]
        existing = ledger["stability_reports"].get(evaluator_id)
        if existing is not None and existing != report["report_id"]:
            raise ValidationError("quality v3 campaign stability report cannot be replaced")
        ledger["stability_reports"][evaluator_id] = report["report_id"]
        write_json(path, ledger)
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return ledger


def _update_campaign_transfer(
    *, root: Path, preregistration_id: str, evaluator_id: str, round_number: int,
    execution_id: str, shard_index: int, bundle_id: str, new_state: str | None = None,
) -> dict[str, Any]:
    if evaluator_id not in {"reviewer-a", "reviewer-b"} or round_number not in {1, 2} or shard_index not in {1, 2}:
        raise ValidationError("quality v3 calibration transfer slot is outside the frozen campaign")
    path = _campaign_ledger_path(root, preregistration_id)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock_path = path.with_suffix(".lock")
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        ledger = _read_json(path, "quality v3 calibration campaign ledger") if path.is_file() else {
            "contract": "tome4-quality-calibration-campaign-ledger-v3",
            "schema_version": 3,
            "preregistration_id": preregistration_id,
            "external_transfer_limit": 8,
            "transfers": [],
            "stability_reports": {},
        }
        if (
            ledger.get("contract") != "tome4-quality-calibration-campaign-ledger-v3"
            or ledger.get("preregistration_id") != preregistration_id
            or ledger.get("external_transfer_limit") != 8
            or not isinstance(ledger.get("transfers"), list)
            or not isinstance(ledger.get("stability_reports"), dict)
        ):
            raise ValidationError("quality v3 calibration campaign ledger is invalid")
        key = (evaluator_id, round_number, shard_index)
        matches = [
            entry for entry in ledger["transfers"]
            if (entry.get("evaluator_id"), entry.get("round"), entry.get("shard_index")) == key
        ]
        if new_state is None:
            if matches:
                raise ValidationError("quality v3 calibration transfer slot is already consumed")
            if len(ledger["transfers"]) >= ledger["external_transfer_limit"]:
                raise ValidationError("quality v3 calibration external transfer limit is exhausted")
            entry = {
                "evaluator_id": evaluator_id, "round": round_number,
                "execution_id": execution_id, "shard_index": shard_index,
                "bundle_id": bundle_id, "state": "claimed",
            }
            ledger["transfers"].append(entry)
        else:
            if len(matches) != 1:
                raise ValidationError("quality v3 calibration transfer slot is missing or duplicated")
            entry = matches[0]
            if entry.get("execution_id") != execution_id or entry.get("bundle_id") != bundle_id or entry.get("state") != "claimed":
                raise ValidationError("quality v3 calibration transfer slot identity differs")
            if new_state not in {"succeeded", "failed"}:
                raise ValidationError("quality v3 calibration transfer terminal state is invalid")
            entry["state"] = new_state
        write_json(path, ledger)
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return ledger


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


def build_quality_evaluator_bundle(
    sample: dict[str, Any],
    taxonomy: dict[str, Any],
    *,
    evaluator_id: str,
    method_version: str,
) -> dict[str, Any]:
    items = sample.get("items")
    if not isinstance(items, list) or not items:
        raise ValidationError("quality sample has no items")
    if len(items) > MAX_EVALUATOR_ITEMS:
        raise ValidationError(
            f"quality evaluator bundles are limited to {MAX_EVALUATOR_ITEMS} items"
        )
    prefix = "A" if evaluator_id == "reviewer-a" else "B" if evaluator_id == "reviewer-b" else "F"
    bundle: dict[str, Any] = {
        "schema_version": 1,
        "quality_contract": QUALITY_EVALUATOR_BUNDLE_CONTRACT,
        "sample_contract": sample["quality_contract"],
        "sample_id": sample["sample_id"],
        "evaluator_id": evaluator_id,
        "finding_id_prefix": prefix,
        "method_version": method_version,
        "allowed_profiles": [item["id"] for item in taxonomy["profiles"]],
        "allowed_severities": [item["id"] for item in taxonomy["severities"]],
        "allowed_error_codes": [item["code"] for item in taxonomy["error_codes"]],
        "allowed_reuse_scopes": [item["id"] for item in taxonomy["reuse_scopes"]],
        "items": items,
    }
    bundle["bundle_id"] = _canonical_sha256(bundle)
    return bundle


def build_quality_evaluator_command(
    *,
    executable: str,
    provider: str,
    model: str,
    thinking: str,
    system_prompt: str,
    bundle_path: Path,
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
        f"@{bundle_path}",
        "Blindly assess every bundled revision and return only the required items JSON object.",
    ]


def _cache_key(
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
            "cache_contract": QUALITY_EVALUATOR_CACHE_CONTRACT,
            "tool_version": TOOL_VERSION,
            "bundle_id": bundle_id,
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "strict": strict,
        }
    )


def _cache_path(root: Path, key: str) -> Path:
    return root / ".artifacts" / "i18n" / "cache" / "pi-quality-evaluator" / f"{key}.json"


def _cache_key_v2(
    *,
    sample_id: str,
    evaluator_id: str,
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    rules_sha256: str,
    anchors_sha256: str,
    bundle_ids: list[str],
    strict: bool,
) -> str:
    return canonical_sha256_v2(
        {
            "cache_contract": QUALITY_EVALUATOR_CACHE_V2_CONTRACT,
            "tool_version": TOOL_VERSION,
            "sample_id": sample_id,
            "evaluator_id": evaluator_id,
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "rules_sha256": rules_sha256,
            "anchors_sha256": anchors_sha256,
            "bundle_ids": bundle_ids,
            "strict": strict,
        }
    )


def _cache_key_v3(
    *,
    sample_id: str,
    evaluator_id: str,
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    policy_sha256: str,
    severity_matrix_sha256: str,
    anchors_sha256: str,
    bundle_ids: list[str],
    bundle_sha256s: list[str],
    strict: bool,
    clearance_id: str | None = None,
) -> str:
    return canonical_sha256(
        {
            "cache_contract": QUALITY_EVALUATOR_CACHE_V3_CONTRACT,
            "tool_version": TOOL_VERSION,
            "sample_id": sample_id,
            "evaluator_id": evaluator_id,
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "policy_sha256": policy_sha256,
            "severity_matrix_sha256": severity_matrix_sha256,
            "anchors_sha256": anchors_sha256,
            "bundle_ids": bundle_ids,
            "bundle_sha256s": bundle_sha256s,
            "strict": strict,
            "clearance_id": clearance_id,
        }
    )


def _strip_markdown_fence(text: str) -> str:
    """Strip one markdown code fence around a JSON object (mechanical wrapper)."""
    stripped = text.strip()
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    return stripped


def _decode_quality_model_output(raw: bytes) -> tuple[dict[str, Any], str]:
    extracted = extract_event_stream_output(raw, "Pi quality evaluator output")
    try:
        return decode_json_object(extracted, "Pi quality evaluator output"), "none"
    except ValidationError as original:
        # Some models wrap the object in a markdown code fence; strip exactly
        # one fence before the deterministic missing-brace repair.
        try:
            fenced_text = _strip_markdown_fence(extracted.decode("utf-8"))
            fenced = fenced_text.encode("utf-8")
            if fenced != extracted:
                return decode_json_object(fenced, "Pi quality evaluator output"), "stripped-markdown-fence"
        except (UnicodeDecodeError, ValidationError):
            pass
        # Some models occasionally emit the complete items array but omit only
        # the final outer-object brace. Repair exactly that deterministic case;
        # all semantic content still goes through strict assessment validation.
        try:
            text = extracted.decode("utf-8").strip()
        except UnicodeDecodeError:
            raise original
        if text.startswith('{"items"') and text.endswith("]"):
            try:
                repaired = json.loads(text + "}")
            except json.JSONDecodeError:
                raise original
            if isinstance(repaired, dict) and set(repaired) == {"items"}:
                return repaired, "added-missing-outer-brace"
        raise original


def _validated_assessment(
    manifest: Any,
    *,
    sample_path: Path,
    assessment_path: Path,
    strict: bool,
) -> dict[str, Any]:
    validation = validate_quality_run(
        manifest,
        sample_path=sample_path,
        assessment_paths=[assessment_path],
        adjudication_path=None,
        strict=strict,
        # This call validates a standalone assessment, not the official
        # adjudicated pilot gate. It intentionally permits absent adjudication.
        dry_run=True,
    )
    if not validation["ok"]:
        detail = "; ".join(validation["errors"][:5])
        raise ValidationError(f"quality assessment validation failed: {detail}")
    return validation["assessments"][0]


def _load_cached_assessment(
    manifest: Any,
    *,
    path: Path,
    cache_key: str,
    bundle: dict[str, Any],
    sample_path: Path,
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    strict: bool,
    output_path: Path,
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    cached = _read_json(path, "quality evaluator cache")
    expected = {
        "cache_contract": QUALITY_EVALUATOR_CACHE_CONTRACT,
        "cache_key": cache_key,
        "bundle_id": bundle["bundle_id"],
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "prompt_sha256": prompt_sha256,
    }
    if (
        type(cached.get("strict")) is not bool
        or cached.get("strict") is not strict
        or any(cached.get(key) != value for key, value in expected.items())
    ):
        raise ValidationError("quality evaluator cache identity does not match")
    assessment = cached.get("assessment")
    if not isinstance(assessment, dict):
        raise ValidationError("quality evaluator cache has no assessment")
    write_json(output_path, assessment)
    _validated_assessment(
        manifest,
        sample_path=sample_path,
        assessment_path=output_path,
        strict=strict,
    )
    return assessment


def _run_pi_quality_evaluator_v2(
    manifest: Any,
    *,
    sample_path: Path,
    sample: dict[str, Any],
    evaluator_id: str,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    use_cache: bool,
    force: bool,
    pi_executable: str | None,
    started: float,
) -> dict[str, Any]:
    policy = load_policy_v2(manifest)
    rules = load_impact_rules(manifest, policy)
    taxonomy = load_taxonomy(manifest)
    anchors = load_anchors(
        manifest, policy=policy, rules=rules, taxonomy=taxonomy
    )
    bundles = build_evaluator_bundles_v2(
        sample=sample, evaluator_id=evaluator_id, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy,
        max_items=policy["max_shard_items"],
    )
    bundle_ids = [bundle["bundle_id"] for bundle in bundles]
    try:
        system_prompt = load_evaluator_prompt_v2(manifest)
    except ConfigurationError as error:
        raise AgentError("cannot read Pi quality evaluator v2 prompt or rubric") from error
    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    rules_sha256 = canonical_sha256_v2(rules)
    anchors_sha256 = canonical_sha256_v2(anchors)
    evaluator = {
        "kind": "model", "id": evaluator_id, "method_version": "mqm-pilot-v2",
        "provider": provider, "model": model, "thinking": thinking,
        "prompt_sha256": prompt_sha256, "rules_sha256": rules_sha256,
        "anchors_sha256": anchors_sha256, "bundle_ids": bundle_ids,
    }
    key = _cache_key_v2(
        sample_id=sample["sample_id"], evaluator_id=evaluator_id,
        provider=provider, model=model, thinking=thinking,
        prompt_sha256=prompt_sha256, rules_sha256=rules_sha256,
        anchors_sha256=anchors_sha256, bundle_ids=bundle_ids, strict=strict,
    )
    cache_path = _cache_path(manifest.root, key)
    run_directory = create_run_directory(manifest.root, "pi-quality-evaluator-v2")
    run_directory.chmod(0o700)
    assessment_path = run_directory / "assessment.json"
    report_path = run_directory / "pi-quality-evaluator.json"
    report: dict[str, Any] = {
        "schema_version": 2, "tool_version": TOOL_VERSION, "ok": False,
        "mode": "blind-quality-assessment-v2", "version": manifest.version,
        "sample_id": sample["sample_id"], "sample_contract": sample["quality_contract"],
        "evaluator_id": evaluator_id, "provider": provider, "model": model,
        "thinking": thinking, "strict": strict, "items": len(sample["items"]),
        "shards": len(bundles), "bundle_ids": bundle_ids,
        "pi_tools": False, "pi_session": False, "candidate_execution": False,
        "blind_inputs": {
            "other_assessments": False, "adjudication": False,
            "historical_findings": False, "expected_grades": False,
        },
        "prompt_sha256": prompt_sha256, "rules_sha256": rules_sha256,
        "anchors_sha256": anchors_sha256, "result_cache_key": key,
        "cache_decision": "disabled" if not use_cache else "bypass" if force else "miss",
        "attempts": 0, "charged_or_possible_transfers": 0,
        "validated_results": 0, "run_directory": str(run_directory),
        "report": str(report_path),
    }
    if use_cache and not force and cache_path.is_file():
        cached = _read_json(cache_path, "quality evaluator v2 cache")
        expected_cache = {
            "cache_contract": QUALITY_EVALUATOR_CACHE_V2_CONTRACT,
            "cache_key": key, "sample_id": sample["sample_id"],
            "evaluator_id": evaluator_id, "provider": provider, "model": model,
            "thinking": thinking, "prompt_sha256": prompt_sha256,
            "rules_sha256": rules_sha256, "anchors_sha256": anchors_sha256,
            "bundle_ids": bundle_ids, "strict": strict,
        }
        if any(cached.get(field) != value for field, value in expected_cache.items()):
            raise AgentError("quality evaluator v2 cache identity does not match")
        assessment = cached.get("assessment")
        if not isinstance(assessment, dict):
            raise AgentError("quality evaluator v2 cache has no assessment")
        validate_assessment_v2(
            assessment, sample=sample, policy=policy, rules=rules,
            anchors=anchors, taxonomy=taxonomy, expected_evaluator=evaluator,
        )
        write_json(assessment_path, assessment)
        report.update(
            ok=True, cache_decision="hit", assessment=str(assessment_path),
            assessment_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
            validated_results=1, findings=sum(len(item["findings"]) for item in assessment["items"]),
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        return report

    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")
    merged_items: list[dict[str, Any]] = []
    raw_outputs = []
    normalizations = []
    shard_artifacts = []
    for bundle in bundles:
        shard_index = bundle["shard_index"]
        bundle_path = run_directory / f"quality-bundle-{shard_index:03d}.json"
        raw_path = run_directory / f"raw-output-{shard_index:03d}.txt"
        stderr_path = run_directory / f"pi-stderr-{shard_index:03d}.txt"
        write_json(bundle_path, bundle)
        command = build_quality_evaluator_command(
            executable=executable, provider=provider, model=model, thinking=thinking,
            system_prompt=system_prompt, bundle_path=Path(bundle_path.name),
        )
        report["attempts"] += 1
        report["charged_or_possible_transfers"] += 1
        try:
            result = _run_file_review_process(
                command, cwd=run_directory, env=_pi_environment(manifest.root, provider),
                timeout=timeout, raw_output_path=raw_path, stderr_path=stderr_path,
            )
        except (subprocess.TimeoutExpired, OSError) as error:
            report.update(error=str(error), elapsed_seconds=round(time.monotonic() - started, 6))
            write_json(report_path, report)
            raise AgentError(f"Pi quality evaluator v2 shard {shard_index} failed: {error}") from error
        atomic_write_bytes(raw_path, result.stdout)
        if result.stderr:
            atomic_write_bytes(stderr_path, result.stderr)
        raw_outputs.append(str(raw_path))
        if result.returncode != 0 or not result.stdout.strip():
            report.update(
                error=f"Pi shard {shard_index} exited with status {result.returncode}",
                raw_outputs=raw_outputs,
                elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            raise AgentError(f"{report['error']}; report: {report_path}")
        try:
            output, normalization = _decode_quality_model_output(result.stdout)
            if set(output) != {"items"} or not isinstance(output["items"], list):
                raise ValidationError("must return exactly an items array")
            expected_revisions = [item["revision_id"] for item in bundle["items"]]
            received_revisions = [
                item.get("revision_id")
                for item in output["items"]
                if isinstance(item, dict)
            ]
            if received_revisions != expected_revisions:
                raise ValidationError("coverage/order mismatch")
        except ValidationError as error:
            report.update(
                error=f"Pi quality evaluator v2 shard {shard_index}: {error}",
                failed_shard=shard_index, raw_outputs=raw_outputs,
                shard_artifacts=shard_artifacts,
                elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            raise AgentError(f"{report['error']}; report: {report_path}") from error
        parsed_path = run_directory / f"parsed-output-{shard_index:03d}.json"
        write_json(parsed_path, output)
        artifact = {
            "shard_index": shard_index,
            "raw_output": str(raw_path),
            "raw_output_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "parsed_output": str(parsed_path),
            "parsed_output_sha256": hashlib.sha256(parsed_path.read_bytes()).hexdigest(),
            "normalization": normalization,
            "repaired_output": None,
            "repaired_output_sha256": None,
        }
        if normalization != "none":
            repaired_path = run_directory / f"repaired-output-{shard_index:03d}.json"
            write_json(repaired_path, output)
            artifact["repaired_output"] = str(repaired_path)
            artifact["repaired_output_sha256"] = hashlib.sha256(
                repaired_path.read_bytes()
            ).hexdigest()
        shard_artifacts.append(artifact)
        merged_items.extend(output["items"])
        normalizations.append(normalization)
    try:
        assessment = build_assessment_v2(
            sample_id=sample["sample_id"], evaluator=evaluator, items=merged_items
        )
        normalized = validate_assessment_v2(
            assessment, sample=sample, policy=policy, rules=rules,
            anchors=anchors, taxonomy=taxonomy, expected_evaluator=evaluator,
        )
    except ValidationError as error:
        report.update(
            error=f"Pi quality evaluator v2 assessment validation failed: {error}",
            raw_outputs=raw_outputs, shard_artifacts=shard_artifacts,
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}") from error
    write_json(assessment_path, assessment)
    if use_cache and not force:
        cache_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        write_json(
            cache_path,
            {
                "cache_contract": QUALITY_EVALUATOR_CACHE_V2_CONTRACT,
                "cache_key": key, "sample_id": sample["sample_id"],
                "evaluator_id": evaluator_id, "provider": provider, "model": model,
                "thinking": thinking, "prompt_sha256": prompt_sha256,
                "rules_sha256": rules_sha256, "anchors_sha256": anchors_sha256,
                "bundle_ids": bundle_ids, "strict": strict, "assessment": assessment,
            },
        )
    report.update(
        ok=True, assessment=str(assessment_path), raw_outputs=raw_outputs,
        assessment_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
        normalizations=normalizations, shard_artifacts=shard_artifacts,
        findings=sum(len(item["findings"]) for item in normalized["items"]),
        validated_results=1, elapsed_seconds=round(time.monotonic() - started, 6),
    )
    write_json(report_path, report)
    return report


def _run_pi_quality_evaluator_v3(
    manifest: Any,
    *,
    sample: dict[str, Any],
    evaluator_id: str,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    use_cache: bool,
    force: bool,
    pi_executable: str | None,
    started: float,
    preregistration: dict[str, Any],
    run_number: int | None,
    stability_reports: tuple[dict[str, Any], dict[str, Any]] | None,
) -> dict[str, Any]:
    policy = load_policy_v3(manifest)
    matrix = load_severity_matrix(manifest, policy)
    anchors = load_anchors_v2(manifest, policy=policy, matrix=matrix)
    bundles = build_evaluator_bundles_v3(
        sample=sample,
        evaluator_id=evaluator_id,
        policy=policy,
        matrix=matrix,
        max_items=policy["max_shard_items"],
    )
    bundle_ids = [bundle["bundle_id"] for bundle in bundles]
    bundle_sha256s = [canonical_sha256(bundle) for bundle in bundles]
    try:
        system_prompt = load_evaluator_prompt_v3(manifest)
    except ConfigurationError as error:
        raise AgentError("cannot read Pi quality evaluator v3 prompt or rubric") from error
    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    policy_sha256 = canonical_sha256(policy)
    matrix_sha256 = canonical_sha256(matrix)
    anchors_sha256 = canonical_sha256(anchors)
    bundles_by_evaluator = {
        identity: build_evaluator_bundles_v3(
            sample=sample, evaluator_id=identity, policy=policy, matrix=matrix
        )
        for identity in policy["evaluator_ids"]
    }
    bundle_ids_by_evaluator = {
        identity: [bundle["bundle_id"] for bundle in values]
        for identity, values in bundles_by_evaluator.items()
    }
    bundle_hashes_by_evaluator = {
        identity: [canonical_sha256(bundle) for bundle in values]
        for identity, values in bundles_by_evaluator.items()
    }
    clearance_id = None
    registered_evaluator = next(
        (
            item for item in preregistration.get("evaluators", [])
            if isinstance(item, dict) and item.get("id") == evaluator_id
        ),
        None,
    )
    if registered_evaluator is None or any(
        registered_evaluator.get(field) != value
        for field, value in (("provider", provider), ("model", model), ("thinking", thinking))
    ):
        raise ValidationError("quality v3 runner evaluator configuration differs from preregistration")
    if sample["dataset_kind"] == "calibration":
        if run_number not in (1, 2):
            raise ValidationError("quality v3 calibration requires --run-number 1 or 2")
        if use_cache:
            raise ValidationError("quality v3 calibration forbids result cache")
        validate_stability_preregistration_v3(
            preregistration, sample=sample, policy=policy, matrix=matrix, anchors=anchors,
            prompt_sha256=prompt_sha256,
            bundle_ids_by_evaluator=bundle_ids_by_evaluator,
            bundle_sha256s_by_evaluator=bundle_hashes_by_evaluator,
        )
    else:
        if run_number is not None:
            raise ValidationError("quality v3 holdout does not accept --run-number")
        if stability_reports is None:
            raise ValidationError("quality v3 holdout requires two stability reports")
        campaign_ledger = _load_campaign_ledger(
            manifest.root, preregistration["preregistration_id"]
        )
        clearance_id = validate_holdout_clearance_v3(
            sample=sample, preregistration=preregistration,
            stability_reports=stability_reports, policy=policy, matrix=matrix,
            anchors=anchors, prompt_sha256=prompt_sha256,
            campaign_ledger=campaign_ledger,
        )
    evaluator = {
        "kind": "model", "id": evaluator_id, "method_version": "mqm-pilot-v3",
        "provider": provider, "model": model, "thinking": thinking,
        "prompt_sha256": prompt_sha256, "policy_sha256": policy_sha256,
        "severity_matrix_sha256": matrix_sha256, "anchors_sha256": anchors_sha256,
        "bundle_ids": bundle_ids, "bundle_sha256s": bundle_sha256s,
    }
    key = _cache_key_v3(
        sample_id=sample["sample_id"], evaluator_id=evaluator_id,
        provider=provider, model=model, thinking=thinking,
        prompt_sha256=prompt_sha256, policy_sha256=policy_sha256,
        severity_matrix_sha256=matrix_sha256, anchors_sha256=anchors_sha256,
        bundle_ids=bundle_ids, bundle_sha256s=bundle_sha256s, strict=strict,
        clearance_id=clearance_id,
    )
    cache_path = _cache_path(manifest.root, key)
    run_directory = create_run_directory(manifest.root, "pi-quality-evaluator-v3")
    run_directory.chmod(0o700)
    assessment_path = run_directory / "assessment.json"
    report_path = run_directory / "pi-quality-evaluator.json"
    report: dict[str, Any] = {
        "schema_version": 3, "tool_version": TOOL_VERSION, "ok": False,
        "mode": "blind-quality-assessment-v3", "version": manifest.version,
        "sample_id": sample["sample_id"], "sample_contract": sample["quality_contract"],
        "evaluator_id": evaluator_id, "provider": provider, "model": model,
        "thinking": thinking, "strict": strict, "items": len(sample["items"]),
        "shards": len(bundles), "bundle_ids": bundle_ids,
        "bundle_sha256s": bundle_sha256s,
        "pi_tools": False, "pi_session": False, "candidate_execution": False,
        "blind_inputs": {
            "other_assessments": False, "adjudication": False,
            "historical_findings": False, "expected_grades": False,
            "anchors": False,
        },
        "prompt_sha256": prompt_sha256, "policy_sha256": policy_sha256,
        "severity_matrix_sha256": matrix_sha256, "anchors_sha256": anchors_sha256,
        "result_cache_key": key,
        "cache_decision": "disabled" if not use_cache else "bypass" if force else "miss",
        "attempts": 0, "charged_or_possible_transfers": 0,
        "validated_results": 0, "run_directory": str(run_directory),
        "report": str(report_path),
        "preregistration_id": preregistration["preregistration_id"],
        "clearance_id": clearance_id,
    }
    execution_id = hashlib.sha256(os.urandom(32)).hexdigest()
    if sample["dataset_kind"] == "calibration":
        report.update(round=run_number, execution_id=execution_id, shard_transfers=[])
    if use_cache and not force and cache_path.is_file():
        cached = _read_json(cache_path, "quality evaluator v3 cache")
        expected_cache = {
            "cache_contract": QUALITY_EVALUATOR_CACHE_V3_CONTRACT,
            "cache_key": key, "sample_id": sample["sample_id"],
            "evaluator_id": evaluator_id, "provider": provider, "model": model,
            "thinking": thinking, "prompt_sha256": prompt_sha256,
            "policy_sha256": policy_sha256, "severity_matrix_sha256": matrix_sha256,
            "anchors_sha256": anchors_sha256, "bundle_ids": bundle_ids,
            "bundle_sha256s": bundle_sha256s, "strict": strict,
            "clearance_id": clearance_id,
        }
        if any(cached.get(field) != value for field, value in expected_cache.items()):
            raise AgentError("quality evaluator v3 cache identity does not match")
        assessment = cached.get("assessment")
        if not isinstance(assessment, dict):
            raise AgentError("quality evaluator v3 cache has no assessment")
        normalized = validate_assessment_v3(
            assessment, sample=sample, policy=policy, matrix=matrix,
            anchors=anchors, expected_evaluator=evaluator,
        )
        write_json(assessment_path, assessment)
        report.update(
            ok=True, cache_decision="hit", assessment=str(assessment_path),
            assessment_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
            validated_results=1,
            findings=sum(len(item["findings"]) for item in normalized["items"]),
            raw_findings=sum(len(item["raw_findings"]) for item in normalized["items"]),
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        return report

    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")
    merged_items: list[dict[str, Any]] = []
    raw_outputs: list[str] = []
    normalizations: list[str] = []
    shard_artifacts: list[dict[str, Any]] = []
    claimed_transfers: list[tuple[int, str]] = []

    def finalize_calibration_transfers(state: str) -> None:
        if sample["dataset_kind"] != "calibration":
            return
        for claimed_shard, claimed_bundle in claimed_transfers:
            _update_campaign_transfer(
                root=manifest.root,
                preregistration_id=preregistration["preregistration_id"],
                evaluator_id=evaluator_id, round_number=run_number,
                execution_id=execution_id, shard_index=claimed_shard,
                bundle_id=claimed_bundle, new_state=state,
            )
    for bundle in bundles:
        shard_index = bundle["shard_index"]
        bundle_path = run_directory / f"quality-bundle-{shard_index:03d}.json"
        raw_path = run_directory / f"raw-output-{shard_index:03d}.txt"
        stderr_path = run_directory / f"pi-stderr-{shard_index:03d}.txt"
        write_json(bundle_path, bundle)
        command = build_quality_evaluator_command(
            executable=executable, provider=provider, model=model, thinking=thinking,
            system_prompt=system_prompt, bundle_path=Path(bundle_path.name),
        )
        report["attempts"] += 1
        report["charged_or_possible_transfers"] += 1
        if sample["dataset_kind"] == "calibration":
            _update_campaign_transfer(
                root=manifest.root, preregistration_id=preregistration["preregistration_id"],
                evaluator_id=evaluator_id, round_number=run_number,
                execution_id=execution_id, shard_index=shard_index,
                bundle_id=bundle["bundle_id"],
            )
            claimed_transfers.append((shard_index, bundle["bundle_id"]))
        try:
            result = _run_file_review_process(
                command, cwd=run_directory, env=_pi_environment(manifest.root, provider),
                timeout=timeout, raw_output_path=raw_path, stderr_path=stderr_path,
            )
        except (subprocess.TimeoutExpired, OSError) as error:
            finalize_calibration_transfers("failed")
            report.update(error=str(error), elapsed_seconds=round(time.monotonic() - started, 6))
            write_json(report_path, report)
            raise AgentError(f"Pi quality evaluator v3 shard {shard_index} failed: {error}") from error
        atomic_write_bytes(raw_path, result.stdout)
        if result.stderr:
            atomic_write_bytes(stderr_path, result.stderr)
        raw_outputs.append(str(raw_path))
        if result.returncode != 0 or not result.stdout.strip():
            finalize_calibration_transfers("failed")
            report.update(
                error=f"Pi shard {shard_index} exited with status {result.returncode}",
                raw_outputs=raw_outputs, elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            raise AgentError(f"{report['error']}; report: {report_path}")
        try:
            output, normalization = _decode_quality_model_output(result.stdout)
            if set(output) != {"items"} or not isinstance(output["items"], list):
                raise ValidationError("must return exactly an items array")
            expected_revisions = [item["revision_id"] for item in bundle["items"]]
            received_revisions = [item.get("revision_id") for item in output["items"] if isinstance(item, dict)]
            if received_revisions != expected_revisions:
                raise ValidationError("coverage/order mismatch")
        except ValidationError as error:
            finalize_calibration_transfers("failed")
            report.update(
                error=f"Pi quality evaluator v3 shard {shard_index}: {error}",
                failed_shard=shard_index, raw_outputs=raw_outputs,
                shard_artifacts=shard_artifacts,
                elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            raise AgentError(f"{report['error']}; report: {report_path}") from error
        parsed_path = run_directory / f"parsed-output-{shard_index:03d}.json"
        write_json(parsed_path, output)
        shard_artifacts.append(
            {
                "shard_index": shard_index, "raw_output": str(raw_path),
                "raw_output_sha256": hashlib.sha256(result.stdout).hexdigest(),
                "parsed_output": str(parsed_path),
                "parsed_output_sha256": hashlib.sha256(parsed_path.read_bytes()).hexdigest(),
                "normalization": normalization,
            }
        )
        merged_items.extend(output["items"])
        normalizations.append(normalization)
    try:
        assessment = build_assessment_v3(
            sample_id=sample["sample_id"], evaluator=evaluator, items=merged_items
        )
        normalized = validate_assessment_v3(
            assessment, sample=sample, policy=policy, matrix=matrix,
            anchors=anchors, expected_evaluator=evaluator,
        )
    except ValidationError as error:
        finalize_calibration_transfers("failed")
        report.update(
            error=f"Pi quality evaluator v3 assessment validation failed: {error}",
            raw_outputs=raw_outputs, shard_artifacts=shard_artifacts,
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}") from error
    if sample["dataset_kind"] == "calibration":
        finalize_calibration_transfers("succeeded")
        report["shard_transfers"] = [
            {"shard_index": shard_index, "bundle_id": bundle_id, "state": "succeeded"}
            for shard_index, bundle_id in claimed_transfers
        ]
    write_json(assessment_path, assessment)
    if use_cache and not force:
        cache_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        write_json(
            cache_path,
            {
                "cache_contract": QUALITY_EVALUATOR_CACHE_V3_CONTRACT,
                "cache_key": key, "sample_id": sample["sample_id"],
                "evaluator_id": evaluator_id, "provider": provider, "model": model,
                "thinking": thinking, "prompt_sha256": prompt_sha256,
                "policy_sha256": policy_sha256, "severity_matrix_sha256": matrix_sha256,
                "anchors_sha256": anchors_sha256, "bundle_ids": bundle_ids,
                "bundle_sha256s": bundle_sha256s, "strict": strict,
                "clearance_id": clearance_id,
                "assessment": assessment,
            },
        )
    report.update(
        ok=True, assessment=str(assessment_path), raw_outputs=raw_outputs,
        assessment_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
        normalizations=normalizations, shard_artifacts=shard_artifacts,
        findings=sum(len(item["findings"]) for item in normalized["items"]),
        raw_findings=sum(len(item["raw_findings"]) for item in normalized["items"]),
        anchor_rejections=sum(len(item["anchor_rejections"]) for item in normalized["items"]),
        validated_results=1, elapsed_seconds=round(time.monotonic() - started, 6),
    )
    if sample["dataset_kind"] == "calibration":
        report["runner_report_id"] = runner_report_semantic_identity_v3(report)
    write_json(report_path, report)
    return report


def run_pi_quality_evaluator(
    *,
    sample_path: Path,
    evaluator_id: str,
    provider: str,
    model: str,
    thinking: str,
    timeout: int = DEFAULT_TIMEOUT,
    strict: bool = True,
    use_cache: bool = True,
    force: bool = False,
    pi_executable: str | None = None,
    preregistration_path: Path | None = None,
    run_number: int | None = None,
    stability_report_paths: tuple[Path, Path] | None = None,
) -> dict[str, Any]:
    validate_pi_run_options(
        evaluator_id=evaluator_id,
        provider=provider,
        model=model,
        thinking=thinking,
        timeout=timeout,
        strict=strict,
        use_cache=use_cache,
        force=force,
    )
    started = time.monotonic()
    manifest = load_manifest()
    sample_resolved = sample_path.expanduser().resolve()
    raw_sample = _read_json(sample_resolved, "quality sample")
    sample_contract = raw_sample.get("quality_contract")
    if sample_contract in (CALIBRATION_V3_CONTRACT, HOLDOUT_V3_CONTRACT):
        if preregistration_path is None:
            raise ValidationError("quality v3 requires --preregistration")
        preregistration = _read_json(
            preregistration_path.expanduser().resolve(), "quality v3 preregistration"
        )
        stability_reports = None
        if stability_report_paths is not None:
            stability_reports = tuple(
                _read_json(path.expanduser().resolve(), "quality v3 stability report")
                for path in stability_report_paths
            )
        policy_v3 = load_policy_v3(manifest)
        sample_v3 = validate_sample_v3(raw_sample, policy_v3)
        return _run_pi_quality_evaluator_v3(
            manifest,
            sample=sample_v3,
            evaluator_id=evaluator_id,
            provider=provider,
            model=model,
            thinking=thinking,
            timeout=timeout,
            strict=strict,
            use_cache=use_cache,
            force=force,
            pi_executable=pi_executable,
            started=started,
            preregistration=preregistration,
            run_number=run_number,
            stability_reports=stability_reports,
        )
    if sample_contract in (CALIBRATION_CONTRACT, HOLDOUT_CONTRACT):
        sample_v2 = validate_sample_v2(raw_sample)
        return _run_pi_quality_evaluator_v2(
            manifest,
            sample_path=sample_resolved,
            sample=sample_v2,
            evaluator_id=evaluator_id,
            provider=provider,
            model=model,
            thinking=thinking,
            timeout=timeout,
            strict=strict,
            use_cache=use_cache,
            force=force,
            pi_executable=pi_executable,
            started=started,
        )
    if sample_contract not in (SAMPLE_CONTRACT, DRY_RUN_CONTRACT):
        raise ValidationError("unsupported quality sample contract")
    qpolicy = load_quality_policy(manifest)
    taxonomy = load_taxonomy(manifest)
    sample = _load_sample_file(
        sample_resolved,
        manifest=manifest,
        taxonomy=taxonomy,
        qpolicy=qpolicy,
        dry_run=sample_contract == DRY_RUN_CONTRACT,
    )
    method_version = qpolicy["pilot"]["method_version"]
    run_directory = create_run_directory(manifest.root, "pi-quality-evaluator")
    run_directory.chmod(0o700)
    bundle_path = run_directory / "quality-bundle.json"
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    assessment_path = run_directory / "assessment.json"
    report_path = run_directory / "pi-quality-evaluator.json"
    bundle = build_quality_evaluator_bundle(
        sample, taxonomy, evaluator_id=evaluator_id, method_version=method_version
    )
    write_json(bundle_path, bundle)

    prompt_path = manifest.root / "i18n" / "prompts" / "pi-quality-evaluator.md"
    rubric_path = manifest.root / "i18n" / "quality" / "rubric-v1.md"
    try:
        system_prompt = (
            prompt_path.read_text(encoding="utf-8")
            + "\n\n---\n\n"
            + rubric_path.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError("cannot read Pi quality evaluator prompt or rubric") from error
    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    key = _cache_key(
        bundle_id=bundle["bundle_id"],
        provider=provider,
        model=model,
        thinking=thinking,
        prompt_sha256=prompt_sha256,
        strict=strict,
    )
    cache_path = _cache_path(manifest.root, key)
    cache_decision = "disabled" if not use_cache else "bypass" if force else "miss"
    report: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "mode": "blind-quality-assessment-v1",
        "version": manifest.version,
        "sample_id": sample["sample_id"],
        "sample_contract": sample_contract,
        "bundle_id": bundle["bundle_id"],
        "evaluator_id": evaluator_id,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "items": len(bundle["items"]),
        "pi_tools": False,
        "pi_session": False,
        "candidate_execution": False,
        "blind_inputs": {
            "other_assessments": False,
            "adjudication": False,
            "historical_findings": False,
            "expected_grades": False,
        },
        "prompt_sha256": prompt_sha256,
        "result_cache_key": key,
        "cache_decision": cache_decision,
        "attempts": 0,
        "charged_or_possible_transfers": 0,
        "validated_results": 0,
        "run_directory": str(run_directory),
        "bundle": str(bundle_path),
        "raw_output": None,
        "report": str(report_path),
    }

    if use_cache and not force:
        try:
            cached = _load_cached_assessment(
                manifest,
                path=cache_path,
                cache_key=key,
                bundle=bundle,
                sample_path=sample_resolved,
                provider=provider,
                model=model,
                thinking=thinking,
                prompt_sha256=prompt_sha256,
                strict=strict,
                output_path=assessment_path,
            )
        except ValidationError as error:
            report.update(
                error=str(error),
                elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            raise AgentError(
                f"quality evaluator cache validation failed: {error}; "
                f"report: {report_path}"
            ) from error
        if cached is not None:
            report.update(
                ok=True,
                cache_decision="hit",
                assessment=str(assessment_path),
                validated_results=1,
                elapsed_seconds=round(time.monotonic() - started, 6),
            )
            write_json(report_path, report)
            return report

    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")
    command = build_quality_evaluator_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        # Run Pi from the private run directory so the attached file name is
        # relative and does not disclose a host path to the provider.
        bundle_path=Path("quality-bundle.json"),
    )
    report.update(
        attempts=1,
        charged_or_possible_transfers=1,
        raw_output=str(raw_output_path),
    )
    try:
        result = _run_file_review_process(
            command,
            cwd=run_directory,
            env=_pi_environment(manifest.root, provider),
            timeout=timeout,
            raw_output_path=raw_output_path,
            stderr_path=stderr_path,
        )
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b"", error.stderr or b""
        atomic_write_bytes(raw_output_path, stdout)
        atomic_write_bytes(stderr_path, stderr)
        report.update(
            error=f"Pi timed out after {timeout} seconds",
            raw_output_sha256=hashlib.sha256(stdout).hexdigest(),
            stderr=str(stderr_path),
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}")
    except OSError as error:
        report.update(
            error=f"cannot start Pi: {error}",
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}") from error

    atomic_write_bytes(raw_output_path, result.stdout)
    if result.stderr:
        atomic_write_bytes(stderr_path, result.stderr)
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = result.returncode
    report["raw_output_sha256"] = hashlib.sha256(result.stdout).hexdigest()
    if result.returncode != 0 or not result.stdout.strip():
        report["error"] = (
            f"Pi exited with status {result.returncode}"
            if result.returncode != 0
            else "Pi returned an empty response"
        )
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}")
    try:
        output, normalization = _decode_quality_model_output(result.stdout)
        report["normalization"] = normalization
        if set(output) != {"items"} or not isinstance(output["items"], list):
            raise ValidationError("quality evaluator must return exactly an items array")
        assessment = {
            "schema_version": 1,
            "quality_contract": ASSESSMENT_CONTRACT,
            "sample_id": sample["sample_id"],
            "evaluator": {
                "kind": "model",
                "id": evaluator_id,
                "method_version": method_version,
                "provider": provider,
                "model": model,
                "thinking": thinking,
                "prompt_sha256": prompt_sha256,
                "bundle_id": bundle["bundle_id"],
            },
            "items": output["items"],
        }
        write_json(assessment_path, assessment)
        normalized = _validated_assessment(
            manifest,
            sample_path=sample_resolved,
            assessment_path=assessment_path,
            strict=strict,
        )
    except ValidationError as error:
        report.update(
            error=str(error),
            elapsed_seconds=round(time.monotonic() - started, 6),
        )
        write_json(report_path, report)
        raise AgentError(
            f"Pi quality assessment validation failed: {error}; "
            f"report: {report_path}"
        ) from error

    if use_cache and not force:
        cache_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        write_json(
            cache_path,
            {
                "cache_contract": QUALITY_EVALUATOR_CACHE_CONTRACT,
                "cache_key": key,
                "bundle_id": bundle["bundle_id"],
                "provider": provider,
                "model": model,
                "thinking": thinking,
                "prompt_sha256": prompt_sha256,
                "strict": strict,
                "assessment": assessment,
            },
        )
    report.update(
        ok=True,
        assessment=str(assessment_path),
        findings=sum(len(item["findings"]) for item in normalized["items"]),
        validated_results=1,
        elapsed_seconds=round(time.monotonic() - started, 6),
    )
    write_json(report_path, report)
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/pi-quality-evaluator",
        description="Run one isolated Pi model as a blind quality evaluator",
    )
    parser.add_argument("--sample", required=True, type=Path)
    parser.add_argument("--evaluator", required=True)
    parser.add_argument("--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER))
    parser.add_argument("--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING))
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--cache", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--preregistration", type=Path)
    parser.add_argument("--run-number", type=int, choices=(1, 2))
    parser.add_argument("--stability-report", action="append", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    try:
        stability_paths = None
        if arguments.stability_report is not None:
            if len(arguments.stability_report) != 2:
                raise ValidationError("quality v3 holdout requires exactly two --stability-report values")
            stability_paths = tuple(arguments.stability_report)
        report = run_pi_quality_evaluator(
            sample_path=arguments.sample,
            evaluator_id=arguments.evaluator,
            provider=arguments.provider,
            model=arguments.model,
            thinking=arguments.thinking,
            timeout=arguments.timeout,
            strict=arguments.strict,
            use_cache=arguments.cache,
            force=arguments.force,
            preregistration_path=arguments.preregistration,
            run_number=arguments.run_number,
            stability_report_paths=stability_paths,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    print(
        f"OK  Pi quality evaluator {report['evaluator_id']}  "
        f"items={report['items']} findings={report.get('findings', 'cached')} "
        f"cache={report['cache_decision']}"
    )
    print(f"Assessment: {report['assessment']}")
    print(f"Report: {report['report']}")
    return 0
