"""Registration and handlers for review commands."""

from __future__ import annotations
import argparse
from pathlib import Path
from .context import resolve_context, validate_context_options
from .errors import ValidationError
from .locale_model import LocaleLoader
from .proposal import validate_proposal
from .review import DEFAULT_REVIEW_BATCH_SIZE, create_review_index, review_index_summary
from .runtime import LuaRuntime
from .semantic_claims import DEFAULT_REGISTRY as DEFAULT_CLAIMS_REGISTRY, check_registry
from .translation_review import DEFAULT_TRANSLATION_CHARACTER_BUDGET
from .workset import create_workset
from .cli_common import _add_common_arguments, _manifest, _print_json


def register(subparsers: argparse._SubParsersAction) -> None:
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
    workset.set_defaults(handler=dispatch)
    context.set_defaults(handler=dispatch)
    review.set_defaults(handler=dispatch)
    proposal.set_defaults(handler=dispatch)
    claims.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "workset":
        return _workset(arguments)
    if arguments.command == "context":
        return _context(arguments)
    if arguments.command == "review":
        return _review(arguments)
    if arguments.command == "proposal":
        return _proposal(arguments)
    if arguments.command == "claims":
        if arguments.claims_command == "check":
            return _claims_check(arguments)
        raise AssertionError(f"unhandled claims command: {arguments.claims_command}")
    raise AssertionError(f"unhandled command: {arguments.command}")


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
