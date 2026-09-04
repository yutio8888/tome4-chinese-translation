"""Command-line interface for the localization toolchain."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from . import TOOL_VERSION
from .build import build_addon_locale, build_full_locales
from .config import ComponentSpec, Manifest, load_manifest
from .context import resolve_context, validate_context_options
from .errors import I18nToolError, ValidationError
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
from .extract import extract_components, probe_protected_component
from .git_source import GitRepository
from .lint import Issue, lint_documents, lint_terminology, load_policy
from .locale_model import LocaleLoader
from .merge import run_merge
from .proposal import validate_proposal
from .publish import publish_addon
from . import production_review
from . import production_review_v2_lite
from . import production_review_v2_lite_queue
from . import production_review_v2_lite_batch
from . import production_review_v2_lite_migration
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
    validate_report_v3,
    validate_sample_v3,
    validate_stability_report_v3,
    validate_stability_preregistration_v3,
)
from .report import create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_BATCH_SIZE,
    create_review_index,
    review_index_summary,
)
from .runtime import LuaRuntime
from .semantic_claims import DEFAULT_REGISTRY as DEFAULT_CLAIMS_REGISTRY, check_registry
from .status import status_report
from .translation_review import DEFAULT_TRANSLATION_CHARACTER_BUDGET
from .workset import create_workset


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--version-manifest",
        default="tome-1.7.6",
        metavar="VERSION",
        help="version manifest name (default: tome-1.7.6)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="explicit manifest path for the selected --version-manifest",
    )
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/i18n",
        description="ToME4 Chinese localization toolchain",
    )
    parser.add_argument("--tool-version", action="version", version=TOOL_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="validate the pinned toolchain")
    _add_common_arguments(doctor)

    extract = subparsers.add_parser(
        "extract",
        help="extract source strings from pinned Git objects or protected Lua-only inputs",
    )
    _add_common_arguments(extract)
    extract.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="ID",
        help="component to extract; may be repeated",
    )
    extract.add_argument(
        "--all",
        action="store_true",
        help="extract every component with a public or protected source mapping",
    )
    extract.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="per-component extractor timeout in seconds (default: 900)",
    )
    extract.add_argument(
        "--enrich",
        action="store_true",
        help=(
            "produce the enrichment sidecar from the same AST traversal and "
            "build the TU identity index (contract §4.3)"
        ),
    )

    identity = subparsers.add_parser(
        "identity",
        help="TU/entity identity queries and audit (contract §4, §11)",
    )
    identity_subparsers = identity.add_subparsers(
        dest="identity_command", required=True
    )
    identity_show = identity_subparsers.add_parser(
        "show", help="show one TU's anchor/slot/revision/binding"
    )
    _add_common_arguments(identity_show)
    identity_show.add_argument("tu_uid", metavar="TU_UID")
    identity_audit = identity_subparsers.add_parser(
        "audit",
        help="UNKNOWN rate, conflicts and the rename queue between two runs",
    )
    _add_common_arguments(identity_audit)

    lint = subparsers.add_parser("lint", help="validate canonical translations")
    _add_common_arguments(lint)
    lint.add_argument(
        "--component", action="append", default=[], metavar="ID", help="component to lint"
    )
    lint.add_argument(
        "--strict", action="store_true", help="treat warnings as blocking failures"
    )
    lint.add_argument(
        "--baseline",
        metavar="COMMIT",
        help="compare against the frozen baseline for this translation commit",
    )
    lint.add_argument(
        "--incremental",
        metavar="BASE..HEAD",
        help="incremental invalidation over a commit range (contract §8)",
    )
    lint.add_argument(
        "--domain",
        choices=("source", "translation", "rule"),
        default="source",
        help="incremental domain (default: source)",
    )
    lint.add_argument(
        "--self-check",
        action="store_true",
        help="run the whole-set canonical self-check (exit 2 on mismatch)",
    )
    lint.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: new ERROR findings fail with exit code 1",
    )
    lint.add_argument(
        "--legacy-report",
        action="store_true",
        help="expand the folded legacy technical-debt report",
    )

    baseline = subparsers.add_parser(
        "baseline",
        help="frozen baseline snapshots and reports (contract §7)",
    )
    baseline_subparsers = baseline.add_subparsers(
        dest="baseline_command", required=True
    )
    baseline_freeze = baseline_subparsers.add_parser(
        "freeze", help="freeze the current findings as the baseline for a commit"
    )
    _add_common_arguments(baseline_freeze)
    baseline_freeze.add_argument(
        "--commit",
        required=True,
        metavar="COMMIT",
        help="translation repository commit this baseline belongs to",
    )
    baseline_report = baseline_subparsers.add_parser(
        "report", help="new / legacy / resolved statistics"
    )
    _add_common_arguments(baseline_report)
    baseline_report.add_argument(
        "--commit",
        required=True,
        metavar="COMMIT",
        help="translation repository commit to compare against",
    )

    status = subparsers.add_parser(
        "status", help="compare canonical translations with pinned official locales"
    )
    _add_common_arguments(status)
    status.add_argument(
        "--component", action="append", default=[], metavar="ID", help="component to compare"
    )

    build = subparsers.add_parser(
        "build", help="build deterministic full or addon locale artifacts"
    )
    _add_common_arguments(build)
    build.add_argument(
        "--profile",
        required=True,
        choices=("full", "addon"),
        help="artifact profile to build",
    )
    build.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="ID",
        help=(
            "component to build; may be repeated. For addon builds, an explicit "
            "selection is an independently checkable minimal overlay"
        ),
    )
    build.add_argument(
        "--require-complete",
        action="store_true",
        help="fail an addon build when any required component/layer is unavailable",
    )

    publish = subparsers.add_parser(
        "publish",
        help=(
            "publish the core addon overlay into the release addon repository "
            "(dry run by default; use --apply to write)"
        ),
    )
    _add_common_arguments(publish)
    publish.add_argument(
        "--apply",
        action="store_true",
        help="write the artifact into the release repository (default: dry run)",
    )
    publish.add_argument(
        "--bump",
        action="store_true",
        help="bump addon_version patch in release init.lua",
    )
    publish.add_argument(
        "--commit",
        action="store_true",
        help="git add/commit the published files in the release repository",
    )

    merge = subparsers.add_parser(
        "merge", help="classify a snapshot and generate a non-destructive candidate"
    )
    _add_common_arguments(merge)
    merge.add_argument("--component", required=True, metavar="ID")
    merge.add_argument(
        "--snapshot",
        required=True,
        type=Path,
        help="new normalized extraction snapshot.jsonl",
    )
    merge.add_argument(
        "--base-snapshot",
        type=Path,
        help="previous accepted snapshot; omit for bootstrap coverage mode",
    )
    merge.add_argument(
        "--base-tu-index",
        type=Path,
        help="optional base tu_index.jsonl for L1-L5 identity matching",
    )
    merge.add_argument(
        "--new-tu-index",
        type=Path,
        help="optional new tu_index.jsonl for L1-L5 identity matching",
    )

    workset = subparsers.add_parser(
        "workset", help="create a bounded translation workset from a merge report"
    )
    _add_common_arguments(workset)
    workset.add_argument("--merge-report", required=True, type=Path)
    workset.add_argument("--limit", type=int, default=50)
    workset.add_argument(
        "--section",
        dest="section_prefix",
        help="only include sections with this prefix",
    )
    workset.add_argument(
        "--classification",
        choices=("all", "added", "untranslated-existing", "source-changed"),
        default="all",
    )

    context = subparsers.add_parser(
        "context", help="resolve bounded canonical translation and terminology context"
    )
    _add_common_arguments(context)
    context.add_argument("--component", required=True, metavar="ID")
    context.add_argument("--section", dest="section_prefix")
    context.add_argument("--query")
    context.add_argument("--limit", type=int, default=50)

    review = subparsers.add_parser(
        "review",
        help=(
            "offline export of bounded review artifacts (candidate bundles and index) "
            "for an explicit scope; no provider dispatch, does not review"
        ),
    )
    _add_common_arguments(review)
    review.add_argument(
        "--batch-size", type=int, default=DEFAULT_REVIEW_BATCH_SIZE,
        help=(
            "hard maximum items per bundle (default: 10; translation v2 maximum: "
            "10; code v1 maximum: 100)"
        ),
    )
    review.add_argument(
        "--character-budget",
        type=int,
        default=DEFAULT_TRANSLATION_CHARACTER_BUDGET,
        help=(
            "maximum summed canonical JSON characters for translation items per "
            "bundle (default: 24000); the index also records actual payload bytes"
        ),
    )
    review.add_argument(
        "--scope",
        action="append",
        choices=("translations", "code"),
        required=True,
        help="export scope; repeat to include both translations and code",
    )

    proposal = subparsers.add_parser(
        "proposal", help="validate a structured proposal against its workset"
    )
    _add_common_arguments(proposal)
    proposal.add_argument("--workset", required=True, type=Path)
    proposal.add_argument("--proposal", required=True, type=Path)
    proposal.add_argument("--allow-partial", action="store_true")
    proposal.add_argument("--strict", action="store_true")

    claims = subparsers.add_parser(
        "claims", help="validate semantic-claim and runtime-composition registries"
    )
    claims_subparsers = claims.add_subparsers(dest="claims_command", required=True)
    claims_check = claims_subparsers.add_parser(
        "check", help="strictly validate a semantic-claim regression registry"
    )
    claims_check.add_argument(
        "--registry", type=Path, default=DEFAULT_CLAIMS_REGISTRY,
        help=f"registry path (default: {DEFAULT_CLAIMS_REGISTRY})",
    )
    claims_check.add_argument(
        "--strict", action="store_true",
        help="request the normative fail-closed validation profile",
    )
    claims_check.add_argument("--json", action="store_true", help="print machine-readable JSON")

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

    production = subparsers.add_parser(
        "production", help="non-authoritative production-review shadow calibration",
    )
    production_sub = production.add_subparsers(dest="production_command", required=True)
    authoritative = production_sub.add_parser("authoritative-catalog", help="formal WP2-Lite catalog candidate")
    authoritative_sub = authoritative.add_subparsers(dest="production_action", required=True)
    authoritative_build = authoritative_sub.add_parser("build")
    _add_common_arguments(authoritative_build)
    authoritative_build.add_argument("--output", required=True, type=Path)
    authoritative_build.add_argument("--recorded-at")
    authoritative_build.add_argument("--recorded-by", default="WP2L-1 EXECUTOR")
    authoritative_check = authoritative_sub.add_parser("check")
    _add_common_arguments(authoritative_check)
    authoritative_check.add_argument("--candidate-catalog", required=True, type=Path)
    retirement = production_sub.add_parser("wp1-retirement", help="read-only exact WP1 retirement preflight")
    retirement_sub = retirement.add_subparsers(dest="production_action", required=True)
    retirement_preflight = retirement_sub.add_parser("preflight")
    _add_common_arguments(retirement_preflight)
    retirement_preflight.add_argument("--candidate-catalog", required=True, type=Path)
    queue = production_sub.add_parser("queue", help="rebuildable WP2-Lite SQLite projection")
    queue_sub = queue.add_subparsers(dest="production_action", required=True)
    queue_sub.add_parser("init")
    queue_rebuild = queue_sub.add_parser("rebuild")
    queue_rebuild.add_argument("--treeish", default="HEAD")
    queue_sub.add_parser("check")
    queue_status = queue_sub.add_parser("status")
    queue_status.add_argument("--json", action="store_true")
    batch = production_sub.add_parser("batch", help="single WP2-Lite active batch")
    batch_sub = batch.add_subparsers(dest="production_action", required=True)
    batch_start = batch_sub.add_parser("start")
    batch_start.add_argument("--limit", type=int, default=80)
    batch_start.add_argument("--retry-blocked", action="store_true")
    batch_sub.add_parser("show")
    batch_abandon = batch_sub.add_parser("abandon")
    batch_abandon.add_argument("--discard-uncommitted-results", action="store_true")
    batch_abandon.add_argument("--restore-evidence", action="store_true")
    recover = batch_sub.add_parser("recover")
    recover.add_argument("--from-head", action="store_true")
    batch_sub.add_parser("surface-export")
    batch_import = batch_sub.add_parser("surface-import")
    batch_import.add_argument("--input", required=True, type=Path)
    batch_sub.add_parser("contextual-export")
    contextual_import = batch_sub.add_parser("contextual-import")
    contextual_import.add_argument("--input", required=True, type=Path)
    adjudicate = batch_sub.add_parser("adjudicate")
    adjudicate.add_argument("--input", required=True, type=Path)
    batch_sub.add_parser("prepare-evidence")
    finalize = batch_sub.add_parser("finalize")
    finalize.add_argument("--commit", required=True)
    batch_sub.add_parser("recover-from-head")
    migration = production_sub.add_parser("migration", help="quiescent catalog migration")
    migration_sub = migration.add_subparsers(dest="production_action", required=True)
    migration_plan = migration_sub.add_parser("plan")
    migration_plan.add_argument("--candidate-catalog", required=True, type=Path)
    migration_plan.add_argument("--output", type=Path)
    migration_plan.add_argument("--recorded-at")
    migration_plan.add_argument("--recorded-by", default="WP2L-5 EXECUTOR")
    migration_check = migration_sub.add_parser("check")
    migration_check.add_argument("--input", required=True, type=Path)
    migration_check.add_argument("--candidate-catalog", required=True, type=Path)
    migration_apply = migration_sub.add_parser("apply")
    migration_apply.add_argument("--input", required=True, type=Path)
    migration_apply.add_argument("--candidate-catalog", required=True, type=Path)
    repair = production_sub.add_parser("repair", help="committed repair preflight")
    repair_sub = repair.add_subparsers(dest="production_action", required=True)
    repair_preflight = repair_sub.add_parser("preflight")
    _add_common_arguments(repair_preflight)
    repair_preflight.add_argument("--batch-id", required=True)
    repair_preflight.add_argument("--output", type=Path)
    locator = production_sub.add_parser("locator", help="production locator snapshot")
    locator_sub = locator.add_subparsers(dest="production_action", required=True)
    locator_bootstrap = locator_sub.add_parser("bootstrap")
    _add_common_arguments(locator_bootstrap)
    locator_bootstrap.add_argument("--recorded-at", required=True)
    locator_bootstrap.add_argument("--recorded-by", required=True)
    locator_check = locator_sub.add_parser("check")
    locator_check.add_argument("--snapshot", required=True, type=Path)
    locator_check.add_argument("--occurrences", required=True, type=Path)
    locator_check.add_argument("--locators", required=True, type=Path)
    catalog = production_sub.add_parser("catalog", help="production catalog shadow snapshot")
    catalog_sub = catalog.add_subparsers(dest="production_action", required=True)
    catalog_build = catalog_sub.add_parser("build")
    catalog_check = catalog_sub.add_parser("check")
    _add_common_arguments(catalog_build)
    _add_common_arguments(catalog_check)
    for item in (catalog_build, catalog_check):
        item.add_argument("--locator-snapshot", required=True, type=Path)
        item.add_argument("--occurrences", required=True, type=Path)
        item.add_argument("--locators", required=True, type=Path)
        if item is catalog_build:
            item.add_argument("--recorded-at", required=True)
            item.add_argument("--recorded-by", required=True)
        else:
            item.add_argument("--catalog", required=True, type=Path)
            item.add_argument("--entries", required=True, type=Path)
            item.add_argument("--exclusions", required=True, type=Path)
    policy = production_sub.add_parser("shadow-policy", help="shadow queue policy")
    policy_sub = policy.add_subparsers(dest="production_action", required=True)
    policy_build = policy_sub.add_parser("build")
    policy_check = policy_sub.add_parser("check")
    for item in (policy_build, policy_check):
        for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions"):
            item.add_argument(f"--{flag}", required=True, type=Path)
        item.add_argument("--manifest", type=Path)
        item.add_argument("--version-manifest", default="tome-1.7.6")
        if item is policy_check: item.add_argument("--policy", required=True, type=Path)
    journal = production_sub.add_parser("shadow-journal", help="one-shot shadow journal")
    journal_sub = journal.add_subparsers(dest="production_action", required=True)
    journal_bootstrap = journal_sub.add_parser("bootstrap")
    journal_check = journal_sub.add_parser("check")
    for item in (journal_bootstrap, journal_check):
        for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy"):
            item.add_argument(f"--{flag}", required=True, type=Path)
        item.add_argument("--manifest", type=Path); item.add_argument("--version-manifest", default="tome-1.7.6")
        if item is journal_bootstrap:
            item.add_argument("--recorded-at", required=True)
            item.add_argument("--recorded-by", required=True)
        else:
            for flag in ("group", "events", "checkpoint"):
                item.add_argument(f"--{flag}", required=True, type=Path)
    replay = production_sub.add_parser("replay", help="replay shadow journal")
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy", "group", "events", "checkpoint"):
        replay.add_argument(f"--{flag}", required=True, type=Path)
    replay.add_argument("--manifest", type=Path); replay.add_argument("--version-manifest", default="tome-1.7.6")
    replay.add_argument("--detail", action="store_true", help="include queued revision IDs")
    batch = production_sub.add_parser("batch-draft", help="build a non-dispatchable shadow draft")
    batch.add_argument("--shadow", action="store_true", required=True)
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy", "group", "events", "checkpoint"):
        batch.add_argument(f"--{flag}", required=True, type=Path)
    batch.add_argument("--manifest", type=Path); batch.add_argument("--version-manifest", default="tome-1.7.6")
    reconcile = production_sub.add_parser("reconciliation", help="shadow conservation and live-drift report")
    _add_common_arguments(reconcile)
    reconcile.add_argument("action", choices=("report",))
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions",
                 "policy", "group", "events", "checkpoint", "batch"):
        reconcile.add_argument(f"--{flag}", required=True, type=Path)

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
    return parser


def _manifest(arguments: argparse.Namespace) -> Manifest:
    return load_manifest(
        version=arguments.version_manifest,
        manifest_path=arguments.manifest,
    )


def _select_components(
    manifest: Manifest,
    identifiers: Iterable[str],
    *,
    default: str,
) -> list[ComponentSpec]:
    requested = list(identifiers)
    if requested:
        return [
            manifest.component(identifier)
            for identifier in dict.fromkeys(requested)
        ]
    if default == "extract":
        return [component for component in manifest.components if component.extract_by_default]
    if default == "status":
        return [
            component
            for component in manifest.components
            if component.official_locale is not None
        ]
    return list(manifest.components)


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _doctor(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    required_files = [
        manifest.root / manifest.terminology,
        manifest.root / manifest.policy,
        *(manifest.root / component.translation for component in manifest.components),
        *(
            manifest.root / component.copy_fragment
            for component in manifest.components
            if component.copy_fragment is not None
        ),
        *(manifest.root / path for path in manifest.manual_definitions),
    ]
    missing = []
    not_regular = []
    terminology_path = manifest.root / manifest.terminology
    terminology_ok = terminology_path.is_dir() or terminology_path.is_file()
    if not terminology_ok:
        if terminology_path.exists():
            not_regular.append(str(terminology_path))
        else:
            missing.append(str(terminology_path))
    for path in required_files[1:]:
        if path.is_file():
            continue
        if path.exists():
            not_regular.append(str(path))
        else:
            missing.append(str(path))
    if missing or not_regular:
        problems = []
        if missing:
            problems.append("missing: " + ", ".join(missing))
        if not_regular:
            problems.append("not regular files: " + ", ".join(not_regular))
        raise ValidationError(
            "required localization files are invalid: " + "; ".join(problems)
        )

    runtime = LuaRuntime(manifest)
    runtime_report = runtime.doctor()
    repositories: dict[str, Any] = {}
    warnings: list[str] = []
    for name, spec in manifest.repositories.items():
        path = spec.resolve(manifest.root)
        if not path.exists() and not spec.required:
            warnings.append(f"optional repository is absent: {name}: {path}")
            repositories[name] = {"path": str(path), "available": False}
            continue
        repository = GitRepository(path)
        check_worktree = name not in manifest.protected_repositories
        report = repository.validate(
            spec.commit, check_worktree=check_worktree
        )
        report["available"] = True
        if report["clean"] is False:
            warnings.append(f"repository has worktree changes: {name}: {path}")
        if not check_worktree:
            warnings.append(
                f"repository worktree scan skipped because it contains a protected source: {name}"
            )
        repositories[name] = report

    extractor_repository = GitRepository(
        manifest.repository_path(manifest.extractor.repository)
    )
    extractor_repository.validate(
        manifest.extractor.commit, check_worktree=False
    )

    protected_sources: dict[str, Any] = {}
    for component in manifest.components:
        if component.protected_source is None:
            continue
        available = probe_protected_component(manifest, runtime, component)
        protected_sources[component.id] = {
            "available": available,
            "access": "lua-extractor-only",
        }
        if not available:
            warnings.append(
                f"declared protected source is unavailable: {component.id}"
            )

    report = {
        "ok": True,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest": str(manifest.path),
        "runtime": runtime_report,
        "repositories": repositories,
        "protected_sources": protected_sources,
        "extractor_commit": manifest.extractor.commit,
        "warnings": warnings,
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  manifest       {manifest.version}")
        print(
            "OK  runtime        "
            f"{runtime_report['lua_version']} / {runtime_report['luajit_version']}"
        )
        print(
            "OK  LPeg           "
            f"{runtime_report['lpeg_rock_version']} ({runtime_report['lpeg_runtime_version']})"
        )
        for name, repository in repositories.items():
            availability = "OK" if repository.get("available") else "SKIP"
            detail = repository.get("path")
            print(f"{availability:<5}repository      {name}: {detail}")
        for component, protected in protected_sources.items():
            availability = "OK" if protected["available"] else "SKIP"
            print(
                f"{availability:<5}protected source {component}: "
                f"{protected['access']}"
            )
        for warning in warnings:
            print(f"WARN              {warning}")
    return 0


def _extract(arguments: argparse.Namespace) -> int:
    if arguments.timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    manifest = _manifest(arguments)
    components = _select_components(
        manifest, arguments.component, default="extract"
    )
    if arguments.all:
        components = [
            component
            for component in manifest.components
            if (
                component.source_repository is not None and component.sources
            )
            or component.protected_source is not None
        ]
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    report = extract_components(
        manifest,
        runtime,
        components,
        timeout=arguments.timeout,
        enrich=arguments.enrich,
    )
    if arguments.json:
        _print_json(report)
    else:
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} "
                f"{item['tdef_count']:>7} tDef  {item['snapshot_sha256'][:16]}"
            )
        print(f"Artifacts: {report['run_directory']}")
    return 0


def _issue_line(issue: Issue) -> str:
    location = issue.logical_path
    if issue.line is not None:
        location += f":{issue.line}"
    return f"{issue.severity.upper():7} {issue.code:24} {location}  {issue.message}"


def _lint(arguments: argparse.Namespace) -> int:
    if arguments.baseline or arguments.incremental:
        return _lint_identity_mode(arguments)
    manifest = _manifest(arguments)
    components = _select_components(manifest, arguments.component, default="lint")
    policy = load_policy(manifest)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    documents = []
    copy_fragment_documents = []
    for component in components:
        if component.copy_fragment:
            copy_fragment_documents.append(
                (
                    component.id,
                    loader.load_path(
                        manifest.root / component.copy_fragment,
                        logical_path=component.copy_fragment,
                    ),
                )
            )
        documents.append(
            (
                component.id,
                loader.load_path(
                    manifest.root / component.translation,
                    logical_path=component.translation,
                ),
            )
        )
    issues, metrics = lint_documents(documents, policy, require_nonempty=True)
    copy_fragment_issues, copy_fragment_metrics = lint_documents(
        copy_fragment_documents,
        policy,
        require_nonempty=False,
    )
    issues.extend(copy_fragment_issues)
    metrics["copy_fragment_translations"] = copy_fragment_metrics["translations"]
    metrics["copy_fragment_components"] = copy_fragment_metrics["components"]
    metrics["copy_fragment_duplicate_runtime_keys"] = copy_fragment_metrics[
        "duplicate_runtime_keys"
    ]
    terminology_issues, terminology_metrics = lint_terminology(
        manifest.root / manifest.terminology
    )
    issues.extend(terminology_issues)
    metrics["errors"] = sum(issue.severity == "error" for issue in issues)
    metrics["warnings"] = sum(issue.severity == "warning" for issue in issues)
    metrics["terminology"] = terminology_metrics
    report = {
        "ok": metrics["errors"] == 0
        and (not arguments.strict or metrics["warnings"] == 0),
        "version": manifest.version,
        "strict": arguments.strict,
        "metrics": metrics,
        "issues": [issue.to_dict() for issue in issues],
    }
    run_directory = create_run_directory(manifest.root, "lint")
    report["run_directory"] = str(run_directory)
    write_json(run_directory / "lint.json", report)
    if arguments.json:
        _print_json(report)
    else:
        limit = 80
        for issue in issues[:limit]:
            print(_issue_line(issue))
        if len(issues) > limit:
            print(f"... {len(issues) - limit} additional issues are in the JSON report")
        print(
            f"Checked {metrics['translations']} translations: "
            f"{metrics['errors']} errors, {metrics['warnings']} warnings"
        )
        print(f"Report: {run_directory / 'lint.json'}")
    if not report["ok"]:
        raise ValidationError(
            f"lint failed with {metrics['errors']} errors and {metrics['warnings']} warnings"
        )
    return 0


def _current_indexes_for(manifest: Manifest) -> dict[str, Any]:
    """Current identity indexes keyed by component.

    Shares the fail-closed scan with the extract path (V3/V10): a partial
    trio (entities/tu/identity) or a corrupt identity.json raises
    ValidationError instead of being silently skipped, so identity
    show/audit cannot read a half-written component index.
    """
    from .extract import _read_current_indexes

    current_root = manifest.root / ".artifacts" / "i18n" / "identity" / "current"
    if not current_root.is_dir():
        return {}
    return {
        index.component: index for index in _read_current_indexes(current_root)
    }


def _records_by_component(
    records: Iterable[Any],
    components: Iterable[ComponentSpec],
    *,
    indexes: dict[str, Any] | None = None,
) -> dict[str, list[Any]]:
    """Assign FindingRecords to components.

    Translation-path mapping is the primary owner signal, but entity-level
    findings (duplicate-talent-id / duplicate-effect-id) carry a source
    section as their Issue.logical_path, so they never match a translation
    file path. They are attributed through the identity evidence instead:
    the component index whose TUs contain the record's subject/participants
    (never string-matching the section text).
    """
    by_path: dict[str, str] = {}
    for component in components:
        by_path[component.translation] = component.id
        if component.copy_fragment:
            by_path[component.copy_fragment] = component.id
    indexes = indexes or {}

    def via_tu(record: Any) -> str | None:
        for component_id, index in indexes.items():
            if record.tu_uid in index.tus:
                return component_id
        for component_id, index in indexes.items():
            if any(participant in index.tus for participant in record.participants):
                return component_id
        return None

    grouped: dict[str, list[Any]] = {}
    for record in records:
        owner = by_path.get(record.issue.logical_path)
        if owner is None:
            owner = via_tu(record)
        if owner is None:
            continue
        grouped.setdefault(owner, []).append(record)
    return grouped


def _identity_show(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    tu_uid = arguments.tu_uid
    indexes = _current_indexes_for(manifest)
    match = None
    owner = None
    for component, index in indexes.items():
        tu = index.tus.get(tu_uid)
        if tu is not None:
            match = tu
            owner = component
            break
    if match is None:
        raise ValidationError(
            f"TU {tu_uid} not found in the current identity indexes; "
            "run extract --enrich first"
        )
    entity = None
    if match.entity_uid is not None:
        entity = indexes[owner].entities.get(match.entity_uid)
    report = {
        "tu": match.to_dict(),
        "entity": entity.to_dict() if entity is not None else None,
        "component": owner,
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"TU      {match.tu_uid}")
        print(f"binding {match.identity_binding}  component={match.component}")
        print(
            f"entity  {match.entity_uid or '-'}  kind={match.kind}  "
            f"anchor={match.anchor_key or '-'}"
        )
        print(f"slot    {match.semantic_slot}  discriminator={match.discriminator}")
        print(f"sections {', '.join(match.sections[:5])}")
        for revision in match.revisions:
            print(
                f"rev     {revision.revision_uid[:16]}  "
                f"source={revision.source!r}"
            )
    return 0


def _identity_audit(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    components = _select_components(manifest, [], default="extract")
    from .identity import diff_indexes
    from .pipeline import extract_enriched

    previous = _current_indexes_for(manifest)
    current, extract_report = extract_enriched(manifest, runtime, components)
    events: list[dict[str, Any]] = []
    for component in components:
        if component.id not in current:
            continue
        new_index = current[component.id]
        old_index = previous.get(component.id)
        if old_index is not None:
            events.extend(
                event.to_dict()
                for event in diff_indexes(base=old_index, new=new_index)
            )
        else:
            for uid, entity in new_index.entities.items():
                events.append(
                    {
                        "kind": "created",
                        "component": component.id,
                        "entity_kind": entity.kind,
                        "section": (
                            sorted(entity.sections)[0] if entity.sections else None
                        ),
                        "old_anchor_key": None,
                        "new_anchor_key": entity.anchor_key,
                        "old_entity_uid": None,
                        "new_entity_uid": uid,
                        "similarity": None,
                    }
                )
    summary: dict[str, int] = {}
    for event in events:
        kind = event.get("kind")
        summary[kind] = summary.get(kind, 0) + 1
    rename_queue = [
        event
        for event in events
        if event.get("kind") in ("rename_candidate", "ambiguous", "hint")
    ]
    report = {
        "ok": True,
        "events": events,
        "rename_queue": rename_queue,
        "summary": summary,
        "components": {
            component.id: current[component.id].stats
            for component in components
            if component.id in current
        },
        "extract_run_directory": extract_report.get("run_directory"),
    }
    run_directory = create_run_directory(manifest.root, "identity-audit")
    write_json(run_directory / "audit.json", report)
    report["run_directory"] = str(run_directory)
    if arguments.json:
        _print_json(report)
    else:
        for component in components:
            if component.id not in current:
                continue
            stats = current[component.id].stats
            print(
                f"OK  {component.id:<16} tus={stats['tus']} "
                f"strong={stats['strong_tus']} "
                f"unknown_fallback={stats['unknown_fallback_occurrences']} "
                f"conflicts={stats['conflicts']}"
            )
        print(
            f"Events: unchanged={summary.get('unchanged', 0)} "
            f"created={summary.get('created', 0)} "
            f"deleted={summary.get('deleted', 0)} "
            f"rename_candidate={summary.get('rename_candidate', 0)} "
            f"ambiguous={summary.get('ambiguous', 0)} "
            f"hint={summary.get('hint', 0)}"
        )
        if rename_queue:
            print(f"Rename queue: {len(rename_queue)} entries (see audit.json)")
        print(f"Report: {run_directory / 'audit.json'}")
    return 0


def _verify_freeze_provenance(manifest: Manifest, requested_commit: str) -> str:
    """Bind a `baseline freeze --commit` label to the translation repo HEAD.

    Contract §7.1: the commit in the baseline filename is the translation
    repository commit this baseline was generated from, and a baseline whose
    generation environment cannot be rebuilt is invalid for CI. To keep that
    honest for a personal project, the caller-supplied commit must resolve to
    exactly the current HEAD and the tracked/index worktree must be clean, so a
    dirty worktree can never masquerade as a frozen commit.
    """
    from .errors import ContractError

    repository = GitRepository(manifest.root)
    resolved = repository.resolve_commit(requested_commit)
    head = repository.resolve_commit("HEAD")
    if resolved != head:
        raise ContractError(
            f"baseline freeze --commit {requested_commit!r} resolves to "
            f"{resolved[:12]} but the translation repository HEAD is "
            f"{head[:12]}; a frozen baseline must be generated from the "
            "current HEAD (commit your changes first)"
        )
    status = repository.worktree_porcelain()
    if status.strip():
        raise ContractError(
            "translation repository worktree is not clean; a baseline must be "
            "frozen from a committed tree (stash or commit your changes first):\n"
            + status.rstrip()
        )
    return resolved


def _baseline_freeze(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    components = _select_components(manifest, [], default="lint")
    from .baseline import write_baseline
    from .pipeline import run_enriched_lint

    frozen_commit = _verify_freeze_provenance(manifest, arguments.commit)
    pipeline = run_enriched_lint(manifest, runtime, loader, components)
    extractable_ids = set(pipeline["indexes"])
    records_by_component = _records_by_component(
        pipeline["records"], components, indexes=pipeline["indexes"]
    )

    frozen: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for component in components:
        if component.id not in extractable_ids:
            skipped.append(
                {
                    "component": component.id,
                    "reason": "no reproducible source extraction",
                    "findings": len(records_by_component.get(component.id, [])),
                }
            )
            continue
        records = records_by_component.get(component.id, [])
        snapshot_sha = next(
            (
                item["snapshot_sha256"]
                for item in pipeline["extract"].get("components", [])
                if item["component"] == component.id
            ),
            "",
        )
        engine_commit = (
            manifest.repositories[component.source_repository].commit
            if component.source_repository
            else ""
        )
        baseline = write_baseline(
            manifest_root=manifest.root,
            component=component.id,
            translation_commit=frozen_commit,
            source_snapshot_sha256=snapshot_sha,
            engine_commit=engine_commit,
            extractor_commit=manifest.extractor.commit,
            rules_registry_sha256=pipeline["registries"]["rules_registry_sha256"],
            slot_registry_sha256=pipeline["registries"]["slot_registry_sha256"],
            records=records,
        )
        frozen.append(
            {
                "component": component.id,
                "entries": len(baseline.entries),
                "baseline": str(baseline.path),
                "sha256": baseline.sha256,
            }
        )
    report = {
        "ok": True,
        "translation_commit": frozen_commit,
        "components": frozen,
        "skipped": skipped,
        "metrics": pipeline["metrics"],
        "binding": pipeline["binding"],
    }
    if arguments.json:
        _print_json(report)
    else:
        for item in frozen:
            print(f"OK  {item['component']:<16} baseline={item['entries']} findings")
        for item in skipped:
            print(
                f"SKIP {item['component']:<16} {item['reason']} "
                f"({item['findings']} findings unbaselined)"
            )
        print(f"Baselines frozen for translation commit {frozen_commit}")
    return 0


def _resolve_translation_commit(manifest: Manifest, requested: str) -> str:
    """Resolve a `--commit` label to a full translation-repository commit OID.

    Baselines are keyed and named by the full OID (§7.1); a short sha or rev
    expression from the operator is canonicalized here so freeze/report/lint
    all address the same on-disk artifact. An unresolvable label is a
    contract-level failure.
    """
    repository = GitRepository(manifest.root)
    return repository.resolve_commit(requested)


def _load_required_baselines(
    manifest: Manifest,
    *,
    components: list[ComponentSpec],
    indexes: dict[str, Any],
    commit: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load baselines for the components that have reproducible extraction.

    Fail-closed (§7.1): every component present in ``indexes`` (i.e. with a
    reproducible source extraction this run) MUST have a loadable, intact
    baseline; a missing or corrupt one is a ValidationError, never a silent
    skip. Components without reproducible extraction are the only legitimate
    absence and are returned explicitly as ``skipped``. An empty required
    set (no component demands a baseline) is also a failure: a CI gate over
    no valid baseline cannot return success.
    """
    from .baseline import read_baseline

    required = [component for component in components if component.id in indexes]
    skipped = [
        {
            "component": component.id,
            "reason": "no reproducible source extraction",
        }
        for component in components
        if component.id not in indexes
    ]
    if not required:
        raise ValidationError(
            f"no reproducible-extraction component demands a baseline for "
            f"commit {commit}; a CI gate over an empty valid set cannot pass"
        )
    baselines: dict[str, Any] = {}
    load_errors: list[tuple[str, str]] = []
    for component in required:
        try:
            baselines[component.id] = read_baseline(
                manifest.root,
                component=component.id,
                translation_commit=commit,
            )
        except ValidationError as error:
            load_errors.append((component.id, str(error)))
    if load_errors:
        details = "; ".join(f"{cid}: {msg}" for cid, msg in load_errors)
        raise ValidationError(
            f"missing or corrupt baselines for commit {commit}; refusing CI "
            f"judgement (fail-closed): {details}"
        )
    return baselines, skipped


def _baseline_report(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    components = _select_components(manifest, [], default="lint")
    from .baseline import ci_gate, compute_baseline_state
    from .pipeline import run_enriched_lint, validate_baselines

    pipeline = run_enriched_lint(manifest, runtime, loader, components)
    records_by_component = _records_by_component(
        pipeline["records"], components, indexes=pipeline["indexes"]
    )

    resolved_commit = _resolve_translation_commit(manifest, arguments.commit)
    baselines, skipped = _load_required_baselines(
        manifest,
        components=components,
        indexes=pipeline["indexes"],
        commit=resolved_commit,
    )
    validate_baselines(
        manifest,
        baselines=baselines,
        extract_report=pipeline["extract"],
        registries=pipeline["registries"],
    )
    states: dict[str, dict[str, Any]] = {}
    total_gate: dict[str, int] = {
        "new_errors": 0,
        "new_warnings": 0,
        "legacy_errors": 0,
        "legacy_warnings": 0,
        "resolved": 0,
    }
    for component_id, baseline in baselines.items():
        state = compute_baseline_state(
            baseline, records_by_component.get(component_id, [])
        )
        passed, gate = ci_gate(state)
        for key in total_gate:
            total_gate[key] += gate[key]
        states[component_id] = {
            "passed": passed,
            "gate": gate,
            "new": [record.to_dict() for record in state.new],
            "legacy": [record.to_dict() for record in state.legacy],
            "resolved": [entry.to_dict() for entry in state.resolved],
            "legacy_on_touched_tu": list(state.legacy_on_touched_tu),
        }
    report = {
        "ok": bool(baselines) and all(state["passed"] for state in states.values()),
        "translation_commit": resolved_commit,
        "components": states,
        "skipped": skipped,
        "totals": total_gate,
        "binding": pipeline["binding"],
    }
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"baseline report vs {resolved_commit}: "
            f"new_errors={total_gate['new_errors']} "
            f"new_warnings={total_gate['new_warnings']} "
            f"legacy_errors={total_gate['legacy_errors']} "
            f"legacy_warnings={total_gate['legacy_warnings']} "
            f"resolved={total_gate['resolved']}"
        )
        for component_id, state in states.items():
            for record in state["new"][:20]:
                print(
                    f"NEW  {component_id:<16} {record['code']:24} "
                    f"{record['message'][:100]}"
                )
    if not report["ok"]:
        raise ValidationError(
            f"baseline gate failed: {total_gate['new_errors']} new errors"
        )
    return 0


def _lint_identity_mode(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    if arguments.baseline:
        components = _select_components(manifest, arguments.component, default="lint")
        from .baseline import ci_gate, compute_baseline_state
        from .pipeline import run_enriched_lint, validate_baselines

        pipeline = run_enriched_lint(manifest, runtime, loader, components)
        records_by_component = _records_by_component(
            pipeline["records"], components, indexes=pipeline["indexes"]
        )
        resolved_commit = _resolve_translation_commit(
            manifest, arguments.baseline
        )
        baselines, skipped = _load_required_baselines(
            manifest,
            components=components,
            indexes=pipeline["indexes"],
            commit=resolved_commit,
        )
        validate_baselines(
            manifest,
            baselines=baselines,
            extract_report=pipeline["extract"],
            registries=pipeline["registries"],
        )
        new_errors = 0
        report_states: dict[str, dict[str, Any]] = {}
        for component_id, baseline in baselines.items():
            records = records_by_component.get(component_id, [])
            state = compute_baseline_state(baseline, records)
            passed, gate = ci_gate(state)
            new_errors += gate["new_errors"]
            report_states[component_id] = {
                "passed": passed,
                "gate": gate,
                "new": [record.to_dict() for record in state.new],
                "legacy": [record.to_dict() for record in state.legacy],
                "resolved": [entry.to_dict() for entry in state.resolved],
            }
        report = {
            "ok": bool(baselines) and new_errors == 0,
            "mode": "baseline",
            "translation_commit": resolved_commit,
            "components": report_states,
            "skipped": skipped,
            "binding": pipeline["binding"],
        }
        run_directory = create_run_directory(manifest.root, "lint-baseline")
        write_json(run_directory / "lint.json", report)
        report["run_directory"] = str(run_directory)
        if arguments.json:
            _print_json(report)
        else:
            print(
                f"baseline {resolved_commit}: new errors={new_errors} "
                f"({'OK' if new_errors == 0 else 'FAIL'})"
            )
            for component_id, state in report_states.items():
                gate = state["gate"]
                print(
                    f"  {component_id:<16} new_err={gate['new_errors']} "
                    f"new_warn={gate['new_warnings']} "
                    f"legacy_err={gate['legacy_errors']} "
                    f"legacy_warn={gate['legacy_warnings']} "
                    f"resolved={gate['resolved']}"
                )
                if arguments.legacy_report:
                    for record in state["legacy"][:50]:
                        print(
                            f"    LEGACY {record['code']:24} "
                            f"{record['message'][:80]}"
                        )
        if arguments.ci and new_errors > 0:
            from .errors import I18nToolError

            raise I18nToolError(
                f"baseline CI gate failed: {new_errors} new errors"
            )
        return 0

    # --incremental
    base, head = arguments.incremental.split("..", 1)
    if not base or not head:
        raise ValidationError("--incremental expects BASE..HEAD")
    if arguments.domain == "source":
        from .git_source import GitRepository
        from .incremental import incremental_source_flow

        repository_name = manifest.repositories["engine"].name
        engine_repository = GitRepository(manifest.repository_path(repository_name))
        base = engine_repository.resolve_commit(base)
        head = engine_repository.resolve_commit(head)
        components = _select_components(manifest, arguments.component, default="lint")
        artifact_directory = (
            create_run_directory(manifest.root, "lint-incremental")
            if arguments.self_check
            else None
        )
        result = incremental_source_flow(
            manifest=manifest,
            runtime=runtime,
            loader=loader,
            components=components,
            engine_repository=engine_repository,
            base_commit=base,
            head_commit=head,
            self_check=arguments.self_check,
            artifact_directory=artifact_directory,
        )
        report = dict(result)
        report["ok"] = True
        # Keep the self-check verdict separate from the aggregated ok: the
        # exception dispatch must follow the actual gate that failed, not the
        # render-only aggregate (FR2 regression fix: --self-check --ci with a
        # passed self-check and new ERRORs must raise I18nToolError/exit 1,
        # not IncrementalCheckError/exit 2; a failed self-check keeps exit 2
        # priority). The aggregated ok still expresses ANY enabled gate
        # failure for the JSON/text render.
        self_check_failed = False
        if arguments.self_check and result.get("self_check") is not None:
            self_check_failed = not result["self_check"]["passed"]
            report["ok"] = result["self_check"]["passed"]
        # FR2: the JSON/text ok must agree with the CI gate. The flow already
        # reports new_errors; when --ci is passed a non-zero count flips ok
        # to False BEFORE any render (the raise below keeps the established
        # exit code and fingerprint message). Without --ci the counts never
        # influence ok (V7).
        ci = result.get("ci") or {}
        new_error_count = ci.get("new_errors", 0)
        if arguments.ci and new_error_count > 0:
            report["ok"] = False
        if arguments.json:
            _print_json(report)
        else:
            findings = result["findings"]
            print(
                f"incremental {arguments.incremental} domain=source: "
                f"affected_tus={result['affected_tus']} "
                f"previous={findings['previous']} kept={findings['kept']} "
                f"recomputed={findings['recomputed']} "
                f"incremental={findings['incremental']}"
            )
            if result.get("deleted_files"):
                print(f"deleted_files: {len(result['deleted_files'])}")
            if result.get("widened_components"):
                print(f"widened: {sorted(result['widened_components'])}")
            ci = result.get("ci") or {}
            print(
                f"ci: new_errors={ci.get('new_errors', 0)} "
                f"legacy_errors={ci.get('legacy_errors', 0)}"
            )
            if result.get("self_check") is not None:
                check = result["self_check"]
                print(
                    f"self-check: {'PASS' if check['passed'] else 'MISMATCH'} "
                    f"(full={check['full_findings']})"
                )
        if arguments.self_check and self_check_failed:
            from .errors import IncrementalCheckError

            raise IncrementalCheckError(
                "incremental self-check failed: canonical forms differ"
            )
        if arguments.ci:
            from .errors import I18nToolError

            # §7.4/§11: only NEW ERROR findings (recomputed errors whose
            # fingerprint is absent from the base error fingerprints) fail
            # the gate; legacy ERROR stays technical debt (H3). The flow
            # reports new_errors directly so the CLI never miscounts from
            # the final full records set.
            first_fingerprint = (ci.get("new_error_fingerprints") or [""])[0]
            if new_error_count:
                detail = (
                    f" (first fingerprint: {first_fingerprint})"
                    if first_fingerprint
                    else ""
                )
                raise I18nToolError(
                    "incremental CI gate failed: "
                    f"{new_error_count} new ERROR findings{detail}"
                )
        return 0
    if arguments.domain == "rule":
        return _lint_incremental_rule(arguments, manifest, runtime, loader)
    if arguments.domain == "translation":
        return _lint_incremental_translation(arguments, manifest, runtime, loader)
    raise AssertionError(f"unhandled domain: {arguments.domain}")


def _changed_editorial_keys(
    base_entries: Iterable[dict[str, Any]],
    head_entries: Iterable[dict[str, Any]],
    semantic: Any,
) -> set[tuple[str, str, str | None]]:
    """H4/D5/R5/R8: bidirectional added / deleted / semantically-changed keys.

    Each (section, source, source_tag) key carries a multiset of occurrence
    identities - (semantic payload, line) - because the same key can
    legitimately repeat; a key is affected when its base and head multisets
    differ. A dict that keeps only the last occurrence would fold a
    duplicated defective occurrence into invisibility (R5); the occurrence
    line is part of the identity so a pure reorder of duplicated occurrences
    still recomputes the record against the head document (R8: the kept
    base record would otherwise carry stale issue metadata and diverge from
    the full-head canonical form).
    """
    base_by_key: dict[
        tuple[str, str, str | None], Counter[tuple[Any, Any]]
    ] = defaultdict(Counter)
    head_by_key: dict[
        tuple[str, str, str | None], Counter[tuple[Any, Any]]
    ] = defaultdict(Counter)
    for entry in base_entries:
        base_by_key[
            (entry.get("section"), entry.get("source"), entry.get("source_tag"))
        ][(semantic(entry), entry.get("line"))] += 1
    for entry in head_entries:
        head_by_key[
            (entry.get("section"), entry.get("source"), entry.get("source_tag"))
        ][(semantic(entry), entry.get("line"))] += 1
    return {
        key
        for key in set(base_by_key) | set(head_by_key)
        if base_by_key.get(key, Counter()) != head_by_key.get(key, Counter())
    }


def _rule_signature(rule: Any) -> tuple[Any, ...]:
    """H4: the full semantic signature of a rule entry.

    schema_version / severity / evidence_key_spec changes alter the frozen
    fingerprint (§6.1), so they must drive recomputation even when the
    rule_id set is unchanged."""
    return (
        rule.rule_id,
        rule.schema_version,
        rule.severity,
        rule.evidence_key_spec,
    )


def affected_rule_ids(
    base_registry: Any, head_registry: Any
) -> frozenset[str]:
    """Rule IDs whose semantic signature differs between two registries."""
    base_signatures = {_rule_signature(rule) for rule in base_registry.rules.values()}
    head_signatures = {_rule_signature(rule) for rule in head_registry.rules.values()}
    return frozenset(signature[0] for signature in base_signatures ^ head_signatures)


def _lint_incremental_rule(
    arguments: argparse.Namespace,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
) -> int:
    from .errors import ContractError
    from .fingerprint import RuleRegistry
    from .findings import FindingContext, build_finding_records
    from .git_source import GitRepository
    from .identity import (
        RULES_REGISTRY_RELATIVE_PATH,
        UnloadedSources,
    )
    from .lint import parse_policy
    from .pipeline import extract_enriched, lint_documents_specs

    repository = GitRepository(manifest.root)
    base, head = arguments.incremental.split("..", 1)
    base = repository.resolve_commit(base)
    head = repository.resolve_commit(head)
    changed = repository.changed_paths(base, head)
    registry_path = "i18n/quality/rules-registry-v1.json"
    policy_path = "i18n/policy.json"
    unloaded_path = "i18n/quality/unloaded-sources-v1.json"
    registry_changed = registry_path in changed
    policy_changed = policy_path in changed
    unloaded_changed = unloaded_path in changed

    # H4/V4: the head registry/policy come from the resolved head commit
    # blob (required, fail-closed) - uncommitted worktree content can never
    # masquerade as head. The base side comes from the base blob when the
    # file changed in the range, otherwise it equals head. Every read is
    # strict: corrupt/missing JSON aborts instead of silently falling back.
    head_registry_data = _read_commit_json(
        repository, head, registry_path, "rule registry"
    )
    head_registry = RuleRegistry.from_dict(
        head_registry_data, label=f"rule registry@{head[:12]}"
    )
    if registry_changed:
        base_registry = RuleRegistry.from_dict(
            _read_commit_json(repository, base, registry_path, "rule registry"),
            label=f"rule registry@{base[:12]}",
        )
    else:
        base_registry = head_registry

    affected_rules: set[str] = set()
    if registry_changed:
        affected_rules |= set(
            affected_rule_ids(base_registry, head_registry)
        )
    head_policy_data = _read_commit_json(
        repository, head, policy_path, "lint policy"
    )
    head_policy = parse_policy(head_policy_data, label=f"lint policy@{head[:12]}")
    if policy_changed:
        base_policy = parse_policy(
            _read_commit_json(repository, base, policy_path, "lint policy"),
            label=f"lint policy@{base[:12]}",
        )
        # D3: the three policy allowlists are consumed only by these four
        # rules (lint.py _format_issue/_format_shape_issue/empty-target/
        # runtime-collision), so a policy change recomputes exactly them.
        affected_rules |= {
            "format-mismatch",
            "format-shape-difference",
            "empty-target",
            "runtime-collision",
        }
    else:
        base_policy = head_policy
    # R4: the unloaded-sources registry is a rule-domain dependency: an
    # exemption change toggles duplicate-talent-id / duplicate-effect-id
    # ERROR findings. Loaded strictly from base/head blobs (fail-closed);
    # the head side is always required, so a corrupt/missing active registry
    # aborts even when nothing else changed.
    head_unloaded = UnloadedSources.from_dict(
        _read_commit_json(
            repository, head, unloaded_path, "unloaded-sources registry"
        ),
        label=f"unloaded-sources registry@{head[:12]}",
    )
    if unloaded_changed:
        base_unloaded = UnloadedSources.from_dict(
            _read_commit_json(
                repository, base, unloaded_path, "unloaded-sources registry"
            ),
            label=f"unloaded-sources registry@{base[:12]}",
        )
        affected_rules |= {"duplicate-talent-id", "duplicate-effect-id"}
    else:
        base_unloaded = head_unloaded
    if not affected_rules:
        # No rule/policy semantic change: F_new == F_previous, so both flags
        # hold trivially; they are reported explicitly, never silently
        # dropped. The active registry was validated above (fail-closed).
        report = {
            "domain": "rule",
            "base": base,
            "head": head,
            "registry_changed": registry_changed,
            "policy_changed": policy_changed,
            "unloaded_changed": unloaded_changed,
            "affected_rules": [],
            "findings": 0,
            "ok": True,
        }
        if arguments.self_check:
            report["self_check"] = {"passed": True, "full_findings": 0}
        report["ci"] = {"new_errors": 0, "legacy_errors": 0}
        if arguments.json:
            _print_json(report)
        else:
            print(f"rule domain: no rule change in {base}..{head}")
        return 0
    components = _select_components(manifest, arguments.component, default="lint")
    indexes, _ = extract_enriched(manifest, runtime, components)
    # V4: translation documents come from the resolved head commit blobs
    # (never the worktree).
    specs, _ = _document_specs_at_commit(repository, loader, components, head)

    def records_for(
        issues: Any, contexts: Any, registry: Any, unloaded: Any
    ) -> list[Any]:
        bound = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=indexes.get(context.component),
            )
            for name, context in contexts.items()
        }
        conflicts: list[Any] = []
        for index in indexes.values():
            conflicts.extend(index.conflicts)
        records, _ = build_finding_records(
            registry=registry,
            issues=issues,
            contexts=bound,
            conflicts=conflicts,
            unloaded_sources=unloaded,
        )
        return records

    issues_head, contexts_head, _ = lint_documents_specs(
        manifest, specs, policy=head_policy
    )
    issues_base, contexts_base, _ = lint_documents_specs(
        manifest, specs, policy=base_policy
    )
    # R4: base records use the base unloaded registry, head records the head
    # one (an exemption change alters which duplicate ERRORs are emitted).
    head_records = records_for(
        issues_head, contexts_head, head_registry, head_unloaded
    )
    base_records = records_for(
        issues_base, contexts_base, base_registry, base_unloaded
    )
    # F_new = (F_previous - findings(affected)) + recompute(affected)
    f_new = tuple(
        sorted(
            [
                *[record for record in base_records if record.rule_id not in affected_rules],
                *[record for record in head_records if record.rule_id in affected_rules],
            ],
            key=lambda record: record.fingerprint,
        )
    )
    base_error_fingerprints = frozenset(
        record.fingerprint
        for record in base_records
        if record.issue.severity == "error"
    )
    new_error_count = sum(
        1
        for record in f_new
        if record.issue.severity == "error"
        and record.fingerprint not in base_error_fingerprints
    )
    legacy_error_count = sum(
        1
        for record in f_new
        if record.issue.severity == "error"
        and record.fingerprint in base_error_fingerprints
    )
    report = {
        "domain": "rule",
        "base": base,
        "head": head,
        "registry_changed": registry_changed,
        "policy_changed": policy_changed,
        "unloaded_changed": unloaded_changed,
        "affected_rules": sorted(affected_rules),
        "findings": {
            "previous": len(base_records),
            "incremental": len(f_new),
        },
        "records": [record.to_dict() for record in f_new],
        "ok": True,
    }
    if arguments.self_check:
        from .invalidation import self_check as canonical_self_check

        passed = canonical_self_check(incremental=f_new, full=head_records)
        report["self_check"] = {
            "passed": passed,
            "full_findings": len(head_records),
        }
        report["ok"] = report["ok"] and passed
    # V6/V7: counts are always reported; only --ci turns them into a gate.
    report["ci"] = {
        "new_errors": new_error_count,
        "legacy_errors": legacy_error_count,
    }
    if arguments.ci:
        report["ok"] = report["ok"] and new_error_count == 0
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"rule domain: affected rules={sorted(affected_rules)} "
            f"previous={len(base_records)} incremental={len(f_new)}"
        )
        if report.get("self_check") is not None:
            print(
                f"self-check: "
                f"{'PASS' if report['self_check']['passed'] else 'MISMATCH'}"
            )
        if report.get("ci") is not None:
            print(f"ci: new_errors={report['ci']['new_errors']}")
    if arguments.self_check and report["self_check"]["passed"] is False:
        from .errors import IncrementalCheckError

        raise IncrementalCheckError(
            "incremental self-check failed: canonical forms differ"
        )
    if arguments.ci and new_error_count > 0:
        from .errors import I18nToolError

        raise I18nToolError(
            f"incremental CI gate failed: {new_error_count} new ERROR findings"
        )
    return 0


def _load_document_at(
    repository: GitRepository,
    loader: LocaleLoader,
    commit: str,
    logical_path: str,
) -> Any | None:
    """Load a logical translation document at ``commit``; None only when the
    file is genuinely absent there. Git failures and Lua loader errors
    propagate (fail closed): a corrupt document is never treated as missing
    and an absent one is never mistaken for a broken repository."""
    blob = repository.read_blob_optional(commit, logical_path)
    if blob is None:
        return None
    return loader.load_bytes(blob, logical_path=logical_path)


def _document_specs_at_commit(
    repository: GitRepository,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
    commit: str,
) -> tuple[list[tuple[str, Any, bool]], dict[tuple[str, str], Any | None]]:
    """Load main + copy documents of every component at ``commit``.

    Returns (specs, docs_by_file) where docs_by_file maps (component_id,
    logical_path) to the document or None when the file is absent at that
    commit. The logical path stays identical across commits so identical
    entries produce identical Issue logical_paths (self-check parity).
    """
    specs: list[tuple[str, Any, bool]] = []
    docs: dict[tuple[str, str], Any | None] = {}
    for component in components:
        main = _load_document_at(repository, loader, commit, component.translation)
        docs[(component.id, component.translation)] = main
        if main is not None:
            specs.append((component.id, main, False))
        if component.copy_fragment:
            copy = _load_document_at(
                repository, loader, commit, component.copy_fragment
            )
            docs[(component.id, component.copy_fragment)] = copy
            if copy is not None:
                specs.append((component.id, copy, True))
    return specs, docs


def _read_commit_json(
    repository: GitRepository,
    commit: str,
    relative: str,
    label: str,
) -> dict[str, Any]:
    """Read and parse a required JSON artifact at ``commit`` (fail closed)."""
    from .errors import ContractError

    blob = repository.read_blob_optional(commit, relative)
    if blob is None:
        raise ContractError(f"{label} is missing at {commit[:12]}")
    try:
        data = json.loads(blob.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(
            f"{label}@{commit[:12]} is not valid JSON: {error}"
        ) from error
    if not isinstance(data, dict):
        raise ContractError(f"{label}@{commit[:12]} must be an object")
    return data


def _bind_identity_contexts(
    contexts: dict[str, Any], indexes: dict[str, Any]
) -> dict[str, Any]:
    """FR1: ensure a component-key identity context exists for every indexed
    component.

    Entity-conflict participants are resolved through ``contexts.get(component)``
    in build_finding_records; when a translation document is absent at a
    commit (head-only main/copy), that context would be missing and the
    conflict would fall back to a synthetic participant TU - producing a
    different fingerprint than the side where the document exists. The
    identity binding therefore never depends on document presence: an
    existing main context keeps its entries and gets the index bound, a
    missing one becomes an identity-only context (empty entries, index
    bound). Translation-entry lookups are unaffected (empty entries add no
    groups; _bind still walks every context including the copy fragment).
    """
    from .findings import FindingContext

    bound = dict(contexts)
    for component_id, index in indexes.items():
        existing = bound.get(component_id)
        if existing is not None:
            bound[component_id] = FindingContext(
                component=component_id,
                entries=existing.entries,
                index=index,
            )
        else:
            bound[component_id] = FindingContext(
                component=component_id, entries=(), index=index
            )
    return bound


def _lint_incremental_translation(
    arguments: argparse.Namespace,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
) -> int:
    from .errors import I18nToolError
    from .fingerprint import RuleRegistry
    from .findings import FindingContext, build_finding_records
    from .git_source import GitRepository
    from .identity import (
        RULES_REGISTRY_RELATIVE_PATH,
        UNLOADED_SOURCES_RELATIVE_PATH,
        UnloadedSources,
        tu_uid_fallback,
    )
    from .lint import parse_policy, stable_entry_id
    from .pipeline import extract_enriched, lint_documents_specs

    repository = GitRepository(manifest.root)
    base, head = arguments.incremental.split("..", 1)
    base = repository.resolve_commit(base)
    head = repository.resolve_commit(head)
    changed = repository.changed_paths(base, head)
    components = _select_components(manifest, arguments.component, default="lint")
    affected_components = [
        component
        for component in components
        if component.translation in changed
        or (
            component.copy_fragment is not None
            and component.copy_fragment in changed
        )
    ]
    if not affected_components:
        # No translation changed: F_new == F_previous, both flags hold
        # trivially; they are reported explicitly, never silently dropped.
        report = {
            "domain": "translation",
            "base": base,
            "head": head,
            "affected_components": [],
            "affected_tus": 0,
            "ok": True,
        }
        if arguments.self_check:
            report["self_check"] = {"passed": True, "full_findings": 0}
        report["ci"] = {"new_errors": 0, "legacy_errors": 0}
        if arguments.json:
            _print_json(report)
        else:
            print("translation domain: no translation files changed in the range")
        return 0
    indexes, _ = extract_enriched(manifest, runtime, components)
    # H4/V4: the rules registry, unloaded-sources registry and lint policy
    # all come from the resolved head commit blobs (never the worktree), so
    # uncommitted content cannot masquerade as head. Reads are fail-closed.
    head_registry = RuleRegistry.from_dict(
        _read_commit_json(repository, head, RULES_REGISTRY_RELATIVE_PATH, "rule registry"),
        label=f"rule registry@{head[:12]}",
    )
    unloaded_sources = UnloadedSources.from_dict(
        _read_commit_json(
            repository, head, UNLOADED_SOURCES_RELATIVE_PATH, "unloaded-sources registry"
        ),
        label=f"unloaded-sources registry@{head[:12]}",
    )
    head_policy = parse_policy(
        _read_commit_json(repository, head, manifest.policy, "lint policy"),
        label=f"lint policy@{head[:12]}",
    )

    def semantic(entry: dict[str, Any]) -> str:
        import json as _json

        return _json.dumps(
            [entry.get("target"), entry.get("args_order"), entry.get("special")],
            ensure_ascii=False,
            sort_keys=True,
        )

    # H4/D5/V4: the main translation and the copy fragment are independent
    # logical documents; each is loaded from the resolved base and head
    # commit blobs (never the worktree) so base records represent the true
    # base (including copy-fragment findings) and added / deleted /
    # semantically-changed entries are collected bidirectionally. A
    # genuinely absent file on either side compares as the empty side;
    # loader errors fail closed.
    specs_head, head_docs = _document_specs_at_commit(
        repository, loader, components, head
    )
    specs_base, base_docs = _document_specs_at_commit(
        repository, loader, components, base
    )
    logical_files: list[tuple[str, str, bool]] = []
    for component in components:
        logical_files.append((component.id, component.translation, False))
        if component.copy_fragment:
            logical_files.append((component.id, component.copy_fragment, True))

    affected_tus: set[str] = set()

    def add_editorial(
        component_id: str, section: str, source: str, source_tag: str | None
    ) -> None:
        editorial_id = stable_entry_id(component_id, section, source, source_tag)
        component_index = indexes.get(component_id)
        candidates = (
            component_index.editorial_to_tu.get(editorial_id, ())
            if component_index is not None
            else ()
        )
        if candidates:
            affected_tus.update(candidates)
        else:
            # No index mapping: use the frozen fallback TU, exactly like
            # build_finding_records::_bind (D5).
            affected_tus.add(tu_uid_fallback(editorial_id))

    def collect_changes(
        component_id: str, base_doc: Any | None, head_doc: Any | None
    ) -> None:
        base_entries = (
            list(base_doc.translations) if base_doc is not None else []
        )
        head_entries = (
            list(head_doc.translations) if head_doc is not None else []
        )
        if not base_entries and not head_entries:
            return
        if base_doc is None or head_doc is None:
            # Head-only or base-only logical file: every entry that exists
            # on either side changed (added or deleted).
            changed_keys = {
                (
                    entry.get("section"),
                    entry.get("source"),
                    entry.get("source_tag"),
                )
                for entry in [*base_entries, *head_entries]
            }
        else:
            changed_keys = _changed_editorial_keys(
                base_entries, head_entries, semantic
            )
        for section, source, source_tag in changed_keys:
            add_editorial(
                component_id, section or "", source or "", source_tag
            )

    for component_id, path, _is_copy in logical_files:
        collect_changes(
            component_id,
            base_docs.get((component_id, path)),
            head_docs.get((component_id, path)),
        )

    issues_head, contexts_head, _ = lint_documents_specs(
        manifest, specs_head, policy=head_policy
    )
    issues_base, contexts_base, _ = lint_documents_specs(
        manifest, specs_base, policy=head_policy
    )
    conflicts: list[Any] = []
    for index in indexes.values():
        conflicts.extend(index.conflicts)

    def records_for(issues: Any, contexts: Any) -> list[Any]:
        bound = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=indexes.get(context.component),
            )
            for name, context in contexts.items()
        }
        # FR1: the identity binding must not depend on whether the component
        # document exists at this commit.
        bound = _bind_identity_contexts(bound, indexes)
        records, _ = build_finding_records(
            registry=head_registry,
            issues=issues,
            contexts=bound,
            conflicts=conflicts,
            unloaded_sources=unloaded_sources,
        )
        return records

    head_records = records_for(issues_head, contexts_head)
    base_records = records_for(issues_base, contexts_base)

    # R2 (cycle 3): recompute/kept are participant-aware, and runtime
    # collision records are correlated across the base/head sides through a
    # stable family key. The subject of a runtime-collision record is the
    # collision-id fallback TU while the actual editorial TUs live in
    # participants; a touched participant forces recompute on the head side
    # and out of kept on the base side. Because the collision_id (issue
    # entry_id) is a hash of component/source/source_tag, both sides of the
    # same collision share one family key: when ANY member of the family is
    # directly touched (e.g. base A+B already collides and head adds C, with
    # only C affected), the base member must leave kept and the head member
    # must be recomputed - otherwise the stale A+B record would linger next
    # to the correct A+B+C record.
    def _touched(record: Any) -> bool:
        return record.tu_uid in affected_tus or any(
            participant in affected_tus for participant in record.participants
        )

    def _family_key(record: Any) -> tuple[Any, ...] | None:
        if record.rule_id == "runtime-collision" and record.issue.entry_id is not None:
            return ("runtime-collision", record.issue.entry_id)
        return None

    touched_families = frozenset(
        key
        for record in [*base_records, *head_records]
        for key in [(_family_key(record) if _touched(record) else None)]
        if key is not None
    )

    def _record_affected(record: Any) -> bool:
        if _touched(record):
            return True
        key = _family_key(record)
        return key is not None and key in touched_families

    recomputed = tuple(record for record in head_records if _record_affected(record))
    kept = tuple(record for record in base_records if not _record_affected(record))
    incremental_records = tuple(
        sorted([*kept, *recomputed], key=lambda record: record.fingerprint)
    )
    report: dict[str, Any] = {
        "domain": "translation",
        "base": base,
        "head": head,
        "affected_components": [component.id for component in affected_components],
        "affected_tus": len(affected_tus),
        "affected_tu_uids": sorted(affected_tus),
        "findings": {
            "previous": len(base_records),
            "kept": len(kept),
            "recomputed": len(recomputed),
            "incremental": len(incremental_records),
        },
        "records": [record.to_dict() for record in incremental_records],
        "ok": True,
    }
    if arguments.self_check:
        from .invalidation import self_check as canonical_self_check

        passed = canonical_self_check(
            incremental=incremental_records, full=head_records
        )
        report["self_check"] = {
            "passed": passed,
            "full_findings": len(head_records),
        }
        report["ok"] = report["ok"] and passed
    # H4/D5: report new/legacy error counts regardless of --ci; the gate only
    # fails when --ci is passed (legacy ERROR stays technical debt).
    previous_error_fingerprints = {
        record.fingerprint
        for record in base_records
        if record.issue.severity == "error"
    }
    new_errors = sum(
        1
        for record in incremental_records
        if record.issue.severity == "error"
        and record.fingerprint not in previous_error_fingerprints
    )
    legacy_errors = sum(
        1
        for record in incremental_records
        if record.issue.severity == "error"
        and record.fingerprint in previous_error_fingerprints
    )
    report["ci"] = {"new_errors": new_errors, "legacy_errors": legacy_errors}
    if arguments.ci:
        # The CI gate is opt-in: counts are always reported, but new_errors
        # only influences ok/exit when --ci is passed (legacy CLI semantics).
        report["ok"] = report["ok"] and new_errors == 0
    if arguments.json:
        _print_json(report)
    else:
        findings = report["findings"]
        print(
            f"incremental translation {base}..{head}: "
            f"affected_tus={len(affected_tus)} "
            f"previous={findings['previous']} kept={findings['kept']} "
            f"recomputed={findings['recomputed']} "
            f"incremental={findings['incremental']}"
        )
        if report.get("ci") is not None:
            print(f"ci: new_errors={report['ci']['new_errors']}")
    if arguments.self_check and report["self_check"]["passed"] is False:
        from .errors import IncrementalCheckError

        raise IncrementalCheckError(
            "incremental self-check failed: canonical forms differ"
        )
    if arguments.ci and report["ci"]["new_errors"] > 0:
        raise I18nToolError(
            "incremental CI gate failed: "
            f"{report['ci']['new_errors']} new ERROR findings"
        )
    return 0


def _status(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    components = _select_components(manifest, arguments.component, default="status")
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = status_report(manifest, loader, components)
    run_directory = create_run_directory(manifest.root, "status")
    report["run_directory"] = str(run_directory)
    write_json(run_directory / "status.json", report)
    if arguments.json:
        _print_json(report)
    else:
        for item in report["components"]:
            if not item["official_available"]:
                print(
                    f"SKIP {item['component']:<16} no pinned official locale "
                    f"({item['canonical_entries']} canonical entries)"
                )
                continue
            print(
                f"OK   {item['component']:<16} "
                f"same={item['identical']} changed={item['changed']} "
                f"new={item['canonical_only']} official-only={item['official_only']}"
            )
        print(f"Report: {run_directory / 'status.json'}")
    return 0


def _build(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if arguments.component:
        components = _select_components(
            manifest, arguments.component, default="build"
        )
        if arguments.profile == "full":
            missing_outputs = [
                component.id
                for component in components
                if component.full_output is None
            ]
            if missing_outputs:
                label = "component" if len(missing_outputs) == 1 else "components"
                verb = "has" if len(missing_outputs) == 1 else "have"
                raise ValidationError(
                    f"{label} {', '.join(repr(value) for value in missing_outputs)} "
                    f"{verb} no full_output mapping"
                )
        else:
            non_eligible = [
                component.id for component in components if not component.addon_eligible
            ]
            if non_eligible:
                raise ValidationError(
                    "addon build requires addon-eligible components; not eligible: "
                    + ", ".join(non_eligible)
                )
    elif arguments.profile == "full":
        components = [
            component
            for component in manifest.components
            if component.full_output is not None
        ]
    else:
        components = [
            component for component in manifest.components if component.addon_eligible
        ]
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    if arguments.profile == "full":
        report = build_full_locales(manifest, loader, components)
    else:
        report = build_addon_locale(
            manifest,
            loader,
            components,
            include_external_requirements=not bool(arguments.component),
        )
    if arguments.json:
        _print_json(report)
    elif arguments.profile == "full":
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} {item['translation_entries']:>7} entries  "
                f"{item['sha256'][:16]}"
            )
        print(f"Artifacts: {report['run_directory']}")
    else:
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} delta={item['delta_entries']} "
                f"inherited={item['inherited_entries']} "
                f"override={item['override_entries']} new={item['new_entries']}"
            )
        for item in report["skipped"]:
            print(f"SKIP {item['component']:<16} {item['reason']}")
        completeness = "complete" if report["complete"] else "INCOMPLETE"
        print(
            f"Addon artifact: {completeness}, "
            f"{report['verification']['patch_runtime_keys']} runtime keys, "
            f"{report['sha256'][:16]}"
        )
        print(f"Output: {report['output']}")
    if (
        arguments.profile == "addon"
        and arguments.require_complete
        and not report["complete"]
    ):
        raise ValidationError(
            "addon artifact is incomplete; see "
            f"{Path(report['run_directory']) / 'build.json'}"
        )
    return 0


def _merge(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    component = manifest.component(arguments.component)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    base_index = None
    new_index = None
    if arguments.base_tu_index or arguments.new_tu_index:
        if not (arguments.base_tu_index and arguments.new_tu_index):
            raise ValidationError(
                "identity matching requires both --base-tu-index and "
                "--new-tu-index"
            )
        from .identity import read_index_files

        entities_base = arguments.base_tu_index.parent / "entities.jsonl"
        entities_new = arguments.new_tu_index.parent / "entities.jsonl"
        base_index = read_index_files(
            component=component.id,
            entities_path=entities_base,
            tu_index_path=arguments.base_tu_index,
        )
        new_index = read_index_files(
            component=component.id,
            entities_path=entities_new,
            tu_index_path=arguments.new_tu_index,
        )
    merge_kwargs: dict[str, Any] = {}
    if base_index is not None and new_index is not None:
        merge_kwargs = {"base_index": base_index, "new_index": new_index}
    report = run_merge(
        manifest,
        loader,
        component,
        new_snapshot_path=arguments.snapshot,
        base_snapshot_path=arguments.base_snapshot,
        **merge_kwargs,
    )
    if arguments.json:
        _print_json(report)
    else:
        counts = report["counts"]
        print(
            f"OK  {component.id:<16} candidate={counts['candidate_translations']} "
            f"exact={counts['exact_editorial']} moved={counts['moved_section']}"
        )
        print(
            f"    untranslated={counts['untranslated']} "
            f"source-changed={counts['source_changed_suggestions']} "
            f"obsolete/unextracted={counts['obsolete_or_unextracted']}"
        )
        safety = "SAFE" if report["safe_to_apply"] else "REVIEW REQUIRED"
        print(f"Candidate: {safety}  {report['candidate']}")
        print(f"Report: {report['report']}")
    return 0


def _workset(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    workset = create_workset(
        manifest,
        merge_report_path=arguments.merge_report,
        limit=arguments.limit,
        section_prefix=arguments.section_prefix,
        classification=arguments.classification,
    )
    if arguments.json:
        _print_json(workset)
    else:
        selection = workset["selection"]
        print(
            f"OK  workset {workset['workset_id'][:16]}  "
            f"selected={selection['selected']}/"
            f"{selection['available_after_filter']} terms={len(workset['terminology'])}"
        )
        print(f"Output: {workset['output']}")
        print(f"Proposal template: {workset['proposal_template']}")
    return 0


def _context(arguments: argparse.Namespace) -> int:
    validate_context_options(
        section_prefix=arguments.section_prefix,
        query=arguments.query,
        limit=arguments.limit,
    )
    manifest = _manifest(arguments)
    component = manifest.component(arguments.component)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    result = resolve_context(
        manifest,
        loader,
        component,
        section_prefix=arguments.section_prefix,
        query=arguments.query,
        limit=arguments.limit,
    )
    if arguments.json:
        _print_json(result)
    else:
        selection = result["selection"]
        print(
            f"OK  context {result['context_id'][:16]}  "
            f"selected={selection['selected']}/{selection['available']} "
            f"terms={len(result['terminology'])}"
        )
        print(f"Output: {result['output']}")
    return 0


def _review(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    scopes = frozenset(arguments.scope)
    index = create_review_index(
        manifest,
        batch_size=arguments.batch_size,
        character_budget=arguments.character_budget,
        include_translations="translations" in scopes,
        include_code="code" in scopes,
    )
    if arguments.json:
        _print_json(index)
    else:
        summary = review_index_summary(index)
        print(
            f"OK  review {summary['review_id'][:16]}  "
            f"bundles={summary['bundles']} "
            f"translations={summary['translation_bundles']} "
            f"code={summary['code_bundles']}"
        )
        print(f"Index: {summary['index']}")
        if index.get("redacted_absolute_path_count"):
            print(
                "Redacted absolute paths: "
                f"{index['redacted_absolute_path_count']}"
            )
    return 0


def _proposal(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = validate_proposal(
        manifest,
        workset_path=arguments.workset,
        proposal_path=arguments.proposal,
        allow_partial=arguments.allow_partial,
        strict=arguments.strict,
    )
    if arguments.json:
        _print_json(report)
    else:
        coverage = report["coverage"]
        print(
            f"{'OK' if report['ok'] else 'FAIL'} proposal "
            f"{report['proposal_id'][:16]}  "
            f"coverage={coverage['proposed']}/{coverage['workset_items']} "
            f"errors={report['errors']} warnings={report['warnings']}"
        )
        print(f"Report: {report['report']}")
        if report.get("validated_proposal"):
            print(f"Validated: {report['validated_proposal']}")
    if not report["ok"]:
        raise ValidationError(
            f"proposal validation failed with {report['errors']} errors and "
            f"{report['warnings']} warnings"
        )
    return 0


def _publish(arguments: argparse.Namespace) -> int:
    if arguments.commit and not arguments.apply:
        raise ValidationError("publish --commit requires --apply")

    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = publish_addon(
        manifest,
        loader,
        apply=arguments.apply,
        bump=arguments.bump,
        commit=arguments.commit,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"Release repository: {report['release_repository']}")
        print(f"Locale file:        {report['locale_file']}")
        print(
            f"Entries:            {report['old_entries']} -> {report['new_entries']} "
            f"(delta {report['delta_runtime_keys']} runtime keys)"
        )
        print(f"SHA-256:            {report['old_sha256'][:16]} -> {report['new_sha256'][:16]}")
        if report.get("bump_addon_version"):
            print(
                f"addon_version:      {report['old_addon_version']} -> "
                f"{report['new_addon_version']}"
            )
        if report["applied"]:
            print(
                f"Applied:            OK (verified {report['verified_entries']} entries)"
            )
            if report.get("release_head"):
                print(f"Release HEAD:       {report['release_head']}")
        else:
            print("Applied:            dry run (re-run with --apply to publish)")
    return 0


_PUBLIC_DLC_ROOT = Path("/Users/yun/projects/tome4-dlcs")
_PUBLIC_DLC_PATHS = {
    "TOME_DLC_ASHES_ROOT": "ashes-urhrok/tome-ashes-urhrok",
    "TOME_DLC_CULTS_ROOT": "cults/tome-cults",
    "TOME_DLC_ORCS_ROOT": "orcs/tome-orcs",
}


def _public_dlc_root() -> Path:
    """Resolve the public DLC root portably (contract AC-9).

    Priority: TOME_PUBLIC_DLC_ROOT env override (if a directory), then
    ~/projects/tome4-dlcs (POSIX home), then the legacy macOS default
    /Users/yun/projects/tome4-dlcs. The last candidate is also the final
    fallback, so behavior on the original machine is unchanged.
    """
    configured = os.environ.get("TOME_PUBLIC_DLC_ROOT")
    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.append(Path.home() / "projects" / "tome4-dlcs")
    candidates.append(_PUBLIC_DLC_ROOT)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[-1]


def _inject_public_dlc_env() -> None:
    """Point DLC extraction at the public GPL v3 release when the env is unset.

    The official DLC sources are GPL v3 public (see AGENTS.md). The public
    release under _public_dlc_root() is the canonical extraction input; the
    legacy TOME_DLC_*_ROOT values (if set by the user) still take precedence.
    """
    public_dlc_root = _public_dlc_root()
    if not public_dlc_root.is_dir():
        return
    for env_name, relative in _PUBLIC_DLC_PATHS.items():
        if env_name in os.environ:
            continue
        candidate = public_dlc_root / relative
        if candidate.is_dir():
            os.environ[env_name] = str(candidate)


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


def _production_bytes(path: Path, label: str) -> bytes:
    try:
        if not path.is_file() or path.is_symlink():
            raise production_review.ProductionReviewError(f"{label} is not an ordinary file: {path}")
        return path.read_bytes()
    except OSError as error:
        raise production_review.ProductionReviewError(f"cannot read {label}: {path}: {error}") from error


def _production_read(path: Path, label: str = "artifact") -> Any:
    return production_review.parse_canonical_object(_production_bytes(path, label), label)


def _production(arguments: argparse.Namespace) -> int:
    configured_root = os.environ.get("I18N_REPOSITORY_ROOT")
    root = (Path(configured_root).resolve() if configured_root else
            Path(__file__).resolve().parents[2])
    if not root.is_dir():
        raise production_review.ProductionReviewError(
            f"repository root is not an ordinary directory: {root}")
    evidence = root / "evidence" / "production-review"
    quality = root / "i18n" / "quality" / "production-review"
    command, action = arguments.production_command, getattr(arguments, "production_action", None)

    def snapshot_inputs(*, operational: bool = True) -> tuple[dict[str, Any], bytes, bytes, bytes]:
        manifest_raw = _production_bytes(arguments.locator_snapshot, "locator manifest")
        value = production_review.parse_canonical_object(manifest_raw, "locator manifest")
        occurrences = _production_bytes(arguments.occurrences, "occurrences")
        locators = _production_bytes(arguments.locators, "locators")
        production_review.check_locator_snapshot(value, occurrences, locators)
        if operational:
            production_review.check_locator_snapshot_live(value, occurrences, locators, _manifest(arguments))
        return value, manifest_raw, occurrences, locators

    def catalog_inputs(*, operational: bool = True) -> tuple[dict[str, Any], bytes, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
        locator, locator_raw, occurrences, locators = snapshot_inputs(operational=operational)
        expected_terminology = None
        expected_sources = None
        if operational:
            manifest = _manifest(arguments)
            expected_terminology = production_review.terminology_snapshot(root)
            expected_sources = production_review.source_identities_from_manifest(manifest)
        raw = _production_bytes(arguments.catalog, "catalog manifest")
        value = production_review.parse_canonical_object(raw, "catalog manifest")
        entries, exclusions = production_review.check_catalog(
            value, _production_bytes(arguments.entries, "catalog entries"),
            _production_bytes(arguments.exclusions, "catalog exclusions"),
            locator_manifest=locator, locator_manifest_raw=locator_raw,
            occurrences_raw=occurrences, locators_raw=locators,
            expected_terminology_snapshot_id=expected_terminology,
            expected_source_identities=expected_sources,
            require_current_rules=operational)
        return value, raw, entries, exclusions, locator

    def policy_input(catalog: dict[str, Any], catalog_raw: bytes, locator: dict[str, Any]) -> dict[str, Any]:
        return production_review.check_shadow_policy(
            _production_read(arguments.policy, "shadow policy"), catalog=catalog,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator)

    def journal_inputs(catalog: dict[str, Any], catalog_raw: bytes, entries: list[dict[str, Any]],
                       exclusions: list[dict[str, Any]], policy: dict[str, Any], locator: dict[str, Any]):
        group = _production_read(arguments.group, "journal group")
        raw = _production_bytes(arguments.events, "journal events")
        checkpoint = _production_read(arguments.checkpoint, "journal checkpoint")
        replayed = production_review.check_shadow_journal(
            group, raw, checkpoint, catalog=catalog, catalog_manifest_raw=catalog_raw,
            locator_manifest=locator, entries=entries, exclusions=exclusions, policy=policy)
        return group, raw, checkpoint, replayed

    if command == "authoritative-catalog" and action == "build":
        manifest = _manifest(arguments)
        files = production_review_v2_lite.build_catalog(
            manifest, recorded_at=arguments.recorded_at or production_review_v2_lite.utc_now(),
            recorded_by=arguments.recorded_by)
        production_review_v2_lite.write_candidate(files, arguments.output, repository_root=root)
        value = production_review_v2_lite.check_catalog_tree(arguments.output, manifest)
        report = {"catalog_id": value["catalog_id"], "occurrences": value["occurrence_count"],
                  "entries": value["entry_count"], "exclusions": value["exclusion_count"],
                  "directory": str(arguments.output), "bytes": sum(map(len, files.values()))}
    elif command == "authoritative-catalog" and action == "check":
        value = production_review_v2_lite.check_catalog_tree(arguments.candidate_catalog, _manifest(arguments))
        report = {"catalog_id": value["catalog_id"], "occurrences": value["occurrence_count"],
                  "entries": value["entry_count"], "exclusions": value["exclusion_count"], "ok": True}
    elif command == "wp1-retirement" and action == "preflight":
        report = production_review_v2_lite.retirement_preflight(
            root, arguments.candidate_catalog, _manifest(arguments))
    elif command == "queue":
        if action == "init":
            report = production_review_v2_lite_queue.init(root)
        elif action == "rebuild":
            report = production_review_v2_lite_queue.rebuild(root, treeish=arguments.treeish)
        elif action == "check":
            report = production_review_v2_lite_queue.check(root)
        elif action == "status":
            report = production_review_v2_lite_queue.status(root)
        else:
            raise AssertionError(f"unhandled queue action: {action}")
    elif command == "batch":
        if action == "start":
            report = production_review_v2_lite_batch.start(root, limit=arguments.limit, retry_blocked=arguments.retry_blocked)
        elif action == "show":
            report = production_review_v2_lite_batch.show(root)
        elif action == "abandon":
            report = production_review_v2_lite_batch.abandon(root, discard_uncommitted_results=arguments.discard_uncommitted_results, restore_evidence=arguments.restore_evidence)
        elif action == "recover":
            report = (production_review_v2_lite_batch.recover_from_head(root)
                      if arguments.from_head else production_review_v2_lite_batch.recover(root))
        elif action == "surface-export":
            report = production_review_v2_lite_batch.surface_export(root)
        elif action == "surface-import":
            try:
                values = json.loads(arguments.input.read_text(encoding="utf-8"))
                if not isinstance(values, dict):
                    raise ValueError("surface import index must be an object")
                outputs = {key: (Path(value).read_bytes() if isinstance(value, str) and Path(value).is_file() else value) for key, value in values.items()}
            except (OSError, UnicodeError, ValueError, TypeError) as error:
                raise production_review.ProductionReviewError(f"invalid surface import input: {error}") from error
            report = production_review_v2_lite_batch.surface_import(root, outputs)
        elif action == "contextual-export":
            report = production_review_v2_lite_batch.contextual_export(root)
        elif action == "contextual-import":
            try:
                values = json.loads(arguments.input.read_text(encoding="utf-8"))
                outputs = {key: (Path(value).read_bytes() if isinstance(value, str) and Path(value).is_file() else value) for key, value in values.items()}
            except (OSError, UnicodeError, ValueError, TypeError) as error:
                raise production_review.ProductionReviewError(f"invalid contextual import input: {error}") from error
            report = production_review_v2_lite_batch.contextual_import(root, outputs)
        elif action == "adjudicate":
            report = production_review_v2_lite_batch.adjudicate(root, arguments.input)
        elif action == "prepare-evidence":
            report = production_review_v2_lite_batch.prepare_evidence(root)
        elif action == "finalize":
            report = production_review_v2_lite_batch.finalize(root, arguments.commit)
        elif action == "recover-from-head":
            report = production_review_v2_lite_batch.recover_from_head(root)
        else:
            raise AssertionError(f"unhandled batch action: {action}")
    elif command == "migration" and action == "plan":
        report = production_review_v2_lite_migration.plan(
            root, arguments.candidate_catalog, recorded_at=arguments.recorded_at,
            recorded_by=arguments.recorded_by, output=arguments.output)
    elif command == "migration" and action == "check":
        report = production_review_v2_lite_migration.check(
            root, arguments.input, candidate_catalog=arguments.candidate_catalog)
    elif command == "migration" and action == "apply":
        report = production_review_v2_lite_migration.apply(
            root, arguments.input, candidate_catalog=arguments.candidate_catalog)
    elif command == "repair" and action == "preflight":
        report = production_review_v2_lite_migration.repair_preflight(
            root, arguments.batch_id, output=arguments.output, manifest=_manifest(arguments))
    elif command == "locator" and action == "bootstrap":
        manifest = _manifest(arguments)
        value, occurrences, locators = production_review.build_locator_snapshot(
            manifest, recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
        directory = evidence / "locator-snapshots" / value["locator_snapshot_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value),
            "occurrences.jsonl": occurrences, "locators.jsonl": locators}, directory,
            root=root, budget=production_review.BUDGETS["locator"], category="locator")
        report = {"locator_snapshot_id": value["locator_snapshot_id"], "occurrences": value["occurrences_count"],
            "locators": value["locators_count"], "directory": str(directory),
            "bytes": len(occurrences)+len(locators)+len(production_review.canonical_bytes(value))}
    elif command == "locator" and action == "check":
        value = _production_read(arguments.snapshot, "locator manifest")
        occurrences, locators = production_review.check_locator_snapshot(
            value, _production_bytes(arguments.occurrences, "occurrences"), _production_bytes(arguments.locators, "locators"))
        report = {"locator_snapshot_id": value["locator_snapshot_id"], "occurrences": len(occurrences),
            "locators": len(locators), "ok": True}
    elif command == "catalog" and action == "build":
        locator_manifest, locator_manifest_raw, occurrences, locators = snapshot_inputs()
        value, entries_raw, exclusions_raw = production_review.build_catalog(locator_manifest,
            occurrences, locators, locator_manifest_raw=locator_manifest_raw,
            terminology_snapshot_id=production_review.terminology_snapshot(root),
            source_identities=production_review.source_identities_from_manifest(_manifest(arguments)),
            recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
        directory = evidence / "catalogs" / value["catalog_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value),
            "entries.jsonl": entries_raw, "exclusions.jsonl": exclusions_raw}, directory,
            root=root, budget=production_review.BUDGETS["catalog"], category="catalog")
        report = {"catalog_id": value["catalog_id"], "entries": value["entry_count"],
            "exclusions": value["exclusion_count"], "directory": str(directory),
            "bytes": len(entries_raw)+len(exclusions_raw)+len(production_review.canonical_bytes(value))}
    elif command == "catalog" and action == "check":
        locator_manifest, locator_manifest_raw, occurrences, locators = snapshot_inputs()
        manifest = _manifest(arguments)
        value = _production_read(arguments.catalog, "catalog manifest")
        entries, exclusions = production_review.check_catalog(value, _production_bytes(arguments.entries, "catalog entries"),
            _production_bytes(arguments.exclusions, "catalog exclusions"), locator_manifest=locator_manifest,
            locator_manifest_raw=locator_manifest_raw, occurrences_raw=occurrences, locators_raw=locators,
            expected_terminology_snapshot_id=production_review.terminology_snapshot(root),
            expected_source_identities=production_review.source_identities_from_manifest(manifest),
            require_current_rules=True)
        report = {"catalog_id": value["catalog_id"], "entries": len(entries), "exclusions": len(exclusions), "ok": True}
    elif command == "shadow-policy":
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        if action == "build":
            value = production_review.build_shadow_policy(catalog, locator_manifest,
                catalog_manifest_raw=catalog_raw, terminology_snapshot_id=catalog["terminology_snapshot_id"],
                source_identities=catalog["source_identities"], recorded_at=catalog["recorded_at"],
                recorded_by=catalog["recorded_by"])
            directory = quality / "shadow-policies" / value["shadow_policy_id"]
            production_review.atomic_publish_directory({"policy.json": production_review.canonical_bytes(value)},
                directory, root=root, budget=production_review.BUDGETS["policy"], category="policy")
            report = {"shadow_policy_id": value["shadow_policy_id"], "directory": str(directory),
                "bytes": len(production_review.canonical_bytes(value))}
        else:
            value = production_review.check_shadow_policy(_production_read(arguments.policy, "shadow policy"), catalog=catalog,
                catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
            report = {"shadow_policy_id": value["shadow_policy_id"], "ok": True}
    elif command in ("shadow-journal", "replay"):
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        if command == "shadow-journal" and action == "bootstrap":
            group, events, checkpoint = production_review.build_shadow_journal(entries, exclusions, catalog,
                policy, catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest,
                recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
            raw = production_review._jsonl(events); directory = evidence / "shadow-journals" / group["group_id"]
            production_review.atomic_publish_directory({"group.json": production_review.canonical_bytes(group),
                "events.jsonl": raw, "checkpoint.json": production_review.canonical_bytes(checkpoint)},
                directory, root=root, budget=production_review.BUDGETS["journal"], category="journal")
            report = {"group_id": group["group_id"], "checkpoint_id": checkpoint["checkpoint_id"],
                "events": len(events), "directory": str(directory),
                "bytes": len(raw)+len(production_review.canonical_bytes(group))+len(production_review.canonical_bytes(checkpoint))}
        else:
            group, raw, checkpoint, report = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
            if not getattr(arguments, "detail", False): report.pop("queued_revisions", None)
            report.update({"group_id": group["group_id"], "checkpoint_id": checkpoint["checkpoint_id"], "ok": True})
    elif command == "batch-draft":
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        group, raw, checkpoint, _ = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
        value = production_review.build_shadow_batch(entries, catalog, policy, group, raw, checkpoint, exclusions,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
        directory = evidence / "batches" / value["shadow_batch_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value)},
            directory, root=root, budget=production_review.BUDGETS["batch"], category="batch")
        report = {"shadow_batch_id": value["shadow_batch_id"], "eligible": len(value["eligible"]),
            "batch_selected": len(value["batch_selected"]), "carry_over": len(value["carry_over"]),
            "directory": str(directory), "bytes": len(production_review.canonical_bytes(value))}
    elif command == "reconciliation":
        # Validate the complete frozen chain before independently measuring drift.
        locator_manifest, locator_raw, frozen_occurrences_raw, frozen_locators_raw = snapshot_inputs(operational=False)
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs(operational=False)
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        group, raw, checkpoint, _ = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
        batch = production_review.validate_shadow_batch(_production_read(arguments.batch, "shadow batch"), entries=entries,
            exclusions=exclusions, catalog=catalog, policy=policy, group=group, events_raw=raw, checkpoint=checkpoint,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
        events = production_review.parse_jsonl(raw, "journal events")
        report = production_review.reconciliation_report(entries, exclusions, events, batch)
        try:
            manifest = _manifest(arguments); runtime_info = LuaRuntime(manifest).doctor()
            live_occurrences = production_review.load_occurrences(manifest)
            live_occurrences_raw = production_review._jsonl(live_occurrences)
            current_manifest_sha = hashlib.sha256(manifest.raw_bytes).hexdigest()
            current_ordinals = production_review._component_ordinals(c.id for c in manifest.components)
            current_loader_sha = hashlib.sha256(_production_bytes(root / "tools/i18nlib/locale_model.py", "loader contract")).hexdigest()
            current_terminology = production_review.terminology_snapshot(root)
            current_sources = production_review.source_identities_from_manifest(manifest)
            axes = {
                "manifest_sha_and_order": locator_manifest["manifest_sha256"] == current_manifest_sha and locator_manifest["manifest_component_ordinals"] == current_ordinals,
                "loader_contract_sha_and_runtime": locator_manifest["loader_contract_path"] == "tools/i18nlib/locale_model.py" and locator_manifest["loader_contract_sha256"] == current_loader_sha and locator_manifest["lua_runtime"] == runtime_info["lua_version"] and locator_manifest["lua_build"] == runtime_info["luajit_version"],
                "occurrences": live_occurrences_raw == frozen_occurrences_raw,
                "terminology_snapshot": catalog["terminology_snapshot_id"] == current_terminology,
                "source_identities": catalog["source_identities"] == current_sources,
                "current_rules": catalog["rules_version"] == production_review.RULES_VERSION and policy["rules_version"] == production_review.RULES_VERSION,
                "fully_reconstructed_catalog": False,
            }
            try:
                live_locator, live_locator_raw, live_locators_raw = production_review.build_locator_snapshot_from_occurrences(
                    live_occurrences, manifest_sha256=current_manifest_sha, manifest_component_ordinals=current_ordinals,
                    loader_contract_path="tools/i18nlib/locale_model.py", loader_contract_sha256=current_loader_sha,
                    lua_runtime=runtime_info["lua_version"], lua_build=runtime_info["luajit_version"],
                    recorded_at=locator_manifest["recorded_at"], recorded_by=locator_manifest["recorded_by"])
                rebuilt, rebuilt_entries, rebuilt_exclusions = production_review.build_catalog(
                    live_locator, live_locator_raw, live_locators_raw, locator_manifest_raw=production_review.canonical_bytes(live_locator),
                    terminology_snapshot_id=current_terminology, source_identities=current_sources,
                    recorded_at=catalog["recorded_at"], recorded_by=catalog["recorded_by"])
                axes["fully_reconstructed_catalog"] = (rebuilt == catalog and rebuilt_entries == _production_bytes(arguments.entries, "catalog entries") and rebuilt_exclusions == _production_bytes(arguments.exclusions, "catalog exclusions"))
            except production_review.ProductionReviewError:
                pass
        except (production_review.ProductionReviewError, I18nToolError, OSError):
            live_occurrences = []
            axes = {key: False for key in production_review.RECONCILIATION_AXES}
        drift = not all(axes.values())
        report.update({"catalog_id":catalog["catalog_id"], "group_id":group["group_id"],
                       "shadow_batch_id":batch["shadow_batch_id"], "live_occurrences":len(live_occurrences),
                       "drift_axes":axes, "drift":drift, "shadow_publication_blocked":drift})
        production_review.validate_reconciliation_artifact(report)
        artifact = root / ".artifacts/i18n/production-review/reconciliation.json"
        try:
            artifact.parent.mkdir(parents=True, exist_ok=True)
            with artifact.open("wb") as handle:
                handle.write(production_review.canonical_bytes(report)); handle.flush(); os.fsync(handle.fileno())
            production_review._fsync_directory(artifact.parent)
        except OSError as error:
            raise production_review.ProductionReviewError(f"cannot publish reconciliation artifact: {error}") from error
        report["artifact"] = str(artifact)
        if not report["ok"]: raise production_review.ProductionReviewError("shadow reconciliation conservation failed")
    else:
        raise AssertionError(f"unhandled production command: {command}/{action}")
    if command in {"migration", "repair"}:
        sys.stdout.buffer.write(production_review.canonical_bytes(report))
        return 0 if report.get("ok", True) else 1
    if command == "queue" and action == "status":
        if arguments.json:
            sys.stdout.buffer.write(production_review.canonical_bytes(report))
        else:
            print(f"catalog {report['catalog_id']}")
            print(f"evidence HEAD {report['evidence_head']}")
            states = ", ".join(f"{key}={value}" for key, value in report["explicit_overrides"].items()) or "none"
            print(f"overrides {states}; queued={report['implicit_queued']}; reconciliation={report['reconciliation_count']}")
            print(f"active writer {'yes' if report['active_writer'] else 'no'}")
    else:
        _print_json(report)
    if command == "queue" and action == "check" and not report["ok"]:
        return 1
    return 0


def _claims_check(arguments: argparse.Namespace) -> int:
    report = check_registry(arguments.registry, strict=arguments.strict)
    if arguments.json:
        _print_json(report)
    else:
        print(
            "OK  semantic claims "
            f"numeric={report['numeric_claims']} "
            f"briefings={report['reviewer_briefings']} "
            f"compositions={report['runtime_compositions']} "
            f"pending={report['pending']}"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    _inject_public_dlc_env()
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "doctor":
            return _doctor(arguments)
        if arguments.command == "extract":
            return _extract(arguments)
        if arguments.command == "lint":
            return _lint(arguments)
        if arguments.command == "baseline":
            if arguments.baseline_command == "freeze":
                return _baseline_freeze(arguments)
            if arguments.baseline_command == "report":
                return _baseline_report(arguments)
            raise AssertionError(
                f"unhandled baseline command: {arguments.baseline_command}"
            )
        if arguments.command == "identity":
            if arguments.identity_command == "show":
                return _identity_show(arguments)
            if arguments.identity_command == "audit":
                return _identity_audit(arguments)
            raise AssertionError(
                f"unhandled identity command: {arguments.identity_command}"
            )
        if arguments.command == "status":
            return _status(arguments)
        if arguments.command == "build":
            return _build(arguments)
        if arguments.command == "publish":
            return _publish(arguments)
        if arguments.command == "merge":
            return _merge(arguments)
        if arguments.command == "workset":
            return _workset(arguments)
        if arguments.command == "context":
            return _context(arguments)
        if arguments.command == "review":
            return _review(arguments)
        if arguments.command == "proposal":
            return _proposal(arguments)
        if arguments.command == "production":
            return _production(arguments)
        if arguments.command == "claims":
            if arguments.claims_command == "check":
                return _claims_check(arguments)
            raise AssertionError(f"unhandled claims command: {arguments.claims_command}")
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
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    except (production_review.ProductionReviewError, production_review.ledger.LedgerError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
