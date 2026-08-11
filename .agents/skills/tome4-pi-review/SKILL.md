---
name: tome4-pi-review
description: Run bounded, read-only Pi semantic discovery for ToME4 canonical translations, or legacy finding review for public repository code changes, visibly in a tmux pane. Do not use this Skill to send terminology, prior audit findings, Facts, or source trees into translation semantic discovery; do not use it for translation generation.
---

# ToME4 Pi review

Use the repository's contract-dispatched review pipeline. Translation semantic discovery is
v2; public code review remains legacy v1. Keep Pi isolated from tools, sessions, repository
context, and source trees. Interactive runs execute the Pi CLI in a
tmux split pane so the operator can watch the audit live; the wrapper applies the same
strict validation, caching and report writing as the headless tools.

Each Pi review or remediation invocation receives a maximum of 20 minutes (1200 seconds)
by default. Keep this per-bundle timeout unless the user explicitly requests a different
limit; do not silently shorten it for a large bundle.

## Prepare the review

1. Read the active `AGENTS.md`. For translation review, the main agent also reads
   `TERMINOLOGY.md` and `terminology.tsv`, but the blind semantic v2 bundle must not receive
   terminology rows or Facts; those are available only for later claim adjudication.
2. Select the smallest requested scope:
   - Translations: `python3 -B tools/i18n review --scope translations`
   - Public changes: `python3 -B tools/i18n review --scope code`
   - Both: `python3 -B tools/i18n review --scope translations --scope code`
3. Read the generated `review-index.json`, not source paths. Report each bundle's contract,
   channel, item count, `item_character_budget`, `item_character_count`, actual
   host `artifact_bytes`, actual outbound `payload_bytes`, and oversized-item marker before
   invoking Pi. Translation v2 sends only the minimal revision/source/target provider projection;
   its exact compact JSON is sent over stdin from fixed cwd `/private/tmp`, never through Pi
   `@file` expansion, and an explicit empty `--append-system-prompt` disables project/global
   `APPEND_SYSTEM.md` discovery. Mixed indexes legitimately contain translation v2 and code v1.

## Authorize external review

Pi sends each bounded bundle to the configured external provider. Translation v2 bundles are
covered by the project-level transfer authorization in `AGENTS.md` and do not require
per-invocation approval; before the first real invocation the main agent still reports the
provider, model, bundle kind/contract, item count, item character count and actual payload
bytes for the record. For any non-translation-v2 outbound content (tasks, plans, code or
other bundles), state the same details and obtain explicit user authorization before the
first real invocation.

Do not enable project-wide network access or bypass approvals. If an escalation is denied,
stop; do not invoke Pi indirectly or copy the data through another channel.

## Run Pi in a tmux pane

Invoke one validated bundle at a time (the tool defaults to the current tmux session):

```bash
tools/pi-tmux review --bundle <absolute-bundle-path>
```

The tool splits the current tmux session into a new pane, runs the isolated Pi CLI there
with output streamed live, waits for completion, and validates the result exactly like
`tools/pi-review`. A cache hit (exact validated result) skips the pane entirely.

Pane lifecycle and options:

- The pane stays open after the audit (default `--keep-pane`) so the operator can inspect
  it; the final summary prints `Pane: %N — close with: tmux kill-pane -t %N`.
- `--no-keep-pane` closes the pane when the worker exits.
- `--layout vertical|horizontal`, `--percent <n>`, and `--session <name>` control the split.
- Outside tmux, `--fallback foreground` runs headless (still streams output to the caller);
  without it the tool fails closed.
- Provider/model/thinking defaults are used unless the user requests overrides. For a large
  index, process a bounded batch, report progress, and continue only within the authorized
  scope. Use `--force` only for an explicitly requested fresh observation and never to
  bypass external-transfer authorization.

Remediation uses the same 20-minute per-bundle limit and pane behavior, but only for findings
that the main agent has independently confirmed and classified. Translation v2 assessments
contain pending observations and are intentionally rejected by the legacy remediation runner:

```bash
tools/pi-tmux remediate --bundle <absolute-bundle-path> --review <validated-review.json>
```

Translation worksets can also run visibly: `tools/pi-tmux translate --workset <workset.json>`.

## Report findings

Read only validated `review.json` and `pi-review.json` artifacts. For translation v2, report
item coverage, `context-insufficient`, observation count and manual-queue count; preserve
`bundle_id`, `revision_id`, evidence spans and `finding_id`. Every model observation remains
pending until the main agent verifies it; do not summarize it by severity. An empty semantic
assessment is not an overall clean result because the language-quality channel is separate.
For code v1 only, summarize the legacy findings by severity. Do not automatically apply
suggestions or modify canonical Lua/code.

Never give isolated Pi source paths, raw extraction logs, arbitrary workspace files,
credentials, or tools. Translation bundles may include canonical DLC translation entries;
that does not authorize source-tree access.
