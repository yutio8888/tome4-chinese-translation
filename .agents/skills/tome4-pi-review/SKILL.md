---
name: tome4-pi-review
description: Run bounded, read-only Pi audits for ToME4 canonical translations or public repository changes, visibly in a tmux pane. Use when running a Pi review pass (translation, terminology, code, audit findings, independent second pass) from Pi or Codex as the main agent; do not use for translation generation or protected DLC source inspection.
---

# ToME4 Pi review

Use the repository's validated review pipeline. Keep Pi isolated from tools, sessions,
repository context, and protected DLC sources. Interactive runs execute the Pi CLI in a
tmux split pane so the operator can watch the audit live; the wrapper applies the same
strict validation, caching and report writing as the headless tools.

Each Pi review or remediation invocation receives a maximum of 20 minutes (1200 seconds)
by default. Keep this per-bundle timeout unless the user explicitly requests a different
limit; do not silently shorten it for a large bundle.

## Prepare the review

1. Read the active `AGENTS.md`. For translation review, also read `TERMINOLOGY.md`
   and `terminology.tsv` before generating bundles.
2. Select the smallest requested scope:
   - Translations: `python3 -B tools/i18n review --scope translations`
   - Public changes: `python3 -B tools/i18n review --scope code`
   - Both: `python3 -B tools/i18n review --scope translations --scope code`
3. Read the generated `review-index.json`, not protected source paths. Report the bundle
   count and scope before invoking Pi.

## Authorize external review

Pi sends each bounded bundle to the configured external provider. Before the first real
invocation, state the provider, model, bundle kind, item count, and that the bundle contents
will leave the local sandbox. Obtain explicit user authorization for that data transfer.

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

Remediation uses the same 20-minute per-bundle limit and the same pane behavior:

```bash
tools/pi-tmux remediate --bundle <absolute-bundle-path> --review <validated-review.json>
```

Translation worksets can also run visibly: `tools/pi-tmux translate --workset <workset.json>`.

## Report findings

Read only validated `review.json` and `pi-review.json` artifacts (they are identical in
shape to the headless pipeline's). Summarize findings by severity, preserve `bundle_id`
and `item_id`, and distinguish Pi claims from independently verified facts. Do not
automatically apply suggestions or modify canonical Lua/code.

Never give Pi protected DLC paths, raw protected extraction logs, arbitrary workspace files,
credentials, or tools. Translation bundles may include canonical DLC translation entries;
that does not authorize access to DLC source repositories.
