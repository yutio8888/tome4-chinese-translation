"""Run bounded Pi audits inside a tmux pane so the operator can watch live.

The wrapper builds the exact same isolated Pi command as ``tools/pi-review``,
``tools/pi-remediate`` and ``tools/pi-subagent``, but executes it inside a
tmux split pane.  A small ``worker`` subprocess runs inside the pane, tees
Pi's stdout/stderr into the run directory (``raw-output.txt`` /
``pi-stderr.txt``) while mirroring both streams to the pane, and finally
writes ``worker-status.json``.  The wrapper waits for that status file and
then applies the same strict validation, caching and report writing as the
headless tools, so the two entry points stay interchangeable.

When tmux is unavailable the tool can fall back to a foreground run
(``--fallback foreground``) that still streams Pi's output to the caller.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
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
    MAX_WORKSET_ITEMS,
    _pi_environment,
    build_translation_command,
)
from .pi_remediate import (
    REMEDIATION_CONTRACT,
    _read_review,
    _validate_remediation,
    build_remediation_command,
)
from .pi_review import (
    _cached_review_path,
    _load_cached_review,
    _review_cache_key,
    _validate_findings,
    _write_cached_review,
    build_review_command,
)
from .proposal import decode_json_object, extract_event_stream_output, read_json_object, validate_proposal
from .report import create_run_directory, write_json
from .review import (
    DEFAULT_REVIEW_TIMEOUT,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    validate_review_bundle,
)
from .workset import proposal_template_for, validate_workset


JOB_SCHEMA_VERSION = 1
WORKER_STATUS_SCHEMA_VERSION = 1
WORKER_GRACE_SECONDS = 120


# ---------------------------------------------------------------------------
# tmux helpers
# ---------------------------------------------------------------------------


def _run_tmux(
    tmux: str, arguments: list[str], *, check: bool = True, timeout: float = 20.0
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            [tmux, *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise AgentError(f"cannot run tmux: {error}") from error
    if check and result.returncode != 0:
        raise AgentError(
            f"tmux command failed: tmux {' '.join(arguments)}: {result.stderr.strip()}"
        )
    return result


def resolve_session(tmux: str, requested: str | None) -> str:
    """Return the tmux session to split: an explicit one or the caller's own."""
    if requested:
        result = _run_tmux(tmux, ["has-session", "-t", requested], check=False)
        if result.returncode != 0:
            raise AgentError(f"tmux session does not exist: {requested}")
        return requested
    pane = os.environ.get("TMUX_PANE")
    if pane:
        result = _run_tmux(
            tmux, ["display-message", "-p", "-t", pane, "#{session_name}"], check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    result = _run_tmux(
        tmux, ["display-message", "-p", "#{session_name}"], check=False
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise AgentError(
            "cannot determine the tmux session; run inside tmux or pass --session"
        )
    return result.stdout.strip()


def split_pane(
    tmux: str,
    *,
    session: str,
    layout: str,
    percent: int,
    start_directory: Path,
    command: str,
    title: str,
) -> str:
    flag = "-h" if layout == "vertical" else "-v"
    result = _run_tmux(
        tmux,
        [
            "split-window",
            flag,
            "-p",
            str(percent),
            "-t",
            session,
            "-c",
            str(start_directory),
            "-P",
            "-F",
            "#{pane_id}",
            command,
        ],
    )
    pane_id = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
    if not pane_id.startswith("%"):
        raise AgentError(f"tmux split-window did not report a pane id: {pane_id!r}")
    _run_tmux(tmux, ["select-pane", "-t", pane_id, "-T", title], check=False)
    return pane_id


def pane_is_dead(tmux: str, pane_id: str) -> bool:
    result = _run_tmux(
        tmux,
        ["display-message", "-p", "-t", pane_id, "#{pane_dead}"],
        check=False,
    )
    if result.returncode != 0:
        return True
    return result.stdout.strip() == "1"


def kill_pane(tmux: str, pane_id: str) -> None:
    _run_tmux(tmux, ["kill-pane", "-t", pane_id], check=False)


def _worker_pid_is_alive(pid_path: Path) -> bool:
    try:
        pid = int(json.loads(pid_path.read_text(encoding="utf-8"))["pid"])
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _read_status(run_directory: Path) -> dict[str, Any]:
    path = run_directory / "worker-status.json"
    try:
        status = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AgentError(f"invalid worker status: {path}") from error
    if not isinstance(status, dict):
        raise AgentError("worker status must be an object")
    if status.get("schema_version") != WORKER_STATUS_SCHEMA_VERSION:
        raise AgentError("worker status has an unsupported schema")
    return status


def wait_for_worker(
    run_directory: Path,
    *,
    tmux: str | None,
    pane_id: str | None,
    wait_timeout: int,
) -> dict[str, Any]:
    """Wait for the worker's status file; also detect a killed pane."""
    status_path = run_directory / "worker-status.json"
    pid_path = run_directory / "worker.pid"
    started = time.monotonic()
    last_report = 0.0
    while time.monotonic() - started < wait_timeout:
        if status_path.exists():
            return _read_status(run_directory)
        if pid_path.exists() and not _worker_pid_is_alive(pid_path):
            raise AgentError(
                "the tmux worker terminated before reporting; the pane was likely interrupted"
            )
        if tmux is not None and pane_id is not None and pane_is_dead(tmux, pane_id):
            raise AgentError(
                f"the tmux pane {pane_id} terminated before the worker reported"
            )
        now = time.monotonic()
        if now - last_report >= 30:
            last_report = now
            elapsed = int(now - started)
            print(
                f"... waiting for Pi in tmux pane {pane_id} ({elapsed}s elapsed)",
                flush=True,
            )
        time.sleep(1)
    raise AgentError(
        f"timed out waiting for the tmux worker after {wait_timeout} seconds"
    )


# ---------------------------------------------------------------------------
# worker: runs inside the pane, tees Pi output and reports status
# ---------------------------------------------------------------------------


class PaneStreamRenderer:
    """Render the pi `--mode json` event stream like a normal terminal.

    Fragments are assembled into complete lines (flushed on newline),
    reasoning deltas are dimmed, status events become short cyan markers,
    and non-event lines pass through unchanged. The raw stream written to
    raw-output.txt is never styled and drops message_update events entirely
    (they carry the full accumulated partial and bloat the file by GBs).
    """

    _STATUS = ("agent_start", "agent_end", "turn_start", "turn_end")
    _MAX_LINE = 240

    def __init__(self, mirror: Any, use_color: bool) -> None:
        self.mirror = mirror
        self.use_color = use_color
        self.buffer = ""
        self.mode = "text"

    def _write(self, text: str) -> None:
        self.mirror.write(text.encode("utf-8"))
        self.mirror.flush()

    def _status(self, text: str) -> None:
        if self.use_color:
            self._write(f"\x1b[36m{text}\x1b[0m\n")
        else:
            self._write(text + "\n")

    def _emit_line(self, text: str) -> None:
        text = text.rstrip("\r")
        if not text:
            return
        if self.use_color and self.mode == "thinking":
            self._write(f"\x1b[2m{text}\x1b[0m\n")
        else:
            self._write(text + "\n")

    def _append(self, delta: str) -> None:
        self.buffer += delta
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            self._emit_line(line)
        if len(self.buffer) > self._MAX_LINE:
            self._emit_line(self.buffer[: self._MAX_LINE] + "…")
            self.buffer = ""

    def feed_line(self, line: bytes) -> None:
        try:
            event = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._write(line.decode("utf-8", errors="replace") + "\n")
            return
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            self._write(line.decode("utf-8", errors="replace") + "\n")
            return
        event_type = event["type"]
        if event_type == "message_update":
            assistant_event = event.get("assistantMessageEvent")
            if not isinstance(assistant_event, dict):
                return
            event_kind = assistant_event.get("type")
            if event_kind == "thinking_start":
                self.mode = "thinking"
            elif event_kind == "text_start":
                self.mode = "text"
            delta = assistant_event.get("delta")
            if isinstance(delta, str) and delta:
                self._append(delta)
            return
        if event_type in self._STATUS:
            self._status(f"[pi] {event_type}")
            return
        if event_type in ("message_start", "message_end"):
            message = event.get("message")
            role = message.get("role") if isinstance(message, dict) else "?"
            self._status(f"[pi] {event_type} role={role}")
            return

    def flush(self) -> None:
        if self.buffer:
            self._emit_line(self.buffer)
            self.buffer = ""


def _pump(stream: Any, path: Path, mirror: Any) -> None:
    """Write a raw stream to path while mirroring it unchanged."""
    try:
        with path.open("wb") as handle:
            for chunk in iter(lambda: stream.read(65536), b""):
                handle.write(chunk)
                handle.flush()
                mirror.write(chunk)
                mirror.flush()
    finally:
        stream.close()


def _is_message_update_line(line: bytes) -> bool:
    try:
        event = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return isinstance(event, dict) and event.get("type") == "message_update"


def _pump_with_preview(stream: Any, path: Path, mirror: Any) -> None:
    """Write the raw stream to path (minus message_update deltas) while
    mirroring a readable line-oriented preview to the pane/caller."""
    renderer = PaneStreamRenderer(mirror, use_color=bool(getattr(mirror, "isatty", lambda: False)()))
    pending = b""
    try:
        with path.open("wb") as handle:
            for chunk in iter(lambda: stream.read(65536), b""):
                pending += chunk
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    if not _is_message_update_line(line):
                        handle.write(line + b"\n")
                        handle.flush()
                    renderer.feed_line(line)
            if pending:
                if not _is_message_update_line(pending):
                    handle.write(pending + b"\n")
                    handle.flush()
                renderer.feed_line(pending)
    finally:
        renderer.flush()
        stream.close()


def run_worker_job(job: dict[str, Any], job_path: Path) -> dict[str, Any]:
    """Execute the job's Pi command, mirroring output to the pane/caller."""
    run_directory = job_path.parent
    raw_output_path = run_directory / "raw-output.txt"
    stderr_path = run_directory / "pi-stderr.txt"
    status_path = run_directory / "worker-status.json"
    write_json(run_directory / "worker.pid", {"pid": os.getpid()})
    argv = job.get("argv")
    if not isinstance(argv, list) or not argv or not all(
        isinstance(value, str) for value in argv
    ):
        raise AgentError("worker job has an invalid argv")
    root = Path(job["root"]).expanduser().resolve()
    provider = job.get("provider")
    timeout = job.get("timeout_seconds")
    if not isinstance(timeout, int) or timeout < 1:
        raise AgentError("worker job has an invalid timeout_seconds")
    started = time.monotonic()
    print(
        f"[pi-tmux] worker {os.getpid()} starting {argv[0]} "
        f"(provider={provider}, timeout={timeout}s)",
        flush=True,
    )
    environment = _pi_environment(root, provider)
    try:
        process = subprocess.Popen(
            argv,
            cwd=Path(job.get("cwd", run_directory)).expanduser().resolve(),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        status = {
            "schema_version": WORKER_STATUS_SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "pi_returncode": None,
            "timed_out": False,
            "error": f"cannot start Pi: {error}",
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "raw_output_sha256": None,
        }
        write_json(status_path, status)
        print(f"[pi-tmux] worker failed to start Pi: {error}", file=sys.stderr, flush=True)
        return status
    stdout_thread = threading.Thread(
        target=_pump_with_preview, args=(process.stdout, raw_output_path, sys.stdout.buffer)
    )
    stderr_thread = threading.Thread(
        target=_pump, args=(process.stderr, stderr_path, sys.stderr.buffer)
    )
    stdout_thread.start()
    stderr_thread.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    stdout_thread.join()
    stderr_thread.join()
    raw_sha = None
    if raw_output_path.exists():
        raw_sha = hashlib.sha256(raw_output_path.read_bytes()).hexdigest()
    status = {
        "schema_version": WORKER_STATUS_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "pi_returncode": process.returncode,
        "timed_out": timed_out,
        "error": f"Pi timed out after {timeout} seconds" if timed_out else None,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "raw_output_sha256": raw_sha,
    }
    write_json(status_path, status)
    if timed_out:
        print(f"[pi-tmux] worker: Pi timed out after {timeout}s", file=sys.stderr, flush=True)
    else:
        print(f"[pi-tmux] worker finished: pi_returncode={process.returncode}", flush=True)
    return status


def worker_main(job_path: Path) -> int:
    resolved = job_path.expanduser().resolve()
    try:
        job = json.loads(resolved.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot read worker job {resolved}: {error}", file=sys.stderr)
        return 125
    if not isinstance(job, dict) or job.get("job_schema_version") != JOB_SCHEMA_VERSION:
        print(f"ERROR: unsupported worker job: {resolved}", file=sys.stderr)
        return 125
    try:
        status = run_worker_job(job, resolved)
    except (AgentError, ValidationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 125
    if status.get("timed_out"):
        return 124
    if status.get("pi_returncode") is None:
        return 125
    return int(status["pi_returncode"])


# ---------------------------------------------------------------------------
# shared execution
# ---------------------------------------------------------------------------


def _pane_command(job_path: Path, keep_pane: bool) -> str:
    worker = (
        f"{shlex.quote(sys.executable)} -B "
        f"{shlex.quote(str(Path(__file__).resolve().parents[1] / 'pi-tmux'))} "
        f"worker --job {shlex.quote(str(job_path))}"
    )
    if keep_pane:
        # NB: zsh treats `status` as a read-only special variable, so the
        # exit code must be captured into a plain name like `rc`.
        return (
            f"{worker}; rc=$?; "
            f"printf '\\n[pi-tmux] worker exited with status %s; Ctrl-D or `exit` closes this pane.\\n' \"$rc\"; "
            f"exec \"${{SHELL:-/bin/sh}}\""
        )
    return worker


def execute_in_pane(
    *,
    run_directory: Path,
    title: str,
    job: dict[str, Any],
    timeout: int,
    tmux_executable: str | None,
    session: str | None,
    layout: str,
    percent: int,
    keep_pane: bool,
    fallback: str,
) -> tuple[dict[str, Any], str | None]:
    """Run the job's Pi command in a tmux pane (or foreground) and wait."""
    job_path = run_directory / "job.json"
    write_json(job_path, job)
    tmux = tmux_executable or shutil.which("tmux")
    pane_id: str | None = None
    if tmux and (session or os.environ.get("TMUX")):
        try:
            target_session = resolve_session(tmux, session)
            command = _pane_command(job_path, keep_pane)
            pane_id = split_pane(
                tmux,
                session=target_session,
                layout=layout,
                percent=percent,
                start_directory=run_directory,
                command=command,
                title=title,
            )
            print(
                f"Pi running in tmux pane {pane_id} (session '{target_session}', "
                f"{layout} split) — watch it there",
                flush=True,
            )
        except AgentError as error:
            if fallback != "foreground":
                raise
            print(f"tmux unavailable ({error}); falling back to foreground", file=sys.stderr)
            pane_id = None
    else:
        if fallback != "foreground":
            raise AgentError(
                "not running inside tmux; re-run inside tmux, pass --session, "
                "or use --fallback foreground"
            )
        print("tmux unavailable; running Pi in the foreground (no pane)", flush=True)
    if pane_id is None:
        status = run_worker_job(job, job_path)
    else:
        status = wait_for_worker(
            run_directory,
            tmux=tmux,
            pane_id=pane_id,
            wait_timeout=timeout + WORKER_GRACE_SECONDS,
        )
        if not keep_pane:
            kill_pane(tmux, pane_id)
    return status, pane_id


def _fail(report: dict[str, Any], report_path: Path, message: str) -> None:
    report["ok"] = False
    report["error"] = message
    report["elapsed_seconds"] = round(time.monotonic() - report["_started"], 6)
    write_json(report_path, report)


# ---------------------------------------------------------------------------
# review
# ---------------------------------------------------------------------------


def run_tmux_review(
    *,
    bundle_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    use_cache: bool,
    force: bool,
    pi_executable: str | None = None,
    tmux_executable: str | None = None,
    session: str | None = None,
    layout: str = "vertical",
    percent: int = 35,
    keep_pane: bool = True,
    fallback: str = "error",
) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_manifest()
    bundle_resolved = bundle_path.expanduser().resolve()
    bundle = validate_review_bundle(manifest, bundle_resolved)
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")

    run_directory = create_run_directory(manifest.root, "pi-review-tmux")
    run_directory.chmod(0o700)
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
        "execution": "cache" if cache_decision == "hit" else "tmux",
        "session": session,
        "pane": None,
        "keep_pane": keep_pane,
        "run_directory": str(run_directory),
        "raw_output": str(run_directory / "raw-output.txt"),
        "report": str(report_path),
        "_started": started,
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
                    "execution": "cache",
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
        _fail(report, report_path, "pi is not available on PATH")
        raise AgentError(f"pi is not available on PATH; report: {report_path}")
    _pi_environment(manifest.root, provider)  # fail fast on missing credentials
    command = build_review_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        bundle=bundle,
        bundle_resolved=bundle_resolved,
    )
    job = {
        "job_schema_version": JOB_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "kind": "review",
        "root": str(manifest.root),
        "provider": provider,
        "cwd": str(run_directory),
        "argv": command,
        "timeout_seconds": timeout,
    }
    report.update(
        {
            "attempts": 1,
            "charged_or_possible_transfers": 1,
        }
    )
    try:
        status, pane_id = execute_in_pane(
            run_directory=run_directory,
            title=f"pi-review:{bundle['bundle_id'][:12]}",
            job=job,
            timeout=timeout,
            tmux_executable=tmux_executable,
            session=session,
            layout=layout,
            percent=percent,
            keep_pane=keep_pane,
            fallback=fallback,
        )
    except AgentError as error:
        _fail(report, report_path, str(error))
        raise
    report["pane"] = pane_id
    if pane_id is None:
        report["execution"] = "foreground"
    stderr_path = run_directory / "pi-stderr.txt"
    if stderr_path.exists() and stderr_path.stat().st_size:
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = status.get("pi_returncode")
    report["raw_output_sha256"] = status.get("raw_output_sha256")
    raw = (run_directory / "raw-output.txt").read_bytes() if (run_directory / "raw-output.txt").exists() else b""
    if status.get("timed_out"):
        message = f"Pi timed out after {timeout} seconds"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    if status.get("pi_returncode") != 0:
        message = f"Pi exited with status {status.get('pi_returncode')}"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    if not raw.strip():
        _fail(report, report_path, "Pi returned an empty response")
        raise AgentError(f"Pi returned an empty response; report: {report_path}")
    try:
        model_output = decode_json_object(
            extract_event_stream_output(raw, "Pi review output"),
            "Pi review output",
        )
        summary, output = _validate_findings(bundle, model_output, strict=strict)
    except ValidationError as error:
        _fail(report, report_path, str(error))
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


# ---------------------------------------------------------------------------
# remediation
# ---------------------------------------------------------------------------


def run_tmux_remediation(
    *,
    bundle_path: Path,
    review_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    pi_executable: str | None = None,
    tmux_executable: str | None = None,
    session: str | None = None,
    layout: str = "vertical",
    percent: int = 35,
    keep_pane: bool = True,
    fallback: str = "error",
) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_manifest()
    bundle_resolved = bundle_path.expanduser().resolve()
    bundle = validate_review_bundle(manifest, bundle_resolved)
    review_resolved = review_path.expanduser().resolve()
    review = _read_review(review_resolved, bundle)
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")

    run_directory = create_run_directory(manifest.root, "pi-remediate-tmux")
    run_directory.chmod(0o700)
    remediation_path = run_directory / "remediation.json"
    report_path = run_directory / "pi-remediation.json"
    prompt_path = manifest.root / "i18n" / "prompts" / "pi-remediator.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi remediator prompt: {prompt_path}") from error
    report: dict[str, Any] = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "remediation_contract": REMEDIATION_CONTRACT,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "bundle": str(bundle_resolved),
        "bundle_id": bundle["bundle_id"],
        "review": str(review_resolved),
        "review_id": review["review_id"],
        "kind": bundle["kind"],
        "prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "timeout_seconds": timeout,
        "execution": "tmux",
        "session": session,
        "pane": None,
        "keep_pane": keep_pane,
        "run_directory": str(run_directory),
        "raw_output": str(run_directory / "raw-output.txt"),
        "report": str(report_path),
        "_started": started,
    }
    executable = pi_executable or shutil.which("pi")
    if not executable:
        _fail(report, report_path, "pi is not available on PATH")
        raise AgentError(f"pi is not available on PATH; report: {report_path}")
    _pi_environment(manifest.root, provider)  # fail fast on missing credentials
    command = build_remediation_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        bundle=bundle,
        bundle_resolved=bundle_resolved,
        review_resolved=review_resolved,
        review_id=review["review_id"],
    )
    job = {
        "job_schema_version": JOB_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "kind": "remediate",
        "root": str(manifest.root),
        "provider": provider,
        "cwd": str(run_directory),
        "argv": command,
        "timeout_seconds": timeout,
    }
    try:
        status, pane_id = execute_in_pane(
            run_directory=run_directory,
            title=f"pi-remediate:{bundle['bundle_id'][:12]}",
            job=job,
            timeout=timeout,
            tmux_executable=tmux_executable,
            session=session,
            layout=layout,
            percent=percent,
            keep_pane=keep_pane,
            fallback=fallback,
        )
    except AgentError as error:
        _fail(report, report_path, str(error))
        raise
    report["pane"] = pane_id
    if pane_id is None:
        report["execution"] = "foreground"
    stderr_path = run_directory / "pi-stderr.txt"
    if stderr_path.exists() and stderr_path.stat().st_size:
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = status.get("pi_returncode")
    report["raw_output_sha256"] = status.get("raw_output_sha256")
    raw = (run_directory / "raw-output.txt").read_bytes() if (run_directory / "raw-output.txt").exists() else b""
    if status.get("timed_out"):
        message = f"Pi timed out after {timeout} seconds"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    if status.get("pi_returncode") != 0:
        message = f"Pi exited with status {status.get('pi_returncode')}"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    try:
        output = decode_json_object(
            extract_event_stream_output(raw, "Pi remediation output"),
            "Pi remediation output",
        )
        summary = _validate_remediation(bundle, review, output)
    except ValidationError as error:
        _fail(report, report_path, str(error))
        raise AgentError(f"Pi remediation validation failed: {error}; report: {report_path}") from error
    output["remediation_id"] = hashlib.sha256(
        json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    write_json(remediation_path, output)
    report.update(
        {
            "ok": True,
            "summary": summary,
            "remediation": str(remediation_path),
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    )
    write_json(report_path, report)
    return report


# ---------------------------------------------------------------------------
# translation
# ---------------------------------------------------------------------------


def run_tmux_translation(
    *,
    workset_path: Path,
    provider: str,
    model: str,
    thinking: str,
    timeout: int,
    strict: bool,
    pi_executable: str | None = None,
    tmux_executable: str | None = None,
    session: str | None = None,
    layout: str = "vertical",
    percent: int = 35,
    keep_pane: bool = True,
    fallback: str = "error",
) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_manifest()
    workset_resolved, workset, _ = read_json_object(workset_path, "workset")
    validate_workset(manifest, workset)
    items = workset["items"]
    if len(items) > MAX_WORKSET_ITEMS:
        raise ValidationError(
            f"Pi worksets are limited to {MAX_WORKSET_ITEMS} items; split this workset"
        )
    if timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if not provider or not model or not thinking:
        raise ValidationError("Pi provider, model, and thinking level must be non-empty")

    template_value = proposal_template_for(workset)
    template_raw_path = workset.get("proposal_template")
    if not isinstance(template_raw_path, str):
        raise ValidationError("workset has no proposal_template path")
    template_path, on_disk_template, _ = read_json_object(
        Path(template_raw_path), "proposal template"
    )
    if on_disk_template != template_value:
        raise ValidationError("proposal template is stale or does not match the workset")

    prompt_path = manifest.root / "i18n" / "prompts" / "pi-translator.md"
    try:
        system_prompt = prompt_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise AgentError(f"cannot read Pi translator prompt: {prompt_path}") from error
    executable = pi_executable or shutil.which("pi")
    if not executable:
        raise AgentError("pi is not available on PATH")

    run_directory = create_run_directory(manifest.root, "pi-translate-tmux")
    run_directory.chmod(0o700)
    proposal_path = run_directory / "proposal.json"
    report_path = run_directory / "pi-translation.json"
    report: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "ok": False,
        "version": manifest.version,
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "strict": strict,
        "workset": str(workset_resolved),
        "workset_id": workset["workset_id"],
        "component": workset["component"],
        "items": len(items),
        "prompt": str(prompt_path),
        "prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
        "timeout_seconds": timeout,
        "execution": "tmux",
        "session": session,
        "pane": None,
        "keep_pane": keep_pane,
        "run_directory": str(run_directory),
        "raw_output": str(run_directory / "raw-output.txt"),
        "report": str(report_path),
        "_started": started,
    }
    _pi_environment(manifest.root, provider)  # fail fast on missing credentials
    command = build_translation_command(
        executable=executable,
        provider=provider,
        model=model,
        thinking=thinking,
        system_prompt=system_prompt,
        workset_resolved=workset_resolved,
        template_path=template_path,
    )
    job = {
        "job_schema_version": JOB_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "kind": "translate",
        "root": str(manifest.root),
        "provider": provider,
        "cwd": str(manifest.root),
        "argv": command,
        "timeout_seconds": timeout,
    }
    try:
        status, pane_id = execute_in_pane(
            run_directory=run_directory,
            title=f"pi-translate:{workset['workset_id'][:12]}",
            job=job,
            timeout=timeout,
            tmux_executable=tmux_executable,
            session=session,
            layout=layout,
            percent=percent,
            keep_pane=keep_pane,
            fallback=fallback,
        )
    except AgentError as error:
        _fail(report, report_path, str(error))
        raise
    report["pane"] = pane_id
    if pane_id is None:
        report["execution"] = "foreground"
    stderr_path = run_directory / "pi-stderr.txt"
    if stderr_path.exists() and stderr_path.stat().st_size:
        report["stderr"] = str(stderr_path)
    report["pi_returncode"] = status.get("pi_returncode")
    report["raw_output_sha256"] = status.get("raw_output_sha256")
    raw = (run_directory / "raw-output.txt").read_bytes() if (run_directory / "raw-output.txt").exists() else b""
    if status.get("timed_out"):
        message = f"Pi timed out after {timeout} seconds"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    if status.get("pi_returncode") != 0:
        message = f"Pi exited with status {status.get('pi_returncode')}"
        _fail(report, report_path, message)
        raise AgentError(f"{message}; report: {report_path}")
    if not raw.strip():
        _fail(report, report_path, "Pi returned an empty response")
        raise AgentError(f"Pi returned an empty response; report: {report_path}")
    try:
        output_value = decode_json_object(
            extract_event_stream_output(raw, "Pi output"),
            "Pi output",
        )
    except ValidationError as error:
        _fail(report, report_path, str(error))
        raise AgentError(f"{error}; Pi report: {report_path}") from error
    if set(output_value) == {"proposals"}:
        output_value = {
            "schema_version": 1,
            "workset_id": workset["workset_id"],
            "proposals": output_value["proposals"],
        }
        report["normalization"] = "added-deterministic-envelope"
    else:
        report["normalization"] = "none"
    write_json(proposal_path, output_value)
    report["proposal"] = str(proposal_path)
    try:
        validation = validate_proposal(
            manifest,
            workset_path=workset_resolved,
            proposal_path=proposal_path,
            allow_partial=False,
            strict=strict,
        )
    except I18nToolError as error:
        _fail(report, report_path, str(error))
        raise type(error)(f"{error}; Pi report: {report_path}") from error
    report["proposal_validation"] = validation["report"]
    report["proposal_id"] = validation["proposal_id"]
    report["errors"] = validation["errors"]
    report["warnings"] = validation["warnings"]
    if not validation["ok"]:
        _fail(
            report,
            report_path,
            f"proposal validation failed with {validation['errors']} errors and "
            f"{validation['warnings']} warnings",
        )
        raise ValidationError(f"Pi proposal failed validation; report: {report_path}")
    report["ok"] = True
    report["validated_proposal"] = validation["validated_proposal"]
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)
    write_json(report_path, report)
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _add_pi_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--provider", default=os.environ.get("TOME_PI_PROVIDER", DEFAULT_PROVIDER)
    )
    parser.add_argument("--model", default=os.environ.get("TOME_PI_MODEL", DEFAULT_MODEL))
    parser.add_argument(
        "--thinking", default=os.environ.get("TOME_PI_THINKING", DEFAULT_THINKING)
    )
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="reject malformed model output (default: true)",
    )
    parser.add_argument(
        "--pi",
        dest="pi_executable",
        default=None,
        help="Pi executable to run (default: pi on PATH)",
    )


def _add_tmux_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--session",
        default=None,
        help="tmux session to split (default: the caller's own session)",
    )
    parser.add_argument(
        "--layout",
        choices=("vertical", "horizontal"),
        default="vertical",
        help="vertical = side-by-side panes, horizontal = stacked (default: vertical)",
    )
    parser.add_argument(
        "--percent",
        type=int,
        default=35,
        help="size of the new pane as a percentage (default: 35)",
    )
    parser.add_argument(
        "--keep-pane",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="leave the pane open after the audit for inspection (default: true)",
    )
    parser.add_argument(
        "--fallback",
        choices=("error", "foreground"),
        default="error",
        help="behavior when tmux is unavailable (default: error)",
    )
    parser.add_argument(
        "--tmux",
        dest="tmux_executable",
        default=None,
        help="tmux executable to use (default: tmux on PATH)",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/pi-tmux",
        description="Run bounded Pi audits in a tmux pane so the operator can watch",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    review = subparsers.add_parser("review", help="review a bundle in a tmux pane")
    review.add_argument("--bundle", required=True, type=Path)
    review.add_argument("--timeout", type=int, default=DEFAULT_REVIEW_TIMEOUT)
    review.add_argument(
        "--cache",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="reuse an exact validated result before starting Pi (default: true)",
    )
    review.add_argument(
        "--force",
        action="store_true",
        help="bypass cache lookup and do not replace the cached observation",
    )
    _add_pi_options(review)
    _add_tmux_options(review)

    remediate = subparsers.add_parser(
        "remediate", help="produce remediation proposals in a tmux pane"
    )
    remediate.add_argument("--bundle", required=True, type=Path)
    remediate.add_argument("--review", required=True, type=Path)
    remediate.add_argument("--timeout", type=int, default=DEFAULT_REVIEW_TIMEOUT)
    _add_pi_options(remediate)
    _add_tmux_options(remediate)

    translate = subparsers.add_parser(
        "translate", help="translate a workset in a tmux pane"
    )
    translate.add_argument("--workset", required=True, type=Path)
    translate.add_argument("--timeout", type=int, default=900)
    _add_pi_options(translate)
    _add_tmux_options(translate)

    worker = subparsers.add_parser(
        "worker", help=argparse.SUPPRESS, description="internal pane worker"
    )
    worker.add_argument("--job", required=True, type=Path)
    return parser


def _pane_hint(report: dict[str, Any]) -> str | None:
    pane = report.get("pane")
    if not pane or not report.get("keep_pane"):
        return None
    return f"Pane: {pane} — close with: tmux kill-pane -t {pane}"


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    if arguments.command == "worker":
        return worker_main(arguments.job)
    try:
        if arguments.command == "review":
            report = run_tmux_review(
                bundle_path=arguments.bundle,
                provider=arguments.provider,
                model=arguments.model,
                thinking=arguments.thinking,
                timeout=arguments.timeout,
                strict=arguments.strict,
                use_cache=arguments.cache,
                force=arguments.force,
                pi_executable=arguments.pi_executable,
                tmux_executable=arguments.tmux_executable,
                session=arguments.session,
                layout=arguments.layout,
                percent=arguments.percent,
                keep_pane=arguments.keep_pane,
                fallback=arguments.fallback,
            )
        elif arguments.command == "remediate":
            report = run_tmux_remediation(
                bundle_path=arguments.bundle,
                review_path=arguments.review,
                provider=arguments.provider,
                model=arguments.model,
                thinking=arguments.thinking,
                timeout=arguments.timeout,
                strict=arguments.strict,
                pi_executable=arguments.pi_executable,
                tmux_executable=arguments.tmux_executable,
                session=arguments.session,
                layout=arguments.layout,
                percent=arguments.percent,
                keep_pane=arguments.keep_pane,
                fallback=arguments.fallback,
            )
        else:
            report = run_tmux_translation(
                workset_path=arguments.workset,
                provider=arguments.provider,
                model=arguments.model,
                thinking=arguments.thinking,
                timeout=arguments.timeout,
                strict=arguments.strict,
                pi_executable=arguments.pi_executable,
                tmux_executable=arguments.tmux_executable,
                session=arguments.session,
                layout=arguments.layout,
                percent=arguments.percent,
                keep_pane=arguments.keep_pane,
                fallback=arguments.fallback,
            )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    if arguments.command == "review":
        summary = report["summary"]
        print(
            f"OK  Pi review {report['bundle_id'][:16]}  "
            f"kind={report['kind']} findings={summary['findings']} "
            f"cache={report['cache_decision']} attempts={report['attempts']}"
        )
        print(f"Review: {report['review']}")
    elif arguments.command == "remediate":
        print(
            f"OK  Pi remediation {report['bundle_id'][:16]}  "
            f"proposals={report['summary']['proposals']}"
        )
        print(f"Remediation: {report['remediation']}")
    else:
        print(
            f"OK  Pi proposal {report['proposal_id'][:16]}  "
            f"items={report['items']} errors={report['errors']} warnings={report['warnings']}"
        )
        print(f"Validated: {report['validated_proposal']}")
    print(f"Report: {report['report']}")
    hint = _pane_hint(report)
    if hint:
        print(hint)
    return 0
