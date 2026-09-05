"""Registration and handlers for quality commands."""

from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
from typing import Any
from .config import Manifest
from .errors import ValidationError
from .facts_study import (
    run_build as run_facts_study_build,
    run_bundles as run_facts_study_bundles,
    run_report as run_facts_study_report,
    run_validate as run_facts_study_validate,
)
from .facts_curation import (
    run_curation_build,
    run_execution_manifest,
    run_curation_bundles,
    run_curation_prepare,
    run_curation_report,
    run_curation_select,
    run_curation_validate,
)
from .locale_model import LocaleLoader
from .pi_quality import _register_campaign_stability_report
from .quality import (
    create_quality_run_directory,
    load_taxonomy,
    run_dry_run as quality_run_dry_run,
    run_inventory as quality_run_inventory,
    run_report as quality_run_report,
    run_sample as quality_run_sample,
    run_validation as quality_run_validation,
)
from .quality_v2 import (
    adjudicate_v2,
    build_disputes_v2,
    build_report_v2,
    build_stability_report_v2,
    canonical_sha256,
    load_anchors,
    load_impact_rules,
    load_evaluator_prompt_v2,
    load_policy_v2,
    match_assessments_v2,
    read_json_object,
    run_calibration_v2,
    run_evaluator_bundles_v2,
    validate_assessment_v2,
    validate_sample_v2,
    validate_stability_preregistration_v2,
    bytes_sha256,
)
from .quality_v3 import (
    adjudicate_v3,
    build_disputes_v3,
    build_evaluator_bundles_v3,
    build_report_v3,
    build_stability_report_v3,
    load_anchors_v2,
    load_evaluator_prompt_v3,
    load_policy_v3,
    load_severity_matrix,
    match_assessments_v3,
    run_calibration_v3,
    run_evaluator_bundles_v3,
    validate_assessment_v3,
    validate_adjudication_validation_v3,
    validate_match_v3,
    validate_sample_v3,
    validate_stability_preregistration_v3,
)
from .report import write_json
from .runtime import LuaRuntime
from .cli_common import _add_common_arguments, _manifest, _print_json


def register(subparsers: argparse._SubParsersAction) -> None:
    quality = subparsers.add_parser(
        "quality",
        help=(
            "translation quality: current-revision inventory, deterministic "
            "pilot sampling, strict assessment/adjudication validation and "
            "consistency reports"
        ),
    )
    quality_subparsers = quality.add_subparsers(dest="quality_command", required=True)
    quality_inventory = quality_subparsers.add_parser(
        "inventory",
        help="build the current revision inventory with deterministic gate/risk facts",
    )
    _add_common_arguments(quality_inventory)
    quality_sample = quality_subparsers.add_parser(
        "sample",
        help="deterministic stratified pilot sample and assessment templates",
    )
    _add_common_arguments(quality_sample)
    quality_sample.add_argument(
        "--inventory",
        required=True,
        type=Path,
        help="inventory.jsonl produced by 'quality inventory'",
    )
    quality_sample.add_argument(
        "--size",
        type=int,
        default=None,
        help="sample size (default: policy pilot size 120)",
    )
    quality_sample.add_argument(
        "--seed",
        default=None,
        help="deterministic sampling seed (default: policy seed)",
    )
    quality_sample.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "build the 12-item rubric try-out bundle that never enters the "
            "official pilot sample (size/seed come from policy dry_run)"
        ),
    )
    quality_validate = quality_subparsers.add_parser(
        "validate",
        help=(
            "strictly validate sample, assessments and adjudication against "
            "taxonomy/policy and revision identity"
        ),
    )
    _add_common_arguments(quality_validate)
    quality_validate.add_argument("--sample", required=True, type=Path)
    quality_validate.add_argument(
        "--assessment",
        action="append",
        default=[],
        type=Path,
        metavar="ASSESSMENT",
        help="assessment JSON; may be repeated (pilot: exactly two)",
    )
    quality_validate.add_argument(
        "--adjudication",
        type=Path,
        help="adjudication JSON (required for the official pilot sample)",
    )
    quality_validate.add_argument(
        "--dry-run",
        action="store_true",
        help="validate a dry-run sample; adjudication is optional",
    )
    quality_validate.add_argument("--strict", action="store_true")
    quality_report = quality_subparsers.add_parser(
        "report",
        help="build the consistency and calibration report from a validation run",
    )
    _add_common_arguments(quality_report)
    quality_report.add_argument("--validation", required=True, type=Path)
    quality_calibration = quality_subparsers.add_parser(
        "calibration", help="generate mutually-exclusive evaluator-v2 calibration and holdout datasets",
    )
    _add_common_arguments(quality_calibration)
    quality_calibration.add_argument("--inventory", required=True, type=Path)
    quality_calibration.add_argument("--calibration-size", type=int, default=32)
    quality_calibration.add_argument("--holdout-size", type=int, default=32)
    quality_bundles = quality_subparsers.add_parser(
        "evaluator-bundles", help="build offline evaluator-v2 shards without calling a provider",
    )
    _add_common_arguments(quality_bundles)
    quality_bundles.add_argument("--sample", required=True, type=Path)
    quality_bundles.add_argument("--evaluator", required=True)
    quality_bundles.add_argument("--max-items", type=int, default=20)
    quality_match = quality_subparsers.add_parser(
        "match", help="normalize and match two complete evaluator-v2 assessments",
    )
    _add_common_arguments(quality_match)
    quality_match.add_argument("--sample", required=True, type=Path)
    quality_match.add_argument("--assessment", action="append", required=True, type=Path)
    quality_disputes = quality_subparsers.add_parser(
        "disputes", help="build an anonymous dispute bundle and separate identity mapping",
    )
    _add_common_arguments(quality_disputes)
    quality_disputes.add_argument("--match", required=True, type=Path)
    quality_disputes.add_argument("--sample", required=True, type=Path)
    quality_disputes.add_argument("--assessment", action="append", required=True, type=Path)
    quality_disputes.add_argument("--seed", default="tome4-quality-disputes-v2")
    quality_adjudicate = quality_subparsers.add_parser(
        "adjudicate-v2", help="validate human fact adjudication and recompute severity",
    )
    _add_common_arguments(quality_adjudicate)
    quality_adjudicate.add_argument("--match", required=True, type=Path)
    quality_adjudicate.add_argument("--adjudication", required=True, type=Path)
    quality_adjudicate.add_argument("--strict", action="store_true")
    quality_report_v2 = quality_subparsers.add_parser(
        "report-v2", help="build evaluator-v2 item, issue, fact, severity and burden metrics",
    )
    _add_common_arguments(quality_report_v2)
    quality_report_v2.add_argument("--match", required=True, type=Path)
    quality_report_v2.add_argument("--adjudication-validation", type=Path)
    quality_stability = quality_subparsers.add_parser(
        "stability-v2",
        help="compare two real frozen evaluator runs against preregistered stability thresholds",
    )
    _add_common_arguments(quality_stability)
    quality_stability.add_argument("--sample", required=True, type=Path)
    quality_stability.add_argument(
        "--assessment", action="append", required=True, type=Path
    )
    quality_stability.add_argument(
        "--run-report", action="append", required=True, type=Path
    )
    quality_stability.add_argument("--preregistration", required=True, type=Path)
    quality_calibration_v3 = quality_subparsers.add_parser(
        "calibration-v3", help="project the frozen evaluator-v2 32+32 selection into v3 contracts",
    )
    _add_common_arguments(quality_calibration_v3)
    quality_calibration_v3.add_argument("--inventory", required=True, type=Path)
    quality_bundles_v3 = quality_subparsers.add_parser(
        "evaluator-bundles-v3", help="build offline evaluator-v3 shards without calling a provider",
    )
    _add_common_arguments(quality_bundles_v3)
    quality_bundles_v3.add_argument("--sample", required=True, type=Path)
    quality_bundles_v3.add_argument("--evaluator", required=True)
    quality_match_v3 = quality_subparsers.add_parser(
        "match-v3", help="normalize anchors and match two complete evaluator-v3 assessments",
    )
    _add_common_arguments(quality_match_v3)
    quality_match_v3.add_argument("--sample", required=True, type=Path)
    quality_match_v3.add_argument("--assessment", action="append", required=True, type=Path)
    quality_disputes_v3 = quality_subparsers.add_parser(
        "disputes-v3", help="build an anonymous v3 dispute bundle and identity mapping",
    )
    _add_common_arguments(quality_disputes_v3)
    quality_disputes_v3.add_argument("--match", required=True, type=Path)
    quality_disputes_v3.add_argument("--sample", required=True, type=Path)
    quality_disputes_v3.add_argument("--seed", default="tome4-quality-disputes-v3")
    quality_adjudicate_v3 = quality_subparsers.add_parser(
        "adjudicate-v3", help="validate v3 finding rejection or provisional severity adjudication",
    )
    _add_common_arguments(quality_adjudicate_v3)
    quality_adjudicate_v3.add_argument("--match", required=True, type=Path)
    quality_adjudicate_v3.add_argument("--adjudication", required=True, type=Path)
    quality_adjudicate_v3.add_argument("--strict", action="store_true")
    quality_report_v3 = quality_subparsers.add_parser(
        "report-v3", help="build raw-model, anchor-normalized, severity and burden metrics",
    )
    _add_common_arguments(quality_report_v3)
    quality_report_v3.add_argument("--match", required=True, type=Path)
    quality_report_v3.add_argument("--adjudication-validation", type=Path)
    quality_stability_v3 = quality_subparsers.add_parser(
        "stability-v3", help="compare two real frozen evaluator-v3 runs against preregistration",
    )
    _add_common_arguments(quality_stability_v3)
    quality_stability_v3.add_argument("--sample", required=True, type=Path)
    quality_stability_v3.add_argument("--assessment", action="append", required=True, type=Path)
    quality_stability_v3.add_argument("--run-report", action="append", required=True, type=Path)
    quality_stability_v3.add_argument("--preregistration", required=True, type=Path)
    facts_build = quality_subparsers.add_parser(
        "facts-study-build",
        help="build a new isolated 20-item supplemental-only Facts study set",
    )
    _add_common_arguments(facts_build)
    facts_build.add_argument("--inventory", required=True, type=Path)
    facts_build.add_argument(
        "--exclude-sample", action="append", default=[], required=True, type=Path,
        help="sample/dataset whose revision IDs must be excluded; repeat for every frozen lineage",
    )
    facts_build.add_argument("--seed", default="tome4-facts-study-v2-candidate")
    facts_bundles = quality_subparsers.add_parser(
        "facts-study-bundles",
        help="freeze seven blinded arm bundles and the exact 33-slot preregistration",
    )
    _add_common_arguments(facts_bundles)
    facts_bundles.add_argument("--sample", required=True, type=Path)
    facts_bundles.add_argument("--facts", required=True, type=Path)
    facts_bundles.add_argument("--gold", required=True, type=Path)
    facts_bundles.add_argument("--gold-review", action="append", required=True, type=Path)
    facts_bundles.add_argument("--gold-adjudication", required=True, type=Path)
    facts_validate = quality_subparsers.add_parser(
        "facts-study-validate",
        help="strictly validate all 33 assessments or run the offline fake replay",
    )
    _add_common_arguments(facts_validate)
    for flag in ("sample", "facts", "neutral", "gold", "preregistration"):
        facts_validate.add_argument(f"--{flag}", required=True, type=Path)
    facts_validate.add_argument("--bundle", action="append", required=True, type=Path)
    facts_validate.add_argument("--assessment", action="append", default=[], type=Path)
    facts_validate.add_argument("--run-report", action="append", default=[], type=Path)
    facts_validate.add_argument("--fake-runner", action="store_true")
    facts_report = quality_subparsers.add_parser(
        "facts-study-report",
        help="build causal metrics and the preregistered Facts-channel decision",
    )
    _add_common_arguments(facts_report)
    facts_report.add_argument("--validation", required=True, type=Path)
    facts_bundles.add_argument(
        "--pool", type=Path, help="curation pool.json (required for sample v2)"
    )
    facts_bundles.add_argument(
        "--facts-pool", type=Path,
        help="80-item pool facts packet (required for sample v2)",
    )
    facts_validate.add_argument(
        "--pool", type=Path, help="curation pool.json (required for sample v2)"
    )
    facts_validate.add_argument(
        "--facts-pool", type=Path,
        help="80-item pool facts packet (required for sample v2)",
    )
    facts_validate.add_argument(
        "--execution-manifest", type=Path,
        help="user-authorized execution manifest (required for external v2 assessments)",
    )
    curation_build = quality_subparsers.add_parser(
        "facts-study-curation-build",
        help="build the deterministic 80-item source-side curation pool",
    )
    _add_common_arguments(curation_build)
    curation_build.add_argument("--inventory", required=True, type=Path)
    curation_build.add_argument(
        "--exclude-sample", action="append", default=[], type=Path,
        help="artifact whose revision IDs must be excluded; repeat as needed",
    )
    curation_build.add_argument("--seed", default="tome4-facts-study-curation-v1")
    curation_build.add_argument(
        "--protocol", choices=("v3", "v4"), default="v3",
        help="pool construction protocol: v3 baseline band or v4 long-source enriched band",
    )
    curation_prepare = quality_subparsers.add_parser(
        "facts-study-curation-prepare",
        help="build the target-visible curator bundle from the frozen Facts packet",
    )
    _add_common_arguments(curation_prepare)
    curation_prepare.add_argument("--pool", required=True, type=Path)
    curation_prepare.add_argument("--facts", required=True, type=Path)
    curation_prepare.add_argument("--inventory", required=True, type=Path)
    curation_select = quality_subparsers.add_parser(
        "facts-study-curation-select",
        help="select the final 20 items from the curator assessment (natural first)",
    )
    _add_common_arguments(curation_select)
    curation_select.add_argument("--pool", required=True, type=Path)
    curation_select.add_argument("--facts", required=True, type=Path)
    curation_select.add_argument("--curator", required=True, type=Path)
    curation_select.add_argument("--inventory", required=True, type=Path)
    curation_select.add_argument("--controlled-variants", type=Path)
    curation_select.add_argument("--seed", default="tome4-facts-study-curation-select-v1")
    curation_select.add_argument(
        "--protocol", choices=("v3", "v4", "v5"), default="v5",
        help="selection quota protocol (v5 = corpus-aligned quotas)",
    )
    manifest = quality_subparsers.add_parser(
        "facts-study-execution-manifest",
        help="bind a user authorization to an offline-frozen preregistration for external execution",
    )
    _add_common_arguments(manifest)
    manifest.add_argument("--preregistration", required=True, type=Path)
    manifest.add_argument("--authorization-id", required=True)
    manifest.add_argument("--granted-at", required=True)
    manifest.add_argument("--output", required=True, type=Path)
    manifest.add_argument("--mode", choices=("sequential", "parallel"), default="sequential")
    manifest.add_argument("--concurrency", type=int, default=1)
    manifest.add_argument("--retry-transmission", type=int, default=0, choices=(0, 1, 2, 3))
    quality.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "quality":
        if arguments.quality_command == "inventory":
            return _quality_inventory(arguments)
        if arguments.quality_command == "sample":
            return _quality_sample(arguments)
        if arguments.quality_command == "validate":
            return _quality_validate(arguments)
        if arguments.quality_command == "report":
            return _quality_report(arguments)
        if arguments.quality_command == "calibration":
            return _quality_calibration_v2(arguments)
        if arguments.quality_command == "evaluator-bundles":
            return _quality_evaluator_bundles_v2(arguments)
        if arguments.quality_command == "match":
            return _quality_match_v2(arguments)
        if arguments.quality_command == "disputes":
            return _quality_disputes_v2(arguments)
        if arguments.quality_command == "adjudicate-v2":
            return _quality_adjudicate_v2(arguments)
        if arguments.quality_command == "report-v2":
            return _quality_report_v2(arguments)
        if arguments.quality_command == "stability-v2":
            return _quality_stability_v2(arguments)
        if arguments.quality_command == "calibration-v3":
            return _quality_calibration_v3(arguments)
        if arguments.quality_command == "evaluator-bundles-v3":
            return _quality_evaluator_bundles_v3(arguments)
        if arguments.quality_command == "match-v3":
            return _quality_match_v3(arguments)
        if arguments.quality_command == "disputes-v3":
            return _quality_disputes_v3(arguments)
        if arguments.quality_command == "adjudicate-v3":
            return _quality_adjudicate_v3(arguments)
        if arguments.quality_command == "report-v3":
            return _quality_report_v3(arguments)
        if arguments.quality_command == "stability-v3":
            return _quality_stability_v3(arguments)
        if arguments.quality_command == "facts-study-build":
            return _quality_facts_study_build(arguments)
        if arguments.quality_command == "facts-study-curation-build":
            return _quality_facts_study_curation_build(arguments)
        if arguments.quality_command == "facts-study-curation-prepare":
            return _quality_facts_study_curation_prepare(arguments)
        if arguments.quality_command == "facts-study-curation-select":
            return _quality_facts_study_curation_select(arguments)
        if arguments.quality_command == "facts-study-execution-manifest":
            return _quality_facts_study_execution_manifest(arguments)
        if arguments.quality_command == "facts-study-bundles":
            return _quality_facts_study_bundles(arguments)
        if arguments.quality_command == "facts-study-validate":
            return _quality_facts_study_validate(arguments)
        if arguments.quality_command == "facts-study-report":
            return _quality_facts_study_report(arguments)
        raise AssertionError(
            f"unhandled quality command: {arguments.quality_command}"
        )
    raise AssertionError(f"unhandled command: {arguments.command}")


def _quality_inventory(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = quality_run_inventory(manifest, loader)
    if arguments.json:
        _print_json(report)
    else:
        summary = report["summary"]
        print(
            f"OK  quality inventory {report['version']}  "
            f"entries={summary['entries']} occurrences={summary['occurrences']}"
        )
        print(f"    sha256={report['inventory_sha256'][:16]}")
        print(f"    profiles={summary['profiles']}")
        print(f"    risk flags={summary['risk_flags']}")
        print(f"Output: {report['inventory']}")
    return 0


def _quality_sample(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if arguments.dry_run:
        if arguments.size is not None or arguments.seed is not None:
            raise ValidationError(
                "--dry-run uses the policy dry_run size/seed; "
                "--size/--seed cannot be combined with --dry-run"
            )
        report = quality_run_dry_run(
            manifest,
            inventory_path=arguments.inventory,
        )
        if arguments.json:
            _print_json(report)
        else:
            print(
                f"OK  quality dry-run {report['sample_id'][:16]}  "
                f"size={report['size']} "
                f"official={report['official_sample_id'][:16]}"
            )
            if report["unmet_constraints"]:
                for unmet in report["unmet_constraints"]:
                    print(
                        f"    UNMET {unmet['id']}: "
                        f"{unmet.get('value', '')} "
                        f"{unmet['actual']}/{unmet['target_min']}"
                    )
            print(f"Output: {report['dry_run_path']}")
        return 0
    report = quality_run_sample(
        manifest,
        inventory_path=arguments.inventory,
        size=arguments.size,
        seed=arguments.seed,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality sample {report['sample_id'][:16]}  "
            f"size={report['size']} buckets={report['bucket_counts']}"
        )
        print(f"    coverage={report['coverage']}")
        if report["unmet_constraints"]:
            for unmet in report["unmet_constraints"]:
                print(f"    UNMET {unmet['id']}: {unmet['actual']}/{unmet['target_min']}")
        print(f"Output: {report['sample_path']}")
    return 0


def _quality_validate(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if not arguments.dry_run and arguments.adjudication is None:
        raise ValidationError(
            "quality validate requires --adjudication for the official "
            "pilot sample (or pass --dry-run)"
        )
    report = quality_run_validation(
        manifest,
        sample_path=arguments.sample,
        assessment_paths=arguments.assessment,
        adjudication_path=arguments.adjudication,
        strict=arguments.strict or None,
        dry_run=arguments.dry_run,
    )
    if arguments.json:
        _print_json(report)
    else:
        status = "OK" if report["ok"] else "FAIL"
        print(f"{status} quality validate {report['sample_id'][:16]}")
        for error in report["errors"]:
            print(f"    ERROR {error}")
        for warning in report["warnings"]:
            print(f"    WARN  {warning}")
        for assessment in report["assessments"]:
            print(
                f"    {assessment['evaluator_id']}: {assessment['items']} items"
            )
        print(f"Output: {report['validation_path']}")
    if not report["ok"]:
        raise ValidationError(
            "quality validation failed: "
            + "; ".join(report["errors"][:5])
        )
    return 0


def _quality_report(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = quality_run_report(
        manifest,
        validation_path=arguments.validation,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality report {report['sample_id'][:16]}")
        for assessment in report.get("assessments", []):
            print(
                f"    {assessment['evaluator_id']}: items={assessment['items']} "
                f"findings={assessment['findings']}"
            )
        agreement = report.get("agreement", {})
        if "note" not in agreement:
            print(
                f"    context agreement={agreement.get('context_sufficient_agreement')} "
                f"defect agreement={agreement.get('defect_presence_agreement')}"
            )
            print(
                f"    major agreement={agreement.get('major_or_worse_agreement')} "
                f"kappa={agreement.get('severity_weighted_kappa')}"
            )
        print(f"Output: {report['report_md']}")
    return 0


def _quality_calibration_v2(arguments: argparse.Namespace) -> int:
    if arguments.calibration_size != 32 or arguments.holdout_size != 32:
        raise ValidationError("quality v2 calibration and holdout sizes are frozen at 32")
    report = run_calibration_v2(_manifest(arguments), arguments.inventory)
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v2 datasets calibration={report['calibration_id'][:16]} "
            f"holdout={report['holdout_id'][:16]} inventory={report['inventory_entries']}"
        )
        print(f"Manifest: {report['manifest']}")
    return 0


def _quality_evaluator_bundles_v2(arguments: argparse.Namespace) -> int:
    report = run_evaluator_bundles_v2(
        _manifest(arguments), sample_path=arguments.sample,
        evaluator_id=arguments.evaluator, max_items=arguments.max_items,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v2 shards evaluator={report['evaluator_id']} "
            f"shards={report['shard_count']} max-items={report['max_items']}"
        )
        print(f"Index: {report['index']}")
    return 0


def _quality_v2_inputs(arguments: argparse.Namespace) -> tuple[
    Manifest, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    manifest = _manifest(arguments)
    policy = load_policy_v2(manifest)
    rules = load_impact_rules(manifest, policy)
    taxonomy = load_taxonomy(manifest)
    anchors = load_anchors(
        manifest, policy=policy, rules=rules, taxonomy=taxonomy
    )
    return manifest, policy, rules, anchors, taxonomy


def _validated_v2_assessments(
    paths: list[Path], *, sample: dict[str, Any], policy: dict[str, Any],
    rules: dict[str, Any], anchors: dict[str, Any], taxonomy: dict[str, Any],
) -> list[dict[str, Any]]:
    if len(paths) != 2:
        raise ValidationError("quality v2 requires exactly two assessments")
    normalized = []
    expected_rules = canonical_sha256(rules)
    expected_anchors = canonical_sha256(anchors)
    for path in paths:
        value = read_json_object(path, "quality v2 assessment")
        if value.get("evaluator", {}).get("rules_sha256") != expected_rules:
            raise ValidationError("quality v2 assessment rules hash does not match")
        if value.get("evaluator", {}).get("anchors_sha256") != expected_anchors:
            raise ValidationError("quality v2 assessment anchors hash does not match")
        normalized.append(
            validate_assessment_v2(
                value, sample=sample, policy=policy, rules=rules,
                anchors=anchors, taxonomy=taxonomy,
            )
        )
    if [item["evaluator"]["id"] for item in normalized] != policy["evaluator_ids"]:
        raise ValidationError("quality v2 assessments must be reviewer-a then reviewer-b")
    return normalized


def _quality_match_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, taxonomy = _quality_v2_inputs(arguments)
    sample = validate_sample_v2(read_json_object(arguments.sample, "quality v2 sample"))
    assessments = _validated_v2_assessments(
        arguments.assessment, sample=sample, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy,
    )
    match = match_assessments_v2(
        sample=sample, left_assessment=assessments[0],
        right_assessment=assessments[1], policy=policy,
    )
    run_directory = create_quality_run_directory(manifest.root, "issue-match-v2")
    path = run_directory / "issue-match.json"
    write_json(path, match)
    report = {
        "match_id": match["match_id"], "issues": len(match["issues"]),
        "manual_queue": len(match["manual_queue"]), "match": str(path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 match issues={report['issues']} manual={report['manual_queue']}")
        print(f"Match: {path}")
    return 0


def _quality_disputes_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, taxonomy = _quality_v2_inputs(arguments)
    sample = validate_sample_v2(read_json_object(arguments.sample, "quality v2 sample"))
    assessments = _validated_v2_assessments(
        arguments.assessment, sample=sample, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy,
    )
    match = read_json_object(arguments.match, "quality v2 issue match")
    dispute, identity = build_disputes_v2(
        match=match, sample=sample, assessments=(assessments[0], assessments[1]),
        seed=arguments.seed,
    )
    run_directory = create_quality_run_directory(manifest.root, "disputes-v2")
    dispute_path = run_directory / "dispute.json"
    identity_path = run_directory / "dispute-identity.json"
    write_json(dispute_path, dispute)
    write_json(identity_path, identity)
    report = {
        "dispute_id": dispute["dispute_id"], "items": len(dispute["items"]),
        "dispute": str(dispute_path), "identity_mapping": str(identity_path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 disputes items={report['items']}")
        print(f"Dispute: {dispute_path}")
        print(f"Identity: {identity_path}")
    return 0


def _quality_adjudicate_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, _ = _quality_v2_inputs(arguments)
    match = read_json_object(arguments.match, "quality v2 issue match")
    adjudication = read_json_object(arguments.adjudication, "quality v2 adjudication")
    validation = adjudicate_v2(
        match=match, adjudication=adjudication, policy=policy, rules=rules,
        anchors=anchors, strict=arguments.strict,
    )
    run_directory = create_quality_run_directory(manifest.root, "adjudication-v2")
    path = run_directory / "adjudication-validation.json"
    write_json(path, validation)
    report = {
        "validation_id": validation["validation_id"], "items": len(validation["items"]),
        "validation": str(path), "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 adjudication items={report['items']}")
        print(f"Validation: {path}")
    return 0


def _quality_report_v2(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    match = read_json_object(arguments.match, "quality v2 issue match")
    validation = (
        read_json_object(arguments.adjudication_validation, "quality v2 adjudication validation")
        if arguments.adjudication_validation else None
    )
    report = build_report_v2(match=match, adjudication_validation=validation)
    run_directory = create_quality_run_directory(manifest.root, "report-v2")
    path = run_directory / "report.json"
    write_json(path, report)
    summary = {**report, "report": str(path), "run_directory": str(run_directory)}
    if arguments.json:
        _print_json(summary)
    else:
        print(
            f"OK  quality v2 report issues={report['issue_metrics']['issue_union']} "
            f"manual={report['human_burden']['issues_requiring_adjudication']}"
        )
        print(f"Report: {path}")
    return 0


def _quality_stability_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, taxonomy = _quality_v2_inputs(arguments)
    if len(arguments.assessment) != 2 or len(arguments.run_report) != 2:
        raise ValidationError(
            "quality stability-v2 requires exactly two assessments and two run reports"
        )
    sample = validate_sample_v2(
        read_json_object(arguments.sample, "quality v2 stability sample")
    )
    preregistration = validate_stability_preregistration_v2(
        read_json_object(
            arguments.preregistration, "quality v2 stability preregistration"
        ),
        sample=sample,
        policy=policy,
        rules=rules,
        anchors=anchors,
        prompt_sha256=hashlib.sha256(
            load_evaluator_prompt_v2(manifest).encode("utf-8")
        ).hexdigest(),
    )
    assessments = []
    expected_rules = canonical_sha256(rules)
    expected_anchors = canonical_sha256(anchors)
    expected_prompt = preregistration["frozen_inputs"]["prompt_sha256"]
    for path in arguments.assessment:
        value = read_json_object(path, "quality v2 stability assessment")
        evaluator = value.get("evaluator", {})
        if (
            evaluator.get("rules_sha256") != expected_rules
            or evaluator.get("anchors_sha256") != expected_anchors
            or evaluator.get("prompt_sha256") != expected_prompt
        ):
            raise ValidationError("quality stability assessment frozen hashes differ")
        assessments.append(
            validate_assessment_v2(
                value,
                sample=sample,
                policy=policy,
                rules=rules,
                anchors=anchors,
                taxonomy=taxonomy,
            )
        )
    run_reports = tuple(
        read_json_object(path, "quality v2 runner report")
        for path in arguments.run_report
    )
    report = build_stability_report_v2(
        sample=sample,
        assessments=(assessments[0], assessments[1]),
        run_reports=(run_reports[0], run_reports[1]),
        assessment_sha256s=(
            bytes_sha256(arguments.assessment[0]),
            bytes_sha256(arguments.assessment[1]),
        ),
        run_report_sha256s=(
            bytes_sha256(arguments.run_report[0]),
            bytes_sha256(arguments.run_report[1]),
        ),
        preregistration=preregistration,
        policy=policy,
    )
    run_directory = create_quality_run_directory(manifest.root, "stability-v2")
    path = run_directory / "stability-report.json"
    write_json(path, report)
    summary = {**report, "report": str(path), "run_directory": str(run_directory)}
    if arguments.json:
        _print_json(summary)
    else:
        print(
            f"{'OK' if report['passed'] else 'FAIL'} quality v2 stability "
            f"evaluator={report['evaluator']['id']} "
            f"jaccard={report['metrics']['finding_jaccard']:.3f}"
        )
        print(f"Report: {path}")
    return 0 if report["passed"] else 1


def _quality_v3_inputs(arguments: argparse.Namespace) -> tuple[
    Manifest, dict[str, Any], dict[str, Any], dict[str, Any]
]:
    manifest = _manifest(arguments)
    policy = load_policy_v3(manifest)
    matrix = load_severity_matrix(manifest, policy)
    anchors = load_anchors_v2(manifest, policy=policy, matrix=matrix)
    return manifest, policy, matrix, anchors


def _validated_v3_assessments(
    paths: list[Path], *, sample: dict[str, Any], policy: dict[str, Any],
    matrix: dict[str, Any], anchors: dict[str, Any], prompt_sha256: str,
) -> list[dict[str, Any]]:
    if len(paths) != 2:
        raise ValidationError("quality v3 requires exactly two assessments")
    expected = {
        "prompt_sha256": prompt_sha256,
        "policy_sha256": canonical_sha256(policy),
        "severity_matrix_sha256": canonical_sha256(matrix),
        "anchors_sha256": canonical_sha256(anchors),
    }
    normalized = []
    for path in paths:
        value = read_json_object(path, "quality v3 assessment")
        evaluator = value.get("evaluator", {})
        if any(evaluator.get(field) != digest for field, digest in expected.items()):
            raise ValidationError("quality v3 assessment frozen hashes do not match")
        bundles = build_evaluator_bundles_v3(
            sample=sample, evaluator_id=evaluator.get("id"), policy=policy,
            matrix=matrix, max_items=policy["max_shard_items"],
        )
        if (
            evaluator.get("bundle_ids") != [bundle["bundle_id"] for bundle in bundles]
            or evaluator.get("bundle_sha256s") != [canonical_sha256(bundle) for bundle in bundles]
        ):
            raise ValidationError("quality v3 assessment shard identities do not match")
        normalized.append(
            validate_assessment_v3(
                value, sample=sample, policy=policy, matrix=matrix, anchors=anchors
            )
        )
    if [item["evaluator"]["id"] for item in normalized] != policy["evaluator_ids"]:
        raise ValidationError("quality v3 assessments must be reviewer-a then reviewer-b")
    return normalized


def _quality_calibration_v3(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_calibration_v3(manifest, arguments.inventory)
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v3 calibration={report['calibration_id']} "
            f"holdout={report['holdout_id']} revisions-unchanged={report['revisions_unchanged']}"
        )
        print(f"Index: {report['index']}")
    return 0


def _quality_evaluator_bundles_v3(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_evaluator_bundles_v3(
        manifest, sample_path=arguments.sample, evaluator_id=arguments.evaluator,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v3 shards evaluator={report['evaluator_id']} "
            f"shards={report['shard_count']} max-items={report['max_items']}"
        )
        print(f"Index: {report['index']}")
    return 0


def _quality_match_v3(arguments: argparse.Namespace) -> int:
    manifest, policy, matrix, anchors = _quality_v3_inputs(arguments)
    sample = validate_sample_v3(read_json_object(arguments.sample, "quality v3 sample"), policy)
    assessments = _validated_v3_assessments(
        arguments.assessment, sample=sample, policy=policy, matrix=matrix, anchors=anchors,
        prompt_sha256=hashlib.sha256(load_evaluator_prompt_v3(manifest).encode("utf-8")).hexdigest(),
    )
    match = match_assessments_v3(
        sample=sample, left_assessment=assessments[0], right_assessment=assessments[1]
    )
    run_directory = create_quality_run_directory(manifest.root, "issue-match-v3")
    path = run_directory / "issue-match.json"
    write_json(path, match)
    report = {
        "match_id": match["match_id"], "issues": len(match["issues"]),
        "manual_queue": len(match["manual_queue"]), "match": str(path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v3 match issues={report['issues']} manual={report['manual_queue']}")
        print(f"Match: {path}")
    return 0


def _quality_disputes_v3(arguments: argparse.Namespace) -> int:
    manifest, policy, _, _ = _quality_v3_inputs(arguments)
    sample = validate_sample_v3(read_json_object(arguments.sample, "quality v3 sample"), policy)
    match = validate_match_v3(read_json_object(arguments.match, "quality v3 issue match"))
    dispute, identity = build_disputes_v3(match=match, sample=sample, seed=arguments.seed)
    run_directory = create_quality_run_directory(manifest.root, "disputes-v3")
    dispute_path = run_directory / "dispute.json"
    identity_path = run_directory / "dispute-identity.json"
    write_json(dispute_path, dispute)
    write_json(identity_path, identity)
    report = {
        "dispute_id": dispute["dispute_id"], "items": len(dispute["items"]),
        "dispute": str(dispute_path), "identity_mapping": str(identity_path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v3 disputes items={report['items']}")
        print(f"Dispute: {dispute_path}")
        print(f"Identity: {identity_path}")
    return 0


def _quality_adjudicate_v3(arguments: argparse.Namespace) -> int:
    manifest, policy, _, _ = _quality_v3_inputs(arguments)
    match = validate_match_v3(read_json_object(arguments.match, "quality v3 issue match"))
    adjudication = read_json_object(arguments.adjudication, "quality v3 adjudication")
    validation = adjudicate_v3(
        match=match, adjudication=adjudication, policy=policy, strict=arguments.strict
    )
    run_directory = create_quality_run_directory(manifest.root, "adjudication-v3")
    path = run_directory / "adjudication-validation.json"
    write_json(path, validation)
    report = {
        "validation_id": validation["validation_id"], "items": len(validation["items"]),
        "validation": str(path), "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v3 adjudication items={report['items']}")
        print(f"Validation: {path}")
    return 0


def _quality_report_v3(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    match = validate_match_v3(read_json_object(arguments.match, "quality v3 issue match"))
    validation = (
        validate_adjudication_validation_v3(
            read_json_object(arguments.adjudication_validation, "quality v3 adjudication validation"),
            match=match,
        )
        if arguments.adjudication_validation else None
    )
    report = build_report_v3(match=match, adjudication_validation=validation)
    run_directory = create_quality_run_directory(manifest.root, "report-v3")
    path = run_directory / "report.json"
    write_json(path, report)
    summary = {**report, "report": str(path), "run_directory": str(run_directory)}
    if arguments.json:
        _print_json(summary)
    else:
        print(
            f"OK  quality v3 report raw={report['raw_model_metrics']['left_findings']}/"
            f"{report['raw_model_metrics']['right_findings']} "
            f"manual={report['human_burden']['issues_requiring_adjudication']}"
        )
        print(f"Report: {path}")
    return 0


def _quality_stability_v3(arguments: argparse.Namespace) -> int:
    manifest, policy, matrix, anchors = _quality_v3_inputs(arguments)
    if len(arguments.assessment) != 2 or len(arguments.run_report) != 2:
        raise ValidationError("quality stability-v3 requires exactly two assessments and two run reports")
    sample = validate_sample_v3(read_json_object(arguments.sample, "quality v3 stability sample"), policy)
    raw_assessments = [read_json_object(path, "quality v3 stability assessment") for path in arguments.assessment]
    evaluator_ids = {value.get("evaluator", {}).get("id") for value in raw_assessments}
    if len(evaluator_ids) != 1:
        raise ValidationError("quality stability-v3 requires one evaluator identity")
    assessments = [
        validate_assessment_v3(
            value, sample=sample, policy=policy, matrix=matrix, anchors=anchors
        )
        for value in raw_assessments
    ]
    bundles_by_evaluator = {
        evaluator_id: build_evaluator_bundles_v3(
            sample=sample, evaluator_id=evaluator_id, policy=policy,
            matrix=matrix, max_items=policy["max_shard_items"],
        )
        for evaluator_id in policy["evaluator_ids"]
    }
    bundle_hashes = {
        evaluator_id: [canonical_sha256(bundle) for bundle in bundles]
        for evaluator_id, bundles in bundles_by_evaluator.items()
    }
    expected_prompt = hashlib.sha256(load_evaluator_prompt_v3(manifest).encode("utf-8")).hexdigest()
    expected_static = {
        "prompt_sha256": expected_prompt,
        "policy_sha256": canonical_sha256(policy),
        "severity_matrix_sha256": canonical_sha256(matrix),
        "anchors_sha256": canonical_sha256(anchors),
    }
    for assessment in assessments:
        identity = assessment["evaluator"]
        if any(identity.get(field) != digest for field, digest in expected_static.items()):
            raise ValidationError("quality v3 stability assessment frozen hashes differ")
        evaluator_id = identity["id"]
        if (
            identity["bundle_ids"] != [bundle["bundle_id"] for bundle in bundles_by_evaluator[evaluator_id]]
            or identity["bundle_sha256s"] != bundle_hashes[evaluator_id]
        ):
            raise ValidationError("quality v3 stability assessment shard identities differ")
    preregistration = validate_stability_preregistration_v3(
        read_json_object(arguments.preregistration, "quality v3 stability preregistration"),
        sample=sample, policy=policy, matrix=matrix, anchors=anchors,
        prompt_sha256=expected_prompt,
        bundle_ids_by_evaluator={
            evaluator_id: [bundle["bundle_id"] for bundle in bundles]
            for evaluator_id, bundles in bundles_by_evaluator.items()
        },
        bundle_sha256s_by_evaluator=bundle_hashes,
    )
    run_reports = tuple(
        read_json_object(path, "quality v3 runner report") for path in arguments.run_report
    )
    ledger_path = (
        manifest.root / ".artifacts" / "i18n" / "quality" / "calibration-campaigns"
        / f"{preregistration['preregistration_id']}.json"
    )
    campaign_ledger = read_json_object(ledger_path, "quality v3 calibration campaign ledger")
    report = build_stability_report_v3(
        sample=sample, assessments=(assessments[0], assessments[1]),
        run_reports=(run_reports[0], run_reports[1]),
        assessment_sha256s=(bytes_sha256(arguments.assessment[0]), bytes_sha256(arguments.assessment[1])),
        run_report_sha256s=(bytes_sha256(arguments.run_report[0]), bytes_sha256(arguments.run_report[1])),
        preregistration=preregistration,
        campaign_ledger=campaign_ledger,
    )
    run_directory = create_quality_run_directory(manifest.root, "stability-v3")
    path = run_directory / "stability-report.json"
    write_json(path, report)
    if report["passed"]:
        _register_campaign_stability_report(
            root=manifest.root, preregistration=preregistration, report=report,
        )
    summary = {**report, "report": str(path), "run_directory": str(run_directory)}
    if arguments.json:
        _print_json(summary)
    else:
        print(
            f"{'OK' if report['passed'] else 'FAIL'} quality v3 stability "
            f"evaluator={report['evaluator']['id']} "
            f"raw-jaccard={report['metrics']['raw_model']['finding_jaccard']:.3f}"
        )
        print(f"Report: {path}")
    return 0 if report["passed"] else 1


def _quality_facts_study_build(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_facts_study_build(
        manifest, inventory=arguments.inventory,
        exclusions=arguments.exclude_sample, seed=arguments.seed,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Facts study candidate items={report['items']} status={report['status']}")
        print(f"Sample: {report['sample']}")
        print("External preregistration remains blocked until two reviews and adjudication are frozen.")
    return 0


def _quality_facts_study_bundles(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    sample_value = read_json_object(arguments.sample, "facts study sample")
    if sample_value.get("contract") == "tome4-quality-facts-study-sample-v2":
        if arguments.pool is None or arguments.facts_pool is None:
            raise ValidationError(
                "sample v2 requires --pool and --facts-pool for the curation chain"
            )
        report = run_curation_bundles(
            manifest, pool_path=arguments.pool, sample_path=arguments.sample,
            facts_pool_path=arguments.facts_pool, facts_path=arguments.facts,
            gold_path=arguments.gold, gold_review_paths=arguments.gold_review,
            gold_adjudication_path=arguments.gold_adjudication,
        )
    else:
        report = run_facts_study_bundles(
            manifest, sample_path=arguments.sample, facts_path=arguments.facts,
            gold_path=arguments.gold, gold_review_paths=arguments.gold_review,
            gold_adjudication_path=arguments.gold_adjudication,
        )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Facts study preregistered slots={report['slots']} shards={report['shards']}")
        print(f"Preregistration: {report['preregistration']}")
    return 0


def _quality_facts_study_validate(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    prereg_value = read_json_object(arguments.preregistration, "facts study preregistration")
    if prereg_value.get("contract") == "tome4-quality-facts-study-preregistration-v2":
        if arguments.pool is None or arguments.facts_pool is None:
            raise ValidationError(
                "sample v2 requires --pool and --facts-pool for the curation chain"
            )
        report = run_curation_validate(
            manifest, pool_path=arguments.pool, sample_path=arguments.sample,
            facts_pool_path=arguments.facts_pool, facts_path=arguments.facts,
            neutral_path=arguments.neutral, gold_path=arguments.gold,
            prereg_path=arguments.preregistration, bundle_paths=arguments.bundle,
            fake_runner=arguments.fake_runner,
            assessment_paths=arguments.assessment,
            runner_report_paths=arguments.run_report,
            execution_manifest_path=arguments.execution_manifest,
        )
    else:
        report = run_facts_study_validate(
            manifest, sample_path=arguments.sample, facts_path=arguments.facts,
            neutral_path=arguments.neutral, gold_path=arguments.gold,
            prereg_path=arguments.preregistration, bundle_paths=arguments.bundle,
            assessment_paths=arguments.assessment,
            runner_report_paths=arguments.run_report, fake_runner=arguments.fake_runner,
        )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Facts study validation mode={report['mode']} slots=33/33")
        print(f"Validation: {report['validation']}")
    return 0


def _quality_facts_study_report(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    validation_value = read_json_object(arguments.validation, "facts study validation index")
    if validation_value.get("contract") == "tome4-quality-facts-study-validation-index-v2":
        report = run_curation_report(manifest, validation_path=arguments.validation)
    else:
        report = run_facts_study_report(manifest, validation_path=arguments.validation)
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Facts study decision={report['decision']['result']} holdout-clearance=false")
        print(f"Report: {report['report']}")
    return 0


def _quality_facts_study_execution_manifest(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_execution_manifest(
        manifest, preregistration_path=arguments.preregistration,
        authorization_id=arguments.authorization_id, granted_at=arguments.granted_at,
        output_path=arguments.output,
        execution_mode=arguments.mode, concurrency=arguments.concurrency,
        transmission_failure_max_retries=arguments.retry_transmission,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Execution manifest bound to preregistration={report['preregistration_id'][:16]}")
        print(f"Manifest: {report['manifest']}")
    return 0


def _quality_facts_study_curation_build(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_curation_build(
        manifest, inventory=arguments.inventory,
        exclusions=arguments.exclude_sample, seed=arguments.seed,
        protocol_version=arguments.protocol,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Curation pool items={report['items']} protocol={report['protocol_version']} status={report['status']}")
        print(f"Pool: {report['pool']}")
        print("Facts authoring is target-blind; no target-visible role may start before it is frozen.")
    return 0


def _quality_facts_study_curation_prepare(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_curation_prepare(
        manifest, pool_path=arguments.pool, facts_path=arguments.facts,
        inventory_path=arguments.inventory,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  Curator bundle items={report['items']} status={report['status']}")
        print(f"Curator bundle: {report['curator_bundle']}")
    return 0


def _quality_facts_study_curation_select(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = run_curation_select(
        manifest, pool_path=arguments.pool, facts_path=arguments.facts,
        curator_path=arguments.curator, inventory_path=arguments.inventory,
        controlled_variants_path=arguments.controlled_variants,
        seed=arguments.seed, protocol_version=arguments.protocol,
    )
    if arguments.json:
        _print_json(report)
    else:
        if report["status"] == "shortfall":
            print(
                f"SHORTFALL  fact-dependent needed={report['shortfall']['fact_dependent_needed']} "
                f"status_code=2"
            )
            print(f"Controlled variant request: {report['controlled_variant_request']}")
        else:
            print(f"OK  Curation sample study={report['study_id'][:16]} traps={report['fact_traps']}")
            print(f"Sample: {report['sample']}")
    return int(report.get("status_code", 0))
