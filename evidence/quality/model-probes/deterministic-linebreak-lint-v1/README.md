# Deterministic Chinese hard-line-break candidate scan v1

Status: complete exploratory tool-development run. No model was called. The scanner rebuilds the 30,308-row canonical inventory at production translation commit `1666481409f4c0d63d66e84659f6b6145d8d25d0`, learns only corpus-level Han character and contiguous-bigram counts, and emits conservative candidates where a literal LF appears to split a cohesive Chinese bigram.

The rule was developed after R033 (`包\n裹`) was known and after exploratory inspection of this snapshot. It is therefore not an independent evaluation. `RULE-CONTRACT.json` records that disclosure and freezes the final exploratory rule. Every scanner output remains `CANDIDATE_NOT_GROUND_TRUTH`; `SOURCE-AUDIT.json` separately records the fixed-source decisions.

The canonical scan found 246 raw Han-LF-Han boundaries in 89 revisions and emitted five candidates. All five matched atoms were confirmed as format defects:

- `包\n裹` — the known R033 defect;
- `存\n在`;
- `获\n得` inside one list item;
- `使\n用`;
- `误\n解`.

The four findings after R033 are new to this scan. The `获得` item is intentionally retained: a blanket list exclusion would hide a literal word split. This result supports using the scanner as a review warning. It does not support a prevalence estimate, a confidence interval, an unbiased `5/5` precision claim, or an error-level CI gate. A future frozen snapshot or independent holdout must evaluate the unchanged rule.

Rebuild and verify:

```bash
node evidence/quality/model-probes/deterministic-linebreak-lint-v1/test-scanner.mjs
node evidence/quality/model-probes/deterministic-linebreak-lint-v1/verify.mjs --repo /path/to/source-repo
```
