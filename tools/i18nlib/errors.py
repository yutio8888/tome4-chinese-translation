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


class AgentError(I18nToolError):
    exit_code = 6
