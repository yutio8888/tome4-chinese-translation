# Frozen subagent task

Perform a fresh, read-only methodological re-review.

Read exactly these three substantive inputs in the shared workspace and no other project files:

1. `tome4-agent-eval/evidence/quality/model-probes/next-research-plan-gpt-rereview-v2/PLAN-UNDER-REVIEW.md`
2. `tome4-agent-eval/evidence/quality/model-probes/next-research-plan-gpt-rereview-v2/REVIEW-PROMPT.md`
3. `tome4-agent-eval/evidence/quality/model-probes/next-research-plan-gpt-rereview-v2/REVIEW-SCHEMA.json`

Do not inspect the prior review, synthesis, result, Git history, AGENTS files, source samples or any other repository content. Do not use the network. Do not edit files. Return exactly one strict JSON object conforming to `REVIEW-SCHEMA.json`, without a Markdown fence or commentary.
