# Claude Opus route-purity qualification v1

This package is an independent route-qualification probe. It contains only three fixed integers and does not include translation records, real experimental samples, sealed references, adjudication, defect identifiers, provenance, credentials or host-local paths.

The qualification question is narrow: under Claude Code `2.1.247`, can the exact frozen `claude-opus-5` command produce one correct synthetic structured response while its own stream telemetry proves that only Opus message iterations were used and that no advisor, fallback, prompt suggestion, subagent, MCP, parent tool or server tool participated?

Current status is `READY_FOR_PRIMARY_LEAD_PREFLIGHT`. No model call has been made by this package.

## Frozen workflow

1. Run the local parser fixture gate: `node test-parser.mjs`.
2. Commit every file in this directory, including `FROZEN-HASHES.json`.
3. The primary lead runs `node preflight.mjs --write`. Preflight checks the frozen Claude Code `2.1.247` and bubblewrap `0.11.1` versions, six required environment controls, frozen hashes, outbound sanitization, fixtures, Git commit/blob lineage and the executor fixture baseline. It also performs only four no-model sandbox checks: CLI version, authentication status, full host-HOME masking and private-runtime writability.
4. Inspect and commit the immutable `PREFLIGHT.json`. The runner rejects a preflight that is not committed unchanged at the current `HEAD`, whose frozen package commit is not an ancestor of `HEAD`, or whose frozen blobs changed along that lineage.
5. Only if the committed immutable `PREFLIGHT.json` says `GO`, run `node run.mjs --attempt 1`.
6. The runner creates a new attempt directory and writes only `RAW.stdout`, `RAW.stderr` and `CALL.json` with exclusive-create semantics.
7. Run `node parse.mjs --attempt 1` separately. It writes `CANDIDATE.json` once and never alters the raw envelope or call record.

Failed transport attempts and invalid purity candidates remain evidence. A retry must use a new positive attempt number. Existing attempt directories and artifacts are never overwritten.

## Fail-closed interpretation

`QUALIFIED_OPUS_ONLY` requires all frozen conditions simultaneously. The parser accepts only a known event topology: one init first, optional known rate-limit/thinking telemetry, a contiguous set of fully formed Opus assistant messages, one direct receipt, and one success result last. Any unknown event or content-block type fails. Every known event and route-critical nested object has a frozen allowed-key set, including init, rate-limit, assistant/message/usage/content, receipt, result/usage/iteration, model usage and cache telemetry. Unknown telemetry is invalid. Init must report the observed first-party OAuth `apiKeySource` value `none`.

Global recursive counting must find exactly one `tool_use` and one `tool_result`, both at the prescribed direct locations; the structured caller must explicitly be `{ "type": "direct" }`. Keys and type values are normalized across case, snake/camel spelling and punctuation. Every model, canonical-model or provider alias anywhere in the envelope must carry the expected exact value. Prompt-suggestion, parent-tool aliases, subagent IDs, and tool/MCP/computer/web-search or fetch suffix families are invalid. Assistant-message usage cannot contain server-tool telemetry.

`modelUsage` must be a non-null Opus-only object with canonical model, `firstParty` provider, zero search requests and nonzero, internally consistent token telemetry. Every iteration must be a message, must identify Opus/first-party if those optional fields are emitted, and its required token counters must sum exactly to terminal usage and `modelUsage`. Init `skills` and `plugins` must both be empty. Receipt, terminal, subagent and server-tool telemetry use exact fail-closed structures. Missing telemetry, an unknown field in the strict counter structures, a prompt suggestion, advisor/fallback signal, non-null parent tool-use ID, MCP server or any other global tool signal is `INVALID_ROUTE_PURITY`.

The process does not inherit credential environment variables or expose the host HOME. Bubblewrap masks the entire host HOME with a tmpfs, exposes the synthetic bundle read-only, and binds one private `0700` ephemeral runtime. Exactly one ordinary host credential file with `0600` permissions is copied into that runtime's writable `CLAUDE_CONFIG_DIR`, permitting OAuth refresh without exposing settings, histories, projects, plugins or other HOME content. The runtime is deleted after every smoke or call. If this minimal credential source, its permissions, the sandbox smoke, or cleanup contract cannot be verified, preflight is `NO_GO`.

Before `CANDIDATE.json` can be created, the parser verifies ordinary non-symlink `CALL`, `PREFLIGHT`, frozen-manifest and RAW files; exact CALL fields; package-commit/blob/HEAD lineage; request/input/prompt/schema/frozen/preflight/binary hashes; displayed argument contract; and both RAW hashes.

Outbound bytes are limited to `PROMPT.md`, the provider-neutral `INPUT.json`, and `SCHEMA.json`. For this package, the local scanner is a fixture gate that verifies those exact frozen outbound bytes and its explicit regression cases; it is not a general-purpose security filter. It rejects credential shapes, Unix absolute paths, Windows drive-root paths, bare numeric experiment IDs such as `R033` or `P005`, real experiment identifiers, and model/provider provenance in this frozen payload. URI-scheme URLs such as the HTTPS JSON Schema identifier are excluded only from path matching and remain allowed.

A passing result qualifies only the exact route contract for prospective use. It does not score model quality, compare providers, or retroactively turn the earlier mixed Opus/Haiku envelope into a pure Opus result.
