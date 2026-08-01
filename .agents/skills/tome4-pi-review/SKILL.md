---
name: tome4-pi-review
description: Run bounded, read-only Pi audits for ToME4 canonical translations or public repository changes. Use when the user asks Codex to call Pi for translation review, terminology review, code review, audit findings, review bundles, or an independent second pass; do not use for translation generation or protected DLC source inspection.
---

# ToME4 Pi review

Use the repository's validated review pipeline. Keep Pi isolated from tools, sessions,
repository context, and protected DLC sources.

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

Do not enable project-wide network access or bypass Codex approvals. If an escalation is
denied, stop; do not invoke Pi indirectly or copy the data through another channel.

## Run Pi

Invoke one validated bundle at a time:

```bash
tools/pi-review --bundle <absolute-bundle-path>
```

Use the provider/model/thinking defaults unless the user requests overrides. For a large
index, process a bounded batch, report progress, and continue only within the authorized
scope. Exact validated results are reused before Pi starts; use `--force` only for an
explicitly requested fresh observation and never to bypass external-transfer authorization.

The remediation command uses the same 20-minute per-bundle limit:

```bash
tools/pi-remediate --bundle <absolute-bundle-path> --review <validated-review.json>
```

## Report findings

Read only validated `review.json` and `pi-review.json` artifacts. Summarize findings by
severity, preserve `bundle_id` and `item_id`, and distinguish Pi claims from independently
verified facts. Do not automatically apply suggestions or modify canonical Lua/code.

Never give Pi protected DLC paths, raw protected extraction logs, arbitrary workspace files,
credentials, or tools. Translation bundles may include canonical DLC translation entries;
that does not authorize access to DLC source repositories.
