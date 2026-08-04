"""Run a file-reading Pi reviewer against a bounded review bundle.

Same bounded bundle scope, findings contract and strict validation as
``tools/pi-review``, but the Pi subprocess is started with an explicit
``--tools read,bash`` allowlist instead of ``--no-tools``.  The model may
therefore verify evidence against public project, game and DLC sources;
``edit``/``write`` are never enabled, the working directory is the manifest
root so relative source paths resolve, and the run stays ephemeral
(``--no-session --no-approve --no-context-files --no-skills``).

The output contract, cache identity and report shape deliberately match the
isolated pipeline so the same artifact consumers work unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .config import load_manifest
from .errors import AgentError, I18nToolError, ValidationError
from .pi_agent import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_THINKING,
    _pi_environment,
)
from .pi_review import (
    _canonical_sha256,
    _cached_review_path,
    _load_cached_review,
    _validate_findings,
    _write_cached_review,
)
from .proposal import decode_json_object, extract_event_stream_output
from .report import atomic_write_bytes, create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_TIMEOUT,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    validate_review_bundle,
)

TOOLS_ALLOWLIST = "read,bash"


def _run_git_snapshot_command(root: Path, arguments: list[str], label: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            cwd=root,
            env={key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise AgentError(f"cannot inspect worktree {label}: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise AgentError(f"cannot inspect worktree {label}: {detail or 'git failed'}")
    return result.stdout


def _git_worktree_snapshot(root: Path) -> bytes:
    """Hash tracked and non-ignored untracked state, including a dirty baseline."""
    status = _run_git_snapshot_command(
        root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"], "status"
    )
    head = _run_git_snapshot_command(root, ["rev-parse", "--verify", "HEAD"], "HEAD")
    tracked_diff = _run_git_snapshot_command(
        root, ["diff", "--binary", "--no-ext-diff", "HEAD", "--"], "tracked diff"
    )
    untracked = _run_git_snapshot_command(
        root, ["ls-files", "--others", "--exclude-standard", "-z"], "untracked files"
    )
    digest = hashlib.sha256()
    for label, value in (
        (b"status", status),
        (b"head", head),
        (b"tracked-diff", tracked_diff),
        (b"untracked", untracked),
    ):
        digest.update(label + b"\0" + len(value).to_bytes(8, "big") + value)
    for raw_path in sorted(path for path in untracked.split(b"\0") if path):
        relative = Path(os.fsdecode(raw_path))
        if relative.is_absolute() or ".." in relative.parts:
            raise AgentError(f"unsafe untracked path while snapshotting worktree: {relative}")
        path = root / relative
        digest.update(b"path\0" + raw_path + b"\0")
        try:
            if path.is_symlink():
                digest.update(b"symlink\0" + os.fsencode(os.readlink(path)))
            elif path.is_file():
                file_digest = hashlib.sha256()
                with path.open("rb") as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b""):
                        file_digest.update(block)
                digest.update(b"file\0" + file_digest.digest())
            else:
                digest.update(b"other\0")
        except OSError as error:
            raise AgentError(f"cannot hash untracked worktree path {relative}: {error}") from error
    git_directory_raw = _run_git_snapshot_command(
        root, ["rev-parse", "--git-dir"], "git directory"
    ).decode("utf-8", errors="strict").strip()
    git_directory = Path(git_directory_raw)
    if not git_directory.is_absolute():
        git_directory = root / git_directory
    exclude_path = git_directory / "info" / "exclude"
    try:
        exclude = exclude_path.read_bytes() if exclude_path.exists() else b""
    except OSError as error:
        raise AgentError(f"cannot hash git exclude file: {error}") from error
    digest.update(b"git-info-exclude\0" + hashlib.sha256(exclude).digest())
    return digest.digest()


def _record_worktree_check(report: dict[str, Any], before: bytes, after: bytes) -> bool:
    unchanged = before == after
    report.update(
        {
            "versioned_worktree_snapshot_before_sha256": before.hex(),
            "versioned_worktree_snapshot_after_sha256": after.hex(),
            "versioned_worktree_unchanged": unchanged,
            "worktree_check_scope": "tracked-and-nonignored-untracked",
            "ignored_paths_checked": False,
            "git_metadata_checked": ["info/exclude"],
        }
    )
    return unchanged


def _kill_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _is_message_update_line(line: bytes) -> bool:
    try:
        event = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return isinstance(event, dict) and event.get("type") == "message_update"


def _pump_file_review_stream(
    source: Any, output_path: Path, *, filter_message_updates: bool
) -> None:
    with output_path.open("wb") as output:
        for line in iter(source.readline, b""):
            if filter_message_updates and _is_message_update_line(line):
                continue
            output.write(line)
            output.flush()


def _run_file_review_process(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int,
    raw_output_path: Path,
    stderr_path: Path,
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    assert process.stdout is not None and process.stderr is not None
    stdout_thread = threading.Thread(
        target=_pump_file_review_stream,
        args=(process.stdout, raw_output_path),
        kwargs={"filter_message_updates": True},
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=_pump_file_review_stream,
        args=(process.stderr, stderr_path),
        kwargs={"filter_message_updates": False},
        daemon=True,
    )
    stdout_thread.start()
    stderr_thread.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
    # Also clean up same-group descendants after a normal Pi exit.  A process
    # that deliberately creates a new session remains outside this boundary.
    _kill_process_group(process)
    if process.poll() is None:
        process.wait()
    stdout_thread.join(timeout=5)
    stderr_thread.join(timeout=5)
    if stdout_thread.is_alive() or stderr_thread.is_alive():
        process.stdout.close()
        process.stderr.close()
        stdout_thread.join(timeout=1)
        stderr_thread.join(timeout=1)
    process.stdout.close()
    process.stderr.close()
    if stdout_thread.is_alive() or stderr_thread.is_alive():
        raise OSError("Pi stream readers did not terminate after process-group cleanup")
    stdout = raw_output_path.read_bytes() if raw_output_path.exists() else b""
    stderr = stderr_path.read_bytes() if stderr_path.exists() else b""
    if timed_out:
        raise subprocess.TimeoutExpired(command, timeout, output=stdout, stderr=stderr)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def _file_review_cache_key(
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
            "cache_contract": "tome4-pi-file-review-cache-v1",
            "tool_version": TOOL_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle_id,
            "provider": provider,
            "model": model,
            "thinking": thinking,
            "prompt_sha256": prompt_sha256,
            "tools": TOOLS_ALLOWLIST,
            "strict": strict,
        }
    )


def build_file_review_command(
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
        "--tools",
        TOOLS_ALLOWLIST,
        "--system-prompt",
        system_prompt,
        "--print",
        f"@{bundle_resolved}",
        (
            "Review only this bundle and return the required JSON object. Do not omit the envelope. "
            "You may read project, game and DLC source files to verify evidence, but must never "
            "modify anything. The exact allowed item_id inventory for this bundle is "
            f"{json.dumps(inventory, ensure_ascii=False)}; copy item_id values verbatim, never use paths."
        ),
    ]


def run_pi_file_review(
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

    run_directory = create_run_directory(manifest.root, "pi-file-review")
    run_directory.chmod(0o700)
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    review_path = run_directory / "review.json"
    report_path = run_directory / "pi-review.json"
    prompt_path = manifest.root / "i18n" / "prompts" / "pi-reviewer-files.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi file reviewer prompt: {prompt_path}") from error

    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    cache_key = _file_review_cache_key(
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
        "mode": "findings-files-v1",
        "pi_tools": True,
        "tools": [TOOLS_ALLOWLIST],
        "os_sandbox": False,
        "provider_credentials_inherited": True,
        "process_group_cleanup": True,
        "detached_descendants_checked": False,
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
            report["error"] = f"Pi file review cache validation failed: {error}"
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
    command = build_file_review_command(
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
    worktree_before = _git_worktree_snapshot(manifest.root)
    try:
        result = _run_file_review_process(
            command,
            cwd=manifest.root,
            env=_pi_environment(manifest.root, provider),
            timeout=timeout,
            raw_output_path=raw_output_path,
            stderr_path=stderr_path,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        atomic_write_bytes(raw_output_path, stdout)
        atomic_write_bytes(stderr_path, stderr)
        report["stderr"] = str(stderr_path)
        report["raw_output_sha256"] = hashlib.sha256(stdout).hexdigest()
        unchanged = _record_worktree_check(
            report, worktree_before, _git_worktree_snapshot(manifest.root)
        )
        report["error"] = (
            f"Pi timed out after {timeout} seconds"
            if unchanged
            else "Pi file review changed the worktree before timing out"
        )
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}")
    except OSError as error:
        unchanged = _record_worktree_check(
            report, worktree_before, _git_worktree_snapshot(manifest.root)
        )
        report["error"] = (
            f"cannot start Pi: {error}"
            if unchanged
            else "Pi file review changed the worktree while starting"
        )
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}") from error

    atomic_write_bytes(raw_output_path, result.stdout)
    if result.stderr:
        atomic_write_bytes(stderr_path, result.stderr)
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = result.returncode
    report["raw_output_sha256"] = hashlib.sha256(result.stdout).hexdigest()
    if not _record_worktree_check(
        report, worktree_before, _git_worktree_snapshot(manifest.root)
    ):
        report["error"] = "Pi file review changed the worktree"
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"{report['error']}; report: {report_path}")
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
                result.stdout, "Pi file review output"
            ),
            "Pi file review output",
        )
        summary, output = _validate_findings(bundle, model_output, strict=strict)
    except ValidationError as error:
        report["error"] = str(error)
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        write_json(report_path, report)
        raise AgentError(f"Pi file review validation failed: {error}; report: {report_path}") from error

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
        prog="tools/pi-review-files",
        description="Run a file-reading Pi reviewer (read/bash only) against a bounded review bundle",
    )
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument(
        "--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER)
    )
    parser.add_argument(
        "--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL)
    )
    parser.add_argument(
        "--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING)
    )
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
        report = run_pi_file_review(
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
        f"OK  Pi file review {report['bundle_id'][:16]}  "
        f"kind={report['kind']} findings={summary['findings']} "
        f"cache={report['cache_decision']} attempts={report['attempts']}"
    )
    print(f"Review: {report['review']}")
    print(f"Report: {report['report']}")
    return 0
