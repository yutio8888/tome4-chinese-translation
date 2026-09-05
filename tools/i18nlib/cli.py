"""Compose the localization CLI and dispatch errors."""

from __future__ import annotations

import argparse
import sys

from . import TOOL_VERSION
from . import (
    cli_doctor,
    cli_identity,
    cli_lint,
    cli_localization,
    cli_production,
    cli_quality,
    cli_review,
    production_review,
)
from .cli_common import _inject_public_dlc_env
from .errors import I18nToolError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/i18n",
        description="ToME4 Chinese localization toolchain",
    )
    parser.add_argument("--tool-version", action="version", version=TOOL_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)
    cli_doctor.register(subparsers)
    cli_localization.register(subparsers)
    cli_identity.register(subparsers)
    cli_lint.register(subparsers)
    cli_review.register(subparsers)
    cli_quality.register(subparsers)
    cli_production.register(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    _inject_public_dlc_env()
    arguments = _parser().parse_args(argv)
    try:
        return arguments.handler(arguments)
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    except (
        production_review.ProductionReviewError,
        production_review.ledger.LedgerError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
