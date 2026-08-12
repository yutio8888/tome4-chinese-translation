"""Typed command failures and stable exit codes."""

from __future__ import annotations


class I18nToolError(RuntimeError):
    exit_code = 1


class ConfigurationError(I18nToolError):
    exit_code = 2


class RuntimeCheckError(I18nToolError):
    exit_code = 3


class ExtractionError(I18nToolError):
    exit_code = 4


class ValidationError(I18nToolError):
    exit_code = 5


class IncrementalCheckError(I18nToolError):
    """Incremental self-check mismatch (contract §11 exit code 2)."""

    exit_code = 2


class ContractError(I18nToolError):
    """Contract violation or missing registry (contract §11 exit code 3)."""

    exit_code = 3


class AgentError(I18nToolError):
    exit_code = 6
